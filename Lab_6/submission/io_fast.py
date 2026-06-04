# Accelerated IO network simulator for Lab 6, with numpy, numba and jax backends.
# The gap junction uses the mean field C_gap*(N*Vd_i - sum_j Vd_j), which is the
# O(N^2) all-to-all sum rewritten as O(N). Axon and dendrite use the new soma
# voltage, as in io_model.py; the coupling is Jacobi (start-of-step) not Gauss-Seidel.
import numpy as np

# constants, identical to io_model.py
g_int = 0.13;  p1 = 0.25;   p2 = 0.15
g_h = 0.12;    g_K_Ca = 35.0
g_ld = 0.01532; g_la = 0.016; g_ls = 0.004
S = 1.0
g_Na_s = 150.0; g_Kdr_s = 9.0; g_K_s = 5.0; g_CaH = 4.5
g_Na_a = 240.0; g_K_a = 240.0
V_Na = 55.0; V_K = -75.0; V_Ca = 120.0; V_h = -43.0; V_l = 10.0
C_gap = 0.05
I_app = 0.0


def initial_state(n_cells, seed=1981, g_CaL_const=None):
    """Reproducible initial state, identical distributions to io_model.py."""
    rng = np.random.default_rng(seed)
    g_CaL = (np.full(n_cells, g_CaL_const) if g_CaL_const is not None
             else rng.normal(0.7, 0.1, n_cells))
    st = dict(
        g_CaL=g_CaL,
        V_soma=rng.uniform(-70, -40, n_cells),
        soma_k=np.full(n_cells, 0.7423159), soma_l=np.full(n_cells, 0.0321349),
        soma_h=np.full(n_cells, 0.3596066), soma_n=np.full(n_cells, 0.2369847),
        soma_x=np.full(n_cells, 0.1),
        V_axon=rng.uniform(-70, -40, n_cells),
        axon_Sodium_h=np.full(n_cells, 0.9), axon_Potassium_x=np.full(n_cells, 0.2369847),
        V_dend=rng.uniform(-70, -40, n_cells),
        dend_Ca2Plus=np.full(n_cells, 3.715), dend_Calcium_r=np.full(n_cells, 0.0113),
        dend_Potassium_s=np.full(n_cells, 0.0049291), dend_Hcurrent_q=np.full(n_cells, 0.0337836),
    )
    return st


