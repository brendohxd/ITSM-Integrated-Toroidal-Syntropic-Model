"""Maximal complete two-form inverse domain, not full coupled generator closure."""
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
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_TWO_NODE_GRAPH_DOMAIN_V1_CONTRACT_2026-10-21.md'
CSHA = 'dd0645e4d411e8ced0a208326e72aaca68cd78086f6abecfab9c8768d428d628'
ENERGY = 'Analysis/MasterTests/test_01_r4c1_scalar_rate_energy_v1.py'
ESHA = 'a159ac186b11fd823f5d8daf33af6a189606e9d80cabe141f97f4feda4bda95e'
DESCRIPTOR = 'Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py'
DSHA = '99a71aa721140a59c0e27af4632e4c52c9ae30138a8ae9af53b690b5c2cee157'
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def load(name, filename, digest):
    if SHA((ROOT/filename).read_bytes()) != digest:
        raise ValueError('source drift: '+filename)
    spec = importlib.util.spec_from_file_location(name, ROOT/filename)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


energy = load('graph_domain_energy', ENERGY, ESHA)
descriptor = load('graph_domain_descriptor', DESCRIPTOR, DSHA)
body, base = energy.body, energy.base


def sources():
    meta = energy.sources()
    additional = {**descriptor.PINS, DESCRIPTOR: DSHA, CONTRACT: CSHA,
        SELF: SHA((ROOT/SELF).read_bytes()),
        'Theory/Gates/RES-001/RES001_R4C1_SCALAR_RATE_ENERGY_V1_REPORT_2026-10-21.md':
        '33a623673d4a62fa8a466b80089ca26755faecee4a91a7a11343dc736b345a3f',
        'Analysis/MasterTests/outputs/r4c1_scalar_rate_energy_v1_attempt_01/summary.json':
        '066bddf8701db87794fd35c49e9832bc4f7e0ccdfc57dd0e9ff0eb04f212ba8a',
        'Analysis/MasterTests/outputs/r4c1_scalar_rate_energy_v1_attempt_01/independent.json':
        'c79b10470b890ef973b7ac630d1a749d824500da089c9c73f9c8c65e0f2a992f',
        'Analysis/MasterTests/outputs/r4c1_scalar_rate_energy_v1_attempt_01/formulas.json':
        '38196c8400c244673846010ba470a2ad9c8a30a9dce24a49f663adaf04bfbbdd'}
    for name, want in additional.items():
        p = ROOT/name; side = Path(str(p)+'.sha256')
        if SHA(p.read_bytes()) != want or side.read_text().split()[0].lower() != want:
            raise ValueError('new source/sidecar drift: '+name)
        meta['pins'][name] = want
        meta['records'][name] = base.metadata(p)
        meta['records'][side.relative_to(ROOT).as_posix()] = base.metadata(side)
    return meta


def progress(stage, **values):
    print(json.dumps(dict(stage=stage, **values), sort_keys=True), flush=True)


def small(ch, name, error):
    ch.add(name, error < mp.mpf('1e-28'), mp.nstr(error, 70), 'normalized < 1e-28')


