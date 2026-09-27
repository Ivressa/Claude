"""Independent re-computation of every answer in the Elec-S1 Part 1 practice tests."""
from fractions import Fraction as F
import math

fails = 0
def check(label, got, expected, rel=1e-9):
    global fails
    ok = math.isclose(float(got), float(expected), rel_tol=rel, abs_tol=1e-12)
    print(f"{'OK ' if ok else 'BAD'} {label}: computed {float(got):.6g}, key says {float(expected):.6g}")
    if not ok:
        fails += 1

# ------------------------------------------------------------ MNA solver --
def solve(n_nodes, resistors=(), vsources=(), isources=()):
    """Nodes 1..n_nodes, node 0 = ground. resistors: (a,b,R); vsources: (plus,minus,V);
    isources: (from,to,I) current I flowing from 'from' to 'to' through the source.
    Returns (node potentials dict, list of vsource currents (flowing out of + terminal))."""
    m = len(vsources)
    size = n_nodes + m
    A = [[F(0)] * size for _ in range(size)]
    z = [F(0)] * size
    def idx(n): return n - 1
    for a, b, R in resistors:
        g = F(1) / F(R)
        for p, q in ((a, b), (b, a)):
            if p:
                A[idx(p)][idx(p)] += g
                if q:
                    A[idx(p)][idx(q)] -= g
    for k, (p, q, V) in enumerate(vsources):
        r = n_nodes + k
        if p: A[idx(p)][r] += 1; A[r][idx(p)] += 1
        if q: A[idx(q)][r] -= 1; A[r][idx(q)] -= 1
        z[r] = F(V)
    for a, b, I in isources:
        if a: z[idx(a)] -= F(I)
        if b: z[idx(b)] += F(I)
    # Gaussian elimination
    for c in range(size):
        piv = next(r for r in range(c, size) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]; z[c], z[piv] = z[piv], z[c]
        for r in range(size):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
                z[r] -= f * z[c]
    x = [z[i] / A[i][i] for i in range(size)]
    V = {0: F(0)}
    V.update({n: x[idx(n)] for n in range(1, n_nodes + 1)})
    # MNA unknown is the current entering the + terminal from the circuit side;
    # current delivered out of + terminal = -x
    I = [-x[n_nodes + k] for k in range(m)]
    return V, I

# ------------------------------------------------------- topology counter --
def topology(points, components, wires):
    """components/wires: lists of (p, q). Returns dict of counts, using the marking
    convention of Test 1 (nodes = electrically distinct nodes)."""
    parent = {p: p for p in points}
    def find(p):
        while parent[p] != p:
            parent[p] = parent[parent[p]]; p = parent[p]
        return p
    for p, q in wires:
        parent[find(p)] = find(q)
    nets = {}
    for p in points:
        nets.setdefault(find(p), set()).add(p)
    terminals = {r: 0 for r in nets}
    for p, q in components:
        terminals[find(p)] += 1
        terminals[find(q)] += 1
    nodes = [r for r in nets if terminals[r] >= 3]
    series_joints = [r for r in nets if terminals[r] == 2]
    B = len(components) - len(series_joints)
    N = len(nodes)
    degree = {p: 0 for p in points}
    for p, q in list(components) + list(wires):
        degree[p] += 1; degree[q] += 1
    return dict(potentials=len(nets), nodes=N, branches=B, node_eqs=N - 1,
                meshes=B - N + 1, parts_with_wires=len(components) + len(wires),
                drawn_junctions=sum(1 for p in points if degree[p] >= 3),
                dots=len(points))

print("== Sanity check: Test 1 circuit (marker's answers: 2 nodes, 10 parts, 4 branches)")
pts = ["TL", "T1", "T2", "TR", "BL", "B1", "B2", "BR"]
comps = [("BL", "TL"), ("T1", "B1"), ("T2", "B2"), ("TR", "BR")]
wires = [("TL", "T1"), ("T1", "T2"), ("T2", "TR"), ("BL", "B1"), ("B1", "B2"), ("B2", "BR")]
t = topology(pts, comps, wires)
check("Test1 nodes", t["nodes"], 2); check("Test1 parts incl. wires", t["parts_with_wires"], 10)
check("Test1 branches", t["branches"], 4)