# vectorised numpy backend
def run_numpy(n_cells, sim_seconds=1.0, delta=0.01, enable_gj=True,
              I_pulse10ms=2.0, seed=1981, g_CaL_const=None, record=True):
    st = initial_state(n_cells, seed, g_CaL_const)
    Vs = st['V_soma']; Va = st['V_axon']; Vd = st['V_dend']
    sk, sl, sh, sn, sx = st['soma_k'], st['soma_l'], st['soma_h'], st['soma_n'], st['soma_x']
    ah, ax = st['axon_Sodium_h'], st['axon_Potassium_x']
    dCa, dr, ds, dq = st['dend_Ca2Plus'], st['dend_Calcium_r'], st['dend_Potassium_s'], st['dend_Hcurrent_q']
    g_CaL = st['g_CaL']
    exp = np.exp

    n_steps = int(sim_seconds * 1000 / delta + 0.5)
    full = (record == 'all')
    trace = (np.empty((n_steps, n_cells)) if full else np.empty(n_steps)) if record else None
    t = 0.0
    for it in range(n_steps):
        if record:
            trace[it] = Vs if full else Vs[0]
        # soma
        soma_I_leak = g_ls * (Vs - V_l)
        soma_I_interact = (g_int / p1) * (Vs - Vd) + (g_int / (1 - p2)) * (Vs - Va)
        soma_Ical = g_CaL * sk * sk * sk * sl * (Vs - V_Ca)
        sk_inf = 1 / (1 + exp(-(Vs + 61) / 4.2))
        sl_inf = 1 / (1 + exp((Vs + 85) / 8.5))
        s_tau_l = 20 * exp((Vs + 160) / 30) / (1 + exp((Vs + 84) / 7.3)) + 35
        sk_n = sk + delta * (sk_inf - sk)
        sl_n = sl + delta * (sl_inf - sl) / s_tau_l
        sm_inf = 1 / (1 + exp(-(Vs + 30) / 5.5))
        sh_inf = 1 / (1 + exp((Vs + 70) / 5.8))
        soma_Ina = g_Na_s * sm_inf**3 * sh * (Vs - V_Na)
        s_tau_h = 3 * exp(-(Vs + 40) / 33)
        sh_n = sh + delta * (sh_inf - sh) / s_tau_h
        soma_Ikdr = g_Kdr_s * sn**4 * (Vs - V_K)
        sn_inf = 1 / (1 + exp(-(Vs + 3) / 10))
        s_tau_n = 5 + 47 * exp((Vs + 50) / 900)
        sn_n = sn + delta * (sn_inf - sn) / s_tau_n
        soma_Ik = g_K_s * sx**4 * (Vs - V_K)
        s_alpha_x = 0.13 * (Vs + 25) / (1 - exp(-(Vs + 25) / 10))
        s_beta_x = 1.69 * exp(-(Vs + 35) / 80)
        s_tau_x_inv = s_alpha_x + s_beta_x
        sx_inf = s_alpha_x / s_tau_x_inv
        sx_n = sx + delta * (sx_inf - sx) * s_tau_x_inv
        soma_dv = S * (-(soma_I_leak + soma_I_interact + soma_Ik + soma_Ikdr + soma_Ina + soma_Ical))
        Vs_new = Vs + soma_dv * delta

        # axon, using new soma
        axon_I_leak = g_la * (Va - V_l)
        axon_I_interact = (g_int / p2) * (Va - Vs_new)
        am_inf = 1 / (1 + exp(-(Va + 30) / 5.5))
        ah_inf = 1 / (1 + exp((Va + 60) / 5.8))
        axon_Ina = g_Na_a * am_inf**3 * ah * (Va - V_Na)
        a_tau_h = 1.5 * exp(-(Va + 40) / 33)
        ah_n = ah + delta * (ah_inf - ah) / a_tau_h
        axon_Ik = g_K_a * ax**4 * (Va - V_K)
        a_alpha_x = 0.13 * (Va + 25) / (1 - exp(-(Va + 25) / 10))
        a_beta_x = 1.69 * exp(-(Va + 35) / 80)
        a_tau_x_inv = a_alpha_x + a_beta_x
        ax_inf = a_alpha_x / a_tau_x_inv
        ax_n = ax + delta * (ax_inf - ax) * a_tau_x_inv
        axon_dv = S * (-(axon_I_leak + axon_I_interact + axon_Ina + axon_Ik))
        Va_new = Va + axon_dv * delta

        # dend, using new soma
        dend_I_app = -I_app + (-I_pulse10ms if 200 * sim_seconds < t < 210 * sim_seconds else 0)
        dend_I_leak = g_ld * (Vd - V_l)
        dend_I_interact = (g_int / (1 - p1)) * (Vd - Vs_new)
        dend_Icah = g_CaH * dr * dr * (Vd - V_Ca)
        d_alpha_r = 1.7 / (1 + exp(-(Vd - 5) / 13.9))
        d_beta_r = 0.02 * (Vd + 8.5) / (exp((Vd + 8.5) / 5) - 1.0)
        d_tau_r_inv5 = d_alpha_r + d_beta_r
        dr_inf = d_alpha_r / d_tau_r_inv5
        dr_n = dr + delta * (dr_inf - dr) * d_tau_r_inv5 * 0.2
        dend_Ikca = g_K_Ca * ds * (Vd - V_K)
        cav = 0.00002 * dCa
        d_alpha_s = cav * (cav < 0.01) + 0.01 * (cav > 0.01)
        d_tau_s_inv = d_alpha_s + 0.015
        ds_inf = d_alpha_s / d_tau_s_inv
        ds_n = ds + delta * (ds_inf - ds) * d_tau_s_inv
        dend_Ih = g_h * dq * (Vd - V_h)
        q_inf = 1 / (1 + exp((Vd + 80) / 4))
        tau_q_inv = exp(-0.086 * Vd - 14.6) + exp(0.070 * Vd - 1.87)
        dq_n = dq + delta * (q_inf - dq) * tau_q_inv
        if enable_gj:
            dend_I_gap = C_gap * (n_cells * Vd - Vd.sum())   # O(N) mean-field
        else:
            dend_I_gap = 0.0
        dCa_n = dCa + delta * (-3 * dend_Icah - 0.075 * dCa)
        dend_dv = S * (-(dend_I_leak + dend_I_gap + dend_I_interact + dend_I_app
                         + dend_Icah + dend_Ikca + dend_Ih))
        Vd_new = Vd + dend_dv * delta

        # commit
        Vs, Va, Vd = Vs_new, Va_new, Vd_new
        sk, sl, sh, sn, sx = sk_n, sl_n, sh_n, sn_n, sx_n
        ah, ax = ah_n, ax_n
        dCa, dr, ds, dq = dCa_n, dr_n, ds_n, dq_n
        t += delta
    return trace