def exact(ch):
    q = sy.Matrix(sy.symbols('q0:3', real=True)); momenta = sy.Matrix(sy.symbols('P0:3', real=True))
    s, Z, b = sy.symbols('s Z b', real=True)
    coordinates = list(q)+list(momenta)+[s, Z]
    g = b*q.dot(q)
    theta = list(momenta)+[sy.Integer(0)]*3+[0, -g*s]
    omega = sy.Matrix(8, 8, lambda i, j: sy.diff(theta[j], coordinates[i])-sy.diff(theta[i], coordinates[j]))
    r = sy.Matrix(sy.symbols('r0:8', real=True))
    dg = sy.Matrix([sy.diff(g, x) for x in q])
    vq = r[3:6, 0]; vz = -r[6]/g; vs = (r[7]-s*dg.dot(vq))/g
    vp = -r[:3, 0]-s*dg*vz
    recovered = sy.Matrix(list(vq)+list(vp)+[vs, vz])
    ch.add('full_cross_coupled_inverse_identity', all(sy.cancel(x) == 0 for x in omega*recovered-r))
    ch.add('full_two_form_skew_with_retained_crosses', omega+omega.T == sy.zeros(8))
    ch.add('deleting_B_cross_changes_inverse', sy.cancel(vs-r[7]/g) != 0)
    # Exact variational identity with nonzero background two-form drift.
    perturbation = sy.Matrix(sy.symbols('u0:8', real=True))
    background = sy.Matrix(sy.symbols('T0:8', real=True))
    rates = sy.Matrix(sy.symbols('v0:8', real=True))
    eps = sy.Symbol('eps', real=True)
    drift = sum((sy.diff(omega, x)*perturbation[j] for j, x in enumerate(coordinates)), sy.zeros(8))*background
    shifted = omega.subs(dict(zip(coordinates, [x+eps*u for x, u in zip(coordinates, perturbation)])), simultaneous=True)
    actual = sy.diff(shifted*(background+eps*rates), eps).subs(eps, 0)
    ch.add('exact_linearization_retains_background_drift', all(sy.expand(z) == 0 for z in actual-omega*rates-drift))
    ch.add('background_drift_cannot_be_zeroed_generically', any(sy.expand(z) != 0 for z in drift))
    # Analytic BOTH-node identities, including a moving-frame cross example.
    angle = sy.Symbol('theta', real=True)
    e, k, p = sy.symbols('e k p', positive=True)
    w = e*sy.cos(angle); gg = b*w*w
    za, sa = sy.Function('Zrate')(angle), sy.Function('srate')(angle)
    rs = -gg*za; rz_adjusted = gg*sa
    for n, node in enumerate((sy.pi/2, 3*sy.pi/2)):
        ch.add('both_node_'+str(n)+'_adjusted_double_traces', all(sy.simplify(expr.subs(angle, node)) == 0
               for expr in (rs, k*sy.diff(rs, angle), rz_adjusted, k*sy.diff(rz_adjusted, angle))))
        raw_rz = 2*p*b*w  # canonical frame rate V_y=1, srate=0
        slope = sy.simplify(k*sy.diff(raw_rz, angle).subs(angle, node))
        ch.add('raw_rZ_simple_zero_cross_counterexample_'+str(n), slope == (-1 if n == 0 else 1)*2*p*b*e*k)
    x = sy.Symbol('x', positive=True); f = sy.Function('f')(x)
    ch.add('Hardy_first_integration_identity', sy.simplify(sy.diff(-sy.diff(f, x)**2/x, x)
           +2*sy.diff(f, x)*sy.diff(f, x, 2)/x-sy.diff(f, x)**2/x**2) == 0)
    ch.add('Rellich_second_integration_identity', sy.simplify(sy.diff(-f*f/(3*x**3), x)
           +sy.Rational(2, 3)*f*sy.diff(f, x)/x**3-f*f/x**4) == 0)
    ch.add('finite_interval_double_Hardy_constant', (sy.Rational(2, 3)*2)**2 == sy.Rational(16, 9))
    concave = sy.sin(x)-2*x/sy.pi
    ch.add('sine_chord_endpoint_values', concave.subs(x, 0) == 0 and concave.subs(x, sy.pi/2) == 0)
    ch.add('sine_chord_concavity_identity', sy.diff(concave, x, 2) == -sy.sin(x))
    eta = sy.Symbol('eta', positive=True)
    values = {b: 5*eta/11, p: eta/5, e: sy.Rational(1, 500), k: 40}
    C = sy.pi**2/(3*b*e**2*k**2)
    ch.add('frozen_map_whole_circle_constant', sy.cancel(C.subs(values)-1375*sy.pi**2/(12*eta)) == 0)
    positive_integrand = x**4*(1-x)**4/(1+x*x)
    ch.add('exact_pi_upper_bound_positive_integral', sy.integrate(positive_integrand, (x, 0, 1)) == sy.Rational(22, 7)-sy.pi)
    upper = (sy.Rational(22, 7)**2/(3*b*e**2*k**2)).subs(values)
    ch.add('exact_rational_constant_ceiling', sy.cancel(upper-sy.Rational(166375, 147)/eta) == 0)
    B2 = (p*b)**2*(sy.Rational(11, 4)*e**4+4*e**2)
    coefficient = sy.cancel(B2.subs(values)/eta**4)
    ch.add('B_norm_bound_below_one_on_frozen_eta_domain', coefficient > 0 and coefficient < 1, str(coefficient))
    # Elementary Young estimate for the graph norm. No Hamiltonian sign is used.
    a, h = sy.symbols('a h', real=True)
    ch.add('graph_norm_Young_bound_exact', sy.expand(2*a*a+2*h*h-(a+h)**2-(a-h)**2) == 0)
    ch.add('eta_zero_auxiliary_kernel_retained', omega.subs(b, 0).rank() == 6)
    alpha = sy.Rational(7, 4)
    ch.add('weak_H2_quotient_unbounded_but_L2', alpha < 2 and 2*(alpha-2) > -1 and alpha > sy.Rational(3, 2))
    ch.add('constant_and_simple_zero_quotients_fail_L2', sy.Integer(-4) <= -1 and sy.Integer(-2) <= -1)
    return dict(
        scope='Complete reduced two-form on its retained canonical quotient/mean Hilbert space; not the full generator',
        order=['Q', 'P', 's', 'Z'],
        action='Omega*v=(-vP-B^*vZ, vQ, -g*vZ, g*vs+B*vQ), B=s*Dg including projections and means',
        inverse='vQ=rP; vZ=-rs/g; vs=(rZ-B*rP)/g; vP=-rQ+B^*(rs/g)',
        maximal_domain='Yg={r in L2(canonical+aux): rs/g in L2, (rZ-B*rP)/g in L2}; quotients are a.e., no node value invented',
        graph_norm='N(r)^2=||r||^2+||rs/g||^2+||(rZ-B*rP)/g||^2; N<=actual_graph_norm<=sqrt(3)*N on frozen family',
        analytic_closedness='Omega bounded skew-adjoint and injective because g>0 a.e.; range dense; inverse closed on range=Yg; complete graph norm; not a bounded inverse on all L2',
        B='p*b*(w^2*(a_hxx/2+3*a_hyy/2+a_L/2)+2*w*a_Vy), with mean L and projected Vy',
        B_norm_squared=str(B2.subs(values)),
        trace_equivalence='If rs and rztilde=rZ-B*rP are periodic H2, quotient L2 iff residual AND first derivative vanish at BOTH nodes',
        trace_bound='||r/g||_L2<=pi^2/(3*abs(b)*e^2*k^2)*||r_second||_L2; four nearest-node half-arcs cover whole circle',
        frozen_constant='1375*pi^2/(12*eta) < 166375/(147*eta), 0<eta<=1; reference chart, not physical cutoff',
        Hardy_proof='finite-interval boundary terms -f(a)^2/(3*a^3) and -fprime(a)^2/a are nonpositive; traces zero at node; ||f/x^2||<=4/3||f_second||; H2 extension uses local L2 Taylor remainder',
        full_descriptor='Always r=K*u=Hessian(H)*u-dOmega[u]*Xdot; canonical vQ=rP, including mean rates; no K-image/domain-invariance or full generator closedness is proved',
        weak_example='r=abs(cos(theta))^(7/4) has H2 zero traces; r/g proportional abs(cos(theta))^(-1/4) is unbounded but L2',
        moving_nodes='linearized descriptor and B cross retained; raw rZ may have simple zero; nonlinear moving/lifted nodes and domain persistence remain open',
        limitations='positive graph norm is not positive physical Hamiltonian energy; no physical stability, mode admission, cutoff, healthy GR, matching or evolution')


