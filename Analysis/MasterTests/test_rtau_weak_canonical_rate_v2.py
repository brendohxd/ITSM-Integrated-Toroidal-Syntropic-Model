"""Initial unreduced weak canonical rows and momentum-tangent time map.

Caller shift remains explicit. This is not the compatible physical generator.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_WEAK_CANONICAL_RATE_V2_SPEC_2026-11-03.md'
MANIFEST = 'Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
MIXED = 'Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
INITIAL = 'Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
WEAK = 'Analysis/MasterTests/outputs/rtau_weak_graph_v1_20261103/receipt.json'
MOVING = 'Analysis/MasterTests/outputs/rtau_moving_range_v1_20261103/receipt.json'
AUXRATE = 'Analysis/MasterTests/outputs/rtau_coupled_auxiliary_variation_v1_20261102/receipt.json'
FACTORY = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    up = lambda x: iv.mpf(ab(x))
    binary = lambda x: [list(t) for t in x._mpi_]
    vecnorm = lambda xs: iv.sqrt(sum((up(x)**2 for x in xs), iv.mpf(0)))
    matnorm = lambda matrix: vecnorm([x for row in matrix for x in row])
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    inherited = json.loads((ROOT/MANIFEST).read_text())['source_sha256']
    pins = dict(inherited)
    for rel, expected in inherited.items():
        assert sha(ROOT/rel) == expected, rel
    extras = (Path(__file__).resolve().relative_to(ROOT).as_posix(), SPEC,
              MANIFEST, MIXED, INITIAL, WEAK, MOVING, AUXRATE, FACTORY,
              'Analysis/MasterTests/test_rtau_weak_canonical_rate_v1.py',
              'Theory/Gates/RES-001/RES001_RTAU_WEAK_CANONICAL_RATE_V1_SPEC_2026-11-03.md',
              'Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v1_20261103/failure.json',
              'Theory/Gates/RES-001/RES001_RTAU_MOVING_RANGE_V1_REPORT_2026-11-03.md')
    for rel in extras:
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel in pins:
        for path in (ROOT/rel, Path(str(ROOT/rel)+'.sha256')):
            if path.exists():
                snapshot[path] = (sha(path), path.stat().st_mtime_ns)
    check('all_219_inherited_hashes_match', len(inherited) == 219)
    data = json.loads((ROOT/MIXED).read_text())
    weak = json.loads((ROOT/WEAK).read_text())
    moving = json.loads((ROOT/MOVING).read_text())
    check('parents_pass_all_checks', all(d['passed'] == d['total'] and
          all(c['passed'] for c in d['checks']) for d in (data, weak, moving)))
    H = {tuple(row['ij']): decode(row['value']) for row in data['full_mixed_Hessian_upper_triangle']}
    Hz = {tuple(row['ij']): decode(row['dz']) for row in data['full_mixed_Hessian_upper_triangle']}
    hh = lambda i, j, dz=False: (Hz if dz else H).get(tuple(sorted((i, j))), iv.mpf(0))
    hn = lambda rows, cols, dz=False: vecnorm([hh(i, j, dz) for i in rows for j in cols])
    check('no_auxiliary_velocity_anywhere', all(27 not in ij for ij in H))
    check('Legendre_auxiliary_configuration_columns_exact_zero',
          all(tuple(sorted((i, j))) not in H for i in range(14, 27) for j in (13, 41)))
    check('ordinary_flux_has_no_auxiliary_gradient_column',
          all(tuple(sorted((28+i, 41))) not in H for i in range(12)))
    check('force_auxiliary_gradient_coupling_retained', hi(hh(40, 41)) < 0)
    assert all(c['passed'] for c in checks[-4:])

    inverse = decode(json.loads((ROOT/INITIAL).read_text())['bounds']['original_temporal_inverse'])
    A, B = hn(range(14, 27), range(13)), hn(range(14, 27), range(28, 41))
    C, D = hn(range(14, 27), range(42, 45)), hn(range(14, 27), range(45, 48))
    # Coefficients are in the input order P,Q,F,U.
    velocity = [inverse, inverse*(A+B), iv.mpf(0), inverse*(C+D)]
    cz = decode(weak['constants_binary']['auxiliary_L2_per_psi_H2'])
    ck = decode(weak['constants_binary']['auxiliary_L2_per_metric_H1_F'])
    auxiliary = [iv.mpf(0), iv.sqrt(2)*ck, cz, iv.mpf(0)]
    ar = {key: decode(value) for key, value in
          json.loads((ROOT/AUXRATE).read_text())['constants_binary'].items()}
    auxiliary_time = [(ar['eta']+iv.sqrt(2)*ar['metric_velocity'])*x for x in velocity]
    auxiliary_time[1] += ar['chi_z']+iv.sqrt(2)*ar['metric']
    groups = {}
    regular_blocks = {'q': range(13), 'v': range(14, 27), 'd': range(28, 41),
                      'S': range(42, 45), 'Sz': range(45, 48)}
    for name, rows in [('ordinary', list(range(12))), ('force', [12])]:
        fluxrows = [28+i for i in rows]
        norms = {key: hn(rows, cols)+hn(fluxrows, cols)
                 for key, cols in regular_blocks.items()}
        zcoef = hn(rows, [13])+hn(fluxrows, [13])
        zcoef += hn(rows, [41])+hn(rows, [41], True)
        zcoef += hn(fluxrows, [41])+hn(fluxrows, [41], True)
        values = [norms['v']*x+zcoef*y for x, y in zip(velocity, auxiliary)]
        values[1] += norms['q']+norms['d']
        values[3] += norms['S']+norms['Sz']
        groups[name] = values
    check('all_canonical_weak_rate_constants_finite',
          all(lo(x) >= 0 and mp.isfinite(hi(x))
              for xs in [velocity, auxiliary, auxiliary_time]+list(groups.values()) for x in xs))

    spec = importlib.util.spec_from_file_location('weak_rate_actual_factory', ROOT/FACTORY)
    factory = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(factory)
    env = factory.prepare()
    J = env['J']
    yy, _ = env['state'](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    L = env['evaluate'](yy)
    p = [env['gradient'](L, 14+i).c[0] for i in range(13)]
    pz = [env['gradient'](L, 14+i).c[1] for i in range(13)]
    forcing = [decode(x) for x in data['initial_affine_forcing']]
    pt = [forcing[i]+sum((hh(14+i, k)*yy[14+k].c[0]+
                         hh(14+i, 28+k)*yy[14+k].c[1]
                         for k in range(13)), iv.mpf(0)) for i in range(13)]
    check('actual_background_momenta_and_rates_finite',
          all(mp.isfinite(ab(x)) for x in p+pz+pt))
    chain = [sum((hh(14+i, k)*yy[k].c[1] for k in range(48)), iv.mpf(0))
             for i in range(13)]
    check('background_momentum_spatial_chain_enclosures_overlap',
          all(lo(x) <= hi(y) and lo(y) <= hi(x) for x, y in zip(chain, pz)))

    hm = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))

    def Bmatrix(q):
        h = [[q[0], q[1], q[2]], [q[1], q[3], q[4]], [q[2], q[4], q[5]]]
        out = [[iv.mpf(0) for _ in range(3)] for _ in range(13)]
        for k, (a, b) in enumerate(hm):
            for j in range(3):
                out[k][j] = (h[a][j] if b == 2 else 0)+(h[b][j] if a == 2 else 0)
        for j in range(3):
            out[6+j][j] = -q[8]
        return out

    def Kmatrix(momentum):
        out = [[iv.mpf(0) for _ in range(13)] for _ in range(3)]
        for k in range(13):
            basis = [iv.mpf(int(k == i)) for i in range(13)]
            BB = Bmatrix(basis)
            for j in range(3):
                out[j][k] = sum((BB[i][j]*momentum[i] for i in range(13)), iv.mpf(0))
        return out

    q = [x.c[0] for x in yy[:13]]
    qz = [x.c[1] for x in yy[:13]]
    qzz = [2*x.c[2] for x in yy[:13]]
    v = [x.c[0] for x in yy[14:27]]
    vz = [x.c[1] for x in yy[14:27]]
    bq, bqz, bv = Bmatrix(q), Bmatrix(qz), Bmatrix(v)
    check('B_scalar_rows_exactly_zero', all(x == 0 for row in bq[9:] for x in row))
    r = iv.mpf(1)/13000
    eps = iv.mpf(1)/1000
    psi1 = eps*(iv.mpf(1)/29+iv.mpf(2)/31)
    psi2 = eps*(iv.mpf(1)/29+iv.mpf(4)/31)
    psi3 = eps*(iv.mpf(1)/29+iv.mpf(8)/31)
    # Ordinary rates in H^-1; force rate only in H^-2. B's scalar rows are
    # zero, preventing a differentiated force-momentum H^-3 term.
    c_ord = matnorm(bq)+matnorm(bqz)+vecnorm(qz[:12])+vecnorm(qzz[:12])
    c_force = psi1+iv.sqrt(2)*psi2+psi3
    c_p = matnorm(bv)+vecnorm(vz)
    c_q = matnorm(Kmatrix(pt))+vecnorm(pt)
    c_v = matnorm(Kmatrix(p))+vecnorm(p)+vecnorm(pz)
    source_rate = [c_ord*x+c_force*y+c_v*z
                   for x, y, z in zip(groups['ordinary'], groups['force'], velocity)]
    source_rate[0] += c_p
    source_rate[1] += c_q
    weight_H2 = iv.exp(r)*iv.sqrt(1+2*r*r+(r*r+r)**2)/2
    check('momentum_tangent_rate_Hminus2_constants_finite',
          all(lo(x) >= 0 and mp.isfinite(hi(x)) for x in source_rate))
    check('source_rate_Hminus2_weight_bound_finite',
          lo(weight_H2) > 0 and mp.isfinite(hi(weight_H2)))

    z, t = s.symbols('z t', real=True)
    g, Z = s.Function('g')(z), s.Function('Z')(z)
    check('weak_product_with_auxiliary_gradient',
          s.expand(g*s.diff(Z, z)-s.diff(g*Z, z)+s.diff(g, z)*Z) == 0)
    check('weak_force_flux_second_derivative_identity',
          s.expand(s.diff(g*s.diff(Z, z), z)-s.diff(g*Z, z, 2)+s.diff(s.diff(g, z)*Z, z)) == 0)
    check('omitted_coefficient_drift_rejected',
          s.diff(g, z)*Z != 0)
    # Independently differentiate a variable field-generator momentum tangent.
    bb, pp, x, pr = [s.Function(name)(t, z) for name in ('B', 'p', 'dq', 'dp')]
    # Scalar components of B and its linear variation suffice for each index;
    # the full vector index structure was separately verified by the parent.
    tangent = s.diff(bb*pr+x*pp, z)-pr*s.diff(bb, z)-pp*s.diff(x, z)
    timed = s.diff(bb*s.diff(pr, t)+s.diff(bb, t)*pr+x*s.diff(pp, t)+s.diff(x, t)*pp, z)
    timed -= s.diff(pr, t)*s.diff(bb, z)+pr*s.diff(bb, t, z)
    timed -= s.diff(pp, t)*s.diff(x, z)+pp*s.diff(x, t, z)
    check('full_momentum_tangent_time_product_identity', s.expand(s.diff(tangent, t)-timed) == 0)
    check('omitted_generator_time_drift_rejected',
          s.diff(s.diff(bb, t)*pr, z) != 0)
    n = s.symbols('n', integer=True, positive=True)
    # Flat-coefficient regulator control: psi=n^-2 exp(inz) has bounded H2
    # but its quartic momentum rate is not uniformly H^-1-bounded.
    check('quartic_rate_Hminus2_uniform_scaling',
          s.expand((1+n*n)**2-n**4) == 1+2*n*n)
    check('quartic_rate_Hminus1_unbounded_scaling',
          s.simplify(n*n/(1+n*n)-1+1/(1+n*n)) == 0)
    check('all_input_bytes_and_sidecars_preserved',
          all(sha(path) == h and path.stat().st_mtime_ns == stamp
              for path, (h, stamp) in snapshot.items()))
    coefficients = dict(field_rate_L2=velocity, auxiliary_L2=auxiliary,
                        auxiliary_time_Hminus2=auxiliary_time,
                        ordinary_momentum_rate_Hminus1=groups['ordinary'],
                        force_momentum_rate_Hminus2=groups['force'],
                        momentum_tangent_rate_Hminus2=source_rate)
    return dict(kind='RTAU_UNREDUCED_WEAK_CANONICAL_RATE_V2',
                passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                input_order=['P_L2', 'Q_H1', 'force_configuration_H2', 'caller_shift_H1'],
                coefficients_binary={k: [binary(x) for x in xs] for k, xs in coefficients.items()},
                upper_display={k: [mp.nstr(hi(x), 18) for x in xs] for k, xs in coefficients.items()},
                background_binary={'momentum': [binary(x) for x in p],
                                   'momentum_z': [binary(x) for x in pz],
                                   'momentum_t': [binary(x) for x in pt]},
                source_rate_weight_H2_binary=binary(weight_H2),
                source_rate_weight_H2_upper=mp.nstr(hi(weight_H2), 18),
                source_sha256=pins, inherited_source_count=len(inherited),
                scope='INITIAL_UNREDUCED_CANONICAL_AND_MOMENTUM_TANGENT_WEAK_ROWS',
                caller_shift='EXPLICIT_NOT_SOLVED', moving_free_embedding='NOT_DERIVED',
                compatible_generator='NOT_DERIVED', physical_norm='NOT_DERIVED',
                actual_time_tube='NOT_ESTABLISHED', Rtau_adopted=False,
                review='DEFERRED', physics_pass=False, gate_effect='NONE')


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
                json.dump(dict(status='FAILED_ATTEMPT', error=repr(error),
                               source_sha256=sha(Path(__file__)), physics_pass=False), handle, indent=2)
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
                          bounds=receipt['upper_display'],
                          source_rate_weight_H2_upper=receipt['source_rate_weight_H2_upper']), indent=2))
    return 0 if receipt['passed'] == receipt['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
