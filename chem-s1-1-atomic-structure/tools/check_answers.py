"""Independent re-computation of the numbers and configurations in the Chemistry S1-1 study guide
and worksheet answers. Run: python3 tools/check_answers.py"""
import math

fails = 0
def check(label, got, expected, rel=5e-3):
    global fails
    ok = math.isclose(float(got), float(expected), rel_tol=rel, abs_tol=1e-30)
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {float(got):.5g}, guide says {float(expected):.5g}")
    fails += (not ok)
def same(label, got, expected):
    global fails
    ok = got == expected
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {got!r}, guide says {expected!r}")
    fails += (not ok)

# constants as given in the handout
h, c, e, NA, RH = 6.62e-34, 3.00e8, 1.6e-19, 6.022e23, 3.29e15
amu, me, mp, mn, a0, k = 1.6605e-27, 9.1094e-31, 1.6727e-27, 1.6749e-27, 52.9, 8.99e9
lam = lambda E: h * c / E  # m, from J

print("== Unit 1")
check("mp in amu", mp / amu, 1.0073, 1e-4); check("me in amu = 1/1823", amu / me, 1823, 1e-3)
check("gold atom in amu", 3.2707e-25 / amu, 196.97, 1e-4); check("H atom in amu", 1.6735e-27 / amu, 1.0078, 1e-4)
check("Q7 mp/me", mp / me, 1836); check("Q7 electron fraction of C-12", 6 * me / (12 * amu), 2.74e-4)
check("Q8 atom/nucleus", 100 / 1e-3, 1e5); check("Q8 volume fraction", (1e-3 / 100) ** 3, 1e-15)
check("Q9 e/me", e / me, 1.76e11); check("Q9 e/mp", e / mp, 9.57e7)
check("Q10 Au kg", 196.967 * amu, 3.2706e-25, 1e-4); N = 1e-3 / 3.2707e-25
check("Q10 atoms in 1 g", N, 3.06e21); check("Q10 mol", N / NA, 5.08e-3); check("Q10 M", 1 / (N / NA), 197)
check("Q10 amu*NA (kg/mol)", amu * NA, 1.000e-3)
V = 4 / 3 * math.pi * (2.7e-15) ** 3; rho = 12 * amu / V
check("Q12 V nucleus", V, 8.2e-44, 1e-2); check("Q12 rho", rho, 2.4e17, 1e-2); check("Q12 teaspoon", rho * 5e-6, 1.2e12, 1e-2)
q = [3.2e-19, 4.8e-19, 8.0e-19, 6.4e-19, 1.12e-18]
same("Q13 multiples of e", [round(x / 1.6e-19, 6) for x in q], [2, 3, 5, 4, 7])
same("Q13 2.4e-19 not integer", (2.4e-19 / 1.6e-19) % 1 != 0, True)
m12 = 6 * 1.0073 + 6 * 1.0087 + 6 / 1823; dm = m12 - 12; E = dm * amu * c ** 2
check("Q14 sum of parts", m12, 12.0993, 1e-5); check("Q14 dm (kg)", dm * amu, 1.65e-28)
check("Q14 E per atom", E, 1.48e-11); check("Q14 E in MeV", E / 1.6e-13, 93, 1e-2)
check("Q14 per mol (kJ/mol)", E * NA / 1e3, 8.9e9, 1e-2); check("Q14 ratio to 400 kJ/mol", E * NA / 4e5, 2.2e7, 0.1)
check("Q15 closest approach (m)", k * 2 * 79 * e ** 2 / (5.0 * 1.6e-13), 4.5e-14, 1e-2)

