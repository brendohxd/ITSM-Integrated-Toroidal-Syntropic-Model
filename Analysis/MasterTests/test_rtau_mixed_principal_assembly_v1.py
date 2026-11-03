"""Retained 20-direction principal assembly; full PDE remainder stays open."""
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_MIXED_PRINCIPAL_ASSEMBLY_V1_SPEC_2026-11-04.md'
OWNER = 'Theory/Gates/RES-001/RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md'
ORDINARY = 'Analysis/MasterTests/outputs/rtau_ordinary_ward_energy_v4_20261104/receipt.json'
SETUP = 'Analysis/MasterTests/test_rtau_ordinary_strong_graph_v1.py'
PARAMETERS = 'Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'
LAPSE = 'Analysis/MasterTests/outputs/rtau_other_sector_lapse_identity_v1_20261103/receipt.json'
DENSITY = 'Analysis/MasterTests/outputs/rtau_strong_density_l2_source_v1_20261104/receipt.json'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT/rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    ordinary = json.loads((ROOT/ORDINARY).read_text())
    lapse = json.loads((ROOT/LAPSE).read_text())
    density = json.loads((ROOT/DENSITY).read_text())
    pins = dict(ordinary['source_sha256'])
    for data in (lapse, density):
        for rel, want in data['source_sha256'].items():
            assert rel not in pins or pins[rel] == want, rel
            pins[rel] = want
    for rel in (SPEC, OWNER, ORDINARY, SETUP, PARAMETERS, LAPSE, DENSITY, Path(__file__).resolve().relative_to(ROOT).as_posix()):
        if rel in pins: assert pins[rel] == sha(ROOT/rel), rel
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel, want in pins.items():
        path = ROOT/rel
        assert sha(path) == want, rel
        for p in (path, Path(str(path)+'.sha256')):
            if p.exists(): snapshot[p] = (sha(p), p.stat().st_mtime_ns)
    check('original_219_and_parent_pins_preserved', ordinary['original_source_count'] == 219)
    check('actual_ordinary_principal_certificate_available', ordinary['complete_ordinary_energy'] == 'INITIAL_FROZEN_PRINCIPAL_18_DIRECTION_ENERGY_CERTIFIED')
    check('complete_strong_density_row_and_local_lapse_identity_available', density['passed'] == density['total'] and lapse['passed'] == lapse['total'] and density['density_strength'] == 'L2')

    # Exact variable-coefficient formal adjoint identities, not a constant
    # coefficient oscillator assumption.
    kap, ap, apz, dd, ddz, lam, beta, ss, vp = sp.symbols('kap ap apz d dz lam beta s vp', real=True)
    HF = sp.diag(dd/kap, ap)
    AF = sp.Matrix([[0, kap*ap], [-dd, 0]])
    B1 = sp.Matrix([[-vp, -(2*kap*apz+kap*lam*ap)], [ddz-beta*dd*ss, -vp]])
    flux = HF*AF
    fluxz = sp.Matrix([[0, ddz*ap+dd*apz], [-ddz*ap-dd*apz, 0]])
    formal = 2*fluxz+HF*B1-B1.T*HF
    check('quartic_highest_energy_cancellation_exact', flux+flux.T == sp.zeros(2))
    check('quartic_first_derivative_formal_energy_cancellation_exact', formal.subs(ddz, dd*(lam-beta*ss)).applyfunc(sp.expand) == sp.zeros(2))
    bad = B1.copy()
    bad[0, 1] = -kap*lam*ap
    check('omitted_kinetic_coefficient_gradient_rejected', (2*fluxz+HF*bad-bad.T*HF).subs(ddz, dd*(lam-beta*ss)).applyfunc(sp.expand) != sp.zeros(2))
    bad = B1.copy()
    bad[1, 0] = ddz
    check('omitted_clock_lapse_regulator_gradient_rejected', (2*fluxz+HF*bad-bad.T*HF).subs(ddz, dd*(lam-beta*ss)).applyfunc(sp.expand) != sp.zeros(2))
    zz = sp.symbols('z')
    df, zf, sf = [sp.Function(n)(zz) for n in ('d', 'Z', 's')]
    current = sp.diff(df*sp.diff(zf, zz), zz)-2*beta*sp.diff(df*sf*zf, zz)+beta*df*sf*sp.diff(zf, zz)
    keep = df*sp.diff(zf, zz, 2)+(sp.diff(df, zz)-beta*df*sf)*sp.diff(zf, zz)-2*beta*sp.diff(df*sf, zz)*zf
    check('canonical_regulator_current_keeps_all_Zz_terms', sp.expand(current-keep) == 0)
    kk, aa, cc, Z, xi, pz, tqX, wz, tv = sp.symbols('k a c Z xi pz tqX wz tv', nonzero=True)
    hh = kap*ss*cc/aa**2
    chi = (Z-hh*pz)/(kap*kk**2)
    chidot = ap*xi-sp.I*kk*vp*chi-ap*tqX/kk+ss*wz/(sp.I*kk)
    Zdot = kap*kk**2*chidot-sp.I*kap*kk*ss*tv/aa**2
    wanted = kap*ap*kk**2*xi-sp.I*kk*vp*Z+kk*(-kap*ap*tqX-sp.I*kap*ss*wz-sp.I*kap*ss*tv/aa**2+sp.I*vp*hh*pz)
    check('full_secondary_Legendre_metric_shift_force_row_exact', sp.expand(Zdot-wanted) == 0)
    check('deleting_secondary_metric_part_changes_the_coupling', sp.simplify(sp.diff(wanted, tv)) != 0 and sp.simplify(sp.diff(wanted, pz)) != 0)
    # Independent finite block check of the exact all-order frozen formula.
    F = sp.Matrix([[0, sp.Rational(2, 3)], [-sp.Rational(5, 7), 0]])
    oo = sp.Matrix([[0, 1], [-2, 0]])
    of = sp.Matrix([[sp.I/7, 0], [sp.I/11, 0]])
    fo = sp.Matrix([[sp.Rational(1, 13), sp.Rational(1, 17)], [0, 0]])
    ff = sp.Matrix([[sp.I/19, sp.I/23], [sp.I/29, sp.I/19]])
    DD = sp.diag(sp.zeros(2), F)
    BB = oo.row_join(of).col_join(fo.row_join(ff))
    BD = sp.diag(oo, ff)
    SS = sp.zeros(2).row_join(-of*F.inv()).col_join((F.inv()*fo).row_join(sp.zeros(2)))
    TT = sp.eye(4)+SS/kk
    check('independent_mixed_cross_commutator_identity', (BB+SS*DD-DD*SS-BD).applyfunc(sp.expand) == sp.zeros(4))
    exact = TT*(kk*kk*DD+kk*BB)-(kk*kk*DD+kk*BD)*TT-(SS*BB-BD*SS)
    check('independent_exact_frozen_remainder_identity', exact.applyfunc(sp.expand) == sp.zeros(4))

    # Immutable interval setup: read blocks and profiles without a new
    # action evaluation or Hessian differentiation.
    old = load('mixed_principal_frozen_setup', SETUP)
    parents = {key: json.loads((ROOT/rel).read_text()) for key, rel in old.PARENTS.items()}
    principal = parents['principal']
    tree = ast.parse((ROOT/SETUP).read_text())
    fn = copy.deepcopy(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'calculate'))
    named = lambda n, key: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == key for t in n.targets)
    start = next(i for i, n in enumerate(fn.body) if named(n, 'z'))
    stop = next(i for i, n in enumerate(fn.body) if named(n, 'ii'))
    fn.name = 'initial_interval_blocks'
    fn.body = fn.body[start:stop]+[ast.Return(ast.Call(ast.Name('locals', ast.Load()), [], []))]
    scope = dict(mp=mp, iv=iv, parents=parents, principal=principal, ROOT=ROOT, FACTORY=old.FACTORY,
                 SLOTS=old.SLOTS, importlib=importlib, lo=lo, hi=hi, ab=ab, decode=decode, check=check)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), '<immutable-mixed-principal-blocks>', 'exec'), scope)
    ctx = scope['initial_interval_blocks']()
    mat, mul, add, scale, tr = [ctx[k] for k in ('mat', 'mul', 'add', 'scale', 'tr')]
    MI, BR, GR, c, y = [ctx[k] for k in ('MI', 'BR', 'GR', 'coefficient', 'y')]
    ii, zero = iv.mpc(0, 1), iv.mpf(0)
    for i in range(9):
        BR[i][5] = iv.mpf(1 if i in (0, 2) else 0)/(2*c)
        GR[i][5] = GR[5][i] = iv.mpf(0)
    MI = scale(add(MI, tr(MI)), iv.mpf(1)/2)
    GR = scale(add(GR, tr(GR)), iv.mpf(1)/2)
    par = load('mixed_principal_exact_parameters', PARAMETERS).parameters()
    rational = lambda q: iv.mpf(int(q.p))/int(q.q)
    b, beta0 = rational(par['b']), rational(par['beta'])
    a2 = y[0].c[0]
    a = iv.sqrt(a2)
    kappa = 1/a2
    lambda_z = y[0].c[1]/(2*a2)
    s = y[40].c[0]
    N = iv.exp(-beta0*y[12].c[0])
    mu = a*a*a
    d = b*N*mu*kappa
    dz = d*(lambda_z-beta0*s)
    whole = {tuple(row['ij']): (decode(row['value']), decode(row['dz'])) for row in parents['mixed']['full_mixed_Hessian_upper_triangle']}
    h = lambda i, j: whole.get((min(i, j), max(i, j)), (zero, zero))[0]
    hz = lambda i, j: whole.get((min(i, j), max(i, j)), (zero, zero))[1]
    m = h(26, 26)
    m_z = hz(26, 26)
    check('whole_root_force_temporal_mass_positive', lo(m) > 0)
    aphi = 1/m
    aphi_z = -m_z/(m*m)
    vphi = (h(26, 40)+ctx['shift']*m)/m
    t_q = [[h(26, slot) for slot in old.SLOTS]]
    contains = lambda x: lo(x) <= 0 <= hi(x)
    check('force_velocity_has_no_ordinary_or_shift_gradient_cross', all(h(26, 14+slot) == 0 for slot in old.SLOTS) and all(h(26, i) == 0 for i in (45, 46, 47)))
    check('force_clock_shift_Legendre_coefficient_consistent', contains(h(26, 44)+m*s))
    check('ordinary_auxiliary_flux_columns_are_exact_zero', all(h(28+slot, 13) == 0 and h(28+slot, 41) == 0 for slot in old.SLOTS))
    aq = [(-d*s/(2*a2) if slot in (0, 3) else zero) for slot in old.SLOTS]
    check('retained_metric_auxiliary_gradient_identity_consistent', all(contains(h(slot, 41)-x) for slot, x in zip(old.SLOTS, aq)))
    check('nonmetric_auxiliary_gradient_columns_exact_zero', all(h(slot, 41) == 0 for slot in old.SLOTS if slot not in (0, 3)))
    check('auxiliary_force_gradient_and_mass_consistent', contains(h(13, 13)-b*N*mu) and contains(h(40, 41)+d))
    # Actual ordinary 18-direction material generator, with the proved Ward
    # identity imposed algebraically. Both zero coordinates remain present.
    E = sp.zeros(9, 8)
    E[0, 0], E[2, 0], E[1, 1] = 1, -1, 1
    for j in range(2, 8): E[j+1, j] = 1
    R = mat(8, 9)
    R[0][0], R[0][2], R[1][1] = iv.mpf(1)/2, -iv.mpf(1)/2, iv.mpf(1)
    for j in range(2, 8): R[j][j+1] = iv.mpf(1)
    XX, PP = mat(9, 18), mat(9, 18)
    for i in range(9):
        for j in range(8): XX[i][1+j] = iv.mpf(int(E[i, j]))
        PP[i][9+i] = iv.mpf(1)
    XX[0][14] = XX[2][14] = ii*c
    velocity = mul(MI, add(PP, scale(mul(BR, XX), ii), -1))
    p_rate = add(scale(mul(tr(BR), velocity), -ii), mul(GR, XX))
    ordinary_A1 = [mat(1, 18)[0]]+mul(R, velocity)+p_rate
    # Convert the FULL shift Schur response to material velocities. Keeping
    # Dshift+S*Cshift avoids silently dropping common-advection terms.
    raw_C, raw_D, KI = [ctx[k] for k in ('C', 'D', 'KI')]
    Drelative = add(raw_D, scale(raw_C, ctx['shift']))
    shift_gradient = scale(mul(KI, add(mul(tr(raw_C), velocity), scale(mul(tr(Drelative), XX), ii))), -1)
    t_velocity = [[(velocity[0][j]+velocity[2][j])/2 for j in range(18)]]
    legendre_q = mul(t_q, XX)
    hmetric = kappa*s*c/a2
    fo_row = [-kappa*aphi*legendre_q[0][j]-ii*kappa*s*shift_gradient[2][j]-ii*kappa*s*t_velocity[0][j]/a2
              +(ii*vphi*hmetric if j == 14 else 0) for j in range(18)]
    OF, FO = mat(18, 2), [fo_row, mat(1, 18)[0]]
    for i, val in enumerate(aq): OF[9+i][0] = ii*val
    a2fast = [[zero, kappa*aphi], [-d, zero]]
    a2inv = [[zero, -1/d], [1/(kappa*aphi), zero]]
    fast_A1 = [[-ii*vphi, -ii*(2*kappa*aphi_z+kappa*lambda_z*aphi)], [ii*(dz-beta0*d*s), -ii*vphi]]
    A2, A1, BD = mat(20, 20), mat(20, 20), mat(20, 20)
    for i in range(18):
        for j in range(18): A1[i][j] = BD[i][j] = ordinary_A1[i][j]
        for j in range(2): A1[i][18+j] = OF[i][j]
    for i in range(2):
        for j in range(18): A1[18+i][j] = FO[i][j]
        for j in range(2):
            A2[18+i][18+j] = a2fast[i][j]
            A1[18+i][18+j] = BD[18+i][18+j] = fast_A1[i][j]
    S = mat(20, 20)
    sof = scale(mul(OF, a2inv), -1)
    sfo = mul(a2inv, FO)
    for i in range(18):
        for j in range(2): S[i][18+j] = sof[i][j]
    for i in range(2):
        for j in range(18): S[18+i][j] = sfo[i][j]
    def ci(x): return hi(iv.sqrt(iv.mpf(ab(x.real))**2+iv.mpf(ab(x.imag))**2))
    def cinf(x): return max(hi(sum((iv.mpf(ci(t)) for t in row), zero)) for row in x)
    def norm2(x):
        f = iv.sqrt(sum((iv.mpf(ci(t))**2 for row in x for t in row), zero))
        p = iv.sqrt(iv.mpf(cinf(x))*iv.mpf(cinf(tr(x))))
        return min(hi(f), hi(p))
    sbound = norm2(S)
    threshold = max(1, int(mp.ceil(2*sbound)))
    denominator = 1-iv.mpf(sbound)/threshold
    check('actual_normal_form_has_finite_same_strength_threshold', mp.isfinite(sbound) and lo(denominator) >= mp.mpf('.5'), dict(S_norm=mp.nstr(sbound, 30), signed_abs_k_at_least=threshold))
    remainder_numerator = add(mul(S, A1), mul(BD, S), -1)
    frozen_remainder = iv.mpf(norm2(remainder_numerator))/denominator
    hf1, hf2 = d/kappa, aphi
    fast_lower = iv.mpf(min(lo(hf1), lo(hf2)))
    fast_upper = iv.mpf(max(hi(hf1), hi(hf2)))
    parent_low = decode(ordinary['ordinary_norm_constants']['energy_lower_binary'])
    parent_high = decode(ordinary['ordinary_norm_constants']['energy_upper_binary'])
    base_lower = iv.mpf(min(lo(parent_low), lo(fast_lower)))
    base_upper = iv.mpf(max(hi(parent_high), hi(fast_upper)))
    energy_lower = base_lower*denominator**2
    energy_upper = base_upper*(1+iv.mpf(sbound)/threshold)**2
    frequency = kappa*aphi*d
    check('actual_force_pair_weights_and_quartic_coefficient_positive', lo(fast_lower) > 0 and lo(frequency) > 0)
    check('all_20_principal_directions_kept_with_positive_symbol_norm', len(S) == 20 and lo(energy_lower) > 0 and mp.isfinite(hi(energy_upper)))
    check('frozen_normal_form_remainder_finite_not_full_PDE_remainder', mp.isfinite(hi(frozen_remainder)))
    check('both_actual_cross_blocks_retained', norm2(OF) > 0 and norm2(FO) > 0)
    # Profile-only independent nonzero metric coupling control: no Hessian.
    point = ctx['env']['state'](ctx['env']['J'].variable(iv.mpf('0.3')), False)
    check('omitted_metric_auxiliary_gradient_is_not_identically_zero', ab(point[40].c[0]) > mp.mpf('1e-8'))
    check('all_original_sources_sidecars_and_timestamps_unchanged', all(sha(p) == h0 and p.stat().st_mtime_ns == t for p, (h0, t) in snapshot.items()))
    cbinary = lambda x: {'real': binary(x.real), 'imag': binary(x.imag)}
    encode = lambda x: [[cbinary(t) for t in row] for row in x]
    vals = dict(force_temporal_mass=m, force_temporal_mass_z=m_z, force_inverse_mass=aphi, force_inverse_mass_z=aphi_z,
                force_advection=vphi, d=d, d_z=dz, kappa=kappa, lambda_z=lambda_z, psi_z=s,
                fast_weight_Z=hf1, fast_weight_xi=hf2, quartic_frequency_squared=frequency,
                S_norm_bound=iv.mpf(sbound), frozen_remainder_bound=frozen_remainder,
                transformed_energy_lower=energy_lower, transformed_energy_upper=energy_upper,
                ordinary_to_force_norm=iv.mpf(norm2(FO)), force_to_ordinary_norm=iv.mpf(norm2(OF)))
    return dict(kind='RTAU_MIXED_PRINCIPAL_ASSEMBLY_V1', passed=sum(x['passed'] for x in checks), total=len(checks), checks=checks,
                source_sha256=pins, original_source_count=219, values_binary={k:binary(v) for k,v in vals.items()},
                displays={k:[mp.nstr(lo(v), 30), mp.nstr(hi(v), 30)] for k,v in vals.items()},
                signed_absolute_k_threshold=threshold, threshold_meaning='MATHEMATICAL_FROZEN_SYMBOL_NORMAL_FORM_ONLY_NOT_PHYSICAL_CUTOFF',
                highest_quartic_matrix_binary=encode(A2), first_mixed_matrix_binary=encode(A1), cross_normal_form_matrix_binary=encode(S),
                ordinary_to_force_binary=encode(FO), force_to_ordinary_binary=encode(OF),
                scope='INITIAL_20_DIRECTION_MIXED_SYMBOL_AND_FAST_FORMAL_PRINCIPAL_ENERGY_ONLY',
                variable_coefficient_composition_remainder='NOT_BOUNDED', full_prepared_coupled_energy='NOT_DERIVED',
                moving_constraint_Green_gauge_and_global_partners='NOT_DERIVED', actual_time_tube='NOT_ESTABLISHED', physical_window=False,
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
    else: assert args.verify.read_bytes() == raw, 'Immutable replay differs'
    names = ('quartic_frequency_squared', 'S_norm_bound', 'frozen_remainder_bound', 'transformed_energy_lower', 'transformed_energy_upper')
    print(json.dumps(dict(passed=data['passed'], total=data['total'], failed=[x for x in data['checks'] if not x['passed']],
                          bounds={k:data['displays'][k] for k in names}, signed_absolute_k_threshold=data['signed_absolute_k_threshold'],
                          full_prepared_coupled_energy=data['full_prepared_coupled_energy']), indent=2))
    return 0 if data['passed'] == data['total'] else 1


if __name__ == '__main__': raise SystemExit(main())
