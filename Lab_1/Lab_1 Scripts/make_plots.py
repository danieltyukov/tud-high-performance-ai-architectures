"""Generate the scalability figures used by the Lab 1 report.

TA guidance (Discord, 2026-04-25 evening): plots for scalability are
encouraged; for single-run numbers a table is enough. Hence we keep three
plots that all show how some quantity changes with N (and skip a single-N
optimization-ladder bar chart, since the equivalent table is in the report).
"""

import os

import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report", "lab1", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 120,
    "savefig.bbox": "tight",
})


def fig_q2_scaling():
    """Q2/Q3 coupling time vs N, log-log, with a reference O(N^2) line."""
    Ns = np.array([76, 192, 998])
    coupling_q2 = np.array([4.831, 26.032, 624.182])
    coupling_q3 = np.array([3.098, 19.487, 577.055])
    ref_n2 = coupling_q2[0] * (Ns / Ns[0]) ** 2

    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    ax.loglog(Ns, coupling_q2, "o-", label="Q2 (regular delays)", linewidth=1.8, markersize=7)
    ax.loglog(Ns, coupling_q3, "s--", label="Q3 (zero delays)", linewidth=1.8, markersize=7)
    ax.loglog(Ns, ref_n2, ":", color="gray", label=r"reference $\propto N^2$", linewidth=1.4)
    for x, y in zip(Ns, coupling_q2):
        ax.annotate(f"{y:.1f} s", (x, y), textcoords="offset points", xytext=(8, 4), fontsize=8)
    for x, y in zip(Ns, coupling_q3):
        ax.annotate(f"{y:.1f} s", (x, y), textcoords="offset points", xytext=(8, -12), fontsize=8)
    ax.set_xlabel("Number of centers $N$")
    ax.set_ylabel("calculate_coupling time (s) [log scale]")
    ax.set_xticks(Ns)
    ax.set_xticklabels([str(n) for n in Ns])
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", framealpha=0.95)
    fig.savefig(os.path.join(OUT, "q2_scaling.pdf"))
    fig.savefig(os.path.join(OUT, "q2_scaling.png"))
    plt.close(fig)


def fig_q7_efficiency():
    """Theoretical vs measured Q7-vs-Q6 coupling speedup, across the 3 datasets."""
    datasets = ["TVB76", "TVB192", "TVB998"]
    sparsity_pct = [72.99, 90.42, 96.41]
    theoretical = [3.70, 10.44, 27.86]
    measured = [1.97, 4.95, 17.42]

    x = np.arange(len(datasets))
    w = 0.36
    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    b1 = ax.bar(x - w / 2, theoretical, w, label="theoretical $1/(1-S/100)$", color="#bcd2e8")
    b2 = ax.bar(x + w / 2, measured, w, label="measured Q7-vs-Q6 coupling", color="#1f4e79")
    for bars in (b1, b2):
        for bar in bars:
            ax.annotate(f"{bar.get_height():.1f}×",
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        textcoords="offset points", xytext=(0, 4),
                        ha="center", fontsize=9)
    for i, s in enumerate(sparsity_pct):
        ax.annotate(f"$S={s:.1f}\\%$",
                    (i, max(theoretical[i], measured[i]) * 1.18),
                    ha="center", fontsize=9, color="#444")
    ax.set_xticks(x)
    ax.set_xticklabels(datasets)
    ax.set_ylabel("Coupling speedup (×)")
    ax.set_ylim(0, max(theoretical) * 1.35)
    ax.legend(loc="upper left")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.savefig(os.path.join(OUT, "q7_sparse_efficiency.pdf"))
    fig.savefig(os.path.join(OUT, "q7_sparse_efficiency.png"))
    plt.close(fig)


def fig_optim_scaling():
    """Total simulation time vs N for the four key variants."""
    Ns = np.array([76, 192, 998])
    seq_mlp = np.array([1.104, 4.717, 66.983])
    q6 = np.array([0.0490, 0.1811, 4.9302])
    q7 = np.array([0.0302, 0.0520, 0.3761])
    q9 = np.array([0.0063, 0.0259, 0.7967])

    fig, ax = plt.subplots(figsize=(5.6, 3.7))
    ax.loglog(Ns, seq_mlp, "o-",  label="Sequential MLP (Q5a)",   linewidth=1.8, markersize=7)
    ax.loglog(Ns, q6,      "s--", label="Vectorized dense (Q6)",  linewidth=1.8, markersize=7)
    ax.loglog(Ns, q7,      "^--", label="Vectorized sparse (Q7)", linewidth=1.8, markersize=7)
    ax.loglog(Ns, q9,      "D-",  label="JIT vectorized (Q9)",    linewidth=1.8, markersize=7)
    ax.set_xlabel("Number of centers $N$")
    ax.set_ylabel("Total simulation time (s) [log scale, 15 timesteps]")
    ax.set_xticks(Ns)
    ax.set_xticklabels([str(n) for n in Ns])
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", framealpha=0.95)
    fig.savefig(os.path.join(OUT, "optim_scaling.pdf"))
    fig.savefig(os.path.join(OUT, "optim_scaling.png"))
    plt.close(fig)


if __name__ == "__main__":
    for stale in ("q9_ladder.pdf", "q9_ladder.png"):
        p = os.path.join(OUT, stale)
        if os.path.exists(p):
            os.remove(p)
    fig_q2_scaling()
    fig_q7_efficiency()
    fig_optim_scaling()
    for f in sorted(os.listdir(OUT)):
        print(os.path.join(OUT, f))
