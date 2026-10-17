"""V3: exact univariate Laurent extraction; unchanged evolution equations."""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from math import isqrt
from pathlib import Path
import platform
import re

import numpy as np
import sympy as s

import test_01_r4c1_three_family_finite_k_v3 as parent

ev=parent.ev
ROOT=ev.ROOT
BASE=ev.BASE
PARENT=BASE+'r4c1_three_family_finite_k_attempt_04/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_WEIGHTED_EVOLUTION_V1_CONTRACT_2026-10-17.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FINITE_K_V3_REPORT_2026-10-16.md'
PINS={PARENT+'summary.json':'f94d85d36539097867490f0ce84a656267a56ec61acc170d55a873f2a69a614f',
      REPORT:'8a2e062802551615a3774168693a478d5e658a49f91dfe2a9d8e6dbadb245311',
      CONTRACT:'d327500774dc6dbcbbae5dd8120bf8b97f173f269a40c8cf1dcd4ab35d3220dd',
      'Analysis/MasterTests/test_01_r4c1_g3n5_dust_uniform_propagator_v2.py':'bda5fcb42e6fec850093075d681c712972b951fc08107f3f70eed52420898ca3'}
CLEAN=lambda q:s.factor_terms(s.expand(q))
ON=lambda m:m.applyfunc(CLEAN)
NORM=lambda m:float(np.linalg.norm(m,np.inf))


ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_WEIGHTED_EVOLUTION_V2_COMPUTE_ADDENDUM_2026-10-17.md'
PINS.update({
    ADDENDUM:'4b1b224eb0664549fa98cdfaec654dae078107b178657babcf31097578f5888c',
    'Analysis/MasterTests/test_01_r4c1_three_family_weighted_evolution_v1.py':'c4fa921d5724bf7d045c9a525d2392f2066ee96befda65aaf742a8cf43594beb',
    BASE+'r4c1_three_family_weighted_evolution_attempt_01/interrupted_by_runner.json':'9c72dec75260e2c76350a1b0ab6be6901eb3b10f03931cc019a52370d47064d2',
    BASE+'r4c1_three_family_weighted_evolution_attempt_02/interrupted_by_runner.json':'f8463d6158e59fdd05db72e33d5dd1abcb952129718b27b6904e7cf03c8190c9'})


LAURENT_ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_WEIGHTED_EVOLUTION_V3_LAURENT_ADDENDUM_2026-10-17.md'
PINS.update({
    LAURENT_ADDENDUM:'afca99d85397151732879a87fe93416a1b325c4e3dc9a65ed1dcec77db512673',
    'Analysis/MasterTests/test_01_r4c1_three_family_weighted_evolution_v2.py':'7c2b68a0bebd03e062616a420cdd52625d45bf872e39c977b540ea64057164b5',
    BASE+'r4c1_three_family_weighted_evolution_attempt_03/interrupted.json':'c23b5745fa580d0c8a54e1fcf054a4ddf7da7bacdb00ecca1be6368340239b92'})


class Checks(parent.Checks):
    def exact(self,name,value):
        values=list(value) if isinstance(value,(list,tuple,s.MatrixBase)) else [value]
        bad=[]
        for i,q in enumerate(values):
            numerator=s.expand(s.together(q).as_numer_denom()[0])
            if numerator!=0:bad.append(dict(index=i,residual=str(numerator)))
        self.add(name,not bad,bad,'exact expanded rational numerator zero on declared regular domain')


def implementation_controls(ch):
    import ast
    old=ast.parse((ROOT/'Analysis/MasterTests/test_01_r4c1_three_family_weighted_evolution_v1.py').read_text())
    new=ast.parse((ROOT/SELF).read_text())
    for name in ('Derivation','RationalBox'):
        a=next(n for n in old.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name)
        b=next(n for n in new.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name)
        ch.add('unchanged_scientific_AST_'+name,ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False))
    z=s.Symbol('zero_control',real=True)
    examples=[(z*z-1)/(z-1)-z-1,(s.sqrt(2)*z)**2-2*z*z,1/z-2/(2*z)]
    for i,q in enumerate(examples):ch.exact('rational_zero_checker_control_'+str(i),q)
    probe=Checks();probe.exact('nonzero',examples[0]+1/(z*z+1))
    ch.add('zero_checker_rejects_nonzero_rational_perturbation',not probe.rows[0]['passed'])

    ell=s.Symbol('ell_control',positive=True)
    a=s.Symbol('a_control',positive=True)
    q=ell**2+1/(ell**2*a+2*ell**2*a)
    parsed=laurent(s.Matrix([[q]]),ell)
    ch.exact('laurent_unfactored_monomial_control',parsed[2][0,0]-1)
    ch.exact('laurent_negative_power_retained_control',parsed[-2][0,0]-1/(3*a))
    rejected=False
    try:laurent(s.Matrix([[1/(1+ell)]]),ell)
    except ValueError:rejected=True
    ch.add('reject_genuine_non_Laurent_denominator',rejected)



