# AWS instance specs (for the report)

Captured on the running VM, 2026-04-25.
Use these in the "Hardware" section of the Lab 1 report so timings are
reproducible.

## Hardware

| Property | Value |
|---|---|
| Instance class (inferred) | ~AWS `t3.medium` |
| CPU | Intel Xeon Platinum 8259CL @ 2.50 GHz (Cascade Lake) |
| Sockets / Cores / Threads | 1 / 1 / 2 (SMT enabled) |
| vCPUs visible | 2 |
| Memory | 3.7 GiB |
| OS | Ubuntu 24.04 (kernel 6.17.0-1010-aws, x86_64) |
| Hostname (internal) | `ip-172-31-56-241` (private; do not put in report) |
| Public IP at setup | `52.50.18.71` (may change on `$start`) |

## Software

| Package | Version |
|---|---|
| Python | 3.12.3 |
| NumPy | 2.4.4 |
| Numba | 0.65.0 |
| SciPy | 1.17.1 |
| Matplotlib | 3.10.8 |

## Implications for HPC reasoning

- **Single-threaded NumPy + Numba (Lab 1)**: This is the right machine.
  Vectorization speedups against pure Python should be the textbook
  10–100× range; nothing CPU-architectural will stand in the way.
- **Multi-process (Lab 2 expected)**: Only **1 physical core**. SMT gives 2
  threads but they share execution units, so realistic max parallel
  speedup is ~1.5×, not 2×. Don't be surprised when going from 1 to 2
  workers gives well below ideal scaling — it's the hardware ceiling, not
  your code.
- **GPU (Lab 3 expected)**: Confirm GPU presence with `nvidia-smi` only on
  Lab 3's instance — this t3.medium-class image does not have one.
- **Memory**: TVB998 with `M=2`, `T=3000` (tf=150 ms, dt=0.05 ms) needs
  $N \cdot M \cdot T \approx 6 \times 10^6$ float64 $\approx 48$ MB.
  Comfortably fits.

## Reproducing these numbers

```bash
ssh cese5040 'lscpu | grep -E "Model name|^CPU\(s\)|Thread|Core|Socket"'
ssh cese5040 'free -h'
ssh cese5040 'python3 --version && pip3 list | grep -iE "numpy|numba|scipy|matplotlib"'
```
