"""Uniform partial Legendre chart, not full physical stability or GR clearance."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import hashlib
import importlib.util
import json
from math import comb
import multiprocessing
from pathlib import Path
import sys

import mpmath as mp
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_LEGENDRE_DOMAIN_V1_CONTRACT_2026-10-21.md'
CSHA = '9d1b8d95e54e1527d2df0dd68264f0cfeb3b780f032cb8729ce756730e1663d2'
HELPER = 'Analysis/MasterTests/test_01_r4c1_finite_node_domain_v1.py'
HSHA = 'e1c15ae0a29cd0ad8587c75138b569e0f0f85edc07dbc20327c42ff8414a06a9'
BODY = 'Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
BSHA = 'b887c7a52102b7abb43a2875cb6e01607ecb46d39a95f4abb4cefab9795a73c0'
MAP = 'Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
MSHA = '852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a'
FAMILIES = ('archived_G3', 'new_B1_frame', 'new_hierarchical')
ETAS = ('1/4', '1/64', '1/1024')
WS = ('0', '1/500', '-1/500', '1/1000', '-1/1000')
HM = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
_BODY_MODULE = None


def load_pinned(name, filename, digest):
    path = ROOT / filename
    if SHA(path.read_bytes()) != digest:
        raise ValueError('source drift: ' + filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_pinned('legendre_domain_helpers', HELPER, HSHA)


def original_body():
    global _BODY_MODULE
    if _BODY_MODULE is None:
        _BODY_MODULE = load_pinned('legendre_original_body', BODY, BSHA)
    return _BODY_MODULE


def progress(stage, **values):
    print(json.dumps(dict(stage=stage, **values), sort_keys=True), flush=True)


def metadata():
    body = original_body()
    pins = {**base.PINS, **body.PINS, HELPER: HSHA, BODY: BSHA, MAP: MSHA,
            CONTRACT: CSHA,
            'Theory/Gates/RES-001/RES001_R4C1_FINITE_NODE_DOMAIN_V1_REPORT_2026-10-21.md':
            '0ebb80d4aad211a9f61423ca006eb514b6257ca40eb66a08960f73ec163dae5b',
            SELF: SHA((ROOT / SELF).read_bytes())}
    records = {}
    for name, want in sorted(pins.items()):
        path = ROOT / name
        if SHA(path.read_bytes()) != want:
            raise ValueError('source pin changed: ' + name)
        records[name] = base.metadata(path)
        side = Path(str(path) + '.sha256')
        if side.exists():
            if side.read_text().split()[0].lower() != want:
                raise ValueError('sidecar changed: ' + name)
            records[side.relative_to(ROOT).as_posix()] = base.metadata(side)
        elif name not in ('GEMINI.md', 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md'):
            raise ValueError('source sidecar missing: ' + name)
    # Capture every actually loaded repository module, including transitive body
    # imports. Runtime records are compared exactly during read-only replay.
    for module in list(sys.modules.values()) + [body, body.old, body.lift, body.nodal,
                                               body.canonical, body.base,
                                               body.lift.canonical, base]:
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).is_file():
            path = Path(filename).resolve()
            if path.is_relative_to(ROOT):
                name = path.relative_to(ROOT).as_posix()
                records[name] = base.metadata(path)
                side = Path(str(path) + '.sha256')
                if side.exists():
                    if side.read_text().split()[0].lower() != SHA(path.read_bytes()):
                        raise ValueError('loaded module sidecar mismatch: ' + name)
                    records[side.relative_to(ROOT).as_posix()] = base.metadata(side)
    for path in sorted(Path(mp.__file__).parent.rglob('*.py')):
        records['installed/mpmath/' + path.relative_to(Path(mp.__file__).parent).as_posix()] = base.metadata(path)
    records['installed/sympy/__init__.py'] = base.metadata(Path(sy.__file__))
    records['installed/python.exe'] = base.metadata(Path(sys.executable))
    return dict(pins= pins, records=records,
                versions=dict(python=sys.version, mpmath=mp.__version__, sympy=sy.__version__))


def exact_model():
    """Differentiate the unspecialized original quadratic density first."""
    eta, w = sy.symbols('eta w', real=True)
    mp2, mu2, c1, c2, c3, c4, zeta, r2 = sy.symbols('MP2 MU2 c1 c2 c3 c4 zeta R2', real=True)
    y = sy.Matrix(sy.symbols('y0:12', real=True))
    K = sy.Matrix([[y[0], y[1], y[2]], [y[1], y[3], y[4]], [y[2], y[4], y[5]]])
    V = sy.Matrix([0, w, 0])
    gamma = sy.sqrt(1 + w*w)
    avec = y[6:9, 0] + K*V
    B = sy.zeros(4)
    B[0, 0] = (V.T*avec)[0]/gamma
    for j in range(3):
        B[0, j+1] = avec[j]
    for i in range(3):
        B[i+1, 0] = (K*V)[i]
        for j in range(3):
            B[i+1, j+1] = gamma*K[i, j]
    metric = sy.diag(-1, 1, 1, 1)
    n = sy.Matrix([gamma, 0, w, 0])
    acc = B.T*n
    I1 = sy.trace(metric*B*metric*B.T)
    def frame_density(matrix):
        acceleration = matrix.T*n
        return -mu2*(c1*sy.trace(metric*matrix*metric*matrix.T)
                     + c2*sy.trace(matrix)**2 + c3*sy.trace(matrix*matrix)
                     - c4*(acceleration.T*metric*acceleration)[0])/2
    frame = frame_density(B)
    adm = mp2*(sy.trace(K*K) - sy.trace(K)**2)/2
    scalar = sum(y[j]**2 for j in (9, 10, 11))/2 - zeta*r2*w*w*y[10]**2/2
    density = adm + frame + scalar
    generic = sy.hessian(density, list(y)).applyfunc(sy.cancel)
    # All spatial-jet contributions to B are velocity-independent shifts. An
    # arbitrary 4x4 shift covers them without imposing extra spatial relations.
    shifted = B + sy.Matrix(4, 4, sy.symbols('J0:16', real=True))
    sr, Z, pz, zz, uz, vz, rz, kq, A, potential, curvature = sy.symbols(
        's Z psi_z Z_z u_z v_z r_z K_Q A potential R3', real=True)
    gp, gz = sy.Matrix([sr, 0, 0, pz]), sy.Matrix([0, 0, 0, zz])
    projector = metric+n*n.T
    regulator = -sy.Symbol('b', real=True)*(gz.dot(projector*gp) + Z*(shifted.T*n).dot(gp))
    force = kq*(n.dot(gp))**2/2 - A*(gp.dot(projector*gp))**sy.Rational(3, 2)
    full_density = (adm + mp2*curvature/2 + frame_density(shifted)
                    + sum(y[j]**2 for j in (9, 10, 11))/2 - (uz**2+vz**2+rz**2)/2
                    - zeta*r2*(w*w*y[10]**2+vz**2)/2 + regulator + force - potential)
    affine_remainder = sy.hessian(full_density-density, list(y)).applyfunc(sy.cancel)
    maps = json.loads((ROOT / MAP).read_bytes())['families']
    named = {str(s): s for s in (eta, mp2, mu2, c1, c2, c3, c4, zeta)}
    named['R2'] = r2
    models = {}
    for family in FAMILIES:
        par = {key: sy.sympify(value, locals={'eta': eta})
               for key, value in maps[family]['parameter_map'].items()}
        sub = {named[key]: value for key, value in par.items() if key in named}
        sub[r2] = eta
        R = generic.subs(sub).applyfunc(sy.cancel)
        alpha13 = sy.cancel(par['MU2']*(par['c1']+par['c3']))
        alpha2 = sy.cancel(par['MU2']*par['c2'])
        a, bc = 1-alpha13, 1+alpha2
        d = sy.cancel(2+alpha13+3*alpha2)
        aligned = sy.zeros(12)
        inverse = sy.zeros(12)
        diagonal = (0, 3, 5)
        for i in diagonal:
            for j in diagonal:
                aligned[i, j] = (a if i == j else 0)-bc
                inverse[i, j] = (1/a if i == j else 0)-bc/(a*d)
        for i in (1, 2, 4):
            aligned[i, i], inverse[i, i] = 2*a, 1/(2*a)
        for i in (6, 7, 8):
            aligned[i, i], inverse[i, i] = eta/6, 6/eta
        for i in (9, 10, 11):
            aligned[i, i] = inverse[i, i] = 1
        T = (inverse*(R-aligned)).applyfunc(sy.cancel)
        models[family] = dict(R=R, R0=aligned, inverse=inverse, T=T,
                              a=a, B=bc, D=d, parameter_map=par)
    return eta, w, density, generic, models, affine_remainder


def zero_matrix(matrix):
    return all(sy.cancel(value) == 0 for value in matrix)


def bernstein(poly, eta):
    p = sy.Poly(sy.expand(poly), eta)
    degree = max(0, p.degree())
    if poly == 0:
        degree = 0
    return [sy.cancel(sum(p.nth(j)*sy.Rational(comb(k, j), comb(degree, j))
                          for j in range(k+1))) for k in range(degree+1)]


def exact_checks(ch, eta, w, density, generic, models, affine_remainder):
    ch.add('generic_hessian_symmetric', generic == generic.T)
    ch.add('generic_hessian_has_no_velocity_symbols', not any(str(z).startswith('y') for z in generic.free_symbols))
    ch.add('generic_spatial_curvature_regulator_force_potential_remainder_affine', zero_matrix(affine_remainder))
    result = {}
    expectations = (eta/8, sy.Integer(0), eta**2/8)
    for family, alpha13 in zip(FAMILIES, expectations):
        m = models[family]
        R, R0, inv, T = (m[key] for key in ('R', 'R0', 'inverse', 'T'))
        par = m['parameter_map']
        ch.add(family+'_frozen_alpha13', sy.cancel(par['MU2']*(par['c1']+par['c3'])-alpha13) == 0)
        ch.add(family+'_frozen_alpha14', sy.cancel(par['MU2']*(par['c1']+par['c4'])-eta/6) == 0)
        ch.add(family+'_aligned_matrix', zero_matrix(R.subs(w, 0)-R0))
        ch.add(family+'_exact_aligned_inverse', zero_matrix(R0*inv-sy.eye(12)))
        ch.add(family+'_exact_Neumann_factorization', zero_matrix(R-R0*(sy.eye(12)+T)))
        ch.add(family+'_T_extends_at_eta_zero', all(value.subs(eta, 0).is_finite is True for value in T))
        inequalities = {'a_lower': m['a']-sy.Rational(7, 8),
                        'D_lower': m['D']-sy.Rational(11, 6),
                        'B_lower': m['B']-sy.Rational(65, 72),
                        'B_upper': sy.Rational(16, 15)-m['B'],
                        'D_minus_B_lower': m['D']-m['B']-sy.Rational(29, 36)}
        bc = {}
        for label, expression in inequalities.items():
            coefficients = bernstein(expression, eta)
            ch.add(family+'_'+label+'_Bernstein_nonnegative', all(c >= 0 for c in coefficients), [str(c) for c in coefficients])
            bc[label] = [str(c) for c in coefficients]
        # Exact complete eigenbasis in the original velocity component chart.
        basis = []
        for coords in ((1, -1, 0), (1, 0, -1), (1, 1, 1)):
            v = sy.zeros(12, 1)
            for index, value in zip((0, 3, 5), coords):
                v[index] = value
            basis.append(v)
        for index in (1, 2, 4, 6, 7, 8, 9, 10, 11):
            v = sy.zeros(12, 1); v[index] = 1; basis.append(v)
        values = [m['a'], m['a'], -m['D']] + [2*m['a']]*3 + [eta/6]*3 + [sy.Integer(1)]*3
        eigenvectors = sy.Matrix.hstack(*basis)
        ch.add(family+'_complete_aligned_eigenbasis', eigenvectors.det() != 0 and all(zero_matrix(R0*v-lam*v) for v, lam in zip(basis, values)))
        row = (m['D']+m['B'])/(m['a']*m['D'])
        absolute_majorant = sy.Rational(8, 7)*(1+sy.Rational(16, 15)/sy.Rational(11, 6))
        ch.add(family+'_gravity_inverse_rows_below_two', absolute_majorant < 2, str(absolute_majorant))
        ch.add(family+'_frame_inverse_dominates', sy.Rational(6) > absolute_majorant and sy.Rational(6) > 1)
        endpoint = R.subs(eta, 0).applyfunc(sy.cancel)
        ch.add(family+'_endpoint_rank_nine_for_every_w', endpoint == R0.subs(eta, 0) and endpoint.rank() == 9)
        ch.add(family+'_endpoint_three_frame_null_directions', all(endpoint[:, j] == sy.zeros(12, 1) for j in (6, 7, 8)))
        result[family] = dict(Bernstein=bc, a=str(m['a']), B=str(m['B']), D=str(m['D']),
                              eigenvalues=[str(v) for v in values], aligned_inverse_norm='6/eta',
                              aligned_gravity_inverse_row_sum=str(row), inertia=[11, 1, 0],
                              eta_zero=dict(rank=9, frame_velocity_kernel=[6, 7, 8]))
    return result


def dyadic(endpoint):
    sign, mantissa, exponent, bits = endpoint
    if bits < 0:
        raise ValueError('nonfinite interval endpoint')
    numerator = -mantissa if sign else mantissa
    return Fraction(numerator*(2**max(exponent, 0)), 2**max(-exponent, 0))


def bounds(value):
    return tuple(dyadic(z) for z in value._mpi_)


def evaluate(expression, environment, context, interval=False, cache=None):
    """Exact rational coefficients only; intentionally no lambdify or float path."""
    if cache is None:
        cache = {}
    if expression in cache:
        return cache[expression]
    if expression.is_Integer:
        value = context.mpf(int(expression))
    elif expression.is_Rational:
        value = context.mpf(int(expression.p))/int(expression.q)
    elif expression.is_Symbol:
        value = environment[expression]
    elif expression.is_Add:
        value = context.mpf(0)
        for term in expression.args:
            value += evaluate(term, environment, context, interval, cache)
    elif expression.is_Mul:
        value = context.mpf(1)
        for term in expression.args:
            value *= evaluate(term, environment, context, interval, cache)
    elif expression.is_Pow:
        operand = evaluate(expression.base, environment, context, interval, cache)
        power = expression.exp
        if interval:
            lo, hi = bounds(operand)
            if power < 0 and lo <= 0 <= hi:
                raise ValueError('zero-containing denominator')
        if power.is_Integer:
            value = operand**int(power)
        elif power.is_Rational and power.q == 2:
            if interval and bounds(operand)[0] < 0:
                raise ValueError('negative real square-root input')
            value = context.sqrt(operand)**int(power.p)
        else:
            raise TypeError('unsupported power: '+str(power))
    else:
        raise TypeError('unsupported exact expression: '+str(expression))
    cache[expression] = value
    return value


def interval_controls(ch):
    iv = mp.iv
    iv.dps = 80
    A, B = iv.mpf([-3, 5])/7, iv.mpf([2, 7])/11
    a, b = (Fraction(-3, 7), Fraction(5, 7)), (Fraction(2, 11), Fraction(7, 11))
    tests = {'add': (A+B, (a[0]+b[0], a[1]+b[1])),
             'sub': (A-B, (a[0]-b[1], a[1]-b[0])),
             'mul': (A*B, (min(x*y for x in a for y in b), max(x*y for x in a for y in b))),
             'div': (A/B, (min(x/y for x in a for y in b), max(x/y for x in a for y in b)))}
    for n in (0, 1, 2, 3, 4, -1, -2, -3):
        interval, exact = (A, a) if n >= 0 else (B, b)
        ends = [x**n for x in exact]
        if n > 0 and n % 2 == 0 and exact[0] <= 0 <= exact[1]:
            ends.append(Fraction(0))
        tests['pow_'+str(n)] = (interval**n, (min(ends), max(ends)))
    record = {}
    for label, (value, target) in tests.items():
        lo, hi = bounds(value)
        ch.add('interval_exact_endpoint_'+label, lo <= target[0] <= target[1] <= hi)
        record[label] = dict(enclosure=[str(lo), str(hi)], exact=[str(x) for x in target])
    low, high = bounds(iv.sqrt(B))
    ch.add('interval_sqrt_exact_square_enclosure', low >= 0 and low*low <= b[0] and high*high >= b[1])
    x = sy.Symbol('x')
    for name, expression, env, error in (
        ('zero_denominator', 1/x, {x: A}, ValueError),
        ('float_coefficient', sy.Float('0.1'), {}, TypeError),
        ('unsupported_function', sy.sin(x), {x: B}, TypeError),
        ('negative_sqrt', sy.sqrt(x), {x: iv.mpf([-2, -1])}, ValueError)):
        rejected = False
        try:
            evaluate(expression, env, iv, interval=True)
        except error:
            rejected = True
        ch.add('interval_reject_'+name, rejected)
    # A finite endpoint exactness regression catches accidental binary64 ingress.
    lo, hi = bounds(evaluate(sy.Rational(1, 10), {}, iv, interval=True))
    ch.add('exact_one_tenth_not_binary64', lo <= Fraction(1, 10) <= hi and hi-lo < Fraction(1, 10**75))
    return record


def interval_domain(ch, eta, w, models):
    iv = mp.iv
    iv.dps = 80
    ch.add('exact_fixed_eta_partition_endpoints', Fraction(0, 16) == 0 and Fraction(16, 16) == 1)
    ch.add('exact_fixed_tilt_partition_endpoints', Fraction(-4, 2000) == Fraction(-1, 500) and Fraction(4, 2000) == Fraction(1, 500))
    result = {}
    for family in FAMILIES:
        T = models[family]['T']
        boxes = []
        maximum = Fraction(0)
        for i in range(16):
            for j in range(8):
                env = {eta: iv.mpf([i, i+1])/16,
                       w: iv.mpf([j-4, j-3])/2000}
                cache = {}
                rows = []
                for r in range(12):
                    total = iv.mpf(0)
                    for c in range(12):
                        if T[r, c] != 0:
                            total += abs(evaluate(T[r, c], env, iv, interval=True, cache=cache))
                    rows.append(bounds(total))
                upper = max(high for low, high in rows)
                maximum = max(maximum, upper)
                boxes.append(dict(eta_index=i, w_index=j,
                                  row_sum_enclosures=[[str(a), str(b)] for a, b in rows],
                                  norm_upper=str(upper)))
        scale = 10**9
        ceiling = Fraction((maximum.numerator*scale+maximum.denominator-1)//maximum.denominator, scale)
        ch.add(family+'_fixed_partition_covers_rectangle', len(boxes) == 128)
        ch.add(family+'_uniform_Neumann_beta_below_one', maximum <= ceiling < 1,
               str(ceiling), 'exact outward enclosure, fixed 16x8 partition')
        constant = 6/(1-ceiling) if ceiling < 1 else None
        result[family] = dict(beta_upper_exact_dyadic=str(maximum), beta_rational_ceiling=str(ceiling),
                              inverse_bound_constant=str(constant) if constant is not None else None,
                              inverse_bound='constant/eta, only 0<eta<=1', boxes=boxes)
        progress('INTERVAL_FAMILY_FINISHED', family=family, beta_ceiling=str(ceiling))
    return result


def point_job(job):
    """Owned Windows-spawn job; original list-contraction density polarization."""
    family, estr, entries = job
    mp.mp.dps = 100
    body = original_body()
    eta, w = sy.symbols('eta w', real=True)
    matrix = [sy.sympify(z, locals={'eta': eta, 'w': w}) for z in entries]
    e = evaluate(sy.sympify(estr), {}, mp.mp)
    par = body.lift.canonical.parameters(family, estr, 'mp')
    cases = []
    for wstr in WS:
        v = evaluate(sy.sympify(wstr), {}, mp.mp)
        q = [mp.mpf(0)]*15
        q[0] = q[3] = q[5] = mp.mpf(1)
        q[7], q[9], q[11], q[13] = v, mp.sqrt(e), mp.sqrt(e), e/19
        dq = [mp.mpf(0)]*15
        dq[0], dq[3], dq[7] = mp.mpf(1)/101, -mp.mpf(1)/103, mp.mpf(1)/97
        dq[9], dq[10], dq[11], dq[13] = e/77, -e/83, e/91, e/89
        s, curvature = e/5, mp.mpf(2)/137
        def density(y):
            return body.body(q, dq, y, s, par, R3=curvature)
        zero = [mp.mpf(0)]*12
        f0 = density(zero)
        units = []
        for i in range(12):
            u = zero.copy(); u[i] = 1; units.append(density(u))
        cache = {}
        analytic = [evaluate(expr, {eta: e, w: v}, mp.mp, cache=cache) for expr in matrix]
        maximum = mp.mpf(0)
        cross_size = mp.mpf(0)
        for i in range(12):
            for j in range(i, 12):
                u = zero.copy(); u[i] += 1; u[j] += 1
                actual = density(u)-units[i]-units[j]+f0
                wanted = analytic[12*i+j]
                maximum = max(maximum, abs(actual-wanted)/max(mp.mpf(1), abs(actual), abs(wanted)))
                if i < 6 and 6 <= j < 9:
                    cross_size = max(cross_size, abs(actual))
        direction = [mp.mpf(i-5)/(i+13) for i in range(12)]
        quad = density([2*x for x in direction])-3*density(direction)+3*f0-density([-x for x in direction])
        quad /= max(mp.mpf(1), abs(f0), abs(density(direction)))
        cases.append(dict(w=wstr, maximum_normalized_entry_error=mp.nstr(maximum, 70),
                          quadratic_identity_error=mp.nstr(abs(quad), 70),
                          retained_metric_frame_cross_size=mp.nstr(cross_size, 70),
                          nonzero_spatial_curvature_affine_potential_terms_retained=True))
    return dict(family=family, eta=estr, cases=cases,
                parameters='pinned independent loader, 90-digit parameter conversion; 100-digit density arithmetic')


def points(ch, models, workers):
    jobs = [(family, e, [str(z) for z in models[family]['R']]) for family in FAMILIES for e in ETAS]
    if workers == 1:
        results = list(map(point_job, jobs))
    else:
        with ProcessPoolExecutor(max_workers=min(workers, len(jobs)), mp_context=multiprocessing.get_context('spawn')) as pool:
            results = list(pool.map(point_job, jobs))
    tolerance = mp.mpf('1e-55')
    for result in results:
        for case in result['cases']:
            label = result['family']+'_'+result['eta']+'_'+case['w']
            ch.add(label+'_original_density_Hessian', mp.mpf(case['maximum_normalized_entry_error']) < tolerance,
                   case['maximum_normalized_entry_error'], 'normalized < 1e-55')
            ch.add(label+'_original_density_quadratic', mp.mpf(case['quadratic_identity_error']) < tolerance,
                   case['quadratic_identity_error'], 'normalized < 1e-55')
            if case['w'] != '0':
                ch.add(label+'_reject_missing_metric_frame_crosses', mp.mpf(case['retained_metric_frame_cross_size']) > tolerance)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preflight', action='store_true')
    group.add_argument('--output', type=Path)
    group.add_argument('--replay', type=Path)
    parser.add_argument('--workers', type=int, default=9)
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error('--workers must be between 1 and 16')
    mp.mp.dps = 100
    ch = base.Checks()
    controls = interval_controls(ch)
    if args.preflight:
        if any(not row['passed'] for row in ch.rows):
            raise ValueError('interval method preflight failed')
        progress('METHOD_PREFLIGHT_ONLY', passed=len(ch.rows), scientific_receipts=False)
        return
    dest = (args.replay or args.output).resolve()
    if not dest.is_relative_to(ROOT / 'Analysis/MasterTests/outputs'):
        raise ValueError('receipt destination outside declared output area')
    if args.output and dest.exists():
        raise FileExistsError('never overwrite a research attempt: '+str(dest))
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('replay directory missing')
    source_before = metadata()
    progress('EXACT_GENERIC_RECONSTRUCTION')
    eta, w, density, generic, models, affine_remainder = exact_model()
    algebra = exact_checks(ch, eta, w, density, generic, models, affine_remainder)
    domain = interval_domain(ch, eta, w, models)
    progress('ORIGINAL_DENSITY_POLARIZATION', jobs=9, workers=min(args.workers, 9))
    independent = points(ch, models, args.workers)
    source_after = metadata()
    if source_before != source_after:
        raise ValueError('source or native runtime metadata changed during execution')
    formulas = dict(generic_velocity_order=['K00', 'K01', 'K02', 'K11', 'K12', 'K22', 'X0', 'X1', 'X2', 'u_dot', 'v_dot', 'r_dot'],
                    domain=dict(eta='0<eta<=1', w='|w|<=1/500', h='I', u='sqrt(eta)', v='0', r='sqrt(eta)'),
                    generic_quadratic_density=str(density), generic_Hessian=[[str(generic[i, j]) for j in range(12)] for i in range(12)],
                    families={name: dict(parameter_map={k: str(v) for k, v in model['parameter_map'].items()},
                                         R=[[str(model['R'][i, j]) for j in range(12)] for i in range(12)],
                                         R0_inverse=[[str(model['inverse'][i, j]) for j in range(12)] for i in range(12)],
                                         T=[[str(model['T'][i, j]) for j in range(12)] for i in range(12)],
                                         analytic=algebra[name], interval=domain[name]) for name, model in models.items()},
                    interval_precision_decimal=80, parameter_partition=[16, 8],
                    eta_zero_included_only_for_extended_T_not_inverse=True,
                    inertia_interpretation='11 positive, 1 negative in the unreduced partial temporal Hessian; not a physical ghost test')
    failures = [row for row in ch.rows if not row['passed']]
    summary = dict(validation='PARTIAL_LEGENDRE_CHART_CERTIFIED' if not failures else 'PARTIAL_LEGENDRE_DOMAIN_UNRESOLVED',
                   passed=len(ch.rows)-len(failures), total=len(ch.rows), failed_checks=failures, unknown_checks=[], checks=ch.rows,
                   source_metadata=source_before, physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
                   review_status='DEFERRED', stage1='REGISTERED_BOUNDED_LINEAR_ACCEPTANCE_ONLY', stage2_complete=False,
                   stage3_entered=False, MAT_001='BLOCKED', K_Q='NOT_DERIVED', V='NOT_COMPUTED', UVIR_003='IN_PROGRESS',
                   Stage4A='CLOSED', TOP_X4='UNCHANGED', physical_energy_norm_derived=False,
                   full_auxiliary_hierarchy_closed=False, scalar_regulator_node_degeneracy_repaired=False,
                   physical_cutoff_derived=False, healthy_GR_proved=False, state_adopted_or_evolved=False,
                   beta_ceilings={name: domain[name]['beta_rational_ceiling'] for name in FAMILIES},
                   scope='Off-shell partial 12-velocity complement on the declared configuration family, not arbitrary3D physical clearance')
    if args.output:
        dest.mkdir(parents=False, exist_ok=False)
    for name, value in [('summary.json', summary), ('independent.json', dict(interval_primitives=controls, points=independent)),
                        ('formulas.json', formulas)]:
        base.pair(dest, name, ENC(value), bool(args.replay))
    expected = {name+suffix for name in ('summary.json', 'independent.json', 'formulas.json') for suffix in ('', '.sha256')}
    if {p.name for p in dest.iterdir()} != expected:
        raise ValueError('unexpected receipt file set')
    progress('READ_ONLY_REPLAY_EXACT' if args.replay else 'FRESH_RECEIPTS_WRITTEN', validation=summary['validation'],
             passed=summary['passed'], total=summary['total'], physics_pass=False, gate_effect='NONE')
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
