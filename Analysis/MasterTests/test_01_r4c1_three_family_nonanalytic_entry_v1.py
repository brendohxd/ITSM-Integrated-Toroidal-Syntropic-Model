"""Three-family constrained nonanalytic entry; NOT full physical-window clearance."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_NONANALYTIC_ENTRY_V1_CONTRACT_2026-10-12.md'
SURVEY = BASE + 'r4c1_gr_family_survey_attempt_01/'
G3 = BASE + 'r4c1_g3_attempt_01/'
GV = BASE + 'r4c1_g3v_attempt_01/'
PINNED = {
    CONTRACT: 'c6bf573ef346815a8ad8c9c5c7724858bde06124bcf1fc1681293ec87910b78a',
    SURVEY+'summary.json': 'a41bd5979cc25b0afcbde50fa195882cc58ee95f8e0472867f63288e52354ecf',
    GV+'formulas.json': '1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358',
    GV+'summary.json': '07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae',
    G3+'summary.json': '930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75',
    'Analysis/MasterTests/test_01_r4c1_gr_family_survey_v2.py': '94361b3545770efdb1c4b3cbcf30e4a9c10064105f19e9dce5cd878239a7ed42',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py': '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Theory/Gates/RES-001/RES001_R4C1_GR_FAMILY_SURVEY_REPORT_2026-10-11.md': 'd8f661dbea107626f2b715f61eb6d88ee6d2c1a8cedd29271b5dd36f8da1979b',
    'Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08.md': '952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27',
    'Theory/Gates/RES-001/RES001_R4C1_G3_VERTEX_REGULARITY_CROSSCHECK_REPORT_2026-10-08.md': '0b35ad651859271e9310b8aeec5a0957805efe35cd05fbece96b498969c22409',
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md': '81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
}


def sha(body):
    return hashlib.sha256(body).hexdigest()


def read(path):
    return json.loads((ROOT/path).read_bytes())


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()


def snapshot(paths):
    return {p.relative_to(ROOT).as_posix(): (sha(p.read_bytes()), p.stat().st_size,
                                          p.stat().st_mtime_ns) for p in paths}


class Checks:
    def __init__(self):
        self.rows = []

    def add(self, name, passed, evidence=None):
        self.rows.append(dict(name=name, passed=bool(passed), evidence=evidence))

    def exact(self, name, expression):
        residual = s.factor(expression)
        self.add(name, residual == 0, str(residual))


def collect_pins():
    for name, digest in PINNED.items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise RuntimeError('Frozen direct-source drift: '+name)
    pins = dict(PINNED)
    for prefix in (SURVEY, GV):
        receipt = read(prefix+'summary.json')
        for name, digest in receipt['source_sha256'].items():
            if name in pins and pins[name] != digest:
                raise RuntimeError('Conflicting inherited pin: '+name)
            pins[name] = digest
        pins.update({prefix+name: digest for name, digest in receipt['artifacts'].items()})
    archived = read(G3+'summary.json')
    pins[G3+'trajectories.npy'] = archived['trajectory']['sha256']
    pins[SELF] = sha((ROOT/SELF).read_bytes())
    for name, digest in pins.items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise RuntimeError('Frozen inherited-source drift: '+name)
    paths = [ROOT/name for name in pins]
    sidecars_absent = []
    for name, digest in pins.items():
        side = Path(str(ROOT/name)+'.sha256')
        if side.exists():
            if side.read_text(encoding='utf-8').split()[0].lower() != digest:
                raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        else:
            sidecars_absent.append(name)
    return pins, paths, sidecars_absent


def exact_formulas(checks):
    eta = s.Symbol('eta', positive=True)
    symbols = {q: s.Symbol(q, real=True) for q in
               ('a H Hdot w w_t w_z B_z MP2 MU2 c1 c2 c3 c4 K_Q zeta J0 psi_dot').split()}
    x = symbols
    f2 = x['MU2']*(x['c1']+x['c4'])
    mt = x['MP2']-x['MU2']*(x['c1']+x['c3'])
    gradient = x['MU2']*x['c1']+x['MU2']**2*(x['c1']+x['c3'])**2/(2*mt)
    inherited = read(GV+'formulas.json')
    # Reuse the checked unspecialized covariant contraction, NOT G3-only matrices.
    density = s.sympify(inherited['constrained_vector_quadratic'], locals=x)
    cross = s.diff(density, x['w'], x['w_t'])
    position = s.diff(density, x['w'], 2)
    checks.exact('generic_covariant_kinetic', s.diff(density, x['w_t'], 2)-f2)
    checks.exact('generic_covariant_metric_gradient', -x['a']**2*s.diff(density, x['w_z'], 2)-gradient)
    mw = s.factor((s.diff(cross, x['H'])*x['Hdot']+3*x['H']*cross-position)/f2)
    mx = s.factor(mw-3*x['Hdot']/2-9*x['H']**2/4)
    checks.exact('generic_inherited_mass_not_replaced', mw-s.sympify(inherited['mass_w'], locals=x))
    common = {x['MP2']: 1, x['MU2']: 2*eta/3, x['c1']: s.Rational(1,5),
              x['c4']: s.Rational(1,20), x['K_Q']: 3*eta, x['zeta']: eta/13}
    choices = {'archived_G3': (-s.Rational(7,48), -s.Rational(1,80)),
               'new_B1_frame': (s.Rational(1,10), -s.Rational(1,5)),
               'new_hierarchical': (s.Rational(1,10), -s.Rational(1,5)+3*eta/16)}
    objects = {}
    for name, (c2, c3) in choices.items():
        values = {**common, x['c2']: c2, x['c3']: c3}
        e = x['c4']-3*x['c2']-x['c3']
        d = x['c4']-2*x['c1']-9*x['c2']-3*x['c3']
        scalar_L = s.factor((x['MU2']*(x['c1']+x['c2']+x['c3'])).subs(values))
        mc = s.factor((x['MP2']+x['MU2']*(x['c1']+3*x['c2']+x['c3'])/2).subs(values))
        objects[name] = {q: s.factor(expr.subs(values)) for q, expr in
                         {'K': f2, 'G': gradient, 'M_tensor2': mt, 'M_cosm2': mc,
                          'alphaL': scalar_L, 'cross': x['MU2']*e*x['H'],
                          'A_no_gradient': x['MU2']*d*x['H']**2+x['K_Q']*x['psi_dot']**2-x['zeta']*x['J0']**2,
                          'm_w2': mw, 'm_X2': mx, 'c_V2': gradient/f2}.items()}
        o = objects[name]
        checks.exact(name+'_interior_K', o['K']-eta/6)
        checks.exact(name+'_rank_loss', s.limit(o['K'], eta, 0))
        checks.add(name+'_necessary_interior_signs',
                   all(o[q].subs(eta, 1)>0 and s.limit(o[q], eta, 0)>=0
                       for q in ('K','G','M_tensor2','M_cosm2','alphaL')),
                   'All denominators explicit; sign proof also exported as positive decomposition.')
    checks.exact('B1_mass_Hdot_coefficient', s.diff(objects['new_B1_frame']['m_X2'], x['Hdot'])+s.Rational(17,10))
    checks.exact('hierarchical_mass_Hdot_coefficient', s.diff(objects['new_hierarchical']['m_X2'], x['Hdot'])+s.Rational(17,10)+3*eta/4)
    checks.exact('G3_mass_Hdot_coefficient', s.diff(objects['archived_G3']['m_X2'], x['Hdot'])-s.Rational(1,2))
    checks.add('reject_G3_only_mass_for_new_families', all(
        s.factor(objects[name]['m_X2']-objects['archived_G3']['m_X2']) != 0
        for name in ('new_B1_frame','new_hierarchical')))
    A, pd, lam = s.symbols('A pd lambda', positive=True)
    checks.exact('canonical_cusp_eta_cancels',
                 (2*eta**s.Rational(3,2)/7)*pd**3/(eta/6)**s.Rational(3,2)-12*s.sqrt(6)*pd**3/7)
    checks.exact('psi_chart_rescaling_cusp_invariant', A/lam**3*(lam*pd)**3-A*pd**3)
    checks.exact('psi_chart_regulator_rescaling_invariant', 5*eta/(11*lam**2)*(lam*pd)**2-5*eta*pd**2/11)
    # The continuous Hessian is NOT an ordinary third-order Taylor vertex.
    q = s.Matrix(s.symbols('q1 q2 q3', real=True)); radius = s.sqrt(q.dot(q))
    potential = A*radius**3; derivative = s.Matrix([s.diff(potential, value) for value in q])
    for i in range(3):
        checks.exact('projected_force_gradient_'+str(i), derivative[i]-3*A*radius*q[i])
    Hq = s.hessian(potential, list(q))
    for i in range(3):
        for j in range(3):
            checks.exact('projected_force_Hessian_'+str(i)+str(j), Hq[i,j]-3*A*(radius*int(i==j)+q[i]*q[j]/radius))
    for i, value in enumerate(Hq*q-6*A*radius*q):
        checks.exact('projected_Hessian_radial_eigenvalue_'+str(i), value)
    tangent = s.Matrix([-q[1], q[0], 0])
    for i, value in enumerate(Hq*tangent-3*A*radius*tangent):
        checks.exact('projected_Hessian_tangent_eigenvalue_'+str(i), value)
    checks.exact('A_zero_force_control', potential.subs(A, 0))
    checks.exact('pd_zero_transverse_only_control', (A*pd**3).subs(pd, 0))
    t, C = s.symbols('epsilon C', real=True)
    checks.exact('right_cusp_third', s.diff(-C*t**3,t,3)+6*C)
    checks.exact('left_cusp_third', s.diff(C*t**3,t,3)-6*C)
    checks.exact('symmetric_odd_difference_rejected', -C*abs(2*t)**3+2*C*abs(t)**3-2*C*abs(-t)**3+C*abs(-2*t)**3)
    forms = {name: {key: str(value) for key, value in obj.items()} for name,obj in objects.items()}
    forms.update(interior_sign_proof={'K':'eta/6>0','G':'2 eta/15+alpha13^2/[2(1-alpha13)]>0',
        'M_tensor2':'1-alpha13 >=7/8','M_cosm2':'G3 1-eta/12 >=11/12; B1 1+eta/10; hierarchical 1+eta/10+eta^2/16',
        'alphaL':'G3 eta/36; B1 eta/15; hierarchical eta/15+eta^2/8'},
        projected_force={'q':'grad(Pi)/a+psi_dot*w','potential':'A*|q|^3',
            'gradient':'3*A*|q|*q','Hessian_q_nonzero':'3*A*(|q|*I+q*q^T/|q|)',
            'Hessian_origin':'0 by continuous extension','Hessian_norm':'6*A*|q|',
            'ball_Lipschitz_constant':'6*A*R for |q|<=R',
            'canonical_q':'grad(phi)/(a*sqrt(K_Q))+psi_dot*V/f, phi=sqrt(K_Q)*Pi,V=f*w',
            'scope':'field-space Lipschitz bound; no spatial PDE, full J2/J3 or quantum theorem'},
        direct_regulator_quartic='-b*(psi_dot*w*w_dot+(psi_ddot+2*H*psi_dot)*w^2)^2/2; NOT full Schur quartic',
        units='M_P=1 reference; f dimension1,C_local dimension1,V dimension1,omega dimension1; no observed scales')
    return objects, symbols, eta, forms


def harmonic_and_lipschitz_controls(checks):
    n = s.Symbol('n', positive=True, integer=True)
    # Quarter-interval product-to-sum integral; for odd n, sin((n+/-2)pi/2)
    # equals -sin(n*pi/2). Reflection gives zero for every even n.
    integral_coefficient = 4/s.pi*(1/(2*n)-(1/(n-2)+1/(n+2))/4)
    checks.exact('all_odd_harmonic_closed_form', integral_coefficient+8/(s.pi*n*(n*n-4)))
    z = s.Symbol('z', real=True)
    checks.exact('exact_full_nonlinear_Parseval_energy', s.integrate(s.cos(z)**4,(z,0,2*s.pi))/(2*s.pi)-s.Rational(3,8))
    coefficients = []
    for n in (1,3,5,7,9):
        exact = -8*(-1)**((n-1)//2)/(np.pi*n*(n*n-4))
        numeric = quad(lambda z: np.cos(z)*abs(np.cos(z))*np.cos(n*z), 0,2*np.pi,
                       points=(np.pi/2,3*np.pi/2), epsabs=1e-12, epsrel=1e-12)[0]/np.pi
        error = abs(exact-numeric)
        checks.add('independent_harmonic_'+str(n), error<=1e-10, error)
        coefficients.append(dict(n=n, coefficient=exact, quadrature=numeric, error=error))
    full = quad(lambda z: np.cos(z)**4,0,2*np.pi,epsabs=1e-12)[0]/(2*np.pi)
    checks.add('independent_Parseval_energy',abs(full-3/8)<=1e-10, full)
    tails = []
    with mp.workdps(80):
        for N in (9,31,127):
            energy = sum((8/(mp.pi*n*(n*n-4)))**2/2 for n in range(1,N+1,2))
            tail = mp.mpf(3)/8-energy
            bound = 128/(5*mp.pi**2*N**5)
            checks.add('infinite_harmonic_tail_'+str(N),0<tail<bound, str(tail))
            tails.append(dict(N=N, L2_tail_squared=str(tail), rigorous_upper_bound_squared=str(bound)))
        fundamental_tail = mp.mpf(3)/8-32/(9*mp.pi**2)
        relative = mp.sqrt(fundamental_tail/(mp.mpf(3)/8))
    checks.add('reject_single_harmonic_projection',fundamental_tail>0,str(relative))
    for j in range(12):
        q=np.array([j-6,2-j/3,(-1)**j],float)/8
        p=np.array([2-j/5,-j/7,(-1)**(j+1)],float)/8
        R=max(np.linalg.norm(q),np.linalg.norm(p)); A=.2+j/20
        g=lambda z:3*A*np.linalg.norm(z)*z
        diff=np.linalg.norm(g(q)-g(p)); bound=6*A*R*np.linalg.norm(q-p)
        checks.add('independent_field_space_Lipschitz_'+str(j), diff<=bound*(1+1e-12), [float(diff),float(bound)])
    return dict(coefficients=coefficients, Parseval_mean_square='3/8',
        all_odd_coefficients='b_n=-8*(-1)^((n-1)/2)/(pi*n*(n^2-4)); even n zero',
        general_L2_tail_squared_bound='128/(5*pi^2*N^5), N>=3; bound uses all integer n>N',
        tail_proof='For n>=3, n^2-4>=n^2/2; b_n^2/2<=128/(pi^2*n^6). Sum bounded by integral_N^infinity x^-6 dx.',
        finite_tails=tails, fundamental_discarded_L2_fraction=str(relative),
        scope='instantaneous full nonlinear force profile, not an evolved finite-mode projection')


def initial_conditions(generic, name, eta):
    p=generic.parameters(name,eta)
    if name=='archived_G3':
        p['c2']=-7/48; p['c3']=-1/80
    y=generic.bg.initial(p)
    y[[2,5,6,7]]*=np.sqrt(eta); y[9]*=eta
    y[1]=np.sqrt(generic.bg.physics(y,p)['energy']/(3*generic.bg.effective_mass(p)))
    return p,y


def calculate():
    pins,paths,absent=collect_pins(); before=snapshot(paths); checks=Checks()
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_gr_family_survey_v2 as generic
    objects,sy,es,forms=exact_formulas(checks)
    controls=harmonic_and_lipschitz_controls(checks)
    kernel=generic.GenericKernel()
    old=read(SURVEY+'matrices.json')['snapshots']; archived=read(G3+'summary.json')
    tr=np.load(ROOT/(G3+'trajectories.npy'),allow_pickle=False)
    checks.add('original_112_of_113_failure_preserved', archived['validation']=='FAIL_LOCAL_CHECKS' and
               archived['passed']==112 and archived['total']==113)
    rows=[]; worst_kernel=0.;worst_archive=0.; full_blocks=[]
    for name in ('archived_G3','new_B1_frame','new_hierarchical'):
        for ie,eta in enumerate(generic.ETAS):
            p,y=initial_conditions(generic,name,eta); a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=y
            ph=generic.bg.physics(y,p); Hd=ph['hdot']; pdd=generic.bg.rhs(0,y,p)[9]; J=v*ud-u*vd
            subs={es:s.Rational(str(eta)),sy['a']:a,sy['H']:H,sy['Hdot']:Hd,sy['J0']:J,sy['psi_dot']:pd}
            o={key:float(value.subs(subs)) for key,value in objects[name].items()}
            cusp=p['A']*abs(pd)**3/o['K']**1.5
            checks.add(name+'_'+str(eta)+'_Friedmann_initial',ph['constraint_norm']<1e-12,float(ph['constraint_norm']))
            if name=='archived_G3':
                err=float(np.max(abs(tr[ie,:,1:,0]-y)/(1+abs(y))))
                checks.add('G3_archived_initial_'+str(eta),err<1e-12,err)
            fourth=[]
            for k in (1,2,3,4,5):
                snap=kernel.reduce(y,p,k); i=snap['coordinates'].index('Pi');fourth.append(snap['A'][i,i].real)
            difference=sum((-1)**(4-j)*int(s.binomial(4,j))*fourth[j] for j in range(5))
            quartic_error=abs(difference+24*p['b']/a**4)/max(1.,24*p['b']/a**4)
            checks.add(name+'_'+str(eta)+'_full_coupled_quartic_retained',quartic_error<=1e-10,quartic_error)
            for k in (20,40,80):
                snap=kernel.reduce(y,p,k); coords=snap['coordinates']; block_error=0.;isolation=0.
                for polarization in ('Vy','Vz'):
                    j=coords.index(polarization)
                    for key,target in (('K',o['K']),('R',o['cross']),('A',o['A_no_gradient']-o['G']*(k/a)**2)):
                        block_error=max(block_error,float(abs(snap[key][j,j]-target)/max(1,abs(target))))
                        isolation=max(isolation,max(float(abs(snap[key][j,i])) for i in range(len(coords)) if i!=j))
                worst_kernel=max(worst_kernel,block_error)
                checks.add(name+'_'+str(eta)+'_k'+str(k)+'_covariant_vs_22field',block_error<=1e-10,block_error)
                checks.add(name+'_'+str(eta)+'_k'+str(k)+'_linear_spin1_isolation',isolation<=1e-10,isolation)
                checks.add(name+'_'+str(eta)+'_k'+str(k)+'_constraint_reconstruction',snap['reconstruction_error']<=1e-10,snap['reconstruction_error'])
                j=coords.index('Myz')
                tensor_error=float(abs(snap['K'][j,j]-o['M_tensor2']/2))
                checks.add(name+'_'+str(eta)+'_k'+str(k)+'_tensor_kinetic',tensor_error<=1e-10,tensor_error)
                if name!='archived_G3':
                    saved=next(q for q in old if q['family']==name and q['eta']==eta and q['time']==0 and q['coordinate_mode']==k)
                    err=0.
                    for key in ('A','R','K'):
                        z=np.array(saved[key]); mat=z[...,0]+1j*z[...,1]
                        err=max(err,float(np.max(abs(mat-snap[key])/(1+abs(mat)))))
                    worst_archive=max(worst_archive,err)
                    checks.add(name+'_'+str(eta)+'_k'+str(k)+'_immutable_survey_matrices',err<=1e-10,err)
                omega2=o['c_V2']*(k/a)**2+o['m_X2']
                amplitude_cusp=.01*omega2/(3*cusp) if omega2>0 and cusp>0 else None
                row=dict(family=name,eta=eta,time=0,coordinate_k=k,physical_p=k/a,H=float(H),Hdot=float(Hd),
                    psi_dot=float(pd),psi_ddot=float(pdd),J0=float(J),**o,
                    local_frozen_omega2=omega2,H_over_omega=H/np.sqrt(omega2) if omega2>0 else None,
                    C_local=cusp,ordinary_third_vertex_exists=bool(cusp==0),
                    necessary_cusp_amplitude_limit=amplitude_cusp,small_tilt_diagnostic_limit=np.sqrt(o['K'])/100,
                    direct_regulator_quartic_coefficients=[-.5*p['b']*pd**2,-p['b']*pd*(pdd+2*H*pd),-.5*p['b']*(pdd+2*H*pd)**2],
                    physical_window_admitted=False)
                rows.append(row)
                full_blocks.append(dict(family=name,eta=eta,k=k,coordinates=coords,
                    A=np.stack([snap['A'].real,snap['A'].imag],axis=-1).tolist(),
                    R=np.stack([snap['R'].real,snap['R'].imag],axis=-1).tolist(),
                    K=np.stack([snap['K'].real,snap['K'].imag],axis=-1).tolist()))
    checks.add('all_54_frozen_initial_events_retained',len(rows)==54)
    checks.add('three_family_nonzero_cusps_not_silently_replaced',all(q['C_local']>0 and not q['ordinary_third_vertex_exists'] for q in rows))
    checks.add('no_original_bytes_sizes_mtimes_changed',snapshot(paths)==before,dict(files=len(before)))
    holds=['Full nonlinear dynamical metric/matter sources and scalar/mean/fixed-charge auxiliary reduction',
           'Complete constrained quartic interactions and finite-density physical eigenstate amplitudes',
           'Controlled continuous all-sector frequency/momentum band with quartic dispersion and background remainder',
           'Zero/singular endpoints, full conformal-matter PPN and healthy complete GR recovery',
           'Genuine identifying matter-residue AND nonlinear-force normalization matching; Stage 3 not entered']
    bodies={'formulas.json':encode(forms),'controls.json':encode(controls),
            'grid.json':encode(dict(rows=rows,events=len(rows),maximum_covariant_kernel_difference=worst_kernel,
                   maximum_survey_snapshot_difference=worst_archive,scope='t=0 necessary classical interaction entry; not an admitted physical band')),
            'matrices.json':encode(dict(complex_storage='last axis [real,imag]',snapshots=full_blocks))}
    passed=sum(q['passed'] for q in checks.rows)
    summary=dict(schema='r4c1-three-family-nonanalytic-entry-v1',
        validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(checks.rows),checks=checks.rows,
        status='CONDITIONAL_NONANALYTIC_COUPLED_ENTRY_FULL_PHYSICAL_WINDOW_OPEN',
        physical_decision='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',physical_go=False,
        full_coupled_interactions_computed=False,physical_EFT_cutoff_derived=False,
        stage2_complete=False,stage3_entered=False,all_action_no_go=False,
        review_status='DEFERRED',Rule9_cleared=False,physics_pass=False,gate_effect='NONE',
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',**{'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'},
        K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',substantive_unknowns=holds,
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,artifacts={name:sha(body) for name,body in bodies.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__,mpmath=mp.__version__),
        review_dependencies=['GR-FAMILY-SURVEY','G3V/G3V-CROSSCHECK/G3I','generic variation/G3N5','all inherited deferred review'],
        frozen_comparators='Inherited unchanged; no new PPN/GW data fit or physical-band applicability claim')
    bodies['summary.json']=encode(summary)
    return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_three_family_nonanalytic_entry_attempt_01')
    parser.add_argument('--replay')
    args=parser.parse_args(); dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay directory absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output directory')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            side=(sha(body)+'  '+name+'\n').encode()
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:
                raise RuntimeError('Immutable replay mismatch: '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
          **{key:summary[key] for key in ('validation','passed','total','physics_pass','physical_decision')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
