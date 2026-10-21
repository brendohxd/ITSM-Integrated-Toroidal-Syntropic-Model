"""Constraint-restored scalar-rate energy restriction; no physical-mode clearance."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import traceback

import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_SCALAR_RATE_ENERGY_V1_CONTRACT_2026-10-21.md'
CSHA = 'abdc2005b326ecf23c2e20a77be18332727bad42221afdb1992a1ab17ff2d7c1'
LEGENDRE = 'Analysis/MasterTests/test_01_r4c1_legendre_domain_v1.py'
LSHA = '8b2b229d4b180533a03cbf4fed4869742597098e14cf9828d08d88c2ac3df3cc'
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
READ = lambda name: json.loads((ROOT/name).read_bytes())
STEPS = ('1e-20', '1e-24')
TOL = '1e-28'


def load_module():
    if SHA((ROOT/LEGENDRE).read_bytes()) != LSHA:
        raise ValueError('partial Legendre source changed')
    spec = importlib.util.spec_from_file_location('scalar_energy_legendre', ROOT/LEGENDRE)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


legendre = load_module()
body = legendre.original_body()
base = legendre.base


def progress(stage, **values):
    print(json.dumps(dict(stage=stage, **values), sort_keys=True), flush=True)


def text_number(value):
    return mp.nstr(value, 110)


def sources():
    meta = legendre.metadata()
    additional = {
        CONTRACT: CSHA, SELF: SHA((ROOT/SELF).read_bytes()),
        'Theory/Gates/RES-001/RES001_R4C1_LEGENDRE_DOMAIN_V1_REPORT_2026-10-21.md':
        '2a62ed1ec319a58020dfa252a33ba3f375bb4b3cdf24b48e776a8b030b6469ac',
        'Analysis/MasterTests/outputs/r4c1_legendre_domain_v1_attempt_01/summary.json':
        '94d038eadc170d02e428d5d2be5bc30e0296922c91bcf6b4f31aa966f0368d3b',
        'Analysis/MasterTests/outputs/r4c1_legendre_domain_v1_attempt_01/independent.json':
        '0be6a20e308e5a69ba289a20e8c0049864cea95fad2adcf32a7b02d3552d9901',
        'Analysis/MasterTests/outputs/r4c1_legendre_domain_v1_attempt_01/formulas.json':
        '9e66f66868a3bc1ab83b016cd90aedacae56d86a7c37b982ea8d9aff1706ffae'}
    for name, want in additional.items():
        p = ROOT/name; side = Path(str(p)+'.sha256')
        if SHA(p.read_bytes()) != want or side.read_text().split()[0].lower() != want:
            raise ValueError('new source/sidecar drift: '+name)
        meta['pins'][name] = want
        meta['records'][name] = base.metadata(p)
        meta['records'][side.relative_to(ROOT).as_posix()] = base.metadata(side)
    return meta


def small(ch, name, error, criterion=TOL):
    ch.add(name, error < mp.mpf(criterion), text_number(error), 'normalized < '+criterion)


def symbolic(ch):
    t, p, f = sy.symbols('t p f', real=True)
    p0, d, inv, ell, es, a0, a1, a2, a3, dust, F0, F1 = sy.symbols(
        'P d Rinv ell ell_s a0 a1 a2 a3 Edust F0prime F1prime', real=True)
    # Quadratic stationary response written in its three independent invariants;
    # this proves the dimension-independent identity without a diagonal-R premise.
    q0, q1, q2 = sy.symbols('r0_Rinv_r0 y_dot_d d_Rinv_d', real=True)
    scalar = a0+a1*(p+t*f)+a2*(p+t*f)**2/2+a3*(p+t*f)**3/6
    numerator = q0/2+t*q1+t*t*q2/2-scalar+dust+F0+t*F1
    H = numerator/(p+t*f)
    fs = sy.diff(scalar, t).subs(t, 0)/f
    fss = sy.diff(scalar, t, 2).subs(t, 0)/f**2
    C = numerator.subs(t, 0)
    predicted = (q2-fss*f*f)/p-2*(q1-fs*f+F1)*f/p**2+2*C*f*f/p**3
    ch.add('exact_complete_inverse_clock_second_variation', sy.cancel(sy.diff(H, t, 2).subs(t, 0)-predicted) == 0)
    # A dense, indefinite, nonsingular matrix checks off-diagonal stationary
    # response independently of the invariant notation above.
    R = sy.Matrix([[2, 1], [1, -3]])
    yy = sy.Matrix([p0, ell]); dd = sy.Matrix([d, es])
    E = ((yy+t*dd).T*R.inv()*(yy+t*dd))[0]/2
    ch.add('dense_indefinite_full_velocity_response', sy.cancel(sy.diff(E, t, 2)-(dd.T*R.inv()*dd)[0]) == 0)
    ch.add('frozen_velocity_hessian_rejected', (dd.T*R.inv()*dd)[0] != 0)
    ch.add('generic_lapse_flux_deletion_rejected', sy.cancel(sy.diff(F0/(p+t*f), t, 2).subs(t, 0)-2*F0*f*f/p**3) == 0 and F0 != 0)
    # Retain, rather than silently zero, the initial compatibility residual J.
    K, z, j, esy, dp_y, kq, w, A, b, U, zh = sy.symbols('K Zhat J ell_s_dot_y y_dot_deltaP K_Q w A b U Zhat_value', real=True)
    fs0, fss0 = sy.symbols('f0_s f0_ss', real=True)
    C0 = j-p*(esy+fs0-b*w*w*zh)
    general = (q2-fss0*f*f)/p-2*(dp_y-esy*f-fs0*f)*f/p**2+2*C0*f*f/p**3
    compact = q2/p-2*dp_y*f/p**2+(-fss0/p+2*b*w*w*zh/p**2+2*j/p**3)*f*f
    ch.add('exact_restored_compatibility_residual_identity', sy.cancel(general-compact) == 0)
    ch.add('nonzero_compatibility_residual_not_erased', sy.diff(compact, j) == 2*f*f/p**3)
    # Localization majorant: rho=sqrt(epsilon) makes all exponents integers.
    rho = sy.Symbol('rho', positive=True)
    c, ka, aa, bb, uu, ud, rs, pp, EE, PP, YY, cr, eta = sy.symbols(
        'c Koverp absA absb absU absUd Rmax p E P Y C_R eta', positive=True)
    eps = rho*rho
    delta = (4*ka*c*c*eps**2+48*aa*c**3*eps**3
             +32*bb*c**4/pp**2*(ud*eps**4+uu*rs*eps**3)
             +2*YY*PP/pp**2*rho**7+cr/(eta*pp)*(PP*rho**7+EE*rho**6)**2)
    poly = sy.Poly(sy.expand(delta), rho)
    coefficients = poly.as_dict()
    total = sum(coefficients.values())
    wanted = 4*ka*c*c+48*aa*c**3+32*bb*c**4/pp**2*(ud+uu*rs)+2*YY*PP/pp**2+cr/(eta*pp)*(PP+EE)**2
    ch.add('localization_all_remainder_powers_at_least_two', all(power[0] >= 4 for power in coefficients))
    ch.add('localization_nonnegative_majorant_coefficients', all(v.is_positive is True for v in coefficients.values()))
    ch.add('localization_explicit_Cstar_identity', sy.cancel(total-wanted) == 0)
    eta1 = sy.Symbol('eta_positive', positive=True)
    ch.add('frozen_maps_node_curvature_scale_not_prediction', sy.cancel((3*eta1)/(eta1/5)-15) == 0)
    return dict(
        Hessian='Hss[f,f]=<(d^T R^-1 d-f0_ss*f^2)/p-2*(y.d-f0_s*f+deltaFprime)*f/p^2+2*C0*f^2/p^3>',
        compact='Hss=<(d^T R^-1 d)/p-2*y.deltaP*f/p^2+(-f0_ss/p+2*g*Zhat/p^2+2*J/p^3)*f^2>, deltaF=0 on registered flat family',
        restoration=dict(G='g*Zprime=2*b*U*w^3*wprime', translation='delta_lambda=<G*f>/d_translation; d_translation=-e*k/2',
                         source='deltaS=-G*f+delta_lambda*sin(theta)*wprime',
                         momentum='deltaP_Kzz=I_z(deltaS), deltaP_Xy=delta_lambda*sin(theta), all others zero',
                         flux='F=gamma*pVz; delta pVz=0, hence deltaF=0, but F0prime remains'),
        derivatives=dict(ell_s_Kyy='-2*b*Z*w^2', ell_s_Xy='-b*Z*w',
                         f0_s='K_Q*(1+w^2)*p-3*A*abs(w)^3*p^2',
                         f0_ss='K_Q*(1+w^2)-6*A*abs(w)^3*p'),
        localization=dict(
            hypotheses='fixed eta>0, p>0, e<=1/500, k>0, h=I, w=e*cos(kz), Z=U*w^2, normalized-average L2 f=1 supported epsilon<x<2epsilon near either node; full auxiliary admission NOT assumed',
            length='L=2*pi/k', c='e*k', d_abs='e*k/2',
            bounds='Y>=sup sqrt(y_Kzz^2+y_Xy^2), Rmax>=sup|shift|, sigma>=sup_patch|J|, C_R=200/33',
            M='16*abs(b*U)*c^4',
            P='2*M*sqrt(L)+M/(d_abs*sqrt(L)); ||deltaP||_L2<=P*epsilon^(7/2)',
            E='8*abs(b*U)*(1+2*e)*c^3; ||ell_s*f||_L2<=E*epsilon^3',
            Delta='4*(K_Q/p)*c^2*eps^2+48*abs(A)*c^3*eps^3+32*abs(b)*c^4/p^2*(abs(Ud)*eps^4+abs(U)*Rmax*eps^3)+2*Y*P/p^2*eps^(7/2)+C_R/(eta*p)*(P*eps^(7/2)+E*eps^3)^2',
            theorem='|Hss[f,f]+K_Q/p|<=Delta(epsilon)+2*sigma/p^3',
            Cstar=str(wanted),
            negative_curvature_condition='sigma<=K_Q*p^2/8 and 0<eps<=min(1,L/16,sqrt(K_Q/(4*p*Cstar))) imply Hss[f,f]<=-K_Q/(2*p)',
            limitation='conditional continuum theorem, not certified continuum bounds for the stored initial data, full physical admission, an invariant ghost test or any weighted-domain no-go'))


def perturb(X, vector, step):
    Y = dict(X, Q=[row.copy() for row in X['Q']])
    for row, value in zip(Y['Q'], vector):
        row[11] += step*value
    return Y


def vector_probes(theta):
    raw = {'constant': [mp.mpf(1) for x in theta],
           'cos': [mp.cos(x) for x in theta],
           'cos_squared': [mp.cos(x)**2 for x in theta],
           'sin_twice': [mp.sin(2*x) for x in theta],
           'mixed': [mp.sin(3*x)+mp.mpf(2)*mp.cos(2*x)/7 for x in theta]}
    return {name: [value/mp.sqrt(body.mean([z*z for z in values])) for value in values]
            for name, values in raw.items()}


def grid_job(task):
    index, point, initial, n, offset = task
    ch = base.Checks()
    try:
        raw, X = body.build_data(point, initial, n, offset, 100)
        out = body.restore(X, raw); p = raw['rate']; par = raw['par']
        matrices = [mp.matrix(R) for R in raw['Rs']]
        inverses = [R**-1 for R in matrices]
        ell0 = []; ells = []; ys = []; scalar0 = []; fs = []; fss = []; E = []; F = []
        q, mom, dq = out['q'], out['p'], out['dq']
        zero = [mp.mpf(0)]*12
        maximum_derivative_error = mp.mpf(0)
        stationary_error = mp.mpf(0)
        for i in range(n):
            L0, grad0 = body.local_derivatives(q[i], dq[i], zero, p, par)
            ell0.append(mp.matrix(grad0[:12])); scalar0.append(L0)
            w, Z = q[i][7], q[i][13]
            es = mp.zeros(12, 1); es[3] = -2*par['b']*Z*w*w; es[7] = -par['b']*Z*w
            ells.append(es)
            fs.append(par['K_Q']*(1+w*w)*p-3*par['A']*abs(w)**3*p*p)
            fss.append(par['K_Q']*(1+w*w)-6*par['A']*abs(w)**3*p)
            # Independent original-density polynomial polarization. Along s>0
            # the local force is cubic; no w-third derivative is taken.
            h = p/7
            values = [body.body(q[i], dq[i], zero, p+j*h, par) for j in (-2, -1, 0, 1, 2)]
            want_s = (values[0]-8*values[1]+8*values[3]-values[4])/(12*h)
            want_ss = (values[3]-2*values[2]+values[1])/(h*h)
            _, grad_one = body.local_derivatives(q[i], dq[i], zero, p+1, par)
            maximum_derivative_error = max(maximum_derivative_error,
                abs(want_s-fs[-1])/(1+abs(want_s)), abs(want_ss-fss[-1])/(1+abs(want_ss)),
                max(abs(grad_one[j]-grad0[j]-es[j])/(1+abs(es[j])) for j in range(12)))
            P = mp.matrix([2*z for z in mom[i][:6]]+mom[i][6:12])
            yy = inverses[i]*(P-ell0[-1]); ys.append(yy)
            _, solved_gradient = body.local_derivatives(q[i], dq[i], list(yy), p, par)
            stationary_error = max(stationary_error, max(abs(solved_gradient[a]-P[a])/(1+abs(P[a])) for a in range(12)))
            energy, flux, volume, DV = body.envelope(q[i], mom[i], dq[i], p, list(yy), par, 0)
            E.append(energy); F.append(flux)
        small(ch, 'original_density_scalar_rate_derivatives', maximum_derivative_error)
        small(ch, 'all_twelve_original_density_stationarity_rows', stationary_error)
        divF = body.Dmul(raw['D'], F)
        C = [a+b for a, b in zip(E, divF)]
        # Full restored momentum response to EVERY scalar-rate basis vector.
        responses = [mp.zeros(12, n) for i in range(n)]
        restore_error = mp.mpf(0); flux_response = mp.mpf(0)
        for j in range(n):
            unit = [mp.mpf(i == j) for i in range(n)]
            varied = body.restore(perturb(X, unit, 1), raw)
            Gf = [out['g'][i]*dq[i][13]*unit[i] for i in range(n)]
            lam = body.mean(Gf)/out['d']
            source = [-Gf[i]+lam*raw['sine'][i]*dq[i][7] for i in range(n)]
            primitive = body.mv(raw['I'], source)
            for i in range(n):
                dp = [2*(varied['p'][i][a]-mom[i][a]) for a in range(6)]
                dp += [varied['p'][i][a]-mom[i][a] for a in range(6, 12)]
                expected = [mp.mpf(0)]*12; expected[5] = primitive[i]; expected[7] = lam*raw['sine'][i]
                for a in range(12):
                    responses[i][a, j] = dp[a]
                    restore_error = max(restore_error, abs(dp[a]-expected[a])/(1+abs(expected[a])))
                flux_response = max(flux_response, abs(varied['p'][i][8]-mom[i][8]))
        small(ch, 'full_affine_spatial_global_mean_restore', restore_error)
        small(ch, 'delta_flux_zero_not_F0_flux_deleted', flux_response)
        K = mp.zeros(n); response_term = mp.zeros(n); cross = mp.zeros(n)
        for i in range(n):
            Di = responses[i].copy()
            for a in range(12):
                Di[a, i] -= ells[i][a]
            response_term += Di.T*inverses[i]*Di/(n*p)
            for j in range(n):
                cross[i, j] += sum(ys[i][a]*Di[a, j] for a in range(12))
            K[i, i] = (-fss[i]/p+2*fs[i]/p**2+2*C[i]/p**3)/n
        K += response_term-(cross+cross.T)/(n*p*p)
        small(ch, 'complete_restricted_Hessian_symmetric', max(abs(K[i, j]-K[j, i]) for i in range(n) for j in range(n)))

        def direct(vector, step):
            varied = body.restore(perturb(X, vector, step), raw)
            result = []
            for i in range(n):
                s = p+step*vector[i]
                if s <= 0:
                    raise ValueError('nonpositive force clock on direct probe')
                P = mp.matrix([2*z for z in varied['p'][i][:6]]+varied['p'][i][6:12])
                ell = ell0[i]+step*vector[i]*ells[i]
                velocity = inverses[i]*(P-ell)
                value, flux, vol, DV = body.envelope(q[i], varied['p'][i], dq[i], s, list(velocity), par, 0)
                result.append((value+divF[i])/s)
            return body.mean(result)

        H0 = body.mean([C[i]/p for i in range(n)])
        probes = []; flux_effect = mp.mpf(0); response_effect = mp.mpf(0)
        for name, v in vector_probes(raw['theta']).items():
            vector = mp.matrix(v)
            predicted = (vector.T*K*vector)[0]
            steps = []
            for hstr in STEPS:
                h = mp.mpf(hstr)
                numerical = (direct(v, h)-2*H0+direct(v, -h))/(h*h)
                err = abs(numerical-predicted)/(1+abs(numerical)+abs(predicted))
                small(ch, name+'_direct_resolved_velocity_second_difference_'+hstr, err)
                steps.append(dict(step=hstr, normalized_error=text_number(err), direct_curvature=text_number(numerical)))
            flux = 2*body.mean([divF[i]*v[i]**2 for i in range(n)])/p**3
            temporal = (vector.T*response_term*vector)[0]
            flux_effect = max(flux_effect, abs(flux)); response_effect = max(response_effect, abs(temporal))
            probes.append(dict(name=name, curvature=text_number(predicted), omit_flux_difference=text_number(flux),
                               omit_velocity_response_difference=text_number(temporal), direct_checks=steps))
        compatibility = []
        for i in range(n):
            Zhat = raw['Ud']*q[i][7]**2-raw['R'][i]*dq[i][13]
            J = C[i]+p*(sum(ells[i][a]*ys[i][a] for a in range(12))+fs[i]-out['g'][i]*Zhat)
            compatibility.append(J)
        diag = [n*K[i, i] for i in range(n)]
        offdiag = max(abs(n*K[i, j]) for i in range(n) for j in range(n) if i != j)
        # These are finite numerical row estimates, not interval eigenvalue bounds.
        lower = min(n*K[i, i]-sum(n*abs(K[i, j]) for j in range(n) if j != i) for i in range(n))
        upper = max(n*K[i, i]+sum(n*abs(K[i, j]) for j in range(n) if j != i) for i in range(n))
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset,
            working_digits=100, Hessian=[[text_number(K[i, j]) for j in range(n)] for i in range(n)],
            normalization='Hss=f^T K_payload f; average-L2 operator matrix is n*K_payload; working digits are not certified significant digits',
            numerical_average_L2_Gershgorin=[text_number(lower), text_number(upper)],
            diagonal_range=[text_number(min(diag)), text_number(max(diag))], largest_offdiagonal=text_number(offdiag),
            compatibility_scaled_max=text_number(max(abs(x) for x in compatibility)/(par['K_Q']*p*p)),
            node_compatibility_scaled=text_number(compatibility[0]/(par['K_Q']*p*p)),
            compatibility=[text_number(x) for x in compatibility], probes=probes,
            max_omitted_flux_effect=text_number(flux_effect), max_omitted_temporal_response=text_number(response_effect),
            physical_modes_normalized=False, auxiliary_admission=False, state_adopted_or_evolved=False)
    except Exception:
        ch.add('unexpected_grid_exception', False, traceback.format_exc())
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset, incomplete=True)
    return (index, n, offset), result, ch.rows


def calculate(workers):
    mp.mp.dps = 100
    before = sources(); ch = base.Checks(); formulas = symbolic(ch)
    points = body.lift.READ(body.nodal.reg.JOINT+'independent.json')
    initial = body.lift.READ(body.lift.cop.CERTS)
    if len(points) != 9 or len(initial) != 9 or any(a['family'] != b['family'] or a['eta'] != b['eta'] for a, b in zip(points, initial)):
        raise ValueError('registered input order changed')
    tasks = [(i, a, b, n, o) for i, (a, b) in enumerate(zip(points, initial)) for n in (17, 25, 33) for o in (0, 1)]
    results = {}
    progress('REGISTERED_SCALAR_HESSIAN_TASKS', tasks=len(tasks), workers=min(workers, 16))
    if workers == 1:
        for task in tasks:
            key, result, rows = grid_job(task); results[key] = (result, rows)
            progress('GRID_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    else:
        with ProcessPoolExecutor(max_workers=min(workers, 16), mp_context=multiprocessing.get_context('spawn')) as pool:
            futures = [pool.submit(grid_job, task) for task in tasks]
            for future in as_completed(futures):
                key, result, rows = future.result(); results[key] = (result, rows)
                progress('GRID_FINISHED', key=key, passed=sum(r['passed'] for r in rows), total=len(rows))
    payload = []
    for key in sorted(results):
        result, rows = results[key]; payload.append(result)
        for row in rows:
            ch.add(str(key)+'_'+row['name'], row['passed'], row.get('value'), row.get('criterion'))
    completed = [r for r in payload if not r.get('incomplete')]
    ch.add('all_54_registered_controls_completed', len(completed) == 54)
    ch.add('actual_nonzero_lapse_flux_control_retained', any(mp.mpf(r['max_omitted_flux_effect']) > mp.mpf('1e-70') for r in completed))
    ch.add('actual_nonzero_temporal_response_control_retained', any(mp.mpf(r['max_omitted_temporal_response']) > mp.mpf('1e-70') for r in completed))
    if sources() != before:
        raise ValueError('source/native runtime metadata changed')
    failures = [r for r in ch.rows if not r['passed']]
    summary = dict(validation='CONSTRAINED_SCALAR_RATE_HESSIAN_VERIFIED' if not failures else 'SCALAR_RATE_ENERGY_UNRESOLVED',
                   passed=len(ch.rows)-len(failures), total=len(ch.rows), failed_checks=failures, unknown_checks=[], checks=ch.rows,
                   source_metadata=before, physics_pass=False, gate_effect='NONE', Rule9_cleared=False, review_status='DEFERRED',
                   stage2_complete=False, stage3_entered=False, MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED',
                   UVIR_003='IN_PROGRESS', Stage4A='CLOSED', TOP_X4='UNCHANGED',
                   full_physical_energy_norm_derived=False, full_auxiliary_hierarchy_closed=False,
                   continuum_initial_compatibility_bounds_certified=False, physical_ghost_or_instability_proved=False,
                   physical_cutoff_derived=False, healthy_GR_proved=False, state_adopted_or_evolved=False,
                   complete372_spectrum=False, conditional_localization_theorem=True)
    return summary, dict(cases=payload), formulas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--output', type=Path)
    group.add_argument('--replay', type=Path)
    parser.add_argument('--workers', type=int, default=16)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error('--workers must be1..16')
    if args.preflight:
        ch = base.Checks(); symbolic(ch)
        bad = [r for r in ch.rows if not r['passed']]
        progress('SYMBOLIC_METHOD_PREFLIGHT_ONLY', passed=len(ch.rows)-len(bad), total=len(ch.rows), failures=bad)
        raise SystemExit(bool(bad))
    dest = (args.replay or args.output).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):
        raise ValueError('destination outside declared output root')
    if args.output and dest.exists():
        raise FileExistsError('never overwrite an attempt')
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('replay directory missing')
    summary, independent, formulas = calculate(args.workers)
    if args.output:
        dest.mkdir(parents=False, exist_ok=False)
    for name, value in [('summary.json', summary), ('independent.json', independent), ('formulas.json', formulas)]:
        base.pair(dest, name, ENC(value), bool(args.replay))
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in dest.iterdir()} != expected:
        raise ValueError('unexpected scientific receipt file set')
    progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
             passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    raise SystemExit(bool(summary['failed_checks']))


if __name__ == '__main__':
    multiprocessing.freeze_support(); main()
