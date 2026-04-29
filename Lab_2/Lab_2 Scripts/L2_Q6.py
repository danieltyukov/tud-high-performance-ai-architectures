# L2_Q6.py
# Multiprocessed TVB-MLP with shared memory + initializer, NumPy-vectorised
# MLP, and sparse (CSR) coupling. Numerically equivalent to tvb_par_sm_imp.py
# (validate_q6.py confirms max abs diff ~3e-15 on TVB76).

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data, plot
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


# Worker globals (filled in by init_worker, then read by center_task).
Xs_shared = None
W_data_shared = None
D_data_shared = None
col_idx_shared = None
row_ptr_shared = None
_shm_handles = []


def init_worker(Xs_name, Xs_shape, Xs_dtype,
                W_name, W_shape, W_dtype,
                D_name, D_shape, D_dtype,
                col_name, col_shape, col_dtype,
                row_name, row_shape, row_dtype):
    global Xs_shared, W_data_shared, D_data_shared, col_idx_shared, row_ptr_shared
    global _shm_handles

    Xs_shm = shared_memory.SharedMemory(name=Xs_name)
    W_shm  = shared_memory.SharedMemory(name=W_name)
    D_shm  = shared_memory.SharedMemory(name=D_name)
    C_shm  = shared_memory.SharedMemory(name=col_name)
    R_shm  = shared_memory.SharedMemory(name=row_name)

    Xs_shared      = np.ndarray(Xs_shape,  dtype=Xs_dtype,  buffer=Xs_shm.buf)
    W_data_shared  = np.ndarray(W_shape,   dtype=W_dtype,   buffer=W_shm.buf)
    D_data_shared  = np.ndarray(D_shape,   dtype=D_dtype,   buffer=D_shm.buf)
    col_idx_shared = np.ndarray(col_shape, dtype=col_dtype, buffer=C_shm.buf)
    row_ptr_shared = np.ndarray(row_shape, dtype=row_dtype, buffer=R_shm.buf)

    # Hold refs so the SHM blocks live for the whole worker.
    _shm_handles = [Xs_shm, W_shm, D_shm, C_shm, R_shm]


def f_vec(x, y):
    # MLP forward pass, vectorised across the two state vars.
    sv = np.array([x, y])
    hidden = sv @ layer_1_w_np + layer_1_b_np
    np.maximum(hidden, 0.0, out=hidden)
    out = hidden @ layer_2_w_np + layer_2_b_np
    return float(out[0]), float(out[1])


def calculate_coupling_sparse_vec(t, n):
    # Same sum as the reference, but only over non-zero edges of row n
    # and with the inner loop replaced by NumPy ops.
    s = row_ptr_shared[n]
    e = row_ptr_shared[n + 1]
    if s == e:
        return 0.0

    W_row = W_data_shared[s:e]
    D_row = D_data_shared[s:e]
    col   = col_idx_shared[s:e]

    ready = D_row <= t
    use_tm1 = (col == n) | (D_row == 0)
    src_idx = np.where(use_tm1, t - 1, t - D_row)
    np.maximum(src_idx, 0, out=src_idx)
    # `ready==False` zeros out the contribution; keeps the original
    # x_src=0 -> pre(0)= -1 semantics from calculate_coupling.
    x_src = Xs_shared[col, 0, src_idx] * ready
    c_in = float(np.sum(W_row * (x_src - 1.0)))
    return 1e-3 * c_in


def center_task(t, n, dt):
    c_in = calculate_coupling_sparse_vec(t, n)
    x = Xs_shared[n, 0, t - 1]
    y = Xs_shared[n, 1, t - 1]
    fx, fy = f_vec(x, y)
    return [x + dt * fx, y + dt * (fy + c_in)]


