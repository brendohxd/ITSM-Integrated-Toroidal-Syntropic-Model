"""Complete finite-grid canonical matrices and provisional frozen spectra."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
import hashlib,importlib.util,json,multiprocessing,os,queue,traceback
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import eig
from scipy.optimize import linear_sum_assignment
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ENGINE='Analysis/MasterTests/r4c1_cached_second_variation_v1.py'
ESHA='80e763e7200623280af240dda9d6b6af2ba612180a56fd42da3d988afabef3c3'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CANONICAL_SPECTRUM_V1_CONTRACT_2026-10-20.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/ENGINE).read_bytes())!=ESHA:raise ValueError('cached engine drift')
spec=importlib.util.spec_from_file_location('frozen_cached_second_variation',ROOT/ENGINE)
cv=importlib.util.module_from_spec(spec);spec.loader.exec_module(cv)
dc,pv=cv.dc,cv.pv
PINS=dict(dc.PINS)
PINS.update({ENGINE:ESHA,cv.PARENT:cv.PSHA,CONTRACT:'2b360e8dc0c3e9b6e7391611dab399996e83ab552a72df2b7ec6c5901ec4857a',
 'Theory/Gates/RES-001/RES001_R4C1_COUPLED_DESCRIPTOR_ACTION_V1_REPORT_2026-10-20.md':
 '999e7615c915b46d36859dbaafc5a72f984f75bb02ad2b5efdfdafec82d58419',
 'Analysis/MasterTests/outputs/r4c1_coupled_descriptor_action_attempt_01/summary.json':
 '458c7eb31b747aad761288486afc2f5da650a2f852083b51c9aaa8331fb079de',
 'Analysis/MasterTests/outputs/r4c1_coupled_descriptor_action_attempt_01/independent.json':
 '25f8495dd3f08f476962712339f19db390011994aab72529272922d03f0e46d4'})
_PROGRESS=None
_EVENTS=None

def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')
def worker_init(events):
    global _EVENTS
    _EVENTS=events
def worker_event(key,stage,**kw):
    if _EVENTS is not None:_EVENTS.put(dict(key=list(key),stage=stage,pid=os.getpid(),**kw))

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0].lower()!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    return pins,meta

def frame(X,raw):
    q=pv.coordinates(X,raw);rows=[]
    for qi in q:
        h=pv.tensor(qi);hi=pv.inv3(h);V=qi[6:9];vol=pv.sqrt(pv.det3(h));c=pv.dot(V,pv.mv(h,V));gh=[]
        for j,k in pv.canonical.HM:
            E=[[mp.mpf(0)]*3 for _ in range(3)];E[j][k]=E[k][j]=mp.mpf(1)
            gh.append(raw['par']['b']*vol*(c*sum(hi[a][b]*E[b][a] for a in range(3) for b in range(3))/2+pv.dot(V,pv.mv(E,V))))
        gv=[2*raw['par']['b']*vol*x for x in pv.mv(h,V)]
        rows.append(dict(g=raw['par']['b']*vol*c,gh=gh,gv=gv,s=X['Q'][len(rows)][11]))
    return rows

def dg(v,i,f):
    h=[v['Q'][i][0],v['Q'][i][1],v['M'][0],v['Q'][i][2],v['M'][1],v['M'][2]]
    return pv.dot(f['gh'],h)+pv.dot(f['gv'],v['Q'][i][3:6])

def householder_basis(u):
    n=len(u);r=mp.sqrt(pv.dot(u,u));u=[x/r for x in u]
    a=[u[i]-(1 if i==0 else 0) for i in range(n)];z=pv.dot(a,a)
    if z==0:return [[mp.mpf(int(i==j)) for j in range(1,n)] for i in range(n)]
    return [[mp.mpf(int(i==j))-2*a[i]*a[j]/z for j in range(1,n)] for i in range(n)]

class CanonicalChart:
    def __init__(self,raw,X,T,cache):
        self.raw=raw;self.X=X;self.T=T;self.cache=cache;self.n=raw['n'];self.r=mp.sqrt(self.n)
        self.bases=[];self.labels=[]
        for j in range(10):
            if j in (7,9):B=householder_basis([mp.mpf(1)]*self.n)
            elif j==4:B=householder_basis(raw['sine'])
            else:B=[[mp.mpf(int(i==k)) for k in range(self.n)] for i in range(self.n)]
            self.bases.append(B)
            self.labels.extend(('field',j,k) for k in range(len(B[0])))
        self.labels.extend(('mean',j,0) for j in range(3))
        self.labels.extend(('regulator',i,0) for i in range(1,self.n))
        self.d=len(self.labels);self.D=2*self.d
        if self.d!=11*self.n-1:raise ValueError('canonical dimension mismatch')
        self.f=frame(X,raw);self.h=mp.mpf('1e-22')
        self.ft=frame(pv.shifted(X,T,self.h),raw)
        es=dc.zeros(self.n);ez=dc.zeros(self.n);es['Q'][0][11]=mp.mpf(1);ez['Q'][0][10]=mp.mpf(1)
        self.Hs=cache.action(es);self.Hz=cache.action(ez)
        self.A=mp.matrix([[self.n*self.Hs['Q'][0][11],self.n*self.Hz['Q'][0][11]],
                          [self.n*self.Hs['Q'][0][10],self.n*self.Hz['Q'][0][10]]])
        self.Ainv=self.A**-1;self.amap=[]
        for j in range(self.D):
            v=self.seed(j,self.f);rhs=mp.matrix(self.constraint(v));a=list(self.Ainv*(-rhs));self.amap.append(a)
    def seed(self,j,f):
        v=dc.zeros(self.n);is_p=j>=self.d;kind,a,k=self.labels[j%self.d]
        pz=[mp.mpf(0)]*self.n
        if kind=='field':
            key='P' if is_p else 'Q'
            for i in range(self.n):v[key][i][a]=self.r*self.bases[a][i][k]
        elif kind=='mean':v['PM' if is_p else 'M'][a]=mp.mpf(1)
        elif is_p:pz[a]=self.r
        else:v['Q'][a][10]=self.r
        for i in range(1,self.n):
            if f[i]['g']==0:raise ValueError('unexpected regular grid zero')
            v['Q'][i][11]=-(pz[i]+f[i]['s']*dg(v,i,f[i]))/f[i]['g']
        return v
    def constraint(self,v):
        # The exact-node drift row is retained even when its background rate is tiny.
        h=pv.tensor(pv.coordinates(self.X,self.raw)[0]);tv=self.T['Q'][0][3:6]
        zv=v['Q'][0][3:6]
        Drow=2*self.raw['par']['b']*self.raw['rate']*pv.dot(zv,pv.mv(h,tv))
        return [self.n*pv.dot_chart(self.Hs,v),self.n*pv.dot_chart(self.Hz,v)-Drow]
    def column(self,j):
        v=self.seed(j,self.f);a=self.amap[j]
        v['Q'][0][11]=a[0];v['Q'][0][10]=a[1]
        return v
    def column_dot_regular(self,j):
        v=self.seed(j,self.ft)
        return cv.unstate([mp.im(x)/self.h for x in cv.state(v)],self.n)
    def transpose(self,b):
        q=[r[:10] for r in b['Q']];m=b['M'].copy();pz=[mp.mpf(0)]*self.n
        for i in range(1,self.n):
            f=self.f[i];weight=-b['Q'][i][11]*f['s']/f['g'];pz[i]=-b['Q'][i][11]/f['g']
            for j,a in enumerate((0,1,3)):q[i][j]+=weight*f['gh'][a]
            for j in range(3):q[i][3+j]+=weight*f['gv'][j]
            for j,a in enumerate((2,4,5)):m[j]+=weight*f['gh'][a]
        ret=[]
        for is_p in (False,True):
            for kind,a,k in self.labels:
                if kind=='field':
                    x=[r[a] for r in (b['P'] if is_p else q)]
                    ret.append(self.r*sum(self.bases[a][i][k]*x[i] for i in range(self.n)))
                elif kind=='mean':ret.append(b['PM'][a] if is_p else m[a])
                else:ret.append(self.r*(pz[a] if is_p else b['Q'][a][10]))
        for j,a in enumerate(self.amap):ret[j]+=a[0]*b['Q'][0][11]+a[1]*b['Q'][0][10]
        return ret

def controls(ch,raw,X,y0,out,T,cache,chart):
    ch.small('cached_augmented_temporal_stationarity',cache.stationarity,'1e-40')
    oldg=dc.gradient(X,raw,y0)
    ch.small('cached_first_gradient_all_sectors',max(abs(a-b)/(1+abs(a)+abs(b)) for a,b in zip(cache.first,cv.state(oldg))),'1e-8')
    for seed in (0,1):
        v=dc.dense(raw,seed);actual=cache.action(v)
        for hs in ('1e-18','1e-22'):
            ref=dc.hvp(X,raw,y0,out,v,mp.mpf(hs))
            ch.small('cached_true_Hessian_dense_'+str(seed)+'_'+hs,dc.relative(actual,ref),'1e-8')
        ch.small('cached_linearized_temporal_stationarity_'+str(seed),cache.last_stationarity,'1e-40')
        dv=dc.drift(X,raw,v,T,mp.mpf('1e-22'));kv=dc.combine(actual,dv,-1);expected=[raw['n']*kv['Q'][0][j] for j in (11,10)]
        ch.small('node_constraint_row_reciprocity_'+str(seed),max(abs(a-b)/(1+abs(a)+abs(b)) for a,b in zip(chart.constraint(v),expected)),'1e-8')
    ch.add('complete_canonical_finite_dimension',chart.D==2*(11*raw['n']-1),str(chart.D))

def materialize(ch,key,raw,X,y0,out,T,cache,chart):
    columns=[];canonical_error=mp.mpf(0);constraint_error=mp.mpf(0);stationarity=mp.mpf(0)
    for j in range(chart.D):
        v=chart.column(j);h=cache.action(v);stationarity=max(stationarity,cache.last_stationarity)
        d=dc.drift(X,raw,v,T,mp.mpf('1e-22'));edot=chart.column_dot_regular(j)
        cov=dc.combine(dc.combine(h,d,-1),dc.omega(X,raw,edot),-1)
        columns.append(chart.transpose(cov))
        om=chart.transpose(dc.omega(X,raw,v));expected=[mp.mpf(0)]*chart.D
        if j<chart.d:expected[chart.d+j]=mp.mpf(1)
        else:expected[j-chart.d]=mp.mpf(-1)
        canonical_error=max(canonical_error,max(abs(a-b) for a,b in zip(om,expected)))
        c=chart.constraint(v);constraint_error=max(constraint_error,max(abs(a) for a in c)/(1+dc.norm(v)))
        if j%16==15 or j+1==chart.D:worker_event(key,'matrix_columns',done=j+1,total=chart.D)
    S=pv.trans(columns)
    symmetry=max(abs(S[i][j]-S[j][i])/(1+abs(S[i][j])+abs(S[j][i])) for i in range(chart.D) for j in range(chart.D))
    ch.small('full_canonical_pullback',canonical_error,'1e-8')
    ch.small('full_constraint_embedding',constraint_error,'1e-8')
    ch.small('full_reduced_generator_symmetry_without_symmetrization',symmetry,'1e-8')
    ch.small('full_implicit_velocity_stationarity',stationarity,'1e-40')
    return S,dict(canonical_error=mp.nstr(canonical_error,35),constraint_error=mp.nstr(constraint_error,35),
        symmetry_error=mp.nstr(symmetry,35),stationarity_error=mp.nstr(stationarity,35))

def spectral(ch,S,raw):
    M=np.array([[float(x) for x in row] for row in S]);D=len(M);d=D//2
    if not np.all(np.isfinite(M)):raise ValueError('nonfinite materialized generator')
    diag=np.abs(np.diag(M));floor=max(float(np.max(diag))*1e-30,np.finfo(float).tiny)
    q=np.maximum(diag[:d],floor);p=np.maximum(diag[d:],floor)
    scaling=(p/q)**.25;sc=np.r_[scaling,1/scaling]
    B=sc[:,None]*M*sc[None,:]  # Constant symplectic congruence; no sign removed.
    A=np.r_[B[d:,:],-B[:d,:]]
    with threadpool_limits(limits=1,user_api='blas'):
        lam,left,right=eig(A,left=True,right=True,check_finite=True)
        extra=np.array([2.0**((i%3)-1) for i in range(d)]);extra=np.r_[extra,1/extra]
        other=eig(A*extra[None,:]/extra[:,None],left=False,right=False,check_finite=True)
    cost=np.abs(lam[:,None]-other[None,:])/(1+np.abs(lam[:,None])+np.abs(other[None,:]))
    ia,ib=linear_sum_assignment(cost);match=float(np.max(cost[ia,ib]))
    ch.small('complete_spectrum_constant_canonical_rescaling',mp.mpf(match),'1e-6')
    Anorm=float(np.linalg.norm(A,ord='fro'));eps=np.finfo(float).eps
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
        reliable=np.isfinite(uncertainty) and back<=1e-8 and match<=1e-6
        if not reliable or abs(z)<=10*uncertainty:status='UNRESOLVED_NEAR_ZERO_OR_ILL_CONDITIONED'
        elif abs(z.real)>10*uncertainty:status='FROZEN_NONOSCILLATORY_DIAGNOSTIC_NOT_PHYSICAL_INSTABILITY'
        else:status='OSCILLATORY_WITHIN_NUMERICAL_RESOLUTION'
        energy_status='NOT_ASSIGNED'
        sign=None;normalization=None
        if status=='OSCILLATORY_WITHIN_NUMERICAL_RESOLUTION' and z.imag>0:
            if energy_error>1e-8:energy_status='UNRESOLVED_MODE_ENERGY_IDENTITY'
            elif near:energy_status='DEGENERATE_SUBSPACE_NORMALIZATION_OUTSTANDING'
            elif abs(N)<=1e-10*rn*rn:energy_status='UNRESOLVED_SMALL_ACTION_NORM'
            else:sign=1 if N>0 else -1;normalization=float(1/np.sqrt(abs(N)));energy_status='CANONICAL_ACTION_NORM_RESOLVED_FROZEN_MODE_ONLY'
        safe=lambda x:float(x) if np.isfinite(x) else None
        rows.append(dict(index=i,lambda_psi=[float(z.real),float(z.imag)],
            lambda_reference_proper_time=[float(z.real)*float(raw['rate']),float(z.imag)*float(raw['rate'])],
            lambda_over_H=[float(z.real)*float(raw['rate']/raw['H']),float(z.imag)*float(raw['rate']/raw['H'])],
            backward_error=back,left_right_condition=safe(cond),uncertainty_estimate_not_a_bound=safe(uncertainty),
            action_norm=N,status=status,energy_status=energy_status,Krein_sign=sign,
            canonical_energy=[float(E.real),float(E.imag)],energy_identity_error=energy_error,
            unit_action_amplitude_factor=normalization,nearby_mode_indices=near))
    rows.sort(key=lambda r:(r['lambda_psi'][0],r['lambda_psi'][1],r['index']))
    ch.small('all_eigenpair_backward_errors',mp.mpf(max_backward),'1e-8')
    return dict(modes=rows,mode_count=len(rows),dimension=D,canonical_balancing_factors=[float(x) for x in scaling],
        rescaling_spectral_error=match,max_backward_error=max_backward,
        energy_norm_scope='Canonical symplectic norm for resolvable nondegenerate frozen modes; not SI matching or an evolving energy theorem',
        physical_stability_established=False,physical_window_established=False)

def case_job(task):
    case,point,initial,n,offset=task;key=(case,n,offset);mp.mp.dps=80;mp.iv.dps=80;ch=pv.base.Checks();result={}
    try:
        worker_event(key,'case_start')
        raw,X=pv.build_data(point,initial,n,offset,80);y0,err=pv.baseline(raw,X);out=dc.functional(X,raw,y0)
        cache=cv.CachedHessian(raw,X,y0);T=dc.background(X,raw,y0,out);chart=CanonicalChart(raw,X,T,cache)
        worker_event(key,'cache_ready',dimension=chart.D,nodes=len(cache.t.nodes))
        controls(ch,raw,X,y0,out,T,cache,chart)
        S,metrics=materialize(ch,key,raw,X,y0,out,T,cache,chart)
        spectrum=spectral(ch,S,raw)
        result=dict(family=point['family'],eta=point['eta'],grid=n,node_orientation=offset,
            labels=[list(a) for a in chart.labels],metrics=metrics,spectrum=spectrum,
            canonical_quadratic_form=[[mp.nstr(x,80) for x in row] for row in S],
            auxiliary_block=[[mp.nstr(chart.A[i,j],80) for j in range(2)] for i in range(2)],
            full_matrix_materialized=True,refined_grid_convergence_established=False,
            continuum_domain_admitted=False,state_adopted_or_evolved=False)
    except Exception:ch.add('unexpected_case_exception',False,traceback.format_exc())
    return key,result,ch.rows

def smoke():
    _,before=sources();ch=pv.base.Checks();cv.engine_controls(ch)
    raw={'rate':mp.mpf(1)/3,'H':mp.mpf(1)/5}
    for sign in (1,-1):
        out=spectral(ch,[[mp.mpf(sign),mp.mpf(0)],[mp.mpf(0),mp.mpf(sign)]],raw)
        pos=[r for r in out['modes'] if r['lambda_psi'][1]>0]
        ch.add('oscillator_energy_sign_'+str(sign),len(pos)==1 and pos[0]['Krein_sign']==sign)
    _,after=sources();ch.add('smoke_source_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    print(json.dumps(dict(scope='EXECUTION_ONLY_NO_COSMOLOGICAL_RECEIPT',passed=passed,total=len(ch.rows),
        failed=[r for r in ch.rows if not r['passed']]),sort_keys=True),flush=True)
    return 0 if passed==len(ch.rows) else 1

def file_metadata(p):return (SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
def check_pair(dest,name,raw=None):
    p=dest/name;sc=dest/(name+'.sha256')
    if not p.resolve().is_relative_to(dest) or not sc.resolve().is_relative_to(dest):raise ValueError('escaped case path')
    data=p.read_bytes()
    if sc.read_text().split()[0]!=SHA(data):raise ValueError('case sidecar drift '+name)
    if raw is not None and data!=raw:raise ValueError('read-only replay mismatch '+name)
    return data
def write_pair(dest,name,raw):
    for n,b in ((name,raw),(name+'.sha256',(SHA(raw)+'  '+name+'\n').encode())):
        p=dest/n
        if not p.resolve().is_relative_to(dest):raise ValueError('escaped output path')
        with p.open('xb') as f:f.write(b)

def execute(args,dest):
    pins,before=sources();ch=pv.base.Checks();cv.engine_controls(ch)
    points=pv.lift.READ(pv.nodal.reg.JOINT+'independent.json');initial=pv.lift.READ(pv.lift.cop.CERTS)
    if len(points)!=9 or len(initial)!=9 or any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):raise ValueError('case identity/order')
    grids=sorted(set(int(n) for n in args.grids.split(',')))
    if not grids or any(n not in (17,25,33) for n in grids):raise ValueError('unregistered grid')
    tasks=[(i,p,b,n,o) for i,(p,b) in enumerate(zip(points,initial)) for n in grids for o in (0,1)]
    keys={(t[0],t[3],t[4]) for t in tasks}
    manifest=ENC(dict(source_sha256=pins,source_metadata=before,grids=grids,
        case_keys=[list(k) for k in sorted(keys)],numpy=np.__version__,scipy=scipy.__version__))
    manifest_sha=SHA(manifest)
    if args.output:write_pair(dest,'run_inputs.json',manifest)
    else:check_pair(dest,'run_inputs.json',manifest)
    record={};pending=[]
    case_name=lambda k:'case_%02d_n%d_o%d.json'%k
    for task in tasks:
        key=(task[0],task[3],task[4]);name=case_name(key)
        if args.resume and (dest/name).exists():
            data=json.loads(check_pair(dest,name))
            if data['key']!=list(key) or data['run_input_sha256']!=manifest_sha:raise ValueError('resume case provenance mismatch')
            record[key]=data;progress('sealed_case_reused',key=key)
        else:pending.append(task)
    def accept(r):
        key,data,rows=r
        if key not in keys or key in record:raise ValueError('duplicate/foreign case')
        obj=dict(key=list(key),run_input_sha256=manifest_sha,data=data,checks=rows);b=ENC(obj);name=case_name(key)
        if args.replay:check_pair(dest,name,b)
        else:write_pair(dest,name,b)
        record[key]=obj;progress('case_sealed',key=key,passed=sum(x['passed'] for x in rows),total=len(rows))
    workers=min(pv.nodal.v4.selected_workers(args.workers),max(1,len(pending)))
    progress('canonical_matrix_cases',cases=len(tasks),pending=len(pending),grids=grids,workers=workers,parent_pid=os.getpid())
    if workers==1:
        for task in pending:accept(case_job(task))
    elif pending:
        ctx=multiprocessing.get_context('spawn');events=ctx.Queue()
        with ProcessPoolExecutor(max_workers=workers,mp_context=ctx,initializer=worker_init,initargs=(events,)) as pool:
            jobs={pool.submit(case_job,t):(t[0],t[3],t[4]) for t in pending};remaining=set(jobs)
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
                    accept(r)
        events.close();events.join_thread()
    index=[]
    for key in sorted(record):
        obj=record[key];pv.nodal.reg.joint.merge_checks(ch,obj['checks'],'_'.join(map(str,key))+'_')
        data=obj['data'];index.append(dict(key=list(key),filename=case_name(key),
            payload_sha256=SHA(ENC(obj)),dimension=data.get('spectrum',{}).get('dimension'),
            physical_window_established=False))
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows);complete=len(record)==len(tasks) and all('spectrum' in r['data'] for r in record.values())
    summary=dict(validation='PASS_FINITE_CANONICAL_MATRIX_DIAGNOSTIC_ONLY' if passed==len(ch.rows) and complete else 'FAIL_OR_UNRESOLVED_FINITE_CANONICAL_SPECTRUM',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,grids=grids,
        status='FINITE_CANONICAL_SPECTRUM_'+('LOCALLY_CHECKED' if passed==len(ch.rows) and complete else 'UNRESOLVED')+'_CONTINUUM_PHYSICAL_DOMAIN_OPEN',
        full_matrices_materialized=bool(complete),registered_grid_coverage_complete=bool(set(grids)=={17,25,33}),
        refined_grid_convergence_established=False,continuum_domain_admitted=False,physical_mode_stability_established=False,
        physical_window_established=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    form=dict(cached_Hessian='FXX*v+FXy*(n*s)*(volume*R)^(-1)*FyX*v; original C2 cusp retained',
        canonical='Quotient sections and exact-node auxiliary block, PZ=-g*s only inverted on regular points',
        generator='S=E^T*(K*E-Omega*E_dot), K=Hessian-dOmega[.]*Xdot; no frozen embedding',
        rates='reference proper-time lambda=p*lambda_psi; no SI matching, cutoff or evolving stability claim',
        normalization='Unit symplectic action only for resolvable nondegenerate oscillatory modes; all other modes retained',
        holds='n25/n33 refinement where absent; both continuum nodes, admissibility, nonlinear/physical window and matching remain open')
    for name,obj in (('summary.json',summary),('formulas.json',form),('independent.json',index)):
        if args.replay:check_pair(dest,name,ENC(obj))
        else:write_pair(dest,name,ENC(obj))
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','grids')}),flush=True)
    return 0 if passed==len(ch.rows) and complete else 1

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output');p.add_argument('--resume');p.add_argument('--replay');p.add_argument('--engine-smoke',action='store_true')
    p.add_argument('--grids',default='17');p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
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
    before={f.name:file_metadata(f) for f in dest.iterdir()} if a.replay else None
    rc=execute(a,dest)
    if a.replay:
        after={f.name:file_metadata(f) for f in dest.iterdir()}
        if before!=after:raise ValueError('replay byte/metadata/set mutation')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    return rc

if __name__=='__main__':raise SystemExit(main())
