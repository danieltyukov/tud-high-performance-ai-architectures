"""
Q4.5 (4) runner: train the supplied mlp_adv.py architecture for 3 seeds, 10 epochs.

Mirrors the AdamW + dropout + 512-512 architecture from mlp_adv.py but is wired
up so we can vary the seed and capture train/test accuracy in JSONL. Not part
of the submission - we only submit code for 4.4 and 4.6.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import optax  # noqa: E402
from flax import linen as nn  # noqa: E402
from jax import random  # noqa: E402
from tensorflow.keras.datasets import mnist  # noqa: E402


RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "q5_results.jsonl"
RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_result(record: dict) -> None:
    print("RESULT:", json.dumps(record))
    with RESULTS_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")


class MLPAdv(nn.Module):
    dropout_rate: float = 0.3

    @nn.compact
    def __call__(self, x, train: bool):
        x = nn.Dense(512)(x)
        x = nn.relu(x)
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not train)
        x = nn.Dense(512)(x)
        x = nn.relu(x)
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not train)
        x = nn.Dense(10)(x)
        return x


def train_one(seed: int, epochs: int = 10, batch_size: int = 128):
    (x_tr, y_tr), (x_te, y_te) = mnist.load_data()
    x_tr = (x_tr.astype("float32") / 255.0).reshape(-1, 784)
    x_te = (x_te.astype("float32") / 255.0).reshape(-1, 784)

    key = random.PRNGKey(seed)
    model = MLPAdv()
    init_key, key = random.split(key)
    params = model.init(init_key, jnp.ones([1, 784]), train=True)["params"]
    optimizer = optax.adamw(learning_rate=1e-3, weight_decay=1e-4)
    opt_state = optimizer.init(params)

    @jax.jit
    def loss_fn(params, x, y, do_rng):
        logits = model.apply({"params": params}, x, train=True, rngs={"dropout": do_rng})
        return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, y))

    @jax.jit
    def accuracy(params, x, y):
        logits = model.apply({"params": params}, x, train=False)
        preds = jnp.argmax(logits, axis=-1)
        return 100.0 * jnp.mean(preds == y)

    @jax.jit
    def step(params, opt_state, x, y, do_rng):
        loss, grads = jax.value_and_grad(loss_fn)(params, x, y, do_rng)
        updates, opt_state = optimizer.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        return params, opt_state, loss

    x_tr_j = jnp.array(x_tr)
    y_tr_j = jnp.array(y_tr)
    x_te_j = jnp.array(x_te)
    y_te_j = jnp.array(y_te)

    untrained = float(accuracy(params, x_te_j, y_te_j))

    t0 = time.perf_counter()
    for _ in range(epochs):
        for i in range(0, len(x_tr_j), batch_size):
            key, sub = random.split(key)
            params, opt_state, _ = step(
                params, opt_state,
                x_tr_j[i : i + batch_size],
                y_tr_j[i : i + batch_size],
                sub,
            )
    wall = time.perf_counter() - t0

    test_acc = float(accuracy(params, x_te_j, y_te_j))
    train_acc = float(accuracy(params, x_tr_j, y_tr_j))
    return {
        "seed": seed,
        "untrained": untrained,
        "train_acc": train_acc,
        "test_acc": test_acc,
        "wall_s": wall,
    }


def main():
    for seed in (0, 10, 42):
        out = train_one(seed=seed)
        log_result({"exp": "4.5.4", "lr": 1e-3, "wd": 1e-4, "epochs": 10,
                    "batch": 128, **out})


if __name__ == "__main__":
    main()
