"""Finite-constraint unweighted-domain obstruction; no physical-space admission."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_FINITE_NODE_DOMAIN_V1_CONTRACT_2026-10-21.md'
CSHA = 'fbcc101c6fc653a636072bb63af789d4cad2cb3c1cf3cf1e1d2aa9a35a6d3266'
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENC = lambda obj: (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
PINS = {
    'GEMINI.md': '5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
    'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md': 'd6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
    'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md': '3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
    'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md': '14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
    'Theory/Gates/RES-001/RES001_R4C1_NODAL_DESCRIPTOR_V2_REPORT_2026-10-19.md': 'bb8f83e2e234609a10a755777e3031990037822a99fd4482115404d4cae49d3d',
    'Theory/Gates/RES-001/RES001_R4C1_GLOBAL_NODAL_LIFT_V2_REPORT_2026-10-20.md': '88549485969e0d85ed216afb0ab5ba2c7ab8a577c65bd096fe969f1172024793',
    'Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V3_REPORT_2026-10-20.md': '02aa52ccaca4f2d8f5dc4fb32090d5a5888a1b3151254200be7ac0ec6c6daedd',
    'Theory/Gates/RES-001/RES001_R4C1_PLANAR_REDUCED_HAMILTONIAN_V1_REPORT_2026-10-19.md': '175c41f50b18bb32c6b1b38edb255e61bcd656643f226c8e49171545c051c673',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_DESCRIPTOR_ACTION_V1_REPORT_2026-10-20.md': '999e7615c915b46d36859dbaafc5a72f984f75bb02ad2b5efdfdafec82d58419',
    'Theory/Gates/RES-001/RES001_R4C1_CHECKPOINTED_QR_V2_TRANCHE01_REPORT_2026-10-21.md': '0d36b4609ca129e8e5287a83a657df0de5dd9ac44cfe6f9ca6d93b9ea16b1b8e',
    'Theory/Verification/ITSM_PROVENANCE_TIMESTAMP_TRANSPORT_NOTE_2026-10-21.md': '87d8f3c56d2d782cb0c394342694e619ee155961a849b1f47d52fa53d3e15ff4',
    'Analysis/MasterTests/test_01_r4c1_nodal_descriptor_v2.py': 'b19f4ce9a665d711b3be021cfa149fe3b4753851e1c11d99bc705156537f8bf5',
    'Analysis/MasterTests/test_01_r4c1_planar_reduced_hamiltonian_v1.py': 'f03a2b9ac794569994be8112b0ba1746b8e596669c2d693c9c7310bd48cab27b',
    'Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py': '99a71aa721140a59c0e27af4632e4c52c9ae30138a8ae9af53b690b5c2cee157',
    CONTRACT: CSHA,
}


def metadata(path):
    return dict(sha256=SHA(path.read_bytes()), bytes=path.stat().st_size,
                mtime_ns=path.stat().st_mtime_ns)


def sources():
    pins = {**PINS, SELF: SHA((ROOT / SELF).read_bytes())}
    records = {}
    for name, want in pins.items():
        path = ROOT / name
        if SHA(path.read_bytes()) != want:
            raise ValueError('source drift: ' + name)
        # GEMINI is an authority file without a required adjacent sidecar.
        sidecar = Path(str(path) + '.sha256')
        if sidecar.exists():
            if sidecar.read_text().split()[0] != want:
                raise ValueError('sidecar drift: ' + name)
            records[sidecar.relative_to(ROOT).as_posix()] = metadata(sidecar)
        elif name not in ('GEMINI.md', 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md'):
            raise ValueError('required source sidecar missing: ' + name)
        records[name] = metadata(path)
    for label, module in [('sympy', sy), ('mpmath', mp)]:
        records['installed/' + label + '/__init__.py'] = metadata(Path(module.__file__))
    return pins, records


class Checks:
    def __init__(self):
        self.rows = []

    def add(self, name, condition, value=None, criterion='exact'):
        self.rows.append(dict(name=name, passed=bool(condition), value=value, criterion=criterion))


def pair(dest, name, data, replay):
    path = dest / name
    sidecar = Path(str(path) + '.sha256')
    mark = (SHA(data) + '  ' + name + '\n').encode()
    if replay:
        if path.read_bytes() != data or sidecar.read_bytes() != mark:
            raise ValueError('read-only replay mismatch: ' + name)
    else:
        with path.open('xb') as stream:
            stream.write(data)
        with sidecar.open('xb') as stream:
            stream.write(mark)


def symbolic_form(ch):
    q = sy.symbols('hxx hxy hxz hyy hyz hzz Vx Vy Vz', real=True)
    p = sy.symbols('p0:9', real=True)
    s, Z, a = sy.symbols('s Z delta_s', real=True)
    coordinates = list(q) + list(p) + [s, Z]
    g = sy.Function('g')(*q)
    theta = list(p) + [sy.Integer(0)] * 9 + [sy.Integer(0), -g * s]
    omega = sy.Matrix(20, 20, lambda i, j: sy.diff(theta[j], coordinates[i]) - sy.diff(theta[i], coordinates[j]))
    direction = sy.zeros(20, 1)
    direction[18] = a
    image = omega * direction
    ch.add('complete_symbolic_two_form_antisymmetric', omega + omega.T == sy.zeros(20))
    ch.add('pure_s_full_image_only_Z_row', image == sy.Matrix([0] * 19 + [g * a]))
    ch.add('all_nine_metric_frame_crosses_present',
           all(omega[i, 19] == -s * sy.diff(g, q[i]) for i in range(9)))
    good = sy.diff(omega[18, 19], q[0]) + sy.diff(omega[19, 0], s) + sy.diff(omega[0, 18], Z)
    ch.add('full_coupled_closure_identity', sy.simplify(good) == 0)
    ch.add('dropping_crosses_rejected_by_closure', sy.diff(-g, q[0]) != 0)
    change = sy.eye(20)
    change[0, 18] = 1
    back = change.inv() * direction
    ch.add('fixed_nonsingular_coordinate_congruence',
           sy.simplify(change.T * omega * change * back - change.T * image) == sy.zeros(20, 1))
    # The full metric/frame function g is specialized only after contraction.
    b, e, k, x = sy.symbols('b e k x', real=True)
    hxx, hxy, hxz, hyy, hyz, hzz, vx, vy, vz = q
    h = sy.Matrix([[hxx, hxy, hxz], [hxy, hyy, hyz], [hxz, hyz, hzz]])
    v = sy.Matrix([vx, vy, vz])
    actual_g = b * sy.sqrt(h.det()) * (v.T * h * v)[0]
    base = {hxx: 1, hyy: 1, hzz: 1, hxy: 0, hxz: 0, hyz: 0,
            vx: 0, vy: e * sy.sin(k * x), vz: 0}
    ch.add('registered_simple_node_coupling', sy.simplify(actual_g.subs(base) - b * e ** 2 * sy.sin(k * x) ** 2) == 0)
    ch.add('null_b_case_retained', (b * e ** 2 * sy.sin(k * x) ** 2).subs(b, 0) == 0)
    return dict(scope='Full displayed two-form contraction, arbitrary canonical spectator pairs may be added',
                image='Omega*v_s=(only Z row: g*delta_s)',
                omitted_metric_frame_crosses=False, actual_physical_mode_count_derived=False)


def normalized_kernel(matrix):
    basis = matrix.nullspace()
    if not basis:
        raise ValueError('finite coefficient system has no nonzero kernel')
    vector = basis[0]
    square = sum(z ** 2 for z in vector)
    if square == 0:
        raise ValueError('zero kernel vector cannot be normalized')
    return vector / sy.sqrt(square)


def exact_controls(ch):
    u = sy.Symbol('u', real=True)
    polynomial = (1 - u ** 2) ** 3
    I = sy.integrate(polynomial ** 2, (u, -1, 1))
    ch.add('exact_C2_control_normalization', I == sy.Rational(2048, 3003))
    ch.add('C2_control_endpoint_jets', all(sy.diff(polynomial, u, order).subs(u, sign) == 0
           for order in range(3) for sign in (-1, 1)))
    ch.add('C2_control_not_misrepresented_as_C3', sy.diff(polynomial, u, 3).subs(u, 1) != 0)
    h, rate = sy.symbols('h p', positive=True)
    alpha = rate * sy.sqrt(h) * sy.exp(-sy.Rational(1, 3)) / 2
    peak_bound = sy.exp(sy.Rational(1, 3)) / sy.sqrt(h)
    ch.add('positive_clock_amplitude_bound', sy.simplify(alpha * peak_bound - rate / 2) == 0)
    try:
        normalized_kernel(sy.eye(3))
    except ValueError:
        rejected = True
    else:
        rejected = False
    ch.add('full_rank_insufficient_space_rejected', rejected)
    ch.add('zero_vector_not_unit_norm', sy.zeros(3, 1).dot(sy.zeros(3, 1)) != 1)
    results = []
    for r in (0, 1, 2, 4, 8):
        n = r + 1
        centers = [1 + sy.Rational(2 * j + 1, 2 * n) for j in range(n)]
        width = sy.Rational(1, 4 * n)
        ch.add('strict_support_away_all_nodes_r%d' % r,
               all(1 < c - width < c + width < 2 for c in centers))
        ch.add('disjoint_supports_r%d' % r,
               all(centers[j] + width < centers[j + 1] - width for j in range(n - 1)))
        matrix = sy.Matrix(r, n, lambda i, j: sy.Rational(((i + 2) * (j + 3) + j) % 17 - 8, j + 1))
        coefficient = normalized_kernel(matrix)
        ch.add('arbitrary_rational_constraint_kernel_r%d' % r, matrix * coefficient == sy.zeros(r, 1))
        ch.add('orthogonal_bump_sum_unit_L2_r%d' % r, sy.simplify(coefficient.dot(coefficient)) == 1)
        weights = [(-1) ** j * sy.binomial(r, j) for j in range(n)]
        norm2 = sy.binomial(2 * r, r)
        ch.add('independent_binomial_norm_identity_r%d' % r, sum(w * w for w in weights) == norm2)
        moments = sy.symbols('mu0:%d' % max(1, r))
        defects = []
        for degree in range(r):
            value = sum(weights[j] * sum(sy.binomial(degree, ell) * centers[j] ** (degree - ell) *
                        width ** ell * moments[ell] for ell in range(degree + 1)) for j in range(n))
            defects.append(sy.expand(value))
        ch.add('translated_smooth_bump_moments_annihilated_r%d' % r, all(z == 0 for z in defects))
        leading2 = sum(sy.Rational(weights[j] ** 2, norm2) * sy.integrate(
            sy.expand((centers[j] + width * u) ** 4 * polynomial ** 2), (u, -1, 1)) / I for j in range(n))
        ch.add('exact_leading_coefficient_in_bounds_r%d' % r, 1 <= leading2 <= 16)
        results.append(dict(r=r, bump_count=n, centers=[str(c) for c in centers], half_width=str(width),
                            arbitrary_constraint_matrix=[[str(z) for z in row] for row in matrix.tolist()],
                            exact_kernel=[str(z) for z in coefficient], moment_coefficients=[str(z) for z in weights],
                            coefficient_norm_squared=str(norm2), leading_norm_squared=str(leading2)))
    return results


def quadrature_controls(ch, constructions):
    mp.mp.dps = 80
    def smooth_square(u):
        return mp.exp(-2 / (1 - u * u)) if abs(u) < 1 else mp.mpf(0)
    J = mp.quad(smooth_square, [-1, 0, 1])
    ch.add('smooth_normalizer_analytic_bounds', mp.exp(-mp.mpf(8) / 3) <= J <= 2 * mp.exp(-2), mp.nstr(J, 45))
    ch.add('smooth_normalized_peak_bound', mp.exp(-1) / mp.sqrt(J) <= mp.exp(mp.mpf(1) / 3))
    I = mp.mpf(2048) / 3003
    error = abs(mp.quad(lambda u: (1 - u * u) ** 6, [-1, 0, 1]) - I)
    ch.add('independent_polynomial_norm_quadrature', error < mp.mpf('1e-70'), mp.nstr(error, 20), '<1e-70')
    records = []
    for row in constructions:
        r, n = row['r'], row['bump_count']
        # C2 polynomial examples are verification controls, not the C-infinity
        # proof's entire physical constraint hierarchy.
        centers = [mp.mpf(sy.Rational(z).p) / int(sy.Rational(z).q) for z in row['centers']]
        width = mp.mpf(1) / (4 * n)
        norm2 = mp.mpf(row['coefficient_norm_squared'])
        weights2 = [mp.mpf(int(z) ** 2) / norm2 for z in row['moment_coefficients']]
        leading2 = sy.Rational(row['leading_norm_squared'])
        leading = mp.sqrt(mp.mpf(int(leading2.p)) / int(leading2.q))
        probes = []
        for text in ('.1', '.01', '.001', '.0001'):
            delta = mp.mpf(text)
            image2, remainder2 = mp.mpf(0), mp.mpf(0)
            for c, weight2 in zip(centers, weights2):
                def exact_image(u):
                    y = delta * (c + width * u)
                    return mp.sin(y) ** 4 * (1 - u * u) ** 6
                def remainder(u):
                    y = delta * (c + width * u)
                    return (mp.sin(y) ** 2 - y * y) ** 2 * (1 - u * u) ** 6
                image2 += weight2 * mp.quad(exact_image, [-1, 0, 1]) / I
                remainder2 += weight2 * mp.quad(remainder, [-1, 0, 1]) / I
            ratio = mp.sqrt(image2) / delta ** 2
            remratio = mp.sqrt(remainder2) / delta ** 4
            ch.add('two_sided_norm_bound_r%d_d%s' % (r, text), 4 / mp.pi ** 2 <= ratio <= 4,
                   mp.nstr(ratio, 45), '4/pi^2 <= ratio <= 4')
            ch.add('controlled_fourth_order_remainder_r%d_d%s' % (r, text), remratio <= mp.mpf(16) / 3,
                   mp.nstr(remratio, 45), '<=16/3')
            ch.add('norm_leading_remainder_r%d_d%s' % (r, text),
                   abs(leading - ratio) <= mp.mpf(16) / 3 * delta ** 2,
                   mp.nstr(abs(leading - ratio), 35), '<=(16/3)*delta^2')
            probes.append(dict(k_epsilon=text, image_norm_over_abs_b_e2_delta2=mp.nstr(ratio, 45),
                               remainder_norm_over_abs_b_e2_delta4=mp.nstr(remratio, 45)))
        records.append(dict(r=r, synthetic_moment_constraints=True, physical_ITSM_constraints_instantiated=False, probes=probes))
        print(json.dumps(dict(stage='norm_controls_complete', finite_conditions=r)), flush=True)
    return dict(smooth_J_quadrature=mp.nstr(J, 45), smooth_J_interval_proof='exp(-8/3)<=J<=2*exp(-2)',
                quadratures_not_certified_intervals=True, finite_constraint_controls=records)


def calculate():
    ch = Checks()
    form = symbolic_form(ch)
    constructions = exact_controls(ch)
    numerical = quadrature_controls(ch, constructions)
    return ch, dict(two_form=form, coefficient_controls=constructions, quadrature=numerical)


def execute(dest, replay):
    pins, before = sources()
    ch, independent = calculate()
    _, after = sources()
    ch.add('exact_source_sidecar_metadata_preserved', before == after)
    summary = dict(validation='PASS_CONDITIONAL_FINITE_CONSTRAINT_OBSTRUCTION_ONLY' if all(r['passed'] for r in ch.rows) else 'FAIL_DOMAIN_CONTROLS',
                   passed=sum(r['passed'] for r in ch.rows), total=len(ch.rows), checks=ch.rows,
                   source_sha256=pins, source_metadata=before,
                   scope='Finite homogeneous linear constraints plus localizable scalar-rate bulk freedom in unweighted L2',
                   actual_complete_physical_constraint_hierarchy_instantiated=False,
                   complete_physical_tangent_space_admitted=False, mixed_order_or_weighted_no_go=False,
                   all_action_no_go=False, complete372_spectrum=False, physical_cutoff_derived=False,
                   stage2_complete=False, stage3_entered=False, physics_pass=False, gate_effect='NONE',
                   review_status='DEFERRED', Rule9_cleared=False)
    formulas = dict(full_form='dTheta_other-g ds wedge dZ-s dg wedge dZ; g=b sqrt(det h) V^T h V',
                    image='Omega*v_s=(only Z row:g delta_s); dependent constraint momenta are restored',
                    construction='r+1 disjoint C-infinity unit bumps in (epsilon,2epsilon); rank-nullity for any r real linear functionals defined there',
                    domain='0<epsilon<pi/(8k), fixed finite b, e,k>0, p>0; h=I at the declared analytic slice',
                    lower='(4/pi^2)*abs(b)*e^2*k^2*epsilon^2', upper='4*abs(b)*e^2*k^2*epsilon^2',
                    image_remainder='norm[(g-b e^2 k^2 x^2)delta_s]<=(16/3)*abs(b)*e^2*k^4*epsilon^4',
                    positivity='alpha=p sqrt(h) exp(-1/3)/2; h=epsilon/[4(r+1)]; p+alpha delta_s>=p/2',
                    interpretation='Finite nodal conditions alone do not repair a uniform unweighted inverse if this bulk freedom remains; not physical admission or all-action rejection')
    for name, obj in [('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)]:
        pair(dest, name, ENC(obj), replay)
    print(json.dumps({k: summary[k] for k in ('validation', 'passed', 'total', 'physics_pass', 'gate_effect')}), flush=True)
    return 0 if all(r['passed'] for r in ch.rows) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output')
    parser.add_argument('--replay')
    args = parser.parse_args()
    if bool(args.output) == bool(args.replay):
        parser.error('choose fresh output or exact read-only replay')
    dest = (ROOT / (args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT / 'Analysis/MasterTests/outputs'):
        raise ValueError('outside research output root')
    if args.output:
        dest.mkdir(parents=True, exist_ok=False)
    previous = {p.name: metadata(p) for p in dest.iterdir()} if args.replay else None
    result = execute(dest, bool(args.replay))
    if args.replay:
        if previous != {p.name: metadata(p) for p in dest.iterdir()}:
            raise ValueError('read-only replay changed output bytes/metadata/file set')
        print('READ_ONLY_REPLAY_EXACT', flush=True)
    return result


if __name__ == '__main__':
    raise SystemExit(main())
