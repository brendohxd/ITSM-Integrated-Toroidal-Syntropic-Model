"""Local exact identities and counterexamples; no canonical physics-gate pass."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "Theory/Gates/ITSM_TESTS_01_03_BOUNDED_AUDIT_CONTRACT_2026-09-24.md"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Audit:
    def __init__(self):
        self.checks = []
        self.results = {}

    def check(self, name, expr, nonidentity=False):
        reduced = s.simplify(expr)
        ok = reduced != 0 if nonidentity else reduced == 0
        self.checks.append({"name": name, "expected": "not_identically_zero" if nonidentity else "zero",
                            "residual": str(reduced), "passed": bool(ok)})
        return reduced

    def record(self, **values):
        self.results.update({key: str(value) for key, value in values.items()})


def test1(a):
    u, v, r, psi, chi = fields = s.symbols("u v r psi chi", real=True)
    beta, eta = s.symbols("beta eta", real=True)
    Z = s.symbols("Z", positive=True)
    mp2, mr2, mm2, lp, lr, lam = s.symbols("mp2 mr2 mm2 lp lr lam", nonnegative=True)
    metric = s.diag(-1, 1, 1, 1)
    grad = {f: s.symbols(f"d_{f}_0:4", real=True) for f in fields}
    hess = {f: s.Matrix(4, 4, lambda i, j: s.Symbol(f"h_{f}_{min(i,j)}{max(i,j)}", real=True)) for f in fields}
    upper = {f: metric * s.Matrix(grad[f]) for f in fields}
    box = {f: sum(metric[i, i] * hess[f][i, i] for i in range(4)) for f in fields}

    def dot(f, g):
        return sum(metric[i, i] * grad[f][i] * grad[g][i] for i in range(4))

    def derivative(expr, mu):
        return sum(s.diff(expr, f) * grad[f][mu] + sum(
            s.diff(expr, grad[f][i]) * hess[f][i, mu] for i in range(4)) for f in fields)

    def stress(L, terms):
        return s.Matrix(4, 4, lambda i, j: sum(w * upper[f][i] * upper[f][j]
                                              for w, f in terms) + metric[i, j] * L)

    def divergence(T, nu):
        return sum(derivative(T[mu, nu], mu) for mu in range(4))

    A = s.exp(beta * psi)
    radius2 = u**2 + v**2
    VP = mp2 * radius2 / 2 + lp * radius2**2 / 4
    VR = mr2 * r**2 / 2 + lr * r**4 / 4
    Vm = mm2 * chi**2 / 2
    W = lam * radius2 * r**2 / 4
    LP = -(dot(u, u) + dot(v, v) + Z * dot(psi, psi)) / 2 - VP - W
    LR = -dot(r, r) / 2 - VR
    Lm = -A**2 * dot(chi, chi) / 2 - A**4 * Vm
    TP = stress(LP, [(1, u), (1, v), (Z, psi)])
    TR = stress(LR, [(1, r)])
    Tm = stress(Lm, [(A**2, chi)])
    trace = s.simplify(sum(metric[i, i] * Tm[i, i] for i in range(4)))
    Eu, Ev = box[u] - s.diff(VP + W, u), box[v] - s.diff(VP + W, v)
    Er = box[r] - s.diff(VR + W, r)
    Epsi = Z * box[psi] + beta * trace
    Echi = A**2 * box[chi] + 2 * beta * A**2 * dot(psi, chi) - A**4 * s.diff(Vm, chi)
    a.check("conformal_matter_trace_variation", s.diff(Lm, psi) - beta * trace)
    a.check("wrong_matter_source_sign_rejected", s.diff(Lm, psi) + beta * trace, True)
    for nu in range(4):
        Qmp = beta * trace * upper[psi][nu]
        Qsyn = -s.diff(W, r) * upper[r][nu]
        a.check(f"matter_ward_{nu}", divergence(Tm, nu) - Echi * upper[chi][nu] - Qmp)
        a.check(f"plenum_ward_{nu}", divergence(TP, nu) - Eu * upper[u][nu] - Ev * upper[v][nu]
                - Epsi * upper[psi][nu] + Qmp - Qsyn)
        a.check(f"reservoir_ward_{nu}", divergence(TR, nu) - Er * upper[r][nu] + Qsyn)
        # Directly differentiate the reassigned reservoir stress, not an inserted current.
        shifted_div = divergence(TR - eta * metric * W, nu) - divergence(TR, nu)
        a.check(f"interaction_stress_reassignment_{nu}", shifted_div + eta * metric[nu, nu] * derivative(W, nu))
    # Independent homogeneous FLRW energy equations, with arbitrary H and velocities.
    H = s.symbols("H", real=True)
    vel = dict(zip(fields, s.symbols("ud vd rd psid chid", real=True)))
    T0 = A**2 * vel[chi]**2 - 4 * A**4 * Vm
    acc = {u: -3*H*vel[u]-s.diff(VP+W,u), v: -3*H*vel[v]-s.diff(VP+W,v),
           r: -3*H*vel[r]-s.diff(VR+W,r), psi: -3*H*vel[psi]+beta*T0/Z,
           chi: -(3*H+2*beta*vel[psi])*vel[chi]-A**2*s.diff(Vm,chi)}

    def time_derivative(expr):
        return sum(s.diff(expr, f)*vel[f] + s.diff(expr, vel[f])*acc[f] for f in fields)

    KP = (vel[u]**2 + vel[v]**2 + Z*vel[psi]**2)/2
    KR, Km = vel[r]**2/2, A**2*vel[chi]**2/2
    Qm0, Qs0 = -beta*T0*vel[psi], s.diff(W,r)*vel[r]
    a.check("flrw_matter_energy", time_derivative(Km+A**4*Vm)+6*H*Km-Qm0)
    a.check("flrw_plenum_energy", time_derivative(KP+VP+W)+6*H*KP+Qm0-Qs0)
    a.check("flrw_reservoir_energy", time_derivative(KR+VR)+6*H*KR+Qs0)
    a.check("zero_beta_exact_vs_limit", Qm0.subs(beta,0)-s.limit(Qm0,beta,0))
    a.check("zero_lambda_exact_vs_limit", Qs0.subs(lam,0)-s.limit(Qs0,lam,0))
    a.check("u1_charge_divergence", v*s.diff(VP+W,u)-u*s.diff(VP+W,v))
    a.check("nonzero_energy_transfer_with_conserved_charge", Qs0.subs({u:1,v:1,r:1,lam:1,vel[r]:1})-1)
    a.check("omitted_portal_stress_rejected", derivative(W,1), True)
    a.check("zero_transfer_not_zero_stress", (KR+VR).subs({r:0,vel[r]:1})-s.Rational(1,2))
    zero_extra = {f:0 for f in (u,v,r,psi)}
    zero_extra.update({g:0 for f in (u,v,r,psi) for g in grad[f]})
    a.check("zero_field_GR_control_extra_stress", sum(
        ((TP+TR)[i,j].subs(zero_extra))**2 for i in range(4) for j in range(4)))
    a.check("zero_coupling_matter_equation_GR_control", Echi.subs(beta,0)-(box[chi]-mm2*chi))
    a.record(matter_trace=trace, source_psi=beta*trace, Q_mp="beta*T_m*grad^nu(psi)",
             Q_syn="-lambda*(u^2+v^2)*r*grad^nu(r)/2", Q_syn_FLRW=Qs0,
             shifted_Q_syn="Q_syn + eta*grad^nu(W)", U1_charge_source=0,
             dimensions="[L]=4,[T]=4,[Q]=5,[j_U1]=3,[div j_U1]=4; psi=0,Z=2,u=v=r=chi=1",
             status="PARTIAL_CONFORMAL_CURRENT_AND_RESERVOIR_NONUNIQUENESS_HOLD_FULL_ACTION")


def test2(a):
    Cm, CIR, a0, G, q, mass, radius, scale = s.symbols("Cm CIR a0 G q mass radius scale", positive=True)
    K = CIR*q**3/(12*s.pi*G*a0)
    flux_prefactor = s.diff(K,q)/q
    a.check("cubic_action_flux", flux_prefactor-CIR*q/(4*s.pi*G*a0))
    a.check("newtonian_action_flux", s.diff(q**2/(8*s.pi*G),q)/q-1/(4*s.pi*G))
    q2 = Cm*a0*G*mass/(CIR*radius**2)
    a.check("spherical_gauss_flux", 4*s.pi*radius**2*CIR*q2/(4*s.pi*G*a0)-Cm*mass)
    Cobs2 = Cm**3/CIR
    a.check("physical_force_square", Cm**2*q2-Cobs2*a0*G*mass/radius**2)
    a.check("field_chart_invariance", Cobs2.subs({Cm:Cm/scale,CIR:CIR/scale**3}, simultaneous=True)-Cobs2)
    a.check("two_thirds_not_identified", Cobs2.subs({Cm:1,CIR:1})-s.Rational(4,9), True)
    eps, psi, phiN, phiS = s.symbols("eps psi phiN phiS", real=True)
    g00 = -s.exp(2*Cm*eps*psi)*(1+2*eps*phiN)
    gij = s.exp(2*Cm*eps*psi)*(1-2*eps*phiS)
    a.check("physical_metric_time_potential", s.diff(g00,eps).subs(eps,0)+2*(phiN+Cm*psi))
    a.check("physical_metric_spatial_potential", s.diff(gij,eps).subs(eps,0)+2*(phiS-Cm*psi))
    x,y,k = s.symbols("x y k", positive=True)
    R = x*x+4*y*y
    vx,vy = k*x/R**s.Rational(1,4), 2*k*y/R**s.Rational(1,4)
    curl = s.diff(vy,x)-s.diff(vx,y)
    a.check("nonspherical_curl_formula", curl-k*x*y/R**s.Rational(5,4))
    a.check("universal_algebraic_gradient_rejected", curl.subs({x:1,y:1,k:1}), True)
    vnorm = k*R**s.Rational(1,4)
    a.check("algebraic_flux_can_pass_while_curl_fails", s.diff(vnorm*vx,x)+s.diff(vnorm*vy,y)-3*k*k)
    a.record(C_obs_squared=Cobs2, spherical_force="g_tot=g_N+sqrt(Cm^3*a0/CIR)*sqrt(g_N)",
             fixed_two_thirds_requires="Cm^3/CIR=4/9", metric_time="Phi_m=Phi_N+Cm*psi",
             metric_space="Psi_m=Psi_E-Cm*psi", curl_counterexample=curl,
             curl_at_unit_point=curl.subs({x:1,y:1,k:1}),
             status="CONDITIONAL_SPHERICAL_FORM_UNIVERSAL_POINTWISE_FORM_REJECTED_PARENT_HOLD")


def test3(a):
    Cm,CIR,a0,H,c,ell,chart = s.symbols("Cm CIR a0 H c ell chart", positive=True)
    Cobs2, Cchi = Cm**3/CIR, a0/(c*H)
    reparam = {a0:ell*a0,CIR:ell*CIR}
    physical_scale = Cobs2*a0
    a.check("reference_scale_action_invariance", (CIR/a0).subs(reparam, simultaneous=True)-CIR/a0)
    a.check("reference_scale_force_invariance", physical_scale.subs(reparam, simultaneous=True)-physical_scale)
    a.check("Cchi_changes_by_ell", Cchi.subs(reparam, simultaneous=True)-ell*Cchi)
    a.check("Cchi_not_identified_by_static_action", (Cchi.subs(reparam, simultaneous=True)-Cchi).subs(ell,2), True)
    a.check("measurable_combination_invariant", (Cobs2*Cchi).subs(reparam, simultaneous=True)-Cobs2*Cchi)
    a.check("independent_field_chart_invariance", physical_scale.subs({Cm:Cm/chart,CIR:CIR/chart**3}, simultaneous=True)-physical_scale)
    q,qp = s.symbols("q_dec dq_dec_dN", real=True)
    factor = s.sqrt(1-q)/(2*s.pi)
    slope = -(1+q)+s.diff(factor,q)*qp/factor
    a.check("curvature_branch_redshift_slope", slope-(-(1+q)-qp/(2*(1-q))))
    a.check("multiplier_divisor_ratio", (2*s.pi)/(1/(2*s.pi))-4*s.pi**2)
    a.check("constant_comoving_hubble_length_compatibility", ((1+q)-1)-q)
    a.record(a_dyn=physical_scale, invariant_C_dyn=Cobs2*Cchi,
             SI_dimensions="[c H]=[c^2/L]=L T^-2; dimensional equality does not fix a coefficient",
             frozen_branches="1; 2*pi; 1/(2*pi); sqrt(1-q_dec)/(2*pi); action-derived result absent",
             constant_branch_evolution="a0(z)/a0(0)=H(z)/H(0), conditional on constant Cchi",
             curvature_branch_evolution="a0(z)/a0(0)=H(z)/H(0)*sqrt((1-q(z))/(1-q(0))); q<1",
             curvature_branch_log_slope=slope,
             fixed_comoving_length="L_phys=a*L_com implies a0 proportional to a^-1 if a0 proportional to c^2/L_phys",
             fixed_physical_length="constant a0 under the c^2/L_phys postulate",
             hubble_length="L_phys=c/H compatible with constant L_com only where q_dec=0",
             analyst_blind="false; target values already encountered historically",
             calculation_uses_observations="false", unique_Cchi="NOT_DERIVED",
             status="C_CHI_UNIDENTIFIABLE_WITHOUT_REFERENCE_NORMALIZATION_AND_PARENT_MATCHING")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=int, choices=(1,2,3), required=True)
    args = parser.parse_args()
    audit = Audit()
    {1:test1,2:test2,3:test3}[args.test](audit)
    passed = all(row["passed"] for row in audit.checks)
    payload = {"test":args.test, "local_symbolic_validation":"PASS" if passed else "FAIL",
               "checks":audit.checks, "results":audit.results,
               "runtime":{"python":sys.version.split()[0],"sympy":s.__version__},
               "source_sha256":{"contract":digest(CONTRACT),"executable":digest(Path(__file__))},
               "physics_pass":False,"gate_effect":"NONE","Rule9":"NOT_COMPLETED",
               "canonical_test_complete":False}
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(exist_ok=True)
    target = out / f"test_{args.test:02d}_symbolic_audit.json"
    target.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    target.with_suffix(target.suffix+".sha256").write_text(f"{digest(target)}  {target.name}\n",encoding="ascii")
    for path in (CONTRACT,Path(__file__)):
        path.with_suffix(path.suffix+".sha256").write_text(f"{digest(path)}  {path.name}\n",encoding="ascii")
    print(json.dumps({"test":args.test,"validation":payload["local_symbolic_validation"],
                      "passed":sum(c["passed"] for c in audit.checks),"total":len(audit.checks),
                      "status":audit.results["status"],"sha256":digest(target)}))
    if not passed:
        print(json.dumps([c for c in audit.checks if not c["passed"]],indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
