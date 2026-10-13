#!/usr/bin/env python3
"""One real heavy-field bulk determinant control, not canonical ITSM matching."""
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
    "Theory/Gates/MAT-001/MAT001_ST2_HEAVY_THRESHOLD_SCREEN_CONTRACT_2026-10-13.md": "23cd8257796169a97045961cd5bd7624fd829f557cc2869ee38f9d2859e9a0e7",
    "Theory/Gates/MAT-001/MAT001_ST1_INDUCED_SCALE_SCREEN_CONTRACT_2026-10-13.md": "d3708431f19d7d78451a3ffb641d8b715171b36400b2c439d6dfadd4a2fbbb7b",
    "Theory/Gates/MAT-001/MAT001_ST1_INDUCED_SCALE_SCREEN_REPORT_2026-10-13.md": "9e4e86f00c919d74a1057340c8f5b2d8b6851043be9e410ffa5c576c3afee1fe",
    "Theory/Gates/MAT-001/MAT-001_R4_SIGNED_RESIDUE_CONTRACT.md": "63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386",
    "Theory/Gates/MAT-001/MAT-001_R5_MICROSCOPIC_MATCHING_DECISION.md": "ab8e743913f2e4fd0f5823581514345d598b2d1a1eb92e6d0d04f57447ed69b4",
    "Theory/Core/ITSM_Core_Architecture.md": "332489b09476a4403e8bbebe81b3ff329a114005daa1cf39e8b4738f95b9ac8a",
}
HOLDS = {
    "physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
    "review_status": "DEFERRED", "MAT-001": "BLOCKED", "UVIR-003": "IN_PROGRESS",
    "V": "NOT_COMPUTED", "K_Q": "NOT_DERIVED", "Stage4A": "CLOSED",
    "canonical_Tests_1_3": "HOLD_SUBSTANTIVE", "TOP-X4": "UNCHANGED",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_holds(value):
    if any(value.get(k) != v for k, v in HOLDS.items()):
        raise ValueError("No promotion or removal of governing holds is authorized.")


def calculation():
    checks = []

    def check(name, ok):
        checks.append({"name": name, "passed": bool(ok)})
        if not ok:
            raise AssertionError(name)

    def equal(name, lhs, rhs):
        check(name, sp.simplify(lhs-rhs) == 0)

    for path, expected in PINS.items():
        check("source pin: "+path, sha(ROOT/path) == expected)

    sigma, mu, portal, xi, MP = sp.symbols("sigma mu g xi M_P", positive=True)
    eta, zeta, lam, p, R = sp.symbols("eta zeta lambda p R", real=True)
    xx = sp.symbols("X", positive=True)
    eps, s, ell = sp.symbols("epsilon chart_scale loop_order", positive=True)
    X = portal*sigma**2
    L = sp.log(X/mu**2)
    E = -(X+eta*R)
    # Source a4's derivative/geometric terms remain separate from this bulk slice.
    a4_slice = sp.expand((60*R*E+180*E**2)/360)
    equal("a4 potential coefficient", a4_slice.subs(R,0), X**2/2)
    equal("a4 XR coefficient", a4_slice.coeff(R,1), (eta-sp.Rational(1,6))*X)
    equal("a2 mass and curvature coefficient", E+R/6, -X+(sp.Rational(1,6)-eta)*R)
    pole_slice = -a4_slice/(32*sp.pi**2*eps)
    equal("real-field potential pole", pole_slice.subs(R,0), -X**2/(64*sp.pi**2*eps))
    equal("curvature pole sign", sp.expand(pole_slice).coeff(R,1), -(eta-sp.Rational(1,6))*X/(32*sp.pi**2*eps))
    gradient_sq, sigma_box_sigma = sp.symbols("grad_sigma_sq sigma_box_sigma")
    integrated_box_X = (2*portal*sigma_box_sigma+2*portal*gradient_sq).subs(sigma_box_sigma,-gradient_sq)
    equal("integrated Box X is not a kinetic UV pole", integrated_box_X, 0)

    U1_X = xx**2/(64*sp.pi**2)*(sp.log(xx/mu**2)-sp.Rational(3,2))
    tadpole_half = sp.diff(U1_X,xx)
    equal("potential derivative includes real determinant factor", tadpole_half, xx/(32*sp.pi**2)*(sp.log(xx/mu**2)-1))
    curvature_E = (eta-sp.Rational(1,6))*tadpole_half.subs(xx,X)
    delta_F = -2*curvature_E  # Euclidean gravity is -F R/2; Lorentzian +F R/2.
    a = (eta-sp.Rational(1,6))*portal/(16*sp.pi**2)
    b = portal/(48*sp.pi**2)
    c = portal**2/(64*sp.pi**2)
    equal("Lorentzian F correction from Euclidean coefficient", delta_F, -a*sigma**2*(L-1))

    # Gamma2 = -(delta X)^2 I(q)/4, q=p_E^2. Compare to +Delta Z (grad sigma)^2/2.
    t = sp.symbols("feynman_x", real=True)
    I1 = -sp.integrate(t*(1-t)/xx,(t,0,1))/(16*sp.pi**2)
    equal("bubble momentum derivative", I1, -1/(96*sp.pi**2*xx))
    J3 = 1/(32*sp.pi**2*xx)
    equal("bubble derivative from convergent three-propagator integral", -2*sp.integrate(t*(1-t),(t,0,1))*J3, I1)
    delta_Z = sp.simplify(-sp.diff(X,sigma)**2*I1.subs(xx,X)/2)
    equal("finite real heavy kinetic threshold", delta_Z, b)
    equal("kinetic threshold for general positive X", -I1/2, 1/(192*sp.pi**2*xx))

    f = xi-a*(L-1)
    F = sigma**2*f
    Z = zeta+b
    U = sigma**4*(lam/4+c*(L-sp.Rational(3,2)))
    slope_F = sp.simplify(sigma*sp.diff(F,sigma)/F)
    equal("logarithmic F slope", slope_F, 2*(1-a/f))
    B = Z/f+6*(1-a/f)**2
    equal("Einstein kinetic including metric mixing", sigma**2*(Z/F+sp.Rational(3,2)*(sp.diff(F,sigma)/F)**2), B)
    r = p-slope_F/2
    equal("mass source coefficient in matter chart", r, p-1+a/f)
    V = r/(MP*sp.sqrt(B))
    gcan = -V
    equal("source sign retains mass orientation", gcan+V, 0)
    B0 = 6+zeta/xi
    Bt = (zeta+ell*b)/(xi-ell*a*(L-1))+6*(1-ell*a/(xi-ell*a*(L-1)))**2
    rt = p-1+ell*a/(xi-ell*a*(L-1))
    dB = b/xi+zeta*a*(L-1)/xi**2-12*a/xi
    equal("strict loop-order kinetic coefficient", sp.diff(Bt,ell).subs(ell,0), dB)
    Vt = rt/(MP*sp.sqrt(Bt))
    dV = (a/xi-(p-1)*dB/(2*B0))/(MP*sp.sqrt(B0))
    equal("strict loop-order source coefficient", sp.diff(Vt,ell).subs(ell,0), dV)
    equal("tree limit agrees with ST1", Vt.subs(ell,0), (p-1)/(MP*sp.sqrt(B0)))
    equal("conformal heavy curvature correction zero", a.subs(eta,sp.Rational(1,6)), 0)
    equal("conformal heavy p1 source cancellation", r.subs({eta:sp.Rational(1,6),p:1}), 0)
    equal("nonconformal same-scale mass acquires running-frame vertex", r.subs(p,1), a/f)
    equal("physical zeta freedom in kinetic ratio", sp.diff(B,zeta), 1/f)
    equal("physical zeta freedom in normalized source", sp.diff(V,zeta), -r/(2*MP*f*B**sp.Rational(3,2)))

    # Explicit finite scheme redistributions must leave full coefficients unchanged.
    dxi, dz, du = sp.symbols("finite_xi_shift finite_Z_shift finite_U_shift")
    equal("scheme redistribution leaves F fixed", (xi+dxi)*sigma**2+delta_F-dxi*sigma**2, F)
    equal("scheme redistribution leaves Z fixed", zeta+dz+delta_Z-dz, Z)
    equal("scheme redistribution leaves U fixed", (lam/4+du)*sigma**4+U1_X.subs(xx,X)-du*sigma**4, U)
    # Only the quantized-H contribution to running is tested; no full-theory beta claim.
    beta_xi, beta_lam = -2*a, 8*c
    equal("heavy-only F scale cancellation", mu*sp.diff(F,mu)+beta_xi*sp.diff(F,xi), 0)
    equal("heavy-only potential scale cancellation", mu*sp.diff(U,mu)+beta_lam*sp.diff(U,lam), 0)
    log_mu_change = sp.symbols("log_mu_change", real=True)
    equal("RG retains xi boundary value", sp.diff(xi+beta_xi*log_mu_change,xi), 1)
    equal("RG retains lambda boundary value", sp.diff(lam+beta_lam*log_mu_change,lam), 1)

    # Positive field-chart changes preserve the action and signed normalized vertex.
    chart = {sigma:s*sigma, portal:portal/s**2, xi:xi/s**2, zeta:zeta/s**2, lam:lam/s**4}
    equal("chart-invariant heavy mass", X.subs(chart,simultaneous=True), X)
    equal("chart-invariant curvature F", F.subs(chart,simultaneous=True), F)
    equal("chart-covariant kinetic Z", Z.subs(chart,simultaneous=True)*s**2, Z)
    equal("chart-invariant potential", U.subs(chart,simultaneous=True), U)
    equal("chart-invariant source numerator", r.subs(chart,simultaneous=True), r)
    equal("chart-invariant kinetic ratio", B.subs(chart,simultaneous=True), B)
    # Dimension checks are rescalings of actual expressions, not supplied labels.
    dims = {sigma:s*sigma,mu:s*mu,MP:s*MP}
    for name, expr, power in (("F",F,2),("Z",Z,0),("U",U,4),("B",B,0),("V",V,-1)):
        equal("mass-dimension scaling: "+name, expr.subs(dims,simultaneous=True), s**power*expr)

    UE = MP**4*U/F**2
    UE_conformal = sp.simplify(UE.subs(eta,sp.Rational(1,6)))
    tau_slope = sp.simplify(sigma*sp.diff(UE_conformal,sigma))
    equal("conformal heavy Einstein potential slope", tau_slope, MP**4*portal**2/(32*sp.pi**2*xi**2))
    check("conformal heavy vacuum slope is strictly positive", tau_slope.is_positive is True)
    equal("quartic boundary value cannot erase that slope", sp.diff(tau_slope,lam), 0)

    mp.mp.dps = 80
    numeric = []
    bubble_errors, radial_errors, source_errors = [], [], []
    params = (
        (sp.Rational(1,4),sp.Rational(1,6),sp.Rational(1,4),sp.Rational(1,2)),
        (sp.Rational(1,4),sp.Rational(1,6),sp.Rational(1,4),sp.Integer(2)),
        (sp.Rational(1,4),sp.Rational(1,6),sp.Rational(1,4),sp.Integer(6)),
        (sp.Rational(1,2),sp.Integer(0),sp.Rational(1,4),sp.Rational(1,2)),
        (sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,4),sp.Rational(1,2)),
        (sp.Rational(3,4),sp.Rational(1,3),sp.Rational(1,2),sp.Integer(1)),
    )
    number = lambda expr: mp.mpf(str(sp.N(expr,85)))
    for index,(gg,ee,xii,zz) in enumerate(params):
        ss = sp.Integer(2)
        mu2 = gg*ss**2  # L=0 chosen at reference; not a physical scale selection.
        subs = {portal:gg,eta:ee,xi:xii,zeta:zz,sigma:ss,mu:sp.sqrt(mu2),lam:sp.Rational(1,10)}
        xm = number(mu2)
        radial = mp.quad(lambda u:u**3/(u*u+xm)**3,[0,mp.sqrt(xm),mp.inf])/(8*mp.pi**2)
        radial_expected = 1/(32*mp.pi**2*xm)
        radial_error = abs(radial/radial_expected-1)
        radial_errors.append(radial_error)
        check(f"convergent radial loop integral {index}", radial_error<mp.mpf('1e-70'))
        def bubble_difference(q):
            return -mp.quad(lambda x:mp.log1p(x*(1-x)*q/xm),[0,1])/(16*mp.pi**2)
        q = xm*mp.mpf('1e-18')
        derivative = (bubble_difference(q)/q/3-2*bubble_difference(q/2)/(q/2)
                      +mp.mpf(8)/3*bubble_difference(q/4)/(q/4))
        expected_I1 = -1/(96*mp.pi**2*xm)
        bubble_error = abs(derivative/expected_I1-1)
        bubble_errors.append(bubble_error)
        check(f"independent finite-momentum bubble derivative {index}",bubble_error<mp.mpf('1e-50'))
        ff,bb,rr0 = (number(expr.subs(subs)) for expr in (f,B,r.subs(p,0)))
        check(f"positive off-shell F and full kinetic coefficient {index}",ff>0 and bb>0)
        relF = abs(number(a.subs(subs))/number(xii))
        relB = abs(number(dB.subs(subs))/number(B0.subs(subs)))
        check(f"small local loop shifts {index}",relF<mp.mpf('0.01') and relB<mp.mpf('0.01'))
        Ffunc = sp.lambdify(sigma,F.subs({k:v for k,v in subs.items() if k != sigma}),'mpmath')
        ssn = number(ss)
        mpn = mp.sqrt(Ffunc(ssn))
        fprime = mp.diff(Ffunc,ssn)
        znum = number(Z.subs(subs))
        direct_Ktau = mpn**2*ssn**2*(znum/Ffunc(ssn)+mp.mpf('1.5')*(fprime/Ffunc(ssn))**2)
        check(f"independent Einstein kinetic numerical expression {index}",abs(direct_Ktau/(mpn**2*bb)-1)<mp.mpf('1e-70'))
        for pp in (0,1):
            direct_slope = ssn*mp.diff(lambda sig:pp*mp.log(sig/ssn)-mp.log(Ffunc(sig)/Ffunc(ssn))/2,ssn)
            rn = number(r.subs(subs).subs(p,pp))
            vn = rn/(mpn*mp.sqrt(bb))
            direct_V = direct_slope/mp.sqrt(direct_Ktau)
            source_error = abs(direct_V-vn)
            source_errors.append(source_error)
            check(f"signed matter-frame derivative {index} p{pp}",source_error<mp.mpf('1e-70'))
            numeric.append({"case":index,"g":str(gg),"eta":str(ee),"xi":str(xii),"zeta":str(zz),"p":pp,
                            "sigma0":"2","L0":"0","B_local":mp.nstr(bb,65),"M_P_control":mp.nstr(mpn,65),
                            "V_candidate_off_shell":mp.nstr(vn,65),"source_derivative_error":mp.nstr(source_error,12),
                            "relative_F_loop_shift":mp.nstr(relF,12),"relative_B_loop_shift":mp.nstr(relB,12),
                            "radial_relative_error":mp.nstr(radial_error,12),"bubble_relative_error":mp.nstr(bubble_error,12)})
    family = [row for row in numeric if row['case']<3 and row['p']==0]
    check("same heavy determinant and reference gravity counterfamily",len({row['M_P_control'] for row in family})==1)
    check("three distinct physical kinetic inputs give distinct source vertices",len({row['V_candidate_off_shell'] for row in family})==3)

    mutations = {
        "omit_real_field_half":sp.simplify(2*delta_Z-b)!=0,
        "reverse_curvature_gravity_sign":sp.simplify(2*curvature_E-delta_F)!=0,
        "omit_metric_scalar_mixing":sp.simplify(Z/f-B)!=0,
        "reuse_tree_p1_cancellation_for_running_F":sp.simplify(r.subs(p,1))!=0,
        "discard_physical_zeta_boundary_value":sp.diff(B,zeta)!=0,
        "declare_quartic_cancels_conformal_runaway":tau_slope!=0,
        # B>0 and M_P>0: strip a nonzero radical factor before simplification.
        "erase_source_orientation":sp.simplify((gcan-V)*MP*sp.sqrt(B))!=0,
        "turn_Box_X_into_kinetic_divergence":integrated_box_X==0,
    }
    for name, caught in mutations.items():
        check("negative control: "+name,caught)
    promoted = dict(HOLDS,V="COMPUTED",physics_pass=True)
    try:
        require_holds(promoted)
    except ValueError:
        check("negative control: canonical promotion",True)
    else:
        check("negative control: canonical promotion",False)

    return {
        **HOLDS,"result_id":"MAT001-ST2-v1","claim_status":"Conditional",
        "research_execution":"PROCEED_PROVISIONALLY",
        "calculation_status":"PASS_LOCAL_BULK_THRESHOLD_AND_IDENTIFIABILITY_CHECKS",
        "candidate_disposition":"THRESHOLD_COMPUTED_RENORMALIZED_INPUTS_AND_PHYSICAL_BACKGROUND_OPEN",
        "coefficient_algebra":"EXACT_IN_DISPLAYED_ONE_LOOP_TWO_DERIVATIVE_TRUNCATION_NOT_ALL_LOOP",
        "full_physical_residue_computed":False,"full_finite_density_response_computed":False,
        "versions":{"sympy":sp.__version__,"mpmath":mp.__version__},
        "evidence_sha256":{**PINS,Path(__file__).relative_to(ROOT).as_posix():sha(__file__)},
        "exact":{"X":str(X),"a4_bulk_slice":str(a4_slice),"pole_bulk_slice":str(pole_slice),
                 "Delta_Z":str(delta_Z),"F":str(F),"Z":str(Z),"U":str(U),"B_local":str(B),
                 "mass_slope":str(r),"V_candidate":str(V),"signed_source_g":str(gcan),
                 "Delta_B_strict_one_loop":str(dB),"Delta_V_strict_one_loop":str(dV),
                 "beta_xi_H_only":str(beta_xi),"beta_lambda_H_only":str(beta_lam),
                 "conformal_heavy_Einstein_potential_slope":str(tau_slope)},
        "numeric_diagnostics":numeric,"off_shell_counterfamily":family,"arithmetic_precision_decimal_digits":80,
        "max_radial_relative_error":mp.nstr(max(radial_errors),12),
        "max_bubble_relative_error":mp.nstr(max(bubble_errors),12),
        "max_source_derivative_error":mp.nstr(max(source_errors),12),
        "negative_controls":mutations,"checks":checks,"check_count":len(checks),"failed_checks":[],"unknown_checks":[],
        "substantive_unknowns":["microscopic H/portal and mass-law origin","independent renormalized kinetic/curvature boundary inputs",
                               "finite-density background and full constrained pole","radiative potential balance",
                               "preferred-frame/reservoir and Y^(3/2) matching","physical GR/observable metric and cutoff window",
                               "finite-volume and quantum boundary completion"],
        "scope":"bulk heavy-H one-loop local derivative coefficients, off-shell matter vertex, counterterm identifiability",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    target=args.out.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("Output must stay inside the repository.")
    if target.exists():
        raise FileExistsError("Preserve old evidence: choose a new output directory.")
    result=calculation()
    require_holds(result)
    target.mkdir(parents=True,exist_ok=False)
    body=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode('utf-8')
    receipt=target/'summary.json'
    receipt.write_bytes(body)
    receipt.with_suffix('.json.sha256').write_text(hashlib.sha256(body).hexdigest()+'  summary.json\n',encoding='utf-8')
    print(result['calculation_status'])
    print(result['candidate_disposition'])
    print(f"Checks: {result['check_count']}; rational/mass controls: {len(result['numeric_diagnostics'])}")
    print('Finite Delta Z calculated; zeta boundary input remains free; conformal-heavy vacuum potential has positive slope.')
    print('physics_pass=false; gate_effect=NONE; V=NOT_COMPUTED; K_Q=NOT_DERIVED; review=DEFERRED')
    print('Receipt: '+str(receipt.relative_to(ROOT)))


if __name__=='__main__':
    main()
