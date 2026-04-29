#!/usr/bin/env bash
# Pull AWS results back, regenerate plots, fill report placeholders,
# and compile the final PDF. Idempotent.
set -euo pipefail

REPO=/home/danieltyukov/workspace/tud/tud-high-performance-ai-architectures
LAB="$REPO/Lab_2"
SCRIPTS="$LAB/Lab_2 Scripts"

echo "[finalize] pulling AWS results"
rsync -az cese5040:lab2/results/ "$LAB/results/"
rsync -az cese5040:lab2/figures/ "$LAB/figures/"

echo "[finalize] regenerating plots locally"
cd "$SCRIPTS"
MPLBACKEND=Agg python3 make_plots.py "$LAB/results" "$LAB/figures" || true
# Re-render py-spy SVG -> color PNG (AWS conversion produced 1-bit B/W).
if [ -f "$LAB/figures/pyspy_flame.svg" ]; then
    convert -density 150 -background white -alpha remove \
        "$LAB/figures/pyspy_flame.svg" "$LAB/figures/pyspy_top.png" || true
fi

echo "[finalize] filling report placeholders"
python3 fill_report.py "$REPO"

echo "[finalize] compiling PDF (xelatex, twice for cross-refs)"
cd "$LAB/report"
xelatex -interaction=nonstopmode Lab2_Daniel_Tyukov_5714699.tex >/dev/null 2>&1 || true
xelatex -interaction=nonstopmode Lab2_Daniel_Tyukov_5714699.tex 2>&1 | tail -5
ls -la Lab2_Daniel_Tyukov_5714699.pdf

echo "[finalize] packaging submission"
SUB="$LAB/submission"
mkdir -p "$SUB"
cp "$LAB/report/Lab2_Daniel_Tyukov_5714699.pdf" "$SUB/"
cp "$SCRIPTS/L2_Q6.py" "$SUB/"
cp "$SCRIPTS/L2_Q7.py" "$SUB/"
cp "$SCRIPTS/L2_Q8.py" "$SUB/"
ls -la "$SUB"
echo "[finalize] done"
