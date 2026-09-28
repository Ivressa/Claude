# Thermo-S1 · Part 1: practice tests

Practice material for **IBE³ Physics for Engineers, Thermodynamics module, Part 1:
Description of a system in thermodynamics**. It contains nine progress tests (one per lecture
section, 1.A to 3.C) and one end-of-unit test, each with a full answer key and marking scheme.

The tests use the same format as the Electricity set in
[`../elec-s1-part1-tests`](../elec-s1-part1-tests), which copies Test 1 (21 September 2026).
Each has a unit conversion, a definition with its equation and SI units, tick-box questions,
and a short calculation with the data in a frame. No calculator is needed: the data use
R = 8.3 J·K⁻¹·mol⁻¹ and RT ≈ 2.5 × 10³ J·mol⁻¹ at 300 K.

## What to print

| File | Contents | Pages |
|---|---|---|
| [`pdf/Thermo-S1-Part1_Progress-Tests_1A-3C.pdf`](pdf/Thermo-S1-Part1_Progress-Tests_1A-3C.pdf) | The 9 progress tests, a how-to-use page and a progress tracker | 20 |
| [`pdf/Thermo-S1-Part1_Progress-Tests_Answer-Keys.pdf`](pdf/Thermo-S1-Part1_Progress-Tests_Answer-Keys.pdf) | Model answers, marking schemes, examiner's tips, Test 1 lessons applied to thermodynamics | 27 |
| [`pdf/Thermo-S1-Part1_End-of-Unit-Test.pdf`](pdf/Thermo-S1-Part1_End-of-Unit-Test.pdf) | End-of-unit test: 45 min, 50 marks, sections 1.A–3.C | 5 |
| [`pdf/Thermo-S1-Part1_End-of-Unit-Test_Answer-Key.pdf`](pdf/Thermo-S1-Part1_End-of-Unit-Test_Answer-Key.pdf) | Its key, plus a table saying which progress test to redo | 7 |

Single tests are in [`pdf/papers/`](pdf/papers) and [`pdf/keys/`](pdf/keys). Each progress
test is two pages, one sheet printed double-sided.

## The tests

| Test | Lecture section | Notes, pages | Time | Calculation exercise |
|---|---|---|---|---|
| 1.A | System and state variables | 2–5 | 7 min | Composition of a solution (n, c_m, c) |
| 1.B | Postulates of thermodynamics | 5–7 | 7 min | Equilibrium of a loaded piston |
| 1.C | Equations of state and state functions | 7–10 | 7 min | Partial derivatives; the two effects on dV cancel |
| 2.A | Condensed phases (χ_T, α) | 11–13 | 10 min | Expansion and compression of water |
| 2.B | Gases (β) | 13–14 | 7 min | Tyre pressure after driving |
| 2.C | Principle and method (β = α/pχ_T) | 14–15 | 10 min | Coefficients of a co-volume gas p(V − nb) = nRT |
| 3.A | Low-density gases: historical laws | 15–17 | 7 min | Rising bubble (Boyle) and heated balloon (Charles) |
| 3.B | The ideal gas and Clapeyron's law | 17–20 | 10 min | Four-step piston–cylinder problem |
| 3.C | Real gases (Amagat, Van der Waals) | 20–23 | 10 min | CO₂ at 40 bar: Z ≈ 0.8 |
| End of unit | All of Part 1 | 2–23 | 45 min | 10 exercises, including water in a sealed container (+20 bar for 5 K), a weighted piston, the density of air, and N₂ at 280 bar (Z ≈ 1.1) |

## Lessons from Test 1, applied here

- **Temperatures in kelvins** (capital K, no degree sign; "big K stands for kelvins").
  A temperature *difference* is the same in K and in °C.
- **SI before pV = nRT:** 1 L = 10⁻³ m³, 1 cm² = 10⁻⁴ m², 1 bar = 10⁵ Pa, M in kg·mol⁻¹.
- **Letters before numbers**, units on every value, and powers of ten handled separately.
- **Read diagrams exactly:** the variable held fixed (isotherm, isobar, isochore) tells you
  which partial derivative a slope is.

Several boxes in the student handout are blank (Boxes 4–6 and 8–18). The keys give the
standard definitions; the wording used in class is equally valid.

## Checking and rebuilding

- `python3 tools/check_answers.py` re-derives every number and derivative (78 checks). It
  also shows that the rounded data stay within 1 % of results computed with the exact
  constants.
- `./build.sh` rebuilds every test (paper and key) and the booklets. `./build.sh progress-2A`
  rebuilds a single test. It needs TeX Live and `poppler-utils`.

---
*Unofficial practice material written from the Thermo-S1 Part 1 lecture notes. It is not an
official examination paper.*