# numba njit backend, explicit per-cell loops with the O(N) gap junction
def _make_numba():
    try:
        from numba import njit, prange
    except Exception:
        return None
    import math

    @njit(fastmath=True, cache=True, error_model='numpy')
    def _run(n_cells, n_steps, delta, enable_gj, I_pulse10ms, sim_seconds,
             g_CaL, Vs, Va, Vd, sk, sl, sh, sn, sx, ah, ax, dCa, dr, ds, dq):
        trace = np.empty(n_steps)
        exp = math.exp
        Vs_n = Vs.copy(); Va_n = Va.copy(); Vd_n = Vd.copy()
        t = 0.0
        for it in range(n_steps):
            trace[it] = Vs[0]
            Vd_sum = 0.0
            for i in range(n_cells):
                Vd_sum += Vd[i]
            dend_I_app = -I_app + (-I_pulse10ms if (200 * sim_seconds < t < 210 * sim_seconds) else 0.0)
            for i in range(n_cells):
                vs = Vs[i]; va = Va[i]; vd = Vd[i]
                # soma
                soma_I_leak = g_ls * (vs - V_l)
                soma_I_interact = (g_int / p1) * (vs - vd) + (g_int / (1 - p2)) * (vs - va)
                soma_Ical = g_CaL[i] * sk[i] * sk[i] * sk[i] * sl[i] * (vs - V_Ca)
                sk_inf = 1 / (1 + exp(-(vs + 61) / 4.2))
                sl_inf = 1 / (1 + exp((vs + 85) / 8.5))
                s_tau_l = 20 * exp((vs + 160) / 30) / (1 + exp((vs + 84) / 7.3)) + 35
                sk[i] += delta * (sk_inf - sk[i])
                sl[i] += delta * (sl_inf - sl[i]) / s_tau_l
                sm_inf = 1 / (1 + exp(-(vs + 30) / 5.5))
                sh_inf = 1 / (1 + exp((vs + 70) / 5.8))
                soma_Ina = g_Na_s * sm_inf**3 * sh[i] * (vs - V_Na)
                s_tau_h = 3 * exp(-(vs + 40) / 33)
                sh[i] += delta * (sh_inf - sh[i]) / s_tau_h
                soma_Ikdr = g_Kdr_s * sn[i]**4 * (vs - V_K)
                sn_inf = 1 / (1 + exp(-(vs + 3) / 10))
                s_tau_n = 5 + 47 * exp((vs + 50) / 900)
                sn[i] += delta * (sn_inf - sn[i]) / s_tau_n
                soma_Ik = g_K_s * sx[i]**4 * (vs - V_K)
                s_alpha_x = 0.13 * (vs + 25) / (1 - exp(-(vs + 25) / 10))
                s_beta_x = 1.69 * exp(-(vs + 35) / 80)
                s_tau_x_inv = s_alpha_x + s_beta_x
                sx_inf = s_alpha_x / s_tau_x_inv
                sx[i] += delta * (sx_inf - sx[i]) * s_tau_x_inv
                soma_dv = S * (-(soma_I_leak + soma_I_interact + soma_Ik + soma_Ikdr + soma_Ina + soma_Ical))
                vs_new = vs + soma_dv * delta
                # axon (new soma)
                axon_I_leak = g_la * (va - V_l)
                axon_I_interact = (g_int / p2) * (va - vs_new)
                am_inf = 1 / (1 + exp(-(va + 30) / 5.5))
                ah_inf = 1 / (1 + exp((va + 60) / 5.8))
                axon_Ina = g_Na_a * am_inf**3 * ah[i] * (va - V_Na)
                a_tau_h = 1.5 * exp(-(va + 40) / 33)
                ah[i] += delta * (ah_inf - ah[i]) / a_tau_h
                axon_Ik = g_K_a * ax[i]**4 * (va - V_K)
                a_alpha_x = 0.13 * (va + 25) / (1 - exp(-(va + 25) / 10))
                a_beta_x = 1.69 * exp(-(va + 35) / 80)
                a_tau_x_inv = a_alpha_x + a_beta_x
                ax_inf = a_alpha_x / a_tau_x_inv
                ax[i] += delta * (ax_inf - ax[i]) * a_tau_x_inv
                axon_dv = S * (-(axon_I_leak + axon_I_interact + axon_Ina + axon_Ik))
                va_new = va + axon_dv * delta
                # dend (new soma, O(N) gap junction via Vd_sum)
                dend_I_leak = g_ld * (vd - V_l)
                dend_I_interact = (g_int / (1 - p1)) * (vd - vs_new)
                dend_Icah = g_CaH * dr[i] * dr[i] * (vd - V_Ca)
                d_alpha_r = 1.7 / (1 + exp(-(vd - 5) / 13.9))
                d_beta_r = 0.02 * (vd + 8.5) / (exp((vd + 8.5) / 5) - 1.0)
                d_tau_r_inv5 = d_alpha_r + d_beta_r
                dr_inf = d_alpha_r / d_tau_r_inv5
                dr[i] += delta * (dr_inf - dr[i]) * d_tau_r_inv5 * 0.2
                dend_Ikca = g_K_Ca * ds[i] * (vd - V_K)
                cav = 0.00002 * dCa[i]
                d_alpha_s = cav if cav < 0.01 else 0.01
                d_tau_s_inv = d_alpha_s + 0.015
                ds_inf = d_alpha_s / d_tau_s_inv
                ds[i] += delta * (ds_inf - ds[i]) * d_tau_s_inv
                dend_Ih = g_h * dq[i] * (vd - V_h)
                q_inf = 1 / (1 + exp((vd + 80) / 4))
                tau_q_inv = exp(-0.086 * vd - 14.6) + exp(0.070 * vd - 1.87)
                dq[i] += delta * (q_inf - dq[i]) * tau_q_inv
                dend_I_gap = C_gap * (n_cells * vd - Vd_sum) if enable_gj else 0.0
                dCa[i] += delta * (-3 * dend_Icah - 0.075 * dCa[i])
                dend_dv = S * (-(dend_I_leak + dend_I_gap + dend_I_interact + dend_I_app
                                 + dend_Icah + dend_Ikca + dend_Ih))
                vd_new = vd + dend_dv * delta
                Vs_n[i] = vs_new; Va_n[i] = va_new; Vd_n[i] = vd_new
            for i in range(n_cells):
                Vs[i] = Vs_n[i]; Va[i] = Va_n[i]; Vd[i] = Vd_n[i]
            t += delta
        return trace
    return _run