def convolve(a, b):
    result = {}
    for i, x in a.items():
        for j, y in b.items():
            result[i+j] = result.get(i+j, sy.Integer(0))+x*y
    return {m: sy.simplify(value) for m, value in result.items() if value != 0}


def analytic_controls(ch):
    mp.mp.dps = 100
    controls = []
    cos2 = {0: sy.Rational(1, 2), 2: sy.Rational(1, 4), -2: sy.Rational(1, 4)}
    for number in range(8):
        a, b, c = (sy.Rational(number+1, 13), sy.Rational(number-3, 17), sy.Rational(2-number, 19))
        P = {0: sy.Integer(1), 1: a/(2*sy.I), -1: -a/(2*sy.I),
             2: b/2, -2: b/2, 3: c/(2*sy.I), -3: -c/(2*sy.I)}
        R = convolve(cos2, P)
        pnorm2 = sy.simplify(sum(value*sy.conjugate(value) for value in P.values()))
        rnorm2 = sy.simplify(sum(m**4*value*sy.conjugate(value) for m, value in R.items()))
        def mpq(z):
            return mp.mpf(int(z.p))/int(z.q)
        aa, bb, cc = map(mpq, (a, b, c))
        def pp(t):
            return 1+aa*mp.sin(t)+bb*mp.cos(2*t)+cc*mp.sin(3*t)
        def rr2(t):
            pv = pp(t)
            pd = aa*mp.cos(t)-2*bb*mp.sin(2*t)+3*cc*mp.cos(3*t)
            pdd = -aa*mp.sin(t)-4*bb*mp.cos(2*t)-9*cc*mp.sin(3*t)
            return -2*mp.cos(2*t)*pv-2*mp.sin(2*t)*pd+mp.cos(t)**2*pdd
        cuts = [j*mp.pi/2 for j in range(5)]
        pquad = mp.quad(lambda t: pp(t)**2, cuts)/(2*mp.pi)
        rquad = mp.quad(lambda t: rr2(t)**2, cuts)/(2*mp.pi)
        small(ch, 'Fourier_exact_vs_quad_P_'+str(number), abs(pquad-mpq(pnorm2))/(1+abs(pquad)))
        small(ch, 'Fourier_exact_vs_quad_Rsecond_'+str(number), abs(rquad-mpq(rnorm2))/(1+abs(rquad)))
        ratio = mp.sqrt(mpq(pnorm2)/mpq(rnorm2))
        ch.add('whole_circle_bound_control_'+str(number), ratio < mp.pi**2/3, mp.nstr(ratio, 70), 'dimensionless ratio < pi^2/3; diagnostic, not proof')
        controls.append(dict(Pnorm2=str(pnorm2), Rsecond_norm2=str(rnorm2), ratio=mp.nstr(ratio, 80)))
    # Weak example: x=u^2 removes its integrable endpoint singularity for an
    # independent quadrature; a finite rate value at the node is NOT assigned.
    alpha = mp.mpf(7)/4
    mean_power = lambda a: mp.gamma((a+1)/2)/(mp.sqrt(mp.pi)*mp.gamma((a+2)/2))
    rate2 = mean_power(-mp.mpf(1)/2)
    residual_second2 = alpha**2*((alpha-1)**2*mean_power(2*alpha-4)
                         -2*alpha*(alpha-1)*mean_power(2*alpha-2)+alpha**2*mean_power(2*alpha))
    def weak_rate(u):
        return mp.mpf(2) if u == 0 else 2*u/mp.sqrt(mp.sin(u*u))
    def weak_second(u):
        if u == 0:
            return 2*(alpha*(alpha-1))**2
        x = u*u
        value = alpha*((alpha-1)*mp.sin(x)**(alpha-2)-alpha*mp.sin(x)**alpha)
        return 2*u*value*value
    endpoint = mp.sqrt(mp.pi/2)
    qrate = 2*mp.quad(weak_rate, [0, endpoint])/mp.pi
    qsecond = 2*mp.quad(weak_second, [0, endpoint])/mp.pi
    small(ch, 'weak_unbounded_rate_beta_vs_quad', abs(qrate-rate2)/(1+abs(rate2)))
    small(ch, 'weak_H2_residual_beta_vs_quad', abs(qsecond-residual_second2)/(1+abs(residual_second2)))
    ch.add('weak_example_whole_circle_bound', mp.sqrt(rate2/residual_second2) < mp.pi**2/3)
    return dict(Fourier=controls, weak_example=dict(alpha='7/4', rate_L2_square=mp.nstr(rate2, 80),
                residual_second_L2_square=mp.nstr(residual_second2, 80), node_rate_value='UNBOUNDED_NOT_ASSIGNED',
                quadrature='independent control, not outward interval proof'))


