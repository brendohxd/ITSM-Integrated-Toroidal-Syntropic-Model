"""Exact local auxiliary time-spatial derivatives; no global-domain estimate."""
from math import factorial
import sympy as s


def product(a,b):
    zero=s.zeros(3) if isinstance(a[0],s.MatrixBase) else s.S.Zero
    return [sum((a[j]*b[k-j] for j in range(k+1)),zero.copy() if hasattr(zero,'copy') else zero) for k in range(3)]


def add(*args):
    return [sum((a[k] for a in args),s.zeros(3)) for k in range(3)]


def calculate(h,ht,psi,psit):
    if len(h)!=4 or len(ht)!=4 or len(psi)!=5 or len(psit)!=5:
        raise ValueError('Explicit metric/time jets through 3 and scalar/time jets through 4 required')
    h=[s.Matrix(x) for x in h];ht=[s.Matrix(x) for x in ht]
    if any(x.shape!=(3,3) or x!=x.T for x in h+ht):
        raise ValueError('All metric/time jet matrices must be symmetric 3x3')
    if any(not x.is_Rational for a in h+ht for x in a):
        raise ValueError('This local exact version requires rational metric jets')
    if any(h[0][:k,:k].det()<=0 for k in (1,2,3)):
        raise ValueError('Spatial metric must be positive definite at evaluation point')
    H=[x/factorial(k) for k,x in enumerate(h)]
    T=[x/factorial(k) for k,x in enumerate(ht)]
    inv=[H[0].inv()]
    for k in (1,2):
        inv.append(-inv[0]*sum((H[j]*inv[k-j] for j in range(1,k+1)),s.zeros(3)))
    invt=[-x for x in product(product(inv,T[:3]),inv)]
    hp=[(k+1)*H[k+1] for k in range(3)]
    htp=[(k+1)*T[k+1] for k in range(3)]
    tr=[x.trace()/2 for x in product(inv,hp)]
    trt=[x.trace()/2 for x in add(product(invt,hp),product(inv,htp))]
    A=[x[2,2] for x in inv];At=[x[2,2] for x in invt]
    B=[x-y[2,2] for x,y in zip(product(A,tr),product(product(inv,hp),inv))]
    Bt=[x+y-z[2,2] for x,y,z in zip(product(At,tr),product(A,trt),
        add(product(product(invt,hp),inv),product(product(inv,htp),inv),product(product(inv,hp),invt)))]
    p1=[s.sympify(psi[k+1])/factorial(k) for k in range(3)]
    p2=[s.sympify(psi[k+2])/factorial(k) for k in range(3)]
    t1=[s.sympify(psit[k+1])/factorial(k) for k in range(3)]
    t2=[s.sympify(psit[k+2])/factorial(k) for k in range(3)]
    Z=[-factorial(k)*(x+y) for k,(x,y) in enumerate(zip(product(A,p2),product(B,p1)))]
    Zt=[-factorial(k)*(a+b+c+d) for k,(a,b,c,d) in enumerate(zip(product(At,p2),product(A,t2),product(Bt,p1),product(B,t1)))]
    return dict(Z=Z,Zt=Zt,physical_norm='NOT_DERIVED',global_domain='NOT_SUPPLIED')
