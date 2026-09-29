"""S4H-U: exact coefficient-envelope attempt on the regular B1 interval.

This bounds a formal reduced nonzero-mode graph only. It cannot determine a
physical EFT cutoff, full constrained IVP, GR limit, or parent physics pass.
Earlier receipt-writing main functions are imported but never invoked.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import sympy as s

import test_01_r4c1_moving_energy as previous


principal = previous.principal
prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
CONTRACT = ('Theory/Gates/RES-001/'
            'RES001_R4C1_S4H_UNIFORM_ENVELOPE_CONTRACT_2026-09-29.md')
PINS = {
    CONTRACT: '4cc4c76f1687e667eacd2a755f6c841c0f25493ef140c0724575a352866c0dbb',
    'Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md':
        '82708666dfce4ef214b614bc7da31b294d7569539b97292aaa9a79e906e6266f',
    'Analysis/MasterTests/test_01_r4c1_moving_energy.py':
        '53530ef536f9724833a79263c26130173bfcbcc8bc87b53fca3c151b7edaf059',
    'Analysis/MasterTests/outputs/r4c1_s4h_energy_attempt_01/summary.json':
        '402b9fc09f018d7a99872cfd4de3a3428f35324d51c70ff5604edce6281faabc',
    'Analysis/MasterTests/outputs/r4c1_s4h_energy_attempt_01/detail.json':
        '5d5e0fc8e065988c7d85bf98dfaa25c968f20975e6046071d1962625f3ea2c3a',
    'Analysis/MasterTests/outputs/r4c1_b1_global_regularity_attempt_01/summary.json':
        'f28578a16cda58f907e5c8af97023aedfb818919b2eff131a70dbaf70f767caa',
}

P = s.Symbol('p', positive=True)
STATE = (base.H, base.u, base.v, base.ud, base.vd, base.r,
         base.rd, base.pd, base.rho, base.a, base.C)
GENERATORS = STATE + (P,)
UPPER = {
    base.H: 1, base.u: 3, base.v: 3, base.ud: 3, base.vd: 3,
    base.r: 2, base.rd: 3, base.pd: 2, base.rho: 3,
    base.a: 60, base.C: 60,
}
RADIAL2 = base.u**2 + base.v**2
S = (396*base.H**2 + 18*base.pd**2
     + 6*(base.rd**2 + base.ud**2 + base.vd**2))
LOWER_FACTORS = (
    ('H', base.H, s.Rational(1, 10**5), 0),
    ('radial2', RADIAL2, s.Rational(1, 10**12), 0),
    ('radial2_plus_13', RADIAL2+13, s.Integer(13), 0),
    ('three_radial2_plus_26', 3*RADIAL2+26, s.Integer(26), 0),
    ('rho_m', base.rho, s.Rational(1, 10**9), 0),
    ('a', base.a, s.Integer(1), 0),
    ('C', base.C, s.Rational(1, 60), 0),
    ('p', P, s.Integer(1), 1),
    ('p2_plus_S', P**2+S, s.Integer(1), 2),
)


class EnvelopeFailure(RuntimeError):
    """A symbolic certification obligation is unproved."""


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4HU_pin:' + name, actual == expected, actual)
        audit.test('S4HU_sidecar:' + name,
                   sidecar.exists()
                   and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    b1 = json.loads((ROOT /
        'Analysis/MasterTests/outputs/'
        'r4c1_b1_global_regularity_attempt_01/summary.json').read_text())
    audit.test('S4HU_B1_scope',
               b1['validation'] == 'PASS_LOCAL_CHECKS'
               and b1['status'] == 'EXACT_HOMOGENEOUS_FORWARD_REGULARITY'
               and b1['decision']['B1_exact_regular_t_0_to_4']
                   == 'DERIVED_CONDITIONALLY'
               and b1['physics_pass'] is False
               and b1['Rule9_cleared'] is False)
    return inputs


def prove_box(audit):
    """Verify rational inequalities used to enclose the exact B1 solution."""
    e0 = s.Rational(3469, 1400)
    h02 = s.Rational(3469, 4620)
    e_upper = s.Rational(11, 4)
    partial = sum((s.Rational(1, math.factorial(n))
                   for n in range(5)), s.Integer(0))
    tail_bound = s.Rational(1, 120)/(1-s.Rational(1, 6))
    tests = {
        'e_series_upper': partial+tail_bound < e_upper,
        'initial_energy_and_H_bounds': 0 < e0 < s.Rational(5, 2)
                                      and 0 < h02 < 1,
        'velocity_and_phase_bounds': 2*e0 < 9
                                     and 2*e0/3 < 4,
        'exp4_under_60': e_upper**4 < 60,
        'exp16_under_1e8': e_upper**16 < 10**8,
        'exp24_under_1e11': e_upper**24 < 10**11,
        'dust_lower': 1/(5*e_upper**16) > s.Rational(1, 10**9),
        'H_lower': 1/(5*e_upper**16)/(s.Rational(33, 10))
                   > s.Rational(1, 10**10),
        'radial2_lower': 1/(5*e_upper**24)
                         > s.Rational(1, 10**12),
    }
    for name, result in tests.items():
        audit.test('S4HU_box_' + name, bool(result), str(result))
    if not all(tests.values()):
        raise EnvelopeFailure('The proposed rational B1 box was not proved')
    return {
        'time_interval': '[0,4]',
        'H': '[1e-5,1]',
        'radial2': '[1e-12,5]',
        'rho_m': '[1e-9,3]',
        'a': '[1,60]',
        'C': '[1/60,60]',
        'field_velocity_upper_bounds': {
            'u,v,u_dot,v_dot,r_dot': 3,
            'r,psi_dot': 2,
        },
        'source': 'B1G exact energy, dust and angular-charge invariants',
    }


def read_matrix(name, field):
    raw = json.loads((ROOT / name).read_text())
    return s.Matrix([
        [s.sympify(value, locals=prior.SYMBOLS) for value in row]
        for row in raw[field]
    ])


def classify_factor(factor):
    for name, reference, lower, pdegree in LOWER_FACTORS:
        ratio = s.cancel(factor/reference)
        if ratio.is_number and ratio.is_real and ratio.is_nonzero:
            return name, s.Abs(ratio)*lower, pdegree
    raise EnvelopeFailure('Unrecognized denominator factor: '
                          + str(factor)[:300])


def coefficient_ceiling(coefficient):
    if coefficient.free_symbols:
        raise EnvelopeFailure('Numerator coefficient retains symbols: '
                              + str(coefficient)[:200])
    ceiling = s.ceiling(s.Abs(coefficient))
    if not ceiling.is_Integer:
        raise EnvelopeFailure('Algebraic coefficient ceiling unresolved: '
                              + str(coefficient)[:200])
    return int(ceiling)


def bound_entry(expression):
    """Exact rational bound uniform on the certified box and p>=1."""
    expression = s.cancel(expression)
    if expression == 0:
        return 0, (), 0
    unknown = expression.free_symbols - set(GENERATORS)
    if unknown:
        raise EnvelopeFailure('Unrecognized free symbols: '
                              + ', '.join(sorted(map(str, unknown))))
    numerator, denominator = s.fraction(expression)
    scalar, factors = s.factor_list(denominator)
    if not scalar.is_number or not scalar.is_real or scalar == 0:
        raise EnvelopeFailure('Nonreal or zero denominator scalar: '
                              + str(scalar))
    denominator_lower = s.Abs(scalar)
    denominator_pdegree = 0
    classes = []
    for factor, exponent in factors:
        name, lower, pdegree = classify_factor(factor)
        denominator_lower *= lower**exponent
        denominator_pdegree += pdegree*exponent
        classes.append((name, int(exponent)))
    polynomial = s.Poly(numerator, *GENERATORS, domain='EX')
    numerator_upper = 0
    for monomial, coefficient in polynomial.terms():
        pdegree = monomial[-1]
        if pdegree > denominator_pdegree:
            raise EnvelopeFailure(
                'Numerator p-degree exceeds certified denominator p-degree: '
                + str(pdegree) + ' > ' + str(denominator_pdegree))
        term = coefficient_ceiling(coefficient)
        for variable, exponent in zip(STATE, monomial[:-1]):
            term *= UPPER[variable]**exponent
        numerator_upper += term
    if denominator_lower <= 0:
        raise EnvelopeFailure('Nonpositive certified denominator lower bound')
    bound = s.ceiling(s.Rational(numerator_upper)/denominator_lower)
    if not bound.is_Integer:
        raise EnvelopeFailure('Entrywise rational bound did not resolve')
    return int(bound), tuple(sorted(classes)), denominator_pdegree


def bound_matrix(audit, name, matrix):
    print('S4HU bounding ' + name + '...', flush=True)
    values, factors = [], set()
    failures = []
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            try:
                bound, classes, degree = bound_entry(matrix[i, j])
                values.append(bound)
                factors.update(classes)
                audit.test(f'S4HU_{name}_{i}_{j}', True,
                           f'bound={bound}; denom_pdegree={degree}')
            except (EnvelopeFailure, s.PolynomialError) as exc:
                failures.append((i, j, str(exc)))
                audit.test(f'S4HU_{name}_{i}_{j}', False, str(exc))
    if failures:
        raise EnvelopeFailure(
            name + ': ' + str(len(failures)) + ' unbounded entries; '
            + str(failures[:6]))
    return {
        'entrywise_max': str(max(values, default=0)),
        'nonzero_bounds': sum(value != 0 for value in values),
        'denominator_factor_classes': sorted([list(x) for x in factors]),
        'frobenius_power10': power10_ceiling(12*max(values, default=0)),
    }


def power10_ceiling(value):
    if value <= 1:
        return 0
    exponent, power = 0, 1
    while power < value:
        power *= 10
        exponent += 1
    return exponent


def exercise_envelope_controls(audit):
    """Reject unsafe poles, uncontrolled p growth and undeclared variables."""
    positive = (
        ('registered_product_pole',
         1/(base.H*RADIAL2), 10**17),
        ('positive_dynamic_denominator',
         P**2/(P**2+S), 1),
    )
    for name, expression, expected in positive:
        bound, _, _ = bound_entry(expression)
        audit.test('S4HU_control_' + name, bound == expected, str(bound))
    negative = (
        ('unregistered_pole', 1/(RADIAL2-1),
         'Unrecognized denominator factor'),
        ('excess_p_degree', P**3/(P**2+S),
         'Numerator p-degree exceeds'),
        ('unregistered_symbol', s.Symbol('unregistered'),
         'Unrecognized free symbols'),
    )
    for name, expression, expected in negative:
        try:
            bound_entry(expression)
        except EnvelopeFailure as exc:
            audit.test('S4HU_control_' + name, expected in str(exc),
                       str(exc)[:240])
        else:
            audit.test('S4HU_control_' + name, False,
                       'Mutation was incorrectly certified')


def derive(audit):
    box = prove_box(audit)
    exercise_envelope_controls(audit)
    if not all(check['passed'] for check in audit.checks):
        raise EnvelopeFailure('An envelope rejection control failed')
    p, C = principal.moving_matrices(audit)
    audit.test('S4HU_same_p_symbol', p == P, str(p))
    if p != P:
        raise EnvelopeFailure('Moving generator p symbol differs')
    principal_path = ('Analysis/MasterTests/outputs/'
                      'r4c1_s4h_principal_attempt_01/detail.json')
    metric_path = ('Analysis/MasterTests/outputs/'
                   'r4c1_s4h_metric_attempt_01/detail.json')
    C2 = read_matrix(principal_path, 'C2')
    C1 = read_matrix(principal_path, 'C1')
    M0 = read_matrix(metric_path, 'M0')
    M1 = read_matrix(metric_path, 'M1')
    p2 = (M0*C2+C2.T*M0).applyfunc(s.cancel)
    p1 = (M0*C1+C1.T*M0+M1*C2+C2.T*M1).applyfunc(s.cancel)
    audit.test('S4HU_exact_p2_cancellation', all(x == 0 for x in p2))
    audit.test('S4HU_exact_p_cancellation', all(x == 0 for x in p1))
    if any(x != 0 for x in p2) or any(x != 0 for x in p1):
        raise EnvelopeFailure('A moving energy cancellation failed')
    R = s.Matrix(12, 12, lambda i, j: s.cancel(
        C[i, j]-p**2*C2[i, j]-p*C1[i, j]))
    M0dot = M0.applyfunc(up.dtime)
    M1dot = M1.applyfunc(up.dtime)
    matrices = {
        'M0': M0, 'M1': M1, 'C1': C1, 'M0dot': M0dot,
        'M1dot': M1dot, 'R': R,
    }
    bounds = {}
    for name, matrix in matrices.items():
        bounds[name] = bound_matrix(audit, name, matrix)
    B = {name: 10**info['frobenius_power10']
         for name, info in bounds.items()}
    p0 = max(1, 8*B['M1'])
    upper_metric = s.Rational(B['M0'])+s.Rational(B['M1'], p0)
    BE = (2*B['M0']*B['R']+2*B['M1']*B['C1']+B['M0dot']
          + s.Rational(2*B['M1']*B['R']+B['M1dot']+B['M1'], p0))
    K = 8*BE
    K_power = power10_ceiling(K)
    audit.test('S4HU_positive_formal_mode_domain',
               p0 >= 8*B['M1'] and p0 >= 1)
    audit.test('S4HU_uniform_metric_lower',
               s.Rational(1, 4)-s.Rational(B['M1'], p0)
               >= s.Rational(1, 8))
    audit.test('S4HU_uniform_metric_upper',
               upper_metric >= B['M0'])
    audit.test('S4HU_energy_rate_power10',
               10**K_power >= K)
    return {
        'box': box, 'matrix_bounds': bounds,
        'formal_p0': str(p0),
        'formal_p0_expression': '8*10^'
            + str(bounds['M1']['frobenius_power10']),
        'comoving_k_min': str(60*p0),
        'sufficient_axial_torus_index': str(10*p0),
        'metric_lower': '1/8',
        'metric_upper': str(upper_metric),
        'energy_rate_BE': str(BE),
        'gronwall_rate_K_power10': K_power,
        'physical_EFT_cutoff': 'NOT_DERIVED',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_uniform_attempt_{args.attempt:02d}'
    if target.exists():
        raise SystemExit('Preserved attempt already exists: ' + str(target))
    audit = up.Audit()
    inputs, result, error = {}, None, None
    try:
        inputs = verify(audit)
        if not all(check['passed'] for check in audit.checks):
            raise EnvelopeFailure('Pinned source or parent scope failed')
        result = derive(audit)
    except (EnvelopeFailure, s.PolynomialError, ValueError) as exc:
        error = str(exc)
        audit.test('S4HU_attempt_failure', False, error[:1000])
    valid = error is None and all(check['passed'] for check in audit.checks)
    target.mkdir(parents=True)
    detailpath = target / 'detail.json'
    base.write_json(detailpath, {
        'schema': 'r4c1-s4h-uniform-envelope-detail-v1',
        'status': 'FORMAL_UNIFORM_INTERVAL_ENVELOPE' if valid
                  else 'INCOMPLETE_UNIFORM_ENVELOPE',
        'result': result, 'error': error,
        'assumptions': 'Conditional classical regular B1; t in [0,4]; '
            'p>=p0; fixed comoving k; no physical EFT cutoff',
    })
    summary = {
        'schema': 'r4c1-s4h-uniform-envelope-summary-v1',
        'validation': 'PASS_LOCAL_CHECKS' if valid else 'FAIL_OR_UNKNOWN',
        'passed': sum(check['passed'] for check in audit.checks),
        'total': len(audit.checks),
        'status': 'FORMAL_UNIFORM_INTERVAL_ENVELOPE' if valid
                  else 'INCOMPLETE_UNIFORM_ENVELOPE',
        'physics_pass': False, 'gate_effect': 'NONE',
        'Rule9_cleared': False, 'review_status': 'DEFERRED',
        'decision': {
            'formal_S4H_step4': 'PROVED_ON_DECLARED_FORMAL_DOMAIN'
                                 if valid else 'NOT_PROVED',
            'physical_EFT_cutoff': 'NOT_DERIVED',
            'full_constrained_IVP': 'NOT_PROVED',
            'canonical_Test1': 'HOLD',
            'Tests2_3': 'INCOMPLETE',
        },
        'inputs': inputs, 'executable_sha256': base.sha(Path(__file__)),
        'artifacts': {detailpath.relative_to(ROOT).as_posix():
                      base.sha(detailpath)},
        'checks': audit.checks,
    }
    base.write_json(target / 'summary.json', summary)
    print(json.dumps({key: summary[key] for key in
                      ('validation', 'passed', 'total', 'status')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
