"""
Lab 4 - Q4.6 LeNet-5 on MNIST.

Architecture from the assignment figure (tanh activations after every conv and
dense, average pooling, no padding so 28x28 -> 28 -> 14 -> 10 -> 5):

    Input  [B, 28, 28, 1]
    C1     Conv2D 6 filters, 5x5, valid pad  -> [B, 28, 28, 6]   (with same pad to keep 28)
    S2     AvgPool 2x2 stride 2              -> [B, 14, 14, 6]
    C3     Conv2D 16 filters, 5x5, valid pad -> [B, 10, 10, 16]
    S4     AvgPool 2x2 stride 2              -> [B, 5, 5, 16]
    F5     flatten + Dense 120 + tanh        -> [B, 120]
    F6     Dense 84 + tanh                   -> [B, 84]
    Out    Dense 10                          -> [B, 10]

The first conv uses "SAME" padding so the C1 feature map stays 28x28; this is
the classic LeNet-5 convention (the original used a 32x32 padded input but
modern MNIST implementations just pad the conv).

Optimizer: AdamW. Batched training. Output flattened to L4 results JSONL.
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


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_mnist():
    (x_tr, y_tr), (x_te, y_te) = mnist.load_data()
    x_tr = (x_tr.astype("float32") / 255.0)[..., None]   # [60000, 28, 28, 1]
    x_te = (x_te.astype("float32") / 255.0)[..., None]
    return x_tr, y_tr, x_te, y_te


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class LeNet5(nn.Module):
    @nn.compact
    def __call__(self, x):
        # C1: 1 -> 6, 5x5, keep 28x28 with SAME padding
        x = nn.Conv(features=6, kernel_size=(5, 5), padding="SAME")(x)
        x = nn.tanh(x)
        # S2: 28 -> 14
        x = nn.avg_pool(x, window_shape=(2, 2), strides=(2, 2))
        # C3: 6 -> 16, 5x5 valid -> 10x10
        x = nn.Conv(features=16, kernel_size=(5, 5), padding="VALID")(x)
        x = nn.tanh(x)
        # S4: 10 -> 5
        x = nn.avg_pool(x, window_shape=(2, 2), strides=(2, 2))
        # flatten
        x = x.reshape(x.shape[0], -1)        # [B, 400]
        # F5
        x = nn.Dense(120)(x)
        x = nn.tanh(x)
        # F6
        x = nn.Dense(84)(x)
        x = nn.tanh(x)
        # Output
        x = nn.Dense(10)(x)
        return x


def count_params(params) -> int:
    leaves = jax.tree_util.tree_leaves(params)
    return int(sum(int(np.prod(l.shape)) for l in leaves))


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_lenet(seed: int, lr: float, wd: float, epochs: int, batch_size: int):
    x_tr, y_tr, x_te, y_te = load_mnist()
    key = random.PRNGKey(seed)

    model = LeNet5()
    params = model.init(key, jnp.ones([1, 28, 28, 1]))["params"]
    n_params = count_params(params)

    optimizer = optax.adamw(learning_rate=lr, weight_decay=wd)
    opt_state = optimizer.init(params)

    @jax.jit
    def loss_fn(params, x, y):
        logits = model.apply({"params": params}, x)
        return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(logits, y))

    @jax.jit
    def accuracy(params, x, y):
        logits = model.apply({"params": params}, x)
        preds = jnp.argmax(logits, axis=-1)
        return 100.0 * jnp.mean(preds == y)

    @jax.jit
    def step(params, opt_state, x, y):
        loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
        updates, opt_state = optimizer.update(grads, opt_state, params)
        params = optax.apply_updates(params, updates)
        return params, opt_state, loss

    x_tr_j = jnp.array(x_tr)
    y_tr_j = jnp.array(y_tr)
    x_te_j = jnp.array(x_te)
    y_te_j = jnp.array(y_te)

    untrained = float(accuracy(params, x_te_j, y_te_j))

    # Evaluation in chunks to avoid blowing up memory
    def eval_acc(params, x, y, chunk=2000):
        n = len(x)
        correct = 0
        for i in range(0, n, chunk):
            xb, yb = x[i : i + chunk], y[i : i + chunk]
            logits = model.apply({"params": params}, xb)
            preds = jnp.argmax(logits, axis=-1)
            correct += int(jnp.sum(preds == yb))
        return 100.0 * correct / n

    t0 = time.perf_counter()
    for epoch in range(epochs):
        for i in range(0, len(x_tr_j), batch_size):
            params, opt_state, _ = step(
                params, opt_state, x_tr_j[i : i + batch_size], y_tr_j[i : i + batch_size]
            )
    wall = time.perf_counter() - t0

    train_acc = eval_acc(params, x_tr_j, y_tr_j)
    test_acc = eval_acc(params, x_te_j, y_te_j)

    return {
        "seed": seed,
        "lr": lr,
        "wd": wd,
        "epochs": epochs,
        "batch": batch_size,
        "n_params": n_params,
        "untrained": untrained,
        "train_acc": train_acc,
        "test_acc": test_acc,
        "wall_s": wall,
    }


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def exp_4_6_1():
    """Just report the parameter count once."""
    model = LeNet5()
    key = random.PRNGKey(0)
    params = model.init(key, jnp.ones([1, 28, 28, 1]))["params"]
    n = count_params(params)
    breakdown = {k: int(np.prod(v["kernel"].shape) +
                        np.prod(v["bias"].shape)) for k, v in params.items()}
    log_result({"exp": "4.6.1", "n_params": n, "by_layer": breakdown})


def exp_4_6_3():
    """3 seeds at baseline (lr=1e-3, wd=1e-4) and a LR/WD sweep at seed 10."""
    # 3 seeds, baseline
    for seed in (0, 10, 42):
        out = train_lenet(seed=seed, lr=1e-3, wd=1e-4, epochs=10, batch_size=128)
        log_result({"exp": "4.6.3", "sweep": "seeds", **out})

    # LR / WD sweep at seed 10
    for lr in (1e-2, 1e-3, 1e-4):
        for wd in (0.0, 1e-4, 1e-3):
            out = train_lenet(seed=10, lr=lr, wd=wd, epochs=10, batch_size=128)
            log_result({"exp": "4.6.3", "sweep": "lr_wd", **out})


EXPERIMENTS = {
    "4_6_1": exp_4_6_1,
    "4_6_3": exp_4_6_3,
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
