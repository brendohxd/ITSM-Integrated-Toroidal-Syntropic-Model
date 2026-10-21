"""Full regular-planar Hamiltonian reduction; no physical mode/window clearance."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib, importlib.util, json, multiprocessing, traceback
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sy

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_fixed_charge_patch_momentum_v2.py'
PSHA='2706b05764eea2b9a34dc7be73f78022933a8c444e54f5c8b47b8ceb33fce74f'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_PLANAR_REDUCED_HAMILTONIAN_V1_CONTRACT_2026-10-19.md'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+chr(10)).encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift before import')
spec=importlib.util.spec_from_file_location('frozen_patch_hamiltonian',ROOT/PARENT)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
canonical,base,v4=parent.canonical,parent.base,parent.v4
PINS=dict(parent.PINS)
PINS.update({PARENT:PSHA,CONTRACT:'b61365cab8e359cdb9d542510f5138405bee75394f4e8a3abf9bd182d2bb0b55',
 'Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_PATCH_MOMENTUM_V2_REPORT_2026-10-19.md':
 '1249a068491a7e280f657a7c95ffe5d1ae174009640e5b061150c82fc91e2674'})
_PROGRESS=None
def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+chr(10))

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,digest in pins.items():
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest or side.read_text().split()[0].lower()!=digest:
            raise ValueError('source/sidecar drift '+name)
        for q in (p,side):
            raw=q.read_bytes();meta[q.relative_to(ROOT).as_posix()]=dict(
                sha256=SHA(raw),bytes=len(raw),mtime_ns=q.stat().st_mtime_ns)
    return pins,meta

def exact(ch):
    a,b,c,m,n,L=sy.symbols('Gxx Gxy Gyy mx my L',real=True)
    h=sy.Matrix([[a,b,m],[b,c,n],[m,n,L]])
    rr=sy.Matrix(sy.symbols('rx ry rz'));cc=sy.Matrix(sy.symbols('cx cy cz'))
    pi=h.inv()*(rr+cc)
    ch.zero('all_three_exact_metric_constraint_rows',h*pi-rr-cc)
    th=sy.Symbol('theta',real=True);R=sy.Symbol('R',positive=True)
    pr,pt,dR,dt=sy.symbols('pR ptheta dR dtheta',real=True)
    u,v=R*sy.cos(th),R*sy.sin(th)
    pu,pv=pr*sy.cos(th)-pt*sy.sin(th)/R,pr*sy.sin(th)+pt*sy.cos(th)/R
    du=sy.diff(u,R)*dR+sy.diff(u,th)*dt
    dv=sy.diff(v,R)*dR+sy.diff(v,th)*dt
    ch.zero('finite_polar_canonical_one_form',sy.trigsimp(pu*du+pv*dv-pr*dR-pt*dt))
    ch.zero('finite_polar_charge',sy.trigsimp(u*pv-v*pu-pt))
    k,e,offset=sy.symbols('k e offset',real=True)
    Vy=offset+e*sy.cos(th)
    d=sy.integrate(sy.sin(th)*k*sy.diff(Vy,th),(th,0,2*sy.pi))/(2*sy.pi)
    ch.zero('global_translation_chart_exact_denominator',d+k*e/2)
    M0,dd=sy.symbols('M0 d',nonzero=True)
    ch.zero('global_constraint_solved_without_mean_projection',M0+(-M0/dd)*dd)
    ch.add('zero_translation_chart_is_singular',d.subs(e,0)==0)
    ch.zero('registered_profile_exact_nodes',e**2*sy.cos(sy.pi/2)**2)
    ch.zero('registered_node_force_regulator_inverse_singular',
        sy.diff(-e**2*sy.cos(th)**2*sy.Symbol('b')*sy.Symbol('s'),sy.Symbol('s')).subs(th,sy.pi/2))
    ppsi,E,s=sy.symbols('p_psi E s',nonzero=True)
    ch.zero('clock_Hamiltonian_orientation',-sy.solve(ppsi*s+E,ppsi)[0]-E/s)
    # Exact canonical zero-mode accounting, not a propagating-mode count.
    q0,p0,dpmean,dpfluct,dqmean,dqfluct=sy.symbols('q0 p0 dpmean dpfluct dqmean dqfluct')
    ch.zero('origin_charge_one_form_split',
        (p0+dpfluct)*(dqmean+dqfluct)-(p0*dqmean+dpfluct*dqfluct
        +p0*dqfluct+dpfluct*dqmean))
    z=sy.Symbol('z',real=True)
    fx,fy,F0=sy.Function('pxVz')(z),sy.Function('pyVz')(z),sy.Function('Sprimitive')(z)
    hz=sy.Matrix([fx/2+cc[0],fy/2+cc[1],F0/2+cc[2]])
    ch.zero('actual_transverse_constraints',[
        -2*sy.diff(hz[0],z)+sy.diff(fx,z),-2*sy.diff(hz[1],z)+sy.diff(fy,z)])
    ch.zero('actual_longitudinal_constraint',-2*sy.diff(hz[2],z)+sy.diff(F0,z))
    ch.add('mean_metric_pairs_not_dropped',all(x in pi.free_symbols for x in cc))
    # Formal mass degrees before any numerical reference chart.
    degrees=[3+1,3+1,3+1,2+2,3+1,2+2,1+3,4+0]
    ch.add('all_continuum_constraint_sources_degree4',all(d==4 for d in degrees),degrees)
    ch.add('primitive_metric_momenta_clock_density_degree3',4-1==3)
    return dict(
        metric_gauge='h=[[G(z),m],[m^T,L]], G 2x2, m and L spatial constants but canonical coordinates',
        exact_solution='r=(pVx*Vz/2,pVy*Vz/2,I_z(S)/2), A=<h^-1>, c=A^-1(M-<h^-1*r>), pi_iz=h^-1(r+c)',
        mean_metric_momenta='M=(P_mx/2,P_my/2,P_L); A positive definite since x^T*A*x=<x^T*h^-1*x>>0',
        residual_global_constraint='S=pi_AB*G_ABprime+pV*Vprime+(pVz*Vz)prime+sum_scalar(p*phiprime); <S>=0 required',
        global_translation='f=<sin(kz)*Vy>=0, d=<sin(kz)*Vyprime>!=0, pVy=pVy0-<S0>/d*sin(kz); term lambda*df vanishes',
        fixed_charges='p_theta=Qtheta+fluctuation, p_T=Qdust+fluctuation; zero-mean phase/dust origins quotiented, fluctuating pairs retained',
        clock='psi=tau after variation; s=-pZ/(volume*b*V2)>0, p_psi=-(E0+Edust+Fprime)/s',
        reduced_Hamiltonian='Hpsi=-<p_psi>=<(E0+Edust)/s-F*(1/s)prime>; F=gamma*h^zi*pVi',
        canonical_one_form='mean(pi_AB*dG_AB+pV0*dV+pR*dR+ptheta_fluct*dtheta+pr*dr+pZ*dZ+pT_fluct*dT)+P_m*d_m+P_L*dL',
        zero_mode_and_node_limits='No inverse of translation kernel, no deletion of mean metric pairs; b*V2*s and det R must be regular; actual w=e*cos(kz) has nodes',
        meaning='Full nonlinear regular-planar functional, not a computed mode spectrum, arbitrary3D closure or physical frequency window')

def grids(n,k):
    theta,D=canonical.spectral_grid(n)
    f=np.fft.fftfreq(n,1/n)
    inverse=np.zeros(n,dtype=complex);inverse[1:]=1/(1j*k*f[1:])
    I=np.fft.ifft(inverse[:,None]*np.fft.fft(np.eye(n),axis=0),axis=0).real
    return theta,k*D,I

def data(n,par,eta):
    theta,D,I=grids(n,40);rc=np.sqrt(float(sy.Rational(eta)))
    q=np.zeros((n,15));p=np.zeros_like(q)
    q[:,0]=1+.01*np.cos(theta);q[:,1]=.003*np.sin(theta)
    q[:,2]=.01;q[:,3]=1+.009*np.cos(2*theta);q[:,4]=-.015;q[:,5]=1.02
    q[:,6]=.07+.001*np.cos(2*theta);q[:,7]=.10+.003*np.cos(theta);q[:,8]=.02+.001*np.sin(2*theta)
    radial=rc*(1+.004*np.cos(theta));phase=.002*np.sin(2*theta)
    pR=.003+.001*np.sin(theta);Qtheta=float(sy.Rational(eta))**1.5
    ptheta=Qtheta+.0001*float(sy.Rational(eta))*np.cos(theta)
    q[:,9]=radial*np.cos(phase);q[:,10]=radial*np.sin(phase);q[:,11]=rc*(1+.003*np.sin(theta))
    p[:,9]=pR*np.cos(phase)-ptheta*np.sin(phase)/radial
    p[:,10]=pR*np.sin(phase)+ptheta*np.cos(phase)/radial
    p[:,11]=.005+.001*np.cos(theta)
    q[:,12]=.02;q[:,13]=.03+.001*np.cos(theta);q[:,14]=.001*np.cos(2*theta)
    p[:,14]=.2+.001*np.sin(theta)
    p[:,0]=-.10+.001*np.cos(2*theta);p[:,1]=.002*np.cos(theta);p[:,3]=-.11+.001*np.sin(theta)
    p[:,6]=par['MU2']*(.002+.001*np.sin(2*theta))
    p[:,7]=par['MU2']*(.003+.002*np.cos(2*theta))
    p[:,8]=par['MU2']*(.001+.0003*np.cos(theta))
    h=canonical.tensor_h(q);vol=np.sqrt(np.linalg.det(h))
    v2=np.einsum('ni,nij,nj->n',q[:,6:9],h,q[:,6:9])
    s=float(sy.Rational(eta))/5*(1+.001*np.cos(2*theta))
    p[:,13]=-vol*par['b']*v2*s
    return dict(q=q,p=p,theta=theta,D=D,I=I,mean_pi=np.array([.001,-.002,-.13]),
                radial=radial,phase=phase,pR=pR,ptheta=ptheta,Qtheta=Qtheta,Qdust=.2)

def remaining_source(q,p,D):
    dq=D@q
    return sum(p[:,a]*dq[:,a] for a in (0,1,3))+np.sum(p[:,6:9]*dq[:,6:9],axis=1)\
        +D@(p[:,8]*q[:,8])+np.sum(p[:,9:]*dq[:,9:],axis=1)

def restore(raw,par):
    q=raw['q'].copy();p=raw['p'].copy();D,I,theta=raw['D'],raw['I'],raw['theta']
    if np.min(raw['radial'])<=0:raise ValueError('singular polar chart')
    if max(np.max(abs(q[:,j]-np.mean(q[:,j]))) for j in (2,4,5))>1e-12:
        raise ValueError('input outside planar spatial gauge')
    if max(abs(np.mean(p[:,14])-raw['Qdust']),
           abs(np.mean(q[:,9]*p[:,10]-q[:,10]*p[:,9])-raw['Qtheta']))>1e-12:
        raise ValueError('input does not retain both fixed charges')
    sine=np.sin(theta);d=np.mean(sine*(D@q[:,7]));S0=remaining_source(q,p,D)
    if abs(d)<1e-12:raise ValueError('global translation chart singular')
    if abs(np.mean(sine*q[:,7]))>1e-12 or abs(np.mean(sine*p[:,7]))>1e-12:
        raise ValueError('input not in translation gauge/cotangent chart')
    lam=-np.mean(S0)/d;p[:,7]+=lam*sine
    S=remaining_source(q,p,D)
    if abs(np.mean(S))>1e-10:raise ValueError('residual global momentum constraint')
    h=canonical.tensor_h(q);hi=np.linalg.inv(h);vol=np.sqrt(np.linalg.det(h))
    if np.min(np.linalg.eigvalsh(h))<=0:raise ValueError('nonpositive spatial metric')
    v2=np.einsum('ni,nij,nj->n',q[:,6:9],h,q[:,6:9])
    if par['b']<=0 or np.min(v2)<=0 or np.min(p[:,14])<=0:
        raise ValueError('singular tilt/regulator or nonpositive dust')
    r=np.column_stack((p[:,6]*q[:,8]/2,p[:,7]*q[:,8]/2,I@S/2))
    A=np.mean(hi,axis=0)
    c=np.linalg.solve(A,raw['mean_pi']-np.mean(np.einsum('nij,nj->ni',hi,r),axis=0))
    restored=np.einsum('nij,nj->ni',hi,r+c)
    p[:,2]=2*restored[:,0];p[:,4]=2*restored[:,1];p[:,5]=restored[:,2]
    _,hi,grad,DV,R3=canonical.spatial_geometry(q,D)
    energy,flux,blocks=canonical.full_blocks(q,hi,grad,DV,p,par,R3)
    s=blocks['psi_hat']
    if np.min(s)<=0:raise ValueError('nonpositive force clock')
    local=energy+D@flux
    p[:,12]=-local/s
    H=np.mean(local/s)
    Hparts=np.mean(energy/s-(D@(1/s))*flux)
    return dict(q=q,p=p,H=H,Hparts=Hparts,S0=S0,S=S,lam=lam,d=d,
                energy=energy,flux=flux,blocks=blocks,R3=R3,hi=hi,grad=grad,DV=DV)

def true_constraints(q,p,D):
    h=canonical.tensor_h(q);pi=np.zeros_like(h)
    for a,(i,j) in enumerate(canonical.HM):pi[:,i,j]=pi[:,j,i]=p[:,a]/(1 if i==j else 2)
    C=np.zeros((len(q),3))
    hpi=np.einsum('nij,nj->ni',h,pi[:,:,2])
    for i in range(3):C[:,i]=-2*(D@hpi[:,i])+D@(p[:,6+i]*q[:,8])
    dq=D@q
    C[:,2]+=sum(p[:,a]*dq[:,a] for a in range(6))+np.sum(p[:,6:9]*dq[:,6:9],axis=1)\
        +np.sum(p[:,9:]*dq[:,9:],axis=1)
    return C

def one_form(ch,raw,out):
    q,p,theta=out['q'],out['p'],raw['theta']
    errors=[]
    for seed in (1,2,3):
        variation=np.zeros_like(q)
        variation[:,0]=.001*np.cos(seed*theta);variation[:,1]=.001*np.sin(seed*theta)
        variation[:,3]=.001*np.cos((seed+1)*theta)
        dm=np.array([.001/seed,-.002/seed]);dL=.003/seed
        variation[:,2]=dm[0];variation[:,4]=dm[1];variation[:,5]=dL
        variation[:,6]=.001*np.sin(seed*theta);variation[:,7]=.001*np.cos(seed*theta)
        variation[:,8]=.001*np.cos((seed+1)*theta)
        dR=.001*np.cos(seed*theta);dt=.001*np.sin((seed+1)*theta)
        phase,radial=raw['phase'],raw['radial']
        variation[:,9]=np.cos(phase)*dR-radial*np.sin(phase)*dt
        variation[:,10]=np.sin(phase)*dR+radial*np.cos(phase)*dt
        variation[:,11]=.001*np.sin(seed*theta)
        variation[:,13]=.001*np.cos(seed*theta);variation[:,14]=.001*np.cos((seed+1)*theta)
        direct=np.mean(np.sum(p*variation,axis=1))
        reduced=np.mean(sum(raw['p'][:,a]*variation[:,a] for a in (0,1,3))
            +np.sum(raw['p'][:,6:9]*variation[:,6:9],axis=1)
            +raw['pR']*dR+(raw['ptheta']-raw['Qtheta'])*dt
            +p[:,11]*variation[:,11]+p[:,13]*variation[:,13]
            +(p[:,14]-raw['Qdust'])*variation[:,14])
        reduced+=2*raw['mean_pi'][:2]@dm+raw['mean_pi'][2]*dL
        errors.append(abs(direct-reduced)/(1+abs(direct)+abs(reduced)))
    ch.small('full_reduced_canonical_one_form',max(errors),'1e-8')
    return max(errors)

def independent_density(ch,raw,out,par,family,eta):
    mp.mp.dps=80;i=3
    q,p=out['q'],out['p'];mpf=lambda v:mp.mpf(repr(float(v)))
    h=mp.matrix([[mpf(v) for v in row] for row in canonical.tensor_h(q)[i]])
    V=mp.matrix([mpf(v) for v in q[i,6:9]]);vol=mp.sqrt(mp.det(h))
    c=(V.T*h*V)[0];gamma=mp.sqrt(1+c)
    y=mp.matrix([mpf(v) for v in out['blocks']['y'][i]]);s=mpf(out['blocks']['psi_hat'][i])
    config=dict(h=h,hi=h**-1,V=V,gamma=gamma,DV=mp.matrix([[mpf(v) for v in row] for row in out['DV'][i]]),
        spatial={name:mp.matrix([mpf(v) for v in out['grad'][i,j]]) for name,j in
                 (('u',9),('v',10),('r',11),('psi',12),('Z',13),('T',14))},
        proper={'T':mp.mpf(0)},u=mpf(q[i,9]),v=mpf(q[i,10]),r=mpf(q[i,11]),
        psi=mpf(q[i,12]),Z=mpf(q[i,13]),R3=mpf(out['R3'][i]),epsilon=mp.mpf(1))
    pp=canonical.parameters(family,eta,'mp')
    body=lambda yy,ss,zz:canonical.mp_body(config,pp,yy,ss,zz,include_dust=False)
    Ppsi=mpf(p[i,12])/vol;PZ=mpf(p[i,13])/vol
    psi0=mp.diff(lambda ss:body(y,ss,0),s)
    zh=(psi0-Ppsi)/(pp['b']*c)
    PY=mp.matrix([mpf(v) for v in np.r_[2*p[i,:6],p[i,6:12]]])/vol
    errors=[]
    for j in range(12):
        def fn(a):
            yy=mp.matrix(y);yy[j]=a
            return body(yy,s,zh)
        got=mp.diff(fn,y[j]);errors.append(abs(got-PY[j])/(1+abs(got)+abs(PY[j])))
    gotpsi=mp.diff(lambda ss:body(y,ss,zh),s);gotZ=mp.diff(lambda z:body(y,s,z),zh)
    errors.extend([abs(gotpsi-Ppsi)/(1+abs(gotpsi)+abs(Ppsi)),abs(gotZ-PZ)/(1+abs(gotZ)+abs(PZ))])
    E=vol*((PY.T*y)[0]+Ppsi*s+PZ*zh-body(y,s,zh))
    C=mp.exp(pp['beta']*config['psi']);dT=config['spatial']['T']
    E+=mpf(p[i,14])*mp.sqrt(C*C+(dT.T*config['hi']*dT)[0])
    target=mpf(out['energy'][i])+mpf(p[i,12])*s
    errors.append(abs(E-target)/(1+abs(E)+abs(target)))
    ch.small('independent_original_mpmath_all_momenta_and_energy',max(errors),'1e-8')
    return base.SHOW(max(errors))

def grid_control(ch,n,par,eta,family):
    raw=data(n,par,eta);out=restore(raw,par);q,p=out['q'],out['p']
    D,I,theta=raw['D'],raw['I'],raw['theta']
    tag=str(n)+'_';checks=base.Checks()
    eye=np.eye(n)-np.ones((n,n))/n
    checks.small('periodic_primitive_both_sides',max(np.max(abs(D@I-eye)),np.max(abs(I@D-eye))),'1e-8')
    checks.small('periodic_skew_adjoint',np.max(abs(D+D.T)),'1e-8')
    CC=true_constraints(q,p,D)
    checks.small('all_three_original_spatial_constraints',np.max(abs(CC))/(1+np.max(abs(out['S']))),'1e-8')
    checks.small('nonprojected_global_constraint',abs(np.mean(out['S'])),'1e-8')
    means=np.array([np.mean(p[:,2]/2),np.mean(p[:,4]/2),np.mean(p[:,5])])
    checks.small('all_three_mean_metric_momenta',np.max(abs(means-raw['mean_pi'])),'1e-8')
    checks.small('both_fixed_global_charges',max(abs(np.mean(q[:,9]*p[:,10]-q[:,10]*p[:,9])-raw['Qtheta']),
        abs(np.mean(p[:,14])-raw['Qdust'])),'1e-8')
    checks.small('clock_weighted_flux_integration_by_parts',abs(out['H']-out['Hparts'])/(1+abs(out['H'])),'1e-8')
    lapse=1/out['blocks']['psi_hat']
    original=canonical.hamiltonian(q,p,lapse,D,par)/(2*np.pi)
    checks.small('original_unreduced_lapse_generator',abs(original)/(1+abs(out['H'])),'1e-8')
    gerrs=[]
    for j in range(3):
        shift=np.zeros((n,3));shift[:,j]=.1+.03*np.sin((j+1)*theta)
        actual=canonical.diffeo(q,p,shift,D)/(2*np.pi)
        target=np.mean(np.sum(CC*shift,axis=1))
        gerrs.append(abs(actual-target)/(1+abs(actual)+abs(target)))
    checks.small('all_original_diffeomorphism_generators',max(gerrs),'1e-8')
    pullback=one_form(checks,raw,out)
    checks.add('omitted_mean_momenta_rejected',np.max(abs(raw['mean_pi']))>.01)
    checks.add('omitted_global_constraint_rejected',abs(np.mean(out['S0']))>1e-12,repr(float(np.mean(out['S0']))))
    flux_effect=out['H']-np.mean(out['energy']/out['blocks']['psi_hat'])
    checks.add('omitted_clock_weighted_flux_rejected',abs(flux_effect)>1e-12,repr(float(flux_effect)))
    volume=out['blocks']['volume'];curvature_effect=np.mean(par['MP2']*volume*out['R3']*lapse/2)
    checks.add('omitted_spatial_Ricci_rejected',abs(curvature_effect)>1e-12,repr(float(curvature_effect)))
    checks.add('analytic_nodeless_method_control_not_grid_inference',.973*.069**2>0 and
        np.min(np.linalg.eigvalsh(canonical.tensor_h(q)))>.973-1e-12)
    if n==17:
        guards=(('negative_dust','dust','nonpositive dust'),('wrong_charge','charge','fixed charges'),
                ('zero_tilt','tilt','singular tilt'),('reverse_clock','clock','nonpositive force clock'),
                ('zero_translation_denominator','translation','translation chart'),('polar_origin','polar','polar chart'))
        for label,kind,message in guards:
            bad=dict(raw,q=raw['q'].copy(),p=raw['p'].copy(),radial=raw['radial'].copy())
            if kind=='dust':bad['p'][0,14]=-1;bad['p'][1,14]+=1+raw['p'][0,14]
            if kind=='charge':bad['p'][:,14]+=.01
            if kind=='tilt':bad['q'][0,6:9]=0
            if kind=='clock':bad['p'][:,13]*=-1
            if kind=='translation':bad['q'][:,7]=.1
            if kind=='polar':bad['radial'][0]=0
            rejected=False
            try:restore(bad,par)
            except ValueError as exc:rejected=message in str(exc)
            checks.add('domain_guard_rejects_'+label,rejected)
    parent.joint.merge_checks(ch,checks.rows,tag)
    return raw,out,dict(grid=n,Hpsi=repr(float(out['H'])),mean_constraint_before=repr(float(np.mean(out['S0']))),
        translation_correction=repr(float(out['lam'])),clock_flux_effect=repr(float(flux_effect)),
        curvature_effect=repr(float(curvature_effect)),spatial_constraint_residual=repr(float(np.max(abs(CC)))),
        one_form_error=repr(float(pullback)),min_tilt_squared=repr(float(np.min(
            np.einsum('ni,nij,nj->n',q[:,6:9],canonical.tensor_h(q),q[:,6:9])))))

def case_job(task):
    index,family,eta=task;ch=base.Checks();par=canonical.parameters(family,eta)
    controls=[];reference=None;independent=None
    try:
        for n in (17,25,33):
            raw,out,record=grid_control(ch,n,par,eta,family);controls.append(record)
            if n==25:independent=independent_density(ch,raw,out,par,family,eta)
        vals=[float(x['Hpsi']) for x in controls]
        ch.small('three_grid_Hamiltonian_agreement_diagnostic',max(abs(v-vals[-1]) for v in vals)/(1+abs(vals[-1])),'1e-8')
    except Exception:
        ch.add('unexpected_case_exception',False,traceback.format_exc())
    return index,dict(family=family,eta=eta,controls=controls,original_density_error=independent,
        meaning='Nodeless method controls only; no registered state adoption, frequency roots or physical domain.'),ch.rows

def calculate(workers):
    pins,before=sources();ch=base.Checks();form=exact(ch)
    if not all(r['passed'] for r in ch.rows):raise ValueError('exact derivation failure '+repr([r for r in ch.rows if not r['passed']]))
    tasks=[(i,f,e) for i,(f,e) in enumerate((f,e) for f in canonical.FAMILIES for e in canonical.ETAS)]
    results={};progress('reduced_Hamiltonian_cases',cases=len(tasks),workers=min(workers,len(tasks)))
    if workers==1:
        for task in tasks:
            r=case_job(task);results[r[0]]=r;progress('Hamiltonian_case_complete',index=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,len(tasks)),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for future in as_completed(jobs):
                r=future.result()
                if r[0]!=jobs[future] or r[0] in results:raise ValueError('case identity')
                results[r[0]]=r;progress('Hamiltonian_case_complete',index=r[0])
    records=[]
    for i in range(len(tasks)):
        _,record,rows=results[i];records.append(record)
        parent.joint.merge_checks(ch,rows,record['family']+'_'+record['eta']+'_')
    _,after=sources();ch.add('all_original_bytes_sidecars_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_REGULAR_PLANAR_HAMILTONIAN_REDUCTION_ONLY' if passed==len(ch.rows) else 'FAIL_OR_UNRESOLVED_REDUCTION',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='REGULAR_PLANAR_FUNCTIONAL_SUPPLIED_REGISTERED_NODES_MODES_WINDOW_OPEN',
        physical_mode_spectrum_computed=False,registered_nodal_state_admitted=False,state_adopted_or_evolved=False,
        arbitrary3D_constraint_closure_proved=False,physical_frequency_window_established=False,action_no_go=False,
        stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    return {'summary.json':summary,'formulas.json':form,'independent.json':records}

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output');p.add_argument('--replay');p.add_argument('--workers',type=int,default=16)
    p.add_argument('--progress-log');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose one output/replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    record=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:record(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+chr(10)).encode()
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay set changed')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or record(f)!=before[name]:raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1
if __name__=='__main__':raise SystemExit(main())