print("== 1.A")
check("Ex1 0.0258 MV in mV", 0.0258e6 * 1e3, 2.58e7)
pts = ["A1", "A2", "A3", "B", "M1", "M2", "M3"]
comps = [("M1", "A1"), ("A2", "B"), ("B", "M2"), ("A3", "M3")]           # e, L1, L2, L3
wires = [("A1", "A2"), ("A2", "A3"), ("M1", "M2"), ("M2", "M3")]
check("Ex3 distinct potentials", topology(pts, comps, wires)["potentials"], 3)
VA, VB, VM = 6.0, 2.0, 0.0
check("Ex3 u_AB", VA - VB, 4.0); check("Ex3 voltmeter V on B, COM on A", VB - VA, -4.0)
VA, VB, VC = 12.0, 4.5, -3.0
check("Ex4 u_AB", VA - VB, 7.5); check("Ex4 u_BC", VB - VC, 7.5)
check("Ex4 u_CA", VC - VA, -15.0); check("Ex4 sum", (VA - VB) + (VB - VC) + (VC - VA), 0)

print("== 1.B")
check("Ex1 4000 mAh in C", 4000e-3 * 3600, 14400)
check("Ex4 N electrons", 3.2e-3 * 5.0 / 1.6e-19, 1.0e17)
check("Test1 Ex4 drift speed (reference)", 1.0 / (8.0e28 * 2.0e-19 * 2.0e-6), 3.125e-5)

print("== 1.C")
check("Ex1 2.5e-2 kW in mW", 2.5e-2 * 1e3 * 1e3, 2.5e4)
pts = ["TL", "T1", "T2", "TR", "BL", "B1", "B2", "BR", "M"]
comps = [("BL", "TL"), ("T1", "B1"), ("T1", "T2"), ("T2", "B2"), ("TR", "M"), ("M", "BR")]
wires = [("TL", "T1"), ("T2", "TR"), ("BL", "B1"), ("B1", "B2"), ("B2", "BR")]
t = topology(pts, comps, wires)
check("Ex3 nodes", t["nodes"], 3); check("Ex3 branches", t["branches"], 5)
check("Ex3 parts incl. wires", t["parts_with_wires"], 11); check("Ex3 meshes", t["meshes"], 3)
check("Ex3 distractor: drawn junctions", t["drawn_junctions"], 4)
check("Ex3 distractor: dots", t["dots"], 9)
check("Ex4 energy J", 5.0 * 2.0 * 5400, 5.4e4); check("Ex4 energy Wh", 5.0 * 2.0 * 1.5, 15)

print("== 2.A")
check("Ex1 R from slope 20 mA/V", 1 / 20e-3, 50)
i = [1.0, 2.0, 4.0]; u = [0.70, 0.90, 2.00]
check("Ex4 naive (kOhm)", sum(uk / ik for uk, ik in zip(u, i)) / 3, 0.55)
check("Ex4 sum u*i", sum(uk * ik for uk, ik in zip(u, i)), 10.5)
check("Ex4 sum i^2", sum(ik ** 2 for ik in i), 21)
Rhat = sum(uk * ik for uk, ik in zip(u, i)) / sum(ik ** 2 for ik in i)
check("Ex4 regression (kOhm)", Rhat, 0.5)
check("Ex4 residual 1", u[0] - Rhat * i[0], 0.2); check("Ex4 residual 2", u[1] - Rhat * i[1], -0.1)
check("Ex4 residual 3", u[2] - Rhat * i[2], 0.0)

