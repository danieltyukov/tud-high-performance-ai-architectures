"""Dev-only: validate L1_Q8 (JIT sequential MLP) against the sequential MLP reference."""

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
import tvb_seq_mlp as ref
import L1_Q8 as q8


def main():
    dt, tf, speed = 0.05, 15.0, 4.0
    total_timesteps = int(tf / dt)

    for name, loader in [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
    ]:
        W_np, D_np = loader()
        W_list = W_np.tolist()
        D_list = D_np.tolist()
        N = W_np.shape[0]

        t0 = time.time()
        _, Xs_ref = ref.simulate(W_list, D_list, N, ref.MLP_M, dt, tf, speed, sparse_flag=False)
        t_ref = time.time() - t0
        Xs_ref = np.asarray(Xs_ref)

        # Warm-up to isolate JIT compilation cost
        _ = q8.simulate(W_np, D_np, total_timesteps, dt, speed)
        t0 = time.time()
        _, Xs_q8, _ = q8.simulate(W_np, D_np, total_timesteps, dt, speed)
        t_q8 = time.time() - t0

        diff = np.max(np.abs(Xs_q8 - Xs_ref))
        speedup = t_ref / t_q8
        print(f"\n{name} (N={N}, T={total_timesteps})")
        print(f"  reference (Python loops) : {t_ref:.4f}s")
        print(f"  L1_Q8 (warm JIT)         : {t_q8:.4f}s")
        print(f"  speedup                  : {speedup:.2f}x")
        print(f"  max |Xs_q8 - Xs_ref|     : {diff:.3e}")


if __name__ == "__main__":
    main()
