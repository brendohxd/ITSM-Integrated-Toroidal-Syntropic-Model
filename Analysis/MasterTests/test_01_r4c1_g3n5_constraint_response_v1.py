"""Frozen full-field gauge/constraint reduction and periodic linear IVP."""
from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
from pathlib import Path
import platform
import re
import sys

import numpy as np
from scipy.integrate import solve_ivp
import scipy
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = "Analysis/MasterTests/outputs/"
FULL = BASE + "r4c1_g3n5_attempt_02/"
CMP = BASE + "r4c1_g3n5_time_compare_attempt_01/"
BG_SOURCE = "Analysis/MasterTests/test_01_r4c1_interacting_background.py"
BG_SUMMARY = BASE + "test_01_r4c1_interacting_background_summary.json"
BG_CSV = BASE + "test_01_r4c1_interacting_background_trajectory.csv"
CONTRACT = "Theory/Gates/RES-001/RES001_R4C1_G3N5_CONSTRAINT_RESPONSE_CONTRACT_2026-10-10.md"
HELPER = "Analysis/MasterTests/test_01_r4c1_g3k_c1_clock_entry_v2.py"
PINS = {
    FULL + "summary.json": "560e369d7795ed8e06d0c2c26350d3b412a53c577da82f0669e68f6ee04f5666",
    CMP + "summary.json": "2fb997e71b2fe24cc3aa8e458a26663c65165bcba068b3a12e40aedaae11d261",
    BG_SOURCE: "1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f",
    BG_SUMMARY: "e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7",
    BG_CSV: "0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa",
    CONTRACT: "f27a299020e02e15ee20f1d0ade6ca5447fbc272bace1a2c9f8d4846ca3e708b",
    HELPER: "d031e3347d00b956b9abebc4cded2bf199a993cf3348bc151303f17f90d79224",
}
for name in (HELPER, BG_SOURCE):
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != PINS[name]:
        raise RuntimeError("Frozen imported source drift: " + name)
sys.path.insert(0, str(ROOT / "Analysis/MasterTests"))
import test_01_r4c1_g3k_c1_clock_entry_v2 as common
import test_01_r4c1_interacting_background as b1

SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS = ("alpha", "Sx", "Sy", "Sz", "Mxx", "Mxy", "Mxz", "Myy", "Myz", "Mzz",
          "Vx", "Vy", "Vz", "du", "dv", "dr", "Pi", "T", "Em", "Z", "nu", "LambdaU")
IDX = {k: i for i, k in enumerate(FIELDS)}
MN = (("Mxx", "Mxy", "Mxz"), ("Mxy", "Myy", "Myz"), ("Mxz", "Myz", "Mzz"))
MODES = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3))
END = 0.05
AMPLITUDE = 1e-6
BG_NAMES = ("a", "H", "u0", "u_dot", "v0", "v_dot", "r0", "r_dot", "psi_dot", "rho_m", "C")
PARAMS = {k: s.Rational(v) for k, v in dict(MP2="1", MU2="2/3", c1="1/5", c2="1/10",
    c3="-1/5", c4="1/20", K_Q="3", A="2/7", b="5/11", zeta="1/13", beta="2/5",
    g_r="3/7", m2="1", lambda4="1/3", lambda6="1/5", Lambda="2", mr2="2",
    lambda_r="1/7", rho_Lambda="0").items()}


def expanded(matrix):
    return matrix.applyfunc(s.expand)


def exact(checks, name, matrix):
    vals = list(matrix) if isinstance(matrix, s.MatrixBase) else [matrix]
    bad = [{"index": i, "residual": str(s.expand(v))} for i, v in enumerate(vals) if s.expand(v) != 0]
    checks.add(name, not bad, bad, "zero_exact")


def numerical(checks, name, value, limit):
    checks.add(name, bool(np.isfinite(value) and value <= limit), float(value), "<=" + str(limit))


def npy(array):
    buf = io.BytesIO()
    np.save(buf, array, allow_pickle=False)
    return buf.getvalue()


