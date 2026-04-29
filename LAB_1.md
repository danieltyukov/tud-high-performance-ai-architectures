# Lab 1 — Sequential analysis, sparsity, vectorization, JIT

Total: ~92.5 points across 9 exercises. Code submission required only for
exercises **1.6, 1.7, 1.8, 1.9** as `L1_Q6.py`, `L1_Q7.py`, `L1_Q8.py`, `L1_Q9.py`.

See `TVB_ALGORITHM.md` for the math.
See `SUBMISSION_GUIDELINES.md` for naming and grading rules.

## Provided scripts (in `Lab_1/Lab_1 Scripts/`)

| Script | Local dynamics | Storage | Sparse mode | Notes |
|---|---|---|---|---|
| `tvb_seq.py`        | hand-coded `f(x,y,freq)` | nested Python lists | no  | Baseline. Default tf=150 ms, dataset=TVB76. |
| `tvb_seq_sparse.py` | hand-coded                | nested Python lists | **yes** (CSR) | Default dataset=TVB192. |
| `tvb_seq_mlp.py`    | **MLP** (L=64, M=2)       | nested lists        | flag `USE_SPARSE` | Default tf=15 ms, dataset=TVB192. |
| `tvb_seq_jit.py`    | **MLP**, parameter-arg style | NumPy `Xs[N,M,T]` | no | Numba-friendly layout. **Has a known bug** (see below). |

### Default parameters (mostly the same across files)

```python
dt    = 0.05    # ms
tf    = 150.0   # 15.0 in the MLP scripts
speed = 4.0     # mm/ms
freq  = 1.0
M     = 2
```

So `total_timesteps = tf/dt` = 3000 (or 300 for tf=15).

### Heads-up bugs / oddities to watch for

- `tvb_seq_jit.py` references `D_timestep` inside `simulate(...)` but never
  passes it as a parameter — it relies on it being a global created in
  `__main__`. If you refactor / call `simulate` from elsewhere, you'll get a
  `NameError`. Pass `D_timestep` explicitly.
- `Lecture_1&2 scripts/ip_jit.py` calls `image.shape[:2]` on a PIL `Image`
  object — PIL has no `.shape`. The script as-shipped will crash on the print;
  use `image.size` or convert to NumPy first. (Demo bug, not lab code.)
- `Lecture_1&2 scripts/ip_vec.py` reads `hq.png`, but only `lq.png` is
  shipped. Rename or supply your own image.
- `lib/mlp_params.py` slices `mlp_params` (a Python list) with arithmetic —
  works, but `f()` inside `tvb_seq_jit.py` does the same slicing **every call**
  on a NumPy array. That's pure overhead per timestep; precompute once.

## Exercise-by-exercise plan

### 1.1 — Pen-and-paper analysis (20 pts)

1. Time complexity wrt $N$ (centers) and $T$ (timesteps): the dominant term is
   the `for n: for i in range(N)` coupling double-loop inside the timestep
   loop, so it is $\mathcal{O}(N^2 \cdot T)$. The local-dynamics + step part
   is $\mathcal{O}(N \cdot T)$.
2. State memory: $N \cdot M \cdot T$ elements; scales linearly with each.
3. Linear $K_{\text{pre}}$ factoring: see `TVB_ALGORITHM.md` — the trick is to
   precompute $\sum_{j} W_{ij}$ once per row.
4. Parallelism across timesteps: limited by min-delay barrier; see
   TVB_ALGORITHM.md.

### 1.2 — Profile `tvb_seq.py` (7.5 pts)

Add `tic-toc` (use `time.time()` or `time.perf_counter()`) around:
- the *entire* `simulate` body (already has `start`/`end`).
- only the `calculate_coupling` call (already accumulated into `c_duration`).

Run for **150 timesteps** on TVB76, TVB192, TVB998. Report total time and
coupling time. Confirm coupling dominates and scales as $\mathcal{O}(N^2)$.

### 1.3 — Zero-delay version (7.5 pts)

Override D with all zeros. Re-run 1.2. Coupling time should be ~the same — the
inner loop still does N multiplies per destination; only the index math
slightly changes. Use this to argue that the cost is in the multiply-add, not
in the delay-handling branches.

### 1.4 — Sparse computation (20 pts)

1. Theoretical speedup with sparsity $S\%$: $\dfrac{1}{1 - S/100}$ for the
   coupling part only. Apply Amdahl's law to get end-to-end speedup.
2. TVB192 sparsity: count zeros in `W` directly:
   `np.mean(W == 0) * 100`. (Around 60–70% typical.)
3. Run `tvb_seq_sparse.py` for 150 timesteps and compare measured vs.
   theoretical.