print("== Unit 2")
check("656 nm frequency", c / 656e-9, 4.57e14); check("656 nm photon J", h * c / 656e-9, 3.03e-19)
check("656 nm photon eV", h * c / 656e-9 / e, 1.89); check("hc/e in eV nm", h * c / e * 1e9, 1241, 1e-3)
check("Q2 nu", c / 650e-9, 4.62e14); check("Q2 T", 650e-9 / c, 2.17e-15)
check("Q3 E J", h * c / 650e-9, 3.06e-19); check("Q3 E eV", h * c / 650e-9 / e, 1.91)
for n2, lam_nm, nu in [(3, 657, 4.57e14), (4, 486, 6.17e14), (5, 434, 6.91e14), (6, 410, 7.31e14)]:
    f = RH * (1 / 4 - 1 / n2 ** 2); check(f"Q7 Balmer {n2}->2 nu", f, nu); check(f"Q7 Balmer {n2}->2 lambda nm", c / f * 1e9, lam_nm)
dE = 13.6 * (1 / 4 - 1 / 9)
check("Q8 3->2 eV", dE, 1.89); check("Q8 3->2 J", dE * e, 3.02e-19); check("Q8 lambda nm", lam(dE * e) * 1e9, 657)
check("Q8 RH = 13.6 eV/h", 13.6 * e / h, 3.29e15)
check("Q9 Lyman 2->1 nm", c / (RH * 0.75) * 1e9, 122); check("Q9 Lyman limit nm", c / RH * 1e9, 91.2)
check("Q9 Paschen limit nm", c / (RH / 9) * 1e9, 821); check("Balmer limit nm", c / (RH / 4) * 1e9, 365)
check("Q9 E2-E1", 13.6 * 0.75, 10.2); check("Q9 Balmer max gap", 13.6 / 4, 3.40)
check("Q10 IE J", 13.6 * e, 2.18e-18); check("Q10 IE kJ/mol", 13.6 * e * NA / 1e3, 1310)
check("Q11 4->1 nm", c / (RH * (1 - 1 / 16)) * 1e9, 97, 1e-2); check("Q11 3->1 nm", c / (RH * (1 - 1 / 9)) * 1e9, 103, 1e-2)
check("Q11 4->3 nm", c / (RH * (1 / 9 - 1 / 16)) * 1e9, 1876); same("Q11 number of lines", math.comb(4, 2), 6)
gaps = [13.6 * (1 - 1 / p ** 2) for p in range(2, 30)]
same("Q12 10.2 absorbed", any(abs(g - 10.2) < 0.01 for g in gaps), True)
same("Q12 11.0 not absorbed", any(abs(g - 11.0) < 0.05 for g in gaps), False)
same("Q12 12.09 absorbed", any(abs(g - 12.09) < 0.01 for g in gaps), True); check("Q12 excess", 15.0 - 13.6, 1.4)
nu = c / 1876e-9; x = nu / RH
check("Q13 nu", nu, 1.599e14, 1e-3); check("Q13 nu/RH", x, 0.0486); check("Q13 n2=4", 1 / math.sqrt(1 / 9 - x), 4, 1e-2)
check("Q13 n1=4 fails", 1 / math.sqrt(1 / 16 - x), 8.5, 1e-2)
check("Q14 He+ E3", -54.4 / 9, -6.04); check("Q14 He+ 3->2 eV", 54.4 * (1 / 4 - 1 / 9), 7.56)
check("Q14 He+ 3->2 nm", lam(54.4 * (1 / 4 - 1 / 9) * e) * 1e9, 164)
check("Q14 He+ 6->4 = H 3->2", 54.4 * (1 / 16 - 1 / 36), 13.6 * (1 / 4 - 1 / 9), 1e-9)
Eph = h * c / 532e-9
check("Q15 photon J", Eph, 3.73e-19); check("Q15 photons/s", 1e-3 / Eph, 2.7e15, 1e-2)
check("Q15 mol per hour", 1e-3 / Eph * 3600 / NA, 1.6e-5, 1e-2)

print("== Unit 3")
same("Q1 orbitals n=3", sum(2 * l + 1 for l in range(3)), 9)
allowed = lambda n, l, m: 0 <= l <= n - 1 and -l <= m <= l
same("Q2 allowed", [allowed(*t) for t in [(2, 2, 0), (3, 1, -1), (1, 0, 1), (4, 3, -2), (2, 1, 2), (5, 0, 0)]],
     [False, True, False, True, False, True])
