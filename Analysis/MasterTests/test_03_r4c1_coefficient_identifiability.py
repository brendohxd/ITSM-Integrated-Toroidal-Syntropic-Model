"""R4C1-C1: target-independent current-action identifiability, not blind clearance.

Exact covariant/field-space tests precede repeated background controls.
The local spherical normalization is conditional, not a B1 galaxy solution.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s

import test_01_r4c1_interacting_background as bg
from test_01_r4c1_full_variation import frame_blocks, connection_tensor


ROOT = Path(__file__).resolve().parents[2]
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':
        '81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
    'Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_CONTRACT_2026-09-25.md':
        '29f54fbef62d6a2b2a5d29d772633a87694a9ed1d05f7b00244833b88075465d',
    'Analysis/MasterTests/test_01_r4c1_full_variation.py':
        'aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':
        '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/test_01_r4c1_gr_limit.py':
        '0730de78971da97345517477115ace91bd0b9c1c0ae0b136c07067854a38a710',
}
OUT = ROOT/'Analysis/MasterTests/outputs/test_03_r4c1_coefficient_identifiability_summary.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self):
        self.checks = []

    def exact(self, name, residual, nonzero=False):
        residual = s.simplify(residual)
        passed = residual.is_zero is False if nonzero else residual == 0
        self.checks.append(dict(name=name, passed=bool(passed), residual=str(residual),
                               expected='nonzero' if nonzero else 'zero'))

    def numeric(self, name, passed, value, criterion):
        self.checks.append(dict(name=name, passed=bool(passed), value=value, criterion=criterion))


def flat(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flat(item)
        else:
            yield item


def homogeneous_variation(audit):
    lapse, scale, ell = s.symbols('N a ell', positive=True)
    pdot, j0, kdot, z, lam, v0, vs = s.symbols('pdot j0 kdot z lam v0 vs', real=True)
    g = s.diag(-lapse**2, scale**2, scale**2, scale**2)
    gi = g.inv()
    coeff = {key:s.Symbol(key, real=True) for key in ('M','c1','c2','c3','c4','K','A','b','zz')}
    # Off-unit timelike U: the force projector is normalized before variation.
    U = [ell/lapse, s.S.Zero, s.S.Zero, s.S.Zero]
    V = s.diag(v0,vs,vs,vs).tolist()
    p = [pdot,s.S.Zero,s.S.Zero,s.S.Zero]
    block = frame_blocks(g.tolist(),gi.tolist(),U,V,[j0,0,0,0],p,
                         [kdot,0,0,0],z,lam,coeff)
    A = coeff['A']
    audit.exact('normalized_homogeneous_Y_zero',block['Y'])
    audit.exact('normalized_homogeneous_Q',block['Q']-pdot/lapse)
    collections = {'L':block['Ls'],'frame_E_algebraic':block['F'],
                   'connection_momentum':block['P'],'metric_algebraic':block['B2'],
                   'connection_stress':connection_tensor(U,block['P'],gi.tolist())}
    for name,values in collections.items():
        residuals = [s.simplify(s.diff(value,A)) for value in flat(values)]
        audit.numeric(f'homogeneous_A_derivative_{name}',all(x==0 for x in residuals),
                      [str(x) for x in residuals if x!=0],'every component exactly zero')
    hp = s.Matrix(block['h'])*s.Matrix(p)
    flux = -3*A*s.sqrt(block['Y'])*hp
    audit.exact('homogeneous_cubic_force_flux_zero',sum(x*x for x in flux))
    # An unnormalized projector is a different off-shell theory.
    wrong_Y = (s.Matrix(p).T*(gi+s.Matrix(U)*s.Matrix(U).T)*s.Matrix(p))[0]
    audit.exact('unnormalized_projector_mutation_rejected',wrong_Y.subs({ell:2,pdot:1,lapse:1}),True)
    return dict(branch='normalized timelike, spatially aligned homogeneous fields',
                result='A absent from full homogeneous equations, not merely omitted in an ODE',
                metric_scope='includes algebraic stress and connection momentum dependence',
                currents='Qmp=beta*T_m*grad(psi); Qsyn=-g_r*s*r*grad(r)/2; no A at fixed fields')


def quadratic_regularity(audit):
    x,y,z = s.symbols('qx qy qz',real=True)
    A,eps = s.symbols('A eps',positive=True)
    q = s.Matrix([x,y,z])
    r = s.sqrt(q.dot(q))
    f = A*r**3
    gradient = s.Matrix([s.diff(f,v) for v in q])
    hessian = s.hessian(f,q)
    analytic_hessian = 3*A*(r*s.eye(3)+q*q.T/r)
    audit.exact('cubic_gradient_formula',sum(s.simplify(v)**2 for v in gradient-3*A*r*q))
    audit.exact('cubic_hessian_formula_nonzero_q',sum(s.simplify(v)**2 for v in hessian-analytic_hessian))
    audit.exact('radial_hessian_eigenvalue',sum(s.simplify(v)**2 for v in hessian*q-6*A*r*q))
    tangent = s.Matrix([-y,x,0])
    audit.exact('transverse_hessian_eigenvalue',sum(s.simplify(v)**2 for v in hessian*tangent-3*A*r*tangent))
    audit.exact('hessian_operator_norm_zero_limit',s.limit(6*A*eps,eps,0,dir='+'))
    audit.exact('gradient_norm_zero_limit',s.limit(3*A*eps**2,eps,0,dir='+'))
    audit.exact('cubic_first_two_orders_vanish',s.limit(A*eps**3/eps**2,eps,0,dir='+'))
    audit.exact('quadratic_Y_mutation_rejected',s.diff(A*x*x,x,2),True)
    third_plus = s.diff(A*x**3,x,3)
    third_minus = s.diff(-A*x**3,x,3)
    audit.exact('analytic_third_vertex_mutation_rejected',third_plus-third_minus,True)
    return dict(field_space='f=A|q|^3 is C2 with gradient and Hessian zero at q=0; not C3',
                chain_rule='q(fields) smooth in normalized timelike chart; volume factor cannot create orders <=2',
                conclusion='full pre-constraint classical quadratic action independent of A on this branch',
                reduction_hold='inherited by a regular constraint reduction only; no invertibility or stability proved',
                quantum_hold='no statement that radiative or nonlinear corrections are A independent')


def invariant_and_static_checks(audit):
    A,K,b,beta,sigma,lam,G,mass,R,H,Cproj,d = s.symbols(
        'A K b beta sigma lambda G_static M_source R H C_proj d',positive=True)
    new = dict(A=A/sigma**3,K=K/sigma**2,b=b/sigma**2,beta=beta/sigma)
    audit.exact('canonical_cubic_chart_invariant',new['A']/new['K']**s.Rational(3,2)-A/K**s.Rational(3,2))
    audit.exact('canonical_regulator_chart_invariant',new['b']/new['K']-b/K)
    audit.exact('canonical_matter_chart_invariant',new['beta']/s.sqrt(new['K'])-beta/s.sqrt(K))
    audit.exact('A_only_physical_change',lam*A/K**s.Rational(3,2)/(A/K**s.Rational(3,2))-lam)
    audit.exact('A_only_not_chart_mutation_rejected',(lam*A/K**s.Rational(3,2)-A/K**s.Rational(3,2)).subs(lam,4),True)
    # z_new=sigma*z and psi_new=sigma*psi preserve all three auxiliary terms.
    z,lap = s.symbols('z lap',real=True)
    audit.exact('auxiliary_chart_rescaling',new['b']*((sigma*z)**2/2+sigma*z*sigma*lap)-b*(z*z/2+z*lap))
    # Bulk energy of a fixed nonzero Fourier mode on a periodic box.
    theta = s.Symbol('theta',real=True)
    amp,k = s.symbols('amp k',positive=True)
    avg_cubic = 2*s.integrate(s.sin(theta)**3,(theta,0,s.pi))/(2*s.pi)
    avg_reg = s.integrate(s.cos(theta)**2,(theta,0,2*s.pi))/(2*s.pi)
    audit.exact('periodic_cubic_mean',avg_cubic-4/(3*s.pi))
    audit.exact('periodic_regulator_mean',b*amp**2*k**4*avg_reg/2-b*amp**2*k**4/4)
    bulk_change = (lam-1)*A*amp**3*k**3*avg_cubic
    audit.exact('periodic_bulk_A_change_not_boundary',bulk_change.subs(lam,4),True)
    # Positive local-gradient branch, with regulator retained in the variation.
    X = s.Symbol('X',real=True)
    psi,rho = s.Function('psi')(X),s.Function('rho')(X)
    L = -A*s.diff(psi,X)**3-b*s.diff(psi,X,2)**2/2-beta*rho*psi
    EL = s.diff(L,psi)-s.diff(s.diff(L,s.diff(psi,X)),X)+s.diff(s.diff(L,s.diff(psi,X,2)),X,2)
    expected = 3*A*s.diff(s.diff(psi,X)**2,X)-b*s.diff(psi,X,4)-beta*rho
    audit.exact('static_flux_and_regulator_sign',EL-expected)
    radial_psi,radial_rho = s.Function('radial_psi')(R),s.Function('radial_rho')(R)
    qR = s.diff(radial_psi,R)
    lapR = s.diff(qR,R)+2*qR/R
    radial_L = R**2*(-A*qR**3-b*lapR**2/2-beta*radial_rho*radial_psi)
    radial_EL = (s.diff(radial_L,radial_psi)-s.diff(s.diff(radial_L,qR),R)
                 +s.diff(s.diff(radial_L,s.diff(radial_psi,R,2)),R,2))/R**2
    radial_flux = R**2*(3*A*qR**2-b*s.diff(lapR,R))
    audit.exact('spherical_regulator_flux_from_action',radial_EL-s.diff(radial_flux,R)/R**2+beta*radial_rho)
    forcegrad = s.sqrt(beta*mass/(12*s.pi*A))/R
    amplitude = s.simplify(R*forcegrad)
    reg_flux = -b*R**2*s.diff(s.diff(forcegrad,R)+2*forcegrad/R,R)
    audit.exact('leading_profile_regulator_flux',reg_flux-2*b*amplitude/R)
    regulator_ratio = s.simplify(reg_flux/(3*A*R**2*forcegrad**2))
    audit.exact('regulator_subleading_ratio',regulator_ratio-2*b/(3*A*amplitude*R))
    audit.exact('spherical_integrated_flux',4*s.pi*R**2*3*A*forcegrad**2-beta*mass)
    audit.exact('missing_factor_three_mutation_rejected',4*s.pi*R**2*A*forcegrad**2-beta*mass,True)
    gbar = G*mass/R**2
    adyn = s.simplify((beta*forcegrad)**2/gbar)
    audit.exact('conditional_acceleration_scale',adyn-beta**3/(12*s.pi*G*A))
    audit.exact('conditional_scale_chart_invariant',new['beta']**3/(12*s.pi*G*new['A'])-adyn)
    audit.exact('force_amplitude_scaling',forcegrad.subs(A,lam*A)/forcegrad-1/s.sqrt(lam))
    audit.exact('fixed_force_mutation_rejected',(forcegrad.subs(A,4*A)-forcegrad),True)
    audit.exact('scale_log_sensitivity_to_A',s.diff(adyn,A)*A/adyn+1)
    cchi = adyn/(Cproj**2*H)
    audit.exact('C_chi_scaling_at_fixed_background',cchi.subs(A,lam*A)/cchi-1/lam)
    # d=sqrt(1-q_dec)>0. These are inverse assignments, never predictions.
    comparators = [('one',s.S.One),('two_pi',2*s.pi),('inverse_two_pi',1/(2*s.pi)),
                   ('curvature',d/(2*s.pi))]
    assignments = {}
    for name,target in comparators:
        needed = beta**3/(12*s.pi*G*Cproj**2*H*target)
        audit.exact(f'reverse_assignment_{name}',cchi.subs(A,needed)-target)
        assignments[name] = str(needed)
    audit.exact('acceleration_mass_dimension',s.Integer(0)-(-2+1)-1)
    return dict(chart='psi_new=sigma psi; z_new=sigma z; K_new=K/sigma^2; A_new=A/sigma^3; b_new=b/sigma^2; beta_new=beta/sigma',
                invariants=['A/K^(3/2)','b/K','beta/sqrt(K)'],
                periodic_energy_density='4 A amp^3 k^3/(3 pi)+b amp^2 k^4/4; k=2 pi |n|/L',
                static_equation='3 A div(|grad psi| grad psi)-b Delta^2 psi=beta rho',
                static_scope='positive beta, frozen local frame, spherical compensated/local patch; regulator-subleading force formula only',
                radial_integrated_flux='4 pi R^2 [3 A q^2-b d(q_prime+2q/R)/dR]=beta M(<R)',
                leading_profile_regulator_ratio=str(regulator_ratio),
                approximation_hold='require 2b/(3A amplitude R)<<1 plus weak potential, local/quasistatic and backreaction bounds; no common domain proved',
                force_amplitude=str(forcegrad),a_dynamic=str(adyn),
                projection_relation='a_dynamic=C_proj^2 a0; C_proj not derived',
                target_sensitivity='at fixed H and other coefficients, C_chi scales as 1/A in this conditional reduction',
                inverse_assignments=assignments,
                inverse_assignment_scope='arbitrary target insertion exposed, not a permitted matching prescription',
                redshift_prediction='NOT_DERIVED: physical local matching and C_proj remain open')


def background_controls(audit):
    grid = np.linspace(0.,4.,801)
    factors = (.25,1.,4.)
    runs = {}
    for factor in factors:
        p = {**bg.PARAMS,'A':factor*bg.PARAMS['A']}
        sol = bg.integrate(p,'DOP853',1e-11,1e-13)
        y = sol.sol(grid)
        summary = bg.summarize_solution(sol,p)
        audit.numeric(f'A_factor_{factor}_integration',summary['success'] and summary['all_finite'],
                      summary['message'],'completed [0,4] and all finite')
        for key in ('max_normalized_Friedmann','max_charge_drift','max_dust_integral_drift'):
            audit.numeric(f'A_factor_{factor}_{key}',summary[key]<1e-8,summary[key],'<1e-8')
        runs[factor] = (p,y,bg.physics(y,p),summary)
    base_y,base_data = runs[1.][1:3]
    rows = []
    for factor in factors:
        p,y,data,summary = runs[factor]
        trajectory = float(np.max(np.abs(y-base_y)/(1+np.abs(base_y))))
        current_diff = max(float(np.max(np.abs(data[k]-base_data[k])/(1+np.abs(base_data[k]))))
                           for k in ('Qmp','Qsyn','charge','dust_integral','hdot'))
        audit.numeric(f'A_factor_{factor}_background_degeneracy',trajectory<1e-12,trajectory,'<1e-12')
        audit.numeric(f'A_factor_{factor}_current_degeneracy',current_diff<1e-12,current_diff,'<1e-12')
        rows.append(dict(A_factor=factor,trajectory_difference=trajectory,current_difference=current_diff,
                         states_exactly_equal=bool(np.array_equal(y,base_y)),
                         canonical_cubic_ratio=factor,conditional_force_ratio=factor**(-.5),
                         conditional_a_dynamic_ratio=1/factor,
                         max_Friedmann=summary['max_normalized_Friedmann'],
                         charge_drift=summary['max_charge_drift'],dust_drift=summary['max_dust_integral_drift']))
    changed_p = {**bg.PARAMS,'K':4*bg.PARAMS['K']}
    changed = bg.integrate(changed_p,'DOP853',1e-11,1e-13)
    changed_y = changed.sol(grid)
    control_diff = float(np.max(np.abs(changed_y-base_y)/(1+np.abs(base_y))))
    audit.numeric('K_positive_sensitivity_control',changed.success and np.all(np.isfinite(changed_y)) and control_diff>1e-6,
                  control_diff,'completed, finite and >1e-6')
    return dict(rows=rows,K_times_four_trajectory_difference=control_diff,
                interpretation='exact ODE degeneracy control; not independent integrator or stability validation')


def main():
    for name,expected in PINS.items():
        if sha(ROOT/name)!=expected:
            raise RuntimeError(f'FROZEN_INPUT_HASH_MISMATCH: {name}')
    audit = Audit()
    homogeneous = homogeneous_variation(audit)
    quadratic = quadratic_regularity(audit)
    matching = invariant_and_static_checks(audit)
    backgrounds = background_controls(audit)
    passed = sum(item['passed'] for item in audit.checks)
    record = dict(candidate='R4C1-v1',control='R4C1-C1',validation='PASS' if passed==len(audit.checks) else 'FAIL',
                  passed=passed,total=len(audit.checks),checks=audit.checks,
                  homogeneous=homogeneous,quadratic=quadratic,matching=matching,backgrounds=backgrounds,
                  source_sha256=PINS,script_sha256=sha(Path(__file__)),
                  status='CLASSICAL_BACKGROUND_AND_LINEAR_DATA_DO_NOT_IDENTIFY_SPATIAL_FORCE_COEFFICIENT',
                  independent_blinding=False,observed_acceleration_input=False,coefficient_selected=False,
                  C_chi='NOT_DERIVED',a0_redshift='NOT_DERIVED',physical_B1_Hessian_verified=False,
                  quantum_matching='NOT_COMPUTED',canonical_Test3_pass=False,physics_pass=False,
                  gate_effect='NONE',Rule9='NOT_CLEARED')
    record.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','K_Q':'NOT_DERIVED','V':'NOT_COMPUTED','Stage4A':'CLOSED'})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    OUT.with_suffix(OUT.suffix+'.sha256').write_text(f'{sha(OUT)}  {OUT.name}\n',encoding='ascii')
    print(json.dumps({key:record[key] for key in ('validation','passed','total','status','physics_pass')}))
    print(json.dumps(backgrounds))
    for check in audit.checks:
        if not check['passed']:
            print(json.dumps(check))
    return 0 if passed==len(audit.checks) else 1


if __name__=='__main__':
    raise SystemExit(main())
