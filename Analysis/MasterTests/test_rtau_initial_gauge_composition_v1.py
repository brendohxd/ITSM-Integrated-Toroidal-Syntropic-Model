"""Gauge-closed initial weak rates on the compatible initial canonical graph.

No density-coordinate generator, physical energy or time tube is asserted.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V1_SPEC_2026-11-03.md'
MANIFEST = 'Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
RATE = 'Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json'
GRAPH = 'Analysis/MasterTests/outputs/rtau_weak_graph_v1_20261103/receipt.json'
GAUGE = 'Analysis/MasterTests/outputs/r4c1_rtau_gauge_velocity_v1_attempt_01/summary.json'
MAP = 'Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
HELPER = 'Analysis/MasterTests/r4c1_gauge_velocity_v1.py'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary = lambda x: [list(t) for t in x._mpi_]
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    inherited = json.loads((ROOT/MANIFEST).read_text())['source_sha256']
    pins = dict(inherited)
    for rel, expected in inherited.items():
        assert sha(ROOT/rel) == expected, rel
    extras = (Path(__file__).resolve().relative_to(ROOT).as_posix(), SPEC,
              MANIFEST, RATE, GRAPH, GAUGE, MAP, HELPER,
              'Theory/Gates/RES-001/RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md')
    for rel in extras:
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel in pins:
        for path in (ROOT/rel, Path(str(ROOT/rel)+'.sha256')):
            if path.exists():
                snapshot[path] = (sha(path), path.stat().st_mtime_ns)
    check('all_219_inherited_hashes_match', len(inherited) == 219)
    data = {key: json.loads((ROOT/path).read_text())
            for key, path in [('rate', RATE), ('graph', GRAPH), ('gauge', GAUGE), ('map', MAP)]}
    check('all_parent_controls_pass', all(d['passed'] == d['total'] and
          all(c['passed'] for c in d['checks']) for d in data.values()))
    coeff = {key: [decode(x) for x in xs]
             for key, xs in data['rate']['coefficients_binary'].items()}
    mb = data['map']['bounds']
    j = iv.mpf(lo(decode(mb['J_lower_binary'])))
    u = iv.mpf(hi(decode(mb['J_upper_binary'])))
    W = iv.mpf(hi(decode(mb['drift_upper_binary'])))
    P = iv.mpf(hi(decode(mb['drift_derivative_upper_binary'])))
    r = iv.mpf(1)/13000
    Cxi = iv.mpf(max(hi(decode(data['gauge']['bounds'][key])) for key in
                    ('transverse_velocity_L2_H1', 'longitudinal_velocity_L2_H1')))
    Fq = iv.mpf(max(mp.mpf(1), hi(u), hi(1/j**2)))
    field_L2_pullback = Fq*iv.sqrt(u)
    old_shift_pullback = (iv.mpf(max(mp.mpf(1), hi(u), hi(1/j)))+r/j)/iv.sqrt(j)
    drift = W+2*P
    v0 = coeff['field_rate_L2']
    # v0 below has zero original corrective shift. First transform its full
    # background-coordinate rate, then solve the actual periodic gauge row.
    b = [field_L2_pullback*v0[0], field_L2_pullback*(v0[1]+drift), iv.mpf(0), iv.mpf(0)]
    xi = [Cxi*x for x in b]
    xi[3] = iv.mpf(1)  # independent harmonic coordinate velocity norm
    sigma = [old_shift_pullback*x for x in xi]

    def close_caller_shift(values):
        return [values[i]+values[3]*sigma[i] if i < 3 else values[3]*sigma[3]
                for i in range(4)]

    corrected = {key: close_caller_shift(xs) for key, xs in coeff.items()}
    # Canonical momentum rates are distributions. Their dual test weight is
    # J*T_p=1/T_q, rather than T_p alone or the scalar-field weight J.
    G0 = iv.mpf(max(mp.mpf(1), hi(u*u), hi(1/j)))
    ordinary_momentum_pullback = G0*(iv.mpf(max(mp.mpf(1), hi(u)))+2*r)/iv.sqrt(j)
    force_momentum_pullback = (iv.mpf(max(mp.mpf(1), hi(u*u)))+r*u/iv.sqrt(2))/iv.sqrt(j)
    auxiliary_time_pullback = (u*iv.mpf(max(mp.mpf(1), hi(u*u)))+
                               iv.sqrt(2)*r*u+(r+r*r)*u+
                               3*r*u*u/iv.sqrt(2))/iv.sqrt(j)
    adapted = {}
    values = corrected['field_rate_L2'].copy()
    values[1] += drift
    adapted['field_rate_L2'] = [field_L2_pullback*x for x in values]
    values = corrected['ordinary_momentum_rate_Hminus1'].copy()
    values[0] += drift
    adapted['ordinary_momentum_rate_Hminus1'] = [ordinary_momentum_pullback*x for x in values]
    values = corrected['force_momentum_rate_Hminus2'].copy()
    values[0] += W
    adapted['force_momentum_rate_Hminus2'] = [force_momentum_pullback*x for x in values]
    adapted['auxiliary_L2'] = [iv.sqrt(u)*x for x in corrected['auxiliary_L2']]
    values = [x+(W+P)*z for x, z in zip(corrected['auxiliary_time_Hminus2'], corrected['auxiliary_L2'])]
    adapted['auxiliary_time_Hminus2'] = [auxiliary_time_pullback*x for x in values]
    adapted['periodic_corrector_H1_adapted'] = xi
    adapted['corrective_shift_H1_original'] = sigma
    adapted['physical_metric_modulus_rates'] = [iv.exp(4*r)*x for x in b]

    gb = data['graph']['constants_binary']
    f = decode(gb['trace_H1_per_Dminus'])
    momentum = [decode(gb['momentum_'+name+'_L2_per_Dminus']) for name in ('x', 'y', 'z')]
    Qlift = iv.sqrt(2)*iv.exp(2*r)*(1+2*r)*f
    Plift = iv.sqrt(sum((x*x for x in momentum), iv.mpf(0)))
    # Inputs in the output receipt are now Dminus,Qfree,Pfree,F2,Hharm.
    lifted = {key: [xs[0]*Plift+xs[1]*Qlift, xs[1], xs[0], xs[2], xs[3]]
              for key, xs in adapted.items()}
    check('initial_J_orientation_preserved', lo(j) > 0 and lo(u) >= hi(j))
    check('all_closed_and_lifted_constants_finite', all(lo(x) >= 0 and mp.isfinite(hi(x))
          for xs in list(adapted.values())+list(lifted.values()) for x in xs))
    check('harmonic_correction_response_retained', lo(adapted['field_rate_L2'][3]) > 0 and
          lo(adapted['ordinary_momentum_rate_Hminus1'][3]) > 0)

    spec = importlib.util.spec_from_file_location('initial_gauge_existing_helper', ROOT/HELPER)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    z = s.symbols('z', real=True)
    q0 = [s.S.Zero]*14
    q0[0] = q0[3] = q0[5] = s.S.One
    k = [s.S.Zero]*14
    moduli = [s.Rational(1, 13), -s.Rational(2, 19), s.Rational(3, 23)]
    for i, value in zip((2, 4, 5), moduli):
        k[i] = value
    w = s.sin(z)/17
    lie_k = helper.lie_fields(k, [s.S.Zero]*14, [0, 0, w], [0, 0, s.diff(w, z)])
    constants = [s.Rational(1, 7), -s.Rational(1, 11), s.Rational(2, 13)]
    expressions = [c-lie_k[i] for c, i in zip(constants, (2, 4, 5))]
    rates = [lambda x, expression=expression: expression.subs(z, x) for expression in expressions]
    mean = lambda function: s.simplify(s.integrate(s.expand_trig(function(z)), (z, 0, 2*s.pi))/(2*s.pi))

    def primitive(function):
        value = s.integrate(function(z), z)
        value = s.simplify(value-mean(lambda x: value.subs(z, x)))
        return lambda x: value.subs(z, x)

    harmonics = (s.Rational(1, 5), s.Rational(1, 6), -s.Rational(1, 8))
    result = helper.solve(rates, lambda x: s.S.One, lambda x: s.S.One,
                          s.S.One, mean, primitive, harmonics)
    slopes = [function(z) for function in result['coordinate_gradient']]
    corrected_metric = [expressions[0]+slopes[0], expressions[1]+slopes[1], expressions[2]+2*slopes[2]]
    lie_corrector = helper.lie_fields(q0, [s.S.Zero]*14,
                                     [function(z) for function in result['coordinate_velocity']], slopes)
    check('full_field_Lie_correction_matches_metric_composition',
          all(s.simplify(expressions[k]+lie_corrector[i]-corrected_metric[k]) == 0
              for k, i in enumerate((2, 4, 5))))
    check('background_drift_and_modulus_composition_exact',
          all(s.simplify(x-c) == 0 for x, c in zip(corrected_metric, constants)))
    check('physical_modulus_rates_retained_not_zeroed', result['modulus_rates'] == constants)
    check('periodic_harmonic_coordinate_inputs_retained',
          all(s.simplify(mean(function)-h) == 0 for function, h in zip(result['coordinate_velocity'], harmonics)))
    check('corrective_velocities_periodic', all(s.simplify(function(0)-function(2*s.pi)) == 0
                                              for function in result['coordinate_velocity']))
    check('omitted_modulus_constants_rejected', any(c != 0 for c in constants))
    check('omitted_background_drift_rejected', all(s.simplify(lie_k[i]) != 0 for i in (2, 4, 5)))
    # A retained harmonic translation also acts on a nonconstant scalar.
    check('harmonic_translation_not_deleted_from_other_fields',
          s.simplify(harmonics[2]*s.diff(s.sin(z), z)) != 0)

    zz = s.Function('zeta')(z)
    JJ = s.diff(zz, z)
    g = s.Function('g')(z)
    phi = s.Function('phi')
    phip = s.Subs(s.diff(phi(z), z), z, zz)
    phipp = s.Subs(s.diff(phi(z), z, 2), z, zz)
    check('H1_dual_test_pullback_chain_rule',
          s.simplify(s.diff(g*phi(zz), z)-s.diff(g, z)*phi(zz)-g*JJ*phip) == 0)
    second = s.diff(g, z, 2)*phi(zz)+(2*s.diff(g, z)*JJ+g*s.diff(JJ, z))*phip+g*JJ*JJ*phipp
    check('H2_dual_test_pullback_chain_rule', s.simplify(s.diff(g*phi(zz), z, 2)-second) == 0)
    longitudinal = s.Function('xi')(zz)/JJ
    check('original_corrective_shift_chain_rule',
          s.simplify(s.diff(longitudinal, z)-s.Subs(s.diff(s.Function('xi')(z), z), z, zz)+
                     s.Function('xi')(zz)*s.diff(JJ, z)/JJ**2) == 0)
    js = s.symbols('J', positive=True)
    tq, tp = helper.factors(js)
    check('all_field_momentum_pairings_keep_Jacobian', all(s.simplify(js*x*y-1) == 0 for x, y in zip(tq, tp)))
    # Mean of a scalar field versus a scalar density under the SAME map.
    jfixture = 1+s.sin(z)/10
    scalar_mean = s.integrate(s.sin(z)*jfixture, (z, 0, 2*s.pi))/(2*s.pi)
    density_mean = s.integrate(s.sin(z), (z, 0, 2*s.pi))/(2*s.pi)
    check('scalar_and_density_Hminus2_pullbacks_distinguished', scalar_mean == s.Rational(1, 20) and density_mean == 0)
    check('omitted_momentum_density_Jacobian_rejected', s.simplify(js-1) != 0)
    check('all_original_and_new_input_bytes_mtimes_preserved',
          all(sha(path) == h and path.stat().st_mtime_ns == stamp
              for path, (h, stamp) in snapshot.items()))
    return dict(kind='RTAU_INITIAL_GAUGE_CLOSED_WEAK_RATE_V1',
                passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                input_order=['Dminus_Hminus1_assembled', 'Qfree_H1_original',
                             'Pfree_L2_original', 'force_configuration_H2_original',
                             'harmonic_coordinate_velocity_adapted'],
                graph_lift_binary={'Q1_per_Dminus': binary(Qlift), 'P0_per_Dminus': binary(Plift)},
                constants_binary={key: [binary(x) for x in xs] for key, xs in lifted.items()},
                upper_display={key: [mp.nstr(hi(x), 18) for x in xs] for key, xs in lifted.items()},
                canonical_input_constants_binary={key: [binary(x) for x in xs] for key, xs in adapted.items()},
                pullback_binary={key: binary(value) for key, value in dict(
                    field_L2=field_L2_pullback, shift_H1=old_shift_pullback,
                    ordinary_momentum_Hminus1=ordinary_momentum_pullback,
                    force_momentum_Hminus2=force_momentum_pullback,
                    auxiliary_time_Hminus2=auxiliary_time_pullback).items()},
                source_sha256=pins, inherited_source_count=len(inherited),
                scope='INITIAL_SPATIAL_GAUGE_CLOSED_WEAK_RATE_ON_COMPATIBLE_CANONICAL_GRAPH',
                caller_shift='SOLVED_INITIAL_PERIODIC_CORRECTION_WITH_RETAINED_HARMONICS',
                density_chart_time_row='NOT_DERIVED', evolving_Green_inverse='NOT_DERIVED',
                physical_norm='NOT_DERIVED', actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False, review='DEFERRED', physics_pass=False, gate_effect='NONE')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    try:
        receipt = calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=False)
            with (args.output.parent/'failure.json').open('x') as handle:
                json.dump(dict(status='FAILED_ATTEMPT', error=repr(error), source_sha256=sha(Path(__file__)), physics_pass=False), handle, indent=2)
        raise
    raw = (json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open('xb') as handle:
            handle.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as handle:
            handle.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:
        assert args.verify.read_bytes() == raw, 'Immutable replay differs'
    print(json.dumps(dict(passed=receipt['passed'], total=receipt['total'],
                          failed=[c for c in receipt['checks'] if not c['passed']],
                          bounds=receipt['upper_display']), indent=2))
    return 0 if receipt['passed'] == receipt['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
