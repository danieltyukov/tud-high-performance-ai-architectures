"""Plots for the Lab 3 report.

Reads results/all.jsonl and figures/q15_nvprof.txt, q33_nvprof.txt, then
writes:
  figures/scaling_dataset.png   -- runtime vs dataset for every impl
  figures/q15_breakdown.png     -- GPU time breakdown for L3_Q1 on TVB192
  figures/q33_breakdown.png     -- GPU time breakdown for L3_Q2 K=100
  figures/throughput_q2.png     -- throughput vs K
"""
import json
import os
import re

import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS = os.path.join(ROOT, "results")
FIGURES = os.path.join(ROOT, "figures")
os.makedirs(FIGURES, exist_ok=True)


def load_rows():
    rows = []
    with open(os.path.join(RESULTS, "all.jsonl")) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def plot_scaling(rows):
    impls = ["vec_baseline", "vec_full", "cupy", "numba_cuda",
             "jax_cpu", "jax_gpu"]
    pretty = {
        "vec_baseline": "vec (baseline)",
        "vec_full":     "vec (refactored)",
        "cupy":         "CuPy",
        "numba_cuda":   "Numba @cuda.jit",
        "jax_cpu":      "JAX CPU",
        "jax_gpu":      "JAX GPU",
    }
    datasets = ["tvb76", "tvb192", "tvb998"]
    x = np.arange(len(datasets))

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    width = 0.13
    for i, impl in enumerate(impls):
        ts = []
        for ds in datasets:
            t = next((r["min_s"] for r in rows
                     if r["impl"] == impl and r["dataset"] == ds), None)
            ts.append(t if t is not None else float("nan"))
        ax.bar(x + (i - len(impls) / 2 + 0.5) * width, ts, width,
               label=pretty[impl])
    ax.set_yscale("log")
    ax.set_xticks(x); ax.set_xticklabels([d.upper() for d in datasets])
    ax.set_ylabel("min wall time (s, log scale)")
    ax.set_title("TVB simulation, 150 ms, T4 GPU vs CPU (3 reps, min)")
    ax.legend(ncol=3, fontsize=8)
    ax.grid(axis="y", which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "scaling_dataset.png"), dpi=150)
    plt.close(fig)


def parse_nvprof(path):
    """Return list of (name, time_ms, percent) sorted by time desc, plus a
    summary dict with htod_us/dtoh_us/total_ms/utilization estimate."""
    with open(path) as f:
        text = f.read()

    # nvprof prints two blocks under "GPU activities:" -- the main profile
    # and a per-NVTX-range duplicate. We only want the first.
    if "NVTX result:" in text:
        text = text.split("NVTX result:", 1)[0]

    # Lines look like:
    #   59.85%  578.51ms  2999  192.90us  ...  volta_dgemm_64x64_nn
    rows = []
    in_gpu = False
    for line in text.splitlines():
        if "GPU activities:" in line:
            in_gpu = True
            line = line.split("GPU activities:", 1)[1]
        elif "API calls:" in line:
            in_gpu = False
        if not in_gpu:
            continue
        m = re.match(
            r"\s*([\d.]+)%\s+([\d.]+)(us|ms|s)\s+\d+\s+\S+\s+\S+\s+\S+\s+(.+)",
            line)
        if not m:
            continue
        pct = float(m.group(1))
        val = float(m.group(2))
        unit = m.group(3)
        name = m.group(4).strip()
        ms = val * (1 if unit == "ms" else (1e3 if unit == "s" else 1e-3))
        rows.append((name, ms, pct))
    return rows


def shorten(name):
    if "dgemm_64x64_nn" in name: return "dgemm (matmul nn)"
    if "dgemm_64x64_nt" in name: return "dgemm (matmul nt)"
    if "DeviceSegmentedReduce" in name or "ReduceKernel" in name:
        return "segmented reduce"
    if "memcpy HtoD" in name: return "memcpy HtoD"
    if "memcpy DtoH" in name: return "memcpy DtoH"
    if "memset" in name: return "memset"
    if name.startswith("cupy_take"): return "cupy_take (gather)"
    return name.split("__")[0].replace("cupy_", "cupy: ")


def plot_breakdown(nvprof_path, out_name, title):
    rows = parse_nvprof(nvprof_path)
    if not rows:
        return
    # Group by short name.
    groups = {}
    for name, ms, pct in rows:
        s = shorten(name)
        groups[s] = groups.get(s, 0.0) + pct
    items = sorted(groups.items(), key=lambda x: -x[1])

    # Keep top 8, lump the rest.
    top = items[:8]
    rest = sum(p for _, p in items[8:])
    if rest > 0:
        top.append(("(other)", rest))

    labels = [n for n, _ in top]
    pcts = [p for _, p in top]

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.barh(range(len(labels)), pcts)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("% of GPU activity time")
    ax.set_title(title)
    for i, p in enumerate(pcts):
        ax.text(p + 0.5, i, f"{p:.2f}%", va="center", fontsize=8)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, out_name), dpi=150)
    plt.close(fig)


def plot_throughput(rows):
    bs = sorted([r for r in rows if r["impl"] == "cupy_batched"],
                key=lambda r: r["K"])
    if not bs: return

    Ks = [r["K"] for r in bs]
    thr_batched = [r["iters_per_s"] for r in bs]

    # Back-to-back single CuPy throughput on TVB192.
    cupy_192 = next(r for r in rows if r["impl"] == "cupy" and r["dataset"] == "tvb192")
    T = int(150 / 0.05)
    thr_single = T / cupy_192["min_s"]   # single sim throughput, iter/s

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.bar([f"K={k}" for k in Ks], thr_batched, label="batched (L3_Q2)")
    ax.axhline(thr_single, ls="--", color="C3",
               label=f"L3_Q1 back-to-back ({thr_single:.0f} iters/s)")
    ax.set_ylabel("simulation iterations per second")
    ax.set_title("Throughput on TVB192, 150 ms")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURES, "throughput_q2.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    rows = load_rows()
    plot_scaling(rows)
    plot_breakdown(os.path.join(FIGURES, "q15_nvprof.txt"),
                   "q15_breakdown.png",
                   "L3_Q1 (CuPy) on TVB192 — GPU activity breakdown")
    plot_breakdown(os.path.join(FIGURES, "q33_nvprof.txt"),
                   "q33_breakdown.png",
                   "L3_Q2 (CuPy batched, K=100) — GPU activity breakdown")
    plot_throughput(rows)
    print("plots written to", FIGURES)
