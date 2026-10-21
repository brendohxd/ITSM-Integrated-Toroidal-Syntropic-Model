"""Full frozen weak descriptor and maximal graph; not physical evolution admission."""
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
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_WEAK_GENERATOR_REALIZATION_V1_CONTRACT_2026-10-21.md'
CSHA = '9aab26ec3f9e30909ff14e246f540bd8ab5301c14a090c9395c99acecac2c196'
GRAPH = 'Analysis/MasterTests/test_01_r4c1_two_node_graph_domain_v1.py'
GSHA = '193780d9ef812d919ae40a21a39410648aaee6e54b0b51d0cd818efc9d1e53fc'
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
TOL = '1e-20'
STEPS = ('1e-24', '1e-28')

if SHA((ROOT/GRAPH).read_bytes()) != GSHA:
    raise ValueError('frozen graph source drift')
spec = importlib.util.spec_from_file_location('weak_generator_graph_parent', ROOT/GRAPH)
graph = importlib.util.module_from_spec(spec); spec.loader.exec_module(graph)
descriptor, body, base = graph.descriptor, graph.body, graph.base


def progress(stage, **values):
    print(json.dumps(dict(stage=stage, **values), sort_keys=True), flush=True)


def sources():
    meta = graph.sources()
    additional = {GRAPH: GSHA, CONTRACT: CSHA, SELF: SHA((ROOT/SELF).read_bytes()),
        'Theory/Core/ITSM_FOCUSED_ROUTE_ASSESSMENT_EXECUTION_2026-10-21.md':
        '0b209aba477fe49ffab201098a1f5450bcdf685cceeaaacf7140be5b90fefdfa',
        'Theory/Gates/RES-001/RES001_R4C1_TWO_NODE_GRAPH_DOMAIN_V1_REPORT_2026-10-21.md':
        'dfcb4fe7023924c1665ebc2e2fa37beb5d218c1f37358c209717c448421f82d0',
        'Analysis/MasterTests/outputs/r4c1_two_node_graph_domain_v1_attempt_01/summary.json':
        'd01dcf6489222e65cb94a9e530bec930f8fada5d10d346797dbc8c1955c5272a',
        'Analysis/MasterTests/outputs/r4c1_two_node_graph_domain_v1_attempt_01/independent.json':
        '6ddcee256b8a67f8da70a6d827e6d4013097eb859d5bb29a1553cfa016d391bc',
        'Analysis/MasterTests/outputs/r4c1_two_node_graph_domain_v1_attempt_01/formulas.json':
        '76a3ec7cb1f8a2851f506320bf948f8e29ec03e929b492934c9c9829ac75b61a'}
    for name, want in additional.items():
        p = ROOT/name; side = Path(str(p)+'.sha256')
        if SHA(p.read_bytes()) != want or side.read_text().split()[0].lower() != want:
            raise ValueError('source/sidecar drift: '+name)
        meta['pins'][name] = want
        meta['records'][name] = base.metadata(p)
        meta['records'][side.relative_to(ROOT).as_posix()] = base.metadata(side)
    return meta


def small(ch, name, error, criterion=TOL):
    threshold = mp.mpf(criterion)
    ch.add(name, error < threshold, mp.nstr(error, 70), 'normalized < '+mp.nstr(threshold, 10))


