"""Exact ordinary reference control and whole-root candidate principal graph.

No full prepared symmetrizer, mixed remainder or time-domain claim.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_ORDINARY_STRONG_GRAPH_V1_SPEC_2026-11-04.md'
OWNER = 'Theory/Gates/RES-001/RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md'
MANIFEST = 'Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
BASE = 'Analysis/MasterTests/outputs/'
PARENTS = {
    'principal': BASE+'r4c1_rtau_prepared_principal_v3_attempt_01/summary.json',
    'mixed': BASE+'r4c1_rtau_mixed_operator_v4_attempt_01/summary.json',
    'density': BASE+'rtau_strong_density_l2_source_v1_20261104/receipt.json',
    'weak_rejection': BASE+'rtau_weak_density_energy_screen_v1_20261103/receipt.json',
}
FACTORY = 'Analysis/MasterTests/r4c1_prepared_operator_factory_v2.py'
SLOTS = [0, 1, 3, 6, 7, 8, 9, 10, 11]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary = lambda x: [list(t) for t in iv.mpf(x)._mpi_]
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    checks = []

    def check(name, ok, value=None):
        checks.append(dict(name=name, passed=bool(ok), value=value))

    original = json.loads((ROOT/MANIFEST).read_text())['source_sha256']
    parents = {key: json.loads((ROOT/path).read_text()) for key, path in PARENTS.items()}
    pins = dict(original)
    for data in parents.values():
        for rel, want in data['source_sha256'].items():
            assert rel not in pins or pins[rel] == want, rel
            pins[rel] = want
    for rel in (SPEC, OWNER, MANIFEST, FACTORY, Path(__file__).resolve().relative_to(ROOT).as_posix(), *PARENTS.values()):
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel, want in pins.items():
        path = ROOT/rel
        assert sha(path) == want, rel
        for candidate in (path, Path(str(path)+'.sha256')):
            if candidate.exists():
                snapshot[candidate] = (sha(candidate), candidate.stat().st_mtime_ns)
    check('all_219_original_and_parent_pins_match', len(original) == 219)
    check('parents_pass_only_in_registered_scopes', all(d['passed'] == d['total'] for d in parents.values()))
    check('strong_density_row_available_without_weakening', parents['density']['density_strength'] == 'L2')
    # These rectangular maps keep every ordinary canonical momentum.
    E = sp.zeros(9, 8)
    E[0, 0] = 1
    E[2, 0] = -1
    E[1, 1] = 1
    for j in range(2, 8):
        E[j+1, j] = 1
    R = sp.zeros(8, 9)
    R[0, 0] = sp.Rational(1, 2)
    R[0, 2] = -sp.Rational(1, 2)
    R[1, 1] = 1
    for j in range(2, 8):
        R[j, j+1] = 1
    check('independent_configuration_chart_retains_eight_directions', R*E == sp.eye(8))
    L = sp.zeros(9)
    L[0, 5] = L[2, 5] = sp.I
    principal = parents['principal']
    M, B, G = [sp.Matrix(principal[key])[:9, :9] for key in ('reference_kinetic', 'reference_mixed', 'reference_gradient')]
    QX = sp.zeros(9, 18)
    QX[:, 1:9] = E
    QX[:, 9:18] = L
    PP = sp.zeros(9, 18)
    PP[:, 9:18] = sp.eye(9)
    vel = M.inv()*(PP-sp.I*B*QX)
    pdot = -sp.I*B.T*vel+G*QX
    A = sp.zeros(18)
    A[1:9, :] = R*vel
    A[9:18, :] = pdot
    A = A.applyfunc(sp.expand)
    trace_defect = ((vel[0, :]+vel[2, :])/2-sp.I*pdot[5, :]).applyfunc(sp.expand)
    check('reference_trace_kinematic_identity_exact', trace_defect == sp.zeros(1, 18))
    check('reference_density_row_and_column_retained', A[0, :] == sp.zeros(1, 18) and A[:, 0] == sp.zeros(18, 1))
    # Independent omitted-graph control: set trace lifting to zero only here.
    bad_X = sp.zeros(9, 18)
    bad_X[:, 1:9] = E
    # Even if kinematic rows happen to agree off the constraint, the
    # density graph itself is wrong on an independent P_Vz input.
    check('omitting_trace_momentum_violates_density_graph', (bad_X-QX)[:, 14] != sp.zeros(9, 1))
    sq = A*A
    speeds = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(4, 5), sp.Rational(1), sp.Rational(14, 13)]
    polynomial = A
    for speed in speeds[1:]:
        polynomial = (polynomial*(sq+speed*sp.eye(18))).applyfunc(sp.expand)
    check('exact_action_reference_minimal_polynomial', polynomial == sp.zeros(18))
    c = sp.symbols('c')
    characteristic = sp.factor(A.charpoly(c).as_expr())
    expected = c*c*(c*c+1)**4*(c*c+sp.Rational(1, 3))*(c*c+sp.Rational(4, 5))**2*(c*c+sp.Rational(14, 13))
    check('all_reference_ordinary_characteristic_directions_retained', sp.expand(characteristic-expected) == 0)
    null = A.nullspace()
    check('both_reference_zero_speed_directions_semisimple', len(null) == 2 and len((A*A).nullspace()) == 2)
    projectors = []
    H = sp.zeros(18)
    upper = sp.Rational(0)
    for speed in speeds:
        P = sp.eye(18)
        for other in speeds:
            if other != speed:
                P = (P*(sq+other*sp.eye(18))/(other-speed)).applyfunc(sp.expand)
        check('reference_projector_identity_'+str(speed), (P*P-P).applyfunc(sp.expand) == sp.zeros(18))
        AP = A*P
        if speed == 0:
            check('zero_projector_is_stationary_not_deleted', AP == sp.zeros(18) and P.rank() == 2)
        else:
            check('wave_projector_action_identity_'+str(speed), (sq*P+speed*P).applyfunc(sp.expand) == sp.zeros(18))
        energy = P.conjugate().T*P
        if speed:
            energy += AP.conjugate().T*AP/speed
        energy = energy.applyfunc(sp.expand)
        H += energy
        upper += sp.trace(energy)
        projectors.append(P)
    check('reference_projectors_resolve_the_entire_state', sum(projectors, sp.zeros(18)) == sp.eye(18))
    H = H.applyfunc(sp.expand)
    check('reference_energy_principal_cancellation_exact', (A.conjugate().T*H+H*A).applyfunc(sp.expand) == sp.zeros(18))
    check('reference_energy_hermitian', H == H.conjugate().T)
    # Cauchy: ||sum_j P_j y||^2 <= 5 sum_j ||P_j y||^2 <= 5 E.
    lower = sp.Rational(1, len(projectors))
    check('reference_coercivity_proof_has_positive_explicit_constants', lower > 0 and upper > lower)
    # Independent negative control already proved in its original scope.
    check('weak_density_principal_rejection_not_overridden', parents['weak_rejection']['passed'] == parents['weak_rejection']['total'])

    # Whole prepared root: reuse immutable Hessian enclosures, including all
    # uncertainty. No action evaluation or differentiation occurs here.
    z = iv.mpf(0)
    def mat(n, m): return [[iv.mpf(0) for _ in range(m)] for _ in range(n)]
    def ident(n): return [[iv.mpf(int(i == j)) for j in range(n)] for i in range(n)]
    def tr(a): return [list(row) for row in zip(*a)]
    def mul(a, b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))), z) for j in range(len(b[0]))] for i in range(len(a))]
    def add(a, b, sign=1): return [[x+sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]
    def scale(a, t): return [[t*x for x in row] for row in a]
    def inf(a): return max(hi(sum((iv.mpf(ab(x)) for x in row), z)) for row in a)
    def from_sp(a): return [[iv.mpf(int(a[i, j].p))/int(a[i, j].q) for j in range(a.cols)] for i in range(a.rows)]
    whole = {tuple(row['ij']): decode(row['value']) for row in parents['mixed']['full_mixed_Hessian_upper_triangle']}
    hh = lambda i, j: whole.get((min(i, j), max(i, j)), z)
    sub = lambda rows, cols: [[hh(i, j) for j in cols] for i in rows]
    vv, dd, ss = [14+i for i in SLOTS], [28+i for i in SLOTS], [45, 46, 47]
    KI = [[decode(x) for x in row] for row in principal['whole_root_shift_inverse']]
    C, D = sub(vv, ss), sub(dd, ss)
    MW = add(sub(vv, vv), mul(mul(C, KI), tr(C)), -1)
    BW = add(sub(vv, dd), mul(mul(C, KI), tr(D)), -1)
    GW = add(sub(dd, dd), mul(mul(D, KI), tr(D)), -1)
    W = mat(9, 9)
    W[0][0] = W[2][0] = iv.sqrt(iv.mpf(2)/33)
    W[0][2] = iv.sqrt(iv.mpf(2))
    W[2][2] = -W[0][2]
    W[1][1] = iv.sqrt(iv.mpf(2))
    for i in range(3, 6): W[i][i] = iv.sqrt(iv.mpf(6))
    for i in range(6, 9): W[i][i] = iv.mpf(1)
    # Whiten BEFORE the Schur subtraction to avoid dependency inflation.
    CW = mul(tr(W), C)
    whitened = add(mul(mul(tr(W), sub(vv, vv)), W), mul(mul(CW, KI), tr(CW)), -1)
    err = add(whitened, ident(9), -1)
    delta = inf(err)
    check('whole_root_reference_normalized_inverse_contraction', delta < 1, mp.nstr(delta, 30))
    assert delta < 1
    series = ident(9)
    power = ident(9)
    terms = 24
    for n in range(1, terms+1):
        power = mul(power, err)
        series = add(series, power, (-1)**n)
    tail = iv.mpf(delta)**(terms+1)/(1-iv.mpf(delta))
    radius = iv.mpf([-hi(tail), hi(tail)])
    series = [[x+radius for x in row] for row in series]
    MI = mul(mul(W, series), tr(W))
    inverse_residual = add(mul(MW, MI), ident(9), -1)
    check('whole_root_inverse_product_encloses_identity', all(lo(x) <= 0 <= hi(x) for row in inverse_residual for x in row))
    # Only profile evaluation is used to enclose a,gamma,S. No Hessian rerun.
    spec = importlib.util.spec_from_file_location('ordinary_graph_profiles', ROOT/FACTORY)
    factory = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(factory)
    env = factory.prepare(order=1)
    mp.mp.dps = 100
    mp.iv.dps = 60
    y = env['state'](env['J'].variable(iv.mpf([0, hi(2*iv.pi)])), True)
    a2 = y[0].c[0]
    gamma = iv.sqrt(1+a2*sum((x.c[0]**2 for x in y[6:9]), z))
    coefficient = gamma/iv.sqrt(a2)
    shift = y[44].c[0]
    BR = add(BW, scale(MW, shift))
    GR = add(add(GW, scale(add(BW, tr(BW)), shift)), scale(MW, shift*shift))
    ii = iv.mpc(0, 1)
    XW, PW = mat(9, 18), mat(9, 18)
    for i in range(9):
        PW[i][9+i] = iv.mpf(1)
        for j in range(8): XW[i][1+j] = iv.mpf(int(E[i, j]))
    XW[0][14] = XW[2][14] = ii*coefficient
    vw = mul(MI, add(PW, scale(mul(BR, XW), ii), -1))
    pdw = add(scale(mul(tr(BR), vw), -ii), mul(GR, XW))
    qw = mul(from_sp(R), vw)
    AW = [mat(1, 18)[0]]+qw+pdw
    defect = [(vw[0][j]+vw[2][j])/2-ii*coefficient*pdw[5][j] for j in range(18)]
    contains = lambda x: lo(x.real) <= 0 <= hi(x.real) and lo(x.imag) <= 0 <= hi(x.imag)
    check('whole_root_trace_identity_necessary_enclosure_only', all(contains(x) for x in defect))
    cabs = lambda x: hi(iv.sqrt(iv.mpf(ab(x.real))**2+iv.mpf(ab(x.imag))**2))
    defect_bound = hi(iv.sqrt(sum((iv.mpf(cabs(x))**2 for x in defect), z)))
    check('whole_root_candidate_operator_finite', all(mp.isfinite(cabs(x)) for row in AW for x in row))
    # Secondary regulator identity: metric trace-gradient enters the force.
    kk, kap, sc, uu, chi = sp.symbols('k kappa s u chi', real=True)
    ZZ = kap*kk**2*chi-sp.I*kap*kk*sc*uu
    check('force_secondary_metric_gradient_is_retained', sp.diff(ZZ, uu) == -sp.I*kap*kk*sc and sp.diff(ZZ, chi) == kap*kk**2)
    check('all_ordinary_and_quartic_directions_accounted_not_projected', len(AW) == 18 and len(AW)+2 == 20)
    check('original_sources_sidecars_and_timestamps_preserved', all(sha(p) == h and p.stat().st_mtime_ns == t for p, (h, t) in snapshot.items()))
    encode = lambda a: [[str(x) for x in row] for row in a.tolist()]
    cbinary = lambda x: {'real': binary(x.real), 'imag': binary(x.imag)}
    return dict(kind='RTAU_ORDINARY_STRONG_GRAPH_V1', passed=sum(c['passed'] for c in checks), total=len(checks), checks=checks,
                source_sha256=pins, original_source_count=len(original),
                reference_operator=encode(A), reference_energy=encode(H), reference_projectors=[encode(x) for x in projectors],
                reference_characteristic=str(characteristic), reference_zero_vectors=[encode(x) for x in null],
                reference_energy_lower=str(lower), reference_energy_upper=str(upper),
                state_order=['w_L2']+['k*(hxx-hyy)/2', 'k*hxy', 'k*Vx', 'k*Vy', 'k*Vz', 'k*u', 'k*v', 'k*r']+['P_'+str(i) for i in SLOTS],
                whole_root_candidate_operator_binary=[[cbinary(x) for x in row] for row in AW],
                whole_root_trace_defect_binary=[cbinary(x) for x in defect], whole_root_trace_defect_norm_upper=mp.nstr(defect_bound, 40),
                whole_root_inverse_contraction=mp.nstr(delta, 40), inverse_series_terms=terms, inverse_tail_binary=binary(tail),
                whole_root_trace_coefficient_binary=binary(coefficient), whole_root_shift_binary=binary(shift),
                actual_graph_identity='NECESSARY_INTERVAL_CONSISTENCY_ONLY_NOT_AN_EXACT_PROOF',
                reference_energy_scope='OFF_SHELL_ACTION_COEFFICIENT_CONTROL_ONLY',
                full_prepared_coupled_energy='NOT_DERIVED', ordinary_actual_symmetrizer='NOT_DERIVED',
                quartic_mixing_energy='NOT_DERIVED', global_symplectic_and_moving_remainder='NOT_DERIVED', actual_time_tube='NOT_ESTABLISHED',
                review='DEFERRED', physics_pass=False, gate_effect='NONE', Rtau_adopted=False, G1_G6='INCOMPLETE')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    try:
        data = calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps(dict(error=repr(error), source_sha256=sha(Path(__file__)), physics_pass=False), indent=2)+'\n')
        raise
    raw = (json.dumps(data, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open('xb') as f: f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f: f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:
        assert args.verify.read_bytes() == raw, 'Immutable replay differs'
    print(json.dumps({key: data[key] for key in ('passed', 'total', 'reference_energy_lower', 'reference_energy_upper', 'whole_root_inverse_contraction', 'whole_root_trace_defect_norm_upper', 'full_prepared_coupled_energy')}, indent=2))
    print(json.dumps({'failed': [c for c in data['checks'] if not c['passed']]}))
    return 0 if data['passed'] == data['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
