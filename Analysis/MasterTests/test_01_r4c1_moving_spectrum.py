"""R4C1-S4H step 3: exact moving slow-block spectral screen.

The claim is conditional on a regular continuation of the registered B1
solution. It does not prove existence over [0,4], a smooth energy metric,
constraint propagation, a physical cutoff, or a parent physics gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as s

import test_01_r4c1_moving_principal as previous


prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
K, P = previous.K, previous.P
PINS = {
    'Analysis/MasterTests/test_01_r4c1_moving_principal.py':
        '060adab2d7928c1ba072617796145d19a9a5f2943685829a69a4529dbcc10ccb',
    'Analysis/MasterTests/outputs/r4c1_s4h_principal_attempt_01/summary.json':
        '79fdd57fb6f8f6682c40f9ea066b3f91a067ee8ec54397542100b21fa214352a',
}


def verify(audit):
    inputs = previous.verify(audit)
    for name, expected in PINS.items():
        path = ROOT / name
        actual = base.sha(path)
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('S4H4_pin:' + name, actual == expected, actual)
        audit.test('S4H4_sidecar:' + name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        inputs[name] = actual
    summary = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_principal_attempt_01/summary.json').read_text())
    detail_name, detail_hash = next(iter(summary['artifacts'].items()))
    audit.test('S4H4_principal_parent',
               summary['validation'] == 'PASS_LOCAL_CHECKS'
               and summary['status'] == 'PRINCIPAL_COEFFICIENTS_ONLY'
               and summary['passed'] == summary['total'] == 278
               and summary['physics_pass'] is False
               and summary['Rule9_cleared'] is False
               and base.sha(ROOT / detail_name) == detail_hash)
    inputs[detail_name] = detail_hash
    return inputs


def exact_zero(audit, name, matrix):
    reduced = matrix.applyfunc(s.cancel)
    failures = [(i, j, str(reduced[i, j])) for i in range(reduced.rows)
                for j in range(reduced.cols) if reduced[i, j] != 0]
    audit.test(name, not failures, failures[:8] if failures else 'zero_matrix')


def evaluate(poly, A, variable):
    result = s.zeros(A.rows)
    eye = s.eye(A.rows)
    for coeff in s.Poly(poly, variable).all_coeffs():
        result = (result * A + coeff * eye).applyfunc(s.cancel)
    return result


def derive(audit):
    detail = json.loads((ROOT /
        'Analysis/MasterTests/outputs/r4c1_s4h_principal_attempt_01/detail.json').read_text())
    symbols = prior.SYMBOLS
    C2 = s.Matrix([[s.sympify(x, locals=symbols) for x in row]
                   for row in detail['C2']])
    C1 = s.Matrix([[s.sympify(x, locals=symbols) for x in row]
                   for row in detail['C1']])
    exact_zero(audit, 'S4H4_moving_C2_skew', C2 + C2.T)
    audit.test('S4H4_C2_only_phase_pair',
               C2[6, 7] == s.sqrt(165) / 33
               and C2[7, 6] == -s.sqrt(165) / 33
               and all(C2[j, i] == 0 for j in range(12)
                       for i in range(12) if (j, i) not in ((6, 7), (7, 6))))

    H = base.H
    denominators = [s.denom(s.cancel(x)) for x in C1 if x != 0]
    audit.test('S4H4_C1_poles_only_at_H_zero', all(
        s.Poly(d, H).length() == 1 and d.free_symbols <= {H}
        for d in denominators), [str(d) for d in denominators])

    A = C1.extract(K, K)
    lam = s.Symbol('lambda')
    radius2 = base.u**2 + base.v**2
    expected = s.cancel(lam**2 * (lam**2 + 1)**2
                        * (3 * lam**2 + 1)
                        * (13 * lam**2 + radius2 + 13) / 39)
    char = s.factor(A.charpoly(lam).as_expr())
    audit.test('S4H4_all_state_charpoly', s.cancel(char - expected) == 0,
               str(char))
    squarefree = s.Poly(lam * (lam**2 + 1) * (3 * lam**2 + 1)
                        * (13 * lam**2 + radius2 + 13), lam)
    exact_zero(audit, 'S4H4_squarefree_polynomial_annihilates_A',
               evaluate(squarefree, A, lam))
    for index, factor in enumerate((lam, lam**2 + 1, 3*lam**2 + 1,
                                    13*lam**2 + radius2 + 13)):
        quotient = s.div(squarefree, s.Poly(factor, lam))[0]
        trial = evaluate(quotient, A, lam)
        audit.test(f'S4H4_minimal_factor_needed_{index}',
                   any(s.cancel(x) != 0 for x in trial))

    charge = base.a**3 * (base.u * base.vd - base.v * base.ud)
    audit.test('S4H4_angular_charge_initial_one',
               charge.subs({base.a: 1, base.u: 1, base.v: 0,
                            base.ud: 0, base.vd: 1}) == 1)
    audit.test('S4H4_angular_charge_exact_conservation',
               s.cancel(up.dtime(charge)) == 0,
               str(s.cancel(up.dtime(charge))))
    audit.test('S4H4_regular_B1_radius_nonzero_implication',
               charge.subs({base.a: 1, base.u: 1, base.v: 0,
                            base.ud: 0, base.vd: 1}) == 1,
               'On a regular finite-state continuation, J=1 rules out u=v=0; '
               'this does not prove the continuation exists on [0,4].')
    audit.test('S4H4_spectral_factor_separation_on_radius_positive',
               s.cancel((1 + radius2/13) - 1) == radius2/13,
               'For real u,v and J=1, radius2>0, so all squared '
               'frequencies 1,1/3,1+radius2/13 are positive and distinct.')
    return dict(C2=C2, C1=C1, A=A, char=char,
                annihilator=squarefree.as_expr(), charge=charge,
                squared_frequencies=[s.Integer(1), s.Rational(1, 3),
                                     1 + radius2/13])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', type=int, required=True)
    args = parser.parse_args()
    if args.attempt < 1:
        parser.error('--attempt must be positive')
    target = OUT / f'r4c1_s4h_spectrum_attempt_{args.attempt:02d}'
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
        schema='r4c1-s4h-moving-spectrum-detail-v1',
        status='PRINCIPAL_SPECTRUM_CONDITIONAL_REGULAR_B1' if valid else
               'PRINCIPAL_SPECTRUM_FAILED_OR_UNKNOWN',
        charpoly=str(result['char']),
        squarefree_annihilator=str(result['annihilator']),
        angular_charge=str(result['charge']),
        squared_frequencies=[str(x) for x in result['squared_frequencies']],
        regular_domain='real finite state, a>0, H>0, rho_m>0, J=1, k!=0; '
                       'the exact [0,4] solution and physical p cutoff are unproved'))
    summary = dict(
        schema='r4c1-s4h-moving-spectrum-summary-v1',
        validation='PASS_LOCAL_CHECKS' if valid else 'FAIL_LOCAL_CHECKS',
        passed=sum(check['passed'] for check in audit.checks),
        total=len(audit.checks),
        status='PRINCIPAL_SPECTRUM_CONDITIONAL_REGULAR_B1' if valid else
               'PRINCIPAL_SPECTRUM_FAILED_OR_UNKNOWN',
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
        review_status='DEFERRED',
        decision=dict(moving_C2_C1_144='EXACT_FORMULAS',
                      moving_slow_spectrum='CONDITIONAL_REGULAR_B1' if valid
                          else 'NOT_PROVED',
                      smooth_metric='NOT_CONSTRUCTED',
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
