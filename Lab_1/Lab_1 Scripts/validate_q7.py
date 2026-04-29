"""Dev-only: validate L1_Q7 sparse output equals sequential MLP sparse output, and equals L1_Q6 dense."""

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
import tvb_seq_mlp as ref
import L1_Q6 as q6
import L1_Q7 as q7


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

        # Sparse reference (sequential MLP with USE_SPARSE=True)
        t0 = time.time()
        T_ref, Xs_ref = ref.simulate(W_list, D_list, N, ref.MLP_M, dt, tf, speed, sparse_flag=True)
        t_ref = time.time() - t0
        Xs_ref = np.asarray(Xs_ref)

        # Vectorized dense (L1_Q6)
        _, Xs_q6, t_q6, _, _ = q6.simulate(W_np, D_np, total_timesteps, dt, speed)

        # Vectorized sparse (L1_Q7)
        t0 = time.time()
        _, Xs_q7, t_q7, c_q7, m_q7 = q7.simulate(W_np, D_np, total_timesteps, dt, speed)

        print(f"\n{name} (N={N}, T={total_timesteps})")
        print(f"  sequential sparse total : {t_ref:.4f}s")
        print(f"  vectorized dense  (Q6)  : {t_q6:.4f}s")
        print(f"  vectorized sparse (Q7)  : {t_q7:.4f}s   (coupling={c_q7:.4f}s, mlp={m_q7:.4f}s)")
        print(f"  max |Q7 - sparse_ref|   : {np.max(np.abs(Xs_q7 - Xs_ref)):.3e}")
        print(f"  max |Q7 - dense_Q6|     : {np.max(np.abs(Xs_q7 - Xs_q6)):.3e}")


if __name__ == "__main__":
    main()
