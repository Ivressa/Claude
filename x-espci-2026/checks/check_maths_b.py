"""Checks of the Maths B solutions (X-ESPCI 2026): closed forms, spectra, moments."""
import sympy as sp, numpy as np, math
X, a, th = sp.symbols('X alpha theta')
ok = True
def chk(label, cond):
    global ok
    print(('OK ' if cond else 'BAD'), label); ok &= bool(cond)

# Q1: u_n in the four regimes
def u_seq(al, n):
    u=[0,1]
    for k in range(2,n+1): u.append(al*u[-1]-u[-2])
    return u
for al in [3.0, -3.0, 0.7, -1.3]:
    u=u_seq(al,12)
    if abs(al)>2:
        rp=(al+math.sqrt(al*al-4))/2; rm=(al-math.sqrt(al*al-4))/2
        f=[(rp**n-rm**n)/math.sqrt(al*al-4) for n in range(13)]
    else:
        t=math.acos(al/2); f=[math.sin(n*t)/math.sin(t) for n in range(13)]
    chk(f"Q1 alpha={al}", np.allclose(u,f))
chk("Q1 alpha=2", u_seq(2,12)==list(range(13)))
chk("Q1 alpha=-2", u_seq(-2,12)==[(-1)**(n+1)*n for n in range(13)])

# Q3c: int_0^pi (2cos t)^n dt = pi*binom(n,n/2) (n even), 0 (n odd)
for n in range(0,9):
    I=sp.integrate((2*sp.cos(th))**n,(th,0,sp.pi))
    exp_=sp.pi*sp.binomial(n,n//2) if n%2==0 else 0
    chk(f"Q3c n={n}", sp.simplify(I-exp_)==0)

# Q5: chi_n via recurrence; Q5d both coefficient formulas; Q6 roots
chi={0:sp.Integer(1),1:X}
for n in range(2,12): chi[n]=sp.expand(X*chi[n-1]-chi[n-2])
T=lambda n: sp.Matrix(n,n,lambda i,j: 1 if abs(i-j)==1 else 0)
for n in [2,3,4,5,7]:
    chk(f"Q5 chi_{n} = det", sp.expand((X*sp.eye(n)-T(n)).det()-chi[n])==0)
for n in range(2,12):
    f1=sum((-1)**m*sp.binomial(n-m,m)*X**(n-2*m) for m in range(n//2+1))
    f2=sum((-1)**m*sp.Rational(2)**(2*m-n)*sum(sp.binomial(n+1,2*j+1)*sp.binomial(j,m) for j in range(m,n//2+1))*X**(n-2*m) for m in range(n//2+1))
    f3=sp.expand(sp.Rational(1,2**n)*sum(sp.binomial(n+1,2*j+1)*X**(n-2*j)*(X**2-4)**j for j in range(n//2+1)))
    chk(f"Q5d n={n}", sp.expand(chi[n]-f1)==0 and sp.expand(chi[n]-f2)==0 and sp.expand(chi[n]-f3)==0)
for n in [2,3,6,9]:
    ev=np.sort(np.linalg.eigvalsh(np.array(T(n),dtype=float)))
    th_=np.sort(2*np.cos(np.arange(1,n+1)*np.pi/(n+1)))
    chk(f"Q6 n={n}", np.allclose(ev,th_))
# Q5c formula at a complex alpha
al=0.3+0.8j; d=np.sqrt(4-al*al)
for n in [2,5,8]:
    val=complex(chi[n].subs(X,al))
    form=((al+1j*d)/2)**(n+1)-((al-1j*d)/2)**(n+1); form/= (1j*d)
    chk(f"Q5c n={n}", abs(val-form)<1e-9)

# Q8: spectrum of T_n(a,b,c)
for (A,B,C) in [(0.5,2.0,0.5),(-1,3,0.25),(2,-1,-4)]:
    n=7
    M=np.diag([A]*n)+np.diag([B]*(n-1),1)+np.diag([C]*(n-1),-1)
    ev=np.sort(np.linalg.eigvals(M).real)
    th_=np.sort(A+2*math.sqrt(B*C)*np.cos(np.arange(1,n+1)*np.pi/(n+1)))
    chk(f"Q8c a,b,c={A,B,C}", np.allclose(ev,th_))
b,c=sp.symbols('b c')
M=sp.Matrix(5,5,lambda i,j: b if j==i+1 else (c if i==j+1 else 0))
cp=sp.expand((X*sp.eye(5)-M).det())
chk("Q8b char poly depends on bc only", sp.expand(cp.subs(b, b*c).subs(c,1) - cp)==0 or sp.simplify(cp - sp.expand((X*sp.eye(5)-sp.Matrix(5,5,lambda i,j: b*c if j==i+1 else (1 if i==j+1 else 0))).det()))==0)

# Q13b: Catalan moments of the semicircle
x=sp.symbols('x')
for k in range(0,9):
    S=sp.integrate(x**k*sp.sqrt(4-x**2),(x,-2,2))/(2*sp.pi)
    exp_=sp.binomial(k,k//2)/(k//2+1) if k%2==0 else 0
    chk(f"Q13b k={k}: {sp.nsimplify(S)}", sp.simplify(S-exp_)==0)

# Q10: sup errors of Q_n on [0,kappa] and [1-kappa,1]
for kap in [0.1,0.3,0.45]:
    xs=np.linspace(0,kap,400); ys=np.linspace(1-kap,1,400)
    errs=[(np.max(np.abs((1-xs**n)**(2.0**n)-1)), np.max((1-ys**n)**(2.0**n))) for n in [5,10,20,40]]
    bound_ok=all(e1<=(2*kap)**n+1e-12 for (e1,_),n in zip(errs,[5,10,20,40]))
    chk(f"Q10 kappa={kap}: sup|Q_n-1| <= (2 kappa)^n and sup Q_n on [1-kappa,1] -> 0", bound_ok and errs[-1][1]<errs[0][1]+1e-300)
print("ALL OK" if ok else "SOME FAILURES")
