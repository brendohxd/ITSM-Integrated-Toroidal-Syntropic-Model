"""Initial H^-1/H1 coupled reconstruction; no physical evolution claim.

The continuum estimates are proved in the owning report. This executable
evaluates their outward constants and exact independent identity controls.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_WEAK_GRAPH_V1_SPEC_2026-11-03.md'
MANIFEST = 'Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
INVERSE = 'Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
AUDIT = 'Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_audit_v1_attempt_01/summary.json'
FACTORY = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
PULLBACK = 'Analysis/MasterTests/outputs/rtau_canonical_auxiliary_pullback_v2_20261102/receipt.json'
AUXILIARY = 'Analysis/MasterTests/test_rtau_coupled_auxiliary_variation_v1.py'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(x._mpi_[0])
    hi = lambda x: mp.mpf(x._mpi_[1])
    decode = lambda x: iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary = lambda x: [list(t) for t in x._mpi_]
    absolute_upper = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    manifest = json.loads((ROOT / MANIFEST).read_text())
    pins = dict(manifest['source_sha256'])
    inherited_count = len(pins)
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT / rel
        assert digest(path) == expected, rel
        for item in (path, Path(str(path) + '.sha256')):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)
    check('all_219_inherited_hashes_match', inherited_count == 219)
    for rel in (SELF, SPEC, MANIFEST, INVERSE, AUDIT, FACTORY, PULLBACK,
                AUXILIARY,
                'Theory/Gates/RES-001/RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md',
                'Theory/Gates/RES-001/RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_REPORT_2026-11-01.md'):
        path = ROOT / rel
        pins[rel] = digest(path)
        for item in (path, Path(str(path) + '.sha256')):
            if item.exists():
                snapshot[item] = (digest(item), item.stat().st_mtime_ns)

    parent = json.loads((ROOT / INVERSE).read_text())
    audit = json.loads((ROOT / AUDIT).read_text())
    check('parent_and_momentum_audit_pass',
          parent['passed'] == parent['total'] == 31 and
          audit['passed'] == audit['total'] == 12 and
          all(c['passed'] for c in parent['checks'] + audit['checks']))
    n = s.symbols('n', integer=True, positive=True)
    cn = s.Rational(parent['reference_nonzero_mass'])
    cm = s.Rational(parent['reference_mean_mass'])
    r0 = iv.mpf(8400) / 2263
    check('reference_Hminus1_H1_all_nonzero_modes', cn > 1 and
          s.simplify((n*n + cn) - (1+n*n)) == cn-1)
    check('negative_reference_mean_retained', cm == -s.Rational(2263, 8400))
    check('Dinv_Hminus1_L2_all_modes',
          s.simplify(2*n*n - (1+n*n)) == n*n-1)

    r = iv.mpf(1) / 13000
    eps = iv.mpf(1) / 1000
    beta = iv.mpf(2) / 5
    psi0 = eps*(iv.mpf(1)/29 + iv.mpf(1)/31)
    psi1 = eps*(iv.mpf(1)/29 + iv.mpf(2)/31)
    psi2 = eps*(iv.mpf(1)/29 + iv.mpf(4)/31)
    a2prime = iv.exp(r + beta*psi0)*(r + beta*psi1)
    old_error = decode(parent['bounds']['operator_perturbation'])
    d1 = decode(parent['bounds']['trace_first'])
    # The old d1/2 H2->L2 estimate becomes d1 in H1->H^-1.
    error = old_error + d1/2 + a2prime
    contraction = r0*error
    check('weak_space_Neumann_contraction_strict', hi(contraction) < 1,
          mp.nstr(hi(contraction), 30))
    assert hi(contraction) < 1, 'No inverse inferred if this estimate fails'
    green = r0/(1-contraction)

    # Reuse actual profiles and certified root C2 ball without reevaluating
    # the expensive action Hessian or importing an old rest-frame matrix.
    factory = load_module('weak_graph_frozen_factory', FACTORY)
    env = factory.prepare()
    J = env['J']
    yy, _ = env['state'](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    lie = env['lie'](yy[:14], yy[28:42], yy[42:45], yy[45:48])
    rv = [absolute_upper(yy[14+i].c[0] - lie[i].c[0]) for i in (2, 4, 5)]
    check('root_uniform_rate_coefficients_finite',
          all(mp.isfinite(hi(x)) for x in rv))
    e2, e4 = iv.exp(2*r), iv.exp(4*r)
    ratio1, ratio2 = e2, e4
    cs = [(1+ratio2)*e2*iv.sqrt(2), (1+ratio2)*e2*iv.sqrt(2),
          (1+ratio1)*e2*(1+r)/iv.sqrt(2)]
    ce = [ratio2, ratio2, ratio1]
    fbound = iv.mpf(max([hi(green)] +
                      [hi(green*rv[i]*x) for i in range(3) for x in (cs[i], ce[i])]))
    tx = decode(parent['bounds']['transverse_x'])
    ty = decode(parent['bounds']['transverse_y'])
    tz = iv.mpf(11)/10*iv.sqrt(iv.mpf(3469)/4620) + decode(parent['bounds']['longitudinal_difference'])
    source_bounds = [iv.mpf(max(hi(a), hi(b))) for a, b in zip(cs, ce)]
    momenta = [t*fbound+u for t, u in zip((tx, ty, tz), source_bounds)]
    graph = fbound + sum(momenta, iv.mpf(0))
    check('trace_H1_and_all_three_momenta_L2_bounds_finite',
          all(lo(x) > 0 and mp.isfinite(hi(x)) for x in [fbound, graph] + momenta))

    # Exact periodic weak identity and a nonzero omitted-leading-drift probe.
    z = s.symbols('z', real=True)
    aa, ff, test = [s.Function(name)(z) for name in ('A2', 'f', 'test')]
    defect = test*aa*s.diff(ff, z, 2) + aa*s.diff(ff, z)*s.diff(test, z) + s.diff(aa, z)*s.diff(ff, z)*test - s.diff(test*aa*s.diff(ff, z), z)
    check('variable_leading_coefficient_weak_identity', s.expand(defect) == 0)
    missed = s.integrate(s.cos(z)*s.cos(z)*s.cos(2*z)/10, (z, 0, 2*s.pi))/(2*s.pi)
    check('omitting_A2prime_rejected', missed == s.Rational(1, 40), str(missed))
    # Integrating-factor identity on general functions; weak extension follows
    # by continuity, not by differentiating a rough source pointwise.
    a, pb, f, p, src = [s.Function(name)(z) for name in ('a', 'P_b', 'f', 'p_z', 's_z')]
    rr = (s.diff(a, z)*pb-a*s.diff(pb, z))/2
    raw = s.diff(2*a*a*p, z)-s.diff(a*a, z)*p-pb*s.diff(a*a*f, z)-src
    weak = 2*a*(s.diff(a*p-a*pb*f/2, z)-rr*f-src/(2*a))
    check('full_weighted_range_identity', s.expand(raw-weak) == 0)
    check('projected_range_not_automatic', s.simplify((src/(2*a)).subs(src, 2*a)) == 1)
    # Reference principal control, not a new physical background or mode set.
    source_hminus1_squared = n*n/(1+n*n)
    trace_h1_squared = n*n*(1+n*n)/(n*n+cn)**2
    check('rough_derivative_source_uniform_Hminus1',
          s.simplify(1-source_hminus1_squared) == 1/(1+n*n))
    check('reference_trace_H1_uniform',
          s.Poly(s.expand((n*n+cn)**2-n*n*(1+n*n)), n).all_coeffs()[0] > 0 and cn > 1)
    # ||f||H2 = n(1+n^2)/(n^2+cn) >= n/(1+cn), unbounded.
    check('reference_trace_H2_not_uniform',
          s.simplify((1+n*n)*(1+cn)-(n*n+cn)) == 1+cn*n*n)

    # Full metric H1 / force H2 -> auxiliary L2 bound on the actual profile.
    e0 = iv.sqrt(3)*iv.exp(2*r)/2
    d0 = iv.sqrt(3)*iv.exp(r)/2
    z0 = iv.exp(2*r)*(psi2+r*psi1)
    q0 = iv.exp(3*r)
    ck0 = e0*z0+q0*d0*(r*psi1+psi2)
    ck1 = q0*d0*psi1
    cpsi = iv.exp(4*r)*(1+r/2)
    ck = ck0+ck1
    check('actual_auxiliary_L2_constants_positive_finite',
          all(lo(x) > 0 and mp.isfinite(hi(x)) for x in (cpsi, ck, ck0, ck1)))
    aux = load_module('weak_graph_exact_auxiliary', AUXILIARY)
    g = 1+z*z/10
    h = g*g*s.eye(3)
    k = (1+z/5)*s.Matrix([[1, 2, 3], [2, -1, 4], [3, 4, 2]])/19
    psi = z*z/3+z**3/5
    chi = z+z*z/11
    dz, _ = aux.variation(h, s.zeros(3), psi, s.S.Zero, k, s.zeros(3), chi, s.S.Zero, z)
    inv = h.inv()
    mu = g**3
    E = inv/2
    DD = mu*(-inv[:, 2]*inv[2, :]+inv[2, 2]*inv/2)
    pair = lambda x, y: s.trace(x.T*y)
    strong_z, _ = aux.strong(h, s.diff(h, z), s.zeros(3), s.zeros(3), s.diff(psi, z), s.diff(psi, z, 2), s.S.Zero, s.S.Zero)
    expanded = -pair(E, k)*strong_z - (
        mu*inv[2, 2]*s.diff(chi, z, 2) + s.diff(mu*inv[2, 2], z)*s.diff(chi, z)
        + pair(DD, s.diff(k, z))*s.diff(psi, z)
        + pair(s.diff(DD, z), k)*s.diff(psi, z)
        + pair(DD, k)*s.diff(psi, z, 2))/mu
    check('auxiliary_full_six_component_product_rule', s.simplify(dz-expanded) == 0)

    # Initial auxiliary-rate composition remains in the original coordinate;
    # these constants are separate from an asserted physical energy norm.
    pull = json.loads((ROOT / PULLBACK).read_text())
    check('corrected_canonical_rate_parent_passes', pull['passed'] == pull['total'] == 10)
    rate = {k: decode(v) for k, v in pull['constants_binary'].items()}
    # H1 embeds both Q0 and Q1 with norm <=1; full H1 canonical input
    # is only a stronger sufficient control topology, not a selected energy.
    rate_q = rate['configuration'] + rate['configuration_z']

    unchanged = all(digest(path) == h and path.stat().st_mtime_ns == t
                    for path, (h, t) in snapshot.items())
    check('all_inherited_and_new_input_bytes_mtimes_preserved', unchanged)
    bounds = dict(leading_coefficient_derivative=a2prime,
                  H1_Hminus1_operator_perturbation=error, weak_contraction=contraction,
                  green_Hminus1_H1=green, trace_H1_per_Dminus=fbound,
                  graph_H1_L2_per_Dminus=graph, auxiliary_L2_per_psi_H2=cpsi,
                  auxiliary_L2_per_metric_H1_F=ck,
                  canonical_rate_Hminus2_per_Q_H1=rate_q)
    bounds.update({f'momentum_{name}_L2_per_Dminus': value
                   for name, value in zip(('x', 'y', 'z'), momenta)})
    return dict(kind='RTAU_INITIAL_WEAK_GRAPH_V1', passed=sum(c['passed'] for c in checks),
                total=len(checks), checks=checks, inherited_source_count=inherited_count,
                source_sha256=pins, constants_binary={k: binary(v) for k, v in bounds.items()},
                upper_display={k: mp.nstr(hi(v), 18) for k, v in bounds.items()},
                rate_coefficients_binary=[binary(x) for x in rv],
                momentum_source_Hminus1_bounds_binary=[binary(x) for x in cs],
                data_norm='Dminus=||assembled_r||H^-1+sum_i(||s_i||H^-1+|eta_i|)',
                compatible_range='mean(sx)=mean(sy)=0; mean(R*f+s_z/(2*a))=0; independent global I/Q conditions retained',
                scope='INITIAL_LINEAR_WEAK_RECONSTRUCTION_AND_AUXILIARY_OBSERVABLE',
                free_data_source_assembly_constants='NOT_COMPUTED',
                physical_norm='NOT_DERIVED', moving_constraint_domain='NOT_DERIVED',
                coupled_generator='NOT_DERIVED', finite_time_estimate=False,
                review='DEFERRED', physics_pass=False, gate_effect='NONE', Rtau_adopted=False)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    receipt = calculate()
    data = (json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open('xb') as handle:
            handle.write(data)
        with Path(str(args.output)+'.sha256').open('x') as handle:
            handle.write(hashlib.sha256(data).hexdigest()+'\n')
    else:
        assert args.verify.read_bytes() == data, 'Immutable replay differs'
    print(json.dumps(dict(passed=receipt['passed'], total=receipt['total'],
                          failed=[c for c in receipt['checks'] if not c['passed']],
                          bounds=receipt['upper_display']), indent=2))
    return 0 if receipt['passed'] == receipt['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
