"""G3N2 v1: constrained transverse foliation and raw multimode regulator rank.

No full nonlinear solution, physical ghost, all-action or all-classical no-go.
Original scientific files are immutable inputs. Replay is read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE="Analysis/MasterTests/outputs/"
HELPER="Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
if hashlib.sha256((ROOT/HELPER).read_bytes()).hexdigest()!="d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":
    raise RuntimeError("Frozen helper drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
FROZEN={
 "Theory/Gates/RES-001/RES001_R4C1_G3N2_TRANSVERSE_MULTIMODE_ENTRY_CONTRACT_2026-10-09.md":"43878a67d4002e32e3dc70e318659cd65e11699433eee7d7e2b3e5f7a29504db",
 "Theory/Gates/RES-001/RES001_R4C1_G3N1_CLASSICAL_CUSP_AMPLITUDE_REPORT_2026-10-08.md":"c72e32b6f81f35f51d336de945debb8936b94623fdba44e15fc64e0e622202b4",
 "Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md":"952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27",
 "Theory/Gates/RES-001/RES001_R4C1_G3K_C2_PRINCIPAL_TIME_DOMAIN_REPORT_2026-10-09.md":"5145e5e0cb67871ca918d9919b6433233f65e22c9126eb048ece7e0ad5a9e82d",
 BASE+"r4c1_g3n1_attempt_01/summary.json":"1c355b1f40afdc3a770d27adaaa1cd0c2b6b0fefb1d5b00d2cadc08778754167",
 BASE+"r4c1_g3k_c2_attempt_01/summary.json":"31f28b8d0bb12b2ff297f3a2f76d4de0f9ddef49ae5c2d06fce65fbf9d59e39d",
 BASE+"r4c1_g3v_attempt_01/summary.json":"07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae",
 BASE+"r4c1_g3v_attempt_01/formulas.json":"1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358",
 BASE+"r4c1_g3v_attempt_01/samples.json":"93288f37a919d22f59a397ab8ffb732f8386d23ee561469be2bebea489af3d03",
}
MODES=(0,2,4,6)
RHOS=(s.Rational(0),-s.Rational(1,3),s.Rational(1,3),s.Rational(1))
EPSILONS=(0.01,0.001,0.0001)


def tidy(value):return s.factor(s.cancel(value))


def exact(checks,name,expr):
    vals=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    vals=[tidy(v) for v in vals]
    checks.add(name,all(v==0 for v in vals),"zero_exact" if all(v==0 for v in vals) else list(map(str,vals)),"zero_exact")


def convolution(a,b):
    out={}
    for ka,va in a.items():
        for kb,vb in b.items():out[ka+kb]=out.get(ka+kb,0)+va*vb
    return {k:s.simplify(v) for k,v in out.items()}


def basis_fourier(mode):return {0:s.Integer(1)} if mode==0 else {mode:1/s.sqrt(2),-mode:1/s.sqrt(2)}


def gram_exact(rho):
    f={1:s.Rational(1,2),-1:s.Rational(1,2),3:rho/2,-3:rho/2}
    ff=convolution(f,f)
    return s.Matrix(4,4,lambda i,j:s.simplify(convolution(convolution(ff,basis_fourier(MODES[i])),basis_fourier(MODES[j])).get(0,0)))


def mpmatrix(matrix):return mp.matrix([[mp.mpf(str(s.N(v,60))) for v in matrix.row(i)] for i in range(matrix.rows)])


def fnorm(matrix):return mp.sqrt(sum(abs(v)**2 for v in matrix))


def mperror(a,b):return float(fnorm(a-b)/max(mp.mpf(1),fnorm(a),fnorm(b)))


def mpscalar(a,b):return float(abs(a-b)/max(mp.mpf(1),abs(a),abs(b)))


def numeric_basis(i,x):return 1.0 if i==0 else math.sqrt(2)*math.cos(MODES[i]*x)


def mpbasis(i,x):return mp.mpf(1) if i==0 else mp.sqrt(2)*mp.cos(MODES[i]*x)


def intervals(rho):
    if rho==1:return [mp.mpf(0),mp.pi/4,mp.pi/2,3*mp.pi/4,5*mp.pi/4,3*mp.pi/2,7*mp.pi/4,2*mp.pi]
    return [mp.mpf(0),mp.pi/2,3*mp.pi/2,2*mp.pi]


def profile_integrals(checks):
    profiles=[]
    for i,rho in enumerate(RHOS):
        G=gram_exact(rho);gm=mpmatrix(G);rr=mp.mpf(str(s.N(rho,60)))
        minors=[tidy(G[:n,:n].det()) for n in range(1,5)]
        checks.add(f"profile_{i}_positive_Gram_minors",all(v>0 for v in minors),list(map(str,minors)),"exact leading principal minors>0")
        js=mp.matrix(4);worst=0.0
        boundaries=intervals(rho);points=[float(v) for v in boundaries[1:-1]]
        for m in range(4):
            for n in range(m,4):
                native=quad(lambda x:(math.cos(x)+float(rho)*math.cos(3*x))**2*numeric_basis(m,x)*numeric_basis(n,x),0,2*math.pi,points=points,epsabs=1e-12,epsrel=1e-12)[0]/(2*math.pi)
                high=mp.quad(lambda x:(mp.cos(x)+rr*mp.cos(3*x))**2*mpbasis(m,x)*mpbasis(n,x),boundaries)/(2*mp.pi)
                err=max(mpscalar(mp.mpf(str(native)),gm[m,n]),mpscalar(high,gm[m,n]));worst=max(worst,err)
                checks.small(f"profile_{i}_Gram_integral_{m}_{n}",err)
                cubic=mp.quad(lambda x:abs(mp.cos(x)+rr*mp.cos(3*x))**3*mpbasis(m,x)*mpbasis(n,x),boundaries)/(2*mp.pi)
                native_cubic=quad(lambda x:abs(math.cos(x)+float(rho)*math.cos(3*x))**3*numeric_basis(m,x)*numeric_basis(n,x),0,2*math.pi,points=points,epsabs=1e-12,epsrel=1e-12)[0]/(2*math.pi)
                checks.small(f"profile_{i}_absolute_cubic_integral_{m}_{n}",mpscalar(cubic,mp.mpf(str(native_cubic))))
                js[m,n]=js[n,m]=cubic
        profiles.append({"rho":rho,"G":G,"gm":gm,"jm":js,"minors":minors,"quadrature_error":worst})
    return profiles


def symbolic(checks):
    t,x,y,z=s.symbols("t x y z",real=True)
    a,N=s.Function("a")(t),s.Function("N")(t)
    w,B=s.Function("w")(t,z),s.Function("B")(t,z)
    gamma=s.sqrt(1+w*w)
    g=s.diag(-N*N+B*B,a*a,a*a,a*a);g[0,2]=g[2,0]=a*B
    U=s.Matrix([gamma/N,0,(w-B*gamma/N)/a,0]);theta=(g*U).applyfunc(tidy)
    exact(checks,"covariant_transverse_unit_norm",(U.T*g*U)[0]+1)
    hp=g.inv()+U*U.T
    exact(checks,"exact_transverse_projector_tt",hp[0,0]-w*w/N**2)
    coefficient=tidy(theta[2]*s.diff(theta[0],z)-theta[0]*s.diff(theta[2],z))
    expected=a*(N*s.diff(w,z)/gamma+w*w*s.diff(B,z))
    exact(checks,"exact_transverse_Frobenius_three_form",coefficient-expected)
    ep,eta=s.symbols("epsilon eta",positive=True)
    W=s.Function("W")(t,z);sigma=-eta/(8-eta)
    constrained=expected.subs({w:ep*W,B:ep*sigma*W}).doit()
    exact(checks,"constraint_retained_leading_Frobenius",s.diff(constrained,ep).subs(ep,0)-a*N*s.diff(W,z))
    p0,pt,wf,zt,pv,bv,av,Nv=s.symbols("psi_dot psi_ddot w_field z_dot psi_velocity b a_ref N_ref",real=True)
    raw_time=-bv*av**3*wf**2*zt*pv/Nv
    exact(checks,"raw_regulator_psi_z_velocity_mix",s.diff(raw_time,zt,pv)+bv*av**3*wf**2/Nv)
    exact(checks,"raw_regulator_z_velocity_diagonal",s.diff(raw_time,zt,zt))
    # Generic block identity: no particular Apsi can make invertible C algebraic.
    G=gram_exact(s.Rational(1,3));A=s.Matrix(4,4,lambda i,j:s.Symbol(f"A_{min(i,j)}_{max(i,j)}",real=True))
    scale=s.Symbol("regulator_scale",positive=True);C=-scale*ep**2*G
    H=A.row_join(C).col_join(C.T.row_join(s.zeros(4)))
    ci=C.inv();hi=s.zeros(4).row_join(ci.T).col_join(ci.row_join(-ci*A*ci.T))
    exact(checks,"exact_raw_block_inverse_identity",H*hi-s.eye(8))
    tri=s.eye(4).row_join(s.zeros(4)).col_join((-ci*A/2).row_join(s.eye(4)))
    exact(checks,"exact_raw_block_congruence",tri.T*H*tri-s.zeros(4).row_join(C).col_join(C.T.row_join(s.zeros(4))))
    k0=s.Symbol("K_positive",positive=True)
    aligned=(k0*s.eye(4)).row_join(s.zeros(4)).col_join(s.zeros(4).row_join(s.zeros(4)))
    checks.add("aligned_raw_velocity_rank_separate",aligned.rank()==4,aligned.rank(),"rank4; no inverse at epsilon=0")
    return {"theta":[str(v) for v in theta],"Frobenius_dt_dy_dz_coefficient":str(coefficient),
            "shift_sigma_G3":str(sigma),"constraint_retained_Frobenius":str(constrained),
            "leading_Frobenius":"a*N*epsilon*partial_z(W); later O(epsilon^2) response cannot cancel it",
            "local_clock_obstruction":"theta=-mu*dT implies theta wedge dtheta=0; a nonzero computed three-form excludes that local U-orthogonal clock, not other time choices.",
            "raw_regulator_time_term":str(raw_time),"psi_z_basis_modes":list(MODES),
            "Gram_definition":"<W^2 e_m e_n>; average over chi in [0,2pi]",
            "Gram_positivity_argument":"For any nonzero finite basis polynomial q, <W^2*q^2>>0: W is a nonzero finite Fourier polynomial, nonzero on an open interval; q cannot vanish on that entire interval unless all coefficients vanish.",
            "raw_block_inverse":"H^-1=[0,(C^T)^-1;C^-1,-C^-1*Apsi*(C^T)^-1]",
            "raw_block_determinant":"det H=det(C)^2=(b*a^3/N)^8*epsilon^16*det(G)^2, for four psi and four z modes",
            "inverse_leading_limit":"epsilon^4*(H^-1)_zz -> -K/(a^3*b^2/N)*G^-2; nonzero for fixed positive K,b,a,N",
            "rank_scope":"Raw psi/z velocity block before complete nonlinear scalar/tensor/frame/dust constraint response; not the physical reduced Hessian or ghost spectrum.",
            "direct_auxiliary_response":"z2=-[psi_dot*W*W_dot+(psi_ddot+2H*psi_dot)*W^2]; all harmonics0,2,4,6; not full J2",
            "nonclaims":["No full coupled nonlinear field evolution","No all-action or all-classical no-go","No physical ghost or cutoff","No hypersurface-orthogonal replacement of independent U","No C2 dust-clock/G3V cosmic-clock chart conflation"]}


def velocity_block(profile,chart,eps):
    eta=mp.mpf(str(chart["eta"]));aa=mp.mpf(str(chart["a"]));pd=mp.mpf(str(chart["psi_dot"]))
    K=3*eta;b=5*eta/11;Aforce=2*eta**mp.mpf("1.5")/7;sa=aa**3;ee=mp.mpf(str(eps))
    G,J=profile["gm"],profile["jm"]
    A=sa*(K*(mp.eye(4)+ee**2*G)-6*Aforce*abs(pd)*abs(ee)**3*J)
    C=-sa*b*ee**2*G
    H=mp.matrix(8)
    for i in range(4):
        for j in range(4):H[i,j]=A[i,j];H[i,j+4]=C[i,j];H[i+4,j]=C[j,i]
    ci=C**-1;expected=mp.matrix(8)
    lower=-ci*A*ci.T
    for i in range(4):
        for j in range(4):expected[i,j+4]=ci[j,i];expected[i+4,j]=ci[i,j];expected[i+4,j+4]=lower[i,j]
    return H,expected,A,C,K,b,sa


def hessian_control(checks,profile,chart):
    p0=mp.mpf(str(chart["psi_dot"]));eta=mp.mpf(str(chart["eta"]));ee=mp.mpf("0.001")
    rr=mp.mpf(1)/3;K=3*eta;b=5*eta/11;Af=2*eta**mp.mpf("1.5")/7
    bounds=intervals(s.Rational(1,3))
    def lag(dv):
        def integrand(xx):
            wf=ee*(mp.cos(xx)+rr*mp.cos(3*xx))
            pp=p0+sum(dv[i]*mpbasis(i,xx) for i in range(4))
            zz=sum(dv[i+4]*mpbasis(i,xx) for i in range(4))
            return K*(1+wf*wf)*pp*pp/2-Af*abs(wf*pp)**3-b*wf*wf*zz*pp
        return mp.quad(integrand,bounds)/(2*mp.pi)
    H,_,_,_,_,_,_=velocity_block(profile,chart,0.001)
    origin=[mp.mpf(0)]*8;f0=lag(origin);records=[]
    for rel in ("0.0001","0.00005","0.000025"):
        steps=[mp.mpf(rel)*abs(p0)]*4+[mp.mpf(rel)*abs(p0)**3]*4
        worst=0.0
        for i,j in ((0,0),(0,1),(1,1),(0,4),(1,6),(3,7),(4,4)):
            if i==j:
                plus=origin.copy();minus=origin.copy();plus[i]=steps[i];minus[i]=-steps[i]
                actual=(lag(plus)-2*f0+lag(minus))/steps[i]**2
            else:
                total=mp.mpf(0)
                for si in (-1,1):
                    for sj in (-1,1):
                        point=origin.copy();point[i]=si*steps[i];point[j]=sj*steps[j]
                        total+=si*sj*lag(point)
                actual=total/(4*steps[i]*steps[j])
            worst=max(worst,mpscalar(actual,H[i,j]))
        checks.small("unexpanded_raw_action_Hessian_step_"+rel,worst)
        records.append({"relative_step":rel,"normalized_error":worst})
    return records


def calculate():
    mp.mp.dps=50
    for name,h in FROZEN.items():
        if common.sha((ROOT/name).read_bytes())!=h:raise RuntimeError("Frozen source drift: "+name)
    parents=[common.read_json(BASE+"r4c1_g3n1_attempt_01/summary.json"),common.read_json(BASE+"r4c1_g3k_c2_attempt_01/summary.json")]
    pins={}
    for parent in parents:
        for mapping in (parent["source_sha256"],parent.get("transitive_source_sha256",{})):
            for name,h in mapping.items():
                if name in pins and pins[name]!=h:raise RuntimeError("Conflicting inherited pin: "+name)
                pins[name]=h
    pins.update(FROZEN);pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins);checks=common.Checks()
    checks.add("all_scientific_pins_and_available_sidecars_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(missing),"known_absent":missing})
    formulas=symbolic(checks)
    print("Integrating exact multimode Gram and unsmoothed force controls...",flush=True)
    profiles=profile_integrals(checks)
    rows=common.read_json(BASE+"r4c1_g3v_attempt_01/samples.json")["rows"]
    checks.add("all_216_parent_chart_records_present",len(rows)==216)
    event_rows=[];phases=(math.pi/5,math.pi/3,math.pi/2,2*math.pi/3,4*math.pi/5)
    for i,row in enumerate(rows):
        eta=row["eta"];aa=row["a"];kk=row["k"];sig=-eta/(8-eta);ee=0.001;rho=1/3
        bracket_bound=1/math.sqrt(1+ee*ee*(1+abs(rho))**2)-abs(sig)*ee*ee*(1+abs(rho))**2
        checks.add(f"chart_{i}_nonzero_Frobenius_bound",bracket_bound>0 and aa>0,bracket_bound,"positive bracket; derivative L2 norm=(1+9*rho^2)/2>0")
        phase_rows=[];worst=0.0
        for xx in phases:
            wf=ee*(math.cos(xx)+rho*math.cos(3*xx));wx=ee*kk*(-math.sin(xx)-3*rho*math.sin(3*xx))
            bf=sig*wf;bx=sig*wx
            # Independent direct metric/U contraction and complex-step derivative.
            def theta(arg):
                wv=ee*(np.cos(arg)+rho*np.cos(3*arg));bv=sig*wv;ga=np.sqrt(1+wv*wv)
                metric=np.diag(np.array([-1+bv*bv,aa*aa,aa*aa,aa*aa],complex));metric[0,2]=metric[2,0]=aa*bv
                unit=np.array([ga,0,(wv-bv*ga)/aa,0],complex)
                return metric@unit
            th=theta(xx);derivative=np.imag(theta(xx+1j*1e-20))*kk/1e-20
            actual=float((th[2].real*derivative[0]-th[0].real*derivative[2]))
            expected=aa*(wx/math.sqrt(1+wf*wf)+wf*wf*bx)
            error=common.discrepancy(actual,expected);worst=max(worst,error)
            phase_rows.append({"chi":xx,"Frobenius_coefficient":actual,"exact_formula":expected,"normalized_error":error})
        checks.small(f"chart_{i}_direct_covariant_Frobenius",worst)
        p=row["psi_dot"];L=row["psi_ddot"]+2*row["H"]*p
        W={1:s.Rational(1,2),-1:s.Rational(1,2),3:s.Rational(1,6),-3:s.Rational(1,6)}
        V={1:s.Rational(1,8),-1:s.Rational(1,8),3:-s.Rational(1,16),-3:-s.Rational(1,16)}
        ww=convolution(W,W);wv=convolution(W,V)
        coeffs={m:float((p*float(wv.get(m,0))+L*float(ww.get(m,0)))*(1 if m==0 else 2)) for m in MODES}
        delta_error=0.0
        for xx in phases:
            wv0=math.cos(xx)+rho*math.cos(3*xx);vv0=math.cos(xx)/4-math.cos(3*xx)/8
            direct=p*wv0*vv0+L*wv0*wv0
            reconstructed=sum(v*math.cos(m*xx) for m,v in coeffs.items())
            delta_error=max(delta_error,common.discrepancy(direct,reconstructed))
        checks.small(f"chart_{i}_full_direct_auxiliary_harmonics",delta_error)
        checks.add(f"chart_{i}_direct_auxiliary_not_identically_zero",any(v!=0 for v in coeffs.values()),list(coeffs.values()),"direct source only; no completed scalar J2 claim")
        event_rows.append({"eta":eta,"method":row["method"],"t":row["t"],"k":kk,
                           "positive_Frobenius_bracket_bound":bracket_bound,"Frobenius_phase_witnesses":phase_rows,
                           "direct_Delta2_cosine_coefficients":{str(m):v for m,v in coeffs.items()},
                           "direct_auxiliary_harmonic_error":delta_error})
    charts=[r for r in rows if r["method"]=="DOP853" and r["t"] in (0,4) and r["k"]==20]
    checks.add("twelve_archived_raw_block_charts",len(charts)==12,len(charts))
    print("Checking raw multimode rank, inverse scaling and unexpanded action...",flush=True)
    blocks=[]
    for ic,chart in enumerate(charts):
        for ip,profile in enumerate(profiles):
            for eps in EPSILONS:
                H,formula,A,C,K,b,sa=velocity_block(profile,chart,eps)
                actual=H**-1;err=mperror(actual,formula)
                label=f"block_{ic}_{ip}_{eps}"
                checks.small(label+"_inverse_formula",err)
                checks.small(label+"_inverse_residual",float(fnorm(H*actual-mp.eye(8))))
                det_expected=mp.det(C)**2
                det_error=mpscalar(mp.det(H)/det_expected,mp.mpf(1))
                checks.small(label+"_determinant",det_error)
                gi=profile["gm"]**-1
                leading=-K/(sa*b*b)*(gi*gi)
                zz=mp.matrix([[actual[i+4,j+4] for j in range(4)] for i in range(4)])
                scaled=mp.mpf(str(eps))**4*zz
                limit_error=mperror(scaled,leading)
                checks.add(label+"_nonuniform_inverse_limit",limit_error<=10*eps*eps,limit_error,"<=10*epsilon^2; raw inverse grows as epsilon^-4")
                blocks.append({"eta":chart["eta"],"t":chart["t"],"rho":str(profile["rho"]),"epsilon":eps,
                               "raw_rank_nonzero_epsilon":8,"raw_rank_at_zero":4,
                               "normalized_inverse_error":err,"normalized_determinant_error":det_error,
                               "scaled_inverse_limit_error":limit_error,
                               "raw_inverse_zz_norm":str(fnorm(zz)),"scope":"raw psi/z block; not post-constraint physical Hessian"})
    benchmark=next(r for r in charts if r["eta"]==1 and r["t"]==0)
    fd=hessian_control(checks,profiles[2],benchmark)
    checks.add("all_144_raw_block_probes_retained",len(blocks)==144,len(blocks))
    source_family=common.read_json(BASE+"r4c1_g3_attempt_01/summary.json")
    failed=[c for c in source_family["checks"] if not c["passed"]]
    checks.add("inherited_failed_parent_preserved",len(failed)==1 and not failed[0]["passed"],failed)
    checks.add("all_source_pins_and_available_sidecars_after",common.inspect_pins(pins)==missing)
    formulas["profile_Gram_controls"]=[{"rho":str(p["rho"]),"Gram":[[str(v) for v in p["G"].row(i)] for i in range(4)],"leading_minors":list(map(str,p["minors"]))} for p in profiles]
    payloads={"formulas.json":common.encode(formulas),"samples.json":common.encode({"transverse_chart_events":event_rows,"raw_velocity_blocks":blocks,"unexpanded_Hessian_controls":fd,"inherited_failed_parent_checks":failed,"profile_integrals_computed_once_per_rho":4})}
    passed=sum(c["passed"] for c in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3n2-transverse-entry-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
             "passed":passed,"total":len(checks.rows),"checks":checks.rows,"source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],
             "artifacts":{name:common.sha(data) for name,data in payloads.items()},"inherited_sidecars_absent":missing,
             "status":"INTRINSIC_PREFERRED_LEAF_AND_UNIFORM_RAW_ALGEBRAIC_Z_EXTENSIONS_REJECTED_FULL_COUPLED_DAE_OPEN" if ok else "MULTIMODE_ENTRY_AUDIT_REQUIRES_DISPOSITION",
             "transverse_charts":216,"raw_block_probes":144,
             "max_Frobenius_normalized_error":max(p["normalized_error"] for e in event_rows for p in e["Frobenius_phase_witnesses"]),
             "min_Frobenius_positive_bracket_bound":min(e["positive_Frobenius_bracket_bound"] for e in event_rows),
             "max_raw_inverse_normalized_error":max(e["normalized_inverse_error"] for e in blocks),
             "max_raw_determinant_normalized_error":max(e["normalized_determinant_error"] for e in blocks),
             "max_unexpanded_Hessian_normalized_error":max(e["normalized_error"] for e in fd),
             "full_nonlinear_scalar_tensor_frame_constraint_response_verified":False,
             "full_reduced_Legendre_map_regular_verified":False,"full_coupled_classical_uniqueness_verified":False,
             "physical_ghost_proven":False,"all_actions_no_go":False,"all_classical_formulations_rejected":False,
             "physical_EFT_cutoff_derived":False,"canonical_tests_1_to_3":"HOLD_SUBSTANTIVE",
             "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
             "review_status":"DEFERRED","Rule9_cleared":False,"physics_pass":False,"gate_effect":"NONE",
             "review_dependencies":["R9-MT1-G3N1","R9-MT1-G3V","R9-MT1-G3K-C2","all inherited scientific and review debt"],
             "runtime":{"python":platform.python_version(),"numpy":np.__version__,"sympy":s.__version__,"scipy":scipy.__version__,"mpmath":mp.__version__,"mp_decimal_digits":mp.mp.dps}}
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",default=BASE+"r4c1_g3n2_attempt_01");parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
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
            with (dest/name).open("xb") as handle:handle.write(data)
            with (dest/(name+".sha256")).open("xb") as handle:handle.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect","Rule9_cleared")}}))
    for c in summary["checks"]:
        if not c["passed"]:print(json.dumps(c))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
