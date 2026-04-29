"""Q8 'before-JIT' baseline — runs tvb_seq_jit.py (NumPy arrays, no @jit) on TVB76 and TVB192."""

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
from lib.mlp_params import mlp_params
import tvb_seq_jit

DT, TF, SPEED = 0.05, 15.0, 4.0
M = 2
total_timesteps = int(TF / DT)

for name, loader in [
    ("TVB76", data.tvb76_weights_lengths),
    ("TVB192", data.tvb192_weights_lengths),
]:
    W, D = loader()
    N = W.shape[0]
    tvb_seq_jit.D_timestep = ((D / SPEED) / DT).astype(int)
    t0 = time.time()
    tvb_seq_jit.simulate(W, tvb_seq_jit.D_timestep, N, M, DT, total_timesteps, mlp_params)
    print(f"[Q8 baseline no-JIT] {name} N={N}: total={time.time()-t0:.4f}s", flush=True)
