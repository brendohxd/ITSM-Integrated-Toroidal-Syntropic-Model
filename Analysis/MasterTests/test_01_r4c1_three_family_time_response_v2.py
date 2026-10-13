"""V2: label-mapped evolving affine response; unchanged R4C1 physics/data."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import uuid

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import block_diag
from scipy.sparse import csr_matrix
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_three_family_response_entry_attempt_02/'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V1_CONTRACT_2026-10-12.md'
DISPOSITION='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V2_DISPOSITION_2026-10-12.md'
PINNED={
    DISPOSITION:'bbd822284f8ee7fe1d9b439420356e8b93ef1ca3ac3faebe2f982e26de706106',
    'Analysis/MasterTests/test_01_r4c1_three_family_time_response_v1.py':'4739598979d8d5e4f3d3b8c1dd818a2548017c92fd39fa3a955eff426463a084',
    CONTRACT:'28e0f0d199966f2ab6462a0eb49693198ed0628ad99cabe35d159da5b6488fb5',
    'Analysis/MasterTests/test_01_r4c1_three_family_response_entry_v2.py':'edf40da0c75f47d6e9a2e9b2386e524d30510d931f15dd21945645bf1cb55434',
    PARENT+'summary.json':'2ebf35fb122449725d8ebfbb4483d260eec5abe22f8ef6115627fe9798db64ad',
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_RESPONSE_ENTRY_V2_REPORT_2026-10-12.md':'332098904fbe1db9c862ae42b24810bb35d8f285560550e91fc56117ec8d29b3',
}
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
ETA=.25
WAVES=(20,40,80)
ODD=(1,3,5)
END=.05
TIMES=np.linspace(0,END,21)
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda v:(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
read=lambda name:json.loads((ROOT/name).read_bytes())
serial=lambda v:np.stack((np.asarray(v).real,np.asarray(v).imag),axis=-1).tolist()
PROGRESS=None


def progress(value):
    if PROGRESS is not None:
        with PROGRESS.open('ab') as stream:stream.write((json.dumps(value,sort_keys=True,allow_nan=False)+'\n').encode())
    print(json.dumps(value),flush=True)


def import_and_pin():
    for name,digest in PINNED.items():
        if sha((ROOT/name).read_bytes())!=digest:raise RuntimeError('Source drift: '+name)
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_three_family_response_entry_v2 as prior
    entry,generic,pins,_,_=prior.pins_and_imports()
    pins.update(PINNED);pins[SELF]=sha((ROOT/SELF).read_bytes())
    pins.update({PARENT+k:v for k,v in read(PARENT+'summary.json')['artifacts'].items()})
    paths=[];absent=[]
    for name,digest in pins.items():
        p=ROOT/name
        if sha(p.read_bytes())!=digest:raise RuntimeError('Inherited drift: '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0]!=digest:raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        else:absent.append(name)
    return prior,entry,generic,pins,paths,absent


class TimeSources:
    def __init__(self,prior,generic,checks):
        self.source=prior.Sources(checks);self.generic=generic;self.mass={};self.permutation={}
        for name in FAMILIES:
            q=self.source.families[name]
            order=q['source_order']
            checks.add(name+'_all22_source_label_bijection',len(order)==22 and len(set(order))==22 and set(order)==set(generic.FIELDS),order)
            self.permutation[name]=np.array([order.index(field) for field in generic.FIELDS])
            sentinel=np.arange(22);labelled=dict(zip(order,sentinel))
            expected=np.array([labelled[field] for field in generic.FIELDS])
            checks.add(name+'_independent_label_dictionary_sentinel',np.array_equal(sentinel[self.permutation[name]],expected))
            checks.add(name+'_reject_V1_positional_source_routing',not np.array_equal(sentinel,expected))
            expr=(q['m_w2'],q['c_V2'],self.source.dt(q['m_w2']))
            order=sorted(set(str(x) for z in expr for x in z.free_symbols))
            self.mass[name]=(order,s.lambdify([[self.source.x[x] for x in order]],expr,'numpy',cse=True))

    def context(self,name,y,p,w,wd,k):
        g=self.generic;rate=np.asarray(g.bg.rhs(0,y,p),float);h=1e-24
        second=np.imag(np.asarray(g.bg.rhs(0,y.astype(complex)+1j*h*rate,p),complex))/h
        a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=y;C=np.exp(p['beta']*psi)
        raw=dict(eta=ETA,a=a,H=H,Hdot=rate[1],Hddot=second[1],u0=u,v0=v,r0=r,
                 u_dot=ud,v_dot=vd,r_dot=rd,u_ddot=rate[3],v_ddot=rate[5],r_ddot=rate[7],
                 u_dddot=second[3],v_dddot=second[5],r_dddot=second[7],psi_dot=pd,
                 psi_ddot=rate[9],psi_dddot=second[9],C=C,C_dot=p['beta']*pd*C,
                 epsilon0=rho/C**4,epsilon_dot=(rate[10]-4*p['beta']*pd*rho)/C**4,
                 lambda0=3*p['MU2']*p['c2']*rate[1]-3*p['MU2']*(p['c1']+p['c3'])*H**2,
                 lambda_dot=3*p['MU2']*p['c2']*second[1]-6*p['MU2']*(p['c1']+p['c3'])*H*rate[1])
        order,fun=self.mass[name];mass,cv,massdot=(float(q) for q in fun([raw[z] for z in order]))
        omega2=cv*k*k/a**2+mass;wd2=-3*H*wd-omega2*w
        omega2dot=-2*H*cv*k*k/a**2+massdot
        wd3=-3*rate[1]*wd-3*H*wd2-omega2dot*w-omega2*wd
        return dict(raw=raw,rate=rate,mass=mass,cv=cv,omega2=omega2,w=w,wd=wd,wd2=wd2,wd3=wd3,k=k)

    def angular(self,name,c,theta):
        k=c['k'];co=np.cos(theta);si=np.sin(theta);w,wd,wd2,wd3=(c[q] for q in ('w','wd','wd2','wd3'))
        raw={**c['raw'],'W':w*co,'W_t':wd*co,'W_z':-k*w*si,'W_tt':wd2*co,
             'W_tz':-k*wd*si,'W_zz':-k*k*w*co,'W_ttt':wd3*co,'W_ttz':-k*wd2*si,'W_tzz':-k*k*wd*co}
        data=np.asarray(self.source.functions[name]([raw[z] for z in self.source.orders[name]]),complex)
        return np.r_[data[:22][self.permutation[name]],data[22:]]

    def fourier(self,name,c,checks=None,label=''):
        q=[self.angular(name,c,z) for z in (0,np.pi/2,np.pi/4,3*np.pi/4)]
        mean=(q[0]+q[1])/2;cosine=(q[0]-q[1])/2;sine=(q[2]-q[3])/2
        if checks is not None:
            error=0.
            for theta in (.137,.421,1.219,2.311):
                actual=self.angular(name,c,theta);fit=mean+cosine*np.cos(2*theta)+sine*np.sin(2*theta)
                error=max(error,float(np.max(abs(actual-fit)/(1+abs(actual)))))
            checks.add(label+'_evolving_exact_Fourier_support',error<=1e-10,error)
        return mean,(cosine-1j*sine)/2


class EvolvingReduction:
    def __init__(self,prior,generic):
        self.prior=prior;self.g=generic;self.op=prior.FullEuler(generic);self.cache={}
        records=self.op.kernel.records
        row=np.array([q['row'] for q in records]);col=np.array([q['column'] for q in records])
        self.jetrow,self.row=np.divmod(row,22);self.jetcol,self.col=np.divmod(col,22)

    def blocks(self,raw,k):
        weights=np.array([1.,0.,0.,0.,1j*k],complex);out=[np.zeros((22,22),complex) for _ in range(4)]
        masks=((self.jetrow!=1)&(self.jetcol!=1),(self.jetrow!=1)&(self.jetcol==1),
               (self.jetrow==1)&(self.jetcol!=1),(self.jetrow==1)&(self.jetcol==1))
        multipliers=(weights[self.jetrow].conj()*weights[self.jetcol],weights[self.jetrow].conj(),weights[self.jetcol],np.ones(len(raw)))
        for matrix,mask,mul in zip(out,masks,multipliers):
            np.add.at(matrix,(self.row[mask],self.col[mask]),raw[mask]*mul[mask])
        return out

    def at(self,bg,p,k,source,sd):
        rate=np.asarray(self.g.bg.rhs(0,bg,p),float);h=1e-24
        raw=self.op.raw(bg,p);derivative=np.imag(self.op.raw(bg.astype(complex)+1j*h*rate,p))/h
        LA,LB,LBT,LK=self.blocks(raw,k);dLA,dLB,dLBT,dLK=self.blocks(derivative,k)
        H=bg[1];EA=LA-dLBT-3*H*LBT;EB=LB-LBT-dLK-3*H*LK;ED=-LK
        dyn=tuple(self.g.FIELDS[4:10]) if k==0 else ('Mxx','Mxy','Myy')
        dyn+=tuple(self.g.FIELDS[10:17]);aux=('Z',) if k==0 else ('Sx','Sy','Sz','Z')
        F=np.zeros((22,len(dyn)),complex);U=np.zeros((22,len(aux)),complex)
        for j,n in enumerate(dyn):F[self.g.IDX[n],j]=1
        F[self.g.IDX['alpha'],dyn.index('Pi')]=-p['beta']
        for j,n in enumerate(aux):U[self.g.IDX[n],j]=1
        a=bg[0];MT=p['MP2']-p['MU2']*(p['c1']+p['c3']);cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
        inverse=np.array([[1/p['b']]],complex) if k==0 else np.diag([2*a*a/(MT*k*k),2*a*a/(MT*k*k),-a*a/(cL*k*k),1/p['b']])
        inverse_dt=2*H*inverse;inverse_dt[-1,-1]=0.
        Y=U.conj().T@LA@F;V=U.conj().T@LB@F;Yd=U.conj().T@dLA@F;Vd=U.conj().T@dLB@F
        Q0=F-U@inverse@Y;Q1=-U@inverse@V
        Q0d=-U@(inverse_dt@Y+inverse@Yd);Q1d=-U@(inverse_dt@V+inverse@Vd)
        S=np.asarray(source[:22],complex)
        auxindices=[self.g.IDX[n] for n in aux]
        # Stored source derivative order is Sx,Sy,Sz,Z; restrict it separately for mean.
        Sd=np.array([sd[('Sx','Sy','Sz','Z').index(n)] for n in aux],complex)
        us=-U@inverse@S[auxindices];usd=-U@(inverse_dt@S[auxindices]+inverse@Sd)
        K=F.conj().T@LK@F-V.conj().T@inverse@V
        Ar=F.conj().T@(EA@Q0+EB@Q0d);Br=F.conj().T@(EA@Q1+EB@(Q0+Q1d))
        forcing=F.conj().T@(S+EA@us+EB@usd)
        acceleration_matrix=np.linalg.solve(K,np.column_stack((Ar,Br,forcing)))
        n=len(dyn);AA=acceleration_matrix[:,:n];BB=acceleration_matrix[:,n:2*n];ff=acceleration_matrix[:,-1]
        G=np.block([[np.zeros((n,n)),np.eye(n)],[AA,BB]]);g=np.r_[np.zeros(n),ff]
        return dict(EA=EA,EB=EB,ED=ED,F=F,U=U,K=K,D=U.conj().T@LA@U,inverse=inverse,
                    Q0=Q0,Q1=Q1,Q0d=Q0d,Q1d=Q1d,us=us,usd=usd,S=S,G=G,g=g,dyn=dyn,aux=aux,
                    coefficient_dt=derivative,raw=raw,AA=AA,BB=BB,ff=ff)

    def reconstruct(self,data,state,p,checks=None,label=''):
        n=len(data['dyn']);y,yd=state[:n],state[n:];ydd=data['AA']@y+data['BB']@yd+data['ff']
        q=data['Q0']@y+data['Q1']@yd+data['us']
        qd=data['Q0d']@y+(data['Q0']+data['Q1d'])@yd+data['Q1']@ydd+data['usd']
        qdd=data['F']@ydd;EA,EB,ED,S=(data[z] for z in ('EA','EB','ED','S'))
        idx=self.g.IDX;alpha,em,nu,lm,dust=(idx[z] for z in ('alpha','Em','nu','LambdaU','T'))
        residual=EA@q+EB@qd+ED@qdd+S
        q[em]=-residual[alpha]/EA[alpha,em]
        residual=EA@q+EB@qd+ED@qdd+S;q[lm]=-residual[nu]/EA[nu,lm]
        residual=EA@q+EB@qd+ED@qdd+S;qd[em]=-residual[dust]/EB[dust,em]
        pieces=(EA@q,EB@qd,ED@qdd,S);scale=max(sum(np.linalg.norm(z,np.inf) for z in pieces),1e-30)
        residual=sum(pieces);error=float(np.linalg.norm(residual,np.inf)/scale)
        if checks is not None:
            checks.add(label+'_all22_sourced_equations',error<=1e-9,error)
            kinetic_identity=data['F'].conj().T@(EB@data['Q1']+ED@data['F'])+data['K']
            checks.add(label+'_exact_acceleration_reduction',np.linalg.norm(kinetic_identity,np.inf)/(1+np.linalg.norm(data['K'],np.inf))<=1e-10)
            checks.add(label+'_auxiliary_inverse',np.linalg.norm(data['D']@data['inverse']-np.eye(len(data['aux'])),np.inf)<=1e-10)
        return dict(q=q,qd=qd,qdd=qdd,ydd=ydd,residual=residual/scale,error=error,scale=float(scale))


def realify(z):return np.r_[z.real,z.imag]
def complexify(z):return z[:len(z)//2]+1j*z[len(z)//2:]


def run_case(name,k,method,src,red,entry,generic,checks):
    p,y0=entry.initial_conditions(generic,name,ETA)
    progress(dict(stage='INITIAL_MAPPING_CHECK',family=name,k=k,method=method))
    start=src.context(name,y0,p,1.,0.,k)
    for mode,so in zip((0,2*k),src.fourier(name,start)):
        data=red.at(y0,p,mode,so[:22],so[22:]);state=np.zeros(2*len(data['dyn']),complex)
        out=red.reconstruct(data,state,p,checks,name+'_k'+str(k)+'_'+method+'_initial_mode'+str(mode))
        old=next(q for q in read(PARENT+'initial_response.json')['events'] if q['family']==name and q['eta']==ETA and q['base_coordinate_k']==k and q['mode']==mode)
        expectedS=np.array(old['full_source'])[:,0]+1j*np.array(old['full_source'])[:,1]
        expectedQ=np.array(old['response'])[:,0]+1j*np.array(old['response'])[:,1]
        source_error=float(np.max(abs(expectedS-data['S'])/(1+abs(expectedS))))
        response_error=float(np.max(abs(expectedQ-out['q'])/(1+abs(expectedQ))))
        checks.add(name+'_k'+str(k)+'_'+method+'_mapped_initial_source_'+str(mode),source_error<=1e-10,source_error)
        checks.add(name+'_k'+str(k)+'_'+method+'_mapped_initial_response_'+str(mode),response_error<=1e-10,response_error)
        if max(source_error,response_error)>1e-10 or out['error']>1e-9:raise RuntimeError('Initial source/response mapping failed before integration')
    def first_rhs(t,z):
        c=src.context(name,z[:12],p,z[12],z[13],k)
        return np.r_[c['rate'],z[13],c['wd2']]
    first=solve_ivp(first_rhs,(0,END),np.r_[y0,1.,0.],method=method,rtol=1e-10,atol=1e-12,max_step=.001,dense_output=True)
    checks.add(name+'_k'+str(k)+'_'+method+'_first_mode_completed',first.success and first.t[-1]==END)
    if not first.success:raise RuntimeError('First-mode integration failed: '+first.message)
    progress(dict(stage='COUPLED_RESPONSE_INTEGRATION',family=name,k=k,method=method,first_order_complete=True))
    cache={}
    def contexts(t):
        if cache.get('t')==t:return cache['data']
        b=first.sol(t);c=src.context(name,b[:12],p,b[12],b[13],k);f0,f2=src.fourier(name,c)
        mean=red.at(b[:12],p,0,f0[:22],f0[22:]);second=red.at(b[:12],p,2*k,f2[:22],f2[22:])
        odd_source=[];odd_G=[];f2kin=p['MU2']*(p['c1']+p['c4'])
        for nn in ODD:
            bn=-8*(-1)**((nn-1)//2)/(np.pi*nn*(nn*nn-4))
            forcing=-3*p['A']*abs(b[9])**3*b[12]*abs(b[12])*bn/2
            odd_source.append(forcing)
            odd_G.append(np.array([[0,1],[-(c['cv']*(nn*k)**2/b[0]**2+c['mass']),-3*b[1]]]))
        G=block_diag(mean['G'],second['G'],*odd_G)
        force=np.r_[mean['g'],second['g'],*[[0.,q/f2kin] for q in odd_source]]
        cache.update(t=t,data=(b,c,mean,second,G,force,odd_source))
        return cache['data']
    def rhs(t,z):
        *_,G,force,oddsource=contexts(t)
        return realify(G@complexify(z)+force)
    def jac(t,z):
        G=contexts(t)[4]
        return csr_matrix(np.block([[G.real,-G.imag],[G.imag,G.real]]))
    size=contexts(0)[4].shape[0]
    options=dict(jac=jac) if method=='Radau' else {}
    response=solve_ivp(rhs,(0,END),np.zeros(2*size),(method),rtol=1e-10,atol=1e-12,max_step=.001,dense_output=True,**options)
    checks.add(name+'_k'+str(k)+'_'+method+'_response_completed',response.success and response.t[-1]==END,
               dict(message=response.message,nfev=response.nfev,njev=response.njev))
    if not response.success:raise RuntimeError('Response integration failed: '+response.message)
    rows=[];states=[];maxrho=0.;maxres=0.;maxdrift=0.;initial=None
    for ti,t in enumerate(TIMES):
        b,c,m,h,G,force,odd_source=contexts(float(t));z=complexify(response.sol(t));states.append(z)
        label=name+'_k'+str(k)+'_'+method+'_t'+str(ti)
        src.fourier(name,c,checks,label)
        channels=[(0,m,z[:26]),(2*k,h,z[26:46])]
        for j,nn in enumerate(ODD):
            S=np.zeros(22,complex);S[generic.IDX['Vy']]=odd_source[j]
            d=red.at(b[:12],p,nn*k,S,np.zeros(4));n=len(d['dyn']);state=np.zeros(2*n,complex)
            iy=d['dyn'].index('Vy');state[iy]=z[46+2*j];state[n+iy]=z[47+2*j]
            channels.append((nn*k,d,state))
        for mode,d,state in channels:
            tag=label+'_mode'+str(mode);out=red.reconstruct(d,state,p,checks,tag);maxres=max(maxres,out['error'])
            n=len(d['dyn']);flow=np.r_[state[n:],out['ydd']]
            if mode not in (0,2*k):
                iy=d['dyn'].index('Vy');nn=mode//k;j=ODD.index(nn)
                scalar_acceleration=-3*b[1]*state[n+iy]-(c['cv']*mode**2/b[0]**2+c['mass'])*state[iy]+odd_source[j]/(p['MU2']*(p['c1']+p['c4']))
                target=np.zeros(n,complex);target[iy]=scalar_acceleration
                error=float(np.max(abs(out['ydd']-target)/(1+abs(target))))
                checks.add(tag+'_odd_evolution_matches_FULL_coupled_reduction',error<=1e-9,error)
            # Numerical differentiation of recovered density along the joint autonomous flow.
            density_errors=[]
            for step in (1e-5,5e-6):
                densities=[]
                for multiple in (2,1,-1,-2):
                    shift=multiple*step;bb=b[:12]+shift*c['rate'];ww=b[12]+shift*b[13];wwd=b[13]+shift*c['wd2']
                    cc=src.context(name,bb,p,ww,wwd,k)
                    if mode in (0,2*k):
                        so=src.fourier(name,cc)[0 if mode==0 else 1];new=red.at(bb,p,mode,so[:22],so[22:])
                    else:
                        nn=mode//k;bn=-8*(-1)**((nn-1)//2)/(np.pi*nn*(nn*nn-4));SS=np.zeros(22,complex)
                        SS[generic.IDX['Vy']]=-3*p['A']*abs(bb[9])**3*ww*abs(ww)*bn/2
                        new=red.at(bb,p,mode,SS,np.zeros(4))
                    recovered=red.reconstruct(new,state+shift*flow,p)
                    densities.append(recovered['q'][generic.IDX['Em']])
                derivative=(-densities[0]+8*densities[1]-8*densities[2]+densities[3])/(12*step)
                error=float(abs(derivative-out['qd'][generic.IDX['Em']])/(1+abs(derivative)+abs(out['qd'][generic.IDX['Em']])))
                density_errors.append(error)
            maxrho=max(maxrho,*density_errors)
            checks.add(tag+'_recovered_density_ACTUAL_flow_derivative',max(density_errors)<=1e-7,density_errors)
            drop=out['residual']-d['EB']@(d['Q0d']@state[:n]+d['Q1d']@state[n:]+d['usd'])/out['scale']
            effect=float(np.linalg.norm(drop-out['residual'],np.inf));maxdrift=max(maxdrift,effect)
            rows.append(dict(time=float(t),mode=int(mode),all22_normalized_residual=out['error'],
                             density_derivative_errors=density_errors,response=serial(out['q']),velocity=serial(out['qd']),
                             residual_by_field=serial(out['residual']),kinetic_eigenvalues=np.linalg.eigvalsh(d['K']).tolist(),
                             omitted_drift_residual=effect))
            if t==0 and mode in (0,2*k):
                saved=read(PARENT+'initial_response.json')['events']
                old=next(q for q in saved if q['family']==name and q['eta']==ETA and q['base_coordinate_k']==k and q['mode']==mode)
                target=np.array(old['response'])[:,0]+1j*np.array(old['response'])[:,1]
                checks.add(tag+'_same_checked_initial_response',np.max(abs(target-out['q'])/(1+abs(target)))<=1e-10)
        if ti in (0,10,20):
            red.op.coefficients(b[:12],p,2*k,checks,label)
            reference=red.op.blocks(red.op.raw(b[:12],p),2*k)
            accelerated=red.blocks(red.op.raw(b[:12],p),2*k)
            blockerror=max(float(np.linalg.norm(x-y,np.inf)/(1+np.linalg.norm(x,np.inf))) for x,y in zip(reference,accelerated))
            checks.add(label+'_vectorized_blocks_match_original22_operator',blockerror<=1e-12,blockerror)
            # Nonzero scalar/metric trial data exercise general reduction beyond prepared y=yd=0.
            for mode,d,_ in channels[:2]:
                n=len(d['dyn']);state=(np.arange(2*n)+1)*1e-4*(1+.37j)
                trial=red.reconstruct(d,state,p,checks,label+'_trial_mode'+str(mode))
                # Deliberate omission controls use actual unreduced fields, never a relabelled checker.
                for field,velocity in (('Em',False),('LambdaU',False),('alpha',False),('Em',True)):
                    q=trial['q'].copy();qd=trial['qd'].copy();index=generic.IDX[field]
                    removed=qd[index] if velocity else q[index]
                    if velocity:qd[index]=0
                    else:q[index]=0
                    residual=d['EA']@q+d['EB']@qd+d['ED']@trial['qdd']+d['S']
                    error=float(np.linalg.norm(residual,np.inf)/trial['scale'])
                    if abs(removed)>1e-12:
                        checks.add(label+'_reject_omitted_'+field+('_velocity' if velocity else '')+'_mode'+str(mode),error>1e-12,error)
                if mode==0:
                    q=trial['q'].copy();q[[generic.IDX[f] for f in ('Mxz','Myz','Mzz')]]=0
                    error=float(np.linalg.norm(d['EA']@q+d['EB']@trial['qd']+d['ED']@trial['qdd']+d['S'],np.inf)/trial['scale'])
                    checks.add(label+'_reject_omitted_mean_metric_coordinates',error>1e-12,error)
                if np.linalg.norm(d['us'])>1e-14:
                    residual=d['EA']@(trial['q']-d['us'])+d['EB']@(trial['qd']-d['usd'])+d['ED']@trial['qdd']+d['S']
                    error=float(np.linalg.norm(residual,np.inf)/trial['scale'])
                    checks.add(label+'_reject_omitted_affine_offset_mode'+str(mode),error>1e-12,error)
    checks.add(name+'_k'+str(k)+'_'+method+'_reject_omitted_affine_basis_drift',maxdrift>1e-12,maxdrift)
    ph=generic.bg.physics(first.sol(TIMES)[:12],p)
    checks.add(name+'_k'+str(k)+'_'+method+'_background_constraint_preserved',np.max(ph['constraint_norm'])<=1e-8,float(np.max(ph['constraint_norm'])))
    return dict(family=name,eta=ETA,k=k,method=method,rows=rows,states=serial(np.array(states)),
                first_order_states=first.sol(TIMES).T.tolist(),maximum_all22_residual=maxres,
                maximum_density_derivative_error=maxrho,nfev=response.nfev,njev=response.njev,
                scope='finite perturbative coefficient trajectories; infinite odd evolved tail and nonlinear remainder NOT certified')


def calculate():
    prior,entry,generic,pins,paths,missing=import_and_pin();before=entry.snapshot(paths);checks=prior.Checks()
    src=TimeSources(prior,generic,checks);red=EvolvingReduction(prior,generic);runs=[]
    for name in FAMILIES:
        for k in WAVES:
            pair=[]
            for method in ('DOP853','Radau'):
                run=run_case(name,k,method,src,red,entry,generic,checks);pair.append(run);runs.append(run)
                progress(dict(stage='TIME_RESPONSE',family=name,k=k,method=method,
                              residual=run['maximum_all22_residual'],density_derivative=run['maximum_density_derivative_error']))
            aa=np.array(pair[0]['states']);bb=np.array(pair[1]['states'])
            error=float(np.max(abs(aa-bb)/(1+abs(aa))))
            checks.add(name+'_k'+str(k)+'_two_method_trajectory_agreement',error<=1e-7,error)
    checks.add('all_original_hash_size_mtime_preserved',entry.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(q['passed'] for q in checks.rows)
    forms=dict(affine_reconstruction='q=Q0*y+Q1*y_dot+u_s; all basis/inverse/source drift retained',
               infinite_odd_forcing='S_Vy(n)=-3*A*abs(psi_dot)^3*w*abs(w)*b_n/2, b_n=-8*(-1)^((n-1)/2)/(pi*n*(n^2-4)), n odd',
               exact_infinite_odd_response='x_n(t)=Integral_0^t Phi_n(t,s)[0,S_Vy(n,s)/alpha14] ds; Phi_n evolves the member vector equation',
               evolved_tail='UNCONTROLLED; retained formula is NOT a tail/remainder certificate',
               first_order='w_ddot+3H*w_dot+(cV^2*k^2/a^2+m_w^2)*w=0',
               scope='registered finite diagnostic subset and perturbative order only')
    bodies={'trajectories.json':encode(dict(runs=runs)), 'formulas.json':encode(forms),
            'controls.json':encode(dict(time=list(TIMES),eta=ETA,waves=list(WAVES),odd_modes=list(ODD),
                        numerical_methods=['DOP853','Radau'],rtol=1e-10,atol=1e-12,max_step=.001,
                        density_difference_steps=[1e-5,5e-6],certified_continuous_error=False))}
    summary=dict(schema='r4c1-three-family-time-response-v2',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
                 passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='CONDITIONAL_FINITE_TIME_RESPONSE_CHECKED_FULL_DOMAIN_OPEN' if passed==len(checks.rows) else 'TIME_RESPONSE_FAILURE_REQUIRES_DISPOSITION',
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',physical_go=False,
                 stage2_complete=False,stage3_entered=False,physical_decision='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',
                 full_second_order_response_solved=False,full_coupled_interactions_computed=False,
                 certified_continuous_error=False,nonlinear_remainder_controlled=False,physical_EFT_cutoff_derived=False,
                 canonical_tests_1_to_3='HOLD_SUBSTANTIVE',**{'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'},
                 K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),
                 source_metadata_preserved=len(before),inherited_sidecars_absent=missing,
                 preserved_v1_disposition='V1 intentionally interrupted for missing source-label permutation. Source/sidecar retained; no completed receipt or validation counts. V2 maps all22 labels explicitly; earlier response-entry V2 unchanged.',
                 substantive_unknowns=['Infinite odd evolved tail and nonlinear remainder','All-eta/all-sector continuous physical frequency/momentum window',
                                      'Complete physical energy/fixed-charge/singular/quartic interacting reduction','Healthy GR/full PPN','Genuine identifying matter-residue and nonlinear-force matching'],
                 review_dependencies=['THREE-FAMILY-RESPONSE-ENTRY-V2','all inherited deferred review'],
                 artifacts={n:sha(b) for n,b in bodies.items()},
                 runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
    bodies['summary.json']=encode(summary)
    return bodies,summary


def main():
    global PROGRESS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_three_family_time_response_attempt_02');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Missing replay directory')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing receipt directory')
    PROGRESS=ROOT/'.local/itsm-context'/('time-response-v2-progress-'+uuid.uuid4().hex+'.jsonl')
    with PROGRESS.open('xb') as stream:stream.write((json.dumps(dict(stage='LAUNCH_UNVERIFIED',source=SELF,source_sha256=sha((ROOT/SELF).read_bytes()),replay=bool(args.replay)),sort_keys=True)+'\n').encode())
    bodies,j=calculate()
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(sha(b)+'  '+n+'\n').encode():raise RuntimeError('Immutable replay mismatch: '+n)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for n,b in bodies.items():
            with (dest/n).open('xb') as stream:stream.write(b)
            with (dest/(n+'.sha256')).open('xb') as stream:stream.write((sha(b)+'  '+n+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
                         validation=j['validation'],passed=j['passed'],total=j['total'],physics_pass=False,status=j['status'])))
    for q in j['checks']:
        if not q['passed']:print(json.dumps(q))
    return int(j['passed']!=j['total'])


if __name__=='__main__':raise SystemExit(main())
