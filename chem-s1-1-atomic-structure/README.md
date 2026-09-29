# Chemistry S1-1: From atomic entities to physico-chemical systems

Study material for **Engineering & Data Sciences, Chemistry S1-1**. It covers the five chapters of the
student handout (the two PDFs in [`lecture/`](lecture)). Each chapter is one unit, and each unit has
three parts:

- **Concepts in detail**: every notion with a precise definition, the reasoning behind it, worked
  examples and common mistakes. Orange boxes complete the blank boxes and tables of the handout.
- **Recap**: one page with the definitions, formulas, key numbers and a "you should be able to" checklist.
- **Worksheet**: 15 questions that get progressively harder, with full worked answers in a
  separate booklet.

## What to print

| File | Contents | Pages |
|---|---|---|
| [`pdf/Chem-S1-1_Study-Guide.pdf`](pdf/Chem-S1-1_Study-Guide.pdf) | Concepts, recap and worksheet for each of the 5 units | 35 |
| [`pdf/Chem-S1-1_Worksheets.pdf`](pdf/Chem-S1-1_Worksheets.pdf) | The 5 worksheets on their own (75 questions) | 11 |
| [`pdf/Chem-S1-1_Worksheet-Answers.pdf`](pdf/Chem-S1-1_Worksheet-Answers.pdf) | Every question with its worked answer | 20 |

## The units

| Unit | Handout | Topics | Worksheet highlights |
|---|---|---|---|
| 1. Classical description of the atom | ch. 1 | Democritus to STM, Thomson, Rutherford, Millikan, particle masses, amu, Z/A, isotopes, ions | Millikan's oil drops, mass defect of carbon-12, Rutherford's closest approach |
| 2. Quantum model of the atom | ch. 2 | EM waves, photons, E = hν, absorption and emission, Balmer/Rydberg, Bohr levels | Series limits, which photons H absorbs, the He⁺ line that coincides with H's red line |
| 3. Quantum numbers and atomic orbitals | ch. 3 | n, ℓ, m_ℓ, m_s; orbitals, degeneracy, nodes, shapes, Zeeman effect, Madelung, spin | 2n² electron states per shell, sodium D doublet, maximum of the 1s radial density |
| 4. Electronic configuration and periodic table | ch. 4 (pp. 13–15) | Aufbau, Pauli, Hund, H to Ar, core/valence, blocks, Cr/Cu exceptions | Iron and its ions, period lengths 2-8-8-18-18-32, the element 168 |
| 5. Atomic properties and periodicity | ch. 5 (pp. 16–20) | Atomic mass, radii, ionisation energy, polarisability, electronegativity (Pauling, Allred–Rochow) | Successive ionisation energies, HCl partial charges, Pauling χ from bond energies |

Question levels: Q1–4 recall (Level 1), Q5–8 apply (Level 2), Q9–12 multi-step (Level 3),
Q13–15 challenge.

## Handout blanks and typos

The guide fills every blank box and table of the handout: the 8 forms of energy (Table 2-1), energy
diagrams, Tables 3-1 to 3-3, the Madelung order, Tables 4-1 and 4-2, and the trend bullets of
chapter 5. Where the answer depends on a convention (for example m_ℓ for p_x and p_y), both usual
conventions are given; follow the one used in class. Typos in the handout are pointed out:
Balmer's formula needs n = 3, 4, 5…, and the right-hand "650" on the spectra should read 700 nm.
Hydrogen's ionisation energy (blank in Table 5-2) is 1312 kJ/mol.

## Checking and rebuilding

- `python3 tools/check_answers.py` recomputes every number in the worked answers (132 checks). It
  uses the handout's constants and builds the electron configurations from Madelung's rule.
- `./build.sh` rebuilds the three PDFs. It needs TeX Live. The sources are in `src/`: `unitN.tex` holds
  the concepts and recap, and `wsN.tex` the worksheet with its answers.

---
*Unofficial study material written from the Chemistry S1-1 student handout.*
