# Exercise 6.1: vary each parameter and report soma-trace morphology.
import warnings
import numpy as np
import io_fast as f

warnings.filterwarnings('ignore')


def features(trace, delta):
    # morphology summary of one soma trace
    v = np.asarray(trace, float)
    if not np.all(np.isfinite(v)):
        return dict(diverged=True)
    vmin, vmax = v.min(), v.max()
    ptp = vmax - vmin
    # spikes: upward crossings of a -20 mV threshold
    thr = -20.0
    above = v > thr
    n_spikes = int(np.sum((~above[:-1]) & (above[1:])))
    dur_s = len(v) * delta / 1000.0
    rate = n_spikes / dur_s if dur_s > 0 else 0
    # dominant oscillation frequency via FFT
    vd = v - v.mean()
    fs = 1000.0 / delta
    spec = np.abs(np.fft.rfft(vd))
    freqs = np.fft.rfftfreq(len(vd), d=1.0 / fs)
    band = (freqs > 0.5) & (freqs < 20)
    fdom = freqs[band][np.argmax(spec[band])] if band.any() and spec[band].max() > 0 else 0.0
    return dict(diverged=False, vmin=vmin, vmax=vmax, ptp=ptp,
                n_spikes=n_spikes, rate_hz=rate, f_dom_hz=fdom, mean=v.mean())


def show(tag, feat):
    if feat.get('diverged'):
        print(f'  {tag:28s} -> DIVERGED (non-finite)')
    else:
        print(f'  {tag:28s} -> Vmin={feat["vmin"]:7.2f} Vmax={feat["vmax"]:7.2f} '
              f'ptp={feat["ptp"]:6.2f}mV  spikes={feat["n_spikes"]:3d} '
              f'({feat["rate_hz"]:4.1f}Hz)  f_osc={feat["f_dom_hz"]:4.1f}Hz')


if __name__ == '__main__':
    D = 0.01
    print('== sim_seconds (delta=0.01, n=1, g_CaL=0.7) ==')
    for s in [0.5, 1.0, 2.0]:
        tr = f.run_numpy(1, sim_seconds=s, delta=D, g_CaL_const=0.7)
        show(f'sim_seconds={s}', features(tr, D))

    print('== delta (sim=1.0, n=1, g_CaL=0.7) ==')
    for d in [0.01, 0.03, 0.05]:
        tr = f.run_numpy(1, sim_seconds=1.0, delta=d, g_CaL_const=0.7)
        show(f'delta={d}', features(tr, d))

    print('== n_cells (sim=1.0, delta=0.01, GJ on) ==')
    for n in [1, 2, 10, 30]:
        tr = f.run_numpy(n, sim_seconds=1.0, delta=D, record='all')
        # population synchrony = mean pairwise correlation
        feats = [features(tr[:, i], D) for i in range(n)]
        show(f'n_cells={n} (cell0)', feats[0])
        if n > 1:
            C = np.corrcoef(tr.T)
            sync = (C[np.triu_indices(n, 1)]).mean()
            print(f'      population synchrony (mean pairwise corr) = {sync:+.3f}')

    print('== enable_gapjunctions (n=30, sim=1.0) ==')
    for gj in [True, False]:
        tr = f.run_numpy(30, sim_seconds=1.0, delta=D, enable_gj=gj, record='all')
        C = np.corrcoef(tr.T)
        sync = (C[np.triu_indices(30, 1)]).mean()
        show(f'GJ={gj} (cell0)', features(tr[:, 0], D))
        print(f'      population synchrony = {sync:+.3f}')

    print('== g_CaL (n=1, sim=1.0, delta=0.01) ==')
    for g in [0.7, 1.8, 2.0]:
        tr = f.run_numpy(1, sim_seconds=1.0, delta=D, g_CaL_const=g)
        show(f'g_CaL={g}', features(tr, D))

    print('== I_pulse10ms (n=30, sim=1.0, delta=0.01) ==')
    for ip in [2.0, 5.0, 8.0, 10.0]:
        tr = f.run_numpy(30, sim_seconds=1.0, delta=D, I_pulse10ms=ip, record='all')
        show(f'I_pulse10ms={ip} (cell0)', features(tr[:, 0], D))
