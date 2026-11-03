// Inferior-Olive network, hand-optimised CPU kernel for the Lab 6 challenge.
// float32, structure-of-arrays, OpenMP across cells, AVX2-vectorised poly-exp.
// Math mirrors io_fast.py run_numpy exactly (Jacobi mean-field gap junction),
// only the dtype (fp32) and the exp implementation differ. The metric is
// mean wall-time per step; 1 s of brain time = 1e5 steps, score = us/step * 0.1.
//
// Build:  see Makefile   Run:  ./io_sim <n_cells> <n_steps> <reps>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <omp.h>

// ---- model constants (identical to io_model.py / io_fast.py), as float ----
#define g_int   0.13f
#define p1      0.25f
#define p2      0.15f
#define g_h     0.12f
#define g_K_Ca  35.0f
#define g_ld    0.01532f
#define g_la    0.016f
#define g_ls    0.004f
#define g_Na_s  150.0f
#define g_Kdr_s 9.0f
#define g_K_s   5.0f
#define g_CaH   4.5f
#define g_Na_a  240.0f
#define g_K_a   240.0f
#define V_Na    55.0f
#define V_K     (-75.0f)
#define V_Ca    120.0f
#define V_h     (-43.0f)
#define V_l     10.0f
#define C_gap   0.05f
#define I_app   0.0f

// derived combinations hoisted out of the loop
#define GI_P1     (g_int / p1)          // soma <- dend
#define GI_1MP2   (g_int / (1.0f - p2)) // soma <- axon
#define GI_P2     (g_int / p2)          // axon <- soma
#define GI_1MP1   (g_int / (1.0f - p1)) // dend <- soma

// Fast vectorisable expf: exp(x) = 2^(x*log2e), split into 2^k * 2^f.
// Degree-6 minimax poly for 2^f on [-0.5,0.5]; ~1e-6 relative error.
// Written so gcc auto-vectorises it (vroundps / vcvttps2dq / vpslld / FMA).
static inline float fexpf(float x) {
    x = x < -87.0f ? -87.0f : (x > 88.0f ? 88.0f : x);
    float z  = x * 1.4426950408889634f;      // log2(e) * x
    float kf = floorf(z + 0.5f);
    float f  = z - kf;                        // in [-0.5, 0.5]
    float p  = 0.99999925f + f*(0.69315308f + f*(0.24015361f
             + f*(0.05594100f + f*(0.00898934f + f*0.00187757f))));
    int   e  = ((int)kf + 127) << 23;         // build 2^k
    float s;
    memcpy(&s, &e, sizeof s);
    return p * s;
}

// State: structure of arrays. One malloc block, 16 arrays.
typedef struct {
    int n;
    float *g_CaL;
    float *Vs, *Va, *Vd;
    float *sk, *sl, *sh, *sn, *sx;
    float *ah, *ax;
    float *dCa, *dr, *ds, *dq;
} State;

static float frand(unsigned int *s) {          // xorshift32 -> [0,1)
    unsigned int x = *s;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    *s = x;
    return (x >> 8) * (1.0f / 16777216.0f);
}

