"""G3N1: leading-cusp, frozen-chart classical Galerkin probe.

No full nonlinear field, physical EFT cutoff, scattering, GR or Test-1 pass.
Parent G3V artifacts are read-only. Original absolute values are retained.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
DIRECT = {
    "Theory/Gates/RES-001/RES001_R4C1_G3N1_CLASSICAL_CUSP_AMPLITUDE_CONTRACT_2026-10-08.md":
        "83a6aafc934d00982b28ce745ef4626fdd6a4a017e5c2dcd328e14ea0985a102",
    "Theory/Gates/RES-001/RES001_R4C1_G3_VERTEX_REGULARITY_CROSSCHECK_REPORT_2026-10-08.md":
        "0b35ad651859271e9310b8aeec5a0957805efe35cd05fbece96b498969c22409",
    "Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/summary.json":
        "b752415f0d5741c80a47dca5c699f7dc2ca54d31fc43ba04ded4c335939bf492",
    "Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/grid.json":
        "bbb332d89a5a63af119c6f7c34580516ca450e19dc46c67a4d0a31c61d3a859b",
    "Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_crosscheck.py":
        "4898f85f20e30bb0ba3c61492d97657bde0163b3bf74a67c60ba38d9cf027f19",
    "Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md":
        "952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27",
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
}
OUT = ROOT / "Analysis/MasterTests/outputs/r4c1_g3n1_attempt_01"
PARENT = ROOT / "Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01"
ETAS = (1.0, 0.25, 0.0625, 0.015625, 0.00390625, 0.0009765625)
TIMES = (0.0, 0.5, 1.0, 2.0, 3.0, 4.0)
KS = (20.0, 40.0, 80.0)
WSTAR = 0.01
TOL = 2e-8
COARSE_TOL = 2e-6


def digest(data):
    return hashlib.sha256(data).hexdigest()


def payload(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def verify(pins):
    for rel, expected in pins.items():
        p = ROOT / rel
        actual = digest(p.read_bytes())
        if actual != expected:
            raise RuntimeError(f"source pin mismatch: {rel}: {actual}")
        side = Path(str(p) + ".sha256")
        if side.exists() and side.read_text().split()[0] != actual:
            raise RuntimeError(f"sidecar mismatch: {rel}")


class Audit:
    def __init__(self):
        self.checks = []

    def test(self, name, condition, value, criterion):
        self.checks.append(dict(name=name, passed=bool(condition),
                                value=value, criterion=criterion))

    def exact(self, name, expression):
        reduced = s.simplify(expression)
        self.test(name, reduced == 0, str(reduced), "zero_exact")


def algebra(audit):
    th = s.symbols("theta", real=True)
    q = s.symbols("q", real=True)
    v, mom = s.symbols("v momentum", real=True)
    w2, D, Cx, C = s.symbols("omega2 D C_X C", positive=True)
    gamma, R = s.symbols("gamma R", positive=True)
    yy = s.symbols("y", nonnegative=True)
    c2 = s.integrate(s.cos(th)**2, (th, 0, 2*s.pi))/(2*s.pi)
    c3 = 2*s.integrate(s.cos(th)**3, (th, 0, s.pi/2))/s.pi
    c5 = 2*s.integrate(s.cos(th)**5, (th, 0, s.pi/2))/s.pi
    harmonic3 = s.simplify(4*c5-3*c3)
    audit.exact("cosine_quadratic_average", c2-s.Rational(1, 2))
    audit.exact("absolute_cubic_average", c3-4/(3*s.pi))
    audit.exact("average_amplitude_kinetic_residue", 2*c2-1)
    audit.exact("canonical_average_cusp_normalization",
                C*s.sqrt(2)**3*c3-2*s.sqrt(2)*Cx.subs(Cx, C*c3))
    V = w2*q*q/2 + D*s.Abs(q)**3
    L = v*v/2-V
    force = s.diff(V, q)
    audit.exact("signed_cusp_force", force-(w2*q+3*D*q*s.Abs(q)))
    audit.exact("probe_momentum", s.diff(L, v)-v)
    H = s.simplify(mom*v-L).subs(v, mom)
    audit.exact("probe_hamiltonian", H-(mom*mom/2+V))
    audit.exact("hamilton_q_equation", s.diff(H, mom)-mom)
    audit.exact("hamilton_momentum_equation", s.diff(H, q)-force)
    audit.exact("probe_velocity_Hessian", s.diff(L, v, 2)-1)
    plus = -yy-gamma*yy**2
    ym = s.symbols("y_minus", negative=True)
    minus = -ym+gamma*ym**2
    audit.exact("positive_signed_force", plus+yy+gamma*yy**2)
    audit.exact("negative_signed_force", minus+ym-gamma*ym**2)
    audit.exact("force_derivative_zero_from_right", s.limit(s.diff(plus, yy), yy, 0, dir="+")+1)
    audit.exact("force_derivative_zero_from_left", s.limit(s.diff(minus, ym), ym, 0, dir="-")+1)
    audit.test("nonzero_cusp_force_not_C2", s.diff(plus, yy, 2) != s.diff(minus, ym, 2),
               [str(s.diff(plus, yy, 2)), str(s.diff(minus, ym, 2))],
               "opposite one-sided second derivatives; gamma>0")
    audit.exact("local_Lipschitz_bound",
                -(s.diff(plus, yy).subs(yy, R))-(1+2*gamma*R))
    dW, dD = s.symbols("omega2_dot D_dot", real=True)
    E = v*v/2+V
    Edot = s.diff(E, q)*v+s.diff(E, v)*(-force)+s.diff(E, w2)*dW+s.diff(E, D)*dD
    audit.exact("time_dependent_energy_balance", Edot-dW*q*q/2-dD*s.Abs(q)**3)
    audit.exact("frozen_energy_balance", Edot.subs({dW:0, dD:0}))
    rr = s.symbols("excess", positive=True)
    beyond = s.expand(((1+rr)**2-1)/2+gamma*((1+rr)**3-1)/3)
    audit.test("positive_energy_turning_bound", beyond.is_positive, str(beyond),
               "potential at |y|>1 exceeds initial energy; gamma>=0")
    audit.exact("third_harmonic_projection", harmonic3-4/(15*s.pi))
    ratio = s.simplify(harmonic3/c3)
    audit.exact("third_to_fundamental_force_ratio", ratio-s.Rational(1,5))
    audit.test("one_mode_invariance_rejected", harmonic3 != 0, str(harmonic3),
               "nonzero third-harmonic force: Galerkin subspace is not invariant")
    delta_energy = (1-yy**2)/2+gamma*(1-yy**3)/3
    regular_denominator = 1+2*gamma*(1+yy+yy**2)/(3*(1+yy))
    audit.exact("endpoint_substituted_energy_quadrature",
                2*delta_energy-(1-yy**2)*regular_denominator)
    audit.exact("regular_quadrature_endpoint", regular_denominator.subs(yy, 1)-(1+gamma))
    audit.test("omitted_cusp_rejected", s.simplify(force-w2*q) != 0,
               str(force-w2*q), "cusp remains in force")
    audit.test("sign_insensitive_force_rejected", s.simplify(3*D*ym*s.Abs(ym)-3*D*ym**2) != 0,
               "negative amplitude", "q|q| is not q^2")
    audit.test("uncorrected_cosine_residue_rejected", c2 != 1, str(c2),
               "X_amplitude is not the canonical average amplitude q")
    audit.test("changing_background_energy_conservation_rejected",
               s.simplify(Edot) != 0, str(s.simplify(Edot)),
               "requires explicit coefficient-work terms")
    dims = dict(q=1, qdot=2, omega2=2, D=1, averaged_L=4, averaged_H=4)
    audit.test("dimension_quadratic_kinetic", 2*dims["qdot"]==4, 2*dims["qdot"], 4)
    audit.test("dimension_quadratic_potential", dims["omega2"]+2*dims["q"]==4,
               dims["omega2"]+2*dims["q"], 4)
    audit.test("dimension_cusp_potential", dims["D"]+3*dims["q"]==4,
               dims["D"]+3*dims["q"], 4)
    audit.test("dimension_EOM_terms", [dims["q"]+2, dims["omega2"]+dims["q"],
               dims["D"]+2*dims["q"]]==[3,3,3], [3,3,3], "all mass dimension 3")
    audit.test("dimension_rescaled_gamma", dims["D"]+dims["q"]-dims["omega2"]==0, 0, 0)
    return dict(
        convention="spatial-average action density, frozen coefficients, one-mode Galerkin probe",
        local_field="X(t,z)=sqrt(2)*q(t)*cos(k*z); X=a^(3/2)*f*w",
        C_X_scope="parent averaged coefficient for X_amplitude*cos(k*z)",
        canonical_average_cusp="D=2*sqrt(2)*C_X",
        integrated_mode_caveat="integrated volume-normalized mode needs a separate volume factor",
        L=str(L), momentum=str(s.diff(L, v)), H=str(H),
        EOM="qddot+omega2*q+3*D*q*abs(q)=0",
        rescaled_EOM="y''+y+gamma*y*abs(y)=0",
        gamma="3*D*q_star/omega2", force_class="C1, locally Lipschitz; not C2 for D>0",
        action_class="C2, not C3 at q=0 for D>0",
        lipschitz_bound="max-norm Jacobian <= 1+2*gamma*R on |y|<=R",
        probe_existence="local uniqueness plus bounded energy orbit gives global frozen-probe evolution",
        energy_bound="|y|<=1; |y'|<=sqrt(1+2*gamma/3) for initial (+/-1,0)",
        changing_energy=str(s.simplify(Edot)),
        harmonic_3=str(harmonic3), harmonic_1=str(c3), harmonic_ratio=str(ratio),
        period_integral="T_tau=4*integral_0^(pi/2)[1+(2*gamma/3)*(1+sin(theta)+sin(theta)^2)/(1+sin(theta))]^(-1/2) dtheta",
        mass_dimensions=dims,
        full_action_Legendre_regular="NOT_DETERMINED",
        full_field_unique_evolution="NOT_DETERMINED",
        regulator_and_auxiliary_quartic="NOT_SUPPLIED",
        single_mode_invariant=False,
    )


def quarter_period(gamma):
    with mp.workdps(50):
        g = mp.mpf(str(gamma))
        def integrand(th):
            u = mp.sin(th)
            return 1/mp.sqrt(1+(2*g/3)*(1+u+u*u)/(1+u))
        return float(mp.quad(integrand, [0, mp.pi/4, mp.pi/2]))


def integrate(gamma, sign, method, coarse=False):
    times = np.linspace(0, 8*np.pi, 401)
    def rhs(t, state):
        y, vel = state
        return [vel, -y-gamma*y*abs(y)]
    def crossing(t, state):
        return state[0]
    crossing.direction = -sign
    options = dict(rtol=1e-8 if coarse else 1e-11,
                   atol=1e-10 if coarse else 1e-13,
                   max_step=np.pi/32, t_eval=times, events=crossing)
    if method == "Radau":
        options["jac"] = lambda t, state: [[0,1],[-1-2*gamma*abs(state[0]),0]]
    sol = solve_ivp(rhs, (0,8*np.pi), [sign,0], method=method, **options)
    if not sol.success or sol.y.shape != (2,401) or not len(sol.t_events[0]):
        raise RuntimeError(f"integrator failure: {method}, gamma={gamma}, {sol.message}")
    y, vel = sol.y
    E = (vel*vel+y*y)/2+gamma*np.abs(y)**3/3
    E0 = 0.5+gamma/3
    return sol, float(np.max(np.abs(E-E0))/E0)


def difference(a, b):
    return float(np.max(np.abs(a-b)/np.maximum(1, np.maximum(np.abs(a),np.abs(b)))))


def numerical(audit):
    rows = json.loads((PARENT/"grid.json").read_bytes())["chart_events"]
    actual = {(r["eta"],r["method"],r["t"],r["k"]) for r in rows}
    wanted = {(eta,method,t,k) for eta in ETAS for method in ("DOP853","Radau")
              for t in TIMES for k in KS}
    audit.test("registered_parent_grid", len(rows)==216 and actual==wanted,
               len(rows), "216 exact frozen chart keys")
    for i, row in enumerate(rows):
        values = [row[key] for key in ("kinetic_weight","gradient_weight",
                                      "canonical_frequency_squared","comoving_cusp_coefficient")]
        audit.test(f"chart_{i}_finite_positive_inputs",
                   all(np.isfinite(x) and x>0 for x in values), values,
                   "finite positive inputs in this sampled grid only")
    selected = [r for r in rows if r["method"]=="DOP853" and r["t"] in (0,4) and r["k"]==20]
    selected.sort(key=lambda r:(-r["eta"],r["t"]))
    audit.test("registered_physical_probes", len(selected)==12, len(selected), 12)
    probes = []
    for i, r in enumerate(selected):
        D = 2*np.sqrt(2)*r["comoving_cusp_coefficient"]
        qstar = r["a"]**1.5*np.sqrt(r["kinetic_weight"])*WSTAR/np.sqrt(2)
        gamma = 3*D*qstar/r["canonical_frequency_squared"]
        probes.append(dict(id=f"chart_{i}",kind="ARCHIVED_FROZEN_CHART_PROBE",
                           eta=r["eta"],t=r["t"],k=r["k"],W_star=WSTAR,
                           q_star=qstar,D=D,omega2=r["canonical_frequency_squared"],gamma=gamma))
    for i, gamma in enumerate((0.0,0.125,1.0)):
        probes.append(dict(id=f"synthetic_{i}",kind="SYNTHETIC_CONTROL_NOT_ITSM_PREDICTION",gamma=gamma))
    results = []
    waveforms = {}
    for probe in probes:
        gamma = probe["gamma"]
        period_q = quarter_period(gamma)
        solutions = {}
        entries = []
        for sign in (1,-1):
            for method in ("DOP853","Radau"):
                sol, drift = integrate(gamma,sign,method)
                solutions[(sign,method)] = sol.y
                qerr = abs(float(sol.t_events[0][0])-period_q)/period_q
                name = f"{probe['id']}_{sign}_{method}"
                audit.test(name+"_energy",drift<=TOL,drift,TOL)
                audit.test(name+"_quarter_period",qerr<=TOL,qerr,TOL)
                max_y = float(np.max(np.abs(sol.y[0])))
                max_v = float(np.max(np.abs(sol.y[1])))
                audit.test(name+"_amplitude_bound",max_y<=1+TOL,max_y,1+TOL)
                bound_v = float(np.sqrt(1+2*gamma/3))
                audit.test(name+"_velocity_bound",max_v<=bound_v*(1+TOL),max_v,bound_v*(1+TOL))
                entry = dict(sign=sign,method=method,energy_drift=drift,
                             quarter_period_error=qerr,first_zero=float(sol.t_events[0][0]),
                             max_abs_y=max_y,max_abs_velocity=max_v,nfev=sol.nfev)
                if gamma == 0:
                    times = np.linspace(0,8*np.pi,401)
                    harmonic = np.array([sign*np.cos(times),-sign*np.sin(times)])
                    err = difference(sol.y,harmonic)
                    audit.test(name+"_harmonic_control",err<=TOL,err,TOL)
                    entry["harmonic_error"] = err
                if probe["id"]=="synthetic_2":
                    coarse, cdrift = integrate(gamma,sign,method,coarse=True)
                    err = difference(sol.y,coarse.y)
                    audit.test(name+"_coarse_fine",err<=COARSE_TOL,err,COARSE_TOL)
                    entry.update(coarse_fine_error=err,coarse_energy_drift=cdrift)
                    if sign == 1:
                        waveforms[method] = sol.y.T.tolist()
                entries.append(entry)
        paired = max(difference(solutions[(sign,"DOP853")],solutions[(sign,"Radau")])
                     for sign in (1,-1))
        parity = max(difference(solutions[(1,m)],-solutions[(-1,m)]) for m in ("DOP853","Radau"))
        audit.test(probe["id"]+"_paired_methods",paired<=TOL,paired,TOL)
        audit.test(probe["id"]+"_signed_parity",parity<=TOL,parity,TOL)
        results.append({**probe, "quarter_period_quadrature":period_q,
                        "paired_method_error":paired,"parity_error":parity,"integrations":entries})
    return dict(chart_events=len(rows),probe_count=len(probes),cases=results,
                synthetic_gamma1_waveforms=waveforms,
                waveform_times_tau=np.linspace(0,8*np.pi,401).tolist())


def evaluate(symbolic_only=False):
    parent = json.loads((PARENT/"summary.json").read_bytes())
    inherited = {**parent["source_sha256"],**parent["transitive_source_sha256"]}
    verify({**inherited,**DIRECT})
    self_hash = digest(Path(__file__).read_bytes())
    audit = Audit()
    formulas = algebra(audit)
    if symbolic_only:
        return None, formulas, audit
    cases = numerical(audit)
    verify({**inherited,**DIRECT})
    if digest(Path(__file__).read_bytes()) != self_hash:
        raise RuntimeError("own executable changed during calculation")
    if not parent["physics_pass"] and parent["Rule9_cleared"] is False:
        audit.test("parent_holds_preserved",True,"physics_pass=false; review deferred","no promotion")
    else:
        raise RuntimeError("unexpected parent status")
    arrays = [entry for p in cases["cases"] for entry in p["integrations"]]
    physical = [p for p in cases["cases"] if p["kind"]=="ARCHIVED_FROZEN_CHART_PROBE"]
    summary = dict(
        schema="r4c1-g3n1-v1",passed=sum(c["passed"] for c in audit.checks),total=len(audit.checks),
        validation="PASS_BOUNDED_CHECKS" if all(c["passed"] for c in audit.checks) else "FAIL",
        status="CONDITIONAL_CLASSICAL_GALERKIN_EVOLUTION_ONE_MODE_CLOSURE_REJECTED",
        checks=audit.checks,source_sha256=DIRECT,transitive_source_sha256=inherited,
        script_sha256=self_hash,
        artifacts={"formulas.json":digest(payload(formulas)),"cases.json":digest(payload(cases))},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                     sympy=s.__version__,mpmath=mp.__version__,quadrature_digits=50),
        numerical_summary=dict(chart_events=216,physical_chart_probes=len(physical),
            synthetic_controls=3,fine_integrations=len(arrays),coarse_integrations=4,
            max_energy_drift=max(e["energy_drift"] for e in arrays),
            max_quarter_period_error=max(e["quarter_period_error"] for e in arrays),
            max_paired_method_error=max(p["paired_method_error"] for p in cases["cases"]),
            max_parity_error=max(p["parity_error"] for p in cases["cases"]),
            physical_gamma_range=[min(p["gamma"] for p in physical),max(p["gamma"] for p in physical)],
            numerical_effect_resolution="NOT_CLAIMED_WHEN_BELOW_REGISTERED_TOLERANCE"),
        single_mode_invariant=False,higher_harmonic_force_ratio="1/5",
        ordinary_cubic_Taylor_vertices_available=False,
        probe_Legendre_regular=True,full_action_Legendre_regular="NOT_DETERMINED",
        full_coupled_classical_uniqueness="NOT_DETERMINED",
        full_quartic_constraint_reduction_verified=False,
        full_finite_density_scattering_verified=False,physical_EFT_cutoff="NOT_DERIVED",
        full_physical_validity_domain_verified=False,quantum_inconsistency_proved=False,
        classical_evolution_no_go=False,all_actions_no_go=False,
        frozen_probe_status="PASS_BOUNDED_CLASSICAL_GALERKIN_PROBE" if all(c["passed"] for c in audit.checks) else "FAIL",
        physical_amplitude_bound="NOT_DERIVED",background_evolution="FROZEN_PROBE_ONLY",
        physics_pass=False,gate_effect="NONE",Rule9_cleared=False,review_status="DEFERRED",
        claim_status="Conditional",research_execution="PROCEED_PROVISIONALLY",
        canonical_tests_1_to_3="HOLD_SUBSTANTIVE",MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",
        K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED",TOP_X4="UNCHANGED",
        review_dependencies=["R9-MT1-G3V-CROSSCHECK","R9-MT1-G3V","R9-MT1-G3V-V1-INTEGRITY",
                             "all parent direct/transitive scientific and review holds"])
    return (summary,cases), formulas, audit


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--replay",action="store_true")
    ap.add_argument("--symbolic-only",action="store_true")
    args = ap.parse_args()
    if args.replay and args.symbolic_only:
        ap.error("replay and symbolic-only are separate modes")
    if not args.replay and not args.symbolic_only and OUT.exists():
        raise SystemExit("Existing output directory: refusing overwrite; use --replay.")
    if args.replay and not OUT.is_dir():
        raise SystemExit("Replay needs the existing sealed output directory.")
    values, formulas, audit = evaluate(args.symbolic_only)
    failures = [c for c in audit.checks if not c["passed"]]
    if args.symbolic_only:
        print(json.dumps(dict(mode="symbolic-only",passed=len(audit.checks)-len(failures),
                              total=len(audit.checks),failures=failures),indent=2))
        return 1 if failures else 0
    summary,cases = values
    outputs = {"formulas.json":payload(formulas),"cases.json":payload(cases),"summary.json":payload(summary)}
    if args.replay:
        for name,data in outputs.items():
            path = OUT/name
            if path.read_bytes() != data:
                raise RuntimeError(f"replay is not byte-identical: {name}")
            if Path(str(path)+".sha256").read_text().split()[0] != digest(data):
                raise RuntimeError(f"replay sidecar mismatch: {name}")
    else:
        OUT.mkdir(parents=True,exist_ok=False)
        for name,data in outputs.items():
            path = OUT/name
            with path.open("xb") as stream:
                stream.write(data)
            with Path(str(path)+".sha256").open("x",encoding="utf-8",newline="\n") as stream:
                stream.write(f"{digest(data)}  {name}\n")
    print(json.dumps({k:summary[k] for k in ("validation","passed","total","status","physics_pass",
                                          "review_status","numerical_summary")},indent=2))
    if failures:
        print(json.dumps(dict(failures=failures),indent=2))
    if args.replay:
        print("All three G3N1 JSON artifacts replay byte-identically; originals are untouched.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

