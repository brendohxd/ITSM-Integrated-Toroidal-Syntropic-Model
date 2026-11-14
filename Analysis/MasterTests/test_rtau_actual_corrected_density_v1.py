"""Actual INITIAL corrected-density L2 row with corrected compatible lift.

Reuses only the reproduced UNREDUCED source inequality, not old lifted bounds.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
MANIFEST = 'Theory/Gates/RES-001/RES001_RTAU_ACTUAL_CORRECTED_DENSITY_V1_PREPARATION_INPUTS_2026-11-05.json'
SPEC = 'Theory/Gates/RES-001/RES001_RTAU_ACTUAL_CORRECTED_DENSITY_V1_EXECUTION_SPEC_2026-11-05.md'
RAW = 'Analysis/MasterTests/test_rtau_strong_density_l2_source_v1.py'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    decode = lambda v: iv.mpf([mp.mpf(tuple(x)) for x in v])
    encode = lambda v: [list(x) for x in iv.mpf(v)._mpi_]
    upper = lambda v: mp.mpf(iv.mpf(v)._mpi_[1])
    sources = dict(raw=BASE+'rtau_strong_density_l2_source_v1_20261104/receipt.json',
                   momentum=BASE+'rtau_momentum_rate_lift_v2_20261104/receipt.json',
                   force=BASE+'rtau_strong_force_coordinate_v3_20261104/receipt.json')
    data = {k: json.loads((ROOT/v).read_text()) for k, v in sources.items()}
    pins = dict(json.loads((ROOT/MANIFEST).read_text())['source_sha256'])
    for item in data.values():
        for rel, h in item['source_sha256'].items():
            assert rel not in pins or pins[rel] == h, rel
            pins[rel] = h
    for rel in [MANIFEST, SPEC, RAW, *sources.values(), Path(__file__).relative_to(ROOT).as_posix()]:
        actual = sha(ROOT/rel)
        assert rel not in pins or pins[rel] == actual, rel
        pins[rel] = actual
    snapshot = {}
    for rel, h in pins.items():
        p = ROOT/rel
        assert sha(p) == h, rel
        for q in [p, Path(str(p)+'.sha256')]:
            if q.exists():
                snapshot[q] = sha(q), q.stat().st_mtime_ns
    checks = []

    def check(name, ok):
        checks.append(dict(name=name, passed=bool(ok)))

    # Reexecute the exact source assembly. Do not rerun the parent Hessian.
    spec = importlib.util.spec_from_file_location('density_unreduced_source_reproduction', ROOT/RAW)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fresh = mod.calculate()
    check('raw_source_twenty_controls_reproduced', fresh['passed'] == fresh['total'] == 20)
    check('raw_density_rows_reproduce_original_bytes_as_data', fresh['rows_binary'] == data['raw']['rows_binary'])
    check('raw_norm_order_not_old_lifted_norm', fresh['output_order'] == [
        'corrected_density_L2_in_named_coordinates', 'Q_H1_original', 'P_L2_original',
        'force_H2_original', 'harmonic_coordinate_velocity_adapted'])
    check('corrected_Sigma_lifts_only', all(data[k]['density_coordinate'] ==
          'Sigma=rho+e_force+b*Z**2/2' for k in ['momentum', 'force']))
    check('new_lift_parent_checks_complete', all(data[k]['passed'] == data[k]['total']
          and all(c['passed'] for c in data[k]['checks']) for k in ['momentum', 'force']))
    Q = list(map(decode, data['momentum']['constants_binary']['full_configuration_H1']))
    P = list(map(decode, data['momentum']['constants_binary']['full_momentum_L2']))
    F = list(map(decode, data['force']['constants_binary']['force_H2_inverse']))
    assert len(Q) == len(P) == len(F) == 8
    raw = list(map(decode, fresh['rows_binary']['original_L2_norm_rate']))
    row = [raw[1]*Q[j]+raw[2]*P[j]+raw[3]*F[j] for j in range(8)]
    row[0] += raw[0]
    row += [raw[4]]
    check('all_global_and_harmonic_inputs_retained', len(row) == 9 and upper(row[-1]) > 0)
    check('strong_density_and_force_bounds_finite', all(mp.isfinite(upper(v)) and upper(v) > 0 for v in row))

    # Exact time differentiation, retaining arbitrary nonzero primitive means.
    # Sympy symbols for the fully generic transformed row algebra.
    names = 'w_t w_x C c c_t c_x alpha alpha_t alpha_x S S_x xi Pxi meanxi meanSxi G'
    wt, wx, C, c, ct, cx, A, At, Ax, S, Sz, xi, Pxi, Hxi, Jmean, G = s.symbols(names)
    chi_x, N, Nz, dp, dp_x, Gx, sigmat, sigma_x = s.symbols('chi_x N N_x dp dp_x G_x sigma_t sigma_x')
    # Full primitive row from the owner: Q contains all current/mean terms.
    Q0 = s.Symbol('Q0')
    sig = s.Symbol('sigma')
    # u=sigma-cPxi; its exact owner row is C*u+alpha*N*dp_x+Q0.
    u = s.Symbol('u')
    u_material = C*u+A*N*dp_x+Q0
    grad_material = N*dp_x+Nz*dp+Sz*chi_x+Gx
    direct = u_material-(At-S*Ax)*chi_x-A*grad_material
    expected = C*(u-A*chi_x)+(C*A-At+S*Ax-A*Sz)*chi_x+Q0-A*Nz*dp-A*Gx
    check('exact_second_normal_form_with_all_coefficient_drift', s.expand(direct-expected) == 0)
    check('omitted_time_drift_rejected', s.expand(direct-expected+At*chi_x) != 0)
    check('omitted_vector_transport_rejected', s.expand(direct-expected+A*Sz*chi_x) != 0)
    # The momentum primitive is not a scalar under density transport.
    z = s.Symbol('z', real=True)
    momentum = 1+s.cos(z)/3
    velocity = s.cos(z)/5
    mean = lambda f: s.integrate(s.expand_trig(f), (z, 0, 2*s.pi))/(2*s.pi)
    def primitive(f):
        v = s.integrate(s.expand_trig(f-mean(f)), z)
        return s.simplify(v-mean(v))
    comm = primitive(s.diff(velocity*momentum, z))-velocity*(momentum-mean(momentum))
    target = velocity*mean(momentum)-mean(velocity*momentum)
    check('nonzero_torus_primitive_gauge_commutator', s.trigsimp(comm-target) == 0 and target != 0)
    # Physical density reconstruction from the FULL Legendre differential.
    p, mu, fp, fps, fs, dmu, fq_dq, bZ, zeta = s.symbols('p mu fp fps fs delta_mu f_q_delta_q bZ zeta')
    delta_e = p*xi/mu-p*fp*dmu/mu-fq_dq-fs*chi_x
    deltaSigma = sig+c*Pxi-(p*fps+fs)*chi_x  # sig here denotes w
    physical = s.expand(deltaSigma-delta_e-bZ*zeta)
    target_phys = sig+c*Pxi-p*fps*chi_x-p*xi/mu+p*fp*dmu/mu+fq_dq-bZ*zeta
    check('physical_rho_reconstruction_keeps_force_and_measure', s.simplify(physical-target_phys) == 0)
    check('rho_is_not_Sigma_rejection', s.simplify(physical-deltaSigma) != 0)
    # Norm composition independently checked on rational scalar fixtures.
    U = list(map(s.Rational, range(1, 9)))
    coeff = list(map(s.Rational, [2, 3, 5, 7, 11]))
    qv, pv, fv = [s.Matrix(range(i, i+8)) for i in [1, 2, 3]]
    manual = coeff[0]*U[0]+coeff[1]*qv.dot(s.Matrix(U))+coeff[2]*pv.dot(s.Matrix(U))+coeff[3]*fv.dot(s.Matrix(U))+coeff[4]*13
    combined = sum((coeff[1]*qv[j]+coeff[2]*pv[j]+coeff[3]*fv[j])*U[j] for j in range(8))+coeff[0]*U[0]+coeff[4]*13
    check('independent_exact_norm_composition_fixture', manual == combined)
    check('source_sidecars_and_timestamps_unchanged', all(sha(p) == h and p.stat().st_mtime_ns == tm for p, (h, tm) in snapshot.items()))
    return dict(kind='RTAU_ACTUAL_CORRECTED_DENSITY_V1', source_sha256=pins,
                checks=checks, passed=sum(c['passed'] for c in checks), total=len(checks),
                input_order=data['force']['inverse_input_order']+['harmonic_coordinate_velocity_adapted'],
                bounds_binary={'initial_original_coordinate_density_L2_norm_rate': list(map(encode, row))},
                upper_display={'initial_original_coordinate_density_L2_norm_rate': [mp.nstr(upper(x), 30) for x in row]},
                raw_inequality_used='original_L2_norm_rate in unreduced Q_H1,P_L2,force_H2 norms; NOT old lifted estimates',
                physical_rho_identity=str(target_phys),
                scope='INITIAL_COMPATIBLE_CORRECTED_DENSITY_L2_NORM_RATE_WITH_PHYSICAL_RHO_RECONSTRUCTION_ONLY',
                full_principal_row_comparison='NOT_YET_ASSEMBLED',
                physical_rho_numeric_reconstruction_constants='NOT_YET_EXPORTED',
                moving_maps='NOT_ASSEMBLED', time_tube='NOT_ESTABLISHED', full_prepared_energy='NOT_DERIVED',
                task_status='PARTIAL_INITIAL_RATE_BOUND_ONLY', Rtau_adopted=False,
                review='DEFERRED', physics_pass=False, gate_effect='NONE', G1_G6='INCOMPLETE')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    args = parser.parse_args()
    if args.output:
        assert not args.output.parent.exists()
    data = calculate()
    raw = (json.dumps(data, sort_keys=True, indent=2)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True)
        args.output.write_bytes(raw)
        Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
    else:
        assert args.verify.read_bytes() == raw, 'Replay differs'
    print(json.dumps({k: data[k] for k in ['passed', 'total', 'task_status', 'physics_pass']}))
    assert data['passed'] == data['total'], [c for c in data['checks'] if not c['passed']]


if __name__ == '__main__':
    main()