def exact(ch):
    x, s = sy.symbols('x s', real=True, nonzero=True)
    yy = sy.Matrix(sy.symbols('y0:2', real=True))
    R = sy.Matrix([[2+x*x, x/3], [x/3, 3+s*s]])
    ell = sy.Matrix([s*x, x*x-s]); P = sy.Matrix([5+x*s, 7+x*x])
    f = x**3+s*s/5
    L = (yy.T*R*yy)[0]/2+ell.dot(yy)+f
    y = R.inv()*(P-ell)
    true = ((P-ell).dot(y)/2-f)/s
    envelope = (P.dot(yy)-L)/s
    T = P.jacobian([x, s])-(R*yy+ell).jacobian([x, s])
    replacement = dict(zip(yy, y))
    correction = (T.T*R.inv()*T/s).subs(replacement)
    difference = sy.hessian(true, (x, s))-sy.hessian(envelope, (x, s)).subs(replacement)
    ch.add('generic_clock_weighted_Legendre_response_identity',
           all(sy.cancel(z) == 0 for z in difference-correction))
    ch.add('nonlinear_source_pullback_not_silently_affine', sy.diff(P[0], x, s) == 1)
    ch.add('frozen_velocity_shortcut_is_not_the_full_Hessian',
           any(sy.cancel(z.subs({x: sy.Rational(1, 2), s: 2})) != 0 for z in correction))
    # Full clock/flux mixed variation at a constant positive background clock.
    a, b, p, u, v, up, vp = sy.symbols('a b p u v up vp')
    h0, hu, hv, huv, F0, Fu, Fv = sy.symbols('h0 hu hv huv F0 Fu Fv')
    clock = p+a*u+b*v
    density = (h0+a*hu+b*hv+a*b*huv)/clock+(F0+a*Fu+b*Fv)*(a*up+b*vp)/clock**2
    got = sy.diff(density, a, b).subs({a: 0, b: 0})
    want = huv/p-(hu*v+hv*u)/p**2+2*h0*u*v/p**3+(Fu*vp+Fv*up)/p**2-2*F0*(u*vp+v*up)/p**3
    ch.add('clock_flux_second_variation_exact', sy.cancel(got-want) == 0)
    ch.add('nonzero_background_flux_cannot_be_deleted', sy.diff(want, F0) != 0)
    # Laurent polynomial proof, not a numerical trigonometric limit.
    z = sy.Symbol('z', nonzero=True)
    sine = (z-z**-1)/(2*sy.I)
    cosine = (z+z**-1)/2
    c2 = (z*z+z**-2)/2
    for j in range(1, 13):
        harmonic = (z**(2*j)-z**(-2*j))/(2*sy.I)
        ch.add('exact_even_shift_harmonic_'+str(j),
               sy.cancel(harmonic-2*sine*cosine*sy.chebyshevu(j-1, c2)) == 0)
        ch.add('both_node_shift_quotient_limit_'+str(j),
               -2*sy.chebyshevu(j-1, -1) == 2*j*(-1)**j)
    # Inverse primitive commutators, including the actual mean term.
    aa = 1+(z*z+z**-2)/7
    ff = 2+(z**3-z**-3)/(2*sy.I)+(z+z**-1)/5
    def modes(expr):
        result = {}
        for term in sy.Add.make_args(sy.expand(expr)):
            m = int(term.as_powers_dict().get(z, 0))
            result[m] = result.get(m, sy.Integer(0))+term/z**m
        return result
    def differentiate(expr):
        return sy.expand(sy.I*z*sy.diff(expr, z))
    def primitive(expr):
        return sy.expand(sum(c*z**m/(sy.I*m) for m, c in modes(expr).items() if m))
    def average(expr):
        return sy.expand(expr).coeff(z, 0)
    primitive_difference = primitive(aa*differentiate(ff))-aa*ff+average(aa*ff)+primitive(differentiate(aa)*ff)
    ch.add('inverse_primitive_product_commutator_with_mean', sy.expand(primitive_difference) == 0)
    ch.add('inverse_primitive_derivative_quotient_identity', sy.expand(primitive(differentiate(ff))-ff+average(ff)) == 0)
    ch.add('mean_omission_is_detected', average(aa*ff) != 0)
    return dict(
        partial_Legendre='delta2 E[u,v]=delta2(E_envelope_at_fixed_y)[u,v]+T_u^T Rcal^-1 T_v; T=delta P_y-delta(volume*L_y)|fixed_y',
        clock_correction='In H=<E/s-F*D(1/s)>, add <T_u^T Rcal^-1 T_v/p> at s=p; volume and full constraint pullback retained',
        clock_flux_mixed=str(want),
        shift='R=sum_j c_j sin(2j theta); R*wprime/w=-2*k*sin(theta)^2*sum_j c_j U_(j-1)(cos(2theta)); limit at BOTH nodes equals Rprime',
        shift_bound='abs(R*wprime/w)<=2*k*sum_j j*abs(c_j), j1..12; reference chart, not a physical cutoff',
        primitive='I(a*D f)=a*f-mean(a*f)-I((D a)*f); I*D=Id-P0',
        actual_K='Hessian(full constrained clock Hamiltonian)-dOmega[u]*registered_background_rate',
        weak_order='Sector-by-sector analytic argument in owning report: frozen K extends H=L2 sections plus means to H^-2 sections plus mean duals, fixed eta>0 only',
        maximal_domain='D(Amax)={u in H: exists v in H, K*u=Omega*v in H^-2}; uniqueness from injective full Omega',
        graph_limit='u_j->u and Amax*u_j->v in H imply K*u_j->K*u and Omega*Amax*u_j->Omega*v in H^-2, hence K*u=Omega*v and u in D(Amax)',
        equivalence='D(Amax)={u in H: K*u in H and K*u in Yg}; actual cross-corrected two-node quotients, not arbitrary raw scalar rows',
        not_proved=['dense D(Amax)', 'resolvent/semigroup', 'domain invariance', 'physical constraint admission',
                    'physical positive energy', 'physical modes/cutoff', 'healthy GR', 'numerical matching'])


