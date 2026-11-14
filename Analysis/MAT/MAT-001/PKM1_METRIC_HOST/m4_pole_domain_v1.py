"""P0-B local-frequency diagnostics, with background and normalization drift.

No stationary physical pole or interacting cutoff is inferred from these roots.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[4]
INPUTS = 'Theory/Gates/MAT-001/MAT001_M4_P0B_POLE_DOMAIN_V1_INPUTS_2026-11-05.json'
PARENT = 'Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/m4_actual_source_kernel_v3_20261105/receipt.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    pins = dict(json.loads((ROOT / INPUTS).read_text())['source_sha256'])
    for rel in [INPUTS, Path(__file__).relative_to(ROOT).as_posix()]:
        pins[rel] = sha(ROOT / rel)
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT / rel
        assert sha(path) == expected, rel
        for item in [path, Path(str(path) + '.sha256')]:
            if item.exists():
                snapshot[item] = (sha(item), item.stat().st_mtime_ns)
    checks = []

    def check(name, passed, evidence=None):
        checks.append(dict(name=name, passed=bool(passed), evidence=evidence))

    names = 'M H rho mu q CJ rho_dot V V_rho V_rhorho delta_e j tau'.split()
    sy = {n: s.Symbol(n, positive=True) for n in names[:6]}
    sy.update({n: s.Symbol(n, real=True) for n in names[6:]})
    M, H, r, mu, q, CJ, v, V, Vr, Vrr = [sy[n] for n in names[:10]]
    V3 = s.Symbol('V_rhorhorho', real=True)
    a = s.Symbol('a', positive=True)
    data = json.loads((ROOT / PARENT).read_text())

    def mat(key):
        return s.Matrix([[s.sympify(t, locals=sy) for t in row]
                         for row in data['nonzero_mode'][key]]).subs(CJ, 2*M)

    K, D, F, C, Bv, Bx = [mat(key) for key in
                           ['K', 'D', 'F', 'C', 'B_velocity', 'B_field']]
    K = K.subs(V, 3*M*H**2-(v**2+r**2*mu**2)/2)
    bg = {a: a*H, r: v, mu: -3*H*mu-2*v*mu/r,
          v: -3*H*v+r*mu**2-Vr, H: -(v*v+r*r*mu*mu)/(2*M),
          q: -H*q, V: Vr*v, Vr: Vrr*v, Vrr: V3*v}

    def dt(matrix):
        return matrix.applyfunc(lambda e: sum(s.diff(e, u)*b for u, b in bg.items()))

    # Differentiate FIRST: radial equilibrium holds at the initial event only.
    event = {v: 0, Vr: r*mu**2, V: 3*M*H**2-r*r*mu**2/2, a: 1}

    def at_event(matrix):
        return matrix.applyfunc(lambda e: s.factor(e.subs(event)))

    K0, K1, K2, D0, D1, F0 = map(at_event, [K, dt(K), dt(dt(K)), D, dt(D), F])
    Ds = (D+D.T)/2
    Fe = at_event(F-dt(Ds)-3*H*Ds)
    Graw = at_event(D-D.T)
    expected_Fe = s.Matrix([
        [-r*r*mu**2*q*q/H**2, mu**4*r**3/(2*H**2*M)],
        [mu**4*r**3/(2*H**2*M), mu**2-Vrr-q*q]])
    check('mixed_symmetric_term_and_volume_derivative_retained',
          s.simplify(Fe-expected_Fe) == s.zeros(2))
    check('naively_frozen_mass_rejected', s.simplify(F0-Fe) != s.zeros(2))
    check('retained_gyroscopic_mixing',
          Graw == s.Matrix([[0, -2*r*mu**2/H], [2*r*mu**2/H, 0]]))
    # Integrating the symmetric mixed term changes only a boundary term.
    check('exact_Euler_mass_identity', s.simplify(
        dt(D)+3*H*D-F - (dt((D-D.T)/2)+3*H*(D-D.T)/2-(F-dt(Ds)-3*H*Ds)))
        == s.zeros(2))

    # Whitening the full evolving kinetic form, INCLUDING the a^3 measure.
    kap = (r*r*mu*mu+2*M*q*q)/H**2
    T = a**(-s.Rational(3, 2))*s.Matrix([
        [1/s.sqrt(kap), 0], [v/(H*s.sqrt(kap)), 1]])  # x=T y
    check('full_evolving_canonical_kinetic_identity',
          s.simplify(a**3*T.T*K*T) == s.eye(2))
    T0, T1, T2 = map(at_event, [T, dt(T), dt(dt(T))])
    Ec = T0.T*K0*T1+T0.T*D0*T0
    Ec_dot = (3*H*Ec+T1.T*K0*T1+T0.T*K1*T1+T0.T*K0*T2
              +T1.T*D0*T0+T0.T*D1*T0+T0.T*D0*T1)
    Fc_raw = T1.T*K0*T1+T1.T*D0*T0+T0.T*D0.T*T1+T0.T*F0*T0
    Fc = (Fc_raw-(Ec_dot+Ec_dot.T)/2).applyfunc(s.factor)
    Gc = (Ec-Ec.T).applyfunc(s.factor)
    Gc_dot = (Ec_dot-Ec_dot.T).applyfunc(s.factor)
    transformed_first = T0.T*(2*K0*T1+(K1+3*H*K0+Graw)*T0)
    transformed_mass = T0.T*(K0*T2+(K1+3*H*K0+Graw)*T1+(D1+3*H*D0-F0)*T0)
    check('canonical_Euler_first_derivative_identity', s.simplify(transformed_first-Gc) == s.zeros(2))
    check('canonical_Euler_mass_identity_including_antisymmetric_drift',
          s.simplify(transformed_mass-(Gc_dot/2-Fc)) == s.zeros(2))
    check('canonical_drift_is_not_zero_at_finite_q', Gc_dot != s.zeros(2))

    w = s.Symbol('omega', real=True)
    Praw = s.factor((-w*w*K0-s.I*w*Graw-Fe).det())
    Pc = s.factor((-w*w*s.eye(2)-s.I*w*Gc-Fc).det())
    slow_raw = r*r*mu*mu/(2*M)
    slow_can = -H**2/4+13*r*r*mu*mu/(4*M)-r**4*mu**4/(2*H**2*M**2)
    check('raw_slow_large_q_limit_with_mixing',
          s.simplify(s.limit(Praw/q**4, q, s.oo)-(r*r*mu*mu-2*M*w*w)/H**2) == 0)
    check('canonical_slow_large_q_limit_with_mixing',
          s.simplify(s.limit(Pc/q**2, q, s.oo)-(-w*w+slow_can)) == 0)
    z = s.Symbol('z', real=True)
    check('canonical_fast_branch_has_unit_large_q_speed',
          s.simplify(s.limit(Pc.subs(w, z*q)/q**4, q, s.oo)-z*z*(z*z-1)) == 0)
    X = s.Symbol('X', nonnegative=True)
    f = -s.Rational(1, 4)+13*X/4-X*X/2
    check('canonical_slow_to_H_bound_by_completed_square',
          s.expand(f-(s.Rational(161, 32)-(X-s.Rational(13, 4))**2/2)) == 0)
    check('canonical_normalization_changes_slow_frequency_at_background_order',
          s.simplify(slow_can-slow_raw) != 0)
    check('chemical_background_rate_not_fast_mode_frequency',
          s.simplify(bg[mu].subs(event)/mu+3*H) == 0)

    # Exact source-free metric map at this event, before assuming a frequency.
    xx = s.Matrix(s.symbols('R drho'))
    xd = s.Matrix(s.symbols('Rdot drhodot'))
    cc = -C.inv()*(Bv*xd+Bx*xx)
    psi = at_event(s.Matrix([-xx[0]-H*cc[1]/q**2]))[0]
    expected_psi = (1+r*r*mu*mu/(2*M*q*q))*xd[0]/H-r*mu*mu*xx[1]/(M*q*q)
    check('actual_metric_map_not_replaced_by_bare_phase', s.simplify(psi-expected_psi) == 0)
    # For the formal canonical slow branch y=(1,O(q^-3)), Psi has this
    # nonzero leading coefficient. This is a diagnostic overlap, NOT a residue.
    psi_y = s.simplify(expected_psi.subs(dict(zip(list(xx)+list(xd),
                              list(T0*s.Matrix([1, 0]))+list((T1-s.I*w*T0)*s.Matrix([1, 0]))))))
    psi_asym = s.simplify(s.limit(q*psi_y, q, s.oo))
    expected_asym = (-s.I*w-H/2-r*r*mu*mu/(2*M*H))/s.sqrt(2*M)
    check('slow_branch_has_metric_overlap', s.simplify(psi_asym-expected_asym) == 0)

    # Independent direct numeric Schur assembly and background-flow derivatives.
    # These finite-difference checks test implementation, not rigorous errors.
    pot = r*r/2+r**4/16+r**6/480
    charge = float(s.sqrt(s.Rational(101, 80)))
    h0 = float(s.sqrt(s.Rational(287, 720)))
    rhs = lambda tt, yy: np.array([
        yy[0]*yy[3], yy[2],
        -3*yy[3]*yy[2]+charge**2/(yy[0]**6*yy[1]**3)
        -yy[1]-yy[1]**3/4-yy[1]**5/80,
        -(yy[2]**2+charge**2/(yy[0]**6*yy[1]**2))/2])
    init = np.array([1., 1., 0., h0])
    forward = solve_ivp(rhs, (0, .01), init, method='DOP853', rtol=2e-13, atol=2e-15, dense_output=True)
    backward = solve_ivp(rhs, (0, -.01), init, method='DOP853', rtol=2e-13, atol=2e-15, dense_output=True)
    check('independent_background_solvers_returned', forward.success and backward.success)

    def direct(time, mode):
        aa, rr, vv, hh = (forward if time >= 0 else backward).sol(time)
        mm = charge/(aa**3*rr**2)
        qq = mode/aa
        pp = rr*rr/2+rr**4/16+rr**6/480
        pr = rr+rr**3/4+rr**5/80
        prr = 1+3*rr**2/4+rr**4/16
        cn = np.array([[2*qq*qq-2*pp, 2*hh], [2*hh, 0.]])
        bv = np.array([[6*hh, -vv], [-2., 0.]])
        bx = np.array([[2*qq*qq, -(pr+rr*mm*mm)], [0., -vv]])
        kn = np.diag([-6., 1.])-bv.T@np.linalg.solve(cn, bv)
        dn = np.array([[-18*hh, 0.], [3*vv, 0.]])-bv.T@np.linalg.solve(cn, bx)
        fn = np.array([[2*qq*qq-18*pp, 3*(rr*mm*mm-pr)],
                       [3*(rr*mm*mm-pr), mm*mm-prr-qq*qq]])-bx.T@np.linalg.solve(cn, bx)
        # Cholesky directly from the unreduced-constraint numeric action.
        tn = np.linalg.inv(np.linalg.cholesky(kn).T)/aa**1.5
        return aa**3, kn, dn, fn, tn

    fixed = {M: 1, H: s.sqrt(s.Rational(287, 720)), r: 1,
             mu: s.sqrt(s.Rational(101, 80)), Vrr: s.Rational(29, 16)}
    # V''(1)=1+3/4+1/16=29/16.
    numeric = s.lambdify(q, [m.subs(fixed) for m in [K0, D0, F0, Fe, Fc, Gc, Gc_dot]], 'numpy', cse=True)
    rows = []
    for mode in [1., 4., 16., 64., 256.]:
        kval, dval, fval, feval, fcval, gcval, gdval = [np.array(m, dtype=float) for m in numeric(mode)]
        b0, kd, dd, fd, td = direct(0., mode)
        block_err = max(np.max(np.abs(kval-kd)), np.max(np.abs(dval-dd)), np.max(np.abs(fval-fd)))
        check(f'independent_uneliminated_Schur_mode_{mode:g}', block_err < 1e-7, float(block_err))
        if mode <= 16:
            errors = []
            for step in [.001, .0005]:
                pp = [direct(j*step, mode) for j in [-2, -1, 0, 1, 2]]

                def derivative(index):
                    return (pp[0][index]-8*pp[1][index]+8*pp[3][index]-pp[4][index])/(12*step)

                kt, dt0 = derivative(1), derivative(2)
                tt = derivative(4)
                ttt = (-pp[4][4]+16*pp[3][4]-30*td+16*pp[1][4]-pp[0][4])/(12*step**2)
                ec = td.T@kd@tt+td.T@dd@td
                ecd = (3*h0*ec+tt.T@kd@tt+td.T@kt@tt+td.T@kd@ttt
                       +tt.T@dd@td+td.T@dt0@td+td.T@dd@tt)
                ft = tt.T@kd@tt+tt.T@dd@td+td.T@dd.T@tt+td.T@fd@td
                fcnum = ft-(ecd+ecd.T)/2
                err = max(np.max(np.abs(fcnum-fcval)),
                          np.max(np.abs((ecd-ecd.T)-gdval))) / max(1., np.max(np.abs(fcval)))
                errors.append(float(err))
            check(f'independent_background_flow_normalized_derivatives_{mode:g}', max(errors) < 2e-5, errors)
        # Roots of the local CONSERVATIVE diagnostics in omega^2.
        raw_scale = np.diag([1/np.sqrt(kval[0, 0]), 1.])
        fr = raw_scale@feval@raw_scale
        gr = raw_scale@np.array(Graw.subs(fixed).subs(q, mode), float)@raw_scale

        def roots(mass, gyro):
            b = np.trace(mass)-gyro[0, 1]**2
            return np.sort_complex(np.roots([1., b, np.linalg.det(mass)]))

        rawroots, canroots = roots(fr, gr), roots(fcval, gcval)
        check(f'diagnostic_real_oscillatory_roots_at_benchmark_{mode:g}',
              np.all(np.abs(canroots.imag) < 1e-10) and np.all(canroots.real > 0))
        rows.append(dict(q=mode, raw_omega_squared=rawroots.real.tolist(),
                         canonical_omega_squared=canroots.real.tolist(),
                         canonical_slow_omega_over_H=float(np.sqrt(canroots[0].real)/h0),
                         chemical_drift_over_slow_omega=float(3*h0/np.sqrt(canroots[0].real)),
                         canonical_fast_omega_over_q=float(np.sqrt(canroots[1].real)/mode),
                         caveat='LOCAL_CONSERVATIVE_DIAGNOSTIC_NOT_PHYSICAL_POLE'))

    check('input_bytes_sidecars_and_timestamps_preserved',
          all(sha(p) == hh and p.stat().st_mtime_ns == tm for p, (hh, tm) in snapshot.items()))
    encode = lambda m: [[str(s.factor(e)) for e in m.row(i)] for i in range(m.rows)]
    return dict(kind='M4_P0B_POLE_DOMAIN_V1', source_sha256=pins, checks=checks,
                passed=sum(c['passed'] for c in checks), total=len(checks),
                event_domain='expanding H>0; q>0; rho,mu,M>0; rho_dot=0 and V_rho=rho*mu^2 at this event only; V>=0 for X<=6 bound',
                exact_local_data=dict(K=encode(K0), D=encode(D0), F=encode(F0),
                                      F_after_symmetric_IBP=encode(Fe), G_raw=encode(Graw),
                                      canonical_T=encode(T0), canonical_T_dot=encode(T1),
                                      canonical_F=encode(Fc), canonical_G=encode(Gc), canonical_G_dot=encode(Gc_dot)),
                exact_canonical_equation='y_ddot+G*y_dot+(G_dot/2-F_c)*y=transformed_source',
                conservative_diagnostic='det(-omega^2*I-i*omega*G-F_c); dropping G_dot requires separate control',
                asymptotic=dict(raw_slow_omega_squared=str(slow_raw), canonical_slow_omega_squared=str(slow_can),
                                X='rho^2*mu^2/(M*H^2), 0<X<=6 if V>=0',
                                canonical_slow_max_omega_over_H='sqrt(161/32)',
                                minimum_chemical_drift_over_canonical_slow_frequency='3*sqrt(32/161) > 1',
                                canonical_fast_omega_over_q='1',
                                slow_metric_overlap_q_times_Psi=str(psi_asym)),
                benchmark_diagnostics=rows,
                disposition='HIGH_Q_ALONE_DOES_NOT_PROVIDE_ADIABATIC_SLOW_FORCE_POLE_IN_REGISTERED_EQUILIBRIUM_FAMILY',
                physical_residue='NOT_COMPUTED_NO_CONTROLLED_PHYSICAL_POLE_WINDOW_ESTABLISHED',
                remaining='Finite-domain retarded-response approximation/error control and interacting cutoff; a fast amplitude root cannot establish the slow matter-force residue. No all-parent exclusion.',
                full_M4='INCOMPLETE', cheap_screen='REPRODUCIBLE_INCOMPLETENESS_WITH_DOMAIN_OBSTRUCTION',
                live_TrackA_V='NOT_COMPUTED', review='DEFERRED', physics_pass=False, gate_effect='NONE')


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
    print(json.dumps(dict(passed=data['passed'], total=data['total'],
                          failed=[c for c in data['checks'] if not c['passed']],
                          disposition=data['disposition'], physics_pass=False)))
    if data['passed'] != data['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
