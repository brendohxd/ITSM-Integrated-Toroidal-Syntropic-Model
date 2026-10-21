"""Checkpointed unchanged-action matrices; OpenBLAS frozen-spectrum diagnostics."""
from __future__ import annotations
import argparse,faulthandler,gc,hashlib,importlib.util,json,multiprocessing,os,queue,sys,traceback
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import linear_sum_assignment
from threadpoolctl import threadpool_info,threadpool_limits

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_canonical_spectrum_v2.py'
PSHA='bf1f7d2f23d8fc233b062e7f4e6851d8932ab8e99a680f25f4d80869c3d16734'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SPECTRUM_V3_EXECUTION_ADDENDUM_2026-10-20.md'
CSHA='78fca3ef3e6dcc685a585ae4ff451f4d6089fd15582857a1bcb5067bc77492ce'
OLD='Analysis/MasterTests/outputs/r4c1_canonical_spectrum_n17_attempt_02/'
IMPORTS={(3,17,0):'0cdca2e57106a8d0ecc35b1a8f1c00c548acef5675f0fd826610808684e25e54',
 (4,17,0):'8f829c6201e60291a6b4068bf0e89ac59d066e248de4a3fea728267e8162e5ad',
 (5,17,1):'97ea907b0e34f3a7a72566e56f1e44c622886bcf9a1e2d16c51f23791615abe5',
 (7,17,0):'cbb902e65be655f900c3bbe3c296358920dd4de7eefdf016f4205302d013fc52'}
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('frozen parent drift')
spec=importlib.util.spec_from_file_location('frozen_canonical_v2',ROOT/PARENT)
num=importlib.util.module_from_spec(spec);spec.loader.exec_module(num)
cv,dc,pv=num.cv,num.dc,num.pv
PINS={**num.PINS,PARENT:PSHA,CONTRACT:CSHA,OLD+'run_inputs.json':
 '6ea6c50f668c645d4fac59a02a3e62456835ba9923483b36e0f5d276fed91775'}
case_name=lambda k:'case_%02d_n%d_o%d.json'%k
matrix_name=lambda k:'matrix_%02d_n%d_o%d.json'%k
PINS.update({OLD+case_name(k):h for k,h in IMPORTS.items()})
_EVENTS=None
_PROGRESS=None

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0].lower()!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    return pins,meta

def backend_identity():
    pools=[]
    for p in threadpool_info():
        f=Path(p['filepath'])
        pools.append({k:p.get(k) for k in ('internal_api','version','architecture','threading_layer')}
          |dict(library=f.name,sha256=SHA(f.read_bytes())))
    return dict(python=sys.version,numpy=np.__version__,scipy=num.scipy.__version__,
                eigensolver='numpy.linalg.eig/eigvals; installed OpenBLAS',loaded_libraries=pools)

def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')

def worker_init(events):
    global _EVENTS
    _EVENTS=events
    faulthandler.enable(all_threads=True)
    # Frozen matrix code emits progress only; no parent numerical state is changed.
    num.worker_init(events)

def matrix_job(task):
    i,point,initial,n,o=task;key=(i,n,o);mp.mp.dps=80;mp.iv.dps=80;ch=pv.base.Checks();data={}
    try:
        num.worker_event(key,'case_start')
        raw,X=pv.build_data(point,initial,n,o,80);y0,err=pv.baseline(raw,X);out=dc.functional(X,raw,y0)
        cache=cv.CachedHessian(raw,X,y0);T=dc.background(X,raw,y0,out)
        chart=num.CanonicalChart(raw,X,T,cache)
        num.worker_event(key,'cache_ready',dimension=chart.D,nodes=len(cache.t.nodes))
        num.controls(ch,raw,X,y0,out,T,cache,chart);gc.collect()
        S,metrics=num.materialize(ch,key,raw,X,y0,out,T,cache,chart)
        data=dict(family=point['family'],eta=point['eta'],grid=n,node_orientation=o,
          labels=[list(a) for a in chart.labels],metrics=metrics,
          canonical_quadratic_form=[[mp.nstr(x,80) for x in row] for row in S],
          auxiliary_block=[[mp.nstr(chart.A[a,b],80) for b in range(2)] for a in range(2)],
          full_matrix_materialized=True,refined_grid_convergence_established=False,
          continuum_domain_admitted=False,state_adopted_or_evolved=False)
        del chart,cache,S,out;gc.collect()
    except Exception:ch.add('unexpected_matrix_exception',False,traceback.format_exc())
    return key,data,ch.rows

