"""Numerical sanity check: L3_Q4 (Numba) and L3_Q5 (JAX) against tvb_vec
on TVB76 / 5 ms. Catches kernel bugs before we trust the timings."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tvb_vec  # noqa: E402
from lib import data  # noqa: E402

W, D = data.tvb76_weights_lengths()
N, M, dt, tf, speed = W.shape[0], 2, 0.05, 5.0, 4.0
_, Xs_ref = tvb_vec.simulate(W, D, N, M, dt, tf, speed)


def check(name, Xs):
    diff = float(np.max(np.abs(Xs_ref - Xs)))
    print(f"max |{name} - baseline| = {diff:.3e}")
    return diff


# Numba @cuda.jit
import L3_Q4  # noqa: E402
_, Xs_numba = L3_Q4.simulate_numba(W, D, dt, tf, speed)
check("numba", Xs_numba)


# JAX (subprocess so we can pick the platform via env var)
import json
import subprocess

cmd = [
    sys.executable, "-c",
    "import os; os.environ['JAX_PLATFORMS']='cpu'; "
    "import jax; jax.config.update('jax_enable_x64', True); "
    "import jax.numpy as jnp; import numpy as np; "
    "import sys; sys.path.insert(0, '" + os.path.dirname(__file__) + "'); "
    "from lib import data; "
    "from lib.mlp_params import layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np; "
    "from L3_Q5 import make_run; "
    "W, D = data.tvb76_weights_lengths(); "
    "N, dt, tf, speed = W.shape[0], 0.05, 5.0, 4.0; "
    "total_T = int(tf/dt); "
    "Wj = jnp.asarray(W); D_ts = jnp.asarray(((D/speed)/dt).astype(np.int64)); "
    "w1 = jnp.asarray(layer_1_w_np); b1 = jnp.asarray(layer_1_b_np); "
    "w2 = jnp.asarray(layer_2_w_np); b2 = jnp.asarray(layer_2_b_np); "
    "n_idx = jnp.arange(N)[:, None]; j_idx = jnp.arange(N)[None, :]; "
    "Xs_init = jnp.zeros((N, 2, total_T)).at[:, :, 0].set(-1.0); "
    "run = make_run(Wj, D_ts, w1, b1, w2, b2, n_idx, j_idx, total_T, dt); "
    "out = run(Xs_init); out.block_until_ready(); "
    "np.save('/tmp/jax_xs.npy', np.asarray(out))",
]
subprocess.check_call(cmd)
Xs_jax = np.load("/tmp/jax_xs.npy")
check("jax", Xs_jax)
