# Lab 1 report

The actual write-up for CESE5040 Lab 1. This folder was bootstrapped from
the generic template at `../../../report/template/`. Each lab gets its own
copy so it can be uploaded to Overleaf as one self-contained project.

## Files

| File | Purpose |
|---|---|
| `Lab1.tex` | The Lab 1 report. Stubs for Questions 1-9 (Exercises 1.1-1.9), pre-built timing tables, commented-out `\lstinputlisting` lines for Q6-Q9. |
| `preamble.tex` | Local copy of the shared style. If you make a generally useful change here, also update `report/template/preamble.tex` so future labs get it. |
| `Makefile` | `make` builds the PDF, `make submit` renames it to the course convention. |
| `.gitignore` | Ignores LaTeX build artifacts. |
| `figures/` | Generated plots go here (PDF or PNG). Reference with `\includegraphics{figures/...}`. |
| `code/` | Final submitted scripts go here: `L1_Q6.py`, `L1_Q7.py`, `L1_Q8.py`, `L1_Q9.py`. Used by `\lstinputlisting`. |

## Build

```bash
cd Lab_1/report/lab1/
make            # produces Lab1.pdf
make submit     # also produces Lab1_Daniel_Tyukov_5714699.pdf  <-- this is what gets uploaded
make watch      # live rebuild via latexmk
make clean      # remove .aux/.log/etc.
```

## Or on Overleaf

1. New Project -> Blank.
2. Upload everything in this folder (including `figures/` and `code/`).
3. Menu -> Main document -> `Lab1.tex`.
4. Compile with **pdfLaTeX**.
5. Download PDF, rename to `Lab1_Daniel_Tyukov_5714699.pdf` before submitting.

## Identity (already pre-filled)

- Name: **Daniel Tyukov**
- Student number: **5714699**

Both appear on the title page and in the page header. They are set by two
`\renewcommand` lines at the top of `Lab1.tex`.

## Submission checklist (per `../../../SUBMISSION_GUIDELINES.md`)

- [ ] Filled in every `\answerhere{}` placeholder.
- [ ] Every figure and table has a caption.
- [ ] Numbers reported with units (use `\SI{X}{\second}`).
- [ ] LLM Usage Disclosure section filled in honestly.
- [ ] PDF renamed to `Lab1_Daniel_Tyukov_5714699.pdf`.
- [ ] `code/L1_Q6.py`, `L1_Q7.py`, `L1_Q8.py`, `L1_Q9.py` ready to upload separately, unzipped.