def imported_matrix(key):
    obj=json.loads((ROOT/(OLD+case_name(key))).read_bytes())
    omitted=('complete_spectrum_constant_canonical_rescaling','all_eigenpair_backward_errors')
    rows=[r for r in obj['checks'] if r['name'] not in omitted]
    failed=[r for r in obj['checks'] if r['name'] in omitted]
    if obj['key']!=list(key) or len(rows)!=15 or not all(r['passed'] for r in rows):raise ValueError('legacy matrix controls')
    if len(failed)!=2 or any(r['passed'] for r in failed):raise ValueError('legacy failures not preserved')
    data={k:v for k,v in obj['data'].items() if k!='spectrum'}
    return data,rows,dict(source=OLD+case_name(key),sha256=IMPORTS[key],legacy_spectrum_failures=failed)

def spectral(ch,S,raw):
    M=np.array([[float(x) for x in row] for row in S]);D=len(M);d=D//2
    if not np.all(np.isfinite(M)):raise ValueError('nonfinite materialized generator')
    diag=np.abs(np.diag(M));floor=max(float(np.max(diag))*1e-30,np.finfo(float).tiny)
    q=np.maximum(diag[:d],floor);p=np.maximum(diag[d:],floor)
    scaling=(p/q)**.25;sc=np.r_[scaling,1/scaling]
    B=sc[:,None]*M*sc[None,:]
    A=np.r_[B[d:,:],-B[:d,:]]
    with threadpool_limits(limits=1,user_api='blas'):
        lam,right=np.linalg.eig(A)
        mu,left0=np.linalg.eig(A.T)
        lc=np.abs(lam.conj()[:,None]-mu[None,:])/(1+np.abs(lam[:,None])+np.abs(mu[None,:]))
        il,jl=linear_sum_assignment(lc);order=np.empty(D,dtype=int);order[il]=jl;left=left0[:,order]
        left_match=float(np.max(lc[il,jl]))
        extra=np.array([2.0**((i%3)-1) for i in range(d)]);extra=np.r_[extra,1/extra]
        other=np.linalg.eigvals(A*extra[None,:]/extra[:,None])
        cost=np.abs(lam[:,None]-other[None,:])/(1+np.abs(lam[:,None])+np.abs(other[None,:]))
        ia,ib=linear_sum_assignment(cost);match=float(np.max(cost[ia,ib]))
        Anorm=float(np.linalg.norm(A,ord='fro'));eps=np.finfo(float).eps
        left_errors=np.linalg.norm(A.T@left-left*lam.conj()[None,:],axis=0)/((Anorm+np.abs(lam))*np.linalg.norm(left,axis=0))
        rows=[];max_backward=0.
        for i,z in enumerate(lam):
            r=right[:,i];l=left[:,i];rn=float(np.linalg.norm(r));ln=float(np.linalg.norm(l))
            residual=float(np.linalg.norm(A@r-z*r));back=residual/((Anorm+abs(z))*rn)
            overlap=abs(np.vdot(l,r));cond=rn*ln/overlap if overlap else float('inf')
            uncertainty=cond*(residual/rn+100*eps*Anorm)
            max_backward=max(max_backward,back)
            N=float(np.real(1j*np.vdot(r,np.r_[-r[d:],r[:d]])))
            E=np.vdot(r,B@r);expected_energy=-1j*z*N
            energy_error=float(abs(E-expected_energy)/(1+abs(E)+abs(expected_energy)))
            near=[j for j,w in enumerate(lam) if j!=i and abs(z-w)/(1+abs(z)+abs(w))<1e-7]
            reliable=np.isfinite(uncertainty) and back<=1e-8 and match<=1e-6 and left_match<=1e-6 and left_errors[i]<=1e-8
            if not reliable or abs(z)<=10*uncertainty:status='UNRESOLVED_NEAR_ZERO_OR_ILL_CONDITIONED'
            elif abs(z.real)>10*uncertainty:status='FROZEN_NONOSCILLATORY_DIAGNOSTIC_NOT_PHYSICAL_INSTABILITY'
            else:status='OSCILLATORY_WITHIN_NUMERICAL_RESOLUTION'
            energy_status='NOT_ASSIGNED';sign=None;normalization=None
            if status=='OSCILLATORY_WITHIN_NUMERICAL_RESOLUTION' and z.imag>0:
                if energy_error>1e-8:energy_status='UNRESOLVED_MODE_ENERGY_IDENTITY'
                elif near:energy_status='DEGENERATE_SUBSPACE_NORMALIZATION_OUTSTANDING'
                elif abs(N)<=1e-10*rn*rn:energy_status='UNRESOLVED_SMALL_ACTION_NORM'
                else:sign=1 if N>0 else -1;normalization=float(1/np.sqrt(abs(N)));energy_status='CANONICAL_ACTION_NORM_RESOLVED_FROZEN_MODE_ONLY'
            safe=lambda x:float(x) if np.isfinite(x) else None
            rows.append(dict(index=i,lambda_psi=[float(z.real),float(z.imag)],
              lambda_reference_proper_time=[float(z.real)*float(raw['rate']),float(z.imag)*float(raw['rate'])],
              lambda_over_H=[float(z.real)*float(raw['rate']/raw['H']),float(z.imag)*float(raw['rate']/raw['H'])],
              backward_error=back,left_backward_error=float(left_errors[i]),left_right_condition=safe(cond),
              uncertainty_estimate_not_a_bound=safe(uncertainty),action_norm=N,status=status,energy_status=energy_status,
              Krein_sign=sign,canonical_energy=[float(E.real),float(E.imag)],energy_identity_error=energy_error,
              unit_action_amplitude_factor=normalization,nearby_mode_indices=near))
    ch.small('complete_spectrum_constant_canonical_rescaling',mp.mpf(match),'1e-6')
    ch.small('all_eigenpair_backward_errors',mp.mpf(max_backward),'1e-8')
    ch.small('left_conjugate_eigenvalue_matching',mp.mpf(left_match),'1e-6')
    ch.small('all_left_eigenpair_backward_errors',mp.mpf(float(np.max(left_errors))),'1e-8')
    rows.sort(key=lambda r:(r['lambda_psi'][0],r['lambda_psi'][1],r['index']))
    return dict(modes=rows,mode_count=len(rows),dimension=D,canonical_balancing_factors=[float(x) for x in scaling],
      rescaling_spectral_error=match,max_backward_error=max_backward,left_matching_error=left_match,
      max_left_backward_error=float(np.max(left_errors)),backend='NumPy OpenBLAS',
      energy_norm_scope='Canonical symplectic norm for resolvable nondegenerate frozen modes; not SI matching or an evolving energy theorem',
      physical_stability_established=False,physical_window_established=False)