_NUMBA_RUN = None


def run_numba(n_cells, sim_seconds=1.0, delta=0.01, enable_gj=True,
              I_pulse10ms=2.0, seed=1981, g_CaL_const=None):
    global _NUMBA_RUN
    if _NUMBA_RUN is None:
        _NUMBA_RUN = _make_numba()
    if _NUMBA_RUN is None:
        raise RuntimeError('numba not available')
    st = initial_state(n_cells, seed, g_CaL_const)
    n_steps = int(sim_seconds * 1000 / delta + 0.5)
    return _NUMBA_RUN(
        n_cells, n_steps, float(delta), bool(enable_gj), float(I_pulse10ms), float(sim_seconds),
        st['g_CaL'], st['V_soma'], st['V_axon'], st['V_dend'],
        st['soma_k'], st['soma_l'], st['soma_h'], st['soma_n'], st['soma_x'],
        st['axon_Sodium_h'], st['axon_Potassium_x'],
        st['dend_Ca2Plus'], st['dend_Calcium_r'], st['dend_Potassium_s'], st['dend_Hcurrent_q'])


# jax backend, jit + lax.scan, runs on CPU or GPU
def run_jax(n_cells, sim_seconds=1.0, delta=0.01, enable_gj=True,
            I_pulse10ms=2.0, seed=1981, g_CaL_const=None, record=True):
    import jax
    import jax.numpy as jnp
    from jax import lax
    st = initial_state(n_cells, seed, g_CaL_const)
    n_steps = int(sim_seconds * 1000 / delta + 0.5)
    arrs = {k: jnp.asarray(v, dtype=jnp.float64 if jax.config.read('jax_enable_x64') else jnp.float32)
            for k, v in st.items()}
    delta = jnp.float32(delta) if not jax.config.read('jax_enable_x64') else jnp.float64(delta)
    enable_gj = bool(enable_gj)

    def step(carry, t):
        (Vs, Va, Vd, sk, sl, sh, sn, sx, ah, ax, dCa, dr, ds, dq) = carry
        exp = jnp.exp
        soma_I_leak = g_ls * (Vs - V_l)
        soma_I_interact = (g_int / p1) * (Vs - Vd) + (g_int / (1 - p2)) * (Vs - Va)
        soma_Ical = arrs['g_CaL'] * sk * sk * sk * sl * (Vs - V_Ca)
        sk_inf = 1 / (1 + exp(-(Vs + 61) / 4.2))
        sl_inf = 1 / (1 + exp((Vs + 85) / 8.5))
        s_tau_l = 20 * exp((Vs + 160) / 30) / (1 + exp((Vs + 84) / 7.3)) + 35
        sk_n = sk + delta * (sk_inf - sk)
        sl_n = sl + delta * (sl_inf - sl) / s_tau_l
        sm_inf = 1 / (1 + exp(-(Vs + 30) / 5.5))
        sh_inf = 1 / (1 + exp((Vs + 70) / 5.8))
        soma_Ina = g_Na_s * sm_inf**3 * sh * (Vs - V_Na)
        s_tau_h = 3 * exp(-(Vs + 40) / 33)
        sh_n = sh + delta * (sh_inf - sh) / s_tau_h
        soma_Ikdr = g_Kdr_s * sn**4 * (Vs - V_K)
        sn_inf = 1 / (1 + exp(-(Vs + 3) / 10))
        s_tau_n = 5 + 47 * exp((Vs + 50) / 900)
        sn_n = sn + delta * (sn_inf - sn) / s_tau_n
        soma_Ik = g_K_s * sx**4 * (Vs - V_K)
        s_alpha_x = 0.13 * (Vs + 25) / (1 - exp(-(Vs + 25) / 10))
        s_beta_x = 1.69 * exp(-(Vs + 35) / 80)
        s_tau_x_inv = s_alpha_x + s_beta_x
        sx_n = sx + delta * (s_alpha_x / s_tau_x_inv - sx) * s_tau_x_inv
        soma_dv = S * (-(soma_I_leak + soma_I_interact + soma_Ik + soma_Ikdr + soma_Ina + soma_Ical))
        Vs_new = Vs + soma_dv * delta

        axon_I_leak = g_la * (Va - V_l)
        axon_I_interact = (g_int / p2) * (Va - Vs_new)
        am_inf = 1 / (1 + exp(-(Va + 30) / 5.5))
        ah_inf = 1 / (1 + exp((Va + 60) / 5.8))
        axon_Ina = g_Na_a * am_inf**3 * ah * (Va - V_Na)
        a_tau_h = 1.5 * exp(-(Va + 40) / 33)
        ah_n = ah + delta * (ah_inf - ah) / a_tau_h
        axon_Ik = g_K_a * ax**4 * (Va - V_K)
        a_alpha_x = 0.13 * (Va + 25) / (1 - exp(-(Va + 25) / 10))
        a_beta_x = 1.69 * exp(-(Va + 35) / 80)
        a_tau_x_inv = a_alpha_x + a_beta_x
        ax_n = ax + delta * (a_alpha_x / a_tau_x_inv - ax) * a_tau_x_inv
        axon_dv = S * (-(axon_I_leak + axon_I_interact + axon_Ina + axon_Ik))
        Va_new = Va + axon_dv * delta

        dend_I_app = -I_app - I_pulse10ms * ((200 * sim_seconds < t) & (t < 210 * sim_seconds))
        dend_I_leak = g_ld * (Vd - V_l)
        dend_I_interact = (g_int / (1 - p1)) * (Vd - Vs_new)
        dend_Icah = g_CaH * dr * dr * (Vd - V_Ca)
        d_alpha_r = 1.7 / (1 + exp(-(Vd - 5) / 13.9))
        d_beta_r = 0.02 * (Vd + 8.5) / (exp((Vd + 8.5) / 5) - 1.0)
        d_tau_r_inv5 = d_alpha_r + d_beta_r
        dr_n = dr + delta * (d_alpha_r / d_tau_r_inv5 - dr) * d_tau_r_inv5 * 0.2
        dend_Ikca = g_K_Ca * ds * (Vd - V_K)
        cav = 0.00002 * dCa
        d_alpha_s = jnp.minimum(cav, 0.01)
        d_tau_s_inv = d_alpha_s + 0.015
        ds_n = ds + delta * (d_alpha_s / d_tau_s_inv - ds) * d_tau_s_inv
        dend_Ih = g_h * dq * (Vd - V_h)
        q_inf = 1 / (1 + exp((Vd + 80) / 4))
        tau_q_inv = exp(-0.086 * Vd - 14.6) + exp(0.070 * Vd - 1.87)
        dq_n = dq + delta * (q_inf - dq) * tau_q_inv
        dend_I_gap = (C_gap * (n_cells * Vd - jnp.sum(Vd))) if enable_gj else 0.0
        dCa_n = dCa + delta * (-3 * dend_Icah - 0.075 * dCa)
        dend_dv = S * (-(dend_I_leak + dend_I_gap + dend_I_interact + dend_I_app
                         + dend_Icah + dend_Ikca + dend_Ih))
        Vd_new = Vd + dend_dv * delta

        carry = (Vs_new, Va_new, Vd_new, sk_n, sl_n, sh_n, sn_n, sx_n,
                 ah_n, ax_n, dCa_n, dr_n, ds_n, dq_n)
        return carry, Vs[0]

    carry0 = (arrs['V_soma'], arrs['V_axon'], arrs['V_dend'],
              arrs['soma_k'], arrs['soma_l'], arrs['soma_h'], arrs['soma_n'], arrs['soma_x'],
              arrs['axon_Sodium_h'], arrs['axon_Potassium_x'],
              arrs['dend_Ca2Plus'], arrs['dend_Calcium_r'], arrs['dend_Potassium_s'], arrs['dend_Hcurrent_q'])
    ts = (jnp.arange(n_steps) * delta).astype(arrs['V_soma'].dtype)

    @jax.jit
    def sim(carry0, ts):
        carry, trace = lax.scan(step, carry0, ts)
        return trace, carry[0]

    trace, final = sim(carry0, ts)
    trace.block_until_ready()
    return np.asarray(trace) if record else None


if __name__ == '__main__':
    import argparse, time
    ap = argparse.ArgumentParser()
    ap.add_argument('--backend', choices=['numpy', 'numba', 'jax'], default='numpy')
    ap.add_argument('--n_cells', type=int, default=30)
    ap.add_argument('--sim_seconds', type=float, default=1.0)
    ap.add_argument('--delta', type=float, default=0.01)
    args = ap.parse_args()
    fn = {'numpy': run_numpy, 'numba': run_numba, 'jax': run_jax}[args.backend]
    tic = time.perf_counter()
    tr = fn(args.n_cells, args.sim_seconds, args.delta)
    dt = time.perf_counter() - tic
    print(f'{args.backend} n={args.n_cells} time={dt:.3f}s  soma0 mean={np.nanmean(tr):.3f}')
