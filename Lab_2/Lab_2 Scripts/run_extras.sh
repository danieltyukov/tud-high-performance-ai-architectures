#!/usr/bin/env bash
# Round-2 measurements: re-run at the actual optimal chunks (TVB76=40,
# TVB192=128) and add the Q6/Q7/Q8 numbers needed for the report.
set -euo pipefail
cd "$(dirname "$0")"
export MPLBACKEND=Agg
export PYTHONUNBUFFERED=1
run() { echo "# $* @ $(date -u +%H:%M:%S)" >&2; python3 bench.py "$@"; }

#### Phase C* — Q2.2.4: 60 ms at the *actual* optimal chunk ####
run par tvb76  15 40  --repeats 3 --tag Cstar_15
run par tvb76  60 40  --repeats 3 --tag Cstar_60
run par tvb192 15 128 --repeats 3 --tag Cstar_15
run par tvb192 60 128 --repeats 3 --tag Cstar_60

#### Phase D* — Q2.3 par_sm at correct chunks ####
run par_sm tvb76  15 40  --repeats 3 --tag Dstar_par_sm
run par_sm tvb192 15 128 --repeats 3 --tag Dstar_par_sm
# tvb998 best chunk picked from D_sm_sweep998 in run_all.sh; we'll do
# a 3-rep follow-up after inspecting that sweep.

#### Phase E* — Q2.4 par_smi at correct chunks ####
run par_smi tvb76  15 40  --repeats 3 --tag Estar_par_smi
run par_smi tvb192 15 128 --repeats 3 --tag Estar_par_smi

#### Phase F — Q2.6 (L2_Q6) timings ####
for ds_chunk in "tvb76 40" "tvb192 128" "tvb998 256"; do
  read -r ds chunk <<< "$ds_chunk"
  echo "# Q6 $ds chunk=$chunk @ $(date -u +%H:%M:%S)" >&2
  for r in 0 1 2; do
    python3 - <<PY
import os, sys, time, json
sys.path.insert(0, '.')
from lib import data
import L2_Q6
loader = {'tvb76': data.tvb76_weights_lengths,
          'tvb192': data.tvb192_weights_lengths,
          'tvb998': data.tvb998_weights_lengths}['$ds']
W, D = loader()
t0 = time.time()
L2_Q6.simulate(W, D, 0.05, 15.0, 4.0, $chunk)
elapsed = time.time() - t0
print(json.dumps({'mode': 'L2_Q6', 'dataset': '$ds', 'tf': 15.0,
                  'chunk': $chunk, 'rep': $r, 'time_s': elapsed,
                  'tag': 'F_q6'}), flush=True)
PY
  done
done

#### Phase G — Q2.7 (L2_Q7) 200 sims ####
# We measure only the parallel-of-sims wall time. The "Q6 200x back-to-back"
# baseline is computed in fill_report.py as 200 * T_one_Q6 from Phase F to
# avoid burning the AWS budget on a redundant serial sweep.
echo "# Q7 200 sims @ $(date -u +%H:%M:%S)" >&2
python3 -u L2_Q7.py --dataset tvb192 --n 200 --tf 15 --chunk 128 \
  > ../results/q7_run.log 2>&1

#### Phase H — Q2.8 (L2_Q8 multithreaded) ####
for ds_tf in "tvb76 15" "tvb76 60" "tvb192 15" "tvb192 60"; do
  read -r ds tf <<< "$ds_tf"
  chunk=40
  [ "$ds" = "tvb192" ] && chunk=128
  run thr "$ds" "$tf" "$chunk" --repeats 3 --tag H_thr
done

#### Phase I — Q2.2.5 py-spy profiling at the optimal chunk (TVB192/128) ####
echo "# py-spy record TVB192 chunk=128 @ $(date -u +%H:%M:%S)" >&2
PYSPY=$HOME/.local/bin/py-spy
"$PYSPY" record -d 25 -o ../figures/pyspy_flame.svg --format flamegraph -- \
  python3 bench.py par tvb192 15 128 --repeats 1 --tag I_pyspy \
  > ../results/pyspy_run.log 2>&1 || true
# Render flame graph to PNG for inclusion in the LaTeX report.
convert -density 200 ../figures/pyspy_flame.svg ../figures/pyspy_top.png \
  >> ../results/pyspy_run.log 2>&1 || true

# Validation run for Q2.6 numerical equivalence.
echo "# validate_q6 @ $(date -u +%H:%M:%S)" >&2
python3 validate_q6.py > ../results/validate_q6.txt 2>&1 || true

echo "# EXTRAS DONE @ $(date -u +%H:%M:%S)" >&2
