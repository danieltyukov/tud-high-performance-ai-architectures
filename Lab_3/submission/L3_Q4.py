"""Q3.4 — TVB on GPU using Numba @cuda.jit.

One kernel per timestep, with one thread per brain region. Each thread
reads its own MLP input from the previous timestep, accumulates the
coupling sum into a register, runs the [2 -> 64 -> 2] MLP fully unrolled,
and writes its [x, y] back at index t. Threads only ever write disjoint
slots in Xs, so no atomics or shared memory are needed.
"""
import time

import numpy as np
from numba import cuda, float64, int64

from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)

MLP_L = 64
THREADS_PER_BLOCK = 128


@cuda.jit
def tvb_step_kernel(Xs, W, D_ts, l1w, l1b, l2w, l2b, t, dt):
    n = cuda.grid(1)
    N = W.shape[0]
    if n >= N:
        return

    # Coupling sum over all source nodes j -> destination n.
    s = 0.0
    for j in range(N):
        d = D_ts[n, j]
        if (j == n) or (d == 0):
            x = Xs[j, 0, t - 1]
        elif t >= d:
            x = Xs[j, 0, t - d]
        else:
            x = 0.0
        s += W[n, j] * (x - 1.0)
    c_in = 1e-3 * s

    # Forward MLP: hidden = ReLU(X @ l1w + l1b); out = hidden @ l2w + l2b.
    x0 = Xs[n, 0, t - 1]
    x1 = Xs[n, 1, t - 1]
    out0 = l2b[0]
    out1 = l2b[1]
    for k in range(MLP_L):
        h = l1b[k] + x0 * l1w[0, k] + x1 * l1w[1, k]
        if h < 0.0:
            h = 0.0
        out0 += h * l2w[k, 0]
        out1 += h * l2w[k, 1]
    out1 += c_in

    # Forward Euler step.
    Xs[n, 0, t] = x0 + out0 * dt
    Xs[n, 1, t] = x1 + out1 * dt


def simulate_numba(W_np, D_np, dt, tf, speed):
    N, M = W_np.shape[0], 2
    total_timesteps = int(tf / dt)

    Xs_np = np.zeros((N, M, total_timesteps))
    Xs_np[:, :, 0] = -1.0
    D_ts_np = ((D_np / speed) / dt).astype(np.int64)

    Xs = cuda.to_device(Xs_np)
    W = cuda.to_device(W_np)
    D_ts = cuda.to_device(D_ts_np)
    l1w = cuda.to_device(layer_1_w_np)
    l1b = cuda.to_device(layer_1_b_np)
    l2w = cuda.to_device(layer_2_w_np)
    l2b = cuda.to_device(layer_2_b_np)

    blocks = (N + THREADS_PER_BLOCK - 1) // THREADS_PER_BLOCK

    cuda.synchronize()
    t0 = time.time()
    for t in range(1, total_timesteps):
        tvb_step_kernel[blocks, THREADS_PER_BLOCK](
            Xs, W, D_ts, l1w, l1b, l2w, l2b, t, dt
        )
    cuda.synchronize()
    elapsed = time.time() - t0

    return elapsed, Xs.copy_to_host()


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

    # Warm up triggers the JIT compile pass for the kernel.
    for _ in range(args.warmup):
        simulate_numba(W, D, args.dt, min(args.tf, 5.0), args.speed)

    times = []
    for _ in range(args.reps):
        elapsed, _ = simulate_numba(W, D, args.dt, args.tf, args.speed)
        times.append(elapsed)

    print(json.dumps({
        "impl": "numba_cuda", "dataset": args.dataset, "tf": args.tf,
        "reps": args.reps, "min_s": min(times), "all_s": times,
    }))
