# Lecture 1 & 2 — Demo scripts walkthrough

These scripts under `Lecture_1&2 scripts/` aren't homework; they're reference
patterns the lectures introduced for **profiling**, **vectorization**, and
**JIT**. Lab 1 expects you to apply these patterns yourself.

## Profiling toolkit (Bessel-function family)

Five scripts compute the same Bessel kernel four different ways. Use them as
templates whenever the lab asks you to instrument something.

| Script | Mechanism | Good for |
|---|---|---|
| `bessel_kernel.py`       | Plain function, used as a target. Run as `python -m timeit ...` or call from a notebook. | Defining the workload separately from the timer. |
| `bessel_time.py`         | `time.time()` wall-clock around inner & outer regions. | Quick *wall-clock* numbers, includes I/O and other processes. |
| `bessel_process_time.py` | `time.process_time()` instead of `time()`. | CPU-only time of *this* process. **Excludes child processes** — see `processtime_vs_time.py`. |
| `bessel_timeit.py`       | `timeit.timeit(lambda: f(arg), number=N)` and `timeit(setup, stmt, number=N)`. | Robust micro-benchmarks; runs N times and you usually take the min/N. |
| `bessel_cprofile.py`     | `cProfile.Profile()` + `pstats.Stats(...).sort_stats('tottime')`. | Function-level breakdown of where time goes. Pair with `snakeviz` for visualization. |

Key idiom from `bessel_cprofile.py`:

```python
prof = cProfile.Profile()
prof.enable()
work()
prof.disable()
pstats.Stats(prof).sort_stats('tottime').print_stats()
```

`primes_cprofile.py` shows how to dump pstats output to a file and re-sort it
later (`p.sort_stats("calls")` vs `"tottime"`). Useful for big runs you don't
want to re-execute.

## `processtime_vs_time.py` — when CPU time lies

Demonstrates that `time.process_time()` does **not** count CPU time spent in
child processes (e.g. via `ProcessPoolExecutor`), while `time.time()` does
(it's wall-clock). When you parallelize across processes in Lab 2/3, prefer
`time.time()` for end-to-end speedups, or use `time.process_time()` to
investigate single-process efficiency.

## `gol.py` — Game of Life: elementwise vs vectorized

Two implementations of the same simulation:

- `gol_elementwise(N, num_generations)`: nested `for row, col` loops, helper
  function decorated with `@jit`. This is the "before" baseline.
- `gol_vectorized(N, numGenerations)`: Builds index arrays
  `p = [0, 0, 1, 2, ..., N-2]` and `q = [1, 2, ..., N-1, N-1]` to do all 8
  neighbor lookups as full-array slices, e.g. `grid[:, p]`. The whole
  generation update is one expression.

The trick worth stealing: **using shifted index arrays to express stencil
neighbors** without explicit loops. Same pattern shows up in coupling
matrices.

## `mb.py` — Mandelbrot: sequential vs vectorized

- `sequential(N, MAX_ITER, ...)`: per-pixel `for i, j` loop calling
  `do_calc(k, z, c)`.
- `vectorized(N, ...)`: `do_calc_vec` keeps a **boolean mask** of points still
  inside the set and updates them in a single broadcast: `z = mask * (z*z + c)`.
  The output array is updated with `np.where(~mask & (out == 0), i, out)`.

Pattern worth stealing for Lab 1.6: **mask out work that doesn't apply this
iteration**. You'll need it in vectorized `calculate_coupling` to handle the
`t < D_row[i]` and self-loop cases.

## `ip_jit.py` and `ip_vec.py` — Seam carving

Same algorithm (content-aware image resizing), two flavors:

- `ip_jit.py`: Pure Python lists everywhere, `@jit` only on the inner DP
  (`compute_cumulative_energy`). Demonstrates that JIT can be applied
  selectively to the hot loop.
- `ip_vec.py`: NumPy arrays end-to-end, plus `@jit` on the cumulative-energy
  step (the only part that's still a sequential dependency `M[i, j] +=
  min(M[i-1, j-1..j+1])`).

**Caveat**: `ip_jit.py` calls `image.shape[:2]` on a PIL `Image`, which has
no `.shape`. Either remove that print or convert via
`np.array(image).shape[:2]`. `ip_vec.py` reads `hq.png`, which isn't shipped
— substitute `lq.png` or your own.

The bigger lesson: **vectorize what you can, JIT what you can't**. The
cumulative-energy DP can't be vectorized along the y-axis (each row depends
on the previous), so JIT is the right tool there.

## What to take into Lab 1

| Lecture pattern | Where it shows up in Lab 1 |
|---|---|
| Tic-toc with `time.time()` around regions of interest | Exercises 1.2, 1.3, 1.5, 1.6, 1.7, 1.8, 1.9 |
| `cProfile` + `snakeviz` to find hotspots | Useful even though not strictly required — confirms `calculate_coupling` is the bottleneck |
| Mask + `np.where` for conditional updates | Vectorized `calculate_coupling` (Ex. 1.6) |
| Shifted index arrays for stencils | Could help if you fully vectorize across the `n` loop |
| Selective `@jit` on the hot inner function | Exercises 1.8, 1.9 |
| Warm up before timing JIT | Exercise 1.8 ("beware not to measure the initial JIT compilation time") |