static void state_init(State *st, int n, unsigned int seed) {
    st->n = n;
    size_t bytes = (size_t)n * sizeof(float);
    st->g_CaL = aligned_alloc(64, bytes);
    st->Vs = aligned_alloc(64, bytes); st->Va = aligned_alloc(64, bytes); st->Vd = aligned_alloc(64, bytes);
    st->sk = aligned_alloc(64, bytes); st->sl = aligned_alloc(64, bytes); st->sh = aligned_alloc(64, bytes);
    st->sn = aligned_alloc(64, bytes); st->sx = aligned_alloc(64, bytes);
    st->ah = aligned_alloc(64, bytes); st->ax = aligned_alloc(64, bytes);
    st->dCa = aligned_alloc(64, bytes); st->dr = aligned_alloc(64, bytes);
    st->ds = aligned_alloc(64, bytes); st->dq = aligned_alloc(64, bytes);
    unsigned int s = seed ? seed : 1981u;
    for (int i = 0; i < n; i++) {
        // g_CaL ~ Normal(0.7,0.1) via Box-Muller (cheap, one-time)
        float u1 = frand(&s), u2 = frand(&s);
        float g = sqrtf(-2.0f*logf(u1 + 1e-9f)) * cosf(6.2831853f*u2);
        st->g_CaL[i] = 0.7f + 0.1f*g;
        st->Vs[i] = -70.0f + 30.0f*frand(&s);
        st->Va[i] = -70.0f + 30.0f*frand(&s);
        st->Vd[i] = -70.0f + 30.0f*frand(&s);
        st->sk[i] = 0.7423159f; st->sl[i] = 0.0321349f; st->sh[i] = 0.3596066f;
        st->sn[i] = 0.2369847f; st->sx[i] = 0.1f;
        st->ah[i] = 0.9f;       st->ax[i] = 0.2369847f;
        st->dCa[i] = 3.715f;    st->dr[i] = 0.0113f;
        st->ds[i] = 0.0049291f; st->dq[i] = 0.0337836f;
    }
}

static void state_free(State *st) {
    free(st->g_CaL); free(st->Vs); free(st->Va); free(st->Vd);
    free(st->sk); free(st->sl); free(st->sh); free(st->sn); free(st->sx);
    free(st->ah); free(st->ax); free(st->dCa); free(st->dr); free(st->ds); free(st->dq);
}

