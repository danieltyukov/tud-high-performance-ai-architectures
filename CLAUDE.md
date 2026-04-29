# Project-local instructions

This file overrides specific rules from the parent `CLAUDE.md` at
`/home/danieltyukov/workspace/tud/CLAUDE.md` for files inside this project
(`tud-high-performance-ai-architectures/`).

## Math notation in `.md` files (overrides parent rule)

Inside this directory, **`.md` files use LaTeX math notation**, not Unicode.
This is the inverse of the parent rule.

- Inline math: `$x^2 + y^2 = z^2$`
- Display math:
  ```
  $$
  \frac{\partial f}{\partial x} = \dots
  $$
  ```
- Use standard LaTeX commands: `\alpha`, `\beta`, `\frac`, `\sqrt`, `\sum`,
  `\prod`, `\int`, `\mathcal{O}`, etc.
- Subscripts and superscripts: `X_{ij}^2`, `\sum_{j=1}^{N}`, etc.

**Why:** This is an HPC course; the `.tex` lab reports use LaTeX, and keeping
the same notation in the project's accompanying `.md` reference docs avoids
mental translation when copying formulas back and forth.

**Scope of the override:**

- `.md` files inside this project → **LaTeX math** (this rule).
- `.tex` files → LaTeX, naturally (always was).
- Chat output / assistant text replies → still **Unicode** per the parent
  rule, unless the user asks otherwise. The user's "in .md files" was
  specific.
- `.md` files outside this project → still **Unicode** per the parent rule.

## Stylistic Unicode that is NOT math

Keep these as Unicode in `.md` prose; they are typographic, not equations:

- `→` for flow / pipelines (e.g. `Lab 1 → Lab 2 → Lab 3`).
- `—` em-dash, `–` en-dash.
- `×` only when used as a count separator in plain text like "2× faster" is
  fine; inside an equation, prefer `\times`.

If in doubt, ask: "is this a *math expression* or a *typographic device*?"
Math → LaTeX. Typography → Unicode.
