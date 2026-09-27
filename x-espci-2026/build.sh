#!/usr/bin/env bash
# Builds the English translation and the worked solutions (pdflatex, two passes).
set -euo pipefail
cd "$(dirname "$0")"
export TEXINPUTS=".:$PWD:"
mkdir -p build
for doc in maths-b/maths-b_solutions_en physics-a/physics-a-pc_paper_en physics-a/physics-a_solutions_en; do
  [ -f "$doc.tex" ] || continue
  dir=$(dirname "$doc"); name=$(basename "$doc")
  for pass in 1 2; do
    (cd "$dir" && pdflatex -interaction=nonstopmode -halt-on-error -output-directory="../build" "$name.tex" > "../build/$name.stdout" 2>&1) \
      || { echo "!! $name failed"; tail -25 "build/$name.log"; exit 1; }
  done
  cp "build/$name.pdf" "$dir/$name.pdf"
  echo "built $dir/$name.pdf ($(grep -c Overfull build/$name.log || true) overfull boxes)"
done
