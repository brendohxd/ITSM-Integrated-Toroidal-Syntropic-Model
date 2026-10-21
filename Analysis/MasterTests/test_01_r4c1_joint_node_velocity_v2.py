"""Joint necessary mean/node/time completion, without adopting or evolving a state."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py'
PARENT_SHA='c6a7e31c2f63d8e6481d2e5a4b4f2725ce376f3de05ab639594a7b9e991f1ae7'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V2_MATRIX_ADDENDUM_2026-10-19.md'
ACCEL='Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda name:json.loads((ROOT/name).read_bytes())
if SHA((ROOT/PARENT).read_bytes())!=PARENT_SHA:raise ValueError('frozen parent drift')
spec=importlib.util.spec_from_file_location('frozen_actual_node',ROOT/PARENT)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
cop=parent.cop;base=cop.base;iv=mp.iv
PINS=dict(parent.PINS)
PINS.update({
 PARENT:PARENT_SHA,
 CONTRACT:'4c24eb869130aa8b13fbecaeb2c9799b525a10823708ffc3e78e58b743ccef97',
 'Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V1_CONTRACT_2026-10-19.md':'1733f68993e70a4d73c365acdfaadf6d5df1c71f3541148987ea4c0fa6da7009',
 'Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v1.py':'dd3a132ac557d5d631b9e7b7bfdfdf17edc9dd1e9b073b06418309ae43a8e631',
 ACCEL+'equations.json':'4aa8b6ff0abea3840a4aaededd6a4a713a89a9c29477d23f1585ee8042723857',
 ACCEL+'summary.json':'9f8d5fce14a4fadf3052eafdf4ec5d0e4adbe3937be991d344ff126fa49f6019',
 ACCEL+'cases.json':'bcaa4b484426ca37eb6d63900e977071bf0ecd3f8fc1f29e48e7ae42c2a8d125',
 'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V4_REPORT_2026-10-19.md':'d5e15cc6545b76038213fa4e1560725b437455ccea6b381be52be762f5393da7',
 'Analysis/MasterTests/test_01_r4c1_coupled_node_dimensional_audit_v2.py':'75b74f737e4b4910058c8ab50c3ef6d96c3d5a318a5fcca784bbfb9edfcd78de',
 'Analysis/MasterTests/outputs/r4c1_coupled_node_dimensional_audit_attempt_02/audit.json':'273f50caceb1f8181c42f012b5e4b16a68f45b5f037f6a14915c78471365b64d',
})
_PROGRESS=None
def progress(stage,**values):
    raw=json.dumps(dict(stage=stage,**values),sort_keys=True)
    print(raw,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as stream:stream.write(raw+'\n')
def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,digest in pins.items():
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest or side.read_text().split()[0].lower()!=digest:
            raise ValueError('pinned source/sidecar drift '+name)
        for q in (p,side):
            raw=q.read_bytes();meta[q.relative_to(ROOT).as_posix()]=dict(
                sha256=SHA(raw),bytes=len(raw),mtime_ns=q.stat().st_mtime_ns)
    return pins,meta
def merge_checks(ch,rows,prefix=''):
    for r in rows:ch.add(prefix+r['name'],r['passed'],r.get('value'),r.get('criterion','exact'))

def build(ch):
    u,fn,form=cop.symbolic(ch)
    for name in ('U','Ud','r1','rt','pressure','mass_source','rho0','F'):
        u.setdefault(name,s.Symbol(name,real=True))
    u['U']=u['zc']
    parse=lambda text:s.sympify(text,locals=u)
    eq=READ(ACCEL+'equations.json')
    H,HB,U,Ud,al,q,K,b,p,be,k=[u[n] for n in ('H','H0','zc','Ud','alpha','qs','K_Q','b','p','beta','k')]
    r1,rt=u['r1'],u['rt'];actual_raw=parse(eq['actual_frame_slope'])
    a=-U-(3*H-HB-2*r1)*p
    brho=(K+2*b*k*k*al)*U-K*HB*p-K*p*r1
    rest=(2*H-3*HB-r1)*a+p*(actual_raw+HB*HB-8*H*HB+6*H*H-rt-4*r1*(H-HB))\
         -(4*b*H*U*k*k*al+(-3*H+r1+be*p)*brho)/K
    Bv=1+2*b*k*k*al/K
    ch.zero('original_exported_undivided_time_condition',parse(eq['transport_defect'])-(Bv*Ud+rest))
    pressure=(K*p*p+u['D']**2+u['rd']**2)/2-u['pot']
    mass=K*p*p-u['zeta']*u['Rc']**2*u['D']**2
    rule={r1:al*q,rt:s.Integer(0),u['pressure']:pressure,u['mass_source']:mass}
    actual=parent.exact_atoms(actual_raw,rule)
    rr=parent.exact_atoms(rest,rule);vel=-rr/Bv
    vh=s.diff(vel,H)+s.diff(vel,q)*u['qh']
    vu=s.diff(vel,U)+s.diff(vel,q)*u['qu']
    ch.zero('exact_velocity_elimination',Bv*vel+rr)
    ch.add('actual_frame_slope_independent_regulator_velocity',not actual.has(Ud,u['zdc']))
    ch.add('inverse_and_all_sensitivities_independent_velocity',
           all(not e.has(u['zdc']) for e in fn['poly'].expressions+fn['residual'].expressions))
    delta=fn['energy'].expressions[0]
    dedv=s.diff(delta,u['zdc']);dj=s.diff(fn['node_flux'].expressions[0],u['zdc'])
    dd=s.symbols('hdd0:3',real=True);u.update({str(v):v for v in dd})
    metric=[parse(t) for t in eq['metric_Euler']]
    matrix=s.Matrix(3,3,lambda i,j:s.diff(metric[i],dd[j]))
    forces=[e.xreplace(dict.fromkeys(dd,s.Integer(0))) for e in metric]
    frame=parse(eq['frame_Euler_normal_jet'])
    slope=parse(eq['actual_frame_slope'])
    frame0=frame.xreplace({u['F']:s.Integer(0)})
    fc=s.diff(frame,u['F'])
    ch.zero('original_frame_acceleration_coefficient',fc+u['MU2']*(u['c1']+u['c4']))
    pack=dict(velocity=[vel,vh,vu,actual],energy_velocity=[dedv,dj],
              normalized=[parse(eq['normalized_transport_defect'])],
              metric_matrix=list(matrix),metric_forces=forces,frame=[frame0,fc],
              jets=[parse(eq[n]) for n in ('transverse_shift_first_jet','transverse_shift_third_jet','longitudinal_shift_third_jet')])
    formulas=dict(mean='F=Ebase+alpha*<Edelta(H,U,Ud_req)>+rho0',
        node='B=K_Q*(U-U0)+alpha*Dnode(H,U,Ud_req)',
        time='Bv*Ud+R=0; Ud_req=-R/Bv',
        chain_rule='total_i(Edelta)=partial_i(Edelta)|Ud+partial_Ud(Edelta)*partial_i(Ud_req), i=H,U; retain corresponding flux derivatives',
        uniqueness='Strict opposing F and B faces, F_H<0 and B_U-B_H*F_U/F_H>0 on the entire fixed rectangle',
        normalized_correction='At the new root use h2=(mean_delta+phase_scaled)/(3*M*(H+H0)),u2=-Dnode/K_Q,r2=qnode; (Ud-Ud0)/alpha=-C_new/Bv',
        authority='Necessary joint completion only, no initial state adoption/evolution or physical window')
    return pack,formulas

_FN=None;_EX=None
def initialize(pack):
    global _FN,_EX
    mp.mp.dps=110;iv.dps=80
    dummy=base.Checks();_,_FN,_=cop.symbolic(dummy)
    if not all(r['passed'] for r in dummy.rows):raise ValueError('frozen utility controls failed')
    _EX={n:base.Eval(expr) for n,expr in pack.items()}
def enclosed(c,H,U,n):
    v0=c['values'];alpha=v0['alpha']
    node=cop.state(c,H,U,iv.mpf(0),iv.mpf(1),_FN)
    vel,vh,vu,actual=_EX['velocity'].interval(node)
    Bv=1+2*v0['b']*v0['k']**2*alpha/v0['K_Q']
    phase=node['D']
    ebase=-3*v0['M']*H**2+(v0['K_Q']*v0['p']**2+phase**2+v0['rd']**2)/2+v0['pot']
    mean=[iv.mpf(0) for _ in range(3)];floor=None
    for j in range(n):
        angle=iv.mpf([base.lo(iv.pi*j/(2*n)),base.hi(iv.pi*(j+1)/(2*n))])
        vv=cop.state(c,H,U,iv.cos(angle),iv.sin(angle),_FN);vv['zdc']=vel
        ed,eh,eu,flux=_FN['energy'].interval(vv)
        dedv,_=_EX['energy_velocity'].interval(vv)
        vals=(ed,eh+dedv*vh,eu+dedv*vu)
        for i,value in enumerate(vals):mean[i]+=value/n
        low=base.lo(-ebase-alpha*(ed+flux));floor=low if floor is None else min(floor,low)
    node['zdc']=vel
    ned,neh,neu,_=_FN['energy'].interval(node)
    dedv,dj=_EX['energy_velocity'].interval(node)
    neh+=dedv*vh;neu+=dedv*vu
    jf=_FN['node_flux'].interval(node)[0]
    Dnode=2*v0['b']*U*v0['k']**2-v0['K_Q']*v0['p']*node['qs']-v0['beta']*(mean[0]-ned-jf)
    Dh=-v0['K_Q']*v0['p']*node['qh']-v0['beta']*(mean[1]-neh-dj*vh)
    Du=2*v0['b']*v0['k']**2-v0['K_Q']*v0['p']*node['qu']-v0['beta']*(mean[2]-neu-dj*vu)
    pt=v0['zeta']*v0['Rc']**2/2
    phase_scaled=v0['Rc']**2*(2*pt-pt**2*alpha)/(2*(1-pt*alpha)**2)
    h2=(mean[0]+phase_scaled)/(3*v0['M']*(H+v0['H0']))
    u2=-Dnode/v0['K_Q']
    corrvals=dict(v0,h2=h2,u2=u2,r2=node['qs'],rho0=v0['rho'])
    Cnew=_EX['normalized'].interval(corrvals)[0]
    return dict(F=ebase+alpha*mean[0]+v0['rho'],B=v0['K_Q']*(U-c['U0'])+alpha*Dnode,
        FH=-6*v0['M']*H+alpha*mean[1],FU=alpha*mean[2],BH=alpha*Dh,BU=v0['K_Q']+alpha*Du,
        density=base.point(floor),Bv=Bv,velocity=vel,velocity_H=vh,velocity_U=vu,
        h2=h2,u2=u2,r2=node['qs'],Cnew=Cnew,velocity_correction_over_e_squared=-Cnew/Bv,
        actual_frame_slope=actual)

def certify(c,ch):
    attempts=[];success=False
    for n in (16,32,64,128,256):
        core=enclosed(c,c['Hall'],c['Uall'],n)
        faces=[enclosed(c,H,U,n) for H,U in
               ((c['Hlo'],c['Uall']),(c['Hhi'],c['Uall']),(c['Hall'],c['Ulo']),(c['Hall'],c['Uhi']))]
        signs=dict(mean_lower_face=base.lo(faces[0]['F'])>0,mean_upper_face=base.hi(faces[1]['F'])<0,
            node_lower_face=base.hi(faces[2]['B'])<0,node_upper_face=base.lo(faces[3]['B'])>0,
            mean_H_derivative=base.hi(core['FH'])<0,positive_density=base.lo(core['density'])>0,
            positive_velocity_coefficient=base.lo(core['Bv'])>0)
        schur=core['BU']-core['BH']*core['FU']/core['FH'] if signs['mean_H_derivative'] else iv.mpf([-mp.inf,mp.inf])
        signs['unique_joint_root_derivative']=base.lo(schur)>0
        signs['finite_bounds']=all(mp.isfinite(t) for value in core.values() for t in (base.lo(value),base.hi(value)))
        attempts.append(dict(boxes=n,criteria=signs,core={k:base.pack(v) for k,v in core.items()},
            mean_lower_face=base.pack(faces[0]['F']),mean_upper_face=base.pack(faces[1]['F']),
            node_lower_face=base.pack(faces[2]['B']),node_upper_face=base.pack(faces[3]['B']),schur=base.pack(schur)))
        if all(signs.values()):success=True;break
    for name,value in signs.items():ch.add(name,value,criterion='strict enclosure on full frozen H/U/amplitude domain')
    return dict(status='CERTIFIED_RESTRICTED_JOINT_MEAN_NODE_VELOCITY_ROOT' if success else 'UNRESOLVED_BY_FIXED_BOUNDS',
        family=c['family'],eta=c['eta'],attempts=attempts,H_bracket=base.pack(c['Hall']),U_bracket=base.pack(c['Uall']),
        full_initial_admission=False,state_adopted_or_evolved=False)

def point_setup(c,H,U,Ud):
    v={k:base.midpoint(value) for k,value in c['values'].items()}
    v.update(H=H,zc=U,zdc=Ud,alpha=mp.mpf(1)/250000,eeabs=mp.mpf(1)/500)
    v['D']=v['Rc']/(1-v['zeta']*v['Rc']**2*v['alpha']/2)
    def at(C,S):
        vv=dict(v,CC=C,SS=S,xi=C*C);poly=_FN['poly'].numeric(vv)
        for j,(rn,qn) in enumerate((('rs','qs'),('rh','qh'),('ru','qu'))):
            vv[rn]=C*S*poly[2*j];vv[qn]=v['k']*poly[2*j+1]
        return vv
    return v,at
def point_system(c,H,U,Ud):
    v,at=point_setup(c,H,U,Ud);mean=mp.mpf(0)
    for j in range(64):
        theta=2*mp.pi*j/64
        mean+=_FN['analytic'].numeric(at(mp.cos(theta),mp.sin(theta)))[0]/64
    mean-=8*v['A']*v['p']**3*v['eeabs']/(3*mp.pi)
    node=at(mp.mpf(0),mp.mpf(1));en=_FN['energy'].numeric(node)[0];flux=_FN['node_flux'].numeric(node)[0]
    ebase=-3*v['M']*H**2+(v['K_Q']*v['p']**2+v['D']**2+v['rd']**2)/2+v['pot']
    rho_node=-ebase-v['alpha']*(en+flux)
    r1=v['alpha']*node['qs'];s2=v['k']**2*v['alpha']
    apsi=-(3*H-r1)*v['p']+2*v['b']*U*s2/v['K_Q']-v['beta']*rho_node/v['K_Q']
    actual=_EX['velocity'].numeric(node)[3]
    f=ebase+v['alpha']*mean+v['rho']
    g=(v['K_Q']+2*v['b']*s2)*U-v['K_Q']*v['H0']*v['p']-v['K_Q']*v['p']*r1-v['beta']*rho_node
    t=(1+2*v['b']*s2/v['K_Q'])*Ud+(2*H-3*v['H0']-r1)*apsi\
      +v['p']*(actual+v['H0']**2-8*H*v['H0']+6*H**2-4*r1*(H-v['H0']))\
      -(4*v['b']*H*U*s2+v['beta']*(-3*H+r1+v['beta']*v['p'])*rho_node)/v['K_Q']
    return mp.matrix([f,g,t]),node
def independent(c,ch):
    start=tuple(base.midpoint(x) for x in (c['values']['H0'],c['U0'],c['values']['zdc']))
    root=mp.findroot(lambda H,U,Ud:tuple(point_system(c,H,U,Ud)[0]),start,
                     tol=mp.mpf('1e-55'),maxsteps=20,solver='mdnewton')
    H,U,Ud=root;res,node=point_system(c,H,U,Ud)
    ch.small('direct_uneliminated_three_equation_point_root',max(abs(x) for x in res),'1e-50')
    ch.add('point_root_inside_frozen_H_U_rectangle',base.lo(c['Hall'])<=H<=base.hi(c['Hall']) and base.lo(c['Uall'])<=U<=base.hi(c['Uall']))
    v,at=point_setup(c,H,U,Ud);n=at(mp.mpf(0),mp.mpf(1))
    eqvals=dict(n,r1=v['alpha']*n['qs'],rt=mp.mpf(0),
                pressure=(v['K_Q']*v['p']**2+v['D']**2+v['rd']**2)/2-v['pot'],
                mass_source=v['K_Q']*v['p']**2-v['zeta']*v['Rc']**2*v['D']**2)
    slope_errors=[]
    for sign in (-1,1):
        vv=dict(eqvals,slope=sign*v['k']*v['eeabs'])
        vv['ty1'],vv['ty3'],vv['R3']=_EX['jets'].numeric(vv)
        mat=_EX['metric_matrix'].numeric(vv);force=_EX['metric_forces'].numeric(vv)
        numeric_matrix=mp.matrix([[mat[3*i+j] for j in range(3)] for i in range(3)])
        ch.add('original_numeric_matrix_entries_retained_'+str(sign),all(numeric_matrix[i,j]==mat[3*i+j] for i in range(3) for j in range(3)))
        ch.add('original_numeric_matrix_nonsingular_'+str(sign),mp.det(numeric_matrix)!=0)
        d=-mp.lu_solve(numeric_matrix,mp.matrix(force))
        vv.update({f'hdd{i}':d[i] for i in range(3)})
        frame0,fc=_EX['frame'].numeric(vv);actual=-frame0/fc
        reduced=_EX['velocity'].numeric(n)[3]
        slope_errors.append(abs(actual-reduced)/(1+abs(actual)+abs(reduced)))
    ch.small('direct_original_metric_frame_slope_both_orientations',max(slope_errors),'1e-70')
    g8,g12=cop.galerkin(c,H,U,8),cop.galerkin(c,H,U,12);errors=[]
    for theta in (mp.mpf(0),mp.pi/7,mp.pi/2):
        errors.extend(abs(a-b)/(1+abs(a)+abs(b)) for a,b in zip(g8(theta),g12(theta)))
    ch.small('independent_original_shift_8_12',max(errors),'1e-30')
    velocity=_EX['velocity'].numeric(n)[0]
    ch.small('point_velocity_matches_exact_elimination',abs(Ud-velocity)/(1+abs(Ud)+abs(velocity)),'1e-50')
    return dict(H=base.SHOW(H),U=base.SHOW(U),Ud=base.SHOW(Ud),point_residual=base.SHOW(max(abs(x) for x in res)),
        original_frame_slope_errors=[base.SHOW(x) for x in slope_errors],galerkin_8_12_difference=base.SHOW(max(errors)),
        interpretation='Independent uneliminated point system and original metric/frame solve; approximate controls, not the interval existence proof.')

def case_job(task):
    i,item=task;ch=base.Checks()
    certificate=dict(family=item['family'],eta=item['eta'],status='COMPUTATION_INCOMPLETE',
                     full_initial_admission=False,state_adopted_or_evolved=False)
    controls={}
    try:
        c=cop.make_case(item,_FN);certificate=certify(c,ch);controls=independent(c,ch)
    except Exception as exc:
        ch.add('implementation_or_control_exception',False,repr(exc))
        certificate['computational_control_incomplete']=True
        controls=dict(error=repr(exc))
    return i,certificate,controls,ch.rows
def calculate(workers):
    mp.mp.dps=110;iv.dps=80
    pins,before=sources();ch=base.Checks();pack,formulas=build(ch)
    if not all(r['passed'] for r in ch.rows):raise ValueError('exact derivation checks failed: '+repr([r for r in ch.rows if not r['passed']]))
    tasks=list(enumerate(READ(cop.CERTS)));results={}
    if len(tasks)!=9:raise ValueError('registered case count drift')
    progress('joint_cases_start',cases=9,workers=min(workers,9))
    if workers==1:
        initialize(pack)
        for task in tasks:
            row=case_job(task);results[row[0]]=row
            progress('joint_case_complete',index=row[0],status=row[1]['status'])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn'),initializer=initialize,initargs=(pack,)) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for future in as_completed(jobs):
                row=future.result()
                if row[0]!=jobs[future] or row[0] in results:raise ValueError('case identity mismatch')
                results[row[0]]=row;progress('joint_case_complete',index=row[0],status=row[1]['status'])
    certs=[];controls=[]
    for i in range(9):
        _,cert,control,checks=results[i];certs.append(cert);controls.append(dict(family=cert['family'],eta=cert['eta'],**control))
        merge_checks(ch,checks,cert['family']+'_'+cert['eta']+'_')
    _,after=sources();ch.add('all_original_bytes_sidecars_metadata_unchanged',before==after)
    count=sum(r['status']=='CERTIFIED_RESTRICTED_JOINT_MEAN_NODE_VELOCITY_ROOT' for r in certs)
    passed=sum(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_RESTRICTED_JOINT_COMPLETION_ONLY' if passed==len(ch.rows) and count==9 else 'FAIL_OR_UNRESOLVED_JOINT_COMPLETION',
        passed=passed,total=len(ch.rows),checks=ch.rows,certified_cases=count,source_sha256=pins,source_metadata=before,
        status='NECESSARY_JOINT_CONSTRUCTION_ONLY_FULL_DOMAIN_OPEN',full_initial_admission=False,state_adopted_or_evolved=False,
        stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        missing_required_physics=['higher rank-changing consistency and persistence','full physical Hessian/Cauchy/energy domain and nonlinear remainder/window','healthy GR','both identifying microscopic matching inputs'])
    return {'summary.json':summary,'formulas.json':formulas,'certificates.json':certs,'independent.json':controls}
def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay');p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log')
    a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose one fresh output or read-only replay')
    workers=parent.selected_workers(a.workers)
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored local area')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    record=lambda q:(SHA(q.read_bytes()),q.stat().st_size,q.stat().st_mtime_ns)
    before={q.name:record(q) for q in dest.iterdir()} if a.replay else None
    data=calculate(workers);payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode()
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay file set changed')
        for name,raw in payload.items():
            q=dest/name
            if q.read_bytes()!=raw or record(q)!=before[name]:raise ValueError('replay bytes/metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as stream:stream.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','certified_cases','status')}),flush=True)
    return 0 if su['passed']==su['total'] and su['certified_cases']==9 else 1
if __name__=='__main__':raise SystemExit(main())
