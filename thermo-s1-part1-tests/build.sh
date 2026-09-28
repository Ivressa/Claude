#!/usr/bin/env bash
# Builds every practice test twice (blank paper + answer key) and the booklets.
# Usage: ./build.sh            (all tests)
#        ./build.sh progress-1A (one test)
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$PWD
BUILD=$ROOT/build
OUT=$ROOT/pdf
mkdir -p "$BUILD" "$OUT/papers" "$OUT/keys"

TESTS=(progress-1A progress-1B progress-1C progress-2A progress-2B progress-2C
       progress-3A progress-3B progress-3C end-of-unit)
[ $# -gt 0 ] && TESTS=("$@")

compile() { # $1 = jobname, $2 = tex input
  (cd src && for pass in 1 2; do
     pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD" \
              -jobname="$1" "$2" > "$BUILD/$1.stdout" 2>&1 \
       || { echo "!! $1 failed, see $BUILD/$1.log"; tail -30 "$BUILD/$1.log"; exit 1; }
   done)
}

for t in "${TESTS[@]}"; do
  [ -f "src/$t.tex" ] || { echo "skip $t (no source)"; continue; }
  echo "== $t"
  compile "$t" "\\input{$t}"
  compile "$t-key" "\\def\\KEY{}\\input{$t}"
  cp "$BUILD/$t.pdf" "$OUT/papers/$t.pdf"
  cp "$BUILD/$t-key.pdf" "$OUT/keys/$t-key.pdf"
done

# Booklets (only when every test exists)
if [ $# -eq 0 ]; then
  for extra in booklet-papers-cover booklet-keys-cover; do
    [ -f "src/$extra.tex" ] && compile "$extra" "\\input{$extra}"
  done
  P=(); K=()
  for t in progress-1A progress-1B progress-1C progress-2A progress-2B progress-2C \
           progress-3A progress-3B progress-3C; do
    P+=("$OUT/papers/$t.pdf"); K+=("$OUT/keys/$t-key.pdf")
  done
  pdfunite "$BUILD/booklet-papers-cover.pdf" "${P[@]}" "$OUT/Thermo-S1-Part1_Progress-Tests_1A-3C.pdf"
  pdfunite "$BUILD/booklet-keys-cover.pdf" "${K[@]}" "$OUT/Thermo-S1-Part1_Progress-Tests_Answer-Keys.pdf"
  cp "$OUT/papers/end-of-unit.pdf" "$OUT/Thermo-S1-Part1_End-of-Unit-Test.pdf"
  cp "$OUT/keys/end-of-unit-key.pdf" "$OUT/Thermo-S1-Part1_End-of-Unit-Test_Answer-Key.pdf"
  echo "Booklets written to $OUT"
fi
