"""Q3.1.2 — Fully vectorised TVB on NumPy.

Same numerics as tvb_vec.py but the for n in range(N) loop inside simulate is
gone. F, calculate_coupling and step now operate on the whole [N, M] state at
once. This is also the base script for the CuPy port (L3_Q1.py).
"""
import time
from typing import List

import numpy as np

from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def f_all(X, w1, b1, w2, b2):
    # X: [N, M]. Two matmuls + ReLU. Output: [N, M].
    h = X @ w1 + b1
    np.maximum(h, 0.0, out=h)
    return h @ w2 + b2


def coupling_all(Xs, W, D_ts, t):
    # Vectorised version of the coupling sum, computed for every destination
    # node n at once. Output shape: [N].
    N = W.shape[0]

    valid = (t >= D_ts)                          # [N, N]
    use_tm1 = (np.arange(N)[None, :] == np.arange(N)[:, None]) | (D_ts == 0)
    src_t = np.where(use_tm1, t - 1, t - D_ts)   # [N, N]
    src_t = np.where(valid, src_t, 0)

    j_idx = np.arange(N)[None, :]                # [1, N], broadcasts to [N, N]
    x_src = Xs[j_idx, 0, src_t]                  # [N, N]
    x_src = np.where(valid, x_src, 0.0)

    contrib = W * (x_src - 1.0)                  # pre(x_src, x_dst) = x_src - 1
    return 1e-3 * contrib.sum(axis=1)            # post(c_in)


def step_all(X_prev, c_in, dt, w1, b1, w2, b2):
    # X_prev: [N, M], c_in: [N]. Forward Euler step on all nodes.
    fx = f_all(X_prev, w1, b1, w2, b2)
    fx[:, 1] = fx[:, 1] + c_in
    return X_prev + fx * dt


def simulate(W, D, N, M, dt, tf, speed):
    total_timesteps = int(tf / dt)
    Xs = np.zeros((N, M, total_timesteps))
    D_ts = ((D / speed) / dt).astype(int)

    Xs[:, :, 0] = -1.0

    w1, b1 = layer_1_w_np, layer_1_b_np
    w2, b2 = layer_2_w_np, layer_2_b_np

    start = time.time()
    for t in range(1, total_timesteps):
        c_in = coupling_all(Xs, W, D_ts, t)
        Xs[:, :, t] = step_all(Xs[:, :, t - 1], c_in, dt, w1, b1, w2, b2)
    end = time.time()

    T = [k * dt for k in range(total_timesteps)]
    print(f"[simulate] Total Time: {end - start:.6f}s")
    return T, Xs


def _load(name):
    if name == "tvb76":  return data.tvb76_weights_lengths()
    if name == "tvb192": return data.tvb192_weights_lengths()
    if name == "tvb998": return data.tvb998_weights_lengths()
    raise SystemExit(f"unknown dataset {name}")


if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("dataset", choices=["tvb76", "tvb192", "tvb998"])
    p.add_argument("--tf", type=float, default=150.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--reps", type=int, default=3)
    args = p.parse_args()

    W, D = _load(args.dataset)
    N, M = W.shape[0], 2

    times = []
    for _ in range(args.reps):
        t0 = time.time()
        simulate(W, D, N, M, args.dt, args.tf, args.speed)
        times.append(time.time() - t0)

    print(json.dumps({
        "impl": "vec_full", "dataset": args.dataset, "tf": args.tf,
        "reps": args.reps, "min_s": min(times), "all_s": times,
    }))
