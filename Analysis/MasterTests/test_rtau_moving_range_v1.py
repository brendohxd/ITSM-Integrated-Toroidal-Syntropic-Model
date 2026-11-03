"""Initial moving weighted range and conditional weak constraint transport.

Not a coupled solution, physical energy norm or finite-time domain theorem.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_MOVING_RANGE_V1_SPEC_2026-11-03.md'
MANIFEST = 'Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
MIXED = 'Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
INVERSE = 'Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
FACTORY = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
WEAK = 'Analysis/MasterTests/outputs/rtau_weak_graph_v1_20261103/receipt.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(x._mpi_[0])
    hi = lambda x: mp.mpf(x._mpi_[1])
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    upper = lambda x: iv.mpf(ab(x))
    binary = lambda x: [list(t) for t in x._mpi_]
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    inherited = json.loads((ROOT/MANIFEST).read_text())['source_sha256']
    pins = dict(inherited)
    snapshot = {}
    selfrel = Path(__file__).resolve().relative_to(ROOT).as_posix()
    extra = (selfrel, SPEC, MANIFEST, MIXED, INVERSE, FACTORY, WEAK,
             'Analysis/MasterTests/test_01_r4c1_rtau_mixed_operator_v4.py',
             'Theory/Gates/RES-001/RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_REPORT_2026-11-01.md',
             'Theory/Gates/RES-001/RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md')
    for rel, expected in inherited.items():
        assert sha(ROOT/rel) == expected, rel
    for rel in extra:
        pins[rel] = sha(ROOT/rel)
    for rel in pins:
        for path in (ROOT/rel, Path(str(ROOT/rel)+'.sha256')):
            if path.exists():
                snapshot[path] = (sha(path), path.stat().st_mtime_ns)
    check('all_219_inherited_source_hashes_match', len(inherited) == 219)
    mixed = json.loads((ROOT/MIXED).read_text())
    inverse = json.loads((ROOT/INVERSE).read_text())
    weak = json.loads((ROOT/WEAK).read_text())
    check('all_parent_checks_pass', all(d['passed'] == d['total'] and
          all(c['passed'] for c in d['checks']) for d in (mixed, inverse, weak)))

    hs = {tuple(row['ij']): decode(row['value'])
          for row in mixed['full_mixed_Hessian_upper_triangle']}
    hh = lambda i, j: hs.get(tuple(sorted((i, j))), iv.mpf(0))
    check('trace_momentum_auxiliary_rate_couplings_exactly_absent',
          all(tuple(sorted((14+i, j))) not in hs for i in (0, 3) for j in (13, 27, 41)))
    assert checks[-1]['passed']

    spec = importlib.util.spec_from_file_location('moving_range_action_factory', ROOT/FACTORY)
    factory = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(factory)
    env = factory.prepare()
    J = env['J']
    yy, _ = env['state'](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    forcing = [decode(x) for x in mixed['initial_affine_forcing']]
    # The exported affine forcing subtracts the known L_vq*v+L_vd*v_z.
    # Add them back to bound the canonical Euler momentum rate itself.
    pt_parts = []
    for i in (0, 3):
        value = forcing[i]
        value += sum((hh(14+i, k)*yy[14+k].c[0] +
                      hh(14+i, 28+k)*yy[14+k].c[1]
                      for k in range(13)), iv.mpf(0))
        pt_parts.append(value)
    pt = upper(sum(pt_parts, iv.mpf(0)))
    check('actual_initial_trace_momentum_rate_finite', mp.isfinite(hi(pt)),
          mp.nstr(hi(pt), 25))
    for center in ('0.3', '1.1', '2.4'):
        ctx = factory.point(center)
        grad, LL = ctx['gradient'], ctx['L']
        direct = sum((grad(LL, i).c[0]-grad(LL, 28+i).c[1]
                      for i in (0, 3)), iv.mpf(0))
        check('direct_action_Pt_enclosed_'+center, ab(direct) <= hi(pt),
              [mp.nstr(lo(direct), 20), mp.nstr(hi(direct), 20)])

    r = iv.mpf(1)/13000
    eps = iv.mpf(1)/1000
    # Use the inherited H/root enclosure directly, avoiding an interval
    # quotient of two dependent conformal metric entries.
    coeff_receipt = 'Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'
    coeff = json.loads((ROOT/coeff_receipt).read_text())
    pins[coeff_receipt] = sha(ROOT/coeff_receipt)
    for path in (ROOT/coeff_receipt, Path(str(ROOT/coeff_receipt)+'.sha256')):
        if path.exists():
            snapshot[path] = (sha(path), path.stat().st_mtime_ns)
    M = upper(decode(coeff['H_interval'])) + eps/31
    B = 2*eps/31
    # P/2-pi is bounded by Terr/(1+exp(2r)) in the parent's nonnegative sum.
    piabs = iv.mpf(11)/10*iv.sqrt(iv.mpf(3469)/4620)
    Pbound = 2*piabs+2*decode(inverse['bounds']['longitudinal_difference'])/(1+iv.exp(2*r))
    Rbound = decode(inverse['bounds']['longitudinal_integrating_factor'])
    Rtime = iv.exp(r)*((M*Pbound+pt)*(r+iv.mpf(1)/2)+Pbound*B)
    weight = iv.exp(r)*(1+r)/2
    weight_time = iv.exp(r)*((1+r)*M+B)/2
    check('moving_range_first_jet_constants_finite',
          all(lo(x) >= 0 and mp.isfinite(hi(x)) for x in (Rbound, Rtime, weight, weight_time)))

    # Full covector-density shift, including the off-diagonal index terms.
    first = [upper(yy[45+i].c[0]) for i in range(3)]
    second = [upper(yy[45+i].c[1]) for i in range(3)]
    b1 = iv.sqrt(sum((x*x for x in first), iv.mpf(0)))
    b2 = iv.sqrt(sum((x*x for x in second), iv.mpf(0)))
    growth = first[2]/2+b1+b2/2
    check('root_uniform_initial_constraint_transport_bound_finite',
          lo(growth) >= 0 and mp.isfinite(hi(growth)))

    t, z = s.symbols('t z', real=True)
    a, P, f, source = [s.Function(name)(t, z) for name in ('a', 'P', 'f', 'source')]
    lamz = s.diff(a, z)/a
    R = (s.diff(a, z)*P-a*s.diff(P, z))/2
    A = (s.diff(a, t)*P+a*s.diff(P, t))*(lamz*f+s.diff(f, z)/2)
    A += a*P*s.diff(lamz, t)*f
    formula = R*s.diff(f, t)+A+s.diff(source, t)/(2*a)-source*s.diff(a, t)/(2*a*a)
    defect = s.diff(R*f+source/(2*a), t)-formula
    divergence = -s.diff((s.diff(a, t)*P+a*s.diff(P, t))*f, z)/2
    check('exact_moving_range_weak_identity', s.simplify(defect-divergence) == 0)
    # A positive nonconstant periodic weight: its derivative cannot be frozen.
    af = s.exp(t)*(2+s.cos(z))
    sf = 2+s.cos(z)
    actual = s.diff(sf/(2*af), t).subs(t, 0)
    check('omitted_time_weight_rejected', s.simplify(actual) == -s.Rational(1, 2))

    u = s.Matrix([s.Function('u'+str(i))(z) for i in range(3)])
    C = s.Matrix([s.Function('C'+str(i))(z) for i in range(3)])
    shift = s.Matrix([s.Function('S'+str(i))(z) for i in range(3)])
    speed = shift[2]
    b = s.diff(shift, z)
    ez = s.Matrix([0, 0, 1])
    LieC = speed*s.diff(C, z)+s.diff(speed, z)*C+ez*(b.dot(C))
    adjoint = -speed*s.diff(u, z)+b*u[2]
    dual_defect = u.dot(LieC)-C.dot(adjoint)-s.diff(speed*C.dot(u), z)
    check('full_covector_density_dual_identity', s.expand(dual_defect) == 0)
    uz = s.diff(u, z)
    lhs = u.dot(adjoint)+uz.dot(s.diff(adjoint, z))
    flux = -speed*(u.dot(u)+uz.dot(uz))/2
    remainder = s.diff(speed, z)*(u.dot(u)-uz.dot(uz))/2
    remainder += u.dot(b)*u[2]+uz.dot(b)*uz[2]+uz.dot(s.diff(b, z))*u[2]
    check('exact_dual_H1_energy_identity', s.expand(lhs-s.diff(flux, z)-remainder) == 0)
    badC = s.Matrix([1, 0, 0])
    badS = s.Matrix([s.sin(z), 0, 0])
    badterm = ez*s.diff(badS, z).dot(badC)
    check('omitting_tensor_index_term_rejected', badterm[2] == s.cos(z))
    check('finite_centre_inhomogeneous_term_not_declared_zero', badterm != s.zeros(3, 1))
    # No term with a third shift derivative appears in the dual identity.
    check('constraint_transport_requires_only_C2_shift',
          all(sum(v.derivative_count for v in [atom]) <= 2
              for atom in remainder.atoms(s.Derivative)))

    check('all_input_bytes_and_sidecar_mtimes_unchanged',
          all(sha(path) == h and path.stat().st_mtime_ns == stamp
              for path, (h, stamp) in snapshot.items()))
    values = dict(initial_Pt_L2_upper=pt, initial_Rt_Hminus1_upper=Rtime,
                  compatibility_per_f_t_L2=Rbound, compatibility_per_f_H1=Rtime,
                  compatibility_per_source_t_Hminus1=weight,
                  compatibility_per_source_Hminus1=weight_time,
                  initial_constraint_Hminus1_norm_growth=growth,
                  shift_first_vector_upper=b1, shift_second_vector_upper=b2,
                  initial_P_absolute_upper=Pbound)
    return dict(kind='RTAU_MOVING_RANGE_FIRST_JET_V1',
                passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                constants_binary={k: binary(v) for k, v in values.items()},
                upper_display={k: mp.nstr(hi(v), 18) for k, v in values.items()},
                source_sha256=pins, inherited_source_count=len(inherited),
                conformal_formula_scope='INITIAL_BACKGROUND_FIRST_JET_ONLY',
                conditional_transport='||C(t)||H^-1 <= exp(integral gamma) ||C(0)||H^-1 on an existing regular exact constrained background',
                actual_time_tube='NOT_ESTABLISHED', full_source_rate_map='NOT_DERIVED',
                physical_norm='NOT_DERIVED', coupled_generator='NOT_DERIVED',
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
            failure = dict(status='FAILED_ATTEMPT', error=repr(error),
                           source_sha256=sha(Path(__file__)), physics_pass=False)
            with (args.output.parent/'failure.json').open('x') as handle:
                json.dump(failure, handle, indent=2, sort_keys=True)
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