def cheby_u(j, x):
    a, b = mp.mpf(1), 2*x
    if j == 0:
        return a
    for _ in range(1, j):
        a, b = b, 2*x*b-a
    return b


def shift_controls(ch, point, initial):
    _, _, _, _, _, _, original = body.lift.setup(point, initial)
    closure = dict(zip(original.__code__.co_freevars, (cell.cell_contents for cell in original.__closure__)))
    coeff, k = closure['coeff'], closure['k']
    if closure['modes'] != 12 or len(coeff) != 12:
        raise ValueError('registered Galerkin harmonic set changed')
    sample = [2*mp.pi*i/65 for i in range(65)]
    values = [original(t)[0] for t in sample]
    recovered = [2*body.mean([v*mp.sin(2*j*t) for v, t in zip(values, sample)]) for j in range(1, 13)]
    fourier_error = max(abs(a-b)/(1+abs(a)+abs(b)) for a, b in zip(coeff, recovered))
    small(ch, 'original_shift_independent_65_sample_Fourier_coefficients', fourier_error, mp.mpf('1e-50'))
    bound = 2*k*sum((j+1)*abs(c) for j, c in enumerate(coeff))
    errors = []
    for node in (mp.pi/2, 3*mp.pi/2):
        exact_limit = 2*k*sum((j+1)*(-1)**(j+1)*c for j, c in enumerate(coeff))
        small(ch, 'actual_shift_removable_node_limit_'+mp.nstr(node, 8),
              abs(original(node)[1]-exact_limit)/(1+abs(exact_limit)), mp.mpf('1e-50'))
        for delta in ('-1e-20', '1e-20', '-0.013', '0.017'):
            t = node+mp.mpf(delta)
            direct = -k*original(t)[0]*mp.sin(t)/mp.cos(t)
            regular = -2*k*mp.sin(t)**2*sum(c*cheby_u(j, mp.cos(2*t)) for j, c in enumerate(coeff))
            errors.append(abs(direct-regular)/(1+abs(direct)+abs(regular)))
            if abs(regular) > bound+mp.mpf('1e-70'):
                raise ValueError('proved shift coefficient bound violated')
    small(ch, 'actual_shift_near_both_nodes_regular_formula', max(errors), mp.mpf('1e-50'))
    # Independent analytic antiderivative and quadrature with a nonzero mean.
    a = lambda t: 2+mp.cos(2*t)/3
    fp = lambda t: 3*mp.cos(3*t)-mp.sin(t)/5
    f = lambda t: 1+mp.sin(3*t)+mp.cos(t)/5
    mean_product = mp.quad(lambda t: a(t)*f(t), [0, mp.pi, 2*mp.pi])/(2*mp.pi)
    small(ch, 'quadrature_keeps_inverse_primitive_mean', abs(mean_product-2), mp.mpf('1e-50'))
    integral = mp.quad(lambda t: a(t)*fp(t), [0, mp.pi, 2*mp.pi])
    small(ch, 'periodic_product_derivative_zero_mean_control', abs(integral), mp.mpf('1e-50'))
    return dict(coefficients=[mp.nstr(c, 105) for c in coeff],
                Fourier_error=mp.nstr(fourier_error, 70), near_node_error=mp.nstr(max(errors), 70),
                shift_quotient_bound=mp.nstr(bound, 105),
                meaning='actual original finite Galerkin profile; no background adoption or evolution')


