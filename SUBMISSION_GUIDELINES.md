# Submission guidelines (distilled from the three guideline PDFs)

## File names

- **Report**: `Lab1_Firstname_Lastname_Studentnumber.pdf`
  (e.g. `Lab1_Pieter_deBoer_123456.pdf`)
- **Code files**: `L1_Qx.py` where x is the exercise number.
  (e.g. `L1_Q6.py` for Exercise 1.6.)
- Submit `.py` files separately, **unzipped**.
- For Lab 1, code is required for exercises **1.6, 1.7, 1.8, 1.9**.

## What gets you points

### In the report

- **Captions on every figure and table.** Missing captions are flagged.
- **Answer the exact question asked, with numbers.** "2.7× faster" beats
  "much faster". When the question says "report the time", give the time.
  When it asks "why?", give a reason.
- **Unemotional, factual prose.** No essay-mode, no narrative. Bullet points
  and tables are fine.
- **Proofread.** Typos, grammar, syntax errors are explicitly called out as
  signs of disrespect for the reader.
- **Disclose LLM use.** Fair use is not penalized. Full-LLM submissions are
  prohibited (refer to lecture slides for the policy). Mention which parts
  the LLM helped with: code, language polish, etc.
- **Don't quit early.** If your computer can't run something, find another
  one or ask the tutor — don't write "I couldn't and so I did half".

### In the code

- **Out-of-the-box runnable.** The graders run it; if it crashes on their
  machine, you lose half the lab mark (-5).
- **Comments that explain *why*, not *what*.** The 9 rules from the guideline:
  1. Don't duplicate the code.
  2. Comments don't excuse unclear code.
  3. If you can't write a clear comment, the code is probably wrong.
  4. Comments should clarify, not confuse.
  5. Explain unidiomatic code.
  6. Link the original source for copied code.
  7. Link external references where helpful.
  8. Add a comment when fixing a bug — say what was wrong.
  9. Mark incomplete bits with TODO/FIXME.
- **Multiple files? Add a short README** explaining the layout. (For Lab 1
  this shouldn't be needed — one file per exercise.)
- **Naming penalty: -1 point** for poorly annotated code.
- **Non-running code penalty: -5 points (half the lab mark).**

## Common quantitative checklist for HPC reports

When you report a benchmark, make sure each number includes:

1. **What was measured** (entire simulation, only `calculate_coupling`, etc.).
2. **What it was measured against** (which baseline, what dataset, how many
   timesteps).
3. **Hardware**: at minimum CPU model from `lscpu` on the AWS instance and
   note that you ran on AWS. Mention if you switched between local and AWS.
4. **Repeats**: at least 3 runs, report the **minimum** for noise-reduction
   (or report mean ± stdev — be explicit).
5. **JIT warm-up**: state whether you discarded the first run.

## Speedup formula reminders

- Speedup: $S = T_{\text{baseline}} / T_{\text{optimized}}$.
- Amdahl's law: if you accelerate the fraction $p$ of total runtime by factor
  $k$, end-to-end speedup is

  $$S_{\text{end-to-end}} \;=\; \frac{1}{(1 - p) + p/k}.$$

  Useful in 1.4 and 1.5.
- Theoretical sparse coupling speedup: $\dfrac{1}{1 - S/100}$ where $S$ is
  sparsity in percent. Apply Amdahl with $p = (\text{coupling time}) / (\text{total time})$.

## Pitfalls specific to this course

- **Don't measure init/plot time in your "simulation time" number** — Ex. 1.2
  explicitly warns about this. Wrap only the simulation kernel in tic-toc.
- **First call to a `@jit`-decorated function compiles**, which can dwarf the
  actual computation on small inputs. Either warm up or skip the first run.
- **Process-time vs wall-clock**: `time.process_time()` ignores child
  processes. For multiprocessing in later labs, use `time.time()`.
- **Don't trust a single run.** Cache misses, scheduling, etc. add noise.
