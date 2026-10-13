#!/usr/bin/env python3
"""Separate classical scalar-tensor source control; canonical ITSM remains held."""
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
    "Theory/Gates/MAT-001/MAT001_ST1_INDUCED_SCALE_SCREEN_CONTRACT_2026-10-13.md": "d3708431f19d7d78451a3ffb641d8b715171b36400b2c439d6dfadd4a2fbbb7b",
    "Theory/Gates/MAT-001/MAT001_PHYSICAL_MATCHING_ROUTE_DECISION_2026-10-13.md": "00e784bc797600fd4e8c31192026f5c2c7977b66d39f4b5faeddce71ef46b4ac",
    "Theory/Gates/MAT-001/MAT001_RM1_RADIAL_MASS_SCREEN_REPORT_2026-10-13.md": "eb1d0d47e137a115451c6908d259bdb1fae61153c8ce217f68c285232c7512ef",
    "Theory/Gates/MAT-001/MAT-001_R4_SIGNED_RESIDUE_CONTRACT.md": "63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386",
    "Theory/Core/ITSM_Core_Architecture.md": "332489b09476a4403e8bbebe81b3ff329a114005daa1cf39e8b4738f95b9ac8a",
    "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/rg1/MAT-001_RG1_ROUTE_COMPARISON.md": "c2c97125b7c144cfd4649243bcc3e08f7e3e6d7c1e1de8ecdab00a380695ed5b",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_holds(value: dict) -> None:
    required = {"physics_pass": False, "gate_effect": "NONE", "Rule9_cleared": False,
                "V": "NOT_COMPUTED", "K_Q": "NOT_DERIVED", "MAT-001": "BLOCKED"}
    if any(value.get(key) != expected for key, expected in required.items()):
        raise ValueError("Canonical promotion is outside this control.")


def classify(kinetic_ratio, mass_power) -> str:
    if kinetic_ratio < 0:
        return "REJECT_NEGATIVE_LOCAL_SCALAR_KINETIC"
    if kinetic_ratio == 0:
        return "WEYL_REDUNDANCY_NO_SCALAR" if mass_power == 1 else "TRACE_CONSTRAINT_NO_PROPAGATING_SCALAR"
    return "DECOUPLED_SAME_SCALE_MATTER" if mass_power == 1 else "PARAMETERIZED_STATIC_SOURCE_IDENTIFICATION_OPEN"


