"""Phase 2 driver: run every measurement Lab 1 needs, in one pass.

Run this on the AWS VM (after activating any venv that has numpy/numba):
    python3 bench_phase2.py | tee /tmp/lab1_bench.log

Use --skip-q2-q3 if the pure-Python TVB998 run is taking too long.
"""

import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
import tvb_seq, tvb_seq_sparse, tvb_seq_mlp
import L1_Q6, L1_Q7, L1_Q8, L1_Q9

DT, SPEED, FREQ, M = 0.05, 4.0, 1.0, 2


def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70, flush=True)


def bench_q2_q3(datasets):
    banner("Q2 / Q3 — tvb_seq.py, 150 timesteps")
    tf = 150.0
    for name, loader in datasets:
        W_np, D_np = loader()
        W = W_np.tolist()
        D = D_np.tolist()
        N = len(W)
        print(f"\n[Q2] {name} (N={N}) regular delays")
        tvb_seq.simulate(W, D, N, M, DT, tf, SPEED, FREQ)
        print(f"\n[Q3] {name} (N={N}) zero delays")
        D0 = [[0.0] * N for _ in range(N)]
        tvb_seq.simulate(W, D0, N, M, DT, tf, SPEED, FREQ)


def bench_q4c():
    banner("Q4c — tvb_seq_sparse.py, TVB192, 150 timesteps")
    W_np, D_np = data.tvb192_weights_lengths()
    W = W_np.tolist()
    D = D_np.tolist()
    N = len(W)
    print(f"\n[Q4c] TVB192 (N={N}) sparse sequential")
    tvb_seq_sparse.simulate_sparse(W, D, N, M, DT, 150.0, SPEED, FREQ)


def bench_q5():
    banner("Q5 — tvb_seq_mlp.py, TVB192, 15 timesteps")
    tf = 15.0
    W_np, D_np = data.tvb192_weights_lengths()
    W = W_np.tolist()
    D = D_np.tolist()
    N = len(W)
    print(f"\n[Q5a] TVB192 MLP dense")
    tvb_seq_mlp.simulate(W, D, N, M, DT, tf, SPEED, sparse_flag=False)
    print(f"\n[Q5c] TVB192 MLP sparse")
    tvb_seq_mlp.simulate(W, D, N, M, DT, tf, SPEED, sparse_flag=True)


def bench_q6_q7(datasets):
    banner("Q6 / Q7 — vectorized dense / sparse, 15 timesteps")
    total_timesteps = int(15.0 / DT)
    for name, loader in datasets:
        W, D = loader()
        N = W.shape[0]
        _, _, t6, c6, m6 = L1_Q6.simulate(W, D, total_timesteps, DT, SPEED)
        _, _, t7, c7, m7 = L1_Q7.simulate(W, D, total_timesteps, DT, SPEED)
        print(f"[Q6] {name} N={N}: total={t6:.4f}s coupling={c6:.4f}s mlp={m6:.4f}s")
        print(f"[Q7] {name} N={N}: total={t7:.4f}s coupling={c7:.4f}s mlp={m7:.4f}s")


def bench_q8(datasets):
    banner("Q8 — JIT sequential MLP (warm), 15 timesteps")
    total_timesteps = int(15.0 / DT)
    for name, loader in datasets:
        W, D = loader()
        N = W.shape[0]
        _, _, t1 = L1_Q8.simulate(W, D, total_timesteps, DT, SPEED)  # warm-up
        _, _, t2 = L1_Q8.simulate(W, D, total_timesteps, DT, SPEED)  # timed
        print(f"[Q8] {name} N={N}: warm={t2:.4f}s  (cold-incl-JIT={t1:.4f}s)")


def bench_q9(datasets):
    banner("Q9 — JIT vectorized (warm), 15 timesteps")
    total_timesteps = int(15.0 / DT)
    for name, loader in datasets:
        W, D = loader()
        N = W.shape[0]
        _, _, t1 = L1_Q9.simulate(W, D, total_timesteps, DT, SPEED)  # warm-up
        _, _, t2 = L1_Q9.simulate(W, D, total_timesteps, DT, SPEED)  # timed
        print(f"[Q9] {name} N={N}: warm={t2:.4f}s  (cold-incl-JIT={t1:.4f}s)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-q2-q3", action="store_true",
                        help="skip the slow pure-Python sweeps (Q2/Q3) when iterating")
    parser.add_argument("--datasets", default="76,192,998",
                        help="comma-separated subset of {76,192,998}")
    args = parser.parse_args()

    chosen = set(args.datasets.split(","))
    all_ds = [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
        ("TVB998", data.tvb998_weights_lengths),
    ]
    datasets = [(n, f) for n, f in all_ds if n.replace("TVB", "") in chosen]
    q8_datasets = [(n, f) for n, f in datasets if n in ("TVB76", "TVB192")]

    t0 = time.time()
    if not args.skip_q2_q3:
        bench_q2_q3(datasets)
    bench_q4c()
    bench_q5()
    bench_q6_q7(datasets)
    bench_q8(q8_datasets)
    bench_q9(datasets)
    banner(f"total bench wall-clock: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