same("Q5 degenerate n=4", sum(2 * l + 1 for l in range(4)), 16); check("Q6 1s->2p", 13.6 - 3.4, 10.2)
nodes = {k: (n - l - 1, l, n - 1) for k, n, l in [("2s", 2, 0), ("3p", 3, 1), ("3d", 3, 2), ("4s", 4, 0), ("4f", 4, 3)]}
same("Q7 nodes", nodes, {"2s": (1, 0, 1), "3p": (1, 1, 2), "3d": (0, 2, 2), "4s": (3, 0, 3), "4f": (0, 3, 3)})
for lab, n, Z, r in [("H 2s", 2, 1, 212), ("H 3s", 3, 1, 476), ("He+ 1s", 1, 2, 26.5), ("Li2+ 1s", 1, 3, 17.6)]:
    check(f"Q9 r {lab}", n * n * a0 / Z, r)
L = {"s": 0, "p": 1, "d": 2, "f": 3, "g": 4}
def madelung_key(sub): n, l = int(sub[:-1]), L[sub[-1]]; return (n + l, n)
same("Q10 order", sorted("5s 4f 3d 4p 6s 4d 5p 4s".split(), key=madelung_key), "4s 3d 4p 5s 4d 5p 6s 4f".split())
same("Q13 2n^2", [2 * sum(2 * l + 1 for l in range(n)) for n in (1, 2, 3)], [2, 8, 18])
E1, E2 = h * c / 589.0e-9, h * c / 589.6e-9
check("Q14 E1 J", E1, 3.372e-19, 1e-4); check("Q14 E1 eV", E1 / e, 2.107, 5e-4)
check("Q14 E2 J", E2, 3.368e-19, 5e-4); check("Q14 E2 eV", E2 / e, 2.105, 5e-4)
check("Q14 dE J", E1 - E2, 3.43e-22); check("Q14 dE eV", (E1 - E2) / e, 2.1e-3, 3e-2)
check("guide: 2.1074 eV", E1 / e, 2.1074, 1e-5); check("guide: 2.1052 eV", E2 / e, 2.1052, 5e-5)
rs = [i * 1e-3 * a0 for i in range(1, 10000)]; P = [r * r * math.exp(-2 * r / a0) for r in rs]
check("Q15 max of r^2 exp(-2r/a0)", rs[P.index(max(P))], a0, 1e-3)

print("== Unit 4 (configurations built with Madelung's rule, Cr and Cu exceptions)")
SUBS = [x for x in sorted([f"{n}{s}" for n in range(1, 10) for s in "spdfg" if L[s] < n], key=madelung_key)
        if madelung_key(x)[0] <= 9]  # up to 9s, which opens period 9
CAP = {"s": 2, "p": 6, "d": 10, "f": 14, "g": 18}
def config(Z):
    out, left = [], Z
    for sub in SUBS:
        if left == 0: break
        x = min(CAP[sub[-1]], left); out.append((sub, x)); left -= x
    d = dict(out)
    if Z in (24, 29):  # Cr, Cu: one 4s electron moves to 3d
        d["4s"] -= 1; d["3d"] += 1
    return d
def unpaired(d):
    tot = 0
    for sub, x in d.items():
        norb = CAP[sub[-1]] // 2; tot += x if x <= norb else 2 * norb - x
    return tot
