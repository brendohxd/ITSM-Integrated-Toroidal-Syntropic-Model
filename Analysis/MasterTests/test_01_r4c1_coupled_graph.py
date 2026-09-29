"""R4C1-S4A: full scalar graph metric, local rate and saved-transfer audit.

No upstream main() calls; no uniform evolution or physics pass is inferred.
"""
from __future__ import annotations

import json
import platform
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s

import test_01_r4c1_zero_branch as prior

up = prior.upstream
base = up.base
ROOT, OUT = base.ROOT, base.OUT
STEM = 'test_01_r4c1_coupled_graph'
a, H, k, C, rho, pd = base.a, base.H, base.k, base.C, base.rho, base.pd
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_GRAPH_CONTRACT_2026-09-26.md':
        '2ec5f0bc84ffb420bdbc1d8d7b0c3a16237ee87e36867ab8b106d5dbf35b3496',
    'Analysis/MasterTests/test_01_r4c1_zero_branch.py':
        '99cd1c52313dc5a5945ef0dd6f747f95848b2115847aec3c40a3fdc3a3ac278f',
    'Analysis/MasterTests/outputs/test_01_r4c1_zero_branch_summary.json':
        '1507c9b40b7a76985a81e520780fed6631eca59880870ae208d60d9587a6f374',
    'Theory/Gates/RES-001/RES001_R4C1_ZERO_BRANCH_REPORT_2026-09-26.md':
        '16f50f7150cddff8c297d237441fd9aabedb9f4f9c6f341b180160c508b619e5',
    'Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_transfers.json':
        '8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330',
}


def verify_sources(audit):
    observed = {}

    def visit(name, expected):
        name = name.replace('\\', '/')
        path = ROOT / name
        digest = base.sha(path)
        audit.test('pin:' + name, digest == expected, digest)
        if name in observed:
            return
        observed[name] = digest
        sidecar = path.with_name(path.name + '.sha256')
        audit.test('sidecar:' + name, sidecar.exists() and
                   sidecar.read_text().split()[0] == digest)
        if digest != expected:
            return
        if name.endswith('_summary.json'):
            raw = json.loads(path.read_text())
            audit.test('upstream_validation:' + name, raw.get('validation') == 'PASS')
            for section in ('inputs', 'artifacts'):
                for child, pin in raw.get(section, {}).items():
                    visit(child, pin)
    for name, pin in PINS.items():
        visit(name, pin)
    return observed


def derive(audit):
    raw = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    R, G, W, Mc, Vc = [prior.parse_matrix(raw, name)
                       for name in ('q_from_x', 'G', 'W', 'Mc', 'Vc')]
    Rt = up.dtime(R)
    A = s.BlockMatrix([[s.zeros(6), s.eye(6)], [-W, -G]]).as_explicit()
    Q = R.row_join(s.zeros(6))
    Qd = Rt.row_join(R)
    transform = Q.col_join(Qd)
    src = prior.read_raw('test_01_r4c1_scalar_constraints_matrices.json')
    aux = s.Matrix([s.sympify(z, locals=prior.SYMBOLS)
                    for z in src['auxiliary_solutions']]).subs(up.PARAMETER_SUBS)
    auxmap = aux.jacobian(list(base.q) + list(base.qd))
    audit.exact('auxiliary_map_is_homogeneous_linear',
                aux - auxmap * base.q.col_join(base.qd))
    reconstructed = prior.tidy(auxmap * transform)
    lapse, shift, de, z = [reconstructed[i, :] for i in range(4)]
    audit.exact('full_dust_multiplier', Qd[4, :] - C*lapse - s.Rational(2, 5)*C*Q[3, :])
    delta = -(k/a)**2 * Q[3, :] + pd*(k/a)*Q[5, :]
    audit.exact('full_regulator_constraint', z + delta)
    audit.exact('full_Mdot_retained', W - Vc - up.dtime(Mc))
    audit.exact('full_q_time_derivative', up.dtime(Q) + Q*A - Qd)
    audit.test('reject_missing_Rdot', any(v != 0 for v in Rt))
    audit.test('reject_missing_Mcdot', any(s.cancel(v) != 0 for v in W - Vc))

    # Build the norm in the original independent q,qdot chart first.
    iq, iv = s.eye(12)[:6, :], s.eye(12)[6:, :]
    dd = -(k/a)**2 * iq[3, :] + pd*(k/a)*iq[5, :]
    density = C**4*auxmap[2, :]/rho + s.Rational(8, 5)*iq[3, :]
    rows, names = [], []
    for i, name in enumerate(('u', 'v', 'r')):
        rows += [iq[i, :], (k/a)*iq[i, :], iv[i, :]]
        names += ['delta_'+name, 'p_delta_'+name, 'delta_'+name+'_dot']
    rows += [s.sqrt(3)*iv[3, :], s.sqrt(s.Rational(5, 11))*dd,
             iv[5, :]/s.sqrt(6), (k/a)*iq[5, :]/s.sqrt(15),
             density, (k/a)*iq[4, :]/C]
    names += ['sqrtK_delta_psi_dot', 'sqrtb_delta_Delta', 'sqrtc14_w_dot',
              'sqrtcL_p_w', 'density_contrast', 'dust_ADM_tilt']
    Fq = s.Matrix.vstack(*rows)
    F = prior.tidy(Fq * transform)
    Fdot = up.dtime(F)
    L = Fdot + F*A
    chosen = [0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14]
    minor_q = s.factor(Fq.extract(chosen, range(12)).det(method='domain-ge'))
    det_R = s.factor(R.det())
    minor = s.factor(minor_q * det_R**2)
    audit.test('full_rank_minor_nonzero_polynomial', minor != 0, str(minor))
    audit.test('reject_two_component_substitution', F.shape == (15, 12) and minor != 0)
    audit.test('reject_frozen_graph_metric', any(s.cancel(v) != 0 for v in Fdot))
    print('Full graph minor:', minor, flush=True)
    return dict(F=F, Fdot=Fdot, L=L, A=A, Fq=Fq, R=R, transform=transform,
                names=names, chosen=chosen, minor=minor, minor_q=minor_q,
                density_velocity=s.factor(density[0, 10]))


