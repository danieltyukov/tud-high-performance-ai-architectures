# Lab 6 code — accelerating the Inferior-Olive simulator

The provided `io_model.py` (sequential de Gruijl IO network) is accelerated with
vectorisation, an O(N) mean-field gap junction, JIT compilation, and a GPU
backend. Files follow the `L6_Qx.py` convention; the rest are shared modules.

| File | Exercise | What it does |
|------|----------|--------------|
| `L6_Q1.py` | 6.1 | Parameter exploration. Sweeps `sim_seconds`, `delta`, `n_cells`, `enable_gapjunctions`, `g_CaL`, `I_pulse10ms` and reports soma-trace morphology (amplitude, spike count, dominant frequency, population synchrony). |
| `L6_Q2.py` | 6.2 | Profiles the baseline (cProfile, Q6.2.1) then times every backend over `N = [1,2,10,30,100,1000,10000,100000]`, Q6.2.3/6.2.4. Metric: µs per simulation step. Writes `../results/sweep.jsonl`. |
| `io_fast.py` | 6.2 | The accelerated simulator (shared module). Three backends over one vectorised step: `run_numpy`, `run_numba` (`@njit`), `run_jax` (`jit`+`lax.scan`, CPU/GPU). Gap junction reduced from O(N²) all-to-all to the O(N) mean field `C_gap·(N·V_d − ΣV_d)`. |
| `bench_baseline.py` | 6.2.1 | Drives/profiles the original `io_model.py` (imports it and monkey-patches its globals, so timings reflect the unmodified code). Used by `L6_Q2.py`. |
| `make_figures.py` | — | Builds the three report figures from `../results/sweep.jsonl` plus fresh short runs. |
| `io_model.py` | — | The provided sequential simulator (unmodified), kept here so the scripts run out-of-the-box. |

## Reproduce (run from this directory)

```bash
python3 L6_Q1.py                                   # 6.1 morphology table
python3 L6_Q2.py                                   # 6.2.1 profile + full CPU sweep
python3 L6_Q2.py --backends jax --label gpu --out results/sweep_gpu.jsonl   # T4 GPU sweep
python3 make_figures.py                            # report figures
```

## Validation & numerical note

At `N=1` (no coupling) every backend matches `io_model.py` to ~1e-14 mV. At
`N>1` the only change is the gap junction moving from a within-step Gauss–Seidel
sweep to a Jacobi update (max Δ = 0.02 mV, corr = 1.0000 at N=30). With the fixed
`C_gap`, forward-Euler is stable only for `N < 2/(δ·C_gap) = 4000`; beyond that the
trajectory diverges (timing is unaffected). See the report for details.