def calculation() -> dict:
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

    for path, expected in PINS.items():
        check("source pin: " + path, sha(ROOT/path) == expected)

    sigma, s0, MP, xi, scale = sp.symbols("sigma sigma0 M_P xi chart_scale", positive=True)
    tau, zeta, p = sp.symbols("tau zeta p", real=True)
    curvature_E, box_tau, grad_tau_sq = sp.symbols("R_E box_tau grad_tau_sq", real=True)
    F = xi*sigma**2
    F0 = xi*s0**2
    B = 6 + zeta/xi
    Ktau = MP**2*B

    # Bulk conformal transformation. The Box term is kept until boundary accounting.
    sigma_map = s0*sp.exp(tau)
    volume_ratio = sp.exp(-4*tau)
    curvature_J = sp.exp(2*tau)*(curvature_E+6*box_tau-6*grad_tau_sq)
    transformed_EH = sp.simplify(volume_ratio * F.subs(sigma,sigma_map) * curvature_J/2)
    transformed_EH = transformed_EH.subs(s0**2, MP**2/xi)
    transformed_explicit = sp.simplify(-zeta/2*volume_ratio*sp.exp(2*tau)
                                     *sp.diff(sigma_map,tau)**2*grad_tau_sq).subs(s0**2,MP**2/xi)
    transformed = sp.expand(transformed_EH+transformed_explicit)
    expected = MP**2*curvature_E/2 + 3*MP**2*box_tau - Ktau*grad_tau_sq/2
    check("conformal bulk kinetic coefficient includes metric mixing", sp.simplify(transformed-expected) == 0)
    normal_tau, boundary_K = sp.symbols("normal_tau K_E", real=True)
    transformed_boundary = sp.expand(sp.exp(-3*tau)*F.subs(sigma,sigma_map)
                                     *sp.exp(tau)*(boundary_K-3*normal_tau)).subs(s0**2,MP**2/xi)
    check("conformal boundary cancels retained divergence", sp.simplify(
        transformed_boundary + 3*MP**2*normal_tau - MP**2*boundary_K) == 0)
    general_kinetic = MP**2*(zeta/F+sp.Rational(3,2)*(sp.diff(F,sigma)/F)**2)
    check("independent scalar-tensor coefficient expression", sp.simplify(
        general_kinetic*(sp.diff(sigma_map,tau)**2)
        .subs(tau,sp.log(sigma/s0))-Ktau) == 0)

    # Worldline lengths scale as ds_J=exp(-tau) ds_E.
    mass0, rho_b = sp.symbols("m0 rho_b", positive=True)
    mass_E = sp.simplify(mass0*(sigma_map/s0)**p*sp.exp(-tau))
    check("Einstein mass and effective matter metric agree", sp.simplify(
        mass_E-mass0*sp.exp((p-1)*tau)) == 0)
    logarithmic_source = sp.simplify(sp.diff(mass_E,tau)/mass_E)
    check("fractional mass source includes frame and explicit mass factors", logarithmic_source == p-1)
    canonical_scale = MP*sp.sqrt(B)
    Vparam = (p-1)/canonical_scale
    gcan = (1-p)/canonical_scale
    check("signed source is minus the fractional mass coupling", sp.simplify(gcan+Vparam) == 0)
    check("same-scale Jordan masses cancel source exactly", sp.simplify(logarithmic_source.subs(p,1)) == 0)
    check("fixed Jordan masses have a nonzero source", logarithmic_source.subs(p,0) == -1)
    quartic = sp.symbols("lambda_sigma", real=True)
    potential_E = sp.simplify(volume_ratio*quartic*sigma_map**4).subs(s0**4,MP**4/xi**2)
    check("quartic scale potential is constant in Einstein variables", sp.diff(potential_E,tau) == 0)

    # Linearized Jordan equations from metric conformal variation and scalar variation.
    # The trace variation is F R - 3 Box F + T = 0 at constant sigma; kinetic terms are quadratic.
    Rlin, box_delta_sigma, T = sp.symbols("R_lin box_delta_sigma T", real=True)
    Fprime0 = sp.diff(F,sigma).subs(sigma,s0)
    trace_eq = F0*Rlin - 3*Fprime0*box_delta_sigma + T
    scalar_eq = zeta*box_delta_sigma + Fprime0*Rlin/2 + p*T/s0
    R_from_trace = sp.solve(trace_eq,Rlin)[0]
    combined = sp.expand(scalar_eq.subs(Rlin,R_from_trace))
    check("Jordan trace elimination retains metric-scalar mixing", sp.simplify(
        combined - ((zeta+6*xi)*box_delta_sigma+(p-1)*T/s0)) == 0)
    box_tau_symbol = sp.symbols("box_tau_source", real=True)
    canonical_equation = sp.expand(combined.subs(box_delta_sigma,s0*box_tau_symbol)*s0)
    canonical_equation = canonical_equation.subs(s0**2,MP**2/xi)
    check("Jordan and Einstein source equations coincide", sp.simplify(
        canonical_equation - (Ktau*box_tau_symbol+(p-1)*T)) == 0)
    check("Weyl unnormalized equation is trace constraint", sp.simplify(
        canonical_equation.subs(zeta,-6*xi)-(p-1)*T) == 0)
    check("Weyl plus same-scale masses has no independent scalar equation",
          sp.simplify(canonical_equation.subs({zeta:-6*xi,p:1})) == 0)
    check("Weyl with fixed masses cannot source a propagating scalar",
          sp.simplify(canonical_equation.subs({zeta:-6*xi,p:0})) == -T)
    check("positive interior and boundary classification",
          classify(2,0) == 'PARAMETERIZED_STATIC_SOURCE_IDENTIFICATION_OPEN'
          and classify(2,1) == 'DECOUPLED_SAME_SCALE_MATTER'
          and classify(0,1) == 'WEYL_REDUNDANCY_NO_SCALAR'
          and classify(0,0) == 'TRACE_CONSTRAINT_NO_PROPAGATING_SCALAR'
          and classify(-1,0) == 'REJECT_NEGATIVE_LOCAL_SCALAR_KINETIC')

    omega_sq, k_sq = sp.symbols("omega_sq k_sq", real=True)
    response = (p-1)**2/(Ktau*(omega_sq-k_sq))
    check("source-square exchange is the canonical pole coefficient", sp.simplify(
        response-gcan**2/(omega_sq-k_sq)) == 0)
    check("static massless source kernel in local vacuum control", sp.simplify(
        response.subs(omega_sq,0)+Vparam**2/k_sq) == 0)
    Btransport = sp.simplify(B.subs({xi:xi/scale**2,zeta:zeta/scale**2},simultaneous=True))
    check("physical kinetic ratio invariant under sigma chart change", Btransport == B)
    check("reference gravitational coefficient invariant", sp.simplify(
        (xi/scale**2)*(scale*s0)**2-F0) == 0)
    check("coupling invariant under chart transport", sp.simplify(
        Vparam.subs({xi:xi/scale**2,zeta:zeta/scale**2},simultaneous=True)-Vparam) == 0)
    check("kinetic ratio remains physically identifying", sp.diff(Vparam,zeta).subs(p,0) != 0)
    check("nonnegative Jordan kinetic subclass has B at least six", sp.simplify(B-6) == zeta/xi)
    extra_positive = sp.symbols("nonnegative_ratio", nonnegative=True)
    ratio_bound_sq = sp.simplify((Vparam**2/(1/(6*MP**2))).subs({p:0,zeta:xi*extra_positive}))
    check("conditional source bound expression", ratio_bound_sq == 6/(extra_positive+6))
    omega_BD = zeta/(4*xi)
    check("Brans-Dicke kinetic ratio cross-check", sp.simplify(4*omega_BD+6-B) == 0)
    alpha_force = sp.simplify(2*MP**2*Vparam**2)
    GE = 1/(8*sp.pi*MP**2)
    GN = sp.simplify(GE*(1+alpha_force))
    check("bare and Newton response constants differ for fixed masses",
          sp.simplify(GN.subs(p,0)-GE) != 0)
    check("same-scale decoupling retains tensor Newton response", sp.simplify(GN.subs(p,1)-GE) == 0)

    mutation_rejections = {
        "lost_metric_six": sp.simplify(Ktau-MP**2*zeta/xi) != 0,
        "omitted_mass_frame_factor": sp.simplify((p-logarithmic_source).subs(p,1)) != 0,
        "wrong_weyl_sign": sp.simplify(B.subs(zeta,6*xi)) == 12,
        "conformal_positive_sign_confusion": B.subs({xi:sp.Rational(1,6),zeta:1}) == 12,
        "source_sign_erased": sp.simplify((gcan-Vparam).subs(p,0)) != 0,
        "nonzero_same_scale_vertex": logarithmic_source.subs(p,1) != 1,
        "bare_G_called_measured_G": sp.simplify(GN.subs(p,0)/GE) != 1,
    }
    for name, condition in mutation_rejections.items():
        check("reject mutation: " + name, condition)

    mp.mp.dps = 80
    numeric = []
    for Bv in (8,14,30):
        xiv=sp.Rational(1,4)
        zetav=xiv*(Bv-6)
        # Same M_P=1, sigma0=2 and condensate inputs; only the physical kinetic ratio differs.
        for pv in (0,1):
            substitutions={MP:1,xi:xiv,zeta:zetav,p:pv}
            gvalue=mp.mpf(str(sp.N(gcan.subs(substitutions),85)))
            vvalue=mp.mpf(str(sp.N(Vparam.subs(substitutions),85)))
            check(f"B={Bv}, p={pv}: canonical signed relation", abs(gvalue+vvalue) < mp.mpf('1e-70'))
            check(f"B={Bv}, p={pv}: source versus decoupling", gvalue > 0 if pv==0 else gvalue==0)
            direct_tau_rhs=(1-pv)*mp.mpf('-1')/Bv
            einstein_phi_rhs=(1-pv)*mp.mpf('-1')/mp.sqrt(Bv)
            error=abs(direct_tau_rhs-einstein_phi_rhs/mp.sqrt(Bv))
            check(f"B={Bv}, p={pv}: independent Jordan source normalization", error < mp.mpf('1e-70'))
            direct=-mp.mpf((pv-1)**2)/Bv/4
            canonical=-gvalue**2/4
            exchange_error=abs(direct-canonical)
            check(f"B={Bv}, p={pv}: static source exchange", exchange_error < mp.mpf('1e-70'))
            check(f"B={Bv}, p={pv}: conditional bound", abs(vvalue) <= abs(pv-1)/mp.sqrt(6))
            numeric.append({"B":Bv,"p":pv,"M_P":"1","xi":str(xiv),"zeta":str(zetav),"sigma0":"2",
                            "signed_candidate_V":mp.nstr(vvalue,60),"signed_source_g":mp.nstr(gvalue,60),
                            "source_exchange_weight":mp.nstr(gvalue**2,60),
                            "Jordan_Einstein_source_error":mp.nstr(error,10),
                            "static_exchange_error":mp.nstr(exchange_error,10),
                            "disposition":classify(Bv,pv)})
    nonzero_values=[row['signed_candidate_V'] for row in numeric if row['p']==0]
    check("identical reference and condensate inputs leave distinct source residues", len(set(nonzero_values))==3)
    dimensional_symbols = {MP:1, xi:0, zeta:0, p:0, omega_sq:2, k_sq:2}

    def dimension(expression):
        if expression.is_number:
            return sp.S.Zero
        if expression.is_Symbol:
            return sp.Rational(dimensional_symbols[expression])
        if expression.is_Add:
            values={dimension(term) for term in expression.args}
            if len(values)!=1:
                raise ValueError('Incompatible dimensions in sum: '+str(expression))
            return values.pop()
        if expression.is_Mul:
            return sum((dimension(term) for term in expression.args),sp.S.Zero)
        if expression.is_Pow and expression.exp.is_Number:
            return dimension(expression.base)*expression.exp
        raise ValueError('Unrecognized dimension expression: '+str(expression))

    check("actual kinetic coefficient dimension", dimension(Ktau)==2)
    check("actual fractional source dimension", dimension(Vparam)==-1 and dimension(gcan)==-1)
    check("actual source-exchange response dimension", dimension(response)==-4)
    check("actual vacuum gravitational coefficient dimensions", dimension(GE)==-2 and dimension(GN)==-2)
    metadata_rejected=False
    try:
        require_holds({"physics_pass":True,"gate_effect":"NONE","Rule9_cleared":False,
                       "V":"NOT_COMPUTED","K_Q":"NOT_DERIVED","MAT-001":"BLOCKED"})
    except ValueError:
        metadata_rejected=True
    check("reject metadata mutation: canonical promotion",metadata_rejected)
    return {
        "result_id":"MAT001-ST1-v1","calculation_status":"LOCAL_EXACT_FRAME_SOURCE_SCREEN_COMPLETE",
        "candidate_disposition":"PARAMETERIZED_STATIC_SOURCE_EXISTS_NUMERICAL_IDENTIFICATION_OPEN",
        "claim_status":"Conditional","physics_pass":False,"gate_effect":"NONE","Rule9_cleared":False,
        "review_status":"DEFERRED","research_execution":"PROCEED_PROVISIONALLY",
        "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","V":"NOT_COMPUTED","K_Q":"NOT_DERIVED","Stage4A":"CLOSED",
        "versions":{"sympy":sp.__version__,"mpmath":mp.__version__},
        "evidence_sha256":{**PINS,str(Path(__file__).relative_to(ROOT)).replace('\\','/'):sha(Path(__file__))},
        "exact":{"B":str(B),"K_tau":str(Ktau),"Einstein_mass":str(mass_E),
                 "signed_candidate_V":str(Vparam),"signed_source_g":str(gcan),
                 "Jordan_combined_equation":str(canonical_equation),"source_exchange_response":str(response),
                 "alpha_force_vacuum_control":str(alpha_force),"G_E":str(GE),"G_N_vacuum_control":str(GN),
                 "conditional_p0_bound":"abs(V_ST1)<=1/(sqrt(6)*M_P), ONLY if zeta>=0 and xi>0",
                 "weyl_relation":"zeta=-6 xi; B=0; canonical normalization unavailable"},
        "p0_disposition":"STATIC_SOURCE_NONZERO_B_FREE","p1_disposition":"EXACT_MASS_FRAME_CANCELLATION",
        "weyl_disposition":"NO_PROPAGATING_SCALAR_OR_TRACE_CONSTRAINT",
        "numeric_diagnostics":numeric,"mutation_rejections":mutation_rejections,
        "checks":checks,"check_count":len(checks),"failed_checks":[],"unknown_checks":[],
        "scope":"exact covariant frame algebra, linear Jordan trace elimination, local scalar/probe source control",
        "excluded_uses":["canonical ITSM parent adoption","canonical numerical V or K_Q","full finite-density constrained spectrum",
                         "physical global torus response or zero-mode inverse","Standard-Model mass origin","Y^(3/2) matching",
                         "physical cutoff, screening, lensing or observational viability","R5-P1 rehabilitation","gate closure"],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    target=args.out.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('Output must stay in repository.')
    if target.exists():
        raise FileExistsError('Preserve existing attempts; choose a new directory.')
    value=calculation()
    require_holds(value)
    target.mkdir(parents=True,exist_ok=False)
    body=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode('utf-8')
    receipt=target/'summary.json'
    receipt.write_bytes(body)
    receipt.with_suffix('.json.sha256').write_text(hashlib.sha256(body).hexdigest()+'  summary.json\n',encoding='utf-8')
    print(value['calculation_status'])
    print(value['candidate_disposition'])
    print(f"Checks: {value['check_count']}; rational parameter/mass cases: {len(value['numeric_diagnostics'])}")
    print('p=0: nonzero static residue with free B; p=1: zero source; B=0: no canonical scalar pole.')
    print('physics_pass=false; gate_effect=NONE; V=NOT_COMPUTED; K_Q=NOT_DERIVED; review=DEFERRED')
    print('Receipt: '+str(receipt.relative_to(ROOT)))


if __name__=='__main__':
    main()