def rate_witness(audit, rec):
    """Post-scan exact strengthening in the unchanged registered norm.

    A fixed-metric differential estimate is tested, not every possible
    uniformly equivalent metric or the full solution operator.
    """
    R = rec['R']
    Ri = R.inv()
    inverse = s.BlockMatrix([[Ri, s.zeros(6)],
                            [-Ri*up.dtime(R)*Ri, Ri]]).as_explicit()
    density = rec['Fq'][13, :]
    # Physical graph data D=1, v_d=-1, with every other row zero.
    y = s.zeros(12, 1)
    y[4] = -C*a/k
    y[10] = (1-density[4]*y[4])/density[10]
    z = prior.tidy(inverse*y)
    expected = s.zeros(15, 1)
    expected[13], expected[14] = 1, -1
    audit.exact('witness_full_original_graph_data', rec['Fq']*y-expected)
    audit.exact('witness_full_canonical_reconstruction', rec['transform']*z-y)
    # The initial squared norm is two; rate = (Fz).T*(Fdot+FA)z / 2.
    terms = [s.cancel((rec['L'][13, j]-rec['L'][14, j])*z[j]/2)
             for j in range(12) if z[j] != 0]
    rate = s.factor(s.cancel(sum(terms)))
    p = s.Symbol('physical_p', positive=True)
    physical_rate = s.factor(rate.subs(k, a*p))
    scalar_velocities = base.ud**2+base.vd**2+base.rd**2
    B = 396*H**2+18*pd**2+6*scalar_velocities
    compact = (p-H)/2-pd/5 + rho*(9*(33*H**2-15*pd**2-5*scalar_velocities)
                                 -s.Rational(21, 2)*p**2)/(p*(B+p**2))
    audit.exact('witness_compact_exact_rate', physical_rate-compact)
    limit = s.limit(compact/p, p, s.oo)
    audit.exact('witness_positive_linear_rate', limit-s.Rational(1, 2))
    audit.test('witness_legitimate_full_data', expected.dot(expected) == 2 and
               density[10] != 0)
    print('Exact fixed-metric witness: rate/p ->', limit, flush=True)
    return dict(original_q_qdot=base.matrix_strings(y),
                canonical_x_xdot=base.matrix_strings(z),
                graph_data=base.matrix_strings(expected), squared_norm=2,
                logarithmic_norm_rate=str(compact), rate_over_p_limit=str(limit),
                interpretation='No wave-number-independent instantaneous rate bound in this fixed graph metric; full IVP remains open',
                provenance='Post-scan strengthening after the initial 94-check run; action, norm, domain and thresholds unchanged')


def mp_args(flow, t, wave):
    return [mp.mpf(float(v)) for v in up.background_args(flow.sol(t), wave)]


