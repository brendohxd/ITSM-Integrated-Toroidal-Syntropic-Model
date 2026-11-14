"""U3 B1/B2 force-operator controls, not a new live action or full amplitude."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[4]
INPUTS = 'Theory/Gates/UVIR-003/UVIR003_U3_ANALYTIC_CONTROLS_V1_INPUTS_2026-11-05.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    pins = dict(json.loads((ROOT/INPUTS).read_text(encoding='utf-8'))['source_sha256'])
    for rel in [INPUTS, Path(__file__).relative_to(ROOT).as_posix()]:
        pins[rel] = sha(ROOT/rel)
    snapshot = {}
    for rel, expected in pins.items():
        path = ROOT/rel
        assert sha(path) == expected, rel
        for item in [path, Path(str(path)+'.sha256')]:
            if item.exists():
                snapshot[item] = sha(item), item.stat().st_mtime_ns
    checks = []

    def check(name, passed, evidence=None):
        checks.append(dict(name=name, passed=bool(passed), evidence=evidence))

    Y = s.Symbol('Y', nonnegative=True)
    sigma, B, ar, K, reg, scale = s.symbols('sigma B a_ref K r_reg scale', positive=True)
    I = s.Symbol('I', nonnegative=True)
    F1 = (Y+sigma**2)**s.Rational(3, 2)-sigma**3
    F2 = F1-s.Rational(3, 2)*sigma*Y
    funcs = [F1, F2]
    series = [s.series(f, Y, 0, 4).removeO() for f in funcs]
    expected = [3*sigma*Y/2+3*Y**2/(8*sigma)-Y**3/(16*sigma**3),
                3*Y**2/(8*sigma)-Y**3/(16*sigma**3)]
    check('existing_series_reproduced_as_input_control', all(s.expand(a-b) == 0 for a, b in zip(series, expected)))
    check('fourth_derivative_for_positive_remainder_bound',
          all(s.simplify(s.diff(f, Y, 4)-s.Rational(9, 16)/(Y+sigma**2)**s.Rational(5, 2)) == 0 for f in funcs))
    check('third_derivative_for_quartic_truncation_error',
          all(s.simplify(s.diff(f, Y, 3)+s.Rational(3, 8)/(Y+sigma**2)**s.Rational(3, 2)) == 0 for f in funcs))
    check('sigma_positive_essential_for_finite_fourth_gradient_vertex',
          s.limit(3/(8*sigma), sigma, 0, dir='+') == s.oo)
    check('pointwise_zero_sigma_limit_does_not_fix_vertex_limit',
          all(s.simplify(s.limit(f, sigma, 0, dir='+')-Y**s.Rational(3, 2)) == 0 for f in funcs))
    # Restoring dimensions: the old dimensionless Y and raw-gradient charts
    # are different representations of exactly the same control.
    raw_sigma = s.Symbol('Sigma_raw', positive=True)
    raw1 = (I+raw_sigma**2)**s.Rational(3, 2)-raw_sigma**3
    raw2 = raw1-s.Rational(3, 2)*raw_sigma*I
    check('normalized_to_raw_gradient_chart_identity', all(
        s.simplify(f.subs(Y, I/ar**2)-raw.subs(raw_sigma, sigma*ar)/ar**3) == 0
        for f, raw in zip(funcs, [raw1, raw2])))
    # Mass dimensions in the declared dimensionless-psi chart.
    dimensions = dict(psi=0, derivative=1, Y=0, sigma=0, a_ref=1,
                      K=2, B=4, r_reg=0, C_m=0, delta_rho=4, chi=1)
    check('action_and_canonical_contact_mass_dimensions',
          dimensions['K']+2 == 4 and dimensions['B'] == 4
          and dimensions['r_reg']+4 == 4
          and 4-4-2*dimensions['K'] == -4)

    mus = [s.simplify(2*s.diff(f, Y)/3) for f in funcs]
    expected_mu = [s.sqrt(Y+sigma**2), Y/(s.sqrt(Y+sigma**2)+sigma)]
    check('exact_static_constitutive_currents', all(s.simplify(a-b) == 0 for a, b in zip(mus, expected_mu)))
    check('B1_linear_IR_constitutive_limit', s.simplify(mus[0].subs(Y, 0)-sigma) == 0)
    check('B2_cubic_flux_IR_constitutive_limit', s.simplify(s.limit(mus[1]/Y, Y, 0, dir='+')-1/(2*sigma)) == 0)
    check('neither_completion_preserves_exact_square_root_asymptote',
          s.limit(mus[0]/s.sqrt(Y), Y, 0, dir='+') == s.oo
          and s.limit(mus[1]/s.sqrt(Y), Y, 0, dir='+') == 0)
    # Stiffness eigenvalues are the Hessian of the SAME spatial energy.
    g = s.Symbol('g', positive=True)
    gx, gy, gz = s.symbols('g_x g_y g_z', real=True)
    grad = s.Matrix([gx, gy, gz])
    hessians = []
    for n, f in enumerate(funcs, 1):
        hess = s.hessian(B*f.subs(Y, grad.dot(grad)/ar**2), grad)
        axis = hess.subs({gx: g, gy: 0, gz: 0}).applyfunc(s.simplify)
        mu = mus[n-1]
        target = s.diag(3*B*(mu+2*Y*s.diff(mu, Y))/ar**2,
                        3*B*mu/ar**2, 3*B*mu/ar**2).subs(Y, g*g/ar**2)
        check(f'B{n}_independent_gradient_Hessian', s.simplify(axis-target) == s.zeros(3))
        hessians.append(axis)
    # B2 mu=Y/(sqrt(Y+sigma^2)+sigma)>=0; parallel multiplier is
    # mu+Y/sqrt(Y+sigma^2), strictly positive for Y>0, zero at Y=0.
    check('B2_positive_parallel_multiplier_identity', s.simplify(
        mus[1]+2*Y*s.diff(mus[1], Y) - (mus[1]+Y/s.sqrt(Y+sigma**2))) == 0)

    # Direct ADM terms from the same unitary, hypersurface-orthogonal host.
    eps, curvature, lapse = s.symbols('epsilon R n', real=True)
    aa = s.Symbol('a', positive=True)
    gg = s.Symbol('grad_pi_squared', nonnegative=True)
    Yadm = eps**2*gg*s.exp(-2*eps*curvature)/(aa**2*ar**2)
    volume = aa**3*(1+eps*lapse)*s.exp(3*eps*curvature)
    c = 3*B*sigma/(2*ar**2)
    lam = 3*B/(8*sigma*ar**4)
    expected_adm = [
        [-c*aa*gg, -c*aa*(lapse+curvature)*gg,
         -c*aa*(lapse*curvature+curvature**2/2)*gg-lam*gg**2/aa],
        [s.Integer(0), s.Integer(0), -lam*gg**2/aa]]
    adm = []
    for n, polynomial in enumerate(series):
        expression = s.series(-B*volume*polynomial.subs(Y, Yadm), eps, 0, 5).removeO().expand()
        coefficients = [s.factor(expression.coeff(eps, j)) for j in [2, 3, 4]]
        check(f'B{n+1}_direct_ADM_quadratic_cubic_quartic',
              all(s.simplify(x-y) == 0 for x, y in zip(coefficients, expected_adm[n])))
        adm.append(coefficients)
    check('B1_changed_quadratic_lapse_source', s.simplify(s.diff(adm[0][1], lapse)+c*aa*gg) == 0)
    check('B2_new_spatial_operator_has_no_quadratic_constraint_source',
          adm[1][1] == 0 and not adm[1][2].has(lapse))

    # Flat factorized force block. This is not the other coupled host block.
    pdot, pp, lap = s.symbols('pi_dot p_pi Delta_pi', real=True)
    k = s.Symbol('k', positive=True)
    stiffness = [3*B*sigma/ar**2, s.Integer(0)]
    dispersions = []
    for n, stiff in enumerate(stiffness, 1):
        L2 = K*pdot**2/2-stiff*gg/2-reg*lap**2/2
        momentum = s.diff(L2, pdot)
        ham = s.expand((pp*pdot-L2).subs(pdot, pp/K))
        check(f'B{n}_one_force_pair_and_nonnegative_quadratic_Hamiltonian',
              s.diff(momentum, pdot) == K
              and s.simplify(ham-(pp**2/(2*K)+stiff*gg/2+reg*lap**2/2)) == 0)
        dispersions.append(s.factor((stiff*k*k+reg*k**4)/K))
    check('B2_nonzero_modes_need_existing_positive_regulator', dispersions[1] == reg*k**4/K
          and dispersions[1].subs(reg, 0) == 0)

    # Amputated four-leg contact: derive it by differentiating the functional,
    # and compare with independent subset polarization, including mixed angles.
    coupling = lam/K**2
    t = s.symbols('t0:4', real=True)
    vecs = [s.Matrix(s.symbols(f'k{i}x k{i}y k{i}z', real=True)) for i in range(4)]
    wavegrad = sum((s.I*t[i]*vecs[i] for i in range(4)), s.zeros(3, 1))
    action4 = -coupling*(wavegrad.dot(wavegrad))**2
    vertex = s.diff(action4, *t).subs(dict.fromkeys(t, 0))
    pairings = (vecs[0].dot(vecs[1])*vecs[2].dot(vecs[3])
                +vecs[0].dot(vecs[2])*vecs[1].dot(vecs[3])
                +vecs[0].dot(vecs[3])*vecs[1].dot(vecs[2]))
    check('four_leg_vertex_sign_and_combinatorics', s.expand(vertex+8*coupling*pairings) == 0)
    examples = [([1, 2, 0], [-1, -2, 0], [0, -2, -1], [0, 2, 1]),
                ([1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 1, 0]),
                ([1, 0, 0], [-1, 0, 0], [-1, 0, 0], [1, 0, 0])]
    polarization_values = []
    for vectors in examples:
        vv = list(map(s.Matrix, vectors))
        # Inclusion-exclusion selects the coefficient of t0*t1*t2*t3 in a
        # homogeneous quartic, without differentiating or using pairings.
        direct = 0
        for bits in itertools.product([0, 1], repeat=4):
            total = sum((bits[i]*vv[i] for i in range(4)), s.zeros(3, 1))
            direct += (-1)**(4-sum(bits))*(-total.dot(total)**2)
        pairs = vv[0].dot(vv[1])*vv[2].dot(vv[3])+vv[0].dot(vv[2])*vv[1].dot(vv[3])+vv[0].dot(vv[3])*vv[1].dot(vv[2])
        polarization_values.append(dict(contact_over_coupling=int(direct), paired=int(-8*pairs)))
    check('independent_subset_polarization_on_elastic_integer_momenta',
          all(x['contact_over_coupling'] == x['paired'] for x in polarization_values), polarization_values)
    costheta = s.Symbol('cos_theta', real=True)
    com = -8*coupling*k**4*(1+2*costheta**2)
    check('finite_sigma_contact_at_right_angle_nonzero', s.simplify(com.subs(costheta, 0)+8*coupling*k**4) == 0)
    check('no_pure_force_cubic_vertex_at_homogeneous_origin',
          all(s.diff(f.subs(Y, eps**2*gg/ar**2), eps, 3).subs(eps, 0) == 0 for f in funcs))

    # Static equation includes the fourth derivative, even for B2.
    z = s.Symbol('z', real=True)
    amplitude = s.Symbol('amplitude', real=True)
    profile = amplitude*s.cos(z)
    fluxB2 = (3*B/(2*sigma*ar**4))*(k*s.diff(profile, z))**3
    nonlinear_static = s.expand_trig(k*s.diff(fluxB2, z))
    projected = s.integrate(nonlinear_static*s.cos(z), (z, 0, 2*s.pi))/s.pi
    regulator_static = -reg*k**4*profile
    check('B2_periodic_fundamental_nonlinear_static_response',
          s.simplify(projected+9*B*amplitude**3*k**4/(8*sigma*ar**4)) == 0)
    check('B2_small_amplitude_finite_wavelength_regulator_dominates',
          s.limit(s.cancel(projected/(-reg*k**4*amplitude)), amplitude, 0) == 0)
    check('torus_mean_source_constraint_retained',
          s.integrate(nonlinear_static+regulator_static, (z, 0, 2*s.pi)) == 0)

    transformed = {B: B/scale**3, sigma: scale*sigma, K: K/scale**2, reg: reg/scale**2}
    check('complete_smoothing_function_field_rescaling', all(s.simplify(
        f.subs({Y: scale**2*Y, sigma: scale*sigma}, simultaneous=True)-scale**3*f) == 0 for f in funcs))
    invariants = [stiffness[0]/K, reg/K, coupling]
    check('dispersion_and_canonical_contact_field_rescaling_invariants', all(
        s.simplify(x.subs(transformed, simultaneous=True)-x) == 0 for x in invariants))
    Cm = s.Symbol('C_m', real=True)
    check('matter_gradient_crossover_rescaling_invariant', s.simplify(
        (Cm*sigma*ar).subs({Cm: Cm/scale, sigma: scale*sigma}, simultaneous=True)-Cm*sigma*ar) == 0)
    # Independent high-precision function evaluation checks Taylor error bounds.
    mp.mp.dps = 70
    error_ratios = []
    for sig in [mp.mpf('0.125'), mp.mpf('1'), mp.mpf('3')]:
        for fraction in [mp.mpf('0.001'), mp.mpf('0.1'), mp.mpf('0.5')]:
            y = fraction*sig**2
            f1 = (y+sig**2)**mp.mpf('1.5')-sig**3
            poly = mp.mpf('1.5')*sig*y+mp.mpf(3)*y*y/(8*sig)-y**3/(16*sig**3)
            rem = f1-poly
            upper = 3*y**4/(128*sig**5)
            lower = 3*y**4/(128*(sig**2+y)**mp.mpf('2.5'))
            error_ratios.append(float(rem/upper))
            assert lower <= rem <= upper, (sig, fraction, rem)
    check('independent_numeric_Taylor_remainder_enclosure',
          all(0 < r <= 1 for r in error_ratios), error_ratios)
    check('input_bytes_sidecars_and_timestamps_preserved',
          all(sha(p) == h and p.stat().st_mtime_ns == tm for p, (h, tm) in snapshot.items()))
    return dict(kind='UVIR003_U3_ANALYTIC_CONTROLS_V1', source_sha256=pins,
                checks=checks, passed=sum(c['passed'] for c in checks), total=len(checks),
                dimensions=dimensions,
                definitions=dict(Y='I/a_ref^2; I=|D psi|^2', Q='U.d psi (unnormalized)',
                                 sigma='CONTROL_SCALE_NOT_DERIVED; dimensionless; raw scale sigma*a_ref',
                                 B='mass^4; A_raw=B/a_ref^3; no microscopic matching',
                                 r_reg='gamma/M_*^2, existing spatial regulator'),
                branches=[dict(name=f'B{i+1}', function=str(f), series=str(series[i]),
                               constitutive_mu=str(mus[i]), dispersion=str(dispersions[i]),
                               direct_ADM_L2_L3_L4=list(map(str, adm[i])),
                               homogeneous_force_pairs=1) for i, f in enumerate(funcs)],
                analytic_domain='sigma>0, real Y>-sigma^2; Taylor about 0 converges for |Y|<sigma^2; physical Y>=0',
                remainder='0< R_after_Y3 <= 3Y^4/(128sigma^5); lower bound 3Y^4/[128(sigma^2+Y)^(5/2)] for Y>0',
                static_equation='div[(2B/a_ref^2)F_i_prime(Y)D psi]-r_reg*Delta^2 psi=C_m*delta_rho in fixed flat frame; torus integral C_m*delta_rho=0',
                canonical_contact=dict(chi='sqrt(K)*pi', coefficient_g4=str(coupling),
                                       convention='iM_contact=-i*8*g4*sum_of_three_spatial_pairings; all four spatial momenta incoming',
                                       COM_amputated_M=str(com), B2_status='FINITE_FORCE_ONLY_CONTACT_KERNEL_FOR_SIGMA_POSITIVE_AND_K_POSITIVE',
                                       external_dispersion='omega_k^2=r_reg*k^4/K for B2; k=0 is a separate shift collective coordinate',
                                       exclusions='Not full exchange+contact, coupled cosmological amplitude, compact-space asymptotic S-matrix, optical theorem or physical cutoff'),
                local_DOF_scope='No fields or higher time derivatives added; one factorized homogeneous force scalar; other host block and nonlinear global rank not certified',
                full_U3='OPEN_NO_UV_ORIGIN_MATCHING_OR_ACTION_ADOPTION',
                screen='COMPLETE_SCOPED_B1_B2_ANALYTIC_CONTROLS', review='DEFERRED',
                physics_pass=False, gate_effect='NONE', UVIR003='IN_PROGRESS', MAT001='BLOCKED',
                K_Q='NOT_DERIVED', live_TrackA_V='NOT_COMPUTED')


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
                          screen=data['screen'], physics_pass=False)))
    if data['passed'] != data['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
