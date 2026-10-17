"""Deterministic, non-promoting COMPACT E1 geometry/response methods checks."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PINS = {
    'GEMINI.md': '5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
    'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md': 'd6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa',
    'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md': '3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
    'Theory/Core/ITSM_Master_Research_Plan.md': '6ac906c0050eb9c4395953b6cdbb0d9aed696bce0b0f7cf4f8c8606a4f781ba3',
    'Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md': '81c7138568d44fd3197b88cb21efe67b17c406ada941f7ff778c2f8821ae074b',
    'Theory/Gates/MAT-001/MAT-001_R5_MICROSCOPIC_MATCHING_DECISION.md': 'ab8e743913f2e4fd0f5823581514345d598b2d1a1eb92e6d0d04f57447ed69b4',
    'Theory/Gates/VOR-001/VOR_TOP_PHASE_WINDING_NORMALIZATION_SPEC_2026-09-05.md': '0c7b9b976c3a3bb93c14b804233f721b5b9540b56739800c3a56b3bbd0ebd308',
    'Theory/Gates/ITSM_TEST_02_T3_TOPOLOGY_ADDENDUM_2026-09-25.md': 'a4f251ff3d751a60ff4130d61a060f199c825604f877e1aeb5dd5515db8f317c',
    'active_research.md': '40d7859b67452a65040665ac1d52f133896234293023dcdda496076802aac2f0',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wire(value):
    if isinstance(value, s.MatrixBase):
        return [[str(x) for x in row] for row in value.tolist()]
    return str(value)


class Audit:
    def __init__(self):
        self.rows = []

    def add(self, name, passed, evidence=''):
        self.rows.append(dict(name=name, passed=bool(passed), evidence=str(evidence)))

    def exact(self, name, residual):
        entries = list(residual) if isinstance(residual, s.MatrixBase) else [residual]
        reduced = [s.simplify(v) for v in entries]
        self.add(name, all(v == 0 for v in reduced), wire(residual))


def wave(T, n):
    return 2*s.pi*T.inv().T*s.Matrix(n)


def pt(v):
    return s.eye(3) - v*v.T/v.dot(v)


def shell(T, labels):
    # Work in k/(2*pi) to keep shell ordering exact and rational.
    rows = [(n, T.inv().T*s.Matrix(n)) for n in labels]
    minimum = min(v.dot(v) for _, v in rows)
    return [(n, v) for n, v in rows if v.dot(v) == minimum], minimum


def mean_projector(rows, weights=None):
    weights = weights or [s.Integer(1)]*len(rows)
    return sum((w*pt(v) for (_, v), w in zip(rows, weights)), s.zeros(3))/sum(weights)


def geometry(a):
    labels = [n for n in itertools.product((-1, 0, 1), repeat=3) if any(n)]
    lattices = dict(cubic=s.eye(3), rectangular=s.diag(1, 1, 2),
                    oblique=s.Matrix([[2, s.Rational(1, 2), s.Rational(1, 3)],
                                      [0, 3, s.Rational(1, 4)], [0, 0, 4]]))
    maps = [s.Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]]), s.diag(-1, 1, 1)]
    result = []
    for name, T in lattices.items():
        volume = abs(T.det())
        a.add(name+'_nonsingular_volume', volume > 0, volume)
        for index, n in enumerate(labels):
            k = wave(T, n)
            a.exact(f'{name}_reciprocal_{index}', T.T*k - 2*s.pi*s.Matrix(n))
            for column in range(3):
                a.exact(f'{name}_periodic_{index}_{column}',
                        s.exp(s.I*(k.dot(T[:, column]))) - 1)
            a.exact(f'{name}_PT_idempotent_{index}', pt(k)**2 - pt(k))
            a.exact(f'{name}_PT_trace_{index}', s.trace(pt(k)) - 2)
            a.exact(f'{name}_scalar_gradient_annihilated_{index}', pt(k)*k)
            for j, M in enumerate(maps):
                a.exact(f'{name}_GL_{j}_mode_{index}',
                        wave(T*M, M.T*s.Matrix(n)) - k)
        for j, M in enumerate(maps):
            a.exact(f'{name}_GL_{j}_volume', abs((T*M).det()) - volume)
        # The generic exponential is an exact Laplacian eigenfunction.
        x = s.Matrix(s.symbols('x0:3', real=True))
        k = wave(T, (1, -1, 1))
        u = s.exp(s.I*k.dot(x))/s.sqrt(volume)
        a.exact(name+'_Laplacian_eigenvalue',
                sum(s.diff(u, z, 2) for z in x) + k.dot(k)*u)
        first, knorm2 = shell(T, labels)
        mean = mean_projector(first)
        result.append(dict(name=name, T=wire(T), volume=str(volume),
                           enumerated_nonzero_modes=len(labels),
                           lowest_shell_n=[list(n) for n, _ in first],
                           lowest_shell_k2=str(4*s.pi**2*knorm2),
                           lowest_shell_mean_PT=wire(mean)))
    cubic, _ = shell(lattices['cubic'], labels)
    rectangular, _ = shell(lattices['rectangular'], labels)
    a.exact('cubic_six_mode_mean', mean_projector(cubic) - s.Rational(2, 3)*s.eye(3))
    a.exact('rectangular_two_mode_mean', mean_projector(rectangular) - s.diag(1, 1, 0))
    # Source weights, not an inferred source law; inversion pair symmetry retained.
    weights = [s.Integer(4) if n[2] else s.Integer(1) for n, _ in cubic]
    weighted = mean_projector(cubic, weights)
    a.exact('cubic_weighted_mean', weighted - s.diag(s.Rational(5, 6), s.Rational(5, 6), s.Rational(1, 3)))
    a.exact('weighted_trace_still_two', s.trace(weighted) - 2)
    a.add('reject_universal_2_over_3_rectangular', mean_projector(rectangular) != s.Rational(2, 3)*s.eye(3))
    a.add('reject_universal_2_over_3_source_weighted', weighted != s.Rational(2, 3)*s.eye(3))
    T = lattices['oblique']; n = s.Matrix([1, 2, 3]); M = maps[0]
    a.add('reject_missing_2pi', T.T*(T.inv().T*n) != 2*s.pi*n)
    a.add('reject_inverse_not_inverse_transpose', T.T*(2*s.pi*T.inv()*n) != 2*s.pi*n)
    a.add('reject_wrong_GL_label_transport', wave(T*M, M*n) != wave(T, n))
    a.add('reject_omitted_volume_normalization', abs(T.det()) != 1, abs(T.det()))
    return lattices, result, wire(weighted)


def numerical(a, lattices):
    mp.mp.dps = 80
    labels = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, -1, 1)]
    points = list(itertools.product(range(5), repeat=3))
    residuals = []
    covariance_errors = []
    for name, Ts in lattices.items():
        T = mp.matrix([[mp.mpf(str(v.p))/mp.mpf(str(v.q)) for v in row]
                       for row in Ts.tolist()])
        volume = abs(mp.det(T)); reciprocal = T**-1
        reciprocal = reciprocal.T
        position = mp.matrix([mp.mpf('0.17'), mp.mpf('0.23'), mp.mpf('-0.31')])
        ks = [2*mp.pi*(reciprocal*mp.matrix(n)) for n in labels]
        samples = []
        for p in points:
            x = T*mp.matrix([(mp.mpf(j)+mp.mpf('0.5'))/5 for j in p])
            samples.append([mp.exp(mp.j*sum(k[j]*(x[j]-position[j]) for j in range(3)))/mp.sqrt(volume) for k in ks])
        error = mp.mpf(0)
        for i in range(len(labels)):
            for j in range(len(labels)):
                overlap = volume*mp.fsum(mp.conj(row[i])*row[j] for row in samples)/125
                error = max(error, abs(overlap - int(i == j)))
        a.add(name+'_independent_quadrature_80digits', error < mp.mpf('1e-70'), mp.nstr(error, 14))
        residuals.append(dict(name=name, max_overlap_error=mp.nstr(error, 14)))
        # Artificial positive Gram weights and real feature functions, not CMB.
        C0 = mp.matrix(4); Cx = mp.matrix(4); positive_form = mp.mpf(0)
        test = [mp.mpf(1), mp.mpf(2), mp.mpf(-1), mp.mpf(3)]
        for k in ks[1:]:
            k2 = mp.fsum(z*z for z in k); weight = 1/(1+k2)
            feature = [mp.mpf(1)] + [z/mp.sqrt(k2) for z in k]
            phase = mp.exp(-mp.j*sum(k[j]*position[j] for j in range(3)))
            for i in range(4):
                for j in range(4):
                    C0[i,j] += weight*feature[i]*feature[j]
                    Cx[i,j] += weight*(phase*feature[i])*mp.conj(phase*feature[j])
            positive_form += weight*abs(mp.fsum(test[i]*feature[i] for i in range(4)))**2
        covariance_error = max(abs(C0[i,j]-Cx[i,j]) for i in range(4) for j in range(4))
        quadratic = mp.fsum(test[i]*Cx[i,j]*test[j] for i in range(4) for j in range(4))
        a.add(name+'_toy_covariance_observer_independent', covariance_error < mp.mpf('1e-70'), mp.nstr(covariance_error,14))
        a.add(name+'_toy_covariance_Gram_positive', positive_form >= 0 and abs(quadratic-positive_form) < mp.mpf('1e-70'), mp.nstr(positive_form,14))
        covariance_errors.append(dict(name=name, observer_phase_error=mp.nstr(covariance_error,14)))
    y = s.symbols('y', real=True)
    for difference in range(-2, 3):
        a.exact('analytic_cell_overlap_'+str(difference),
                s.integrate(s.exp(2*s.pi*s.I*difference*y), (y,0,1)) - int(difference == 0))
    return dict(precision_decimal=80, midpoint_grid=[5,5,5],
                includes_zero_mode=True, orthogonality=residuals,
                toy_covariance=covariance_errors,
                covariance_scope='Artificial Gram features/weights only; no CMB or primordial spectrum')


def response(a):
    K, B, scale, k2 = s.symbols('K B scale k2', positive=True)
    Cm, rho, w2, m2 = s.symbols('Cm rho omega2 m2', real=True)
    V = Cm/s.sqrt(K); freq2 = B*k2/K + m2
    bare = Cm*rho/(K*(w2-freq2))
    canonical = V*rho/(w2-freq2)
    observable = Cm*bare
    a.exact('canonical_one_vertex', s.sqrt(K)*bare - canonical)
    a.exact('observable_two_vertices', observable - V**2*rho/(w2-freq2))
    a.exact('Euler_source_sign', (-K*w2+B*k2+K*m2)*bare + Cm*rho)
    a.exact('static_massive_sign', observable.subs(w2,0) + Cm**2*rho/(B*k2+K*m2))
    a.exact('static_massless', observable.subs({w2:0,m2:0}) + Cm**2*rho/(B*k2))
    a.exact('field_chart_V', (Cm/scale)/s.sqrt(K/scale**2) - V)
    a.exact('field_chart_frequency', (B/scale**2)/(K/scale**2) - B/K)
    a.exact('field_chart_observable', observable.subs({K:K/scale**2,B:B/scale**2,Cm:Cm/scale},simultaneous=True) - observable)
    a.exact('static_times_dispersion_identifies_V_squared', (Cm**2/B)*(B/K) - V**2)
    a.exact('zero_massless_denominator', (K*w2-B*k2-K*m2).subs({w2:0,k2:0,m2:0}))
    omega = s.symbols('omega', real=True)
    pole = s.symbols('Omega_n', positive=True)
    a.exact('omega_plane_single_vertex_residue',
            s.limit((omega-pole)*V/(omega**2-pole**2), omega, pole) - V/(2*pole))
    a.exact('massive_zero_mode_static', observable.subs({w2:0,k2:0}) + Cm**2*rho/(K*m2))
    a.add('reject_bare_vertex_as_V', (Cm/K-V).subs({Cm:1,K:4}) != 0)
    a.add('reject_two_vertex_as_signed_V', (V**2-V).subs({Cm:-1,K:4}) != 0)
    a.add('reject_K_from_volume', V.subs({Cm:1,K:1}) != V.subs({Cm:1,K:4}), 'Same lattice; independent K changes normalized vertex')
    families = []
    for fixed in ('frequency', 'static_transfer'):
        rows = []
        for kval in (1,4,9):
            bval = s.Rational(kval,4) if fixed == 'frequency' else s.Rational(1,4)
            rows.append(dict(K=str(kval), B=str(bval), Cm='1',
                             V_control=str(1/s.sqrt(kval)),
                             cs2=str(bval/kval),
                             static_amplitude=str(1/bval),
                             pole_omega2_over_k2=str(bval/kval)))
        unchanged = 'cs2' if fixed == 'frequency' else 'static_amplitude'
        a.add(f'reject_{fixed}_only_matching', len({r[unchanged] for r in rows}) == 1 and len({r['V_control'] for r in rows}) == 3, rows)
        families.append(dict(fixed=fixed, rows=rows))
    # Generic matrix-interface invariant, not a constrained parent computation.
    D = s.Matrix([[5,1],[1,3]]); j = s.Matrix([1,2]); c = s.Matrix([3,-1])
    S = s.Matrix([[2,1],[0,3]]); inverse = S.inv()
    transformed_D = inverse.T*D*inverse
    transformed_j = inverse.T*j; transformed_c = inverse.T*c
    a.exact('matrix_response_chart_invariance',
            (transformed_c.T*transformed_D.inv()*transformed_j)[0] - (c.T*D.inv()*j)[0])
    return dict(action='K/2 dt(psi)^2 - B/2 grad(psi)^2 - K*m2/2 psi^2 - Cm*rho*psi',
                conditional_only=True, control_K_is_not_live_KQ=True,
                bare_response=str(bare), canonical_response=str(canonical),
                matter_log_mass_response=str(observable),
                retarded_prescription='omega -> omega+i0, exp(-i omega t)',
                single_vertex_omega_plane_residue='V_control/(2*Omega_n), not the vertex itself',
                static_massless='-Cm^2 rho_n/(B k_n^2), n!=0',
                response_to_constant_massless_static_source='No inverse; require compatible zero mean or separate homogeneous dynamics',
                matrix_interface='c_n^T D_n(omega,k)^(-1) j_n; live constrained D,c,j not computed',
                coefficient_counterfamilies=families)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE/'outputs'/'attempt_01')
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT):
        raise SystemExit('Output must remain in the repository')
    target = output/'summary.json'
    if target.exists() or target.with_suffix('.json.sha256').exists():
        raise SystemExit('Refuse to overwrite prior evidence')
    a = Audit(); pins = []
    for name, expected in PINS.items():
        actual = digest(ROOT/name)
        a.add('pin_'+name, actual == expected, actual)
        pins.append(dict(path=name, expected_sha256=expected, actual_sha256=actual))
    if any(not row['passed'] for row in a.rows):
        print(json.dumps(dict(status='STOP_SOURCE_PIN_FAILURE', failures=[r for r in a.rows if not r['passed']]), indent=2))
        return 1
    lattices, lattice_rows, weighted = geometry(a)
    numeric = numerical(a, lattices)
    scalar = response(a)
    failures = [r for r in a.rows if not r['passed']]
    payload = dict(schema='itsm-compact-t3-methods-v1',
                   status='PASS_BOUNDED_METHODS_HOLD_MATCHING' if not failures else 'FAIL_BOUNDED_METHODS',
                   claim_status='Conditional', review_status='DEFERRED',
                   continuation='PROCEED_PROVISIONALLY_METHODS_ONLY',
                   physics_pass=False, gate_effect='NONE', Rule9_cleared=False,
                   MAT_001='BLOCKED', UVIR_003='IN_PROGRESS', K_Q='NOT_DERIVED',
                   V='NOT_COMPUTED', Stage4A='CLOSED', Tests_1_3='HOLD_SUBSTANTIVE',
                   substantive_blockers=['No selected on-shell physical mode or matter residue',
                                        'No microscopic Cm/KQ or nonlinear coefficient relation',
                                        'No action-derived state/spectrum/transfer or physical scale'],
                   local_checks=dict(total=len(a.rows), passed=len(a.rows)-len(failures), failed=len(failures)),
                   failures=failures, source_pins=pins,
                   script_sha256=digest(Path(__file__)),
                   contract_sha256=digest(HERE/'CONTRACT_2026-10-14.md'),
                   literature=[dict(url='https://arxiv.org/html/2306.17112v3', equations='4.20-4.27', role='Geometry and statistical transfer method; not coefficient matching'),
                               dict(url='https://arxiv.org/abs/2610.12418',role='Weekly lens-space literature trail only')],
                   lattices=lattice_rows, source_weighted_cubic_PT=weighted,
                   numerical_controls=numeric, scalar_control=scalar, checks=a.rows)
    output.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=True)+'\n', encoding='utf-8', newline='\n')
    target.with_suffix('.json.sha256').write_text(digest(target)+'\n', encoding='ascii', newline='\n')
    print(json.dumps(dict(status=payload['status'], local_checks=payload['local_checks'],
                          failures=failures, physics_pass=False, gate_effect='NONE',
                          receipt=str(target), sha256=digest(target)), indent=2))
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
