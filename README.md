# CESE5040 — High-Performance Computing and AI Architectures

TU Delft / Erasmus MC, 2026.
Instructors: Christos Strydis, Rajendra Bishnoi, Amirreza Movahedin.

This directory holds course materials, lecture demo scripts, and lab assignments
for the course. Reference files in this repo (read these before starting any new
weekly task):

| File | Purpose |
|---|---|
| `README.md` | This file. High-level orientation. |
| `LAB_1.md` | Full Lab 1 reference: all 9 exercises, what each script does, what to submit. |
| `LECTURE_SCRIPTS.md` | Walk-through of every `.py` in `Lecture_1&2 scripts/` (profiling, vectorization, JIT demos). |
| `TVB_ALGORITHM.md` | The math + data layout behind TVB. The core that all labs build on. |
| `AWS_WORKFLOW.md` | Discord bot + SSH connection to the course AWS instance. |
| `SUBMISSION_GUIDELINES.md` | Report formatting, code-naming, LLM-disclosure rules, common pitfalls. |
| `AWS_INSTANCE_SPECS.md` | Hardware/software details of the course VM — paste into the report's Hardware section. |
| `report/` | **Reference-only** generic LaTeX template for lab reports. See `report/README.md`. |
| `new-lab.sh` | Bootstrap script: `./new-lab.sh 2` → creates `Lab_2/report/lab2/` from the template. |

## Directory layout

```
.
├── Lecture_1&2 scripts/        # Profiling + vectorization + JIT demos
│   ├── bessel_*.py             # 5 ways to time the same Bessel kernel
│   ├── primes_cprofile.py      # cProfile + pstats demo
│   ├── processtime_vs_time.py  # process_time vs time on multiprocessing
│   ├── gol.py                  # Game of Life: elementwise vs vectorized
│   ├── mb.py                   # Mandelbrot: sequential vs vectorized
│   ├── ip_jit.py / ip_vec.py   # Seam carving: JIT vs NumPy vectorized
│   └── lq.png                  # Test image for seam-carving demos
├── Lab_1/
│   ├── Lab_1 Assignment.pdf    # 9-exercise assignment (~57 pts)
│   ├── Lab_1 Scripts/          # provided sequential implementations
│   └── report/lab1/            # YOUR Lab 1 LaTeX report (bootstrapped from report/template/)
│       ├── tvb_seq.py          # Baseline sequential TVB
│       ├── tvb_seq_sparse.py   # CSR-sparse coupling
│       ├── tvb_seq_mlp.py      # Local dynamics replaced by an MLP (dense + sparse modes)
│       ├── tvb_seq_jit.py      # NumPy-array layout, JIT-ready
│       └── lib/
│           ├── data.py         # Downloads/caches TVB connectomes (76/192/998)
│           ├── mlp_params.py   # Hard-coded weights for the MLP local dynamics
│           └── plot.py         # plot_xs (timeseries) and plot_delay_hist
├── Lab Guideline - How to Report Results.pdf
├── Lab Guideline - How to Upload Python Code.pdf
├── Lab Instructions – How to connect to AWS via Discord.pdf
├── Lab_X_Answers_XXXXXX [template].docx   # Course-provided docx template (we mirror its structure in LaTeX)
├── report/                     # GENERIC LaTeX template -- reference-only, never edited per-lab
│   ├── README.md               # how the template works
│   └── template/               # the seed (preamble, Lab.tex, Makefile, ...)
├── new-lab.sh                  # ./new-lab.sh N -> creates Lab_N/report/labN/ from the template
└── scripts/aws-ip.sh           # update SSH config when AWS rotates the instance IP
```

## Course arc (what each lab is likely doing)

The first three labs progressively accelerate TVB:

1. **Lab 1 — Vectorization + JIT.** Profile, analyze sparsity, vectorize with
   NumPy, JIT-compile with Numba. CPU-only. (This lab.)
2. **Lab 2 — likely multi-core / multi-process parallelism.**
3. **Lab 3 — likely GPU (CUDA/CuPy) acceleration.**

So the optimizations you build in Lab 1 are the foundation for Labs 2 and 3 —
keep your Lab 1 code clean and reusable.

## Working environment

- Code runs on a **per-student AWS instance** managed via a Discord bot.
  Budget: **16 hours/week, resets Monday**. Always `$stop` when not actively
  working. See `AWS_WORKFLOW.md`.
- Local development is fine for writing/testing on small TVB datasets (76
  centers); use AWS for the big runs (TVB998) and final timing measurements.
- Python 3.12 preinstalled on the AWS image.

## Submission cheatsheet (Lab 1)

- Report PDF: `Lab1_Firstname_Lastname_Studentnumber.pdf`
- Code (separate, unzipped): `L1_Q6.py`, `L1_Q7.py`, `L1_Q8.py`, `L1_Q9.py`
- Disclose any LLM use. Full-LLM submission is prohibited.
- See `SUBMISSION_GUIDELINES.md` for the full list of pitfalls.
