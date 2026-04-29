# `report/` — generic LaTeX template for CESE5040 lab reports

**This folder is reference-only.** Don't put per-lab work here. The actual
report for each lab lives next to that lab's materials, e.g.:

| Lab | Where the report goes |
|---|---|
| Lab 1 | `../Lab_1/report/lab1/` |
| Lab 2 | `../Lab_2/report/lab2/` (when Lab 2 lands) |
| Lab 3 | `../Lab_3/report/lab3/` (when Lab 3 lands) |

## What's in here

```
report/
└── template/        # the seed -- copy this to Lab_N/report/labN/ for each lab
    ├── Lab.tex      # generic skeleton; rename to LabN.tex on copy
    ├── preamble.tex # shared style (packages, listings, header, math macros)
    ├── Makefile     # auto-detects Lab*.tex; targets: all / submit / watch / clean
    ├── .gitignore   # ignores LaTeX build artifacts
    ├── figures/     # placeholder
    ├── code/        # placeholder
    └── README.md    # how to use the template
```

## Bootstrap a new lab from this template

From the project root:

```bash
./new-lab.sh 2          # creates Lab_2/report/lab2/ from report/template/
```

Then `cd Lab_2/report/lab2/`, edit `Lab2.tex` (lab number, title, question
stubs), and start writing.

## Why this layout

- **`report/template/` stays canonical and clean.** Every lab starts from the
  same seed; if we improve the preamble (e.g. add a new package, fix a style
  bug), we update once here and re-copy when starting the next lab.
- **Per-lab work sits next to its source materials.** `Lab_1/report/lab1/`
  is in the same folder as `Lab_1/Lab_1 Assignment.pdf` and
  `Lab_1/Lab_1 Scripts/`, so everything for one lab travels together.
- **Each `Lab_N/report/labN/` is self-contained.** It has its own copy of
  `preamble.tex`, so you can upload that single folder to Overleaf as one
  project.
