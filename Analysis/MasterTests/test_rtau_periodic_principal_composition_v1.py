"""Periodic principal-operator composition; actual generator/time hold retained."""
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_PERIODIC_PRINCIPAL_COMPOSITION_V1_SPEC_2026-11-04.md'
OWNER = 'Theory/Gates/RES-001/RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md'
SOURCE = 'Analysis/MasterTests/test_rtau_mixed_principal_assembly_v1.py'
PARENT = 'Analysis/MasterTests/outputs/rtau_mixed_principal_assembly_v1_20261104/receipt.json'
ORDINARY = 'Analysis/MasterTests/outputs/rtau_ordinary_ward_energy_v4_20261104/receipt.json'
FACTORY = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
HIGHER = 'Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT/rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Fourier:
    """Exact finite polynomial; multiplication retains every convolution tail."""
    def __init__(self, value=0):
        raw = value if isinstance(value, dict) else {0:sp.sympify(value)}
        self.c = {k:v for k, x in raw.items() if (v := sp.expand(x)) != 0}
    @staticmethod
    def cast(x): return x if isinstance(x, Fourier) else Fourier(x)
    def __add__(self, other):
        other = self.cast(other)
        keys = self.c.keys() | other.c.keys()
        return Fourier({k:self.c.get(k, 0)+other.c.get(k, 0) for k in keys})
    __radd__ = __add__
    def __neg__(self): return Fourier({k:-v for k, v in self.c.items()})
    def __sub__(self, other): return self+-self.cast(other)
    def __rsub__(self, other): return self.cast(other)+-self
    def __mul__(self, other):
        other = self.cast(other)
        result = {}
        for k, a in self.c.items():
            for l, b in other.c.items(): result[k+l] = result.get(k+l, 0)+a*b
        return Fourier(result)
    __rmul__ = __mul__
    def __truediv__(self, scalar):
        assert not isinstance(scalar, Fourier)
        return self*(sp.Integer(1)/sp.sympify(scalar))
    def D(self): return Fourier({k:sp.I*k*v for k, v in self.c.items()})
    def P(self): return Fourier({k:v/(sp.I*k) for k, v in self.c.items() if k})
    def mean(self): return Fourier(self.c.get(0, 0))
    def iszero(self): return not self.c


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary = lambda x: [list(t) for t in iv.mpf(x)._mpi_]
    checks = []
    def check(name, ok, value=None): checks.append(dict(name=name, passed=bool(ok), value=value))
    parent, ordinary = [json.loads((ROOT/rel).read_text()) for rel in (PARENT, ORDINARY)]
    pins = dict(parent['source_sha256'])
    for rel in (SPEC, OWNER, SOURCE, PARENT, ORDINARY, FACTORY, HIGHER, Path(__file__).resolve().relative_to(ROOT).as_posix()):
        if rel in pins: assert pins[rel] == sha(ROOT/rel), rel
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel, want in pins.items():
        p = ROOT/rel
        assert sha(p) == want, rel
        for f in (p, Path(str(p)+'.sha256')):
            if f.exists(): snapshot[f] = (sha(f), f.stat().st_mtime_ns)
    check('all_219_original_and_parent_sources_preserved', parent['original_source_count'] == 219)
    check('all_parent_scoped_checks_pass', parent['passed'] == parent['total'] and ordinary['passed'] == ordinary['total'])

    # Independent noncommuting, spatially varying exact operator control.
    # No sample grid, antiderivative guess or truncated convolution is used.
    co = Fourier({1:sp.Rational(1, 2), -1:sp.Rational(1, 2)})
    sn = Fourier({1:-sp.I/2, -1:sp.I/2})
    co2 = Fourier({2:sp.Rational(1, 2), -2:sp.Rational(1, 2)})
    co3 = Fourier({3:sp.Rational(1, 2), -3:sp.Rational(1, 2)})
    fzero = lambda n, m: [[Fourier() for _ in range(m)] for _ in range(n)]
    fmul = lambda a,b: [[sum((a[i][k]*b[k][j] for k in range(len(b))), Fourier()) for j in range(len(b[0]))] for i in range(len(a))]
    fadd = lambda a,b, sign=1: [[x+sign*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    fmap = lambda a, method: [[getattr(x, method)() for x in row] for row in a]
    fscale = lambda a, scalar: [[x*scalar for x in row] for row in a]
    A, S, BD = fzero(3, 3), fzero(3, 3), fzero(3, 3)
    A[1][2], A[2][1] = 2+co*sp.Rational(1, 7), -3+sn*sp.Rational(1, 11)
    S[0][1], S[0][2] = (1+sn)*sp.I/13, (2+co)*sp.Rational(1, 17)
    S[1][0], S[2][0] = (1+co)*sp.Rational(1, 19), (1+sn)*sp.I/23
    BD[0][0], BD[1][1], BD[2][2] = co+sp.Rational(1, 5), sn*sp.Rational(1, 5), -sn*sp.Rational(1, 5)
    BD[1][2], BD[2][1] = Fourier(sp.Rational(1, 7)), co*sp.Rational(1, 11)
    B = fadd(BD, fadd(fmul(S, A), fmul(A, S), -1), -1)
    F, H = fmul(S, A), fmul(S, B)
    Fz, Fzz, Sz, Hz = fmap(F, 'D'), fmap(fmap(F, 'D'), 'D'), fmap(S, 'D'), fmap(H, 'D')
    u = [[1+sn], [co2+sn], [sp.Rational(1, 3)+co3]]
    applyG = lambda x, bb: fadd(fscale(fmul(A, fmap(fmap(x, 'D'), 'D')), -1), fscale(fmul(bb, fmap(x, 'D')), -sp.I))
    applyT = lambda x: fadd(x, fscale(fmap(fmul(S, x), 'P'), sp.I))
    lhs = fadd(applyT(applyG(u, B)), applyG(applyT(u), BD), -1)
    Rmul = fadd(fadd(fscale(Fz, sp.I), fscale(fmul(A, Sz), sp.I)), fadd(H, fmul(BD, S), -1))
    means = fadd(fadd(fscale(fmap(fmul(Fz, u), 'mean'), -2*sp.I), fscale(fmap(fmul(H, u), 'mean'), -1)), fmul(BD, fmap(fmul(S, u), 'mean')))
    rhs = fadd(fmul(Rmul, u), means)
    rhs = fadd(rhs, fscale(fmap(fmul(Fzz, u), 'P'), -sp.I))
    rhs = fadd(rhs, fmap(fmul(Hz, u), 'P'), -1)
    check('exact_noncommuting_periodic_composition_with_all_tails', all(x.iszero() for row in fadd(lhs, rhs, -1) for x in row))
    check('finite_rank_mean_omission_rejected', any(not x.iszero() for row in means for x in row))
    check('original_primitive_keeps_mean_of_transformed_state', all(x.iszero() for row in fadd(fmap(applyT(u), 'mean'), fmap(u, 'mean'), -1) for x in row))
    id1 = fadd(fmap(fmul(F, fmap(fmap(u, 'D'), 'D')), 'P'), fadd(fadd(fmul(F, fmap(u, 'D')), fmul(Fz, u), -1), fadd(fscale(fmap(fmul(Fz, u), 'mean'), 2), fmap(fmul(Fzz, u), 'P'))), -1)
    check('exact_periodic_P_F_D_squared_identity', all(x.iszero() for row in id1 for x in row))
    id2 = fadd(fmap(fmul(H, fmap(u, 'D')), 'P'), fadd(fadd(fmul(H, u), fmap(fmul(H, u), 'mean'), -1), fmap(fmul(Hz, u), 'P'), -1), -1)
    check('exact_periodic_P_H_D_identity', all(x.iszero() for row in id2 for x in row))

    # Reuse the immutable mixed setup through its coefficient construction.
    # This does not evaluate an action Hessian.
    source = load('periodic_composition_mixed_setup', SOURCE)
    tree = ast.parse((ROOT/SOURCE).read_text())
    fn = copy.deepcopy(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'calculate'))
    def target(node, key):
        return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == key for top in node.targets for t in ast.walk(top))
    end = next(i for i,n in enumerate(fn.body) if target(n, 'A2'))
    fn.name = 'mixed_coefficient_environment'
    fn.body = fn.body[:end]+[ast.Return(ast.Call(ast.Name('locals', ast.Load()), [], []))]
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), '<immutable-mixed-coefficient-setup>', 'exec'), source.__dict__)
    old = source.mixed_coefficient_environment()
    ctx, y = old['ctx'], old['y']
    # Needed second force derivatives come from a closed force formula on
    # certified spatial jets, not a new full Hessian or derivative of a radius.
    fac = load('periodic_composition_spatial_profiles', FACTORY)
    env = fac.prepare()
    mp.mp.dps = 100; mp.iv.dps = 60
    J = env['J']
    higher = json.loads((ROOT/HIGHER).read_text())
    third = decode(higher['whole_circle_third_shift_bound'])
    thirdbox = iv.mpf([-hi(third), hi(third)])
    yy, _ = env['state'](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [thirdbox]*3)
    par = old['par']
    rat = lambda q: iv.mpf(int(q.p))/int(q.q)
    KQ, Aforce, b0, beta0 = [rat(par[k]) for k in ('K_Q', 'A', 'b', 'beta')]
    a2j = yy[0]; aj = a2j**mp.mpf('.5'); kj = 1/a2j
    Nj = env['j'].exp(-yy[12]*beta0); muj = aj**3
    sj = yy[40]; pj = (yy[26]-yy[44]*sj)/Nj
    cvj = sum((v*v for v in yy[6:9]), J(0))*a2j
    gamj = (cvj+1)**mp.mpf('.5')
    rest = [v*(pj+yy[8]*sj/(gamj+1))+(kj*sj if i == 2 else 0) for i,v in enumerate(yy[6:9])]
    Yj = sum((v*v for v in rest), J(0))*a2j
    check('whole_root_force_positive_Y_branch_for_spatial_derivatives', lo(Yj.c[0]) > 0)
    Ysqrt = Yj**mp.mpf('.5')
    tj = cvj*pj+gamj*yy[8]*sj
    fppj = gamj**2*KQ-(cvj*Ysqrt+tj*tj/Ysqrt)*(3*Aforce)
    mj = muj*fppj/Nj
    dj = Nj*muj*kj*b0
    cj = gamj/aj
    fg = dj*sj/a2j/2
    pp, cv, ga, vv, ss, kap, aq, kq = sp.symbols('p cv ga v s kap A K', positive=True)
    Y = cv*pp**2+2*ga*vv*pp*ss+(kap+vv**2)*ss**2
    ff = kq*(ga*pp+vv*ss)**2/2-aq*Y**sp.Rational(3,2)
    want = kq*ga**2-3*aq*(cv*sp.sqrt(Y)+(cv*pp+ga*vv*ss)**2/sp.sqrt(Y))
    check('independent_exact_full_force_fpp_formula', sp.simplify(sp.diff(ff, pp, 2)-want) == 0)
    contains = lambda x: lo(x) <= 0 <= hi(x)
    check('closed_force_mass_and_first_derivative_match_export_enclosures', contains(mj.c[0]-old['m']) and contains(mj.c[1]-old['m_z']))
    mzz = 2*mj.c[2]

    class Pair:
        def __init__(self, v=0, dz=0):
            self.v = v if hasattr(v, '_mpi_') or hasattr(v, '_mpci_') else iv.mpf(v)
            self.z = dz if hasattr(dz, '_mpi_') or hasattr(dz, '_mpci_') else iv.mpf(dz)
        @staticmethod
        def cast(x): return x if isinstance(x, Pair) else Pair(x)
        def __add__(self, other):
            o = self.cast(other);return Pair(self.v+o.v, self.z+o.z)
        __radd__ = __add__
        def __neg__(self): return Pair(-self.v, -self.z)
        def __sub__(self, other): return self+-self.cast(other)
        def __rsub__(self, other): return self.cast(other)+-self
        def __mul__(self, other):
            o = self.cast(other);return Pair(self.v*o.v, self.z*o.v+self.v*o.z)
        __rmul__ = __mul__
        def __truediv__(self, other):
            o = self.cast(other);v = self.v/o.v;return Pair(v, (self.z-v*o.z)/o.v)
        def __rtruediv__(self, other): return self.cast(other)/self
        def __pow__(self, n):
            assert isinstance(n, int) and n >= 0
            result = Pair(1)
            for _ in range(n): result = result*self
            return result
        def conj(self): return Pair(iv.mpc(self.v.real, -self.v.imag), iv.mpc(self.z.real, -self.z.imag))
    pm = lambda n,m: [[Pair() for _ in range(m)] for _ in range(n)]
    pt = lambda a: [list(row) for row in zip(*a)]
    mm = lambda a,b: [[sum((a[i][k]*b[k][j] for k in range(len(b))), Pair()) for j in range(len(b[0]))] for i in range(len(a))]
    ma = lambda a,b, sign=1: [[x+sign*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    ms = lambda a,s: [[x*s for x in row] for row in a]
    pairmat = lambda a,az: [[Pair(v,d) for v,d in zip(row,drow)] for row,drow in zip(a,az)]
    values = lambda a: [[x.v for x in row] for row in a]
    derivs = lambda a: [[x.z for x in row] for row in a]
    dag = lambda a: [[x.conj() for x in row] for row in pt(a)]
    ii = Pair(iv.mpc(0, 1))
    hh, hz = old['h'], old['hz']
    slots = old['old'].SLOTS
    block = lambda rows,cols: [[Pair(hh(i,j), hz(i,j)) for j in cols] for i in rows]
    vs, ds, ws = [14+i for i in slots], [28+i for i in slots], [45,46,47]
    C0, D0 = block(vs, ws), block(ds, ws)
    KIz = old['scale'](old['mul'](old['mul'](ctx['KI'], [[hz(i,j) for j in ws] for i in ws]), ctx['KI']), -1)
    KI = pairmat(ctx['KI'], KIz)
    MP = ma(block(vs,vs), mm(mm(C0, KI), pt(C0)), -1)
    BP = ma(block(vs,ds), mm(mm(C0, KI), pt(D0)), -1)
    GP = ma(block(ds,ds), mm(mm(D0, KI), pt(D0)), -1)
    shift = Pair(ctx['shift'], yy[47].c[0])
    BP = ma(BP, ms(MP, shift))
    # Use raw B in Grel, not already shifted BP.
    rawB = ma(block(vs,ds), mm(mm(C0, KI), pt(D0)), -1)
    GP = ma(ma(GP, ms(ma(rawB, pt(rawB)), shift)), ms(MP, shift*shift))
    MI0 = old['MI']
    MIz = old['scale'](old['mul'](old['mul'](MI0, derivs(MP)), MI0), -1)
    MI = pairmat(MI0, MIz)
    BP = pairmat(old['BR'], derivs(BP))
    GP = pairmat(old['GR'], derivs(GP))
    c = Pair(old['c'], cj.c[1])
    for i in range(9):
        BP[i][5] = Pair(1 if i in (0,2) else 0)/(2*c)
        GP[i][5] = GP[5][i] = Pair()
    a2 = Pair(a2j.c[0], a2j.c[1]);kappa = Pair(kj.c[0], kj.c[1]);s = Pair(sj.c[0], sj.c[1])
    lam = Pair(a2j.c[1]/(2*a2j.c[0]), a2j.c[2]/a2j.c[0]-a2j.c[1]**2/(2*a2j.c[0]**2))
    d = Pair(old['d'], dj.c[1]); dz = Pair(dj.c[1], 2*dj.c[2])
    m = Pair(old['m'], old['m_z']); mz = Pair(old['m_z'], mzz)
    ap = 1/m;apz = -mz/(m*m)
    vp = (Pair(hh(26,40),hz(26,40))+shift*m)/m
    Tq = [[Pair(hh(26,j), hz(26,j)) for j in slots]]
    R = [[Pair(v) for v in row] for row in old['R']]
    X, Pmom = pm(9,18), pm(9,18)
    for i in range(9):
        for j in range(8): X[i][1+j] = Pair(int(old['E'][i,j]))
        Pmom[i][9+i] = Pair(1)
    X[0][14] = X[2][14] = ii*c
    velocity = mm(MI, ma(Pmom, ms(mm(BP,X),ii), -1))
    prate = ma(ms(mm(pt(BP),velocity), -ii), mm(GP,X))
    O = [pm(1,18)[0]]+mm(R,velocity)+prate
    Drel = ma(D0,ms(C0,shift))
    Wshift = ms(mm(KI,ma(mm(pt(C0),velocity),ms(mm(pt(Drel),X),ii))),-1)
    tx = mm(Tq,X)[0]
    tv = [(velocity[0][j]+velocity[2][j])/2 for j in range(18)]
    hmetric = kappa*s*c/a2
    FO = [[-kappa*ap*tx[j]-ii*kappa*s*Wshift[2][j]-ii*kappa*s*tv[j]/a2+(ii*vp*hmetric if j==14 else 0) for j in range(18)],pm(1,18)[0]]
    OF = pm(18,2)
    for i,slot in enumerate(slots):
        if slot in (0,3):OF[9+i][0] = -ii*d*s/(2*a2)
    AF = [[Pair(),kappa*ap],[-d,Pair()]]
    AFinv = [[Pair(),-1/d],[1/(kappa*ap),Pair()]]
    BF = [[-ii*vp,-ii*(2*kappa*apz+kappa*lam*ap)],[ii*(dz-d*s*beta0),-ii*vp]]
    A, B, BD, S = [pm(20,20) for _ in range(4)]
    sof, sfo = ms(mm(OF,AFinv),-1),mm(AFinv,FO)
    for i in range(18):
        for j in range(18):B[i][j]=BD[i][j]=O[i][j]
        for j in range(2):B[i][18+j]=OF[i][j];S[i][18+j]=sof[i][j]
    for i in range(2):
        for j in range(18):B[18+i][j]=FO[i][j];S[18+i][j]=sfo[i][j]
        for j in range(2):A[18+i][18+j]=AF[i][j];B[18+i][18+j]=BD[18+i][18+j]=BF[i][j]
    def ci(x): return hi(iv.sqrt(iv.mpf(ab(x.real))**2+iv.mpf(ab(x.imag))**2))
    def cinf(x): return max(hi(sum((iv.mpf(ci(t)) for t in row), iv.mpf(0))) for row in x)
    def norm2(x): return min(hi(iv.sqrt(sum((iv.mpf(ci(t))**2 for row in x for t in row),iv.mpf(0)))),hi(iv.sqrt(iv.mpf(cinf(x))*iv.mpf(cinf(pt(x))))))
    def compatible(a, stored):
        for row,srow in zip(a,stored):
            for x,y0 in zip(row,srow):
                for part in ('real','imag'):
                    p = getattr(x,part);q=decode(y0[part])
                    if max(lo(p),lo(q))>min(hi(p),hi(q)):return False
        return True
    check('differentiated_same_symbol_values_match_preserved_enclosures', compatible(values(S), parent['cross_normal_form_matrix_binary']) and compatible(values(B),parent['first_mixed_matrix_binary']))
    sv = decode(parent['values_binary']['S_norm_bound'])
    smax = iv.mpf(hi(sv))
    check('global_periodic_T_is_invertible_without_cutoff', hi(smax)<1)
    F = mm(S,A);H=mm(S,B)
    Fz, Fzz = pm(20,20),pm(20,20)
    for i in (9,11):
        Fz[i][18]=Pair(iv.mpc(0,fg.c[1]));Fzz[i][18]=Pair(iv.mpc(0,2*fg.c[2]))
    check('special_F_derivative_matches_first_spatial_product', all(contains((F[i][j].z-Fz[i][j].v).real) and contains((F[i][j].z-Fz[i][j].v).imag) for i in range(20) for j in range(20)))
    # Exact second F derivative uses only the analytic regulator metric row.
    Sz = pairmat(derivs(S),[[iv.mpf(0)]*20 for _ in range(20)])
    Rmul = ma(ma(ms(Fz,ii),ms(mm(A,Sz),ii)),ma(H,mm(BD,S),-1))
    rpre = iv.mpf(norm2(values(Rmul)))+2*iv.mpf(norm2(values(Fz)))+iv.mpf(norm2(values(Fzz)))+iv.mpf(norm2(values(H)))+iv.mpf(norm2(derivs(H)))+iv.mpf(norm2(values(BD)))*smax
    inverse = 1/(1-smax)
    rglobal = rpre*inverse
    emin0 = decode(ordinary['ordinary_norm_constants']['energy_lower_binary'])
    emax0 = decode(ordinary['ordinary_norm_constants']['energy_upper_binary'])
    fast_min = min(lo(old['d']/old['kappa']),lo(old['aphi']))
    fast_max = max(hi(old['d']/old['kappa']),hi(old['aphi']))
    emin = iv.mpf(min(lo(emin0),fast_min))*(1-smax)**2
    emax = iv.mpf(max(hi(emax0),fast_max))*(1+smax)**2
    check('periodic_full_L2_energy_equivalence_positive_finite', lo(emin)>0 and mp.isfinite(hi(emax)))
    check('actual_variable_principal_composition_remainder_finite', mp.isfinite(hi(rglobal)))

    # Ordinary energy derivative from the same complement and zero charge.
    qkeep=[0,1,2,3,5,6,7]
    XC,PC=pm(9,16),pm(9,16)
    for j,slot in enumerate(qkeep):
        for i in range(9):XC[i][j]=Pair(int(old['E'][i,slot]))
    for i in range(9):PC[i][7+i]=Pair(1)
    XC[0][12]=XC[2][12]=ii*c
    KC=ma(PC,ms(mm(BP,XC),ii),-1)
    VC=mm(MI,KC);PDC=ma(ms(mm(pt(BP),VC),-ii),mm(GP,XC));QDC=mm(R,VC)
    bc=[[ii*t/(2*c) for t in VC[5]]]
    CC=[QDC[i] for i in qkeep]+[[PDC[i][j]-(bc[0][j] if i in (0,2) else 0) for j in range(16)] for i in range(9)]
    HC=ma(mm(mm(dag(KC),MI),KC),mm(mm(dag(XC),GP),XC),-1)
    refM,refB,refG=[sp.Matrix(old['principal'][key])[:9,:9] for key in ('reference_kinetic','reference_mixed','reference_gradient')]
    refX,refP=sp.zeros(9,16),sp.zeros(9,16)
    for j,slot in enumerate(qkeep):refX[:,j]=old['E'][:,slot]
    refP[:,7:]=sp.eye(9);refX[0,12]=refX[2,12]=sp.I
    refK=refP-sp.I*refB*refX
    refH=(refK.conjugate().T*refM.inv()*refK-refX.conjugate().T*refG*refX).applyfunc(sp.expand)
    refig=refH.eigenvals()
    check('reference_energy_normalization_norm_factor_exact',min(refig)==sp.Rational(4,33) and max(refig)==6)
    cinv = decode(ordinary['bounds']['normalized_complement_inverse_bound_binary'])*iv.sqrt(iv.mpf(99)/2)
    lbound=decode(ordinary['ordinary_norm_constants']['zero_charge_row_norm_upper_binary'])
    lz=(iv.mpf(norm2(derivs(bc)))+lbound*iv.mpf(norm2(derivs(CC))))*cinv
    fn=iv.sqrt(17+3/(4*c.v**2));fnz=iv.sqrt(iv.mpf(3))*iv.mpf(ab(c.z))/(2*iv.mpf(lo(c.v))**2)
    eh=iv.mpf(max(mp.mpf(1),hi(decode(ordinary['bounds']['action_energy_upper_binary']))))
    hcz=iv.mpf(norm2(derivs(HC)))
    hordz=2*fn*fnz*(1+lbound)**2*eh+2*fn**2*(1+lbound)*lz*eh+fn**2*(1+lbound)**2*hcz
    ordinary_spatial = hordz*iv.mpf(norm2(values(O)))+iv.mpf(hi(emax0))*iv.mpf(norm2(derivs(O)))
    HF=[[d/kappa,Pair()],[Pair(),ap]]
    Bdiff=ms(BF,-ii)
    fluxzz=dj.c[0]*apz.z+2*dj.c[1]*apz.v+(2*dj.c[2])*ap.v
    flux2=[[iv.mpf(0),fluxzz],[-fluxzz,iv.mpf(0)]]
    fast_spatial = iv.mpf(norm2([[x-y for x,y in zip(row,drow)] for row,drow in zip(flux2,derivs(mm(pt(Bdiff),HF)))]))
    check('ordinary_and_fast_spatial_energy_adjoint_bounds_finite', mp.isfinite(hi(ordinary_spatial)) and mp.isfinite(hi(fast_spatial)))
    check('all_original_sources_sidecars_and_timestamps_unchanged',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snapshot.items()))
    vals=dict(S_z_norm=iv.mpf(norm2(derivs(S))),B_z_norm=iv.mpf(norm2(derivs(B))),F_z_norm=iv.mpf(norm2(values(Fz))),F_zz_norm=iv.mpf(norm2(values(Fzz))),
              force_mass_second_spatial_derivative=mzz, global_T_norm=1+smax,global_T_inverse_norm=inverse,
              periodic_composition_Rpre_bound=rpre,periodic_composition_remainder_bound=rglobal,
              global_energy_lower=emin,global_energy_upper=emax,ordinary_energy_z_bound=hordz,
              ordinary_spatial_energy_adjoint_bound=ordinary_spatial,fast_spatial_energy_adjoint_bound=fast_spatial)
    cbinary=lambda x:dict(real=binary(x.real),imag=binary(x.imag))
    return dict(kind='RTAU_PERIODIC_PRINCIPAL_COMPOSITION_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,original_source_count=219,values_binary={k:binary(v) for k,v in vals.items()},displays={k:[mp.nstr(lo(v),30),mp.nstr(hi(v),30)] for k,v in vals.items()},
                normal_form_spatial_derivative_binary=[[cbinary(x.z) for x in row] for row in S],
                operator_identity='T=I+i*P*S; T*G-Gdiag*T=Rpre; P=D^-1*(I-mean); all finite rank mean terms retained',
                scope='ACTUAL_INITIAL_PERIODIC_COMPOSITION_OF_REGISTERED_PRINCIPAL_OPERATOR_AND_SPATIAL_ENERGY_TERMS_ONLY',
                cutoff_used=False,means_preserved=True,all_modes_and_tails_retained=True,
                full_generator_minus_principal='NOT_BOUNDED',T_dot_H_dot_and_moving_constraints='NOT_DERIVED',full_prepared_coupled_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=parser.parse_args()
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_bytes((json.dumps(dict(error=repr(error),source_sha256=sha(Path(__file__)),physics_pass=False),indent=2)+'\n').encode())
        raise
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('xb') as f:f.write((hashlib.sha256(raw).hexdigest()+'\n').encode())
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    names=('global_T_inverse_norm','periodic_composition_remainder_bound','global_energy_lower','global_energy_upper','ordinary_energy_z_bound','fast_spatial_energy_adjoint_bound')
    print(json.dumps(dict(passed=data['passed'],total=data['total'],failed=[c for c in data['checks'] if not c['passed']],bounds={k:data['displays'][k] for k in names},full_energy=data['full_prepared_coupled_energy']),indent=2))
    return 0 if data['passed']==data['total'] else 1


if __name__=='__main__':raise SystemExit(main())
