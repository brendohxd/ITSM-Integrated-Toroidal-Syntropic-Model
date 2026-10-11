"""G3N4: frozen-action quadratic response sources, not their coupled solution.

Bivariate variation retains all response sectors, normal frame equation,
absolute-cubic vector source and homogeneous terms. Replay is read-only.
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
if hashlib.sha256((ROOT/HELPER).read_bytes()).hexdigest()!="d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224":raise RuntimeError("Frozen helper drift")
sys.path.insert(0,str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common

SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PINS={
 "Theory/Gates/RES-001/RES001_R4C1_G3N4_COUPLED_SOURCE_CONTRACT_2026-10-09.md":"a5f5880e894c544794fa46e7e68dfdd07c4960d44791751521b402cd8bb9a2b6",
 "Theory/Gates/RES-001/RES001_R4C1_G3N3_SECOND_ORDER_REGULATOR_REPORT_2026-10-09.md":"7111692a94582e3a1d44f0ca5fa3a5a2a1a4550db009beecc851e841119fd32b",
 BASE+"r4c1_g3n3_attempt_02/summary.json":"ee6683f0b99a087f009e29c653e719fb86647242182c58beea7f44b5e9998871",
 BASE+"r4c1_g3v_attempt_01/formulas.json":"1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358",
}
FIELD_NAMES=("alpha","Sx","Sy","Sz","Mxx","Mxy","Mxz","Myy","Myz","Mzz","Vx","Vy","Vz","du","dv","dr","Pi","T","Em","Z","nu","LambdaU")


def tidy(x):return s.factor(s.cancel(s.expand(x)))


class Jet:
    """Exact polynomial ring modulo e^3 and d^2; coefficients are symbolic."""
    def __init__(self,value=0):
        self.c=dict(value.c) if isinstance(value,Jet) else ({k:s.sympify(v) for k,v in value.items() if v!=0} if isinstance(value,dict) else ({(0,0):s.sympify(value)} if value!=0 else {}))
    def __add__(self,other):
        other=Jet(other);out=self.c.copy()
        for key,v in other.c.items():out[key]=out.get(key,0)+v
        return Jet(out)
    __radd__=__add__
    def __neg__(self):return Jet({k:-v for k,v in self.c.items()})
    def __sub__(self,other):return self+-Jet(other)
    def __rsub__(self,other):return Jet(other)+-self
    def __mul__(self,other):
        other=Jet(other);out={}
        for (i,j),v in self.c.items():
            for (ii,jj),vv in other.c.items():
                if i+ii<=2 and j+jj<=1:out[(i+ii,j+jj)]=out.get((i+ii,j+jj),0)+v*vv
        return Jet(out)
    __rmul__=__mul__
    def __truediv__(self,other):
        if isinstance(other,Jet):raise TypeError("Only scalar divisions; inverse jets are explicit")
        return Jet({k:v/s.sympify(other) for k,v in self.c.items()})
    def clean(self):return Jet({k:s.expand(v) for k,v in self.c.items()})
    def coeff(self,i,j):return self.c.get((i,j),s.Integer(0))


def zeros(n,m=None):return [[Jet() for _ in range(m or n)] for _ in range(n)]
def eye(n):return [[Jet(int(i==j)) for j in range(n)] for i in range(n)]
def transpose(A):return list(map(list,zip(*A)))
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))).clean() for j in range(len(B[0]))] for i in range(len(A))]
def trace(A):return sum(A[i][i] for i in range(len(A)))
def scalar(v,A,w):return sum(v[i]*A[i][j]*w[j] for i in range(len(v)) for j in range(len(w))).clean()


def exact(checks,name,value):
    values=list(value) if isinstance(value,(list,tuple)) else [value]
    residuals=[tidy(v) for v in values];ok=all(v==0 for v in residuals)
    checks.add(name,ok,"zero_exact" if ok else list(map(str,residuals)),"zero_exact")


def derive(checks):
    a=s.Symbol("a",positive=True)
    H,Hd,p,pdd,W,Wt,Wz,Wtt,Wtz,Wzz,B,Bt,Bz,Btt,Btz,Bzz=s.symbols("H Hdot psi_dot psi_ddot W W_t W_z W_tt W_tz W_zz B B_t B_z B_tt B_tz B_zz",real=True)
    MP,MU,K,b,zeta,beta,C,eps0,lam0=s.symbols("MP2 MU2 K_Q b zeta beta C epsilon0 lambda0",real=True)
    c1,c2,c3,c4=s.symbols("c1 c2 c3 c4",real=True)
    u,v,r,ud,vd,rd=s.symbols("u0 v0 r0 u_dot v_dot r_dot",real=True)
    udd,vdd,rdd,Ct,epsdot,lamdot=s.symbols("u_ddot v_ddot r_ddot C_dot epsilon_dot lambda_dot",real=True)
    R={name:s.Symbol(name,real=True) for name in FIELD_NAMES}
    Rt={name:s.Symbol(name+"_t",real=True) for name in FIELD_NAMES}
    Rz={name:s.Symbol(name+"_z",real=True) for name in FIELD_NAMES}
    dtmap={a:a*H,H:Hd,p:pdd,W:Wt,Wt:Wtt,Wz:Wtz,B:Bt,Bt:Btt,Bz:Btz,u:ud,v:vd,r:rd,ud:udd,vd:vdd,rd:rdd,C:Ct,eps0:epsdot,lam0:lamdot,**{R[k]:Rt[k] for k in R}}
    dzmap={W:Wz,Wt:Wtz,Wz:Wzz,B:Bz,Bt:Btz,Bz:Bzz,**{R[k]:Rz[k] for k in R}}
    def deriv(expr,mapping):return sum(s.diff(expr,k)*vv for k,vv in mapping.items() if k in expr.free_symbols)
    def djet(obj,mu):
        if mu not in (0,3):return Jet()
        mapping=dtmap if mu==0 else dzmap
        return Jet({key:deriv(val,mapping) for key,val in obj.c.items()}).clean()
    def dt(expr):return s.expand(deriv(expr,dtmap))
    def dz(expr):return s.expand(deriv(expr,dzmap))

    e=Jet({(1,0):1});d=Jet({(0,1):1})
    N=1+d*R["alpha"];invN=1-d*R["alpha"];invN2=1-2*d*R["alpha"]
    mi=(("Mxx","Mxy","Mxz"),("Mxy","Myy","Myz"),("Mxz","Myz","Mzz"))
    h=[[a*a*(int(i==j)+d*R[mi[i][j]]) for j in range(3)] for i in range(3)]
    hi=[[(int(i==j)-d*R[mi[i][j]])/(a*a) for j in range(3)] for i in range(3)]
    shift=[(e*B*int(i==1)+d*R[name])/a for i,name in enumerate(("Sx","Sy","Sz"))]
    velocity=[(e*W*int(i==1)+d*R[name])/a for i,name in enumerate(("Vx","Vy","Vz"))]
    gam=1+e*e*W*W/2+e*d*W*R["Vy"]+e*e*d*R["Myy"]*W*W/2
    normal=[(gam*invN).clean()]+[(velocity[i]-shift[i]*gam*invN).clean() for i in range(3)]
    frame=[((1+d*R["nu"])*vv).clean() for vv in normal]
    g=zeros(4);gi=zeros(4);g[0][0]=(-N*N+scalar(shift,h,shift)).clean();gi[0][0]=-invN2
    for i in range(3):
        g[0][i+1]=g[i+1][0]=sum(h[i][j]*shift[j] for j in range(3)).clean()
        gi[0][i+1]=gi[i+1][0]=(shift[i]*invN2).clean()
        for j in range(3):g[i+1][j+1]=h[i][j];gi[i+1][j+1]=(hi[i][j]-shift[i]*shift[j]*invN2).clean()
    product=mm(g,gi)
    exact(checks,"bivariate_ADM_inverse",[product[i][j].coeff(ii,jj)-int(i==j and ii==jj==0) for i in range(4) for j in range(4) for ii in range(3) for jj in range(2)])
    unit=scalar(normal,g,normal)+1
    exact(checks,"normalized_n_bivariate_unit",[unit.coeff(i,j) for i in range(3) for j in range(2)])
    off=scalar(frame,g,frame)+1+2*d*R["nu"]
    exact(checks,"normal_frame_variation_retained",[off.coeff(i,j) for i in range(3) for j in range(2)])
    print("Building general bivariate metric/frame connection...",flush=True)
    Gamma=[[[sum(gi[c][j]*(djet(g[j][bb],aa)+djet(g[j][aa],bb)-djet(g[aa][bb],j)) for j in range(4)).clean()/2 for bb in range(4)] for aa in range(4)] for c in range(4)]
    def nabla(vec):return [[(djet(vec[nu],mu)+sum(Gamma[nu][mu][j]*vec[j] for j in range(4))).clean() for nu in range(4)] for mu in range(4)]
    DN=nabla(normal);DU=nabla(frame)
    accN=[sum(normal[j]*DN[j][i] for j in range(4)).clean() for i in range(4)]
    accU=[sum(frame[j]*DU[j][i] for j in range(4)).clean() for i in range(4)]
    I1=sum(gi[i][j]*g[k][l]*DU[i][k]*DU[j][l] for i in range(4) for j in range(4) for k in range(4) for l in range(4)).clean()
    I2=trace(DU)*trace(DU);I3=trace(mm(DU,DU));I4=scalar(accU,g,accU)
    frameL=(-MU*(c1*I1+c2*I2+c3*I3-c4*I4)/2).clean()
    hp=[[(gi[i][j]+normal[i]*normal[j]).clean() for j in range(4)] for i in range(4)]
    volum=1+d*(R["alpha"]+(R["Mxx"]+R["Myy"]+R["Mzz"])/2)
    gradPsi=[p+d*Rt["Pi"],Jet(),Jet(),d*Rz["Pi"]]
    gradZ=[d*Rt["Z"],Jet(),Jet(),d*Rz["Z"]]
    Qu=sum(normal[i]*gradPsi[i] for i in range(4)).clean()
    forceTemporal=K*Qu*Qu/2
    reg=(b*d*d*R["Z"]**2/2-b*scalar(gradZ,hp,gradPsi)-b*d*R["Z"]*sum(accN[i]*gradPsi[i] for i in range(4))).clean()
    uu=u+d*R["du"];vv=v+d*R["dv"];rr=r+d*R["dr"]
    gu=[ud+d*Rt["du"],Jet(),Jet(),d*Rz["du"]]
    gv=[vd+d*Rt["dv"],Jet(),Jet(),d*Rz["dv"]]
    gr=[rd+d*Rt["dr"],Jet(),Jet(),d*Rz["dr"]]
    current=[(vv*gu[i]-uu*gv[i]).clean() for i in range(4)]
    align=(-zeta*scalar(current,hp,current)/2).clean()
    m2,l4,l6,Lambda,mr2,lr,grportal,rhol=s.symbols("m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda",real=True)
    ss=uu*uu+vv*vv
    potential=m2*ss/2+l4*ss*ss/8+l6*ss*ss*ss/(24*Lambda**2)+mr2*rr*rr/2+lr*rr*rr*rr*rr/4+grportal*ss*rr*rr/4+rhol
    canonical=(-scalar(gu,gi,gu)/2-scalar(gv,gi,gv)/2-scalar(gr,gi,gr)/2-potential).clean()
    taugrad=[C+d*Rt["T"],Jet(),Jet(),d*Rz["T"]]
    matter=-(eps0+d*R["Em"])*(C*C*(1+2*d*beta*R["Pi"])*scalar(taugrad,gi,taugrad)+C**4*(1+4*d*beta*R["Pi"]))/2
    multiplier=(lam0+d*R["LambdaU"])*(scalar(frame,g,frame)+1)/2

    # EH+GHY bulk. Spatial Ricci is independent of e, so its e^2 d coefficient vanishes.
    print("Building retained ADM gravity source and action sectors...",flush=True)
    spatialGamma=[[[sum(hi[c][j]*(djet(h[j][bb],aa+1)+djet(h[j][aa],bb+1)-djet(h[aa][bb],j+1)) for j in range(3)).clean()/2 for bb in range(3)] for aa in range(3)] for c in range(3)]
    shiftCov=[sum(h[i][j]*shift[j] for j in range(3)).clean() for i in range(3)]
    Dshift=[[(djet(shiftCov[j],i+1)-sum(spatialGamma[k][i][j]*shiftCov[k] for k in range(3))).clean() for j in range(3)] for i in range(3)]
    extrinsic=[[(invN*(djet(h[i][j],0)-Dshift[i][j]-Dshift[j][i])/2).clean() for j in range(3)] for i in range(3)]
    Kmixed=mm(hi,extrinsic)
    Einstein=MP*(trace(mm(Kmixed,Kmixed))-trace(Kmixed)*trace(Kmixed))/2
    R3symbol=s.Symbol("R3_response",real=True)
    ricci=MP*d*R3symbol/2
    sectors={"Einstein_ADM":Einstein,"spatial_Ricci":ricci,"frame":frameL,"alignment":align,"temporal_force":forceTemporal,"regulator":reg,"Cartesian_scalars_potential_portal":canonical,"dust":matter,"unit_multiplier":multiplier}
    mix={key:tidy((volum*value).coeff(2,1)) for key,value in sectors.items()}
    quad={key:tidy((volum*value).coeff(2,0)) for key,value in sectors.items()}
    for key in ("spatial_Ricci","Cartesian_scalars_potential_portal","dust","unit_multiplier"):exact(checks,key+"_no_direct_quadratic_vector_source",mix[key])
    total=tidy(sum(mix.values()));L2=tidy(sum(quad.values()))
    expectedFrame=MU*((c1+c4)*Wt**2-c1*Wz**2/a**2+(c1+c3)*Wz*Bz/a**2-(c1+c3)*Bz**2/(2*a**2)+2*(c4-3*c2-c3)*H*W*Wt+(c4-2*c1-9*c2-3*c3)*H**2*W**2)/2
    expectedL2=expectedFrame+MP*Bz*Bz/(4*a*a)+(K*p*p-zeta*(v*ud-u*vd)**2)*W*W/2
    exact(checks,"quadratic_action_matches_G3V",L2-expectedL2)
    print("Varying every retained response field before shift substitution...",flush=True)
    coefficients={};sources={}
    for name in FIELD_NAMES:
        cv=tidy(s.diff(total,R[name]));ct=tidy(s.diff(total,Rt[name]));cz=tidy(s.diff(total,Rz[name]))
        coefficients[name]={"value":str(cv),"time_derivative":str(ct),"spatial_derivative":str(cz)}
        sources[name]=tidy(cv-dt(ct)-3*H*ct-dz(cz))
        print(" source "+name,flush=True)
    exact(checks,"full_mixed_source_linear_in_retained_jets",total-sum(s.sympify(coefficients[n]["value"],locals={str(x):x for x in total.free_symbols})*R[n]+s.sympify(coefficients[n]["time_derivative"],locals={str(x):x for x in total.free_symbols})*Rt[n]+s.sympify(coefficients[n]["spatial_derivative"],locals={str(x):x for x in total.free_symbols})*Rz[n] for n in FIELD_NAMES))
    direct=p*W*Wt+(pdd+2*H*p)*W*W
    exact(checks,"Z_source_matches_complete_G3N3_direct_term",sources["Z"]-b*direct)
    J=v*ud-u*vd;Jd=v*udd-u*vdd
    expectedU=zeta*((Jd+3*H*J)*v*W*W+2*J*vd*W*W+2*J*v*W*Wt)
    expectedV=-zeta*((Jd+3*H*J)*u*W*W+2*J*ud*W*W+2*J*u*W*Wt)
    exact(checks,"independent_alignment_du_source",sources["du"]-expectedU)
    exact(checks,"independent_alignment_dv_source",sources["dv"]-expectedV)
    exact(checks,"independent_temporal_psi_source",sources["Pi"]+K*((pdd+3*H*p)*W*W+2*p*W*Wt))
    for name in ("dr","T","Em","LambdaU"):exact(checks,name+"_no_direct_source_not_a_response_solution",sources[name])

    eta=s.Symbol("eta",positive=True)
    family={MP:1,MU:2*eta/3,c1:s.Rational(1,5),c2:-s.Rational(7,48),c3:-s.Rational(1,80),c4:s.Rational(1,20),K:3*eta,b:5*eta/11,zeta:eta/13}
    sigma=-eta/(8-eta)
    shiftmap={B:sigma*W,Bt:sigma*Wt,Bz:sigma*Wz,Btt:sigma*Wtt,Btz:sigma*Wtz,Bzz:sigma*Wzz}
    shifted={name:tidy(value.subs(family).subs(shiftmap)) for name,value in sources.items()}
    reducedL2=tidy(L2.subs(family).subs(shiftmap))
    EW=tidy(s.diff(reducedL2,W)-dt(s.diff(reducedL2,Wt))-3*H*s.diff(reducedL2,Wt)-dz(s.diff(reducedL2,Wz)))
    Wtt_solution=-3*H*Wt+(s.Rational(4,5)+3*eta/(8*(8-eta)))*Wzz/a**2-(2*(Hd+H*H)-18*p*p+6*J*J/13)*W
    exact(checks,"G3_linear_vector_equation_owning_mass",EW.subs(Wtt,Wtt_solution))
    energy=tidy(-dt(shifted["alpha"])-3*H*shifted["alpha"]+2*H*(shifted["Mxx"]+shifted["Myy"]+shifted["Mzz"])+dz(shifted["Sz"]+shifted["Vz"])/a+ud*shifted["du"]+vd*shifted["dv"]+rd*shifted["dr"]+p*shifted["Pi"]+C*shifted["T"]+epsdot*shifted["Em"]+lamdot*shifted["LambdaU"])
    momentum=tidy(a*(dt(shifted["Sz"])+4*H*shifted["Sz"])+2*dz(shifted["Mzz"]))
    exact(checks,"G3_temporal_source_Ward_on_linear_vector_shell",energy.subs(Wtt,Wtt_solution))
    exact(checks,"G3_longitudinal_source_Ward_on_linear_vector_shell",momentum.subs(Wtt,Wtt_solution))
    # Off-shell residuals are exported, not silently discarded.
    ward={"temporal_on_shell_residual":str(tidy(energy.subs(Wtt,Wtt_solution))),"longitudinal_on_shell_residual":str(tidy(momentum.subs(Wtt,Wtt_solution))),
          "temporal_before_vector_shell":str(energy),"longitudinal_before_vector_shell":str(momentum),"vector_equation":str(EW),"vector_Wtt_solution":str(Wtt_solution),
          "gauge_weights":{"time":"delta alpha=xi_t; delta Mii=2Hxi; delta Sz=delta Vz=-xi_z/a; delta f=f_dot xi","longitudinal_space":"delta Sz=a xi_t; delta Mzz=2xi_z; background boosts/scalars unchanged"}}
    formulas={"sectors_mixed_source_functional":{k:str(v) for k,v in mix.items()},"mixed_source_functional":str(total),"quadratic_vector_action":str(L2),
              "response_coefficients":coefficients,"Euler_sources_before_shift":{k:str(v) for k,v in sources.items()},"G3_Euler_sources_after_shift":{k:str(v) for k,v in shifted.items()},
              "Ward":ward,"normal_equation_scope":"nu source retained; unit equation fixes norm response and normal equation determines lambda response in the later solve",
              "homogeneous_scope":"No Laplacian inverse or omitted mean; sources not solved response amplitudes"}
    return formulas,total,{str(x):x for x in total.free_symbols},R,Rt,Rz


def force_controls(checks):
    A,p,W=s.symbols("A p W",real=True);c=s.Symbol("chi",real=True)
    profile=s.cos(c)+s.cos(3*c)/3
    exact(checks,"two_harmonic_profile_is_cubed_cosine",s.expand_trig(profile)-4*s.cos(c)**3/3)
    n=s.Symbol("n",integer=True,positive=True)
    rational=tidy(s.Rational(10)/n-15*n/(n*n-4)+6*n/(n*n-16)-n/(n*n-36))
    exact(checks,"odd_Fourier_rational_identity",rational+23040/(n*(n*n-4)*(n*n-16)*(n*n-36)))
    coefficients=[]
    for m in range(1,32,2):
        exact_value=-s.Integer(5120)*(-1)**((m-1)//2)/(s.pi*m*(m*m-4)*(m*m-16)*(m*m-36))
        actual=mp.mpf(64)/(9*mp.pi)*mp.quad(lambda x:mp.cos(x)**6*mp.cos(m*x),[0,mp.pi/2])
        target=mp.mpf(str(s.N(exact_value,60)))
        error=float(abs(actual-target)/max(mp.mpf(1),abs(target)))
        checks.add(f"odd_force_harmonic_{m}_unexpanded_integral",error<=1e-12,error,"<=1e-12")
        coefficients.append({"mode":m,"coefficient":str(exact_value),"normalized_error":error})
    checks.add("every_odd_force_harmonic_nonzero",all(v["coefficient"]!="0" for v in coefficients),"general denominator has no zero for positive odd m","infinite odd tail; no finite-mode closure")
    # Direct one-sided derivative of the actual nonanalytic density; no Taylor vertex.
    for ep in (mp.mpf("0.01"),mp.mpf("-0.01")):
        aa=mp.mpf("0.14");pd=mp.mpf("0.2");ww=mp.mpf("-0.3")
        actual=mp.diff(lambda vv:-aa*abs(pd*vv)**3,ep*ww)
        target=-3*aa*abs(pd)**3*ep*abs(ep)*ww*abs(ww)
        checks.add("absolute_force_source_sign_"+str(ep),abs(actual-target)<=mp.mpf("1e-30"),str(actual-target),"<=1e-30")
    return {"transverse_Euler_source":"-3*A*abs(psi_dot)^3*e*abs(e)*W*abs(W)","other_second_order_force_sources":"Zero on the first-order pure transverse direction; lapse/spatial metric/psi sources first appear at order |e|^3, other boosts have zero first directional variation there",
            "profile":"W=(4/3)cos(chi)^3","odd_coefficient_general":"-5120*sin(m*pi/2)/(pi*m*(m^2-4)*(m^2-16)*(m^2-36)); m positive odd",
            "even_and_mean_coefficients":"zero by half-period antisymmetry","coefficients":coefficients,"cutoff":"NOT_DERIVED; the infinite harmonic tail is retained"}


def numeric_inputs(which):
    params={"a":"1.4","H":"0.4","MP2":"1.1","MU2":"0.2","c1":"0.2","c2":"-0.14","c3":"-0.0125","c4":"0.05","K_Q":"0.75","b":"0.11","zeta":"0.03","beta":"0.02","C":"1.3","epsilon0":"0.07","lambda0":"0.08","u0":"0.4","v0":"0.6","r0":"0.13","u_dot":"0.7","v_dot":"-0.2","r_dot":"0.03","psi_dot":"0.125","W":"0.3","W_t":"-0.28","W_z":"0.25","B":"-0.2","B_t":"0.11","B_z":"-0.16"}
    if which:params.update({"H":"0.23","a":"1.8","psi_dot":"-0.21","W":"-0.37","W_t":"0.18","W_z":"-0.22","u_dot":"-0.31","v_dot":"0.12"})
    params={k:mp.mpf(v) for k,v in params.items()}
    responses={name:(mp.mpf((i+1)*(1 if not which else (-1)**i))/121,mp.mpf((i%5)-2)/157,mp.mpf((i%7)-3)/173) for i,name in enumerate(FIELD_NAMES)}
    return params,responses


def raw_analytic(e,d,params,responses):
    def q(name,t,z):
        r=responses[name];return r[0]+r[1]*t+r[2]*z
    def point(t,z):
        aa=params["a"]*mp.exp(params["H"]*t);N=1+d*q("alpha",t,z)
        names=(("Mxx","Mxy","Mxz"),("Mxy","Myy","Myz"),("Mxz","Myz","Mzz"))
        h=aa*aa*mp.matrix([[int(i==j)+d*q(names[i][j],t,z) for j in range(3)] for i in range(3)])
        BB=params["B"]+params["B_t"]*t+params["B_z"]*z;WW=params["W"]+params["W_t"]*t+params["W_z"]*z
        shift=mp.matrix([(e*BB*int(i==1)+d*q(name,t,z))/aa for i,name in enumerate(("Sx","Sy","Sz"))])
        vel=mp.matrix([(e*WW*int(i==1)+d*q(name,t,z))/aa for i,name in enumerate(("Vx","Vy","Vz"))])
        gamma=mp.sqrt(1+(vel.T*h*vel)[0]);normal=mp.matrix([gamma/N]+[vel[i]-shift[i]*gamma/N for i in range(3)])
        g=mp.matrix(4);g[0,0]=-N*N+(shift.T*h*shift)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=(h*shift)[i]
            for j in range(3):g[i+1,j+1]=h[i,j]
        return g,normal,h,shift,N
    zero=mp.mpf(0);g,n,h,shift,N=point(zero,zero);gi=g**-1;hi=h**-1
    def derivative(fn,mu):
        if mu==0:return mp.diff(lambda value:fn(value,zero),zero)
        if mu==3:return mp.diff(lambda value:fn(zero,value),zero)
        return mp.mpf(0)
    dg=[mp.matrix([[derivative(lambda t,z:point(t,z)[0][i,j],mu) for j in range(4)] for i in range(4)]) for mu in range(4)]
    Gamma=[[[sum(gi[c,j]*(dg[aa][j,bb]+dg[bb][j,aa]-dg[j][aa,bb]) for j in range(4))/2 for bb in range(4)] for aa in range(4)] for c in range(4)]
    DN=mp.matrix([[derivative(lambda t,z:point(t,z)[1][nu],mu)+sum(Gamma[nu][mu][j]*n[j] for j in range(4)) for nu in range(4)] for mu in range(4)])
    nu=1+d*responses["nu"][0];U=nu*n
    DU=nu*DN+mp.matrix([[d*responses["nu"][1 if mu==0 else 2]*n[j] if mu in (0,3) else 0 for j in range(4)] for mu in range(4)])
    acc=DU.T*U;accN=DN.T*n
    I1=sum(gi[i,j]*g[k,l]*DU[i,k]*DU[j,l] for i in range(4) for j in range(4) for k in range(4) for l in range(4))
    frame=-params["MU2"]*(params["c1"]*I1+params["c2"]*sum(DU[i,i] for i in range(4))**2+params["c3"]*sum(DU[i,j]*DU[j,i] for i in range(4) for j in range(4))-params["c4"]*(acc.T*g*acc)[0])/2
    dh=[mp.matrix([[derivative(lambda t,z:point(t,z)[2][i,j],mu+1) for j in range(3)] for i in range(3)]) for mu in range(3)]
    ht=mp.matrix([[derivative(lambda t,z:point(t,z)[2][i,j],0) for j in range(3)] for i in range(3)])
    G3=[[[sum(hi[c,j]*(dh[aa][j,bb]+dh[bb][j,aa]-dh[j][aa,bb]) for j in range(3))/2 for bb in range(3)] for aa in range(3)] for c in range(3)]
    shiftCov=h*shift
    Dshift=mp.matrix([[derivative(lambda t,z:(point(t,z)[2]*point(t,z)[3])[j],i+1)-sum(G3[k][i][j]*shiftCov[k] for k in range(3)) for j in range(3)] for i in range(3)])
    Km=hi*(ht-Dshift-Dshift.T)/(2*N)
    EH=params["MP2"]*(sum(Km[i,j]*Km[j,i] for i in range(3) for j in range(3))-sum(Km[i,i] for i in range(3))**2)/2
    grads={name:mp.matrix([params[bg]+d*responses[name][1],0,0,d*responses[name][2]]) for name,bg in (("du","u_dot"),("dv","v_dot"),("dr","r_dot"),("Pi","psi_dot"))}
    uv=params["u0"]+d*responses["du"][0];vv=params["v0"]+d*responses["dv"][0];rv=params["r0"]+d*responses["dr"][0]
    current=vv*grads["du"]-uv*grads["dv"];hp=gi+n*n.T
    alignment=-params["zeta"]*(current.T*hp*current)[0]/2
    temporal=params["K_Q"]*(n.T*grads["Pi"])[0]**2/2
    zval=d*responses["Z"][0];zgrad=mp.matrix([d*responses["Z"][1],0,0,d*responses["Z"][2]])
    regulator=params["b"]*zval*zval/2-params["b"]*(zgrad.T*hp*grads["Pi"])[0]-params["b"]*zval*(accN.T*grads["Pi"])[0]
    ss=uv*uv+vv*vv
    potential=mp.mpf("0.1")*ss/2+mp.mpf("0.3")*ss*ss/8+ss**3/96+mp.mpf("0.2")*rv*rv/2+mp.mpf("0.4")*rv**4/4+mp.mpf("0.5")*ss*rv*rv/4+mp.mpf("0.09")
    scalar=-sum((grads[name].T*gi*grads[name])[0] for name in ("du","dv","dr"))/2-potential
    CC=params["C"]*mp.exp(params["beta"]*d*responses["Pi"][0]);tau=mp.matrix([params["C"]+d*responses["T"][1],0,0,d*responses["T"][2]])
    dust=-(params["epsilon0"]+d*responses["Em"][0])*(CC*CC*(tau.T*gi*tau)[0]+CC**4)/2
    unit=(params["lambda0"]+d*responses["LambdaU"][0])*((U.T*g*U)[0]+1)/2
    volume=N*mp.sqrt(mp.det(h))/params["a"]**3
    return volume*(EH+frame+alignment+temporal+regulator+scalar+dust+unit)


def independent(checks,total,symbols,R,Rt,Rz):
    records=[]
    for index in range(2):
        params,responses=numeric_inputs(index)
        sub={symbols[k]:s.Float(str(v),60) for k,v in params.items() if k in symbols}
        sub.update({R[k]:s.Float(str(responses[k][0]),60) for k in R});sub.update({Rt[k]:s.Float(str(responses[k][1]),60) for k in R});sub.update({Rz[k]:s.Float(str(responses[k][2]),60) for k in R})
        expected_expr=total.subs(sub)
        if expected_expr.free_symbols:raise ValueError("Unspecified numeric source symbols: "+str(expected_expr.free_symbols))
        expected=mp.mpf(str(s.N(expected_expr,60)));rows=[];errors=[]
        for step in ("0.001","0.0005","0.00025"):
            ee=dd=mp.mpf(step)
            actual=(raw_analytic(ee,dd,params,responses)-raw_analytic(ee,-dd,params,responses)+raw_analytic(-ee,dd,params,responses)-raw_analytic(-ee,-dd,params,responses)-2*(raw_analytic(mp.mpf(0),dd,params,responses)-raw_analytic(mp.mpf(0),-dd,params,responses)))/(4*dd*ee*ee)
            error=float(abs(actual-expected)/max(mp.mpf(1),abs(expected)));errors.append(error)
            rows.append({"e":step,"d":step,"mixed_coefficient":str(actual),"symbolic_coefficient":str(expected),"normalized_error":error})
        checks.add(f"generic_jet_{index}_full_analytic_mixed_variation",errors[-1]<=1e-5 and all(errors[i+1]<errors[i] or max(errors[i+1],errors[i])<=1e-12 for i in range(2)),errors,"last<=1e-5; decrease or <=1e-12 floor")
        records.append({"params":{k:str(v) for k,v in params.items()},"response_jets":{k:list(map(str,v)) for k,v in responses.items()},"rows":rows})
    return records


def calculate():
    mp.mp.dps=50
    parent=common.read_json(BASE+"r4c1_g3n3_attempt_02/summary.json")
    pins=dict(parent["source_sha256"]);pins.update(PINS);pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins);checks=common.Checks()
    checks.add("all_source_pins_and_available_sidecars_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(missing),"known_absent":missing})
    formulas,total,symbols,R,Rt,Rz=derive(checks)
    force=force_controls(checks)
    print("Checking independent unexpanded analytic mixed variations...",flush=True)
    controls=independent(checks,total,symbols,R,Rt,Rz)
    inherited=common.read_json(BASE+"r4c1_g3n3_attempt_02/response.json")
    checks.add("original_G3_and_N3_failures_retained",len(inherited["inherited_failed_parent_checks"])==1 and len(inherited["superseded_attempt_01_failed_checks"])==2)
    checks.add("all_source_pins_and_available_sidecars_after",common.inspect_pins(pins)==missing)
    payloads={"formulas.json":common.encode(formulas),"force.json":common.encode(force),"independent.json":common.encode({"mp_digits":50,"generic_jets":controls,"inherited_failed_parent_checks":inherited["inherited_failed_parent_checks"],"superseded_N3_attempt_01_failed_checks":inherited["superseded_attempt_01_failed_checks"]})}
    passed=sum(row["passed"] for row in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3n4-coupled-source-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS","passed":passed,"total":len(checks.rows),"checks":checks.rows,
             "status":"UNIT_CONSTRAINED_SECOND_ORDER_SOURCE_LEDGER_CHECKED_RESPONSE_SOLUTION_OPEN" if ok else "COUPLED_SOURCE_LEDGER_REQUIRES_DISPOSITION",
             "response_fields":list(FIELD_NAMES),"source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],"artifacts":{k:common.sha(v) for k,v in payloads.items()},"inherited_sidecars_absent":missing,
             "coupled_plane_wave_sources_verified":ok,"full_second_order_response_solved":False,"full_nonlinear_classical_evolution_verified":False,"physical_reduced_Hessian_verified":False,"physical_EFT_cutoff_derived":False,
             "canonical_tests_1_to_3":"HOLD_SUBSTANTIVE","physics_pass":False,"Rule9_cleared":False,"gate_effect":"NONE","review_status":"DEFERRED",
             "MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
             "review_dependencies":["R9-MT1-G3N3","R9-MT1-G3V","all inherited scientific and review debt"],"runtime":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__,"mp_decimal_digits":mp.mp.dps}}
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--output",default=BASE+"r4c1_g3n4_attempt_01");parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
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
