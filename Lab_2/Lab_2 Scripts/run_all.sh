#!/usr/bin/env bash
# Driver for all Lab 2 measurements. Streams JSON-line results to stdout
# (which the caller should tee to a file). Each phase is annotated with --tag
# so we can grep one phase out of the combined log later.
set -euo pipefail

cd "$(dirname "$0")"
export MPLBACKEND=Agg
export PYTHONUNBUFFERED=1

run() { echo "# $* @ $(date -u +%H:%M:%S)" >&2; python3 bench.py "$@"; }

#### Phase A — Q2.2.2: sequential MLP vs tvb_par at default chunk=40 ####
for ds in tvb76 tvb192; do
  run seq_mlp "$ds" 15 --repeats 3 --tag A_seq
  run par     "$ds" 15 40 --repeats 3 --tag A_par40
done

#### Phase B — Q2.2.3: chunk sweep ####
for c in 2 4 8 16 24 32 40 48 56 64 76; do
  run par tvb76 15 "$c" --repeats 1 --tag B_sweep76
done
for c in 2 4 8 16 32 48 64 96 128 160 192; do
  run par tvb192 15 "$c" --repeats 1 --tag B_sweep192
done

#### Phase C — Q2.2.4: optimal chunk at 60ms ####
# Optimal chunks are filled in by the caller after Phase B completes; we
# default to the values most likely to win (largest = N) so the script is
# self-contained even without re-running.
for ds_chunk in "tvb76 76" "tvb192 192"; do
  read -r ds chunk <<< "$ds_chunk"
  run par "$ds" 15 "$chunk" --repeats 3 --tag C_opt15
  run par "$ds" 60 "$chunk" --repeats 3 --tag C_opt60
done

#### Phase D — Q2.3: shared memory ####
for ds_chunk in "tvb76 76" "tvb192 192"; do
  read -r ds chunk <<< "$ds_chunk"
  run par_sm "$ds" 15 "$chunk" --repeats 3 --tag D_par_sm
done
for c in 32 64 128 256 512; do
  run par_sm tvb998 15 "$c" --repeats 1 --tag D_sm_sweep998
done

#### Phase E — Q2.4: shared memory + initializer ####
for ds_chunk in "tvb76 76" "tvb192 192"; do
  read -r ds chunk <<< "$ds_chunk"
  run par_smi "$ds" 15 "$chunk" --repeats 3 --tag E_par_smi
done
for c in 32 64 128 256 512; do
  run par_smi tvb998 15 "$c" --repeats 1 --tag E_smi_sweep998
done
# Then 3 reps at the best chunk for tvb998 will be filled in afterwards.

echo "# DONE @ $(date -u +%H:%M:%S)" >&2
