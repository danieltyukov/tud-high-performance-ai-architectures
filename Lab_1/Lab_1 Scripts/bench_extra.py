"""Supplemental bench — sequential MLP on TVB76 and TVB998 (the assignment for 1.6 requires it)."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data
import tvb_seq_mlp

DT, TF, SPEED, M = 0.05, 15.0, 4.0, 2

for name, loader in [
    ("TVB76", data.tvb76_weights_lengths),
    ("TVB998", data.tvb998_weights_lengths),
]:
    W_np, D_np = loader()
    W = W_np.tolist()
    D = D_np.tolist()
    N = len(W)
    print(f"\n=== {name} (N={N}) MLP dense, 15 ts ===", flush=True)
    tvb_seq_mlp.simulate(W, D, N, M, DT, TF, SPEED, sparse_flag=False)
    print(f"\n=== {name} (N={N}) MLP sparse, 15 ts ===", flush=True)
    tvb_seq_mlp.simulate(W, D, N, M, DT, TF, SPEED, sparse_flag=True)
