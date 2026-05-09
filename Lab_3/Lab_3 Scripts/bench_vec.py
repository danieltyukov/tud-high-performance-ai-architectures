"""Q3.1.1 — time the unmodified tvb_vec.simulate on TVB76/192/998 at 150ms."""
import argparse
import json
import time

import tvb_vec
from lib import data


def _load(name):
    if name == "tvb76":  return data.tvb76_weights_lengths()
    if name == "tvb192": return data.tvb192_weights_lengths()
    if name == "tvb998": return data.tvb998_weights_lengths()
    raise SystemExit(f"unknown dataset {name}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dataset", choices=["tvb76", "tvb192", "tvb998"])
    p.add_argument("--tf", type=float, default=150.0)
    p.add_argument("--dt", type=float, default=0.05)
    p.add_argument("--speed", type=float, default=4.0)
    p.add_argument("--reps", type=int, default=3)
    args = p.parse_args()

    W, D = _load(args.dataset)
    N, M = W.shape[0], 2

    times = []
    for _ in range(args.reps):
        t0 = time.time()
        tvb_vec.simulate(W, D, N, M, args.dt, args.tf, args.speed)
        times.append(time.time() - t0)

    print(json.dumps({
        "impl": "vec_baseline", "dataset": args.dataset, "tf": args.tf,
        "reps": args.reps, "min_s": min(times), "all_s": times,
    }))
