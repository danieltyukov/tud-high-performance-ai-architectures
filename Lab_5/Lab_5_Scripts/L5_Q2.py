"""Exercises 5.1-5.2: CPU/GPU latency, throughput and power for the MLP.

Run on each backend separately (the JAX platform is fixed per process):
    python3 L5_Q2.py --backend cpu --batches 1
    python3 L5_Q2.py --backend gpu --batches 1,8,64,256,1024,4096,16384,65536,262144
Add --sustain 30 to loop the largest batch for ~30 s so nvidia-smi can read
steady-state GPU power from another shell.
"""
import argparse
import json
import time
import jax
import jax.numpy as jnp
import cloudpickle

p = argparse.ArgumentParser()
p.add_argument("--backend", choices=["cpu", "gpu"], required=True)
p.add_argument("--batches", default="1")
p.add_argument("--runs", type=int, default=1000)
p.add_argument("--sustain", type=float, default=0.0)
args = p.parse_args()

jax.config.update("jax_platform_name", args.backend)
dev = jax.devices(args.backend)[0]

with open("mlp_model.pkl", "rb") as f:
    mlp = cloudpickle.load(f)
mlp_jit = jax.jit(mlp)


def bench(bs, runs):
    x = jax.device_put(jnp.ones((bs, 16)), dev)
    mlp_jit(x).block_until_ready()
    best = float("inf")
    for _ in range(runs):
        t = time.perf_counter()
        mlp_jit(x).block_until_ready()
        best = min(best, time.perf_counter() - t)
    return best


for b in args.batches.split(","):
    bs = int(b)
    runs = args.runs if bs <= 8192 else max(50, args.runs * 8192 // bs)
    lat = bench(bs, runs)
    print(json.dumps({"backend": args.backend, "batch": bs,
                      "latency_s": lat, "throughput": bs / lat}), flush=True)

if args.sustain > 0:
    bs = int(args.batches.split(",")[-1])
    x = jax.device_put(jnp.ones((bs, 16)), dev)
    mlp_jit(x).block_until_ready()
    end = time.time() + args.sustain
    while time.time() < end:
        mlp_jit(x).block_until_ready()
