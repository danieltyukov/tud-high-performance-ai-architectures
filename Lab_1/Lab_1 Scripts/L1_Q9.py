import os
import sys
import time

import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
from lib.mlp_params import (
    layer_1_b_np,
    layer_1_w_np,
    layer_2_b_np,
    layer_2_w_np,
)


@njit(cache=True)
def simulate_jit(W, delays, total_timesteps, dt, l1w, l1b, l2w, l2b):
    N = W.shape[0]
    M = 2
    Xs = np.zeros((N, M, total_timesteps))
    Xs[:, :, 0] = -1.0

    self_or_zero = np.zeros((N, N), dtype=np.bool_)
    for n in range(N):
        for i in range(N):
            if (i == n) or (delays[n, i] == 0):
                self_or_zero[n, i] = True

    c_in = np.empty(N)

    for t in range(1, total_timesteps):
        for n in range(N):
            s = 0.0
            for i in range(N):
                d = delays[n, i]
                if t < d:
                    x_src = 0.0
                elif self_or_zero[n, i]:
                    x_src = Xs[i, 0, t - 1]
                else:
                    x_src = Xs[i, 0, t - d]
                s += W[n, i] * (x_src - 1.0)
            c_in[n] = 1e-3 * s

        sv = Xs[:, :, t - 1].copy()
        hidden = sv @ l1w + l1b
        hidden = np.maximum(hidden, 0.0)
        out = hidden @ l2w + l2b

        for n in range(N):
            Xs[n, 0, t] = sv[n, 0] + dt * out[n, 0]
            Xs[n, 1, t] = sv[n, 1] + dt * (out[n, 1] + c_in[n])

    return Xs


def simulate(W, D, total_timesteps, dt, speed):
    delays = (D / speed / dt).astype(np.int64)
    start = time.time()
    Xs = simulate_jit(
        W, delays, total_timesteps, dt,
        layer_1_w_np, layer_1_b_np, layer_2_w_np, layer_2_b_np,
    )
    duration = time.time() - start
    T_axis = np.arange(total_timesteps) * dt
    return T_axis, Xs, duration


def main():
    dt = 0.05
    tf = 15.0
    speed = 4.0
    total_timesteps = int(tf / dt)

    print(f"{'dataset':>8}  {'N':>5}  {'1st run (incl JIT) (s)':>24}  {'2nd run (s)':>14}")
    for name, loader in [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
        ("TVB998", data.tvb998_weights_lengths),
    ]:
        W, D = loader()
        _, _, t1 = simulate(W, D, total_timesteps, dt, speed)
        _, _, t2 = simulate(W, D, total_timesteps, dt, speed)
        print(f"{name:>8}  {W.shape[0]:>5}  {t1:>24.4f}  {t2:>14.4f}")


if __name__ == "__main__":
    main()
