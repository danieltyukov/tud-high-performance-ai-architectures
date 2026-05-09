#!/usr/bin/env bash
# Lab 3 measurement runner — executes every benchmark we need for the
# report and writes one JSON line per measurement to results/.
set -uo pipefail

cd "$(dirname "$0")"
mkdir -p results figures

DATASETS=(tvb76 tvb192 tvb998)
TF=150
REPS=3
LOG=results

run() {
    echo "=== $* ==="
    "$@" 2>&1 | tee -a "$LOG/all.log"
}

# Q3.1.1 baseline tvb_vec.py
for ds in "${DATASETS[@]}"; do
    run python3 bench_vec.py "$ds" --tf "$TF" --reps "$REPS"
done

# Q3.1.2 fully vectorised numpy
for ds in "${DATASETS[@]}"; do
    run python3 tvb_vec_full.py "$ds" --tf "$TF" --reps "$REPS"
done

# Q3.1.3 CuPy
for ds in "${DATASETS[@]}"; do
    run python3 L3_Q1.py "$ds" --tf "$TF" --reps "$REPS" --warmup 1
done

# Q3.2 batched CuPy
for K in 100 250 500; do
    run python3 L3_Q2.py tvb192 --K "$K" --tf "$TF" --reps "$REPS" --warmup 1
done

# Q3.4 numba @cuda.jit
for ds in "${DATASETS[@]}"; do
    run python3 L3_Q4.py "$ds" --tf "$TF" --reps "$REPS" --warmup 1
done

# Q3.5 JAX cpu and gpu
for plat in cpu gpu; do
    for ds in "${DATASETS[@]}"; do
        run python3 L3_Q5.py "$ds" --platform "$plat" --tf "$TF" --reps "$REPS" --warmup 1
    done
done

echo "=== done ==="
