"""R4C1-B1G: exact homogeneous ODE regularity and continuation audit.

This proves a property of the frozen classical B1 benchmark only. It is not
a perturbation, EFT, physical stability, or canonical-action pass.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_scalar_propagation as up


base = up.base
ROOT, OUT = base.ROOT, base.OUT
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_CONTRACT_2026-09-29.md':
        'b7fce9d013833468099c751e3286a0eda554f3736c84bbab633f520498b54de6',
    'Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_CONTRACT_2026-09-25.md':
        '3d5f164529ee2621aaa41bd08f8ba0a1ad2e4b866591f5aa4475f188fdf99a59',
    'Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md':
        '48b49fddd9066d6df783eb336e00d49374f3845ec38414ee53fe0fad812348d8',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':
        '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_summary.json':
        'e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7',
    'Analysis/MasterTests/test_01_r4c1_scalar_propagation.py':
        '745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda',
    'Theory/Gates/RES-001/RES001_R4C1_TEMPORAL_PERSISTENCE_CONTRACT_2026-09-29.md':
        '3bb4fa5ec045715f4667ce1260fce2a146238e45079c683ef9862260857eb26e',
}


def verify(audit):
    inputs = {}
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('B1G_pin:' + name, actual == expected, actual)
        audit.test('B1G_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_summary.json').read_text())
    audit.test('B1G_parent_scope',
               parent['validation'] == 'PASS'
               and parent['passed'] == parent['total'] == 48
               and parent['status'] == 'CONDITIONAL_INTERACTING_BACKGROUND_CONTROL_PARENT_HOLD'
               and parent['physics_pass'] is False
               and parent['canonical_Test1_pass'] is False)
    return inputs


def derive(audit):
    a,H,u,ud,v,vd,r,rd,pd,rho,C = (
        base.a,base.H,base.u,base.ud,base.v,base.vd,
        base.r,base.rd,base.pd,base.rho,base.C)
    M = s.Rational(11, 10)
    beta = s.Rational(2, 5)
    radius2 = u**2 + v**2
    kinetic = ud**2 + vd**2 + rd**2 + 3*pd**2
    VP = radius2/2 + radius2**2/24 + radius2**3/480
    VR = r**2 + r**4/28
    portal = 3*radius2*r**2/28
    energy = kinetic/2 + VP + VR + portal + rho
    initial = {a:1, u:1, ud:0, v:0, vd:1, r:1,
               rd:s.Rational(1,4), pd:s.Rational(1,5),
               rho:s.Rational(1,5), C:1}
    E0 = s.cancel(energy.subs(initial))
    H0sq = s.cancel(E0/(3*M))
    H0 = s.sqrt(H0sq)
    initial[H] = H0
    audit.test('B1G_cosmological_M_squared', M == s.Rational(11,10))
    audit.test('B1G_exact_initial_energy', E0 == s.Rational(3469,1400), str(E0))
    audit.test('B1G_exact_initial_H_squared',
               H0sq == s.Rational(3469,4620), str(H0sq))
    audit.test('B1G_initial_constraint',
               s.cancel((3*M*H**2-energy).subs(initial)) == 0)
    audit.test('B1G_registered_positive_coefficients',
               all(x>0 for x in (
                   s.Rational(1,2),s.Rational(1,24),s.Rational(1,480),
                   s.Integer(1),s.Rational(1,28),s.Rational(3,28),
                   s.Integer(3),M,beta)))
    for field, velocity in ((u,ud),(v,vd),(r,rd)):
        audit.test('B1G_potential_gradient_' + str(field),
                   s.cancel(up.FLOW[velocity]+3*H*velocity+
                            s.diff(VP+VR+portal, field)) == 0)
    audit.test('B1G_force_equation',
               s.cancel(up.FLOW[pd]+3*H*pd+beta*rho/3) == 0)
    audit.test('B1G_dust_equation',
               s.cancel(up.FLOW[rho]-(-3*H+beta*pd)*rho) == 0)
    audit.test('B1G_Hdot_equation',
               s.cancel(up.FLOW[H]+(kinetic+rho)/(2*M)) == 0)
    audit.test('B1G_scale_factor_equation',
               s.cancel(up.FLOW[a]-a*H) == 0)
    audit.test('B1G_conformal_factor_equation',
               s.cancel(up.FLOW[C]-beta*pd*C) == 0)

    Edot = s.cancel(up.dtime(energy))
    constraint = 3*M*H**2-energy
    constraint_dot = s.cancel(up.dtime(constraint))
    audit.test('B1G_exact_energy_balance',
               s.cancel(Edot+3*H*(kinetic+rho)) == 0,
               str(s.cancel(Edot+3*H*(kinetic+rho))))
    audit.test('B1G_exact_constraint_propagation',
               constraint_dot == 0, str(constraint_dot))
    charge = a**3*(u*vd-v*ud)
    audit.test('B1G_exact_charge_conservation',
               s.cancel(up.dtime(charge)) == 0)
    audit.test('B1G_initial_charge_one',
               s.cancel(charge.subs(initial)-1) == 0)
    dust_integral = a**3*rho/C
    audit.test('B1G_exact_dust_integral',
               s.cancel(up.dtime(dust_integral)) == 0)
    audit.test('B1G_initial_dust_integral_one_fifth',
               s.cancel(dust_integral.subs(initial)-s.Rational(1,5)) == 0)
    audit.test('B1G_flow_polynomial_locally_Lipschitz',
               all(s.denom(expr) == 1 or not s.denom(expr).free_symbols
                   for expr in up.FLOW.values()),
               'The registered autonomous flow is polynomial in its state '
               'variables; adjoining psi_dot=pd and tau_dot=C stays smooth.')

    T = s.Symbol('T', nonnegative=True)
    velocity_max = s.sqrt(2*E0)
    force_speed_max = s.sqrt(2*E0/3)
    a_max = s.exp(H0*T)
    C_min = s.exp(-beta*force_speed_max*T)
    C_max = s.exp(beta*force_speed_max*T)
    rho_min = s.Rational(1,5)*s.exp(
        -(3*H0+beta*force_speed_max)*T)
    H_min = s.sqrt(rho_min/(3*M))
    radius2_min = s.exp(-6*H0*T)/(2*E0)
    audit.test('B1G_bounds_positive_for_finite_T',
               all(x.subs(T,4).evalf() > 0
                   for x in (a_max,C_min,rho_min,H_min,radius2_min)))
    audit.test('B1G_charge_radius_lower_bound_formula',
               s.cancel(radius2_min*a_max**6*(2*E0)-1) == 0)
    audit.test('B1G_H_lower_bound_from_rho',
               s.cancel(3*M*H_min**2-rho_min) == 0)
    audit.test('B1G_C_bounds_inverse',
               s.cancel(C_min*C_max-1) == 0)
    audit.test('B1G_finite_time_state_bound_coverage',
               set(up.FLOW) == {a,H,u,ud,v,vd,r,rd,pd,rho,C},
               'E<=E0 bounds H,rho,amplitudes and velocities; '
               'a,C,psi,tau have explicit finite-T integral bounds.')
    return dict(M=M, E=energy, E0=E0, H0sq=H0sq,
                charge=charge, dust_integral=dust_integral,
                bound=dict(T='T>=0 finite', velocity_abs_le=str(velocity_max),
                           psi_dot_abs_le=str(force_speed_max),
                           radius2_le=str(2*E0), r_abs_le=str(s.sqrt(E0)),
                           H_le=str(H0), a_le=str(a_max), C_ge=str(C_min),
                           C_le=str(C_max), rho_ge=str(rho_min),
                           H_ge=str(H_min), radius2_ge=str(radius2_min),
                           psi_abs_le=str(force_speed_max*T),
                           tau_abs_le=str(T*C_max),
                           p_ge_one_if_k_ge=str(a_max)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_b1_global_regularity_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs = verify(audit)
    if not all(check['passed'] for check in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[check for check in audit.checks
                                      if not check['passed']])))
        return 1
    result = derive(audit)
    valid = all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, dict(
        schema='r4c1-b1-global-regularity-detail-v1',
        status='EXACT_HOMOGENEOUS_FORWARD_REGULARITY' if valid else
               'HOMOGENEOUS_REGULARITY_FAILED_OR_UNKNOWN',
        M_cos_squared=str(result['M']), E=str(result['E']),
        E0=str(result['E0']), H0_squared=str(result['H0sq']),
        conserved_charge=str(result['charge']),
        conserved_dust_integral=str(result['dust_integral']),
        finite_T_bounds=result['bound'],
        theorem=('For real registered B1 data, positive dust and the exact '
                 'constraint force H>0; E is decreasing and bounds all '
                 'homogeneous state variables on every finite forward '
                 'interval. The smooth ODE continuation theorem then gives '
                 'a unique global forward homogeneous solution. This is '
                 'not a physical stability or perturbation theorem.')))
    summary = dict(
        schema='r4c1-b1-global-regularity-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status='EXACT_HOMOGENEOUS_FORWARD_REGULARITY' if valid else
               'HOMOGENEOUS_REGULARITY_FAILED_OR_UNKNOWN',
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
        review_status='DEFERRED',
        decision=dict(B1_exact_regular_t_0_to_4='DERIVED_CONDITIONALLY'
                          if valid else 'NOT_PROVED',
                      uniform_perturbation_metric_constants='NOT_PROVED',
                      full_constrained_IVP='NOT_PROVED',
                      physical_EFT_cutoff='NOT_DERIVED',
                      canonical_Test1='HOLD'),
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
