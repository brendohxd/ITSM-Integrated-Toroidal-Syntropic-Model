"""Deciding nonlinear norm test, not a background evolution certificate."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import traceback
from fractions import Fraction
import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/outputs/rtau_planar_current_drift_audit_v2_20261119/receipt.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_RTAU_NONLINEAR_CONTINUATION_V1_CONTRACT_2026-11-19.md'
FACTORY = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
CURRENT = 'Analysis/MasterTests/test_rtau_planar_current_operator_v2.py'
RAW = 'Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
WEAK = 'Analysis/MasterTests/r4c1_full_weak_action_v1.py'
GATE = 'Theory/Gates/RES-001/'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def enc(data):
    return (json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def convolution(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, Fraction(0)) + x * y
    return out

def exact_controls():
    checks = {}
    N, vol, rate, shift, rz, p, potential, hzz = sp.symbols(
        'N vol rate shift rz p potential hzz', positive=True)
    L = vol * (rate - shift * rz)**2 / (2*N) - N*vol*(hzz*rz**2/2 + potential)
    velocity = shift*rz + N*p/vol
    checks['neutral_scalar_Legendre_map'] = sp.simplify(sp.diff(L, rate).subs(rate, velocity)-p) == 0
    I = sp.simplify((L-p*(rate-shift*rz)).subs(rate, velocity))
    target = -N*p**2/(2*vol)-N*vol*(hzz*rz**2/2+potential)
    checks['canonical_current_scalar_sign'] = sp.simplify(I-target) == 0
    f, chi, longitudinal = sp.symbols('f chi longitudinal', positive=True)
    # Full Schur trace: delta vol=vol*f; delta h^{zz}=-chi*f.
    trace_I = vol*sp.diff(I,vol)-chi*sp.diff(I,hzz)
    checks['scalar_trace_zero_order_coefficient'] = sp.simplify(
        trace_I.subs(hzz,1/longitudinal+chi)
        -(N*p**2/(2*vol)-N*vol*(rz**2/(2*longitudinal)+potential))) == 0
    checks['mixed_metric_inverse_trace_drift_retained'] = sp.simplify(
        sp.diff(1/longitudinal+sp.exp(-f)*chi,f).subs(f,0)+chi) == 0
    dp = sp.symbols('dp')
    checks['exact_current_finite_momentum_increment'] = sp.simplify(
        I.subs(p, p+dp)-I+N/vol*(p*dp+dp**2/2)) == 0
    K = trace_I
    checks['exact_trace_finite_momentum_increment'] = sp.simplify(
        K.subs(p, p+dp)-K-N/vol*(p*dp+dp**2/2)) == 0
    c = sp.symbols('c', positive=True)
    checks['current_second_momentum_differential'] = sp.diff(-c*p**2/2, p, 2) == -c

    n, j = sp.symbols('n j', integer=True, positive=True)
    sumsq = sp.summation(j*j, (j, 1, n-1))
    fourth = n*n/4 + sumsq/2 + (n*n+2*sumsq)/8
    checks['all_N_fourth_moment_count_identity'] = sp.simplify(fourth-(2*n**3+n)/8) == 0
    for size in range(1, 17):
        coeff = {k: Fraction(1, 2) for k in list(range(size, 2*size)) + list(range(-2*size+1, -size+1))}
        square = convolution(coeff, coeff)
        checks[f'exact_Fourier_fourth_moment_N{size}'] = (
            square[0] == Fraction(size, 2) and
            sum(v*v for v in square.values()) == Fraction(2*size**3+size, 8))
    m = sp.symbols('m', positive=True)
    norm2 = sp.simplify((n/2).subs(n, m**8)*m**-10)
    square_norm2 = sp.simplify(((2*n**3+n)/8).subs(n, m**8)*m**-20)
    checks['input_L2_tends_to_zero'] = sp.limit(norm2, m, sp.oo) == 0
    checks['square_L2_diverges'] = sp.limit(square_norm2, m, sp.oo) == sp.oo
    checks['mean_free_square_still_diverges'] = sp.limit(square_norm2-norm2**2, m, sp.oo) == sp.oo
    checks['no_uniform_L2_product_constant'] = sp.limit(square_norm2/norm2**2, m, sp.oo) == sp.oo
    checks['mean_of_input_zero'] = all(0 not in {k for k in list(range(n,2*n))+list(range(-2*n+1,-n+1))} for n in range(1,17))
    # Smooth finite-rank orthogonal projection: h=g-f has ||h||inf<=C||f||2.
    a, C = sp.symbols('a C', positive=True)
    correction = 2*C*a*a + C*C*a*a
    checks['smooth_range_projection_square_error_vanishes'] = sp.limit(correction, a, 0) == 0
    # Fourier Cauchy-Schwarz and 1+2 sum_{n>=1}1/n^2 <=5.
    x = sp.symbols('x', positive=True)
    checks['H1_embedding_explicit_majorant'] = 1+2*(1+sp.integrate(x**-2, (x, 1, sp.oo))) == 5
    checks['square_difference_factorization'] = sp.expand((p+dp)**2-p**2-dp*(2*p+dp)) == 0
    examples = []
    for size in (1, 2, 4, 8, 16):
        examples.append({'m': size, 'N': size**8,
            'input_L2_squared': str(Fraction(1, 2*size**2)),
            'square_L2_squared': str(Fraction(size**4, 4)+Fraction(1, 8*size**12)),
            'mean_free_square_L2_squared': str(Fraction(size**4, 4)+Fraction(1, 8*size**12)-Fraction(1, 4*size**4))})
    return checks, examples

def action_controls():
    mp.mp.dps = 90
    mp.iv.dps = 55
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    ab = lambda x: max(abs(lo(x)), abs(hi(x)))
    env = load('nonlinear_scalar_full_action', FACTORY).prepare()
    current = load('nonlinear_scalar_current', CURRENT)
    J = env['J']; grad = env['gradient']; hj = env['hj']
    y, _ = env['state'](J.variable(iv.mpf('0.3')), False)
    # A genuinely nonconformal full metric, with spatial metric jets zero.
    for i, value in enumerate([iv.mpf(6)/5, iv.mpf(1)/23, iv.mpf(1)/31,
                               iv.mpf(7)/6, -iv.mpf(1)/37, iv.mpf(5)/4]):
        y[i] = J(value); y[28+i] = J(0)
    L = env['evaluate'](y)
    base = current.canonical_coefficients(env, y, L)
    q, spatial = y[:14], y[28:42]
    lapse, volume, gamma, inverse, flux = env['geometry'](q, spatial)
    c = lapse/volume
    tol = mp.mpf('1e-28')
    checks = {}
    checks['full_action_neutral_velocity_Hessian'] = max(ab((hj(L,25,25)-volume/lapse).c[k]) for k in range(3)) < tol
    checks['full_action_neutral_velocity_decouples_every_other_rate'] = all(
        all(ab(hj(L,25,14+i).c[k]) < tol for k in range(3)) for i in range(14) if i != 11)
    p0 = base['momenta'][11]
    checks['full_action_neutral_canonical_momentum'] = max(ab((p0-volume/lapse*base['normal_rates'][11]).c[k]) for k in range(3)) < tol
    Hxx, Hxy, Hyy, mx, my, zz = q[0], q[1], q[3], q[2], q[4], q[5]
    trace = [J(0) for _ in range(14)]
    trace[0] = Hxx-mx*mx/zz; trace[1] = Hxy-mx*my/zz; trace[3] = Hyy-my*my/zz
    density = lambda ll, cc: ll.c.c[0]-sum(cc['momenta'][i].c[0]*cc['normal_rates'][i].c[0] for i in range(14))-cc['F'].c.c[1]
    trace_a0 = lambda cc: sum(cc['C0'][i]*trace[i].c[0]+cc['C1'][i]*trace[i].c[1]+cc['C2'][i]*2*trace[i].c[2] for i in range(14))
    records = []
    for label, delta in [('plus', iv.mpf(1)/17), ('minus', -iv.mpf(2)/19)]:
        changed = list(y); changed[25] += c*delta
        L1 = env['evaluate'](changed)
        cc = current.canonical_coefficients(env, changed, L1)
        expected = c.c[0]*(p0.c[0]*delta+delta*delta/2)
        current_error = ab(density(L1,cc)-density(L,base)+expected)
        trace_error = ab(trace_a0(cc)-trace_a0(base)-expected)
        checks['full_action_current_increment_'+label] = current_error < tol
        checks['full_action_trace_increment_'+label] = trace_error < tol
        checks['full_action_other_momenta_unchanged_'+label] = all(
            max(ab((cc['momenta'][i]-base['momenta'][i]).c[k]) for k in range(3)) < tol
            for i in range(14) if i != 11)
        checks['lapse_flux_unchanged_by_neutral_momentum_'+label] = max(
            ab((cc['F'].c-base['F'].c).c[k]) for k in range(3)) < tol
        records.append({'direction': label, 'current_identity_defect': mp.nstr(current_error, 35),
                        'trace_coefficient_identity_defect': mp.nstr(trace_error, 35)})
    psmax = iv.mpf(1)/1000*(iv.mpf(1)/29+iv.mpf(1)/31)
    lower = iv.exp(-(iv.mpf(2)/5*psmax+iv.mpf(3)/13000))
    checks['prepared_initial_scalar_coefficient_bounded_away_from_zero'] = lo(lower) > 0
    return checks, {'full_action_controls': records,
                    'prepared_N_over_volume_lower': mp.nstr(lo(lower), 40),
                    'new_background_or_evolved_solution': False}

def calculate():
    parent = json.loads((ROOT/PARENT).read_text(encoding='utf-8'))
    pins = dict(parent['source_pins'])
    extra = [SELF,PARENT,CONTRACT,FACTORY,CURRENT,RAW,WEAK,
        GATE+'RES001_RTAU_NONLINEAR_CONTINUATION_V2_SPEC_2026-11-19.md',
        'Analysis/MasterTests/test_rtau_nonlinear_continuation_v1.py',
        'Analysis/MasterTests/outputs/rtau_nonlinear_continuation_v1_20261119/receipt.json',
        GATE+'RES001_RTAU_PLANAR_CURRENT_DRIFT_V2_REPORT_2026-11-19.md',
        GATE+'RES001_RTAU_PLANAR_GAUGE_DOMAIN_V3_REPORT_2026-11-19.md',
        GATE+'RES001_RTAU_INITIAL_FORCED_ENERGY_V1_REPORT_2026-11-14.md',
        GATE+'RES001_RTAU_DENSITY_STATE_MAP_V1_REPORT_2026-11-14.md']
    for name in extra:
        value = digest(ROOT/name)
        assert name not in pins or pins[name] == value, name
        pins[name] = value
    snapshot = {}
    for name, value in pins.items():
        p = ROOT/name; side = Path(str(p)+'.sha256')
        assert digest(p) == value, name
        if not name.endswith('.sha256'):
            assert side.read_text(encoding='utf-8').split()[0].lower() == value, name
        for f in (p,side) if side.exists() else (p,):
            snapshot[f] = (digest(f), f.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks'])
    checks, examples = exact_controls()
    more, action = action_controls(); checks.update(more)
    checks['source_bytes_sidecars_mtimes_preserved'] = all(
        (digest(p),p.stat().st_mtime_ns) == value for p,value in snapshot.items())
    return {'contract': CONTRACT, 'source_pins': pins,
        'checks': [{'name':n,'passed':bool(v)} for n,v in checks.items()],
        'concentration_sequence': examples, 'action_control': action,
        'mathematical_result': 'BASE_FREE_MOMENTUM_L2_TO_NONLINEAR_CURRENT_L2_AND_OPERATOR_H2_TO_L2_CONTINUITY_FAILS_ON_THE_UNREDUCED_CHART',
        'momentum_range_correction': 'SMOOTH_FINITE_RANK_PROJECTION_AND_EXACT_MOMENTUM_RECONSTRUCTION_DO_NOT_REMOVE_THE_QUADRATIC_CONCENTRATION',
        'fixed_I_U1_nonlinear_admission': 'NOT_PROVED_BY_THE_COUNTEREXAMPLE',
        'stronger_term_estimate': 'norm(c*(p^2-q^2))_L2 <= sqrt(5)*norm(c)_infinity*(norm(p)_H1+norm(q)_H1)*norm(p-q)_L2',
        'full_reduced_chart_impossibility': False, 'physical_instability_proved': False,
        'background_persistence': 'OPEN', 'energy_persistence': 'OPEN',
        'time_interval_certified': None, 'review':'DEFERRED', 'Rtau_adopted':False,
        'physics_pass':False, 'gate_effect':'NONE', 'G1_G6':'INCOMPLETE',
        'K_Q':'NOT_DERIVED', 'V':'NOT_COMPUTED'}

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--out'); parser.add_argument('--replay')
    args = parser.parse_args(); data = calculate(); body = enc(data)
    if args.replay:
        assert (ROOT/args.replay).read_bytes() == body, 'replay differs'
    else:
        out = ROOT/args.out; out.mkdir(parents=True, exist_ok=False)
        p = out/'receipt.json'; p.write_bytes(body)
        Path(str(p)+'.sha256').write_bytes((digest(p)+'  '+p.relative_to(ROOT).as_posix()+'\n').encode())
    failures = [c['name'] for c in data['checks'] if not c['passed']]
    print(json.dumps({'passed':len(data['checks'])-len(failures),'total':len(data['checks']),
                      'failures':failures,'pins':len(data['source_pins']), 'physics_pass':False,
                      'background_persistence':'OPEN','replay':bool(args.replay)}))
    assert not failures, failures

if __name__ == '__main__':
    main()