print("== 2.B")
check("Ex1 R from G = 0.25 mS", 1 / 0.25e-3, 4.0e3)
R = 12.0 ** 2 / 72
check("Ex4 R", R, 2.0); check("Ex4 i", 12 / R, 6.0); check("Ex4 E", 72 * 600, 43200)

print("== 2.C")
check("Ex1 1.7 uOhm.cm in Ohm.m", 1.7e-6 * 1e-2, 1.7e-8)
check("Ex3 ratio (2L, 2d)", 2 / 2 ** 2, 0.5)
R = 1.7e-8 * 20 / 0.50e-6
check("Ex4 R", R, 0.68); check("Ex4 p", R * 5.0 ** 2, 17)

print("== 3.A")
check("Ex1 6k || 3k", 6 * 3 / 9, 2.0)
check("Ex3 divider", 3 / 4 * 12, 9.0); check("Ex3 meshes", 5 - 3 + 1, 3); check("Ex3 3x30 || ", 30 / 3, 10)
# nodes: 1 = A, 2 = between E1 and R1, 3 = between E2 and R2
V, _ = solve(3, resistors=[(2, 1, 2), (3, 1, 3), (1, 0, 6)], vsources=[(2, 0, 12), (3, 0, 6)])
check("Ex4 V_A (MNA)", V[1], 8.0); check("Ex4 i3", V[1] / 6, F(4, 3))
check("Ex4 i1", (12 - V[1]) / 2, 2.0); check("Ex4 i2", (6 - V[1]) / 3, F(-2, 3))

print("== 3.B")
check("Ex1 E_Th", 2.0e-3 * 4.7e3, 9.4); check("Ex3 I_No", 12 / 3.0, 4.0)
# network: node1 = E+, node2 = N, node3 = A; B = ground. kOhm and mA units.
Voc, _ = solve(3, resistors=[(1, 2, 6), (2, 0, 3), (2, 3, 1)], vsources=[(1, 0, 12)])
check("Ex4 E_Th (open circuit, MNA)", Voc[3], 4.0)
_, Isc = solve(3, resistors=[(1, 2, 6), (2, 0, 3), (2, 3, 1)], vsources=[(1, 0, 12), (3, 0, 0)])
isc = -Isc[1]   # current flowing from A into the short circuit
check("Ex4 I_No (short circuit, MNA)", isc, F(4, 3))
check("Ex4 R_Th = E_Th / I_No", Voc[3] / isc, 3.0)
check("Tip: E current with AB shorted", F(12) / F(27, 4), F(16, 9))

print("== 3.C")
check("Ex1 Pmax", 12 ** 2 / (4 * 6.0), 6.0)
E, Rt, Rc = 12, 4, 8
i_ = F(E, Rt + Rc)
check("Ex4 i*", i_, 1.0); check("Ex4 u*", Rc * i_, 8.0); check("Ex4 Pc", Rc * i_ ** 2, 8.0)
check("Ex4 eta", F(Rc, Rt + Rc), F(2, 3)); check("Ex4 balance", E * i_ - Rt * i_ ** 2 - Rc * i_ ** 2, 0)
# key graph (illustrative): E=3, E/R=2, load slope 0.5
u_star = 2 / (0.5 + 2 / 3)
check("key graph u*", u_star, 1.714, rel=1e-3); check("key graph i*", 0.5 * u_star, 0.857, rel=1e-3)