def directions(raw):
    result = []
    for frequency in (1, (raw['n']-3)//2):
        v = descriptor.zeros(raw['n'])
        for i, t in enumerate(raw['theta']):
            for j in range(12):
                v['Q'][i][j] = (mp.sin(frequency*t)+(j+2)*mp.cos(frequency*t)/17+mp.mpf(1)/7)/(j+31)
            for j in range(10):
                v['P'][i][j] = (mp.cos(frequency*t)-(j+1)*mp.sin(frequency*t)/19+mp.mpf(1)/11)/(j+37)
        v['M'] = [mp.mpf(1)/41, -mp.mpf(1)/43, mp.mpf(1)/47]
        v['PM'] = [-mp.mpf(1)/53, mp.mpf(1)/59, mp.mpf(1)/61]
        result.append(descriptor.project(v, raw))
    return result


def response_bilinear(X, raw, y0, out, u, v, h):
    yu = descriptor.response(body.shifted(X, u, h), raw, y0, out)
    yv = descriptor.response(body.shifted(X, v, h), raw, y0, out)
    du = [[mp.im(a)/h for a in row] for row in yu]
    dv = [[mp.im(a)/h for a in row] for row in yv]
    terms = []
    for i in range(raw['n']):
        volume = body.geometry(out['q'][i], out['dq'][i])[3]
        terms.append(volume*body.dot(du[i], body.mv(raw['Rs'][i], dv[i]))/raw['rate'])
    return body.mean(terms)


def weak_norm(cov, raw):
    n = raw['n']; total = mp.mpf(0)
    fields = body.trans([[n*x for x in r] for r in cov['Q']])+body.trans([[n*x for x in r] for r in cov['P']])
    for field in fields:
        for m in range(-(n//2), n//2+1):
            c = body.mean([value*mp.exp(-1j*m*t) for value, t in zip(field, raw['theta'])])
            total += abs(c)**2/(1+(40*m)**2)**2
    total += sum(abs(x)**2 for x in cov['M']+cov['PM'])
    return mp.sqrt(total)


def nodal_diagnostic(K, raw):
    n, p, b = raw['n'], raw['rate'], raw['par']['b']
    w = [q[7] for q in raw['q']]
    rs = [n*q[11] for q in K['Q']]
    adjusted = [n*K['Q'][i][10]-p*b*(w[i]**2*(n*K['P'][i][0]/2+3*n*K['P'][i][2]/2+K['PM'][2]/2)
                +2*w[i]*n*K['P'][i][4]) for i in range(n)]
    slopes = (body.Dmul(raw['D'], rs)[0], body.Dmul(raw['D'], adjusted)[0])
    return dict(values=[mp.nstr(rs[0], 70), mp.nstr(adjusted[0], 70)],
                spectral_slopes=[mp.nstr(x, 70) for x in slopes],
                meaning='actual full K on generic method data; single sampled-node interpolant diagnostics only, NOT continuum admission')


def grid_job(task):
    index, point, initial, n, offset = task; ch = base.Checks()
    try:
        raw, X = body.build_data(point, initial, n, offset, 100)
        y0, err = body.baseline(raw, X); out = descriptor.functional(X, raw, y0)
        small(ch, 'original_twelve_velocity_stationarity', err)
        T = descriptor.background(X, raw, y0, out)
        u, v = directions(raw); steps = []; previous = None
        for hs in STEPS:
            h = mp.mpf(hs)
            HU = descriptor.hvp(X, raw, y0, out, u, h)
            HV = descriptor.hvp(X, raw, y0, out, v, h)
            frozen = descriptor.hvp(X, raw, y0, out, v, h, frozen=True)
            DU = descriptor.drift(X, raw, u, T, h)
            DV = descriptor.drift(X, raw, v, T, h)
            KU, KV = descriptor.combine(HU, DU, -1), descriptor.combine(HV, DV, -1)
            actual = body.dot_chart(u, descriptor.combine(HV, frozen, -1))
            expected = response_bilinear(X, raw, y0, out, u, v, h)
            error = abs(actual-expected)/(1+abs(actual)+abs(expected))
            small(ch, 'full_original_Hessian_response_factorization_'+hs, error)
            symmetry = abs(body.dot_chart(u, HV)-body.dot_chart(v, HU))/(1+abs(body.dot_chart(u, HV))+abs(body.dot_chart(v, HU)))
            small(ch, 'all_sector_Hessian_symmetry_'+hs, symmetry)
            drift_size = max(descriptor.norm(DU), descriptor.norm(DV))
            ch.add('background_drift_omission_rejected_'+hs, drift_size > mp.mpf('1e-30'), mp.nstr(drift_size, 70))
            ch.add('implicit_velocity_omission_rejected_'+hs, descriptor.norm(descriptor.combine(HV, frozen, -1)) > mp.mpf('1e-30'))
            if previous is not None:
                small(ch, 'two_step_full_K_agreement', max(descriptor.relative(a, b) for a, b in zip((KU, KV), previous)))
            previous = KU, KV
            steps.append(dict(step=hs, response_bilinear=mp.nstr(expected, 105), response_error=mp.nstr(error, 70),
                Hessian_symmetry_error=mp.nstr(symmetry, 70), drift_norm=mp.nstr(drift_size, 70),
                weak_Hminus2_norms=[mp.nstr(weak_norm(k, raw), 105) for k in (KU, KV)],
                node_forcing=[nodal_diagnostic(k, raw) for k in (KU, KV)]))
        mixed = descriptor.mixed_control(ch, X, raw, y0, u, v, HV) if n == 17 and offset == 0 else None
        shift = shift_controls(ch, point, initial) if n == 17 and offset == 0 else None
        curvature = descriptor.curvature_controls(ch, raw)
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset, steps=steps,
            independent_mixed=mixed, shift=shift, full_Ricci_error=mp.nstr(curvature, 70),
            method_data_physical_admission='NOT_ASSERTED', physical_state_adopted_or_evolved=False,
            norm_weights='Normalized Fourier L2 covectors, field rows multiplied by n; squared H^-2 weight (1+(40*m)^2)^-2; means unweighted')
    except Exception:
        ch.add('unexpected_grid_exception', False, traceback.format_exc())
        result = dict(family=point['family'], eta=point['eta'], grid=n, node_orientation=offset, incomplete=True)
    return (index, n, offset), result, ch.rows


def calculate(workers):
    mp.mp.dps = 100; before = sources(); ch = base.Checks(); formulas = exact(ch)
    points = body.lift.READ(body.nodal.reg.JOINT+'independent.json')
    initial = body.lift.READ(body.lift.cop.CERTS)
    if len(points) != 9 or len(initial) != 9 or any(a['family'] != b['family'] or a['eta'] != b['eta'] for a, b in zip(points, initial)):
        raise ValueError('registered case order changed')
    tasks = [(i, a, b, n, o) for i, (a, b) in enumerate(zip(points, initial)) for n in (17, 25, 33) for o in (0, 1)]
    progress('FULL_WEAK_DESCRIPTOR_CONTROLS', tasks=len(tasks), workers=workers)
    results = {}
    if workers == 1:
        for task in tasks:
            key, result, rows = grid_job(task); results[key] = result, rows
            progress('GRID_FINISHED', key=key, passed=sum(row['passed'] for row in rows), total=len(rows))
    else:
        with ProcessPoolExecutor(max_workers=workers, mp_context=multiprocessing.get_context('spawn')) as pool:
            futures = [pool.submit(grid_job, task) for task in tasks]
            for future in as_completed(futures):
                key, result, rows = future.result(); results[key] = result, rows
                progress('GRID_FINISHED', key=key, passed=sum(row['passed'] for row in rows), total=len(rows))
    records = []
    for key in sorted(results):
        record, rows = results[key]; records.append(record)
        for row in rows:
            ch.add(str(key)+'_'+row['name'], row['passed'], row.get('value'), row.get('criterion'))
    ch.add('all_registered_cases_grids_orientations_complete', len(records) == 54 and not any(r.get('incomplete') for r in records))
    if sources() != before:
        raise ValueError('source/native metadata drift during execution')
    failed = [row for row in ch.rows if not row['passed']]
    summary = dict(validation='FULL_WEAK_DESCRIPTOR_IDENTITIES_VERIFIED' if not failed else 'WEAK_DESCRIPTOR_UNRESOLVED',
        passed=len(ch.rows)-len(failed), total=len(ch.rows), failed_checks=failed, unknown_checks=[], checks=ch.rows,
        source_metadata=before, analytic_maximal_graph_scope='Frozen coefficients, weak H^-2 realization; owning report supplies analytic sector proof',
        physical_admission_proved=False, dense_generator_domain_proved=False, domain_invariance_proved=False,
        evolution_or_semigroup_proved=False, positive_physical_energy_derived=False,
        physical_cutoff_derived=False, physical_frequency_window_established=False, healthy_GR_proved=False,
        state_adopted_or_evolved=False, stage2_complete=False, stage3_entered=False,
        physics_pass=False, gate_effect='NONE', Rule9_cleared=False, review_status='DEFERRED',
        MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED', UVIR_003='IN_PROGRESS', Stage4A='CLOSED', TOP_X4='UNCHANGED')
    return summary, dict(cases=records), formulas


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
        failures = [row for row in ch.rows if not row['passed']]
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
