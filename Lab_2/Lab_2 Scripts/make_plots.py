"""Read the JSON-line bench logs and produce the figures for the Lab 2 report.

Inputs (relative to lab2/results/):
    all.jsonl       — Phases A–E from run_all.sh
    extras.jsonl    — Phases C*/D*/E*/F/G/H from run_extras.sh
    q7_run.log      — printed by L2_Q7.py

Outputs (lab2/figures/):
    chunk_sweep_tvb76.png
    chunk_sweep_tvb192.png
    chunk_sweep_tvb998.png  (par_sm)
    summary tables: dumped to summary.txt
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_jsonl(paths: Iterable[str]):
    rows = []
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                rows.append(json.loads(line))
    return rows


def filter_summary(rows, tag, mode=None, dataset=None):
    out = []
    for r in rows:
        if not r.get("summary"):
            continue
        if r.get("tag") != tag:
            continue
        if mode and r.get("mode") != mode:
            continue
        if dataset and r.get("dataset") != dataset:
            continue
        out.append(r)
    return out


def plot_chunk_sweep(rows, dataset, tag, out_path, title):
    pts = sorted(filter_summary(rows, tag, dataset=dataset),
                 key=lambda r: r["chunk"])
    chunks = [r["chunk"] for r in pts]
    times = [r["min_s"] for r in pts]
    plt.figure(figsize=(6, 4))
    plt.plot(chunks, times, marker="o")
    plt.xlabel("chunk size")
    plt.ylabel("simulation time (s)")
    plt.title(title)
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig(out_path, dpi=130)
    plt.close()
    return list(zip(chunks, times))


def main():
    res_dir = sys.argv[1] if len(sys.argv) > 1 else "../results"
    fig_dir = sys.argv[2] if len(sys.argv) > 2 else "../figures"
    os.makedirs(fig_dir, exist_ok=True)

    rows = load_jsonl([
        os.path.join(res_dir, "all.jsonl"),
        os.path.join(res_dir, "extras.jsonl"),
    ])
    print(f"loaded {len(rows)} json records")

    summary = []

    pts76 = plot_chunk_sweep(
        rows, "tvb76", "B_sweep76",
        os.path.join(fig_dir, "chunk_sweep_tvb76.png"),
        "tvb_par.py — chunk-size sweep (TVB76, 15 ms)",
    )
    pts192 = plot_chunk_sweep(
        rows, "tvb192", "B_sweep192",
        os.path.join(fig_dir, "chunk_sweep_tvb192.png"),
        "tvb_par.py — chunk-size sweep (TVB192, 15 ms)",
    )

    summary.append("# Phase B chunk sweeps (single rep each):")
    summary.append(f"  TVB76 : {pts76}")
    summary.append(f"  TVB192: {pts192}")

    # par_sm sweep on tvb998
    pts998 = sorted(filter_summary(rows, "D_sm_sweep998", dataset="tvb998"),
                    key=lambda r: r["chunk"])
    if pts998:
        plt.figure(figsize=(6, 4))
        plt.plot([r["chunk"] for r in pts998],
                 [r["min_s"] for r in pts998], marker="o")
        plt.xlabel("chunk size"); plt.ylabel("simulation time (s)")
        plt.title("tvb_par_sm.py — chunk-size sweep (TVB998, 15 ms)")
        plt.grid(True, alpha=0.4); plt.tight_layout()
        plt.savefig(os.path.join(fig_dir, "chunk_sweep_tvb998_sm.png"), dpi=130)
        plt.close()
        summary.append(f"  TVB998 par_sm sweep: "
                       f"{[(r['chunk'], r['min_s']) for r in pts998]}")

    pts998i = sorted(filter_summary(rows, "E_smi_sweep998", dataset="tvb998"),
                     key=lambda r: r["chunk"])
    if pts998i:
        summary.append(f"  TVB998 par_smi sweep: "
                       f"{[(r['chunk'], r['min_s']) for r in pts998i]}")

    summary.append("")
    summary.append("# Headline timings (min of 3):")
    for tag in ("A_seq", "A_par40", "Cstar_15", "Cstar_60",
                "Dstar_par_sm", "Estar_par_smi", "F_q6", "H_thr"):
        for r in filter_summary(rows, tag):
            summary.append(
                f"  {tag:14s} {r['mode']:8s} {r['dataset']:7s} "
                f"tf={r['tf']:>4} chunk={r['chunk']} "
                f"min={r['min_s']:.3f}s mean={r['mean_s']:.3f}s"
            )

    out_txt = os.path.join(fig_dir, "summary.txt")
    with open(out_txt, "w") as f:
        f.write("\n".join(summary))
    print("\n".join(summary))
    print(f"\nwrote {out_txt}")


if __name__ == "__main__":
    main()
