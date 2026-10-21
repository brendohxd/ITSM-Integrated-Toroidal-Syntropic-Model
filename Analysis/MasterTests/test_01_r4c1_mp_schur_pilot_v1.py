"""Time-bounded, complete-dimension multiprecision Schur pilot; no physical clearance."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,multiprocessing,os,time,traceback
from pathlib import Path
import mpmath as mp
from mpmath.matrices import eigen as me
import numpy as np
from scipy.optimize import linear_sum_assignment
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_canonical_conditioning_v1.py'
PSHA='013f84f8a342b68d8d2c86c18eeb3e9552599709b9f5ee5cd2462704992aef89'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_MP_SCHUR_PILOT_V1_CONTRACT_2026-10-20.md'
CSHA='13d1a6b7af9b65faa75f232db679be52ffc2cd1e3d1fbb1cce19d576deae1725'
BASE='Analysis/MasterTests/outputs/r4c1_canonical_conditioning_v1_n17_attempt_01/'
INPUT=BASE+'shear_04_n17_o0.json'
REPORT='Theory/Gates/RES-001/RES001_R4C1_CANONICAL_CONDITIONING_V1_REPORT_2026-10-20.md'
LIBSHA='19b0d72370a2c7311d5f1af51bceae5169009e002f77ed39326490f93b2eff99'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
spec=importlib.util.spec_from_file_location('frozen_conditioning_v1',ROOT/PARENT)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
pv=old.pv
PINS={**old.PINS,PARENT:PSHA,CONTRACT:CSHA,
 REPORT:'1a2abd9bfc8716e9b0b04732a0e7dfb36d8b1c01e537d0ae56f70f9e4ed8cd48',
 BASE+'run_inputs.json':'653a3eb897bf12745592d14eeb9fbfb9bce0a15dbfc4af63aa7e73643c9e4c39',
 INPUT:'19737ca7549510770bc4f66fd0ad55361cb37316dac5ca8d35fd8fc27c24d2ee',
 BASE+'case_04_n17_o0.json':'91af5028e7989fe724c1a529f78998ca4e65dbc916d08b2c696a8bc4dd01d929'}
BRANCHES=((35,False),(50,False),(50,True))
_PROGRESS=None

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0]!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    lib=Path(me.__file__)
    if mp.__version__!='1.3.0' or SHA(lib.read_bytes())!=LIBSHA:raise ValueError('installed mpmath algorithm drift')
    meta['installed-mpmath/eigen.py']=dict(sha256=LIBSHA,bytes=lib.stat().st_size,mtime_ns=lib.stat().st_mtime_ns)
    return pins,meta

def emit(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')
def encz(z,dps):return [mp.nstr(mp.re(z),dps+12),mp.nstr(mp.im(z),dps+12)]
def decz(z):return mp.mpc(mp.mpf(z[0]),mp.mpf(z[1]))
def encm(A,dps):return [[encz(A[i,j],dps) for j in range(A.cols)] for i in range(A.rows)]
def decm(a):return mp.matrix([[decz(z) for z in row] for row in a])
def numpy_matrix(A):return np.asarray([[complex(A[i,j]) for j in range(A.cols)] for i in range(A.rows)])

def prepare(dps,rescaled):
    mp.mp.dps=dps
    packed=(ROOT/INPUT).read_bytes()
    if SHA(packed)!=PINS[INPUT]:raise ValueError('matrix changed during phase preparation')
    raw=json.loads(packed)['data']['transformed_forms']['100'];S=mp.matrix(raw);D=S.rows;d=D//2
    diag=[abs(S[i,i]) for i in range(D)];floor=max(diag)*mp.mpf('1e-30')
    if floor==0:raise ValueError('degenerate balancing floor')
    s=[(max(diag[d+i],floor)/max(diag[i],floor))**mp.mpf('.25') for i in range(d)]
    sc=s+[1/x for x in s];B=mp.matrix([[sc[i]*S[i,j]*sc[j] for j in range(D)] for i in range(D)])
    A=mp.matrix(D,D);A[:d,:]=B[d:,:];A[d:,:]=-B[:d,:]
    if rescaled:
        x=[mp.mpf(2)**((i%3)-1) for i in range(d)];x=x+[1/z for z in x]
        A=mp.matrix([[A[i,j]*x[j]/x[i] for j in range(D)] for i in range(D)])
    return A

def worker(conn,phase,dps,rescaled,dependency):
    try:
        mp.mp.dps=dps
        if phase=='timeout_control':time.sleep(10);data={}
        elif phase=='hessenberg':
            A=prepare(dps,rescaled);Q,F=mp.hessenberg(A);data=dict(Q=encm(Q,dps),form=encm(F,dps),dimension=A.rows)
        elif phase=='schur':
            path,want=dependency;p=ROOT/path;b=p.read_bytes()
            if SHA(b)!=want or Path(str(p)+'.sha256').read_text().split()[0]!=want:raise ValueError('phase dependency drift')
            prior=json.loads(b)['data'];Q,F=decm(prior['Q']),decm(prior['form'])
            me.hessenberg_qr(mp.mp,F,Q)
            data=dict(Q=encm(Q,dps),form=encm(F,dps),dimension=F.rows,eigenvalues=[encz(F[i,i],dps) for i in range(F.rows)])
        else:raise ValueError('unknown phase')
        conn.send(dict(status='COMPLETED',data=data))
    except BaseException:conn.send(dict(status='EXECUTION_ERROR',error=traceback.format_exc()))
    finally:conn.close()

def bounded_phase(phase,dps,rescaled,dependency=None,budget=180):
    ctx=multiprocessing.get_context('spawn');recv,send=ctx.Pipe(duplex=False)
    p=ctx.Process(target=worker,args=(send,phase,dps,rescaled,dependency));p.start();send.close()
    start=time.monotonic();last=start;result=None
    emit('phase_started',phase=phase,precision=dps,rescaled=rescaled,pid=p.pid)
    try:
        while True:
            if recv.poll(.5):
                try:result=recv.recv()
                except EOFError:result=dict(status='EXECUTION_ERROR',error='owned child closed result pipe')
                break
            now=time.monotonic()
            if not p.is_alive():result=dict(status='EXECUTION_ERROR',error='owned child exited without a result');break
            if now-start>=budget:result=dict(status='TIME_BUDGET_REACHED',budget_seconds=budget);break
            if now-last>=15:
                emit('verified_phase_wait',phase=phase,precision=dps,rescaled=rescaled,pid=p.pid,process_alive=p.is_alive());last=now
    finally:
        if result is None or result['status']!='COMPLETED':
            if p.is_alive():p.terminate()
        p.join(5)
        if p.is_alive():p.kill();p.join(5)
        recv.close()
    return result

def verify(ch,A,data,phase,dps):
    mp.mp.dps=dps;Q,F=decm(data['Q']),decm(data['form']);a,q,f=numpy_matrix(A),numpy_matrix(Q),numpy_matrix(F);D=len(a)
    with threadpool_limits(limits=1,user_api='blas'):
        backward=float(np.linalg.norm(a@q-q@f)/(1+np.linalg.norm(a)*np.linalg.norm(q)+np.linalg.norm(q)*np.linalg.norm(f)))
        unitary=float(np.linalg.norm(q.conj().T@q-np.eye(D))/D)
        lower=float(np.max(abs(np.tril(f,-2 if phase=='hessenberg' else -1)))/(1+np.linalg.norm(f)))
    ch.small('complete_factorization_backward',mp.mpf(backward),'1e-8')
    ch.small('complete_transformation_unitarity',mp.mpf(unitary),'1e-8')
    ch.small('complete_structure_residual',mp.mpf(lower),'1e-8')
    ch.add('all_retained_dimensions',Q.rows==D and F.rows==D and D==A.rows)
    if phase=='schur':
        E=[decz(x) for x in data['eigenvalues']];tr=sum(A[i,i] for i in range(D));tr2=sum(A[i,j]*A[j,i] for i in range(D) for j in range(D))
        ch.small('complete_trace_identity',abs(sum(E)-tr)/(1+sum(abs(e) for e in E)+abs(tr)),'1e-8')
        ch.small('complete_trace_square_identity',abs(sum(e*e for e in E)-tr2)/(1+sum(abs(e*e) for e in E)+abs(tr2)),'1e-8')
    return dict(backward=backward,unitarity=unitary,structure=lower)

def spectral_distance(a,b):
    x=[decz(z) for z in a];y=[decz(z) for z in b];xf=np.asarray([complex(z) for z in x]);yf=np.asarray([complex(z) for z in y])
    cost=abs(xf[:,None]-yf[None,:])/(1+abs(xf[:,None])+abs(yf[None,:]));ia,ib=linear_sum_assignment(cost)
    return max(abs(x[i]-y[j])/(1+abs(x[i])+abs(y[j])) for i,j in zip(ia,ib))

def smoke():
    _,before=sources();ch=pv.base.Checks();mp.mp.dps=50
    H=mp.matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
    T=mp.matrix([[-3,mp.mpf(1)/7,0,1],[0,-1,1,0],[0,0,2,1],[0,0,0,5]])
    cases=[(H*T*H.T,[-3,-1,2,5]),(mp.matrix([[0,1],[0,0]]),[0,0]),(mp.matrix([[0,-1],[1,0]]),[mp.j,-mp.j])]
    for i,(A,expect) in enumerate(cases):
        Q,F=mp.hessenberg(A);me.hessenberg_qr(mp.mp,F,Q)
        data=dict(Q=encm(Q,50),form=encm(F,50),dimension=A.rows,eigenvalues=[encz(F[j,j],50) for j in range(F.rows)])
        loc=pv.base.Checks();verify(loc,A,data,'schur',50);pv.nodal.reg.joint.merge_checks(ch,loc.rows,str(i)+'_')
        ch.small('known_complete_spectrum_'+str(i),spectral_distance(data['eigenvalues'],[encz(x,50) for x in expect]),'1e-6')
        if i==1:ch.add('Jordan_offdiagonal_retained',abs(F[0,1])>0)
    stop=bounded_phase('timeout_control',35,False,budget=3)
    ch.add('owned_child_timeout_path',stop['status']=='TIME_BUDGET_REACHED')
    _,after=sources();ch.add('source_metadata_unchanged',before==after)
    n=sum(r['passed'] for r in ch.rows);print(json.dumps(dict(scope='EXECUTION_ALGEBRA_ONLY',passed=n,total=len(ch.rows),failed=[r for r in ch.rows if not r['passed']])));return 0 if n==len(ch.rows) else 1

def execute(args,dest):
    pins,before=sources();ch=pv.base.Checks();manifest=ENC(dict(source_sha256=pins,source_metadata=before,key=[4,17,0],branches=BRANCHES,
      phase_budget_seconds=180,mpmath=mp.__version__,backend=old.old.backend_identity()))
    runsha=SHA(manifest)
    if args.output:old.old.num.write_pair(dest,'run_inputs.json',manifest)
    else:old.old.num.check_pair(dest,'run_inputs.json',manifest)
    stages={};execution_status='COMPLETED';stop_point=None
    for dps,scaled in BRANCHES:
        for phase in ('hessenberg','schur'):
            name='%s_d%d_s%d.json'%(phase,dps,scaled);previous='hessenberg_d%d_s%d.json'%(dps,scaled)
            if args.resume and (dest/name).exists():
                obj=json.loads(old.old.num.check_pair(dest,name))
                if obj['run_input_sha256']!=runsha:raise ValueError('resume provenance')
            else:
                dep=((dest/previous).relative_to(ROOT).as_posix(),SHA((dest/previous).read_bytes())) if phase=='schur' else None
                outcome=bounded_phase(phase,dps,scaled,dep)
                if outcome['status']!='COMPLETED':
                    execution_status=outcome['status'];stop_point=dict(phase=phase,precision=dps,rescaled=scaled,outcome=outcome);break
                local=pv.base.Checks();A=prepare(dps,scaled);metrics=verify(local,A,outcome['data'],phase,dps)
                obj=dict(run_input_sha256=runsha,phase=phase,precision=dps,rescaled=scaled,data=outcome['data'],metrics=metrics,checks=local.rows)
                if args.replay:old.old.num.check_pair(dest,name,ENC(obj))
                else:old.old.num.write_pair(dest,name,ENC(obj))
            stages[name]=obj;pv.nodal.reg.joint.merge_checks(ch,obj['checks'],name+'_');emit('phase_sealed',phase=phase,precision=dps,rescaled=scaled)
        if stop_point:break
    complete=len(stages)==6
    if complete:
        mp.mp.dps=65
        a=stages['schur_d35_s0.json']['data']['eigenvalues'];b=stages['schur_d50_s0.json']['data']['eigenvalues'];c=stages['schur_d50_s1.json']['data']['eigenvalues']
        ch.small('complete_spectrum_35_50_precision_agreement',spectral_distance(a,b),'1e-6')
        ch.small('complete_spectrum_independent_canonical_rescaling',spectral_distance(b,c),'1e-6')
    else:ch.add('complete_precision_pilot',False,str(stop_point))
    _,after=sources();ch.add('source_metadata_unchanged',before==after)
    n=sum(r['passed'] for r in ch.rows)
    validation=('PASS_ONE_CASE_SCHUR_PRECISION_ONLY' if n==len(ch.rows) else 'UNRESOLVED_SCHUR_PILOT') if complete else 'EXECUTION_LIMIT_OR_ERROR_NO_SCIENTIFIC_ACCEPTANCE'
    summary=dict(validation=validation,passed=n,total=len(ch.rows),checks=ch.rows,execution_status=execution_status,stop_point=stop_point,
      source_sha256=pins,source_metadata=before,complete_schur_pilot=complete,complete_family_coverage=False,
      left_right_physical_modes_normalized=False,certified_forward_eigenvalue_enclosures=False,
      stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)
    index=[dict(file=name,sha256=SHA(ENC(obj))) for name,obj in sorted(stages.items())]
    formulas=dict(scope='One complete n17 matrix, staged full Hessenberg/Schur factors; no physical mode/energy normalization',
      holds='all-family precision, physical space, negative/nonoscillatory directions, refinement, interactions, healthy GR and matching remain open')
    for name,obj in (('summary.json',summary),('independent.json',index),('formulas.json',formulas)):
        if args.replay:old.old.num.check_pair(dest,name,ENC(obj))
        else:old.old.num.write_pair(dest,name,ENC(obj))
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','execution_status','complete_schur_pilot')}),flush=True)
    return 0 if complete and n==len(ch.rows) else 1

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--resume');p.add_argument('--replay');p.add_argument('--smoke',action='store_true');p.add_argument('--progress-log');a=p.parse_args()
    if a.smoke:
        if any((a.output,a.resume,a.replay)):p.error('smoke is execution-only')
        return smoke()
    if sum(bool(x) for x in (a.output,a.resume,a.replay))!=1:p.error('choose output, resume or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.resume or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    if a.resume and (dest/'summary.json').exists():raise ValueError('terminal attempt cannot resume')
    before={f.name:old.old.num.file_metadata(f) for f in dest.iterdir()} if a.replay else None
    rc=execute(a,dest)
    if a.replay:
        if before!={f.name:old.old.num.file_metadata(f) for f in dest.iterdir()}:raise ValueError('replay byte/metadata/set mutation')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    return rc
if __name__=='__main__':raise SystemExit(main())
