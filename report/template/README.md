# CESE5040 lab-report template

A self-contained, Overleaf-uploadable LaTeX project for a CESE5040 lab report.
**Don't edit files in this directory directly** — instead, copy the whole
folder to `../labN/` and edit there. That keeps the seed clean.

## Files

| File | Purpose |
|---|---|
| `Lab.tex` | Generic skeleton. Rename to `LabN.tex` after copying. Has 3 generic Question stubs and commented-out building blocks for tables, figures, and code listings. |
| `preamble.tex` | All packages, listings styles (Python theme), page header, math macros (`\bigO`, `\code`, `\answerhere`). Lab-agnostic. |
| `Makefile` | `make` builds the PDF, `make submit` renames it to the course convention, `make watch` live-rebuilds via `latexmk`. Auto-detects the `LabN.tex` file. |
| `.gitignore` | Ignores LaTeX build artifacts. |
| `figures/` | Drop generated plots here (PDF or PNG). |
| `code/` | Drop final `LN_Qx.py` files here for `\lstinputlisting`. |

## Bootstrap a new lab

From the parent `report/` directory:

```bash
./new-lab.sh 2          # creates ../lab2/ from this template
```

Then edit `../lab2/Lab2.tex`:

1. The macros at the top:
   ```latex
   \newcommand{\labtitle}{Lab Assignment 2: <subtitle>}
   \renewcommand{\labnumber}{Lab~2}
   ```
2. Add or remove `\subsection{Question N}` blocks to match the new lab's
   exercise count.
3. Fill in answers in place of each `\answerhere{}`.

## Compile

```bash
make            # produces LabN.pdf
make submit     # also produces LabN_Daniel_Tyukov_5714699.pdf
make watch      # live rebuild (Ctrl-C to stop)
```

Or on Overleaf: upload the lab folder as a project, set main document to
`LabN.tex`, compile with **pdfLaTeX**.

## Identity

The template is pre-set for **Daniel Tyukov / 5714699**. To change:

- In `Lab.tex`: edit the two `\renewcommand` lines for `\studentname` and
  `\studentnumber`.
- In `Makefile`: override `NAME` and `NUMBER` (or pass via env, e.g.
  `make NAME=Foo_Bar NUMBER=999 submit`).
