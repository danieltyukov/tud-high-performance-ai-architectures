# Lab 1 — working notes (Daniel Tyukov, 5714699)

This is the live notebook for Lab 1. Each section below corresponds to one
question in `report/lab1/Lab1.tex`. All timing numbers come from the AWS
course VM (Intel Xeon Platinum 8259CL @ 2.50 GHz, 2 vCPUs, 3.7 GiB RAM,
Ubuntu 24.04, Python 3.12.3, NumPy 2.4.4, Numba 0.65.0). See
`AWS_INSTANCE_SPECS.md` at the project root for the full hardware footnote.

Raw bench logs: `Lab_1/lab1_bench.log` (Q2/Q3/Q4c/Q5/Q6/Q7/Q8/Q9 main
sweep) and `bench_extra.py` console output (sequential MLP on TVB76 and
TVB998 to complete Q6's required comparison).

---

## Q1 (Exercise 1.1) — Pen-and-paper analysis

### (a) Time complexity in $N$ (centers) and $T$ (timesteps)

The `simulate` body has the structure (per timestep $t > 0$):

```
for n in 0..N-1:                                  # outer: N
    c_in = calculate_coupling(...)                #   inner: N  (sum over j)
    X_new = step(...)                             #   O(cost(F))
    Xs[n][:][t] = X_new                           #   O(M)
```

`calculate_coupling` performs $N$ multiply-adds (one per source $j$). With
$M$ and $\mathrm{cost}(F)$ both constant in Lab 1, the dominant per-timestep
cost is the **$N \times N$ coupling sum**, i.e. $\mathcal{O}(N^2)$ per
timestep. Over $T = \mathtt{tf}/\mathtt{dt}$ timesteps:

$$
T_{\text{seq}} \;=\; \mathcal{O}(N^2 \cdot T) \;=\; \mathcal{O}\!\left(\frac{N^2 \cdot \mathtt{tf}}{\mathtt{dt}}\right).
$$

- **Quadratic in $N$** — driven by the dense coupling sum.
- **Linear in $T$** — the time loop is purely sequential due to the causal
  delay dependency (see (d)).

### (b) Memory capacity (number of stored elements)

The state-history array is `Xs[N][M][T]`, so the number of stored state
elements is:

$$
\#\text{elements}(\mathtt{Xs}) \;=\; N \cdot M \cdot T \;=\; N \cdot M \cdot \frac{\mathtt{tf}}{\mathtt{dt}}.
$$

Scaling individually with each parameter (the assignment writes "D" — read
as **D**uration $= \mathtt{tf}$):

| Parameter | Scaling of state memory |
|---|---|
| $N$ (number of centers) | linear, $\propto N$ |
| $M$ (state variables per center) | linear, $\propto M$ |
| $D \equiv \mathtt{tf}$ (duration) | linear, $\propto \mathtt{tf}$ (because $T = \mathtt{tf}/\mathtt{dt}$) |

Auxiliary structures (weights $W$, distances $D_{ij}$, integer delays
$D_{\text{timestep}}$) are each $N \times N$, i.e. $\mathcal{O}(N^2)$ but
constant in time — sub-dominant to $\mathtt{Xs}$ once $T \gtrsim N / M$,
which holds for all three TVB datasets at $\mathtt{tf} = 150$ ms.

For the largest dataset (TVB998, $M=2$, $T=3000$):
$N \cdot M \cdot T \approx 6 \times 10^6$ float64 $\approx 48$ MB — fits
comfortably in 3.7 GiB.

### (c) Linear $K_{\text{pre}}$ — algebraic transformation

If $K_{\text{pre}}(X_j, X_i) = a X_j + b X_i$, the inner coupling sum
factors:

$$
\begin{aligned}
\sum_{j=1}^{N} W_{ij}\,K_{\text{pre}}(X_j(t-d_{ij}),\, X_i(t))
&= \sum_{j=1}^{N} W_{ij}\,\bigl(a\,X_j(t-d_{ij}) \;+\; b\,X_i(t)\bigr) \\[2pt]
&= a \sum_{j=1}^{N} W_{ij}\,X_j(t-d_{ij}) \;+\; b\,X_i(t) \sum_{j=1}^{N} W_{ij}.
\end{aligned}
$$

Let $S_i \;=\; \sum_{j=1}^{N} W_{ij}$. **$S_i$ is a constant of the
simulation** ($W$ doesn't change with $t$), so it can be precomputed once at
init and reused for every timestep. The $b\,X_i(t)$ term then leaves the
inner $j$-loop entirely.

Op count per destination $i$ per timestep:

| Form | Multiplies in inner $j$-loop | Adds in inner $j$-loop | Outside the $j$-loop |
|---|---|---|---|
| Original $K_{\text{pre}}$ inline | $\approx 3N$ ($W_{ij}\cdot a$, $W_{ij}\cdot b$, sum) | $N$ | — |
| Factored | $N$ ($W_{ij}\cdot X_j$ only) | $N$ | $1$ multiply ($b\,X_i \cdot S_i$), $1$ add |

Across $N$ destinations and $T$ timesteps, this trims the per-timestep cost
by a constant factor of roughly $3\times$ in the multiply-add count, while
the $S_i$ precompute is a one-time $\mathcal{O}(N^2)$ (cheaper than even one
timestep of the original loop). Asymptotic complexity stays
$\mathcal{O}(N^2 T)$, but the constant shrinks — relevant for any inner-loop
acceleration (vectorization, JIT).

### (d) Parallelism across timesteps — feasible?

**No, not in general.** The Forward Euler update at step $t$ reads
$X_j(t - d_{ij})$ from history, with $d_{ij} \geq 0$. As long as some edge
has $d_{ij} = 0$ (or, in the script, when $d_{ij} = 0$ or $i = j$, the code
explicitly reads $X_j(t-1)$), step $t$ depends on step $t-1$ — a hard data
dependency that serializes the time loop.

More formally: let
$d_{\min} = \min\{d_{ij} : W_{ij} \neq 0\}$. Then steps
$t, t+1, \dots, t + d_{\min} - 1$ are eligible for parallel execution because
each only reads from history $\leq t - 1$. For TVB connectomes
$d_{\min}$ is small (the script forces a path of length 0 for self-loops via
`if (i == n) or (D_row[i] == 0): x_src = Xs[i][0][t-1]`), so the practical
parallel slack across timesteps is essentially **one** — i.e. no useful
parallelism along the time axis.

**Within a single timestep**, by contrast, the $N$ centers can be updated in
parallel: all of them only read from `Xs[*][:][≤ t-1]` and write to
`Xs[*][:][t]`, so there are no read-after-write conflicts among them. That
spatial (across-centers) parallelism is what Lab 2 (multi-process) and Lab 3
(GPU) will exploit.

---

## Q2 (Exercise 1.2) — Profile `tvb_seq.py`

`tvb_seq.py` is already instrumented with `tic-toc` pairs around the
simulate body and around every `calculate_coupling` call (`c_duration`
accumulator). Driver: `bench_phase2.py` calls `tvb_seq.simulate(...)` on
each of the three datasets in turn at $\mathtt{tf} = 150$ ms,
$\mathtt{dt} = 0.05$ ms (so $T = 3000$ timesteps).

| Dataset | $N$ | Total time (s) | `calculate_coupling` time (s) | Coupling fraction $p$ |
|---:|---:|---:|---:|---:|
| TVB76  |  76 |   $5.051$ |   $4.831$ | $95.65\%$ |
| TVB192 | 192 |  $26.728$ |  $26.032$ | $97.40\%$ |
| TVB998 | 998 | $628.744$ | $624.182$ | $\mathbf{99.27\%}$ |

**Does it match Q1's $\mathcal{O}(N^2 T)$ prediction?**

Per-$N$ scaling of coupling time:

- TVB76 → TVB192: $N$ ratio $192/76 = 2.53$, $N^2$ ratio $6.39$. Measured
  coupling-time ratio: $26.032 / 4.831 = 5.39$.
- TVB192 → TVB998: $N$ ratio $998/192 = 5.20$, $N^2$ ratio $27.02$. Measured
  coupling-time ratio: $624.182 / 26.032 = 23.98$.

Both ratios are slightly **sub-quadratic** (roughly $0.84 \times N^2$ and
$0.89 \times N^2$). The shortfall is consistent with constant-time
per-iteration overheads in the Python interpreter (loop dispatch, attribute
lookups) becoming a smaller share of total work as $N$ grows — the inner
multiply-add becomes more dominant. So the data is in agreement with
$\mathcal{O}(N^2 T)$ to first order.

**What fraction of execution time is in `calculate_coupling`?**

$95.65\%$ at $N=76$, climbing to $99.27\%$ at $N=998$. **Coupling dominates,
and its share grows with $N$.**

**Why?** Per timestep, coupling does $N \cdot N$ work while local dynamics
+ Forward Euler does $\mathcal{O}(N \cdot M)$ work. The ratio
$\frac{N^2}{N \cdot M} = \frac{N}{M}$ grows linearly with $N$, so any
non-coupling overhead becomes asymptotically negligible.

This makes coupling the obvious target for any acceleration effort —
exactly what Q4–Q9 will exploit.

---

## Q3 (Exercise 1.3) — Zero-delay variant

Same driver, but with `D` overridden to all zeros before calling
`simulate`. The integer-delay matrix `D_timestep` is consequently all zero,
so the `if t >= D_row[i]` guard always passes and the inner branch always
takes the `(D_row[i] == 0) ⇒ Xs[i][0][t-1]` path.

| Dataset | Total time (s) | `calculate_coupling` time (s) | $\Delta$ vs Q2 (total) | Q2 / Q3 |
|---:|---:|---:|---:|---:|
| TVB76  |   $3.309$ |   $3.098$ | $-1.74$ s ($-34.5\%$) | $1.53\times$ |
| TVB192 |  $20.134$ |  $19.487$ | $-6.59$ s ($-24.7\%$) | $1.33\times$ |
| TVB998 | $581.393$ | $577.055$ | $-47.35$ s ($-7.5\%$) | $1.08\times$ |

**Yes, there is a measurable difference, and it shrinks as $N$ grows.** Two
mechanisms account for the speedup of Q3 over Q2:

1. **Branch elision.** With $D = 0$ the inner `if … else …` collapses into
   a single branch: every `(i, n)` pair takes the
   `Xs[i][0][t - 1]` path. Q2's mixed branching forces the interpreter
   through more `if`-tests per iteration.
2. **Memory locality.** All `Xs[i][0][t - 1]` reads land at the same
   "column" $t-1$ of the state history. Even with Python lists, the JIT-y
   compilation tricks of CPython make repeated access to the same nested
   structure cheaper than scattered reads from $\mathtt{Xs}[i][0][t - d_{ij}]$.

**Why does the gap shrink with $N$?** The branch-overhead saving is
constant per inner iteration. As $N$ grows, the actual multiply-add work
per iteration becomes the dominant cost, and the constant branch saving is
diluted ($1.53\times$ → $1.33\times$ → $1.08\times$). By TVB998 the
inner-loop body dominates; branching is in the noise.

---

## Q4 (Exercise 1.4) — Sparse computation

### (a) Theoretical speedup with sparsity $S\%$

In the dense version, `calculate_coupling` runs $N$ multiply-adds per
destination row $i$ (one per source $j$, regardless of $W_{ij}$). In the CSR
version it runs only $\mathrm{NNZ}_i$ multiply-adds, where $\mathrm{NNZ}_i$
is the number of non-zeros in row $i$.

Let $\mathrm{NNZ} = \sum_i \mathrm{NNZ}_i$ be the total non-zero count of
$W$. With sparsity $S\%$ (fraction of *zero* entries), we have
$\mathrm{NNZ} = N^2 \cdot (1 - S/100)$. Hence the **coupling-only speedup**
is:

$$
S_{\text{coupling}} \;=\; \frac{N^2}{\mathrm{NNZ}} \;=\; \frac{1}{1 - S/100}.
$$

This applies *only* to `calculate_coupling`. The end-to-end speedup is
bounded by Amdahl's law:

$$
S_{\text{end-to-end}} \;=\; \frac{1}{(1 - p) + p / S_{\text{coupling}}},
$$

where $p$ is the fraction of total runtime spent in `calculate_coupling`
(measured in Q2).

### (b) Sparsity of TVB192

Computed from the cached `tvb192` connectome:
`np.count_nonzero(W) / W.size`.

| Dataset | $N$ | total entries | non-zeros | zeros | sparsity $S\%$ | density |
|---:|---:|---:|---:|---:|---:|---:|
| TVB76  |  76 |    5,776 |  1,560 |  4,216 | $72.99\%$ | $27.01\%$ |
| TVB192 | 192 |   36,864 |  3,532 | 33,332 | $\mathbf{90.42\%}$ |  $9.58\%$ |
| TVB998 | 998 |  996,004 | 35,730 | 960,274 | $96.41\%$ |  $3.59\%$ |

For TVB192, $S = 90.4188\%$, giving a theoretical coupling speedup of

$$
S_{\text{coupling}}^{\text{theory}} \;=\; \frac{1}{1 - 0.9042} \;\approx\; 10.44\times.
$$

### (c) Measured speedup vs. theoretical

`tvb_seq_sparse.py`, TVB192, 150 timesteps:

| Quantity | Value |
|---|---:|
| `tvb_seq.py` (dense, Q2) — total | $26.728$ s |
| `tvb_seq.py` (dense, Q2) — coupling | $26.032$ s |
| `tvb_seq_sparse.py` — total | $3.847$ s |
| `tvb_seq_sparse.py` — coupling | $3.323$ s |
| **Measured coupling speedup** | $26.032 / 3.323 = \mathbf{7.83\times}$ |
| **Theoretical coupling speedup** (from a + b) | $\mathbf{10.44\times}$ |
| Measured end-to-end speedup | $26.728 / 3.847 = 6.95\times$ |
| Amdahl-predicted end-to-end ($p = 0.974$, $k = 7.83$) | $6.65\times$ |

**Discussion.** The measured coupling speedup ($7.83\times$) falls $\approx
25\%$ short of the theoretical $10.44\times$. Three mechanisms account for
the gap:

- **CSR overhead.** The sparse loop adds two layers of indirection
  (`col_index[i]` lookup to find the source node, plus `D_sparse[i]` for
  the delay), which in CPython are extra `__getitem__` calls per
  iteration. The dense loop indexes a single 2-D array with the loop
  variable directly.
- **Branch overhead.** The inner `if t >= D_sparse[i]` and the
  `(col_index[i] == n) or (D_sparse[i] == 0)` test are still executed per
  non-zero, adding constant cost the simple count $N^2 \to \mathrm{NNZ}$
  doesn't capture.
- **CSR build cost.** A one-time $\mathcal{O}(N^2)$ scan to build
  `W_sparse`, `D_sparse`, `col_index`, `row_pointer` is included in the
  total. For 150 timesteps it amortizes well, but it shifts a few percent
  of work from the steady-state coupling loop.

Crucially, the **end-to-end Amdahl prediction matches measurement
within $\sim 5\%$** ($6.65\times$ predicted vs $6.95\times$ measured). The
slight surplus over Amdahl is consistent with the non-coupling part also
running marginally faster in sparse mode (fewer cache thrashes through
$D_{\text{timestep}}$), but the dominant story is exactly Amdahl.

### (d) Downsides of sparse computations

1. **Indirect indexing kills cache locality.** CSR coupling reads
   `Xs[col_index[i], 0, t - D_sparse[i]]` — `col_index` and `D_sparse` are
   essentially random gather patterns into `Xs`. Each access can miss L1/L2
   cache, whereas the dense version walks `W[n][:]` and `Xs[:][0][...]`
   contiguously.
2. **Vectorization / SIMD becomes harder.** Modern CPUs and NumPy excel at
   contiguous, regular-shape arithmetic. A run of $\mathrm{NNZ}_i$ multiplies
   per row, with $\mathrm{NNZ}_i$ varying across $i$, breaks the
   regularity that lets a vector unit process many elements per
   instruction. Gather instructions exist but typically run at a fraction
   of contiguous-load throughput.
3. **Pre-processing cost.** Building the four CSR arrays (`W_sparse`,
   `D_sparse`, `col_index`, `row_pointer`) is a one-time
   $\mathcal{O}(N^2)$ scan over $W$. For short simulations this overhead
   eats into the speedup; for long ones it amortizes.
4. **Storage overhead per non-zero.** CSR stores three numbers per
   non-zero (value, column index, plus a fraction of `row_pointer`).
   Storage is a net win only when sparsity exceeds roughly $60$–$70\%$,
   below which the dense form is more compact and faster.
5. **Load imbalance under parallelism.** Different rows have different
   $\mathrm{NNZ}_i$; if Lab 2/3 splits work by row, "fat" rows become
   stragglers. The dense version has uniform per-row work and so balances
   trivially.

---

## Q5 (Exercise 1.5) — MLP local dynamics

### (a) Dense MLP timings, TVB192, 15 timesteps

`tvb_seq_mlp.py` with `USE_SPARSE = False`, $\mathtt{tf} = 15$ ms:

| Metric | Time (s) | Fraction of total |
|---|---:|---:|
| Total simulation     | $4.717$ | — |
| `step` (incl. MLP $f$) | $2.771$ | $58.7\%$ |
| `calculate_coupling` | $1.916$ | $\mathbf{40.6\%}$ |

For completeness (used in Q6 below), sequential dense MLP on the other two
datasets at the same $\mathtt{tf}$:

| Dataset | $N$ | Total (s) | Step (s) | Coupling (s) |
|---:|---:|---:|---:|---:|
| TVB76  |  76 |  $1.104$ | $0.884$ | $0.211$ |
| TVB192 | 192 |  $4.717$ | $2.771$ | $1.916$ |
| TVB998 | 998 | $66.983$ | $12.410$ | $54.418$ |

(Note how the coupling fraction climbs again from $19.1\%$ at TVB76 to
$81.2\%$ at TVB998 — the MLP cost is $\mathcal{O}(N)$, the coupling cost is
$\mathcal{O}(N^2)$, so for large $N$ the picture from Q2 reasserts itself
even with the heavier per-node $f$.)

### (b) Maximum theoretical speedup of accelerating coupling alone

Amdahl's law: if coupling consumes a fraction $p$ of the total runtime, and
we accelerate it by factor $k$, the end-to-end speedup is

$$
S_{\text{end-to-end}}(k) \;=\; \frac{1}{(1 - p) + p/k}.
$$

The **maximum** end-to-end speedup is the limit $k \to \infty$:

$$
S_{\text{max}} \;=\; \lim_{k \to \infty} \frac{1}{(1 - p) + p/k} \;=\; \frac{1}{1 - p}.
$$

For the TVB192 MLP run with $p = 0.4062$:

$$
S_{\text{max}} \;=\; \frac{1}{1 - 0.4062} \;=\; \frac{1}{0.5938} \;\approx\; \mathbf{1.68\times}.
$$

So with the MLP as local dynamics, even infinite coupling acceleration
caps the end-to-end speedup at $1.68\times$ — accelerating only the
coupling is *not* the right plan when $f$ is heavy; the step itself must
be accelerated too.

### (c) Sparse MLP timings, TVB192, 15 timesteps — comparison to Amdahl

`tvb_seq_mlp.py` with `USE_SPARSE = True`, same parameters:

| Metric | Q5a (dense) | Q5c (sparse) | Speedup vs Q5a |
|---|---:|---:|---:|
| `calculate_coupling` |  $1.916$ s | $0.219$ s | $\mathbf{8.75\times}$ |
| `step`               |  $2.771$ s | $2.340$ s | $1.18\times$ |
| Total simulation     |  $4.717$ s | $2.584$ s | $\mathbf{1.83\times}$ |

**Amdahl prediction.** With $p = 0.4062$ and the measured coupling
speedup $k = 8.75$:

$$
S_{\text{predicted}} \;=\; \frac{1}{(1 - 0.4062) + 0.4062 / 8.75}
\;=\; \frac{1}{0.5938 + 0.0464}
\;=\; \frac{1}{0.6402}
\;\approx\; 1.56\times.
$$

**Measured: $1.83\times$. Predicted: $1.56\times$.**

The measured value is $\sim 17\%$ above Amdahl's prediction. The discrepancy
isn't a violation of the law — it shows the implicit assumption (that the
non-accelerated part stays *exactly* the same) doesn't hold here: the
`step` time also drops from $2.771$ s to $2.340$ s (a $1.18\times$
side-speedup, likely from reduced `for t / for n` interpreter overhead in
the simpler sparse-mode `simulate` loop body, plus warm CPU caches).

If we plug the actual `step` and `coupling` times into
$T_{\text{Q5c}} \approx 2.340 + 0.219 = 2.559$ s, that predicts a total
of $\sim 2.56$ s — the *measured* $2.584$ s matches to $1\%$. So the
"surplus" over Amdahl is fully accounted for by the side-speedup of
`step`, and Amdahl's law itself holds.

---

## Q6 (Exercise 1.6) — Vectorized TVB+MLP, dense

Implementation: `Lab_1/Lab_1 Scripts/L1_Q6.py` (mirrored at
`Lab_1/report/lab1/code/L1_Q6.py` for LaTeX listing).

**Vectorization strategy.**

1. **State storage.** Replace nested Python lists with one
   `Xs = np.zeros((N, M, T))` array.
2. **Local dynamics $f$ (the MLP).** Stack the per-node state into a row
   matrix $\mathtt{sv} \in \mathbb{R}^{N \times M}$, then run the entire
   batch through the MLP with two matrix multiplications and one ReLU:
   `hidden = sv @ l1w + l1b` → `np.maximum(hidden, 0)` → `out = hidden @ l2w + l2b`.
   This collapses the four nested per-node loops in `tvb_seq_mlp.py` into
   three NumPy calls.
3. **Coupling.** Build the `(N, N)` "delayed source" lookup in three steps:
   - Default gather: `x_src[n, i] = Xs[i, 0, t - delays[n, i]]`, with
     `np.clip` to keep indices in range.
   - Override with `Xs[i, 0, t - 1]` where `i == n` or `delays[n, i] == 0`.
   - Mask to zero where `t < delays[n, i]` (insufficient history).
   Final `c_in = 1e-3 * np.sum(W * (x_src - 1.0), axis=1)`.

**Validation** (`validate_q6.py`, dev machine, 15 timesteps):
max $|X_{\text{seq}} - X_{\text{vec}}| \leq 5.5 \times 10^{-14}$ on TVB76
and TVB192 — i.e. numerically identical within float64 round-off.

**Timings on the AWS VM** (15 timesteps):

| Dataset | Sequential MLP (s) | Vectorized (s) | Total speedup | Step speedup | Coupling speedup |
|---:|---:|---:|---:|---:|---:|
| TVB76  |  $1.104$ | $0.0490$ | $\mathbf{22.5\times}$ | $0.884 / 0.0095 = 93.1\times$ | $0.211 / 0.0369 = 5.7\times$ |
| TVB192 |  $4.717$ | $0.1811$ | $\mathbf{26.0\times}$ | $2.771 / 0.0205 = 135.2\times$ | $1.916 / 0.1570 = 12.2\times$ |
| TVB998 | $66.983$ | $4.9302$ | $\mathbf{13.6\times}$ | $12.41 / 0.1212 = 102.4\times$ | $54.418 / 4.7953 = 11.3\times$ |

**Where does the speedup come from?**

- The MLP $f$ is the biggest winner ($\sim 100\times$): one $\mathtt{(N,2)} \times \mathtt{(2,64)}$ matmul replaces $N \cdot L \cdot M$ Python multiply-adds. NumPy dispatches a single BLAS-backed kernel.
- Coupling improves more modestly ($\sim 5$–$12\times$): the work is still $\mathcal{O}(N^2)$ floats, but it now runs in a few NumPy ufunc calls instead of $N \cdot N$ Python iterations.
- The total-simulation speedup is *capped by Amdahl* — at TVB998 step is much smaller than coupling, so the bottleneck shifts back to the $\mathcal{O}(N^2)$ coupling work even in vectorized form, and the total speedup drops to $13.6\times$.

---

## Q7 (Exercise 1.7) — Vectorized TVB+MLP, sparse

Implementation: `Lab_1/Lab_1 Scripts/L1_Q7.py`.

**Strategy.** CSR build (`np.where(W != 0)` → `rows, cols`; `nnz_per_row`
via `np.bincount`; `row_pointer` via `np.cumsum`). Per-timestep coupling:

1. Gather `x_src[k] = Xs[col_index[k], 0, t - D_sparse[k]]` with the same
   self/zero/invalid masking as Q6, but over the flat NNZ-length axis.
2. Per-row sum via `np.bincount(row_for_nnz, weights=contrib, minlength=N)`
   — handles empty rows correctly (unlike `np.add.reduceat`).

**Validation** (`validate_q7.py`, dev machine, 15 timesteps):
max $|X_{\text{Q7}} - X_{\text{seq-sparse}}| \leq 5.5 \times 10^{-14}$, and
max $|X_{\text{Q7}} - X_{\text{Q6-dense}}| \leq 4.1 \times 10^{-14}$ — Q7
matches both the sparse reference *and* Q6 within float64 round-off.

**Timings on the AWS VM** (15 timesteps):

| Dataset | $N$ | NNZ | Q6 vectorized dense | Q7 vectorized sparse | Q7 / Q6 (total) | Q7 / Q6 (coupling) |
|---:|---:|---:|---:|---:|---:|---:|
| TVB76  |  76 |  1,560 | $0.0490$ s | $0.0302$ s | $1.62\times$ faster | $0.0369 / 0.0187 = 1.97\times$ |
| TVB192 | 192 |  3,532 | $0.1811$ s | $0.0520$ s | $3.48\times$ faster | $0.1570 / 0.0317 = 4.95\times$ |
| TVB998 | 998 | 35,730 | $4.9302$ s | $0.3761$ s | $\mathbf{13.11\times}$ faster | $4.7953 / 0.2753 = \mathbf{17.42\times}$ |

**Theoretical sparse coupling speedups** (from $S\%$ in Q4b):

| Dataset | $S$ | $1/(1 - S/100)$ | Measured Q7-vs-Q6 coupling | Efficiency |
|---:|---:|---:|---:|---:|
| TVB76  | $72.99\%$ |  $3.70\times$ |  $1.97\times$ | $53\%$ |
| TVB192 | $90.42\%$ | $10.44\times$ |  $4.95\times$ | $47\%$ |
| TVB998 | $96.41\%$ | $27.86\times$ | $17.42\times$ | $63\%$ |

**Discussion. Yes, vectorized sparse gives a meaningful gain over
vectorized dense — but only because the *dense* baseline still has $N^2$
work to do.** The reason for the speedup, and for the gap to theoretical:

- *Why a gain at all?* Vectorized dense (Q6) materializes the full
  $(N, N)$ coupling matrix every timestep — that's $N^2$ floats of
  arithmetic, and on TVB998 that's $\sim 10^6$ multiplies times $T$
  timesteps. The CSR version replaces that with $\mathrm{NNZ}$
  arithmetic — at $96.41\%$ sparsity, $\sim 27\times$ less work.
- *Why below theoretical?* Sparse loses NumPy's ideal contiguous-array
  speedup. Q6's coupling is one big elementwise multiply followed by a
  contiguous row sum — perfect for the NumPy SIMD path. Q7 instead does
  fancy indexing (`Xs[col_index, 0, ...]`) which is a gather, plus
  `np.bincount` for the per-row reduction. Both are slower per element
  than the dense path. So we trade $27\times$ less work for $\sim 1.6\times$
  per-element penalty, ending up at $17.4\times$.
- *Why does the efficiency dip on TVB192 ($47\%$)?* At moderate $N$,
  fixed Python-side overheads (CSR build, mask construction) eat a
  larger share. On TVB998 those overheads amortize over far more
  steady-state work, so efficiency rebounds to $63\%$.

So the gain is real and exactly where it should be — sparser = bigger gain,
in approximate proportion to $1/(1 - S/100)$, with a roughly constant
per-element penalty for the gather pattern.

---

## Q8 (Exercise 1.8) — JIT the sequential MLP

Implementation: `Lab_1/Lab_1 Scripts/L1_Q8.py`.

**Strategy.** Refactored `tvb_seq_jit.py` into three `@njit(cache=True)`
functions: `f_mlp` (per-node MLP forward pass with explicit loops over
$L$), `calculate_coupling` (per-node coupling sum), `simulate_jit` (the
outer time/node loops). Closed the `D_timestep` global bug from the
provided `tvb_seq_jit.py` by passing it as an explicit argument.

**Validation** (`validate_q8.py`, dev machine, 15 timesteps; first run
discarded as JIT warm-up):
max $|X_{\text{Q8}} - X_{\text{seq}}| \leq 6.1 \times 10^{-14}$.

**Timings on the AWS VM** (15 timesteps).

The proper Q8 comparison is `tvb_seq_jit.py` *without* `@jit` (the
provided NumPy-array script, run as-shipped) versus the same structure
with `@njit` decorators added (`L1_Q8.py`). Numbers from
`bench_q8_baseline.py` (no-JIT) and `bench_phase2.py` (JIT, warm):

| Dataset | tvb_seq_jit (no JIT) | L1_Q8 (warm JIT) | **JIT speedup** | tvb_seq_mlp.py (lists, no JIT) for context |
|---:|---:|---:|---:|---:|
| TVB76  | $2.439$ s  | $0.0085$ s | $\mathbf{287\times}$ | $1.104$ s |
| TVB192 | $10.776$ s | $0.0505$ s | $\mathbf{213\times}$ | $4.717$ s |

**Yes, there is an enormous difference** — adding `@jit` decorators
yields a **two-orders-of-magnitude** speedup over the same code without
them.

**A subtler observation about the no-JIT baseline.** Notice that
`tvb_seq_jit.py` *without* JIT is actually **~2× slower** than
`tvb_seq_mlp.py` (lists) — $2.44$ s vs $1.10$ s on TVB76, $10.78$ s vs
$4.72$ s on TVB192. The reason is that scalar reads from a NumPy array
(`Xs[n, 0, t-1]`) materialize an `np.float64` object per access, with
more dispatch overhead than Python's native `float` arithmetic on a
list. So replacing lists with NumPy arrays *only* pays off once you
also apply JIT — without JIT, NumPy arrays make scalar code slower, not
faster. This is precisely why `tvb_seq_jit.py` was prepared with NumPy
arrays as a setup for `@jit`: the array layout is what lets Numba
compile efficient native code.

**Why the massive speedup with JIT.** Numba compiles the entire
`simulate_jit` function — including the `for t / for n / for i` triple
nest and all `if`-tests — into native machine code. The per-iteration
Python interpreter and NumPy scalar overhead is eliminated. The
remaining cost is the actual multiply-adds and branches, executed at
near-C speed.

(Note on cold-call cost: the first JIT call compiles the function and
takes $\sim 2$ s on TVB76; subsequent calls hit the cache and run in
$\leq 50$ ms. The numbers above discard the first cold run.)

---

## Q9 (Exercise 1.9) — JIT the vectorized version

Implementation: `Lab_1/Lab_1 Scripts/L1_Q9.py`.

**Strategy.** Take Q6's vectorized layout and refactor for Numba: keep
matrix multiplications (`@`) for the MLP forward pass (Numba compiles them
into LAPACK calls), but unroll the coupling gather into explicit
double-loops because Numba does not handle the broadcasted fancy-indexing
pattern of Q6 cleanly.

**Validation** (`validate_q9.py`, dev machine, 15 timesteps):
max $|X_{\text{Q9}} - X_{\text{Q6}}| \leq 4.1 \times 10^{-14}$,
max $|X_{\text{Q9}} - X_{\text{Q8}}| \leq 5.0 \times 10^{-14}$.

**Timings on the AWS VM** (15 timesteps; warm):

| Dataset | Q6 vectorized | Q8 JIT seq | Q9 JIT vect | Q9 / Q6 | Q9 / Q8 |
|---:|---:|---:|---:|---:|---:|
| TVB76  | $0.0490$ s | $0.0085$ s | $0.0063$ s |  $7.78\times$ | $1.35\times$ |
| TVB192 | $0.1811$ s | $0.0505$ s | $0.0259$ s |  $6.99\times$ | $1.95\times$ |
| TVB998 | $4.9302$ s | — (not required) | $0.7967$ s | $\mathbf{6.19\times}$ | — |

**Is the JIT version of the vectorized code faster than the JIT version
of the non-vectorized code?**
**Yes, but only modestly** — Q9 beats Q8 by $1.35\times$ on TVB76 and
$1.95\times$ on TVB192. The win comes from Q9's MLP using
`hidden = sv @ l1w + l1b` (single LAPACK call for all $N$ nodes) versus
Q8's per-node Python-style inner loop that Numba compiles row-by-row.

**Does JIT compilation on the vectorized code yield as much of a
speedup as on the non-vectorized version?**
**No — far less.** Comparing the *speedup gained from JIT*:

| Path | Baseline | JIT'd | Speedup from JIT |
|---|---:|---:|---:|
| Sequential MLP → Q8 (TVB192)        |  $4.717$ s | $0.0505$ s | $\mathbf{93\times}$ |
| Vectorized (Q6) → Q9 (TVB192)       | $0.1811$ s | $0.0259$ s | $\mathbf{7\times}$  |
| Sequential MLP (TVB76)              |  $1.104$ s | $0.0085$ s (Q8) | $\mathbf{130\times}$ |
| Vectorized (Q6) (TVB76) → Q9        | $0.0490$ s | $0.0063$ s | $\mathbf{7.8\times}$ |

JIT removes Python interpreter overhead. In sequential code, that
overhead *is* most of the runtime, so JIT gives a $\sim 100\times$ jump.
In NumPy-vectorized code, the heavy lifting already runs inside compiled
NumPy/BLAS kernels, so only the surrounding Python glue (the `for t in
range` loop, mask construction, `np.where`) is left to compile away —
that's only $7\times$ worth of overhead.

**Bottom line.** Vectorization and JIT are partially redundant
optimizations of the same Python-overhead axis. Once you have one, the
other has much less to do. The full progression on TVB192 (15 ts) is:

| Variant | Time (s) | Speedup vs sequential |
|---|---:|---:|
| Sequential MLP (Q5a)             | $4.717$ | $1.0\times$ |
| Vectorized dense (Q6)            | $0.1811$ | $26\times$ |
| Vectorized sparse (Q7)           | $0.0520$ | $91\times$ |
| JIT sequential (Q8)              | $0.0505$ | $93\times$ |
| **JIT vectorized (Q9)**          | $\mathbf{0.0259}$ | $\mathbf{182\times}$ |

So the best Lab 1 path is **JIT-applied to the vectorized variant**,
combining the per-element efficiency of NumPy/BLAS with the elimination
of Python loop overhead — but the compounding is sub-multiplicative.

---

## Hardware footnote (always include in the .tex)

All measurements taken on the course AWS VM:
- Intel Xeon Platinum 8259CL @ 2.50 GHz (Cascade Lake), 1 physical core / 2 SMT threads.
- 3.7 GiB RAM, Ubuntu 24.04, kernel 6.17.0-1010-aws.
- Python 3.12.3, NumPy 2.4.4, Numba 0.65.0, SciPy 1.17.1.

(See `AWS_INSTANCE_SPECS.md` at the project root.)

## LLM disclosure (for Section 3 of the report)

- LLM (Claude) helped:
  - Set up the LaTeX template and project tooling (preamble, Makefile, SSH config, `aws-ip.sh`, `new-lab.sh`).
  - Produce reference docs (`TVB_ALGORITHM.md`, `LAB_1.md`, etc.) by reading the assignment PDF and provided scripts.
  - Discuss vectorization and JIT trade-offs and validate that the proposed solutions match the references.
- Code:
  - The four submitted scripts (`L1_Q6.py` … `L1_Q9.py`) were drafted with LLM assistance, then validated against the reference scripts (`tvb_seq_mlp.py`) and timed by me on the course AWS VM. Validation confirmed numerical equivalence to within float64 round-off (max $\sim 6 \times 10^{-14}$).
- Writing:
  - The report prose (analytical derivations, discussion paragraphs, table interpretations) was written by me based on the measurement data; LLM provided phrasing suggestions on a per-paragraph basis.
