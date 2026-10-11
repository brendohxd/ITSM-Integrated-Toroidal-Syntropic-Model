"""G3K-C2 v1: coupled scalar principal symbol in the global dust-time chart.

A failed strong-hyperbolicity route is not a physical ghost/all-norm no-go.
Uses immutable parent action/receipts; no parent is executed or modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT / HELPER).read_bytes()).hexdigest() != "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper identity changed")
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FROZEN = {
    "Theory/Gates/RES-001/RES001_R4C1_G3K_C2_PRINCIPAL_TIME_DOMAIN_CONTRACT_2026-10-09.md":
        "ee6dbfbcc0a572f812c02f52b0bf3794a91aeb45ccd494f81e73383b5ecdb339",
    "Theory/Gates/RES-001/RES001_R4C1_G3K_C1_CLOCK_ENTRY_REPORT_2026-10-09.md":
        "ccab89c81f331cc7fc0288e998cf190311119b5f1c3717bd48d32752b32aee7c",
    BASE + "r4c1_g3k_c1_attempt_02/summary.json":
        "39818742f14afe951780c20425b206128b11bf8007e3b84efd5743979e3262e7",
    BASE + "r4c1_g3k_c1_attempt_02/samples.json":
        "339373b084ba6b73c2eda87b58c215564afb86dab1ea55dbe3b68267e88c4cff",
    "Analysis/MasterTests/test_01_r4c1_g3_finite_k_scalar.py":
        "05f3c588d8424a9d7f65c69624b483394144da5ae242c75c54f238ef895e37de",
    BASE + "r4c1_g3k_attempt_02/formulas.json":
        "b369f337b38fd29c8d6c16b4fed6bf787069089c682c9c639c38224e161bf8d5",
    BASE + "r4c1_g3k_attempt_02/matrices.npy":
        "48cdb08629a4b1a252c62de632b7cf82d97e8f7b554c93a14376ef7c93ba3989",
    BASE + "r4c1_g3k_attempt_02/samples.json":
        "69102fff332222f34684151e08a218fd92c6ae7a5153fd49d5900cf9e4b430d5",
}
QN = ("xi", "w", "u", "v", "r", "psi", "z")


def tidy(expr):
    return s.factor(s.cancel(expr))


def exact(checks, name, expr):
    vals = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    reduced = [tidy(v) for v in vals]
    checks.add(name, all(v == 0 for v in reduced),
               "zero_exact" if all(v == 0 for v in reduced) else [str(v) for v in reduced], "zero_exact")


def relative_matrix(a, b):
    return float(np.linalg.norm(a - b) / max(1.0, np.linalg.norm(a), np.linalg.norm(b)))


def text_matrix(matrix):
    return [[str(v) for v in matrix.row(i)] for i in range(matrix.rows)]


def symbolic(checks, parameter_names, parent_formulas):
    names = set(parent_formulas["jet_order"]) | set(parameter_names) | {"ap", "bp", "Hx", "Hy"}
    symbols = {name: s.Symbol(name, real=True) for name in names}
    symbols["ap"], symbols["bp"] = s.symbols("ap bp", positive=True)
    # The pinned expression is scientific input, not instructions or arbitrary code.
    L = s.sympify(parent_formulas["dust_clock_scalar_action"], locals=symbols)
    q = [symbols[name] for name in QN]
    d = [symbols[name + "_dot"] for name in QN]
    x = [symbols[name + "_x"] for name in QN]
    B, Bx = symbols["B"], symbols["B_x"]
    zero = {q[0]: 0, d[0]: 0, B: 0, Bx: 0, **{xx: 0 for xx in x}}
    exact(checks, "no_shift_B_mass", s.diff(L, B, B).subs(zero))
    exact(checks, "no_shift_B_q_couplings", s.Matrix([s.diff(L, B, a).subs(zero) for a in q]))
    exact(checks, "no_shift_B_velocity_couplings", s.Matrix([s.diff(L, B, a).subs(zero) for a in d]))
    checks.add("no_B_velocity_in_frozen_action", not any(str(v) == "B_dot" for v in L.free_symbols))
    print("Deriving coupled principal Hessian and retained shift symbol...", flush=True)
    H = s.hessian(L, d + x + [Bx]).subs(zero).applyfunc(tidy)
    T, M, S = H[:7, :7], H[:7, 7:14], H[7:14, 7:14]
    fd, fx, bh = H[14, :7], H[14, 7:14], H[14, 14]
    ap, bp = symbols["ap"], symbols["bp"]
    w, beta, psi, b = symbols["w"], symbols["beta"], symbols["psi"], symbols["b"]
    N, Vol = s.exp(-beta * psi), ap * bp**2
    nu = s.Symbol("nu", real=True)
    c = N * nu / ap
    top = c**2 * T - c * (M + M.T) + S
    cross = (-c * fd + fx).T
    raw = top.row_join(cross).col_join(cross.T.row_join(s.Matrix([[bh]])))
    D8 = s.diag(*([1] * 7 + [N]))
    Q8 = (ap**2 / (N * Vol) * D8.T * raw * D8).applyfunc(tidy)
    h = -b * (w * nu - s.sqrt(1 + w*w))**2
    exact(checks, "exact_regulator_principal_psi_z", Q8[5, 6] - h)
    exact(checks, "exact_regulator_principal_z_diagonal", Q8[6, 6])
    exact(checks, "exact_regulator_no_other_principal_columns", s.Matrix([Q8[i, 6] for i in (0, 1, 2, 3, 4, 7)]))
    Q7 = (Q8[:7, :7] - Q8[:7, 7] * Q8[7, :7] / Q8[7, 7]).applyfunc(tidy)
    Tb = Q7.diff(nu, 2).applyfunc(tidy) / 2
    Rb = (-Q7.diff(nu).subs(nu, 0)).applyfunc(tidy)
    Sb = Q7.subs(nu, 0).applyfunc(tidy)
    exact(checks, "quadratic_principal_polynomial", Q7 - (nu**2 * Tb - nu * Rb + Sb))
    exact(checks, "principal_regulator_kinetic_row", Tb[6, :] - s.Matrix([[0, 0, 0, 0, 0, -b*w*w, 0]]))
    print("Factoring complete coupled characteristic polynomial...", flush=True)
    det5 = tidy(Q7[:5, :5].det(method="laplace"))
    det7 = tidy(Q7.det(method="laplace"))
    exact(checks, "exact_full_characteristic_factor", det7 + b*b*(w*nu-s.sqrt(1+w*w))**4*det5)
    nu_star = s.sqrt(1+w*w)/w
    at_star = Q7.subs(nu, nu_star).applyfunc(tidy)
    exact(checks, "exact_transport_null_direction", at_star[:, 6])
    eta = s.Symbol("eta", positive=True)
    g3 = {symbols["MP2"]: 1, symbols["MU2"]: 2*eta/3,
          symbols["c1"]: s.Rational(1, 5), symbols["c2"]: -s.Rational(7, 48),
          symbols["c3"]: -s.Rational(1, 80), symbols["c4"]: s.Rational(1, 20),
          symbols["K"]: 3*eta, beta: 2*eta**2/5, symbols["zeta"]: eta/13}
    exact(checks, "exact_shift_rank_surface", Q8[7, 7].subs(g3) + eta*(1-5*w*w)/36)
    exact(checks, "unreduced_shift_boundary_only", Q8[7, 7].subs(g3).subs(w, 1/s.sqrt(5)))
    at_family = at_star.subs(g3).applyfunc(tidy)
    minor5 = tidy(at_family[:5, :5].det(method="laplace"))
    minor6 = tidy(at_family[:6, :6].det(method="laplace"))
    checks.add("transport_minors_background_independent", (minor5.free_symbols | minor6.free_symbols) <= {eta, w},
               sorted(str(v) for v in minor5.free_symbols | minor6.free_symbols), "only eta,w")
    kinetic_minor = tidy(Tb[:5, :5].subs(g3).det(method="laplace"))
    exact(checks, "exact_kinetic_regulator_factor", tidy(Tb.det(method="laplace")) + b*b*w**4*tidy(Tb[:5, :5].det(method="laplace")))
    checks.add("kinetic_minor_symbol_dependencies", kinetic_minor.free_symbols <= {eta, w, symbols["u"], symbols["v"]},
               sorted(str(v) for v in kinetic_minor.free_symbols))
    # Independent fixed-frame control, including its algebraic preferred z shell.
    K, C, bc, wc, nc = s.symbols("K_control C_control b_control w_control nu_control", real=True)
    gc = s.sqrt(1+wc*wc)
    sig = wc*nc-gc
    comparator = s.Matrix([[K*(gc*nc-wc)**2-K*C*sig**2, -bc*sig**2], [-bc*sig**2, 0]])
    exact(checks, "healthy_comparator_principal_factor", comparator.det()+bc*bc*sig**4)
    exact(checks, "healthy_comparator_transport_minor", comparator[0, 0].subs(nc, gc/wc)-K/wc**2)
    exact(checks, "aligned_regulator_has_no_time_row", Tb[6, :].subs(w, 0))
    P, Omega = s.symbols("P Omega", real=True)
    exact(checks, "healthy_preferred_elimination_dispersion", (K*Omega**2-K*C*P**2-bc*P**4)/K
          - (Omega**2-C*P**2-(bc/K)*P**4))
    variables = tuple(sorted((Tb.free_symbols | Rb.free_symbols | Sb.free_symbols) - {nu}, key=str))
    coeff = s.lambdify(variables, (Tb, Rb, Sb), "numpy", cse=True)
    speed_symbol = s.lambdify(variables + (nu,), Q7, "numpy", cse=True)
    formulas = {
        "fields": list(QN), "nu": "a_parallel*omega/(N*k)",
        "shift_variable": "B=N*b_shift; no shift constraint removed before principal construction",
        "normalized_Q8": text_matrix(Q8), "normalized_Q7": text_matrix(Q7),
        "Tbar": text_matrix(Tb), "Rbar": text_matrix(Rb), "Sbar": text_matrix(Sb),
        "regulator_principal_mixing": str(h), "nu_star": str(nu_star),
        "full_characteristic_determinant": str(det7), "other_five_field_determinant": str(det5),
        "G3_transport_minor5": str(minor5), "G3_transport_minor6": str(minor6),
        "G3_kinetic_minor5": str(kinetic_minor),
        "exact_multiplicity_argument": "det Q7=-b^2*(w*nu-gamma)^4*det Q5. If det Q5(nu_star)!=0, multiplicity is exactly four. If the six-field minor is nonzero, ker Q7(nu_star) is precisely span(e_z), so geometric multiplicity is one.",
        "companion": "C14=[0,I;-Tbar^-1*Sbar,Tbar^-1*Rbar]; eigenvector=(q,nu*q), with Q7(nu)*q=0",
        "norm_and_scope": "Conventional q/first-derivative Fourier reduction; no all-norm or nonlinear ill-posedness theorem.",
        "k_polynomial_orders": "H_BB=H_Bq=H_Bd=0; F=-ik*fd,G=ik*g1+k^2*fx,A=k^2*bh. Hence Tred is constant, Wred linear and Vred quadratic in k at a fixed background; their time derivatives have lower differential order.",
        "healthy_comparator": {"det": str(comparator.det()), "preferred_dispersion": "Omega^2=C*P^2+(b/K)*P^4, K,b>0,C>=0", "restriction": "Tilted conventional reduction defect is not a preferred-frame ghost."},
        "mathematical_reference": "https://arxiv.org/pdf/gr-qc/0506037, sections I-II,V",
        "nonclaims": ["No physical ghost or instability proven", "No all-action/all-clock/all-norm no-go", "No finite-band EFT or cutoff derived", "No w=0 or w^2=1/5 divided continuation", "No full nonlinear or arbitrary-direction Cauchy theorem"],
    }
    return symbols, variables, coeff, speed_symbol, eta, minor5, minor6, kinetic_minor, formulas


def calculate():
    for name, expected in FROZEN.items():
        if common.sha((ROOT/name).read_bytes()) != expected:
            raise RuntimeError("Frozen input mismatch: " + name)
    c1_summary = common.read_json(BASE + "r4c1_g3k_c1_attempt_02/summary.json")
    pins = dict(c1_summary["source_sha256"])
    for name, value in FROZEN.items():
        if name in pins and pins[name] != value:
            raise RuntimeError("Conflicting source pin: " + name)
        pins[name] = value
    pins[SELF] = common.sha((ROOT/SELF).read_bytes())
    missing = common.inspect_pins(pins)
    checks = common.Checks()
    checks.add("source_pins_and_available_sidecars_before", True, {"pins": len(pins), "available_sidecars": len(pins)-len(missing), "absent": missing})
    family = common.read_json(BASE + "r4c1_g3_attempt_01/summary.json")
    params = {float(r["eta"]): r["parameters"] for r in family["family"]}
    parent_formulas = common.read_json(BASE + "r4c1_g3k_attempt_02/formulas.json")
    symbols, variables, coeff, q_eval, eta_symbol, minor5, minor6, kinetic_minor, formulas = symbolic(checks, list(next(iter(params.values()))), parent_formulas)
    inputs = common.read_json(BASE + "r4c1_g3k_c1_attempt_02/samples.json")["background_events"]
    parent_samples = common.read_json(BASE + "r4c1_g3k_attempt_02/samples.json")
    matrices = np.load(ROOT/(BASE+"r4c1_g3k_attempt_02/matrices.npy"), allow_pickle=False)
    checks.add("parent_matrix_shape", matrices.shape == (120, 5, 7, 7), list(matrices.shape))
    indexed = {(r["eta"],r["tilt"],r["t"],r["method"],r["k"]): matrices[i]
               for i,r in enumerate(parent_samples["events"])}
    rows = []
    for i, event in enumerate(inputs):
        p = params[float(event["eta"])]; y = event["state"]
        values = dict(p)
        values.update(dict(ap=np.exp(y[0]+2*y[1]), bp=np.exp(y[0]-y[1]), Hx=y[8]+2*y[9], Hy=y[8]-y[9], xi=0.0, xi_dot=0.0, B=0.0, B_x=0.0))
        for j,name in enumerate(QN[1:], start=2):
            values[name] = y[j]; values[name+"_dot"] = y[j+8]
        args = tuple(float(values[str(v)]) for v in variables)
        T,R,S = [np.asarray(a,float) for a in coeff(*args)]
        w = y[2]; nu_star = float(np.sqrt(1+w*w)/w)
        label = f"jet_{i}"
        checks.add(label+"_registered_smooth_regular_chart", w>0 and event["Y"]>0 and abs(1-5*w*w)>0 and p["b"]>0)
        expected_beta=2*event["eta"]**2/5
        checks.small(label+"_exact_G3_family_beta", common.discrepancy(p["beta"],expected_beta))
        key=(event["eta"],event["tilt"],event["t"],event["method"])
        archived=[indexed[(*key,k)] for k in (20.0,40.0,80.0)]
        ap,bp,N=values["ap"],values["bp"],np.exp(-p["beta"]*y[6]);Vol=ap*bp*bp
        w1=(archived[2][1]-archived[0][1])/60
        w0=archived[0][1]-20*w1
        vv=np.stack([a[2].reshape(-1) for a in archived])
        vc=np.linalg.solve(np.array([[1,20,400],[1,40,1600],[1,80,6400]],float),vv)
        leadingV=vc[2].reshape(7,7)
        inheritedT=N/Vol*archived[0][0]
        inheritedR=ap/Vol*(w1-w1.conj().T)/1j
        inheritedS=ap*ap/(N*Vol)*leadingV
        archive_errors={"T":relative_matrix(T,inheritedT),"R":relative_matrix(R,inheritedR),"S":relative_matrix(S,inheritedS),
                        "linear_W":relative_matrix(archived[1][1],w0+40*w1),
                        "constant_T":max(relative_matrix(a[0],archived[0][0]) for a in archived)}
        checks.small(label+"_independent_archive_principal_match", max(archive_errors.values()))
        ws=s.Rational(str(w)); es=s.Rational(str(event["eta"]))
        replacements={eta_symbol:es,symbols["w"]:ws}
        exact5=tidy(minor5.subs(replacements)); exact6=tidy(minor6.subs(replacements))
        checks.add(label+"_exact_transport_minors_nonzero", exact5!=0 and exact6!=0
                   and not exact5.free_symbols and not exact6.free_symbols,
                   {"minor5":str(exact5),"minor6":str(exact6)}, "nonzero exact registered-family expressions at archived eta,w")
        kinetic_values={**replacements,symbols["u"]:s.Rational(str(y[3])),symbols["v"]:s.Rational(str(y[4]))}
        exact_kinetic=tidy(kinetic_minor.subs(kinetic_values))
        checks.add(label+"_exact_kinetic_minor_nonzero", exact_kinetic!=0 and not exact_kinetic.free_symbols, str(exact_kinetic))
        scale=np.maximum(abs(np.diag(T)),1e-30)
        scale[6]=abs(T[5,6])**2/max(abs(T[5,5]),abs(T[5,6]),1e-30)
        D=np.diag(1/np.sqrt(scale));Tc=D.T@T@D;Rc=D.T@R@D;Sc=D.T@S@D
        Q=T*nu_star**2-R*nu_star+S
        Qc=D.T@Q@D
        sv=np.linalg.svd(Qc[:6,:6],compute_uv=False); gap=float(sv[-1]/sv[0])
        checks.add(label+"_six_field_rank_margin", gap>=1e-8,gap,"min/max nonzero singular value >=1e-8")
        e=np.zeros(7);e[6]=1
        checks.small(label+"_explicit_principal_null_direction",float(np.linalg.norm(Qc@e)/max(1.0,np.linalg.norm(Qc))))
        companion=np.block([[np.zeros((7,7)),np.eye(7)],[-np.linalg.solve(Tc,Sc),np.linalg.solve(Tc,Rc)]])
        vector=np.r_[e,nu_star*e]
        checks.small(label+"_companion_kernel_relation",float(np.linalg.norm(companion@vector-nu_star*vector)/(max(1.0,np.linalg.norm(companion))*np.linalg.norm(vector))))
        T5,R5,S5=Tc[:5,:5],Rc[:5,:5],Sc[:5,:5]
        M5=np.block([[np.zeros((5,5)),np.eye(5)],[-np.linalg.solve(T5,S5),np.linalg.solve(T5,R5)]])
        speeds,vectors=np.linalg.eig(M5)
        roots=[];residuals=[]
        for nu,vec in zip(speeds,vectors.T):
            q=np.zeros(7,complex);q[:5]=D[:5,:5]@vec[:5]
            Qnu=np.asarray(q_eval(*(args+(nu,))),complex)
            q[6]=-(Qnu[5,:5]@q[:5])/Qnu[5,6]
            error=float(np.linalg.norm(Qnu@q)/max((abs(nu)**2*np.linalg.norm(T)+abs(nu)*np.linalg.norm(R)+np.linalg.norm(S))*np.linalg.norm(q),1e-300))
            roots.append([float(nu.real),float(nu.imag)]);residuals.append(error)
        checks.add(label+"_all_other_characteristic_eigenpairs",max(residuals)<=1e-7,max(residuals),"<=1e-7; no health selection")
        checks.add(label+"_fourfold_transport_defect",len(roots)==10 and exact5!=0 and exact6!=0 and gap>=1e-8,
                   {"algebraic_multiplicity":4,"geometric_multiplicity":1}, "exact factor and nonzero minors, not numerical root splitting")
        rows.append({"eta":event["eta"],"tilt":event["tilt"],"t":event["t"],"method":event["method"],
                     "nu_star":nu_star,"transport_algebraic_multiplicity":4,"transport_geometric_multiplicity":1,
                     "all_characteristic_roots":roots+[[nu_star,0.0]]*4,
                     "other_root_residuals":residuals,"archive_principal_errors":archive_errors,
                     "six_field_rank_margin":gap,"exact_minor5":str(exact5),"exact_minor6":str(exact6),
                     "exact_kinetic_minor5":str(exact_kinetic),
                     "principal_T_condition":float(np.linalg.cond(Tc)),
                     "disposition":"defective conventional unrestricted dust-time principal reduction; no physical ghost claim"})
    checks.add("forty_method_tagged_jets_retained",len(rows)==40)
    checks.add("all_1680_parent_finite_frequency_roots_retained",len(parent_samples["events"])==120 and all(len(r["roots"])==14 for r in parent_samples["events"]))
    checks.add("all_source_pins_after", common.inspect_pins(pins)==missing)
    payloads={"formulas.json":common.encode(formulas),"samples.json":common.encode({"principal_events":rows,"parent_events_unchanged_no_mode_selection":parent_samples["events"],"inherited_failed_parent_assertions":[r for r in family["checks"] if not r["passed"]]})}
    passed=sum(r["passed"] for r in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3k-c2-principal-domain-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
             "passed":passed,"total":len(checks.rows),"checks":checks.rows,
             "status":"COUPLED_UNRESTRICTED_STRONGLY_HYPERBOLIC_DUST_TIME_ROUTE_REJECTED" if ok else "PRINCIPAL_DOMAIN_AUDIT_REQUIRES_DISPOSITION",
             "source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],
             "artifacts":{name:common.sha(data) for name,data in payloads.items()},"inherited_sidecars_absent":missing,
             "principal_state_records":len(rows),"eta_tilt_time_coordinates":32,"parent_root_count":1680,
             "max_principal_archive_discrepancy":max(max(r["archive_principal_errors"].values()) for r in rows),
             "min_six_field_rank_margin":min(r["six_field_rank_margin"] for r in rows),
             "max_other_characteristic_residual":max(max(r["other_root_residuals"]) for r in rows),
             "physical_ghost_proven":False,"physical_instability_proven":False,"all_norms_illposedness_proven":False,
             "finite_band_physical_domain_verified":False,"physical_EFT_cutoff_derived":False,"all_action_no_go":False,
             "strong_hyperbolicity_in_unrestricted_dust_time_verified":False,
             "review_status":"DEFERRED","Rule9_cleared":False,"review_dependencies":["R9-MT1-G3K-C1","all transitive G3K/C1 scientific and review debt"],
             "physics_pass":False,"gate_effect":"NONE","canonical_tests_1_to_3":"HOLD_SUBSTANTIVE",
             "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
             "runtime":{"python":platform.python_version(),"numpy":np.__version__,"sympy":s.__version__}}
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_g3k_c2_attempt_01")
    parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError("Replay directory absent")
    if not args.replay and dest.exists():raise FileExistsError("Refuse existing scientific output")
    payloads,summary=calculate()
    if args.replay:
        for name,data in payloads.items():
            if (dest/name).read_bytes()!=data:raise RuntimeError("Replay bytes differ: "+name)
            if (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":raise RuntimeError("Replay sidecar differs: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in payloads.items():
            with (dest/name).open("xb") as handle:handle.write(data)
            with (dest/(name+".sha256")).open("xb") as handle:handle.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect","Rule9_cleared")}}))
    for check in summary["checks"]:
        if not check["passed"]:print(json.dumps(check))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
