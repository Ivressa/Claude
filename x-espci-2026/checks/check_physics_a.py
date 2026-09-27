"""Checks of the Physics A solutions (X-ESPCI 2026): equations of motion, Taylor angle, spectrum."""
import sympy as sp, numpy as np, math
ok=True
def chk(label, cond):
    global ok
    print(('OK ' if cond else 'BAD'), label); ok &= bool(cond)
t=sp.symbols('t', real=True)
q,B,m,F,w,w0,tau,E,alpha=sp.symbols('q B m F omega omega_0 tau E alpha', positive=True)
I=sp.I
# Q15-16: x'' = (qB/m) y', y'' = -(qB/m) x'  ->  Z'' = -i(qB/m) Z'
W0=q*B/m
R=sp.symbols('R', positive=True)
x=R*sp.cos(W0*t); y=-R*sp.sin(W0*t)
chk("Q16 x eq", sp.simplify(m*sp.diff(x,t,2)-q*B*sp.diff(y,t))==0)
chk("Q16 y eq", sp.simplify(m*sp.diff(y,t,2)+q*B*sp.diff(x,t))==0)
Z=x+I*y
chk("Q16 Z = R exp(-i w0 t)", sp.simplify((Z-R*sp.exp(-I*W0*t)).rewrite(sp.exp))==0)
# Q19: m Z'' = -i q B Z' - (m/tau) Z' + F e^{-i w t}
Z0=F/(m*w*(w0-w-I/tau))
Zf=Z0*sp.exp(-I*w*t)
lhs=sp.diff(Zf,t,2); rhs=-I*w0*sp.diff(Zf,t)-sp.diff(Zf,t)/tau+F/m*sp.exp(-I*w*t)
chk("Q19 forced amplitude", sp.simplify(lhs-rhs)==0)
# Q25: Z = i A t e^{-i w0 t} solves Z'' + i w0 Z' = (qE/2m) e^{-i w0 t} with A = E/(2B), w0 = qB/m
A=E/(2*B)
Zr=I*A*t*sp.exp(-I*W0*t)
chk("Q25 resonant solution", sp.simplify(sp.diff(Zr,t,2)+I*W0*sp.diff(Zr,t)-q*E/(2*m)*sp.exp(-I*W0*t))==0)
# Q22: x-force qE cos(wt) = (qE/2)e^{-iwt} + (qE/2)e^{iwt}
chk("Q22 decomposition", sp.simplify((q*E/2*sp.exp(-I*w*t)+q*E/2*sp.exp(I*w*t)).rewrite(sp.cos)-q*E*sp.cos(w*t))==0)
# Q32: Laplace -> beta = 2
X,Y,Zc,beta=sp.symbols('x y z beta', real=True)
V=alpha/2*(-X**2-Y**2+beta*Zc**2)
chk("Q32 beta=2", sp.solve(sp.diff(V,X,2)+sp.diff(V,Y,2)+sp.diff(V,Zc,2),beta)==[2])
# Q33: wp^2 = 2 q alpha / m ; Q35 roots of w^2 - w0 w + wp^2/2 = 0
wp=sp.symbols('omega_p', positive=True)
roots=sp.solve(sp.Symbol('W')**2-w0*sp.Symbol('W')+wp**2/2, sp.Symbol('W'))
eps=sp.symbols('epsilon', positive=True)
series=[sp.series(r.subs(wp,eps*w0),eps,0,4).removeO() for r in roots]
exp1=sp.expand(w0-eps**2*w0/2); exp2=sp.expand(eps**2*w0/2)
chk("Q35 omega+ ~ w0 - wp^2/(2w0)", any(sp.simplify(sp.expand(s)-exp1 - sp.O(eps**4).removeO())==0 or sp.simplify(sp.expand(s)-exp1).as_poly(eps) is not None and sp.degree(sp.expand(s)-exp1,eps)>=4 for s in series))
chk("Q35 omega- ~ wp^2/(2w0)", any(sp.expand(s)-exp2==0 or (sp.expand(s)-exp2).as_poly(eps) is not None and min(sp.Poly(sp.expand(s)-exp2,eps).monoms())[0]>=4 for s in series))
# Q36: omega- = wp^2/(2 w0) = (2 q alpha/m)/(2 qB/m) = alpha/B
chk("Q36 omega- = alpha/B", sp.simplify((2*q*alpha/m)/(2*q*B/m)-alpha/B)==0)
# Q9-10: f(theta) = P_{1/2}(cos theta) regular at theta=0 ; zero at theta0 -> 180-49.3
from mpmath import mp, legenp, findroot, cos, pi, degrees
mp.dps=30
g=lambda th: legenp(0.5,0,cos(th))
th0=findroot(g, 2.28)
print("   zero of P_1/2(cos theta) at theta0 =", float(degrees(th0)), "deg ; 180-theta0 =", float(180-degrees(th0)))
chk("Q10 Taylor half-angle 49.3", abs(float(180-degrees(th0))-49.29)<0.05)
# check that V = r^(1/2) P_1/2(cos th) is harmonic
r,th=sp.symbols('r theta', positive=True)
f=sp.Function('f')
Vr=sp.sqrt(r)*f(th)
lap=sp.diff(r**2*sp.diff(Vr,r),r)/r**2 + sp.diff(sp.sin(th)*sp.diff(Vr,th),th)/(r**2*sp.sin(th))
ode=sp.simplify(lap*r**sp.Rational(3,2))
print("   ODE:", sp.simplify(ode))
chk("Q9 ODE is f''+cot f' + 3/4 f", sp.simplify(ode-(sp.diff(f(th),th,2)+sp.cos(th)/sp.sin(th)*sp.diff(f(th),th)+sp.Rational(3,4)*f(th)))==0)
# Q13: charge states
peaks={1999.30:17,1888.29:18,1788.93:19,1699.53:20,1618.60:21,1545.11:22,1478.02:23,1416.43:24,1359.76:25,1307.56:26,1259.16:27,1214.20:28,1172.37:29,1133.33:30,1096.81:31,1030.42:33,1000.15:34,971.54:35,944.61:36,2124.14:16,2265.52:15}
z_17=1888.29/(1999.30-1888.29); z_34=971.54/(1000.15-971.54)
print("   z from adjacent peaks:", round(z_17,2), round(z_34,2))
chk("Q13 z(1999.30)=17", round(z_17)==17); chk("Q13 z(1000.15)=34", round(z_34)==34)
ms=[p*z for p,z in peaks.items()]; mh=[z*(p-1.00728) for p,z in peaks.items()]
print("   m = z*(m/z): mean %.0f, spread %.0f ; with proton correction: mean %.1f, spread %.1f" % (np.mean(ms), np.ptp(ms), np.mean(mh), np.ptp(mh)))
chk("Q13 m ~ 3.40e4", abs(np.mean(ms)-3.40e4)<150)
print("   predicted z=32 peak (unlabelled):", round(33971/32+1.007,1))
# Q42 sampling frequency
f_max=1e8*7/(2*math.pi*900); print("   f_max(m/z=900) = %.3g Hz, f_s = %.3g Hz" % (f_max, 2*f_max))
chk("Q42 fs ~ 2.5e5 Hz", 2.3e5<2*f_max<2.7e5)
# Q30 numbers
kB=1.380649e-23; e=1.602e-19; mu=1.6605e-27
mmax=(e*7*0.03)**2/(kB*300)/mu; print("   m_max(z=1,B=7T,d=3cm,300K) = %.2g u" % mmax)
# Q5: Rayleigh with 2 gamma/R vs gamma/R -> ratio sqrt2
eps0,gam,Rr,Q=sp.symbols('epsilon_0 gamma R Q', positive=True)
Qlim=sp.solve(sp.Eq(Q**2/(32*sp.pi**2*eps0*Rr**4),gam/Rr),Q)[0]
Qray=sp.solve(sp.Eq(Q**2/(32*sp.pi**2*eps0*Rr**4),2*gam/Rr),Q)[0]
print("   Q_lim =", sp.simplify(Qlim), "; Rayleigh:", sp.simplify(Qray))
chk("Q5 ratio sqrt2", sp.simplify(Qray/Qlim-sp.sqrt(2))==0)
chk("Q5 Q_lim = 4 pi sqrt(2 eps0 gamma R^3)", sp.simplify(Qlim-4*sp.pi*sp.sqrt(2*eps0*gam*Rr**3))==0)
print("ALL OK" if ok else "SOME FAILURES")
