"""Constant canonical shears of sealed complete matrices; no physical admission."""
from __future__ import annotations
import argparse,gc,hashlib,importlib.util,json,multiprocessing,os,queue,traceback
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sy
from scipy.optimize import linear_sum_assignment
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_canonical_spectrum_v3.py'
PSHA='cce30d6764af1c067785cc876f1c89c9214b977f4b49e79907e57f1256b6eb6f'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CANONICAL_CONDITIONING_V1_CONTRACT_2026-10-20.md'
CSHA='a21377bfbbd83236414f916adc3a88f19ae24ff4d9fb230a96e2865e82dcab6e'
INPUT='Analysis/MasterTests/outputs/r4c1_canonical_spectrum_v3_n17_attempt_01/'
INDEX=INPUT+'independent.json'
ISHA='75d7f1acc3c244d198383aa21e61c8f83fbb8f5d98078c12f474801b69f42bda'
REPORT='Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SPECTRUM_V3_REPORT_2026-10-20.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA or SHA((ROOT/INDEX).read_bytes())!=ISHA:raise ValueError('parent/input-index drift')
spec=importlib.util.spec_from_file_location('frozen_canonical_v3',ROOT/PARENT)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
pv=old.pv
ENTRIES={tuple(r['key']):r for r in json.loads((ROOT/INDEX).read_bytes())}
PINS={**old.PINS,PARENT:PSHA,CONTRACT:CSHA,INDEX:ISHA,
 REPORT:'3a1517866a92ffd19e82af23ac2ebaf75382502b952d01a3e04b29e4c4fc21a9',
 INPUT+'run_inputs.json':'5547070c7db19931a7bb3b6eacea34634cb598f313e11ef55c2e80b8d11feca3',
 INPUT+'summary.json':'f533aa4456d51500e62b7aa5d424d36c3c3ab97cd879ffff8cc5ba286dc4f753',
 INPUT+'formulas.json':'0b70c587079dc436e5173d1cc2569837c3d66728994b46a8f5fd910f4e8efd69'}
for row in ENTRIES.values():
    PINS[INPUT+row['matrix_file']]=row['matrix_sha256']
    PINS[INPUT+row['spectrum_file']]=row['spectrum_sha256']
_EVENTS=None
_PROGRESS=None
case_name=lambda k:'case_%02d_n%d_o%d.json'%k
shear_name=lambda k:'shear_%02d_n%d_o%d.json'%k

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0].lower()!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    return pins,meta

