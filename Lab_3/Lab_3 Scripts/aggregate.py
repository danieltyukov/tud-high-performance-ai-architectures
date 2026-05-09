"""Aggregate per-question logs in results/ into one JSONL and pretty-print
a small summary that the report can refer to."""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
RESULTS = os.path.join(ROOT, "results")


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(RESULTS, "*.log"))):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("{") and '"impl"' in line:
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

    out = os.path.join(RESULTS, "all.jsonl")
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} rows to {out}\n")

    # Print a tabular summary for the report.
    by_impl = {}
    for r in rows:
        key = r["impl"]
        by_impl.setdefault(key, []).append(r)

    for impl in ("vec_baseline", "vec_full", "cupy", "numba_cuda",
                 "jax_cpu", "jax_gpu"):
        if impl not in by_impl:
            continue
        print(f"--- {impl} ---")
        for r in by_impl[impl]:
            ds = r["dataset"]
            t = r["min_s"]
            print(f"  {ds:8s} tf={r['tf']:.0f}ms  min={t:8.4f}s")
        print()

    if "cupy_batched" in by_impl:
        print("--- cupy_batched (Q3.2, tvb192) ---")
        for r in by_impl["cupy_batched"]:
            print(f"  K={r['K']:4d}  min={r['min_s']:8.3f}s  "
                  f"throughput={r['iters_per_s']:8.1f} iters/s")
        print()


if __name__ == "__main__":
    main()