def metric_data(F):
    S = F.T * F
    values = mp.eigsy(S, eigvals_only=True)
    if values[0] <= 0:
        raise ArithmeticError('Full graph metric is not positive definite')
    chol = mp.cholesky(S).T
    return S, chol, values


def amplify(S0, S1, T):
    C0, C1 = mp.cholesky(S0).T, mp.cholesky(S1).T
    amp = max(mp.svd(C1*T*(C0**-1), compute_uv=False))
    vals, vec = mp.eigsy(S0)
    inverse_sqrt = vec * mp.diag([1/mp.sqrt(v) for v in vals]) * vec.T
    evolved = T.T*S1*T
    symmetric = inverse_sqrt*evolved*inverse_sqrt
    symmetric = (symmetric+symmetric.T)/2
    alternative = mp.sqrt(max(mp.eigsy(symmetric, eigvals_only=True)))
    return amp, abs(amp-alternative)/(1+abs(alternative))


def numeric(audit, rec):
    mp.mp.dps = 60
    fF = s.lambdify(up.ARGS, rec['F'], 'mpmath', cse=True)
    fD = s.lambdify(up.ARGS, rec['Fdot'], 'mpmath', cse=True)
    fA = s.lambdify(up.ARGS, rec['A'], 'mpmath', cse=True)
    flow = prior.integrate(prior.PARAMS, 'DOP853', 1e-12, 1e-14)
    audit.test('background_integration', flow.success)
    csv = np.genfromtxt(OUT/'test_01_r4c1_interacting_background_trajectory.csv',
                        delimiter=',', names=True)
    reference = np.vstack([csv[name] for name in up.NAMES])
    error = float(np.max(abs(flow.sol(csv['t'])-reference)/(1+abs(reference))))
    audit.test('unchanged_B1_trajectory', error < 1e-8, error)
    local = []
    for t in (0., .5, 1., 2., 3., 4.):
        print('Full graph local rates at t=', t, flush=True)
        for j in range(9):
            pval = 2*np.pi*2**j
            wave = pval*float(flow.sol(t)[0])
            args = mp_args(flow, t, wave)
            F, D, A = mp.matrix(fF(*args)), mp.matrix(fD(*args)), mp.matrix(fA(*args))
            S, chol, vals = metric_data(F)
            L = D + F*A
            E = L.T*F + F.T*L
            inv = chol**-1
            symmetric = inv.T*E*inv
            mu = max(mp.eigsy((symmetric+symmetric.T)/2, eigvals_only=True))/2
            local.append(dict(t=t, p=pval, mu=float(mu),
                              min_metric_eigenvalue=float(vals[0]),
                              condition=float(vals[vals.rows-1]/vals[0])))
    audit.test('positive_all_54_full_metrics', len(local) == 54 and
               min(x['min_metric_eigenvalue'] for x in local) > 0)
    audit.test('finite_sampled_log_rates', all(np.isfinite(x['mu']) for x in local))

    # Independent centered derivative along the actual background at fixed k.
    t0, step, wave = 1., 1e-6, 2*np.pi
    args = mp_args(flow, t0, wave)
    F, D, A = mp.matrix(fF(*args)), mp.matrix(fD(*args)), mp.matrix(fA(*args))
    L = D+F*A
    E = L.T*F + F.T*L
    Fplus = mp.matrix(fF(*mp_args(flow, t0+step, wave))) * (mp.eye(12)+step*A)
    Fminus = mp.matrix(fF(*mp_args(flow, t0-step, wave))) * (mp.eye(12)-step*A)
    fd = (Fplus.T*Fplus-Fminus.T*Fminus)/(2*step)
    derivative_error = float(mp.norm(fd-E)/(1+mp.norm(E)))
    audit.test('centered_full_energy_derivative', derivative_error < 1e-5, derivative_error)
    wrong = (F*A).T*F+F.T*(F*A)
    audit.test('reject_omitted_Fdot_energy', mp.norm(E-wrong)/(1+mp.norm(E)) > mp.mpf('1e-8'))

    rows, max_alternative = [], 0.
    inherited = prior.read_raw('test_01_r4c1_scalar_propagation_transfers.json')
    audit.test('all_registered_transfer_modes', [row['n'] for row in inherited] == [1, 2, 4, 8])
    for entry in inherited:
        wave = 2*np.pi*entry['n']
        F0 = mp.matrix(fF(*mp_args(flow, 0., wave)))
        F1 = mp.matrix(fF(*mp_args(flow, 4., wave)))
        S0, _, _ = metric_data(F0)
        S1, _, _ = metric_data(F1)
        methods = []
        for method in entry['methods']:
            audit.test('inherited_solver_success_n'+str(entry['n'])+method['method'], method['success'])
            amp, discrepancy = amplify(S0, S1, mp.matrix(method['endpoint_transfer']))
            max_alternative = max(max_alternative, float(discrepancy))
            methods.append(dict(method=method['method'], amplification=float(amp),
                                independent_norm_discrepancy=float(discrepancy)))
        audit.test('both_endpoint_methods_n'+str(entry['n']),
                   [z['method'] for z in methods] == ['DOP853', 'Radau'])
        err = abs(methods[0]['amplification']-methods[1]['amplification'])/(1+abs(methods[1]['amplification']))
        audit.test('two_method_graph_agreement_n'+str(entry['n']), err < 1e-5, err)
        rows.append(dict(n=entry['n'], methods=methods, discrepancy=err))
    audit.test('independent_norm_calculations_agree', max_alternative < 1e-8, max_alternative)
    return dict(local_rates=local, endpoint_transfers=rows,
                independent_norm_discrepancy=max_alternative,
                energy_derivative_relative_error=derivative_error,
                arithmetic='60 decimal digits; background and saved transfer accuracy unchanged',
                scope='Full scalar map; sampled local rates and four saved endpoint transfers only')


