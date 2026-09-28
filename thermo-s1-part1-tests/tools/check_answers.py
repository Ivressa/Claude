"""Independent re-computation of every answer in the Thermo-S1 Part 1 practice tests."""
import math
import sympy as sp

fails = 0
def check(label, got, expected, rel=1e-6):
    global fails
    ok = math.isclose(float(got), float(expected), rel_tol=rel, abs_tol=1e-12)
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {float(got):.6g}, key says {float(expected):.6g}")
    fails += (not ok)
def check_sym(label, expr, expected):
    global fails
    ok = sp.simplify(expr - expected) == 0
    print(f"{'OK ' if ok else 'BAD'} {label}: {sp.simplify(expr)}")
    fails += (not ok)

R_given = 8.3          # value given on the papers
RT300 = 2.5e3          # "RT ~ 2.5e3 J/mol at 300 K" given on the papers
check("RT at 300 K is ~2.5e3 (8.3*300)", R_given * 300, 2.49e3)

print("== 1.A")
check("Ex1 24.5 L/mol in m3/mol", 24.5e-3, 2.45e-2)
n = 5.85 / 58.5
check("Ex4 n", n, 0.100); check("Ex4 c_m (g/L)", 5.85 / 0.500, 11.7)
check("Ex4 c (mol/L)", n / 0.500, 0.200); check("Ex4 c*M", (n / 0.500) * 58.5, 11.7)

print("== 1.B")
check("Ex1 77 K in degC", 77 - 273.15, -196.15)
S = 2.0e-4
check("Ex4 mg/S", 1.0 * 10 / S, 5.0e4); check("Ex4 p", 1.0e5 + 1.0 * 10 / S, 1.5e5)

print("== 1.C")
check("Ex1 1013 hPa in bar", 1013e2 / 1e5, 1.013)
nn, T, p = 1.0, 300.0, 1.0e5
dVdT = nn * R_given / p; dVdp = -nn * R_given * T / p**2
check("Ex4 dV/dT", dVdT, 8.3e-5); check("Ex4 dV/dp", dVdp, -2.49e-7)
check("Ex4 dV", dVdT * 3.0 + dVdp * 1.0e3, 0.0)

print("== 2.A")
check("Ex1 chi_T in bar^-1", 4.5e-10 * 1e5, 4.5e-5)
check("Ex4a dV (mL)", 2.0e-4 * 250 * 50, 2.5)
check("Ex4b dV/V", -5.0e-10 * (101 - 1) * 1e5, -5.0e-3)
# exact (exponential) versions of the linear estimates stay close
check("Ex4a exact exp form (mL)", 250 * (math.exp(2.0e-4 * 50) - 1), 2.5, rel=6e-3)

print("== 2.B")
check("Ex4 dp (Pa)", (1 / 300) * 2.0e5 * 30, 2.0e4)
check("Ex4 p2 (bar)", 2.0 + 0.20, 2.2); check("Ex4 exact ideal p2 = p1*T2/T1", 2.0 * 330 / 300, 2.2)

print("== 2.C")
check("Ex1 beta", 3.3e-3 / (1.0e5 * 1.0e-5), 3.3e-3)
Ts, ps, Vs, ns, Rs, bs = sp.symbols('T p V n R b', positive=True)
Vexpr = ns * Rs * Ts / ps + ns * bs
alpha = sp.diff(Vexpr, Ts) / Vexpr
chiT = -sp.diff(Vexpr, ps) / Vexpr
pexpr = ns * Rs * Ts / (Vs - ns * bs)
beta = (sp.diff(pexpr, Ts) / pexpr)
check_sym("Ex4 alpha = nR/(pV)", alpha - (ns * Rs / (ps * Vexpr)), 0)
check_sym("Ex4 chi_T = nRT/(p^2 V)", chiT - (ns * Rs * Ts / (ps**2 * Vexpr)), 0)
check_sym("Ex4 beta = 1/T", beta, 1 / Ts)
check_sym("Ex4 beta = alpha/(p chi_T)", alpha / (ps * chiT), 1 / Ts)
check_sym("Ex4 b->0 alpha", alpha.subs(bs, 0), 1 / Ts)
check_sym("Ex4 b->0 chi_T", chiT.subs(bs, 0), 1 / ps)
# cyclic relation for a generic equation of state (van der Waals) as a sanity check
a_ = sp.symbols('a', positive=True)
p_vdw = ns * Rs * Ts / (Vs - ns * bs) - a_ * ns**2 / Vs**2
dpdT = sp.diff(p_vdw, Ts); dpdV = sp.diff(p_vdw, Vs)
dVdT_p = -dpdT / dpdV; dVdp_T = 1 / dpdV; dTdV_p = 1 / dVdT_p
check_sym("cyclic rule (vdW)", dpdT * dTdV_p * dVdp_T, -1)

