import json
import matplotlib.pyplot as plt

RESULTS = "../results"
FIG = "../figures"


def load(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def throughput_figure():
    cg = load(f"{RESULTS}/cpu_gpu_sweep.jsonl")
    tpu = load(f"{RESULTS}/tpu_sweep.jsonl")
    cpu = [r for r in cg if r["backend"] == "cpu"]
    gpu = [r for r in cg if r["backend"] == "gpu"]

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for data, label, marker in [(cpu, "CPU (Xeon, 8 vCPU)", "o"),
                                (gpu, "GPU (Tesla T4)", "s"),
                                (tpu, "TPUv2 (NeuSim)", "^")]:
        ax.plot([r["batch"] for r in data],
                [r["throughput"] for r in data],
                marker=marker, label=label)
    ax.axvline(1024, color="gray", ls=":", lw=0.8)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("Batch size")
    ax.set_ylabel("Throughput (inferences/s)")
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(f"{FIG}/throughput_sweep.png", dpi=150)
    print("wrote throughput_sweep.png")


def tpu_bound_figure():
    tpu = load(f"{RESULTS}/tpu_sweep.jsonl")
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    b = [r["batch"] for r in tpu]
    lat = [r["exec_ns"] for r in tpu]
    colors = ["tab:blue" if r["bounded_by"] == "Memory" else "tab:red" for r in tpu]
    ax.scatter(b, lat, c=colors, zorder=3)
    ax.plot(b, lat, color="gray", lw=0.8, zorder=2)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("Batch size")
    ax.set_ylabel("Inference latency (ns)")
    ax.grid(True, which="both", ls="--", alpha=0.3)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([], [], marker="o", ls="", color="tab:blue", label="memory-bound"),
                       Line2D([], [], marker="o", ls="", color="tab:red", label="compute-bound")],
              fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(f"{FIG}/tpu_roofline.png", dpi=150)
    print("wrote tpu_roofline.png")


if __name__ == "__main__":
    throughput_figure()
    tpu_bound_figure()
