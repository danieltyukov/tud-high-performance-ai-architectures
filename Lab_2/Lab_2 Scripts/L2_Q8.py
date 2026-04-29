"""Lab 2 — Exercise 2.8.

Multithreaded port of tvb_par.py: the only change against the provided
process-pool version is `ProcessPoolExecutor` -> `ThreadPoolExecutor`.

Lab Q2.9 also asks about the GIL; the script supports a `--time` flag
that prints wall-clock so the report can compare 15 ms vs 60 ms scaling
against the multiprocess baseline.

Usage:
    python3 L2_Q8.py --dataset tvb76  --tf 15
    python3 L2_Q8.py --dataset tvb192 --tf 60
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
from lib.mlp_params import MLP_L, MLP_M, layer_1_w, layer_1_b, layer_2_w, layer_2_b


def pre(x_src, x_dst):
    return x_src - 1.0


def post(gx):
    return 1e-3 * gx


def f(x, y):
    """MLP local dynamics — kept in pure Python on purpose so the GIL
    contention behaviour matches the provided multiprocessed reference."""
    sv = [x, y]
    hidden = [0] * MLP_L
    out = [0] * MLP_M
    for l in range(MLP_L):
        for m in range(MLP_M):
            hidden[l] += sv[m] * layer_1_w[MLP_L * m + l]
        hidden[l] += layer_1_b[l]
        if hidden[l] <= 0:
            hidden[l] = 0
    for m in range(MLP_M):
        for l in range(MLP_L):
            out[m] += hidden[l] * layer_2_w[MLP_M * l + m]
        out[m] += layer_2_b[m]
    return tuple(out)


def calculate_coupling(Xs, W_row, D_row, t, n):
    c_in = 0.0
    x_dst = Xs[n][0][t - 1]
    N = len(Xs)
    for i in range(N):
        x_src = 0.0
        if t >= D_row[i]:
            if (i == n) or (D_row[i] == 0):
                x_src = Xs[i][0][t - 1]
            else:
                x_src = Xs[i][0][t - D_row[i]]
        c_in += W_row[i] * pre(x_src, x_dst)
    return post(c_in)


def step(Xs, t, n, c_in, dt):
    x = Xs[n][0][t - 1]
    y = Xs[n][1][t - 1]
    fx, fy = f(x, y)
    return [x + dt * fx, y + dt * (fy + c_in)]


def center_task(Xs, W_row, D_row, t, n, dt):
    c_in = calculate_coupling(Xs, W_row, D_row, t, n)
    return step(Xs, t, n, c_in, dt)


def simulate(W, D, N, M, dt, tf, speed, chunk: int):
    """tvb_par.simulate but with a thread pool instead of a process pool."""
    total = int(tf / dt)
    Xs = [[[0.0 for _ in range(total)] for _ in range(M)] for _ in range(N)]
    D_ts = [[int((D[i][j] / speed) / dt) for i in range(N)] for j in range(N)]
    for n in range(N):
        for m in range(M):
            Xs[n][m][0] = -1.0

    start = time.time()
    with ThreadPoolExecutor() as ex:
        for t in range(1, total):
            res = list(ex.map(
                center_task,
                [Xs] * N, W, D_ts, [t] * N, range(N), [dt] * N,
                chunksize=chunk,
            ))
            for n in range(N):
                for m in range(M):
                    Xs[n][m][t] = res[n][m]
    elapsed = time.time() - start
    print(f"{elapsed}")
    return [t * dt for t in range(total)], Xs, elapsed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="tvb76",
                   choices=["tvb76", "tvb192"])
    p.add_argument("--tf", type=float, default=15.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--chunk", type=int, default=40)
    args = p.parse_args()

    loader = {
        "tvb76": data.tvb76_weights_lengths,
        "tvb192": data.tvb192_weights_lengths,
    }[args.dataset]
    W, D = loader()
    W_l = W.tolist()
    D_l = D.tolist()
    N = len(W_l)
    M = 2

    simulate(W_l, D_l, N, M, args.dt, args.tf, args.speed, args.chunk)


if __name__ == "__main__":
    main()
