"""Unprojected |e|^3 mean/first-even evolution; no physical-window clearance."""
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
from scipy.integrate import solve_ivp
from scipy.linalg import block_diag
from scipy.optimize import brentq
from scipy.sparse import csr_matrix
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
PARENT = BASE+'r4c1_cusp3_local_initial_jet_attempt_02/'
RET = BASE+'r4c1_fixed_charge_retarded_comparison_attempt_03/'
PLANAR = BASE+'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_EVOLUTION_V1_CONTRACT_2026-10-16.md'
REPORT = 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_LOCAL_INITIAL_JET_V2_REPORT_2026-10-16.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
          'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX = {n:i for i,n in enumerate(FIELDS)}
AUX = ('Sx','Sy','Sz','Z')
WAVES = ('W','W_t','W_z','W_tt','W_tz','W_zz','W_ttt','W_ttz','W_tzz')
K = 40
TIMES = np.linspace(0.,.05,21)
SHA = lambda b:hashlib.sha256(b).hexdigest()
READ = lambda p:json.loads((ROOT/p).read_bytes())
ENCODE = lambda o:(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CLEAN = lambda e:s.factor(s.cancel(s.expand(e)))
SER = lambda z:np.stack((np.asarray(z).real,np.asarray(z).imag),axis=-1).tolist()
UNSER = lambda z:np.asarray(z)[...,0]+1j*np.asarray(z)[...,1]


class Checks:
    def __init__(self):self.rows=[];self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names:raise ValueError('Duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def small(self,name,value,tol):self.add(name,abs(value)<=tol,float(abs(value)),'<= '+str(tol))
    def exact(self,name,value):
        values=list(value) if isinstance(value,(list,tuple,s.MatrixBase)) else [value]
        bad=[dict(index=i,residual=str(v)) for i,q in enumerate(values) if (v:=CLEAN(q))!=0]
        self.add(name,not bad,bad,'zero_exact')


def inputs():
    parent=READ(PARENT+'summary.json')
    if SHA((ROOT/(PARENT+'summary.json')).read_bytes())!='e3b7146960b8ce2d46eed1178204902659625bb06ef6c41763fea5ecbe2e82a1':
        raise RuntimeError('Parent summary drift')
    pins=dict(parent['source_sha256'])
    pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins[PARENT+'summary.json']='e3b7146960b8ce2d46eed1178204902659625bb06ef6c41763fea5ecbe2e82a1'
    pins[REPORT]='2ef24a3cd6edc6eacbf4a549e94009222e27abffcb56bfa4234586b2f8f42000'
    pins.update({p:SHA((ROOT/p).read_bytes()) for p in (CONTRACT,SELF)})
    absent=parent['inherited_sidecars_absent'];paths=[]
    for name,expected in pins.items():
        p=ROOT/name
        if SHA(p.read_bytes())!=expected:raise RuntimeError('Frozen source drift: '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=expected:raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        elif name not in absent:raise RuntimeError('Required sidecar absent: '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_gr_family_survey_v2 as generic
    import test_01_r4c1_three_family_response_entry_v2 as prior
    import test_01_r4c1_three_family_time_response_v2 as time
    return pins,absent,snapshot,generic,prior,time


class Sources:
    """Sparse generic quadratic polarization, compiled before family choice."""
    def __init__(self,ch):
        print('Compile generic mixed sources and all-time Ward identities',flush=True)
        planar=READ(PLANAR)
        texts=[*planar['Euler_sources_before_shift'].values(),planar['generic_frame_mass_squared'],
               planar['generic_cV2'],planar['quadratic_vector_action']]
        names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts)))
        names.update(('A','Hddot','psi_dddot','u_dddot','v_dddot','r_dddot','C_dot',
                      'epsilon_dot','lambda_dot',*WAVES))
        names.update('a H Hdot psi_dot psi_ddot u0 u_dot u_ddot v0 v_dot v_ddot r0 r_dot r_ddot C epsilon0 lambda0'.split())
        for n in list(names):
            if n=='B' or n.startswith('B_'):names.add('W'+n[1:])
        self.x=x={n:s.Symbol(n,real=True) for n in names}
        mapping=dict(a='a*H',H='Hdot',Hdot='Hddot',psi_dot='psi_ddot',psi_ddot='psi_dddot',
                     W='W_t',W_t='W_tt',W_z='W_tz',W_tt='W_ttt',W_tz='W_ttz',W_zz='W_tzz',
                     u0='u_dot',v0='v_dot',r0='r_dot',u_dot='u_ddot',v_dot='v_ddot',
                     r_dot='r_ddot',C='C_dot',epsilon0='epsilon_dot',lambda0='lambda_dot')
        self.mapping={x[n]:s.sympify(rate,locals=x) for n,rate in mapping.items()}
        def dt(expr):return s.expand(sum(s.diff(expr,z)*rate for z,rate in self.mapping.items() if z in expr.free_symbols))
        self.dt=dt
        sigma=-x['MU2']*(x['c1']+x['c3'])/(x['MP2']-x['MU2']*(x['c1']+x['c3']))
        shift={x[n]:sigma*x['W'+n[1:]] for n in names if n=='B' or n.startswith('B_')}
        spatial_zero={x[n]:0 for n in names if n.startswith('W_') and ('x' in n or 'y' in n)}
        src={n:s.expand(s.sympify(planar['Euler_sources_before_shift'][n],locals=x).xreplace(shift).xreplace(spatial_zero)) for n in FIELDS}
        ch.add('exact22_field_routing',tuple(planar['field_order'])==FIELDS)
        f2=x['MU2']*(x['c1']+x['c4'])
        mass=s.sympify(planar['generic_frame_mass_squared'],locals=x)
        cv=s.sympify(planar['generic_cV2'],locals=x)
        EW=-f2*(x['W_tt']+3*x['H']*x['W_t']+mass*x['W']-cv*x['W_zz']/x['a']**2)
        dzmap={x[n]:x[d] for n,d in dict(W='W_z',W_t='W_tz',W_z='W_zz',W_tt='W_ttz',W_tz='W_tzz').items()}
        def dz(expr):return s.expand(sum(s.diff(expr,z)*rate for z,rate in dzmap.items() if z in expr.free_symbols))
        temporal=-dt(src['alpha'])-3*x['H']*src['alpha']
        temporal+=2*x['H']*sum(src[n] for n in ('Mxx','Myy','Mzz'))+dz(src['Sz']+src['Vz'])/x['a']
        for field,rate in [('du','u_dot'),('dv','v_dot'),('dr','r_dot'),('Pi','psi_dot'),
                           ('T','C'),('Em','epsilon_dot'),('LambdaU','lambda_dot')]:temporal+=x[rate]*src[field]
        ch.exact('generic_offshell_temporal_source_Ward',temporal-(x['H']*x['W']-x['W_t'])*EW)
        ch.exact('generic_offshell_longitudinal_source_Ward',x['a']*(dt(src['Sz'])+4*x['H']*src['Sz'])+2*dz(src['Mzz'])-x['W_z']*EW)
        expressions=[src[n] for n in FIELDS]+[dt(src[n]) for n in ('alpha',*AUX)]
        records=[];coeff=[]
        for row,expr in enumerate(expressions):
            poly=s.Poly(expr,*[x[n] for n in WAVES]);reconstructed=0
            for powers,c in poly.terms():
                if c==0:continue
                if sum(powers)!=2:raise ValueError('Nonquadratic wave source')
                indices=[i for i,q in enumerate(powers) for _ in range(q)]
                records.append((row,*indices));coeff.append(c)
                reconstructed+=c*s.prod(x[n]**power for n,power in zip(WAVES,powers))
            ch.exact('source_polynomial_binding_'+str(row),expr-reconstructed)
        self.row,self.i,self.j=np.asarray(records,int).T
        self.order=sorted({str(q) for e in coeff for q in e.free_symbols})
        ch.add('no_wave_jet_in_compiled_background_coefficients',not set(self.order)&set(WAVES))
        self.fun=s.lambdify([[x[n] for n in self.order]],coeff,'numpy',cse=True)
        self.mass_order=sorted({str(q) for e in (mass,cv,dt(mass)) for q in e.free_symbols})
        self.mass_fun=s.lambdify([[x[n] for n in self.mass_order]],[mass,cv,dt(mass)],'numpy',cse=True)
        self.export=dict(wave_order=list(WAVES),mixed_source_rule='sum c_ij*(first_i*cusp_j+cusp_i*first_j)',
            sparse_coefficients=[dict(row=int(r),i=int(i),j=int(j),coefficient=str(c)) for (r,i,j),c in zip(records,coeff)],
            source_order=list(FIELDS),derivative_order=['alpha',*AUX],generic_mass=str(mass),generic_cv=str(cv),
            generic_temporal_Ward='(H*W-W_t)*EW',generic_longitudinal_Ward='W_z*EW',
            odd_input_modes=[1,3],even_output_modes=[0,2],zero_mode_separate=True,
            missing_global_tail_bound=True)
        ch.add('exact_integer_mode_neighbour_selection',
               {abs(n-sign) for n in (0,2) for sign in (-1,1)}=={1,3})
        ch.add('reject_global_two_mode_closure',abs(4-(-1)) not in (1,3))

    def context(self,g,red,b,p):
        bg=b[:12];rate=np.asarray(g.bg.rhs(0,bg,p),float)
        second=np.imag(np.asarray(g.bg.rhs(0,bg.astype(complex)+1j*1e-24*rate,p),complex))/1e-24
        raw=dict(zip(red.op.kernel.order,red.op.kernel.values(bg,p)))
        a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=bg;C=np.exp(p['beta']*psi)
        raw.update(p,K_Q=p['K'],a=a,H=H,Hdot=rate[1],Hddot=second[1],u0=u,v0=v,r0=r,
            u_dot=ud,v_dot=vd,r_dot=rd,u_ddot=rate[3],v_ddot=rate[5],r_ddot=rate[7],
            u_dddot=second[3],v_dddot=second[5],r_dddot=second[7],psi_dot=pd,psi_ddot=rate[9],
            psi_dddot=second[9],C=C,C_dot=p['beta']*pd*C,epsilon0=rho/C**4,
            epsilon_dot=(rate[10]-4*p['beta']*pd*rho)/C**4,
            lambda0=3*p['MU2']*p['c2']*rate[1]-3*p['MU2']*(p['c1']+p['c3'])*H**2,
            lambda_dot=3*p['MU2']*p['c2']*second[1]-6*p['MU2']*(p['c1']+p['c3'])*H*rate[1])
        mass,cv,md=np.asarray(self.mass_fun([raw[n] for n in self.mass_order]),float)
        w,wd=b[12:];omega=cv*K*K/a**2+mass
        wdd=-3*H*wd-omega*w
        wddd=-3*rate[1]*wd-3*H*wdd-(-2*H*cv*K*K/a**2+md)*w-omega*wd
        return dict(raw=raw,rate=rate,mass=mass,cv=cv,md=md,w=w,wd=wd,wdd=wdd,wddd=wddd,
                    coefficients=np.asarray(self.fun([raw[n] for n in self.order]),complex))

    def polarize(self,c,left,right):
        product=left[self.i,None]*right[self.j]+left[self.j,None]*right[self.i]
        out=np.zeros((27,right.shape[1]),complex)
        np.add.at(out,self.row,c['coefficients'][:,None]*product)
        return out

    def source(self,c,b,p,mode,scale):
        # Column0 is the affine offset; columns1..4 are scaled lower odd states.
        a,H=b[:2];pd=b[9];pdd=c['rate'][9];w,wd=c['w'],c['wd']
        f2=p['MU2']*(p['c1']+p['c4'])
        odd=np.zeros((4,5));odd[0,2]=1;odd[2,4]=1
        jets={};oddforce=[]
        for j,n in enumerate((1,3)):
            r=np.zeros(5);r[1+2*j]=1;rd=np.zeros(5);rd[2+2*j]=1
            cn=-4*(-1)**((n-1)//2)/(np.pi*n*(n*n-4))
            force=-3*p['A']*abs(pd)**3*w*abs(w)*cn/(f2*scale)
            forced=-3*p['A']*cn*(3*pd*abs(pd)*pdd*w*abs(w)+2*abs(pd)**3*abs(w)*wd)/(f2*scale)
            omega=c['cv']*(n*K)**2/a**2+c['mass']
            omegad=-2*H*c['cv']*(n*K)**2/a**2+c['md']
            rdd=-omega*r-3*H*rd;rdd[0]+=force
            rddd=-3*c['rate'][1]*rd-3*H*rdd-omegad*r-omega*rd;rddd[0]+=forced
            odd[2*j+1]=rdd;oddforce.append(force)
            for signed in (n,-n):
                q=signed*K
                jets[signed]=np.stack((r,rd,1j*q*r,rdd,1j*q*rd,-q*q*r,rddd,1j*q*rdd,-q*q*rd))
        full=np.zeros((27,5),complex)
        for sign in (-1,1):
            n=mode-sign
            if n not in jets:raise RuntimeError('Missing required Fourier neighbour')
            q=sign*K
            first=np.array([w,wd,1j*q*w,c['wdd'],1j*q*wd,-q*q*w,
                            c['wddd'],1j*q*c['wdd'],-q*q*wd],complex)/2
            full+=self.polarize(c,first,jets[n])
        m=mode//2;hm=12*(-1)**m/(np.pi*(4*m*m-1)*(4*m*m-9))
        direct=np.zeros(27,complex);X=p['A']*abs(pd)**3*abs(w)**3*hm/scale
        direct[IX['alpha']]=2*X
        for n in ('Mxx','Mzz'):direct[IX[n]]=-X/2
        direct[IX['Myy']]=-2*X
        direct[IX['Pi']]=3*p['A']*((2*abs(pd)*pdd+3*H*pd*abs(pd))*abs(w)**3+
            3*pd*abs(pd)*w*abs(w)*wd)*hm/scale
        direct[22]=6*p['A']*(pd*abs(pd)*pdd*abs(w)**3+abs(pd)**3*w*abs(w)*wd)*hm/scale
        mixed=full.copy();full[:,0]+=direct
        return full,odd,dict(jets=jets,mixed=mixed,direct=direct,oddforce=oddforce)


class System:
    def __init__(self,run,p,first,src,red,g):
        self.run=run;self.p=p;self.first=first;self.src=src;self.red=red;self.g=g
        self.eta=float(s.Rational(run['eta_exact']));self.scale=self.eta**3.5
        self.cache={};self.calls=0

    def at(self,t):
        if self.cache.get('t')==t:return self.cache['data']
        b=self.first.sol(t);c=self.src.context(self.g,self.red,b,self.p)
        datas=[];sources=[];extras=[];maps=[]
        for mode in (0,2):
            full,odd,extra=self.src.source(c,b,self.p,mode,self.scale)
            d=self.red.at(b[:12],self.p,mode*K,np.zeros(22),np.zeros(4))
            ai=[IX[n] for n in d['aux']];di=[AUX.index(n) for n in d['aux']]
            invd=2*b[1]*d['inverse'];invd[-1,-1]=0.
            us=-d['U']@d['inverse']@full[ai]
            usd=-d['U']@(invd@full[ai]+d['inverse']@full[23+np.asarray(di)])
            ff=np.linalg.solve(d['K'],d['F'].conj().T@(full[:22]+d['EA']@us+d['EB']@usd))
            maps.append(dict(us=us,usd=usd,ff=ff));datas.append(d);sources.append(full);extras.append(extra)
        Gc=block_diag(*[d['G'] for d in datas]);B=np.zeros((46,5),complex)
        B[13:26]=maps[0]['ff'];B[36:46]=maps[1]['ff']
        G=np.zeros((96,96));force=np.zeros(96)
        G[:4,:4]=odd[:,1:];force[:4]=odd[:,0]
        G[4:50,:4]=B[:,1:].real;G[50:,:4]=B[:,1:].imag
        G[4:50,4:50]=Gc.real;G[4:50,50:]=-Gc.imag
        G[50:,4:50]=Gc.imag;G[50:,50:]=Gc.real
        force[4:50]=B[:,0].real;force[50:]=B[:,0].imag
        out=dict(b=b,c=c,G=G,force=force,datas=datas,sources=sources,maps=maps,extras=extras)
        self.cache=dict(t=t,data=out);return out

    def rhs(self,t,z):
        data=self.at(t);self.calls+=1
        if self.calls%2000==0:print(json.dumps(dict(stage='EVOLVING',family=self.run['family'],eta=self.run['eta_exact'],method=self.run['method'],calls=self.calls,t=float(t))),flush=True)
        return data['G']@z+data['force']

    def jac(self,t,z):return csr_matrix(self.at(t)['G'])

    def reconstruct(self,t,z,j):
        d=self.at(t);aff=np.r_[1.,z[:4]];base=d['datas'][j];mp=d['maps'][j]
        data={**base,'us':mp['us']@aff,'usd':mp['usd']@aff,'ff':mp['ff']@aff,
              'S':d['sources'][j][:22]@aff}
        zz=z[4:50]+1j*z[50:];state=zz[:26] if j==0 else zz[26:]
        return self.red.reconstruct(data,state,self.p),data,d['sources'][j]@aff


def diagnostics(sys,t,z):
    d=sys.at(t);b,c,p=d['b'],d['c'],sys.p;aff=np.r_[1.,z[:4]]
    residuals=[];wards=[];lapse=[];conditions=[];outs=[]
    for j,mode in enumerate((0,2)):
        out,data,source=sys.reconstruct(t,z,j);q,qd,qdd=out['q'],out['qd'],out['qdd'];outs.append(out)
        S=source[:22];Sd=source[23:]
        temp=-source[22]-3*b[1]*S[0]+2*b[1]*sum(S[IX[n]] for n in ('Mxx','Myy','Mzz'))
        temp+=1j*mode*K*(S[IX['Sz']]+S[IX['Vz']])/b[0]
        for n,rate in [('du',b[3]),('dv',b[5]),('dr',b[7]),('Pi',b[9]),
                       ('T',c['raw']['C']),('Em',c['raw']['epsilon_dot']),('LambdaU',c['raw']['lambda_dot'])]:temp+=rate*S[IX[n]]
        long=b[0]*(Sd[2]+4*b[1]*S[IX['Sz']])+2j*mode*K*S[IX['Mzz']]
        norm=max(np.linalg.norm(source,np.inf),1e-30)
        wards.append(max(abs(temp),abs(long))/norm)
        LA,LB,_,_=sys.red.blocks(data['raw'],mode*K)
        dLA,dLB,_,_=sys.red.blocks(data['coefficient_dt'],mode*K)
        v=qd.copy();v[IX['Em']]=0
        graph=-(dLA[0]@q+LA[0]@v+dLB[0]@qd+LB[0]@qdd+source[22])/LA[0,IX['Em']]
        graphscale=max(abs(graph),abs(qd[IX['Em']]),out['scale'],1e-30)
        lapse.append(abs(graph-qd[IX['Em']])/graphscale)
        residuals.append(out['error']);conditions.append(float(np.linalg.cond(data['K'])))
        if j==0:mean_graph=graph
    q,qd,qdd=(outs[0][n] for n in ('q','qd','qdd'))
    a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=b[:12];rate=c['rate'];C=c['raw']['C']
    J=u*vd-v*ud;Jd=u*rate[5]-v*rate[3];R2=u*u+v*v;R2d=2*(u*ud+v*vd)
    tr=sum(q[IX[n]] for n in ('Mxx','Myy','Mzz'))/2
    trd=sum(qd[IX[n]] for n in ('Mxx','Myy','Mzz'))/2
    dj=u*qd[IX['dv']]+q[IX['du']]*vd-v*qd[IX['du']]-q[IX['dv']]*ud
    djd=u*qdd[IX['dv']]+q[IX['du']]*rate[5]-v*qdd[IX['du']]-q[IX['dv']]*rate[3]
    linear=dj+(tr-q[0])*J
    lineard=djd+(trd-qd[0])*J+(tr-q[0])*Jd
    # All quantities here are coefficients divided by eta^(7/2), including r1.
    offset=-2*a**3*p['zeta']*R2*J*c['w']*z[0]
    offsetd=-2*a**3*p['zeta']*((3*H*R2*J+R2d*J+R2*Jd)*c['w']*z[0]+
                R2*J*(c['wd']*z[0]+c['w']*z[1]))
    Q=a**3*linear+offset;Qd=a**3*(3*H*linear+lineard)+offsetd
    clock=tr-q[0]+2*p['beta']*q[IX['Pi']]+qd[IX['T']]/C
    clockd=trd-qd[0]+2*p['beta']*qd[IX['Pi']]+qdd[IX['T']]/C-qd[IX['T']]*p['beta']*pd/C
    P=a**3*C**3*q[IX['Em']]+a**3*rho/C*clock
    Pd=a**3*C**3*(mean_graph+3*(H+p['beta']*pd)*q[IX['Em']])
    Pd+=a**3*rho/C*(clockd+(3*H+rate[10]/rho-p['beta']*pd)*clock)
    MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
    MT=p['MP2']-p['MU2']*(p['c1']+p['c3']);f2=p['MU2']*(p['c1']+p['c4'])
    cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
    regular=min(a,H,rho,pd,MC,MT,f2,p['b'],p['K'],R2)>0 and cL!=0
    qscale=max(1.,abs(a**3*J));pscale=max(1.,abs(a**3*rho/C))
    return dict(t=float(t),full22_residual=max(residuals),source_Ward=max(wards),
        independent_lapse_drift=max(lapse),Q3_scaled=SER(Q),P3_scaled=SER(P),
        Q3dot_scaled=SER(Qd),P3dot_scaled=SER(Pd),mixed_angular_offset_scaled=float(offset),
        charge_value=max(abs(Q)/qscale,abs(P)/pscale),charge_derivative=max(abs(Qd)/qscale,abs(Pd)/pscale),
        regular=bool(regular),kinetic_condition=max(conditions))


def quadrature_control(sys,t,z,ch,label):
    d=sys.at(t);c=d['c'];aff=np.r_[1.,z[:4]]
    # Quadratic trigonometric polynomial has maximum harmonic 4; 32-point DFT is exact up to roundoff.
    theta=np.arange(32)*2*np.pi/32;values=[]
    for angle in theta:
        first=np.zeros(9,complex);cusp=np.zeros((9,1),complex)
        for sign in (-1,1):
            q=sign*K
            first+=np.array([c['w'],c['wd'],1j*q*c['w'],c['wdd'],1j*q*c['wd'],-q*q*c['w'],
                c['wddd'],1j*q*c['wdd'],-q*q*c['wd']])*np.exp(1j*sign*angle)/2
        for mode,jets in d['extras'][0]['jets'].items():cusp[:,0]+=(jets@aff)*np.exp(1j*mode*angle)
        values.append(sys.src.polarize(c,first,cusp)[:,0])
    values=np.asarray(values)
    for j,mode in enumerate((0,2)):
        direct=np.mean(values*np.exp(-1j*mode*theta[:,None]),axis=0)
        expected=d['extras'][j]['mixed']@aff
        err=float(np.max(abs(direct-expected)/(1+abs(direct)+abs(expected))))
        ch.small(label+'_DFT_mixed_'+str(mode),err,1e-10)


def run_case(run,src,red,g,ch):
    name,ef,method=run['family'],float(s.Rational(run['eta_exact'])),run['method']
    label=name+'_'+run['eta_exact']+'_'+method
    print(json.dumps(dict(stage='START_CASE',case=label)),flush=True)
    p=g.bg.PARAMS.copy()
    for n,expr in READ(PLANAR)['families'][name]['parameter_map'].items():
        p['K' if n=='K_Q' else n]=float(s.sympify(expr).subs(s.Symbol('eta'),s.Rational(run['eta_exact'])))
    p['gr']=3*ef/7
    b0=np.asarray(run['first_order_states'][0],float)
    def first_rhs(t,b):
        c=src.context(g,red,b,p)
        return np.r_[c['rate'],b[13],c['wdd']]
    first=solve_ivp(first_rhs,(0.,.05),b0,method=method,rtol=1e-10,atol=1e-12,max_step=.001,dense_output=True)
    ch.add(label+'_first_complete',first.success and first.t[-1]==.05)
    if not first.success:raise RuntimeError(first.message)
    root=brentq(lambda t:first.sol(t)[12],0.,.05,xtol=5e-15,rtol=1e-14)
    system=System(run,p,first,src,red,g)
    z0=np.zeros(96);b=first.sol(0.)
    MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
    xdot=-4*p['A']*b[9]**3/(3*np.pi*MC*b[1])
    for n in ('Mxx','Myy','Mzz'):z0[4+13+system.at(0.)['datas'][0]['dyn'].index(n)]=2*xdot/(3*system.scale)
    parent=next(r for r in READ(PARENT+'initial_jets.json')['initial_jets'] if
        r['family']==name and r['eta_exact']==run['eta_exact'] and r['archived_method']==method and r['harmonic']==0)
    ch.small(label+'_immutable_mean_initial_state',np.max(abs((z0[4:30]+1j*z0[50:76])*system.scale-UNSER(parent['free_initial_state']))),1e-14)
    for j,mode in enumerate((0,2)):
        parent=next(r for r in READ(PARENT+'initial_jets.json')['initial_jets'] if
            r['family']==name and r['eta_exact']==run['eta_exact'] and r['archived_method']==method and r['harmonic']==mode//2)
        data=system.at(0.);full=data['sources'][j]@np.r_[1.,z0[:4]]*system.scale
        for n,actual,expected in [('source',full[:22],UNSER(parent['source'])),('drift',full[23:],UNSER(parent['auxiliary_source_dt']))]:
            ch.small(label+'_initial_'+n+'_'+str(mode),np.max(abs(actual-expected)/(system.scale+abs(expected))),1e-9)
    options=dict(jac=system.jac) if method=='Radau' else {}
    sol=solve_ivp(system.rhs,(0.,.05),z0,method=method,rtol=1e-10,atol=1e-12,max_step=.001,dense_output=True,**options)
    ch.add(label+'_coupled_complete',sol.success and sol.t[-1]==.05,dict(nfev=sol.nfev,njev=sol.njev))
    if not sol.success:raise RuntimeError(sol.message)
    states=sol.sol(TIMES).T;bstates=first.sol(TIMES).T
    first_error=float(np.max(abs(bstates-np.asarray(run['first_order_states']))/(1+abs(bstates))))
    ch.small(label+'_first_vs_immutable21',first_error,1e-7)
    archived=UNSER(run['scaled_response_and_third_states'])[:,46:50]
    ch.small(label+'_odd_vs_immutable21',np.max(abs(states[:,:4]-archived)/(1+abs(archived))),1e-7)
    probes=[diagnostics(system,float(t),sol.sol(t)) for t in [*TIMES,root]]
    for key,tol in [('full22_residual',1e-9),('source_Ward',1e-9),('independent_lapse_drift',1e-8),
                    ('charge_value',1e-7),('charge_derivative',1e-7)]:
        ch.small(label+'_'+key+'_all_nodes_and_root',max(r[key] for r in probes),tol)
    ch.add(label+'_regular_chart_all_nodes_and_root',all(r['regular'] for r in probes))
    quadrature_control(system,.025,sol.sol(.025),ch,label)
    initial=system.at(0.)
    mixed_witness=float(np.linalg.norm(initial['extras'][1]['mixed'][:,0],np.inf))
    drift_witness=float(np.linalg.norm(initial['sources'][1][23:,0],np.inf))
    ch.add(label+'_reject_omitted_mixed_acceleration',mixed_witness>0,mixed_witness)
    ch.add(label+'_reject_omitted_auxiliary_drift',drift_witness>0,drift_witness)
    offset_witness=max(abs(q['mixed_angular_offset_scaled']) for q in probes)
    ch.add(label+'_reject_omitted_mixed_angular_current',offset_witness>0,offset_witness)
    after=system.at(.05)['c']['w']
    ch.add(label+'_reject_analytic_cubic_after_wave_zero',after<0 and abs(after)**3!=after**3,float(after))
    output=dict(family=name,eta_exact=run['eta_exact'],method=method,times=TIMES.tolist(),
        state_layout='odd1,odd1_dot,odd3,odd3_dot,real(mean26,even2_20),imag(mean26,even2_20)',
        scale=system.scale,states_scaled=states.tolist(),first_order_states=bstates.tolist(),
        root=float(root),root_state_scaled=sol.sol(root).tolist(),diagnostics=probes,
        solver=dict(nfev=sol.nfev,njev=sol.njev,nlu=sol.nlu),
        source_mode_selection='exact for outputs0,2 only; no infinite-mode error bound')
    print(json.dumps(dict(stage='CASE_DONE',case=label,nfev=sol.nfev,maxima={k:max(q[k] for q in probes) for k in ('full22_residual','source_Ward','independent_lapse_drift','charge_value','charge_derivative')})),flush=True)
    return output


def calculate(canary=False,checkpoint=None):
    pins,absent,snapshot,g,prior,time=inputs();before=snapshot();ch=Checks()
    src=Sources(ch);red=time.EvolvingReduction(prior,g)
    if not all(r['passed'] for r in ch.rows):raise RuntimeError('Exact prerequisite failed: '+str([r for r in ch.rows if not r['passed']]))
    runs=READ(RET+'trajectories.json')['runs']
    if canary:runs=[r for r in runs if r['family']=='archived_G3' and r['eta_exact']=='1/4' and r['method']=='DOP853']
    records=[]
    for run in runs:
        result=run_case(run,src,red,g,ch);records.append(result)
        if checkpoint:checkpoint(result,len(records))
    if not canary:
        for name in ('archived_G3','new_B1_frame','new_hierarchical'):
            for eta in ('1/4','1/64','1/1024'):
                a,b=[r for r in records if r['family']==name and r['eta_exact']==eta]
                aa,bb=np.asarray(a['states_scaled']),np.asarray(b['states_scaled'])
                difference=float(np.max(abs(aa-bb)/(1+abs(aa)+abs(bb))))
                ch.small(name+'_'+eta+'_independent_two_method_scaled96_all21',difference,1e-7)
    ch.add('all_source_sidecar_metadata_preserved',before==snapshot())
    scope=dict(claim_status='Conditional',physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        stage2_complete=False,stage3_entered=False,physical_window_admitted=False,full_nonlinear_admission=False,
        continuous_time_certified_error=False,infinite_mode_remainder_bound=False,output_harmonics=[0,2],
        native_goal_resumed=False,canary_only=canary,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',
        UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        remaining=['All-orders constraint/remainder and full-field control','Energy/characteristics/physical interaction window',
                   'Healthy GR and local-gravity evidence','Genuine microscopic matter-residue and nonlinear-force matching'])
    verification=dict(checks=ch.rows,total=len(ch.rows),passed=sum(r['passed'] for r in ch.rows))
    ok=verification['passed']==verification['total']
    verification['validation']='PASS_LOCAL_CONTROLS' if ok else 'FAIL_LOCAL_CONTROLS'
    bodies={'formulas.json':ENCODE(src.export),'trajectories.json':ENCODE(dict(runs=records)),
            'verification.json':ENCODE(verification),'scope.json':ENCODE(scope)}
    summary=dict(schema='r4c1-cusp3-evolution-v1',**verification,**scope,
        status=('ENGINEERING_CANARY_ONLY' if canary else 'CONDITIONAL_RETAINED_MODE_EVOLUTION_ONLY') if ok else 'EVOLUTION_UNRESOLVED',
        case_count=len(records),source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,artifacts={n:SHA(b) for n,b in bodies.items()},
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
        review_id='R9-MT1-CUSP3-EVOLUTION-V1',review_dependencies=['CUSP3-LOCAL-INITIAL-JET-V2','INITIAL-CHARGE-COMPLETION-V4',
            'FIXED-CHARGE-RETARDED-V3','GENERIC-WWR/EVOLVING-REDUCTION','all transitive debt'])
    bodies['summary.json']=ENCODE(summary)
    return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_cusp3_evolution_attempt_01')
    parser.add_argument('--canary',action='store_true');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        original=READ((dest/'summary.json').relative_to(ROOT).as_posix())
        if original['canary_only']!=args.canary:raise ValueError('Replay scope differs')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    else:
        if dest.exists():raise FileExistsError('Refuse existing output')
        dest.mkdir(parents=True)
    def checkpoint(record,index):
        if not args.replay:
            p=dest/('case_'+str(index).zfill(2)+'.json');body=ENCODE(record)
            with p.open('xb') as f:f.write(body)
            with Path(str(p)+'.sha256').open('x') as f:f.write(SHA(body)+'  '+p.name+'\n')
    try:bodies,summary=calculate(args.canary,checkpoint)
    except BaseException as exc:
        if not args.replay:
            body=ENCODE(dict(validation='INTERRUPTED_OR_FAILED',error_type=type(exc).__name__,error=str(exc),physics_pass=False))
            with (dest/'interrupted.json').open('xb') as f:f.write(body)
        raise
    if args.replay:
        for name,b in bodies.items():
            if (dest/name).read_bytes()!=b or (dest/(name+'.sha256')).read_text().split()[0]!=SHA(b):raise RuntimeError('Replay differs: '+name)
        for i,r in enumerate(READ((dest/'trajectories.json').relative_to(ROOT).as_posix())['runs'],1):
            if (dest/('case_'+str(i).zfill(2)+'.json')).read_bytes()!=ENCODE(r):raise RuntimeError('Checkpoint differs')
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay modified outputs')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,b in bodies.items():
            with (dest/name).open('xb') as f:f.write(b)
            with (dest/(name+'.sha256')).open('x') as f:f.write(SHA(b)+'  '+name+'\n')
    print(json.dumps({n:summary[n] for n in ('validation','passed','total','status','case_count','physics_pass')}),flush=True)
    return 0 if summary['passed']==summary['total'] else 1


if __name__=='__main__':raise SystemExit(main())
