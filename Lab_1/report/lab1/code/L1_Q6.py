import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
from lib.mlp_params import (
    MLP_M,
    layer_1_b_np,
    layer_1_w_np,
    layer_2_b_np,
    layer_2_w_np,
)


def simulate(W, D, total_timesteps, dt, speed):
    N = W.shape[0]
    delays = (D / speed / dt).astype(int)

    Xs = np.zeros((N, MLP_M, total_timesteps))
    Xs[:, :, 0] = -1.0

    self_or_zero = np.eye(N, dtype=bool) | (delays == 0)
    src_idx = np.arange(N)[None, :]

    c_duration = 0.0
    f_duration = 0.0
    start = time.time()

    for t in range(1, total_timesteps):
        c_start = time.time()
        t_src = t - delays
        valid = t_src >= 0
        t_src_clipped = np.clip(t_src, 0, t - 1)
        x_src = Xs[src_idx, 0, t_src_clipped]
        x_hist = Xs[:, 0, t - 1]
        x_src = np.where(self_or_zero, x_hist[None, :], x_src)
        x_src = np.where(valid, x_src, 0.0)
        c_in = 1e-3 * np.sum(W * (x_src - 1.0), axis=1)
        c_duration += time.time() - c_start

        f_start = time.time()
        sv = Xs[:, :, t - 1]
        hidden = sv @ layer_1_w_np + layer_1_b_np
        np.maximum(hidden, 0, out=hidden)
        out = hidden @ layer_2_w_np + layer_2_b_np
        f_duration += time.time() - f_start

        Xs[:, 0, t] = sv[:, 0] + dt * out[:, 0]
        Xs[:, 1, t] = sv[:, 1] + dt * (out[:, 1] + c_in)

    total_duration = time.time() - start
    T_axis = np.arange(total_timesteps) * dt
    return T_axis, Xs, total_duration, c_duration, f_duration


def main():
    dt = 0.05
    tf = 15.0
    speed = 4.0
    total_timesteps = int(tf / dt)

    print(f"{'dataset':>8}  {'N':>5}  {'total (s)':>11}  {'coupling (s)':>14}  {'mlp (s)':>10}")
    for name, loader in [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
        ("TVB998", data.tvb998_weights_lengths),
    ]:
        W, D = loader()
        _, _, total, coupling, mlp = simulate(W, D, total_timesteps, dt, speed)
        print(f"{name:>8}  {W.shape[0]:>5}  {total:>11.4f}  {coupling:>14.4f}  {mlp:>10.4f}")


if __name__ == "__main__":
    main()
