"""Numerical sanity check for L2_Q6.

Runs the dense provided implementation (tvb_par_sm_imp.py) and the
optimised L2_Q6 simulation on a small dataset and prints the maximum
absolute difference. Trajectories should match to floating-point
tolerance (~1e-12) since the only changes between the two are the order
of additions inside f() and the equivalent CSR rewrite of the coupling
loop.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data

import L2_Q6
import bench

W, D = data.tvb76_weights_lengths()
tf, dt, speed = 5.0, 0.05, 4.0

# Reference: dense + per-call shared-memory attach (tvb_par_sm.py).
import tvb_par_sm_imp
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory

N = W.shape[0]
total = int(tf / dt)
Xs_ref = np.zeros((N, 2, total))
Xs_ref[:, :, 0] = -1.0
D_ts = ((D / speed) / dt).astype(int)

Xs_shm = shared_memory.SharedMemory(create=True, size=Xs_ref.nbytes)
W_shm = shared_memory.SharedMemory(create=True, size=W.nbytes)
D_shm = shared_memory.SharedMemory(create=True, size=D_ts.nbytes)
try:
    Xs_a = np.ndarray(Xs_ref.shape, dtype=Xs_ref.dtype, buffer=Xs_shm.buf)
    W_a = np.ndarray(W.shape, dtype=W.dtype, buffer=W_shm.buf)
    D_a = np.ndarray(D_ts.shape, dtype=D_ts.dtype, buffer=D_shm.buf)
    np.copyto(Xs_a, Xs_ref); np.copyto(W_a, W); np.copyto(D_a, D_ts)
    Xs_a[:, :, 0] = -1.0

    with ProcessPoolExecutor(
        initializer=tvb_par_sm_imp.init_worker,
        initargs=(Xs_shm.name, Xs_a.shape, Xs_a.dtype,
                  W_shm.name, W_a.shape, W_a.dtype,
                  D_shm.name, D_a.shape, D_a.dtype),
    ) as ex:
        for t in range(1, total):
            res = list(ex.map(
                tvb_par_sm_imp.center_task,
                [t] * N, range(N), [dt] * N, chunksize=N,
            ))
            for n, xy in enumerate(res):
                Xs_a[n, 0, t] = xy[0]
                Xs_a[n, 1, t] = xy[1]
    Xs_ref = Xs_a.copy()
finally:
    for shm in (Xs_shm, W_shm, D_shm):
        shm.close(); shm.unlink()

# Test: optimised L2_Q6 simulation.
_, Xs_opt, _ = L2_Q6.simulate(W, D, dt, tf, speed, chunk=N)

diff = np.abs(Xs_ref - Xs_opt).max()
print(f"max |ref - opt| = {diff:.3e}")
assert diff < 1e-9, f"L2_Q6 diverges from reference by {diff:.3e}"
print("OK")