def inputs():
    ps=ev.READ(PARENT+'summary.json')
    pins=dict(ps['source_sha256'])
    pins.update({PARENT+n:h for n,h in ps['artifacts'].items()})
    pins.update(PINS)
    pins[SELF]=ev.SHA((ROOT/SELF).read_bytes())
    paths=[]
    absent=ps['inherited_sidecars_absent']
    for n,h in pins.items():
        p=ROOT/n
        if ev.SHA(p.read_bytes())!=h:raise RuntimeError('Frozen source drift '+n)
        paths.append(p)
        side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=h:raise RuntimeError('Sidecar drift '+n)
            paths.append(side)
        elif n not in absent:raise RuntimeError('Required sidecar absent '+n)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    import test_01_r4c1_gr_family_survey_v2 as generic
    import test_01_r4c1_three_family_response_entry_v2 as prior
    import test_01_r4c1_three_family_time_response_v2 as time
    return pins,absent,snapshot,generic,prior,time


class RationalBox:
    """Exact outward real intervals; irrational root endpoints rounded out."""
    def __init__(self,box):self.box=box

    @lru_cache(maxsize=None)
    def at(self,q):
        if q.is_Rational:return q,q
        if q in self.box:return self.box[q]
        if q.is_Add:
            vals=[self.at(a) for a in q.args]
            return sum(a for a,b in vals),sum(b for a,b in vals)
        if q.is_Mul:
            lo=hi=s.Integer(1)
            for arg in q.args:
                a,b=self.at(arg)
                vals=(lo*a,lo*b,hi*a,hi*b)
                lo,hi=min(vals),max(vals)
            return lo,hi
        if q.is_Pow:
            a,b=self.at(q.base)
            n=q.exp
            if n.is_Integer:
                if n<0:
                    lo,hi=self.at(q.base**(-n))
                    if lo<=0<=hi:raise ZeroDivisionError('Interval denominator '+str(q))
                    return 1/hi,1/lo
                vals=[a**n,b**n]
                if n%2==0 and a<=0<=b:vals.append(s.Integer(0))
                return min(vals),max(vals)
            if n==s.Rational(1,2):
                if a<0:raise ValueError('Negative root interval')
                scale=10**18
                floor=lambda v:s.Rational(isqrt(int(s.floor(v*scale**2))),scale)
                return floor(a),floor(b)+s.Rational(1,scale)
        raise ValueError('Unsupported real interval '+str(q))

    def absolute(self,q):
        real,imag=s.expand_complex(q).as_real_imag()
        return sum(max(abs(v) for v in self.at(CLEAN(part))) for part in (real,imag))


def laurent(matrix,ell):
    out={}
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            for term in s.Add.make_args(s.expand(matrix[i,j])):
                if term==0:continue
                num,den=s.fraction(term)
                dp=s.Poly(den,ell,domain='EX')
                if len(dp.terms())!=1:raise ValueError('Nonmonomial Laurent denominator at '+str((i,j))+': '+str(den))
                (degree,),coefficient=dp.terms()[0]
                for (power,),value in s.Poly(num,ell,domain='EX').terms():
                    coeff=CLEAN(value/coefficient)
                    if ell in coeff.free_symbols:raise ValueError('ell in Laurent coefficient')
                    out.setdefault(int(power-degree),s.zeros(matrix.rows,matrix.cols))[i,j]+=coeff
            rebuilt=sum((m[i,j]*ell**power for power,m in out.items()),s.Integer(0))
            numerator=s.expand(s.together(matrix[i,j]-rebuilt).as_numer_denom()[0])
            if numerator!=0:raise ValueError('Exact Laurent reconstruction failed at '+str((i,j)))
    return {k:ON(v) for k,v in out.items()}


