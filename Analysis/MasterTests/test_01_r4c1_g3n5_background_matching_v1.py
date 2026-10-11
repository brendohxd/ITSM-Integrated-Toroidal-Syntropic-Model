"""Full 22-field first variation and B1 background input match, not a PDE solve."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
PARENT = BASE + "r4c1_g3n4_force_attempt_01/"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
RAW = "Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v1.py"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_G3N5_BACKGROUND_MATCHING_CONTRACT_2026-10-09.md"
for name, digest in ((HELPER, "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224"),
                     (RAW, "0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7")):
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
        raise RuntimeError("Frozen dependency drift: " + name)
sys.path.insert(0, str(ROOT/"Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common
import test_01_r4c1_g3n5_response_kernel_v1 as raw

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS, MN = raw.FIELDS, raw.M_NAMES
PINS = {
    RAW: "0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7",
    CONTRACT: "bf932d7664d20abb0377c1bc1ff9c5ecf792ef157e0f8f12d0a37f55adc137ac",
    PARENT+"summary.json": "ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287",
    PARENT+"independent.json": "dcd529971dc9eac6449619fc26284f3ea18a357f6406f44e35fb93145868d45e",
    "Theory/Gates/RES-001/RES001_R4C1_G3N5_RESPONSE_KERNEL_CONTRACT_2026-10-09.md":
        "11cf25cef8cc0192f1f690dbf1f7fee2f9e0268eff508d7fb1a65709907f2c02",
    "Theory/Gates/RES-001/RES001_R4C1_G3N4_COUPLED_SOURCE_REPORT_2026-10-09.md":
        "1c7eca17f22a8e3e3ec39bb09017d05908b133f130b1f24e85f523b18af47a4b",
    "Theory/Gates/RES-001/RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md":
        "48b49fddd9066d6df783eb336e00d49374f3845ec38414ee53fe0fad812348d8",
    BASE+"test_01_r4c1_interacting_background_summary.json":
        "e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7",
    BASE+"test_01_r4c1_interacting_background_trajectory.csv":
        "0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa",
}


class First:
    """Exact dual ring modulo d^2; no second-order or full-kernel execution."""
    def __init__(self, x=0):
        self.c = x.c if isinstance(x, First) else (
            tuple(s.sympify(q) for q in x) if isinstance(x, (tuple,list))
            else (s.sympify(x), s.Integer(0)))

    def __add__(self, other):
        other = First(other)
        return First(tuple(self.c[i]+other.c[i] for i in range(2)))
    __radd__ = __add__

    def __neg__(self):
        return First(tuple(-q for q in self.c))

    def __sub__(self, other):
        return self + -First(other)

    def __rsub__(self, other):
        return First(other) + -self

    def __mul__(self, other):
        other = First(other)
        return First((self.c[0]*other.c[0], self.c[0]*other.c[1]+self.c[1]*other.c[0]))
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, First):
            raise TypeError("Explicit inverse required")
        return First(tuple(q/s.sympify(other) for q in self.c))

    def clean(self):
        return First(tuple(s.expand(q) for q in self.c))


def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))).clean()
             for j in range(len(B[0]))] for i in range(len(A))]


def trace(A):
    return sum(A[i][i] for i in range(len(A))).clean()


def contraction(v,A,w):
    return sum(v[i]*A[i][j]*w[j] for i in range(len(v)) for j in range(len(w))).clean()


def exact(checks, name, expr):
    values = list(expr) if isinstance(expr,(list,tuple,s.MatrixBase)) else [expr]
    reduced = [s.cancel(s.expand(q)) for q in values]
    ok = all(q == 0 for q in reduced)
    checks.add(name,ok,"zero_exact" if ok else list(map(str,reduced)),"zero_exact")


def derive(checks):
    a = s.Symbol("a", positive=True)
    H,Hd,p,pdd = s.symbols("H Hdot psi_dot psi_ddot", real=True)
    MP,MU,K,b,zeta,beta,C,eps,lam = s.symbols(
        "MP2 MU2 K_Q b zeta beta C epsilon0 lambda0",real=True)
    c1,c2,c3,c4 = s.symbols("c1 c2 c3 c4",real=True)
    u,v,r,ud,vd,rd,udd,vdd,rdd,epsd = s.symbols(
        "u0 v0 r0 u_dot v_dot r_dot u_ddot v_ddot r_ddot epsilon_dot",real=True)
    m2,l4,l6,cutoff,mr2,lr,portal,vacuum = s.symbols(
        "m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda",real=True)
    R = {k:s.Symbol(k,real=True) for k in FIELDS}
    D = {k:[s.Symbol(k+"_"+c,real=True) for c in "txyz"] for k in FIELDS}
    DD = {k:{(i,j):s.Symbol(k+"_"+"txyz"[i]+"txyz"[j],real=True)
             for i in range(4) for j in range(i,4)} for k in FIELDS}
    bgdt = {a:a*H,H:Hd,p:pdd,u:ud,v:vd,r:rd,ud:udd,vd:vdd,rd:rdd,
            C:beta*p*C,eps:epsd}
    maps=[]
    for i in range(4):
        mapping=dict(bgdt) if i==0 else {}
        for k in FIELDS:
            mapping[R[k]]=D[k][i]
            mapping.update({D[k][j]:DD[k][tuple(sorted((i,j)))] for j in range(4)})
        maps.append(mapping)
    def deriv(expr,i):
        return s.expand(sum(s.diff(expr,q)*dq for q,dq in maps[i].items()
                            if q in expr.free_symbols))
    def dj(obj,i):
        return First(tuple(deriv(q,i) for q in obj.c)).clean()
    d=First((0,1))
    alpha=R["alpha"]
    M=[[R[MN[i][j]] for j in range(3)] for i in range(3)]
    N,invN=1+d*alpha,First((1,-alpha))
    h=[[a*a*(int(i==j)+d*M[i][j]) for j in range(3)] for i in range(3)]
    hi=[[First((int(i==j),-M[i][j]))/(a*a) for j in range(3)] for i in range(3)]
    shifts=[d*R[k]/a for k in ("Sx","Sy","Sz")]
    velocities=[d*R[k]/a for k in ("Vx","Vy","Vz")]
    n=[invN]+[(velocities[i]-shifts[i]*invN).clean() for i in range(3)]
    U=[((1+d*R["nu"])*q).clean() for q in n]
    g=[[First(0) for j in range(4)] for i in range(4)]
    gi=[[First(0) for j in range(4)] for i in range(4)]
    g[0][0],gi[0][0]=(-N*N).clean(),First((-1,2*alpha))
    for i in range(3):
        g[0][i+1]=g[i+1][0]=(a*d*R[("Sx","Sy","Sz")[i]]).clean()
        gi[0][i+1]=gi[i+1][0]=(shifts[i]*invN*invN).clean()
        for j in range(3):
            g[i+1][j+1],gi[i+1][j+1]=h[i][j],hi[i][j]
    product=mm(g,gi)
    exact(checks,"first_order_inverse_all_directions",
          [product[i][j].c[q]-int(i==j and q==0)
           for i in range(4) for j in range(4) for q in range(2)])
    exact(checks,"first_order_normalized_frame",(contraction(n,g,n)+1).c)
    exact(checks,"raw_normal_variation_not_discarded",(contraction(U,g,U)+1+2*d*R["nu"]).c)
    Gamma=[[[sum(gi[k][l]*(dj(g[l][j],i)+dj(g[l][i],j)-dj(g[i][j],l))
                    for l in range(4)).clean()/2
             for j in range(4)] for i in range(4)] for k in range(4)]
    exact(checks,"direct_connection_metric_compatibility",
          [(dj(g[i][j],mu)-sum(Gamma[k][mu][i]*g[k][j]+Gamma[k][mu][j]*g[i][k]
                              for k in range(4))).clean().c[q]
           for mu in range(4) for i in range(4) for j in range(4) for q in range(2)])
    def nabla(vec):
        return [[(dj(vec[j],i)+sum(Gamma[j][i][k]*vec[k] for k in range(4))).clean()
                 for j in range(4)] for i in range(4)]
    DU,DN=nabla(U),nabla(n)
    accU=[sum(U[i]*DU[i][j] for i in range(4)).clean() for j in range(4)]
    accN=[sum(n[i]*DN[i][j] for i in range(4)).clean() for j in range(4)]
    invariants=[
        sum(gi[i][j]*g[k][l]*DU[i][k]*DU[j][l]
            for i in range(4) for j in range(4) for k in range(4) for l in range(4)).clean(),
        (trace(DU)*trace(DU)).clean(),trace(mm(DU,DU)),contraction(accU,g,accU)]
    trM=sum(M[i][i] for i in range(3))
    trMt=sum(D[MN[i][i]][0] for i in range(3))
    divS=sum(D[k][i] for i,k in enumerate(("Sx","Sy","Sz"),1))
    divV=sum(D[k][i] for i,k in enumerate(("Vx","Vy","Vz"),1))
    jtrace=3*H*(R["nu"]-alpha)+trMt/2+(divV-divS)/a
    expected=[First((3*H*H,2*H*jtrace)),First((9*H*H,6*H*(jtrace+D["nu"][0]))),
              First((3*H*H,2*H*jtrace)),First(0)]
    for i in range(4):
        exact(checks,f"frame_invariant_{i+1}_first_variation",
              (invariants[i]-expected[i]).clean().c)
    frame=-MU*(c1*invariants[0]+c2*invariants[1]+c3*invariants[2]-c4*invariants[3])/2
    hp=[[(gi[i][j]+n[i]*n[j]).clean() for j in range(4)] for i in range(4)]
    gp=[p+d*D["Pi"][0]]+[d*D["Pi"][i] for i in range(1,4)]
    gz=[d*D["Z"][i] for i in range(4)]
    projected=contraction(gp,hp,gp)
    exact(checks,"projected_Y_zero_to_first_order",projected.c)
    Q=sum(n[i]*gp[i] for i in range(4))
    temporal=K*Q*Q/2
    regulator=b*d*d*R["Z"]*R["Z"]/2-b*contraction(gz,hp,gp)-b*d*R["Z"]*sum(accN[i]*gp[i] for i in range(4))
    uu,vv,rr=u+d*R["du"],v+d*R["dv"],r+d*R["dr"]
    gu=[ud+d*D["du"][0]]+[d*D["du"][i] for i in range(1,4)]
    gv=[vd+d*D["dv"][0]]+[d*D["dv"][i] for i in range(1,4)]
    gr=[rd+d*D["dr"][0]]+[d*D["dr"][i] for i in range(1,4)]
    current=[(vv*gu[i]-uu*gv[i]).clean() for i in range(4)]
    align=-zeta*contraction(current,hp,current)/2
    ss=(uu*uu+vv*vv).clean()
    pot=(m2*ss/2+l4*ss*ss/8+l6*ss*ss*ss/(24*cutoff*cutoff)
         +mr2*rr*rr/2+lr*rr*rr*rr*rr/4+portal*ss*rr*rr/4+vacuum).clean()
    canonical=-(contraction(gu,gi,gu)+contraction(gv,gi,gv)+contraction(gr,gi,gr))/2-pot
    C2,C4=C*C*(1+2*beta*d*R["Pi"]),C**4*(1+4*beta*d*R["Pi"])
    gtau=[C+d*D["T"][0]]+[d*D["T"][i] for i in range(1,4)]
    dust=-(eps+d*R["Em"])*(C2*contraction(gtau,gi,gtau)+C4)/2
    multiplier=(lam+d*R["LambdaU"])*(contraction(U,g,U)+1)/2
    for label,expression in (("alignment",align),("regulator",regulator)):
        exact(checks,label+"_zero_background_first_variation",expression.clean().c)
    G3=[[[sum(hi[k][l]*(dj(h[l][j],i+1)+dj(h[l][i],j+1)-dj(h[i][j],l+1))
                for l in range(3)).clean()/2 for j in range(3)] for i in range(3)] for k in range(3)]
    shiftcov=[sum(h[i][j]*shifts[j] for j in range(3)).clean() for i in range(3)]
    Dshift=[[(dj(shiftcov[j],i+1)-sum(G3[k][i][j]*shiftcov[k] for k in range(3))).clean()
             for j in range(3)] for i in range(3)]
    extrinsic=[[(invN*(dj(h[i][j],0)-Dshift[i][j]-Dshift[j][i])).clean()/2
                for j in range(3)] for i in range(3)]
    km=mm(hi,extrinsic)
    adm=MP*(trace(mm(km,km))-trace(km)*trace(km))/2
    Ricci=[[(sum(dj(G3[k][i][j],k+1)-dj(G3[k][i][k],j+1)
                for k in range(3))).clean() for j in range(3)] for i in range(3)]
    curvature=sum(hi[i][j]*Ricci[i][j] for i in range(3) for j in range(3)).clean()
    flux=[(sum(D[MN[i][j]][j+1] for j in range(3))-sum(D[MN[j][j]][i+1] for j in range(3)))/a**2
          for i in range(3)]
    exact(checks,"linear_Ricci_explicit_spatial_divergence",
          curvature.c[1]-sum(deriv(flux[i],i+1) for i in range(3)))
    volume=1+d*(alpha+trM/2)
    sectors={name:(volume*expression).clean().c[1] for name,expression in (
        ("Einstein_ADM",adm),("spatial_Ricci",MP*curvature/2),("raw_frame",frame),
        ("canonical_potential",canonical),("temporal_force",temporal),
        ("alignment",align),("regulator",regulator),("dust",dust),("unit_multiplier",multiplier))}
    total=s.expand(sum(sectors.values()))
    pot0=pot.c[0]
    gradients=[s.diff(pot0,q) for q in (u,v,r)]
    ct=c1+3*c2+c3
    ks=ud*ud+vd*vd+rd*rd+K*p*p
    rho=eps*C**4
    linear_control=(3*MP*H*H*alpha-3*MP*H*H*trM/2-MP*H*trMt+2*MP*H*divS/a
        -3*MU*ct*H*H*R["nu"]+3*MU*ct*H*H*alpha/2-3*MU*ct*H*H*trM/4
        -MU*ct*H*trMt/2-MU*ct*H*(divV-divS)/a-3*MU*c2*H*D["nu"][0]
        +ud*D["du"][0]+vd*D["dv"][0]+rd*D["dr"][0]+K*p*D["Pi"][0]
        -(ks/2+pot0+rho)*alpha+(ks/4-pot0/2)*trM
        -sum(gradients[i]*R[k] for i,k in enumerate(("du","dv","dr")))
        -beta*rho*R["Pi"]+eps*C**3*D["T"][0]-lam*R["nu"]
        +MP*curvature.c[1]/2)
    exact(checks,"complete_22_field_linear_density_independent_formula",total-linear_control)
    def euler(density,k):
        out=s.diff(density,R[k])-deriv(s.diff(density,D[k][0]),0)-3*H*s.diff(density,D[k][0])
        out-=sum(deriv(s.diff(density,D[k][i]),i) for i in range(1,4))
        out+=sum(deriv(deriv(s.diff(density,DD[k][(i,j)]),i),j)
                 for i in range(1,4) for j in range(i,4))
        return s.expand(out)
    E={k:euler(total,k) for k in FIELDS}
    exact(checks,"periodic_linear_Ricci_all_22_Euler_operators_zero",
          [euler(sectors["spatial_Ricci"],k) for k in FIELDS])
    mc=MP+MU*ct/2
    Friedmann=3*mc*H*H-ks/2-pot0-rho
    acceleration=2*mc*Hd+ks+rho
    scalar_eq=[udd+3*H*ud+gradients[0],vdd+3*H*vd+gradients[1],rdd+3*H*rd+gradients[2]]
    psi_eq=K*(pdd+3*H*p)+beta*rho
    dust_eq=epsd+3*(H+beta*p)*eps
    normal_eq=-lam+3*MU*c2*Hd-3*MU*(c1+c3)*H*H
    expectedE={k:s.Integer(0) for k in FIELDS}
    expectedE.update({"alpha":Friedmann,"Mxx":(Friedmann+acceleration)/2,
        "Myy":(Friedmann+acceleration)/2,"Mzz":(Friedmann+acceleration)/2,
        "du":-scalar_eq[0],"dv":-scalar_eq[1],"dr":-scalar_eq[2],
        "Pi":-psi_eq,"T":-C**3*dust_eq,"nu":normal_eq})
    for k in FIELDS:
        exact(checks,"background_tadpole_matches_B1_"+k,E[k]-expectedE[k])
    # Independent raw-norm homogeneous action: vary before fixing its constraints.
    N0,sigma,tau,z,psi=s.symbols("N sigma tau z psi",real=True)
    ad,add,nd,sigd,sigdd,taud,taudd,zd,zdd,lamd=s.symbols(
        "a_dot a_ddot N_dot sigma_dot sigma_ddot tau_dot tau_ddot z_dot z_ddot lambda_dot",real=True)
    positions=[a,N0,sigma,u,v,r,psi,tau,eps,lam,z]
    speeds=[ad,nd,sigd,ud,vd,rd,p,taud,epsd,lamd,zd]
    accs=[add,s.Symbol("N_ddot",real=True),sigdd,udd,vdd,rdd,pdd,taudd,
          s.Symbol("epsilon_ddot",real=True),s.Symbol("lambda_ddot",real=True),zdd]
    dtmap=dict(zip(positions,speeds));dtmap.update(zip(speeds,accs));dtmap[C]=beta*p*C
    def partial(expr,q):
        return s.diff(expr,q)+(beta*C*s.diff(expr,C) if q==psi else 0)
    def dt(expr):
        return s.expand(sum(s.diff(expr,q)*dq for q,dq in dtmap.items() if q in expr.free_symbols))
    L=(-3*MP*a*ad*ad/N0
       -MU*a**3*((c1+c2+c3+c4*sigma*sigma)*sigd*sigd+
                 6*c2*(ad/a)*sigma*sigd+3*ct*(ad/a)**2*sigma*sigma)/(2*N0)
       +a**3*ks/(2*N0)-N0*a**3*pot0+
       a**3*eps*(C*C*taud*taud/N0-N0*C**4)/2+
       N0*a**3*lam*(1-sigma*sigma)/2+N0*a**3*b*z*z/2)
    EH={q:s.expand(partial(L,q)-dt(s.diff(L,dq))) for q,dq in zip(positions,speeds)}
    noether=sum(EH[q]*dq for q,dq in zip(positions,speeds) if q!=N0)-N0*dt(EH[N0])
    exact(checks,"raw_homogeneous_time_reparametrization_Noether_identity",noether)
    onchart={N0:1,nd:0,sigma:1,sigd:0,sigdd:0,ad:a*H,add:a*(Hd+H*H),
             z:0,zd:0,zdd:0,taud:C,taudd:beta*p*C}
    comparisons=[("alpha",N0,a**3),("Mxx",a,6*a*a),("nu",sigma,a**3),
                 ("du",u,a**3),("dv",v,a**3),("dr",r,a**3),
                 ("Pi",psi,a**3),("T",tau,a**3),("Em",eps,a**3),
                 ("LambdaU",lam,a**3),("Z",z,a**3)]
    for field,q,measure in comparisons:
        exact(checks,"independent_lapse_unfixed_variation_"+field,
              EH[q].subs(onchart,simultaneous=True)/measure-E[field])
    rhod=s.Symbol("rho_dot",real=True)
    rho_symbol=s.Symbol("rho",real=True)
    F=Friedmann.subs(rho,rho_symbol)
    A=acceleration.subs(rho,rho_symbol)
    Fdot=s.expand(deriv(F,0)+s.diff(F,rho_symbol)*rhod)
    source=psi_eq.subs(rho,rho_symbol)
    continuity=rhod+3*H*rho_symbol-beta*p*rho_symbol
    exact(checks,"Friedmann_propagation_off_shell_identity",
          Fdot-3*H*A+sum(dq*eq for dq,eq in zip((ud,vd,rd),scalar_eq))+p*source+continuity)
    rates={Hd:-(ks+rho_symbol)/(2*mc),udd:-3*H*ud-gradients[0],
           vdd:-3*H*vd-gradients[1],rdd:-3*H*rd-gradients[2],
           pdd:-3*H*p-beta*rho_symbol/K,rhod:-3*H*rho_symbol+beta*p*rho_symbol}
    exact(checks,"Friedmann_constraint_propagates_without_projection",Fdot.subs(rates,simultaneous=True))
    badpsi=dict(rates);badpsi[pdd]=-3*H*p+beta*rho_symbol/K
    baddust=dict(rates);baddust[rhod]=-3*H*rho_symbol-beta*p*rho_symbol
    mutants={"wrong_psi_source":s.cancel(s.expand(Fdot.subs(badpsi,simultaneous=True))),
             "wrong_dust_source":s.cancel(s.expand(Fdot.subs(baddust,simultaneous=True)))}
    exact(checks,"wrong_psi_source_preserved_nonzero_residual",mutants["wrong_psi_source"]+2*beta*p*rho_symbol)
    exact(checks,"wrong_dust_source_preserved_nonzero_residual",mutants["wrong_dust_source"]-2*beta*p*rho_symbol)
    checks.add("wrong_source_mutants_rejected_for_generic_nonzero_exchange",
               all(q!=0 for q in mutants.values()),{k:str(q) for k,q in mutants.items()},"beta*psi_dot*rho != 0")
    exact(checks,"K_Q_zero_endpoint_retains_algebraic_psi_condition",source.subs(K,0)-beta*rho_symbol)
    GR={MU:0,K:0,u:0,v:0,r:0,ud:0,vd:0,rd:0,beta:0}
    exact(checks,"algebraic_GR_Friedmann_endpoint_only",F.subs(GR)-(3*MP*H*H-vacuum-rho_symbol))
    exact(checks,"algebraic_GR_Raychaudhuri_endpoint_only",A.subs(GR)-(2*MP*Hd+rho_symbol))
    residual=s.expand(F.subs({beta:0,portal:0})-(3*MP*H*H-vacuum-rho_symbol))
    checks.add("zero_exchange_not_pure_GR",residual!=0,str(residual),"other sectors still gravitate")
    formulas={"scope":"All 22 first-variation tadpoles and background matching, not the quadratic kernel or full evolution",
        "sector_linear_densities_over_a3":{k:str(s.expand(q)) for k,q in sectors.items()},
        "background_Euler_over_a3":{k:str(q) for k,q in E.items()},
        "linear_Ricci_flux":list(map(str,flux)),"M_cos_squared":str(mc),
        "Friedmann_residual":str(F),"Raychaudhuri_residual":str(A),
        "Friedmann_derivative_identity":"F_dot = 3 H A - sum(q_dot S_q) - psi_dot P_psi - D_dust",
        "raw_lapse_unfixed_homogeneous_action":str(s.expand(L)),
        "raw_homogeneous_Euler":{str(k):str(q) for k,q in EH.items()},
        "raw_Noether_identity":str(s.cancel(s.expand(noether))),
        "background_rate_map":{str(k):str(s.cancel(q)) for k,q in rates.items()},
        "rate_map_domain":["a>0","C>0","M_cos_squared>0","K_Q>0"],
        "lambda_U":str(lam+normal_eq),
        "psi_K_Q_zero_unsolved_condition":str(source.subs(K,0)),
        "wrong_source_residuals":{k:str(q) for k,q in mutants.items()},
        "nonclaims":["No new on-shell trajectory","No general T3 response or evolution","No physical Hessian/stability/cutoff","No healthy continuous GR limit","No microscopic K_Q or V"]}
    quadratic_free=s.expand(total-sectors["spatial_Ricci"])
    symbols={str(q):q for q in quadratic_free.free_symbols}
    return formulas,quadratic_free,symbols,R,D


def independent(checks,linear,symbols,R,D):
    records=[]
    for index in range(2):
        params,jets=raw.numeric_inputs(index)
        substitutions={symbols[k]:s.Float(str(q),60) for k,q in params.items() if k in symbols}
        substitutions.update({R[k]:s.Float(str(jets[k][0]),60) for k in FIELDS})
        substitutions.update({D[k][i]:s.Float(str(jets[k][i+1]),60) for k in FIELDS for i in range(4)})
        target_expr=linear.subs(substitutions)
        if target_expr.free_symbols:
            raise RuntimeError("Unspecified local-density symbols: "+str(target_expr.free_symbols))
        target=mp.mpf(str(s.N(target_expr,60)))
        errors=[];rows=[]
        for step in ("0.001","0.0005","0.00025"):
            d=mp.mpf(step)
            value=(raw.raw_analytic(d,params,jets)-raw.raw_analytic(-d,params,jets))/(2*d)
            error=float(abs(value-target)/max(1,abs(value),abs(target)))
            errors.append(error)
            rows.append({"d":step,"actual":str(value),"target":str(target),"normalized_error":error})
        checks.add(f"independent_unexpanded_first_variation_{index}",
                   errors[-1]<=1e-5 and all(errors[i+1]<errors[i] or max(errors[i],errors[i+1])<=1e-12 for i in range(2)),
                   errors,"last<=1e-5; decreasing or <=1e-12 floor")
        records.append({"params":{k:str(q) for k,q in params.items()},
                        "response_jets":{k:list(map(str,q)) for k,q in jets.items()},"rows":rows})
    return records


def calculate():
    mp.mp.dps=50
    parent=common.read_json(PARENT+"summary.json")
    pins=dict(parent["source_sha256"]);pins.update(PINS)
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins)
    checks=common.Checks()
    checks.add("all_source_pins_before",True,{"pins":len(pins),"available_sidecars":len(pins)-len(missing),"known_absent":missing})
    print("Deriving direct all-direction first variation and raw background matching...",flush=True)
    formulas,linear,symbols,R,D=derive(checks)
    print("Running independent exact-unexpanded first-difference controls...",flush=True)
    controls=independent(checks,linear,symbols,R,D)
    inherited=common.read_json(PARENT+"independent.json")
    checks.add("original_G3_N3_failures_retained",
               len(inherited["inherited_failed_parent_checks"])==1 and len(inherited["superseded_N3_attempt_01_failed_checks"])==2)
    checks.add("all_source_pins_after",common.inspect_pins(pins)==missing)
    artifacts={"formulas.json":common.encode(formulas),"independent.json":common.encode(
        {"mp_digits":50,"scope":"Illustrative off-shell local first variations, not on-shell PDE solutions","jets":controls,
         "inherited_failed_parent_checks":inherited["inherited_failed_parent_checks"],
         "superseded_N3_attempt_01_failed_checks":inherited["superseded_N3_attempt_01_failed_checks"]})}
    passed=sum(row["passed"] for row in checks.rows);ok=passed==len(checks.rows)
    summary={"schema":"r4c1-g3n5-background-matching-v1","validation":"PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        "passed":passed,"total":len(checks.rows),"checks":checks.rows,
        "status":"ALL_22_BACKGROUND_TADPOLES_MATCH_B1_FULL_RESPONSE_OPEN" if ok else "BACKGROUND_MATCHING_REQUIRES_DISPOSITION",
        "response_fields":list(FIELDS),"spatial_directions":["x","y","z"],
        "source_sha256":dict(sorted(pins.items())),"script_sha256":pins[SELF],
        "artifacts":{k:common.sha(q) for k,q in artifacts.items()},"inherited_sidecars_absent":missing,
        "full_G3N5_kernel_compared":False,"new_on_shell_trajectory_verified":False,
        "full_nonlinear_evolution_verified":False,"physical_Hessian_verified":False,
        "physical_EFT_cutoff_derived":False,"healthy_continuous_GR_limit_verified":False,
        "physics_pass":False,"gate_effect":"NONE","Rule9_cleared":False,"review_status":"DEFERRED",
        "canonical_tests_1_to_3":"HOLD_SUBSTANTIVE","MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS",
        "K_Q":"NOT_DERIVED","V":"NOT_COMPUTED","Stage4A":"CLOSED","TOP-X4":"UNCHANGED",
        "review_dependencies":["R9-MT1-G3N5","R9-MT1-G3N4","B1 and all inherited scientific/review debt"],
        "runtime":{"python":platform.python_version(),"sympy":s.__version__,"mpmath":mp.__version__,"mp_decimal_digits":mp.mp.dps}}
    artifacts["summary.json"]=common.encode(summary)
    return artifacts,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_g3n5_background_match_attempt_01")
    parser.add_argument("--replay",metavar="EXISTING_OUTPUT")
    args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir(): raise FileNotFoundError("Replay destination absent")
    if not args.replay and dest.exists(): raise FileExistsError("Refuse existing scientific output")
    artifacts,summary=calculate()
    if args.replay:
        for name,data in artifacts.items():
            if (dest/name).read_bytes()!=data or (dest/(name+".sha256")).read_text()!=common.sha(data)+"  "+name+"\n":
                raise RuntimeError("Replay mismatch: "+name)
        action="READ_ONLY_REPLAY_EXACT"
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,data in artifacts.items():
            with (dest/name).open("xb") as f: f.write(data)
            with (dest/(name+".sha256")).open("xb") as f: f.write((common.sha(data)+"  "+name+"\n").encode())
        action="NEW_RECEIPTS_WRITTEN"
    print(json.dumps({"action":action,**{k:summary[k] for k in ("validation","passed","total","status","physics_pass","gate_effect","Rule9_cleared")}}))
    for row in summary["checks"]:
        if not row["passed"]: print(json.dumps(row))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":
    raise SystemExit(main())
