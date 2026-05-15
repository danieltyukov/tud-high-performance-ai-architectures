"""
Build figures for the Lab 4 report from the JSONL result files.
Reads:
    Lab_4/results/q4_results.jsonl
    Lab_4/results/q5_results.jsonl
    Lab_4/results/q6_results.jsonl
Writes:
    Lab_4/figures/q444_batch_sweep.png
    Lab_4/figures/q445_lr_sweep.png
    Lab_4/figures/q463_lr_wd_heatmap.png
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def load(path):
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def q444_batch_sweep():
    rows = [r for r in load(RES / "q4_results.jsonl") if r["exp"] == "4.4.4"]
    if not rows:
        print("[q444] no rows yet")
        return
    rows.sort(key=lambda r: r["batch"])
    bs = [r["batch"] for r in rows]
    tr = [r["train_acc"] for r in rows]
    te = [r["test_acc"] for r in rows]

    x = np.arange(len(bs))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    w = 0.38
    ax.bar(x - w / 2, tr, w, label="train", color="#1f77b4")
    ax.bar(x + w / 2, te, w, label="test", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(bs)
    ax.set_xlabel("Batch size")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Q4.4 (4): batch size sweep, lr=1e-3, 10 epochs")
    ax.legend(loc="lower left")
    for xi, val in zip(x - w / 2, tr):
        ax.text(xi, val + 1, f"{val:.1f}", ha="center", fontsize=8)
    for xi, val in zip(x + w / 2, te):
        ax.text(xi, val + 1, f"{val:.1f}", ha="center", fontsize=8)
    plt.tight_layout()
    out = FIG / "q444_batch_sweep.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[q444] -> {out}")


def q445_lr_sweep():
    rows = [r for r in load(RES / "q4_results.jsonl") if r["exp"] == "4.4.5"]
    if not rows:
        print("[q445] no rows yet")
        return
    rows.sort(key=lambda r: r["lr"])
    lrs = [r["lr"] for r in rows]
    tr = [r["train_acc"] for r in rows]
    te = [r["test_acc"] for r in rows]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(lrs, tr, "o-", label="train", color="#1f77b4")
    ax.plot(lrs, te, "s-", label="test", color="#ff7f0e")
    ax.set_xscale("log")
    ax.set_xlabel("Learning rate")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Q4.4 (5): lr sweep at batch=64, 10 epochs")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    out = FIG / "q445_lr_sweep.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[q445] -> {out}")


def q463_lr_wd_heatmap():
    rows = [r for r in load(RES / "q6_results.jsonl")
            if r.get("exp") == "4.6.3" and r.get("sweep") == "lr_wd"]
    if not rows:
        print("[q463] no rows yet")
        return
    lrs = sorted({r["lr"] for r in rows}, reverse=True)
    wds = sorted({r["wd"] for r in rows})
    mat = np.full((len(lrs), len(wds)), np.nan)
    for r in rows:
        i = lrs.index(r["lr"])
        j = wds.index(r["wd"])
        mat[i, j] = r["test_acc"]

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    im = ax.imshow(mat, cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(wds)))
    ax.set_xticklabels([f"{w:g}" for w in wds])
    ax.set_yticks(range(len(lrs)))
    ax.set_yticklabels([f"{l:g}" for l in lrs])
    ax.set_xlabel("Weight decay")
    ax.set_ylabel("Learning rate")
    ax.set_title("Q4.6 (3): LeNet-5 test accuracy, lr x wd")
    for i in range(len(lrs)):
        for j in range(len(wds)):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                    color="white" if mat[i, j] < 90 else "black", fontsize=9)
    fig.colorbar(im, ax=ax, label="Test acc (%)")
    plt.tight_layout()
    out = FIG / "q463_lr_wd_heatmap.png"
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"[q463] -> {out}")


def main():
    q444_batch_sweep()
    q445_lr_sweep()
    q463_lr_wd_heatmap()


if __name__ == "__main__":
    main()
