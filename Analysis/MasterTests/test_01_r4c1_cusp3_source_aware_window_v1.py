"""Source-aware lower/fast particular responses; no nonlinear-window admission."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s

import test_01_r4c1_cusp3_coupled_tail_v3 as parent

ROOT,BASE=parent.ROOT,parent.BASE
READ,ENCODE,SHA,CLEAN,MAT=parent.READ,parent.ENCODE,parent.SHA,parent.CLEAN,parent.MAT
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CUSP3_SOURCE_AWARE_WINDOW_V1_CONTRACT_2026-10-17.md'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
COUPLED=BASE+'r4c1_cusp3_coupled_tail_attempt_03/'
CONSTANTS=BASE+'r4c1_cusp3_coupled_constants_attempt_01/'
LINEAR=parent.LINEAR
ROOTS=parent.ROOT_AUDIT
K=40
FAST=(9,19)
PROGRESS=None


def progress(**record):
    if PROGRESS is not None:
        with PROGRESS.open('ab') as stream:stream.write(ENCODE(record))
    print(json.dumps(record,sort_keys=True),flush=True)


class Checks(parent.Checks):
    pass


def inputs():
    pins={};absent=set()
    summaries={COUPLED:'a9645d8477a2693514181be81df293360f22b37ec6574701f9b6c5898c30012c',
               CONSTANTS:'ae576de4b785e0f66bc29d4fdea01925b2113742b266ceddbf6374f28f3ec87a'}
    for base,digest in summaries.items():
        q=READ(base+'summary.json')
        if SHA((ROOT/(base+'summary.json')).read_bytes())!=digest:raise ValueError('Parent drift '+base)
        if q['passed']!=q['total']:raise ValueError('Parent incomplete '+base)
        pins.update(q['source_sha256'])
        pins.update({base+n:h for n,h in q.get('artifacts',{}).items()})
        pins[base+'summary.json']=digest
        absent.update(q['inherited_sidecars_absent'])
    pins.update({CONTRACT:'0535e0f45202e30c1ad9049f091d9a86bc88fbc2fdf2a5a7acf3e54315191b49',
        SELF:SHA((ROOT/SELF).read_bytes()),
        'Theory/Gates/RES-001/RES001_R4C1_CUSP3_COUPLED_TAIL_V3_REPORT_2026-10-17.md':
        '43cc89b62514024746108b0e735b93f9ce70d12d9143ed12d67c76e33c63cfb0'})
    paths=[]
    for name,digest in sorted(pins.items()):
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest:raise ValueError('Input drift '+name)
        paths.append(p)
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise ValueError('Sidecar drift '+name)
            paths.append(side)
        elif name not in absent:raise ValueError('Missing sidecar '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    return pins,sorted(absent),snapshot


class Case:
    def __init__(self,index,ch):
        self.index=index;self.ch=ch
        self.old=old=READ(COUPLED+'case_'+str(index).zfill(2)+'.json')
        self.linear=linear=READ(LINEAR+'case_'+str(index).zfill(2)+'.json')
        self.family=old['family'];self.eta=e=s.Rational(old['eta_exact'])
        progress(stage='LOAD_FROZEN_COUPLED_SYSTEM',index=index,family=self.family,eta=str(e))
        self.x=x={n:s.Symbol(n,positive=True) if n in ('a','C','ell') else s.Symbol(n,real=True)
            for n in 'a H u0 u_dot v0 v_dot r0 r_dot psi_dot rho C w wd aw m ell sigma'.split()}
        self.bg=[x[n] for n in 'a H u0 u_dot v0 v_dot r0 r_dot psi_dot rho C'.split()]
        a,H,u,ud,v,vd,r,rd,pd,rho,C=self.bg
        self.a,self.H,self.m,self.ell=a,H,x['m'],x['ell']
        self.w,self.wd,self.aw,self.sign=x['w'],x['wd'],x['aw'],x['sigma']
        planar=READ(parent.ev.PLANAR)
        p={n:s.sympify(q) for n,q in linear['formulas']['parameter_map'].items()}
        p.update({n:s.sympify(q).subs(s.Symbol('eta'),e)
                  for n,q in planar['families'][self.family]['parameter_map'].items()})
        self.fixed=p;self.scale=e**s.Rational(7,2)
        self.MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        rad=u*u+v*v
        V=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*e*rad*r*r/28
        kin=ud*ud+vd*vd+rd*rd+p['K_Q']*pd*pd
        self.rates=s.Matrix([a*H,-(kin+rho)/(2*self.MC),
            ud,-3*H*ud-s.diff(V,u),vd,-3*H*vd-s.diff(V,v),
            rd,-3*H*rd-s.diff(V,r),-3*H*pd-p['beta']*rho/p['K_Q'],
            (-3*H+p['beta']*pd)*rho,p['beta']*pd*C])
        self.dbg=lambda q:CLEAN(sum(s.diff(q,z)*rate for z,rate in zip(self.bg,self.rates)
                                     if z in q.free_symbols))
        wire=READ(parent.CUSP+'formulas.json')
        context={**x,**p,'Hdot':self.rates[1],'I':s.I,'sqrt':s.sqrt}
        self.cv=CLEAN(s.sympify(wire['generic_cv'],locals=context))
        self.mass=CLEAN(s.sympify(wire['generic_mass'],locals=context))
        self.wdd=CLEAN(-3*H*self.wd-(self.cv*K*K/a**2+self.mass)*self.w)
        self.variables=[*self.bg,self.w,self.wd,self.aw,self.sign,self.m]
        self.velocity=[*self.rates,self.wd,self.wdd,self.sign*self.wd,0,0]
        self.dt=lambda q:CLEAN(sum(s.diff(q,z)*rate for z,rate in zip(self.variables,self.velocity)
                                   if z in q.free_symbols))
        self.dtm=lambda M:M.applyfunc(self.dt)
        self.matrix=lambda q:s.Matrix([[s.sympify(v,locals={**x,'I':s.I,'sqrt':s.sqrt})
                                        for v in row] for row in q['entries']])
        L=linear['formulas'];self.lm={n:self.matrix(q) for n,q in L['matrices'].items()}
        self.Nf=self.matrix(old['formulas']['forced_numerator'])
        self.g=s.sympify(L['g'],locals=x)
        self.den=CLEAN(1-self.g/(K*self.m)**2)
        self.dend=self.dt(self.den)
        self.box=parent.weighted.RationalBox({
            **{x[n]:tuple(map(s.Rational,b)) for n,b in linear['bounds']['background_box'].items()},
            self.w:(-s.Rational(25,19),s.Rational(25,19)),
            self.wd:(-s.Rational(205,4),s.Rational(205,4)),
            self.aw:(s.Integer(0),s.Rational(25,19)),self.sign:(s.Integer(-1),s.Integer(1))})
        allowed=set(self.variables)
        ch.add('complete_export_symbol_binding',
               (self.Nf.free_symbols|self.den.free_symbols).issubset(allowed))
        ch.add('same_fixed_family_and_case',old['family']==linear['family']
               and old['eta_exact']==linear['eta_exact'])
        self.mu=s.Rational(linear['bounds']['mu_exact'])
        self.qmax=max(sum(self.box.absolute(self.lm['Q'][i,j]) for j in range(20)) for i in range(20))
        self.normfactor=self.box.absolute(s.sqrt(20*self.qmax))

    def lower(self):
        progress(stage='SOURCE_AWARE_LOWER',index=self.index)
        a,H=self.a,self.H;p=self.fixed;pd=self.x['psi_dot'];w,wd,aw,sgn=self.w,self.wd,self.aw,self.sign
        pdd=self.rates[8];pddd=self.dbg(pdd)
        c=3*p['A']/(p['MU2']*(p['c1']+p['c4'])*self.scale)
        F=-c*pd**3*w*aw
        Fd=-c*(3*pd**2*pdd*w*aw+2*pd**3*aw*wd)
        Fdd=-c*((6*pd*pdd**2+3*pd**2*pddd)*w*aw
                +12*pd**2*pdd*aw*wd+2*pd**3*(sgn*wd**2+aw*self.wdd))
        for sign in (-1,1):
            sub={aw:sign*w,sgn:sign}
            self.ch.exact_matrix('F_dot_sign_'+str(sign),
                s.Matrix([(self.dt(F)-Fd).subs(sub)]))
            self.ch.exact_matrix('F_ddot_sign_'+str(sign),
                s.Matrix([(self.dt(Fd)-Fdd).subs(sub)]))
        self.ch.exact_matrix('source_F_and_Fdot_match_at_zero',s.Matrix([F,Fd]).subs({w:0,aw:0}))
        B=CLEAN(a*a*F/(self.cv*K*K))
        Bd=CLEAN(a*a*(2*H*F+Fd)/(self.cv*K*K))
        Bdd=CLEAN(a*a*((4*H*H+2*self.rates[1])*F+4*H*Fd+Fdd)/(self.cv*K*K))
        J=CLEAN(Bdd+3*H*Bd+self.mass*B)
        for sign in (-1,1):
            sub={aw:sign*w,sgn:sign}
            self.ch.exact_matrix('B_dot_sign_'+str(sign),s.Matrix([(self.dt(B)-Bd).subs(sub)]))
            self.ch.exact_matrix('B_ddot_sign_'+str(sign),s.Matrix([(self.dt(Bd)-Bdd).subs(sub)]))
        self.ch.exact_matrix('B_and_Bdot_zero_matching',s.Matrix([B,Bd]).subs({w:0,aw:0}))
        n=s.Symbol('n',positive=True);cn=s.Symbol('cn',real=True)
        uu,uv=s.symbols('uu uv',real=True)
        om=self.cv*(K*n/a)**2+self.mass
        udd=-3*H*uv-om*uu-J*cn/n**2
        residual=udd+Bdd*cn/n**2+3*H*(uv+Bd*cn/n**2)+om*(uu+B*cn/n**2)-F*cn
        self.ch.exact_matrix('exact_lower_particular_split',s.Matrix([residual]))
        # Complete redshifting modified energy, valid almost everywhere.
        omega2=self.cv*(K*n/a)**2
        derivative=2*uv*udd+2*(omega2+1)*uu*uv-2*H*omega2*uu**2
        expected=-6*H*uv**2-2*H*omega2*uu**2+2*(1-self.mass)*uu*uv-2*J*cn*uv/n**2
        self.ch.exact_matrix('complete_lower_compensated_energy',s.Matrix([derivative-expected]))
        init={a:1,pd:self.eta/5,w:1,aw:1}
        B0=CLEAN(B.subs(init))
        self.ch.add('reject_erasing_initial_lower_transient',B0!=0,str(B0))
        MB,MD,MJ=[self.box.absolute(q) for q in (B,Bd,J)]
        L=CLEAN(s.Rational(5,4)*(MD+41*MB+MJ/20))
        R=CLEAN(L/12+MB);V=CLEAN(L+MD)
        self.lower_formulas=dict(F=F,F_dot=Fd,F_ddot_ae=Fdd,B=B,B_dot=Bd,B_ddot_ae=Bdd,J=J)
        self.lower_bounds=dict(B=str(MB),B_dot=str(MD),J=str(MJ),
            compensated_energy_constant=str(L),displacement_constant=str(R),velocity_constant=str(V),
            displacement='|r_n|/scale<=R*|c_n|/n^2',
            velocity='|r_n_dot|/scale<=V*|c_n|/|n|',
            energy='sqrt(Eu_n)<=L*|c_n|/|n|',
            initial='u_n(0)=-B(0)c_n/n^2, u_n_dot(0)=-B_dot(0)c_n/n^2',
            regularity='B,B_dot continuous; B_ddot bounded a.e.; no delta at w=0',
            time='[0,1/20]',all_signed_odd_n=True)
        self.Fscaled=F
        self.constants=[R*s.Rational(36,15)*s.Rational(4,3)**5,
                        V*s.Rational(36,15)*s.Rational(4,3)**4,
                        R*s.Rational(36,15)*s.Rational(4,3)**5,
                        V*s.Rational(36,15)*s.Rational(4,3)**4,
                        s.Rational(256,45),s.Rational(256,45),s.Rational(1024,105)]
        self.decays=[5,4,5,4,3,3,4]
        self.ch.add('outward_lower_constants_finite',
                    all(q.is_Rational and q>0 for q in (MB,MD,MJ,L,R,V)))

    def normal_form(self):
        progress(stage='FULL_FAST_PARTICULAR',index=self.index)
        ell=K*self.m;F=self.lm['F'];L=self.lm['L'];drift=self.lm['drift'];d=self.den
        Ff=F.extract(FAST,FAST);Fi=Ff.inv()
        self.ch.exact_matrix('complete_fast_block_inverse',Ff*Fi-s.eye(2))
        part=-Fi*self.Nf.extract(FAST,range(7))/ell**2
        P=s.zeros(20,7)
        for i,row in enumerate(FAST):P[row,:]=part[i,:]
        P=P.applyfunc(CLEAN)
        selected=s.zeros(20,7)
        for row in FAST:selected[row,:]=self.Nf[row,:]
        self.ch.exact_matrix('full_fast_source_cancellation',ell**2*F*P+selected)
        Ds=s.zeros(7)
        for j,n in enumerate((self.m-1,self.m+1)):
            Ds[2*j,2*j+1]=1
            Ds[2*j+1,2*j]=-(self.cv*(n*K/self.a)**2+self.mass)
            Ds[2*j+1,2*j+1]=-3*self.H
            Ds[2*j+1,4+j]=self.Fscaled
        Pd=(self.dtm(P)+P*Ds).applyfunc(CLEAN)
        Nb=sum((self.lm['N'+str(j)]/ell**j for j in range(8)),s.zeros(20))
        slow=self.Nf-selected
        residual=(d*(slow+ell*L*P+drift*P-Pd)+Nb*P+P*self.dend).applyfunc(CLEAN)
        check=(d*self.Nf+d*(ell**2*F+ell*L+drift)*P+Nb*P
               -d*Pd+P*self.dend-residual)
        self.ch.exact_matrix('entire_forced_affine_identity',check)
        self.ch.add('reject_omitting_denominator_drift',any(q!=0 for q in P*self.dend))
        self.ch.add('reject_omitting_input_and_basis_drift',any(q!=0 for q in Pd))
        self.ch.add('no_evolution_projection',P.shape==(20,7) and residual.shape==(20,7))
        self.P,self.Pd,self.Ds,self.Nbar,self.R=P,Pd,Ds,Nb,residual
        self.G=(ell**2*F+ell*L+drift+Nb/d)
        self.models=dict(P_numerator=MAT(P),P_numerator_total_dot=MAT(Pd),
            residual_numerator_over_d_squared=MAT(residual),input_generator=MAT(Ds),
            denominator=str(d),denominator_dot=str(self.dend),fast_block=MAT(Ff),
            source_numerator=MAT(self.Nf),lower={n:str(q) for n,q in self.lower_formulas.items()},
            state='z=v+P_num*s/d; v(0)=-P(0), not zero',all_twenty_states=True)

    def rows(self,M,decays=None,constants=None):
        decays=self.decays if decays is None else decays
        constants=self.constants if constants is None else constants
        parts=parent.weighted.laurent(M,self.m);result=[]
        for i in range(M.rows):
            terms=[(power-decays[j],self.box.absolute(mat[i,j])*constants[j])
                   for power,mat in parts.items() for j in range(M.cols) if mat[i,j]!=0]
            if not terms:result.append(dict(power=None,constant='0'));continue
            power=max(q for q,c in terms)
            constant=CLEAN(sum(c*s.Integer(4)**(q-power) for q,c in terms))
            result.append(dict(power=power,constant=str(constant)))
        return result,sorted(parts)

    def maximum(self,rows):
        power=max(q['power'] for q in rows if q['power'] is not None)
        constant=max(s.Rational(q['constant'])*s.Integer(4)**(q['power']-power)
                     for q in rows if q['power'] is not None)
        return power,constant

    def bounds(self):
        progress(stage='SOURCE_AWARE_CONTINUOUS_BOUNDS',index=self.index)
        prows,pp=self.rows(self.P);rrows,rp=self.rows(self.R)
        pP,MP=self.maximum(prows);pR,MR=self.maximum(rrows)
        CP=self.normfactor*MP;CR=self.normfactor*MR
        pV=max(pP,pR)
        CV=CLEAN(CP*s.Integer(4)**(pP-pV)+CR*s.Integer(4)**(pR-pV)/20)
        pZ=max(pV,pP);CZ=CLEAN(CV*s.Integer(4)**(pV-pZ)+CP*s.Integer(4)**(pP-pZ))
        self.ch.add('complete_compensated_response_has_tail',pZ<0,pZ)
        if pZ>=0:raise ArithmeticError('No decaying complete source-aware response')
        fields=[];exports={}
        for kind,key,skey in [('field','coupled_field_from_weighted','qsource'),
                              ('Euler_velocity','coupled_rate_from_weighted','qdsource')]:
            A=self.matrix(self.old['formulas'][key])
            B=self.matrix(self.old['formulas']['nonzero'][skey])
            combined=(A*self.P+self.den*B).applyfunc(CLEAN)
            ar,ap=self.rows(A,[0]*20,[s.Integer(1)]*20)
            br,bp=self.rows(combined)
            exports[kind+'_combined_source_numerator']=MAT(combined)
            for i,(name,aa,bb) in enumerate(zip(parent.FIELDS,ar,br)):
                if kind=='Euler_velocity' and name=='LambdaU':
                    fields.append(dict(kind=kind,field=name,unused=True,actual_derivative='NOT_BOUNDED'))
                    continue
                terms=[]
                # ||v||inf <= 4 sqrt(Ev); include -P(0) in CV.
                if aa['power'] is not None:
                    terms.append((aa['power']+pV,4*s.Rational(aa['constant'])*CV*s.exp(self.mu/40)))
                if bb['power'] is not None:terms.append((bb['power'],s.Rational(bb['constant'])))
                if not terms:fields.append(dict(kind=kind,field=name,zero=True));continue
                power=max(q for q,c in terms);constant=sum(c*s.Integer(4)**(q-power) for q,c in terms)
                fields.append(dict(kind=kind,field=name,power=power,constant=str(constant),
                    Sobolev_s_strictly_below=str(-power-s.Rational(1,2)),
                    absolute_series_proved=power<-1))
        pointwise=all(q.get('zero') or q.get('power',0)<-1 for q in fields if q['kind']=='field')
        result=dict(lower=self.lower_bounds,input_decays=self.decays,
            input_constants=list(map(str,self.constants)),particular_rows=prows,residual_rows=rrows,
            particular_Laurent_powers=pp,residual_Laurent_powers=rp,
            particular_power=pP,residual_power=pR,complete_response_power=pZ,
            particular_Q_constant=str(CP),residual_Q_constant=str(CR),
            compensated_response_Q_constant=str(CV),full_response_Q_constant=str(CZ),
            mu_exact=str(self.mu),initial_compensation_included=True,
            complete_bound='sqrt(E_z_m)<=CZ exp(mu/40)|m|^power; |m|>=4, [0,1/20]',
            tail='sum_|m|>N |m|^(2s) E_z_m <= 2 CZ^2 exp(mu/20) N^(2s+2power+1)/(-2power-2s-1)',
            tail_s_strictly_below=str(-pZ-s.Rational(1,2)),fields=fields,
            all22_fields_absolute_Fourier_series=pointwise,
            mean_and_retained_pair='inherit separate CUSP3_COUPLED_TAIL_V3/CONSTANTS_V1 bounds',
            physical_window_admitted=False,useful_accuracy=False,full_nonlinear_remainder=False,
            physical_energy_positive=False,uniform_eta_endpoint=False)
        self.models.update(exports);self.estimate=result
        return result

    def controls(self,red):
        progress(stage='INDEPENDENT_SOURCE_AWARE_CONTROLS',index=self.index)
        order=self.variables
        # Keep the new complete corrector derivative, not a frozen source/basis.
        fun=s.lambdify([order],[self.P/self.den,self.Pd/self.den-self.P*self.dend/self.den**2,
              self.R/self.den**2,self.Ds,self.Nf/self.den,self.G,
              self.matrix(self.old['formulas']['source']),
              *[self.lm[n].subs(self.ell,K*self.m) for n in
                ('B','B_dot','U','U_dot','Tw','Tw_dot','Tw_inverse','Q')]],
              'numpy',cse=True)
        lowerfun=s.lambdify([order],list(self.lower_formulas.values())+
                            [self.mass,self.cv,*self.rates,self.wdd],'numpy',cse=True)
        p=parent.generic.bg.PARAMS.copy()
        for n,q in self.fixed.items():p['K' if n=='K_Q' else n]=float(q)
        p['gr']=float(3*self.eta/7)
        runs=[q for q in READ(parent.CUSP+'trajectories.json')['runs']
              if q['family']==self.family and s.Rational(q['eta_exact'])==self.eta]
        maximum={n:0. for n in ('affine','source','generator','all22','derivative',
                                 'lower_displacement','lower_velocity','root_displacement','root_velocity')}
        points=0;nodes=0;lower_checks=0;derivatives=0;root_checks=0
        R=s.Rational(self.lower_bounds['displacement_constant'])
        V=s.Rational(self.lower_bounds['velocity_constant'])
        def rel(a,b):return float(np.max(abs(a-b))/(1+np.max(abs(a))+np.max(abs(b))))
        def cn(n):return float(-4*np.sin(n*np.pi/2)/(np.pi*n*(n*n-4)))
        def excess(value,bound):return max(0.,float(abs(value)-bound))/(1+abs(value)+bound)
        for run in runs:
            for it,stored in enumerate(run['first_order_states']):
                b=np.asarray(stored,float);bg=b[:12];C=np.exp(p['beta']*bg[8])
                args=np.array([*bg[:8],bg[9],bg[10],C,b[12],b[13],abs(b[12]),np.sign(b[12]),4.])
                lc=np.asarray(lowerfun(args),complex).real
                # Seven lower formulas followed by mass,cv,eleven rates,wdd.
                mass,cv=lc[7:9];rates=lc[9:20];wdd=lc[20]
                z=np.asarray(run['states_scaled'][it],float)
                for j,n in enumerate((1,3)):
                    maximum['lower_displacement']=max(maximum['lower_displacement'],
                        excess(z[2*j],float(R)*abs(cn(n))/n**2))
                    maximum['lower_velocity']=max(maximum['lower_velocity'],
                        excess(z[2*j+1],float(V)*abs(cn(n))/n))
                    lower_checks+=1
                for m in (4,32):
                    args[-1]=m
                    values=[np.asarray(q,complex) for q in fun(args)]
                    PP,PD,RR,DD,ff,G,S,B,Bd,U,Ud,Tw,Twd,Ti,Q=values
                    ell=K*m
                    inputs=np.array([float(R)*cn(m-1)/(4*(m-1)**2),
                        float(V)*cn(m-1)/(4*(m-1)),
                        float(R)*cn(m+1)/(4*(m+1)**2),float(V)*cn(m+1)/(4*(m+1)),
                        cn(m-1),cn(m+1),12*(-1)**(m//2)/(np.pi*(m*m-1)*(m*m-9))])
                    src=S@inputs
                    d=red.at(bg,p,ell,src[:22],src[23:])
                    tf=np.eye(20)+U/ell;tfi=np.linalg.inv(tf)
                    O=parent.ev.READ(parent.FINITE)['SO2_map']['entries']
                    O=np.asarray([[complex(s.sympify(q)) for q in row] for row in O])
                    O20=np.zeros((20,20),complex);O20[:10,:10]=O;O20[10:,10:]=O
                    M=Tw@tfi@B@O20.conj().T
                    Md=(Twd@tfi@B-Tw@tfi@(Ud/ell)@tfi@B+Tw@tfi@Bd)@O20.conj().T
                    independentG=(Md+M@d['G'])@np.linalg.inv(M)
                    independentf=M@np.r_[np.zeros(10),d['ff']]
                    maximum['source']=max(maximum['source'],rel(ff@inputs,independentf))
                    maximum['generator']=max(maximum['generator'],rel(G,independentG))
                    direct=independentf+independentG@(PP@inputs)-PD@inputs
                    maximum['affine']=max(maximum['affine'],rel(RR@inputs,direct))
                    trial=np.cos(np.arange(20)+.17)*1e-4
                    physical=np.linalg.solve(M,trial+PP@inputs)
                    full=red.reconstruct(d,physical,p)
                    maximum['all22']=max(maximum['all22'],full['error'])
                    # Fourth-order directional derivative along the full local flow.
                    direction=np.r_[rates,b[13],wdd,np.sign(b[12])*b[13],0.,0.]
                    h=min(1e-3,abs(b[12])/(20*max(abs(b[13]),1.)))
                    if h>1e-9:
                        ds=DD@inputs
                        def at(v):
                            ar=args+v*direction
                            return np.asarray(fun(ar)[0],complex)@(inputs+v*ds)
                        numerical=(-at(2*h)+8*at(h)-8*at(-h)+at(-2*h))/(12*h)
                        maximum['derivative']=max(maximum['derivative'],rel(numerical,PD@inputs))
                        derivatives+=1
                    points+=1
                nodes+=1
            for j,n in enumerate((1,3)):
                rr=run['root_state_scaled'][2*j];vv=run['root_state_scaled'][2*j+1]
                maximum['root_displacement']=max(maximum['root_displacement'],
                    excess(rr,float(R)*abs(cn(n))/n**2))
                maximum['root_velocity']=max(maximum['root_velocity'],
                    excess(vv,float(V)*abs(cn(n))/n))
                root_checks+=1
        for name,value in maximum.items():self.ch.small('independent_'+name,value,1e-7 if name=='derivative' else 1e-9)
        self.ch.add('all42_unchanged_nodes',nodes==42,nodes)
        self.ch.add('all84_full_forced_action_probes',points==84,points)
        self.ch.add('all84_compensated_derivative_controls',derivatives==84,derivatives)
        self.ch.add('all84_stored_lower_checks',lower_checks==84,lower_checks)
        self.ch.add('all_four_stored_root_modes',root_checks==4,root_checks)
        return dict(maxima=maximum,background_nodes=nodes,action_probes=points,
                    derivative_probes=derivatives,lower_probes=lower_checks,root_probes=root_checks,
                    new_time_integrations=False)

    def run(self,red):
        self.lower();self.normal_form();estimate=self.bounds()
        self.partial=dict(formulas=self.models,bounds=estimate)
        numeric=self.controls(red)
        progress(stage='CASE_COMPLETE',index=self.index,particular=estimate['particular_power'],
                 residual=estimate['residual_power'],response=estimate['complete_response_power'],
                 pointwise_fields=estimate['all22_fields_absolute_Fourier_series'])
        return dict(index=self.index,family=self.family,eta_exact=str(self.eta),
                    bounds=estimate,formulas=self.models,numerics=numeric,checks=self.ch.rows)


def calculate(emit):
    pins,absent,snapshot=inputs();before=snapshot();checks=[];cases=[]
    red=parent.evolving.EvolvingReduction(parent.prior,parent.generic)
    for index in range(9):
        ch=Checks();der=None
        try:
            der=Case(index,ch);record=der.run(red);ok=all(q['passed'] for q in ch.rows)
            record['accepted']=ok
        except Exception as exc:
            ch.add('calculation_completed',False,dict(type=type(exc).__name__,message=str(exc)))
            record=dict(getattr(der,'partial',{}),index=index,accepted=False,checks=ch.rows,
                        error=str(exc),traceback=traceback.format_exc());ok=False
        emit('case_'+str(index).zfill(2)+'.json',ENCODE(record))
        cases.append(dict(index=index,accepted=ok,
            response_power=record.get('bounds',{}).get('complete_response_power'),
            pointwise_fields=record.get('bounds',{}).get('all22_fields_absolute_Fourier_series'),
            action_probes=record.get('numerics',{}).get('action_probes',0)))
        checks.extend(dict(q,name=str(index)+'|'+q['name']) for q in ch.rows)
        if not ok:break
    ch=Checks();ch.add('all_nine_cases',len(cases)==9,len(cases))
    ch.add('all756_independent_full_action_probes',sum(q['action_probes'] for q in cases)==756)
    ch.add('source_hash_size_mtime_preserved',before==snapshot());checks+=ch.rows
    passed=sum(q['passed'] for q in checks);complete=passed==len(checks)
    return dict(schema='r4c1-cusp3-source-aware-window-v1',
        validation='PASS_LOCAL_SOURCE_AWARE_ESTIMATE' if complete else 'FAIL_LOCAL_SOURCE_AWARE_ESTIMATE',
        status='SOURCE_AWARE_CUBIC_ESTIMATE' if complete else 'SOURCE_AWARE_ESTIMATE_UNRESOLVED',
        passed=passed,total=len(checks),checks=checks,cases=cases,
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,claim_status='Conditional',review_status='DEFERRED',
        Rule9_cleared=False,physics_pass=False,gate_effect='NONE',physical_window_admitted=False,
        full_nonlinear_remainder=False,useful_accuracy=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',
        UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        review_dependencies=['CUSP3-COUPLED-TAIL-V3/CONSTANTS-V1','LOW-RANK-WEIGHTED-EVOLUTION-V2',
            'lower odd response/root audit','CUSP3-EVOLUTION-V1','generic action/reduction',
            'all transitive deferred review debt'])


def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_cusp3_source_aware_window_attempt_01')
    ap.add_argument('--replay');ap.add_argument('--progress');args=ap.parse_args()
    if args.progress:
        PROGRESS=(ROOT/args.progress).resolve();PROGRESS.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        if PROGRESS.exists():raise FileExistsError('Refuse progress overwrite')
        PROGRESS.touch()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse existing evidence')
    else:dest.mkdir(parents=True)
    artifacts={}
    def emit(name,body):
        digest=SHA(body);side=(digest+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:
                raise ValueError('Immutable replay drift '+name)
        else:
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write(side)
        artifacts[name]=digest
    try:
        out=calculate(emit);out['artifacts']=dict(artifacts);emit('summary.json',ENCODE(out))
    except BaseException as exc:
        if not args.replay:emit('interrupted.json',ENCODE(dict(error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise ValueError('Replay changed metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:out[k] for k in ('validation','passed','total','status','physics_pass')}),flush=True)
    for q in out['checks']:
        if not q['passed']:print(json.dumps(q),flush=True)
    return int(out['passed']!=out['total'])


if __name__=='__main__':sys.exit(main())
