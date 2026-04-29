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
def f_mlp(x, y, l1w, l1b, l2w, l2b):
    L = l1w.shape[1]
    hidden = np.zeros(L)
    for l in range(L):
        s = l1b[l] + x * l1w[0, l] + y * l1w[1, l]
        if s > 0.0:
            hidden[l] = s
    out0 = l2b[0]
    out1 = l2b[1]
    for l in range(L):
        out0 += hidden[l] * l2w[l, 0]
        out1 += hidden[l] * l2w[l, 1]
    return out0, out1


@njit(cache=True)
def calculate_coupling(Xs, W_row, D_row, t, n):
    N = W_row.shape[0]
    c_in = 0.0
    for i in range(N):
        if t >= D_row[i]:
            if (i == n) or (D_row[i] == 0):
                x_src = Xs[i, 0, t - 1]
            else:
                x_src = Xs[i, 0, t - D_row[i]]
        else:
            x_src = 0.0
        c_in += W_row[i] * (x_src - 1.0)
    return 1e-3 * c_in


@njit(cache=True)
def simulate_jit(W, D_timestep, total_timesteps, dt, l1w, l1b, l2w, l2b):
    N = W.shape[0]
    M = 2
    Xs = np.zeros((N, M, total_timesteps))
    for n in range(N):
        for m in range(M):
            Xs[n, m, 0] = -1.0
    for t in range(1, total_timesteps):
        for n in range(N):
            c_in = calculate_coupling(Xs, W[n], D_timestep[n], t, n)
            x = Xs[n, 0, t - 1]
            y = Xs[n, 1, t - 1]
            fx, fy = f_mlp(x, y, l1w, l1b, l2w, l2b)
            Xs[n, 0, t] = x + dt * fx
            Xs[n, 1, t] = y + dt * (fy + c_in)
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
    ]:
        W, D = loader()
        _, _, t1 = simulate(W, D, total_timesteps, dt, speed)
        _, _, t2 = simulate(W, D, total_timesteps, dt, speed)
        print(f"{name:>8}  {W.shape[0]:>5}  {t1:>24.4f}  {t2:>14.4f}")


if __name__ == "__main__":
    main()
