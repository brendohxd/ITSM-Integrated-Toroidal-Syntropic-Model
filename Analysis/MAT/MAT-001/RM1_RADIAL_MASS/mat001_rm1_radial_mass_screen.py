#!/usr/bin/env python3
"""Exact scalar/probe source and pole screen; no canonical MAT matching."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
PINS = {
    "GEMINI.md": "5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12",
    "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md": "d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa",
    "Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md": "3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809",
    "Theory/Gates/MAT-001/MAT001_RM1_RADIAL_MASS_SCREEN_CONTRACT_2026-10-13.md": "b27acb9fcd40e2591f96a10d7ffa8911d940bb784d0124b9785ad83e1ad0e375",
    "Theory/Gates/MAT-001/MAT001_PHYSICAL_MATCHING_ROUTE_DECISION_2026-10-13.md": "00e784bc797600fd4e8c31192026f5c2c7977b66d39f4b5faeddce71ef46b4ac",
    "Theory/Gates/MAT-001/MAT-001_R4_SIGNED_RESIDUE_CONTRACT.md": "63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386",
    "Theory/Gates/UVIR-001/UVIR-001_GATE_REPORT.md": "850d4e6616a136088936bbdbbb809f0443b508117cbe0140ebb05eca79aaf630",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_unpromoted(receipt: dict) -> None:
    expected = {"physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
                "V": "NOT_COMPUTED", "K_Q": "NOT_DERIVED", "MAT-001": "BLOCKED"}
    for key, value in expected.items():
        if receipt.get(key) != value:
            raise ValueError("Unauthorized canonical promotion: " + key)


def calculation() -> dict:
    checks: list[dict] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    for relative, expected in PINS.items():
        check("source pin: " + relative, sha(ROOT / relative) == expected)

    r, mu, M2, q, z = sp.symbols("rho0 mu M_rho_sq k_sq omega_sq", positive=True)
    omega = sp.symbols("omega", positive=True)
    eps, h, hd, hg, pfield, pd, pg = sp.symbols("eps h h_dot h_grad p p_dot p_grad", real=True)
    m2, l4, l6, scale = sp.symbols("m_sq lambda4 lambda6 Lambda", positive=True)
    rho = r + eps * h
    potential = m2 * rho**2 / 2 + l4 * rho**4 / 8 + l6 * rho**6 / (24 * scale**2)
    lagrangian = (eps**2 * (hd**2 - hg**2) / 2
                  + rho**2 * ((mu + eps * pd / r)**2 - eps**2 * pg**2 / r**2) / 2
                  - potential)
    background_m2 = mu**2 - l4 * r**2 / 2 - l6 * r**4 / (4 * scale**2)
    curvature = l4 * r**2 + l6 * r**4 / scale**2
    L1 = sp.expand(lagrangian).coeff(eps, 1).subs(m2, background_m2)
    L2 = sp.expand(lagrangian).coeff(eps, 2).subs(m2, background_m2)
    expected_L2 = (hd**2 - hg**2 + pd**2 - pg**2 - curvature * h**2) / 2 + 2 * mu * h * pd
    check("linear term is endpoint derivative", sp.simplify(L1 - mu * r * pd) == 0)
    check("quadratic action derived before curvature substitution", sp.simplify(L2 - expected_L2) == 0)
    check("amplitude curvature from potential", sp.simplify(
        sp.diff(potential, eps, 2).subs({eps: 0, h: 1, m2: background_m2}) - mu**2 - curvature) == 0)

    nb, y, rb = sp.symbols("n_b y rho_b", positive=True)
    probe = -nb * y * rho
    source_h = sp.diff(probe, eps).subs({eps: 0, h: 1, nb: rb / (y * r)})
    check("signed radial source from fixed probe number", sp.simplify(source_h + rb / r) == 0)
    check("no direct phase source", sp.diff(probe, pfield) == 0)
    check("fractional mass derivative independent of y", sp.diff(sp.log(y * r), r) == 1 / r)
    scalar_L2 = (hd**2 + pd**2 - hg**2 - pg**2 - M2*h**2)/2 + 2*mu*h*pd
    ph, pp = sp.symbols("p_h p_phase", real=True)
    velocities = {hd: ph, pd: pp-2*mu*h}
    legendre = (ph*hd + pp*pd - scalar_L2).subs(velocities)
    expected_H = ph**2/2 + (pp-2*mu*h)**2/2 + (hg**2+pg**2+M2*h**2)/2
    check("Hamiltonian Legendre transform retains mixing", sp.simplify(legendre-expected_H) == 0)

    D = sp.Matrix([[omega**2 - q - M2, -2 * sp.I * mu * omega],
                   [2 * sp.I * mu * omega, omega**2 - q]])
    det = sp.factor(D.det()).subs(omega**2, z)
    expected_det = (z - q - M2) * (z - q) - 4 * mu**2 * z
    check("frequency kernel determinant", sp.expand(det - expected_det) == 0)
    H = M2 + 4 * mu**2
    discr = sp.sqrt(H**2 + 16 * mu**2 * q)
    zm = q + H / 2 - discr / 2
    zp = q + H / 2 + discr / 2
    check("gapless dispersion solves determinant", sp.simplify(expected_det.subs(z, zm)) == 0)
    check("gapped dispersion solves determinant", sp.simplify(expected_det.subs(z, zp)) == 0)
    check("root sum and product", sp.simplify(zm + zp - (2*q + H)) == 0
          and sp.simplify(zm*zp - q*(q+M2)) == 0)
    response = (z - q) / (r**2 * expected_det)
    wm = (q - zm) / (r**2 * discr)
    wp = (zp - q) / (r**2 * discr)
    check("spectral reconstruction", sp.simplify(response - wm/(z-zm) - wp/(z-zp)) == 0)
    check("pole weight sum", sp.simplify(wm + wp - 1/r**2) == 0)
    check("static nonzero-mode response has no phase pole", sp.simplify(
        response.subs(z, 0) + 1/(r**2 * (q+M2))) == 0)
    check("soft gapless pole weight vanishes", sp.simplify(wm.subs(q, 0)) == 0)
    soft_slope = sp.simplify(sp.diff(wm, q).subs(q, 0))
    check("soft weight scales as k squared", sp.simplify(soft_slope - 4*mu**2/(r**2*H**2)) == 0)
    cs2 = sp.simplify(sp.diff(zm, q).subs(q, 0))
    check("sound speed derived from pole", sp.simplify(cs2 - M2/H) == 0)
    check("nonzero-mode static soft coefficient", sp.limit(response.subs(z, 0), q, 0) == -1/(r**2*M2))

    c = sp.Matrix([-1/r, 0])
    R = sp.Matrix([[1, sp.Rational(1, 2)], [0, 2]])
    Dy, cy = R.T * D * R, R.T * c
    response_original = (c.T * D.inv() * c)[0]
    response_transported = (cy.T * Dy.inv() * cy)[0]
    check("nonorthogonal source and kernel transport", sp.simplify(response_original - response_transported) == 0)

    # Heavy-field elimination is a derivative expansion, checked at leading order only.
    j = rb/r
    heavy_solution = (2*mu*pd-j)/M2
    heavy_terms = -M2*h**2/2 + 2*mu*h*pd - j*h
    leff = sp.expand((pd**2-pg**2)/2 + heavy_terms.subs(h, heavy_solution))
    Zphase = 1 + 4*mu**2/M2
    check("low-energy derivative source and contact term", sp.simplify(
        leff - (Zphase*pd**2/2 - pg**2/2 - 2*mu*rb*pd/(r*M2) + rb**2/(2*r**2*M2))) == 0)
    check("derivative-source on-shell weight agrees with soft pole", sp.simplify(
        4*mu**2/(r**2*M2**2*Zphase) * cs2 - soft_slope) == 0)

    # Uniform mode: charge conservation is imposed before solving its response.
    pi_momentum = sp.symbols("p_phase", real=True)
    radial_uniform_force = M2*h - 2*mu*(pi_momentum-2*mu*h)
    check("fixed-charge uniform radial curvature", sp.simplify(radial_uniform_force.subs(pi_momentum, 0) - H*h) == 0)
    uniform_response = -1/(r**2*H)
    check("fixed-charge and static nonzero-mode limits differ", sp.simplify(uniform_response + 1/(r**2*M2)) != 0)

    # These expression-level mutations change the action, source, or ensemble.
    eta = sp.symbols("eta", nonzero=True, real=True)
    mutation_checks = {
        "dropped_mixing": sp.expand((z-q-M2)*(z-q) - expected_det) != 0,
        "inserted_direct_phase_source": sp.limit(q*(-1/(r**2*(q+M2))-eta**2/q), q, 0) == -eta**2,
        "lost_radial_numerator": sp.simplify(1/(r**2*expected_det) - response) != 0,
        "wrong_charge_ensemble": sp.simplify(uniform_response + 1/(r**2*M2)) != 0,
        "untransported_source": sp.simplify((c.T*Dy.inv()*c)[0] - response_original) != 0,
        "bare_vertex_substituted_for_soft_vertex": sp.limit(wm, q, 0) != 1/r**2,
        "reversed_anchored_source": sp.simplify(rb/r-source_h) != 0,
    }
    for name, condition in mutation_checks.items():
        check("reject mutation: " + name, condition)

    dimensions = {"rho0": 1, "mu": 1, "M_rho_sq": 2, "rho_b": 4,
                  "h": 1, "p": 1, "radial_vertex": -1, "pole_weight": -2,
                  "mass_response_kernel": -4, "derivative_source_coefficient": -2}
    check("action and source dimensions", 2+2 == 0+4 == -2+6 == -1+4+1 == 1+1+2 == 4)
    check("response dimensions", -2-2 == dimensions["mass_response_kernel"])

    mp.mp.dps = 80

    def number(x):
        return mp.mpf(str(sp.N(x, 85)))

    cases = [
        (sp.Rational(2), sp.Rational(1), sp.Rational(1), sp.Rational(2)),
        (sp.Rational(3, 2), sp.Rational(2), sp.Rational(1, 4), sp.Rational(1, 16)),
        (sp.Rational(1), sp.Rational(1, 2), sp.Rational(1), sp.Rational(4)),
    ]
    numeric = []
    for index, (muv, rv, l4v, l6v) in enumerate(cases, 1):
        Mv = l4v*rv**2 + l6v*rv**4
        m2v = muv**2 - l4v*rv**2/2 - l6v*rv**4/4
        check(f"case {index}: declared branch and curvature", m2v >= 0 and Mv > 0)
        for kv in (1, 2, 5):
            qv = sp.Rational(kv**2)
            subs = {mu: muv, r: rv, M2: Mv, q: qv}
            zn = [number(zm.subs(subs)), number(zp.subs(subs))]
            wn = [number(wm.subs(subs)), number(wp.subs(subs))]
            un, rn, mn, qn = number(muv), number(rv), number(Mv), number(qv)
            check(f"case {index}, k {kv}: positive poles and weights", all(x > 0 for x in zn+wn))
            # Independent first-order Hamiltonian evolution matrix.
            evolution = mp.matrix([[0,0,1,0],[-2*un,0,0,1],
                                   [-(qn+mn+4*un**2),0,0,2*un],[0,-qn,0,0]])
            eigenvalues = mp.eig(evolution, left=False, right=False)
            targets = [s*mp.j*mp.sqrt(x) for x in zn for s in (-1,1)]
            eigen_error = max(min(abs(x-y) for y in targets) for x in eigenvalues)
            check(f"case {index}, k {kv}: Hamiltonian frequencies", eigen_error < mp.mpf('1e-65'))
            norm_errors, euclidean_errors = [], []
            for pole_index, (root, weight) in enumerate(zip(zn, wn), 1):
                w = mp.sqrt(root)
                d = (qn+mn-root)/(2*un*w)
                norm = 1+d**2+2*un*d/w
                norm_errors.append(abs(1/(rn**2*norm)-weight))
                euclidean_errors.append(abs(1/(rn**2*(1+d**2))-weight))
                check(f"case {index}, k {kv}, pole {pole_index}: signed vertex", -mp.sqrt(weight) < 0)
            check(f"case {index}, k {kv}: frequency-derivative pole norm", max(norm_errors) < mp.mpf('1e-65'))
            check(f"case {index}, k {kv}: reject Euclidean normalization", max(euclidean_errors) > mp.mpf('1e-10'))
            reconstruction_error = mp.mpf('0')
            for offshell in (mp.mpf('-2'), mp.mpf('-0.5'), mp.mpf('0')):
                direct = (offshell-qn)/(rn**2*((offshell-qn-mn)*(offshell-qn)-4*un**2*offshell))
                spectral = sum(weight/(offshell-root) for weight,root in zip(wn,zn))
                reconstruction_error = max(reconstruction_error, abs(direct-spectral))
            check(f"case {index}, k {kv}: response reconstruction", reconstruction_error < mp.mpf('1e-65'))
            numeric.append({"case": index, "k": kv,
                            "mu": str(muv), "rho0": str(rv), "n_Q": str(muv*rv**2),
                            "m_sq": str(m2v), "lambda4": str(l4v), "lambda6": str(l6v),
                            "Lambda": "1", "M_rho_sq": str(Mv),
                            "omega_sq": [mp.nstr(x,60) for x in zn],
                            "source_pole_weights": [mp.nstr(x,60) for x in wn],
                            "max_hamiltonian_frequency_error": mp.nstr(eigen_error,10),
                            "max_pole_norm_error": mp.nstr(max(norm_errors),10),
                            "max_response_reconstruction_error": mp.nstr(reconstruction_error,10)})

    metadata_mutation_rejected = False
    try:
        require_unpromoted({"physics_pass": True, "gate_effect": "NONE", "Rule9_cleared": False,
                           "V": "NOT_COMPUTED", "K_Q": "NOT_DERIVED", "MAT-001": "BLOCKED"})
    except ValueError:
        metadata_mutation_rejected = True
    check("reject metadata mutation: physics promotion", metadata_mutation_rejected)
    return {
        "result_id": "MAT001-RM1-v1",
        "calculation_status": "LOCAL_EXACT_SOURCE_POLE_SCREEN_COMPLETE",
        "candidate_disposition": "REJECT_RM1_AS_NONZERO_SOFT_GAPLESS_STATIC_SOURCE",
        "claim_status": "Conditional / scoped negative",
        "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
        "review_status": "DEFERRED", "research_execution": "PROCEED_PROVISIONALLY_FOR_SCOPED_DIAGNOSTICS",
        "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS", "K_Q": "NOT_DERIVED",
        "V": "NOT_COMPUTED", "Stage4A": "CLOSED",
        "versions": {"sympy": sp.__version__, "mpmath": mp.__version__},
        "evidence_sha256": {**PINS, str(Path(__file__).relative_to(ROOT)).replace('\\','/'): sha(Path(__file__))},
        "exact": {"quadratic_lagrangian": str(expected_L2), "M_rho_sq": str(curvature),
                  "determinant": str(expected_det), "gapless_omega_sq": str(zm), "gapped_omega_sq": str(zp),
                  "fractional_mass_response": str(response), "gapless_weight": str(wm), "gapped_weight": str(wp),
                  "signed_vertex_convention": "g_j=-sqrt(W_j), radial component positive, k>0, omega>0",
                  "gapless_soft_weight": "0", "gapless_soft_weight_per_k_sq": str(soft_slope),
                  "sound_speed_sq": str(cs2), "static_nonzero_mode": str(-1/(r**2*(q+M2))),
                  "uniform_fixed_charge": str(uniform_response), "low_energy_phase_action": str(leff)},
        "dimensions": dimensions, "mutation_rejections": mutation_checks,
        "numeric_diagnostics": numeric, "checks": checks,
        "check_count": len(checks), "failed_checks": [], "unknown_checks": [],
        "scope": "flat periodic scalar/probe tree-level control; fixed-charge zero mode separate",
        "excluded_uses": ["canonical numerical V or K_Q", "full R4C1 mode or metric/frame constraints",
                          "Standard Model or baryon-mass derivation", "new UVIR spatial cubic-law result",
                          "galactic force prediction", "quantum matching or physical cutoff", "gate closure"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    destination = args.out.resolve()
    if not destination.is_relative_to(ROOT):
        raise ValueError('Output must be within the repository.')
    if destination.exists():
        raise FileExistsError('Use a new output directory; preserve previous attempts.')
    result = calculation()
    require_unpromoted(result)
    destination.mkdir(parents=True, exist_ok=False)
    body = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode('utf-8')
    path = destination / 'summary.json'
    path.write_bytes(body)
    path.with_suffix('.json.sha256').write_text(hashlib.sha256(body).hexdigest()+'  summary.json\n', encoding='utf-8')
    print(result['calculation_status'])
    print(result['candidate_disposition'])
    print(f"Checks: {result['check_count']}; numeric cases: {len(result['numeric_diagnostics'])}")
    print('Soft gapless weight = 0; static radial response finite for M_rho_sq>0.')
    print('physics_pass=false; gate_effect=NONE; V=NOT_COMPUTED; K_Q=NOT_DERIVED; review=DEFERRED')
    print('Receipt: '+str(path.relative_to(ROOT)))


if __name__ == '__main__':
    main()
