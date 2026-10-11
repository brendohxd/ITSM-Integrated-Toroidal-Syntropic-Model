"""70-digit independent IVP/finite-difference witness; v1 remains immutable."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE="Analysis/MasterTests/outputs/"
OLD=BASE+"r4c1_g3n5_constraint_response_attempt_01/"
ENGINE="Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v1.py"
ADDENDUM="Theory/Gates/RES-001/RES001_R4C1_G3N5_RESPONSE_PRECISION_V2_ADDENDUM_2026-10-10.md"
PINS={ENGINE:"6b9cc5f402957172c0dfcaa2f0a81997235287380e77a60c4649eb9e16a09f37",
      OLD+"summary.json":"b13e97122e724e58465db28df036ee835fd305b31078146cb7a283da38ee9d95",
      ADDENDUM:"a7242a538b09719bd03f3001379c729729f3c2a901c0ab309b72383e1b4fda5b"}
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!=PINS[ENGINE]:
    raise RuntimeError("Immutable v1 engine drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3n5_constraint_response_v1 as v1
common=v1.common
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ORDER=40


def scalar(value):
    if isinstance(value,s.Rational):return mp.mpf(int(value.p))/int(value.q)
    return mp.mpmathify(value)


class Series:
    """Truncated coefficient convolution, with exact integer-power recurrences."""
    work=0

    def __init__(self,value=0):
        self.c=[scalar(value)]+[mp.mpf(0)]*ORDER

    @classmethod
    def wrap(cls,value):return value if isinstance(value,cls) else cls(value)

    def __add__(self,other):
        other=self.wrap(other);out=Series()
        for j in range(self.work+1):out.c[j]=self.c[j]+other.c[j]
        return out

    __radd__=__add__

    def __neg__(self):
        out=Series()
        for j in range(self.work+1):out.c[j]=-self.c[j]
        return out

    def __sub__(self,other):return self+-self.wrap(other)
    def __rsub__(self,other):return self.wrap(other)+-self

    def __mul__(self,other):
        other=self.wrap(other);out=Series()
        for j in range(self.work+1):
            out.c[j]=sum((self.c[k]*other.c[j-k] for k in range(j+1)
                          if self.c[k]!=0 and other.c[j-k]!=0),mp.mpf(0))
        return out

    __rmul__=__mul__

    def reciprocal(self):
        if self.c[0]==0:raise ZeroDivisionError("Outside reciprocal series domain")
        out=Series(1/self.c[0])
        for j in range(1,self.work+1):
            out.c[j]=-sum((self.c[k]*out.c[j-k] for k in range(1,j+1)),mp.mpf(0))/self.c[0]
        return out

    def __truediv__(self,other):return self*self.wrap(other).reciprocal()
    def __rtruediv__(self,other):return self.wrap(other)*self.reciprocal()

    def __pow__(self,power):
        if int(power)!=power:raise TypeError("Only integer powers are registered")
        power=int(power)
        if power<0:return self.reciprocal()**(-power)
        out=Series(1);base=self
        while power:
            if power%2:out=out*base
            power//=2
            if power:base=base*base
        return out

    def evaluate(self,t,order=ORDER,derivative=0):
        result=mp.mpf(0)
        for j in range(order,derivative-1,-1):
            factor=1
            for k in range(derivative):factor*=j-k
            result=result*t+factor*self.c[j]
        return result


def numerical(checks,name,value,limit):
    checks.add(name,mp.isfinite(value) and value<=mp.mpf(str(limit)),str(value),"<="+str(limit))


def flatfun(op,matrices):
    return s.lambdify([op.bg],[list(q) for q in matrices],"mpmath",cse=True)


def product(flat,rows,columns,vector):
    return [sum((flat[i*columns+j]*vector[j] for j in range(columns)),mp.mpf(0)) for i in range(rows)]


def norm(vector):return max(abs(q) for q in vector)


def controls(checks):
    Series.work=ORDER;x=Series();x.c[1]=mp.mpf(1)
    inv=1/(1+x)
    numerical(checks,"series_reciprocal_exact_control",max(abs(inv.c[j]-(-1)**j) for j in range(ORDER+1)),"1e-60")
    y=Series(1)
    for j in range(ORDER):
        Series.work=j;y.c[j+1]=y.c[j]/(j+1)
    numerical(checks,"series_exponential_IVP_control",max(abs(y.c[j]-1/mp.factorial(j)) for j in range(ORDER+1)),"1e-60")


def background_series(op):
    initial=[scalar(q) if q!=op.h0 else mp.sqrt(mp.mpf(3469)/4620) for q in op.initial]
    states=[Series(q) for q in initial]
    fn=s.lambdify([op.bg],list(op.rates),"mpmath",cse=True)
    for order in range(ORDER):
        Series.work=order;rate=fn(states)
        for j in range(len(states)):states[j].c[order+1]=Series.wrap(rate[j]).c[order]/(order+1)
    return states


def response_series(op,chart,background,checks):
    N=chart["dimension"];mode=chart["mode"]
    E0,E1,E2=(chart["symbolic"][q] for q in ("E0","E1","E2"))
    v1.exact(checks,"background_independent_acceleration_"+str(mode),op.dtm(E2))
    if any(q.free_symbols & set(op.bg) for q in E2):
        raise ValueError("Constant inverse requested outside its verified domain")
    fn=flatfun(op,(E0,E1))
    initial=[q.c[0] for q in background]
    block=flatfun(op,(E2,))(initial)[0]
    inverse=mp.matrix([block[j*N:(j+1)*N] for j in range(N)])**-1
    eps=mp.mpf("1e-6")
    y=[Series(eps*((j+1)+mp.j*(-1)**j)/(N+1)) for j in range(N)]
    v=[Series(eps*((-1)**j*(j+1)-mp.j)/(N+1)) for j in range(N)]
    if mode==(0,0,0):
        y=[Series(q.c[0].real) for q in y];v=[Series(q.c[0].real) for q in v]
        name=chart["names"]
        v[name.index("dv")].c[0]=-y[name.index("du")].c[0]-sum(y[name.index(k)].c[0] for k in ("Mxx","Myy","Mzz"))/2-scalar(v1.PARAMS["beta"])*y[name.index("Pi")].c[0]
    for order in range(ORDER):
        Series.work=order;A,B=fn(background)
        forcing=[Series.wrap(q).c[order] for q in product(A,N,N,y)]
        bterm=[Series.wrap(q).c[order] for q in product(B,N,N,v)]
        acceleration=-inverse*mp.matrix([a+b for a,b in zip(forcing,bterm)])
        for j in range(N):
            y[j].c[order+1]=v[j].c[order]/(order+1)
            v[j].c[order+1]=acceleration[j]/(order+1)
    return y,v


def reconstructors(op,chart):
    mats=chart["symbolic"];Q0,Q1=mats["Q0"],mats["Q1"]
    emL,emM=mats["EmL"],mats["EmM"]
    rec=flatfun(op,(Q0,Q1,op.dtm(Q0),op.dtm(Q1),emL,emM,op.dtm(emL),op.dtm(emM)))
    mode=dict(zip(op.k,chart["mode"]))
    full=flatfun(op,tuple(q.subs(mode) for q in (op.EA,op.EB,op.ED)))
    def point(bg,y,v,w):
        N=len(y);q0,q1,q0d,q1d,el,ev,eld,evd=rec(bg)
        q=[a+b for a,b in zip(product(q0,22,N,y),product(q1,22,N,v))]
        qd=[a+b+c for a,b,c in zip(product(q0d,22,N,y),
            product([a+b for a,b in zip(q0,q1d)],22,N,v),product(q1,22,N,w))]
        # D annihilates every eliminated auxiliary column, so this has the
        # exact same acceleration contribution as F*y_ddot.
        qdd=product(q0,22,N,w)
        q[v1.IDX["Em"]]=(product(el,1,N,y)[0]+product(ev,1,N,v)[0])
        qd[v1.IDX["Em"]]=(product(eld,1,N,y)[0]+product([a+b for a,b in zip(el,evd)],1,N,v)[0]+product(ev,1,N,w)[0])
        A,B,D=full(bg)
        provisional=[a+b+c for a,b,c in zip(product(A,22,22,q),product(B,22,22,qd),product(D,22,22,qdd))]
        row=v1.IDX["nu"];column=v1.IDX["LambdaU"]
        q[column]=-provisional[row]/A[row*22+column]
        terms=(product(A,22,22,q),product(B,22,22,qd),product(D,22,22,qdd))
        residual=norm([sum(row) for row in zip(*terms)])/max(sum(norm(row) for row in terms),mp.mpf("1e-20"))
        return q,qd,residual
    return point,full


def coeffstrings(series):return [[[str(q.real),str(q.imag)] for q in obj.c] for obj in series]


def calculate():
    mp.mp.dps=70
    old=common.read_json(OLD+"summary.json");pins=dict(old["source_sha256"])
    for name,value in {**PINS,**{OLD+k:v for k,v in old["artifacts"].items()}}.items():
        if name in pins and pins[name]!=value:raise ValueError("Parent pin collision: "+name)
        pins[name]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes());missing=common.inspect_pins(pins)
    checks=common.Checks();checks.add("all_source_pins_before",True,{"pins":len(pins),"sidecars":len(pins)-len(missing),"absent":missing})
    failures=[q for q in old["checks"] if not q["passed"]]
    checks.add("v1_failures_preserved_and_scoped",len(failures)==5 and all(q["name"].startswith("full_Euler_refinement_") for q in failures))
    checks.add("v1_non_refinement_controls_passed",all(q["passed"] for q in old["checks"] if q not in failures))
    controls(checks)
    print("Reusing frozen v1 operator and chart proofs; constructing 70-digit series",flush=True)
    op=v1.Operator(checks)
    for mode in v1.MODES:op.exact_initial_gauge(checks,mode)
    charts=[op.chart(checks,mode) for mode in v1.MODES]
    background=background_series(op)
    time=[mp.mpf(j)/5120 for j in range(257)]
    bg_values=[[q.evaluate(t) for q in background] for t in time]
    bg_tail=max(abs(q.evaluate(t)-q.evaluate(t,32))/max(1,abs(q.evaluate(t))) for q in background for t in time)
    numerical(checks,"background_series_order_convergence",bg_tail,"1e-20")
    constraint=s.lambdify([op.bg],op.constraint,"mpmath",cse=True)
    numerical(checks,"high_precision_background_constraint",max(abs(constraint(bg)) for bg in bg_values),"1e-20")
    checks.add("high_precision_background_domain",all(min(bg[0],bg[9],bg[10])>0 for bg in bg_values))
    reference=np.load(ROOT/OLD/"unreduced_fields.npy",allow_pickle=False)
    old_diagnostics=common.read_json(OLD+"diagnostics.json")
    reports=[];allfields=[];coeffs=[]
    for mi,chart in enumerate(charts):
        mode=chart["mode"];print("70-digit coupled Taylor IVP mode "+str(mode),flush=True)
        y,v=response_series(op,chart,background,checks)
        tail=max(abs(q.evaluate(t)-q.evaluate(t,32))/mp.mpf("1e-6") for q in y+v for t in time)
        numerical(checks,"response_series_order_convergence_"+str(mode),tail,"1e-20")
        derivative=max(abs(a.evaluate(t,derivative=1)-b.evaluate(t))/mp.mpf("1e-6") for a,b in zip(y,v) for t in time)
        numerical(checks,"series_velocity_matches_true_derivative_"+str(mode),derivative,"1e-20")
        point,full=reconstructors(op,chart);values=[];analytic=mp.mpf(0);reduced_residual=mp.mpf(0);charge=[]
        reduced=flatfun(op,tuple(chart["symbolic"][k] for k in ("E0","E1","E2")))
        for t,bg in zip(time,bg_values):
            yy=[q.evaluate(t) for q in y];vv=[q.evaluate(t,derivative=1) for q in y];ww=[q.evaluate(t,derivative=2) for q in y]
            q,qd,residual=point(bg,yy,vv,ww);values.append(q);analytic=max(analytic,residual)
            A,B,D=reduced(bg);N=len(y)
            terms=(product(A,N,N,yy),product(B,N,N,vv),product(D,N,N,ww))
            reduced_residual=max(reduced_residual,norm([sum(row) for row in zip(*terms)])/max(sum(norm(row) for row in terms),mp.mpf("1e-20")))
            if mode==(0,0,0):
                a,H,u,ud,vv0,vd,r,rd,p,rho,C=bg
                charge.append(a**3*(u*qd[v1.IDX["dv"]]+q[v1.IDX["du"]]*vd-vv0*qd[v1.IDX["du"]]-q[v1.IDX["dv"]]*ud+
                    (sum(q[v1.IDX[k]] for k in ("Mxx","Myy","Mzz"))/2-q[v1.IDX["alpha"]])*(u*vd-vv0*ud)))
        numerical(checks,"true_polynomial_full_Euler_residual_"+str(mode),analytic,"1e-20")
        numerical(checks,"true_polynomial_reduced_Euler_residual_"+str(mode),reduced_residual,"1e-20")
        rounded=np.array([[complex(q) for q in row] for row in values]);allfields.append(rounded)
        disagreement=float(np.max(np.abs(rounded-reference[mi]))/max(v1.AMPLITUDE,np.max(np.abs(rounded)),np.max(np.abs(reference[mi]))))
        numerical(checks,"retained_v1_trajectory_agreement_"+str(mode),mp.mpf(disagreement),"1e-7")
        fd=[]
        for count in (65,129,257):
            stride=256//(count-1);dt=time[stride]-time[0];maximum=mp.mpf(0)
            for j in range(2,count-2):
                index=j*stride
                q=values[index]
                qd=[(-values[index+2*stride][i]+8*values[index+stride][i]-8*values[index-stride][i]+values[index-2*stride][i])/(12*dt) for i in range(22)]
                qdd=[(-values[index+2*stride][i]+16*values[index+stride][i]-30*q[i]+16*values[index-stride][i]-values[index-2*stride][i])/(12*dt*dt) for i in range(22)]
                A,B,D=full(bg_values[index]);terms=(product(A,22,22,q),product(B,22,22,qd),product(D,22,22,qdd))
                error=norm([sum(row) for row in zip(*terms)])/max(sum(norm(row) for row in terms),mp.mpf("1e-20"))
                maximum=max(maximum,error)
            fd.append({"samples":count,"error":str(maximum)})
        coarse,fine=mp.mpf(fd[0]["error"]),mp.mpf(fd[-1]["error"])
        improvement=coarse/max(fine,mp.mpf("1e-69"))
        numerical(checks,"original_fine_FD_criterion_"+str(mode),fine,"1e-5")
        checks.add("original_refinement_criterion_"+str(mode),improvement>=4 or max(coarse,fine)<=mp.mpf("1e-10"),
                   {"improvement":str(improvement),"errors":fd},">=4 or both<=1e-10; unchanged")
        drift=None
        if charge:
            drift=max(abs(q-charge[0]) for q in charge)/mp.mpf("1e-6")
            numerical(checks,"high_precision_mean_charge_drift",drift,"1e-8")
            numerical(checks,"high_precision_initial_mean_charge",abs(charge[0])/mp.mpf("1e-6"),"1e-12")
        reports.append({"mode":list(mode),"coordinates":chart["names"],"analytic_Euler_residual":str(analytic),
            "reduced_Euler_residual":str(reduced_residual),
            "series_tail":str(tail),"trajectory_disagreement":disagreement,"finite_difference":fd,
            "linearized_charge_drift":str(drift) if drift is not None else None,
            "unchanged_kinetic_eigenvalues":old_diagnostics["modes"][mi]["kinetic_eigenvalues"]})
        coeffs.append({"mode":list(mode),"coordinates":chart["names"],"y_coefficients":coeffstrings(y),"v_coefficients":coeffstrings(v)})
    checks.add("all_source_pins_after",common.inspect_pins(pins)==missing)
    payloads={"unreduced_fields.npy":v1.npy(np.array(allfields)),
        "series_coefficients.json":common.encode({"digits":70,"degree":40,"background_order":list(v1.BG_NAMES),
            "background_coefficients":coeffstrings(background),"response_coefficients":coeffs,
            "coefficient_representation":"real/imag decimal strings; Taylor powers, not derivatives"}),
        "diagnostics.json":common.encode({"modes":reports,"inherited_v1_failed_checks":failures,
            "inherited_v1_status":old["validation"],"inherited_v1_summary_sha256":PINS[OLD+"summary.json"],
            "kinetic_signs_not_reclassified":True,"mean_negative_eigenvalue":-0.55,
            "diagnosis_boundary":"Higher precision tests numerical limitations without rewriting or forgiving the original failed attempt",
            "physics_nonclaims":["No physical EFT cutoff or stability/ghost conclusion","No nonlinear or second-order forcing solve",
                "No global Cauchy theorem, physical DOF count, canonical matching or healthy continuous GR"]})}
    passed=sum(q["passed"] for q in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3n5-constraint-response-v2","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        "passed":passed,"total":len(checks.rows),"checks":checks.rows,
        "status":"CONDITIONAL_COUPLED_LINEAR_IVP_AND_70DIGIT_WITNESS_CHECKED" if ok else "PRECISION_WITNESS_REQUIRES_DISPOSITION",
        "source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],"artifacts":{k:common.sha(v) for k,v in payloads.items()},
        "inherited_sidecars_absent":missing,"coupled_linear_IVP_completed":ok,"old_v1_validation":"FAIL_LOCAL_CHECKS",
        "physics_pass":False,"gate_effect":"NONE","Rule9_cleared":False,"review_status":"DEFERRED",
        "canonical_tests_1_to_3":"HOLD_SUBSTANTIVE","MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS",
        "K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
        "full_nonlinear_evolution_verified":False,"full_second_order_response_solved":False,"physical_Hessian_verified":False,
        "physical_EFT_cutoff_derived":False,"runtime":{"mpmath":mp.__version__,"mp_decimal_digits":mp.mp.dps,
            "numpy":np.__version__,"sympy":s.__version__}}
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_g3n5_constraint_response_attempt_02")
    parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists():raise FileExistsError("Refuse existing scientific output")
    payloads,summary=calculate()
    if args.replay:
        for name,data in payloads.items():
            if (dest/name).read_bytes()!=data or (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Exact replay mismatch: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in payloads.items():
            with (dest/name).open("xb") as out:out.write(data)
            with (dest/(name+".sha256")).open("xb") as out:out.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect")}}))
    for q in summary["checks"]:
        if not q["passed"]:print(json.dumps(q))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