def to_csr(W, D_ts):
    # Dense -> CSR. Delays are carried alongside the weights so the
    # worker doesn't have to re-derive them from W's column index.
    N = W.shape[0]
    W_data, D_data, col_idx = [], [], []
    row_ptr = [0]
    for i in range(N):
        for j in range(N):
            if W[i, j] != 0.0:
                W_data.append(W[i, j])
                D_data.append(int(D_ts[i, j]))
                col_idx.append(j)
        row_ptr.append(len(W_data))
    return (np.asarray(W_data, dtype=np.float64),
            np.asarray(D_data, dtype=np.int64),
            np.asarray(col_idx, dtype=np.int64),
            np.asarray(row_ptr, dtype=np.int64))


def simulate(W, D, dt, tf, speed, chunk):
    N = W.shape[0]
    M = 2
    total = int(tf / dt)
    Xs = np.zeros((N, M, total), dtype=np.float64)
    Xs[:, :, 0] = -1.0
    D_ts = ((D / speed) / dt).astype(np.int64)

    W_data, D_data, col_idx, row_ptr = to_csr(W, D_ts)

    Xs_shm = shared_memory.SharedMemory(create=True, size=Xs.nbytes)
    W_shm  = shared_memory.SharedMemory(create=True, size=W_data.nbytes)
    D_shm  = shared_memory.SharedMemory(create=True, size=D_data.nbytes)
    C_shm  = shared_memory.SharedMemory(create=True, size=col_idx.nbytes)
    R_shm  = shared_memory.SharedMemory(create=True, size=row_ptr.nbytes)
    try:
        Xs_a = np.ndarray(Xs.shape,      dtype=Xs.dtype,      buffer=Xs_shm.buf)
        W_a  = np.ndarray(W_data.shape,  dtype=W_data.dtype,  buffer=W_shm.buf)
        D_a  = np.ndarray(D_data.shape,  dtype=D_data.dtype,  buffer=D_shm.buf)
        C_a  = np.ndarray(col_idx.shape, dtype=col_idx.dtype, buffer=C_shm.buf)
        R_a  = np.ndarray(row_ptr.shape, dtype=row_ptr.dtype, buffer=R_shm.buf)
        np.copyto(Xs_a, Xs)
        np.copyto(W_a, W_data)
        np.copyto(D_a, D_data)
        np.copyto(C_a, col_idx)
        np.copyto(R_a, row_ptr)

        start = time.time()
        with ProcessPoolExecutor(
            initializer=init_worker,
            initargs=(Xs_shm.name, Xs_a.shape, Xs_a.dtype,
                      W_shm.name,  W_a.shape,  W_a.dtype,
                      D_shm.name,  D_a.shape,  D_a.dtype,
                      C_shm.name,  C_a.shape,  C_a.dtype,
                      R_shm.name,  R_a.shape,  R_a.dtype),
        ) as ex:
            for t in range(1, total):
                results = list(ex.map(
                    center_task, [t]*N, range(N), [dt]*N,
                    chunksize=chunk,
                ))
                for n, xy in enumerate(results):
                    Xs_a[n, 0, t] = xy[0]
                    Xs_a[n, 1, t] = xy[1]
        elapsed = time.time() - start

        np.copyto(Xs, Xs_a)
    finally:
        for shm in (Xs_shm, W_shm, D_shm, C_shm, R_shm):
            shm.close()
            shm.unlink()

    T = [t * dt for t in range(total)]
    print(elapsed)
    return T, Xs, elapsed


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="tvb192",
                   choices=["tvb76", "tvb192", "tvb998"])
    p.add_argument("--tf", type=float, default=15.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--chunk", type=int, default=None,
                   help="executor.map chunksize; default = N")
    p.add_argument("--no-plot", action="store_true")
    args = p.parse_args()

    loader = {"tvb76":  data.tvb76_weights_lengths,
              "tvb192": data.tvb192_weights_lengths,
              "tvb998": data.tvb998_weights_lengths}[args.dataset]
    W, D = loader()

    chunk = args.chunk if args.chunk is not None else W.shape[0]
    T, Xs, _ = simulate(W, D, args.dt, args.tf, args.speed, chunk)

    if not args.no_plot:
        plot.plot_xs(T, Xs, args.speed)
