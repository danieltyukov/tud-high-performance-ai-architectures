"""Dev-only: validate L1_Q9 (JIT vectorized) against L1_Q6 (vectorized) and L1_Q8 (JIT sequential)."""

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
import L1_Q6 as q6
import L1_Q8 as q8
import L1_Q9 as q9


def main():
    dt, tf, speed = 0.05, 15.0, 4.0
    total_timesteps = int(tf / dt)

    for name, loader in [
        ("TVB76", data.tvb76_weights_lengths),
        ("TVB192", data.tvb192_weights_lengths),
    ]:
        W_np, D_np = loader()
        N = W_np.shape[0]

        # Vectorized (Q6)
        _, Xs_q6, t_q6, _, _ = q6.simulate(W_np, D_np, total_timesteps, dt, speed)
        # Warm-up Q8 and Q9 JIT
        _ = q8.simulate(W_np, D_np, total_timesteps, dt, speed)
        _ = q9.simulate(W_np, D_np, total_timesteps, dt, speed)
        # Timed runs
        _, Xs_q8, t_q8 = q8.simulate(W_np, D_np, total_timesteps, dt, speed)
        _, Xs_q9, t_q9 = q9.simulate(W_np, D_np, total_timesteps, dt, speed)

        print(f"\n{name} (N={N}, T={total_timesteps})")
        print(f"  Q6 vectorized            : {t_q6:.4f}s")
        print(f"  Q8 JIT sequential (warm) : {t_q8:.4f}s")
        print(f"  Q9 JIT vectorized (warm) : {t_q9:.4f}s")
        print(f"  max |Q9 - Q6|            : {np.max(np.abs(Xs_q9 - Xs_q6)):.3e}")
        print(f"  max |Q9 - Q8|            : {np.max(np.abs(Xs_q9 - Xs_q8)):.3e}")


if __name__ == "__main__":
    main()
