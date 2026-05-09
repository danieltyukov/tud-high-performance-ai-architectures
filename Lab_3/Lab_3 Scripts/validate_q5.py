"""Numerical sanity check: JAX simulation vs tvb_vec on TVB76 / 5 ms.

Standalone (does not import L3_Q5 to avoid its argparse) but uses the
exact same scan body.
"""
import os
os.environ["JAX_PLATFORMS"] = "cpu"

import sys

import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tvb_vec
from lib import data
from lib.mlp_params import (
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def make_run(W, D_ts, w1, b1, w2, b2, n_idx, j_idx, total_T, dt):
    def body(Xs, t):
        valid = (t >= D_ts)
        use_tm1 = (n_idx == j_idx) | (D_ts == 0)
        src_t = jnp.where(use_tm1, t - 1, t - D_ts)
        src_t = jnp.where(valid, src_t, 0)
        x_src = Xs[j_idx, 0, src_t]
        x_src = jnp.where(valid, x_src, 0.0)
        contrib = W * (x_src - 1.0)
        c_in = 1e-3 * contrib.sum(axis=1)
        X_prev = Xs[:, :, t - 1]
        h = X_prev @ w1 + b1
        h = jnp.maximum(h, 0.0)
        fx = h @ w2 + b2
        fx = fx.at[:, 1].add(c_in)
        new_X = X_prev + fx * dt
        Xs = Xs.at[:, :, t].set(new_X)
        return Xs, None

    @jax.jit
    def run(Xs_init):
        Xs, _ = jax.lax.scan(body, Xs_init, jnp.arange(1, total_T))
        return Xs

    return run


def main():
    W, D = data.tvb76_weights_lengths()
    N, M, dt, tf, speed = W.shape[0], 2, 0.05, 5.0, 4.0
    total_T = int(tf / dt)

    _, Xs_ref = tvb_vec.simulate(W, D, N, M, dt, tf, speed)

    Wj = jnp.asarray(W)
    D_ts = jnp.asarray(((D / speed) / dt).astype(np.int64))
    w1 = jnp.asarray(layer_1_w_np)
    b1 = jnp.asarray(layer_1_b_np)
    w2 = jnp.asarray(layer_2_w_np)
    b2 = jnp.asarray(layer_2_b_np)
    n_idx = jnp.arange(N)[:, None]
    j_idx = jnp.arange(N)[None, :]
    Xs_init = jnp.zeros((N, 2, total_T)).at[:, :, 0].set(-1.0)

    run = make_run(Wj, D_ts, w1, b1, w2, b2, n_idx, j_idx, total_T, dt)
    Xs_jax = np.asarray(run(Xs_init))
    diff = float(np.max(np.abs(Xs_ref - Xs_jax)))
    print(f"max |jax - baseline| = {diff:.3e}")


if __name__ == "__main__":
    main()
