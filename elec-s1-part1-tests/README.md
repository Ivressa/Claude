# Elec-S1 · Part 1 — Practice tests

Practice material for **IBE³ Physics for Engineers, Electricity module, Part 1: Foundations
of DC circuit theory**. There are nine progress tests, one per lecture section (1.A to
3.C), and one end-of-unit test. Each comes with an answer key and a marking scheme.

The format copies Test 1 (21 September 2026): a unit conversion, a definition with its equation
and SI units, tick-box questions, and a short calculation with the data in a frame. Answers go
in squared frames, and a "Marking" column sits in the margin. No calculator is needed.

## What to print

| File | Contents | Pages |
|---|---|---|
| [`pdf/Elec-S1-Part1_Progress-Tests_1A-3C.pdf`](pdf/Elec-S1-Part1_Progress-Tests_1A-3C.pdf) | The 9 progress tests, a how-to-use page and a progress tracker | 20 |
| [`pdf/Elec-S1-Part1_Progress-Tests_Answer-Keys.pdf`](pdf/Elec-S1-Part1_Progress-Tests_Answer-Keys.pdf) | Model answers, marking schemes, examiner's tips, lessons from Test 1 | 26 |
| [`pdf/Elec-S1-Part1_End-of-Unit-Test.pdf`](pdf/Elec-S1-Part1_End-of-Unit-Test.pdf) | End-of-unit test: 45 min, 50 marks, sections 1.A–3.C | 6 |
| [`pdf/Elec-S1-Part1_End-of-Unit-Test_Answer-Key.pdf`](pdf/Elec-S1-Part1_End-of-Unit-Test_Answer-Key.pdf) | Its key, plus a table saying which progress test to redo | 9 |

Single tests are in [`pdf/papers/`](pdf/papers) and [`pdf/keys/`](pdf/keys). Each progress
test is two pages, one sheet printed double-sided.

## The tests

| Test | Lecture section | Notes, pages | Time | Calculation exercise |
|---|---|---|---|---|
| 1.A | From potential to electric voltage | 2–7 | 7 min | Voltages from potentials, sum round a loop |
| 1.B | From charge to electric current | 7–11 | 7 min | Number of electrons from *i* and Δ*t* |
| 1.C | Circuits and two-terminal components | 11–14 | 7 min | Energy received by a phone (J and W·h) |
| 2.A | Characteristic curve, evidence for Ohm's law | 14–19 | 10 min | Naive mean vs least-squares estimate of *R* |
| 2.B | The ohmic conductor and Ohm's law | 19–21 | 7 min | Joule effect in a rear-window demister |
| 2.C | Pouillet's law | 21–22 | 7 min | Resistance and losses of a copper wire |
| 3.A | Kirchhoff's laws (combinations, divider, Millman) | 22–29 | 10 min | Millman's theorem |
| 3.B | Thévenin's and Norton's theorems | 29–33 | 10 min | Thévenin model of a three-resistor network |
| 3.C | Operating point of a circuit | 34–38 | 10 min | Operating point, power, efficiency |
| End of unit | All of Part 1 | 2–38 | 45 min | 10 exercises, including drift velocity + Pouillet, Millman with a reversed source, Thévenin + operating point + matching |

## How to use them

1. After studying a section, take its progress test in exam conditions: timer on, no notes,
   no calculator.
2. Mark it with the key. Each circled number in the margin is one marking item, and the scheme
   under each exercise says what earns it.
3. Mark out of 20 = score × 20/14. Log it in the tracker. Below 14/20, re-read the section
   and retake the test a few days later.
4. Finish with the end-of-unit test. Its diagnosis table says which progress tests to redo.

## Lessons from Test 1 built into the tests

- **Unit symbols are exact.** k (kilo) ≠ K (kelvin), m ≠ M. The unit of current is the
  **ampere (A)**, an SI base unit, not "C s⁻¹". Charge is in coulombs (C).
- **Nodes are electrically distinct nodes.** Points joined only by wires form one node. Each
  plain wire segment between two dots counts as a two-terminal component. Branches join
  distinct nodes. (Test 1: 2 nodes, 10 components, 4 branches.)
- **Letters before numbers.** Isolate the unknown literally (v = i/(neS)), then substitute
  with units.
- **Powers of ten on their own.** 1/(3.2 × 10⁴) = 0.31 × 10⁻⁴ = 3.1 × 10⁻⁵ m/s.

The answer keys point these out in red "Examiner's tip" boxes wherever they come up.

## Rebuilding the PDFs

You need TeX Live (`pdflatex`, with `circuitikz`, `tcolorbox`, `siunitx`) and `poppler-utils`
(for `pdfunite`).

```bash
./build.sh               # every test, both versions, and the four booklets
./build.sh progress-2A   # a single test (paper + key)
python3 tools/check_answers.py   # recomputes every numerical answer (exact nodal analysis)
```

Each test is a single file in `src/`. The answer key is that same file compiled with
`\def\KEY{}`, which fills the frames with the model answers (see `src/ibetest.cls`). To write
a new test, copy a progress test and change the exercises.

---
*Unofficial practice material written from the Elec-S1 Part 1 lecture notes. It is not an
official examination paper.*
