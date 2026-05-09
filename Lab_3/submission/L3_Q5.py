import argparse
import json
import os
import sys
import time


def _parse():
    p = argparse.ArgumentParser()
    p.add_argument("dataset", choices=["tvb76", "tvb192", "tvb998"])
    p.add_argument("--platform", choices=["cpu", "gpu"], default="gpu")
    p.add_argument("--tf", type=float, default=150.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--reps", type=int, default=3)
    p.add_argument("--warmup", type=int, default=1)
    return p.parse_args()


# Pick the JAX backend before importing it. JAX_PLATFORMS expects "cpu" or
# "cuda"; the assignment text uses the friendlier "gpu" name, so we map.
_args = _parse()
os.environ["JAX_PLATFORMS"] = "cuda" if _args.platform == "gpu" else _args.platform

import jax  # noqa: E402
jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402

import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import data  # noqa: E402
from lib.mlp_params import (  # noqa: E402
    layer_1_b_np, layer_1_w_np, layer_2_b_np, layer_2_w_np,
)


def make_run(W, D_ts, w1, b1, w2, b2, n_idx, j_idx, total_T, dt):
    def body(Xs, t):
        valid = (t >= D_ts)
        use_tm1 = (n_idx == j_idx) | (D_ts == 0)
        src_t = jnp.where(use_tm1, t - 1, t - D_ts)
        src_t = jnp.where(valid, src_t, 0)

        x_src = Xs[j_idx, 0, src_t]                  # [N, N]
        x_src = jnp.where(valid, x_src, 0.0)
        contrib = W * (x_src - 1.0)
        c_in = 1e-3 * contrib.sum(axis=1)            # [N]

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


def _load(name):
    if name == "tvb76":  return data.tvb76_weights_lengths()
    if name == "tvb192": return data.tvb192_weights_lengths()
    if name == "tvb998": return data.tvb998_weights_lengths()
    raise SystemExit(f"unknown dataset {name}")


def main():
    W_np, D_np = _load(_args.dataset)
    N = W_np.shape[0]
    total_T = int(_args.tf / _args.dt)
    print(f"[L3_Q5] platform={_args.platform} devices={jax.devices()}", flush=True)

    W = jnp.asarray(W_np)
    D_ts = jnp.asarray(((D_np / _args.speed) / _args.dt).astype(np.int64))
    w1 = jnp.asarray(layer_1_w_np)
    b1 = jnp.asarray(layer_1_b_np)
    w2 = jnp.asarray(layer_2_w_np)
    b2 = jnp.asarray(layer_2_b_np)
    n_idx = jnp.arange(N)[:, None]
    j_idx = jnp.arange(N)[None, :]

    Xs_init = jnp.zeros((N, 2, total_T)).at[:, :, 0].set(-1.0)
    run = make_run(W, D_ts, w1, b1, w2, b2, n_idx, j_idx, total_T, _args.dt)

    # Warmup runs trigger JIT compile and let XLA settle on a final plan.
    for _ in range(_args.warmup):
        out = run(Xs_init); out.block_until_ready()

    times = []
    for _ in range(_args.reps):
        t0 = time.time()
        out = run(Xs_init); out.block_until_ready()
        times.append(time.time() - t0)

    print(json.dumps({
        "impl": f"jax_{_args.platform}", "dataset": _args.dataset,
        "tf": _args.tf, "reps": _args.reps,
        "min_s": min(times), "all_s": times,
    }))


if __name__ == "__main__":
    main()
