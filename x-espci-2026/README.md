# X–ESPCI 2026 entrance exam: Maths B and Physics A, with worked solutions

Two papers from the **École Polytechnique – ESPCI admission exam 2026** (Tuesday 14 April 2026).
Each comes with full worked solutions in English, and the physics paper also has an English
translation.

| Paper | Original (French) | English translation | Worked solutions (English) |
|---|---|---|---|
| **Mathematics B**: MP–MPI track, paper 3, 4 h, no calculator | [`maths-b/maths-b-mp-mpi_paper_fr.pdf`](maths-b/maths-b-mp-mpi_paper_fr.pdf) | — | [`maths-b/maths-b_solutions_en.pdf`](maths-b/maths-b_solutions_en.pdf) |
| **Physics A**: PC track, paper 3, 4 h, no calculator | [`physics-a/physique-a-pc_paper_fr.pdf`](physics-a/physique-a-pc_paper_fr.pdf) | [`physics-a/physics-a-pc_paper_en.pdf`](physics-a/physics-a-pc_paper_en.pdf) | [`physics-a/physics-a_solutions_en.pdf`](physics-a/physics-a_solutions_en.pdf) |

## What the papers cover

**Mathematics B.** The paper studies how the eigenvalues of large matrices spread out. It has
four parts:
- a second-order recurrence (Chebyshev polynomials);
- the tridiagonal matrices *Tₙ* and *Tₙ(a,b,c)*: their spectra, and the arcsine law as the
  limiting distribution of their eigenvalues;
- a self-contained proof of Weierstrass's approximation theorem;
- Wigner's semicircle law for random symmetric matrices, proved by the moment method (Catalan
  numbers).

**Physics A.** *Modern techniques for the mass spectrometry of complex molecules*, in two
parts:
- electrospray ionisation: electrostatic pressure, the Rayleigh limit and the Taylor cone;
- FT-ICR mass spectrometry: cyclotron motion, damped forced resonance, the resonant spiral,
  trapping (magnetron motion), image-current detection with the reciprocity theorem, and
  Nyquist sampling.

## Key answers at a glance

| Maths B | Physics A |
|---|---|
| Q3c: *I(fₙ)* = C(n, n/2) for even *n*, 0 for odd *n* | Q5: *Q*_lim = 4π√(2ε₀γR³) |
| Q6: eigenvalues of *Tₙ*: 2 cos(kπ/(n+1)) | Q7–8: *E* ∝ r^(−1/2), δ = 1/2 |
| Q8c: *a* + 2√(bc) cos(kπ/(n+1)) | Q13: *z* = 17 and 34, *m* ≈ 3.40 × 10⁴ u, about 5 × 10³ atoms |
| Q9b: *qₙ(y)* ~ (n/π) arccos((a−y)/(2√(bc))) | Q16: ω₀ = qB/m |
| Q10: sup error ≤ (2κ)ⁿ, which is why κ < 1/2 | Q19: *Z₀* = F / [mω(ω₀ − ω − i/τ)] |
| Q12: Weierstrass (after rescaling *Pₙ(X/2)*) | Q25–26: *A* = E/2B, Archimedean spiral |
| Q13b: Σ(f₂ₚ) = Catalan number Cₚ | Q32–35: β = 2, ω_p = √(2qα/m), ω₊ ≈ ω₀ − ω_p²/2ω₀, ω₋ ≈ α/B |
| Q17b: semicircle law (convergence in probability) | Q40: Δq = −2q y₀/d; Q42: f_s ≈ 2.5 × 10⁵ Hz |

## How the answers were checked

The scripts in `checks/` re-derive every closed form (with sympy) and every number
(`python3 checks/check_maths_b.py`, `python3 checks/check_physics_a.py`). Among other things:
- the first zero of the Taylor-cone solution is at 130.71°, which is exactly the 49.3° cone
  half-angle quoted in the paper;
- all 21 labelled peaks of figure 2 give integer charges;
- after correcting for the attached protons, the protein mass comes out as 33 970 ± 2 u.

## Rebuilding

Run `./build.sh`. It uses pdflatex (TeX Live with `babel`, `siunitx`, `tcolorbox`, `pgfplots`).
The two figures in `physics-a/fig/` are rendered from the original paper.

---
*Unofficial solutions and translation. The original French papers prevail; the papers belong to
École Polytechnique / ESPCI.*
