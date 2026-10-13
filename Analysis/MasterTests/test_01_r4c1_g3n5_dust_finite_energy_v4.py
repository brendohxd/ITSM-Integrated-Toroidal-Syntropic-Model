"""Full-state finite bounds; explicit zero R6 and genuine omission controls."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_ENERGY_V4_CONTRACT_2026-10-12.md'
ENGINE = 'Analysis/MasterTests/test_01_r4c1_g3n5_dust_actual_order_v3.py'
if hashlib.sha256((ROOT / ENGINE).read_bytes()).hexdigest() != '7d7da3e67e5a24736baea8956c6ca717a3d52ebcb50b521d50543c8a50cad5ab':
    raise RuntimeError('Frozen V3 source drift')
sys.path.insert(0, str(ROOT / 'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_actual_order_v3 as library
old, prior, common, engine = library.old, library.prior, library.common, library.engine
PROGRESS = None


def progress(message):
    print(message, flush=True)
    if PROGRESS is not None:
        PROGRESS.write(message + '\n')
        PROGRESS.flush()


def calculate():
    parent = BASE + 'r4c1_g3n5_dust_actual_order_attempt_03/'
    ps = common.read_json(parent + 'summary.json')
    expected = '7f0888a9096145c42257bcccf84b8e7fdc3d98a1f10e05bbfd4f68a00dcf5c60'
    if common.sha((ROOT / (parent + 'summary.json')).read_bytes()) != expected:
        raise RuntimeError('Frozen V3 receipt drift')
    pins = dict(ps['source_sha256'])
    pins.update({parent + name: digest for name, digest in ps['artifacts'].items()})
    pins[parent + 'summary.json'] = expected
    reference_parent = BASE + 'r4c1_g3n5_dust_normalized_reference_attempt_02/'
    reference_digest = '5db4548cd8d74201310c4e046873b660e5cee33c70c7a7aa12b8f38dd219b47a'
    if common.sha((ROOT / (reference_parent + 'summary.json')).read_bytes()) != reference_digest:
        raise RuntimeError('Frozen normalized-reference receipt drift')
    reference_summary = common.read_json(reference_parent + 'summary.json')
    reference_formulas = common.read_json(reference_parent + 'formulas.json')
    pins.update(reference_summary['source_sha256'])
    pins.update({reference_parent + name: digest for name, digest in reference_summary['artifacts'].items()})
    pins[reference_parent + 'summary.json'] = reference_digest
    failed_parent = BASE + 'r4c1_g3n5_dust_finite_energy_attempt_03/'
    failed_digest = 'b043478a67b9337ed5c09c9d3167de30192b78de04bf86b137e0f5395b0cf5da'
    if common.sha((ROOT/(failed_parent+'summary.json')).read_bytes()) != failed_digest:
        raise RuntimeError('Preserved V3 FAIL receipt drift')
    failed_summary = common.read_json(failed_parent+'summary.json')
    pins.update(failed_summary['source_sha256'])
    pins.update({failed_parent+name:value for name,value in failed_summary['artifacts'].items()})
    pins[failed_parent+'summary.json'] = failed_digest
    for rel in (SELF, CONTRACT, ENGINE,
                'Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_energy_v1.py',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_ENERGY_CONTRACT_2026-10-12.md',
                BASE + 'r4c1_g3n5_dust_finite_energy_attempt_01/interruption.json',
                'Analysis/MasterTests/test_01_r4c1_g3n5_dust_finite_energy_v2.py',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_ENERGY_V2_CONTRACT_2026-10-12.md',
                BASE + 'r4c1_g3n5_dust_finite_energy_attempt_02/interruption.json',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_BOUND_BALANCE_REPORT_2026-10-12.md'):
        pins[rel] = common.sha((ROOT / rel).read_bytes())
    absent = common.inspect_pins(pins)
    paths = [ROOT / name for name in pins]
    paths.extend(Path(str(path) + '.sha256') for path in list(paths) if Path(str(path) + '.sha256').exists())
    before = old.parent.snapshot(paths)
    checks = common.Checks()
    progress('V4 inputs pinned; full-state zero-aware source calculation started')
    checks.add('failed_v3_retained_not_relabelled',
               failed_summary['passed']==71 and failed_summary['total']==72
               and [row['name'] for row in failed_summary['checks'] if not row['passed']]==['highest_source_omission_rejected']
               and not failed_summary['finite_mode_error_bounds_proved'])
    checks.add('independent_reference_component_verified_not_full_error',
               reference_summary['passed'] == reference_summary['total'] == 46
               and reference_summary['normalized_reference_bound_proved']
               and not reference_summary['full_finite_mode_bound_proved']
               and not reference_summary['physics_pass'])
    bg = old.Background()
    a, H, u, ud, v, vd, r, rd, pd, rho, C = bg.bg
    ell = bg.ell
    eps = s.Symbol('eps', positive=True)
    sy = {**bg.sy, 'eps': eps}
    on = lambda mat: mat.applyfunc(s.cancel)
    shell = lambda mat: mat.applyfunc(lambda val: bg.constraint_reduce_scalar(val) if val != 0 else s.Integer(0))
    exact = lambda name, mat: old.parent.exact(checks, name, on(mat))
    checks.add('parent_scoped_order_proved_not_physical_closure',
               ps['passed'] == ps['total'] == 72 and ps['mathematical_asymptotic_order'] == 2
               and not ps['physics_pass'] and not ps['full_dust_milestone_complete'])
    un = common.read_json(BASE + 'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    maps = {name: old.parent.import_matrix(obj, bg.sy) for name, obj in common.read_json(un['general_exact_maps_source'])['matrices'].items()}
    Tw, Twi, U, Q, cm = [maps[name] for name in ('wave_map_Tw', 'wave_inverse_Twi', 'fast_cross_map_U', 'positive_evolution_Q', 'longitudinal_velocity_scaling_C')]
    checks.add('all_full_generator_terms_retained',
               sorted(int(name.removeprefix('residual_numerator_')) for name in maps if name.startswith('residual_numerator_')) == list(range(6)))
    checks.add('inherited_full_energy_domain', s.Rational(un['mu_exact']) < 60)
    D = s.diag(*[s.Rational(value) for value in un['lower_metric_diagonal']])
    rank = s.zeros(20)
    rank[6:8, 6:8] = s.Matrix([v, -u]) * s.Matrix([[v, -u]]) / 13
    exact('Q_positive_lower_identity', Q - D - rank)
    checks.add('positive_lower_metric', all(value > 0 for value in D.diagonal()))
    F, L = maps['dispersive_principal_F'], maps['ordinary_wave_principal_L']
    exact('full_fast_principal_Q_skew', Q * F + F.conjugate().T * Q)
    exact('full_wave_principal_Q_skew', Q * L + L.conjugate().T * Q)
    raw = common.read_json(old.PARENT + 'matrices.json')
    Az, bi, obs, M, fields = [old.parent.import_matrix(raw[name], bg.sy) for name in ('balanced_generator', 'balancing_map_inverse', 'actual_dust_observable', 'leading_dust_generator', 'full_field_reconstruction')]
    Ci = s.eye(20)
    Ci[13, 13] = a / ell
    Ac = (bg.dt(cm) + cm * Az) * Ci
    Oc = obs * bi * Ci
    apolys = [s.Poly(value.subs(ell, 1/eps) * eps**2, eps) for value in Ac]
    adegree = max((int(poly.degree()) for poly in apolys if not poly.is_zero), default=0)
    blocks = {2-power:s.Matrix(20,20,lambda i,j:apolys[i*20+j].nth(power)) for power in range(adegree+1)}
    exact('complete_Laurent_generator', Ac - sum((mat * ell**power for power, mat in blocks.items()), s.zeros(20)))
    progress('Complete action-exported generator coefficients extracted and reconstructed')
    prep = common.read_json(BASE + 'r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json')
    sharper = common.read_json(BASE + 'r4c1_g3n5_prepared_dust_sharper_attempt_01/formulas.json')
    corrected = common.read_json(BASE + 'r4c1_g3n5_corrected_dust_remainder_attempt_04/formulas.json')
    hs = {j: old.parent.import_matrix(prep['matrices']['comparison_lift_H' + str(j)], bg.sy) for j in range(4)}
    rs = {j: old.parent.import_matrix(sharper['matrices']['exact_source_R' + str(j)], bg.sy) for j in range(2, 6)}
    q3, h4, N2 = [old.parent.import_matrix(corrected['matrices'][name], bg.sy) for name in ('wave_addition_q3', 'fast_addition_H4', 'lift_generator_N2')]
    hc = {**hs, 3: hs[3] + q3, 4: h4}
    exact('complete_order_two_cancellation', shell(rs[2] - hs[0] * N2 + blocks[1] * q3 + blocks[2] * h4))
    exact('wave_correction_preserves_lower_order', blocks[2] * q3)
    checks.add('no_unregistered_generator_power', set(blocks) <= {-2,-1,0,1,2})
    if not set(blocks) <= {-2,-1,0,1,2}:
        raise ValueError('Reject unknown generator powers; do not truncate')
    # Independent noncommuting polynomial derivation of EVERY coefficient
    # update. This proves the product rule without requiring a global GCD of
    # the large actual background rational expressions.
    generic = lambda label:s.Matrix(2,2,lambda i,j:s.Symbol(f'{label}_{i}_{j}'))
    ga = {power:generic('A'+str(power)) for power in (-2,-1,0,1,2)}
    gh = {power:generic('H'+str(power)) for power in range(4)}
    gq = {3:generic('q3'),4:generic('q4')}
    gqd = {3:generic('q3dot'),4:generic('q4dot')}
    gm,gn = generic('M'),generic('N2')
    gp = sum((mat*eps**(-power) for power,mat in ga.items()),s.zeros(2))
    ghold = sum((mat*eps**power for power,mat in gh.items()),s.zeros(2))
    gadd = sum((mat*eps**power for power,mat in gq.items()),s.zeros(2))
    gdadd = sum((mat*eps**power for power,mat in gqd.items()),s.zeros(2))
    gdelta = gp*gadd-gdadd-gadd*gm-(ghold+gadd)*gn*eps**2
    for power in range(2,7):
        expected_update = sum((mat*gq[d+power] for d,mat in ga.items() if d+power in gq),s.zeros(2))
        if power in gq:expected_update -= gqd[power]+gq[power]*gm
        expected_update -= (gh.get(power-2,s.zeros(2))+gq.get(power-2,s.zeros(2)))*gn
        extracted = gdelta.applyfunc(lambda value:s.Poly(value,eps).nth(power))
        exact('generic_complete_source_coefficient_'+str(power),extracted-expected_update)
    adds = {3: q3, 4: h4}
    rc = {}
    for power in range(3, 7):
        value = rs.get(power, s.zeros(20, 2)) + sum((mat * adds[d + power] for d, mat in blocks.items() if d + power in adds), s.zeros(20, 2))
        if power in adds:
            value -= bg.dt(adds[power]) + adds[power] * M
        if power - 2 in hc:
            value -= hc[power - 2] * N2
        rc[power] = value
        progress('Complete corrected source R' + str(power) + ' retained factored')
    Hc = sum((mat / ell**power for power, mat in hc.items()), s.zeros(20, 2))
    Rc = sum((mat / ell**power for power, mat in rc.items()), s.zeros(20, 2))
    Mc = M + N2 / ell**2
    J = Oc * Hc
    g = -s.Rational(22, 375) * a*a
    den = 1 - g / ell**2
    Cw = Tw * (s.eye(20) - U / (ell * den) + U*U / (ell**2 * den))
    Cwi = (s.eye(20) + U / ell) * Twi
    exact('full_wave_coordinate_inverse', Cw * Cwi - s.eye(20))
    Ow = Oc * Cwi
    checks.add('drift_omission_rejected', any(val != 0 for val in bg.dt(Hc)) and bg.dt(cm)[13, 13] != 0)
    exact('complete_R6_explicitly_zero', rc[6])
    nonzero_sources = [power for power,mat in rc.items() if any(val != 0 for val in mat)]
    checks.add('genuine_nonzero_source_coefficients_retained', nonzero_sources == [3,4,5])
    toy_t = s.Symbol('t', real=True)
    checks.add('negative_forcing_sign_rejected', s.diff(s.exp(toy_t)-1,toy_t) != (s.exp(toy_t)-1)-1)
    boxes = {bg.sy[name]: tuple(s.Rational(val) for val in bounds) for name, bounds in un['background_boxes'].items()}
    box = engine.EnclosureBox(boxes)
    constbox = engine.EnclosureBox({})
    checks.add('Q_upper_metric_on_frozen_box', box.absolute(u*u+v*v) <= s.Rational(13,8))
    norm = lambda mat: max(box.norm(mat), box.norm(mat.T))
    source_norms = {power:norm(mat) for power,mat in rc.items()}
    progress('Whole-background majorants for ALL factored source coefficients derived')
    checks.add('leading_generator_norm', norm(M) <= s.Rational(21, 10))
    nn = norm(on(N2))
    init = {a:1, H:s.sqrt(s.Rational(3469,4620)), u:1, ud:0, v:0, vd:1,
            r:1, rd:s.Rational(1,4), pd:s.Rational(1,5), rho:s.Rational(1,5), C:1}
    d1 = old.parent.import_matrix(prep['matrices']['initial_fast_mismatch'], sy)
    d2 = old.parent.import_matrix(prep['matrices']['initial_remainder'], sy)
    Eorig = sum((mat.subs(init) / ell**power for power, mat in hs.items()), s.zeros(20,2)) + d1.subs(init)/ell + d2.subs(init).subs(eps,1/ell)/ell**2
    exact('original_prepared_observable_normalization', Oc.subs(init)*Eorig-s.eye(2))
    Q0 = Q.subs(init)
    coeff = common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc = np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    ar = common.read_json(old.PARENT+'trajectories.json')
    times = np.asarray(ar['time'], float)
    Phi = np.asarray(ar['leading_Phi'], complex)
    mu, T = s.Rational(21,10), s.Rational(1,20)
    rows, controls = [], []
    # Controls use the ORIGINAL exported Ac and its actual drift, independently
    # of reconstructed source coefficients. No full trajectory is projected.
    numeric_mp = s.lambdify([bg.bg,ell], (Ac,Hc,bg.dt(Hc),Mc,Rc,rc[3],rc[4],rc[5]), 'mpmath', cse=True)
    energy_mp = s.lambdify([bg.bg], bg.energy, 'mpmath', cse=True)
    numeric_archive = s.lambdify([bg.bg,ell], (fields*bi,Oc*cm,Ow,Q), 'numpy', cse=True)
    sqrt_upper = lambda value: constbox.evaluate(s.sqrt(value))[1]
    for item in ar['modes']:
        kval = item['ell']
        subs = {ell:s.Integer(kval)}
        j0 = on(J.subs(init).subs(subs))
        checks.add('initial_normalization_invertible_' + str(kval), j0.det() != 0)
        if j0.det() == 0:
            raise RuntimeError('Singular initial normalization')
        ji = on(j0.inv())
        ji_bound = constbox.norm(ji)
        ji_delta = constbox.norm(ji-s.eye(2))
        reference_row = next(row for row in reference_formulas['modes'] if row['ell'] == kval)
        reference_inverse = s.Rational(reference_row['K_J0_inverse'])
        reference_source = s.Rational(reference_row['K_source'])
        reference_rate = s.Rational(reference_row['reference_rate'])
        checks.add('same_initial_normalization_bound_'+str(kval), ji_bound == reference_inverse)
        initial = on(Cw.subs(init).subs(subs)*(Eorig.subs(subs)-Hc.subs(init).subs(subs)*ji))
        energies = [s.simplify((initial[:,col].conjugate().T*Q0*initial[:,col])[0]) for col in range(2)]
        upper_energies = [max(s.Integer(0), constbox.evaluate(value)[1]) for value in energies]
        k_initial = sum(sqrt_upper(value) for value in upper_energies)
        checks.add('retained_initial_mismatch_not_discarded_' + str(kval), k_initial > 0)
        ow = Ow.subs(subs)
        observation_squares = [sum(box.absolute(ow[i,j])**2/D[j,j] for j in range(20)) for i in range(2)]
        k_observation = sqrt_upper(max(observation_squares))
        # FULL forcing is bounded by a rigorous product majorant, not by
        # dropping terms or normalizing a huge coupled background fraction.
        coordinate_bound = norm(Cw.subs(subs))
        residual_bound = sum(value/s.Integer(kval)**power for power,value in source_norms.items())
        k_source = s.Rational(3,2)*coordinate_bound*residual_bound
        rate = mu + nn / kval**2
        def bounds(t):
            ret = k_observation * k_initial * s.exp(30*t)
            forced = k_observation * k_source * ji_bound * t * s.exp(max(30,rate)*t)
            reference = reference_source * reference_inverse * t * s.exp(reference_rate*t)
            return ret, forced, reference, ret+forced+reference
        # Strictly mathematical full-state/normalization bounds, not a chosen
        # scientific tolerance. Leave their actual sizes visible.
        err = violation = fields_error = observable_error = 0.
        for ix,t in enumerate(times):
            point = np.polynomial.polynomial.polyval(t,bc.T)
            ff,oo,*_ = [np.asarray(mat,complex) for mat in numeric_archive(point,kval)]
            z = prior.complex_array(item['balanced'][ix])
            actual = prior.complex_array(item['dust_observables'][ix])
            archived_fields = prior.complex_array(item['full_fields'][ix])
            fields_error = max(fields_error,float(np.linalg.norm(ff@z-archived_fields,np.inf)/max(1.,np.linalg.norm(archived_fields,np.inf))))
            observable_error = max(observable_error,float(np.linalg.norm(oo@z-actual,np.inf)/max(1.,np.linalg.norm(actual,np.inf))))
            value = float(np.linalg.norm(actual[:,:2]-Phi[ix],np.inf))
            err = max(err,value)
            bound = float(bounds(s.Rational(str(t)))[-1])
            violation = max(violation,value-bound-1e-9*(1+abs(bound)))
        for name,value,limit in (('all_four_columns_22_fields',fields_error,1e-10),('actual_observable',observable_error,1e-10),('full_error_bound',violation,0.)):
            checks.add(name+'_'+str(kval),value<=limit,value,'<='+str(limit))
        omission_max = {power:0. for power in nonzero_sources}
        with mp.workdps(70):
            for t in (0.,.025,.05):
                point = [mp.mpf(str(value)) for value in np.polynomial.polynomial.polyval(t,bc.T)]
                point[1] = mp.sqrt(mp.mpf(10)*energy_mp(point)/33)
                aa,hh,hd,mc,rr,*parts = numeric_mp(point,kval)
                nrm = lambda mat:max(sum(abs(mat[i,j]) for j in range(mat.cols)) for i in range(mat.rows))
                residual = float(nrm(aa*hh-hd-hh*mc-rr)/max(mp.mpf(1),nrm(rr)))
                checks.add('raw_full_source_control_'+str(kval)+'_'+str(t),residual<=1e-30,residual,'<=1e-30; 70-digit algebraic shell')
                omissions = {}
                for power,part in zip((3,4,5),parts):
                    omitted = float(nrm(part/mp.mpf(kval)**power)/max(mp.mpf(1),nrm(rr)))
                    omission_max[power] = max(omission_max[power],omitted)
                    omissions[str(power)] = omitted
                controls.append(dict(ell=kval,time=t,residual=residual,precision=70,genuine_coefficient_omissions=omissions))
        for power,detected in omission_max.items():
            checks.add('genuine_source_omission_rejected_R'+str(power)+'_'+str(kval),detected>1e-30,detected,'>1e-30; at least one unchanged 70-digit point')
        ret,forced,ref,total = bounds(T)
        rows.append(dict(ell=kval,initial_Q_bound=str(k_initial),initial_energy_bounds=[str(value) for value in upper_energies],observation_Q_bound=str(k_observation),source_Q_bound=str(k_source),coordinate_norm_bound=str(coordinate_bound),residual_norm_bound=str(residual_bound),J0_inverse_bound=str(ji_bound),normalized_reference_source_bound=str(reference_source),reference_rate=str(reference_rate),lift_rate=str(rate),retained_bound=str(ret),forced_bound=str(forced),reference_bound=str(ref),total_bound=str(total),endpoint_display=dict(retained=float(ret),forced=float(forced),reference=float(ref),total=float(total)),sampled_original_error=err,bound_violation=violation))
        progress('Finite full-state bound completed for original ell='+str(kval))
    checks.add('five_modes_four_original_columns_preserved',sorted(row['ell'] for row in rows)==list(old.MODES) and all(np.array(item['initial_balanced']).shape==(20,4,2) for item in ar['modes']))
    checks.add('input_pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(row['passed'] for row in checks.rows)
    ok=passed==len(checks.rows)
    formulas=dict(modes=rows,source_coefficient_bounds={str(power):str(value) for power,value in source_norms.items()},matrices={('factored_R'+str(power)):prior.wire(mat) for power,mat in rc.items()},domain='Original nonzero ell=4,8,16,32,64; registered linear rotating B1 shell, 0<=t<=1/20; positive a,C,rho, J=1; both prepared columns, full coupled 20 states/22 fields',inequality='||W_full-Phi_M W0||_infinity <= [K_O K_initial exp(30t)+K_O K_source ||J0^-1||_infinity t exp(max(30,lambda_lift)t)+K_normalized_reference ||J0^-1||_infinity t exp(lambda_reference*t)] ||W0||_infinity',proof='Complete Laurent coefficient extraction and generic noncommuting source-update identities; inherited full Q-energy propagator with Qdot and Q-skew principals; Q>=D observable Cauchy-Schwarz bound; column Q energies for FULL initial mismatch; ALL factored source coefficients and rigorous coordinate/residual product majorants with positive forcing; separately verified normalized-reference component with matching initial chart. No state projection or term omission.',reference_component=reference_parent+'summary.json',physical_window_proved=False,useful_finite_band_accuracy_proved=False)
    diagnostics=dict(raw_source_controls=controls,original_archive_reused=True,new_trajectory_runs=0,retained_initial_response=True,complementary_columns_unchanged=True,largest_normalized_source_residual=max(row['residual'] for row in controls))
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diagnostics)}
    summary=dict(schema='r4c1-g3n5-dust-finite-energy-v4',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='FINITE_ENERGY_BOUNDS_CHECKED_USEFULNESS_OPEN' if ok else 'FINITE_ENERGY_BOUNDS_NOT_VERIFIED',finite_mode_error_bounds_proved=ok,full_dust_milestone_complete=False,useful_finite_mode_accuracy_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={name:common.sha(body) for name,body in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,mpmath=mp.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_finite_energy_attempt_04')
    ap.add_argument('--replay')
    ap.add_argument('--progress-file')
    args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.progress_file and not args.replay:
        progress_path=(ROOT/args.progress_file).resolve()
        progress_path.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS=progress_path.open('x',encoding='utf-8')
    try:bodies,summary=calculate()
    except BaseException:
        if PROGRESS is not None:traceback.print_exc(file=PROGRESS);PROGRESS.flush()
        raise
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=summary['validation'],passed=summary['passed'],total=summary['total'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    if PROGRESS is not None:PROGRESS.close()
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
