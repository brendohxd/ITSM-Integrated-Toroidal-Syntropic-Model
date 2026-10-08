"""G3A: signed formal slow action and canonical symplectic pullback.

No physical-cutoff, conserved cosmological energy or quantum-ghost claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"Analysis/MasterTests/outputs"
PINS={
    "Theory/Gates/RES-001/RES001_R4C1_G3_SLOW_ACTION_CONTRACT_2026-09-30.md":
        "f6a35a4ade82c8d925b44d6984164eb761e50015936623b0683e071516f62a43",
    "Theory/Gates/RES-001/RES001_R4C1_G3_ZERO_EVOLUTION_REPORT_2026-09-30.md":
        "d350c85fafb752502c017b7c93bc0223b4386ed72c39080c3e01126478d60f02",
    "Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/summary.json":
        "1f13df62495f3a39198b697a7387f14086338306a8a5e24462b1e873800f1b5a",
    "Analysis/MasterTests/outputs/r4c1_g3e_attempt_01/formulas.json":
        "f634e510fd6e04f51f0c2c6cc1f43d284b0b0c9e5d9c44d4a3b4de9d8a35e87f",
    "Analysis/MasterTests/outputs/r4c1_g3e_gr_attempt_01/summary.json":
        "813353365311041ba341c96ec5949520e927df06f69bde8e5be19227930a5d28",
}


def sha(data):return hashlib.sha256(data).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:raise RuntimeError("FROZEN_INPUT_HASH_MISMATCH: "+name)


def tidy(expr):
    if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))


def derive(audit):
    import test_01_r4c1_scalar_constraints as b
    eta=s.Symbol("eta",positive=True)
    X,Xd,Xdd=s.symbols("X Xdot Xddot",real=True)
    nxt=s.Matrix(s.symbols("next_u next_v next_r next_T",real=True))
    nxtdot=s.Matrix(s.symbols("next_u_dot next_v_dot next_r_dot next_T_dot",real=True))
    symbols={str(val):val for val in vars(b).values() if isinstance(val,s.Symbol)}
    symbols.update({str(val):val for val in [eta,X,Xd,Xdd,*nxt,*nxtdot]})
    parse=lambda text:s.sympify(text,locals=symbols)
    raw=json.loads((OUT/"r4c1_g3s_attempt_01/matrices.json").read_bytes())
    previous=json.loads((OUT/"r4c1_g3e_attempt_01/formulas.json").read_bytes())
    def matrix(key):return s.Matrix([[parse(val) for val in row] for row in raw[key]])
    Mc,Vc,G,W=[matrix(key) for key in ("Mc","Vc","G","W")]
    flow={parse(key):parse(val) for key,val in raw["flow"].items()}
    def dt(expr):
        if isinstance(expr,s.MatrixBase):return expr.applyfunc(dt)
        out=s.diff(expr,X)*Xd+s.diff(expr,Xd)*Xdd
        out+=sum(s.diff(expr,z)*zd for z,zd in zip(nxt,nxtdot))
        out+=sum(s.diff(expr,z)*fz for z,fz in flow.items() if expr.has(z))
        return out
    Ms=(Mc+Mc.T)/2
    Qpot=tidy(Vc+dt(Ms))
    audit.exact("source_gyro_equals_antisymmetric_mixing",Mc-Mc.T-G)
    audit.exact("boundary_adjusted_potential_symmetric",Qpot-Qpot.T)
    audit.exact("boundary_adjusted_Euler_position",Qpot+dt(G)/2-W)
    Y=[parse(val) for val in previous["propagating_embedding"]]
    F=[parse(val) for val in previous["force_embedding"]]
    x=s.Matrix([Y[0]/b.k+nxt[0]/b.k**2,Y[1]/b.k+nxt[1]/b.k**2,
                Y[2]/b.k+nxt[2]/b.k**2,F[0]/b.k+F[1]/b.k**2+F[2]/b.k**3,
                Y[3]/b.k+nxt[3]/b.k**2,X])
    xd=tidy(dt(x))
    print("Pulling back the full signed canonical action...",flush=True)
    Lgyro=((xd.T*xd)[0]+(xd.T*G*x)[0]-(x.T*Qpot*x)[0])/2
    # v1 used .coeff(k, n) before normalizing denominators: that is not a
    # Laurent coefficient and can silently miss terms with k in a divisor.
    # Normalize the rational function and extract powers from polynomials.
    numerator,denominator=s.cancel(Lgyro).as_numer_denom()
    den_terms=s.Poly(denominator,b.k).terms()
    if len(den_terms)!=1:
        raise RuntimeError("ACTION_NOT_A_FINITE_LAURENT_POLYNOMIAL")
    (den_power,),den_coefficient=den_terms[0]
    powers={power[0]-den_power:tidy(value/den_coefficient)
            for power,value in s.Poly(numerator,b.k).terms()}
    audit.test("Laurent_coefficients_independent_of_k",all(not value.has(b.k) for value in powers.values()))
    audit.test("no_unchecked_growing_action_powers",all(power<=4 for power in powers))
    for power in range(1,5):audit.exact(f"growing_action_k{power}_cancels",powers.get(power,s.S.Zero))
    L0=powers.get(0,s.S.Zero)
    audit.test("dummy_amplitudes_absent_from_leading_action",all(not L0.has(z) for z in [*nxt,*nxtdot]))
    audit.exact("leading_acceleration_quadratic_absent",s.diff(L0,Xdd,2))
    accel=tidy(s.diff(L0,Xdd))
    D,E=tidy(s.diff(accel,X)),tidy(s.diff(accel,Xd))
    audit.exact("leading_acceleration_linear",accel-D*X-E*Xd)
    boundary1=D*X*Xd+E*Xd**2/2
    L1=tidy(L0-dt(boundary1))
    audit.exact("acceleration_removed_by_boundary",s.diff(L1,Xdd))
    cross=tidy(s.diff(L1,X,1,Xd,1))
    boundary2=cross*X**2/2
    Lred=tidy(L1-dt(boundary2))
    K=tidy(s.diff(Lred,Xd,2));U=tidy(-s.diff(Lred,X,2))
    audit.exact("leading_first_order_action",Lred-(K*Xd**2-U*X**2)/2)
    audit.exact("leading_action_boundary_identity",L0-Lred-dt(boundary1+boundary2))
    expected_K=parse(previous["kinetic_prefactor"])
    mass=parse(previous["normalized_coefficients"][0])
    audit.exact("signed_kinetic_matches_differential_prefactor",K-expected_K)
    audit.exact("slow_action_potential_matches_evolving_mass",U-K*mass)
    audit.exact("slow_action_kinetic_time_independent",dt(K))
    EL=tidy(dt(s.diff(Lred,Xd))-s.diff(Lred,X))
    audit.exact("slow_action_Euler_matches_G3E",EL-expected_K*(Xdd+mass*X))
    # The canonical symplectic form retains the original M_c, not a metric
    # on velocities. Only the on-solution phase map uses Xdd=-mass*X.
    pi=tidy((xd+Mc*x).subs(Xdd,-mass*X))
    Qx=x.jacobian([X,Xd]);Qpi=pi.jacobian([X,Xd])
    omega=tidy(Qx.T*Qpi-Qpi.T*Qx)
    omega0=omega.applyfunc(lambda val:tidy(s.limit(val,b.k,s.oo)))
    audit.exact("independent_symplectic_pullback",omega0-s.Matrix([[0,K],[-K,0]]))
    audit.exact("physical_chi_kinetic_sign",K*eta/b.k**2+(12-eta)/b.k**2)
    P=s.Symbol("P_X",real=True)
    Hamiltonian=tidy(P**2/(2*K)+U*X**2/2)
    Hvel=(K*Xd**2+U*X**2)/2
    audit.exact("Hamiltonian_is_Legendre_transform",Hamiltonian-(Xd*s.diff(Lred,Xd)-Lred).subs(Xd,P/K))
    audit.exact("time_dependent_energy_balance",dt(Hvel).subs(Xdd,-mass*X)-dt(U)*X**2/2)
    # Exact coefficient-event check of the full boundary relation. This is
    # an algebra jet, not an additional on-shell cosmological sample.
    event={b.a:s.Rational(7,5),b.H:s.Rational(3,5),b.u:s.Rational(2,3),b.ud:s.Rational(1,7),
        b.v:s.Rational(1,5),b.vd:s.Rational(2,7),b.r:s.Rational(1,4),b.rd:-s.Rational(1,9),
        b.pd:s.Rational(1,8),b.rho:s.Rational(1,10),b.C:s.Rational(6,5),eta:s.Rational(1,4)}
    q=s.Matrix([s.Rational(1,j+2) for j in range(6)])
    qd=s.Matrix([s.Rational(-1,j+3) for j in range(6)])
    raw_event=((qd.T*qd)[0]/2+(qd.T*Mc*q)[0]-(q.T*Vc*q)[0]/2).subs(event)
    gyro_event=((qd.T*qd)[0]/2+(qd.T*G*q)[0]/2-(q.T*Qpot*q)[0]/2).subs(event)
    boundary_event=((qd.T*Ms*q)[0]+(q.T*dt(Ms)*q)[0]/2).subs(event)
    audit.exact("independent_rational_full_boundary_identity",raw_event-gyro_event-boundary_event)
    audit.exact("independent_rational_symplectic_congruence",omega0.subs(event)-s.Matrix([[0,K],[-K,0]]).subs(event))
    audit.test("negative_kinetic_domain_recorded",tidy(K+(12-eta)/eta)==0,
               "K=1-12/eta <= -11 for 0<eta<=1; sign not normalized away")
    print("Signed leading action kinetic coefficient: "+str(K),flush=True)
    return dict(base=b,eta=eta,args=list(flow)+[eta],K=K,U=U,mass=mass,L0=L0,Lred=Lred,
        boundary=tidy(boundary1+boundary2),omega=omega0,Hamiltonian=Hamiltonian,energy_dot=tidy(dt(U)*X**2/2))


def sample(audit,data):
    d=data; b=d["base"]
    family=json.loads((OUT/"r4c1_g3_attempt_01/summary.json").read_bytes())
    tr=np.load(OUT/"r4c1_g3_attempt_01/trajectories.npy",allow_pickle=False)
    functions={key:s.lambdify(d["args"],d[key],"numpy",cse=True) for key in ("K","U","mass")}
    rows=[];minmass=np.inf;maxmass=-np.inf;positive_mass=0;worst=0.
    for ie,member in enumerate(family["family"]):
        eta=member["eta"]; params=member["parameters"]
        for im,method in enumerate(family["trajectory"]["methods"]):
            for t in (0.,.5,1.,2.,3.,4.):
                a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=tr[ie,im,1:,int(round(t*200))]
                args=[a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params["beta"]*psi),eta]
                K,U,mass=[float(functions[key](*args)) for key in ("K","U","mass")]
                worst=max(worst,abs(U-K*mass)/(1+abs(U)))
                minmass=min(minmass,mass);maxmass=max(maxmass,mass)
                positive_mass+=mass>0
                rows.append(dict(eta=eta,method=method,t=t,K=K,U=U,mass=mass,
                    frozen_reduced_Hessian=[1/K,U],
                    instantaneous_energy_signature="negative_definite" if mass>0 else "indefinite" if mass<0 else "degenerate",
                    interpretation="Frozen reduced-action Hessian only; not a stationary physical-pole or cutoff verdict"))
    audit.test("all_sampled_kinetic_signs_negative",all(row["K"]<0 for row in rows))
    audit.test("sampled_action_Euler_coefficient_agreement",worst<1e-12,worst,"normalized <1e-12")
    return dict(rows=rows,min_mass=minmass,max_mass=maxmass,positive_mass_cases=int(positive_mass),
                max_action_Euler_discrepancy=worst)


def evaluate():
    verify(PINS)
    previous=json.loads((OUT/"r4c1_g3e_attempt_01/summary.json").read_bytes())
    inherited={**previous["source_sha256"],**previous["transitive_source_sha256"]}
    verify(inherited)
    import test_01_r4c1_equal_newton_scalar as gs
    audit=gs.Audit();data=derive(audit);samples=sample(audit,data)
    formulas={key:str(data[key]) for key in ("K","U","mass","L0","Lred","boundary","Hamiltonian","energy_dot")}
    formulas["symplectic_form"]=[[str(val) for val in row] for row in data["omega"].tolist()]
    payload=(json.dumps(formulas,indent=2,allow_nan=False)+"\n").encode("utf-8")
    passed=sum(check["passed"] for check in audit.checks)
    record=dict(schema="r4c1-g3a-v2",validation="PASS_LOCAL_CHECKS" if passed==len(audit.checks) else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=inherited,
        script_sha256=sha(Path(__file__).read_bytes()),artifacts={"formulas.json":sha(payload)},samples=samples,
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        status="CONDITIONAL_NEGATIVE_FORMAL_SLOW_KINETIC_POSITIVE_ENERGY_CLAIM_UNSUPPORTED" if passed==len(audit.checks) else "INCOMPLETE_FAILED_ACTION_AUDIT_NOT_A_PHYSICS_RESULT",
        positive_energy_slow_branch_verified=False,stationary_physical_pole_verified=False,
        physical_EFT_cutoff_derived=False,controlled_finite_k_remainder_verified=False,
        healthy_continuous_GR_limit_verified=False,all_action_no_go=False,
        physics_pass=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        review_status="DEFERRED",Rule9_cleared=False,gate_effect="NONE",
        MAT_001="BLOCKED",UVIR_003="IN_PROGRESS",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED")
    return record,payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",default="Analysis/MasterTests/outputs/r4c1_g3a_attempt_02")
    parser.add_argument("--replay",action="store_true")
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError("OUTPUT_OUTSIDE_MASTER_TESTS")
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError("OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT")
    record,payload=evaluate();encoded=(json.dumps(record,indent=2,allow_nan=False)+"\n").encode("utf-8")
    same=None
    if args.replay:
        same=(directory/"summary.json").read_bytes()==encoded and (directory/"formulas.json").read_bytes()==payload
        print(json.dumps(dict(replay=True,byte_identical=same,summary_sha256=sha(encoded))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,content in (("summary.json",encoded),("formulas.json",payload)):
            (directory/name).write_bytes(content)
            (directory/(name+".sha256")).write_text(sha(content)+"  "+name+"\n",encoding="ascii")
    print(json.dumps({key:record[key] for key in ("validation","passed","total","status","physics_pass")}))
    for check in record["checks"]:
        if not check["passed"]:print(json.dumps(check))
    if args.replay and not same:return 2
    return 0 if record["passed"]==record["total"] else 1


if __name__=="__main__":raise SystemExit(main())
