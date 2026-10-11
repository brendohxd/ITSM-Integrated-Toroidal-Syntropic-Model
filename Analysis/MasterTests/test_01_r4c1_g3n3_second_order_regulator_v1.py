"""G3N3: second-order regulator and dust equations with induced fields retained.

Not the solved all-sector nonlinear response, reduced physical Hessian or cutoff.
New outputs refuse replacement. Replay recomputes without writing scientific files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE="Analysis/MasterTests/outputs/"
HELPER="Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT/HELPER).read_bytes()).hexdigest()!="d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PINS={
 "Theory/Gates/RES-001/RES001_R4C1_G3N3_SECOND_ORDER_REGULATOR_CONTRACT_2026-10-09.md":"525c4ac96d08574912a49c31e7e64df597a1e13e34bffbc483ad36a23c9a9530",
 "Theory/Gates/RES-001/RES001_R4C1_G3N2_TRANSVERSE_MULTIMODE_ENTRY_REPORT_2026-10-09.md":"e0f066347d13bbd00566cf8f9af5857e424e4c8ce1102f1eebd457b419c9da19",
 BASE+"r4c1_g3n2_attempt_01/summary.json":"7f0fee4b79104cb43dab3b712b851c1de253d683fe870e920bb2d80e18789252",
 BASE+"r4c1_g3n2_attempt_01/formulas.json":"f898a66f3581782386cdf5960c9ea9dfdd0522508a42d7366abeaa8f3ba939b6",
 BASE+"r4c1_g3n2_attempt_01/samples.json":"f175c5047bb90574708e6c61c3d8f27aac59cf5b13ae0becc0b77682549f98c1",
 "Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md":"0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b",
}
MODES=(0,2,4,6)


def tidy(x):return s.factor(s.cancel(x))


def exact(checks,name,x):
    values=list(x) if isinstance(x,s.MatrixBase) else [x]
    values=[tidy(v) for v in values]
    ok=all(v==0 for v in values)
    checks.add(name,ok,"zero_exact" if ok else list(map(str,values)),"zero_exact")


def derive(checks):
    ep=s.Symbol("epsilon",real=True)
    a=s.Symbol("a",positive=True);H,p,pdd=s.symbols("H psi_dot psi_ddot",real=True)
    alpha,at,az=s.symbols("alpha alpha_t alpha_z",real=True)
    W,Wt,Wz,B,Bt,Bz=s.symbols("W W_t W_z B B_t B_z",real=True)
    V=s.symbols("V_x V_y V_z",real=True)
    Vt=s.symbols("V_x_t V_y_t V_z_t",real=True)
    Vz=s.symbols("V_x_z V_y_z V_z_z",real=True)
    S=s.symbols("S_x S_y S_z",real=True)
    St=s.symbols("S_x_t S_y_t S_z_t",real=True)
    Sz=s.symbols("S_x_z S_y_z S_z_z",real=True)
    M=s.zeros(3);mt={};mz={}
    for i in range(3):
        for j in range(i,3):
            name=f"M_{i}{j}";value=s.Symbol(name,real=True)
            M[i,j]=M[j,i]=value
            mt[value]=s.Symbol(name+"_t",real=True);mz[value]=s.Symbol(name+"_z",real=True)
    tmap={alpha:at,W:Wt,B:Bt,**dict(zip(V,Vt)),**dict(zip(S,St)),**mt}
    zmap={alpha:az,W:Wz,B:Bz,**dict(zip(V,Vz)),**dict(zip(S,Sz)),**mz}
    Pi,Pit,Piz,Pitt,Pitz,Pizz=s.symbols("Pi Pi_t Pi_z Pi_tt Pi_tz Pi_zz",real=True)
    Tt,Tz=s.symbols("T_t T_z",real=True);C=s.Symbol("C",positive=True)
    beta,b=s.symbols("beta b",real=True)

    def tr(x):
        if isinstance(x,s.MatrixBase):return x.applyfunc(tr)
        poly=s.Poly(s.expand(x),ep)
        return sum(v*ep**power[0] for power,v in poly.terms() if power[0]<=2)
    def d(x,mu):
        if mu==0:return tr(a*H*s.diff(x,a)+sum(s.diff(x,k)*v for k,v in tmap.items()))
        if mu==3:return tr(sum(s.diff(x,k)*v for k,v in zmap.items()))
        return s.Integer(0)

    N=1+ep**2*alpha
    shift=s.Matrix([ep**2*S[0]/a,(ep*B+ep**2*S[1])/a,ep**2*S[2]/a])
    velocity=s.Matrix([ep**2*V[0]/a,(ep*W+ep**2*V[1])/a,ep**2*V[2]/a])
    spatial=a*a*(s.eye(3)+ep**2*M)
    g=s.zeros(4);g[0,0]=tr(-N*N+(shift.T*spatial*shift)[0])
    for i in range(3):
        g[0,i+1]=g[i+1,0]=tr((spatial*shift)[i])
        for j in range(3):g[i+1,j+1]=spatial[i,j]
    gi=s.zeros(4);gi[0,0]=-1+2*ep**2*alpha
    for i in range(3):
        gi[0,i+1]=gi[i+1,0]=shift[i]
        for j in range(3):gi[i+1,j+1]=tr((s.eye(3)-ep**2*M)[i,j]/a**2-shift[i]*shift[j])
    gamma=1+ep**2*W*W/2
    U=s.Matrix([tr(gamma*(1-ep**2*alpha))]+[tr(velocity[i]-shift[i]*gamma*(1-ep**2*alpha)) for i in range(3)])
    exact(checks,"general_second_order_ADM_inverse",tr(g*gi)-s.eye(4))
    exact(checks,"general_second_order_unit_normalization",tr((U.T*g*U)[0])+1)
    hp=tr(gi+U*U.T)
    connection=[[[tr(sum(gi[c,j]*(d(g[j,bb],aa)+d(g[j,aa],bb)-d(g[aa,bb],j)) for j in range(4))/2)
                  for bb in range(4)] for aa in range(4)] for c in range(4)]
    DU=s.Matrix(4,4,lambda mu,nu:tr(d(U[nu],mu)+sum(connection[nu][mu][j]*U[j] for j in range(4))))
    grad=s.Matrix([p+ep**2*Pit,0,0,ep**2*Piz])
    second=s.zeros(4);second[0,0]=pdd+ep**2*Pitt
    second[0,3]=second[3,0]=ep**2*Pitz;second[3,3]=ep**2*Pizz
    Hess=s.Matrix(4,4,lambda i,j:tr(second[i,j]-sum(connection[c][i][j]*grad[c] for c in range(4))))
    Delta=tr(sum(hp[i,j]*Hess[i,j] for i in range(4) for j in range(4))+s.trace(DU)*(U.T*grad)[0])
    coefficients=[tidy(s.expand(Delta).coeff(ep,i)) for i in range(3)]
    direct=p*W*Wt+(pdd+2*H*p)*W*W
    linear=Pizz/a**2+p*Vz[2]/a
    expected=linear+direct
    exact(checks,"Delta_background_zero",coefficients[0])
    exact(checks,"Delta_transverse_first_order_zero",coefficients[1])
    exact(checks,"complete_second_order_regulator_operator",coefficients[2]-expected)
    eliminated=[alpha,*M,*S,V[0],V[1],at,az,*mt.values(),*mz.values(),*St,*Sz,*Vt]
    for name in dict.fromkeys(eliminated):exact(checks,"Delta2_independent_of_"+str(name),s.diff(coefficients[2],name))
    checks.add("reject_missing_induced_psi_curvature",tidy(expected-direct-p*Vz[2]/a)==Pizz/a**2 and Pizz/a**2!=0)
    checks.add("reject_missing_longitudinal_frame_divergence",tidy(expected-direct-Pizz/a**2)==p*Vz[2]/a and p*Vz[2]/a!=0)
    exact(checks,"linear_part_matches_S1",coefficients[2].subs({W:0,Wt:0})-linear)
    exact(checks,"quadratic_direct_part_matches_G3V",coefficients[2].subs({Pizz:0,Vz[2]:0})-direct)
    exact(checks,"first_order_shift_does_not_remove_induced_operator",coefficients[2].subs(B,-s.Symbol("eta")*W/(8-s.Symbol("eta")))-expected)

    taugrad=s.Matrix([C+ep**2*Tt,0,0,ep**2*Tz])
    C2=C**2*(1+2*beta*ep**2*Pi);C4=C**4*(1+4*beta*ep**2*Pi)
    dust=tr(C2*(taugrad.T*gi*taugrad)[0]+C4)
    dust2=tidy(s.expand(dust).coeff(ep,2))
    exact(checks,"complete_second_order_dust_constraint",dust2-2*C**4*(alpha+beta*Pi-Tt/C))
    alpha_solution=Tt/C-beta*Pi
    exact(checks,"dust_lapse_solution_retains_induced_fields",dust2.subs(alpha,alpha_solution))
    checks.add("reject_tau_equals_cosmic_time_substitution",alpha_solution!=0,"alpha=T_t/C-beta*Pi","not a premature alpha=0 gauge")
    Z=s.Symbol("Z",real=True);reg=b*Z*Z/2+b*Z*coefficients[2]
    exact(checks,"regulator_Z_equation",s.diff(reg,Z)-b*(Z+expected))
    exact(checks,"full_regulator_quartic_pullback",reg.subs(Z,-expected)+b*expected**2/2)
    checks.add("reject_direct_source_as_full_Z_solution",tidy(s.diff(reg,Z).subs(Z,-direct))==b*linear and b*linear!=0)

    k=s.Symbol("k",positive=True);chi=s.Symbol("chi",real=True)
    wp=s.cos(chi)+s.cos(3*chi)/3;vt=s.cos(chi)/4-s.cos(3*chi)/8
    fourier={};mode_records=[]
    # Direct coefficients are obtained by exact trigonometric integration.
    for mode in MODES:
        weight=s.Integer(1) if mode==0 else s.Rational(1,2)
        dw=s.integrate(s.expand_trig(wp*vt*s.cos(mode*chi)),(chi,0,2*s.pi))/(2*s.pi*weight)
        ww=s.integrate(s.expand_trig(wp**2*s.cos(mode*chi)),(chi,0,2*s.pi))/(2*s.pi*weight)
        direct_mode=tidy(p*dw+(pdd+2*H*p)*ww)
        Pim,Vm=s.symbols(f"Pi_{mode} V_{mode}",real=True);mu=mode*k
        full=tidy(direct_mode-mu*mu*Pim/a**2+p*mu*Vm/a)
        regulator_action=-b*weight*full**2/2
        # These are regulator-only response derivatives, not full J2 forces.
        force_Pi=tidy(s.diff(regulator_action,Pim));force_V=tidy(s.diff(regulator_action,Vm))
        exact(checks,f"mode_{mode}_regulator_Pi_variation",force_Pi-b*weight*mu*mu*full/a**2)
        exact(checks,f"mode_{mode}_regulator_frame_variation",force_V+b*weight*p*mu*full/a)
        if mode==0:
            exact(checks,"mean_not_inverted_or_removed",full-direct_mode)
        else:
            exact(checks,f"mode_{mode}_induced_response_can_change_Z",full.subs({Pim:a*a*direct_mode/(mu*mu),Vm:0}))
        fourier[mode]=(dw,ww,direct_mode,full)
        mode_records.append({"mode":mode,"average_weight":str(weight),"direct_Delta2":str(direct_mode),"full_Delta2":str(full),"Z_solution":str(-full),
                             "regulator_only_response_Pi":str(force_Pi),"regulator_only_response_V":str(force_V)})
    reconstructed=sum(v[2]*s.cos(mode*chi) for mode,v in fourier.items())
    exact(checks,"all_direct_harmonics_exact_reconstruction",s.trigsimp(s.expand_trig(reconstructed-direct.subs({W:wp,Wt:vt}))))
    formulas={"Delta_coefficients":list(map(str,coefficients)),"linear_induced_operator":str(linear),"direct_transverse_source":str(direct),
              "dust_constraint_second_order":str(dust2),"dust_lapse_solution":str(alpha_solution),"full_Z_solution":str(-expected),
              "regulator_quartic_contribution":str(-b*expected**2/2),"mode_equations":mode_records,
              "metric_response_symbols_retained":[str(v) for v in dict.fromkeys([alpha,*M,*S,*V])],
              "dimensions":{"Delta2":2,"Z":2,"Pi":0,"V_i":0,"W":0,"psi_dot":1,"psi_ddot":2,"T":-1,"regulator_density":4},
              "scope":"Complete regulator/dust equations through order two for the inherited transverse (t,z) chart; not solved all-sector response or physical evolution."}
    return formulas,fourier


def jets_for(which):
    values={"a":"1.4","H":"0.4","p":"0.125","pdd":"-0.09090909090909090909","C":"1.3","beta":"0.2",
            "alpha":("0.17","-0.11","0.13"),"W":("0.3","-0.28571428571428571429","0.25"),
            "B":("-0.2","0.11111111111111111111","-0.16666666666666666667"),
            "Pi":("0.19","-0.07","0.23","0.11","-0.09","0.31"),"T":("0.12","-0.16","0.18")}
    values["M"]=[[mp.mpf(i+j+1)/40 for j in range(3)] for i in range(3)]
    values["Mt"]=[[mp.mpf(2*i+2*j-3)/70 for j in range(3)] for i in range(3)]
    values["Mz"]=[[mp.mpf(i+j-2)/90 for j in range(3)] for i in range(3)]
    for name in ("S","V"):
        values[name]=[[mp.mpf((i+1)*(j+1))/(31 if name=="S" else -37) for j in range(3)] for i in range(3)]
    if which:
        values["H"]="0.23";values["p"]="-0.21";values["pdd"]="0.16";values["a"]="1.8"
        values["alpha"]=("-0.15","0.21","-0.09");values["W"]=("-0.37","0.18","-0.22")
        values["Pi"]=("-0.23","0.17","-0.11","0.27","0.15","-0.41")
    for name in ("a","H","p","pdd","C","beta"):values[name]=mp.mpf(values[name])
    for name in ("alpha","W","B","Pi","T"):values[name]=tuple(map(mp.mpf,values[name]))
    return values


def direct_covariant(ep,jets):
    def lin(j,t,z):return j[0]+j[1]*t+j[2]*z
    def quad(j,t,z):return j[0]+j[1]*t+j[2]*z+j[3]*t*t/2+j[4]*t*z+j[5]*z*z/2
    def point(t,z):
        aa=jets["a"]*mp.exp(jets["H"]*t);N=1+ep*ep*lin(jets["alpha"],t,z)
        spatial=aa*aa*(mp.eye(3)+ep*ep*mp.matrix([[jets["M"][i][j]+jets["Mt"][i][j]*t+jets["Mz"][i][j]*z for j in range(3)] for i in range(3)]))
        shift=mp.matrix([ep*ep*lin(jets["S"][i],t,z)/aa+(ep*lin(jets["B"],t,z)/aa if i==1 else 0) for i in range(3)])
        velocity=mp.matrix([ep*ep*lin(jets["V"][i],t,z)/aa+(ep*lin(jets["W"],t,z)/aa if i==1 else 0) for i in range(3)])
        gamma=mp.sqrt(1+(velocity.T*spatial*velocity)[0]);U=mp.matrix([gamma/N]+[velocity[i]-shift[i]*gamma/N for i in range(3)])
        g=mp.matrix(4);g[0,0]=-N*N+(shift.T*spatial*shift)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=(spatial*shift)[i]
            for j in range(3):g[i+1,j+1]=spatial[i,j]
        grad=mp.matrix([jets["p"]+jets["pdd"]*t+ep*ep*(jets["Pi"][1]+jets["Pi"][3]*t+jets["Pi"][4]*z),0,0,
                        ep*ep*(jets["Pi"][2]+jets["Pi"][4]*t+jets["Pi"][5]*z)])
        return g,U,grad,N*mp.sqrt(mp.det(spatial))
    zero=mp.mpf(0);g,U,grad,vol=point(zero,zero);gi=g**-1
    def derivative(fun,mu):
        if mu==0:return mp.diff(lambda v:fun(v,zero),zero)
        if mu==3:return mp.diff(lambda v:fun(zero,v),zero)
        return mp.mpf(0)
    dg=[mp.matrix([[derivative(lambda t,z:point(t,z)[0][i,j],mu) for j in range(4)] for i in range(4)]) for mu in range(4)]
    Gamma=[[[sum(gi[c,j]*(dg[aa][j,bb]+dg[bb][j,aa]-dg[j][aa,bb]) for j in range(4))/2 for bb in range(4)] for aa in range(4)] for c in range(4)]
    DU=mp.matrix([[derivative(lambda t,z:point(t,z)[1][nu],mu)+sum(Gamma[nu][mu][j]*U[j] for j in range(4)) for nu in range(4)] for mu in range(4)])
    second=mp.matrix(4);second[0,0]=jets["pdd"]+ep*ep*jets["Pi"][3]
    second[0,3]=second[3,0]=ep*ep*jets["Pi"][4];second[3,3]=ep*ep*jets["Pi"][5]
    Hess=mp.matrix([[second[i,j]-sum(Gamma[c][i][j]*grad[c] for c in range(4)) for j in range(4)] for i in range(4)])
    hp=gi+U*U.T;theta=sum(DU[i,i] for i in range(4));acc=DU.T*U
    delta=sum(hp[i,j]*Hess[i,j] for i in range(4) for j in range(4))+theta*(U.T*grad)[0]
    def flux(t,z,mu):
        gp,up,gradient,vp=point(t,z);return vp*((gp**-1+up*up.T)*gradient)[mu]
    divergence=sum(derivative(lambda t,z:flux(t,z,mu),mu) for mu in range(4))/vol
    alternative=divergence-(acc.T*grad)[0]
    taugrad=mp.matrix([jets["C"]+ep*ep*jets["T"][1],0,0,ep*ep*jets["T"][2]])
    Cnow=jets["C"]*mp.exp(jets["beta"]*ep*ep*jets["Pi"][0])
    dust=Cnow*Cnow*(taugrad.T*gi*taugrad)[0]+Cnow**4
    return {"Delta":delta,"alternative":alternative,"dust":dust,"unit_error":abs((U.T*g*U)[0]+1)}


def independent(checks):
    records=[]
    for ij in range(2):
        jets=jets_for(ij);base=direct_covariant(mp.mpf(0),jets)
        expected=jets["Pi"][5]/jets["a"]**2+jets["p"]*jets["V"][2][2]/jets["a"]+jets["p"]*jets["W"][0]*jets["W"][1]+(jets["pdd"]+2*jets["H"]*jets["p"])*jets["W"][0]**2
        dust_expected=2*jets["C"]**4*(jets["alpha"][0]+jets["beta"]*jets["Pi"][0]-jets["T"][1]/jets["C"])
        errors=[];rows=[]
        for eps in ("0.001","0.0005","0.00025"):
            e=mp.mpf(eps);plus=direct_covariant(e,jets);minus=direct_covariant(-e,jets)
            D2=(plus["Delta"]+minus["Delta"]-2*base["Delta"])/(2*e*e)
            F2=(plus["dust"]+minus["dust"]-2*base["dust"])/(2*e*e)
            errD=float(abs(D2-expected)/max(mp.mpf(1),abs(expected)))
            errF=float(abs(F2-dust_expected)/max(mp.mpf(1),abs(dust_expected)))
            errors.append(max(errD,errF))
            alt=max(abs(p["Delta"]-p["alternative"]) for p in (base,plus,minus))
            unit=max(p["unit_error"] for p in (base,plus,minus))
            checks.add(f"jet_{ij}_{eps}_covariant_identity",alt<=mp.mpf("1e-30"),str(alt),"<=1e-30")
            checks.add(f"jet_{ij}_{eps}_exact_unit_frame",unit<=mp.mpf("1e-30"),str(unit),"<=1e-30")
            rows.append({"epsilon":eps,"Delta2":str(D2),"expected_Delta2":str(expected),"normalized_Delta2_error":errD,
                         "dust2":str(F2),"expected_dust2":str(dust_expected),"normalized_dust2_error":errF,"Delta_identity_error":str(alt),"unit_error":str(unit)})
        checks.add(f"jet_{ij}_second_order_convergence",errors[-1]<=1e-5 and all(errors[n+1]<errors[n] or max(errors[n+1],errors[n])<=1e-12 for n in range(2)),errors,"last<=1e-5; decrease or <=1e-12 floor")
        records.append({"jet_index":ij,"inputs":{k:str(v) for k,v in jets.items()},"rows":rows})
    return records


def calculate():
    mp.mp.dps=50
    parent=common.read_json(BASE+"r4c1_g3n2_attempt_01/summary.json")
    pins=dict(parent["source_sha256"]);pins.update(PINS);pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins);checks=common.Checks()
    checks.add("all_pins_and_available_sidecars_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(missing),"known_absent":missing})
    print("Deriving complete second-order regulator and dust constraints...",flush=True)
    formulas,fourier=derive(checks)
    print("Checking unexpanded general metric/frame response jets...",flush=True)
    controls=independent(checks)
    parent_rows=common.read_json(BASE+"r4c1_g3v_attempt_01/samples.json")["rows"]
    n2rows=common.read_json(BASE+"r4c1_g3n2_attempt_01/samples.json")["transverse_chart_events"]
    checks.add("all_216_inherited_chart_and_source_pairs",len(parent_rows)==len(n2rows)==216)
    p,pdd,H=s.symbols("psi_dot psi_ddot H",real=True)
    events=[]
    for i,(row,n2row) in enumerate(zip(parent_rows,n2rows)):
        checks.add(f"chart_{i}_coordinate_pair",all(row[k]==n2row[k] for k in ("eta","t","k","method")))
        values={p:row["psi_dot"],pdd:row["psi_ddot"],H:row["H"]}
        ds={str(mode):float(fourier[mode][2].subs(values)) for mode in MODES}
        err=max(common.discrepancy(ds[str(mode)],n2row["direct_Delta2_cosine_coefficients"][str(mode)]) for mode in MODES)
        checks.small(f"chart_{i}_all_direct_harmonics_match_parent",err)
        events.append({"eta":row["eta"],"t":row["t"],"method":row["method"],"k":row["k"],"direct_Delta2":ds,
                       "mean_Z2":-ds["0"],"induced_Pi_V_amplitudes":"UNSOLVED", "source_error":err})
    inherited=common.read_json(BASE+"r4c1_g3n2_attempt_01/samples.json")["inherited_failed_parent_checks"]
    checks.add("inherited_G3_failure_retained",len(inherited)==1 and inherited[0]["passed"] is False,inherited)
    checks.add("all_pins_and_sidecars_after",common.inspect_pins(pins)==missing)
    payloads={"formulas.json":common.encode(formulas),"response.json":common.encode({"charts":events,"inherited_failed_parent_checks":inherited}),"independent.json":common.encode({"mp_digits":50,"control_jets":controls})}
    passed=sum(r["passed"] for r in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3n3-second-order-regulator-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS","passed":passed,"total":len(checks.rows),"checks":checks.rows,
             "status":"COUPLED_SECOND_ORDER_REGULATOR_AND_DUST_EQUATIONS_DERIVED_REMAINING_RESPONSE_OPEN" if ok else "SECOND_ORDER_RESPONSE_REQUIRES_DISPOSITION",
             "source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],"artifacts":{k:common.sha(v) for k,v in payloads.items()},"inherited_sidecars_absent":missing,
             "full_second_order_regulator_equation_verified":ok,"second_order_dust_constraint_verified":ok,
             "full_second_order_all_sector_response_solved":False,"full_coupled_classical_uniqueness_verified":False,"physical_reduced_Hessian_verified":False,"physical_EFT_cutoff_derived":False,
             "all_actions_no_go":False,"physical_ghost_proven":False,"canonical_tests_1_to_3":"HOLD_SUBSTANTIVE","physics_pass":False,"Rule9_cleared":False,"gate_effect":"NONE",
             "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
             "review_status":"DEFERRED","review_dependencies":["R9-MT1-G3N2","R9-MT1-S1","all inherited scientific and review debt"],
             "max_source_coefficient_error":max(r["source_error"] for r in events),
             "independent_final_max_error":max(max(r["normalized_Delta2_error"],r["normalized_dust2_error"]) for j in controls for r in j["rows"][-1:]),
             "runtime":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__,"mp_decimal_digits":mp.mp.dps}}
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",default=BASE+"r4c1_g3n3_attempt_01");parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError("Replay destination absent")
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
            with (dest/name).open("xb") as f:f.write(data)
            with (dest/(name+".sha256")).open("xb") as f:f.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect","Rule9_cleared")}}))
    for check in summary["checks"]:
        if not check["passed"]:print(json.dumps(check))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