4. Downsides of sparse: indirect indexing → cache-unfriendly; CSR overhead per
   row; loses regularity that vectorization/SIMD wants; preprocessing cost.

### 1.5 — MLP local dynamics (10 pts)

1. Run `tvb_seq_mlp.py` with `USE_SPARSE=False` for **15 timesteps** on
   TVB192. Note `step` time and `calculate_coupling` time.
2. With MLP, local dynamics gets *much* heavier ($\approx 256$ MACs vs. $\sim 5$ ops). So the
   share of total time spent on coupling drops — Amdahl's law caps the
   speedup of accelerating coupling alone.
3. Re-run with `USE_SPARSE=True`. Coupling speeds up; total speedup follows
   Amdahl with the new fraction.

### 1.6 — Vectorized TVB + MLP, dense (12.5 pts) → submit `L1_Q6.py`

Refactor `tvb_seq_mlp.py` into NumPy:

- Replace nested Python lists with NumPy arrays. The provided NumPy-ready MLP
  weights are in `lib/mlp_params.py` as `layer_1_w_np`, `layer_1_b_np`,
  `layer_2_w_np`, `layer_2_b_np`.
- Vectorize **`f` (the MLP)** as two `np.matmul` (or `@`) calls with a ReLU in
  between. You can run the MLP for *all N nodes at once* by stacking states
  into an `(N, M)` matrix.
- Vectorize **`calculate_coupling`**:
  - Build a "delayed-source" array of shape (N, N): for each (n, i), pick
    `Xs[i, 0, t - D_timestep[n, i]]`. Use `np.take_along_axis` or fancy
    indexing.
  - Apply the delay-validity mask with `np.where` (the spec hints at this).
  - The pre-synapse subtract becomes a broadcast: `(x_src - 1.0)`.
  - Multiply by W and sum along the source axis.
- Optionally vectorize the `for n` loop in `simulate` too (you mostly have to,
  for big speedups).

Run for **15 timesteps** on TVB76, TVB192, TVB998. Report total + per-part
speedup against the sequential MLP version. (Run sequential MLP on 76 and
998 too — `tvb_seq_mlp.py` only ships configured for TVB192.)

### 1.7 — Vectorized TVB + MLP, sparse (12.5 pts) → submit `L1_Q7.py`

Same as 1.6 but use the CSR arrays. Vectorization of sparse coupling is
*tricky* — fancy indexing on `col_index` lets you gather all source x's, then
`np.add.reduceat` with `row_pointer[:-1]` does the per-row sum:

```python
src      = Xs[col_index, 0, t - D_sparse]    # shape (NNZ,)
contrib  = W_sparse * (src - 1.0)
c_in_all = np.add.reduceat(contrib, row_pointer[:-1])  # shape (N,)
```

The 15-timestep run probably won't show a meaningful speedup vs 1.6 — you've
traded contiguous `(N, N)` math for `(NNZ,)` math, which kills vectorization
efficiency and adds gather overhead. That's the expected answer.

### 1.8 — JIT the sequential MLP (5 pts) → submit `L1_Q8.py`

Start from `tvb_seq_jit.py`. Add `@jit` decorators to the hot functions
(`f`, `calculate_coupling`, `step`, optionally `simulate`). Run for **15
timesteps** on TVB76 and TVB192. **Beware first-call compilation cost** —
either warm up with a tiny call before timing, or use `@jit(cache=True)` and
discard the first run.

Don't forget to **pass `D_timestep` to `simulate` explicitly** — see the bug
note above.

### 1.9 — JIT the vectorized version (5 pts) → submit `L1_Q9.py`

Apply Numba to your 1.6 code. Numba supports a useful subset of NumPy, so
some operations may need to be unrolled back into loops it can compile well.

The expected finding: JIT on top of vectorized code gives a **smaller**
speedup than JIT on top of pure-Python code, because the vectorized version
is already running in compiled C inside NumPy. JIT can still help when there
is residual Python control flow around NumPy calls.

## Suggested working order this weekend

1. Read this file + `TVB_ALGORITHM.md`.
2. Run `tvb_seq.py` locally — confirm it works, look at the plot.
3. Pen-and-paper 1.1 (no code needed).
4. AWS up: do 1.2, 1.3, 1.4, 1.5 (just runs + numbers, no big refactors).
5. The two big refactors: 1.6 then 1.7. Submit `L1_Q6.py`, `L1_Q7.py`.
6. JIT pass: 1.8 then 1.9. Submit `L1_Q8.py`, `L1_Q9.py`.
7. Write the report; sanity-check numbers on AWS again before submitting.
