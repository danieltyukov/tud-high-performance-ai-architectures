"""
Lab 4 Q4.4 driver. Same MLP as mlp.py (784 -> Dense(128) -> ReLU -> Dense(10))
with hand-rolled SGD; toggles batching, normalization, LR and dataset size.

Usage: python L4_Q4.py {4_4_1..4_4_6|all}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("JAX_PLATFORMS", "cpu")

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
from flax import linen as nn  # noqa: E402
from jax import grad, random  # noqa: E402
from tensorflow.keras.datasets import mnist  # noqa: E402
import optax  # noqa: E402


RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "q4_results.jsonl"
RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_result(record: dict) -> None:
    print("RESULT:", json.dumps(record))
    with RESULTS_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")


def load_mnist(normalize: bool = True):
    (x_tr, y_tr), (x_te, y_te) = mnist.load_data()
    x_tr = x_tr.astype("float32")
    x_te = x_te.astype("float32")
    if normalize:
        x_tr = x_tr / 255.0
        x_te = x_te / 255.0
    return x_tr.reshape(-1, 784), y_tr, x_te.reshape(-1, 784), y_te


class MLP(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.Dense(128)(x)
        x = nn.relu(x)
        x = nn.Dense(10)(x)
        return x


def build_model(seed: int):
    model = MLP()
    params = model.init(random.PRNGKey(seed), jnp.ones([1, 784]))["params"]
    return model, params


def make_train_fns(model):
    @jax.jit
    def loss_fn(params, x, y):
        logits = model.apply({"params": params}, x)
        return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, y))

    @jax.jit
    def accuracy(params, x, y):
        preds = jnp.argmax(model.apply({"params": params}, x), axis=-1)
        return 100.0 * jnp.mean(preds == y)

    @jax.jit
    def sgd_step(params, x, y, lr):
        grads = grad(loss_fn)(params, x, y)
        return jax.tree_util.tree_map(lambda p, g: p - lr * g, params, grads)

    return loss_fn, accuracy, sgd_step


def train_per_sample(seed: int, lr: float, epochs: int, normalize: bool = True):
    """Original mlp.py loop: one sample per step."""
    x_tr, y_tr, x_te, y_te = load_mnist(normalize=normalize)
    model, params = build_model(seed)
    _, accuracy, sgd_step = make_train_fns(model)

    x_tr_j, y_tr_j = jnp.array(x_tr), jnp.array(y_tr)
    x_te_j, y_te_j = jnp.array(x_te), jnp.array(y_te)
    lr_j = jnp.float32(lr)

    untrained = float(accuracy(params, x_te_j, y_te_j))

    t0 = time.perf_counter()
    for _ in range(epochs):
        for i in range(len(x_tr_j)):
            params = sgd_step(params, x_tr_j[i], y_tr_j[i], lr_j)
    wall = time.perf_counter() - t0

    return {
        "untrained": untrained,
        "train_acc": float(accuracy(params, x_tr_j, y_tr_j)),
        "test_acc": float(accuracy(params, x_te_j, y_te_j)),
        "wall_s": wall,
    }


def train_batched(seed: int, lr: float, epochs: int, batch_size: int,
                  n_train: int | None = None, normalize: bool = True):
    """Minibatch loop added for Q4.4 (4)."""
    x_tr, y_tr, x_te, y_te = load_mnist(normalize=normalize)
    if n_train is not None:
        x_tr, y_tr = x_tr[:n_train], y_tr[:n_train]

    model, params = build_model(seed)
    _, accuracy, sgd_step = make_train_fns(model)

    x_tr_j, y_tr_j = jnp.array(x_tr), jnp.array(y_tr)
    x_te_j, y_te_j = jnp.array(x_te), jnp.array(y_te)
    lr_j = jnp.float32(lr)

    untrained = float(accuracy(params, x_te_j, y_te_j))

    t0 = time.perf_counter()
    for _ in range(epochs):
        for i in range(0, len(x_tr_j), batch_size):
            params = sgd_step(params, x_tr_j[i : i + batch_size],
                              y_tr_j[i : i + batch_size], lr_j)
    wall = time.perf_counter() - t0

    return {
        "untrained": untrained,
        "train_acc": float(accuracy(params, x_tr_j, y_tr_j)),
        "test_acc": float(accuracy(params, x_te_j, y_te_j)),
        "wall_s": wall,
    }


# Experiments

def exp_4_4_1():
    for seed in (0, 10, 42):
        out = train_per_sample(seed=seed, lr=0.001, epochs=10)
        log_result({"exp": "4.4.1", "seed": seed, "lr": 0.001, **out})


def exp_4_4_2():
    out = train_per_sample(seed=10, lr=0.001, epochs=10, normalize=False)
    log_result({"exp": "4.4.2", "seed": 10, "lr": 0.001, "normalize": False, **out})


def exp_4_4_3():
    for lr in (0.1, 1e-4, 1e-7):
        out = train_per_sample(seed=10, lr=lr, epochs=10)
        log_result({"exp": "4.4.3", "seed": 10, "lr": lr, **out})


def exp_4_4_4():
    for bs in (32, 64, 128, 256, 512):
        out = train_batched(seed=10, lr=0.001, epochs=10, batch_size=bs)
        log_result({"exp": "4.4.4", "seed": 10, "lr": 0.001, "batch": bs, **out})


def exp_4_4_5():
    for lr in (0.001, 0.01, 0.1, 0.5):
        out = train_batched(seed=10, lr=lr, epochs=10, batch_size=64)
        log_result({"exp": "4.4.5", "seed": 10, "lr": lr, "batch": 64, **out})


def exp_4_4_6():
    # Two LRs: 1e-3 underfits at this batch size, 0.1 fits + overfits.
    for lr in (0.001, 0.1):
        out = train_batched(seed=10, lr=lr, epochs=20, batch_size=64, n_train=1000)
        log_result({"exp": "4.4.6", "seed": 10, "lr": lr, "batch": 64,
                    "n_train": 1000, "epochs": 20, **out})


EXPERIMENTS = {
    "4_4_1": exp_4_4_1, "4_4_2": exp_4_4_2, "4_4_3": exp_4_4_3,
    "4_4_4": exp_4_4_4, "4_4_5": exp_4_4_5, "4_4_6": exp_4_4_6,
}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("which", choices=list(EXPERIMENTS.keys()) + ["all"])
    args = p.parse_args()
    if args.which == "all":
        for name, fn in EXPERIMENTS.items():
            print(f"\n=== {name} ===")
            fn()
    else:
        EXPERIMENTS[args.which]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