def main():
    audit = up.Audit()
    inputs = verify_sources(audit)
    if not all(c['passed'] for c in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN', failures=[c for c in audit.checks if not c['passed']])))
        return 1
    print('Constructing full graph map and exact rank minor...', flush=True)
    rec = derive(audit)
    samples = numeric(audit, rec)
    print('Deriving exact density/tilt rate witness...', flush=True)
    witness = rate_witness(audit, rec)
    formulas = OUT/(STEM+'_matrices.json')
    sample_path = OUT/(STEM+'_samples.json')
    base.write_json(formulas, dict(schema='r4c1-coupled-graph-matrices-v1',
        graph_rows=rec['names'], graph_map=base.matrix_strings(rec['F']),
        graph_map_derivative=base.matrix_strings(rec['Fdot']),
        original_graph_map=base.matrix_strings(rec['Fq']),
        selected_minor_rows=rec['chosen'], original_chart_minor=str(rec['minor_q']),
        full_canonical_minor=str(rec['minor']),
        density_dtau_dot_coefficient=str(rec['density_velocity']),
        exact_rate_witness=witness,
        metric_definition='S=F.T*F',
        energy_derivative_definition='E=(Fdot+F*A).T*F+F.T*(Fdot+F*A)',
        generator_source='test_01_r4c1_scalar_propagation_matrices.json:G,W'))
    base.write_json(sample_path, samples)
    passed = sum(c['passed'] for c in audit.checks)
    valid = passed == len(audit.checks)
    result = dict(schema='r4c1-coupled-graph-summary-v1', validation='PASS' if valid else 'FAIL',
        passed=passed, total=len(audit.checks),
        status='FIXED_GRAPH_DIFFERENTIAL_BOUND_REJECTED_FULL_IVP_OPEN' if valid else 'UNVALIDATED',
        physics_pass=False, gate_effect='NONE', review_status='DEFERRED', Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=['R9-MT1-S3','R9-MT1-S2','R9-MT1-S1','R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=inputs, executable_sha256=base.sha(Path(__file__)),
        artifacts={path.relative_to(ROOT).as_posix():base.sha(path) for path in (formulas, sample_path)},
        full_constrained_IVP='NOT_PROVED', uniform_energy_estimate='NOT_ESTABLISHED',
        fixed_metric_differential_bound='REJECTED_BY_EXACT_DENSITY_TILT_SEQUENCE' if valid else 'UNVALIDATED',
        canonical=dict(MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED'),
        summary=dict(full_graph_minor=str(rec['minor']),
                     exact_witness_rate_over_p=witness['rate_over_p_limit'],
                     endpoint_amplifications=[dict(n=x['n'], amplification=x['methods'][0]['amplification'])
                                              for x in samples['endpoint_transfers']],
                     max_local_rate=max(x['mu'] for x in samples['local_rates']),
                     max_metric_condition=max(x['condition'] for x in samples['local_rates']),
                     independent_norm_discrepancy=samples['independent_norm_discrepancy']),
        versions=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__),
        checks=audit.checks)
    base.write_json(OUT/(STEM+'_summary.json'), result)
    print(json.dumps({key:result[key] for key in ('validation','passed','total','status','summary')}))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
