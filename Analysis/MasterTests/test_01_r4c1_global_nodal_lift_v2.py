"""Global undivided nodal lift and initial coordinate-flow controls, not physical clearance."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,importlib.util,json,multiprocessing,traceback
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sy
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_nodal_descriptor_v2.py'
PSHA='b19f4ce9a665d711b3be021cfa149fe3b4753851e1c11d99bc705156537f8bf5'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_GLOBAL_NODAL_LIFT_V1_CONTRACT_2026-10-19.md'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+chr(10)).encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
spec=importlib.util.spec_from_file_location('frozen_undivided_nodes',ROOT/PARENT)
nodal=importlib.util.module_from_spec(spec);spec.loader.exec_module(nodal)
planar,canonical,base=nodal.planar,nodal.canonical,nodal.base
cop=nodal.reg.cop
PINS=dict(nodal.PINS)
PINS.update({
 'Analysis/MasterTests/test_01_r4c1_global_nodal_lift_v1.py':'052000518f5c745a028aba3def170c1ae0b6b276c8a124aab3c5cbec70a9c6ee',
 'Theory/Gates/RES-001/RES001_R4C1_GLOBAL_NODAL_LIFT_V2_FLUX_ADDENDUM_2026-10-19.md':'9730305c00a173905f3c2f2d4b6742338cd8b2a1dc31ed9a8451ff5936486de5',
 'Analysis/MasterTests/outputs/r4c1_global_nodal_lift_attempt_01/summary.json':'4035b08090b924deff25d6e485c3e0755a58e1c7dd443d2e526a02f95d24be25',
 'Analysis/MasterTests/outputs/r4c1_global_nodal_lift_attempt_01/formulas.json':'08058e16cf87399b7f59e130f364dee99484ee41f6e122b6828e5407fd7ac19e',
 'Analysis/MasterTests/outputs/r4c1_global_nodal_lift_attempt_01/independent.json':'bb0c6c71355c8a8da7c4c614af5f6eff940d2341f7ff4ebf307c204a05e07220',
 PARENT:PSHA,CONTRACT:'bc94c33a7b2e1bb6793c43afe32272732cc845b9e058cb2f11c608d4d038297b',
 'Theory/Gates/RES-001/RES001_R4C1_NODAL_DESCRIPTOR_V2_REPORT_2026-10-19.md':
 'bb8f83e2e234609a10a755777e3031990037822a99fd4482115404d4cae49d3d'})
_PROGRESS=None
def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+chr(10))
def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for n,d in pins.items():
        p=ROOT/n;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=d or sc.read_text().split()[0].lower()!=d:raise ValueError('source/sidecar drift '+n)
        for q in (p,sc):
            raw=q.read_bytes();meta[q.relative_to(ROOT).as_posix()]=dict(
                sha256=SHA(raw),bytes=len(raw),mtime_ns=q.stat().st_mtime_ns)
    return pins,meta
class StableDerivative:
    """D(f-f[0]) only in derivative evaluation; no state mean is removed."""
    def __init__(self,matrix):self.matrix=matrix
    def __matmul__(self,value):
        value=np.asarray(value)
        return self.matrix@(value-value[0])
def grid(n,offset):
    theta,D0,I=planar.grids(n,40)
    return theta+offset,StableDerivative(D0),I
def restore_undivided(raw,par,omit_flux=False):
    s=np.asarray(raw['s']);dtype=np.result_type(raw['q'],raw['p'],s,raw['mean_pi'])
    q=raw['q'].astype(dtype);p=raw['p'].astype(dtype);D,I,theta=raw['D'],raw['I'],raw['theta']
    if np.min(np.real(s))<=0:raise ValueError('nonpositive force clock')
    if np.max(abs(q[:,12]-q[0,12]))>1e-12:raise ValueError('force-clock spatial gauge')
    if max(np.max(abs(q[:,j]-np.mean(q[:,j]))) for j in (2,4,5))>1e-12:raise ValueError('metric spatial gauge')
    if max(abs(np.mean(p[:,14])-raw['Qdust']),abs(np.mean(q[:,9]*p[:,10]-q[:,10]*p[:,9])-raw['Qtheta']))>1e-10:
        raise ValueError('fixed charge changed')
    h=canonical.tensor_h(q)
    if np.min(np.linalg.eigvalsh(np.real(h)))<=0 or np.min(np.real(p[:,14]))<=0:raise ValueError('metric/dust branch')
    hi=np.linalg.inv(h);vol=np.sqrt(np.linalg.det(h))
    c=np.einsum('ni,nij,nj->n',q[:,6:9],h,q[:,6:9]);g=par['b']*vol*c
    p[:,13]=-g*s  # NO division by c or g, including exact zeros.
    sine=np.sin(theta);d=np.mean(sine*(D@q[:,7]))
    if abs(d)<1e-12 or abs(np.mean(sine*q[:,7]))>1e-12:raise ValueError('translation chart')
    p[:,7]-=np.mean(sine*p[:,7])/np.mean(sine*sine)*sine
    S0=planar.remaining_source(q,p,D);lam=-np.mean(S0)/d;p[:,7]+=lam*sine
    S=planar.remaining_source(q,p,D)
    if abs(np.mean(S))>1e-10:raise ValueError('global momentum constraint')
    r=np.column_stack((p[:,6]*q[:,8]/2,p[:,7]*q[:,8]/2,I@S/2))
    A=np.mean(hi,axis=0)
    const=np.linalg.solve(A,raw['mean_pi']-np.mean(np.einsum('nij,nj->ni',hi,r),axis=0))
    pi=np.einsum('nij,nj->ni',hi,r+const)
    p[:,2]=2*pi[:,0];p[:,4]=2*pi[:,1];p[:,5]=pi[:,2]
    _,hi,grad,DV,R3=canonical.spatial_geometry(q,D);grad[:,12,:]=0
    E,F,blocks=nodal.partial_blocks(q,hi,grad,DV,p,par,R3,s)
    divF=D@F
    total=E+(0 if omit_flux else divF)
    p[:,12]=-total/s
    return dict(H=np.mean(E/s-(0 if omit_flux else F*(D@(1/s)))) ,Hdirect=np.mean(total/s),q=q,p=p,g=g,S=S,lam=lam,divF=divF,E=E,F=F,
                blocks=blocks,grad=grad,DV=DV,R3=R3)
def setup(point,initial):
    rat=sy.Rational(point['eta']);et=mp.mpf(rat.p)/rat.q
    par=canonical.parameters(point['family'],point['eta'],'mp')
    H,U,Ud=[mp.mpf(point[n]) for n in ('H','U','Ud')]
    HB=base.midpoint(cop.unpack(initial['H_background']))
    vals=dict(par,k=mp.mpf(40),p=et/5,H0=HB,Rc=mp.sqrt(et),rd=mp.sqrt(et)/4)
    c=dict(values={n:base.point(v) for n,v in vals.items()})
    return par,vals,H,U,Ud,cop.galerkin(c,H,U,8),cop.galerkin(c,H,U,12)
def initial_lift(n,offset_index,par,vals,H,U,Ud,shift):
    offset=mp.pi/2 if offset_index==0 else 3*mp.pi/2
    theta,D,I=grid(n,float(offset));e=mp.mpf(1)/500;k=vals['k'];rate=vals['p'];Rc=vals['Rc']
    w=[];wp=[];Rv=[];Rz=[]
    for j in range(n):
        angle=offset+2*mp.pi*j/n
        ww=mp.mpf(0) if j==0 else e*mp.cos(angle)
        w.append(float(ww));wp.append(float(-k*e*mp.sin(angle)))
        rr,qq=shift(angle);Rv.append(float(rr));Rz.append(float(qq))
    w,wp,Rv,Rz=map(np.array,(w,wp,Rv,Rz));pn={n:float(v) for n,v in par.items()}
    q=np.zeros((n,15));q[:,[0,3,5]]=1;q[:,7]=w
    q[:,9]=q[:,11]=float(Rc);q[:,13]=float(U)*w*w
    p=np.zeros_like(q);s=np.full(n,float(rate))
    _,hi,grad,DV,R3=canonical.spatial_geometry(q,D)
    # Analytic initial jets are separate from the spectral operator diagnostics.
    grad[:]=0;grad[:,7,2]=wp;grad[:,13,2]=2*float(U)*w*wp
    DV[:]=0;DV[:,2,1]=wp;R3[:]=0
    E,F,co=nodal.partial_blocks(q,hi,grad,DV,p,pn,R3,s)
    den=pn['MP2']-pn['MU2']*(pn['c1']+pn['c3']+2*pn['c3']*w*w-2*pn['c4']*(1+w*w)*w*w)
    ty=-pn['MU2']*(pn['c1']+pn['c3']+2*pn['c3']*w*w)*wp/(np.sqrt(1+w*w)*den)
    phase=float(Rc/(1-par['zeta']*Rc**2*e**2/2))
    y=np.zeros((n,12));y[:,0]=y[:,3]=float(H);y[:,4]=-ty/2;y[:,5]=float(H)-Rz
    y[:,7]=-float(vals['H0'])*w-Rv*wp;y[:,10]=phase;y[:,11]=float(Rc/4)
    PY=np.einsum('nij,nj->ni',co['R'],y)+co['ell']
    p[:,:6]=PY[:,:6]/2;p[:,6:12]=PY[:,6:]
    E0,F,co=nodal.partial_blocks(q,hi,grad,DV,p,pn,R3,s)
    h=1e-20
    Ep,_,_=nodal.partial_blocks(q,hi,grad,DV,p,pn,R3,s.astype(complex)+1j*h)
    dE=np.imag(Ep)/h
    zh=float(Ud)*w*w-Rv*(2*float(U)*w*wp)
    g=co['g'];p[:,12]=-dE-g*zh;p[:,13]=-g*s
    p[:,14]=-(E0+p[:,12]*s+D@F)
    mean_pi=np.array([np.mean(p[:,2]/2),np.mean(p[:,4]/2),np.mean(p[:,5])])
    return dict(q=q,p=p,s=s,D=D,I=I,theta=theta,mean_pi=mean_pi,
                Qtheta=float(vals['Rc']**2),Qdust=.2,y=y,wp=wp,shift=Rv,shiftprime=Rz,
                Zdot=float(Ud)*w*w/float(rate),rate=float(rate),H=float(H),HB=float(vals['H0']),Rc=float(Rc))
def variation(raw,kind,j,step):
    r=dict(raw,p=raw['p'].astype(complex),s=raw['s'].astype(complex),mean_pi=raw['mean_pi'].astype(complex))
    n=len(raw['q']);v=np.zeros(n);v[j]=1
    if kind in (0,1,3,6,9,11):r['p'][:,kind]+=1j*step*v
    elif kind==7:
        si=np.sin(raw['theta']);v-=si*si[j]/np.sum(si*si);r['p'][:,7]+=1j*step*v
    elif kind==8:r['p'][:,8]+=1j*step*v
    elif kind=='phase':
        v-=1/n;r['p'][:,10]+=1j*step*v/raw['Rc']
    elif kind=='dust':
        v-=1/n;r['p'][:,14]+=1j*step*v
    elif kind=='s':r['s']+=1j*step*v
    else:raise ValueError('unknown variation')
    return r
def flow(ch,raw,par,step):
    n=len(raw['q']);p0=raw['rate'];H=raw['H'];target={}
    target[0]=target[3]=np.full(n,2*H/p0);target[1]=np.zeros(n)
    for kind in (6,8,9,'phase','dust'):target[kind]=np.zeros(n)
    target[7]=-raw['HB']*raw['q'][:,7]/p0
    target[11]=np.full(n,raw['Rc']/(4*p0))
    errors=[];raw_s=[]
    for kind in (0,1,3,6,7,8,9,11,'phase','dust','s'):
        got=np.array([n*np.imag(restore_undivided(variation(raw,kind,j,step),par)['H'])/step for j in range(n)])
        if kind=='s':
            g=par['b']*raw['q'][:,7]**2
            raw_s=got+g*raw['Zdot']
        else:errors.append(np.max(abs(got-target[kind])/(1+abs(got)+abs(target[kind]))))
    merrors=[]
    for j,want in enumerate((0,0,2*H/p0)):
        r=dict(raw,mean_pi=raw['mean_pi'].astype(complex))
        r['mean_pi'][j]+=1j*step*(.5 if j<2 else 1)
        got=np.imag(restore_undivided(r,par)['H'])/step
        merrors.append(abs(got-want)/(1+abs(got)+abs(want)))
    scalar=float(np.max(abs(raw_s)))/par['K_Q']
    ch.small('all_initial_coordinate_and_mean_rates_'+str(step),mp.mpf(float(max(errors+merrors))),'1e-8')
    ch.small('scalar_rate_row_on_KQ_scale_'+str(step),mp.mpf(scalar),'1e-4')
    return dict(step=repr(step),coordinate_rate_error=repr(float(max(errors+merrors))),
                scalar_row_max_raw=repr(float(np.max(abs(raw_s)))),scalar_row_KQ_scaled=repr(scalar),
                node_scalar_row=repr(float(raw_s[0])))
def independent_node(ch,raw,out,parmp):
    mp.mp.dps=100;y=mp.matrix([mp.mpf(repr(float(v))) for v in out['blocks']['y'][0]])
    rate=mp.mpf(repr(raw['rate']));wp=mp.mpf(repr(float(raw['wp'][0])))
    Rc=mp.mpf(repr(raw['Rc']))
    config=dict(h=mp.eye(3),hi=mp.eye(3),V=mp.matrix([0,0,0]),gamma=mp.mpf(1),
        DV=mp.matrix([[0,0,0],[0,0,0],[0,wp,0]]),u=Rc,v=mp.mpf(0),r=Rc,psi=mp.mpf(0),Z=mp.mpf(0),
        R3=mp.mpf(0),epsilon=mp.mpf(1),proper={'T':mp.mpf(1)},
        spatial={n:mp.matrix([0,0,0]) for n in ('u','v','r','psi','Z','T')})
    body=lambda yy,s:canonical.mp_body(config,parmp,yy,s,0,include_dust=False)
    errors=[]
    want=np.r_[2*out['p'][0,:6],out['p'][0,6:12]]
    for j in range(12):
        def fn(t):
            yy=mp.matrix(y);yy[j]=t;return body(yy,rate)
        val=mp.diff(fn,y[j]);errors.append(abs(val-mp.mpf(repr(float(want[j]))))/(1+abs(val)+abs(float(want[j]))))
    pp=mp.diff(lambda s:body(y,s),rate)
    errors.append(abs(pp-parmp['K_Q']*rate))
    ch.small('original100digit_node_density_all_momenta',max(errors),'1e-8')
    return base.SHOW(max(errors))
def grid_case(ch,n,offset,par,vals,H,U,Ud,shift):
    pn={k:float(v) for k,v in par.items()};raw=initial_lift(n,offset,par,vals,H,U,Ud,shift)
    out=restore_undivided(raw,pn);checks=base.Checks();D=raw['D'];q,p=out['q'],out['p']
    unstabilized_curvature=canonical.spatial_geometry(raw['q'],D.matrix)[4]
    flux_error=abs(out['Hdirect']-out['H'])/(1+abs(out['H']))
    checks.small('periodic_flux_forms_agree',flux_error,'1e-8')
    checks.add('initial_configuration_and_means_not_projected',np.array_equal(q,raw['q']))
    checks.add('analytic_node_included_exactly',q[0,7]==0 and out['g'][0]==0)
    checks.small('derivative_of_exact_constants',np.max(abs(D@np.ones(n))),'1e-8')
    checks.small('Fourier_derivative',np.max(abs(D@np.cos(raw['theta'])+40*np.sin(raw['theta']))),'1e-8')
    eye=np.eye(n)-np.ones((n,n))/n
    checks.small('periodic_primitive',np.max(abs(D@raw['I']-eye)),'1e-8')
    checks.small('derivative_adjoint_control',np.max(abs(D.matrix+D.matrix.T)),'1e-8')
    CC=planar.true_constraints(q,p,D)
    checks.small('all_original_spatial_constraints',np.max(abs(CC)),'1e-8')
    checks.small('forward_momenta_retained_by_spatial_restore',np.max(abs(p[:,:12]-raw['p'][:,:12])/(1+abs(raw['p'][:,:12]))),'1e-8')
    checks.small('both_declared_global_charges',max(abs(np.mean(p[:,14])-.2),
        abs(np.mean(q[:,9]*p[:,10]-q[:,10]*p[:,9])-raw['Qtheta'])),'1e-8')
    checks.add('local_dust_positive',np.min(p[:,14])>0,repr(float(np.min(p[:,14]))))
    target=np.array([np.mean(p[:,2]/2),np.mean(p[:,4]/2),np.mean(p[:,5])])
    checks.small('mean_metric_momenta_retained',np.max(abs(target-raw['mean_pi'])),'1e-8')
    checks.small('nodal_p_psi_on_natural_scalar_scale',
                 abs(p[0,12]-pn['K_Q']*raw['rate'])/(pn['K_Q']*raw['rate']),'1e-4')
    # The original generator has no divided force inverse.
    sh=np.column_stack((.02*np.sin(raw['theta']),.03*np.cos(raw['theta']),.04*np.sin(2*raw['theta'])))
    gg=canonical.diffeo(q,p,sh,D)/(2*np.pi)
    checks.small('original_unreduced_diffeomorphism_generator',abs(gg-np.mean(np.sum(CC*sh,axis=1))),'1e-8')
    flows=[flow(checks,raw,pn,1e-18)]
    if n==25:flows.append(flow(checks,raw,pn,1e-22))
    # Full nodal Z variation, preserving charges and all mean metric momenta.
    r=dict(raw,q=raw['q'].astype(complex));r['q'][0,13]+=1j*1e-20
    HZ=n*np.imag(restore_undivided(r,pn)['H'])/1e-20
    checks.small('original_auxiliary_nodal_Z_row',abs(HZ)/(1+pn['b']/raw['rate']),'1e-8')
    checks.add('deleting_lapse_flux_changes_node_row',abs(out['divF'][0]/raw['rate']**2)>1e-12,
               repr(float(out['divF'][0]/raw['rate']**2)))
    if n==17:
        for label,change in [('zero_clock','clock'),('changed_dust_charge','charge')]:
            r=dict(raw,s=raw['s'].copy(),p=raw['p'].copy())
            if change=='clock':r['s'][0]=0
            else:r['p'][:,14]+=.01
            bad=False
            try:restore_undivided(r,pn)
            except ValueError as exc:bad=('clock' in str(exc) if change=='clock' else 'charge' in str(exc))
            checks.add('guard_'+label,bad)
    indep=independent_node(checks,raw,out,par) if n==25 else None
    nodal.reg.joint.merge_checks(ch,checks.rows,f'{n}_{offset}_')
    return dict(grid=n,node_orientation=offset,minimum_dust=repr(float(np.min(p[:,14]))),
        original_spatial_residual=repr(float(np.max(abs(CC)))),mean_dust=repr(float(np.mean(p[:,14]))),
        mean_phase=repr(float(np.mean(q[:,9]*p[:,10]-q[:,10]*p[:,9]))),flows=flows,
        nodal_Z_row=repr(float(HZ)),independent_node_error=indep,Hpsi=repr(float(np.real(out['H']))),
        periodic_flux_forms_error=repr(float(flux_error)),
        unstabilized_curvature_noise=repr(float(np.max(abs(unstabilized_curvature-out['R3'])))),
        status='FINITE_GRID_INITIAL_FLOW_CONTROL_NOT_FULL_ADMISSION')
def case_job(task):
    index,point,initial=task;mp.mp.dps=100;mp.iv.dps=80;ch=base.Checks();records=[]
    try:
        par,vals,H,U,Ud,g8,g12=setup(point,initial)
        error=max(abs(a-b)/(1+abs(a)+abs(b)) for t in (0,mp.pi/7,mp.pi/2)
                  for a,b in zip(g8(t),g12(t)))
        ch.small('original8_12_shift_control',error,'1e-30')
        for n in (17,25,33):
            for offset in (0,1):records.append(grid_case(ch,n,offset,par,vals,H,U,Ud,g12))
    except Exception:ch.add('unexpected_case_exception',False,traceback.format_exc())
    return index,dict(family=point['family'],eta=point['eta'],controls=records,
        physical_spectrum_computed=False,full_admission=False,state_adopted_or_evolved=False),ch.rows
def calculate(workers):
    pins,before=sources();ch=base.Checks()
    points=READ(nodal.reg.JOINT+'independent.json');initial=READ(cop.CERTS)
    if not(len(points)==len(initial)==9):raise ValueError('case count')
    if any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):
        raise ValueError('input family/eta ordering mismatch')
    tasks=[(i,a,b) for i,(a,b) in enumerate(zip(points,initial))];out={}
    progress('global_nodal_lift_cases',cases=9,workers=min(workers,9))
    if workers==1:
        for t in tasks:
            r=case_job(t);out[r[0]]=r;progress('global_nodal_lift_case_complete',index=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for f in as_completed(jobs):
                r=f.result()
                if r[0]!=jobs[f] or r[0] in out:raise ValueError('case identity')
                out[r[0]]=r;progress('global_nodal_lift_case_complete',index=r[0])
    records=[]
    for i in range(9):
        _,record,rows=out[i];records.append(record)
        nodal.reg.joint.merge_checks(ch,rows,record['family']+'_'+record['eta']+'_')
    _,after=sources();ch.add('original_source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    su=dict(validation='PASS_GLOBAL_NODAL_INITIAL_FLOW_ONLY' if passed==len(ch.rows) else 'FAIL_OR_UNRESOLVED_GLOBAL_NODAL_LIFT',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='GLOBAL_NODAL_LIFT_INITIAL_FLOW_CONTROL_COMPLETE_DAE_SPECTRUM_WINDOW_OPEN' if passed==len(ch.rows)
               else 'GLOBAL_NODAL_LIFT_OR_INITIAL_FLOW_REJECTED_OR_PRECISION_HOLD',
        full_initial_admission=False,background_momentum_evolution_verified=False,full_nodal_hierarchy_verified=False,
        physical_mode_spectrum_computed=False,physical_frequency_window_established=False,state_adopted_or_evolved=False,
        stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    form=dict(global_restore='original mean/charge/spatial solution with pZ=-g*s; g=0 allowed, s>0 required',
        forward_lift='P_y=R*y+ell; ppsi=-partial_s(E0)|P_y-g*Zhat; local pT from lapse with flux',
        derivative_stability='D(f-f[0]) keeps the derivative of an exact constant exactly zero; no state/physical mean projected',
        physical_holds='Initial coordinate-flow comparison only; full momentum evolution/nodal hierarchy, physical function space, Hessian/drift/spectrum/window remain open')
    return {'summary.json':su,'formulas.json':form,'independent.json':records}
def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay')
    p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose output or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    record=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:record(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(nodal.v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
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
