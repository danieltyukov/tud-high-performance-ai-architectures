# Exercise 6.2: profile the baseline (Q6.2.1) then time every backend over the
# n_cells sweep (Q6.2.3/6.2.4). Metric is wall time per step in us; the real-time
# budget is one step per delta = 10 us of brain time, and 1 s of brain time is
# 100000 steps. Run `python3 L6_Q2.py`, or pass --backends to limit it.
import argparse
import cProfile
import json
import pstats
import io as _io
import time
import warnings
import numpy as np

import io_fast as f
from bench_baseline import run_baseline

warnings.filterwarnings('ignore')  # large-N divergence gives inf/nan, timing still valid

N_PER_S = int(1.0 * 1000 / 0.01 + 0.5)   # 100000 steps = 1 s brain time


def profile_baseline(n_cells=30, sim_seconds=0.05):
    # Q6.2.1: cProfile the baseline and print the hotspots
    pr = cProfile.Profile()
    pr.enable()
    run_baseline(n_cells, sim_seconds=sim_seconds, delta=0.01)
    pr.disable()
    s = _io.StringIO()
    pstats.Stats(pr, stream=s).sort_stats('tottime').print_stats(6)
    print(f'== Q6.2.1 baseline profile (N={n_cells}, {int(sim_seconds*1000/0.01)} steps) ==')
    for line in s.getvalue().splitlines():
        if 'io_model.py' in line or 'function calls' in line:
            print(line)
    print()


def bench_one(backend, n_cells, meas_seconds, warm=True):
    # mean us/step for one backend at n_cells
    delta = 0.01
    if backend == 'baseline':
        et, _ = run_baseline(n_cells, sim_seconds=meas_seconds, delta=delta)
        steps = int(meas_seconds * 1000 / delta + 0.5)
        return et / steps * 1e6
    fn = {'numpy': f.run_numpy, 'numba': f.run_numba, 'jax': f.run_jax}[backend]
    if warm and backend in ('numba', 'jax'):
        fn(n_cells, sim_seconds=0.005, delta=delta)   # compile at this N (jax recompiles per shape)
    best = np.inf
    reps = 3 if backend != 'baseline' else 1
    for _ in range(reps):
        tic = time.perf_counter()
        fn(n_cells, sim_seconds=meas_seconds, delta=delta)
        dt = time.perf_counter() - tic
        best = min(best, dt)
    steps = int(meas_seconds * 1000 / delta + 0.5)
    return best / steps * 1e6


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='../results/sweep.jsonl')
    ap.add_argument('--backends', default='baseline,numpy,numba,jax')
    ap.add_argument('--label', default='cpu')   # 'cpu' or 'gpu' (host tag)
    ap.add_argument('--no-profile', action='store_true', help='skip the Q6.2.1 profile step')
    args = ap.parse_args()

    if not args.no_profile and 'baseline' in args.backends:
        profile_baseline()

    sweep = [1, 2, 10, 30, 100, 1000, 10000, 100000]
    # per backend: largest N to attempt, and run length in brain-seconds per N
    limits = {
        'baseline': (100,    {1: 0.5, 2: 0.5, 10: 0.2, 30: 0.1, 100: 0.05}),
        'numpy':    (100000, {n: (0.1 if n <= 1000 else 0.02) for n in sweep}),
        'numba':    (100000, {n: (0.1 if n <= 1000 else 0.02) for n in sweep}),
        'jax':      (100000, {n: 0.1 for n in sweep}),
    }

    rows = []
    for backend in args.backends.split(','):
        nmax, lens = limits[backend]
        for n in sweep:
            if n > nmax:
                continue
            ms = lens.get(n, 0.02)
            try:
                us = bench_one(backend, n, ms)
            except Exception as e:
                print(f'{backend} n={n}: FAILED {e}')
                continue
            total_s = us * N_PER_S / 1e6
            row = dict(backend=backend, host=args.label, n_cells=n,
                       us_per_step=round(us, 4), total_1s_brain_s=round(total_s, 4),
                       meas_seconds=ms)
            rows.append(row)
            print(f'{backend:9s} n={n:6d}  {us:9.2f} us/step   1s-brain={total_s:9.2f}s')

    with open(args.out, 'a') as fh:
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    print(f'\nwrote {len(rows)} rows to {args.out}')
