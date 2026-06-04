# Runs and profiles the provided io_model.py by importing it and patching its
# globals, so the timings reflect the original numerics.
import argparse
import time
import numpy as np


def run_baseline(n_cells=30, sim_seconds=1.0, delta=0.01, enable_gj=True,
                 seed=1981, g_CaL_const=None, I_pulse10ms=2.0, record_all=False):
    # returns (exec_time, soma trace of cell 0)
    import io_model as m
    # patch the globals the update_* functions read
    m.n_cells = n_cells
    m.sim_seconds = sim_seconds
    m.delta = delta
    m.enable_gapjunctions = enable_gj
    m.I_pulse10ms = I_pulse10ms

    rng = np.random.default_rng(seed)
    if g_CaL_const is None:
        g_CaL = rng.normal(0.7, 0.1, n_cells)
    else:
        g_CaL = np.full(n_cells, g_CaL_const)

    # initial state, same values as io_model.py
    V_soma = rng.uniform(-70, -40, size=(n_cells,))
    soma_k = np.full(n_cells, 0.7423159)
    soma_l = np.full(n_cells, 0.0321349)
    soma_h = np.full(n_cells, 0.3596066)
    soma_n = np.full(n_cells, 0.2369847)
    soma_x = np.full(n_cells, 0.1)

    V_axon = rng.uniform(-70, -40, size=(n_cells,))
    axon_Sodium_h = np.full(n_cells, 0.9)
    axon_Potassium_x = np.full(n_cells, 0.2369847)

    V_dend = rng.uniform(-70, -40, size=(n_cells,))
    dend_Ca2Plus = np.full(n_cells, 3.715)
    dend_Calcium_r = np.full(n_cells, 0.0113)
    dend_Potassium_s = np.full(n_cells, 0.0049291)
    dend_Hcurrent_q = np.full(n_cells, 0.0337836)

    n_simsteps = int(sim_seconds * 1000 / delta + 0.5)
    # record cell 0 only unless record_all
    rec_cells = range(n_cells) if record_all else [0]
    v_trace = {c: np.empty((n_simsteps, 4)) for c in rec_cells}
    t = 0.0

    tic = time.process_time()
    for i_epoch in range(n_simsteps):
        for i_cell in range(n_cells):
            at = i_epoch if i_cell in v_trace else -1
            vt = v_trace.get(i_cell)
            if vt is None:
                vt = np.empty((1, 4))  # scratch, not recorded
            m.update_soma(i_cell, vt, at, V_soma, V_axon, V_dend,
                          soma_k, soma_l, soma_h, soma_n, soma_x, g_CaL)
            m.update_axon(i_cell, vt, at, V_soma, V_axon,
                          axon_Sodium_h, axon_Potassium_x)
            m.update_dend(i_cell, vt, at, t, V_soma, V_dend,
                          dend_Ca2Plus, dend_Calcium_r, dend_Potassium_s, dend_Hcurrent_q)
            if at >= 0:
                vt[at, -1] = t
        t += delta
    exec_time = time.process_time() - tic
    return exec_time, v_trace[0]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n_cells', type=int, default=30)
    ap.add_argument('--sim_seconds', type=float, default=1.0)
    ap.add_argument('--delta', type=float, default=0.01)
    ap.add_argument('--no_gj', action='store_true')
    ap.add_argument('--profile', action='store_true')
    args = ap.parse_args()

    if args.profile:
        import cProfile
        import pstats
        import io as _io
        pr = cProfile.Profile()
        pr.enable()
        et, _ = run_baseline(args.n_cells, args.sim_seconds, args.delta, not args.no_gj)
        pr.disable()
        s = _io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats('tottime').print_stats(15)
        print(s.getvalue())
        print(f'wall (process_time): {et:.3f} s')
    else:
        et, tr = run_baseline(args.n_cells, args.sim_seconds, args.delta, not args.no_gj)
        print(f'n_cells={args.n_cells} time={et:.3f}s  soma0[mean={np.nanmean(tr[:,0]):.3f}]')