def smooth_direction(raw):
    n = raw['n']; v = descriptor.zeros(n)
    for i, t in enumerate(raw['theta']):
        for j in range(10):
            v['Q'][i][j] = (mp.sin((j+1)*t)+mp.cos((j+2)*t))/(j+17)
            v['P'][i][j] = (mp.cos((j+1)*t)-mp.sin((j+2)*t))/(j+19)
        v['Q'][i][4] = 1+mp.cos(2*t)/7
        v['Q'][i][10] = 1+mp.cos(3*t)/11
        v['Q'][i][11] = 1+mp.sin(2*t)/13
    v['M'] = [mp.mpf(1)/17, -mp.mpf(1)/19, mp.mpf(1)/13]
    v['PM'] = [-mp.mpf(1)/23, mp.mpf(1)/29, mp.mpf(1)/31]
    return descriptor.project(v, raw)


def grid_job(task):
    index, point, initial, n, offset = task; ch = base.Checks()
    try:
        raw, X = body.build_data(point, initial, n, offset, 100)
        v = smooth_direction(raw)
        cov = descriptor.omega(X, raw, v)
        p, b = raw['rate'], raw['par']['b']
        rQ = [[n*x for x in row[:10]] for row in cov['Q']]
        rP = [[n*x for x in row] for row in cov['P']]
        rs = [n*row[11] for row in cov['Q']]; rz = [n*row[10] for row in cov['Q']]
        w = [row[7] for row in raw['q']]; g = [b*x*x for x in w]
        B = [p*b*(w[i]**2*(rP[i][0]/2+3*rP[i][2]/2+cov['PM'][2]/2)+2*w[i]*rP[i][4]) for i in range(n)]
        za = [None if g[i] == 0 else -rs[i]/g[i] for i in range(n)]
        sa = [None if g[i] == 0 else (rz[i]-B[i])/g[i] for i in range(n)]
        # At exact nodes the B coefficients vanish. Form B^*vZ through products,
        # never by inventing auxiliary rate values at the nodes.
        adj = [[mp.mpf(0)]*10 for _ in range(n)]
        mean_adj = mp.mpf(0)
        for i in range(n):
            if za[i] is not None:
                adj[i][0] = p*b*w[i]**2*za[i]/2
                adj[i][2] = 3*p*b*w[i]**2*za[i]/2
                adj[i][4] = 2*p*b*w[i]*za[i]
                mean_adj += p*b*w[i]**2*za[i]/(2*n)
        sine = raw['sine']; coefficient = body.mean([sine[i]*adj[i][4] for i in range(n)])/body.mean([x*x for x in sine])
        for i in range(n):
            adj[i][4] -= coefficient*sine[i]
        canonical_error = max(abs(rP[i][j]-v['Q'][i][j])/(1+abs(v['Q'][i][j])) for i in range(n) for j in range(10))
        canonical_error = max(canonical_error, max(abs(-rQ[i][j]-adj[i][j]-v['P'][i][j])/(1+abs(v['P'][i][j])) for i in range(n) for j in range(10)))
        canonical_error = max(canonical_error, max(abs(cov['PM'][j]-v['M'][j]) for j in range(3)),
                              max(abs(-cov['M'][j]-(mean_adj if j == 2 else 0)-v['PM'][j]) for j in range(3)))
        small(ch, 'original_full_two_form_canonical_inverse_with_means', canonical_error)
        auxiliary_error = max(max(abs(za[i]-v['Q'][i][10])/(1+abs(v['Q'][i][10])), abs(sa[i]-v['Q'][i][11])/(1+abs(v['Q'][i][11])))
                              for i in range(n) if g[i] != 0)
        small(ch, 'regular_auxiliary_inverse_no_exact_node_division', auxiliary_error)
        ch.add('exact_node_auxiliary_values_not_invented', sum(x is None for x in za) == sum(x is None for x in sa) == 1)
        # Check the TRUE adjoint, including translation projection and mean L.
        lhs = body.mean([B[i]*v['Q'][i][10] for i in range(n)])
        rhs = body.mean([sum(adj[i][j]*rP[i][j] for j in range(10)) for i in range(n)])+mean_adj*cov['PM'][2]
        small(ch, 'B_adjoint_retains_projection_and_mean_integral', abs(lhs-rhs)/(1+abs(lhs)+abs(rhs)))
        raw_error = max(abs(rz[i]/g[i]-v['Q'][i][11]) for i in range(n) if g[i] != 0)
        ch.add('deleting_cross_changes_auxiliary_reconstruction', raw_error > mp.mpf('1e-20'), mp.nstr(raw_error, 70), 'nonzero omission control')
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset,
                      canonical_error=mp.nstr(canonical_error, 70), auxiliary_error=mp.nstr(auxiliary_error, 70),
                      adjoint_error=mp.nstr(abs(lhs-rhs), 70), omitted_cross_error=mp.nstr(raw_error, 70),
                      regular_Z_rates=[None if x is None else mp.nstr(x, 105) for x in za],
                      regular_s_rates=[None if x is None else mp.nstr(x, 105) for x in sa],
                      node_auxiliary_values='NOT_ASSIGNED; analytic constructed-residual traces are separate controls',
                      meaning='finite-grid action identity only; finite nodal matrices retain their null rows, not an injective discrete inverse',
                      full_K_image_tested=False, physical_domain_admitted=False, state_adopted_or_evolved=False)
    except Exception:
        ch.add('unexpected_grid_exception', False, traceback.format_exc())
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset, incomplete=True)
    return (index, n, offset), result, ch.rows


