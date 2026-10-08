"""G3S: coupled scalar symbol on G3's separately frozen equal-Newton family.

Pure import/replay of generic S1 formulas; never invoke an older main().
Finite-momentum roots are formal diagnostics, not EFT-admissibility evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
import sympy as s
from scipy.optimize import linear_sum_assignment

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_BASE = ROOT / "Analysis/MasterTests/outputs"
PINS = {
    "Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_SCALAR_CONTRACT_2026-09-30.md":
        "92fc34dd19f2bc5de077703b0e7a8b209c14fdf1ae66674bc1f8176d8e4be1c5",
    "Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md":
        "81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3",
    "Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md":
        "1b9fbc4185b61d1e37d7865baa811994e235523eb9ecc22432c733b4bc38aa04",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json":
        "930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75",
    "Analysis/MasterTests/outputs/r4c1_g3_attempt_01/trajectories.npy":
        "b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json":
        "27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a",
    "Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_summary.json":
        "10bdc2ac1faeb30203cd75f5015ab41e64dd19b6cef37193f6987baf85bfc033",
    "Analysis/MasterTests/test_01_r4c1_scalar_constraints.py":
        "977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed",
    "Analysis/MasterTests/test_01_r4c1_interacting_background.py":
        "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md":
        "0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b",
    "Analysis/MasterTests/test_01_r4c1_scalar_propagation.py":
        "745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda",
    "Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md":
        "653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(pins):
    for name, expected in pins.items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: " + name)


class Audit:
    def __init__(self):
        self.checks = []

    def exact(self, name, expr):
        vals = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
        residual = [s.expand(s.factor(val)) for val in vals]
        self.test(name, all(val == 0 for val in residual),
                  "zero_exact" if all(val == 0 for val in residual) else list(map(str, residual)))

    def test(self, name, ok, value=None, criterion=None):
        self.checks.append(dict(name=name, passed=bool(ok), value=value, criterion=criterion))


def derive(audit):
    import test_01_r4c1_scalar_constraints as base
    eta = s.Symbol("eta", positive=True)
    a,H,u,ud,v,vd,r,rd,pd,rho,C,k = [getattr(base, key) for key in
        ("a","H","u","ud","v","vd","r","rd","pd","rho","C","k")]
    subs = {base.MP:1, base.MU:2*eta/3, base.c1:s.Rational(1,5),
        base.c2:-s.Rational(7,48), base.c3:-s.Rational(1,80), base.c4:s.Rational(1,20),
        base.KQ:3*eta, base.b:5*eta/11, base.zeta:eta/13, base.beta:2*eta**2/5,
        base.m2:1, base.l4:s.Rational(1,3), base.l6:s.Rational(1,5),
        base.Lambda:2, base.mr2:2, base.lr:s.Rational(1,7), base.gr:3*eta/7}
    raw = json.loads((OUTPUT_BASE / "test_01_r4c1_scalar_constraints_matrices.json").read_bytes())
    symbols = {str(val):val for val in vars(base).values() if isinstance(val,s.Symbol)}
    def matrix(key):
        return s.Matrix([[s.sympify(val,locals=symbols) for val in row]
                         for row in raw[key]]).subs(subs)
    K,M,V,pre = [matrix(key) for key in ("K","M","V","preconstraint_hessian")]
    mc2 = 1-eta/12
    mass = 1+(u*u+v*v)/6+(u*u+v*v)**2/80+3*eta*r*r/14
    flow = {a:a*H, H:-(ud**2+vd**2+rd**2+3*eta*pd**2+rho)/(2*mc2),
        u:ud, ud:-3*H*ud-mass*u, v:vd, vd:-3*H*vd-mass*v,
        r:rd, rd:-3*H*rd-2*r-r**3/7-3*eta*(u*u+v*v)*r/14,
        pd:-3*H*pd-2*eta*rho/15, rho:(-3*H+2*eta**2*pd/5)*rho,
        C:2*eta**2*pd*C/5}
    def tidy(mat):
        return mat.applyfunc(s.cancel)
    def dt(expr):
        if isinstance(expr,s.MatrixBase):
            return expr.applyfunc(dt)
        return sum(s.diff(expr,x)*fx for x,fx in flow.items() if expr.has(x))
    J = s.eye(6)
    J[:,4] = s.Matrix([ud,vd,rd,pd,C,k/a])
    dbar = 144*(1-eta/12)*(1-eta/8)/eta
    audit.exact("generic_G3_diagonal_kinetic", J.T*K*J-s.diag(1,1,1,3*eta,dbar*H**2,eta/6))
    R = J*s.diag(1,1,1,1/s.sqrt(3*eta),1/(H*s.sqrt(dbar)),s.sqrt(6/eta))/a**s.Rational(3,2)
    Rt = dt(R)
    audit.exact("full_action_canonical_kinetic",a**3*R.T*K*R-s.eye(6))
    print("Canonicalizing G3 scalar action at symbolic eta...",flush=True)
    Mc = tidy(a**3*(R.T*K*Rt+R.T*M*R))
    Vc = tidy(a**3*(R.T*V*R-Rt.T*K*Rt-Rt.T*M*R-R.T*M.T*Rt))
    G = tidy(Mc-Mc.T)
    W = tidy(Vc+dt(Mc))
    audit.exact("canonical_potential_symmetric",Vc-Vc.T)
    audit.exact("gyro_antisymmetric",G+G.T)
    audit.exact("time_dependent_variational_identity",W-W.T-dt(G))
    B = dt(K)+3*H*K+M-M.T
    E = dt(M)+3*H*M+V
    audit.exact("retained_Euler_velocity_transform",a**3*R.T*(2*K*Rt+B*R)-G)
    audit.exact("retained_Euler_position_transform",a**3*R.T*(K*dt(Rt)+B*Rt+E*R)-W)
    omitted_R = tidy(a**3*R.T*E*R-W)
    audit.test("reject_omitted_canonical_derivatives",any(val!=0 for val in omitted_R))
    p = s.Symbol("p",real=True)
    def coefficients(mat):
        polys = [s.Poly(s.cancel(val.subs(k,a*p)),p) for val in mat]
        deg = max(int(poly.degree()) for poly in polys if not poly.is_zero)
        return [s.Matrix(6,6,[poly.nth(j) for poly in polys]) for j in range(deg+1)]
    vp,gp,wp = [coefficients(mat) for mat in (Vc,G,W)]
    audit.test("spatial_degrees",len(vp)==5 and len(wp)==5 and len(gp)<=2,
               {"Vc":len(vp)-1,"G":len(gp)-1,"W":len(wp)-1})
    audit.exact("quartic_rank_one",wp[4]-s.diag(0,0,0,s.Rational(5,33),0,0))
    audit.exact("quartic_matches_action",wp[4]-vp[4])
    slow = [0,1,2,4,5]
    left,right = wp[3].extract(slow,[3]),wp[3].extract([3],slow)
    leading = tidy(wp[2].extract(slow,slow)-left*right/wp[4][3,3])
    gyro = tidy(gp[1].extract(slow,slow))
    audit.exact("slow_leading_symmetric",leading-leading.T)
    audit.exact("slow_gyro_antisymmetric",gyro+gyro.T)
    audit.test("reject_omitted_fast_elimination",any(val!=0 for val in left*right))
    audit.test("reject_omitted_Mcdot",any(s.factor(val)!=0 for val in wp[2]-vp[2]))
    nu = s.Symbol("nu",real=True)
    pencil = nu**2*s.eye(5)+nu*gyro+leading
    characteristic = s.factor(pencil.det())
    # A falsifiable algebraic comparator, not a substituted dispersion law.
    frame_speed2 = 4/(3*(8-eta))
    expected = nu**2*(nu**2+1)**2*(nu**2+1+eta*(u*u+v*v)/13)*(nu**2+frame_speed2)
    audit.exact("coupled_characteristic_comparator",characteristic-expected)
    A = s.BlockMatrix([[s.zeros(5),s.eye(5)],[-leading,-gyro]]).as_explicit()
    nullity = 10-A.rank()
    alg_zero = next(j for j in range(11) if s.factor(s.expand(characteristic).coeff(nu,j))!=0)
    audit.test("zero_multiplicity_recorded",alg_zero>=nullity>=1,
               {"algebraic":alg_zero,"geometric":int(nullity)})
    audit.exact("eta1_frame_speed",frame_speed2.subs(eta,1)-s.Rational(4,21))
    audit.exact("positive_eta_endpoint_speed_limit",s.limit(frame_speed2,eta,0,dir="+")-s.Rational(1,6))
    audit.test("frame_speed_positive_entire_registered_eta_interval",
               s.simplify(frame_speed2.subs(eta,0))>0 and frame_speed2.subs(eta,1)>0,
               "4/[3(8-eta)] lies in (1/6,4/21] for 0<eta<=1; denominator positive")
    print("Coupled scalar characteristic: "+str(characteristic),flush=True)
    return dict(eta=eta,args=list(flow)+[k,eta],flow=flow,subs=subs,base=base,
        K=K,pre=pre,R=R,Mc=Mc,Vc=Vc,G=G,W=W,leading=leading,gyro=gyro,
        characteristic=characteristic,frame_speed2=frame_speed2,
        zero_algebraic=int(alg_zero),zero_geometric=int(nullity),p4=wp[4][3,3])


def generator(G,W):
    n = len(G)
    return np.block([[np.zeros((n,n)),np.eye(n)],[-W,-G]])


def complex_values(vals):
    return [[float(val.real),float(val.imag)] for val in vals]


def numerical(audit,data,parent):
    import test_01_r4c1_interacting_background as bg
    trajectory = np.load(OUTPUT_BASE/"r4c1_g3_attempt_01/trajectories.npy",allow_pickle=False)
    args = data["args"]
    functions = {key:s.lambdify(args,data[key],"numpy",cse=True)
                 for key in ("K","pre","G","W","leading","gyro")}
    flowfn = s.lambdify(args,list(data["flow"].values()),"numpy",cse=True)
    flow_error = schur_error = pencil_error = final_error = 0.
    zero_record=[]; rows=[]; positive_leading_growth=[]
    for ie,family in enumerate(parent["family"]):
        eta = family["eta"]; params=family["parameters"]
        for im,method in enumerate(parent["trajectory"]["methods"]):
            tr = trajectory[ie,im]
            for time in (0.,.5,1.,2.,3.,4.):
                it = int(round(time*200))
                if tr[0,it] != time:
                    raise RuntimeError("REGISTERED_TIME_NOT_PRESENT")
                state = tr[1:,it]
                aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi,psi_d,rm,tau = state
                values = [aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi_d,rm,
                          np.exp(params["beta"]*psi),1.,eta]
                desired_rhs = bg.rhs(time,state,params)
                desired = np.array([desired_rhs[j] for j in (0,1,2,3,4,5,6,7,9,10)]+
                                   [params["beta"]*psi_d*values[10]])
                got = np.asarray(flowfn(*values),float)
                flow_error=max(flow_error,float(np.max(abs(got-desired)/(1+abs(desired)))))
                for n in (1,2,4,8):
                    values[-2]=2*np.pi*n
                    pre=np.asarray(functions["pre"](*values),float)
                    reduced=pre[:12,:12]-pre[:12,12:]@np.linalg.solve(pre[12:,12:],pre[12:,:12])
                    kk=np.asarray(functions["K"](*values),float)
                    schur_error=max(schur_error,float(np.max(abs(reduced[:6,:6]-kk))/(1+np.max(abs(kk)))))
                values[-2]=1.
                leading=np.asarray(functions["leading"](*values),float)
                gyro=np.asarray(functions["gyro"](*values),float)
                leading_vals=np.linalg.eigvals(generator(gyro,leading))
                growth=float(max(np.real(leading_vals)))
                if growth>1e-6:
                    positive_leading_growth.append(dict(eta=eta,method=method,t=time,growth=growth))
                expected=np.sort([1.,1.,np.sqrt(1+eta*(uu*uu+vv*vv)/13),np.sqrt(4/(3*(8-eta)))])
                row=dict(eta=eta,method=method,t=time,expected_linear_speeds=expected.tolist(),
                         leading_exponents=complex_values(leading_vals),samples=[])
                for p in (20.,40.,80.,160.):
                    values[-2]=aa*p
                    G=np.asarray(functions["G"](*values),float)
                    W=np.asarray(functions["W"](*values),float)
                    eig,vec=np.linalg.eig(generator(G,W))
                    residual=0.
                    for j,val in enumerate(eig):
                        position=vec[:6,j]
                        den=(abs(val)**2+abs(val)*np.linalg.norm(G,2)+np.linalg.norm(W,2))*np.linalg.norm(position)
                        residual=max(residual,float(np.linalg.norm((val**2*np.eye(6)+val*G+W)@position)/max(den,1e-300)))
                    pencil_error=max(pencil_error,residual)
                    oscillatory=np.sort(np.imag(eig)[np.imag(eig)>1e-7])
                    fast_error=None; linear_error=None; matched=[]
                    if len(oscillatory)>=5:
                        fast_error=float(abs(oscillatory[-1]/p**2-np.sqrt(5/33))/np.sqrt(5/33))
                        candidates=oscillatory[:-1]/p
                        ii,jj=linear_sum_assignment(abs(expected[:,None]-candidates[None,:]))
                        linear_error=float(np.max(abs(expected[ii]-candidates[jj])/expected[ii]))
                        matched=candidates[jj].tolist()
                    if p==160.:
                        final_error=max(final_error,fast_error if fast_error is not None else 1e99,
                                        linear_error if linear_error is not None else 1e99)
                    row["samples"].append(dict(p=p,pencil_residual=residual,
                        fast_relative_error=fast_error,linear_relative_error=linear_error,
                        matched_linear_speeds=matched,exponents=complex_values(eig)))
                rows.append(row)
    audit.test("new_flow_matches_pure_background_RHS",flow_error<1e-12,flow_error,"normalized <1e-12")
    audit.test("new_family_numeric_Schur_agreement",schur_error<1e-8,schur_error,"normalized <1e-8")
    audit.test("full_frequency_pencil_residuals",pencil_error<1e-8,pencil_error,"<1e-8")
    return dict(records=rows,max_flow_residual=flow_error,max_Schur_residual=schur_error,
        max_frequency_pencil_residual=pencil_error,max_final_propagating_coefficient_error=final_error,
        asymptotic_reach="SUPPORTED_AT_REGISTERED_SAMPLES" if final_error<.05 else "NONASYMPTOTIC_OR_UNRESOLVED",
        formal_leading_growth_detected=bool(positive_leading_growth),growth_records=positive_leading_growth)


def evaluate():
    verify(PINS)
    parent=json.loads((OUTPUT_BASE/"r4c1_g3_attempt_01/summary.json").read_bytes())
    s1=json.loads((OUTPUT_BASE/"test_01_r4c1_scalar_constraints_summary.json").read_bytes())
    transitive={**s1["inputs"],**parent["source_sha256"],**parent["transitive_source_sha256"]}
    verify(transitive)
    audit=Audit()
    mutant={**PINS,next(iter(PINS)):"0"*64}
    try:
        verify(mutant)
        rejected=False
    except RuntimeError as exc:
        rejected="FROZEN_INPUT_HASH_MISMATCH" in str(exc)
    audit.test("source_mutation_rejected_before_outputs",rejected)
    audit.test("original_failed_receipt_retained",parent["validation"]=="FAIL_LOCAL_CHECKS" and
               parent["passed"]==112 and parent["total"]==113,
               {"validation":parent["validation"],"passed":parent["passed"],"total":parent["total"]})
    data=derive(audit)
    numerical_data=numerical(audit,data,parent)
    matrices={key:[[str(val) for val in row] for row in data[key].tolist()]
              for key in ("R","Mc","Vc","G","W","leading","gyro")}
    matrices.update(dict(characteristic=str(data["characteristic"]),
        slow_order=["x_u","x_v","x_r","x_T","x_W"],frame_speed_squared=str(data["frame_speed2"]),
        quartic_coefficient=str(data["p4"]),zero_algebraic=data["zero_algebraic"],
        zero_geometric=data["zero_geometric"],flow={str(k):str(v) for k,v in data["flow"].items()}))
    passed=sum(check["passed"] for check in audit.checks)
    summary=dict(schema="r4c1-g3s-v1",validation="PASS_LOCAL_CHECKS" if passed==len(audit.checks) else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,
        transitive_source_sha256=transitive,script_sha256=sha(Path(__file__).read_bytes()),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
        scalar_characteristic=str(data["characteristic"]),frame_speed_squared=str(data["frame_speed2"]),
        zero_root=dict(algebraic=data["zero_algebraic"],geometric=data["zero_geometric"]),
        numerical=numerical_data,status="CONDITIONAL_G3_SCALAR_SYMBOL_ZERO_BRANCH_AND_EFT_OPEN",
        physics_pass=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        healthy_continuous_GR_limit_verified=False,full_IVP_verified=False,physical_EFT_cutoff_derived=False,
        gate_effect="NONE",review_status="DEFERRED",Rule9_cleared=False,
        MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED")
    payload=(json.dumps(matrices,indent=2,allow_nan=False)+"\n").encode("utf-8")
    summary["artifacts"]={"matrices.json":sha(payload)}
    return summary,payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3s_attempt_01")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args()
    directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUTPUT_BASE.resolve()):
        raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify(PINS)
    if not args.replay and directory.exists():
        raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record,payload=evaluate()
    encoded=(json.dumps(record,indent=2,allow_nan=False)+"\n").encode("utf-8")
    identical=None
    if args.replay:
        identical=(directory/"summary.json").read_bytes()==encoded and (directory/"matrices.json").read_bytes()==payload
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(encoded))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,content in (("summary.json",encoded),("matrices.json",payload)):
            (directory/name).write_bytes(content)
            (directory/(name+".sha256")).write_text(sha(content)+"  "+name+"\n",encoding="ascii")
    print(json.dumps({key:record[key] for key in ("validation","passed","total","status","physics_pass","zero_root")}))
    for check in record["checks"]:
        if not check["passed"]:
            print(json.dumps(check))
    if args.replay and not identical:
        return 2
    return 0 if record["passed"]==record["total"] else 1


if __name__=="__main__":
    raise SystemExit(main())
