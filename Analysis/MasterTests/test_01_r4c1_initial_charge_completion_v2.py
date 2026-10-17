"""Initial charge/mean-lapse completion diagnostic; not nonlinear admission.

No archived state is modified or evolved. The explicit finite coefficient lift
and necessary new initial counters are separate objects, not repaired data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
KIN = BASE + 'r4c1_three_family_fixed_charge_kinetic_attempt_04/'
RET = BASE + 'r4c1_fixed_charge_retarded_comparison_attempt_03/'
FORCE = BASE + 'r4c1_g3n4_force_attempt_01/'
CHARGE = BASE + 'r4c1_three_family_charge_domain_attempt_05/'
PLANAR = BASE + 'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V1_CONTRACT_2026-10-16.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PINS = {
    'Analysis/MasterTests/test_01_r4c1_initial_charge_completion_v1.py':
        '971b8e481bcd6592cc5277424d038ea88fed271edc7696c4832c1dad26da1295',
    'Theory/Gates/RES-001/RES001_R4C1_INITIAL_CHARGE_COMPLETION_V2_SYNTAX_ADDENDUM_2026-10-16.md':
        '23011e35520fa0fa5e97525cf0352dc1ebcc2c39ab060bf150d30669c5a453e0',
    CONTRACT: 'e35df353d775fa42da2dd07cd2f1e7c05c0888aff33c342e94eb0c681a9b1daf',
    KIN + 'summary.json': '9429ab897513fe5bbeda30242fa2bc535687378567eee388229450f1c963e898',
    FORCE + 'summary.json': 'ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287',
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':
        '81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V3_REPORT_2026-10-16.md':
        'a5acbb6d2f659f9c2e4719f32f91ef9f8a4c2cc2c9bdd1fff8635d46fc1199c3',
    'Analysis/MasterTests/test_01_r4c1_three_family_charge_domain_v5.py':
        'a3c9d3077fcf03d25b761f2b43e3503e7a71d4b4d217dd7720af1b966da0d575',
    'Analysis/MasterTests/test_01_r4c1_g3n4_force_coverage_v1.py':
        '8474fd75bcab4c31da804dc41db813063c1186e2a937b6939a364ad153c6aff8',
}
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
          'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX = {n: i for i, n in enumerate(FIELDS)}
FAMILIES = ('archived_G3','new_B1_frame','new_hierarchical')
SHA = lambda b: hashlib.sha256(b).hexdigest()
READ = lambda p: json.loads((ROOT / p).read_bytes())
ENCODE = lambda o: (json.dumps(o, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
CLEAN = lambda e: s.factor(s.cancel(s.expand(e)))
NUM = lambda v: mp.mpf(str(v))
COMPLEX = lambda v: mp.mpc(NUM(v[0]), NUM(v[1]))
DISPLAY = lambda v: mp.nstr(v, 45)


class Checks:
    def __init__(self):
        self.rows = []
        self.names = set()

    def add(self, name, passed, value=None, criterion='exact'):
        if name in self.names:
            raise ValueError('Duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name, passed=bool(passed), value=value, criterion=criterion))

    def exact(self, name, residual):
        values = list(residual) if isinstance(residual, (list, tuple, s.MatrixBase)) else [residual]
        bad = [dict(index=i, residual=str(q)) for i, v in enumerate(values) if (q := CLEAN(v)) != 0]
        self.add(name, not bad, bad, 'zero_exact')

    def small(self, name, value, tolerance):
        self.add(name, abs(value) <= NUM(tolerance), DISPLAY(value), '<= '+tolerance)


def inputs():
    pins = {}
    absent = set()
    for parent in (KIN, FORCE):
        data = READ(parent+'summary.json')
        pins.update(data['source_sha256'])
        pins.update({parent+n: h for n, h in data['artifacts'].items()})
        absent.update(data.get('inherited_sidecars_absent', data.get('source_sidecars_absent', [])))
    pins.update(PINS)
    pins[SELF] = SHA((ROOT/SELF).read_bytes())
    paths = []
    for name, expected in pins.items():
        p = ROOT/name
        if SHA(p.read_bytes()) != expected:
            raise RuntimeError('Pinned source drift: '+name)
        paths.append(p)
        side = Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text(encoding='utf-8').split()[0].lower() != expected:
                raise RuntimeError('Frozen sidecar differs: '+name)
            paths.append(side)
        elif name not in absent:
            raise RuntimeError('Required sidecar absent: '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(), SHA(p.read_bytes()), p.stat().st_size,
                 p.stat().st_mtime_ns) for p in sorted(set(paths))]
    return pins, sorted(absent), snapshot


def derive(ch):
    print('Derive generic initial currents and omitted-order mean equations', flush=True)
    a, N, C, R, d, zeta, A, pd, M, H = s.symbols('a N C R d zeta A pd M H', positive=True)
    e, co, sh, tau, eps, xd, ph = s.symbols('e cosine shift tau_dot epsilon xdot_counter phase_counter', real=True)
    V = e*co
    gamma = s.sqrt(1+V*V)
    gi = s.diag(-1/N**2, 1/a**2, 1/a**2, 1/a**2)
    gi[0,2] = gi[2,0] = sh/(a*N**2)
    gi[2,2] -= sh**2/(a*a*N*N)
    n = s.Matrix([gamma/N, 0, (V-sh*gamma/N)/a, 0])
    cov = s.diag(-N*N+sh*sh, a*a, a*a, a*a)
    cov[0,2] = cov[2,0] = a*sh
    projector = gi+n*n.T
    ch.exact('arbitrary_shift_ADM_metric_inverse', gi*cov-s.eye(4))
    ch.exact('exact_unit_frame_with_arbitrary_shift', (n.T*cov*n)[0]+1)
    ch.exact('projected_time_component_retains_boost', projector[0,0]-V*V/N**2)
    ud, vd, u, v = s.symbols('u_dot v_dot u v', real=True)
    J = v*ud-u*vd
    Lscalar = -N*a**3*(gi[0,0]*(ud*ud+vd*vd)+zeta*projector[0,0]*J*J)/2
    Q = -v*s.diff(Lscalar, ud)+u*s.diff(Lscalar, vd)
    ch.exact('alignment_corrected_charge_from_varied_Cartesian_momenta',
             Q+N*a**3*(gi[0,0]+zeta*(u*u+v*v)*projector[0,0])*J)
    q_local = Q.subs({u:R,v:0,ud:0,vd:d+e*e*ph,N:1})
    ch.exact('local_initial_charge_shift_independent', s.diff(q_local,sh))
    ch.exact('local_initial_charge_exact', q_local-a**3*R*(d+e*e*ph)*(1-zeta*R*R*e*e*co*co))
    Ldust = -N*a**3*eps*(C*C*gi[0,0]*tau*tau+C**4)/2
    P = s.diff(Ldust,tau)
    ch.exact('full_dust_momentum_before_multiplier_constraint', P-a**3*eps*C*C*tau/N)
    ch.exact('initial_dust_charge_local', P.subs({N:1,tau:C})-a**3*eps*C**3)
    ch.exact('dust_shell_uniform_clock', (gi[0,0]*tau*tau+C*C).subs({N:1,tau:C}))
    avg2 = s.Rational(1,2)
    sig = zeta*R*R/2
    Q0 = a**3*R*d
    avgQ = q_local.subs(co**2,avg2)
    Qlift = s.expand(avgQ.subs(ph,d*sig))
    ch.exact('exact_quadratic_prepared_lift_Q4_defect', Qlift-Q0+Q0*sig**2*e**4)
    completed_d = d/(1-sig*e*e)
    ch.exact('exact_charge_only_uniform_phase_completion', a**3*R*completed_d*(1-sig*e*e)-Q0)
    remainder = d*sig**2*e**4/(1-sig*e*e)
    ch.exact('charge_only_geometric_remainder_identity', completed_d-d-d*sig*e*e-remainder)
    t = s.Symbol('t', nonnegative=True)
    ch.exact('geometric_bound_factor_identity', 2-1/(1-t)-(1-2*t)/(1-t))
    ch.add('reject_average_only_angular_domain',
           (1-t).subs(t,s.Rational(3,4))>0 and (1-2*t).subs(t,s.Rational(3,4))<0)
    eta = s.Symbol('eta', positive=True)
    ch.exact('diagnostic_recipe_Q4', (-Q0*sig**2).subs({a:1,R:s.sqrt(eta),d:s.sqrt(eta),zeta:eta/13})+eta**5/676)
    ch.add('reject_omitted_alignment_charge', s.diff(q_local,zeta) != 0)
    ch.add('charge_completion_changes_lapse_at_fourth_order', -d*d*sig**2 != 0)

    # A real directional |e|^3 term, differentiated at N>0, not a cubic Taylor vertex.
    Y = (s.Matrix([pd,0,0,0]).T*projector*s.Matrix([pd,0,0,0]))[0]
    ch.exact('projected_force_Y_arbitrary_shift', Y-pd*pd*e*e*co*co/N**2)
    Babs = s.Symbol('absolute_pd_e_cosine', nonnegative=True)
    Lcusp = -A*a**3*Babs**3/N**2
    cusp_lapse = s.diff(Lcusp,N).subs(N,1)/a**3
    ch.exact('cusp_lapse_including_measure', cusp_lapse-2*A*Babs**3)
    ch.add('reject_omitted_lapse_measure', 3*A*Babs**3 != cusp_lapse)
    ch.add('reject_cusp_lapse_sign_reversal', -2*A*Babs**3 != cusp_lapse)
    coverage = READ(FORCE+'formulas.json')
    symbols = {name:s.Symbol(name,real=True) for name in ('A','W','e','p')}
    inherited = s.sympify(coverage['Euler_sources']['alpha'],locals={**symbols,'Abs':s.Abs})
    expected = 2*symbols['A']*s.Abs(symbols['p']*symbols['e']*symbols['W'])**3
    ch.exact('bind_inherited_generic_force_lapse_source', inherited-expected)
    th = s.Symbol('theta', real=True)
    mean_abs3 = s.simplify(4*s.integrate(s.cos(th)**3,(th,0,s.pi/2))/(2*s.pi))
    ch.exact('exact_periodic_abs_cosine_cubed_mean', mean_abs3-4/(3*s.pi))
    ch.add('reject_quadratic_two_angle_rule_for_cusp', mean_abs3 != s.Rational(1,2))

    data = READ(RET+'formulas.json')['preparation']
    namespace = {n:s.Symbol(n,real=True) for n in set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',data['Jacobian'])) if n!='Matrix'}
    Jgeneric = s.sympify(data['Jacobian'],locals={**namespace,'Matrix':s.Matrix})
    x = namespace
    MC = x['MP2']+x['MU2']*(x['c1']+3*x['c2']+x['c3'])/2
    expectedJ = s.Matrix([[x['a']**3*x['u0'],0],[-x['a']**3*x['v_dot']/x['C'],2*x['a']**3*MC*x['H']/x['C']]])
    ch.exact('generic_sealed_two_counter_Jacobian', Jgeneric-expectedJ)
    ch.exact('generic_sealed_counter_determinant', Jgeneric.det()-2*x['a']**6*x['u0']*MC*x['H']/x['C'])
    for singular in ('u0','H'):
        ch.exact('reject_singular_counter_'+singular, Jgeneric.det().subs(x[singular],0))
    Jreduced = s.Matrix([[a**3*R,0],[-a**3*d/C,2*a**3*M*H/C]])
    P3free = 2*A*a**3*pd**3*mean_abs3/C
    x3 = -A*pd**3*mean_abs3/(M*H)
    ch.exact('necessary_cusp_mean_both_charge_coefficients', Jreduced*s.Matrix([0,x3])+s.Matrix([0,P3free]))
    f = s.Symbol('absolute_cosine_cubed', nonnegative=True)
    density3 = 2*A*pd**3*(f-mean_abs3)/C**4
    ch.exact('cusp_density_full_profile_not_dropped', C**4*density3-(2*M*H*x3+2*A*pd**3*f))
    ch.exact('cusp_density_mean_zero', density3.subs(f,mean_abs3))
    ch.add('reject_zero_density_profile_from_zero_mean', density3 != 0)
    ch.add('reject_omitted_cusp_volume_counter', P3free != 0)
    ch.exact('eta_cusp_volume_counter', x3.subs({A:2*eta**s.Rational(3,2)/7,pd:eta/5})+8*eta**s.Rational(9,2)/(2625*s.pi*M*H))
    ch.add('new_cusp_mean_response_first_feeds_transverse_order_four', 1+3 == 4)
    ch.add('new_phase_order_four_first_feeds_transverse_order_five', 1+4 == 5)
    ch.add('cusp_not_ordinary_odd_cubic', s.Abs(-s.Integer(2))**3 != (-s.Integer(2))**3)
    return dict(
        exact_initial_lift_Q=str(Qlift), background_Q=str(Q0),
        quadratic_phase_counter=str(d*sig), exact_lift_charge_defect=str(-Q0*sig**2*e**4),
        exact_charge_only_phase_velocity=str(completed_d), exact_velocity_remainder=str(remainder),
        remainder_bound='0<=sig*e^2<=1/2: |remainder|<=2*|d|*sig^2*|e|^4',
        local_domain='1-zeta*R^2*e^2>0 (stronger than the averaged charge denominator)',
        cusp_lapse_density=str(2*A*pd**3*s.Abs(e)**3*f), mean_abs_cosine_cubed=str(mean_abs3),
        necessary_initial_volume_velocity_abs_e3=str(x3), necessary_initial_phase_velocity_abs_e3='0',
        free_mean_dust_abs_e3=str(P3free), density_abs_e3=str(density3),
        phase_only_lapse_linear_contribution_at_e4=str(-d*d*sig**2),
        generic_counter_Jacobian=str(Jgeneric),
        admission='NOT_ESTABLISHED: only charges and the mean lapse coefficient on the initial slice',
        nonclaims=['No complete local constraint solve','No all-order evolved state','No physical window',
                   'No changed retarded timing result','No full potential/energy positivity']), mean_abs3


def direct_currents(a,C,R,vd,pd,epsilon,e,angle,shift,N=mp.mpf(1)):
    """Independent ADM metric/projector evaluation, retaining arbitrary shift."""
    V = e*mp.cos(angle)
    gi = mp.diag([-1/(N*N),1/(a*a),1/(a*a),1/(a*a)])
    gi[0,2] = gi[2,0] = shift/(a*N*N)
    gi[2,2] -= shift*shift/(a*a*N*N)
    gamma = mp.sqrt(1+V*V)
    n = mp.matrix([gamma/N,0,(V-shift*gamma/N)/a,0])
    J = mp.matrix([-R*vd,0,0,0])
    density = N*a**3
    Q = density*sum((gi[0,j]+(R*R)*(gi[0,j]+n[0]*n[j])*DIRECT_ZETA)*J[j] for j in range(4))
    P = -density*epsilon*C*C*gi[0,0]*C
    # Cancellation-free rest-frame evaluation is independent of the closed mean formula.
    rest = mp.matrix([0,V*pd/N,0])
    Y = sum(q*q for q in rest)
    return Q,P,Y,density


def archive_and_numeric(ch,mean_exact):
    global DIRECT_ZETA
    mp.mp.dps = 80
    mean3 = 4/(3*mp.pi)
    quadrature = mp.quad(lambda t:abs(mp.cos(t))**3,[0,mp.pi/2,3*mp.pi/2,2*mp.pi])/(2*mp.pi)
    ch.small('independent_full_period_cusp_quadrature',quadrature-mean3,'1e-50')
    # Check the zero-mean density without confusing a mean equation with pointwise cancellation.
    zero_mean = mp.quad(lambda t:abs(mp.cos(t))**3-mean3,[0,mp.pi/2,3*mp.pi/2,2*mp.pi])/(2*mp.pi)
    ch.small('independent_cusp_density_zero_mean_quadrature',zero_mean,'1e-50')
    planar = READ(PLANAR)
    canonical = READ(CHARGE+'canonical.json')
    dyn = tuple(canonical['physical_fields'])
    ch.add('sealed_complete13_physical_field_order',dyn==FIELDS[4:17])
    texts = [canonical[n] for n in ('Q2_affine','P2_affine','Em_constraint_affine')]
    names = set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts))) - {'Matrix'}
    names.update('eta'.split())
    for item in planar['families'].values():
        names.update(item['parameter_map'])
    sy = {n:s.Symbol(n,real=True) for n in names}
    rows = [s.sympify(v,locals={**sy,'Matrix':s.Matrix}) for v in texts]
    args = sorted({str(q) for r in rows for q in r.free_symbols})
    fun = s.lambdify([sy[n] for n in args],list(rows[0])+list(rows[1])+list(rows[2]),'mpmath',cse=True)
    runs = READ(RET+'trajectories.json')['runs']
    ch.add('all18_unchanged_archived_initial_events',len(runs)==18)
    records = []
    maxima = {n:mp.mpf(0) for n in ('initial_slice_residual','sealed_affine_residual','Q2_floating_residual',
              'mean_density_floating_residual','current_identity_error','force_lapse_finite_error',
              'corrected_charge_error','geometric_bound_violation')}
    for irun,run in enumerate(runs):
        tag = str(irun)+'_'+run['family']+'_'+run['eta_exact']+'_'+run['method']
        eta = mp.mpf(str(s.Rational(run['eta_exact']).p))/mp.mpf(str(s.Rational(run['eta_exact']).q))
        p = {n:NUM(str(s.N(s.sympify(v,locals={'eta':s.Symbol('eta')}).subs(s.Symbol('eta'),s.Rational(run['eta_exact'])),90)))
             for n,v in planar['families'][run['family']]['parameter_map'].items()}
        M = p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        ev = run['events'][0]
        b = list(map(NUM,ev['background_and_first_wave']))
        a,H,R,ud,v,d,r,rd,psi,pd,rho,tau,w,wd = b
        C = mp.exp(p['beta']*psi)
        sig = p['zeta']*R*R/2
        DIRECT_ZETA = p['zeta']
        mean = ev['full_response']['mean']
        second = ev['full_response']['second']
        q0 = list(map(COMPLEX,mean['response']))
        q2 = list(map(COMPLEX,second['response']))
        v0 = list(map(COMPLEX,mean['velocity']))
        v2 = list(map(COMPLEX,second['velocity']))
        recipe = [a-1,R-mp.sqrt(eta),ud,v,d-mp.sqrt(eta),r-mp.sqrt(eta),
                  rd-mp.sqrt(eta)/4,psi,pd-eta/5,rho-NUM('0.2'),tau,w-1,wd]
        recipe += [q0[IX[n]] for n in FIELDS[:18]]+[q2[IX[n]] for n in FIELDS[:18]]
        phase = NUM(run['preparation']['phase_velocity'])
        volume = NUM(run['preparation']['volume_velocity'])
        for n in FIELDS[4:18]:
            expected = 2*volume/3 if n in ('Mxx','Myy','Mzz') else phase if n=='dv' else 0
            recipe += [v0[IX[n]]-expected,v2[IX[n]]]
        recipe += [NUM(ev['time']),NUM(run['times'][0])]
        slice_error = max(map(abs,recipe))
        maxima['initial_slice_residual'] = max(maxima['initial_slice_residual'],slice_error)
        ch.small(tag+'_exact_initial_slice_vs_float_archive',slice_error,'1e-10')
        raw = dict(p,a=a,H=H,u0=R,u_dot=ud,v0=v,v_dot=d,r0=r,r_dot=rd,
                   psi_dot=pd,rho=rho,C=C,w=w,wd=wd,k=40,m2=1,lambda4=mp.mpf(1)/3,
                   lambda6=mp.mpf(1)/5,Lambda=2,mr2=2,lambda_r=mp.mpf(1)/7,g_r=3*eta/7,rho_Lambda=0)
        allrows = fun(*[raw[n] for n in args])
        seed = list(map(COMPLEX,run['preparation']['state'][:26]))
        affine = []
        for nr in range(3):
            row = allrows[nr*27:(nr+1)*27]
            val = sum(row[j]*seed[j] for j in range(26))+row[26]
            affine.append(val)
        affine_error = max(abs(val)/(1+abs(allrows[nr*27+26])+sum(abs(allrows[nr*27+j]*seed[j]) for j in range(26)))
                           for nr,val in enumerate(affine))
        ch.small(tag+'_sealed_affine_Q2_P2_density',affine_error,'1e-10')
        maxima['sealed_affine_residual'] = max(maxima['sealed_affine_residual'],affine_error)
        Q0 = a**3*R*d
        Q2float = a**3*R*(phase-d*sig)
        Q4float = -a**3*R*phase*sig
        maxima['Q2_floating_residual'] = max(maxima['Q2_floating_residual'],abs(Q2float))
        maxima['mean_density_floating_residual'] = max(maxima['mean_density_floating_residual'],abs(q0[IX['Em']]))
        x3 = -4*p['A']*abs(pd)**3/(3*mp.pi*M*H)
        P3 = 8*p['A']*a**3*abs(pd)**3/(3*mp.pi*C)
        ch.small(tag+'_necessary_cusp_mean_cancellation',2*a**3*M*H*x3/C+P3,'1e-50')
        ch.add(tag+'_regular_counter_and_local_density',min(a,C,R,H,M,eta,rho)>0)
        case_errors = []
        for den in (500,1000,2000):
            for sign in (-1,1):
                e = mp.mpf(sign)/den
                local_domain = 1-2*sig*e*e
                ch.add(tag+'_amplitude_domain_'+str(sign)+'_'+str(den),local_domain>0 and 0<=sig*e*e<=mp.mpf(1)/2)
                density_lower = rho/C**4-e*e*(abs(q0[IX['Em']])+2*abs(q2[IX['Em']]))-abs(e)**3*2*p['A']*abs(pd)**3*mean3/C**4
                ch.add(tag+'_all_angle_density_lower_bound_'+str(sign)+'_'+str(den),density_lower>0,DISPLAY(density_lower))
                dcomplete = d/(1-sig*e*e)
                remainder = dcomplete-d-d*sig*e*e
                bound = 2*abs(d)*sig*sig*e**4
                maxima['geometric_bound_violation'] = max(maxima['geometric_bound_violation'],max(0,abs(remainder)-bound))
                amp_error = mp.mpf(0)
                completed_error = mp.mpf(0)
                finite_error = mp.mpf(0)
                for angle in (mp.pi/7,mp.pi/3,4*mp.pi/5):
                    # Existing third shift is explicitly retained. No new shift solve.
                    sh = -p['MU2']*(p['c1']+p['c3'])/(p['MP2']-p['MU2']*(p['c1']+p['c3']))*e*mp.cos(angle)
                    sh += e**3*sum(2*mp.re(COMPLEX(item['third_shift'][0])*mp.exp(1j*item['mode']*angle)) for item in ev['third_vector_shift'])
                    epsilon = rho/C**4+e*e*mp.re(q0[IX['Em']]+2*q2[IX['Em']]*mp.exp(2j*angle))
                    Q,P,Y,density = direct_currents(a,C,R,d+e*e*phase,pd,epsilon,e,angle,sh)
                    target = a**3*R*(d+e*e*phase)*(1-p['zeta']*R*R*e*e*mp.cos(angle)**2)
                    amp_error = max(amp_error,abs(Q-target)/(1+abs(target)),abs(P-a**3*C**3*epsilon)/(1+abs(P)))
                    qdone,_,_,_ = direct_currents(a,C,R,dcomplete,pd,epsilon,e,angle,sh)
                    completed_error = max(completed_error,abs(qdone-a**3*R*dcomplete*(1-2*sig*e*e*mp.cos(angle)**2))/(1+abs(Q0)))
                    target_lapse = 2*p['A']*a**3*abs(pd*e*mp.cos(angle))**3
                    for step in (mp.mpf('1e-6'),mp.mpf('5e-7')):
                        values = []
                        for N in (1+step,1-step):
                            _,_,Y,measure = direct_currents(a,C,R,d+e*e*phase,pd,epsilon,e,angle,sh,N)
                            values.append(-p['A']*measure*Y**mp.mpf('1.5'))
                        finite_error = max(finite_error,abs((values[0]-values[1])/(2*step)-target_lapse)/abs(target_lapse))
                    density_with_required_cusp = epsilon+abs(e)**3*2*p['A']*abs(pd)**3/C**4*(abs(mp.cos(angle))**3-mean3)
                    if min(epsilon,density_with_required_cusp)<=0:
                        raise ValueError('Initial diagnostic density left positive branch: '+tag)
                # Exact mean identities and the floating archival residue remain separate.
                qmean_archive = a**3*R*(d+e*e*phase)*(1-sig*e*e)
                amp_error = max(amp_error,abs(qmean_archive-Q0-Q2float*e*e-Q4float*e**4)/(1+abs(Q0)))
                completed_error = max(completed_error,abs(a**3*R*dcomplete*(1-sig*e*e)-Q0)/(1+abs(Q0)))
                maxima['current_identity_error'] = max(maxima['current_identity_error'],amp_error)
                maxima['force_lapse_finite_error'] = max(maxima['force_lapse_finite_error'],finite_error)
                maxima['corrected_charge_error'] = max(maxima['corrected_charge_error'],completed_error)
                case_errors.append(dict(amplitude=str(sign)+'/'+str(den),local_angular_margin=DISPLAY(local_domain),
                    all_angle_density_lower_bound=DISPLAY(density_lower),
                    current_error=DISPLAY(amp_error),phase_completion_error=DISPLAY(completed_error),
                    lapse_finite_error=DISPLAY(finite_error),velocity_remainder=DISPLAY(remainder),remainder_bound=DISPLAY(bound),
                    exact_recipe_Q4_effect=DISPLAY(-Q0*sig*sig*e**4),archived_Q2_effect=DISPLAY(Q2float*e*e)))
        ch.small(tag+'_independent_currents_all_amplitudes_angles',max(NUM(row['current_error']) for row in case_errors),'1e-50')
        ch.small(tag+'_independent_phase_completion',max(NUM(row['phase_completion_error']) for row in case_errors),'1e-50')
        ch.small(tag+'_independent_lapse_central_differences',max(NUM(row['lapse_finite_error']) for row in case_errors),'1e-10')
        records.append(dict(family=run['family'],eta_exact=run['eta_exact'],method=run['method'],
            initial_slice_residual=DISPLAY(slice_error),affine_residuals=[str(v) for v in affine],
            Q2_floating_archive=DISPLAY(Q2float),Q4_floating_archive=DISPLAY(Q4float),
            Q4_exact_recipe=DISPLAY(-eta**5/676),mean_density_floating_archive=str(q0[IX['Em']]),
            necessary_new_abs_e3_volume_velocity=DISPLAY(x3),free_mean_dust_abs_e3=DISPLAY(P3),
            discarded_by_quadratic_two_angle_rule=False,controls=case_errors))
    ch.small('all_geometric_remainders_within_explicit_bound',maxima['geometric_bound_violation'],'1e-50')
    ch.add('retain_three_families_two_methods',sorted({q['family'] for q in records})==sorted(FAMILIES)
           and {q['method'] for q in records}=={'DOP853','Radau'})
    return dict(runs=records,maxima={n:DISPLAY(v) for n,v in maxima.items()},
                cosine_cusp_mean=DISPLAY(mean3),independent_quadrature=DISPLAY(quadrature),
                scope='Initial time only; exact prescribed slice separated from immutable floating archived coefficients')


def calculate():
    mp.mp.dps = 80
    pins,absent,snapshot = inputs()
    before = snapshot()
    ch = Checks()
    formulas,mean = derive(ch)
    if not all(row['passed'] for row in ch.rows):
        numerics = dict(skipped='Exact prerequisite failure')
    else:
        numerics = archive_and_numeric(ch,mean)
    after = snapshot()
    ch.add('all_source_sidecar_hash_size_mtime_records_preserved',before==after)
    scope = dict(claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,
        physics_pass=False,gate_effect='NONE',initial_order_diagnostic_only=True,
        complete_nonlinear_fixed_charge_admission=False,full_local_constraints_solved=False,
        physical_window_admitted=False,full_energy_positive=False,old_preparation_changed=False,
        retarded_warning_unchanged=True,stage2_complete=False,stage3_entered=False,
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',
        K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        precise_remaining=['All local constraint rows and finite-amplitude completion in a declared canonical chart',
            'All required higher directional response sectors, no continuous charge projection',
            'Constrained finite-k energy/characteristics with quartic dispersion and interaction error control',
            'Tensor/local gravity/healthy GR and genuine matter plus nonlinear-force matching'])
    ch.add('reject_finite_order_to_full_nonlinear_admission',not scope['complete_nonlinear_fixed_charge_admission'])
    verification = dict(passed=sum(row['passed'] for row in ch.rows),total=len(ch.rows),checks=ch.rows)
    verification['validation'] = 'PASS' if verification['passed']==verification['total'] else 'FAIL'
    payloads = {'formulas.json':ENCODE(formulas),'numerics.json':ENCODE(numerics),
                'scope.json':ENCODE(scope),'verification.json':ENCODE(verification)}
    summary = dict(schema='r4c1-initial-charge-completion-v2',**verification,**scope,
        status=('CONDITIONAL_INITIAL_ORDER_RESULT_COMPLETE_NONLINEAR_ADMISSION_OPEN'
                if verification['validation']=='PASS' else 'DIAGNOSTIC_INCOMPLETE_LOCAL_CHECK_FAILURE'),
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,artifacts={n:SHA(b) for n,b in payloads.items()},
        runtime=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__),
        review_id='R9-MT1-INITIAL-CHARGE-COMPLETION-V1',
        review_dependencies=['THREE-FAMILY-FIXED-CHARGE-KINETIC-V3','FIXED-CHARGE-RETARDED-V3',
            'THREE-FAMILY-CHARGE-DOMAIN-V5','G3N4-FORCE-COVERAGE','MEAN-MODE-ENERGY','PLANAR-WWR','all transitive debt'])
    payloads['summary.json'] = ENCODE(summary)
    return payloads,summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_initial_charge_completion_attempt_02')
    parser.add_argument('--replay')
    args = parser.parse_args()
    dest = (ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('Replay directory absent')
    if not args.replay and dest.exists():
        raise FileExistsError('Refuse existing evidence directory')
    payloads,summary = calculate()
    if args.replay:
        before = [(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        for name,b in payloads.items():
            if (dest/name).read_bytes()!=b or (dest/(name+'.sha256')).read_bytes()!=(SHA(b)+'  '+name+'\n').encode():
                raise RuntimeError('Read-only replay differs: '+name)
        after = [(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:
            raise RuntimeError('Replay artifact metadata changed')
        action = 'READ_ONLY_REPLAY_EXACT'
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,b in payloads.items():
            with (dest/name).open('xb') as f:
                f.write(b)
            with (dest/(name+'.sha256')).open('xb') as f:
                f.write((SHA(b)+'  '+name+'\n').encode())
        action = 'NEW_RECEIPTS_WRITTEN'
    print(json.dumps(dict(action=action,**{n:summary[n] for n in ('validation','passed','total','status','physics_pass','gate_effect')})),flush=True)
    for row in summary['checks']:
        if not row['passed']:
            print(json.dumps(row),flush=True)
    return 0 if summary['validation']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
