# Builds the report figures from results/sweep.jsonl plus short fresh runs.
import json
import warnings
import io as _io
import cProfile
import pstats
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io_fast as f
from bench_baseline import run_baseline

warnings.filterwarnings('ignore')
FIG = '../figures'
plt.rcParams.update({'font.size': 10, 'axes.grid': True, 'grid.alpha': 0.3,
                     'figure.dpi': 130, 'savefig.bbox': 'tight'})

def load_sweep():
    rows = [json.loads(l) for l in open('../results/sweep.jsonl')]
    by = {}
    for r in rows:
        key = r['backend'] if r['host'] == 'cpu' else r['backend'] + '-gpu'
        by.setdefault(key, []).append((r['n_cells'], r['us_per_step']))
    for k in by:
        by[k].sort()
    return by

# figure 1: baseline profile breakdown and scaling
def fig_profile():
    pr = cProfile.Profile()
    pr.enable()
    run_baseline(n_cells=30, sim_seconds=0.05, delta=0.01)
    pr.disable()
    st = pstats.Stats(pr)
    tt = {}
    for (fn, line, name), (cc, nc, tot, cum, callers) in st.stats.items():
        if 'io_model.py' in fn and name.startswith('update_'):
            tt[name] = tot
    names = ['update_dend', 'update_soma', 'update_axon']
    vals = [tt.get(n, 0) for n in names]

    by = load_sweep()
    base = by['baseline']
    bn = [n for n, _ in base]; bt = [t for _, t in base]

    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    colors = ['#c0392b', '#2980b9', '#27ae60']
    ax[0].bar([n.replace('update_', '') for n in names], vals, color=colors)
    tot = sum(vals)
    for i, v in enumerate(vals):
        ax[0].text(i, v, f'{v/tot*100:.0f}%', ha='center', va='bottom', fontsize=9)
    ax[0].set_ylabel('cumulative time (s)')
    ax[0].set_title('(a) Sequential hotspots, $N=30$')

    ax[1].loglog(bn, bt, 'o-', color='#c0392b', label='baseline (measured)')
    # O(N) and O(N^2) guides anchored at N=10
    n0, t0 = bn[2], bt[2]
    xs = np.array(bn, float)
    ax[1].loglog(xs, t0 * (xs / n0), '--', color='gray', alpha=0.7, label='$O(N)$')
    ax[1].loglog(xs, t0 * (xs / n0)**2, ':', color='black', alpha=0.7, label='$O(N^2)$')
    ax[1].set_xlabel('number of cells $N$'); ax[1].set_ylabel('wall time / step (µs)')
    ax[1].set_title('(b) Baseline scaling'); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(f'{FIG}/fig_profile.png'); plt.close(fig)
    print('wrote fig_profile.png', {n: round(v, 2) for n, v in zip(names, vals)})

# figure 2: per-step wall time vs N for all backends
def fig_scaling():
    by = load_sweep()
    style = {
        'baseline': ('baseline (sequential)', 'o-', '#c0392b'),
        'numpy':    ('NumPy (vectorised)',    's-', '#8e44ad'),
        'numba':    ('Numba JIT (CPU)',       '^-', '#2980b9'),
        'jax':      ('JAX/XLA (CPU)',         'D-', '#16a085'),
        'jax-gpu':  ('JAX/XLA (GPU, T4)',     'v-', '#e67e22'),
    }
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for key, (lab, mk, col) in style.items():
        if key not in by:
            continue
        ns = [n for n, _ in by[key]]; ts = [t for _, t in by[key]]
        ax.loglog(ns, ts, mk, color=col, label=lab, markersize=5)
    ax.axhline(10, color='black', ls='--', lw=1, alpha=0.6)
    ax.text(1.2, 11, 'real-time budget (10 µs/step)', fontsize=8)
    ax.set_xlabel('number of cells $N$')
    ax.set_ylabel('wall time per simulation step (µs)')
    ax.set_title('Per-step cost vs. population size')
    ax.legend(fontsize=8, loc='upper left')
    fig.tight_layout(); fig.savefig(f'{FIG}/fig_scaling.png'); plt.close(fig)
    print('wrote fig_scaling.png')

# figure 3: g_CaL firing modes, gap-junction synchrony, and validation
def fig_morphology():
    D = 0.01
    t = np.arange(int(0.6 * 1000 / D + 0.5)) * D  # 0.6 s window in ms
    fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.2))

    # (a) g_CaL firing modes, single cell
    for g, c in [(0.7, '#2980b9'), (1.8, '#e67e22'), (2.0, '#c0392b')]:
        tr = f.run_numpy(1, sim_seconds=0.6, delta=D, g_CaL_const=g)
        ax[0].plot(t, tr, color=c, lw=0.8, label=f'$g_{{CaL}}={g}$')
    ax[0].set_title('(a) $g_{CaL}$: oscillation $\\to$ spiking')
    ax[0].set_xlabel('time (ms)'); ax[0].set_ylabel('$V_{soma}$ (mV)')
    ax[0].legend(fontsize=8, loc='upper right')

    # (b) gap junctions on vs off, 30 cells
    for gj, c, a in [(False, '#999999', 0.5), (True, '#c0392b', 0.7)]:
        tr = f.run_numpy(30, sim_seconds=0.6, delta=D, enable_gj=gj, record='all')
        for i in range(30):
            ax[1].plot(t, tr[:, i], color=c, lw=0.3, alpha=a)
    ax[1].plot([], [], color='#999999', label='GJ off (independent)')
    ax[1].plot([], [], color='#c0392b', label='GJ on (synchronised)')
    ax[1].set_title('(b) Gap junctions: $N=30$')
    ax[1].set_xlabel('time (ms)'); ax[1].set_ylabel('$V_{soma}$ (mV)')
    ax[1].legend(fontsize=8, loc='upper right')

    # (c) validation: baseline vs vectorised, single cell
    _, base = run_baseline(n_cells=1, sim_seconds=0.6, delta=D)
    vec = f.run_numpy(1, sim_seconds=0.6, delta=D)
    ax[2].plot(t, base[:, 0], color='black', lw=1.4, label='baseline')
    ax[2].plot(t, vec, color='#16a085', lw=0.8, ls='--', label='vectorised')
    md = np.nanmax(np.abs(base[:, 0] - vec))
    ax[2].set_title(f'(c) Validation, $N=1$ (max $\\Delta$={md:.1e} mV)')
    ax[2].set_xlabel('time (ms)'); ax[2].set_ylabel('$V_{soma}$ (mV)')
    ax[2].legend(fontsize=8, loc='upper right')

    fig.tight_layout(); fig.savefig(f'{FIG}/fig_morphology.png'); plt.close(fig)
    print('wrote fig_morphology.png')

if __name__ == '__main__':
    fig_profile()
    fig_scaling()
    fig_morphology()