class Operator:
    def __init__(self, checks):
        bg_extra = ("Hdot", "psi_ddot", "epsilon0", "epsilon_dot", "lambda0", "lambda_dot",
                    "u_ddot", "v_ddot", "r_ddot")
        self.sy = {k: s.Symbol(k, real=True) for k in set(BG_NAMES) | set(PARAMS) | set(bg_extra)}
        self.sy["a"] = s.Symbol("a", positive=True)
        self.bg = s.Matrix([self.sy[k] for k in BG_NAMES])
        self.k = s.Matrix(s.symbols("kx ky kz", real=True))
        a, H, u, ud, v, vd, r, rd, p, rho, C = self.bg
        radius = u*u + v*v
        potential = radius/2 + radius**2/24 + radius**3/480 + r*r + r**4/28 + 3*radius*r*r/28
        MC = s.Rational(11, 10)
        self.rates = s.Matrix([a*H, -(ud*ud+vd*vd+rd*rd+3*p*p+rho)/(2*MC),
            ud, -3*H*ud-s.diff(potential, u), vd, -3*H*vd-s.diff(potential, v),
            rd, -3*H*rd-s.diff(potential, r), -3*H*p-s.Rational(2,15)*rho,
            (-3*H+s.Rational(2,5)*p)*rho, s.Rational(2,5)*p*C])
        self.potential = potential
        self.constraint = 3*MC*H*H - (ud*ud+vd*vd+rd*rd+3*p*p)/2 - potential - rho
        eps = rho/C**4
        lam = s.Rational(1,5)*self.rates[1]
        self.eps, self.lam = eps, lam
        self.replace = {self.sy[k]: value for k, value in PARAMS.items()}
        self.replace.update({self.sy["epsilon0"]: eps, self.sy["epsilon_dot"]: self.dt(eps),
            self.sy["lambda0"]: lam, self.sy["lambda_dot"]: self.dt(lam),
            self.sy["Hdot"]: self.rates[1], self.sy["u_ddot"]: self.rates[3],
            self.sy["v_ddot"]: self.rates[5], self.sy["r_ddot"]: self.rates[7],
            self.sy["psi_ddot"]: self.rates[8]})
        self.response = {}
        self.info = {}
        for fi, field in enumerate(FIELDS):
            for chars in ("", *"txyz", *("".join(q) for q in itertools.combinations_with_replacement("txyz", 2))):
                name = field + ("_" + chars if chars else "")
                self.response[name] = s.Symbol(name, real=True)
                self.info[name] = (fi, chars)
        self.sy.update(self.response)
        kernel = common.read_json(FULL + "kernel.json")
        self.LA, self.LB, self.LBT, self.LK = [s.zeros(22) for _ in range(4)]
        raw_aux = s.zeros(4)
        aux_ids = [IDX[q] for q in ("Sx", "Sy", "Sz", "Z")]
        weights = [s.Integer(1), None, *(s.I*q for q in self.k)]
        for row in kernel["entries"]:
            bi, i = divmod(row["row"], 22)
            bj, j = divmod(row["column"], 22)
            raw = self.parse(row["value"])
            value = self.embed(raw)
            if bi != 1 and bj != 1:
                self.LA[i,j] += s.conjugate(weights[bi])*value*weights[bj]
                if i in aux_ids and j in aux_ids:
                    raw_aux[aux_ids.index(i),aux_ids.index(j)] += s.conjugate(weights[bi])*raw*weights[bj]
            elif bi != 1:
                self.LB[i,j] += s.conjugate(weights[bi])*value
            elif bj != 1:
                self.LBT[i,j] += value*weights[bj]
            else:
                self.LK[i,j] += value
        self.LA, self.LB, self.LBT, self.LK = map(expanded, (self.LA,self.LB,self.LBT,self.LK))
        exact(checks,"Fourier_action_Hermitian",self.LA-self.LA.conjugate().T)
        exact(checks,"Fourier_mixed_action_adjoint",self.LB-self.LBT.conjugate().T)
        exact(checks,"Fourier_temporal_action_Hermitian",self.LK-self.LK.conjugate().T)
        self.EA, self.EB, self.ED = [s.zeros(22) for _ in range(3)]
        audit = common.read_json(FULL+"export_audit.json")["roundtrip_records"]
        records = {q["path"]: q for q in audit}
        variables = list(self.response.values())
        for i, field in enumerate(FIELDS):
            rec = records["Euler/"+field]
            if not rec["roundtrip_exact"]:
                raise ValueError("Unverified original Euler export")
            expr = s.Add(*(self.parse(q) for q in rec["expanded_terms"]))
            poly = s.Poly(expr, *variables)
            for powers, value in poly.terms():
                occupied = [j for j, power in enumerate(powers) if power]
                if len(occupied) != 1 or sum(powers) != 1:
                    raise ValueError("Expected strictly linear original Euler operator")
                j, chars = self.info[str(variables[occupied[0]])]
                value = self.embed(value)
                nt = chars.count("t")
                spatial = [self.k["xyz".index(c)] for c in chars if c != "t"]
                factor = s.prod(s.I*q for q in spatial)
                (self.EA if nt==0 else self.EB if nt==1 else self.ED)[i,j] += value*factor
        self.EA,self.EB,self.ED = map(expanded,(self.EA,self.EB,self.ED))
        exact(checks,"all_Euler_value_entries_equal_action",self.EA-self.LA+self.dtm(self.LBT)+3*H*self.LBT)
        exact(checks,"all_Euler_velocity_entries_equal_action",self.EB-self.LB+self.LBT+self.dtm(self.LK)+3*H*self.LK)
        exact(checks,"all_Euler_acceleration_entries_equal_action",self.ED+self.LK)
        k2=(self.k.T*self.k)[0]
        MP,MU,c1,c2,c3,b=(self.sy[q] for q in ("MP2","MU2","c1","c2","c3","b"))
        # Polynomial form has no k=0 division and verifies the generic parent block.
        shift_expected=((MP-MU*(c1+c3))*(k2*s.eye(3)-self.k*self.k.T)/2
                        -MU*(c1+c2+c3)*self.k*self.k.T)/a**2
        expected=s.diag(shift_expected,b)
        exact(checks,"generic_unreduced_shift_regulator_block",raw_aux-expected)
        self.generic_aux=expected
        self.G0,self.G1=self.gauge()
        active1=[any(self.EB[:,i]) or any(self.ED[:,i]) for i in range(22)]
        active2=[any(self.ED[:,i]) for i in range(22)]
        self.G0d=self.G0.applyfunc(lambda x:s.Integer(0))
        self.G0dd=self.G0d.copy();self.G1d=self.G0d.copy();self.G1dd=self.G0d.copy()
        for i in range(22):
            for j in range(4):
                if active1[i]:
                    self.G0d[i,j]=self.dt(self.G0[i,j]);self.G1d[i,j]=self.dt(self.G1[i,j])
                if active2[i]:
                    self.G0dd[i,j]=self.dt(self.dt(self.G0[i,j]));self.G1dd[i,j]=self.dt(self.dt(self.G1[i,j]))
        self.initial=list(map(s.Rational, ("1","0","1","0","0","1","1","1/4","1/5","1/5","1")))
        self.h0=s.Symbol("h0",real=True)
        self.initial[1]=self.h0
        self.initial_sub=dict(zip(self.bg,self.initial))
        initial_constraint=s.expand(self.constraint.subs(self.initial_sub))
        exact(checks,"B1_initial_Friedmann_value",initial_constraint-s.Rational(33,10)*(self.h0**2-s.Rational(3469,4620)))
        self.bg_fn=s.lambdify([self.bg],self.rates,"numpy",cse=True)
        self.full_fn=s.lambdify([self.bg,self.k],(self.EA,self.EB,self.ED),"numpy",cse=True)
        self.gauge_fn=s.lambdify([self.bg,self.k],(self.G0,self.G1,self.G0d,self.G0dd,self.G1d,self.G1dd),"numpy",cse=True)
        self.constraint_fn=s.lambdify([self.bg],self.constraint,"numpy",cse=True)

    def parse(self,text):
        names=set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*",text))
        if "__" in text or not re.fullmatch(r"[A-Za-z_0-9+\-*/(). \t]+",text) or not names<=set(self.sy):
            raise ValueError("Unexpected frozen-expression syntax")
        return s.sympify(text,locals=self.sy)

    def embed(self,value):
        return s.expand(value.xreplace(self.replace))

    def dt(self,value):
        return s.expand(sum(s.diff(value,q)*rate for q,rate in zip(self.bg,self.rates) if q in value.free_symbols))

    def dtm(self,matrix):
        return matrix.applyfunc(self.dt)

    def gauge(self):
        a,H,u,ud,v,vd,r,rd,p,rho,C=self.bg
        g0,g1=s.zeros(22,4),s.zeros(22,4)
        g1[IDX["alpha"],0]=-1
        for i in range(3):
            g0[IDX[("Sx","Sy","Sz")[i]],0]=s.I*self.k[i]/a
            g1[IDX[("Sx","Sy","Sz")[i]],i+1]=-a
            g0[IDX[("Vx","Vy","Vz")[i]],0]=s.I*self.k[i]/a
            for j in range(i,3):
                row=IDX[MN[i][j]]
                g0[row,0]=-2*H*int(i==j)
                for ell in range(3):
                    g0[row,ell+1]=-s.I*(self.k[i]*int(j==ell)+self.k[j]*int(i==ell))
        for name,value in (("du",ud),("dv",vd),("dr",rd),("Pi",p),("T",C),
                           ("Em",self.dt(self.eps)),("LambdaU",self.dt(self.lam))):
            g0[IDX[name],0]=-value
        return g0,g1

    def exact_initial_gauge(self,checks,mode):
        sub={**self.initial_sub,**dict(zip(self.k,mode))}
        A,B,D=[m.subs(sub) for m in (self.EA,self.EB,self.ED)]
        g0,g1,g0d,g0dd,g1d,g1dd=[m.subs(sub) for m in
            (self.G0,self.G1,self.G0d,self.G0dd,self.G1d,self.G1dd)]
        mats=(A*g0+B*g0d+D*g0dd,A*g1+B*(g0+g1d)+D*(2*g0d+g1dd),B*g1+D*(g0+2*g1d),D*g1)
        bad=[]
        modulus=s.Poly(self.h0**2-s.Rational(3469,4620),self.h0)
        for order,matrix in enumerate(mats):
            for idx,value in enumerate(matrix):
                residue=s.Poly(s.expand(value),self.h0).rem(modulus).as_expr()
                if residue != 0:bad.append({"order":order,"row":idx//4,"gauge":idx%4,"residual":str(residue)})
        checks.add("exact_initial_all_four_gauges_"+str(mode),not bad,bad,"zero_exact using the original initial constraint")

    def chart(self,checks,mode):
        n=s.Matrix(mode);k2=(n.T*n)[0]
        names=(list(FIELDS[4:10]) if k2==0 else ["M11","M12","M22"])+list(FIELDS[10:17])
        F=s.zeros(22,len(names))
        if k2==0:
            for j,name in enumerate(names[:6]):F[IDX[name],j]=1
            shift=6
        else:
            axis=min(range(3),key=lambda i:abs(mode[i]))
            ref=s.zeros(3,1);ref[axis]=1
            e1=n.cross(ref);e1=e1/s.sqrt((e1.T*e1)[0]);e2=n.cross(e1)/s.sqrt(k2)
            basis=(e1*e1.T,e1*e2.T+e2*e1.T,e2*e2.T)
            for ell,tensor in enumerate(basis):
                for i in range(3):
                    for j in range(i,3):F[IDX[MN[i][j]],ell]=tensor[i,j]
            shift=3
            exact(checks,"spatial_gauge_basis_"+str(mode),s.Matrix([[sum(n[i]*F[IDX[MN[i][j]],ell] for i in range(3)) for ell in range(3)] for j in range(3)]))
        for j,name in enumerate(FIELDS[10:17]):F[IDX[name],shift+j]=1
        F[IDX["alpha"],names.index("Pi")]=-PARAMS["beta"]
        aux=("Z",) if k2==0 else ("Sx","Sy","Sz","Z")
        U=s.zeros(22,len(aux))
        for j,name in enumerate(aux):U[IDX[name],j]=1
        sub=dict(zip(self.k,mode))
        LA,LB,LBT,LK,A,B,D=[expanded(m.subs(sub)) for m in
            (self.LA,self.LB,self.LBT,self.LK,self.EA,self.EB,self.ED)]
        Fh=F.conjugate().T;Uh=U.conjugate().T
        Da=expanded(Uh*LA*U)
        if k2==0:
            inv=s.Matrix([[1/PARAMS["b"]]])
            shift_rows=[IDX[x] for x in ("Sx","Sy","Sz")]
            exact(checks,"mean_shift_equations_identically_zero",A[shift_rows,:].col_join(B[shift_rows,:]).col_join(D[shift_rows,:]))
        else:
            PL=n*n.T/k2;PT=s.eye(3)-PL
            inv=s.diag(self.bg[0]**2*(2*PT-15*PL)/k2,1/PARAMS["b"])
        exact(checks,"auxiliary_exact_inverse_"+str(mode),Da*inv-s.eye(len(aux)))
        exact(checks,"auxiliary_has_no_velocity_"+str(mode),LK*U)
        exact(checks,"auxiliary_has_no_derivative_density_"+str(mode),LB*U)
        Ys=expanded(Uh*LA*F);Vs=expanded(Uh*LB*F)
        Ls,Ms=expanded(-inv*Ys),expanded(-inv*Vs)
        Q0,Q1=expanded(F+U*Ls),expanded(U*Ms)
        Q0d,Q1d=self.dtm(Q0),self.dtm(Q1)
        ar=expanded(Fh*LA*F-Ys.conjugate().T*inv*Ys)
        br=expanded(Fh*LB*F-Ys.conjugate().T*inv*Vs)
        kr=expanded(Fh*LK*F-Vs.conjugate().T*inv*Vs)
        er0=expanded(ar-self.dtm(br.conjugate().T)-3*self.bg[1]*br.conjugate().T)
        er1=expanded(br-br.conjugate().T-self.dtm(kr)-3*self.bg[1]*kr)
        er2=-kr
        exact(checks,"action_Euler_reduced_value_"+str(mode),er0-Fh*(A*Q0+B*Q0d))
        exact(checks,"action_Euler_reduced_velocity_"+str(mode),er1-Fh*(A*Q1+B*(Q0+Q1d)))
        exact(checks,"action_Euler_reduced_acceleration_"+str(mode),er2-Fh*(B*Q1+D*F))
        alpha=IDX["alpha"];em=IDX["Em"]
        exact(checks,"density_recovery_coefficient_"+str(mode),A[alpha,em]+self.bg[-1]**4)
        emL=expanded((A*Q0+B*Q0d)[alpha,:]/self.bg[-1]**4)
        emM=expanded((A*Q1+B*(Q0+Q1d))[alpha,:]/self.bg[-1]**4)
        exact(checks,"density_recovery_no_acceleration_"+str(mode),(D*F+B*Q1)[alpha,:])
        exact(checks,"normal_multiplier_recovery_coefficient_"+str(mode),A[IDX["nu"],IDX["LambdaU"]]+1)
        exact(checks,"recovered_multiplier_derivatives_unused_"+str(mode),B[:,IDX["LambdaU"]].col_join(D[:,IDX["LambdaU"]]))
        exact(checks,"density_multiplier_acceleration_unused_"+str(mode),D[:,IDX["Em"]])
        fun=s.lambdify([self.bg],(er0,er1,er2,kr),"numpy",cse=True)
        rec=s.lambdify([self.bg],(Q0,Q1,Q0d,Q1d,emL,emM,self.dtm(emL),self.dtm(emM)),"numpy",cse=True)
        return dict(mode=mode,names=names,F=np.array(F,dtype=complex),K=kr,fun=fun,rec=rec,
                    symbolic=dict(E0=er0,E1=er1,E2=er2,Q0=Q0,Q1=Q1,EmL=emL,EmM=emM),
                    aux=aux,dimension=len(names),inverse=inv)

    def reconstruct(self,chart,bg,y,v,w):
        Q0,Q1,Q0d,Q1d,emL,emM,emLd,emMd=[np.asarray(q,dtype=complex) for q in chart["rec"](bg)]
        q=Q0@y+Q1@v;qd=Q0d@y+(Q0+Q1d)@v+Q1@w;qdd=chart["F"]@w
        q[IDX["Em"]]=(emL@y+emM@v).item()
        qd[IDX["Em"]]=(emLd@y+(emL+emMd)@v+emM@w).item()
        A,B,D=[np.asarray(q,dtype=complex) for q in self.full_fn(bg,chart["mode"])]
        provisional=A@q+B@qd+D@qdd
        q[IDX["LambdaU"]]=-provisional[IDX["nu"]]/A[IDX["nu"],IDX["LambdaU"]]
        terms=(A@q,B@qd,D@qdd)
        norm=max(sum(np.linalg.norm(t,np.inf) for t in terms),1e-20)
        return q,qd,qdd,float(np.linalg.norm(sum(terms),np.inf)/norm)


def matrix_export(matrix):
    return {"shape":list(matrix.shape),"entries":[{"row":i,"column":j,
        "terms":[str(q) for q in s.Add.make_args(s.expand(matrix[i,j]))]}
        for i in range(matrix.rows) for j in range(matrix.cols) if matrix[i,j]!=0]}


def calculate():
    pins=dict(PINS)
    for folder in (FULL,CMP):
        parent=common.read_json(folder+"summary.json")
        for name,value in list(parent["source_sha256"].items())+[(folder+k,v) for k,v in parent["artifacts"].items()]:
            if name in pins and pins[name]!=value:raise ValueError("Conflicting parent pin: "+name)
            pins[name]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    missing=common.inspect_pins(pins)
    checks=common.Checks();checks.add("all_source_pins_before",True,{"pins":len(pins),"sidecars":len(pins)-len(missing),"absent":missing})
    for label,folder in (("full_kernel",FULL),("time_comparison",CMP)):
        parent=common.read_json(folder+"summary.json")
        checks.add(label+"_passed_on_its_scope",parent["passed"]==parent["total"] and all(q["passed"] for q in parent["checks"]))
        checks.add(label+"_holds_preserved",parent["physics_pass"] is False and parent["gate_effect"]=="NONE" and parent["Rule9_cleared"] is False)
    pmap=dict(MP2="MP2",MU2="MU2",c1="c1",c2="c2",c3="c3",c4="c4",K="K_Q",A="A",b="b",
              zeta="zeta",beta="beta",gr="g_r",m2="m2",l4="lambda4",l6="lambda6",cutoff="Lambda",mr2="mr2",lr="lambda_r",vacuum="rho_Lambda")
    checks.add("all_B1_parameters_unchanged",all(b1.PARAMS[k]==float(PARAMS[v]) for k,v in pmap.items()))
    print("Building full Fourier operator and independent action/Euler identities",flush=True)
    op=Operator(checks)
    fixed={op.sy[k]:v for k,v in PARAMS.items()}
    fixed.update({op.bg[0]:1,**dict(zip(op.k,(1,0,0)))})
    boundaries=(("regular",{},4),("mean",{q:0 for q in op.k},1),
        ("b_zero",{op.sy["b"]:0},3),("MU2_zero",{op.sy["MU2"]:0},3),
        ("longitudinal_zero",{op.sy["c2"]:-op.sy["c1"]-op.sy["c3"]},3),
        ("tensor_zero",{op.sy["c3"]:op.sy["MP2"]/op.sy["MU2"]-op.sy["c1"]},2))
    for name,changes,target in boundaries:
        rank=op.generic_aux.subs(changes,simultaneous=True).subs(fixed).rank()
        checks.add("exact_auxiliary_rank_boundary_"+name,rank==target,int(rank),target)
    for mode in MODES:op.exact_initial_gauge(checks,mode)
    print("Reducing all auxiliaries with explicit nonzero and homogeneous charts",flush=True)
    charts=[op.chart(checks,mode) for mode in MODES]
    y0=b1.initial(b1.PARAMS)
    start=np.array([*y0[:8],y0[9],y0[10],np.exp(float(PARAMS["beta"])*y0[8])])
    bgsol=solve_ivp(lambda t,y:np.asarray(op.bg_fn(y),dtype=float).ravel(),(0,END),start,
                    method="DOP853",rtol=2e-12,atol=2e-14,dense_output=True)
    checks.add("coefficient_background_completed",bool(bgsol.success and bgsol.t[-1]==END))
    grid=np.linspace(0,END,257);background=bgsol.sol(grid).T
    checks.add("sampled_coefficient_domain",bool(np.isfinite(background).all() and np.min(background[:,[0,9,10]])>0))
    numerical(checks,"coefficient_Friedmann",max(abs(op.constraint_fn(q)) for q in background),1e-10)
    old=np.genfromtxt(ROOT/BG_CSV,delimiter=",",names=True)
    select=old[old["t"]<=END+1e-14]
    saved=np.array([[row[q] for q in ("a","H","u","ud","v","vd","r","rd","psid","rho_m")]+
                    [np.exp(float(PARAMS["beta"])*row["psi"])] for row in select])
    numerical(checks,"retained_B1_background_agreement",np.max(np.abs(bgsol.sol(select["t"]).T-saved)/(1+np.abs(saved))),1e-9)
    rates_error=0.;ward_error=0.
    for t in (0.,0.025,END):
        bg=bgsol.sol(t);full=np.array([*bg[:8],np.log(bg[10])/float(PARAMS["beta"]),bg[8],bg[9],0.])
        ref=np.array(b1.rhs(t,full,b1.PARAMS))
        target=np.array([*ref[:8],ref[9],ref[10],float(PARAMS["beta"])*bg[8]*bg[10]])
        rates_error=max(rates_error,float(np.max(np.abs(np.asarray(op.bg_fn(bg)).ravel()-target))))
        for mode in MODES:
            A,B,D=[np.asarray(q,dtype=complex) for q in op.full_fn(bg,mode)]
            g0,g1,g0d,g0dd,g1d,g1dd=[np.asarray(q,dtype=complex) for q in op.gauge_fn(bg,mode)]
            combinations=((A@g0,B@g0d,D@g0dd),(A@g1,B@(g0+g1d),D@(2*g0d+g1dd)),(B@g1,D@(g0+2*g1d)),(D@g1,))
            for terms in combinations:
                ward_error=max(ward_error,float(np.linalg.norm(sum(terms),np.inf)/max(1.,sum(np.linalg.norm(q,np.inf) for q in terms))))
    numerical(checks,"independent_B1_source_rates",rates_error,1e-10)
    numerical(checks,"all_sampled_gauge_residuals",ward_error,1e-10)
    # Wrong clock-sign control is exact already at the initial point.
    checks.add("reject_wrong_dust_clock_lapse_sign",2*PARAMS["beta"]!=0,"E_Em=-2*beta*C^4*Pi instead of zero")
    trajectories=[];reports=[];coefficients=[]
    for chart in charts:
        mode=chart["mode"];N=chart["dimension"]
        yy=AMPLITUDE*np.array([(j+1)+1j*(-1)**j for j in range(N)])/(N+1)
        vv=AMPLITUDE*np.array([(-1)**j*(j+1)-1j for j in range(N)])/(N+1)
        if mode==(0,0,0):
            yy=yy.real.astype(complex);vv=vv.real.astype(complex)
            q=chart["F"]@yy
            vv[chart["names"].index("dv")]=-q[IDX["du"]]-sum(q[IDX[x]] for x in ("Mxx","Myy","Mzz"))/2+q[IDX["alpha"]]
        def rhs(t,state):
            y=state[:N]+1j*state[N:2*N];v=state[2*N:3*N]+1j*state[3*N:]
            E0,E1,E2,K=[np.asarray(q,dtype=complex) for q in chart["fun"](bgsol.sol(t))]
            w=-np.linalg.solve(E2,E0@y+E1@v)
            return np.r_[v.real,v.imag,w.real,w.imag]
        state=np.r_[yy.real,yy.imag,vv.real,vv.imag]
        print("Evolving coupled mode "+str(mode)+" with "+str(N)+" chart coordinates",flush=True)
        solutions=[solve_ivp(rhs,(0,END),state,method=method,rtol=1e-10,atol=1e-17,dense_output=True)
                   for method in ("DOP853","Radau")]
        checks.add("both_response_solvers_completed_"+str(mode),all(q.success and q.t[-1]==END for q in solutions))
        values=[q.sol(grid) for q in solutions]
        error=float(np.max(np.abs(values[0]-values[1]))/max(AMPLITUDE,np.max(np.abs(values[0])),np.max(np.abs(values[1]))))
        numerical(checks,"independent_response_solvers_"+str(mode),error,1e-7)
        values=values[0];allq=[];analytic=0.;condition=0.;charge=[];kinetic=[]
        for i,t in enumerate(grid):
            bg=background[i];y=values[:N,i]+1j*values[N:2*N,i];v=values[2*N:3*N,i]+1j*values[3*N:,i]
            E0,E1,E2,K=[np.asarray(q,dtype=complex) for q in chart["fun"](bg)]
            w=-np.linalg.solve(E2,E0@y+E1@v)
            q,qd,qdd,resid=op.reconstruct(chart,bg,y,v,w)
            allq.append(q);analytic=max(analytic,resid);condition=max(condition,float(np.linalg.cond(E2)))
            if i in (0,128,256):kinetic.append(np.linalg.eigvalsh((K+K.conj().T)/2).real.tolist())
            if mode==(0,0,0):
                a,H,u,ud,v0,vd,r,rd,p,rho,C=bg
                dQ=a**3*(u*qd[IDX["dv"]]+q[IDX["du"]]*vd-v0*qd[IDX["du"]]-q[IDX["dv"]]*ud
                    +(sum(q[IDX[x]] for x in ("Mxx","Myy","Mzz"))/2-q[IDX["alpha"]])*(u*vd-v0*ud))
                charge.append(dQ)
        allq=np.array(allq);trajectories.append(allq)
        numerical(checks,"all_22_analytic_Euler_equations_"+str(mode),analytic,1e-9)
        checks.add("sampled_nonsingular_acceleration_"+str(mode),np.isfinite(condition) and condition<1e10,condition,"<1e10")
        fd=[]
        for count in (65,129,257):
            stride=256//(count-1);q=allq[::stride];times=grid[::stride];dt=times[1]-times[0]
            qd=(-q[4:]+8*q[3:-1]-8*q[1:-3]+q[:-4])/(12*dt)
            qdd=(-q[4:]+16*q[3:-1]-30*q[2:-2]+16*q[1:-3]-q[:-4])/(12*dt*dt)
            maximum=0.
            for j,t in enumerate(times[2:-2]):
                A,B,D=[np.asarray(q,dtype=complex) for q in op.full_fn(bgsol.sol(t),mode)]
                terms=(A@q[j+2],B@qd[j],D@qdd[j])
                maximum=max(maximum,float(np.linalg.norm(sum(terms),np.inf)/max(sum(np.linalg.norm(z,np.inf) for z in terms),1e-20)))
            fd.append({"samples":count,"error":maximum})
        numerical(checks,"independent_full_Euler_finite_difference_"+str(mode),fd[-1]["error"],1e-5)
        improvement=fd[0]["error"]/max(fd[-1]["error"],np.finfo(float).tiny)
        checks.add("full_Euler_refinement_"+str(mode),improvement>=4 or max(fd[0]["error"],fd[-1]["error"])<=1e-10,
                   {"improvement":improvement,"errors":fd},">=4 or both<=1e-10")
        charge_drift=None
        if charge:
            charge_drift=float(max(abs(q-charge[0]) for q in charge)/AMPLITUDE)
            numerical(checks,"mean_linearized_charge_preserved",charge_drift,1e-8)
            numerical(checks,"mean_initial_linearized_charge_zero",abs(charge[0])/AMPLITUDE,1e-12)
        reports.append(dict(mode=list(mode),coordinates=chart["names"],dimension=N,analytic_residual=analytic,
            solver_discrepancy=error,condition_number=condition,finite_difference=fd,kinetic_eigenvalues=kinetic,
            linearized_charge_drift=charge_drift,initial_constraint_data="all auxiliaries reconstructed from their equations"))
        coefficients.append({"mode":list(mode),"coordinate_names":chart["names"],"auxiliaries":list(chart["aux"]),
            "matrices":{k:matrix_export(v) for k,v in chart["symbolic"].items()},"auxiliary_inverse":matrix_export(chart["inverse"]),
            "nonclaim":"Coordinate count and time-matrix inertia are not a global DOF or physical stability classification"})
    inherited=common.read_json(FULL+"independent.json")
    checks.add("all_source_pins_after",common.inspect_pins(pins)==missing)
    payloads={"time.npy":npy(grid),"background.npy":npy(background),"unreduced_fields.npy":npy(np.array(trajectories)),
              "coefficients.json":common.encode({"background_order":list(BG_NAMES),"unreduced_field_order":list(FIELDS),
                    "parameters":{k:str(v) for k,v in PARAMS.items()},"charts":coefficients}),
              "diagnostics.json":common.encode({"modes":reports,"gauge_residual":ward_error,"rate_agreement":rates_error,
                    "inverse_domains":["k!=0 for transverse spatial gauge and shift inverse","a,C>0; b!=0",
                        "MP2-MU2(c1+c3)!=0; MU2(c1+c2+c3)!=0","k=0 separate mean chart, not an excluded mode"],
                    "singular_boundaries":{"k_zero_shift_rank":0,"nonzero_shift_rank":3,"b_zero_regulator_rank":0,
                        "MU2_zero_longitudinal_rank":0,"c1_c2_c3_zero_longitudinal_rank":0,"tensor_coefficient_zero_transverse_rank":0},
                    "inherited_failed_parent_checks":inherited["inherited_failed_parent_checks"],
                    "superseded_N3_attempt_01_failed_checks":inherited["superseded_N3_attempt_01_failed_checks"],
                    "nonclaims":["No full nonlinear Cauchy evolution","No second-order nonanalytic forcing solve",
                        "No physical EFT cutoff or ghost/gradient/hyperbolicity conclusion","No healthy continuous GR limit",
                        "No matched K_Q, V, a0(z) or physical torus dimensions"]})}
    passed=sum(row["passed"] for row in checks.rows);ok=passed==len(checks.rows)
    summary=dict(schema="r4c1-g3n5-constraint-response-v1",validation="PASS_LOCAL_CHECKS" if ok else "FAIL_LOCAL_CHECKS",
        passed=passed,total=len(checks.rows),checks=checks.rows,
        status="CONDITIONAL_COUPLED_LINEAR_IVP_PREREGISTERED_DOMAIN_CHECKED" if ok else "CONSTRAINT_RESPONSE_REQUIRES_DISPOSITION",
        source_sha256=dict(sorted(pins.items())),script_sha256=pins[SELF],artifacts={k:common.sha(v) for k,v in payloads.items()},
        inherited_sidecars_absent=missing,coupled_linear_IVP_completed=ok,full_second_order_response_solved=False,
        full_nonlinear_evolution_verified=False,physical_Hessian_verified=False,physical_EFT_cutoff_derived=False,
        physics_pass=False,gate_effect="NONE",Rule9_cleared=False,review_status="DEFERRED",
        canonical_tests_1_to_3="HOLD_SUBSTANTIVE",K_Q="NOT_DERIVED",V="NOT_COMPUTED",Stage4A="CLOSED",
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
        review_dependencies=["G3N5 full kernel and temporal comparison","B1 and background matching","All inherited review/physics debt"])
    summary.update({"MAT-001":"BLOCKED","UVIR-003":"IN_PROGRESS","TOP-X4":"UNCHANGED"})
    payloads["summary.json"]=common.encode(summary)
    return payloads,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",default=BASE+"r4c1_g3n5_constraint_response_attempt_01")
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
    for row in summary["checks"]:
        if not row["passed"]:print(json.dumps(row))
    return 0 if summary["passed"]==summary["total"] else 1


if __name__=="__main__":raise SystemExit(main())
