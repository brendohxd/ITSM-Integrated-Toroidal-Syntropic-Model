"""Complete classical R4C1 frame/metric variation; conditional, not gate closure.

General algebra is checked by SymPy directional differentiation. A separate
exact rational Taylor algebra evaluates full 4D off-shell Ward residuals.
No fitted inputs, field equations imposed on the probes, or provider calls.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import random
from fractions import Fraction as F
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_CHECK_CONTRACT_2026-09-25.md":
        "ad553a06fcec073cc176a68ef3f6b1bb77b5506d0ba5006606ff56ab595318db",
    "Analysis/MasterTests/test_01_r4c1_current_audit.py":
        "625c6e1b32818719ba0f12ff93b37ea680e6955f9f60f37784f99a45e7f3d740",
}
OUT = ROOT / "Analysis/MasterTests/outputs/test_01_r4c1_full_variation_summary.json"
N = 4


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def outer(a,b):
    return [[x*y for y in b] for x in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def mv(a,v):
    return [dot(row,v) for row in a]


def mm(a,b):
    bt = transpose(b)
    return [[dot(row,col) for col in bt] for row in a]


def matadd(*terms):
    return [[sum(a[i][j] for a in terms) for j in range(N)] for i in range(N)]


def scale(q,a):
    return [[q*x for x in row] for row in a]


def eye():
    return [[int(i==j) for j in range(N)] for i in range(N)]


def symouter(a,b):
    return scale(F(1,2),matadd(outer(a,b),outer(b,a)))


def trace(a):
    return sum(a[i][i] for i in range(N))


def frame_blocks(g,gi,U,V,J,p,k,z,lam,c):
    """Explicit L, dL/dV, dL/dU, 2dL/dg at fixed covariant gradients.

    Matrices P[a][c]=P_c^a, B2[m][n]=2 partial L/partial g_mn.
    This implementation uses either exact symbolic or rational-jet scalars.
    """
    M,c1,c2,c3,c4,K,A,b,zz = [c[name] for name in ('M','c1','c2','c3','c4','K','A','b','zz')]
    Ulow = mv(g,U)
    ell2 = -dot(U,Ulow)
    ell = ell2**F(1,2)
    n = [x/ell for x in U]
    nl = mv(g,n)
    h = matadd(gi,outer(n,n))
    hc = matadd(g,outer(nl,nl))
    hm = matadd(eye(),outer(n,nl))
    Q,Qz,Jn = dot(n,p),dot(n,k),dot(n,J)
    Y = dot(p,mv(h,p))
    w = [p[i]+Q*nl[i] for i in range(N)]
    wz = [k[i]+Qz*nl[i] for i in range(N)]
    wJ = [J[i]+Jn*nl[i] for i in range(N)]
    au = mv(transpose(V),U)
    aul = mv(g,au)
    vv = mv(transpose(V),n)
    D = dot(nl,vv)
    BB = dot(w,vv)
    accel = [x/ell for x in mv(hm,vv)]
    I1 = trace(mm(mm(mm(gi,V),g),transpose(V)))
    LU = -M*(c1*I1+c2*trace(V)**2+c3*trace(mm(V,V))-c4*dot(au,aul))/2
    LU += lam*(dot(U,Ulow)+1)/2
    LA = -zz*dot(J,mv(h,J))/2
    LQ = K*Q**2/2-A*Y**F(3,2)
    LR = b*z*z/2-b*dot(k,mv(h,p))-b*z*BB/ell

    PU = scale(-M,matadd(scale(c1,mm(mm(gi,V),g)),scale(c2*trace(V),eye()),
                         scale(c3,transpose(V)),scale(-c4,outer(U,aul))))
    PR = scale(-b*z/ell,outer(n,w))
    FU = [M*c4*x+lam*y for x,y in zip(mv(V,aul),Ulow)]
    FA = [-zz*Jn*x/ell for x in wJ]
    FQ = [(K-3*A*Y**F(1,2))*Q*x/ell for x in w]
    hvw = mv(transpose(hm),mv(V,w))
    hcv = mv(hc,vv)
    FR = [-b*(Q*wz[i]+Qz*w[i])/ell
          -b*z*(nl[i]*BB+hvw[i]+w[i]*D+Q*hcv[i])/ell2 for i in range(N)]

    B2U = matadd(scale(-M*c1,matadd(mm(mm(transpose(V),gi),V),
        scale(-1,mm(mm(mm(mm(gi,V),g),transpose(V)),gi)))),
        scale(M*c4,outer(au,au)),scale(lam,outer(U,U)))
    Ju,pu,ku = mv(gi,J),mv(gi,p),mv(gi,k)
    B2A = scale(zz,matadd(outer(Ju,Ju),scale(-Jn**2,outer(n,n))))
    B2Q = matadd(scale(K*Q**2,outer(n,n)),
                scale(3*A*Y**F(1,2),matadd(outer(pu,pu),scale(-Q**2,outer(n,n)))))
    B2R = matadd(scale(2*b,symouter(ku,pu)),scale(-2*b*Q*Qz,outer(n,n)),
        scale(-2*b*z/ell,matadd(scale(BB+Q*D,outer(n,n)),scale(Q,symouter(vv,n)))))
    return {'Ls':[LU,LA,LQ,LR], 'P':matadd(PU,PR), 'PU':PU,'PR':PR,
            'F':[sum(x) for x in zip(FU,FA,FQ,FR)],
            'B2':matadd(B2U,B2A,B2Q,B2R), 'B2s':[B2U,B2A,B2Q,B2R],
            'n':n,'h':h,'Q':Q,'Y':Y,'a':accel}


def connection_tensor(U,P,gi):
    PP = mm(P,gi)
    return [[[(U[m]*PP[k][n]+U[n]*PP[k][m]+U[k]*(PP[m][n]+PP[n][m])
              -U[m]*PP[n][k]-U[n]*PP[m][k])/2 for n in range(N)]
             for m in range(N)] for k in range(N)]


class Audit:
    def __init__(self):
        self.checks = []

    def check(self,name,value,nonzero=False):
        if isinstance(value,Jet):
            value = value.constant
        if isinstance(value,(int,F)):
            ok = value != 0 if nonzero else value == 0
            residual = str(value)
        else:
            value = s.simplify(value)
            ok = value.is_zero is False if nonzero else value == 0
            residual = str(value)
        self.checks.append({'name':name,'passed':bool(ok),'residual':residual,
                            'expected':'nonzero_exact' if nonzero else 'zero_exact'})


def symbolic_variations(a):
    g = s.diag(-1,1,1,1)
    U = s.Matrix([s.Rational(10,3),s.Rational(8,3),0,0])
    V = s.Matrix(N,N,lambda i,j:s.Rational(1+2*i-j,7))
    J = s.Matrix([2,3,-1,4])
    p,k = s.Matrix([-1,2,2,1]),s.Matrix([3,-2,1,2])
    z,lam,t = s.symbols('z lambda_U variation',real=True)
    c = {key:s.Symbol(key,real=True) for key in ('M','c1','c2','c3','c4','K','A','b','zz')}

    def evaluate(gg,uu,vv):
        return frame_blocks(gg.tolist(),gg.inv().tolist(),list(uu),vv.tolist(),list(J),list(p),list(k),z,lam,c)

    base = evaluate(g,U,V)
    for i in range(N):
        for j in range(N):
            varied = V.copy()
            varied[i,j] += t
            L = sum(evaluate(g,U,varied)['Ls'])
            a.check(f'direct_V_variation_{i}{j}',s.diff(L,t).subs(t,0)-base['P'][i][j])
    for i in range(N):
        varied = U.copy()
        varied[i] += t
        L = sum(evaluate(g,varied,V)['Ls'])
        a.check(f'direct_U_variation_{i}',s.diff(L,t).subs(t,0)-base['F'][i])
    for i in range(N):
        for j in range(i,N):
            varied = g.copy()
            varied[i,j] += t
            if i != j:
                varied[j,i] += t
            blocks = evaluate(varied,U,V)
            for sector in range(4):
                target = base['B2s'][sector][i][j]*(1 if i!=j else F(1,2))
                a.check(f'direct_metric_sector_{sector}_{i}{j}',
                        s.diff(blocks['Ls'][sector],t).subs(t,0)-target)
    # Match connection-variation coefficients with arbitrary independent
    # symmetric metric derivative variables, not a selected numeric tensor.
    P = [[s.Symbol(f'P{i}{j}') for j in range(N)] for i in range(N)]
    dg = [[[s.Symbol(f'dg{k}_{min(i,j)}{max(i,j)}') for j in range(N)]
           for i in range(N)] for k in range(N)]
    gi = g.inv().tolist()
    conn = [[[sum(gi[c][d]*(dg[a0][d][b]+dg[b][d][a0]-dg[d][a0][b])/2
                     for d in range(N)) for b in range(N)] for a0 in range(N)] for c in range(N)]
    direct = sum(P[a0][c0]*conn[c0][a0][b]*U[b] for a0 in range(N) for c0 in range(N) for b in range(N))
    CC = connection_tensor(list(U),P,gi)
    expected = sum(CC[k0][m][n]*dg[k0][m][n]/2 for k0 in range(N) for m in range(N) for n in range(N))
    a.check('connection_metric_derivative_identity',s.expand(direct-expected))
    for var in sorted({v for plane in dg for row in plane for v in row},key=str):
        a.check(f'connection_coefficient_{var}',s.diff(s.expand(direct-expected),var))


ZERO = (0,0,0,0)
INDICES = tuple((i,j,k,l) for i in range(4) for j in range(4-i)
                for k in range(4-i-j) for l in range(4-i-j-k))


class Jet:
    """Taylor COEFFICIENTS (not derivatives), exact total degree <=3.

    Differentiation lowers the known order. Only constant Ward residuals are
    consumed: they need no more than the supplied third field derivatives.
    """
    def __init__(self,data=0):
        self.data = ({k:F(v) for k,v in data.items() if v} if isinstance(data,dict)
                     else ({ZERO:F(data)} if data else {}))

    @property
    def constant(self):
        return self.data.get(ZERO,F(0))

    def __add__(self,other):
        other = other if isinstance(other,Jet) else Jet(other)
        out = self.data.copy()
        for k,v in other.data.items():
            out[k] = out.get(k,F(0))+v
        return Jet(out)

    __radd__ = __add__

    def __neg__(self):
        return Jet({k:-v for k,v in self.data.items()})

    def __sub__(self,other):
        return self+-other

    def __rsub__(self,other):
        return other+-self

    def __mul__(self,other):
        if not isinstance(other,Jet):
            return Jet({k:v*F(other) for k,v in self.data.items()})
        out = {}
        for k,v in self.data.items():
            for l,w in other.data.items():
                p = tuple(x+y for x,y in zip(k,l))
                if sum(p)<=3:
                    out[p] = out.get(p,F(0))+v*w
        return Jet(out)

    __rmul__ = __mul__

    def __truediv__(self,other):
        return self*(other**-1) if isinstance(other,Jet) else self*F(1,other)

    def __rtruediv__(self,other):
        return other*(self**-1)

    def __pow__(self,power):
        power = F(power)
        if power.denominator == 1 and power >= 0:
            out = Jet(1)
            for _ in range(int(power)):
                out = out*self
            return out
        base = self.constant
        if not base:
            raise ValueError('Nonintegral/inverse jet power at zero')
        if power.denominator == 1:
            prefactor = base**int(power)
        elif power.denominator == 2 and base>0:
            num,den = math.isqrt(base.numerator),math.isqrt(base.denominator)
            if num*num!=base.numerator or den*den!=base.denominator:
                raise ValueError('Probe requires an exact rational square root')
            prefactor = F(num,den)**power.numerator
        else:
            raise ValueError('Unsupported exact jet exponent')
        small = (self-base)/base
        out,term,coeff = Jet(1),Jet(1),F(1)
        for n in range(1,4):
            term = term*small
            coeff *= (power-n+1)/n
            out += coeff*term
        return prefactor*out

    def d(self,axis):
        out = {}
        for k,v in self.data.items():
            if k[axis]:
                p = list(k)
                p[axis] -= 1
                out[tuple(p)] = k[axis]*v
        return Jet(out)

    def exp_zero(self):
        if self.constant:
            raise ValueError('exp probe requires zero constant')
        return 1+self+self**2/2+self**3/6


def jet_arithmetic_controls(a):
    x = s.Symbol('x')
    j = Jet({ZERO:4,(1,0,0,0):2,(2,0,0,0):-3,(3,0,0,0):1})
    poly = 4+2*x-3*x*x+x**3
    for power in (F(-1),F(1,2),F(3,2)):
        expected = s.series(poly**s.Rational(power.numerator,power.denominator),x,0,4).removeO().expand()
        actual = j**power
        for order in range(4):
            a.check(f'jet_independent_sympy_power_{power}_{order}',
                    s.Rational(actual.data.get((order,0,0,0),0))-expected.coeff(x,order))
    ex = (j-4).exp_zero()
    expected = s.series(s.exp(poly-4),x,0,4).removeO().expand()
    for order in range(4):
        a.check(f'jet_independent_exp_{order}',s.Rational(ex.data.get((order,0,0,0),0))-expected.coeff(x,order))
    a.check('jet_mixed_derivative',Jet({(1,2,0,0):F(3,7)}).d(0).d(1).d(1).constant-F(6,7))


def jet_probe(a,seed):
    rng = random.Random(seed)

    def field(value,gradient=None):
        data = {key:F(rng.randint(-2,2),20) for key in INDICES if key!=ZERO}
        data[ZERO] = F(value)
        if gradient is not None:
            for i,v in enumerate(gradient):
                key = tuple(int(k==i) for k in range(N))
                data[key] = F(v)
        return Jet(data)

    g = [[None]*N for _ in range(N)]
    eta = [[(-1 if i==0 else 1)*int(i==j) for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(i,N):
            g[i][j] = g[j][i] = field(eta[i][j])
    perturb = matadd(g,scale(-1,eta))
    # (eta+dg)^-1 = [I-eta.dg+(eta.dg)^2-(eta.dg)^3] eta.
    H = mm(eta,perturb)
    gi = mm(matadd(eye(),scale(-1,H),mm(H,H),scale(-1,mm(mm(H,H),H))),eta)
    prod = mm(g,gi)
    a.check(f'{seed}_inverse_metric_all_coefficients',sum(
        v*v for i in range(N) for j in range(N) for v in (prod[i][j]-int(i==j)).data.values()))
    U0 = (2,0,0,0) if seed==4101 else (F(10,3),F(8,3),0,0)
    p0 = (1,2,2,1) if seed==4101 else (-1,2,2,1)
    U = [field(x) for x in U0]
    u,v,r,psi,z,eps,lam,tau = [field(x,gr) for x,gr in (
        (1,None),(2,None),(1,None),(0,p0),(1,None),(2,None),(1,None),(0,(2,F(1,2),0,0)))]
    du,dv,dr,p,k,de,dl,dt = [[f.d(i) for i in range(N)] for f in (u,v,r,psi,z,eps,lam,tau)]
    gamma = [[[sum(gi[c][d]*(g[d][b].d(aa)+g[d][aa].d(b)-g[aa][b].d(d))/2
                         for d in range(N)) for b in range(N)] for aa in range(N)] for c in range(N)]
    V = [[U[b].d(aa)+sum(gamma[b][aa][cc]*U[cc] for cc in range(N)) for b in range(N)] for aa in range(N)]
    c = dict(zip(('M','c1','c2','c3','c4','K','A','b','zz'),
                 (F(2,3),F(1,5),F(-1,7),F(2,9),F(3,11),F(3),F(2,7),F(5,11),F(1,13))))
    beta,gr,m2,l4,l6,cutoff,mr2,lr = F(2,5),F(3,7),F(1),F(1,3),F(1,5),F(2),F(2),F(1,7)
    J = [v*du[i]-u*dv[i] for i in range(N)]
    blocks = frame_blocks(g,gi,U,V,J,p,k,z,lam,c)
    a.check(f'{seed}_force_domain_Y',blocks['Y'].constant-9)
    a.check(f'{seed}_off_shell_frame_norm',dot(U,mv(g,U)).constant+4)
    P,FC = blocks['P'],blocks['F']
    CC = connection_tensor(U,P,gi)

    def divvec(w):
        return sum(w[mu].d(mu)+sum(gamma[mu][mu][d]*w[d] for d in range(N)) for mu in range(N))

    def divmixed(T):
        return [sum(T[mu][nu].d(mu)+sum(gamma[mu][mu][d]*T[d][nu]
            -gamma[d][mu][nu]*T[mu][d] for d in range(N)) for mu in range(N)) for nu in range(N)]

    def divstress(T):
        return divmixed(mm(T,g))

    divP = divmixed(P)
    EU = [FC[i]-divP[i] for i in range(N)]
    divCC = [[sum(CC[aa][m][n].d(aa)+sum(
        gamma[aa][aa][d]*CC[d][m][n]+gamma[m][aa][d]*CC[aa][d][n]
        +gamma[n][aa][d]*CC[aa][m][d] for d in range(N)) for aa in range(N))
        for n in range(N)] for m in range(N)]

    up = lambda x:mv(gi,x)
    dotg = lambda x,y:dot(x,up(y))
    radius = u*u+v*v
    VP = m2*radius/2+l4*radius**2/8+l6*radius**3/(24*cutoff**2)
    VR = mr2*r*r/2+lr*r**4/4
    W = gr*radius*r*r/4
    Wr = gr*radius*r/2
    LPhi = -(dotg(du,du)+dotg(dv,dv))/2-VP-W
    LP = LPhi+sum(blocks['Ls'])
    LR = -dotg(dr,dr)/2-VR
    conform = (beta*psi).exp_zero()
    Lm = -eps*(conform**2*dotg(dt,dt)+conform**4)/2
    TP_alg = matadd(scale(LP,gi),outer(up(du),up(du)),outer(up(dv),up(dv)),blocks['B2'])
    TP = matadd(TP_alg,scale(-1,divCC))
    TR = matadd(outer(up(dr),up(dr)),scale(LR,gi))
    Tm = matadd(scale(eps*conform**2,outer(up(dt),up(dt))),scale(Lm,gi))
    Ttotal = matadd(TP,TR,Tm)

    Cj = mv(blocks['h'],J)
    divCj = divvec(Cj)
    Vs = m2/2+l4*radius/4+l6*radius**2/(8*cutoff**2)
    Eu = divvec(up(du))-2*u*Vs-gr*u*r*r/2+c['zz']*(2*dot(Cj,dv)+v*divCj)
    Ev = divvec(up(dv))-2*v*Vs-gr*v*r*r/2-c['zz']*(2*dot(Cj,du)+u*divCj)
    Er = divvec(up(dr))-mr2*r-lr*r**3-Wr
    hp,hk = mv(blocks['h'],p),mv(blocks['h'],k)
    Pi = [c['K']*blocks['Q']*blocks['n'][i]-3*c['A']*blocks['Y']**F(1,2)*hp[i]
          -c['b']*hk[i]-c['b']*z*blocks['a'][i] for i in range(N)]
    Ep = -divvec(Pi)
    Ez = c['b']*(z+divvec(hp)-dot(blocks['a'],p))
    Elam = (dot(U,mv(g,U))+1)/2
    Etau = divvec([eps*conform**2*x for x in up(dt)])
    Eeps = -(conform**2*dotg(dt,dt)+conform**4)/2
    Ttrace = trace(mm(Tm,g))
    vectorward = [dot(EU,V[nu])+q for nu,q in enumerate(divmixed(outer(U,EU)))]
    DP,DR,DM,DT = map(divstress,(TP,TR,Tm,Ttotal))
    totalres = []
    for nu in range(N):
        rhsP = Eu*du[nu]+Ev*dv[nu]+Ep*p[nu]+Ez*k[nu]+Elam*dl[nu]-Wr*dr[nu]+vectorward[nu]
        rhsR = Er*dr[nu]+Wr*dr[nu]
        rhsM = Etau*dt[nu]+Eeps*de[nu]+beta*Ttrace*p[nu]
        a.check(f'{seed}_plenum_Ward_{nu}',DP[nu]-rhsP)
        a.check(f'{seed}_reservoir_Ward_{nu}',DR[nu]-rhsR)
        a.check(f'{seed}_matter_Ward_{nu}',DM[nu]-rhsM)
        residual = DT[nu]-(Eu*du[nu]+Ev*dv[nu]+(Ep+beta*Ttrace)*p[nu]+Ez*k[nu]
            +Elam*dl[nu]+Er*dr[nu]+Etau*dt[nu]+Eeps*de[nu]+vectorward[nu])
        totalres.append(residual.constant)
        a.check(f'{seed}_complete_Ward_{nu}',residual)
    missing_conn = divstress(divCC)
    a.check(f'{seed}_omitted_connection_stress_rejected',sum(q.constant**2 for q in missing_conn),True)
    a.check(f'{seed}_wrong_connection_stress_sign_rejected',sum((2*q.constant)**2 for q in missing_conn),True)
    a.check(f'{seed}_omitted_vector_Ward_terms_rejected',sum(q.constant**2 for q in vectorward),True)
    return {'seed':seed,'spacetime_dimensions':4,'jet_total_degree':3,
            'arithmetic':'exact fractions; no tolerance',
            'complete_Ward_residuals':[str(x) for x in totalres],
            'physical_background':False,'U_norm_squared':'-4','Y':'9'}


def main():
    for name,expected in PINS.items():
        if sha(ROOT/name)!=expected:
            raise RuntimeError(f'FROZEN_INPUT_HASH_MISMATCH: {name}')
    audit = Audit()
    symbolic_variations(audit)
    print('Direct symbolic variations completed',flush=True)
    jet_arithmetic_controls(audit)
    probes = []
    for seed in (4101,4102):
        probes.append(jet_probe(audit,seed))
        print(f'Exact 4D Ward probe {seed} completed',flush=True)
    passed = sum(c['passed'] for c in audit.checks)
    record = {'candidate':'R4C1-v1','checkpoint':'complete_classical_variation_Ward',
        'validation':'PASS' if passed==len(audit.checks) else 'FAIL',
        'passed':passed,'total':len(audit.checks),'checks':audit.checks,'probes':probes,
        'status':'CONDITIONAL_CLASSICAL_VARIATION_PARENT_AND_BACKGROUND_HOLD',
        'action_changed':False,'source_sha256':PINS,'script_sha256':sha(Path(__file__)),
        'runtime':{'python':platform.python_version(),'sympy':s.__version__},
        'scope':'general tensor variation with finite exact off-shell checks; not universal proof by sampling',
        'physical_background_verified':False,'physical_Hessian_verified':False,
        'healthy_continuous_GR_limit_verified':False,'quantum_renormalization_verified':False,
        'canonical_Test1_pass':False,'physics_pass':False,'gate_effect':'NONE','Rule9':'NOT_CLEARED',
        'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','K_Q':'NOT_DERIVED','V':'NOT_COMPUTED','Stage4A':'CLOSED'}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    OUT.with_suffix(OUT.suffix+'.sha256').write_text(f'{sha(OUT)}  {OUT.name}\n',encoding='ascii')
    print(json.dumps({k:record[k] for k in ('validation','passed','total','status','physics_pass')}))
    for check in audit.checks:
        if not check['passed']:
            print(json.dumps(check))
    return 0 if passed==len(audit.checks) else 1


if __name__=='__main__':
    raise SystemExit(main())
