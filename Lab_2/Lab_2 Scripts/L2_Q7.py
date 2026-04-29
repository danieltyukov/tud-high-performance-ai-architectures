# L2_Q7.py
# Throughput-oriented multiprocessing: launch N_sims complete TVB
# simulations in parallel, one full sim per worker. Each sim uses the
# same vectorised + sparse kernel as L2_Q6, just without the inner pool.

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def to_csr(W, D_ts):
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


def simulate_single(W, D, dt, tf, speed):
    # Vectorised + sparse single-process simulation. No multiprocessing
    # inside — that's the whole point of Q7.
    N = W.shape[0]
    M = 2
    total = int(tf / dt)
    D_ts = ((D / speed) / dt).astype(np.int64)
    W_data, D_data, col_idx, row_ptr = to_csr(W, D_ts)

    Xs = np.zeros((N, M, total), dtype=np.float64)
    Xs[:, :, 0] = -1.0

    for t in range(1, total):
        # MLP for all N centres in two matmuls.
        x_in = Xs[:, :, t - 1]
        hidden = x_in @ layer_1_w_np + layer_1_b_np
        np.maximum(hidden, 0.0, out=hidden)
        out_mlp = hidden @ layer_2_w_np + layer_2_b_np

        for n in range(N):
            s, e = row_ptr[n], row_ptr[n + 1]
            if s == e:
                c_in = 0.0
            else:
                W_row = W_data[s:e]
                D_row = D_data[s:e]
                col   = col_idx[s:e]
                ready = D_row <= t
                use_tm1 = (col == n) | (D_row == 0)
                src_idx = np.where(use_tm1, t - 1, t - D_row)
                np.maximum(src_idx, 0, out=src_idx)
                x_src = Xs[col, 0, src_idx] * ready
                c_in = 1e-3 * float(np.sum(W_row * (x_src - 1.0)))
            Xs[n, 0, t] = x_in[n, 0] + dt * out_mlp[n, 0]
            Xs[n, 1, t] = x_in[n, 1] + dt * (out_mlp[n, 1] + c_in)

    return Xs


def _worker(args):
    W, D, dt, tf, speed = args
    Xs = simulate_single(W, D, dt, tf, speed)
    # Only ship back the last column to keep IPC small.
    return Xs[:, :, -1]


def run_parallel(W, D, n_sims, dt, tf, speed):
    args_list = [(W, D, dt, tf, speed) for _ in range(n_sims)]
    t0 = time.time()
    with ProcessPoolExecutor() as ex:
        list(ex.map(_worker, args_list, chunksize=1))
    return time.time() - t0


def run_sequential_q6(W, D, n_sims, dt, tf, speed, chunk):
    import L2_Q6
    t0 = time.time()
    for _ in range(n_sims):
        L2_Q6.simulate(W, D, dt, tf, speed, chunk)
    return time.time() - t0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="tvb192",
                   choices=["tvb76", "tvb192", "tvb998"])
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--tf", type=float, default=15.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--baseline", choices=["none", "q6_serial"], default="none")
    p.add_argument("--chunk", type=int, default=None)
    args = p.parse_args()

    loader = {"tvb76":  data.tvb76_weights_lengths,
              "tvb192": data.tvb192_weights_lengths,
              "tvb998": data.tvb998_weights_lengths}[args.dataset]
    W, D = loader()
    N = W.shape[0]
    timesteps_per_sim = int(args.tf / args.dt)

    print(f"[Q7] dataset={args.dataset} N={N} tf={args.tf}ms "
          f"n_sims={args.n} timesteps/sim={timesteps_per_sim}")

    t_par = run_parallel(W, D, args.n, args.dt, args.tf, args.speed)
    iters = args.n * timesteps_per_sim
    print(f"[Q7][parallel-of-sims]  wall={t_par:.3f}s  "
          f"throughput={iters / t_par:.1f} iter/s")

    if args.baseline == "q6_serial":
        chunk = args.chunk if args.chunk is not None else N
        t_serial = run_sequential_q6(W, D, args.n, args.dt, args.tf,
                                     args.speed, chunk)
        print(f"[Q7][q6-back-to-back]  wall={t_serial:.3f}s  "
              f"throughput={iters / t_serial:.1f} iter/s")
        print(f"[Q7] throughput ratio = "
              f"{(iters/t_par) / (iters/t_serial):.2f}x")