def emit(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')
def worker_init(events):
    global _EVENTS
    _EVENTS=events
def event(key,stage,**kw):
    if _EVENTS is not None:_EVENTS.put(dict(key=list(key),stage=stage,pid=os.getpid(),**kw))
def relative(A,B):
    return max(abs(A[i,j]-B[i,j])/(1+abs(A[i,j])+abs(B[i,j])) for i in range(A.rows) for j in range(A.cols))
def strings(A,digits):return [[mp.nstr(A[i,j],digits) for j in range(A.cols)] for i in range(A.rows)]

def shear(S,key,precision,ch):
    d=S.rows//2;K=S[:d,:d];C=S[:d,d:];B=S[d:,:d];M=S[d:,d:]
    event(key,'factor_start',precision=precision,dimension=d)
    LU,piv=mp.mp.LU_decomp(M,use_cache=False);F=mp.matrix(d,d)
    for j in range(d):
        x=mp.mp.U_solve(LU,mp.mp.L_solve(LU,B.column(j),piv))
        for i in range(d):F[i,j]=x[i]
        if j%16==15 or j+1==d:event(key,'mixed_solve_columns',precision=precision,done=j+1,total=d)
    ch.small('full_mixed_solve_residual',relative(M*F,B),'1e-8')
    L=(F+F.T)/2
    ch.small('canonical_shear_generator_symmetry',relative(L,L.T),'1e-8')
    event(key,'congruence_start',precision=precision)
    ML=M*L;LM=L.T*M;Bn=B-ML;Cn=C-LM;CL=C*L;LR=L.T*Bn
    Kn=K-CL-LR
    Sn=mp.matrix(2*d,2*d);Sn[:d,:d]=Kn;Sn[:d,d:]=Cn;Sn[d:,:d]=Bn;Sn[d:,d:]=M
    # Reassembly checks are algebraic; generic direct-product controls below are independent.
    ch.small('inverse_block_reassembly_algebraic',max(relative(Kn+CL+LR,K),relative(Cn+LM,C),relative(Bn+ML,B)),'1e-8')
    ch.add('all_directions_retained',Sn.rows==S.rows and Sn.cols==S.cols)
    return Sn,L

def pair_distance(a,b):
    x=np.asarray([complex(*r['lambda_psi']) for r in a['modes']]);y=np.asarray([complex(*r['lambda_psi']) for r in b['modes']])
    cost=abs(x[:,None]-y[None,:])/(1+abs(x[:,None])+abs(y[None,:]));ia,ib=linear_sum_assignment(cost)
    return float(cost[ia,ib].max())

def mapping_controls(ch,original,transformed,L,spectrum):
    M=np.asarray(original,float);N=np.asarray(transformed,float);LL=np.asarray(L,float);d=len(M)//2
    scale=np.asarray(spectrum['canonical_balancing_factors']);scale=np.r_[scale,1/scale]
    H=scale[:,None]*N*scale[None,:];A=np.r_[H[d:,:],-H[:d,:]];A0=np.r_[M[d:,:],-M[:d,:]]
    with threadpool_limits(limits=1,user_api='blas'):
        lam,R=np.linalg.eig(A);v=scale[:,None]*R;u=np.r_[v[:d],v[d:]-LL@v[:d]]
        residual=np.linalg.norm(A0@u-u*lam[None,:],axis=0)/((np.linalg.norm(A0)+abs(lam))*np.linalg.norm(u,axis=0))
        oldnorm=np.real(1j*np.sum(u.conj()*np.r_[-u[d:],u[:d]],axis=0))
        newnorm=np.real(1j*np.sum(R.conj()*np.r_[-R[d:],R[:d]],axis=0))
        err=np.max(abs(oldnorm-newnorm)/(1+abs(oldnorm)+abs(newnorm)))
    ch.small('mapped_original_coordinate_backward_error',mp.mpf(float(residual.max())),'1e-8')
    ch.small('mapped_canonical_action_norm',mp.mpf(float(err)),'1e-8')
    return dict(max_original_backward_error=float(residual.max()),max_action_norm_mapping_error=float(err))

def transform_job(key):
    mp.mp.dps=100;ch=pv.base.Checks();result={}
    try:
        event(key,'case_start')
        src=json.loads((ROOT/(INPUT+ENTRIES[key]['matrix_file'])).read_bytes());data=src['data'];raw=data['canonical_quadratic_form']
        blocks={};Ls={}
        for precision in (80,100):
            with mp.workdps(precision):
                local=pv.base.Checks();A=mp.matrix(raw);Sn,L=shear(A,key,precision,local)
                pv.nodal.reg.joint.merge_checks(ch,local.rows,'precision_'+str(precision)+'_')
                blocks[str(precision)]=strings(Sn,precision);Ls[str(precision)]=strings(L,precision)
            gc.collect()
        ch.small('complete_transformed_matrix_precision_agreement',relative(mp.matrix(blocks['80']),mp.matrix(blocks['100'])),'1e-8')
        result=dict(family=data['family'],eta=data['eta'],key=list(key),dimension=len(raw),
          transformed_forms=blocks,shears=Ls,full_input_matrix=ENTRIES[key]['matrix_file'],
          numerical_coordinate_change_only=True,state_adopted_or_evolved=False,physical_window_established=False)
    except Exception:ch.add('representation_route_unresolved',False,traceback.format_exc())
    return key,result,ch.rows

def smoke():
    _,before=sources();mp.mp.dps=100;ch=pv.base.Checks();old.cv.engine_controls(ch)
    # Independent exact generic-block proof: S need not be symmetric.
    S=sy.Matrix(4,4,sy.symbols('a0:16'));l0,l1,l2=sy.symbols('l0:3');L=sy.Matrix([[l0,l1],[l1,l2]])
    I=sy.eye(2);Z=sy.zeros(2);T=I.row_join(Z).col_join((-L).row_join(I));Ti=I.row_join(Z).col_join(L.row_join(I))
    O=Z.row_join(-I).col_join(I.row_join(Z));J=-O
    K,C,B,M=S[:2,:2],S[:2,2:],S[2:,:2],S[2:,2:]
    N=(K-C*L-L.T*(B-M*L)).row_join(C-L.T*M).col_join((B-M*L).row_join(M))
    zero=lambda A:all(sy.expand(x)==0 for x in A)
    ch.add('exact_generic_block_congruence',zero(N-T.T*S*T))
    ch.add('exact_symplectic_and_inverse',zero(T.T*O*T-O) and zero(T*Ti-sy.eye(4)))
    ch.add('exact_Hamiltonian_similarity',zero(J*N-Ti*(J*S)*T))
    for i,(sign,kappa) in enumerate(((1,mp.mpf(9)/49),(-1,mp.mpf(9)/49),(1,-mp.mpf(2)/7),(1,mp.mpf(0)))):
        a=mp.mpf(10)**12;S=sign*mp.matrix([[a*a+kappa,a],[a,mp.mpf(1)]])
        loc=pv.base.Checks();N,L=shear(S,(-1,0,i),100,loc)
        pv.nodal.reg.joint.merge_checks(ch,loc.rows,'oscillator_'+str(i)+'_')
        T=mp.eye(2);T[1,0]=-L[0,0]
        ch.small('independent_direct_product_'+str(i),relative(N,T.T*S*T),'1e-8')
        sc=pv.base.Checks();out=old.spectral(sc,strings(N,100),{'rate':mp.mpf(1),'H':mp.mpf(1)})
        pv.nodal.reg.joint.merge_checks(ch,sc.rows,'oscillator_spectrum_'+str(i)+'_')
        if kappa>0:
            pos=[r for r in out['modes'] if r['lambda_psi'][1]>0]
            ch.add('signed_action_retained_'+str(i),len(pos)==1 and pos[0]['Krein_sign']==sign)
        elif kappa<0:ch.add('real_growing_pair_retained',len(out['modes'])==2 and any(r['lambda_psi'][0]>0 for r in out['modes']))
        else:ch.add('zero_modes_retained_without_sign',len(out['modes'])==2 and all(r['Krein_sign'] is None for r in out['modes']))
    S=mp.matrix([[3,1,2,0],[1,4,0,1],[0,2,2,0],[1,0,0,3]]);loc=pv.base.Checks();N,L=shear(S,(-2,0,0),100,loc)
    T=mp.eye(4);T[2:,:2]=-L
    ch.small('nonsymmetric_input_and_mixed_remainder_retained',relative(N,T.T*S*T),'1e-8')
    ch.add('antisymmetric_mixed_remainder_not_erased',any(N[i,j]!=0 for i in range(2,4) for j in range(2)))
    rejected=False
    try:shear(mp.matrix([[1,0],[0,0]]),(-3,0,0),100,pv.base.Checks())
    except ZeroDivisionError:rejected=True
    ch.add('singular_momentum_block_rejected',rejected)
    _,after=sources();ch.add('smoke_source_metadata_unchanged',before==after)
    n=sum(r['passed'] for r in ch.rows);print(json.dumps(dict(scope='EXECUTION_ALGEBRA_ONLY',passed=n,total=len(ch.rows),failed=[r for r in ch.rows if not r['passed']])));return 0 if n==len(ch.rows) else 1

def execute(args,dest):
    pins,before=sources();ch=pv.base.Checks()
    keys=set(ENTRIES) if not args.keys else {tuple(map(int,k.split(':'))) for k in args.keys.split(',')}
    if not keys or not keys<=set(ENTRIES):raise ValueError('foreign selected keys')
    manifest=ENC(dict(source_sha256=pins,source_metadata=before,keys=[list(k) for k in sorted(keys)],backend=old.backend_identity()))
    runsha=SHA(manifest)
    if args.output:old.num.write_pair(dest,'run_inputs.json',manifest)
    else:old.num.check_pair(dest,'run_inputs.json',manifest)
    transforms={};records={};pending=[]
    def accept(r):
        key,data,rows=r
        if key not in keys or key in transforms:raise ValueError('foreign/duplicate worker key')
        obj=dict(key=list(key),run_input_sha256=runsha,data=data,checks=rows);payload=ENC(obj)
        if args.replay:old.num.check_pair(dest,shear_name(key),payload)
        else:old.num.write_pair(dest,shear_name(key),payload)
        transforms[key]=obj;emit('shear_stage_sealed',key=key,passed=sum(r['passed'] for r in rows),total=len(rows))
    for key in sorted(keys):
        p=dest/shear_name(key)
        if args.resume and p.exists():
            obj=json.loads(old.num.check_pair(dest,p.name))
            if obj['key']!=list(key) or obj['run_input_sha256']!=runsha:raise ValueError('resume transform provenance')
            transforms[key]=obj
        else:pending.append(key)
    workers=min(pv.nodal.v4.selected_workers(args.workers),max(1,len(pending)));emit('shear_stage',cases=len(keys),pending=len(pending),workers=workers,parent_pid=os.getpid())
    if workers==1:
        for key in pending:accept(transform_job(key))
    elif pending:
        ctx=multiprocessing.get_context('spawn');events=ctx.Queue()
        with ProcessPoolExecutor(max_workers=workers,mp_context=ctx,initializer=worker_init,initargs=(events,)) as pool:
            jobs={pool.submit(transform_job,k):k for k in pending};remaining=set(jobs)
            while remaining:
                done,remaining=wait(remaining,timeout=1,return_when=FIRST_COMPLETED)
                while True:
                    try:e=events.get_nowait()
                    except queue.Empty:break
                    if tuple(e['key']) not in keys:raise ValueError('foreign progress key')
                    stage=e.pop('stage');emit('worker_'+stage,**e)
                for f in done:
                    r=f.result()
                    if r[0]!=jobs[f]:raise ValueError('worker identity')
                    accept(r)
        events.close();events.join_thread()
    emit('algebra_pool_released_before_spectrum');mp.mp.dps=100
    points=pv.lift.READ(pv.nodal.reg.JOINT+'independent.json')
    for key in sorted(keys):
        trans=transforms[key];ts=SHA(ENC(trans));p=dest/case_name(key)
        if args.resume and p.exists():
            obj=json.loads(old.num.check_pair(dest,p.name))
            if obj['key']!=list(key) or obj['run_input_sha256']!=runsha or obj['transform_sha256']!=ts:raise ValueError('resume spectrum provenance')
        else:
            local=pv.base.Checks();data={}
            try:
                t=trans['data'];raw={'rate':mp.mpf(points[key[0]]['eta'])/5,'H':mp.mpf(points[key[0]]['H'])};spectra={}
                for precision in ('80','100'):
                    c=pv.base.Checks();spectra[precision]=old.spectral(c,t['transformed_forms'][precision],raw)
                    pv.nodal.reg.joint.merge_checks(local,c.rows,'precision_'+precision+'_')
                local.small('complete_spectral_precision_agreement',mp.mpf(pair_distance(spectra['80'],spectra['100'])),'1e-6')
                orig=json.loads((ROOT/(INPUT+ENTRIES[key]['matrix_file'])).read_bytes())['data']['canonical_quadratic_form']
                mapping=mapping_controls(local,orig,t['transformed_forms']['100'],t['shears']['100'],spectra['100'])
                data=dict(spectra=spectra,mapping=mapping,physical_stability_established=False,physical_window_established=False)
            except Exception:local.add('spectrum_or_mapping_unresolved',False,traceback.format_exc())
            obj=dict(key=list(key),run_input_sha256=runsha,transform_sha256=ts,data=data,checks=local.rows)
            if args.replay:old.num.check_pair(dest,p.name,ENC(obj))
            else:old.num.write_pair(dest,p.name,ENC(obj))
        records[key]=obj;emit('spectrum_sealed',key=key,passed=sum(r['passed'] for r in obj['checks']),total=len(obj['checks']))
    index=[]
    for key in sorted(keys):
        for label,obj in (('shear',transforms[key]),('spectrum',records[key])):pv.nodal.reg.joint.merge_checks(ch,obj['checks'],'_'.join(map(str,key))+'_'+label+'_')
        index.append(dict(key=list(key),transform_sha256=SHA(ENC(transforms[key])),spectrum_sha256=SHA(ENC(records[key]))))
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows);ok=passed==len(ch.rows)
    summary=dict(validation='PASS_FINITE_CANONICAL_REPRESENTATION_ONLY' if ok else 'UNRESOLVED_CANONICAL_CONDITIONING',passed=passed,total=len(ch.rows),checks=ch.rows,
      source_sha256=pins,source_metadata=before,keys=[list(k) for k in sorted(keys)],complete_coarse_coverage=keys==set(ENTRIES),
      stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',physical_window_established=False)
    formulas=dict(shear='L=sym(M^-1*B); T=[[I,0],[-L,I]]; full nonsymmetrized S_new=T^T*S*T',
      holds='Numerical-coordinate diagnostic only; physical domain, refinement, interactions, healthy GR and identifying matching remain open')
    for name,obj in (('summary.json',summary),('independent.json',index),('formulas.json',formulas)):
        if args.replay:old.num.check_pair(dest,name,ENC(obj))
        else:old.num.write_pair(dest,name,ENC(obj))
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','complete_coarse_coverage')}),flush=True);return 0 if ok else 1

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--resume');p.add_argument('--replay');p.add_argument('--smoke',action='store_true');p.add_argument('--keys');p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
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
    if a.resume and (dest/'summary.json').exists():raise ValueError('complete output cannot resume')
    before={f.name:old.num.file_metadata(f) for f in dest.iterdir()} if a.replay else None
    rc=execute(a,dest)
    if a.replay:
        if before!={f.name:old.num.file_metadata(f) for f in dest.iterdir()}:raise ValueError('replay byte/metadata/set mutation')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    return rc
if __name__=='__main__':raise SystemExit(main())
