"""Complete cusp-order source/constraint/response bounds; no physical-window GO."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import traceback

import numpy as np
import sympy as s

import test_01_r4c1_cusp3_evolution_v1 as ev
import test_01_r4c1_three_family_weighted_evolution_v4 as weighted
import test_01_r4c1_gr_family_survey_v2 as generic
import test_01_r4c1_three_family_response_entry_v2 as prior
import test_01_r4c1_three_family_time_response_v2 as evolving

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
LINEAR=BASE+'r4c1_low_rank_inverse_attempt_02/'
LOWER=BASE+'r4c1_cusp_odd_response_tail_attempt_01/'
ROOT_AUDIT=BASE+'r4c1_cusp_odd_response_root_audit_attempt_01/'
CUSP=BASE+'r4c1_cusp3_evolution_attempt_01/'
KERNEL=BASE+'r4c1_g3n5_attempt_02/kernel.json'
FINITE=BASE+'r4c1_three_family_finite_k_attempt_04/formulas.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CUSP3_COUPLED_TAIL_V1_CONTRACT_2026-10-17.md'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS=ev.FIELDS
IX=ev.IX
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENCODE=lambda q:(json.dumps(q,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CLEAN=lambda q:s.factor(s.cancel(s.expand(q)))
MAT=lambda M:dict(shape=list(M.shape),entries=[[str(q) for q in M.row(i)] for i in range(M.rows)])
K=40
PROGRESS=None


def progress(**record):
    body=ENCODE(record)
    if PROGRESS is not None:
        with PROGRESS.open('ab') as stream:stream.write(body)
    print(json.dumps(record,sort_keys=True),flush=True)


class Checks(ev.Checks):
    def exact_matrix(self,name,M):
        bad=[]
        for i,q in enumerate(M):
            z=CLEAN(q)
            if z!=0:bad.append(dict(index=i,residual=str(z)))
        self.add(name,not bad,bad,'zero_exact')
        if bad:raise ArithmeticError(name+': '+str(bad[:2]))


def inputs():
    pins={};absent=set()
    expected={LINEAR:'7ceafaf52d8fe217f4b3f598a47cf75e50b7e4118f7b97bed66c322938f450f7',
              LOWER:'c908e715864be379d28445c3f5e32d173d23986b5db291c79eb1836dc94ed602',
              ROOT_AUDIT:'cc709dd431d8d1d11d1273eb7591aa2f9ac515b61307fef42515db9a11fc2632'}
    for base,digest in expected.items():
        parent=READ(base+'summary.json')
        if SHA((ROOT/(base+'summary.json')).read_bytes())!=digest:raise ValueError('Parent drift '+base)
        pins.update(parent['source_sha256'])
        pins.update({base+n:h for n,h in parent['artifacts'].items()})
        pins[base+'summary.json']=digest
        absent.update(parent['inherited_sidecars_absent'])
    pins[CONTRACT]='fea3fe06df8c983ff44c90538a97d42f43a3a9f42dba8eb7e8fafca61a9341ee'
    pins[SELF]=SHA((ROOT/SELF).read_bytes())
    paths=[]
    for name,digest in sorted(pins.items()):
        p=ROOT/name
        if SHA(p.read_bytes())!=digest:raise ValueError('Input drift '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise ValueError('Sidecar drift '+name)
            paths.append(side)
        elif name not in absent:raise ValueError('Missing sidecar '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    return pins,sorted(absent),snapshot


class Case:
    """Specialize only the generic action; never a B1-reduced operator."""
    def __init__(self,index,ch):
        self.index=index;self.ch=ch
        accepted=READ(LINEAR+'case_'+str(index).zfill(2)+'.json')
        self.family=accepted['family'];self.eta=e=s.Rational(accepted['eta_exact'])
        self.accepted=accepted
        progress(stage='CASE_START',index=index,family=self.family,eta=str(e))
        source=READ(CUSP+'formulas.json');planar=READ(ev.PLANAR);kernel=READ(KERNEL)
        names=set()
        texts=[q['value'] for q in kernel['entries']]
        texts += [q['coefficient'] for q in source['sparse_coefficients']]
        texts += [source['generic_cv'],source['generic_mass']]
        names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts)))
        names.update('rho w wd aw ell m inverse_ell'.split())
        x={n:s.Symbol(n,positive=True) if n in ('a','C','ell','inverse_ell') else s.Symbol(n,real=True)
           for n in names}
        self.x=x
        self.bg=[x[n] for n in 'a H u0 u_dot v0 v_dot r0 r_dot psi_dot rho C'.split()]
        a,H,u,ud,v,vd,r,rd,pd,rho,C=self.bg
        self.a,self.H,self.m,self.ell=a,H,x['m'],x['ell']
        self.w,self.wd,self.aw=x['w'],x['wd'],x['aw']
        fixed={n:s.sympify(q).subs(s.Symbol('eta'),e)
               for n,q in planar['families'][self.family]['parameter_map'].items()}
        fixed.update(m2=s.Integer(1),lambda4=s.Rational(1,3),lambda6=s.Rational(1,5),
                     Lambda=s.Integer(2),mr2=s.Integer(2),lambda_r=s.Rational(1,7),
                     rho_Lambda=s.Integer(0),g_r=3*e/7)
        self.fixed=fixed;self.scale=e**s.Rational(7,2)
        self.f2=fixed['MU2']*(fixed['c1']+fixed['c4'])
        self.MC=fixed['MP2']+fixed['MU2']*(fixed['c1']+3*fixed['c2']+fixed['c3'])/2
        rad=u*u+v*v
        V=rad/2+rad**2/24+rad**3/480+r*r+r**4/28+3*e*rad*r*r/28
        kin=ud*ud+vd*vd+rd*rd+fixed['K_Q']*pd*pd
        rates=[a*H,-(kin+rho)/(2*self.MC),ud,-3*H*ud-s.diff(V,u),
               vd,-3*H*vd-s.diff(V,v),rd,-3*H*rd-s.diff(V,r),
               -3*H*pd-fixed['beta']*rho/fixed['K_Q'],
               (-3*H+fixed['beta']*pd)*rho,fixed['beta']*pd*C]
        self.rates=s.Matrix(rates)
        self.dt=lambda q:CLEAN(sum(s.diff(q,z)*rate for z,rate in zip(self.bg,rates) if z in q.free_symbols))
        self.dtm=lambda M:M.applyfunc(self.dt)
        subs={x[n]:q for n,q in fixed.items() if n in x}
        subnames={'epsilon0':rho/C**4,'lambda0':3*fixed['MU2']*fixed['c2']*rates[1]
                  -3*fixed['MU2']*(fixed['c1']+fixed['c3'])*H*H,
                  'Hdot':rates[1],'Hddot':self.dt(rates[1]),
                  'psi_ddot':rates[8],'psi_dddot':self.dt(rates[8]),
                  'u_ddot':rates[3],'v_ddot':rates[5],'r_ddot':rates[7],
                  'u_dddot':self.dt(rates[3]),'v_dddot':self.dt(rates[5]),'r_dddot':self.dt(rates[7])}
        subs.update({x[n]:q for n,q in subnames.items() if n in x})
        self.load=lambda q:CLEAN(s.sympify(q,locals={**x,'I':s.I,'sqrt':s.sqrt}).subs(subs,simultaneous=True))
        self.cv=self.load(source['generic_cv']);self.mass=self.load(source['generic_mass'])
        self.md=self.dt(self.mass)
        ch.add('speed_in_registered_box',s.Rational(1,10)<=self.cv<=1,str(self.cv))
        self.wdd=-3*H*self.wd-(self.cv*K*K/a**2+self.mass)*self.w
        self.wddd=(-3*rates[1]*self.wd-3*H*self.wdd
                     -(-2*H*self.cv*K*K/a**2+self.md)*self.w
                     -(self.cv*K*K/a**2+self.mass)*self.wd)
        ch.add('leading_velocity_constant',s.Integer(1601)<41**2)
        ch.add('lower_displacement_conversion',s.Rational(5,722)<s.Rational(1,144))
        records=source['sparse_coefficients'];self.records=records
        self.coeff=[self.load(q['coefficient']) for q in records]
        self.source=self.make_source()
        self.ward_checks()
        # Hessian assembly includes ALL five jet blocks; z is the Fourier direction.
        mats=[s.zeros(22) for _ in range(4)];weights=[1,0,0,0,s.I*self.ell]
        for rec in kernel['entries']:
            bi,i=divmod(rec['row'],22);bj,j=divmod(rec['column'],22)
            value=self.load(rec['value'])
            if bi!=1 and bj!=1:mats[0][i,j]+=s.conjugate(weights[bi])*value*weights[bj]
            elif bi!=1:mats[1][i,j]+=s.conjugate(weights[bi])*value
            elif bj!=1:mats[2][i,j]+=value*weights[bj]
            else:mats[3][i,j]+=value
        self.LA,self.LB,self.LBT,self.LK=[M.applyfunc(CLEAN) for M in mats]
        self.EA=(self.LA-self.dtm(self.LBT)-3*H*self.LBT).applyfunc(CLEAN)
        self.EB=(self.LB-self.LBT-self.dtm(self.LK)-3*H*self.LK).applyfunc(CLEAN)
        self.ED=-self.LK
        self.box=weighted.RationalBox({a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(1,5),s.Integer(1)),
            **{z:(s.Integer(-2),s.Integer(2)) for z in (u,ud,v,vd,r,rd)},
            pd:(e/10,e/5),rho:(s.Rational(1,6),s.Rational(1,4)),C:(s.Integer(1),s.Rational(250,249)),
            self.w:(-s.Rational(25,19),s.Rational(25,19)),
            self.wd:(-s.Rational(205,4),s.Rational(205,4)),self.aw:(s.Integer(0),s.Rational(25,19))})
        self.unknowns=[*self.bg,self.w,self.wd,self.aw,self.m]
        self.numeric_coeff=s.lambdify([self.unknowns],self.coeff+[self.mass,self.cv,self.md,*rates,
                                                              self.wdd,self.wddd],'numpy',cse=True)

    def make_source(self):
        m,a,H=self.m,self.a,self.H;pd=self.x['psi_dot']
        pdd=self.rates[8];w,wd,aw=self.w,self.wd,self.aw
        F=-3*self.fixed['A']*pd**3*w*aw/(self.f2*self.scale)
        Fd=-3*self.fixed['A']*(3*pd**2*pdd*w*aw+2*pd**3*aw*wd)/(self.f2*self.scale)
        result=s.zeros(27,7)
        for branch,sign in enumerate((1,-1)):
            n=m-sign
            rr=s.zeros(1,7);vv=s.zeros(1,7);cc=s.zeros(1,7)
            rr[0,2*branch]=1;vv[0,2*branch+1]=1;cc[0,4+branch]=1
            omega=self.cv*(n*K/a)**2+self.mass
            od=-2*H*self.cv*(n*K/a)**2+self.md
            dd=-omega*rr-3*H*vv+F*cc
            ddd=-3*self.rates[1]*vv-3*H*dd-od*rr-omega*vv+Fd*cc
            lower=s.Matrix.vstack(rr,vv,s.I*n*K*rr,dd,s.I*n*K*vv,-(n*K)**2*rr,
                                  ddd,s.I*n*K*dd,-(n*K)**2*vv)
            q=sign*K
            first=s.Matrix([w,wd,s.I*q*w,self.wdd,s.I*q*wd,-q*q*w,
                            self.wddd,s.I*q*self.wdd,-q*q*wd])/2
            for record,c in zip(self.records,self.coeff):
                i,j,row=record['i'],record['j'],record['row']
                result[row,:]+=c*(first[i]*lower[j,:]+first[j]*lower[i,:])
        A=self.fixed['A'];X=A*pd**3*w*w*aw/self.scale
        result[0,6]+=2*X
        result[4,6]-=X/2;result[9,6]-=X/2;result[7,6]-=2*X
        result[16,6]+=3*A*((2*pd*pdd+3*H*pd*pd)*w*w*aw+3*pd*pd*w*aw*wd)/self.scale
        result[22,6]+=6*A*(pd*pd*pdd*w*w*aw+pd**3*w*aw*wd)/self.scale
        return result.applyfunc(CLEAN)

    def ward_checks(self):
        M=self.source;H,a,m=self.H,self.a,self.m
        temp=-M[22,:]-3*H*M[0,:]+2*H*(M[4,:]+M[7,:]+M[9,:])
        temp+=s.I*m*K*(M[3,:]+M[12,:])/a
        for field,rate in [('du',self.x['u_dot']),('dv',self.x['v_dot']),
                           ('dr',self.x['r_dot']),('Pi',self.x['psi_dot'])]:
            temp+=rate*M[IX[field],:]
        long=a*(M[25,:]+4*H*M[3,:])+2*s.I*m*K*M[9,:]
        for label,row in [('temporal',temp),('longitudinal',long)]:
            self.ch.exact_matrix(label+'_all_four_free_lower_columns',row[:,:4])
            # h=(c_-+c_+)/2, (m-3)c_-+(m+3)c_+=0.
            self.ch.exact_matrix(label+'_exact_cusp_convolution_Ward',
                s.Matrix([row[4]+row[6]/2+(row[5]+row[6]/2)*(3-m)/(m+3)]))
        n=s.Symbol('n',integer=True,positive=True)
        self.ch.add('all22_plus5_source_rows',M.shape==(27,7),list(M.shape))
        self.ch.add('direct_cusp_and_auxiliary_drift_retained',
                    M[0,6]!=0 and any(M[25,j]!=0 for j in range(7))
                    and any(M[26,j]!=0 for j in range(7)))

    def reduction(self,mean):
        progress(stage='ACTION_REDUCTION',index=self.index,mean=mean)
        ell=self.ell;H=self.H;a=self.a;p=self.fixed
        replace={ell:0} if mean else {ell:K*self.m}
        LA,LB,LK,EA,EB,ED=[M.subs(replace) for M in
                           (self.LA,self.LB,self.LK,self.EA,self.EB,self.ED)]
        dyn=FIELDS[4:10] if mean else ('Mxx','Mxy','Myy')
        dyn=(*dyn,*FIELDS[10:17]);aux=('Z',) if mean else ('Sx','Sy','Sz','Z')
        F=s.zeros(22,len(dyn));U=s.zeros(22,len(aux))
        for j,n in enumerate(dyn):F[IX[n],j]=1
        F[0,dyn.index('Pi')]=-p['beta']
        for j,n in enumerate(aux):U[IX[n],j]=1
        MT=p['MP2']-p['MU2']*(p['c1']+p['c3'])
        cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
        inv=s.Matrix([[1/p['b']]]) if mean else s.diag(
            2*a*a/(MT*(K*self.m)**2),2*a*a/(MT*(K*self.m)**2),
            -a*a/(cL*(K*self.m)**2),1/p['b'])
        invd=self.dtm(inv)
        Y=U.T*LA*F;VV=U.T*LB*F
        Q0=(F-U*inv*Y).applyfunc(CLEAN);Q1=(-U*inv*VV).applyfunc(CLEAN)
        Q0d=self.dtm(Q0);Q1d=self.dtm(Q1)
        kin=(F.T*LK*F-VV.T*inv*VV).applyfunc(CLEAN)
        self.ch.exact_matrix(('mean' if mean else 'nonzero')+'_regular_auxiliary_inverse',
                             U.T*LA*U*inv-s.eye(len(aux)))
        # The fixed-case kinetic matrix is mode/background independent.
        self.ch.add(('mean' if mean else 'nonzero')+'_kinetic_is_constant',
                    not kin.free_symbols,sorted(map(str,kin.free_symbols)))
        if kin.free_symbols:raise ValueError('Unexpected nonconstant kinetic inverse')
        ki=kin.inv()
        self.ch.exact_matrix(('mean' if mean else 'nonzero')+'_full_kinetic_inverse',
                             kin*ki-s.eye(len(dyn)))
        src=self.source.subs(self.m,0) if mean else self.source
        ai=[IX[n] for n in aux];di=[23+ev.AUX.index(n) for n in aux]
        us=(-U*inv*src[ai,:]).applyfunc(CLEAN)
        usd=(-U*(invd*src[ai,:]+inv*src[di,:])).applyfunc(CLEAN)
        acc=(ki*F.T*(src[:22,:]+EA*us+EB*usd)).applyfunc(CLEAN)
        AA=(ki*F.T*(EA*Q0+EB*Q0d)).applyfunc(CLEAN)
        BB=(ki*F.T*(EA*Q1+EB*(Q0+Q1d))).applyfunc(CLEAN)
        n=len(dyn);G=s.zeros(2*n);G[:n,n:]=s.eye(n);G[n:,:n]=AA;G[n:,n:]=BB
        qstate=Q0.row_join(Q1)
        qdstate=(Q0d+Q1*AA).row_join(Q0+Q1d+Q1*BB)
        qddstate=(F*AA).row_join(F*BB)
        qsource=us.copy();qdsource=Q1*acc+usd;qddsource=F*acc
        # Complete density, multiplier and density-rate reconstructions.
        for target,row in [('Em','alpha'),('LambdaU','nu')]:
            for qm,qdm,qddm,sm in [(qstate,qdstate,qddstate,s.zeros(22,2*n)),
                                   (qsource,qdsource,qddsource,src[:22,:])]:
                res=EA*qm+EB*qdm+ED*qddm+sm
                qm[IX[target],:]=-res[IX[row],:]/EA[IX[row],IX[target]]
        for qm,qdm,qddm,sm in [(qstate,qdstate,qddstate,s.zeros(22,2*n)),
                               (qsource,qdsource,qddsource,src[:22,:])]:
            res=EA*qm+EB*qdm+ED*qddm+sm
            qdm[IX['Em'],:]=-res[IX['T'],:]/EB[IX['T'],IX['Em']]
        result=dict(G=G,acc=acc,us=us,usd=usd,source=src,kinetic=kin,
                    qstate=qstate.applyfunc(CLEAN),qsource=qsource.applyfunc(CLEAN),
                    qdstate=qdstate.applyfunc(CLEAN),qdsource=qdsource.applyfunc(CLEAN))
        self.ch.exact_matrix(('mean' if mean else 'nonzero')+'_acceleration_reduction',
                             F.T*(EB*Q1+ED*F)+kin)
        return result

    def coefficients(self,M):
        return weighted.laurent(M,self.m)

    def tail_rows(self,M,input_decay,input_constant):
        parts=self.coefficients(M);out=[]
        for i in range(M.rows):
            terms=[]
            for power,mat in parts.items():
                for j in range(M.cols):
                    if mat[i,j]!=0:
                        terms.append((power-input_decay[j],
                                      self.box.absolute(mat[i,j])*input_constant[j]))
            if not terms:out.append(dict(power=None,constant='0'));continue
            power=max(q for q,c in terms)
            constant=CLEAN(sum(c*s.Integer(4)**(q-power) for q,c in terms))
            out.append(dict(power=power,constant=str(constant)))
        return out,sorted(parts)

    def bounds(self,nz,mean):
        progress(stage='CONTINUOUS_BOUNDS',index=self.index)
        accepted=self.accepted
        def matrix(name):
            return s.Matrix([[s.sympify(q,locals={**self.x,'I':s.I,'sqrt':s.sqrt})
                              for q in row] for row in accepted['formulas']['matrices'][name]['entries']])
        O=s.Matrix([[s.sympify(q) for q in row] for row in READ(FINITE)['SO2_map']['entries']])
        O20=s.diag(O,O);ell=K*self.m
        B=matrix('B').subs(self.ell,ell);Bi=matrix('B_inverse').subs(self.ell,ell)
        Tw,Ti,U,Q=[matrix(n) for n in ('Tw','Tw_inverse','U','Q')]
        inverse_num=sum((matrix('inverse_coefficient_'+str(j))/ell**j for j in range(4)),s.zeros(20))
        raw=s.zeros(20,7);raw[10:,:]=nz['acc']
        forced=(Tw*inverse_num*B*O20.T*raw).applyfunc(CLEAN)
        physical=(O20*Bi*(s.eye(20)+U/ell)*Ti).applyfunc(CLEAN)
        P=s.Rational(45,10108)
        # pi>3, |m+-1|>=m/2, sqrt(5/722)<1/12, m>=4.
        constants=[64*P/27,128*P/9,64*P/27,128*P/9,
                   s.Rational(128,9),s.Rational(128,9),s.Rational(1024,105)]
        decays=[4,3,4,3,3,3,4]
        fr,fp=self.tail_rows(forced,decays,constants)
        maxpower=max(q['power'] for q in fr if q['power'] is not None)
        Fc=max(s.Rational(q['constant'])*s.Integer(4)**(q['power']-maxpower)
               for q in fr if q['power'] is not None)
        qmax=max(sum(self.box.absolute(Q[i,j]) for j in range(20)) for i in range(20))
        Cforce=self.box.absolute(s.sqrt(20*qmax))*Fc
        mu=s.Rational(accepted['bounds']['mu_exact'])
        # sqrt(E)<=Cforce*t*exp(mu*t/2)*m^maxpower; ||w||inf<=4sqrt(E).
        self.ch.add('forced_decay_is_summable_at_s0',maxpower<=-1,maxpower)
        if maxpower>=0:raise ArithmeticError('No unweighted transformed-response tail')
        qstate=(nz['qstate']*physical).applyfunc(CLEAN)
        qdstate=(nz['qdstate']*physical).applyfunc(CLEAN)
        qs,qp=self.tail_rows(qstate,[0]*20,[s.Integer(1)]*20)
        qds,qdp=self.tail_rows(qdstate,[0]*20,[s.Integer(1)]*20)
        qf,qfp=self.tail_rows(nz['qsource'],decays,constants)
        qdf,qdfp=self.tail_rows(nz['qdsource'],decays,constants)
        recon=[]
        for label,states,sources in [('field',qs,qf),('field_rate',qds,qdf)]:
            for name,st,so in zip(FIELDS,states,sources):
                terms=[]
                if st['power'] is not None:
                    terms.append((st['power']+maxpower,
                                  s.Rational(st['constant'])*Cforce/5*s.exp(mu/40)))
                if so['power'] is not None:terms.append((so['power'],s.Rational(so['constant'])))
                if not terms:
                    recon.append(dict(kind=label,field=name,zero=True));continue
                power=max(q for q,c in terms)
                const=sum(c*s.Integer(4)**(q-power) for q,c in terms)
                recon.append(dict(kind=label,field=name,pointwise_power=power,
                    constant=str(const),Sobolev_s_strictly_below=str(-power-s.Rational(1,2)),
                    bound='sum_|m|>N |m|^(2s)|component_m|^2 <= 2 C^2 N^(2s+2power+1)/(-2power-2s-1)',
                    domain='integer N>=4; signed even m; stated strict s range'))
        mean_inputs=[P/27,P*4/9,P/27,P*4/9,s.Rational(4,9),s.Rational(4,9),s.Rational(4,9)]
        mg=max(sum(self.box.absolute(mean['G'][i,j]) for j in range(26)) for i in range(26))
        mf=max(sum(self.box.absolute(mean['acc'][i,j])*mean_inputs[j] for j in range(7))
               for i in range(13))
        # Three equal diagonal metric rates from the inherited charge-compatible preparation.
        y0=8*self.fixed['A']*(self.eta/5)**3*5/(27*self.MC*self.scale)
        mean_bound=(y0+mf/20)*s.exp(mg/20)
        mq=[]
        for key in ('qstate','qdstate'):
            skey='qsource' if key=='qstate' else 'qdsource'
            for i,name in enumerate(FIELDS):
                cst=sum(self.box.absolute(mean[key][i,j]) for j in range(26))
                csrc=sum(self.box.absolute(mean[skey][i,j])*mean_inputs[j] for j in range(7))
                mq.append(dict(kind=key,field=name,constant=str(cst*mean_bound+csrc)))
        export=dict(forced_numerator=MAT(forced),physical_from_weighted=MAT(physical),
            coupled_field_from_weighted=MAT(qstate),coupled_rate_from_weighted=MAT(qdstate))
        bounds=dict(time='[0,1/20]',mode_domain='signed even |m|>=4; ell=40m; eta fixed',
            forcing_power=maxpower,forcing_Q_constant=str(Cforce),mu_exact=str(mu),
            weighted_response_pointwise='sqrt(E_m)<=Cforce*exp(mu/40)*|m|^power/20',
            weighted_tail='sum_|m|>N |m|^(2s) E_m <= (Cforce^2/200)*exp(mu/20)*N^(2s+2power+1)/(-2power-2s-1)',
            weighted_s_strictly_below=str(-maxpower-s.Rational(1,2)),
            forcing_rows=fr,forcing_Laurent_powers=fp,field_reconstruction=recon,
            field_Laurent_powers=qp,rate_Laurent_powers=qdp,
            field_source_powers=qfp,rate_source_powers=qdfp,
            mean=dict(state_inf_bound=str(mean_bound),generator_inf=str(mg),forcing_inf=str(mf),
                      initial_inf_bound=str(y0),all22_field_and_rate_bounds=mq,
                      separate_constraint_chart=True),
            useful_accuracy=False,physical_cutoff=False,physical_energy_positive=False,
            full_nonlinear_remainder=False,uniform_eta_endpoint=False,
            proof='Exact Laurent coefficients bounded on the inherited continuous background box. '
                  'Complete Schur denominator>=1. Forced weighted energy uses the inherited full generator; '
                  'the mean uses its own 26-state norm and charge-compatible preparation. '
                  'No sampled maximum enters a continuum constant.')
        return bounds,export

    def numeric(self,nz,mean,red):
        progress(stage='INDEPENDENT_CONTROLS',index=self.index)
        symbols=self.unknowns
        fn=s.lambdify([symbols],[self.source,nz['acc'],nz['us'],nz['usd'],nz['G'],
                                mean['source'],mean['acc'],mean['us'],mean['usd'],mean['G']],
                       'numpy',cse=True)
        p=generic.bg.PARAMS.copy()
        for n,q in self.fixed.items():p['K' if n=='K_Q' else n]=float(q)
        p['gr']=float(3*self.eta/7)
        runs=[q for q in READ(CUSP+'trajectories.json')['runs']
              if q['family']==self.family and s.Rational(q['eta_exact'])==self.eta]
        maxima=dict(source=0.,forcing=0.,auxiliary=0.,drift=0.,generator=0.,equations=0.,
                    legacy_source=0.,periodic_convolution=0.)
        omissions=dict(direct=0.,auxiliary_drift=0.,fast_forcing=0.)
        records=[];count=0;legacy=0
        class Reference:pass
        ref=Reference()
        ref.row,ref.i,ref.j=np.array([(q['row'],q['i'],q['j']) for q in self.records]).T
        ref.polarize=lambda c,l,r:ev.Sources.polarize(ref,c,l,r)
        def relative(a,b):return float(np.max(abs(a-b))/(1+np.max(abs(a))+np.max(abs(b))))
        for ir,run in enumerate(runs):
            initial=np.asarray(run['states_scaled'][0],float)
            leading=run['first_order_states'][0]
            expected=np.zeros_like(initial)
            initial_rate=-8*p['A']*leading[9]**3/(9*np.pi*float(self.MC)*leading[1]*float(self.scale))
            for j in (0,3,5):expected[4+13+j]=initial_rate
            self.ch.small('run'+str(ir)+'_inherited_charge_compatible_initial_state',
                          relative(initial,expected),1e-12)
            for it,stored in enumerate(run['first_order_states']):
                b=np.asarray(stored,float);bg=b[:12];C=np.exp(p['beta']*bg[8])
                values=[*bg[:8],bg[9],bg[10],C,b[12],b[13],abs(b[12]),0.]
                cc=np.asarray(self.numeric_coeff(values),complex).real
                ncoef=len(self.coeff);mass,cv,md=cc[ncoef:ncoef+3]
                rates=cc[ncoef+3:ncoef+14]
                context=dict(coefficients=cc[:ncoef],mass=mass,cv=cv,md=md,
                             rate=np.r_[rates[:8],0.,rates[8:10],0.],
                             w=b[12],wd=b[13],wdd=cc[-2],wddd=cc[-1])
                for m in (0,2,4,6,8,12,32):
                    values[-1]=m;vv=[np.asarray(q,complex) for q in fn(values)]
                    src,acc,us,usd,G=vv[5:] if m==0 else vv[:5]
                    n1,n2=m-1,m+1
                    cn=lambda n:float(-4*np.sin(n*np.pi/2)/(np.pi*n*(n*n-4)))
                    cm,cp=cn(n1),cn(n2)
                    hm=12*(-1)**(m//2)/(np.pi*(m*m-1)*(m*m-9))
                    P=float(s.Rational(45,10108))
                    aff=np.array([P*cm/(24*abs(n1)),P*cm/3,
                                  P*cp/(24*abs(n2)),P*cp/3,cm,cp,hm])
                    if m==0:aff[2:4]=aff[:2]
                    actual=src@aff
                    d=red.at(bg,p,m*K,actual[:22],actual[23:])
                    maxima['forcing']=max(maxima['forcing'],relative(acc@aff,d['ff']))
                    maxima['auxiliary']=max(maxima['auxiliary'],relative(us@aff,d['us']))
                    maxima['drift']=max(maxima['drift'],relative(usd@aff,d['usd']))
                    maxima['generator']=max(maxima['generator'],relative(G,d['G']))
                    state=np.cos(np.arange(len(d['G']))+.3)*1e-4
                    out=red.reconstruct(d,state,p)
                    maxima['equations']=max(maxima['equations'],out['error'])
                    omissions['direct']=max(omissions['direct'],float(np.max(abs(src[:,6]*hm))))
                    omissions['auxiliary_drift']=max(omissions['auxiliary_drift'],float(np.max(abs(usd@aff))))
                    omissions['fast_forcing']=max(omissions['fast_forcing'],float(abs((acc@aff)[-1])))
                    count+=1
                    if m in (0,2):
                        stored_state=np.asarray(run['states_scaled'][it])
                        old,_,_=ev.Sources.source(ref,context,b,p,m,float(self.scale))
                        want=old@np.r_[1.,stored_state[:4]]
                        if m==0:q=np.r_[stored_state[:2],stored_state[:2],cm,cp,hm]
                        else:q=np.r_[stored_state[:4],cm,cp,hm]
                        maxima['legacy_source']=max(maxima['legacy_source'],relative(src@q,want))
                        legacy+=1
                    if ir==0 and it in (0,10,20):
                        maxima['periodic_convolution']=max(maxima['periodic_convolution'],
                            self.periodic_control(m,aff,context,b,p,ref,actual))
                records.append(dict(run=ir,node=it,time=run['times'][it]))
        # Admissible leading zero-crossing jets at an unchanged background event.
        b=np.asarray(runs[0]['first_order_states'][0],float)
        bg=b[:12];C=np.exp(p['beta']*bg[8])
        values=[*bg[:8],bg[9],bg[10],C,0.,1.,0.,0.]
        zero_max=0.;zero_count=0
        for m in (0,2,4,6,8,12,32):
            values[-1]=m;vv=[np.asarray(q,complex) for q in fn(values)]
            src,acc,us,usd,G=vv[5:] if m==0 else vv[:5]
            cn=lambda n:float(-4*np.sin(n*np.pi/2)/(np.pi*n*(n*n-4)))
            cm,cp=cn(m-1),cn(m+1)
            hm=12*(-1)**(m//2)/(np.pi*(m*m-1)*(m*m-9))
            aff=np.array([cm*1e-5,cm*1e-5,cp*1e-5,cp*1e-5,cm,cp,hm])
            actual=src@aff
            d=red.at(bg,p,m*K,actual[:22],actual[23:])
            out=red.reconstruct(d,np.zeros(len(d['G'])),p)
            zero_max=max(zero_max,out['error'],relative(acc@aff,d['ff']),
                         relative(us@aff,d['us']),relative(usd@aff,d['usd']))
            zero_count+=1
        self.ch.small('leading_zero_crossing_all22_equations_and_drift',zero_max,1e-9)
        self.ch.add('seven_leading_zero_crossing_controls',zero_count==7,zero_count)
        maxima['source']=max(maxima['legacy_source'],maxima['periodic_convolution'])
        for key,value in maxima.items():self.ch.small('independent_'+key,value,1e-9)
        for key,value in omissions.items():self.ch.add('reject_omitted_'+key,value!=0,value)
        self.ch.add('all42_unchanged_background_nodes',len(records)==42,len(records))
        self.ch.add('all294_seven_mode_controls',count==294,count)
        self.ch.add('all84_old_mean_first_even_controls',legacy==84,legacy)
        return dict(maxima=maxima,omissions=omissions,action_probes=count,
                    legacy_probes=legacy,background_nodes=records,wave_zero_probes=zero_count,
                    wave_zero_max=zero_max)

    def periodic_control(self,m,aff,c,b,p,ref,want):
        # Independent angular product, then numerical Fourier integration.
        # No use of the new seven-column source/constraint matrix.
        theta=2*np.pi*np.arange(8192)/8192
        w,wd,wdd,wddd=c['w'],c['wd'],c['wdd'],c['wddd']
        co,si=np.cos(theta),np.sin(theta)
        first=np.array([w*co,wd*co,-K*w*si,wdd*co,-K*wd*si,-K*K*w*co,
                        wddd*co,-K*wdd*si,-K*K*wd*co])
        lower=np.zeros_like(first)
        a,H=b[:2];pd=b[9];pdd=c['rate'][9];f2=p['MU2']*(p['c1']+p['c4'])
        scale=float(self.scale)
        used=set()
        for branch,n in enumerate((m-1,m+1)):
            if abs(n) in used:continue
            used.add(abs(n));n=abs(n)
            rr,rd=aff[2*branch:2*branch+2]
            cn=-4*np.sin(n*np.pi/2)/(np.pi*n*(n*n-4))
            F=-3*p['A']*pd**3*w*abs(w)*cn/(f2*scale)
            Fd=-3*p['A']*(3*pd*pd*pdd*w*abs(w)+2*pd**3*abs(w)*wd)*cn/(f2*scale)
            omega=c['cv']*(n*K/a)**2+c['mass'];od=-2*H*c['cv']*(n*K/a)**2+c['md']
            dd=-omega*rr-3*H*rd+F
            ddd=-3*c['rate'][1]*rd-3*H*dd-od*rr-omega*rd+Fd
            cnth,snth=np.cos(n*theta),np.sin(n*theta);q=n*K
            lower+=2*np.array([rr*cnth,rd*cnth,-q*rr*snth,dd*cnth,-q*rd*snth,
                               -q*q*rr*cnth,ddd*cnth,-q*dd*snth,-q*q*rd*cnth])
        angular=np.zeros((27,len(theta)))
        for record,cc in zip(self.records,c['coefficients']):
            i,j,row=record['i'],record['j'],record['row']
            angular[row]+=cc*(first[i]*lower[j]+first[j]*lower[i])
        Aw=p['A'];ab=abs(w*co);abdot=3*w*abs(w)*wd*abs(co)**3
        X=Aw*pd**3*ab**3/scale
        angular[0]+=2*X;angular[4]-=X/2;angular[9]-=X/2;angular[7]-=2*X
        angular[16]+=3*Aw*((2*pd*pdd+3*H*pd*pd)*ab**3+pd*pd*abdot)/scale
        angular[22]+=6*Aw*(pd*pd*pdd*ab**3+pd**3*abdot/3)/scale
        got=np.mean(angular*np.exp(-1j*m*theta),axis=1)
        return float(np.max(abs(got-want))/(1+np.max(abs(got))+np.max(abs(want))))

    def run(self,red):
        nz=self.reduction(False);mean=self.reduction(True)
        bounds,extra=self.bounds(nz,mean)
        numbers=self.numeric(nz,mean,red)
        progress(stage='CASE_COMPLETE',index=self.index,forcing_power=bounds['forcing_power'])
        return dict(index=self.index,family=self.family,eta_exact=str(self.eta),checks=self.ch.rows,
            bounds=bounds,numerics=numbers,formulas=dict(
                input_order=['r_(m-1)/scale','rd_(m-1)/scale','r_(m+1)/scale','rd_(m+1)/scale',
                             'c_(m-1)','c_(m+1)','h_m'],
                source_order=[*FIELDS,'alpha_dot','Sx_dot','Sy_dot','Sz_dot','Z_dot'],
                source=MAT(self.source),nonzero={k:MAT(v) for k,v in nz.items()},
                mean={k:MAT(v) for k,v in mean.items()},**extra))


def calculate(emit):
    pins,absent,snapshot=inputs();before=snapshot();checks=[];cases=[]
    red=evolving.EvolvingReduction(prior,generic)
    for index in range(9):
        ch=Checks()
        try:
            der=Case(index,ch);record=der.run(red)
            accepted=all(q['passed'] for q in ch.rows)
            record['accepted']=accepted
        except Exception as exc:
            ch.add('calculation_completed',False,dict(type=type(exc).__name__,message=str(exc)))
            record=dict(index=index,accepted=False,checks=ch.rows,error=str(exc),traceback=traceback.format_exc())
            accepted=False
        emit('case_'+str(index).zfill(2)+'.json',ENCODE(record))
        cases.append(dict(index=index,accepted=accepted,
            forcing_power=record.get('bounds',{}).get('forcing_power'),
            action_probes=record.get('numerics',{}).get('action_probes',0)))
        checks.extend(dict(q,name=str(index)+'|'+q['name']) for q in ch.rows)
        if not accepted:break
    ch=Checks();ch.add('all_nine_cases',len(cases)==9,len(cases))
    ch.add('all2646_independent_action_probes',sum(q['action_probes'] for q in cases)==2646)
    ch.add('source_hash_size_mtime_preserved',before==snapshot());checks+=ch.rows
    passed=sum(q['passed'] for q in checks);complete=passed==len(checks)
    return dict(schema='r4c1-cusp3-coupled-tail-v1',
        validation='PASS_LOCAL_COUPLED_ORDER3_BOUND' if complete else 'FAIL_LOCAL_COUPLED_ORDER3_BOUND',
        status='COUPLED_ORDER3_BOUND_COMPLETE' if complete else 'COUPLED_ORDER3_BOUND_UNRESOLVED',
        passed=passed,total=len(checks),checks=checks,cases=cases,
        source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,
        source_metadata_preserved=len(before),claim_status='Conditional',review_status='DEFERRED',
        Rule9_cleared=False,physics_pass=False,gate_effect='NONE',physical_window_admitted=False,
        useful_error_control=False,full_nonlinear_remainder=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',
        UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        review_dependencies=['CUSP3-EVOLUTION-V1','LOW-RANK-WEIGHTED-EVOLUTION-V2',
          'CUSP-ODD-RESPONSE-TAIL-V1','CUSP-ODD-RESPONSE-ROOT-AUDIT-V1',
          'THREE-FAMILY-FINITE-K-V3','generic action/evolving reduction','all transitive debt'],
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))


def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_cusp3_coupled_tail_attempt_01')
    ap.add_argument('--replay');ap.add_argument('--progress')
    args=ap.parse_args()
    if args.progress:
        PROGRESS=(ROOT/args.progress).resolve()
        PROGRESS.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        if PROGRESS.exists():raise FileExistsError('Refuse progress log overwrite')
        PROGRESS.touch()
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse evidence overwrite')
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
        summary=calculate(emit);summary['artifacts']=dict(artifacts);emit('summary.json',ENCODE(summary))
    except BaseException as exc:
        if not args.replay:emit('interrupted.json',ENCODE(dict(error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise ValueError('Replay changed artifact metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','physics_pass')}),flush=True)
    for q in summary['checks']:
        if not q['passed']:print(json.dumps(q),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':
    sys.exit(main())
