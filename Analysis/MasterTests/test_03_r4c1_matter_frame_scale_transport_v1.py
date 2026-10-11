"""Conditional local scale transport and H-tracking compatibility, not a0(z)."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import sys

import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE="Analysis/MasterTests/outputs/"
HELPER="Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT/HELPER).read_bytes()).hexdigest()!="d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen integrity helper drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT="Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_FRAME_TRANSPORT_CONTRACT_2026-10-09.md"
TRAJECTORY=BASE+"test_01_r4c1_interacting_background_trajectory.csv"
PARENTS={
    BASE+"r4c1_g3n5_background_match_attempt_01/summary.json":
        "c248ab693091c230f0c1880050488e88a0b7c2bd244e78031cad537bac554229",
    BASE+"test_01_r4c1_interacting_background_summary.json":
        "e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7",
    BASE+"test_03_r4c1_coefficient_identifiability_summary.json":
        "49b10df599d6158f02ae6e55febe054f5b6fe2e3a2b53ee70daf7196f44d2fcf",
}
PINS={
    CONTRACT:"3387bea692d703c047232f9fd242903690a3c7af978f4877a3d6567f218821ac",
    TRAJECTORY:"0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa",
    "Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md":
        "c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a",
    "Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_CONTRACT_2026-09-25.md":
        "29f54fbef62d6a2b2a5d29d772633a87694a9ed1d05f7b00244833b88075465d",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_BACKGROUND_MATCHING_REPORT_2026-10-09.md":
        "02149779c57449df86f0a32262c03daba0ebbddb408f00f2dbc4efcd4e0a0533",
    "Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_CONTRACT_2026-09-25.md":
        "3d5f164529ee2621aaa41bd08f8ba0a1ad2e4b866591f5aa4475f188fdf99a59",
    "Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md":
        "48b49fddd9066d6df783eb336e00d49374f3845ec38414ee53fe0fad812348d8",
    BASE+"r4c1_g3n5_background_match_attempt_01/independent.json":
        "f2712b50ea4586379c3baf34a59fc8df03bf72669ec3ad7270a82a7ac050eb52",
}


def exact(checks,name,expression):
    residual=s.cancel(s.expand(expression))
    checks.add(name,residual==0,"zero_exact" if residual==0 else str(residual),"zero_exact")


def symbolic(checks):
    C,A,b,K,beta,GE,P,R,M,q,z,dz,lap,pm,sigma=s.symbols(
        "C A b K_Q beta G_E P R_m M_m grad_psi_m z_m grad_z_m lap_psi_m psi_dot_m sigma",
        positive=True)
    H,p,Hd,pdd,Gd,Pd,rho,rhod,mc,ud,vd,rd,psi=s.symbols(
        "H_E psi_dot Hdot psi_ddot G_E_dot P_dot rho_E rho_E_dot M_cos2 u_dot v_dot r_dot psi_bar",
        real=True)
    S=H+beta*p
    DE=beta**3/(12*s.pi*GE*A)
    GM=C**2*GE;AM=A/C
    DM=beta**3/(12*s.pi*GM*AM)
    exact(checks,"frozen_C_cubic_action_density",
          -A*(C*q)**3/C**4+AM*q**3)
    exact(checks,"frozen_C_eliminated_regulator_density",
          -b*(C*C*lap)**2/(2*C**4)+b*lap*lap/2)
    exact(checks,"frozen_C_first_order_auxiliary_regulator_density",
          (b*(C*C*z)**2/2-b*(C**3*dz)*(C*q))/C**4-(b*z*z/2-b*dz*q))
    exact(checks,"frozen_C_temporal_kinetic_density",
          K*(C*pm)**2/(2*C**4)-(K/C**2)*pm*pm/2)
    rm=s.Symbol("rho_m",positive=True)
    exact(checks,"frozen_C_source_density",-beta*C**4*rm*psi/C**4+beta*rm*psi)
    an=s.Symbol("frame_acceleration_m",real=True)
    exact(checks,"frozen_C_auxiliary_acceleration_density",
          -b*(C*C*z)*(C*an)*(C*q)/C**4+b*z*an*q)
    F3,F4=s.symbols("div_cubic_m laplacian_squared_m",real=True)
    exact(checks,"frozen_C_nonlinear_flux_equation",
          (3*A*C**3*F3-b*C**4*F4-beta*C**4*rm)/C**4-
          (3*AM*F3-b*F4-beta*rm))
    exact(checks,"dust_mass_and_radius_Newtonian_component_map",
          GE*(C*M)/(R/C)**2/C-GM*M/R**2)
    exact(checks,"conditional_dynamic_scale_map",DM-DE/C)
    HM=S/C
    a=s.Symbol("a_E",positive=True)
    ad=a*H;Cd=beta*p*C
    exact(checks,"matter_clock_Hubble_map",(Cd*a+C*ad)/(C*a)/C-HM)
    exact(checks,"matter_dust_continuity_from_Einstein_exchange",
          (rhod-4*beta*p*rho)/C**5+3*HM*rho/C**4-
          (rhod+3*H*rho-beta*p*rho)/C**5)
    combo=DM/HM
    chi=combo/P**2
    exact(checks,"C_cancels_in_dimensionless_scale_Hubble_ratio",
          combo-beta**3/(12*s.pi*A*GE*S))
    ks=ud*ud+vd*vd+rd*rd+K*p*p
    Sdot=-(ks+rho)/(2*mc)-3*beta*H*p-beta**2*rho/K
    exact(checks,"Sdot_from_B1_background_action",
          (Hd+beta*pdd).subs({Hd:-(ks+rho)/(2*mc),pdd:-3*H*p-beta*rho/K},simultaneous=True)-Sdot)
    dchi=s.diff(chi,H)*Hd+s.diff(chi,p)*pdd+s.diff(chi,GE)*Gd+s.diff(chi,P)*Pd
    exact(checks,"general_constant_Cchi_compatibility_identity",
          dchi/chi+Gd/GE+(Hd+beta*pdd)/S+2*Pd/P)
    measure=GE*S*P**2
    dmeasure=s.diff(measure,H)*Hd+s.diff(measure,p)*pdd+s.diff(measure,GE)*Gd+s.diff(measure,P)*Pd
    exact(checks,"tracking_condition_product_form",dchi/chi+dmeasure/measure)
    exact(checks,"scale_transport_logarithmic_rate",
          (s.diff(DM,GE)*Gd+s.diff(DM,C)*Cd)/DM+Gd/GE+beta*p)
    exact(checks,"psi_chart_invariance_of_Cchi",
          chi.subs({beta:beta/sigma,A:A/sigma**3,p:sigma*p},simultaneous=True)-chi)
    exact(checks,"psi_chart_invariance_of_conformal_factor",
          s.exp((beta/sigma)*(sigma*psi))-s.exp(beta*psi))
    D=s.Symbol("spherical_gradient_amplitude",positive=True)
    RE=s.Symbol("R_E",positive=True)
    exact(checks,"spherical_regulator_subleading_ratio_unit_invariance",
          2*b/(3*AM*D*(C*RE))-2*b/(3*A*D*RE))
    wrong={
        "omit_conformal_clock_rate":s.cancel(H/C-HM),
        "omit_mass_conversion":s.cancel(GE*M/(R/C)**2/C-GM*M/R**2),
        "omit_acceleration_unit_conversion":s.cancel(DE-DM),
    }
    checks.add("wrong_frame_mutants_have_nonzero_generic_residuals",
               all(v!=0 for v in wrong.values()),{k:str(v) for k,v in wrong.items()},
               "generic beta*psi_dot != 0 and C != 1; endpoints can be nondiagnostic")
    h0=s.sqrt(s.Rational(3469,4620))
    initial={H:h0,p:s.Rational(1,5),rho:s.Rational(1,5),K:3,mc:s.Rational(11,10),
             beta:s.Rational(2,5),ud:0,vd:1,rd:s.Rational(1,4)}
    sd0=s.simplify(Sdot.subs(initial))
    expected=-s.Rational(553,880)-6*h0/25-s.Rational(4,375)
    exact(checks,"B1_initial_Sdot_exact_target_free",sd0-expected)
    checks.add("constant_GE_P_does_not_automatically_track_H_at_B1_start",
               bool(sd0<0),str(sd0),"strictly negative Sdot at frozen initial point")
    # No numerical G, projection factor or acceleration is selected.
    return {"scope":"Conditional constant-local-C map; no common physical domain or coupled G_eff derived",
        "matter_frame_maps":{"a_m":"C*a_E","dt_m":"C*dt_E","M_E":"C*M_m","rho_E":"C^4*rho_m",
            "G_m":str(GM),"A_m":str(AM),"b_m":str(b),"K_Q_m":str(K/C**2),"z_m":"z_E/C^2"},
        "a_dyn_E":str(DE),"a_dyn_m":str(DM),"H_m":str(HM),"C_dyn":str(s.cancel(combo)),
        "C_chi_conditional":str(s.cancel(chi)),"S_dot":str(Sdot),
        "constant_Cchi_condition":"d/dt_E [G_E(t)*(H_E+beta*psi_dot)*P(t)^2] = 0",
        "B1_initial_Sdot":str(sd0),"wrong_frame_residuals":{k:str(v) for k,v in wrong.items()},
        "normalized_shapes_general":{"a_dyn":"C_ref*G_E_ref/(C*G_E)",
            "C_chi":"G_E_ref*P_ref^2*S_ref/(G_E*P^2*S)"},
        "sampled_policy":"G_E and P held constant only for normalized diagnostic profiles; no values assigned",
        "nonclaims":["No physical a0(z)","No selected C_chi, A, P or microscopic K_Q",
            "No common B1/static weak-field validity domain","No adiabatic bound or coupled G_eff(k,z)",
            "No observed redshift, photon/radiation model or SI calibration"]},float(sd0)


def centered(values,dt):
    return (values[:-4]-8*values[1:-3]+8*values[3:-1]-values[4:])/(12*dt)


def normalized_error(actual,expected):
    return float(np.max(np.abs(actual-expected)/np.maximum.reduce(
        (np.ones_like(actual),np.abs(actual),np.abs(expected)))))


def profiles(checks,initial_Sdot):
    data=np.genfromtxt(ROOT/TRAJECTORY,names=True,delimiter=",")
    t=data["t"];a=data["a"];H=data["H"];psi=data["psi"];p=data["psid"];rho=data["rho_m"]
    beta=2/5;K=3.;mc=11/10
    checks.add("saved_B1_grid_unchanged",len(t)==801 and t[0]==0 and t[-1]==4 and
               np.allclose(np.diff(t),0.005,rtol=0,atol=1e-14),{"samples":len(t),"dt":float(t[1]-t[0])})
    B1=common.read_json(BASE+"test_01_r4c1_interacting_background_summary.json")
    checks.add("saved_B1_parameters_unchanged",B1["parameters"]["beta"]==beta and
               B1["parameters"]["K"]==K and B1["M_cos_squared"]==mc)
    C=np.exp(beta*psi);am=C*a;S=H+beta*p;hm=S/C;eps=rho/C**4
    ks=data["ud"]**2+data["vd"]**2+data["rd"]**2+K*p*p
    Sdot=-(ks+rho)/(2*mc)-3*beta*H*p-beta*beta*rho/K
    checks.add("initial_rate_agrees_with_exact_frozen_point",
               abs(Sdot[0]-initial_Sdot)<=1e-14,{"numeric":float(Sdot[0]),"exact_to_float":initial_Sdot},"<=1e-14")
    anorm=C[-1]/C;chinorm=S[-1]/S
    zref=am[-1]/am-1
    checks.add("sampled_transport_domain_finite_positive",
               all(np.all(np.isfinite(q)) and np.all(q>0) for q in (C,am,S,hm,eps,anorm,chinorm)),
               {"min_S":float(S.min()),"min_C":float(C.min()),"min_rho_matter":float(eps.min())})
    checks.add("sampled_formal_redshift_reference_not_calibration",
               zref[-1]==0 and np.all(np.diff(zref)<0) and np.all(zref>=0),
               {"t_ref":4,"z_ref_initial":float(zref[0])},"scale-factor coordinate only")
    checks.add("normalized_profiles_have_unit_reference",anorm[-1]==1 and chinorm[-1]==1)
    checks.add("sampled_constant_GE_P_coefficient_not_constant",
               float(np.max(np.abs(chinorm-1)))>1e-4,
               {"maximum_separation":float(np.max(np.abs(chinorm-1))),
                "end_to_start_coefficient_ratio":float(1/chinorm[0])},"separation>1e-4; not a physical exclusion")
    finite=[]
    for stride in (4,2,1):
        ids=np.arange(0,len(t),stride)
        tt=t[ids];dt=float(tt[1]-tt[0]);interior=ids[2:-2]
        witnesses={
            "dust_proper_clock":(centered(data["tau"][ids],dt),C[interior]),
            "matter_expansion":(centered(np.log(am[ids]),dt),S[interior]),
            "matter_dust_continuity":(centered(eps[ids],dt),-3*S[interior]*eps[interior]),
            "normalized_scale_log_rate":(centered(np.log(anorm[ids]),dt),-beta*p[interior]),
            "normalized_coefficient_log_rate":(centered(np.log(chinorm[ids]),dt),-Sdot[interior]/S[interior]),
        }
        errors={k:normalized_error(*q) for k,q in witnesses.items()}
        finite.append({"samples":len(ids),"dt":dt,"interior_samples":len(interior),
                       "normalized_errors":errors,"boundaries_excluded":2})
    for name in finite[-1]["normalized_errors"]:
        coarse=finite[0]["normalized_errors"][name];fine=finite[-1]["normalized_errors"][name]
        checks.add("finest_transport_"+name,fine<=1e-6,fine,"<=1e-6")
        checks.add("transport_refinement_"+name,
                   coarse>=4*fine or max(coarse,fine)<=1e-10,
                   {"coarse":coarse,"fine":fine,"improvement":coarse/fine if fine else None},
                   "coarse/fine>=4 or both<=1e-10")
    # Explicit normalized profiles, not an acceleration in physical units.
    matrix=np.column_stack((t,C,am,hm,eps,zref,anorm,chinorm,S,Sdot))
    buffer=io.StringIO()
    np.savetxt(buffer,matrix,delimiter=",",fmt="%.17g",comments="",
               header="t_E,C,a_m,H_m,rho_matter,z_ref,a_dyn_normalized_constant_GE,Cchi_normalized_constant_GE_P,S,S_dot")
    points=[]
    for i in (0,200,400,600,800):
        points.append({"t_E":float(t[i]),"C":float(C[i]),"H_m":float(hm[i]),"z_ref":float(zref[i]),
                       "a_dyn_normalized":float(anorm[i]),"Cchi_normalized":float(chinorm[i])})
    return buffer.getvalue().encode(),{"finite_difference_controls":finite,"sampled_points":points,
        "normalized_end_to_start":{"a_dyn":float(1/anorm[0]),"Cchi":float(1/chinorm[0])},
        "source_policy":"saved B1 trajectory; no reintegration, fit or physical validity inference",
        "C_chi_tracking_policy":"constant G_E and P is an explicit diagnostic assumption, not a derived physical property"}


def calculate():
    pins={};parents={}
    for name,digest in PARENTS.items():
        if common.sha((ROOT/name).read_bytes())!=digest: raise RuntimeError("Frozen parent drift: "+name)
        parents[name]=common.read_json(name)
        for path,value in parents[name]["source_sha256"].items():
            if path in pins and pins[path]!=value: raise RuntimeError("Parent source-map conflict: "+path)
            pins[path]=value
        pins[name]=digest
    for path,value in PINS.items():
        if path in pins and pins[path]!=value: raise RuntimeError("Direct source-map conflict: "+path)
        pins[path]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins)
    checks=common.Checks()
    checks.add("all_direct_transitive_pins_before",True,
               {"pins":len(pins),"available_sidecars":len(pins)-len(missing),"known_absent":missing})
    checks.add("parents_remain_local_only",all(q["physics_pass"] is False and q["gate_effect"]=="NONE"
               for q in parents.values()))
    formulas,sd0=symbolic(checks)
    csv,evidence=profiles(checks,sd0)
    inherited=common.read_json(BASE+"r4c1_g3n5_background_match_attempt_01/independent.json")
    evidence["inherited_failed_parent_checks"]=inherited["inherited_failed_parent_checks"]
    evidence["superseded_N3_attempt_01_failed_checks"]=inherited["superseded_N3_attempt_01_failed_checks"]
    checks.add("original_G3_N3_failures_retained",
               len(evidence["inherited_failed_parent_checks"])==1 and len(evidence["superseded_N3_attempt_01_failed_checks"])==2)
    checks.add("all_direct_transitive_pins_after",common.inspect_pins(pins)==missing)
    artifacts={"formulas.json":common.encode(formulas),"independent.json":common.encode(evidence),
               "normalized_profiles.csv":csv}
    passed=sum(q["passed"] for q in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-c3-matter-frame-scale-transport-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        "passed":passed,"total":len(checks.rows),"checks":checks.rows,
        "status":"CONDITIONAL_FRAME_TRANSPORT_TRACKING_CONDITION_NOT_PHYSICAL_A0_Z" if ok else "TRANSPORT_REQUIRES_DISPOSITION",
        "source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],
        "artifacts":{k:common.sha(q) for k,q in artifacts.items()},"inherited_sidecars_absent":missing,
        "physical_weak_field_response_derived":False,"physical_G_eff_derived":False,
        "quasistatic_remainder_bounded":False,"common_physical_domain_verified":False,
        "a0_z":"NOT_PREDICTED","C_chi":"NOT_DERIVED","projection_factor":"NOT_DERIVED",
        "analyst_blinded":False,"physics_pass":False,"canonical_Test3_pass":False,"gate_effect":"NONE",
        "Rule9_cleared":False,"review_status":"DEFERRED","canonical_tests_1_to_3":"HOLD_SUBSTANTIVE",
        "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED","V":"NOT_COMPUTED",
        "Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
        "review_dependencies":["R4C1-C1","B1","G3N5 background match","all inherited physics and review debt"],
        "runtime":{"python":platform.python_version(),"numpy":np.__version__,"sympy":s.__version__}}
    artifacts["summary.json"]=common.encode(summary)
    return artifacts,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_c3_frame_transport_attempt_01")
    parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir(): raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists(): raise FileExistsError("Refuse existing scientific output")
    artifacts,summary=calculate()
    if args.replay:
        for name,data in artifacts.items():
            if (dest/name).read_bytes()!=data or (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Read-only replay mismatch: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in artifacts.items():
            with (dest/name).open("xb") as f:f.write(data)
            with (dest/(name+".sha256")).open("xb") as f:f.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect")}}))
    for row in summary["checks"]:
        if not row["passed"]:print(json.dumps(row))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":
    raise SystemExit(main())
