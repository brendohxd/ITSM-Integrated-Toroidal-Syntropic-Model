"""G3Z: finite-rate inner frequency pencil of G3's zero-speed sector.

Frozen-event asymptotics only, not an evolving-mode or physical-cutoff proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import sympy as s
from scipy.optimize import linear_sum_assignment

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"Analysis/MasterTests/outputs"
PINS={
    "Theory/Gates/RES-001/RES001_R4C1_G3_ZERO_INNER_CONTRACT_2026-09-30.md":
        "47723c96936643b6be19d22e00a4f98bc3f4208cb409e61c255e041b7ce725e5",
    "Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_SCALAR_REPORT_2026-09-30.md":
        "4d2ea777b8edfb23e52438e271286b8990da2f1720acb05dbd4707f8efb43de7",
    "Theory/Gates/RES-001/RES001_R4C1_ZERO_BRANCH_REPORT_2026-09-26.md":
        "16f50f7150cddff8c297d237441fd9aabedb9f4f9c6f341b180160c508b619e5",
    "Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/summary.json":
        "550caae54b03b490a5388ecd363ad0f9ff0d8d4891021d2eb1c366871d54378a",
    "Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/matrices.json":
        "1877c4b4412e37b15ed6297d099ff12302c59cdad929858085b97178eae47355",
    "Analysis/MasterTests/test_01_r4c1_equal_newton_scalar.py":
        "eb5d8c41938d346a294aa03f713ea10655b939234dab7935f4a0ee9f774553f9",
}


def sha(content):
    return hashlib.sha256(content).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:
            raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: "+name)


def derive(audit):
    import test_01_r4c1_scalar_constraints as base
    symbols={str(val):val for val in vars(base).values() if isinstance(val,s.Symbol)}
    eta=s.Symbol("eta",positive=True)
    symbols["eta"]=eta
    raw=json.loads((OUT/"r4c1_g3s_attempt_01/matrices.json").read_bytes())
    def mat(key):
        return s.Matrix([[s.sympify(val,locals=symbols) for val in row] for row in raw[key]])
    G,W=mat("G"),mat("W")
    p=s.Symbol("p",positive=True); lam=s.Symbol("lambda",real=True)
    def coeff(mat):
        polys=[s.Poly(s.cancel(val.subs(base.k,base.a*p)),p) for val in mat]
        return [s.Matrix(6,6,[poly.nth(j) for poly in polys]) for j in range(5)]
    gc,wc=coeff(G),coeff(W)
    pc=[wc[j]+lam*gc[j]+(lam**2*s.eye(6) if j==0 else s.zeros(6)) for j in range(5)]
    audit.exact("single_quartic_force_block",pc[4]-s.diag(0,0,0,s.Rational(5,33),0,0))
    slow=[0,1,2,4,5]; fast=3
    f4,f3,f2=[pc[j][fast,fast] for j in (4,3,2)]
    inverse={4:1/f4,5:-f3/f4**2,6:f3**2/f4**3-f2/f4**2}
    def correction(i,j,power,inv):
        return sum(pc[r][i,fast]*pc[t][fast,j]*val for r in range(4)
                   for t in range(4) for q,val in inv.items() if r+t-q==power)
    jet=[]; simple=[]
    for power in range(3):
        jet.append(s.Matrix(5,5,lambda i,j:s.factor(s.cancel(
            pc[power][slow[i],slow[j]]-correction(slow[i],slow[j],power,inverse)))))
        simple.append(s.Matrix(5,5,lambda i,j:s.factor(s.cancel(
            pc[power][slow[i],slow[j]]-correction(slow[i],slow[j],power,{4:1/f4})))))
    weights=[1,1,1,1,0]
    limit=s.zeros(5)
    for i in range(5):
        for j in range(5):
            degree=weights[i]+weights[j]
            for power in range(degree+1,3):
                audit.exact(f"scaled_divergence_cancellation_{i}_{j}_{power}",jet[power][i,j])
            limit[i,j]=jet[degree][i,j]
    audit.exact("propagating_limit_matches_G3S",limit[:4,:4]-mat("leading")[:4,:4])
    audit.test("propagating_limit_lambda_independent",all(not val.has(lam) for val in limit[:4,:4]))
    inverse_wave=limit[:4,:4].inv()
    inner=s.factor(s.cancel(limit[4,4]-(limit[4,:4]*inverse_wave*limit[:4,4])[0]))
    polynomial=s.Poly(inner,lam)
    audit.test("inner_degree_recorded",polynomial.degree()==2,int(polynomial.degree()),"degree two or report unresolved")
    coefficients=[s.factor(polynomial.nth(j)) for j in range(3)]
    audit.exact("inner_lambda2_comparator",coefficients[2]+(12-eta)/eta)
    normalized=[s.factor(s.cancel(val/coefficients[2])) for val in coefficients]
    audit.test("reject_fast_denominator_subleading_omission",
               any(s.factor(val)!=0 for val in jet[0]-simple[0]))
    print("Derived G3Z finite-rate quadratic; checking independent rational Schur limit...",flush=True)
    event={base.a:s.Rational(7,5),base.H:s.Rational(3,5),base.u:s.Rational(2,3),
        base.ud:s.Rational(1,7),base.v:s.Rational(1,5),base.vd:s.Rational(2,7),
        base.r:s.Rational(1,4),base.rd:-s.Rational(1,9),base.pd:s.Rational(1,8),
        base.rho:s.Rational(1,10),base.C:s.Rational(6,5),eta:s.Rational(1,4),lam:s.Rational(2,5)}
    P=sum((pc[j]*p**j for j in range(5)),s.zeros(6)).subs(event)
    schur=P.extract(slow,slow)-P.extract(slow,[fast])*P.extract([fast],slow)/P[fast,fast]
    scale=s.diag(1/p,1/p,1/p,1/p,1)
    exact_limit=(scale*schur*scale).applyfunc(lambda val:s.limit(s.cancel(val),p,s.oo))
    audit.exact("independent_exact_rational_Schur_limit",exact_limit-limit.subs(event))
    return dict(base=base,eta=eta,p=p,lam=lam,G=G,W=W,limit=limit,inner=inner,
                coefficients=coefficients,normalized=normalized,fast_inverse=inverse)


def numerical(audit,data,parent):
    import test_01_r4c1_equal_newton_scalar as gs
    b=data["base"]; eta=data["eta"]
    args=[getattr(b,name) for name in ("a","H","u","ud","v","vd","r","rd","pd","rho","C")]+[b.k,eta]
    quadratic=s.lambdify(args,data["normalized"],"numpy",cse=True)
    fG=s.lambdify(args,data["G"],"numpy",cse=True)
    fW=s.lambdify(args,data["W"],"numpy",cse=True)
    family=json.loads((OUT/"r4c1_g3_attempt_01/summary.json").read_bytes())
    trajectories=np.load(OUT/"r4c1_g3_attempt_01/trajectories.npy",allow_pickle=False)
    saved={(row["eta"],row["method"],row["t"]):row for row in parent["numerical"]["records"]}
    rows=[]; worst=0.; residual=0.; maxroot=-np.inf; mincoeff=np.inf
    for ie,member in enumerate(family["family"]):
        e=member["eta"]; params=member["parameters"]
        for im,method in enumerate(family["trajectory"]["methods"]):
            tr=trajectories[ie,im]
            for t in (0.,.5,1.,2.,3.,4.):
                state=tr[1:,int(round(200*t))]
                a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=state
                values=[a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params["beta"]*psi),1.,e]
                coefficients=np.asarray(quadratic(*values),float)
                inner_roots=np.roots(coefficients[::-1])
                maxroot=max(maxroot,float(np.max(inner_roots.real)))
                mincoeff=min(mincoeff,float(abs(-(12-e)/e)))
                row=dict(eta=e,method=method,t=t,normalized_coefficients=coefficients.tolist(),
                         inner_roots=gs.complex_values(inner_roots),samples=[])
                original=saved[(e,method,t)]
                for sample in original["samples"]:
                    p=sample["p"]; values[-2]=a*p
                    full=np.array([complex(*z) for z in sample["exponents"]])
                    cost=abs(inner_roots[:,None]-full[None,:])/(1+abs(inner_roots[:,None]))
                    ii,jj=linear_sum_assignment(cost)
                    err=float(np.max(cost[ii,jj])); matched=full[jj]
                    G=np.asarray(fG(*values),float);W=np.asarray(fW(*values),float)
                    recomputed=np.linalg.eigvals(gs.generator(G,W))
                    ci,cj=linear_sum_assignment(abs(full[:,None]-recomputed[None,:])/(1+abs(full[:,None])))
                    residual=max(residual,float(np.max(abs(full[ci]-recomputed[cj])/(1+abs(full[ci])))))
                    if p==160.: worst=max(worst,err)
                    row["samples"].append(dict(p=p,normalized_matching_error=err,
                                             matched_roots=gs.complex_values(matched)))
                rows.append(row)
    audit.test("all_sampled_quadratics_regular",mincoeff>0,mincoeff,"nonzero leading coefficient; exact eta-domain stated")
    audit.test("recomputed_full_pencil_matches_pinned_roots",residual<1e-8,residual,"normalized <1e-8")
    return dict(records=rows,max_p160_inner_matching_error=worst,
        diagnostic_reach="SUPPORTED_AT_REGISTERED_SAMPLES" if worst<.05 else "NONASYMPTOTIC_OR_UNRESOLVED",
        max_recomputed_full_root_discrepancy=residual,max_inner_real_exponent=maxroot,
        min_absolute_lambda2_coefficient=mincoeff)


def evaluate():
    verify(PINS)
    parent=json.loads((OUT/"r4c1_g3s_attempt_01/summary.json").read_bytes())
    transitive={**parent["source_sha256"],**parent["transitive_source_sha256"]}
    verify(transitive)
    import test_01_r4c1_equal_newton_scalar as gs
    audit=gs.Audit()
    data=derive(audit)
    numerical_data=numerical(audit,data,parent)
    payload=dict(inner_pencil=str(data["inner"]),coefficient_order=["lambda^0","lambda^1","lambda^2"],
        coefficients=list(map(str,data["coefficients"])),normalized_coefficients=list(map(str,data["normalized"])),
        scaled_finite_limit=[[str(val) for val in row] for row in data["limit"].tolist()],
        inverse_fast_series={str(j):str(val) for j,val in data["fast_inverse"].items()},
        scope="Frozen canonical frequency event at fixed lambda as physical p tends to infinity; not a time-evolution theorem")
    passed=sum(check["passed"] for check in audit.checks)
    summary=dict(schema="r4c1-g3z-v1",validation="PASS_LOCAL_CHECKS" if passed==len(audit.checks) else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,
        transitive_source_sha256=transitive,script_sha256=sha(Path(__file__).read_bytes()),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        numerical=numerical_data,status="CONDITIONAL_G3_FINITE_RATE_INNER_PENCIL_EVOLUTION_AND_EFT_OPEN",
        physics_pass=False,gate_effect="NONE",review_status="DEFERRED",Rule9_cleared=False,
        canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        full_IVP_verified=False,healthy_continuous_GR_limit_verified=False,physical_EFT_cutoff_derived=False,
        MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED")
    encoded=(json.dumps(payload,indent=2,allow_nan=False)+"\n").encode("utf-8")
    summary["artifacts"]={"pencil.json":sha(encoded)}
    return summary,encoded


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3z_attempt_01")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()): raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify(PINS)
    if not args.replay and directory.exists(): raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record,payload=evaluate()
    encoded=(json.dumps(record,indent=2,allow_nan=False)+"\n").encode("utf-8")
    identical=None
    if args.replay:
        identical=(directory/"summary.json").read_bytes()==encoded and (directory/"pencil.json").read_bytes()==payload
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(encoded))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,content in (("summary.json",encoded),("pencil.json",payload)):
            (directory/name).write_bytes(content)
            (directory/(name+".sha256")).write_text(sha(content)+"  "+name+"\n",encoding="ascii")
    print(json.dumps({key:record[key] for key in ("validation","passed","total","status","physics_pass")}))
    for check in record["checks"]:
        if not check["passed"]: print(json.dumps(check))
    if args.replay and not identical:return 2
    return 0 if record["passed"]==record["total"] else 1


if __name__=="__main__": raise SystemExit(main())