def smoke():
    _,before=sources();ch=pv.base.Checks();cv.engine_controls(ch)
    raw={'rate':mp.mpf(1)/3,'H':mp.mpf(1)/5}
    for sign in (1,-1):
        local=pv.base.Checks();out=spectral(local,[[mp.mpf(sign),mp.mpf(0)],[mp.mpf(0),mp.mpf(sign)]],raw)
        pv.nodal.reg.joint.merge_checks(ch,local.rows,'oscillator_'+str(sign)+'_')
        pos=[r for r in out['modes'] if r['lambda_psi'][1]>0]
        ch.add('oscillator_energy_sign_'+str(sign),len(pos)==1 and pos[0]['Krein_sign']==sign)
    _,after=sources();ch.add('smoke_source_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    print(json.dumps(dict(scope='EXECUTION_ONLY_NO_COSMOLOGICAL_RECEIPT',passed=passed,total=len(ch.rows),
      failed=[r for r in ch.rows if not r['passed']])),flush=True)
    return 0 if passed==len(ch.rows) else 1

def execute(args,dest):
    pins,before=sources();ch=pv.base.Checks();cv.engine_controls(ch)
    points=pv.lift.READ(pv.nodal.reg.JOINT+'independent.json');initial=pv.lift.READ(pv.lift.cop.CERTS)
    if len(points)!=9 or len(initial)!=9 or any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):raise ValueError('case identity/order')
    grids=sorted(set(int(n) for n in args.grids.split(',')))
    if not grids or any(n not in (17,25,33) for n in grids):raise ValueError('unregistered grid')
    tasks=[(i,p,b,n,o) for i,(p,b) in enumerate(zip(points,initial)) for n in grids for o in (0,1)]
    allkeys={(t[0],t[3],t[4]) for t in tasks};keys=allkeys
    if args.keys:
        keys={tuple(map(int,k.split(':'))) for k in args.keys.split(',')}
        if not keys or not keys<=allkeys:raise ValueError('foreign selected key')
        tasks=[t for t in tasks if (t[0],t[3],t[4]) in keys]
    manifest=ENC(dict(source_sha256=pins,source_metadata=before,grids=grids,
      case_keys=[list(k) for k in sorted(keys)],backend=backend_identity()))
    runsha=SHA(manifest)
    if args.output:num.write_pair(dest,'run_inputs.json',manifest)
    else:num.check_pair(dest,'run_inputs.json',manifest)
    matrices={};cases={};pending=[]
    def matrix_object(key,data,rows):
        origin=imported_matrix(key)[2] if key in IMPORTS else None
        return dict(key=list(key),run_input_sha256=runsha,data=data,checks=rows,imported_from=origin)
    def accept_matrix(r):
        key,data,rows=r
        if key not in keys or key in matrices:raise ValueError('foreign/duplicate matrix')
        obj=matrix_object(key,data,rows);payload=ENC(obj)
        if args.replay:num.check_pair(dest,matrix_name(key),payload)
        else:num.write_pair(dest,matrix_name(key),payload)
        matrices[key]=obj;progress('matrix_sealed',key=key,passed=sum(r['passed'] for r in rows),total=len(rows))
    for t in tasks:
        key=(t[0],t[3],t[4]);p=dest/matrix_name(key)
        if args.resume and p.exists():
            obj=json.loads(num.check_pair(dest,p.name))
            if obj['key']!=list(key) or obj['run_input_sha256']!=runsha:raise ValueError('matrix resume provenance')
            matrices[key]=obj;progress('sealed_matrix_reused',key=key)
        elif not args.replay and key in IMPORTS:
            data,rows,_=imported_matrix(key);accept_matrix((key,data,rows))
        else:pending.append(t)
    workers=min(pv.nodal.v4.selected_workers(args.workers),max(1,len(pending)))
    progress('matrix_stage',selected=len(keys),pending=len(pending),workers=workers,parent_pid=os.getpid())
    if workers==1:
        for t in pending:accept_matrix(matrix_job(t))
    elif pending:
        ctx=multiprocessing.get_context('spawn');events=ctx.Queue()
        with ProcessPoolExecutor(max_workers=workers,mp_context=ctx,initializer=worker_init,initargs=(events,)) as pool:
            jobs={pool.submit(matrix_job,t):(t[0],t[3],t[4]) for t in pending};remaining=set(jobs)
            while remaining:
                done,remaining=wait(remaining,timeout=1,return_when=FIRST_COMPLETED)
                while True:
                    try:e=events.get_nowait()
                    except queue.Empty:break
                    if tuple(e['key']) not in keys:raise ValueError('foreign progress key')
                    stage=e.pop('stage');progress('worker_'+stage,**e)
                for f in done:
                    r=f.result()
                    if r[0]!=jobs[f]:raise ValueError('worker case identity')
                    accept_matrix(r)
        events.close();events.join_thread()
    gc.collect();progress('algebra_pool_released_before_spectrum')
    for key in sorted(keys):
        mat=matrices[key];msha=SHA(ENC(mat));p=dest/case_name(key)
        if args.resume and p.exists():
            obj=json.loads(num.check_pair(dest,p.name))
            if obj['key']!=list(key) or obj['run_input_sha256']!=runsha or obj['matrix_sha256']!=msha:raise ValueError('spectrum resume provenance')
            cases[key]=obj;progress('sealed_spectrum_reused',key=key);continue
        mp.mp.dps=80;local=pv.base.Checks();out={}
        try:
            data=mat['data'];S=data['canonical_quadratic_form'];point=points[key[0]]
            eta=mp.mpf(point['eta']);raw=dict(rate=eta/5,H=mp.mpf(point['H']))
            out=spectral(local,S,raw)
        except Exception:local.add('unexpected_spectrum_exception',False,traceback.format_exc())
        obj=dict(key=list(key),run_input_sha256=runsha,matrix_sha256=msha,
                 matrix_file=matrix_name(key),data=out,checks=local.rows)
        if args.replay:num.check_pair(dest,p.name,ENC(obj))
        else:num.write_pair(dest,p.name,ENC(obj))
        cases[key]=obj;progress('spectrum_sealed',key=key,passed=sum(r['passed'] for r in local.rows),total=len(local.rows))
    index=[]
    for key in sorted(keys):
        mat,case=matrices[key],cases[key]
        for label,obj in (('matrix',mat),('spectrum',case)):
            pv.nodal.reg.joint.merge_checks(ch,obj['checks'],'_'.join(map(str,key))+'_'+label+'_')
        index.append(dict(key=list(key),matrix_file=matrix_name(key),matrix_sha256=SHA(ENC(mat)),
          spectrum_file=case_name(key),spectrum_sha256=SHA(ENC(case)),dimension=case['data'].get('dimension')))
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows);complete=keys==allkeys
    matrices_complete=all(m['data'].get('full_matrix_materialized',False) for m in matrices.values())
    ok=passed==len(ch.rows) and matrices_complete
    summary=dict(validation='PASS_SELECTED_FINITE_CANONICAL_DIAGNOSTIC_ONLY' if ok else 'UNRESOLVED_FINITE_CANONICAL_SPECTRUM',
      passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
      status='FINITE_CANONICAL_SPECTRUM_'+('LOCALLY_CHECKED' if ok else 'UNRESOLVED')+'_CONTINUUM_PHYSICAL_DOMAIN_OPEN',
      selected_keys=[list(k) for k in sorted(keys)],grids=grids,full_selected_matrices_materialized=matrices_complete,
      complete_declared_grid_family_node_coverage=complete,registered_grid_coverage_complete=bool(complete and set(grids)=={17,25,33}),
      refined_grid_convergence_established=False,continuum_domain_admitted=False,physical_mode_stability_established=False,
      physical_window_established=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
      physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    formulas=dict(matrix='Frozen V2 CanonicalChart, controls and materialize; unchanged cached Hessian, constraints and E_dot',
      numerical='NumPy OpenBLAS right/transpose eigensystems; left matching plus unchanged full canonical-rescaling control',
      rates='reference proper-time lambda=p*lambda_psi; no SI matching, cutoff or evolving stability claim',
      uncertainty='conditioning heuristic only, not an eigenvalue enclosure or physical-domain bound',
      holds='all failed spectra retained; refinement, continuum nodes, nonlinear domain, healthy GR and both matching inputs remain open')
    for name,obj in (('summary.json',summary),('independent.json',index),('formulas.json',formulas)):
        if args.replay:num.check_pair(dest,name,ENC(obj))
        else:num.write_pair(dest,name,ENC(obj))
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','complete_declared_grid_family_node_coverage')}),flush=True)
    return 0 if ok else 1

def main():
    global _PROGRESS
    faulthandler.enable(all_threads=True)
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output');p.add_argument('--resume');p.add_argument('--replay');p.add_argument('--engine-smoke',action='store_true')
    p.add_argument('--grids',default='17');p.add_argument('--keys');p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log')
    a=p.parse_args()
    if a.engine_smoke:
        if any((a.output,a.resume,a.replay)):p.error('smoke cannot write scientific receipts')
        return smoke()
    if sum(bool(x) for x in (a.output,a.resume,a.replay))!=1:p.error('choose output, resume or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.resume or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    if a.resume and (dest/'summary.json').exists():raise ValueError('completed output cannot resume; use replay')
    before={f.name:num.file_metadata(f) for f in dest.iterdir()} if a.replay else None
    rc=execute(a,dest)
    if a.replay:
        after={f.name:num.file_metadata(f) for f in dest.iterdir()}
        if before!=after:raise ValueError('replay byte/metadata/set mutation')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    return rc

if __name__=='__main__':raise SystemExit(main())