print("== End-of-unit")
check("Ex1a", 0.047e3 * 1e3, 4.7e4); check("Ex1b", 3000e-3 * 3600, 1.08e4); check("Ex1c", 1.5e-6, 1.5e-6)
pts = ["TL", "T1", "TR", "TR2", "BL", "B1", "BR", "BR2", "M1", "M2"]
comps = [("BL", "TL"), ("T1", "M1"), ("M1", "B1"), ("TR", "M2"), ("M2", "BR"), ("M1", "M2"), ("TR2", "BR2")]
wires = [("TL", "T1"), ("T1", "TR"), ("TR", "TR2"), ("BL", "B1"), ("B1", "BR"), ("BR", "BR2")]
t = topology(pts, comps, wires)
check("Ex4 nodes", t["nodes"], 4); check("Ex4 branches", t["branches"], 7)
check("Ex4 node equations", t["node_eqs"], 3); check("Ex4 meshes", t["meshes"], 4)
check("Ex4 distractor: drawn junctions", t["drawn_junctions"], 6); check("Ex4 distractor: dots", t["dots"], 10)
check("Ex5 G from slope 2 V/mA (mS)", 1 / 2.0, 0.5)
v = 4.0 / (8.0e28 * 1.6e-19 * 2.5e-6)
check("Ex6 v", v, 1.25e-4); check("Ex6 dt (s)", 10 / v, 8.0e4); check("Ex6 dt (h)", 10 / v / 3600, 22.2, rel=2e-3)
R = 1.7e-8 * 10 / 2.5e-6
check("Ex6 R", R, 0.068); check("Ex6 p", R * 16, 1.088)
i = [1.0, 2.0, 3.0, 4.0]; u = [2.1, 4.1, 5.9, 8.0]
check("Ex7 sum u*i", sum(a * b for a, b in zip(u, i)), 60.0); check("Ex7 sum i^2", sum(b * b for b in i), 30)
check("Ex7 R (kOhm)", 60.0 / 30, 2.0); check("Ex7 G (mS)", 1 / 2.0, 0.5); check("Ex7 p (mW)", 8.0 * 4.0, 32)
# Ex8: node1 = E+, node2 = N (top of R2/R3). kOhm, mA.
V, I = solve(2, resistors=[(1, 2, 2), (2, 0, 6), (2, 0, 3)], vsources=[(1, 0, 12)])
check("Ex8 i (mA)", I[0], 3.0); check("Ex8 u (V)", V[2], 6.0)
check("Ex8 i2 (mA)", V[2] / 6, 1.0); check("Ex8 i3 (mA)", V[2] / 3, 2.0); check("Ex8 Req", 12 / I[0], 4.0)
# Ex9: E2 reversed: its + terminal on ground, so node3 (between E2 and R2) is at -4 V
V, _ = solve(3, resistors=[(2, 1, 4), (3, 1, 4), (1, 0, 2)], vsources=[(2, 0, 12), (0, 3, 4)])
check("Ex9 V_A (MNA)", V[1], 2.0)
V, _ = solve(3, resistors=[(2, 1, 4), (3, 1, 4), (1, 0, 2)], vsources=[(2, 0, 12), (3, 0, 4)])
check("Ex9 distractor (E2 not reversed)", V[1], 4.0)
# Ex10: node1 = E+, node2 = N, node3 = A. Ohms.
net = [(1, 2, 3), (2, 0, 6), (2, 3, 2)]
Voc, _ = solve(3, resistors=net, vsources=[(1, 0, 24)])
_, Isc = solve(3, resistors=net, vsources=[(1, 0, 24), (3, 0, 0)])
check("Ex10 E_Th", Voc[3], 16); check("Ex10 I_No", -Isc[1], 4); check("Ex10 R_Th", Voc[3] / -Isc[1], 4)
V, _ = solve(3, resistors=net + [(3, 0, 12)], vsources=[(1, 0, 24)])
check("Ex10 u* (full circuit with Rc)", V[3], 12); check("Ex10 i* (full circuit)", V[3] / 12, 1)
check("Ex10 eta", F(12, 16), 0.75); check("Ex10 Pmax", F(16 ** 2, 4 * 4), 16)
V, _ = solve(3, resistors=net + [(3, 0, 4)], vsources=[(1, 0, 24)])
check("Ex10 Pc at matching (full circuit)", V[3] ** 2 / 4, 16)
best = max((F(16) ** 2 * r / (4 + r) ** 2, r) for r in [F(k, 10) for k in range(1, 400)])
check("Ex10 argmax Pc by scan", best[1], 4)

print("\nFAILURES:", fails)
