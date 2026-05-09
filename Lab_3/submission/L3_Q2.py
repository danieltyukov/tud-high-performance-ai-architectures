import time

import cupy as cp
import numpy as np

from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def simulate_batched(W_np, D_np, K, dt, tf, speed):
    N, M = W_np.shape[0], 2
    total_timesteps = int(tf / dt)

    W = cp.asarray(W_np)
    D_ts = cp.asarray(((D_np / speed) / dt).astype(np.int64))
    w1 = cp.asarray(layer_1_w_np)
    b1 = cp.asarray(layer_1_b_np)
    w2 = cp.asarray(layer_2_w_np)
    b2 = cp.asarray(layer_2_b_np)

    Xs = cp.zeros((K, N, M, total_timesteps))
    Xs[:, :, :, 0] = -1.0

    j_idx = cp.arange(N)[None, :]                              # [1, N]
    n_idx = cp.arange(N)[:, None]                              # [N, 1]

    cp.cuda.Stream.null.synchronize()
    t0 = time.time()
    for t in range(1, total_timesteps):
        valid = (t >= D_ts)
        use_tm1 = (n_idx == j_idx) | (D_ts == 0)
        src_t = cp.where(use_tm1, t - 1, t - D_ts)
        src_t = cp.where(valid, src_t, 0)

        x_src = Xs[:, j_idx, 0, src_t]                         # [K, N, N]
        x_src = cp.where(valid, x_src, 0.0)
        contrib = W * (x_src - 1.0)
        c_in = 1e-3 * contrib.sum(axis=2)                      # [K, N]

        X_prev = Xs[:, :, :, t - 1]                            # [K, N, M]
        h = X_prev @ w1 + b1
        cp.maximum(h, 0.0, out=h)
        fx = h @ w2 + b2
        fx[..., 1] += c_in
        Xs[:, :, :, t] = X_prev + fx * dt
    cp.cuda.Stream.null.synchronize()
    elapsed = time.time() - t0

    return elapsed, Xs


def _load(name):
    if name == "tvb76":  return data.tvb76_weights_lengths()
    if name == "tvb192": return data.tvb192_weights_lengths()
    if name == "tvb998": return data.tvb998_weights_lengths()
    raise SystemExit(f"unknown dataset {name}")


if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("dataset", choices=["tvb76", "tvb192", "tvb998"], default="tvb192", nargs="?")
    p.add_argument("--K", type=int, default=100)
    p.add_argument("--tf", type=float, default=150.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--reps", type=int, default=3)
    p.add_argument("--warmup", type=int, default=1)
    args = p.parse_args()

    W, D = _load(args.dataset)
    N = W.shape[0]
    total_T = int(args.tf / args.dt)

    # Warm up (small tf so we do not pay full memory cost twice).
    for _ in range(args.warmup):
        simulate_batched(W, D, args.K, args.dt, min(args.tf, 5.0), args.speed)

    times = []
    for _ in range(args.reps):
        elapsed, _ = simulate_batched(W, D, args.K, args.dt, args.tf, args.speed)
        times.append(elapsed)

    best = min(times)
    print(json.dumps({
        "impl": "cupy_batched", "dataset": args.dataset, "K": args.K,
        "tf": args.tf, "reps": args.reps, "min_s": best, "all_s": times,
        "iters_per_s": (args.K * total_T) / best,
    }))