print("== 3.A")
check("Ex1 2.0 bar.L in J", 2.0e5 * 1.0e-3, 200)
check("Ex4a V2 (cm3)", 3.0 * 2.0 / 1.0, 6.0)
check("Ex4b V' (L)", 3.0 * 350 / 300, 3.5)
check("Ex4b V' with 273.15 (L)", 3.0 * (77 + 273.15) / (27 + 273.15), 3.5, rel=1e-3)
check("Ex4 trap: degC ratio (L)", 3.0 * 77 / 27, 8.555, rel=1e-3)
check_sym("Ex2 chi_T of pV=C", -sp.diff(sp.Symbol('C') / ps, ps) / (sp.Symbol('C') / ps), 1 / ps)

print("== 3.B")
check("Ex3 Z", 1.0e6 * 2.5e-3 / (1.0 * RT300), 1.0)
V1 = 50e-4 * 0.50
check("Ex4 V1", V1, 2.5e-3); p1 = 0.10 * RT300 / V1; check("Ex4 p1", p1, 1.0e5)
p2 = p1 * 50 / 25; check("Ex4 p2", p2, 2.0e5)
p3 = p2 * 450 / 300; check("Ex4 p3", p3, 3.0e5)
V4 = 0.10 * RT300 * 450 / 300 / 1.0e5; check("Ex4 V4", V4, 3.75e-3)
check("Ex4 L4 (m)", V4 / 50e-4, 0.75)
check("Ex4 V4 with R=8.314 (m3)", 0.10 * 8.314 * 450 / 1.0e5, 3.74e-3, rel=2e-3)
check("notes worked example: ideal V of 1 mol air at 2 bar, 25 C (L)", 8.314 * 298.15 / 2e5 * 1e3, 12.39, rel=1e-3)

print("== 3.C")
check("Ex1 b in cm3/mol", 4.27e-5 * 1e6, 42.7)
V = 0.50e-3; pid = RT300 / V
check("Ex4 p_id", pid, 5.0e6)
rep = RT300 / (V - 4.0e-5); att = 0.36 / V**2
check("Ex4 V-nb", V - 4.0e-5, 4.6e-4); check("Ex4 repulsive term", rep, 5.43e6, rel=1e-3)
check("Ex4 attractive term", att, 1.44e6); check("Ex4 p_vdW", rep - att, 4.0e6, rel=2e-3)
check("Ex4 Z", (rep - att) / pid, 0.80, rel=2e-3)
check("Ex4 with exact CO2 constants (bar)", (8.314 * 300 / (V - 4.27e-5) - 0.364 / V**2) / 1e5, 40.0, rel=5e-3)

print("== End of unit")
check("Ex1a", 350e-6, 3.50e-4); check("Ex1b", -40 + 273.15, 233.15); check("Ex1c", 5.0e-10 * 1e5, 5.0e-5)
dpdT_water = 2.0e-4 / 5.0e-10
check("Ex5 dp/dT water (Pa/K)", dpdT_water, 4.0e5); check("Ex5 dp (Pa)", dpdT_water * 5.0, 2.0e6)
check("Ex5 ideal gas p/T (Pa/K)", 1.0e5 / 300, 3.33e2, rel=2e-3)
check("Ex5 ratio ~1e3", dpdT_water / (1.0e5 / 300), 1.2e3)
check_sym("Ex6 ideal alpha", sp.diff(ns * Rs * Ts / ps, Ts) / (ns * Rs * Ts / ps), 1 / Ts)
check_sym("Ex6 ideal chi_T", -sp.diff(ns * Rs * Ts / ps, ps) / (ns * Rs * Ts / ps), 1 / ps)
check_sym("Ex6 ideal beta", sp.diff(ns * Rs * Ts / Vs, Ts) / (ns * Rs * Ts / Vs), 1 / Ts)
check("Ex7a p2 (bar)", 3.0 * 400 / 300, 4.0); check("Ex7a with 273.15", 3.0 * 400.15 / 300.15, 4.0, rel=1e-3)
check("Ex7b V' (cm3)", 1.0 * 1.0 / 1.25, 0.80)
p8 = 1.0e5 + 20 * 10 / 1.0e-2
check("Ex8 p", p8, 1.2e5); V81 = 1.0e-2 * 0.25; check("Ex8 V1", V81, 2.5e-3)
check("Ex8 n", p8 * V81 / RT300, 0.12); check("Ex8 h2 (cm)", 25 * 360 / 300, 30); check("Ex8 dh (cm)", 30 - 25, 5)
M = 0.78 * 28 + 0.21 * 32 + 0.01 * 40
check("Ex9 M (g/mol)", M, 28.96); check("Ex9 rho (29 g/mol)", 1.0e5 * 29e-3 / RT300, 1.16)
check("Ex9 rho with R=8.314, M=28.96", 1.0e5 * 28.96e-3 / (8.314 * 300), 1.16, rel=5e-3)
V10 = 0.10e-3
check("Ex10 p_id", RT300 / V10, 2.5e7); check("Ex10 V-nb", V10 - 4.0e-5, 6.0e-5)
rep10 = RT300 / (V10 - 4.0e-5); att10 = 0.14 / V10**2
check("Ex10 repulsive", rep10, 4.17e7, rel=2e-3); check("Ex10 attractive", att10, 1.4e7)
check("Ex10 p", rep10 - att10, 2.77e7, rel=2e-3); check("Ex10 Z", (rep10 - att10) / 2.5e7, 1.107, rel=2e-3)

print("\nFAILURES:", fails)
