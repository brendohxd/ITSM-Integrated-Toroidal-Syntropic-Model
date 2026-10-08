"""G3E: formal evolving low-frequency branch, not a full PDE/EFT proof."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import scipy
import sympy as s
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"Analysis/MasterTests/outputs"
PINS={
    "Theory/Gates/RES-001/RES001_R4C1_G3_ZERO_EVOLUTION_CONTRACT_2026-09-30.md":
        "d1d64c216465956424589f95c940116bc198f5670552297b7e611894bcd385fa",
    "Theory/Gates/RES-001/RES001_R4C1_G3_ZERO_INNER_REPORT_2026-09-30.md":
        "fe8d380be77af9e5ccecb02c62b8264d5ecbb6bf5d42153755c2914cd355cdbd",
    "Analysis/MasterTests/outputs/r4c1_g3z_attempt_01/summary.json":
        "60d9de53f95592512e094ffc60c81a781ab8f9b33a8afa93dbf53943efbb34bf",
    "Analysis/MasterTests/outputs/r4c1_g3z_attempt_01/pencil.json":
        "abb6a23cba1f80b0a02bf76d1bb47153bd745be55e83c44e9bd8183f9a9d5bb4",
}


def sha(data):return hashlib.sha256(data).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:
            raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: "+name)


def tidy(expr):
    if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))


def derive(audit):
    import test_01_r4c1_scalar_constraints as b
    raw=json.loads((OUT/"r4c1_g3s_attempt_01/matrices.json").read_bytes())
    eta=s.Symbol("eta",positive=True)
    symbols={str(x):x for x in vars(b).values() if isinstance(x,s.Symbol)}
    symbols["eta"]=eta
    def parse(text):return s.sympify(text,locals=symbols)
    def mat(key):return s.Matrix([[parse(val) for val in row] for row in raw[key]])
    flow={parse(key):parse(val) for key,val in raw["flow"].items()}
    G,W,R=mat("G"),mat("W"),mat("R")
    X,Xd,Xdd=s.symbols("X Xdot Xddot",real=True)
    def dt(expr,frozen=False):
        if isinstance(expr,s.MatrixBase):return expr.applyfunc(lambda val:dt(val,frozen))
        result=s.diff(expr,X)*Xd+s.diff(expr,Xd)*Xdd
        if not frozen:result+=sum(s.diff(expr,z)*fz for z,fz in flow.items() if expr.has(z))
        return result
    def coeff(matrix):
        polys=[s.Poly(s.cancel(val),b.k) for val in matrix]
        return [s.Matrix(6,6,[poly.nth(j) for poly in polys]) for j in range(5)]
    gc,wc=coeff(G),coeff(W)
    audit.exact("no_higher_gyro_powers",sum(gc[2:],s.zeros(6)))
    audit.exact("only_force_quartic_block",wc[4]-s.diag(0,0,0,5/(33*b.a**4),0,0))
    fast=3; prop=[0,1,2,4]
    Y=s.Matrix(s.symbols("Y_u Y_v Y_r Y_T",real=True))
    Z=s.Matrix(s.symbols("next_u next_v next_r next_T",real=True))
    F1,F2,F3=s.symbols("F1 F2 F3",real=True)
    v0=s.Matrix([0,0,0,0,0,X]);vd0=s.Matrix([0,0,0,0,0,Xd])
    v1=s.Matrix([Y[0],Y[1],Y[2],F1,Y[3],0])
    v2=s.Matrix([Z[0],Z[1],Z[2],F2,Z[3],0])
    v3=s.Matrix([0,0,0,F3,0,0])
    e3=wc[3]*v0+wc[4]*v1
    f1=tidy(s.solve(e3[fast],F1)[0])
    e2=wc[2]*v0+wc[3]*v1+wc[4]*v2
    f2=tidy(s.solve(e2[fast].subs(F1,f1),F2)[0])
    e1=wc[1]*v0+wc[2]*v1+wc[3]*v2+wc[4]*v3+gc[1]*vd0
    f3=tidy(s.solve(e1[fast].subs({F1:f1,F2:f2},simultaneous=True),F3)[0])
    fs={F1:f1,F2:f2,F3:f3}
    audit.exact("force_k3_constraint",e3[fast].subs(fs,simultaneous=True))
    audit.exact("force_k2_constraint",e2[fast].subs(fs,simultaneous=True))
    audit.exact("force_k1_constraint",e1[fast].subs(fs,simultaneous=True))
    for power,eq in ((3,e3),(2,e2)):
        audit.exact(f"propagating_k{power}_cancellation",eq.extract(prop,[0]).subs(fs,simultaneous=True))
    leading=tidy(e1.extract(prop,[0]).subs(fs,simultaneous=True))
    A=tidy(leading.jacobian(Y))
    rem=leading.subs(dict.fromkeys(Y,0))
    y=tidy(-A.inv()*rem)
    ysubs=dict(zip(Y,y))
    audit.exact("propagating_k1_constraint",leading.subs(ysubs,simultaneous=True))
    audit.exact("W_k3_cancellation",e3[5].subs(fs,simultaneous=True))
    audit.exact("W_k2_cancellation",e2[5].subs(fs,simultaneous=True))
    audit.exact("W_k1_cancellation",e1[5].subs(fs,simultaneous=True))
    lead1=tidy(v1.subs({F1:f1},simultaneous=True).subs(ysubs,simultaneous=True))
    lead2=tidy(v2.subs({F2:f2},simultaneous=True).subs(ysubs,simultaneous=True))
    lead3=tidy(v3.subs({F3:f3},simultaneous=True).subs(ysubs,simultaneous=True))
    def equation(frozen=False):
        eq=(s.Matrix([0,0,0,0,0,Xdd])+gc[0]*vd0+gc[1]*dt(lead1,frozen)
             +wc[0]*v0+wc[1]*lead1+wc[2]*lead2+wc[3]*lead3)[5]
        return tidy(eq)
    eq=equation()
    audit.test("next_order_propagating_amplitudes_cancel",all(not eq.has(z) for z in Z))
    co=[tidy(s.diff(eq,z)) for z in (X,Xd,Xdd)]
    audit.exact("linear_second_order_closure",eq-sum(c*z for c,z in zip(co,(X,Xd,Xdd))))
    audit.exact("evolving_kinetic_prefactor",co[2]+(12-eta)/eta)
    normalized=[tidy(c/co[2]) for c in co]
    frozen=equation(True)
    frozen_co=[tidy(s.diff(frozen,z)/co[2]) for z in (X,Xd,Xdd)]
    previous=json.loads((OUT/"r4c1_g3z_attempt_01/pencil.json").read_bytes())
    expected=s.Matrix([parse(text) for text in previous["normalized_coefficients"]])
    audit.exact("frozen_control_recovers_inner_pencil",s.Matrix(frozen_co)-expected)
    audit.test("reject_omitted_coefficient_derivatives",any(tidy(a-c)!=0 for a,c in zip(normalized,frozen_co)))
    audit.test("reduced_equation_comoving_k_independent",all(not val.has(b.k) for val in normalized))
    print("Evolving zero equation derived; reconstructing matter/frame response...",flush=True)
    q=tidy(R*(v0+lead1/b.k))
    qd=tidy(dt(q).subs(Xdd,-normalized[1]*Xd-normalized[0]*X))
    subs={b.MP:1,b.MU:2*eta/3,b.c1:s.Rational(1,5),b.c2:-s.Rational(7,48),
        b.c3:-s.Rational(1,80),b.c4:s.Rational(1,20),b.KQ:3*eta,b.b:5*eta/11,
        b.zeta:eta/13,b.beta:2*eta**2/5,b.m2:1,b.l4:s.Rational(1,3),b.l6:s.Rational(1,5),
        b.Lambda:2,b.mr2:2,b.lr:s.Rational(1,7),b.gr:3*eta/7}
    upstream=json.loads((OUT/"test_01_r4c1_scalar_constraints_matrices.json").read_bytes())
    aux=s.Matrix([parse(text) for text in upstream["auxiliary_solutions"]]).subs(subs)
    fields=dict(zip(list(b.qd)+list(b.q),list(qd)+list(q)))
    reconstructed=tidy(aux.subs(fields,simultaneous=True))
    lapse,shift,de,z=list(reconstructed)
    beta=2*eta**2/5
    audit.exact("reconstructed_dust_normalization",qd[4]-b.C*lapse-beta*b.C*q[3])
    delta=tidy(-b.k**2*q[3]/b.a**2+b.pd*b.k*q[5]/b.a)
    audit.exact("reconstructed_regulator_constraint",z+delta)
    density=tidy(b.C**4*de+4*beta*b.rho*q[3])
    tilt=tidy(b.k*q[4]/(b.a*b.C))
    quantities={"density_contrast":density/b.rho,"comoving_dust_divergence":b.k*tilt,
                "comoving_frame_divergence":b.k*q[5],"lapse":lapse,"regulator":z}
    maps={}
    for name,quantity in quantities.items():
        physical=tidy(quantity.subs({X:X/b.k,Xd:Xd/b.k},simultaneous=True))
        limit=tidy(s.limit(physical,b.k,s.oo))
        audit.test("finite_leading_map_"+name,not limit.has(s.oo,s.zoo,s.nan))
        maps[name]=[tidy(s.diff(limit,v)) for v in (X,Xd)]
        audit.exact("linear_leading_map_"+name,limit-sum(c*v for c,v in zip(maps[name],(X,Xd))))
    density_velocity=s.Matrix([maps["density_contrast"],maps["comoving_dust_divergence"]])
    determinant=tidy(density_velocity.det())
    print("Normalized evolving coefficients: "+str(normalized),flush=True)
    return dict(base=b,eta=eta,flow=flow,normalized=normalized,frozen=frozen_co,
        prefactor=co[2],force=[f1,f2.subs(ysubs,simultaneous=True),f3.subs(ysubs,simultaneous=True)],
        propagating=y,maps=maps,density_velocity=density_velocity,map_determinant=determinant,
        q=q,qd=qd,aux=reconstructed)


def numerical(audit,data):
    import test_01_r4c1_interacting_background as bg
    b=data["base"]
    args=[getattr(b,key) for key in ("a","H","u","ud","v","vd","r","rd","pd","rho","C")]+[data["eta"]]
    coefficients=s.lambdify(args,data["normalized"],"numpy",cse=True)
    family=json.loads((OUT/"r4c1_g3_attempt_01/summary.json").read_bytes())
    trajectory=np.load(OUT/"r4c1_g3_attempt_01/trajectories.npy",allow_pickle=False)
    rows=[];samples=[];grid=np.linspace(0.,4.,101)
    worst_background=worst_transfer=worst_liouville=0.
    for ie,member in enumerate(family["family"]):
        eta=member["eta"];params=member["parameters"];runs=[]
        initial=trajectory[ie,0,1:,0]
        for im,method in enumerate(family["trajectory"]["methods"]):
            def rhs(t,y):
                state=y[:12]
                a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=state
                c0,c1,c2=coefficients(a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params["beta"]*psi),eta)
                generator=np.array([[0.,1.],[-c0,-c1]])
                return np.r_[bg.rhs(t,state,params),(generator@y[12:16].reshape(2,2)).ravel(),c1]
            sol=solve_ivp(rhs,(0.,4.),np.r_[initial,np.eye(2).ravel(),0.],
                          method=method,rtol=1e-11,atol=1e-13,dense_output=True)
            audit.test(f"eta_{eta}_{method}_integration",sol.success and sol.t[-1]==4.,sol.message)
            vals=sol.sol(grid)
            reference=trajectory[ie,im,1:,::8]
            difference=float(np.max(abs(vals[:12]-reference)/(1+abs(reference))))
            F=vals[12:16].T.reshape(-1,2,2)
            expected=np.exp(-vals[16]);got=np.linalg.det(F)
            liouville=float(np.max(abs(got-expected)/(1+abs(expected))))
            amplification=float(max(np.linalg.norm(mat,2) for mat in F))
            audit.test(f"eta_{eta}_{method}_background_agreement",difference<1e-8,difference,"normalized <1e-8")
            audit.test(f"eta_{eta}_{method}_Liouville_identity",liouville<1e-7,liouville,"normalized <1e-7")
            audit.test(f"eta_{eta}_{method}_finite_transfer",bool(np.all(np.isfinite(F))))
            worst_background=max(worst_background,difference);worst_liouville=max(worst_liouville,liouville)
            runs.append(F)
            rows.append(dict(eta=eta,method=method,background_difference=difference,
                             Liouville_residual=liouville,max_chart_amplification=amplification,final_transfer=F[-1].tolist()))
            samples.append(dict(eta=eta,method=method,t=grid.tolist(),transfer=F.tolist()))
        difference=float(np.max(abs(runs[0]-runs[1])/(1+abs(runs[0]))))
        audit.test(f"eta_{eta}_two_method_transfer_agreement",difference<1e-7,difference,"normalized <1e-7")
        worst_transfer=max(worst_transfer,difference)
    return dict(rows=rows,worst_background_difference=worst_background,worst_transfer_difference=worst_transfer,
                worst_Liouville_residual=worst_liouville),samples


def evaluate():
    verify(PINS)
    previous=json.loads((OUT/"r4c1_g3z_attempt_01/summary.json").read_bytes())
    transitive={**previous["source_sha256"],**previous["transitive_source_sha256"]}
    verify(transitive)
    import test_01_r4c1_equal_newton_scalar as gs
    audit=gs.Audit()
    data=derive(audit)
    numerical_data,samples=numerical(audit,data)
    formulas=dict(normalized_coefficient_order=["X","Xdot","Xddot"],
        normalized_coefficients=list(map(str,data["normalized"])),frozen_coefficients=list(map(str,data["frozen"])),
        kinetic_prefactor=str(data["prefactor"]),force_embedding=list(map(str,data["force"])),
        propagating_embedding=list(map(str,data["propagating"])),
        physical_leading_maps={name:list(map(str,row)) for name,row in data["maps"].items()},
        density_velocity_map_determinant=str(data["map_determinant"]),
        scope="Formal large-comoving-k low-frequency branch with well-prepared initial data; not full PDE/EFT theorem")
    payloads={"formulas.json":(json.dumps(formulas,indent=2,allow_nan=False)+"\n").encode("utf-8"),
              "transfer.json":(json.dumps(samples,indent=2,allow_nan=False)+"\n").encode("utf-8")}
    passed=sum(check["passed"] for check in audit.checks)
    result=dict(schema="r4c1-g3e-v1",validation="PASS_LOCAL_CHECKS" if passed==len(audit.checks) else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=transitive,
        script_sha256=sha(Path(__file__).read_bytes()),artifacts={name:sha(content) for name,content in payloads.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__),
        numerical=numerical_data,status="CONDITIONAL_EVOLVING_LOW_FREQUENCY_BRANCH_FULL_IVP_AND_EFT_OPEN",
        physics_pass=False,gate_effect="NONE",review_status="DEFERRED",Rule9_cleared=False,
        canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        full_IVP_verified=False,healthy_continuous_GR_limit_verified=False,physical_EFT_cutoff_derived=False,
        MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED")
    return result,payloads


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3e_attempt_01")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record,payloads=evaluate()
    payloads["summary.json"]=(json.dumps(record,indent=2,allow_nan=False)+"\n").encode("utf-8")
    identical=None
    if args.replay:
        identical=all((directory/name).read_bytes()==content for name,content in payloads.items())
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(payloads["summary.json"]))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,content in payloads.items():
            (directory/name).write_bytes(content)
            (directory/(name+".sha256")).write_text(sha(content)+"  "+name+"\n",encoding="ascii")
    print(json.dumps({key:record[key] for key in ("validation","passed","total","status","physics_pass")}))
    for check in record["checks"]:
        if not check["passed"]:print(json.dumps(check))
    if args.replay and not identical:return 2
    return 0 if record["passed"]==record["total"] else 1


if __name__=="__main__":raise SystemExit(main())
