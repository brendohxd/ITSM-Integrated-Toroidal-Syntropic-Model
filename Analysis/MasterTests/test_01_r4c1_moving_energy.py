"""R4C1-S4H: pointwise formal high-p energy-rate screen on moving B1.

This is an exact rational/symbolic calculation at each regular state. It
does not establish an interval-uniform constant, exact B1 existence on
[0,4], constraint propagation, or a physical EFT wave-number domain.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_moving_metric as previous


principal = previous.previous.previous
prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
PINS = {
    'Analysis/MasterTests/test_01_r4c1_moving_metric.py':
        '15dc947f35e9d3b03049bba4352a1e5c47b34bf12edc77d3c5252d33a683c3cf',
    'Analysis/MasterTests/outputs/r4c1_s4h_metric_attempt_01/summary.json':
        'f4ccfbb01969d848bc5390da5cd7008e4fd5ce14e2d2ef7109156189291e0020',
    'Analysis/MasterTests/outputs/r4c1_s4h_metric_attempt_01/detail.json':
        'c743348c84385ecd576d3a196f7e37f843d72ee2654b50d94deebf99611086a5',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4H6_pin:' + name, actual == expected, actual)
        audit.test('S4H6_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    parent = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_metric_attempt_01/summary.json').read_text())
    audit.test('S4H6_parent_scope',
               parent['validation'] == 'PASS_LOCAL_CHECKS'
               and parent['status'] == 'MOVING_FORMAL_METRIC_POINTWISE_ONLY'
               and parent['physics_pass'] is False
               and parent['Rule9_cleared'] is False)
    return inputs


def parse(name, field):
    raw = json.loads((ROOT / name).read_text())
    return s.Matrix([[s.sympify(x, locals=prior.SYMBOLS) for x in row]
                     for row in raw[field]])


def finite(expr):
    return not expr.has(s.oo, -s.oo, s.zoo, s.nan)


def derive(audit):
    p, C = principal.moving_matrices(audit)
    principal_path = ('Analysis/MasterTests/outputs/'
                      'r4c1_s4h_principal_attempt_01/detail.json')
    metric_path = ('Analysis/MasterTests/outputs/'
                   'r4c1_s4h_metric_attempt_01/detail.json')
    C2, C1 = parse(principal_path, 'C2'), parse(principal_path, 'C1')
    M0, M1 = parse(metric_path, 'M0'), parse(metric_path, 'M1')
    R = s.Matrix(12, 12, lambda i, j:
                 s.cancel(C[i, j] - p**2*C2[i, j] - p*C1[i, j]))

    finite_limits = 0
    p_factors = set()
    S = (396*base.H**2 + 18*base.pd**2
         + 6*(base.rd**2 + base.ud**2 + base.vd**2))
    for i in range(12):
        print(f'S4H6 bounded rational remainder row {i}/11', flush=True)
        for j in range(12):
            limit = s.cancel(s.limit(R[i, j], p, s.oo))
            good = finite(limit) and not limit.has(p)
            audit.test(f'S4H6_finite_C_remainder_{i}_{j}', good,
                       str(limit)[:180])
            finite_limits += int(good)
            denominator = s.denom(C[i, j])
            _, factors = s.factor_list(denominator, p)
            for factor, _ in factors:
                monic = s.Poly(factor, p).monic().as_expr()
                p_factors.add(str(monic))
                audit.test(f'S4H6_no_unregistered_p_pole_{i}_{j}_{len(p_factors)}',
                           s.cancel(monic-p) == 0
                           or s.cancel(monic-(p**2+S)) == 0,
                           str(monic))
    audit.test('S4H6_all_144_bounded', finite_limits == 144, finite_limits)

    radius2 = base.u**2 + base.v**2
    allowed = (base.H, radius2, radius2+13, 3*radius2+26)
    metric_factors = set()
    for matrix in (M0, M1):
        for expr in matrix:
            if expr == 0:
                continue
            _, factors = s.factor_list(s.denom(s.cancel(expr)))
            for factor, _ in factors:
                metric_factors.add(str(factor))
                audit.test('S4H6_metric_pole_' + str(len(audit.checks)),
                           any(s.cancel(factor / candidate).is_number
                               and s.cancel(factor / candidate) != 0
                               for candidate in allowed),
                           str(factor))

    print('S4H6 differentiating moving metric through full B1 flow...', flush=True)
    M0dot = M0.applyfunc(up.dtime)
    M1dot = M1.applyfunc(up.dtime)
    audit.test('S4H6_metric_flow_derivatives_no_p',
               all(not entry.has(p) for entry in M0dot)
               and all(not entry.has(p) for entry in M1dot))
    audit.test('S4H6_metric_flow_derivatives_finite_regular',
               all(finite(entry) for entry in M0dot)
               and all(finite(entry) for entry in M1dot),
               'Rational derivatives are finite where their inherited '
               'denominators are nonzero; interval suprema not computed.')
    S2 = (M0*C2 + C2.T*M0).applyfunc(s.cancel)
    S1 = (M0*C1 + C1.T*M0 + M1*C2 + C2.T*M1).applyfunc(s.cancel)
    audit.test('S4H6_exact_p2_energy_cancellation', all(x == 0 for x in S2))
    audit.test('S4H6_exact_p_energy_cancellation', all(x == 0 for x in S1))
    audit.test('S4H6_full_moving_Mdot_formula',
               not any(entry.has(p) for entry in M0dot)
               and not any(entry.has(p) for entry in M1dot),
               'Mdot=M0dot+(M1dot+H*M1)/p, from pdot=-Hp; '
               'M0dot and M1dot use every registered B1 flow component.')
    return dict(denominator_factors=sorted(p_factors),
                metric_denominator_factors=sorted(metric_factors),
                finite_remainder_limits=finite_limits,
                energy_identity=(
                    'E=M0*R+R.T*M0+M1*C1+C1.T*M1+M0dot+'
                    '(M1*R+R.T*M1+M1dot+H*M1)/p after exact p2/p cancellation'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_energy_attempt_{args.attempt:02d}'
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
        schema='r4c1-s4h-moving-energy-detail-v1',
        status='POINTWISE_FORMAL_HIGH_P_ENERGY_RATE' if valid else
               'POINTWISE_ENERGY_FAILED_OR_UNKNOWN',
        p_denominator_factors=result['denominator_factors'],
        metric_denominator_factors=result['metric_denominator_factors'],
        finite_C_remainder_limits=result['finite_remainder_limits'],
        energy_identity=result['energy_identity'],
        positivity_condition='p>=max(1,8*||M1(t)||_F) gives M>=I/8 '
                             'at each regular B1 state; no uniform p0',
        domain='conditional finite regular B1 state; exact [0,4] existence '
               'and physical p cutoff unproved'))
    summary = dict(
        schema='r4c1-s4h-moving-energy-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status='POINTWISE_FORMAL_HIGH_P_ENERGY_RATE' if valid else
               'POINTWISE_ENERGY_FAILED_OR_UNKNOWN',
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
        review_status='DEFERRED',
        decision=dict(moving_C2_C1_144='EXACT_FORMULAS',
                      moving_slow_spectrum='CONDITIONAL_REGULAR_B1',
                      moving_metric='POINTWISE_FORMAL',
                      pointwise_energy_rate='BOUNDED_FORMAL' if valid
                          else 'NOT_PROVED',
                      uniform_interval_energy_constant='NOT_PROVED',
                      full_constrained_IVP='NOT_PROVED',
                      physical_EFT_cutoff='NOT_DERIVED'),
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={detailpath.relative_to(ROOT).as_posix(): base.sha(detailpath)},
        checks=audit.checks)
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
