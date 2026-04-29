"""Benchmark harness for Lab 2 multiprocessing experiments.

Re-implements the `simulate()` loop from the three course-provided scripts
(tvb_par, tvb_par_sm, tvb_par_sm_imp) and from tvb_seq_mlp, but with the
chunk size and dataset chosen at the command line. Originals are kept
untouched so they still match what the assignment refers to.

Usage:
    python3 bench.py par      <dataset> <tf> <chunk> [repeats]
    python3 bench.py par_sm   <dataset> <tf> <chunk> [repeats]
    python3 bench.py par_smi  <dataset> <tf> <chunk> [repeats]
    python3 bench.py seq_mlp  <dataset> <tf>         [repeats]
    python3 bench.py thr      <dataset> <tf> <chunk> [repeats]

Output: one JSON line per run on stdout, suitable for tee + jq.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import shared_memory

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import data  # noqa: E402

# Import the worker bodies from the course-provided scripts unchanged.
import tvb_par  # noqa: E402
import tvb_par_sm  # noqa: E402
import tvb_par_sm_imp  # noqa: E402
import tvb_seq_mlp  # noqa: E402


def load(dataset: str):
    if dataset == "tvb76":
        return data.tvb76_weights_lengths()
    if dataset == "tvb192":
        return data.tvb192_weights_lengths()
    if dataset == "tvb998":
        return data.tvb998_weights_lengths()
    raise SystemExit(f"unknown dataset {dataset}")


def run_seq_mlp(W, D, tf: float, dt: float = 0.05, speed: float = 4.0):
    # Keep the same dtype as the assignment script: pure Python lists.
    W_l = W.tolist()
    D_l = D.tolist()
    N = len(W_l)
    M = 2
    t0 = time.time()
    tvb_seq_mlp.simulate(W_l, D_l, N, M, dt, tf, speed, sparse_flag=False)
    return time.time() - t0


def run_par(W, D, tf: float, chunk: int, dt: float = 0.05, speed: float = 4.0):
    # Re-implementation of tvb_par.simulate() that parameterises chunk size.
    W_l = W.tolist()
    D_l = D.tolist()
    N = len(W_l)
    M = 2
    total = int(tf / dt)
    Xs = [[[0.0] * total for _ in range(M)] for _ in range(N)]
    D_ts = [[int((D_l[i][j] / speed) / dt) for i in range(N)] for j in range(N)]
    for n in range(N):
        for m in range(M):
            Xs[n][m][0] = -1.0

    t0 = time.time()
    with ProcessPoolExecutor() as ex:
        for t in range(1, total):
            res = list(
                ex.map(
                    tvb_par.center_task,
                    [Xs] * N, W_l, D_ts, [t] * N, range(N), [dt] * N,
                    chunksize=chunk,
                )
            )
            for n in range(N):
                for m in range(M):
                    Xs[n][m][t] = res[n][m]
    return time.time() - t0


def run_par_sm(W, D, tf: float, chunk: int, dt: float = 0.05, speed: float = 4.0):
    N = W.shape[0]
    M = 2
    total = int(tf / dt)
    Xs = np.zeros((N, M, total))
    D_ts = ((D / speed) / dt).astype(int)

    Xs_shm = shared_memory.SharedMemory(create=True, size=Xs.nbytes)
    W_shm = shared_memory.SharedMemory(create=True, size=W.nbytes)
    D_shm = shared_memory.SharedMemory(create=True, size=D_ts.nbytes)
    try:
        Xs_s = np.ndarray(Xs.shape, dtype=Xs.dtype, buffer=Xs_shm.buf)
        W_s = np.ndarray(W.shape, dtype=W.dtype, buffer=W_shm.buf)
        D_s = np.ndarray(D_ts.shape, dtype=D_ts.dtype, buffer=D_shm.buf)
        np.copyto(Xs_s, Xs); np.copyto(W_s, W); np.copyto(D_s, D_ts)
        Xs_s[:, :, 0] = -1.0

        t0 = time.time()
        with ProcessPoolExecutor() as ex:
            for t in range(1, total):
                res = list(
                    ex.map(
                        tvb_par_sm.center_task,
                        [Xs_shm.name] * N, [Xs_s.shape] * N, [Xs_s.dtype] * N,
                        [W_shm.name] * N, [W_s.shape] * N, [W_s.dtype] * N,
                        [D_shm.name] * N, [D_s.shape] * N, [D_s.dtype] * N,
                        [t] * N, range(N), [dt] * N,
                        chunksize=chunk,
                    )
                )
                for n in range(N):
                    for m in range(M):
                        Xs_s[n, m, t] = res[n][m]
        elapsed = time.time() - t0
    finally:
        for shm in (Xs_shm, W_shm, D_shm):
            shm.close(); shm.unlink()
    return elapsed


def run_par_smi(W, D, tf: float, chunk: int, dt: float = 0.05, speed: float = 4.0):
    N = W.shape[0]
    M = 2
    total = int(tf / dt)
    Xs = np.zeros((N, M, total))
    D_ts = ((D / speed) / dt).astype(int)

    Xs_shm = shared_memory.SharedMemory(create=True, size=Xs.nbytes)
    W_shm = shared_memory.SharedMemory(create=True, size=W.nbytes)
    D_shm = shared_memory.SharedMemory(create=True, size=D_ts.nbytes)
    try:
        Xs_a = np.ndarray(Xs.shape, dtype=Xs.dtype, buffer=Xs_shm.buf)
        W_a = np.ndarray(W.shape, dtype=W.dtype, buffer=W_shm.buf)
        D_a = np.ndarray(D_ts.shape, dtype=D_ts.dtype, buffer=D_shm.buf)
        np.copyto(Xs_a, Xs); np.copyto(W_a, W); np.copyto(D_a, D_ts)
        Xs_a[:, :, 0] = -1.0

        t0 = time.time()
        with ProcessPoolExecutor(
            initializer=tvb_par_sm_imp.init_worker,
            initargs=(
                Xs_shm.name, Xs_a.shape, Xs_a.dtype,
                W_shm.name, W_a.shape, W_a.dtype,
                D_shm.name, D_a.shape, D_a.dtype,
            ),
        ) as ex:
            for t in range(1, total):
                res = list(
                    ex.map(
                        tvb_par_sm_imp.center_task,
                        [t] * N, range(N), [dt] * N,
                        chunksize=chunk,
                    )
                )
                for n in range(N):
                    for m in range(M):
                        Xs_a[n, m, t] = res[n][m]
        elapsed = time.time() - t0
    finally:
        for shm in (Xs_shm, W_shm, D_shm):
            shm.close(); shm.unlink()
    return elapsed


def run_thr(W, D, tf: float, chunk: int, dt: float = 0.05, speed: float = 4.0):
    # Same body as run_par but with a thread pool. center_task from tvb_par
    # is pure-Python and uses lists, so it is GIL-bound.
    W_l = W.tolist()
    D_l = D.tolist()
    N = len(W_l)
    M = 2
    total = int(tf / dt)
    Xs = [[[0.0] * total for _ in range(M)] for _ in range(N)]
    D_ts = [[int((D_l[i][j] / speed) / dt) for i in range(N)] for j in range(N)]
    for n in range(N):
        for m in range(M):
            Xs[n][m][0] = -1.0

    t0 = time.time()
    with ThreadPoolExecutor() as ex:
        for t in range(1, total):
            res = list(
                ex.map(
                    tvb_par.center_task,
                    [Xs] * N, W_l, D_ts, [t] * N, range(N), [dt] * N,
                    chunksize=chunk,
                )
            )
            for n in range(N):
                for m in range(M):
                    Xs[n][m][t] = res[n][m]
    return time.time() - t0


RUNNERS = {
    "seq_mlp": run_seq_mlp,
    "par": run_par,
    "par_sm": run_par_sm,
    "par_smi": run_par_smi,
    "thr": run_thr,
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=list(RUNNERS))
    p.add_argument("dataset")
    p.add_argument("tf", type=float)
    p.add_argument("chunk", nargs="?", type=int, default=None)
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--tag", default="")
    args = p.parse_args()

    W, D = load(args.dataset)
    needs_chunk = args.mode != "seq_mlp"
    if needs_chunk and args.chunk is None:
        raise SystemExit("chunk required for this mode")

    runner = RUNNERS[args.mode]
    times = []
    for r in range(args.repeats):
        if needs_chunk:
            t = runner(W, D, args.tf, args.chunk)
        else:
            t = runner(W, D, args.tf)
        times.append(t)
        rec = {
            "mode": args.mode, "dataset": args.dataset, "tf": args.tf,
            "chunk": args.chunk, "rep": r, "time_s": t, "tag": args.tag,
        }
        print(json.dumps(rec), flush=True)

    summary = {
        "mode": args.mode, "dataset": args.dataset, "tf": args.tf,
        "chunk": args.chunk, "repeats": args.repeats,
        "min_s": min(times), "mean_s": sum(times) / len(times),
        "summary": True, "tag": args.tag,
    }
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
