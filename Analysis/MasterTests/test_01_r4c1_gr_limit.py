"""R4C1-G1: test GR implications, not just a vanishing source label.

Derives static response and physical transverse mode from the action, then
audits a preregistered classical endpoint family and canonical coefficients.
No claim of full interacting stability or an all-path GR no-go is made.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
import sympy as s

import test_01_r4c1_interacting_background as bg
from test_01_r4c1_full_variation import frame_blocks, connection_tensor, matadd, scale

ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':
        '81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
    'Theory/Gates/RES-001/RES001_R4C1_GR_LIMIT_CONTRACT_2026-09-25.md':
        'bd403fe7f2ec1df70a58552f357c2e27d07c0d26797d39a9569178ca5992c580',
    'Analysis/MasterTests/test_01_r4c1_full_variation.py':
        'aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':
        '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
}
OUT = ROOT/'Analysis/MasterTests/outputs/test_01_r4c1_gr_limit_summary.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self):
        self.checks = []

    def exact(self,name,value,nonzero=False):
        value = s.simplify(value)
        passed = value.is_zero is False if nonzero else value == 0
        self.checks.append(dict(name=name,passed=bool(passed),residual=str(value),
                               expected='nonzero_exact' if nonzero else 'zero_exact'))

    def numeric(self,name,passed,value,criterion):
        self.checks.append(dict(name=name,passed=bool(passed),value=value,criterion=criterion))


def geometry(g,coords):
    gi = g.inv()
    G = [[[s.simplify(sum(gi[c,d]*(s.diff(g[d,b],coords[a])+s.diff(g[d,a],coords[b])
                      -s.diff(g[a,b],coords[d]))/2 for d in range(4)))
           for b in range(4)] for a in range(4)] for c in range(4)]
    return gi,G


def coefficients():
    return {k:s.Symbol(k,real=True) for k in ('M','c1','c2','c3','c4','K','A','b','zz')}


def static_response(audit):
    t,x,y,z,epsilon = s.symbols('t x y z epsilon',real=True)
    coords = (t,x,y,z)
    f,h = s.Function('phi',real=True)(x),s.Function('chi',real=True)(x)
    g = s.diag(-s.exp(2*epsilon*f),*[s.exp(-2*epsilon*h)]*3)
    gi,G = geometry(g,coords)
    U = [s.exp(-epsilon*f),s.Integer(0),s.Integer(0),s.Integer(0)]
    V = [[s.simplify(s.diff(U[b],coords[a])+sum(G[b][a][c]*U[c] for c in range(4)))
          for b in range(4)] for a in range(4)]
    c = coefficients()
    M,c1,c3,c4 = [c[k] for k in ('M','c1','c3','c4')]
    lam = s.Symbol('lambda_U',real=True)
    block = frame_blocks(g.tolist(),gi.tolist(),U,V,[0]*4,[0]*4,[0]*4,s.Integer(0),lam,c)
    P = block['P']
    EU = [s.simplify(block['F'][b]-sum(s.diff(P[a][b],coords[a])+sum(
        G[a][a][cc]*P[cc][b]-G[cc][a][b]*P[a][cc] for cc in range(4)) for a in range(4))) for b in range(4)]
    lam_sol = s.solve(EU[0],lam)[0]
    CC = connection_tensor(U,P,gi.tolist())
    divCC = [[sum(s.diff(CC[a][m][n],coords[a])+sum(G[a][a][cc]*CC[cc][m][n]
        +G[m][a][cc]*CC[a][cc][n]+G[n][a][cc]*CC[a][m][cc] for cc in range(4))
        for a in range(4)) for n in range(4)] for m in range(4)]
    TU = matadd(scale(block['Ls'][0],gi.tolist()),block['B2s'][0],scale(-1,divCC))
    linear = lambda expr:s.simplify(s.diff(expr.subs(lam,lam_sol),epsilon).subs(epsilon,0))
    TU1 = [[linear(TU[i][j]) for j in range(4)] for i in range(4)]
    audit.exact('static_frame_time_equation',EU[0].subs(lam,lam_sol))
    for i in range(1,4):
        audit.exact(f'static_frame_spatial_equation_{i}',EU[i])
        audit.exact(f'static_frame_spatial_stress_linear_{i}',TU1[i][i])
    audit.exact('static_frame_energy_linear',TU1[0][0]-M*(c1+c4)*s.diff(f,x,2))
    Ric = s.Matrix(4,4,lambda m,n:s.simplify(sum(
        s.diff(G[a][m][n],coords[a])-s.diff(G[a][m][a],coords[n])
        +sum(G[a][a][cc]*G[cc][m][n]-G[a][n][cc]*G[cc][m][a] for cc in range(4)) for a in range(4))))
    R = s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
    Ein = Ric-g*R/2
    E00,E22 = [s.simplify(s.diff(Ein[i,i],epsilon).subs(epsilon,0)) for i in (0,2)]
    audit.exact('Einstein_00_linear',E00-2*s.diff(h,x,2))
    audit.exact('Einstein_transverse_linear',E22-s.diff(f-h,x,2))
    MP,rho = s.symbols('MP2 rho',positive=True)
    # Independent ADM spatial-curvature reduction and boundary check.
    R3 = s.simplify(R.subs(f,0).doit())
    audit.exact('conformal_spatial_curvature',R3-s.exp(2*epsilon*h)*(
        4*epsilon*s.diff(h,x,2)-2*epsilon**2*s.diff(h,x)**2))
    rawEH = MP*s.exp(epsilon*(f-3*h))*R3/2
    EH2 = s.simplify(s.diff(rawEH,epsilon,2).subs(epsilon,0)/2)
    boundary = s.diff(2*MP*(f-h)*s.diff(h,x),x)
    reducedEH = MP*(s.diff(h,x)**2-2*s.diff(f,x)*s.diff(h,x))
    audit.exact('static_EH_boundary_reduction',EH2-boundary-reducedEH)
    reducedU = M*(c1+c4)*s.diff(f,x)**2/2
    fullU2 = s.simplify(s.diff(s.sqrt(-g.det())*block['Ls'][0],epsilon,2).subs(epsilon,0)/2)
    audit.exact('static_frame_action_reduction',fullU2-reducedU)
    L2 = reducedEH+reducedU-rho*f
    Ef = s.diff(L2,f)-s.diff(s.diff(L2,s.diff(f,x)),x)
    Eh = s.diff(L2,h)-s.diff(s.diff(L2,s.diff(h,x)),x)
    audit.exact('static_lapse_matches_full_tensor',Ef-(MP*E00-TU1[0][0]-rho))
    audit.exact('static_spatial_matches_full_tensor',Eh-2*MP*E22)
    return {'Newtonian_equation':'(2 M_P^2-M_U^2 c14) Laplacian phi = rho; chi=phi on nonzero modes',
            'G_static':'1/[8 pi M_P^2 (1-alpha14/2)]',
            'G_cos':'1/[8 pi M_P^2 (1+(alpha13+3alpha2)/2)]',
            'domain':'zero-scalar, zero-exchange frame-metric linear response; nonzero Fourier/local quasistatic modes',
            'not_claimed':'global isolated positive mass on empty T3, static dust equilibrium, or full PPN metric'}


def transverse_reduction(audit):
    t,x,y,z,e = s.symbols('t x y z epsilon',real=True)
    coords = (t,x,y,z)
    B,W = s.Function('B',real=True)(t,x),s.Function('w',real=True)(t,x)
    g = s.diag(-1+e*e*B*B,1,1,1)
    g[0,2] = g[2,0] = e*B
    gi,G = geometry(g,coords)
    u0 = s.sqrt(1+e*e*W*W)
    U = s.Matrix([u0,0,e*W-e*B*u0,0])
    audit.exact('transverse_exact_unit_constraint',(U.T*g*U)[0]+1)
    V1 = [[s.simplify(s.diff(s.diff(U[b],coords[a])+sum(G[b][a][c]*U[c] for c in range(4)),e).subs(e,0))
           for b in range(4)] for a in range(4)]
    eta = s.diag(-1,1,1,1).tolist()
    coeff = coefficients()
    M,c1,c2,c3,c4 = [coeff[k] for k in ('M','c1','c2','c3','c4')]
    MP = s.Symbol('MP2',positive=True)
    blocks = frame_blocks(eta,eta,[s.Integer(1),0,0,0],V1,[0]*4,[0]*4,[0]*4,s.Integer(0),s.Integer(0),coeff)
    # Flat spatial metric, N=1: EH ADM term is MP2/2 (Kij Kij-K^2).
    shift = [s.Integer(0),B,s.Integer(0)]
    KK = s.Matrix(3,3,lambda i,j:-(s.diff(shift[j],coords[i+1])+s.diff(shift[i],coords[j+1]))/2)
    LEH = MP*(sum(k*k for k in KK)-s.trace(KK)**2)/2
    wd,wx,bx = s.symbols('w_dot w_x B_x',real=True)
    L2 = s.simplify((blocks['Ls'][0]+LEH).subs({s.diff(W,t):wd,s.diff(W,x):wx,s.diff(B,x):bx}))
    expected = M*(c1+c4)*wd**2/2-M*c1*wx**2/2+M*(c1+c3)*wx*bx/2+(MP-M*(c1+c3))*bx**2/4
    audit.exact('transverse_action_from_covariant_frame_and_EH',L2-expected)
    shift_solution = s.solve(s.diff(L2,bx),bx)[0]
    reduced = s.simplify(L2.subs(bx,shift_solution))
    KT = s.simplify(s.diff(reduced,wd,2))
    GT = s.simplify(-s.diff(reduced,wx,2))
    audit.exact('physical_transverse_kinetic',KT-M*(c1+c4))
    audit.exact('physical_transverse_gradient',GT-(M*c1+M**2*(c1+c3)**2/(2*(MP-M*(c1+c3)))))
    aa1,aa3,aa14 = M*c1/MP,M*c3/MP,M*(c1+c4)/MP
    literature_speed = (aa1-aa1**2/2+aa3**2/2)/(aa14*(1-aa1-aa3))
    audit.exact('derived_transverse_speed_matches_normalized_literature',GT/KT-literature_speed)
    return {'quadratic_action':str(L2),'shift_gradient_solution':str(shift_solution),
            'K_transverse':str(KT),'G_transverse':str(GT),
            'scope':'physical transverse mode after eliminating metric shift; zero-scalar Minkowski control, k!=0',
            'holds':'zero Fourier mode and scalar sector not reduced; not B1 interacting stability'}


def exact_limits(audit):
    eta = s.Symbol('eta',positive=True)
    M = 2*eta/3
    c1,c2,c3,c4 = s.Rational(1,5),s.Rational(1,10),-s.Rational(1,5),s.Rational(1,20)
    a13,a14,act = M*(c1+c3),M*(c1+c4),M*(c1+3*c2+c3)
    gs,gc = 1/(1-a14/2),1/(1+act/2)
    ratio = s.factor(gc/gs)
    audit.exact('B1_static_over_bare',gs.subs(eta,1)-s.Rational(12,11))
    audit.exact('B1_cosmological_over_bare',gc.subs(eta,1)-s.Rational(10,11))
    audit.exact('B1_cosmological_over_static',ratio.subs(eta,1)-s.Rational(5,6))
    audit.exact('zero_exchange_equals_GR_rejected',ratio.subs(eta,1)-1,True)
    audit.exact('luminal_tensor_still_not_GR',1/(1-a13)-1)
    audit.exact('couplings_approach_common_GR_value',s.limit(ratio,eta,0)-1)
    bare_ratio = (1-(c1+c4)/2)/(1+(c1+3*c2+c3)/2)
    audit.exact('bare_ci_normalization_error_rejected',bare_ratio-ratio.subs(eta,1),True)
    KT = s.factor(M*(c1+c4))
    cv2 = s.factor(c1/(c1+c4))
    audit.exact('physical_mode_K_eta',KT-eta/6)
    audit.exact('physical_mode_speed_finite',cv2-s.Rational(4,5))
    audit.exact('physical_mode_endpoint_rank_drop',s.limit(KT,eta,0))
    # Compare the limit itself: infinity-infinity is not a zero residual.
    audit.numeric('canonical_frame_inverse_unbounded',s.limit(1/s.sqrt(KT),eta,0)==s.oo,
                  str(s.limit(1/s.sqrt(KT),eta,0)),'+infinity')
    K,A,b,beta = 3*eta,2*eta/7,5*eta/11,2*eta**2/5
    cubic = s.factor(A/K**s.Rational(3,2))
    audit.numeric('canonical_force_cubic_nonuniform',s.limit(cubic,eta,0)==s.oo,str(cubic),'diverges as eta^(-1/2)')
    audit.exact('canonical_force_regulator_ratio',b/K-s.Rational(5,33))
    audit.exact('canonical_matter_coupling_decouples',s.limit(beta/s.sqrt(K),eta,0))
    u,v,ud,vd,m = s.symbols('u v ud vd m',real=True)
    density = u*vd-v*ud
    energy = (ud*ud+vd*vd+m*m*(u*u+v*v))/2
    for sign in (-1,1):
        squares = (ud+sign*m*v)**2+(vd-sign*m*u)**2
        audit.exact(f'charge_energy_bound_square_{sign}',squares-2*(energy-sign*m*density))
    return {'G_static_over_G_bare':str(gs),'G_cos_over_G_bare':str(gc),'G_cos_over_G_static':str(ratio),
            'B1_G_cos_over_G_static':'5/6','K_T':str(KT),'c_vector_squared':str(cv2),
            'canonical_force_cubic':str(cubic),'canonical_force_regulator':str(s.factor(b/K)),
            'canonical_matter_coupling':str(s.factor(beta/s.sqrt(K))),
            'charge_bound':'rho_Phi >= m |N_charge|/a^3 on homogeneous positive-potential branch',
            'zero_exchange_GR_implication':'REJECTED_FOR_RETAINED_B1_FRAME',
            'healthy_perturbative_limit':'NOT_ESTABLISHED_NONUNIFORM_REGISTERED_PATH',
            'all_paths_no_go':False,'physical_scattering_cutoff_derived':False}


def background_family(audit):
    grid = np.linspace(0,4,801)
    hg = np.sqrt(.2/3)
    ag = (1+1.5*hg*grid)**(2/3)
    control = np.array([ag,hg/(1+1.5*hg*grid),.2/ag**3])
    rows = []
    for eta in (1.,.25,.0625,.015625,.00390625,.0009765625):
        p = bg.PARAMS.copy()
        for key in ('MU2','zeta','K','A','b','gr'):
            p[key] *= eta
        p['beta'] *= eta**2
        y0 = bg.initial(p)
        for i in (2,5,6,7):
            y0[i] *= np.sqrt(eta)
        y0[9] *= eta
        y0[1] = np.sqrt(bg.physics(y0,p)['energy']/(3*bg.effective_mass(p)))
        sol = solve_ivp(lambda t,y:bg.rhs(t,y,p),(0.,4.),y0,method='DOP853',rtol=1e-11,atol=1e-13,dense_output=True)
        yy = sol.sol(grid)
        data = bg.physics(yy,p)
        error = float(np.max(np.abs(yy[[0,1,10]]-control)/(1+np.abs(control))))
        driftQ = float(np.max(np.abs(data['charge']-data['charge'][0]))/max(1.,abs(data['charge'][0])))
        driftD = float(np.max(np.abs(data['dust_integral']-data['dust_integral'][0]))/max(1.,abs(data['dust_integral'][0])))
        residual = float(np.max(data['constraint_norm']))
        row = dict(eta=eta,success=bool(sol.success and sol.t[-1]==4),normalized_metric_dust_error=error,
                   max_Friedmann=residual,charge_initial=float(data['charge'][0]),charge_drift=driftQ,dust_drift=driftD,
                   K_T=eta/6,canonical_force_cubic_ratio=eta**-.5)
        rows.append(row)
        audit.numeric(f'family_{eta}_integrated',row['success'],sol.message,'t=4 completed')
        audit.numeric(f'family_{eta}_constraints',max(residual,driftQ,driftD)<1e-8,
                      dict(Friedmann=residual,charge_drift=driftQ,dust_drift=driftD),'<1e-8 each')
        audit.numeric(f'family_{eta}_charge_value',abs(data['charge'][0]-eta)<1e-14,float(data['charge'][0]),'equals eta, not fixed nonzero charge')
    errors = [row['normalized_metric_dust_error'] for row in rows]
    audit.numeric('classical_background_converges_monotonically',all(b<a for a,b in zip(errors,errors[1:])),errors,'strictly decreasing sampled errors')
    last_ratio = errors[-2]/errors[-1]
    audit.numeric('classical_background_asymptotic_refinement',2<last_ratio<6,last_ratio,'2<ratio<6 for factor-four eta step')
    return rows


def main():
    for name,expected in PINS.items():
        if sha(ROOT/name)!=expected:
            raise RuntimeError(f'FROZEN_INPUT_HASH_MISMATCH: {name}')
    audit = Audit()
    static = static_response(audit)
    print('Direct static tensor and action response derived',flush=True)
    transverse = transverse_reduction(audit)
    print('Metric-shift-reduced transverse action derived',flush=True)
    limits = exact_limits(audit)
    family = background_family(audit)
    passed = sum(item['passed'] for item in audit.checks)
    record = dict(candidate='R4C1-v1',control='R4C1-G1',validation='PASS' if passed==len(audit.checks) else 'FAIL',
        passed=passed,total=len(audit.checks),checks=audit.checks,static_response=static,transverse=transverse,
        limits=limits,background_family=family,source_sha256=PINS,script_sha256=sha(Path(__file__)),
        status='ZERO_EXCHANGE_GR_IMPLICATION_REJECTED_CLASSICAL_ENDPOINT_PERTURBATIVE_HOLD',
        scope='conditional frame-metric controls and registered family; not full B1 stability or all-path no-go',
        healthy_continuous_GR_limit_verified=False,physical_B1_Hessian_verified=False,
        canonical_Test1_pass=False,physics_pass=False,gate_effect='NONE',Rule9='NOT_CLEARED')
    record.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','K_Q':'NOT_DERIVED','V':'NOT_COMPUTED','Stage4A':'CLOSED'})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    OUT.with_suffix(OUT.suffix+'.sha256').write_text(f'{sha(OUT)}  {OUT.name}\n',encoding='ascii')
    print(json.dumps({key:record[key] for key in ('validation','passed','total','status','physics_pass')}))
    print(json.dumps({'limits':limits,'background_family':family}))
    for check in audit.checks:
        if not check['passed']:
            print(json.dumps(check))
    return 0 if passed==len(audit.checks) else 1


if __name__=='__main__':
    raise SystemExit(main())
