#!/usr/bin/env bash
# Builds the study guide, the worksheets and the worksheet answers (pdflatex, two passes).
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$PWD; BUILD=$ROOT/build; OUT=$ROOT/pdf
mkdir -p "$BUILD" "$OUT"
compile() { # $1 = jobname, $2 = tex input
  (cd src && for pass in 1 2; do
     pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" \
              -jobname="$1" "$2" > "$BUILD/$1.stdout" 2>&1 \
       || { echo "!! $1 failed, see $BUILD/$1.log"; tail -30 "$BUILD/$1.log"; exit 1; }
   done)
  echo "built $1 ($(grep -c Overfull "$BUILD/$1.log" || true) overfull boxes)"
}
compile study-guide "\\input{study-guide}"
compile worksheets "\\input{worksheets}"
compile worksheet-answers "\\def\\KEY{}\\input{worksheets}"
cp "$BUILD/study-guide.pdf"       "$OUT/Chem-S1-1_Study-Guide.pdf"
cp "$BUILD/worksheets.pdf"        "$OUT/Chem-S1-1_Worksheets.pdf"
cp "$BUILD/worksheet-answers.pdf" "$OUT/Chem-S1-1_Worksheet-Answers.pdf"
echo "PDFs written to $OUT"