class Derivation:
    def __init__(self,ch):
        print('Parse accepted unspecialized full finite-k action',flush=True)
        wire=ev.READ(PARENT+'formulas.json')
        texts=' '.join(e for key in ('A','R','K') for row in wire[key]['entries'] for e in row)
        names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',texts))-{'I','sqrt'}
        names.update(('rho','eta','p'))
        x={n:s.Symbol(n,positive=True) if n in ('a','ell','eta','p','C') else s.Symbol(n,real=True) for n in names}
        self.x=x
        loc={**x,'I':s.I,'sqrt':s.sqrt}
        load=lambda key:s.Matrix([[s.sympify(q,locals=loc) for q in row] for row in wire[key]['entries']])
        O=s.Matrix([[s.sympify(q,locals=loc) for q in row] for row in wire['SO2_map']['entries']])
        self.O20=s.diag(O,O)
        a,ell=x['a'],x['ell']
        H,u,ud,v,vd,r,rd,pd,rho,C=(x[n] for n in ('H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho','C'))
        MP=x['MP2'];MU=x['MU2'];f2=MU*(x['c1']+x['c4'])
        MC=MP+MU*(x['c1']+3*x['c2']+x['c3'])/2
        rad=u*u+v*v
        potential=x['m2']*rad/2+x['lambda4']*rad**2/8+x['lambda6']*rad**3/(24*x['Lambda']**2)
        potential+=x['mr2']*r*r/2+x['lambda_r']*r**4/4+x['g_r']*rad*r*r/4+x['rho_Lambda']
        kinetic=ud*ud+vd*vd+rd*rd+x['K_Q']*pd*pd
        self.bg=s.Matrix([a,H,u,ud,v,vd,r,rd,pd,rho,C])
        self.rates=s.Matrix([a*H,-(kinetic+rho)/(2*MC),ud,-3*H*ud-s.diff(potential,u),
            vd,-3*H*vd-s.diff(potential,v),rd,-3*H*rd-s.diff(potential,r),
            -3*H*pd-x['beta']*rho/x['K_Q'],(-3*H+x['beta']*pd)*rho,x['beta']*pd*C])
        self.potential=potential;self.energy=kinetic/2+potential+rho;self.MC=MC
        self.constraint=3*MC*H*H-self.energy
        self.dt=lambda m:m.applyfunc(lambda q:CLEAN(sum(s.diff(q,z)*rate for z,rate in zip(self.bg,self.rates) if z in q.free_symbols)))
        ch.exact('generic_background_energy_balance',self.dt(s.Matrix([self.energy]))[0]+3*H*(kinetic+rho))
        ch.exact('generic_background_constraint_preserved',self.dt(s.Matrix([self.constraint]))[0])
        ch.exact('generic_dust_charge_preserved',self.dt(s.Matrix([a**3*rho/C]))[0])
        self.A,self.R,self.K=[ON((O.T*load(key)*O).subs(x['epsilon0'],rho/C**4)) for key in ('A','R','K')]
        Ki=s.diag(*(1/self.K[i,i] for i in range(10)))
        ch.exact('complete_generic_kinetic_inverse',self.K*Ki-s.eye(10))
        G=s.zeros(20);G[:10,10:]=s.eye(10)
        G[10:,:10]=ON(Ki*(self.A-self.dt(self.R)-3*H*self.R))
        G[10:,10:]=ON(Ki*(self.R.conjugate().T-self.R-self.dt(self.K)-3*H*self.K))
        self.G=G
        print('Derive invertible mixed-order balance and retain its drift',flush=True)
        B=s.eye(20);Bi=s.eye(20)
        for i in range(10):
            if i not in (3,9):B[i,i]=ell/a;Bi[i,i]=a/ell
        B[9,9]=ell**2/a**2;B[9,3]=-s.I*ell*pd/a
        Bi[9,9]=a*a/ell**2;Bi[9,3]=s.I*a*pd/ell
        B[19,13]=-s.I*a*pd/ell;Bi[19,13]=s.I*a*pd/ell
        ch.exact('mixed_balance_exact_inverse',B*Bi-s.eye(20))
        self.B,self.Bi=B,Bi;self.Bd=self.dt(B)
        blocks=laurent(ON((self.Bd+B*G)*Bi),ell)
        self.blocks=blocks
        ch.add('all_balance_powers_retained',set(blocks).issubset({-2,-1,0,1,2}),sorted(blocks))
        F,L=blocks[2],blocks[1]
        fast=(9,19);rest=[i for i in range(20) if i not in fast]
        Ff=F.extract(fast,fast)
        ch.exact('dispersive_block_exact',Ff-s.Matrix([[0,1/a**2],[-x['b']/(x['K_Q']*a*a),0]]))
        residual=F.copy()
        for i in fast:
            for j in fast:residual[i,j]=0
        ch.exact('degree_two_only_retained_dispersive_pair',residual)
        off=s.zeros(20);Ld=L.copy();U=s.zeros(20);Ffi=Ff.inv()
        for i in rest:
            for j in fast:off[i,j]=L[i,j];Ld[i,j]=0
        for i in fast:
            for j in rest:off[i,j]=L[i,j];Ld[i,j]=0
        upper=ON(off.extract(rest,fast)*Ffi);lower=ON(-Ffi*off.extract(fast,rest))
        for i,ii in enumerate(rest):
            for j,jj in enumerate(fast):U[ii,jj]=upper[i,j]
        for i,ii in enumerate(fast):
            for j,jj in enumerate(rest):U[ii,jj]=lower[i,j]
        U=ON(U);g=CLEAN(s.trace(U*U)/2)
        ch.exact('generic_fast_cross_commutator',F*U-U*F+off)
        ch.exact('generic_fast_cubic_inverse_identity',U**3-g*U)
        ch.exact('generic_fast_denominator_sign_binding',g+a*a*x['beta']**2*f2/x['b'])
        self.U,self.Ud,self.g=U,self.dt(U),g
        print('Derive generic wave/dust coordinates, not B1 substitution',flush=True)
        cs=s.sympify(wire['scalar_c2'],locals=loc)
        ct=s.sympify(wire['tensor_c2'],locals=loc)
        cv=s.sympify(wire['vector_c2'],locals=loc)
        kh=self.K[0,0]
        d=s.I*MP/(s.sqrt(2)*f2);c=s.I*MP/(s.sqrt(2)*kh*cs)
        e=CLEAN(-a*Ld[10,3]/cs)
        Tw=s.eye(20);Ti=s.eye(20)
        Tw[13,:]=s.eye(20)[13,:]+d*s.eye(20)[0,:]
        Tw[0,:]=s.eye(20)[0,:]+c*Tw[13,:]+e*s.eye(20)[3,:]
        Ti[0,:]=s.eye(20)[0,:]-c*s.eye(20)[13,:]-e*s.eye(20)[3,:]
        Ti[13,:]=s.eye(20)[13,:]-d*Ti[0,:]
        Gm=s.Matrix([[1+x['zeta']*v*v,-x['zeta']*u*v,0],[-x['zeta']*u*v,1+x['zeta']*u*u,0],[0,0,1]])
        matter_shift=ON(-a*Gm.inv()*Ld.extract([16,17,18],[3]))
        for i in range(3):Tw[6+i,3]=matter_shift[i];Ti[6+i,3]=-matter_shift[i]
        Tw,Ti=ON(Tw),ON(Ti)
        ch.exact('generic_wave_map_inverse',Tw*Ti-s.eye(20))
        self.Tw,self.Ti,self.Twd=Tw,Ti,self.dt(Tw)
        Fw,Lw=ON(Tw*F*Ti),ON(Tw*Ld*Ti)
        Q=s.eye(20);Q[0,0]=cs;Q[1,1]=Q[2,2]=ct;Q[4,4]=Q[5,5]=cv;Q[9,9]=x['b']/x['K_Q']
        Q[6:9,6:9]=Gm
        self.Q,self.Qd=Q,self.dt(Q)
        ch.exact('complete_dispersive_positive_power_Q_skew',Q*Fw+Fw.conjugate().T*Q)
        ch.exact('complete_wave_positive_power_Q_skew',Q*Lw+Lw.conjugate().T*Q)
        ch.exact('slow_coordinates_no_order_ell_rows',Lw.extract([3,13],range(20)))
        rank=s.zeros(20);rank[6:8,6:8]=x['zeta']*s.Matrix([v,-u])*s.Matrix([[v,-u]])
        D=Q-rank
        ch.exact('Q_positive_diagonal_plus_positive_rank_one',D-s.diag(*D.diagonal()))
        self.D=D
        M0,M1,M2=(blocks.get(i,s.zeros(20)) for i in (0,-1,-2))
        ns=[ON(L*U-U*Ld+M0),ON(M0*U+M1-self.Ud),ON(M1*U+M2),ON(M2*U)]
        # Coefficientwise exact verification avoids a large monolithic expansion.
        pre={}
        def add(k,m):pre[k]=pre.get(k,s.zeros(20))+m
        for k,m in blocks.items():add(k,m);add(k-1,m*U)
        add(2,-F);add(1,-Ld-U*F);add(0,-U*Ld);add(-1,-self.Ud)
        for k,m in pre.items():ch.exact('complete_fast_remainder_power_'+str(k),m-(ns[-k] if -3<=k<=0 else s.zeros(20)))
        invpoly=[s.eye(20),-U,U*U-g*s.eye(20)]
        Nj=[]
        for j in range(6):
            Nj.append(ON(Tw*sum((invpoly[k]*ns[j-k] for k in range(3) if 0<=j-k<4),s.zeros(20))*Ti))
            print('Full nonpositive remainder coefficient',j,'retained',flush=True)
        self.F,self.L,self.N,self.drift=Fw,Lw,Nj,ON(self.Twd*Ti)
        self.S0=ON(self.Qd+Q*self.drift+self.drift.conjugate().T*Q)
        self.Sj=[ON(Q*n+n.conjugate().T*Q) for n in Nj]
        ch.add('reject_omitted_mixed_basis_drift',any(z!=0 for z in self.Bd))
        ch.add('reject_omitted_fast_map_drift',any(z!=0 for z in self.Ud))
        ch.add('reject_omitted_wave_map_drift',any(z!=0 for z in self.Twd))
        ch.add('reject_omitted_complete_remainder',any(z!=0 for n in Nj for z in n))
        ch.add('quartic_pair_not_deleted',self.F[9,19]!=0 and self.F[19,9]!=0)
        self.eta=x['eta'];self.family={}
        for name,fam in ev.READ(ev.PLANAR)['families'].items():
            sub={x[n]:s.sympify(val,locals={'eta':self.eta}) for n,val in fam['parameter_map'].items() if n in x}
            # Same scalar potential as the pinned background executable, and
            # the g_r=3*eta/7 choice already used by the immutable CUSP3 runs.
            sub.update({x[n]:val for n,val in dict(m2=s.Integer(1),lambda4=s.Rational(1,3),
                lambda6=s.Rational(1,5),Lambda=s.Integer(2),mr2=s.Integer(2),lambda_r=s.Rational(1,7),
                rho_Lambda=s.Integer(0),g_r=3*self.eta/7).items()})
            self.family[name]=sub
            for label,val in dict(kinetic_trace=kh,tensor=ct,vector=cv,scalar=cs,quartic=x['b']/x['K_Q'],f2=f2,b=x['b']).items():
                ok,proof=parent.interval_positive(CLEAN(val.subs(sub)),self.eta)
                ch.add(name+'_regular_positive_'+label,ok,proof)
            for i in (0,1,4,9):
                ok,proof=parent.interval_positive(CLEAN((D[i,i]-s.Rational(1,10)).subs(sub)),self.eta)
                ch.add(name+'_Q_lower_one_tenth_'+str(i),ok,proof)

    def bounds(self,ch):
        x=self.x;eta=self.eta
        a,H,u,ud,v,vd,r,rd,pd,rho,C=self.bg
        eta_cases=(s.Rational(1,4),s.Rational(1,64),s.Rational(1,1024))
        results=[]
        for name,sub in self.family.items():
            initial={a:1,u:s.sqrt(eta),ud:0,v:0,vd:s.sqrt(eta),r:s.sqrt(eta),rd:s.sqrt(eta)/4,pd:eta/5,rho:s.Rational(1,5),C:1}
            E0=CLEAN(self.energy.subs(sub).subs(initial));MC=CLEAN(self.MC.subs(sub))
            for label,expr in dict(energy_below_one=1-E0,H_initial_above_quarter=16*E0-3*MC,MC_positive=MC).items():
                ok,proof=parent.interval_positive(CLEAN(expr),eta);ch.add(name+'_background_'+label,ok,proof)
            # With Hdot=-3H^2+(V+rho/2)/MC, positive potential/rho prevent
            # H from crossing zero and give H>=H0/(1+3H0*t)>1/5.
            ch.exact(name+'_H_lower_differential_comparison',
                (self.rates[1]+3*H*H-(self.potential+rho/2+self.constraint)/self.MC).subs(sub))
            positive_potential=s.Poly(self.potential.subs(sub),u,v,r)
            ch.add(name+'_potential_nonnegative',all(coef.is_nonnegative and all(k%2==0 for k in powers) for powers,coef in positive_potential.terms()))
            # Rational endpoint inequalities used in the analytic bootstrap.
            ch.add(name+'_positive_clock_bootstrap',s.Rational(1,5)-s.Rational(2,15)*(s.Rational(20,19))**3/20>(s.Rational(20,19))**3/10)
            ch.add(name+'_rho_lower_bootstrap',s.Rational(1,5)*(s.Rational(19,20))**3>s.Rational(1,6))
            ch.add(name+'_rho_upper_bootstrap',s.Rational(1,5)*s.Rational(250,249)<s.Rational(1,4))
            ch.add(name+'_C_upper_bootstrap',s.Rational(16000,15999)<s.Rational(250,249))
            for value in eta_cases:
                print('Exact rational full-state energy box',name,str(value),flush=True)
                fixed={q:CLEAN(e.subs(eta,value)) for q,e in sub.items()}
                box={a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(1,5),s.Integer(1)),
                    **{z:(s.Integer(-2),s.Integer(2)) for z in (u,ud,v,vd,r,rd)},
                    pd:(value/10,value/5),rho:(s.Rational(1,6),s.Rational(1,4)),C:(s.Integer(1),s.Rational(250,249))}
                bx=RationalBox(box)
                energy=[ON(m.subs(fixed)) for m in [self.S0,*self.Sj]]
                rows=[]
                for i in range(20):
                    rows.append(CLEAN(10*(sum(bx.absolute(energy[0][i,j]) for j in range(20))+
                        sum(sum(bx.absolute(energy[k+1][i,j]) for j in range(20))/4**k for k in range(6)))))
                mu=max([s.Integer(0),*rows])
                ch.add(name+'_'+str(value)+'_exact_finite_energy_constant',all(q.is_Rational for q in rows) and mu>=0)
                results.append(dict(family=name,eta_exact=str(value),energy_row_bounds=list(map(str,rows)),mu_exact=str(mu),
                    mu_display=float(mu),endpoint_log_amplification_upper=float(mu/40),
                    background_box={str(k):list(map(str,pair)) for k,pair in box.items()},initial_energy=str(E0.subs(eta,value))))
        return dict(cases=results,ell_min=4,time_domain='0<=s<=t<=1/20',eta_scope='three registered fixed eta values; not eta=0 or a uniform GR limit',
            inequality='sqrt(E(t))<=exp(mu*(t-s)/2)*sqrt(E(s))',E='w^dagger*Q(t)*w',Q_lower='I/10',
            exact_continuous_time_box_proof='E0<1, V>=0; E_dot=-3H*(kinetic+rho), Hdot=-3H^2+(V+rho/2)/MC on shell; '
                'H0>1/4, H0<1, 1<=a<=exp(1/20)<=20/19, |u,v,r,ud,vd,rd|<2; '
                'a^3*pd=eta/5-(2*eta/15)*integral(a^3*rho), rho<=E0<1 gives eta/10<pd<=eta/5; '
                'C<=exp(1/16000)<=16000/15999<250/249; rho=C/(5*a^3) stays in (1/6,1/4).',
            energy_bound_proof='Q>=I/10. All positive-power Q-symmetric terms cancel exactly. '
                '1-g/ell^2>=1; ell>=4. Exact outward intervals and Hermitian absolute-row bounds on '
                'Q_dot+Q*drift+drift.H*Q and every (Q*N_j+N_j.H*Q)/ell^j give E_dot<=mu*E.',
            physical_energy_positive=False,nonlinear_or_interaction_window=False)

    def numeric(self,ch,g,prior,time,bounds):
        x=self.x;ell=x['ell']
        mats=[self.B,self.Bi,self.Bd,self.U,self.Ud,self.Tw,self.Ti,self.Twd,self.Q,self.Qd,self.F,self.L,self.drift,*self.N]
        symbols=sorted(set().union(*(m.free_symbols for m in mats)),key=str)
        fn=s.lambdify([symbols],mats+[s.Matrix([[self.g]])],'numpy',cse=True)
        red=time.EvolvingReduction(prior,g)
        O=np.asarray(self.O20,complex)
        limits={(r['family'],r['eta_exact']):r for r in bounds['cases']}
        records=[]
        for ir,run in enumerate(ev.READ(parent.PARENT+'trajectories.json')['runs']):
            eta=s.Rational(run['eta_exact']);p=g.bg.PARAMS.copy()
            for n,e in ev.READ(ev.PLANAR)['families'][run['family']]['parameter_map'].items():
                p['K' if n=='K_Q' else n]=float(s.sympify(e).subs(s.Symbol('eta'),eta))
            p['gr']=float(3*eta/7)
            print('Independent full-action weighted controls',ir,run['family'],str(eta),flush=True)
            maxima={k:0. for k in ('inverse','generator','energy','auxiliary','box','energy_majorant')}
            witnesses={k:0. for k in ('balance_drift','wave_drift','remainder')}
            bound=limits[(run['family'],run['eta_exact'])]
            for it,bfull in enumerate(run['first_order_states']):
                b=np.asarray(bfull[:12],float)
                raw=dict(zip(red.op.kernel.order,red.op.kernel.values(b,p)))
                raw['rho']=b[10]
                for z,pair in bound['background_box'].items():
                    value=raw[z];lo,hi=map(lambda q:float(s.Rational(q)),pair)
                    maxima['box']=max(maxima['box'],lo-value,value-hi,0.)
                for mode in (4,80):
                    raw['ell']=mode
                    vals=[np.asarray(m,complex) for m in fn([raw[str(z)] for z in symbols])]
                    B,Bi,Bd,U,Ud,Tw,Ti,Twd,Q,Qd,F,L,drift=vals[:13]
                    Ns=vals[13:19];gg=float(vals[19][0,0].real)
                    tf=np.eye(20)+U/mode;den=1-gg/mode**2
                    tfi=np.eye(20)-U/(mode*den)+U@U/(mode**2*den)
                    data=red.at(b,p,mode,np.zeros(22),np.zeros(4));G=data['G']
                    ac=(Bd+B@O.conj().T@G@O)@Bi
                    exact=(Twd+Tw@tfi@(ac@tf-Ud/mode))@Ti
                    residual=drift+sum((n/mode**k for k,n in enumerate(Ns)),np.zeros((20,20),complex))/den
                    factored=mode**2*F+mode*L+residual
                    err=NORM(exact-factored)/(1+NORM(exact)+NORM(factored))
                    M=Tw@tfi@B@O.conj().T
                    Md=(Twd@tfi@B-Tw@tfi@(Ud/mode)@tfi@B+Tw@tfi@Bd)@O.conj().T
                    P=M.conj().T@Q@M
                    Pd=Md.conj().T@Q@M+M.conj().T@Qd@M+M.conj().T@Q@Md
                    lhs=Pd+G.conj().T@P+P@G
                    rhs=M.conj().T@(Qd+factored.conj().T@Q+Q@factored)@M
                    en=NORM(lhs-rhs)/(1+NORM(lhs)+NORM(rhs))
                    rec=red.reconstruct(data,np.linspace(.01,.2,20)*(1+.1j),p)
                    inverse=max(NORM(B@Bi-np.eye(20)),NORM(Tw@Ti-np.eye(20)),NORM(tf@tfi-np.eye(20)))
                    sym=Qd+Q@residual+residual.conj().T@Q
                    majorant=float(np.max(np.linalg.eigvalsh(sym-float(s.Rational(bound['mu_exact']))*Q)))
                    maxima['generator']=max(maxima['generator'],err);maxima['energy']=max(maxima['energy'],en)
                    maxima['inverse']=max(maxima['inverse'],inverse);maxima['auxiliary']=max(maxima['auxiliary'],rec['error'])
                    maxima['energy_majorant']=max(maxima['energy_majorant'],majorant,0.)
                    witnesses['balance_drift']=max(witnesses['balance_drift'],NORM(Tw@tfi@Bd@Bi@tf@Ti)/(1+NORM(exact)))
                    witnesses['wave_drift']=max(witnesses['wave_drift'],NORM(drift)/(1+NORM(exact)))
                    witnesses['remainder']=max(witnesses['remainder'],NORM(residual)/(1+NORM(exact)))
                    records.append(dict(run=ir,node=it,ell=mode,generator=err,energy_derivative=en,auxiliary=rec['error'],inverse=inverse,
                        Q_eigenvalue_min=float(np.min(np.linalg.eigvalsh(Q))),energy_majorant_violation=max(0.,majorant)))
            for key,val in maxima.items():ch.small(str(ir)+'_all_nodes_'+key,val,1e-9)
            for key,val in witnesses.items():ch.add(str(ir)+'_reject_omitted_'+key,val>1e-12,val,'>1e-12')
        return dict(records=records,independent_full_action_reducer=True,new_integrations=False,
            archived_nodes_are_not_continuous_time_certification=True)

    def export(self):
        matrices={n:parent.MAT(m) for n,m in dict(B=self.B,B_inverse=self.Bi,B_dot=self.Bd,U=self.U,U_dot=self.Ud,
            Tw=self.Tw,Tw_inverse=self.Ti,Tw_dot=self.Twd,Q=self.Q,Q_dot=self.Qd,F=self.F,L=self.L,drift=self.drift,
            **{'N'+str(i):m for i,m in enumerate(self.N)}).items()}
        return dict(matrices=matrices,g=str(self.g),state='w=Tw*(I+U/ell)^(-1)*B*SO2^dagger*(y,y_dot)',
            complete_generator='ell^2*F+ell*L+drift+sum(N_j/ell^j)/(1-g/ell^2)',
            full_generic_action_source=PARENT+'formulas.json',all_20_states_retained=True,
            zero_mode_excluded=True,positive_norm_not_canonical_energy=True)