// One full simulation of n_steps. Records Vs[0] each step into trace (len n_steps).
// Persistent parallel region: no per-step fork/join. Two omp-for per step
// (reduction of the dendrite mean, then the cell update), both O(N).
static void run_sim(State *st, int n_steps, float delta, int enable_gj,
                    float I_pulse10ms, float sim_seconds, float *trace) {
    const int n = st->n;
    float *Vs = st->Vs, *Va = st->Va, *Vd = st->Vd;
    float *sk = st->sk, *sl = st->sl, *sh = st->sh, *sn = st->sn, *sx = st->sx;
    float *ah = st->ah, *ax = st->ax;
    float *dCa = st->dCa, *dr = st->dr, *ds = st->ds, *dq = st->dq;
    float *g_CaL = st->g_CaL;
    const float Ngj = enable_gj ? (float)n : 0.0f;
    // per-thread partial sums, padded to 64 B to avoid false sharing
    const int NT = omp_get_max_threads();
    double (*psum)[8] = calloc((size_t)NT, sizeof(*psum));

    #pragma omp parallel
    {
        const int tid = omp_get_thread_num();
        float t = 0.0f;
        for (int step = 0; step < n_steps; step++) {
            // --- dendrite mean over OLD Vd (needed by the gap junction) ---
            // Two barriers/step is the minimum: one after the sum, one after
            // the update. Per-thread partials avoid the reduction's extra sync.
            double loc = 0.0;
            #pragma omp for schedule(static) nowait
            for (int i = 0; i < n; i++) loc += (double)Vd[i];
            psum[tid][0] = loc;
            #pragma omp barrier                    // barrier 1: all partials in
            double sig = 0.0;
            for (int tt = 0; tt < NT; tt++) sig += psum[tt][0];
            const float Sig = enable_gj ? (float)sig : 0.0f;

            float dend_I_app = -I_app +
                ((200.0f*sim_seconds < t && t < 210.0f*sim_seconds) ? -I_pulse10ms : 0.0f);

            // --- per-cell update (Jacobi: reads old state + global Sig) ---
            #pragma omp for simd schedule(runtime) nowait
            for (int i = 0; i < n; i++) {
                float vs = Vs[i], va = Va[i], vd = Vd[i];

                // soma
                float soma_I_leak = g_ls * (vs - V_l);
                float soma_I_interact = GI_P1*(vs - vd) + GI_1MP2*(vs - va);
                float ki = sk[i];
                float soma_Ical = g_CaL[i] * ki*ki*ki * sl[i] * (vs - V_Ca);
                float sk_inf = 1.0f/(1.0f + fexpf(-(vs + 61.0f)/4.2f));
                float sl_inf = 1.0f/(1.0f + fexpf((vs + 85.0f)/8.5f));
                float s_tau_l = 20.0f*fexpf((vs + 160.0f)/30.0f)
                                / (1.0f + fexpf((vs + 84.0f)/7.3f)) + 35.0f;
                sk[i] = ki + delta*(sk_inf - ki);
                sl[i] = sl[i] + delta*(sl_inf - sl[i])/s_tau_l;
                float sm_inf = 1.0f/(1.0f + fexpf(-(vs + 30.0f)/5.5f));
                float sh_inf = 1.0f/(1.0f + fexpf((vs + 70.0f)/5.8f));
                float soma_Ina = g_Na_s * sm_inf*sm_inf*sm_inf * sh[i] * (vs - V_Na);
                float s_tau_h = 3.0f*fexpf(-(vs + 40.0f)/33.0f);
                sh[i] = sh[i] + delta*(sh_inf - sh[i])/s_tau_h;
                float sni = sn[i]; float sn2 = sni*sni;
                float soma_Ikdr = g_Kdr_s * sn2*sn2 * (vs - V_K);
                float sn_inf = 1.0f/(1.0f + fexpf(-(vs + 3.0f)/10.0f));
                float s_tau_n = 5.0f + 47.0f*fexpf((vs + 50.0f)/900.0f);
                sn[i] = sni + delta*(sn_inf - sni)/s_tau_n;
                float sxi = sx[i]; float sx2 = sxi*sxi;
                float soma_Ik = g_K_s * sx2*sx2 * (vs - V_K);
                float s_alpha_x = 0.13f*(vs + 25.0f)/(1.0f - fexpf(-(vs + 25.0f)/10.0f));
                float s_beta_x = 1.69f*fexpf(-(vs + 35.0f)/80.0f);
                float s_tau_x_inv = s_alpha_x + s_beta_x;
                float sx_inf = s_alpha_x/s_tau_x_inv;
                sx[i] = sxi + delta*(sx_inf - sxi)*s_tau_x_inv;
                float soma_dv = -(soma_I_leak + soma_I_interact + soma_Ik + soma_Ikdr + soma_Ina + soma_Ical);
                float vs_new = vs + soma_dv*delta;

                // axon (uses new soma)
                float axon_I_leak = g_la*(va - V_l);
                float axon_I_interact = GI_P2*(va - vs_new);
                float am_inf = 1.0f/(1.0f + fexpf(-(va + 30.0f)/5.5f));
                float ah_inf = 1.0f/(1.0f + fexpf((va + 60.0f)/5.8f));
                float axon_Ina = g_Na_a * am_inf*am_inf*am_inf * ah[i] * (va - V_Na);
                float a_tau_h = 1.5f*fexpf(-(va + 40.0f)/33.0f);
                ah[i] = ah[i] + delta*(ah_inf - ah[i])/a_tau_h;
                float axi = ax[i]; float ax2 = axi*axi;
                float axon_Ik = g_K_a * ax2*ax2 * (va - V_K);
                float a_alpha_x = 0.13f*(va + 25.0f)/(1.0f - fexpf(-(va + 25.0f)/10.0f));
                float a_beta_x = 1.69f*fexpf(-(va + 35.0f)/80.0f);
                float a_tau_x_inv = a_alpha_x + a_beta_x;
                float ax_inf = a_alpha_x/a_tau_x_inv;
                ax[i] = axi + delta*(ax_inf - axi)*a_tau_x_inv;
                float axon_dv = -(axon_I_leak + axon_I_interact + axon_Ina + axon_Ik);
                float va_new = va + axon_dv*delta;

                // dend (uses new soma, O(N) mean-field gap junction)
                float dend_I_leak = g_ld*(vd - V_l);
                float dend_I_interact = GI_1MP1*(vd - vs_new);
                float dri = dr[i];
                float dend_Icah = g_CaH * dri*dri * (vd - V_Ca);
                float d_alpha_r = 1.7f/(1.0f + fexpf(-(vd - 5.0f)/13.9f));
                float d_beta_r = 0.02f*(vd + 8.5f)/(fexpf((vd + 8.5f)/5.0f) - 1.0f);
                float d_tau_r_inv5 = d_alpha_r + d_beta_r;
                float dr_inf = d_alpha_r/d_tau_r_inv5;
                dr[i] = dri + delta*(dr_inf - dri)*d_tau_r_inv5*0.2f;
                float dend_Ikca = g_K_Ca * ds[i] * (vd - V_K);
                float cav = 0.00002f*dCa[i];
                float d_alpha_s = cav < 0.01f ? cav : 0.01f;
                float d_tau_s_inv = d_alpha_s + 0.015f;
                float ds_inf = d_alpha_s/d_tau_s_inv;
                ds[i] = ds[i] + delta*(ds_inf - ds[i])*d_tau_s_inv;
                float dend_Ih = g_h * dq[i] * (vd - V_h);
                float q_inf = 1.0f/(1.0f + fexpf((vd + 80.0f)/4.0f));
                float tau_q_inv = fexpf(-0.086f*vd - 14.6f) + fexpf(0.070f*vd - 1.87f);
                dq[i] = dq[i] + delta*(q_inf - dq[i])*tau_q_inv;
                float dend_I_gap = C_gap*(Ngj*vd - Sig);
                dCa[i] = dCa[i] + delta*(-3.0f*dend_Icah - 0.075f*dCa[i]);
                float dend_dv = -(dend_I_leak + dend_I_gap + dend_I_interact + dend_I_app
                                  + dend_Icah + dend_Ikca + dend_Ih);
                float vd_new = vd + dend_dv*delta;

                Vs[i] = vs_new; Va[i] = va_new; Vd[i] = vd_new;
            }
            #pragma omp barrier                    // barrier 2: all updates in
            #pragma omp master
            { trace[step] = Vs[0]; }               // no barrier (benign)
            t += delta;
        }
    }
    free(psum);
}

