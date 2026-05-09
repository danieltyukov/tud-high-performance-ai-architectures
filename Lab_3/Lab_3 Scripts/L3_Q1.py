"""Q3.1.3 — TVB on GPU using CuPy.

The numerics are identical to tvb_vec_full.py (Q3.1.2). Only difference:
arrays live on the GPU and ops dispatch through CuPy. The MLP weights and
the connectivity matrices are uploaded once, before the time loop, so that
the only per-step cost is the GPU compute itself plus a few small kernel
launches.
"""
import time

import numpy as np

import cupy as cp

from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def coupling_all_gpu(Xs, W, D_ts, t, j_idx, n_idx):
    valid = (t >= D_ts)
    use_tm1 = (n_idx == j_idx) | (D_ts == 0)
    src_t = cp.where(use_tm1, t - 1, t - D_ts)
    src_t = cp.where(valid, src_t, 0)

    x_src = Xs[j_idx, 0, src_t]
    x_src = cp.where(valid, x_src, 0.0)

    contrib = W * (x_src - 1.0)
    return 1e-3 * contrib.sum(axis=1)


def step_all_gpu(X_prev, c_in, dt, w1, b1, w2, b2):
    h = X_prev @ w1 + b1
    cp.maximum(h, 0.0, out=h)
    fx = h @ w2 + b2
    fx[:, 1] += c_in
    return X_prev + fx * dt


def simulate_gpu(W_np, D_np, N, M, dt, tf, speed, sync_each_step=False):
    total_timesteps = int(tf / dt)

    # Upload everything we will need to the GPU exactly once.
    W = cp.asarray(W_np)
    D_ts = cp.asarray(((D_np / speed) / dt).astype(np.int64))
    w1 = cp.asarray(layer_1_w_np)
    b1 = cp.asarray(layer_1_b_np)
    w2 = cp.asarray(layer_2_w_np)
    b2 = cp.asarray(layer_2_b_np)

    Xs = cp.zeros((N, M, total_timesteps))
    Xs[:, :, 0] = -1.0

    j_idx = cp.arange(N)[None, :]
    n_idx = cp.arange(N)[:, None]

    cp.cuda.Stream.null.synchronize()
    t0 = time.time()
    for t in range(1, total_timesteps):
        c_in = coupling_all_gpu(Xs, W, D_ts, t, j_idx, n_idx)
        Xs[:, :, t] = step_all_gpu(Xs[:, :, t - 1], c_in, dt, w1, b1, w2, b2)
        if sync_each_step:
            cp.cuda.Stream.null.synchronize()
    cp.cuda.Stream.null.synchronize()
    elapsed = time.time() - t0

    T = [k * dt for k in range(total_timesteps)]
    print(f"[simulate_gpu] Total Time: {elapsed:.6f}s")
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
    p.add_argument("--warmup", type=int, default=1)
    args = p.parse_args()

    W, D = _load(args.dataset)
    N, M = W.shape[0], 2

    # Warm up to absorb first-call CUDA context creation and kernel JIT.
    for _ in range(args.warmup):
        simulate_gpu(W, D, N, M, args.dt, min(args.tf, 5.0), args.speed)

    times = []
    for _ in range(args.reps):
        t0 = time.time()
        simulate_gpu(W, D, N, M, args.dt, args.tf, args.speed)
        cp.cuda.Stream.null.synchronize()
        times.append(time.time() - t0)

    print(json.dumps({
        "impl": "cupy", "dataset": args.dataset, "tf": args.tf,
        "reps": args.reps, "min_s": min(times), "all_s": times,
    }))
