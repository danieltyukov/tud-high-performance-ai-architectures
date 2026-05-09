"""Sanity check: tvb_vec_full and L3_Q1 (CuPy) match tvb_vec on TVB76, tf=5ms.

Catches refactoring bugs before we trust the timing numbers.
"""
import numpy as np

import tvb_vec
import tvb_vec_full
from lib import data


def main():
    W, D = data.tvb76_weights_lengths()
    N, M = W.shape[0], 2
    dt, tf, speed = 0.05, 5.0, 4.0

    _, Xs_ref = tvb_vec.simulate(W, D, N, M, dt, tf, speed)
    _, Xs_vec = tvb_vec_full.simulate(W, D, N, M, dt, tf, speed)

    diff_vec = float(np.max(np.abs(Xs_ref - Xs_vec)))
    print(f"max |vec_full - baseline| = {diff_vec:.3e}")

    try:
        import L3_Q1
        _, Xs_cupy = L3_Q1.simulate_gpu(W, D, N, M, dt, tf, speed)
        import cupy as cp
        Xs_cupy_np = cp.asnumpy(Xs_cupy)
        diff_cupy = float(np.max(np.abs(Xs_ref - Xs_cupy_np)))
        print(f"max |cupy - baseline|     = {diff_cupy:.3e}")
    except Exception as e:
        print(f"L3_Q1 (CuPy) skipped: {e}")


if __name__ == "__main__":
    main()