int main(int argc, char **argv) {
    int   n_cells = argc > 1 ? atoi(argv[1]) : 100000;
    int   n_steps = argc > 2 ? atoi(argv[2]) : 3000;
    int   reps    = argc > 3 ? atoi(argv[3]) : 3;
    float delta   = 0.01f;
    int   gj      = 1;

    State st;
    float *trace = malloc((size_t)n_steps * sizeof(float));

    // warm-up (page-in, cache, thread spin-up)
    state_init(&st, n_cells, 1981u);
    run_sim(&st, n_steps < 200 ? n_steps : 200, delta, gj, 2.0f, 1.0f, trace);
    state_free(&st);

    double best = 1e30;
    float check = 0.0f;
    for (int r = 0; r < reps; r++) {
        state_init(&st, n_cells, 1981u);
        struct timespec t0, t1;
        clock_gettime(CLOCK_MONOTONIC, &t0);
        run_sim(&st, n_steps, delta, gj, 2.0f, 1.0f, trace);
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double dt = (t1.tv_sec - t0.tv_sec) + 1e-9*(t1.tv_nsec - t0.tv_nsec);
        if (dt < best) best = dt;
        check = trace[n_steps - 1];
        state_free(&st);
    }

    double us_per_step = best / n_steps * 1e6;
    double total_1s = us_per_step * 100000.0 / 1e6;   // 1e5 steps = 1 s brain
    printf("n_cells=%d steps=%d threads=%d  best=%.4fs  %.4f us/step  1s-brain=%.4f s  (Vs0[last]=%.3f)\n",
           n_cells, n_steps, omp_get_max_threads(), best, us_per_step, total_1s, check);
    free(trace);
    return 0;
}