same("Q3 Cl", config(17), {"1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 5})
same("Q5 unpaired N, O, F", [unpaired(config(z)) for z in (7, 8, 9)], [3, 2, 1])
same("Fe", config(26), {"1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 6, "4s": 2, "3d": 6})
same("Q7 Br valence", {k: v for k, v in config(35).items() if k[0] == "4" or k == "3d"}, {"4s": 2, "3d": 10, "4p": 5})
same("Q6 (d) Sr", config(38)["5s"], 2)
same("Q10-11, Q14 unpaired Fe Cr Cu Mn Zn", [unpaired(config(z)) for z in (26, 24, 29, 25, 30)], [4, 6, 1, 5, 0])
same("Q14 Mn2+ (3d5) / Mn3+ (3d4)", [unpaired({"3d": 5}), unpaired({"3d": 4})], [5, 4])
period_subs = {}
for sub in SUBS:  # a period starts at each ns
    if sub.endswith("s"): p = int(sub[:-1]); period_subs[p] = []
    period_subs[p].append(sub)
same("Q13 period lengths 1-7", [sum(CAP[s[-1]] for s in period_subs[p]) for p in range(1, 8)], [2, 8, 8, 18, 18, 32, 32])
same("Q15 period 8 subshells", period_subs[8], ["8s", "5g", "6f", "7d", "8p"])
same("Q15 next noble gas Z", 118 + sum(CAP[s[-1]] for s in period_subs[8]), 168)

print("== Unit 5")
check("Cl average", 0.7577 * 34.97 + 0.2423 * 36.97, 35.45, 5e-4)
check("K average", 0.9326 * 38.96 + 0.0673 * 40.96, 39.09, 1e-4)
check("B abundance of 10B", (11.009 - 10.81) / (11.009 - 10.013), 0.200)
check("Q4 Na IE J/atom", 496e3 / NA, 8.24e-19); check("Q4 Na IE eV", 496e3 / NA / e, 5.15)
check("Q4 1 eV in kJ/mol", e * NA / 1e3, 96.4, 1e-3)
check("Q9 Na lambda nm", lam(496e3 / NA) * 1e9, 241); check("Q9 He lambda nm", lam(2372e3 / NA) * 1e9, 50.4)
check("Q9 He J/atom", 2372e3 / NA, 3.94e-18); check("Q9 PES Ek", 21.2 - 496e3 / NA / e, 16.0)
check("Q12 delta e (C)", 1.08 * 3.336e-30 / 127e-12, 2.84e-20); check("Q12 delta", 1.08 * 3.336e-30 / 127e-12 / e, 0.18, 2e-2)
chi = {"H": 2.2, "F": 3.98, "Cl": 3.16, "Br": 2.96, "I": 2.66}
same("Q12 polarity order", sorted(["F", "Cl", "Br", "I"], key=lambda x: chi[x] - chi["H"]), ["I", "Br", "Cl", "F"])
dHF = 567 - math.sqrt(436 * 158); dHI = 299 - math.sqrt(436 * 151)
check("Q13 sqrt(436*158)", math.sqrt(436 * 158), 262.5, 1e-3); check("Q13 Delta HF", dHF, 304.5, 1e-3)
check("Q13 dchi HF", 0.102 * math.sqrt(dHF), 1.78); check("Q13 chi F", 2.20 + 0.102 * math.sqrt(dHF), 3.98)
check("Q13 Delta HI", dHI, 42.4, 1e-3); check("Q13 dchi HI", 0.102 * math.sqrt(dHI), 0.66, 1e-2); check("Q13 chi I", 2.20 + 0.102 * math.sqrt(dHI), 2.86)
check("Pauling arithmetic-mean HF (not used)", math.sqrt((567 - (436 + 158) / 2) / 96.5), 1.67)
sig_Cl = 6 * 0.35 + 8 * 0.85 + 2 * 1.00
check("Q14 Slater sigma Cl", sig_Cl, 10.9); check("Q14 Zeff Cl", 17 - sig_Cl, 6.1)
check("Q14 chi_AR Cl", 0.359 * 6.1 / 0.99 ** 2 + 0.744, 2.98); check("Slater Zeff F", 9 - (6 * 0.35 + 2 * 0.85), 5.2)
check("Slater Zeff Na", 11 - (8 * 0.85 + 2), 2.2)
IE = {"Mg": [738, 1451, 7733, 10543], "Al": [578, 1817, 2745, 11577]}
for el, v in IE.items():
    ratios = [v[i + 1] / v[i] for i in range(3)]
    same(f"jump position {el} (valence electrons)", ratios.index(max(ratios)) + 1, {"Mg": 2, "Al": 3}[el])

print("\nFAILURES:", fails)
