"""Full coupled planar Hessian/descriptor actions; no physical-mode admission."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,importlib.util,json,multiprocessing,traceback
from pathlib import Path
import mpmath as mp
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
PSHA='b887c7a52102b7abb43a2875cb6e01607ecb46d39a95f4abb4cefab9795a73c0'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_COUPLED_DESCRIPTOR_ACTION_V1_CONTRACT_2026-10-20.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA:raise ValueError('parent drift')
spec=importlib.util.spec_from_file_location('frozen_precision_first_variation',ROOT/PARENT)
pv=importlib.util.module_from_spec(spec);spec.loader.exec_module(pv)
PINS=dict(pv.PINS)
PINS.update({PARENT:PSHA,CONTRACT:'c990146583f55e58e605943ea36224b8c631678159a3746ee133f659f85f7cf8',
 'Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V3_REPORT_2026-10-20.md':
 '02aa52ccaca4f2d8f5dc4fb32090d5a5888a1b3151254200be7ac0ec6c6daedd',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_03/summary.json':
 '15620d36fbed613229d740bb3cb15980929f98ac8b4d4435a757dd93d6454dfe',
 'Analysis/MasterTests/outputs/r4c1_nodal_momentum_tangency_attempt_03/independent.json':
 '75f02f299e568df9d031c9a58b2ed658411f3581d982e474f091ffb0e82f887a'})
_PROGRESS=None
STEPS=('1e-18','1e-22')
dot,mm,mv,trans,mean=pv.dot,pv.mm,pv.mv,pv.trans,pv.mean

def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0].lower()!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            raw=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=f.stat().st_mtime_ns)
    return pins,meta

def ricci(q,D):
    """Full nonlinear planar three-Ricci, with all metric components retained."""
    n=len(q);dq=trans([pv.Dmul(D,c) for c in trans(q)]);his=[];Gs=[]
    for x,dx in zip(q,dq):
        h=pv.tensor(x);hi=pv.inv3(h);dh=pv.tensor(dx);his.append(hi)
        G=[[[sum(hi[k][l]*((dh[l][j] if i==2 else 0)+(dh[l][i] if j==2 else 0)
            -(dh[i][j] if l==2 else 0))/2 for l in range(3)) for j in range(3)] for i in range(3)] for k in range(3)]
        Gs.append(G)
    dG=[[[pv.Dmul(D,[g[k][i][j] for g in Gs]) for j in range(3)] for i in range(3)] for k in range(3)]
    scalars=[]
    for z in range(n):
        g=Gs[z];R=[[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                R[i][j]=dG[2][i][j][z]-(sum(dG[k][i][k][z] for k in range(3)) if j==2 else 0)
                R[i][j]+=sum(g[k][k][l]*g[l][i][j]-g[k][j][l]*g[l][i][k] for k in range(3) for l in range(3))
        scalars.append(sum(his[z][i][j]*R[i][j] for i in range(3) for j in range(3)))
    return scalars

def functional(X,raw,ys):
    """Full spatial functional; ys are stationary ONLY for gradient evaluation."""
    out=pv.restore(X,raw);q,p,dq=out['q'],out['p'],out['dq'];R3=ricci(q,raw['D'])
    E=[];F=[]
    for i in range(raw['n']):
        e,f,_,_=pv.envelope(q[i],p[i],dq[i],X['Q'][i][11],ys[i],raw['par'],R3[i]);E.append(e);F.append(f)
    invs=pv.Dmul(raw['D'],[1/x[11] for x in X['Q']])
    out.update(H=mean([e/x[11]-f*ds for e,x,f,ds in zip(E,X['Q'],F,invs)]),R3=R3,E=E,F=F)
    return out

def gradient(X,raw,ys):
    tape=pv.Tape();Y,variables=pv.variables(X,tape);out=functional(Y,raw,ys)
    return pv.unpack(tape.grad(out['H'],variables),raw['n'])

def solve_true(X,raw):
    """Fresh full complement solve, used for independent mixed-value controls."""
    out=pv.restore(X,raw);ys=[]
    for i,(q,p,dq) in enumerate(zip(out['q'],out['p'],out['dq'])):
        s=X['Q'][i][11];vol=pv.geometry(q,dq)[3];zero=[mp.mpf(0)]*12
        _,d0=pv.local_derivatives(q,dq,zero,s,raw['par']);columns=[]
        for j in range(12):
            e=zero.copy();e[j]=mp.mpf(1);_,d=pv.local_derivatives(q,dq,e,s,raw['par'])
            columns.append([d[k]-d0[k] for k in range(12)])
        R=mp.matrix(trans(columns));P=[2*a for a in p[:6]]+p[6:12]
        ys.append(list(mp.lu_solve(R,mp.matrix([a/vol-b for a,b in zip(P,d0[:12])]))))
    return ys

def response(Xpert,raw,y0,base_out):
    """True first implicit response; no frozen-y Hessian shortcut."""
    out=pv.restore(Xpert,raw);ys=[]
    for i,(q,p,dq) in enumerate(zip(out['q'],out['p'],out['dq'])):
        s=Xpert['Q'][i][11];vol=pv.geometry(q,dq)[3]
        _,d=pv.local_derivatives(q,dq,y0[i],s,raw['par'])
        P=[2*a for a in p[:6]]+p[6:12]
        bvol=pv.geometry(base_out['q'][i],base_out['dq'][i])[3]
        Rcal=mp.matrix(raw['Rs'][i])*bvol
        dy=list(mp.lu_solve(Rcal,mp.matrix([a-vol*b for a,b in zip(P,d[:12])])))
        ys.append([a+b for a,b in zip(y0[i],dy)])
    return ys

def zeros(n):
    return dict(Q=[[mp.mpf(0)]*12 for _ in range(n)],P=[[mp.mpf(0)]*10 for _ in range(n)],
                M=[mp.mpf(0)]*3,PM=[mp.mpf(0)]*3,tau=mp.mpf(0))
def combine(a,b,scale=1):return pv.unpack([x+scale*y for x,y in zip(pv.flatten(a),pv.flatten(b))],len(a['Q']))
def scale(a,s):return pv.unpack([s*x for x in pv.flatten(a)],len(a['Q']))
def norm(a):return max(abs(x) for x in pv.flatten(a))
def relative(a,b):return max(abs(x-y)/(1+abs(x)+abs(y)) for x,y in zip(pv.flatten(a),pv.flatten(b)))

def project(v,raw):
    v={k:([r.copy() for r in x] if k in ('Q','P') else x.copy() if k in ('M','PM') else x) for k,x in v.items()}
    si=raw['sine'];si2=dot(si,si)
    for k in ('Q','P'):
        for j in (7,9):
            c=mean([r[j] for r in v[k]])
            for r in v[k]:r[j]-=c
        c=dot(si,[r[4] for r in v[k]])/si2
        for i,r in enumerate(v[k]):r[4]-=si[i]*c
    v['tau']=mp.mpf(0);return v

def dense(raw,seed):
    n=raw['n'];v=zeros(n)
    for i in range(n):
        for j in range(12):v['Q'][i][j]=mp.mpf(((i+1+seed)*(j+2))%11-5)/101
        for j in range(10):v['P'][i][j]=mp.mpf(((i+2)*(j+1+seed))%13-6)/103
    v['M']=[mp.mpf((j+1)*(seed+1))/107 for j in range(3)]
    v['PM']=[-mp.mpf(j+2+seed)/109 for j in range(3)]
    return project(v,raw)

def background(X,raw,y0,out):
    g=gradient(X,raw,y0);n=raw['n'];T=zeros(n)
    # Direct derivative of <s*Zdot*g> supplies every canonical/mean cross.
    tape=pv.Tape();Y,vars=pv.variables(X,tape);oo=pv.restore(Y,raw)
    root=mean([raw['rate']*raw['Zdot'][i]*oo['g'][i] for i in range(n)])
    c=pv.unpack(tape.grad(root,vars),n)
    for i in range(n):
        T['Q'][i][:10]=[n*x for x in g['P'][i]]
        T['P'][i]=[-n*(g['Q'][i][j]+c['Q'][i][j]) for j in range(10)]
        ratio=raw['Rp'][i] if i==0 else raw['R'][i]*raw['wp'][i]/raw['q'][i][7]
        T['Q'][i][10]=raw['Zdot'][i]
        T['Q'][i][11]=(-raw['U']-(3*raw['H']-raw['HB']-raw['Rp'][i])*raw['rate']+raw['rate']*ratio)/raw['rate']
    T['M']=g['PM'].copy();T['PM']=[-a-b for a,b in zip(g['M'],c['M'])]
    return T

def omega(X,raw,v):
    """Action of dTheta, in the retained quotient chart; field rows contain 1/n."""
    n=raw['n'];q=pv.coordinates(X,raw);v=project(v,raw);out=zeros(n);par=raw['par']
    cross=[[mp.mpf(0)]*10 for _ in range(n)];mean_cross=[mp.mpf(0)]*3
    for i,(qi,vi) in enumerate(zip(q,v['Q'])):
        h=pv.tensor(qi);hi=pv.inv3(h);V=qi[6:9];vol=pv.sqrt(pv.det3(h));c=dot(V,mv(h,V));g=par['b']*vol*c
        gh=[]
        for j,k in pv.canonical.HM:
            E=[[mp.mpf(0)]*3 for _ in range(3)];E[j][k]=E[k][j]=mp.mpf(1)
            gh.append(par['b']*vol*(c*sum(hi[a][b]*E[b][a] for a in range(3) for b in range(3))/2+dot(V,mv(E,V))))
        gv=[2*par['b']*vol*x for x in mv(h,V)]
        dh=[vi[0],vi[1],v['M'][0],vi[2],v['M'][1],v['M'][2]]
        dg=dot(gh,dh)+dot(gv,vi[3:6]);s=X['Q'][i][11]
        for j,a in enumerate((0,1,3)):cross[i][j]=s*gh[a]*vi[10]
        for j in range(3):cross[i][3+j]=s*gv[j]*vi[10]
        for j,a in enumerate((2,4,5)):mean_cross[j]+=s*gh[a]*vi[10]/n
        out['Q'][i][10]=(g*vi[11]+s*dg)/n
        out['Q'][i][11]=-g*vi[10]/n
        out['P'][i]=[x/n for x in vi[:10]]
    si=raw['sine'];c=dot(si,[r[4] for r in cross])/dot(si,si)
    for i in range(n):
        cross[i][4]-=si[i]*c
        for j in range(10):out['Q'][i][j]=(-v['P'][i][j]-cross[i][j])/n
    out['M']=[-a-b for a,b in zip(v['PM'],mean_cross)];out['PM']=v['M'].copy()
    return out

def hvp(X,raw,y0,out,v,step,frozen=False):
    Y=pv.shifted(X,v,step);yy=y0 if frozen else response(Y,raw,y0,out)
    g=gradient(Y,raw,yy)
    ret=pv.unpack([mp.im(x)/step for x in pv.flatten(g)],raw['n']);ret['tau']=mp.mpf(0)
    return ret

def drift(X,raw,v,T,step):
    return pv.unpack([mp.im(x)/step for x in pv.flatten(omega(pv.shifted(X,v,step),raw,T))],raw['n'])

def curvature_controls(ch,raw):
    n=raw['n'];a=mp.mpf('1e-5');q=[r.copy() for r in raw['q']]
    for i,t in enumerate(raw['theta']):q[i][0]=mp.exp(2*a*mp.cos(t));q[i][3]=mp.exp(-2*a*mp.cos(t))
    R=ricci(q,raw['D']);analytic=[-2*(40*a*mp.sin(t))**2 for t in raw['theta']]
    ch.small('nonzero_full_Ricci_analytic_control',max(abs(x-y) for x,y in zip(R,analytic)),'1e-30')
    ch.add('Ricci_second_variation_not_deleted',max(abs(x) for x in R)>mp.mpf('1e-9'))
    qnp=np.array([[float(x) for x in r] for r in q]);Dnp=pv.lift.StableDerivative(np.array([[float(x) for x in row] for row in raw['D']]))
    oldR=pv.canonical.spatial_geometry(qnp,Dnp)[4]
    ch.small('full_Ricci_original_general_geometry',max(abs(mp.mpf(float(a))-b)/(1+abs(b)) for a,b in zip(oldR,R)),'1e-8')
    return max(abs(x-y) for x,y in zip(R,analytic))

def mixed_control(ch,X,raw,y0,v,w,hvpw):
    predicted=pv.dot_chart(v,hvpw);values=[]
    for hs in ('1e-12','1e-16'):
        h=mp.mpf(hs);total=mp.mpf(0)
        for av,aw in ((1,1),(1,-1),(-1,1),(-1,-1)):
            pert=combine(X,combine(scale(v,av),scale(w,aw)),h)
            yy=solve_true(pert,raw)
            total+=av*aw*functional(pert,raw,yy)['H']
        got=total/(4*h*h);err=abs(got-predicted)/(1+abs(got)+abs(predicted))
        ch.small('independent_full_Legendre_mixed_'+hs,err,'1e-7')
        values.append(dict(step=hs,error=mp.nstr(err,30),value=mp.nstr(got,30)))
    return values

def grid_job(task):
    case,point,initial,n,offset=task;mp.mp.dps=100;mp.iv.dps=80;ch=pv.base.Checks();record={}
    try:
        raw,X=pv.build_data(point,initial,n,offset,100);y0,err=pv.baseline(raw,X);out=functional(X,raw,y0)
        ch.small('base_temporal_stationarity',err,'1e-40');curv=curvature_controls(ch,raw)
        inherited=pv.functional(X,raw,y0);ch.small('full_curvature_matches_initial_H',abs(out['H']-inherited['H']),'1e-40')
        T=background(X,raw,y0,out);v,w=dense(raw,0),dense(raw,1)
        zs=zeros(n);ss=zeros(n);zs['Q'][0][10]=mp.mpf(1);ss['Q'][0][11]=mp.mpf(1)
        oz,os=omega(X,raw,zs),omega(X,raw,ss)
        ch.small('both_node_auxiliary_two_form_rows_null',max(norm(oz),norm(os)),'1e-40')
        ov,ow=omega(X,raw,v),omega(X,raw,w)
        ch.small('full_two_form_antisymmetry',abs(pv.dot_chart(v,ow)+pv.dot_chart(w,ov)),'1e-40')
        steps=[];previous=None
        for hs in STEPS:
            h=mp.mpf(hs)
            HV,HW,HZ,HS=[hvp(X,raw,y0,out,d,h) for d in (v,w,zs,ss)]
            DV,DW,DZ,DS=[drift(X,raw,d,T,h) for d in (v,w,zs,ss)]
            KV,KW,KZ,KS=[combine(a,b,-1) for a,b in zip((HV,HW,HZ,HS),(DV,DW,DZ,DS))]
            symmetry=abs(pv.dot_chart(v,HW)-pv.dot_chart(w,HV))/(1+abs(pv.dot_chart(v,HW))+abs(pv.dot_chart(w,HV)))
            ch.small('complete_Hessian_symmetry_'+hs,symmetry,'1e-8')
            od=pv.unpack([mp.im(x)/h for x in pv.flatten(omega(pv.shifted(X,T,h),raw,w))],n)
            balance=pv.dot_chart(v,KW)-pv.dot_chart(w,KV)+pv.dot_chart(v,od)
            ch.small('descriptor_background_two_form_balance_'+hs,abs(balance)/(1+norm(KV)+norm(KW)),'1e-8')
            A=mp.matrix([[n*KS['Q'][0][11],n*KZ['Q'][0][11]],[n*KS['Q'][0][10],n*KZ['Q'][0][10]]])
            det=mp.det(A);den=abs(A[0,0]*A[1,1])+abs(A[0,1]*A[1,0])
            rankratio=abs(det)/den if den else mp.mpf(0)
            resolved=rankratio>mp.mpf('1e-8')
            schur=None
            if resolved:
                rhs=mp.matrix([n*KV['Q'][0][11],n*KV['Q'][0][10]])
                u=mp.lu_solve(A,-rhs);correction=combine(scale(KS,u[0]),scale(KZ,u[1]));reduced=combine(KV,correction)
                defect=max(abs(n*reduced['Q'][0][j]) for j in (10,11))/(1+norm(KV)+norm(correction))
                ch.small('coupled_node_auxiliary_Schur_constraints_'+hs,defect,'1e-8')
                canonical_effect=max([abs(x) for row in correction['P'] for x in row]+[abs(x) for x in correction['PM']])
                schur=dict(coefficients=[mp.nstr(x,35) for x in u],constraint_error=mp.nstr(defect,30),
                    retained_canonical_momentum_effect=mp.nstr(canonical_effect,30),full_correction=[mp.nstr(x,25) for x in pv.flatten(correction)])
            aux=dict(block=[[mp.nstr(A[i,j],35) for j in range(2)] for i in range(2)],determinant=mp.nstr(det,35),
                normalized_determinant_margin=mp.nstr(rankratio,30),sampled_nonsingular=bool(resolved),schur=schur)
            if previous is not None:
                discrepancy=max(relative(a,b) for a,b in zip((HV,HW,HZ,HS,KV,KW,KZ,KS),previous))
                ch.small('all_sector_two_step_operator_agreement',discrepancy,'1e-8')
            previous=(HV,HW,HZ,HS,KV,KW,KZ,KS)
            steps.append(dict(step=hs,Hessian_symmetry_error=mp.nstr(symmetry,30),two_form_balance=mp.nstr(balance,30),
                drift_norm=mp.nstr(max(norm(DV),norm(DW)),30),auxiliary=aux,
                node_descriptor_columns={name:[mp.nstr(x,25) for x in pv.flatten(col)] for name,col in (('s',KS),('Z',KZ))}))
        kinetic=zeros(n)
        for r in kinetic['P']:r[6]=mp.mpf(1)
        actual=hvp(X,raw,y0,out,kinetic,mp.mpf('1e-22'));wrong=hvp(X,raw,y0,out,kinetic,mp.mpf('1e-22'),frozen=True)
        expect=1/(raw['rate']*n)
        ch.small('full_implicit_kinetic_inverse_control',max(abs(r[6]-expect)/(1+abs(expect)) for r in actual['P']),'1e-8')
        ch.add('frozen_velocity_Hessian_shortcut_rejected',norm(combine(actual,wrong,-1))>mp.mpf('1e-8'))
        ch.add('omitted_background_drift_nonzero',max(norm(DV),norm(DW))>mp.mpf('1e-30'))
        mixed=mixed_control(ch,X,raw,y0,v,w,HW) if n==17 else None
        record=dict(family=point['family'],eta=point['eta'],grid=n,node_orientation=offset,steps=steps,
            independent_mixed=mixed,full_Ricci_error=mp.nstr(curv,30),stationarity_error=mp.nstr(err,30),
            operator_action_implemented=True,full_matrix_materialized=False,physical_spectrum_computed=False,
            continuum_domain_admitted=False,state_adopted_or_evolved=False)
    except Exception:ch.add('unexpected_grid_exception',False,traceback.format_exc())
    return (case,n,offset),record,ch.rows

def calculate(workers):
    pins,before=sources();ch=pv.base.Checks()
    points=pv.lift.READ(pv.nodal.reg.JOINT+'independent.json');initial=pv.lift.READ(pv.lift.cop.CERTS)
    if len(points)!=9 or len(initial)!=9 or any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):raise ValueError('case order')
    tasks=[(i,a,b,n,o) for i,(a,b) in enumerate(zip(points,initial)) for n in (17,25,33) for o in (0,1)];out={}
    progress('coupled_descriptor_tasks',tasks=54,workers=min(workers,16))
    if workers==1:
        for t in tasks:
            r=grid_job(t);out[r[0]]=r;progress('grid_complete',key=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,16),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(grid_job,t):(t[0],t[3],t[4]) for t in tasks}
            for f in as_completed(jobs):
                r=f.result()
                if r[0]!=jobs[f] or r[0] in out:raise ValueError('grid identity')
                out[r[0]]=r;progress('grid_complete',key=r[0])
    records=[]
    for key in sorted(out):
        _,rec,rows=out[key];records.append(rec);pv.nodal.reg.joint.merge_checks(ch,rows,'_'.join(map(str,key))+'_')
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows);complete=len(records)==54 and all('steps' in r and len(r['steps'])==2 for r in records)
    resolved=complete and all(s['auxiliary']['sampled_nonsingular'] for r in records for s in r['steps'])
    su=dict(validation='PASS_COUPLED_PLANAR_DESCRIPTOR_ACTION_ONLY' if passed==len(ch.rows) and complete else 'FAIL_OR_UNRESOLVED_COUPLED_DESCRIPTOR',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='COUPLED_OPERATOR_ACTION_'+('LOCALLY_VERIFIED' if passed==len(ch.rows) and complete else 'UNRESOLVED')+'_PHYSICAL_DOMAIN_OPEN',
        all_sampled_auxiliary_blocks_nonsingular=bool(resolved),full_matrix_materialized=False,
        physical_mode_spectrum_computed=False,full_nodal_hierarchy_verified=False,continuum_domain_admitted=False,
        physical_window_established=False,state_adopted_or_evolved=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    form=dict(Hessian='Full Legendre response plus nonlinear constraint pullback and full Ricci; not frozen-y',
        descriptor='K*v=Hessian*v-dOmega[v]*Xdot; Omega*deltaXdot=K*deltaX',
        two_form='Theta=<P*dQ-g*s*dZ>+PM*dM, with metric/frame crosses and quotient sections',
        node='Finite-grid two-row auxiliary Schur block, not a continuum/physical-mode certificate',
        bounds='100 digits, fixed complex steps1e-18/1e-22; independent true mixed differences1e-12/1e-16 on n17',
        holds='Complete auxiliary/background admission, both continuum traces, function space, full modes, nonlinear and physical window/matching remain open')
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
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    meta=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:meta(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(pv.nodal.v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode()
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay set drift')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or meta(f)!=before[name]:raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','status','all_sampled_auxiliary_blocks_nonsingular')}),flush=True)
    return 0 if su['passed']==su['total'] else 1

if __name__=='__main__':raise SystemExit(main())
