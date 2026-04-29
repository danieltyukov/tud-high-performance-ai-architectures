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


def build_csr(W, delays):
    N = W.shape[0]
    rows, cols = np.where(W != 0)
    W_sparse = W[rows, cols]
    D_sparse = delays[rows, cols]
    nnz_per_row = np.bincount(rows, minlength=N)
    row_pointer = np.zeros(N + 1, dtype=np.int64)
    row_pointer[1:] = np.cumsum(nnz_per_row)
    return W_sparse, D_sparse, cols, row_pointer, rows


def simulate(W, D, total_timesteps, dt, speed):
    N = W.shape[0]
    delays = (D / speed / dt).astype(int)

    W_sparse, D_sparse, col_index, row_pointer, row_for_nnz = build_csr(W, delays)
    self_or_zero = (col_index == row_for_nnz) | (D_sparse == 0)

    Xs = np.zeros((N, MLP_M, total_timesteps))
    Xs[:, :, 0] = -1.0

    c_duration = 0.0
    f_duration = 0.0
    start = time.time()

    for t in range(1, total_timesteps):
        c_start = time.time()
        t_src = t - D_sparse
        valid = t_src >= 0
        t_src_clipped = np.clip(t_src, 0, t - 1)
        x_src = Xs[col_index, 0, t_src_clipped]
        x_hist_at_cols = Xs[col_index, 0, t - 1]
        x_src = np.where(self_or_zero, x_hist_at_cols, x_src)
        x_src = np.where(valid, x_src, 0.0)
        contrib = W_sparse * (x_src - 1.0)
        c_in = 1e-3 * np.bincount(row_for_nnz, weights=contrib, minlength=N)
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

    print(f"{'dataset':>8}  {'N':>5}  {'NNZ':>7}  {'total (s)':>11}  {'coupling (s)':>14}  {'mlp (s)':>10}")
    for name, loader in [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
        ("TVB998", data.tvb998_weights_lengths),
    ]:
        W, D = loader()
        nnz = int(np.count_nonzero(W))
        _, _, total, coupling, mlp = simulate(W, D, total_timesteps, dt, speed)
        print(f"{name:>8}  {W.shape[0]:>5}  {nnz:>7}  {total:>11.4f}  {coupling:>14.4f}  {mlp:>10.4f}")


if __name__ == "__main__":
    main()
