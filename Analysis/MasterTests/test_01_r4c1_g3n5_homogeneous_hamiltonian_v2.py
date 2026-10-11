"""Independent unfixed-lapse homogeneous Hamiltonian and full momentum-block comparison."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BASE="Analysis/MasterTests/outputs/"
PARENT=BASE+"r4c1_g3n5_mean_mode_energy_attempt_02/"
PRECISE=BASE+"r4c1_g3n5_constraint_response_attempt_02/"
CONTRACT="Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_CONTRACT_2026-10-11.md"
HELPER="Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT/HELPER).read_bytes()).hexdigest()!="d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()


def exact(checks,name,value):
    vals=list(value) if isinstance(value,s.MatrixBase) else [value]
    bad=[{"index":i,"residual":str(r)} for i,v in enumerate(vals) if (r:=s.factor(s.expand(v)))!=0]
    checks.add(name,not bad,bad,"zero_exact")


def parse_matrix(record,sy):
    m=s.zeros(*record["shape"])
    for row in record["entries"]:
        text=row["value"]
        names=set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*",text))
        if "__" in text or not re.fullmatch(r"[A-Za-z_0-9+\-*/(). \t]+",text) or not names<=set(sy)|{"sqrt"}:
            raise ValueError("Unexpected frozen coefficient syntax")
        m[row["row"],row["column"]]=s.sympify(text,locals={**sy,"sqrt":s.sqrt})
    return m


def derive(checks):
    vol,MC,N,K,C,R,eps,V=s.symbols("volume MC lapse K C radius epsilon potential",positive=True)
    xd,Rd,rd,pd,td,wd=s.symbols("volume_log_dot radius_dot reservoir_dot psi_dot tau_dot theta_dot",real=True)
    velocities=s.Matrix([xd,Rd,rd,pd,td,wd])
    momenta=s.Matrix(s.symbols("p_volume p_radius p_reservoir p_psi p_tau charge",real=True))
    # Full aligned homogeneous action with lapse and density left unfixed.
    L=-MC*vol*xd**2/(3*N)+vol*(Rd**2+rd**2+K*pd**2+R**2*wd**2)/(2*N)-N*vol*V \
        +vol*eps*(C**2*td**2/N-N*C**4)/2
    dL=s.Matrix([s.diff(L,q) for q in velocities])
    inv=s.solve([dL[i]-momenta[i] for i in range(6)],list(velocities),dict=True)[0]
    exact(checks,"unfixed_lapse_all_six_momenta_inverse",dL.subs(inv)-momenta)
    H=s.factor((momenta.dot(velocities)-L).subs(inv))
    px,pR,pr,pp,pt,Q=momenta
    expected=N*(-3*px**2/(4*MC*vol)+pR**2/(2*vol)+pr**2/(2*vol)+pp**2/(2*K*vol)
                +Q**2/(2*vol*R**2)+vol*V+pt**2/(2*vol*eps*C**2)+vol*eps*C**4/2)
    exact(checks,"unfixed_lapse_direct_Legendre_Hamiltonian",H-expected)
    positive_eps=pt/(vol*C**3)
    exact(checks,"positive_dust_density_constraint",s.diff(H,eps).subs(eps,positive_eps))
    reduced=s.factor(H.subs(eps,positive_eps)/N)
    expected_reduced=expected.subs(eps,positive_eps)/N
    exact(checks,"dust_Hamiltonian_positive_branch",reduced-expected_reduced)
    exact(checks,"dust_Hamiltonian_is_C_times_conserved_momentum",s.diff(reduced,pt)-C)
    exact(checks,"lapse_primary_secondary_constraint",s.diff(H,N).subs(eps,positive_eps)-reduced)
    cb,pbg=s.symbols("C_background psi_background_dot",positive=True)
    other=reduced-C*pt
    dust=cb*other/C
    phase_momentum=s.sqrt(2*K*vol*(-other+pp**2/(2*K*vol)-C*pt))
    phase=-pbg*phase_momentum
    exact(checks,"dust_clock_solution_for_conserved_momentum",reduced.subs(pt,-other/C))
    exact(checks,"phase_clock_constraint_solution",reduced.subs(pp,phase_momentum))
    exact(checks,"normalized_trace_to_volume_inverse_hessian",
          s.diff(dust,px,2).subs(cb,C)*s.Rational(4,3)+2/(MC*vol))
    # A positive future dust momentum and nonzero charge stay separate choices.
    result=dict(L=str(L),momenta=list(map(str,dL)),Hamiltonian_unfixed_lapse=str(H),
                dust_density_solution=str(positive_eps),constraint=str(reduced),
                dust_clock_H=str(dust),phase_clock_H=str(phase),
                charge_normalization="momenta per coordinate-cell volume; integrated values multiply (2*pi)^3",
                dust_sector="original P_tau varies; comparator fixes P_tau=1/5")
    return result


def comparisons(checks,record):
    names=("a","H","u0","u_dot","v0","v_dot","r0","r_dot","psi_dot","rho_m","C")
    sy={k:s.Symbol(k,real=True) for k in names}
    sy["a"]=s.Symbol("a",positive=True)
    a,H,u,ud,v,vd,r,rd,p,rho,C=[sy[k] for k in names]
    vol=a**3
    MC=s.Rational(11,10)
    K=s.Integer(3)
    potential=(u*u+v*v)/2+(u*u+v*v)**2/24+(u*u+v*v)**3/480+r*r+r**4/28+3*(u*u+v*v)*r*r/28
    constraint=3*MC*H*H-(ud*ud+vd*vd+rd*rd+K*p*p)/2-potential-rho
    modulus=s.Poly(constraint,H)
    def shell(value):
        if value==0:return s.Integer(0)
        num,den=s.fraction(s.cancel(value))
        return s.factor(s.Poly(num,H).rem(modulus).as_expr()/den)
    def checked(name,m):
        exact(checks,name,m.applyfunc(shell))
    Mnames=["Mxx","Mxy","Mxz","Myy","Myz","Mzz"]
    # q_old=P q_volume/shear. Five shear variables use Frobenius-normalized bases.
    def metric_basis(n):
        P=s.zeros(n)
        for f in ("Mxx","Myy","Mzz"):
            P[Mnames.index(f),0]=s.Rational(2,3)
        P[Mnames.index("Mxx"),1]=1/s.sqrt(2)
        P[Mnames.index("Myy"),1]=-1/s.sqrt(2)
        P[Mnames.index("Mxx"),2]=P[Mnames.index("Myy"),2]=1/s.sqrt(6)
        P[Mnames.index("Mzz"),2]=-2/s.sqrt(6)
        for col,f in enumerate(("Mxy","Mxz","Myz"),3):
            P[Mnames.index(f),col]=1/s.sqrt(2)
        for i in range(6,n):P[i,i]=1
        return P
    kd=parse_matrix(record["dust_action"]["K"],sy)
    kp=parse_matrix(record["phase_action"]["K"],sy)
    kboth=parse_matrix(record["fixed_both_action"]["K"],sy)
    Pb=metric_basis(11)
    Pd=metric_basis(12)
    kt=s.simplify(Pd.T*kd*Pd)
    expected_dust=s.diag(-2*MC/3,*([s.Rational(1,4)]*5),*([s.Rational(1,6)]*3),1,1,3)
    checked("independent_all_twelve_dust_charge_kinetic_entries",kt-expected_dust)
    c=3/(4*MC*vol)
    B=s.diag(c,*([-2/vol]*5),*([-3/vol]*3),-1/(2*vol),-1/(2*vol))
    radial=(u*ud+v*vd)/s.sqrt(u*u+v*v)
    momenta=s.Matrix([-2*MC*vol*H]+[0]*8+[vol*radial,vol*rd])
    bvec=B*momenta
    hessian=-2*B+4*bvec*bvec.T/(K*vol*p**2)
    kk=s.simplify(Pb.T*kboth*Pb)
    checked("independent_all_121_fixed_both_momentum_Hessian_entries",vol*kk*hessian-s.eye(11))
    # Original fixed-complex-only phase chart retains the dust canonical pair.
    Pp=metric_basis(12)
    kg=s.simplify(Pp.T*kp*Pp)
    Bext=s.diag(B,0)
    gradient=s.Matrix([*list(2*bvec),-C])
    full_hessian=-2*Bext+gradient*gradient.T/(K*vol*p**2)
    checked("independent_all_144_varying_dust_momentum_Hessian_entries",vol*kg*full_hessian-s.eye(12))
    mixed=full_hessian.extract([0,11],[0,11])
    exact(checks,"original_mixed_negative_determinant",mixed.det()+2*c*C**2/(K*vol*p**2))
    # Analytic positivity at fixed P_tau: U is strictly positive on B1.
    angular=(u*vd-v*ud)**2/(2*(u*u+v*v))
    U=vol*(potential+rho+angular)
    F=K*vol*p**2/2
    checked("Lorentzian_momentum_norm_F_plus_positive_potential",
            s.Matrix([(momenta.T*B*momenta)[0]-F-U]))
    hessian_at_rest=s.diag(2*c*U/F,*([4/vol]*5),*([6/vol]*3),1/vol,1/vol)
    checks.add("fixed_dust_local_positivity_domain",True,
               {"basis_proof":"Lorentzian congruence to timelike momentum rest frame: positive diagonal since U>0,F>0,c>0",
                "rest_diagonal":list(map(str,hessian_at_rest.diagonal())),
                "U":str(U),"F":str(F),
                "nonclaim":"additional global charge restriction; not a stability theorem for original ensemble"})
    return {"volume_shear_basis_dust":str(Pd),"volume_shear_basis_fixed_both":str(Pb),
            "dust_K":str(expected_dust),"fixed_both_momentum_Hessian":str(hessian),
            "varying_dust_momentum_Hessian":str(full_hessian),
            "fixed_dust_positive_potential":str(U),"clock_radicand_F":str(F),
            "physical_propagating_ghost_identified":False}


def calculate(compare=False,parent_sha=None):
    folder=PARENT if compare else PRECISE
    expected=parent_sha if compare else "04705ea37aa944a567387073b1eda81c824d447566d061ddfd684abfbf30649d"
    parent=common.read_json(folder+"summary.json")
    if common.sha((ROOT/(folder+"summary.json")).read_bytes())!=expected:
        raise ValueError("Parent summary pin mismatch")
    pins=dict(parent["source_sha256"])
    pins[folder+"summary.json"]=expected
    for name,h in parent["artifacts"].items():pins[folder+name]=h
    pins[CONTRACT]="b82a740a0bb12946e6ae195fb0f6648d6727f8a87c7d9ae96c1fd491c6191446"
    pins["Analysis/MasterTests/test_01_r4c1_g3n5_homogeneous_hamiltonian_v1.py"]="9dc1cb370a7995b794a9240b7f789cff726590cbdd00ef4e340f9a74c3aeff18"
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins)
    checks=common.Checks()
    checks.add("all_source_pins_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(missing),"absent":missing})
    checks.add("parent_checked_on_its_declared_scope",parent["passed"]==parent["total"] and parent["physics_pass"] is False)
    print("Independent direct unfixed-lapse homogeneous Legendre transform",flush=True)
    formulas=derive(checks)
    compared=None
    if compare:
        print("Independent complete charge-sector momentum block comparisons",flush=True)
        compared=comparisons(checks,common.read_json(PARENT+"charge_sectors.json"))
    checks.add("all_source_pins_after",common.inspect_pins(pins)==missing)
    payloads={"formulas.json":common.encode(formulas)}
    if compare:payloads["comparison.json"]=common.encode(compared)
    passed=sum(q["passed"] for q in checks.rows)
    summary=dict(schema="r4c1-g3n5-homogeneous-Hamiltonian-v2",passed=passed,total=len(checks.rows),checks=checks.rows,
       validation="PASS_LOCAL_CHECKS" if passed==len(checks.rows) else "FAIL_LOCAL_CHECKS",
       scope="FULL_CANONICAL_MOMENTUM_COMPARISON" if compare else "UNFIXED_HOMOGENEOUS_LEGENDRE_ONLY",
       comparison_completed=compare and passed==len(checks.rows),
       compared_parent_summary_sha256=parent_sha if compare else None,
       source_sha256=dict(sorted(pins.items())),script_sha256=pins[SELF],inherited_sidecars_absent=missing,
       artifacts={k:common.sha(v) for k,v in payloads.items()},
       physics_pass=False,gate_effect="NONE",Rule9_cleared=False,review_status="DEFERRED",
       canonical_tests_1_to_3="HOLD_SUBSTANTIVE",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED",
       runtime=dict(python=platform.python_version(),sympy=s.__version__),
       nonclaims=["No full Test-1 closure","No physical EFT band or local propagating ghost conclusion",
                  "Fixed dust comparator is not a repair of the original charge ensemble"])
    summary.update({"MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","TOP-X4":"UNCHANGED"})
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",default=BASE+"r4c1_g3n5_homogeneous_hamiltonian_attempt_02")
    p.add_argument("--replay",metavar="EXISTING_OUTPUT")
    p.add_argument("--compare",action="store_true")
    p.add_argument("--parent-sha",metavar="FROZEN_CANONICAL_SUMMARY_SHA256")
    args=p.parse_args()
    if args.compare and (not args.parent_sha or not re.fullmatch("[0-9a-f]{64}",args.parent_sha)):
        raise ValueError("--compare requires the explicit frozen canonical summary SHA-256")
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():raise FileExistsError("Refuse existing scientific output")
    payloads,summary=calculate(args.compare,args.parent_sha)
    if args.replay:
        for name,data in payloads.items():
            if (dest/name).read_bytes()!=data or (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Exact replay mismatch: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in payloads.items():
            with (dest/name).open("xb") as f:f.write(data)
            with (dest/(name+".sha256")).open("xb") as f:f.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,"passed":summary["passed"],"total":summary["total"],"validation":summary["validation"],
                      "physics_pass":False,"gate_effect":"NONE"}))
    for row in summary["checks"]:
        if not row["passed"]:print(json.dumps(row))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
