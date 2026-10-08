"""G3V: coupled transverse ADM constraint and vertex-regularity diagnostic.

Unchanged R4C1 action and archived G3 backgrounds; no full quartic constraint
solution, finite-density scattering amplitude or physical EFT cutoff claimed.
Outputs refuse existing directories. Replay recomputes without writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Analysis/MasterTests/outputs"
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_CONTRACT_2026-10-08.md":
        "53940518eeff7ca46fb5a9373db6e4637360eeedaeffcba6044af5cc580ac3ac",
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md":
        "1b9fbc4185b61d1e37d7865baa811994e235523eb9ecc22432c733b4bc38aa04",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md":
        "0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b",
    "Theory/Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_REPORT_2026-10-08.md":
        "035d1480904b2459b6a4e8b6df91d381065a653fdeb49583fcdb3dbfc4ac49f4",
    "Analysis/MasterTests/outputs/r4c1_g3i_attempt_01/summary.json":
        "0d85d136e7c7a3c4cd4b49d984f70d3bfdbdd70aed82b3fc423181028aa1d9c7",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json":
        "930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy":
        "b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506",
    "Analysis/MasterTests/outputs/r4c1_g3_fd_attempt_01/summary.json":
        "00ceee7e06cca286baab567e169373ce2b5d1b8ec057f5a7fd5746d6c6748c98",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md":
        "c2a5c82f285dc04adcfffed4ba5c562661ddca98c4d045802ffb6e88bfeefd68",
}
ETAS = (1., .25, .0625, .015625, .00390625, .0009765625)
TIMES = (0., .5, 1., 2., 3., 4.)
WAVENUMBERS = (20., 40., 80.)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encode(data):
    return (json.dumps(data, indent=2, allow_nan=False) + "\n").encode("utf-8")

def tidy(expr):
    if isinstance(expr, s.MatrixBase):
        return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))

def verify(pins):
    for name, digest in pins.items():
        path = ROOT / name
        if sha(path.read_bytes()) != digest:
            raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: " + name)
        sidecar = path.with_name(path.name + ".sha256")
        if sidecar.exists() and sidecar.read_text(encoding="ascii").split()[0] != digest:
            raise RuntimeError("SIDECAR_HASH_MISMATCH: " + name)

class Audit:
    def __init__(self):
        self.checks = []
    def test(self, name, passed, value=None, criterion=None):
        self.checks.append(dict(name=name, passed=bool(passed), value=value, criterion=criterion))
    def exact(self, name, expr):
        values = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
        values = [tidy(v) for v in values]
        self.test(name, all(v == 0 for v in values),
                  "zero_exact" if all(v == 0 for v in values) else list(map(str, values)), "zero_exact")

def derive(audit):
    ep = s.Symbol("epsilon", real=True)
    a, N, MU2, MP2 = s.symbols("a N MU2 MP2", positive=True)
    H, Nd, w, wd, wz, B, Bd, Bz = s.symbols("H Ndot w wdot wz B Bdot Bz", real=True)
    p, pd, J, K, A, b, zeta = s.symbols("psidot psiddot J0 K_Q A b zeta", real=True)
    cs = s.symbols("c1 c2 c3 c4", real=True)
    c1, c2, c3, c4 = cs
    jets = (a, H, N, Nd, w, wd, wz, B, Bd, Bz, p, pd)
    def dt(expr):
        return (s.diff(expr,a)*a*H+s.diff(expr,N)*Nd+s.diff(expr,w)*wd+
                s.diff(expr,B)*Bd+s.diff(expr,p)*pd)
    def dz(expr):
        return s.diff(expr,w)*wz+s.diff(expr,B)*Bz
    sigma = s.sqrt(1+ep**2*w**2)
    g = s.diag(-N**2+ep**2*B**2, a**2, a**2, a**2)
    g[0,2] = g[2,0] = a*ep*B
    gi = tidy(g.inv())
    U = s.Matrix([sigma/N,0,ep*(w-B*sigma/N)/a,0])
    dg = [g.applyfunc(dt),s.zeros(4),s.zeros(4),g.applyfunc(dz)]
    gamma = [[[tidy(sum(gi[c,d]*(dg[i][d,j]+dg[j][d,i]-dg[d][i,j])
                        for d in range(4))/2) for j in range(4)]
              for i in range(4)] for c in range(4)]
    deriv = [U.applyfunc(dt),s.zeros(4,1),s.zeros(4,1),U.applyfunc(dz)]
    F = s.Matrix(4,4,lambda i,j: deriv[i][j]+sum(gamma[j][i][v]*U[v] for v in range(4)))
    h = gi+U*U.T
    audit.exact("future_unit_constraint",(U.T*g*U)[0]+1)
    audit.exact("ADM_volume",g.det()+a**6*N**2)
    audit.exact("projector_idempotence",h*g*h-h)
    audit.exact("projector_orthogonal_to_frame",h*g*U)
    audit.exact("Y_exact_shift_independence",h[0,0]*p**2-ep**2*p**2*w**2/N**2)
    def coeff(expr,n):
        return tidy(s.diff(expr,ep,n).subs(ep,0)/s.factorial(n))
    def trunc(matrix):
        return matrix.applyfunc(lambda x: sum(coeff(x,n)*ep**n for n in range(3)))
    # Background derivatives are nonzero: F0,F1,F2 and metric terms are retained.
    Ft,gt,git,Ut = map(trunc,(F,g,gi,U))
    acc = Ft.T*Ut
    invs = [s.trace(git*Ft*gt*Ft.T),s.trace(Ft)**2,s.trace(Ft*Ft),(acc.T*gt*acc)[0]]
    I0,I1,I2 = [[coeff(v,n) for v in invs] for n in range(3)]
    for i in range(4):
        audit.exact(f"spin1_linear_invariant_zero_{i+1}",I1[i])
    frame2N = tidy(-MU2*(c1*I2[0]+c2*I2[1]+c3*I2[2]-c4*I2[3])/2)
    audit.exact("frame_no_lapse_velocity",s.diff(frame2N,Nd))
    audit.exact("frame_no_shift_velocity",s.diff(frame2N,Bd))
    frame2 = tidy(frame2N.subs(N,1))
    # Direct EH/GHY ADM extrinsic-curvature contraction.
    gamma3 = a**2*s.eye(3)
    shiftcov = s.Matrix([0,a*ep*B,0])
    Kij = s.Matrix(3,3,lambda i,j:(2*H*gamma3[i,j]-
        (s.diff(shiftcov[j],B)*Bz if i==2 else 0)-
        (s.diff(shiftcov[i],B)*Bz if j==2 else 0))/(2*N))
    mixed = gamma3.inv()*Kij
    eh2 = coeff(MP2*(s.trace(mixed*mixed)-s.trace(mixed)**2)/2,2).subs(N,1)
    audit.exact("EH_shift_gradient",eh2-MP2*Bz**2/(4*a**2))
    taud,C,epsm,alpha,ud,vd,rd = s.symbols("taud C eps_m alpha ud vd rd",real=True)
    dust = -epsm*(C**2*gi[0,0]*taud**2+C**4)/2
    scalars = -gi[0,0]*(ud**2+vd**2+rd**2)/2
    audit.exact("dust_no_transverse_shift_source",s.diff(dust,B))
    audit.exact("minimal_scalars_no_transverse_shift_source",s.diff(scalars,B))
    dust_eq = C**2*gi[0,0]*taud**2+C**4
    alpha_eq = tidy(s.diff(dust_eq.subs({taud:C,N:1+ep*alpha}),ep).subs(ep,0))
    audit.exact("dust_linear_constraint_fixes_lapse",alpha_eq-2*C**4*alpha)
    force2 = coeff(K*(U[0]*p)**2/2,2).subs(N,1)
    align2 = coeff(-zeta*h[0,0]*J**2/2,2).subs(N,1)
    audit.exact("force_quadratic_mass",force2-K*p**2*w**2/2)
    audit.exact("alignment_quadratic_mass",align2+zeta*J**2*w**2/2)
    theta = s.trace(F)
    Hess = s.Matrix(4,4,lambda i,j:(pd if i==j==0 else 0)-gamma[0][i][j]*p)
    Delta = tidy(sum(h[i,j]*Hess[i,j] for i in range(4) for j in range(4))+theta*U[0]*p)
    Ds = [coeff(Delta,n) for n in range(3)]
    audit.exact("Delta_background_zero",Ds[0])
    audit.exact("Delta_linear_spin1_zero",Ds[1])
    audit.exact("Delta_second_order",Ds[2]-(p*w*wd+(pd+(2*H-Nd/N)*p)*w**2)/N**2)
    zz = s.Symbol("z_aux",real=True)
    auxiliary = b*zz**2/2+b*zz*Delta
    audit.exact("auxiliary_bulk_equation",s.diff(auxiliary,zz)-b*(zz+Delta))
    reg4 = tidy(-b*Ds[2].subs({N:1,Nd:0})**2/2)
    audit.exact("regulator_no_quadratic_spin1",coeff(-b*Delta**2/2,2))
    audit.exact("regulator_induced_direct_quartic",coeff(-b*Delta**2/2,4).subs({N:1,Nd:0})-reg4)
    L2 = tidy(frame2+eh2+force2+align2)
    seq = tidy(s.diff(L2,Bz))
    sden = tidy(s.diff(seq,Bz))
    ssol = tidy(s.solve(seq,Bz)[0])
    reduced = tidy(L2.subs(Bz,ssol))
    f2,G = tidy(s.diff(reduced,wd,2)),tidy(-a**2*s.diff(reduced,wz,2))
    cross,raw_w2 = tidy(s.diff(reduced,w,wd)),tidy(s.diff(reduced,w,2))
    audit.exact("shift_rank",sden-(MP2-MU2*(c1+c3))/(2*a**2))
    audit.exact("physical_vector_kinetic",f2-MU2*(c1+c4))
    audit.exact("physical_vector_gradient",G-(MU2*c1+MU2**2*(c1+c3)**2/(2*(MP2-MU2*(c1+c3)))))
    audit.exact("quadratic_decomposition",reduced-(f2*wd**2/2+cross*w*wd+raw_w2*w**2/2-G*wz**2/(2*a**2)))
    audit.exact("G1_flat_zero_background_control",reduced.subs({H:0,p:0,J:0})-(f2*wd**2/2-G*wz**2/(2*a**2)))
    Hd = s.Symbol("Hdot",real=True)
    mass_w = tidy((s.diff(cross,H)*Hd+3*H*cross-raw_w2)/f2)
    mass_X = tidy(mass_w-s.Rational(3,2)*Hd-s.Rational(9,4)*H**2)
    wdd,wzz,pdflow,Jd = s.symbols("wddot wzz psiddot_flow Jdot",real=True)
    density = a**3*reduced
    momentum = s.diff(density,wd)
    momentum_dot = (s.diff(momentum,a)*a*H+s.diff(momentum,H)*Hd+
                    s.diff(momentum,w)*wd+s.diff(momentum,wd)*wdd+
                    s.diff(momentum,p)*pdflow+s.diff(momentum,J)*Jd)
    direct_eom = tidy((momentum_dot-s.diff(density,w)+s.diff(density,wz,wz)*wzz)/a**3)
    audit.exact("direct_variational_tilt_equation",direct_eom-
                (f2*wdd+3*H*f2*wd+f2*mass_w*w-G*wzz/a**2))
    eta = s.Symbol("eta",positive=True)
    g3 = {MU2:2*eta*MP2/3,c1:s.Rational(1,5),c2:-s.Rational(7,48),
          c3:-s.Rational(1,80),c4:s.Rational(1,20)}
    audit.exact("G3_scale",f2.subs(g3)-eta*MP2/6)
    audit.exact("G3_speed_control",(G/f2).subs(g3)-(s.Rational(4,5)+3*eta/(8*(8-eta))))
    audit.exact("G3_mass_from_complete_background_flow",mass_w.subs(g3)-
                (2*H**2+2*Hd+(zeta*J**2-K*p**2)/(eta*MP2/6)))
    f,rpos = s.symbols("f r_positive",positive=True)
    avg = s.integrate(s.cos(rpos)**3,(rpos,0,s.pi/2))*2/s.pi
    audit.exact("mean_abs_cos_cubed",avg-4/(3*s.pi))
    cw = a**3*A*s.Abs(p)**3*avg
    cV,cX = tidy(cw/f**3),tidy(cw/(a**s.Rational(9,2)*f**3))
    dimensions = {a:0,N:0,ep:0,w:0,B:0,cs[0]:0,cs[1]:0,cs[2]:0,cs[3]:0,
                  MU2:2,MP2:2,H:1,Nd:1,wd:1,wz:1,Bd:1,Bz:1,p:1,pd:2,J:3,
                  K:2,A:1,b:0,zeta:-2,Hd:2,f:1}
    def dimension(expr):
        if expr.is_number:
            return s.Integer(0)
        if expr in dimensions:
            return s.Integer(dimensions[expr])
        if expr.func == s.Abs:
            return dimension(expr.args[0])
        if expr.is_Mul:
            return sum(dimension(arg) for arg in expr.args)
        if expr.is_Pow and expr.exp.is_number:
            return dimension(expr.base)*expr.exp
        if expr.is_Add:
            dims = [dimension(arg) for arg in expr.args]
            if len(set(dims)) != 1:
                raise ValueError("INCONSISTENT_DIMENSION: "+str(expr))
            return dims[0]
        raise ValueError("UNKNOWN_DIMENSION: "+str(expr))
    for name,expr,expected in (("L2",L2,4),("f2",f2,2),("G",G,2),
            ("cross",cross,3),("raw_mass",raw_w2,4),("mass_w",mass_w,2),
            ("mass_X",mass_X,2),("Delta2",Ds[2],2),("reg4",reg4,4),("cusp_X",cX,1)):
        audit.test("mass_dimension_"+name,dimension(expr)==expected,int(dimension(expr)),str(expected))
    right,left = s.diff(-cw*rpos**3,rpos,3),s.diff(cw*rpos**3,rpos,3)
    audit.exact("third_right",right+6*cw)
    audit.exact("third_left",left-6*cw)
    audit.exact("A_zero_control",cw.subs(A,0))
    audit.exact("psidot_zero_transverse_control",cw.subs(p,0))
    grad = s.Symbol("force_gradient",positive=True)
    audit.test("psidot_zero_force_gradient_cusp_retained",tidy(a**3*A*(grad/a)**3)!=0,
               str(tidy(a**3*A*(grad/a)**3)),"nonzero for A>0, grad>0")
    aux2 = s.Symbol("shift_second_order",real=True)
    audit.exact("stationary_shift_cubic_correction_zero",s.diff(L2,Bz).subs(Bz,ssol)*aux2)
    aq,qq,yy,y2,hh = s.symbols("aux_source q y y2 aux_Hessian",real=True)
    toy = hh*yy**2/2+aq*qq*yy
    correction = s.expand(toy.subs({qq:ep*qq,yy:ep*(-aq*qq/hh)+ep**2*y2})).coeff(ep,3)
    audit.exact("regular_auxiliary_stationarity_identity",correction)
    audit.test("even_degree_three_not_trilinear",right==-left,
               "opposite one-sided thirds; even degree-three functional")
    audit.test("zero_background_mass_shortcut_detected",tidy(reduced-reduced.subs({H:0,p:0,J:0}))!=0)
    audit.test("frozen_shift_shortcut_detected",tidy(G-MU2*c1)!=0)
    audit.test("omitted_force_mass_detected",force2!=0)
    audit.test("omitted_alignment_mass_detected",align2!=0)
    formulas = dict(
        convention="(-+++), spatially flat gauge, pure transverse spin-1, k!=0",
        U0=str(U[0]),Uy=str(U[2]),
        frame_invariants_background=list(map(str,I0)),frame_invariants_order2=list(map(str,I2)),
        frame_quadratic_before_IBP=str(frame2),EH_quadratic=str(eh2),
        force_quadratic=str(force2),alignment_quadratic=str(align2),
        full_quadratic_before_shift=str(L2),shift_equation=str(seq),
        shift_gradient_solution=str(ssol),shift_rank=str(sden),
        reduced_quadratic_before_IBP=str(reduced),kinetic_weight=str(f2),gradient_weight=str(G),
        raw_cross_weight=str(cross),raw_mass_weight=str(raw_w2),
        physical_tilt_mass_squared=str(mass_w),comoving_canonical_mass_squared=str(mass_X),
        tilt_EOM="wddot+3H wdot+(G/f^2*k^2/a^2+mass_w)w=0",
        canonical_EOM="Xddot+(G/f^2*k^2/a^2+mass_X)X=0; X=a^(3/2) f w",
        Y_exact=str(tidy(h[0,0]*p**2)),Delta_exact=str(Delta),Delta_orders=list(map(str,Ds)),
        regulator_direct_quartic=str(reg4),
        force_average_w_coefficient=str(cw),force_average_local_V_coefficient=str(cV),
        force_local_physical_density_coefficient=str(tidy(cV/a**3)),
        force_average_comoving_X_coefficient=str(cX),third_right=str(right),third_left=str(left),
        stationary_elimination_scope="regular first-order constraints; no full J2/J3 or quartic Schur complement",
        dimension=dict(a=0,w=0,epsilon=0,A=1,psidot=1,f=1,V=1,X=1,
                       kinetic_weight=2,mass_squared=2,canonical_cusp_coefficient=1),
        regularity="C2 but not C3 at zero amplitude where A>0 and psidot!=0")
    data = dict(jets=jets,ep=ep,a=a,H=H,N=N,Nd=Nd,w=w,wd=wd,wz=wz,B=B,Bd=Bd,Bz=Bz,
                p=p,pd=pd,J=J,K=K,A=A,b=b,zeta=zeta,MU2=MU2,MP2=MP2,cs=cs,I0=I0,I2=I2,
                f2=f2,G=G,cross=cross,raw_w2=raw_w2,mass_w=mass_w,mass_X=mass_X,Hd=Hd,
                Delta2=Ds[2].subs({N:1,Nd:0}),reduced=reduced)
    return data,formulas

def direct_metric_probe(ep):
    """Independent unexpanded ADM contractions at the frozen diagnostic jet."""
    a,H = mp.mpf(7)/5,mp.mpf(2)/5
    w,B = mp.mpf(3)/10,-mp.mpf(1)/5
    wd,wz,Bd,Bz = -mp.mpf(2)/7,mp.mpf(1)/4,mp.mpf(1)/9,-mp.mpf(1)/6
    p,pd = mp.mpf(1)/8,-mp.mpf(1)/11
    sigma = mp.sqrt(1+ep**2*w**2)
    g = mp.diag([-1+ep**2*B**2,a*a,a*a,a*a])
    g[0,2] = g[2,0] = a*ep*B
    gi = g**-1
    dg = [mp.zeros(4) for _ in range(4)]
    dg[0][0,0] = 2*ep**2*B*Bd
    dg[0][0,2] = dg[0][2,0] = a*ep*(Bd+H*B)
    for i in range(1,4):
        dg[0][i,i] = 2*a*a*H
    dg[3][0,0] = 2*ep**2*B*Bz
    dg[3][0,2] = dg[3][2,0] = a*ep*Bz
    gamma = [[[sum(gi[c,d]*(dg[i][d,j]+dg[j][d,i]-dg[d][i,j]) for d in range(4))/2
               for j in range(4)] for i in range(4)] for c in range(4)]
    U = mp.matrix([sigma,0,ep*(w-B*sigma)/a,0])
    du = mp.zeros(4)
    du[0,0],du[3,0] = ep**2*w*wd/sigma,ep**2*w*wz/sigma
    du[0,2] = ep/a*(wd-Bd*sigma-B*ep**2*w*wd/sigma-H*(w-B*sigma))
    du[3,2] = ep/a*(wz-Bz*sigma-B*ep**2*w*wz/sigma)
    F = mp.matrix(4,4)
    for i in range(4):
        for j in range(4):
            F[i,j] = du[i,j]+sum(gamma[j][i][v]*U[v] for v in range(4))
    tr = lambda m: sum(m[i,i] for i in range(4))
    acc = F.T*U
    invs = [tr(gi*F*g*F.T),tr(F)**2,tr(F*F),(acc.T*g*acc)[0]]
    h = gi+U*U.T
    Hess = mp.matrix(4,4)
    for i in range(4):
        for j in range(4):
            Hess[i,j] = (pd if i==j==0 else 0)-gamma[0][i][j]*p
    delta = sum(h[i,j]*Hess[i,j] for i in range(4) for j in range(4))+tr(F)*U[0]*p
    return dict(invariants=invs,Y=h[0,0]*p*p,Delta=delta,
                projector_error=max(abs(v) for v in h*g*h-h),unit_error=abs((U.T*g*U)[0]+1))

def independent_checks(audit,d):
    with mp.workdps(60):
        R = mp.mpf
        subs = dict(zip(d["jets"],(s.Rational(7,5),s.Rational(2,5),1,0,s.Rational(3,10),
            -s.Rational(2,7),s.Rational(1,4),-s.Rational(1,5),s.Rational(1,9),
            -s.Rational(1,6),s.Rational(1,8),-s.Rational(1,11))))
        expect = [R(str(s.N(v.subs(subs),60))) for v in d["I2"]]
        expect0 = [R(str(s.N(v.subs(subs),60))) for v in d["I0"]]
        delta2 = R(str(s.N(d["Delta2"].subs(subs),60)))
        rows,frame_errors = [],[]
        for hv in ("0.001","0.0005","0.00025"):
            hh = R(hv)
            vals = {n:direct_metric_probe(n*hh) for n in (-3,-2,-1,0,1,2,3)}
            errors = [max(abs((vals[n]["invariants"][j]-expect0[j])/(n*hh)**2-expect[j])/
                (1+abs(expect[j])) for n in (-3,-2,-1,1,2,3)) for j in range(4)]
            frame_errors.append(max(errors))
            proj_error = max(v["projector_error"] for v in vals.values())
            y_error = max(abs(vals[n]["Y"]-(n*hh)**2*(R(1)/8)**2*(R(3)/10)**2) for n in vals)
            delta_error = max(abs(vals[n]["Delta"]/(n*hh)**2-delta2)/(1+abs(delta2)) for n in vals if n)
            forceA = R(2)/7*R(".25")**R("1.5")
            volume = (R(7)/5)**3
            coef = volume*forceA*abs(R(1)/8)**3*abs(R(3)/10)**3
            F = {n:-volume*forceA*vals[n]["Y"]**R("1.5") for n in vals}
            dr = (F[3]-3*F[2]+3*F[1]-F[0])/hh**3
            dl = (F[0]-3*F[-1]+3*F[-2]-F[-3])/hh**3
            er,el = abs(dr/coef+6),abs(dl/coef-6)
            sym = (F[2]-2*F[1]+2*F[-1]-F[-2])/(2*hh**3*coef)
            audit.test(f"jet_h_{hv}_projector_Y",max(proj_error,y_error)<=R("1e-12"),
                       float(max(proj_error,y_error)),"<=1e-12")
            audit.test(f"jet_h_{hv}_unit",max(v["unit_error"] for v in vals.values())<=R("1e-12"))
            audit.test(f"jet_h_{hv}_Delta2",delta_error<=R("1e-12"),float(delta_error))
            audit.test(f"jet_h_{hv}_symmetric_stencil_false_zero",abs(sym)<=R("1e-12"),
                       float(sym),"symmetric odd stencil zero; opposite one-sided thirds")
            rows.append(dict(h=float(hh),frame_order2_errors=list(map(float,errors)),
                projector_error=float(proj_error),Y_error=float(y_error),Delta2_error=float(delta_error),
                third_right_over_coefficient=float(dr/coef),third_left_over_coefficient=float(dl/coef),
                third_right_error=float(er),third_left_error=float(el)))
        audit.test("finest_unexpanded_frame_agreement",frame_errors[-1]<=R("1e-5"),
                   float(frame_errors[-1]),"<=1e-5")
        audit.test("frame_errors_decrease",all(v<u for u,v in zip(frame_errors,frame_errors[1:])) or
                   max(frame_errors)<=R("1e-8"),list(map(float,frame_errors)),"decreasing or all <=1e-8")
        audit.test("finest_right_cusp_agreement",rows[-1]["third_right_error"]<=1e-5)
        audit.test("finest_left_cusp_agreement",rows[-1]["third_left_error"]<=1e-5)
    return rows

def sample_backgrounds(audit,d):
    import test_01_r4c1_interacting_background as bg
    family = json.loads((OUT/"r4c1_g3_attempt_01/summary.json").read_bytes())
    old = np.load(OUT/"r4c1_g3_attempt_01/trajectories.npy",allow_pickle=False)
    refine = json.loads((OUT/"r4c1_g3_fd_attempt_01/summary.json").read_bytes())
    failures = [c for c in family["checks"] if not c["passed"]]
    audit.test("original_G3_failure_preserved",family["passed"]==112 and family["total"]==113 and len(failures)==1,
               failures,"original 801-point derivative failure retained")
    audit.test("independent_G3_refinement_witness",refine["passed"]==refine["total"]==18 and
               not [c for c in refine["checks"] if not c["passed"]])
    audit.test("six_frozen_eta_members",tuple(v["eta"] for v in family["family"])==ETAS)
    audit.test("trajectory_metadata",old.shape==tuple(family["trajectory"]["shape"]) and
               family["trajectory"]["fields"]==["t",*bg.NAMES] and
               tuple(family["trajectory"]["methods"])==("DOP853","Radau"))
    syms = [d[n] for n in ("MU2","MP2")]+list(d["cs"])+[d[n] for n in ("H","Hd","p","J","K","zeta")]
    exprs = [d[n] for n in ("f2","G","mass_w","mass_X","cross","raw_w2")]
    fun = s.lambdify(syms,exprs,"numpy",cse=True)
    rows = []
    for ie,eta in enumerate(ETAS):
        params = family["family"][ie]["parameters"]
        for im,method in enumerate(family["trajectory"]["methods"]):
            run = family["family"][ie]["runs"][method]
            witnesses = {k:run[k] for k in ("max_normalized_Friedmann","max_charge_drift","max_dust_integral_drift")}
            audit.test(f"eta_{eta}_{method}_pinned_onshell_witness",run["success"] and max(witnesses.values())<1e-8,
                       witnesses,"<1e-8 inherited witness")
            for t in TIMES:
                index = int(round(t*200))
                audit.test(f"eta_{eta}_{method}_t_{t}_archived_time",abs(old[ie,im,0,index]-t)<1e-15)
                y = old[ie,im,1:,index]
                aa,H,u,ud,v,vd,rr,rd,psi,psid,rho,tau = map(float,y)
                flow = bg.rhs(t,y,params)
                J0 = v*ud-u*vd
                f2,G,mw,mX,cross,rw2 = map(float,fun(params["MU2"],params["MP2"],params["c1"],params["c2"],
                    params["c3"],params["c4"],H,flow[1],psid,J0,params["K"],params["zeta"]))
                den = params["MP2"]-params["MU2"]*(params["c1"]+params["c3"])
                # Local coefficient is per physical volume: average L=a^3*(-cV |V|^3).
                cV = 4*params["A"]*abs(psid)**3/(3*np.pi*f2**1.5)
                cX = cV/aa**1.5
                audit.test(f"eta_{eta}_{method}_t_{t}_regular_chart",
                           min(aa,H,rho,f2,G,den,params["b"])>0 and np.isfinite([aa,H,rho,f2,G,mw,mX,cV]).all(),
                           dict(a=aa,H=H,rho=rho,f2=f2,G=G,shift_denominator=den))
                audit.test(f"eta_{eta}_{method}_t_{t}_physical_scale",abs(f2-eta/6)<=1e-15,f2,"eta/6, M_P=1")
                audit.test(f"eta_{eta}_{method}_t_{t}_nonzero_cusp",cV>0,cV,"A>0, sampled psidot!=0")
                for k in WAVENUMBERS:
                    rows.append(dict(eta=eta,method=method,t=t,k=k,a=aa,H=H,Hdot=float(flow[1]),
                        psidot=psid,psiddot=float(flow[9]),J0=J0,shift_denominator=den,
                        kinetic_weight=f2,gradient_weight=G,speed_squared=G/f2,
                        raw_cross_weight=cross,raw_mass_weight=rw2,physical_tilt_mass_squared=mw,
                        canonical_mass_squared=mX,canonical_frequency_squared=G/f2*(k/aa)**2+mX,
                        local_physical_density_cusp_coefficient=cV,
                        local_comoving_volume_cusp_coefficient=aa**3*cV,comoving_cusp_coefficient=cX,
                        third_right=-6*cX,third_left=6*cX,regularity="C2_NOT_C3_IN_THIS_DIRECTION"))
    audit.test("all_216_chart_events",len(rows)==216)
    return rows,failures

def evaluate():
    verify(PINS)
    parent = json.loads((OUT/"r4c1_g3i_attempt_01/summary.json").read_bytes())
    inherited = {**parent["source_sha256"],**parent["transitive_source_sha256"]}
    for path,digest in PINS.items():
        if path in inherited and inherited[path]!=digest:
            raise RuntimeError("CONFLICTING_SOURCE_PIN: "+path)
    verify(inherited)
    audit = Audit()
    print("G3V: full-connection transverse ADM blocks...",flush=True)
    data,formulas = derive(audit)
    print("G3V: unexpanded metric checks and pinned background grid...",flush=True)
    jets = independent_checks(audit,data)
    rows,failures = sample_backgrounds(audit,data)
    payloads = {"formulas.json":encode(formulas),"grid.json":encode(dict(chart_events=rows,
        independent_jet_checks=jets,zero_controls=dict(A_zero="cusp absent",
        psidot_zero="transverse cusp absent",psidot_zero_force_gradient="finite-k force-gradient cusp retained")))}
    passed = sum(c["passed"] for c in audit.checks)
    valid = passed==len(audit.checks)
    result = dict(schema="r4c1-g3v-v1",passed=passed,total=len(audit.checks),
        validation="PASS_LOCAL_CHECKS" if valid else "FAIL_LOCAL_CHECKS",
        status="CONDITIONAL_COUPLED_TRANSVERSE_C2_NOT_C3_ORDINARY_TAYLOR_VERTEX_OBSTRUCTION" if valid
               else "G3V_FAILURES_REQUIRE_DISPOSITION",checks=audit.checks,
        source_sha256=PINS,transitive_source_sha256=inherited,script_sha256=sha(Path(__file__).read_bytes()),
        artifacts={name:sha(value) for name,value in payloads.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,
                     mpmath=mp.__version__,independent_probe_digits=60),
        numerical_summary=dict(chart_events=len(rows),
            min_cusp_coefficient=min(r["comoving_cusp_coefficient"] for r in rows),
            max_cusp_coefficient=max(r["comoving_cusp_coefficient"] for r in rows),
            physical_tilt_mass_range=[min(r["physical_tilt_mass_squared"] for r in rows),
                                      max(r["physical_tilt_mass_squared"] for r in rows)],
            independent_jet_checks=jets),inherited_original_failure=failures,
        research_execution="PROCEED_PROVISIONALLY" if valid else "HOLD_VALIDATION",claim_status="Conditional",
        ordinary_cubic_Taylor_vertices_available=False,full_quartic_constraint_reduction_verified=False,
        full_finite_density_scattering_verified=False,physical_EFT_cutoff="NOT_DERIVED",
        full_physical_validity_domain_verified=False,quantum_inconsistency_proved=False,
        classical_evolution_no_go=False,all_actions_no_go=False,dependent_scattering_route="HOLD_SUBSTANTIVE",
        physics_pass=False,gate_effect="NONE",Rule9_cleared=False,review_status="DEFERRED",
        canonical_tests_1_to_3="HOLD_SUBSTANTIVE",MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",
        K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED",TOP_X4="UNCHANGED",
        review_dependencies=["R9-MT1-G3I","R9-MT1-G3DF","R9-MT1-VARIATION","R9-MT1-B1",
            "R9-MT1-G1","R9-MT1-S1","R9-MT1-S2","R9-MT1-S3","R9-MT1-G2","R9-MT1-G3","R9-MT1-G3S",
            "R9-MT1-G3Z","R9-MT1-G3E","R9-MT1-G3A","R9-MT1-G3F","R9-MT1-G3D","PD1","Track-A"])
    return result,payloads

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01")
    parser.add_argument("--replay",action="store_true")
    parser.add_argument("--symbolic-only",action="store_true",help="print diagnostics, no receipts")
    args = parser.parse_args()
    directory = (ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):
        raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    if directory.exists() and not args.replay and not args.symbolic_only:
        raise RuntimeError("REFUSE_EXISTING_OUTPUT_DIRECTORY")
    if args.symbolic_only:
        verify(PINS)
        audit = Audit()
        _,formulas = derive(audit)
        print(json.dumps(formulas,indent=2))
        print(json.dumps([c for c in audit.checks if not c["passed"]],indent=2))
        return 0 if all(c["passed"] for c in audit.checks) else 1
    result,payloads = evaluate()
    payloads["summary.json"] = encode(result)
    if args.replay:
        for name,data in payloads.items():
            if data!=(directory/name).read_bytes():
                raise RuntimeError("REPLAY_BYTE_MISMATCH: "+name)
            if (directory/(name+".sha256")).read_text(encoding="ascii").split()[0]!=sha(data):
                raise RuntimeError("REPLAY_SIDECAR_MISMATCH: "+name)
        print(json.dumps(dict(replay=True,byte_identical=True,summary_sha256=sha(payloads["summary.json"]))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,data in payloads.items():
            (directory/name).write_bytes(data)
            (directory/(name+".sha256")).write_text(sha(data)+"  "+name+"\n",encoding="ascii")
    print(json.dumps({k:result[k] for k in ("validation","passed","total","status","physics_pass")}))
    for check in result["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    return 0 if result["passed"]==result["total"] else 1

if __name__=="__main__":
    raise SystemExit(main())
