"""
Lab 4 Q4.6 LeNet-5 on MNIST.

Pipeline: 28x28x1 -> Conv(6,5x5,SAME)+tanh -> AvgPool 2x2 -> Conv(16,5x5,VALID)
+tanh -> AvgPool 2x2 -> flatten -> Dense 120 + tanh -> Dense 84 + tanh ->
Dense 10. AdamW optimiser, batched training. 61,706 parameters.

Usage: python L4_Q6.py {4_6_1|4_6_3|all}
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
import numpy as np  # noqa: E402
import optax  # noqa: E402
from flax import linen as nn  # noqa: E402
from jax import random  # noqa: E402
from tensorflow.keras.datasets import mnist  # noqa: E402


RESULTS_PATH = Path(__file__).resolve().parent.parent / "results" / "q6_results.jsonl"
RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def log_result(record: dict) -> None:
    print("RESULT:", json.dumps(record))
    with RESULTS_PATH.open("a") as f:
        f.write(json.dumps(record) + "\n")


def load_mnist():
    (x_tr, y_tr), (x_te, y_te) = mnist.load_data()
    x_tr = (x_tr.astype("float32") / 255.0)[..., None]
    x_te = (x_te.astype("float32") / 255.0)[..., None]
    return x_tr, y_tr, x_te, y_te


class LeNet5(nn.Module):
    @nn.compact
    def __call__(self, x):
        x = nn.tanh(nn.Conv(features=6, kernel_size=(5, 5), padding="SAME")(x))
        x = nn.avg_pool(x, window_shape=(2, 2), strides=(2, 2))
        x = nn.tanh(nn.Conv(features=16, kernel_size=(5, 5), padding="VALID")(x))
        x = nn.avg_pool(x, window_shape=(2, 2), strides=(2, 2))
        x = x.reshape(x.shape[0], -1)
        x = nn.tanh(nn.Dense(120)(x))
        x = nn.tanh(nn.Dense(84)(x))
        return nn.Dense(10)(x)


def count_params(params) -> int:
    return int(sum(int(np.prod(l.shape)) for l in jax.tree_util.tree_leaves(params)))


def train_lenet(seed: int, lr: float, wd: float, epochs: int, batch_size: int):
    x_tr, y_tr, x_te, y_te = load_mnist()
    model = LeNet5()
    params = model.init(random.PRNGKey(seed), jnp.ones([1, 28, 28, 1]))["params"]
    n_params = count_params(params)

    optimizer = optax.adamw(learning_rate=lr, weight_decay=wd)
    opt_state = optimizer.init(params)

    @jax.jit
    def loss_fn(params, x, y):
        logits = model.apply({"params": params}, x)
        return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, y))

    @jax.jit
    def accuracy(params, x, y):
        preds = jnp.argmax(model.apply({"params": params}, x), axis=-1)
        return 100.0 * jnp.mean(preds == y)

    @jax.jit
    def step(params, opt_state, x, y):
        _, grads = jax.value_and_grad(loss_fn)(params, x, y)
        updates, opt_state = optimizer.update(grads, opt_state, params)
        return optax.apply_updates(params, updates), opt_state

    x_tr_j, y_tr_j = jnp.array(x_tr), jnp.array(y_tr)
    x_te_j, y_te_j = jnp.array(x_te), jnp.array(y_te)

    untrained = float(accuracy(params, x_te_j, y_te_j))

    # Chunked eval avoids one giant forward pass over 60k 28x28 images.
    def eval_acc(params, x, y, chunk=2000):
        correct = 0
        for i in range(0, len(x), chunk):
            preds = jnp.argmax(model.apply({"params": params}, x[i:i + chunk]), axis=-1)
            correct += int(jnp.sum(preds == y[i:i + chunk]))
        return 100.0 * correct / len(x)

    t0 = time.perf_counter()
    for _ in range(epochs):
        for i in range(0, len(x_tr_j), batch_size):
            params, opt_state = step(params, opt_state,
                                     x_tr_j[i:i + batch_size],
                                     y_tr_j[i:i + batch_size])
    wall = time.perf_counter() - t0

    return {
        "seed": seed, "lr": lr, "wd": wd, "epochs": epochs, "batch": batch_size,
        "n_params": n_params, "untrained": untrained,
        "train_acc": eval_acc(params, x_tr_j, y_tr_j),
        "test_acc": eval_acc(params, x_te_j, y_te_j),
        "wall_s": wall,
    }


# Experiments

def exp_4_6_1():
    model = LeNet5()
    params = model.init(random.PRNGKey(0), jnp.ones([1, 28, 28, 1]))["params"]
    breakdown = {k: int(np.prod(v["kernel"].shape) + np.prod(v["bias"].shape))
                 for k, v in params.items()}
    log_result({"exp": "4.6.1", "n_params": count_params(params), "by_layer": breakdown})


def exp_4_6_3():
    for seed in (0, 10, 42):
        out = train_lenet(seed=seed, lr=1e-3, wd=1e-4, epochs=10, batch_size=128)
        log_result({"exp": "4.6.3", "sweep": "seeds", **out})
    for lr in (1e-2, 1e-3, 1e-4):
        for wd in (0.0, 1e-4, 1e-3):
            out = train_lenet(seed=10, lr=lr, wd=wd, epochs=10, batch_size=128)
            log_result({"exp": "4.6.3", "sweep": "lr_wd", **out})


EXPERIMENTS = {"4_6_1": exp_4_6_1, "4_6_3": exp_4_6_3}


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
