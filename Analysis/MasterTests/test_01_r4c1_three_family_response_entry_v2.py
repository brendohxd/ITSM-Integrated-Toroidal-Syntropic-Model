"""V2: completed paired mixed derivatives; unchanged sourced initial-response physics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

import numpy as np
import scipy
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_RESPONSE_ENTRY_V1_CONTRACT_2026-10-12.md'
ENTRY='Analysis/MasterTests/test_01_r4c1_three_family_nonanalytic_entry_v1.py'
SOURCE=BASE+'r4c1_g3n4_attempt_01/formulas.json'
DISPOSITION='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_RESPONSE_ENTRY_V2_DISPOSITION_2026-10-12.md'
PINNED={
    DISPOSITION:'32b387254924dfa6f6efe1af48a9a078ffa923ce79b8e495d4205c4dd2d40123',
    CONTRACT:'fa737c57c36a76561ef24a492d707701ba735b0e68454bb17233eebdb41c84d1',
    ENTRY:'ab0f65fb8b99043714abbd152f45ac1d438931a91debac5d06d6fb28ec86d04d',
    SOURCE:'1dee96271de67aec5336ac84753c18728a65e130e05c1c7731559c5a6a49727a',
    BASE+'r4c1_three_family_nonanalytic_entry_attempt_01/summary.json':'0b06579cbab005fe454023fc1a2a2f89b48f15463ea5a3dc5b7712828db67fdf',
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_NONANALYTIC_ENTRY_V1_REPORT_2026-10-12.md':'091905e3322a70e815788a634d0b058425442ed8ba42f1ff92e48c30772d96c9',
    'Theory/Gates/RES-001/RES001_R4C1_G3N4_COUPLED_SOURCE_REPORT_2026-10-09.md':'1c7eca17f22a8e3e3ec39bb09017d05908b133f130b1f24e85f523b18af47a4b',
    'Analysis/MasterTests/test_01_r4c1_three_family_response_entry_v1.py':'f44f532ce85ba213f1fd7d3aa9d1ab700833065b74596429ac264c56da937cad',
    BASE+'r4c1_three_family_response_entry_attempt_01/summary.json':'e4dbb787ebfdef15fe87566fb3a9a39f130932f023799df897466180997e7d16',
}


def sha(body):return hashlib.sha256(body).hexdigest()
def encode(value):return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def read(name):return json.loads((ROOT/name).read_bytes())
def tidy(value):return s.factor(s.cancel(s.expand(value)))


class Checks:
    def __init__(self):self.rows=[]
    def add(self,name,passed,evidence=None):self.rows.append(dict(name=name,passed=bool(passed),evidence=evidence))
    def exact(self,name,value):
        residue=tidy(value);self.add(name,residue==0,str(residue))


def pins_and_imports():
    for name,digest in PINNED.items():
        if sha((ROOT/name).read_bytes())!=digest:raise RuntimeError('Direct source drift: '+name)
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_three_family_nonanalytic_entry_v1 as entry
    import test_01_r4c1_gr_family_survey_v2 as generic
    pins,_,_=entry.collect_pins()
    pins.update(PINNED);pins[SELF]=sha((ROOT/SELF).read_bytes())
    for prefix in ('r4c1_three_family_nonanalytic_entry_attempt_01/','r4c1_g3n4_force_attempt_01/','r4c1_three_family_response_entry_attempt_01/'):
        j=read(BASE+prefix+'summary.json')
        pins.update({BASE+prefix+k:v for k,v in j['artifacts'].items()})
    paths=[];missing=[]
    for name,digest in pins.items():
        p=ROOT/name
        if sha(p.read_bytes())!=digest:raise RuntimeError('Inherited source drift: '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        else:missing.append(name)
    return entry,generic,pins,paths,missing


class Sources:
    def __init__(self,checks):
        original=read(SOURCE)
        names=set()
        for text in [*original['Euler_sources_before_shift'].values(),original['quadratic_vector_action']]:
            names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',text))
        for coeff in original['response_coefficients'].values():
            for text in coeff.values():names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',text))
        names.update('eta Hddot psi_dddot W_ttt W_ttz W_tzz B B_t B_tt r0 r_dot r_ddot u_dddot v_dddot r_dddot C C_dot epsilon0 epsilon_dot lambda0 lambda_dot'.split())
        self.sy={name:s.Symbol(name,real=True) for name in names};self.sy['eta']=s.Symbol('eta',positive=True)
        self.x=self.sy;self.original=original
        self.sources={k:s.sympify(v,locals=self.sy) for k,v in original['Euler_sources_before_shift'].items()}
        self.L2=s.sympify(original['quadratic_vector_action'],locals=self.sy)
        self.mapping={}
        for a,b in dict(a='a*H',H='Hdot',Hdot='Hddot',psi_dot='psi_ddot',psi_ddot='psi_dddot',
            W='W_t',W_t='W_tt',W_z='W_tz',W_tt='W_ttt',W_tz='W_ttz',W_zz='W_tzz',
            B='B_t',B_t='B_tt',B_z='B_tz',u0='u_dot',v0='v_dot',r0='r_dot',
            u_dot='u_ddot',v_dot='v_ddot',r_dot='r_ddot',C='C_dot',epsilon0='epsilon_dot',lambda0='lambda_dot').items():
            if a in self.sy:self.mapping[self.sy[a]]=s.sympify(b,locals=self.sy)
        self.spatial={}
        for a,b in dict(W='W_z',W_t='W_tz',W_z='W_zz',W_tt='W_ttz',W_tz='W_tzz',B='B_z',B_t='B_tz',B_z='B_zz').items():
            if a in self.sy:self.spatial[self.sy[a]]=self.sy[b]
        checks.exact('paired_spatial_acceleration_derivative',self.dz(self.sy['W_tt'])-self.sy['W_ttz'])
        checks.exact('paired_spatial_mixed_velocity_derivative',self.dz(self.sy['W_tz'])-self.sy['W_tzz'])
        checks.exact('commuting_time_spatial_derivatives_on_Wt',self.dt(self.dz(self.sy['W_t']))-self.dz(self.dt(self.sy['W_t'])))
        checks.exact('commuting_time_spatial_derivatives_on_Wz',self.dt(self.dz(self.sy['W_z']))-self.dz(self.dt(self.sy['W_z'])))
        for field,coef in original['response_coefficients'].items():
            cv,ct,cz=[s.sympify(coef[key],locals=self.sy) for key in ('value','time_derivative','spatial_derivative')]
            checks.exact('generic_22field_source_Euler_'+field,self.sources[field]-cv+self.dt(ct)+3*self.x['H']*ct+self.dz(cz))
        self.families={};self.functions={};self.orders={};self.wards={}
        for name in ('archived_G3','new_B1_frame','new_hierarchical'):
            self.specialize(name,checks)

    def dt(self,value):return s.expand(sum(s.diff(value,q)*rate for q,rate in self.mapping.items() if q in value.free_symbols))
    def dz(self,value):return s.expand(sum(s.diff(value,q)*rate for q,rate in self.spatial.items() if q in value.free_symbols))

    def specialize(self,name,checks):
        x=self.x;e=x['eta'];c2=-s.Rational(7,48) if name=='archived_G3' else s.Rational(1,10)
        c3=-s.Rational(1,80) if name=='archived_G3' else (-s.Rational(1,5) if name=='new_B1_frame' else -s.Rational(1,5)+3*e/16)
        constants={x['MP2']:1,x['MU2']:2*e/3,x['c1']:s.Rational(1,5),x['c2']:c2,x['c3']:c3,
                   x['c4']:s.Rational(1,20),x['K_Q']:3*e,x['b']:5*e/11,x['zeta']:e/13}
        alpha13=tidy((2*e/3)*(s.Rational(1,5)+c3));sigma=tidy(-alpha13/(1-alpha13))
        shift={x[b]:sigma*x[w] for b,w in [('B','W'),('B_t','W_t'),('B_z','W_z'),('B_tt','W_tt'),('B_tz','W_tz'),('B_zz','W_zz')]}
        src={field:tidy(value.subs(constants).subs(shift)) for field,value in self.sources.items()}
        density=tidy(self.L2.subs(constants).subs(shift));W,Wt,Wz=x['W'],x['W_t'],x['W_z']
        EW=tidy(s.diff(density,W)-self.dt(s.diff(density,Wt))-3*x['H']*s.diff(density,Wt)-self.dz(s.diff(density,Wz)))
        cross=s.diff(density,W,Wt);position=s.diff(density,W,2);f2=s.diff(density,Wt,2)
        mw=tidy((self.dt(cross)+3*x['H']*cross-position.subs(Wz,0))/f2)
        cv=tidy(-x['a']**2*s.diff(density,Wz,2)/f2)
        shell=-3*x['H']*Wt+cv*x['W_zz']/x['a']**2-mw*W
        checks.exact(name+'_correct_member_vector_shell',EW.subs(x['W_tt'],shell))
        temporal=-self.dt(src['alpha'])-3*x['H']*src['alpha']+2*x['H']*(src['Mxx']+src['Myy']+src['Mzz'])
        temporal+=self.dz(src['Sz']+src['Vz'])/x['a']
        for field,rate in [('du','u_dot'),('dv','v_dot'),('dr','r_dot'),('Pi','psi_dot'),('T','C'),('Em','epsilon_dot'),('LambdaU','lambda_dot')]:
            temporal+=x[rate]*src[field]
        longitudinal=x['a']*(self.dt(src['Sz'])+4*x['H']*src['Sz'])+2*self.dz(src['Mzz'])
        checks.exact(name+'_off_shell_temporal_source_identity',temporal-(x['H']*W-Wt)*EW)
        checks.exact(name+'_off_shell_longitudinal_source_identity',longitudinal-Wz*EW)
        auxiliary=('Sx','Sy','Sz','Z');ds={field:tidy(self.dt(src[field])) for field in auxiliary}
        expr=[*src.values(),*ds.values()]
        order=sorted(set(str(q) for v in expr for q in v.free_symbols))
        self.functions[name]=s.lambdify([[x[q] for q in order]],expr,'numpy',cse=True)
        self.orders[name]=order
        self.families[name]=dict(sources=src,auxiliary_source_dt=ds,source_order=list(src),aux_order=list(auxiliary),
                                 sigma=sigma,m_w2=mw,c_V2=cv,vector_shell=shell)
        self.wards[name]=dict(temporal_before_shell=str(tidy(temporal)),longitudinal_before_shell=str(tidy(longitudinal)),
            vector_Euler=str(EW),temporal_minus_expected=str(tidy(temporal-(x['H']*W-Wt)*EW)),
            longitudinal_minus_expected=str(tidy(longitudinal-Wz*EW)))
        for field in ('T','Em','LambdaU'):
            checks.exact(name+'_clock_unit_direct_source_zero_'+field,src[field])
        print(json.dumps(dict(stage='SOURCE_AND_WARD_ALGEBRA',family=name)),flush=True)

    def values(self,name,eta,y,p,generic,k,theta):
        rates=np.array(generic.bg.rhs(0,y,p),float);small=1e-24
        acceleration=np.imag(np.array(generic.bg.rhs(0,y.astype(complex)+1j*small*rates,p),complex))/small
        a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=y;Hd=rates[1];pdd=rates[9];Hdd=acceleration[1];pd3=acceleration[9]
        C=np.exp(p['beta']*psi);J=v*ud-u*vd
        raw={'eta':eta,'a':a,'H':H,'Hdot':Hd,'Hddot':Hdd,'u0':u,'v0':v,'r0':r,'u_dot':ud,'v_dot':vd,'r_dot':rd,
             'u_ddot':rates[3],'v_ddot':rates[5],'r_ddot':rates[7],'u_dddot':acceleration[3],'v_dddot':acceleration[5],
             'r_dddot':acceleration[7],'psi_dot':pd,'psi_ddot':pdd,'psi_dddot':pd3,'C':C,'C_dot':p['beta']*pd*C,
             'epsilon0':rho/C**4,'epsilon_dot':(rates[10]-4*p['beta']*pd*rho)/C**4,
             'lambda0':3*p['MU2']*p['c2']*Hd-3*p['MU2']*(p['c1']+p['c3'])*H**2,
             'lambda_dot':3*p['MU2']*p['c2']*Hdd-6*p['MU2']*(p['c1']+p['c3'])*H*Hd}
        f=self.families[name];coef={self.x[q]:value for q,value in raw.items() if q in self.x}
        mw=float(f['m_w2'].subs(coef));cv=float(f['c_V2'].subs(coef));omega2=cv*k*k/a**2+mw
        mw_dot=float(self.dt(f['m_w2']).subs(coef))
        W=np.cos(theta);Wz=-k*np.sin(theta);Wzz=-k*k*W;Wtt=-omega2*W
        raw.update(W=W,W_t=0.,W_z=Wz,W_tt=Wtt,W_tz=0.,W_zz=Wzz,
                   W_ttt=-3*H*Wtt-2*H*cv*Wzz/a**2-mw_dot*W,W_ttz=-omega2*Wz,W_tzz=0.)
        return raw

    def angular(self,name,eta,y,p,generic,k,theta):
        values=self.values(name,eta,y,p,generic,k,theta)
        data=np.array(self.functions[name]([values[q] for q in self.orders[name]]),complex)
        source=dict(zip(self.families[name]['source_order'],data[:22]))
        derivative=dict(zip(self.families[name]['aux_order'],data[22:]))
        return source,derivative

    def fourier(self,name,eta,y,p,generic,k,checks):
        angles=(0.,np.pi/2,np.pi/4,3*np.pi/4)
        q=[self.angular(name,eta,y,p,generic,k,z) for z in angles]
        out=[]
        for which in (0,1):
            fields=self.families[name]['source_order' if which==0 else 'aux_order']
            vectors=[np.array([item[which][field] for field in fields]) for item in q]
            mean=(vectors[0]+vectors[1])/2;cosine=(vectors[0]-vectors[1])/2;sine=(vectors[2]-vectors[3])/2
            highest=0.
            for angle in (.137,.421,1.219,2.311):
                exact=np.array([self.angular(name,eta,y,p,generic,k,angle)[which][field] for field in fields])
                model=mean+cosine*np.cos(2*angle)+sine*np.sin(2*angle)
                highest=max(highest,float(np.max(abs(exact-model)/(1+abs(exact)))))
            checks.add(name+'_'+str(eta)+'_k'+str(k)+'_analytic_Fourier_support_'+str(which),highest<=1e-10,highest)
            out.append((mean,(cosine-1j*sine)/2))
        return out


class FullEuler:
    def __init__(self,generic):self.generic=generic;self.kernel=generic.GenericKernel();self.fields=generic.FIELDS;self.idx=generic.IDX

    def raw(self,y,p):return np.asarray(self.kernel.fun(self.kernel.values(y,p)),complex)

    def blocks(self,raw,k):
        LA,LB,LBT,LK=[np.zeros((22,22),complex) for _ in range(4)]
        weights=(1.,None,0.,0.,1j*k)
        for row,value in zip(self.kernel.records,raw):
            bi,i=divmod(row['row'],22);bj,j=divmod(row['column'],22)
            if bi!=1 and bj!=1:LA[i,j]+=np.conj(weights[bi])*value*weights[bj]
            elif bi!=1:LB[i,j]+=np.conj(weights[bi])*value
            elif bj!=1:LBT[i,j]+=value*weights[bj]
            else:LK[i,j]+=value
        return LA,LB,LBT,LK

    def coefficients(self,y,p,k,checks,label):
        rate=np.asarray(self.generic.bg.rhs(0,y,p),float);small=1e-24
        values=self.raw(y,p);directional=np.imag(self.raw(y.astype(complex)+1j*small*rate,p))/small
        h=1e-4
        numeric=(-self.raw(y+2*h*rate,p)+8*self.raw(y+h*rate,p)-8*self.raw(y-h*rate,p)+self.raw(y-2*h*rate,p))/(12*h)
        error=float(np.max(abs(numeric-directional)/(1+abs(directional))))
        checks.add(label+'_independent_coefficient_chain_rule',error<=1e-8,error)
        LA,LB,LBT,LK=self.blocks(values,k);dLA,dLB,dLBT,dLK=self.blocks(directional,k)
        EA=LA-dLBT-3*y[1]*LBT;EB=LB-LBT-dLK-3*y[1]*LK;ED=-LK
        return (LA,LB,LBT,LK),(EA,EB,ED)

    def response(self,y,p,k,source,source_dt,checks,label):
        blocks,euler=self.coefficients(y,p,k,checks,label);LA,LB,LBT,LK=blocks;EA,EB,ED=euler
        dynamics=tuple(self.fields[4:10]) if k==0 else ('Mxx','Mxy','Myy')
        dynamics+=tuple(self.fields[10:17]);auxiliary=('Z',) if k==0 else ('Sx','Sy','Sz','Z')
        F=np.zeros((22,len(dynamics)),complex);U=np.zeros((22,len(auxiliary)),complex)
        for j,name in enumerate(dynamics):F[self.idx[name],j]=1
        F[self.idx['alpha'],dynamics.index('Pi')]=-p['beta']
        for j,name in enumerate(auxiliary):U[self.idx[name],j]=1
        a,H=y[:2];MT=p['MP2']-p['MU2']*(p['c1']+p['c3']);cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
        inv=np.array([[1/p['b']]],complex) if k==0 else np.diag([2*a*a/(MT*k*k),2*a*a/(MT*k*k),-a*a/(cL*k*k),1/p['b']])
        invdot=inv*2*H
        invdot[-1,-1]=0.
        D=U.conj().T@LA@U;Ys=U.conj().T@LA@F;Vs=U.conj().T@LB@F
        checks.add(label+'_member_auxiliary_inverse',np.linalg.norm(D@inv-np.eye(len(auxiliary)),np.inf)<=1e-10)
        checks.add(label+'_auxiliary_no_acceleration_or_density_velocity',max(np.linalg.norm(LK@U,np.inf),np.linalg.norm(LB@U,np.inf))<=1e-10)
        Ms=-inv@Vs;Q1=U@Ms
        S=np.array([source[field] for field in self.fields],complex)
        Sd=np.array([source_dt[field] for field in auxiliary],complex)
        us=-U@inv@(U.conj().T@S)
        usd=-U@(invdot@(U.conj().T@S)+inv@Sd)
        Kr=F.conj().T@LK@F-Vs.conj().T@inv@Vs
        forcing=F.conj().T@(S+EA@us+EB@usd)
        acceleration=np.linalg.solve(Kr,forcing)
        q=us.copy();qd=Q1@acceleration+usd;qdd=F@acceleration
        alpha=self.idx['alpha'];em=self.idx['Em'];nu=self.idx['nu'];lm=self.idx['LambdaU'];dust=self.idx['T']
        residual=EA@q+EB@qd+ED@qdd+S
        q[em]=-residual[alpha]/EA[alpha,em]
        residual=EA@q+EB@qd+ED@qdd+S
        q[lm]=-residual[nu]/EA[nu,lm]
        residual=EA@q+EB@qd+ED@qdd+S
        qd[em]=-residual[dust]/EB[dust,em]
        pieces=(EA@q,EB@qd,ED@qdd,S);residual=sum(pieces)
        scale=max(sum(float(np.linalg.norm(term,np.inf)) for term in pieces),1e-30)
        error=float(np.linalg.norm(residual,np.inf)/scale)
        checks.add(label+'_all_22_sourced_Euler_equations',error<=1e-9,error)
        auxerror=float(np.linalg.norm((EA@q+EB@qd+ED@qdd+S)[[self.idx[n] for n in auxiliary]],np.inf)/scale)
        checks.add(label+'_unreduced_sourced_auxiliaries',auxerror<=1e-9,auxerror)
        if k==0:
            rows=[self.idx[n] for n in ('Sx','Sy','Sz')]
            mean_shift_norm=float(max(np.linalg.norm(EA[rows],np.inf),np.linalg.norm(EB[rows],np.inf),np.linalg.norm(ED[rows],np.inf)))
            checks.add(label+'_mean_shift_not_inverted',mean_shift_norm<=1e-10,mean_shift_norm)
        naive_error=float(np.linalg.norm(S,np.inf)/scale)
        drop_offset=float(np.linalg.norm(EA@(q-us)+EB@(qd-usd)+ED@qdd+S,np.inf)/scale)
        if np.linalg.norm(us,np.inf)>1e-14:
            checks.add(label+'_reject_dropped_affine_auxiliary_offset',drop_offset>1e-12,drop_offset)
        checks.add(label+'_reject_zero_everywhere_when_sourced',np.linalg.norm(S,np.inf)>0 and naive_error>1e-12,naive_error)
        def serial(vector):return np.stack((vector.real,vector.imag),axis=-1).tolist()
        return dict(mode=k,dynamics=list(dynamics),auxiliaries=list(auxiliary),
            response_fields=list(self.fields),response=serial(q),response_velocity=serial(qd),
            response_acceleration_used_by_Euler=serial(qdd),reduced_acceleration=serial(acceleration),
            full_source=serial(S),affine_auxiliary=serial(us),affine_auxiliary_dt=serial(usd),
            kinetic_eigenvalues=np.linalg.eigvalsh(Kr).tolist(),
            normalized_all_field_residual=error,residual_by_field=serial(residual/scale),
            normalization=scale,omitted_unconstrained_auxiliary_accelerations='not required by original Euler operator; not zero acceleration claims',
            scope='compatible initial coefficient data with free y=y_dot=0; not a time trajectory or physical energy classification')


def calculate():
    entry,generic,pins,paths,missing=pins_and_imports();before=entry.snapshot(paths);checks=Checks()
    src=Sources(checks);operator=FullEuler(generic);events=[];worst=0.
    for name in ('archived_G3','new_B1_frame','new_hierarchical'):
        for eta in generic.ETAS:
            p,y=entry.initial_conditions(generic,name,eta)
            for basek in (20,40,80):
                (s0,s2),(d0,d2)=src.fourier(name,eta,y,p,generic,basek,checks)
                fields=src.families[name]['source_order'];auxfields=src.families[name]['aux_order']
                for mode,S,Sd in ((0,s0,d0),(2*basek,s2,d2)):
                    label=name+'_'+str(eta)+'_k'+str(basek)+'_response'+str(mode)
                    data=operator.response(y,p,mode,dict(zip(fields,S)),dict(zip(auxfields,Sd)),checks,label)
                    worst=max(worst,data['normalized_all_field_residual'])
                    events.append(dict(family=name,eta=eta,base_coordinate_k=basek,time=0,**data))
                print(json.dumps(dict(stage='INITIAL_SOURCED_RESPONSE',family=name,eta=eta,k=basek)),flush=True)
    # Entire odd force branch retained by formula, independent of finite odd truncation.
    force={'full_degree_two_transverse_source':'-3*A*abs(psi_dot)^3*e*abs(e)*w*abs(w)*cos(kz)*abs(cos(kz))',
           'odd_source_coefficient':'-3*A*abs(psi_dot)^3*e*abs(e)*w*abs(w)*b_n',
           'b_n':'-8*(-1)^((n-1)/2)/(pi*n*(n^2-4)), positive odd n; even and mean zero',
           'compatible_initial_transverse_acceleration_coefficient':'S_Vy(n)/[MU2*(c1+c4)], initial free response zero',
           'forcing_L2_tail_squared_upper_bound':'[3*A*abs(psi_dot)^3*e*abs(e)*w*abs(w)]^2 * 128/(5*pi^2*N^5), N>=3',
           'scope':'infinite second-order force branch; no finite invariant manifold or evolved tail certificate'}
    for amplitude in (1.,-1.):
        direct=-3*.2*abs(.3)**3*amplitude*abs(amplitude)*(-.4)*abs(-.4)
        wrong=-3*.2*abs(.3)**3*amplitude**2*(-.4)*abs(-.4)
        checks.add('absolute_force_signed_amplitude_'+str(amplitude),direct>0 if amplitude>0 else direct<0,direct)
        if amplitude<0:checks.add('reject_even_amplitude_force_replacement',direct!=wrong)
    checks.add('all_108_mean_and_second_harmonic_events_retained',len(events)==108)
    checks.add('every_22field_response_row_retained',all(len(q['response'])==22 for q in events))
    checks.add('original_hash_size_mtime_preserved',entry.snapshot(paths)==before,dict(files=len(before)))
    forms={name:dict(sources={k:str(v) for k,v in data['sources'].items()},
                    auxiliary_source_dt={k:str(v) for k,v in data['auxiliary_source_dt'].items()},
                    shift=str(data['sigma']),vector_shell=str(data['vector_shell']),source_ward=src.wards[name])
           for name,data in src.families.items()}
    bodies={'formulas.json':encode(dict(families=forms,nonanalytic_force=force)),
            'initial_response.json':encode(dict(events=events,maximum_normalized_22field_residual=worst)),
            'controls.json':encode(dict(analytic_source_scope='generic original bivariate sources independently Euler-reconstructed before family specialization',
                    derivative_scope='raw REAL coefficient complex-step with independent five-point directional control',
                    response_scope='forced member-dependent auxiliary offset/time drift, density/normal/dust recovery; not time evolution',
                    field_order=list(generic.FIELDS)))}
    checks.add('V1_failed_attempt_retained',read(BASE+'r4c1_three_family_response_entry_attempt_01/summary.json')['validation']=='FAIL_LOCAL_CHECKS')
    checks.add('initial_response_bytes_IDENTICAL_to_V1',bodies['initial_response.json']==(ROOT/(BASE+'r4c1_three_family_response_entry_attempt_01/initial_response.json')).read_bytes())
    passed=sum(q['passed'] for q in checks.rows)
    holds=['Full time-dependent second-order response and controlled nonlinear remainder',
           'Complete nonlinear auxiliary/quartic physical reduction and finite-density eigenstate interactions',
           'Controlled continuous all-sector physical frequency/momentum band and healthy GR recovery',
           'Mean/fixed-charge/singular physical-energy sectors and full conformal-matter PPN',
           'Genuine identifying matter-residue and nonlinear-force matching; Stage 3 not entered']
    summary=dict(schema='r4c1-three-family-response-entry-v2',
        validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
        status='CONDITIONAL_COUPLED_INITIAL_RESPONSE_CHECKED_FULL_EVOLUTION_AND_DOMAIN_OPEN' if passed==len(checks.rows) else 'SOURCED_RESPONSE_FAILURE_REQUIRES_DISPOSITION',
        compatible_initial_response_verified=passed==len(checks.rows),full_second_order_response_solved=False,
        full_nonlinear_evolution_verified=False,full_coupled_interactions_computed=False,physical_EFT_cutoff_derived=False,
        physical_go=False,physical_decision='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',
        **{'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'},K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,
        preserved_v1_disposition='V1 958/964 retained FAIL: temporal chain rule introduced third mixed jets without the paired spatial derivatives. V2 completes the spatial map and commuting-derivative controls; no source, action, data or tolerance changed. All initial-response bytes must match V1.',
        artifacts={name:sha(body) for name,body in bodies.items()},substantive_unknowns=holds,
        review_dependencies=['THREE-FAMILY-NONANALYTIC-ENTRY','G3N4/FORCE-COVERAGE','G3N5','all inherited deferred review'],
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
    bodies['summary.json']=encode(summary)
    return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default=BASE+'r4c1_three_family_response_entry_attempt_02');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay directory absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output directory')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(sha(body)+'  '+name+'\n').encode():
                raise RuntimeError('Immutable replay mismatch: '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
          **{key:summary[key] for key in ('validation','passed','total','physics_pass','status')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
