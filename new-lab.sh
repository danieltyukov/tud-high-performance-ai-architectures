#!/usr/bin/env bash
# Bootstrap a new lab report folder from the generic template.
# Usage: ./new-lab.sh <lab-number>
# Example: ./new-lab.sh 2  -> creates Lab_2/report/lab2/ from report/template/

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <lab-number>" >&2
    exit 1
fi

n="$1"
if ! [[ "$n" =~ ^[0-9]+$ ]]; then
    echo "error: lab number must be an integer (got: $n)" >&2
    exit 1
fi

root="$(cd "$(dirname "$0")" && pwd)"
src="$root/report/template"
dst="$root/Lab_$n/report/lab$n"

if [[ ! -d "$src" ]]; then
    echo "error: template not found at $src" >&2
    exit 1
fi
if [[ -e "$dst" ]]; then
    echo "error: $dst already exists" >&2
    exit 1
fi

mkdir -p "$(dirname "$dst")"
cp -r "$src" "$dst"
mv "$dst/Lab.tex" "$dst/Lab$n.tex"

# Pre-fill the lab number in the new file (best-effort; user still edits title).
sed -i "s/\\\\renewcommand{\\\\labnumber}{Lab~N}/\\\\renewcommand{\\\\labnumber}{Lab~$n}/" "$dst/Lab$n.tex"
sed -i "s/Lab Assignment N: <subtitle>/Lab Assignment $n: <subtitle>/" "$dst/Lab$n.tex"

echo "Created $dst"
echo
echo "Next steps:"
echo "  1. cd $dst"
echo "  2. Edit Lab$n.tex -- update \\labtitle subtitle and add Question stubs."
echo "  3. make    (build the PDF)"