def calculate():
    pins,absent,snapshot,g,prior,time=inputs();before=snapshot();ch=Checks()
    implementation_controls(ch)
    der=Derivation(ch)
    good=lambda:all(r['passed'] for r in ch.rows)
    bounds=der.bounds(ch) if good() else dict(skipped='Exact identity prerequisite failed')
    numbers=der.numeric(ch,g,prior,time,bounds) if good() else dict(skipped='Exact/bound prerequisite failed')
    ch.add('source_sidecar_hash_size_mtime_preserved',before==snapshot())
    passed=sum(r['passed'] for r in ch.rows);complete=passed==len(ch.rows)
    scope=dict(claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,physics_pass=False,gate_effect='NONE',
        weighted_linear_estimate_verified=complete,canonical_energy_positive=False,ordinary_wave_Jordan_defect_removed=False,
        full_nonlinear_fixed_charge_admission=False,physical_window_admitted=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',
        K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',native_goal_resumed=False)
    bodies={'formulas.json':ev.ENCODE(der.export()),'bounds.json':ev.ENCODE(bounds),'numerics.json':ev.ENCODE(numbers),
        'verification.json':ev.ENCODE(dict(checks=ch.rows,passed=passed,total=len(ch.rows))),'scope.json':ev.ENCODE(scope)}
    summary=dict(schema='r4c1-three-family-weighted-evolution-v3',validation='PASS_LOCAL_ESTIMATE' if complete else 'FAIL_LOCAL_ESTIMATE',
        status='CONDITIONAL_FULL_STATE_WEIGHTED_LINEAR_ESTIMATE' if complete else 'WEIGHTED_ESTIMATE_UNRESOLVED',
        passed=passed,total=len(ch.rows),checks=ch.rows,**scope,source_sha256=dict(sorted(pins.items())),
        inherited_sidecars_absent=absent,source_metadata_preserved=len(before),artifacts={n:ev.SHA(b) for n,b in bodies.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        review_id='R9-MT1-THREE-FAMILY-WEIGHTED-EVOLUTION-V3',review_dependencies=['THREE-FAMILY-FINITE-K-V3',
            'CUSP3-EVOLUTION-V1','THREE-FAMILY-FIXED-CHARGE-KINETIC-V3','GENERIC-KERNEL/EVOLVING-REDUCTION','all transitive debt'])
    bodies['summary.json']=ev.ENCODE(summary)
    return bodies,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_three_family_weighted_evolution_attempt_04');ap.add_argument('--replay')
    args=ap.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse existing evidence')
    else:dest.mkdir(parents=True)
    try:bodies,summary=calculate()
    except BaseException as exc:
        if not args.replay:
            body=ev.ENCODE(dict(validation='INTERRUPTED_NO_ACCEPTED_RECEIPT',error_type=type(exc).__name__,error=str(exc),physics_pass=False))
            with (dest/'interrupted.json').open('xb') as f:f.write(body)
            with (dest/'interrupted.json.sha256').open('xb') as f:f.write((ev.SHA(body)+'  interrupted.json\n').encode())
        raise
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(ev.SHA(b)+'  '+n+'\n').encode():raise RuntimeError('Replay differs '+n)
        after=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay changed metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for n,b in bodies.items():
            with (dest/n).open('xb') as f:f.write(b)
            with (dest/(n+'.sha256')).open('xb') as f:f.write((ev.SHA(b)+'  '+n+'\n').encode())
    print(json.dumps({n:summary[n] for n in ('validation','passed','total','status','physics_pass')}),flush=True)
    for r in summary['checks']:
        if not r['passed']:print(json.dumps(r),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
