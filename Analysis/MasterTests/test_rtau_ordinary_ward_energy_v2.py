"""Actual ordinary Ward identity and attempted whole-root action energy.

No quartic/moving/global/time-domain admission is inferred.
"""
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_ORDINARY_WARD_ENERGY_V2_SPEC_2026-11-04.md'
OWNER = 'Theory/Gates/RES-001/RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md'
PREVIOUS = 'Analysis/MasterTests/test_rtau_ordinary_strong_graph_v1.py'
RECEIPT = 'Analysis/MasterTests/outputs/rtau_ordinary_strong_graph_v1_20261104/receipt.json'
BODY = 'Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
WEAK = 'Analysis/MasterTests/r4c1_full_weak_action_v1.py'
ROUTE = 'Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
PARAMETERS = 'Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT/rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    decode = lambda x: iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary = lambda x: [list(t) for t in iv.mpf(x)._mpi_]
    checks = []

    def check(name, ok, value=None): checks.append(dict(name=name, passed=bool(ok), value=value))

    old = load('immutable_ordinary_graph_setup', PREVIOUS)
    parent = json.loads((ROOT/RECEIPT).read_text())
    pins = dict(parent['source_sha256'])
    for rel in (PREVIOUS, RECEIPT, BODY, WEAK, ROUTE, PARAMETERS, SPEC, OWNER, 'Analysis/MasterTests/test_rtau_ordinary_ward_energy_v1.py', 'Theory/Gates/RES-001/RES001_RTAU_ORDINARY_WARD_ENERGY_V1_SPEC_2026-11-04.md', 'Analysis/MasterTests/outputs/rtau_ordinary_ward_energy_v1_20261104/failure.json', Path(__file__).resolve().relative_to(ROOT).as_posix()):
        if rel in pins: assert pins[rel] == sha(ROOT/rel), rel
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel, want in pins.items():
        p = ROOT/rel
        assert sha(p) == want, rel
        for path in (p, Path(str(p)+'.sha256')):
            if path.exists(): snapshot[path] = (sha(path), path.stat().st_mtime_ns)
    check('original_219_and_all_inherited_pins_match', parent['original_source_count'] == 219)
    check('reference_parent_checks_pass_in_their_scope', parent['passed'] == parent['total'])
    par = load('ordinary_Ward_exact_parameters', PARAMETERS).parameters()
    check('registered_MP2_is_one_not_an_assumed_new_normalization', par['MP2'] == 1)

    # Exact direction in arbitrary frozen orthonormal derivative data.
    # gamma is independent here: no use of a rounded gamma^2 relation.
    vx, vy, vz, gamma, e, MP2 = sp.symbols('vx vy vz gamma e MP2', nonzero=True, real=True)
    V = sp.Matrix([vx, vy, vz])
    kxx, kxy, kxz, kyy, kyz, kzz = sp.symbols('kxx kxy kxz kyy kyz kzz', real=True)
    K = sp.Matrix([[kxx, kxy, kxz], [kxy, kyy, kyz], [kxz, kyz, kzz]])
    DV = sp.Matrix(3, 3, sp.symbols('dv0:9', real=True))
    X = sp.Matrix(sp.symbols('x0:3', real=True))

    def tensor(k, dv, x):
        acc3 = x+k*V
        out = sp.zeros(4)
        out[0, 0] = (V.dot(acc3))/gamma
        for j in range(3): out[0, j+1] = acc3[j]
        for i in range(3):
            out[i+1, 0] = sum(V[j]*dv[i, j] for j in range(3))/gamma+(k*V)[i]
            for j in range(3): out[i+1, j+1] = dv[i, j]+gamma*k[i, j]
        return out

    dk = sp.zeros(3)
    dk[2, 2] = -e
    ddv = sp.zeros(3)
    ddv[2, 2] = gamma*e
    dx = sp.Matrix([0, 0, vz*e])
    T = tensor(K, DV, X)
    TT = tensor(K+dk, DV+ddv, X+dx)
    check('all_16_frame_derivative_tensor_components_invariant', (TT-T).applyfunc(sp.expand) == sp.zeros(4))
    n = sp.Matrix([gamma, vx, vy, vz])
    check('frame_acceleration_contraction_invariant', ((TT-T).T*n).applyfunc(sp.expand) == sp.zeros(4, 1))
    adm = lambda k: MP2*(sp.trace(k*k)-sp.trace(k)**2)/2
    check('exact_ADM_direction_is_transverse_trace', sp.expand(adm(K+dk)-adm(K)-e*MP2*(kxx+kyy)) == 0)
    # Confirm the proof tensor is the exact pinned source tensor, including
    # both X+K*V and the spatial temporal component; no replacement action.
    tree = ast.parse((ROOT/BODY).read_text(encoding='utf-8-sig'))
    body = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'body')
    strings = {ast.unparse(node) for node in ast.walk(body) if isinstance(node, ast.Assign)}
    required = {
        'a = [x + z for x, z in zip(y[6:9], mv(hi, kv))]',
        'B[0][0] = dot(V, mv(h, a)) / gam',
        'B[0][j + 1] = a[j]',
        'B[i + 1][0] = dot(hv, DV[i]) / gam + kv[i]',
        'B[i + 1][j + 1] = DV[i][j] + gam * khi[i][j]',
    }
    check('pinned_action_uses_every_proved_tensor_component', required <= strings, sorted(required-strings))
    weak_tree = ast.parse((ROOT/WEAK).read_text())
    weak_strings = {ast.unparse(node) for node in ast.walk(weak_tree) if isinstance(node, ast.Assign)}
    check('pinned_shift_X_and_K_normalization_match_direction',
          'X = [(v[6 + i] - R * d[6 + i] + q[8] * Sz[i] + gamma * hi[i][2] * Nz) / N for i in range(3)]' in weak_strings
          and 'K.append((v[slot] - lie) / (2 * N))' in {ast.unparse(node) for node in ast.walk(weak_tree) if isinstance(node, ast.Expr)})
    # Restore physical derivatives and volume, including lapse; this is
    # a frozen-principal rescaling, not a future conformal evolution ansatz.
    aa, NN, ga, htx, hty = sp.symbols('a N gam htx hty', positive=True)
    restored = NN*aa**3*MP2*((htx/(NN*aa**2)+hty/(NN*aa**2))/2)*e
    check('conformal_lapse_volume_restoration_exact', sp.simplify(restored-aa*MP2*(htx+hty)*e/2) == 0)
    # Canonical energy identity, with arbitrary real symmetric kinetic and
    # gradient blocks, requires only a symmetric B+B^T. Verify the general
    # Hamiltonian cancellation on an independent generic complex 2-field case.
    mr = sp.Matrix([[2, sp.Rational(1, 7)], [sp.Rational(1, 7), 3]])
    br = sp.Matrix([[sp.Rational(1, 5), sp.Rational(1, 3)], [sp.Rational(-2, 7), sp.Rational(1, 11)]])
    gr = sp.Matrix([[sp.Rational(2, 9), sp.Rational(1, 13)], [sp.Rational(1, 13), sp.Rational(-5, 8)]])
    qi = sp.eye(2).row_join(sp.zeros(2))
    pi = sp.zeros(2).row_join(sp.eye(2))
    vv = mr.inv()*(pi-sp.I*br*qi)
    pd = -sp.I*br.T*vv+gr*qi
    gen = vv.col_join(pd)
    hh = (pi-sp.I*br*qi).conjugate().T*mr.inv()*(pi-sp.I*br*qi)-qi.conjugate().T*gr*qi
    check('independent_full_canonical_energy_identity', (gen.conjugate().T*hh+hh*gen).applyfunc(sp.expand) == sp.zeros(4))

    # Reuse ONLY the frozen interval-block setup from the previous source.
    # It reads the existing action Hessian and evaluates profiles, not a
    # new action Hessian. Exact old reference tests need not be repeated.
    parents = {key: json.loads((ROOT/path).read_text()) for key, path in old.PARENTS.items()}
    principal = parents['principal']
    source_tree = ast.parse((ROOT/PREVIOUS).read_text())
    fn = copy.deepcopy(next(x for x in source_tree.body if isinstance(x, ast.FunctionDef) and x.name == 'calculate'))
    target = lambda node, name: isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)
    start = next(i for i, node in enumerate(fn.body) if target(node, 'z'))
    stop = next(i for i, node in enumerate(fn.body) if target(node, 'ii'))
    fn.name = 'exported_interval_blocks'
    fn.body = fn.body[start:stop]+[ast.Return(ast.Call(ast.Name('locals', ast.Load()), [], []))]
    scope = dict(iv=iv, mp=mp, sp=sp, parents=parents, principal=principal, ROOT=ROOT, FACTORY=old.FACTORY,
                 check=check, lo=lo, hi=hi, ab=ab, decode=decode, importlib=importlib, SLOTS=old.SLOTS)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), '<immutable-exported-block-setup>', 'exec'), scope)
    ctx = scope['exported_interval_blocks']()
    mat, mul, add, tr, scale = [ctx[k] for k in ('mat', 'mul', 'add', 'tr', 'scale')]
    MI, MW, BR, GR, coeff = [ctx[k] for k in ('MI', 'MW', 'BR', 'GR', 'coefficient')]
    z = iv.mpf(0)
    ii = iv.mpc(0, 1)
    # The proved Ward identity is used algebraically, not guessed from zero
    # containment. Keep containment as a separate consistency check.
    residual = [coeff*BR[i][5]-iv.mpf(1 if i in (0, 2) else 0)/2 for i in range(9)]
    check('raw_whole_root_enclosure_consistent_with_exact_B_Ward', all(lo(x) <= 0 <= hi(x) for x in residual))
    check('raw_whole_root_enclosure_consistent_with_exact_G_Ward', all(lo(GR[i][5]) <= 0 <= hi(GR[i][5]) for i in range(9)))
    for i in range(9):
        BR[i][5] = iv.mpf(1 if i in (0, 2) else 0)/(2*coeff)
        GR[i][5] = GR[5][i] = iv.mpf(0)
    MI = scale(add(MI, tr(MI)), iv.mpf(1)/2)
    GR = scale(add(GR, tr(GR)), iv.mpf(1)/2)
    # Complement: seven Q variables (without Q_Vz), then all nine P.
    E = sp.zeros(9, 8)
    E[0, 0] = 1
    E[2, 0] = -1
    E[1, 1] = 1
    for j in range(2, 8): E[j+1, j] = 1
    R = sp.zeros(8, 9)
    R[0, 0] = sp.Rational(1, 2)
    R[0, 2] = -sp.Rational(1, 2)
    R[1, 1] = 1
    for j in range(2, 8): R[j, j+1] = 1
    qkeep = [0, 1, 2, 3, 5, 6, 7]

    def conjugate(a): return [[iv.mpc(x.real, -x.imag) for x in row] for row in tr(a)]
    def ci(x):
        real = iv.mpf(ab(x.real))
        imag = iv.mpf(ab(x.imag))
        return hi(iv.sqrt(real*real+imag*imag))
    def cinf(a): return max(hi(sum((iv.mpf(ci(x)) for x in row), z)) for row in a)
    def spiv(x):
        re, im = sp.expand_complex(x).as_real_imag()
        def real_iv(t):
            if t.is_Rational: return iv.mpf(int(t.p))/int(t.q)
            if t.is_Add: return sum((real_iv(v) for v in t.args), z)
            if t.is_Mul:
                out = iv.mpf(1)
                for v in t.args: out *= real_iv(v)
                return out
            if t.is_Pow and t.exp == sp.Rational(1, 2): return iv.sqrt(real_iv(t.base))
            if t.is_Pow and t.exp.is_Integer: return real_iv(t.base)**int(t.exp)
            if t.is_Pow and t.exp == -sp.Rational(1, 2): return 1/iv.sqrt(real_iv(t.base))
            raise TypeError(str(t))
        return iv.mpc(real_iv(re), real_iv(im))
    def ivmat(a): return [[spiv(a[i, j]) for j in range(a.cols)] for i in range(a.rows)]

    def complement_blocks(mi, b, g, c):
        X0, P0 = mat(9, 16), mat(9, 16)
        for j, slot in enumerate(qkeep):
            for i in range(9): X0[i][j] = iv.mpf(int(E[i, slot]))
        for i in range(9): P0[i][7+i] = iv.mpf(1)
        X0[0][12] = X0[2][12] = ii*c
        K0 = add(P0, scale(mul(b, X0), ii), -1)
        v = mul(mi, K0)
        pd = add(scale(mul(tr(b), v), -ii), mul(g, X0))
        qd = mul(ivmat(R), v)
        bb = [[ii*x/(2*c) for x in v[5]]]
        CC = [qd[j] for j in qkeep]+[
            [pd[i][j]-(bb[0][j] if i in (0, 2) else 0) for j in range(16)] for i in range(9)]
        HC = add(mul(mul(conjugate(K0), mi), K0), mul(mul(conjugate(X0), g), X0), -1)
        return HC, CC, bb

    H, C, b = complement_blocks(MI, BR, GR, coeff)
    # Independent exact reference complement, computed from raw action
    # reference blocks rather than inherited fitted projector weights.
    MR, B0, G0 = [sp.Matrix(principal[k])[:9, :9] for k in ('reference_kinetic', 'reference_mixed', 'reference_gradient')]
    XS = sp.zeros(9, 16)
    PS = sp.zeros(9, 16)
    for j, slot in enumerate(qkeep): XS[:, j] = E[:, slot]
    PS[:, 7:] = sp.eye(9)
    XS[0, 12] = XS[2, 12] = sp.I
    KS = PS-sp.I*B0*XS
    VS = MR.inv()*KS
    PD = -sp.I*B0.T*VS+G0*XS
    QD = R*VS
    bs = sp.I*VS[5, :]/2
    CS = QD[qkeep, :].col_join(PD-sp.Matrix([1, 0, 1, 0, 0, 0, 0, 0, 0])*bs)
    HS = (KS.conjugate().T*MR.inv()*KS-XS.conjugate().T*G0*XS).applyfunc(sp.expand)
    check('reference_complement_action_energy_conserved_exactly', (CS.conjugate().T*HS+HS*CS).applyfunc(sp.expand) == sp.zeros(16))
    check('reference_complement_generator_has_no_zero_mode', CS.det() != 0)
    # Congruence whitening of the actual action-energy quotient.
    W = sp.zeros(16)
    for j in range(7): W[j, j] = 1/sp.sqrt(HS[j, j])
    W[7, 7] = W[9, 7] = sp.sqrt(sp.Rational(33, 8))
    W[7, 9] = sp.sqrt(sp.Rational(1, 8))
    W[9, 9] = -W[7, 9]
    W[8, 8] = 1/sp.sqrt(2)
    for j in (10, 11): W[j, j] = 1/sp.sqrt(6)
    W[12, 12] = sp.sqrt(sp.Rational(2, 11))
    for j in (13, 14, 15): W[j, j] = 1
    check('reference_action_energy_whitening_exact', (W.T*HS*W).applyfunc(sp.simplify) == sp.eye(16))
    WI = W.inv()
    ww, wi = ivmat(W), ivmat(WI)
    identity16 = [[iv.mpf(int(i == j)) for j in range(16)] for i in range(16)]
    Hnormal = mul(mul(conjugate(ww), H), ww)
    hdelta = cinf(add(Hnormal, identity16, -1))
    check('whole_root_energy_perturbation_bound_is_finite', mp.isfinite(hdelta), mp.nstr(hdelta, 40))
    CN = (WI*CS*W).applyfunc(sp.simplify)
    CNinv = CN.inv().applyfunc(sp.simplify)
    Cnormal = mul(mul(wi, C), ww)
    Cerror = mul(ivmat(CNinv), add(Cnormal, ivmat(CN), -1))
    cdelta = cinf(Cerror)
    check('whole_root_complement_inverse_perturbation_finite', mp.isfinite(cdelta), mp.nstr(cdelta, 40))
    # A failed sufficient numerical bound is retained as inconclusive; it
    # is not converted to a stability/instability assertion or a failed
    # bookkeeping assertion. Acceptance fields below state the disposition.
    hcert = hdelta < 1
    ccert = cdelta < 1
    bounds = dict(energy_relative_error=mp.nstr(hdelta, 40), complement_inverse_error=mp.nstr(cdelta, 40))
    if hcert:
        frob2 = lambda a: sum((iv.mpf(ci(x))**2 for row in a for x in row), z)
        hlow = (1-iv.mpf(hdelta))/frob2(ww)
        hupp = (1+iv.mpf(hdelta))*frob2(wi)
        bounds.update(action_energy_lower_binary=binary(hlow), action_energy_upper_binary=binary(hupp))
    if ccert:
        cninv_bound = iv.mpf(cinf(ivmat(CNinv)))/(1-iv.mpf(cdelta))
        bounds['normalized_complement_inverse_bound_binary'] = binary(cninv_bound)
    check('exact_zero_direction_not_removed', all(B0[i, 5] == (sp.Rational(1, 2) if i in (0, 2) else 0) for i in range(9)) and G0[:, 5] == sp.zeros(9, 1))
    check('original_sources_and_sidecars_unchanged', all(sha(p) == h and p.stat().st_mtime_ns == t for p, (h, t) in snapshot.items()))
    cbinary = lambda x: {'real': binary(x.real), 'imag': binary(x.imag)}
    return dict(kind='RTAU_ORDINARY_WARD_ENERGY_V2', passed=sum(x['passed'] for x in checks), total=len(checks), checks=checks,
                source_sha256=pins, original_source_count=219,
                exact_Ward_identity='Brel[:,Vz]=(a*MP2/gamma)*t; Grel[:,Vz]=0', exact_trace_graph_identity=True,
                proof_scope='ALL_FROZEN_INITIAL_CONFORMAL_COEFFICIENTS_ARBITRARY_TILT_AND_ORDINARY_DERIVATIVES',
                energy_complement_binary=[[cbinary(x) for x in row] for row in H],
                generator_complement_binary=[[cbinary(x) for x in row] for row in C], zero_to_complement_row_binary=[cbinary(x) for x in b[0]],
                bounds=bounds, action_energy_complement_coercive=hcert, ordinary_complement_inverse_certified=ccert,
                complete_ordinary_energy='READY_FOR_NORM_CONSTANTS' if hcert and ccert else 'INSUFFICIENT_INTERVAL_BOUND',
                full_prepared_coupled_energy='NOT_DERIVED', quartic_mixing_energy='NOT_DERIVED',
                moving_global_symplectic_remainder='NOT_DERIVED', actual_time_tube='NOT_ESTABLISHED',
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
            (args.output.parent/'failure.json').write_bytes((json.dumps(dict(error=repr(error), source_sha256=sha(Path(__file__)), physics_pass=False), indent=2)+'\n').encode())
        raise
    raw = (json.dumps(data, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=False)
        with args.output.open('xb') as f: f.write(raw)
        with Path(str(args.output)+'.sha256').open('xb') as f: f.write((hashlib.sha256(raw).hexdigest()+'\n').encode())
    else:
        assert args.verify.read_bytes() == raw, 'Immutable replay differs'
    print(json.dumps({key: data[key] for key in ('passed', 'total', 'bounds', 'exact_trace_graph_identity', 'complete_ordinary_energy', 'full_prepared_coupled_energy')}, indent=2))
    print(json.dumps({'failed': [c for c in data['checks'] if not c['passed']]}))
    return 0 if data['passed'] == data['total'] else 1


if __name__ == '__main__': raise SystemExit(main())
