# The Virtual Brain (TVB) — Algorithm reference

This is the math + data layout that every Lab 1 script implements.
All four `tvb_seq*.py` files are variations on this same loop.

## What TVB models

TVB partitions the brain into **$N$ regions** ("centers"). Each center represents
the aggregate activity of a population of neurons (a *neural mass*). Centers
are sparsely interconnected with connection-specific **weights** (synaptic
strength) and **delays** (signal-propagation time, derived from physical
distances and a propagation speed).

Per-patient personalization comes from MRI-derived connectivity: each patient's
weight matrix $W$ and tract-length matrix $D$ are different, so simulations must
be re-run repeatedly during model fitting. **That re-fitting loop is the
workload the course wants to accelerate.**

## State and equations

Each center $i \in [1, N]$ has an $M$-dimensional state vector
$\vec{X}_i(t) \in \mathbb{R}^M$. In Lab 1, $M = 2$ (two state variables $x$ and
$y$ per center).

The continuous dynamics are:

$$
\frac{d\vec{X}_i(t)}{dt} \;=\; F\!\bigl(\vec{X}_i(t)\bigr) \;+\; C_i(t) \;+\; u(t) \;+\; \eta(t)
$$

- $F$: local dynamics (per-center). In `tvb_seq.py` it is a hand-coded
  FitzHugh–Nagumo-like nonlinearity. In `tvb_seq_mlp.py` it is replaced by a
  small MLP (input $M = 2$, hidden $L = 64$, output $M = 2$).
- $C_i(t)$: coupling input — the contribution of all *other* centers, with delays.
- $u(t)$, $\eta(t)$: external input and noise. **Ignored in this lab.**

Forward Euler discretization (timestep $h = \mathtt{dt}$):

$$
\vec{X}_i(t+1) \;=\; \vec{X}_i(t) \;+\; h \cdot \bigl( F(\vec{X}_i(t)) \;+\; C_i(t) \bigr)
$$

Coupling input:

$$
C_i(t) \;=\; K_{\text{post}}\!\left(\;\sum_{j=1}^{N} W_{ij} \cdot K_{\text{pre}}\!\bigl(X_j(t - d_{ij}),\; X_i(t)\bigr)\;\right)
$$

- $W_{ij}$: connection weight from $j \to i$ (most are zero — sparse).
- $d_{ij}$: integer delay in timesteps, derived as
  $d_{ij} = \lfloor (D_{ij} / \mathtt{speed}) / \mathtt{dt} \rfloor$.
- $K_{\text{pre}}$, $K_{\text{post}}$: pre- and post-synaptic transforms. In
  Lab 1 code:
  - `pre(x_src, x_dst)` $= x_{\text{src}} - 1.0$
  - `post(gx)` $= 10^{-3} \cdot gx$

> Note: the $K_{\text{pre}}$ used in code depends only on $x_{\text{src}}$ in
> the Lab 1 scripts (it ignores $x_{\text{dst}}$). Exercise 1.1.3 asks you to
> exploit a *linear* $K_{\text{pre}}$ to factor the inner sum — this is a real
> optimization on the existing code.

## Data layout (sequential reference)

```
W[N][N]           # weights, dense
D[N][N]           # tract lengths (mm)
D_timestep[N][N]  # = int((D[i][j] / speed) / dt)
Xs[N][M][T]       # state history; Xs[n][0][t] is x of node n at timestep t
T  = tf / dt      # total timesteps
```

Sequential update order per timestep $t$ (after $t = 0$ init):

```
for n in 0..N-1:
    c_in    = calculate_coupling(Xs, W[n], D_timestep[n], t, n)   # delayed sum
    X_new   = step(Xs, t, n, c_in, dt, ...)                       # Forward Euler
    Xs[n][:][t] = X_new
```

`calculate_coupling` reads $\mathtt{Xs}[i, 0, t - \mathtt{D\_timestep}[i, n]]$
for every source $i$, guarded by $t \geq \mathtt{D\_row}[i]$ (skip until enough
history exists) and a special case for the self-loop and zero-delay edges.

## Sparse (CSR) form

Most entries of $W$ are zero. Lab 1 uses **Compressed Sparse Row** to skip
multiplications by zero:

```
W_sparse     # non-zero W values, in row-major order
D_sparse     # delays, aligned to W_sparse
col_index    # source node j for each non-zero entry
row_pointer  # length N+1; entries for row n live in [row_pointer[n], row_pointer[n+1])
```

The sparse coupling loop iterates only over a row's non-zeros:

```
for i in row_pointer[n] .. row_pointer[n+1]-1:
    j = col_index[i]
    contribution from Xs[j][0][t - D_sparse[i]] times W_sparse[i]
```

If sparsity is $S\%$ (fraction of zeros), the theoretical speedup of the
coupling sum is roughly

$$
\text{speedup} \;\approx\; \frac{1}{1 - S/100}.
$$

Exercise 1.4 asks you to compare measured to theoretical — Amdahl's law applies
because only the coupling part is accelerated, not `step` / local dynamics /
Python overhead.

## The three TVB datasets

`lib/data.py` lazily downloads from the-virtual-brain/tvb-data on GitHub and
caches under `~/.cache/tvb_algo/`:

| Dataset | $N$ (centers) | Used for |
|---|---|---|
| `tvb76_weights_lengths()`  | 76  | Quick local runs |
| `tvb192_weights_lengths()` | 192 | Default / scaling experiments |
| `tvb998_weights_lengths()` | 998 | Heavy run — needs AWS for sane runtimes |

## Complexity (useful for Exercise 1.1)

Per timestep:
- Coupling: $\mathcal{O}(N^2)$ dense, $\mathcal{O}(\mathrm{NNZ})$ sparse
  ($\mathrm{NNZ}$ = non-zeros in $W$).
- Local dynamics: $\mathcal{O}(N \cdot \mathrm{cost}(F))$. For the MLP,
  $\mathrm{cost}(F) = 2 \cdot \mathrm{MLP\_M} \cdot \mathrm{MLP\_L} \approx 256$ MACs.
- Step (Forward Euler): $\mathcal{O}(N \cdot M)$.

Across the simulation: multiply the above by $T = \mathtt{tf}/\mathtt{dt}$
timesteps.

State memory: $N \cdot M \cdot T$ floats. With $N = 998$, $M = 2$, $T = 3000$
($\mathtt{tf} = 150$ ms, $\mathtt{dt} = 0.05$ ms) that's $\approx 6 \times 10^6$
floats $\approx 48$ MB — fine.

## Why parallelism across timesteps is hard

Forward Euler at step $t$ needs $\mathtt{Xs}$ values from steps $t - d_{ij}$ for
every source $j$. The minimum delay across all edges sets a hard barrier — you
can't run step $t+1$ until step $t$ (or at least $t - d_{\min}$) has finished.
Within a single timestep, however, **all $N$ nodes can be updated in parallel**
because they all read from $\mathtt{Xs}[\cdot, :, t-1]$ (and earlier) and write
to $\mathtt{Xs}[\cdot, :, t]$. That's the parallelism Labs 2/3 will exploit.