def calculate(workers):
    mp.mp.dps = 100; before = sources(); ch = base.Checks()
    formulas = exact(ch); controls = analytic_controls(ch)
    points = body.lift.READ(body.nodal.reg.JOINT+'independent.json'); initial = body.lift.READ(body.lift.cop.CERTS)
    if len(points) != 9 or len(initial) != 9 or any(a['family'] != b['family'] or a['eta'] != b['eta'] for a, b in zip(points, initial)):
        raise ValueError('registered case ordering changed')
    tasks = [(i, a, b, n, o) for i, (a, b) in enumerate(zip(points, initial)) for n in (17, 25, 33) for o in (0, 1)]
    progress('FULL_TWO_FORM_DOMAIN_CONTROLS', tasks=len(tasks), workers=workers)
    results = {}
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
    ch.add('all_registered_cases_grids_orientations_completed', len(payload) == 54 and not any(r.get('incomplete') for r in payload))
    if sources() != before:
        raise ValueError('source/native metadata changed during execution')
    failed = [r for r in ch.rows if not r['passed']]
    summary = dict(validation='TWO_FORM_GRAPH_DOMAIN_VERIFIED' if not failed else 'TWO_NODE_GRAPH_DOMAIN_UNRESOLVED',
        passed=len(ch.rows)-len(failed), total=len(ch.rows), failed_checks=failed, unknown_checks=[], checks=ch.rows,
        source_metadata=before, two_form_inverse_domain_derived=True, full_generator_domain_closed=False,
        K_image_admitted=False, domain_invariance_proved=False, positive_physical_energy_derived=False,
        physical_ghost_or_instability_proved=False, physical_frequency_window_established=False,
        physical_cutoff_derived=False, healthy_GR_proved=False, state_adopted_or_evolved=False,
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False, review_status='DEFERRED',
        stage2_complete=False, stage3_entered=False, MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED',
        UVIR_003='IN_PROGRESS', Stage4A='CLOSED', TOP_X4='UNCHANGED', complete372_spectrum=False)
    return summary, dict(analytic_controls=controls, cases=payload), formulas


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
        ch = base.Checks(); exact(ch)
        failures = [r for r in ch.rows if not r['passed']]
        progress('EXACT_METHOD_PREFLIGHT_ONLY', passed=len(ch.rows)-len(failures), total=len(ch.rows), failures=failures)
        raise SystemExit(bool(failures))
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
        raise ValueError('unexpected receipt file set')
    progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
             passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    raise SystemExit(bool(summary['failed_checks']))


if __name__ == '__main__':
    multiprocessing.freeze_support(); main()
