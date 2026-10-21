"""Deterministic multicore nodal calculation with exact structured solves."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import faulthandler
import multiprocessing as multiprocessing
import os
import sys
import time
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V3_EXECUTION_ADDENDUM_2026-10-18.md'
COUPLED_SOURCE='Analysis/MasterTests/test_01_r4c1_coupled_node_completion_v1.py'
COUPLED_SHA='6fe275eed4aef446978809f12225af8aac16a546bddada8709d5a0ace9911a88'
TRANSPORT='Analysis/MasterTests/outputs/r4c1_node_velocity_transport_attempt_02/'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda name:json.loads((ROOT/name).read_bytes())
CLEAN=lambda x:s.factor(s.cancel(s.expand(x)))
SHOW=lambda x:mp.nstr(x,60)
if SHA((ROOT/COUPLED_SOURCE).read_bytes())!=COUPLED_SHA:raise ValueError('coupled utility drift before import')
spec=importlib.util.spec_from_file_location('frozen_coupled_node_utilities',ROOT/COUPLED_SOURCE)
cop=importlib.util.module_from_spec(spec);spec.loader.exec_module(cop)
base=cop.base;iv=mp.iv
PINS=dict(cop.PINS)
PINS.update({COUPLED_SOURCE:COUPLED_SHA,
    CONTRACT:'b02d70c9d164366cadfd4eff29e1906f1b61e76a5f71eb324a1f3a6a294f11d9',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V2_PARALLEL_ADDENDUM_2026-10-18.md':'67525e65ee101f893b4829ce1e73b50db0ad1dd414ea2885d150646629d6ea00',
    'Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v2.py':'3132188c8b2e061c9617cd35308f699e13223c120c03b1513bc854a74b4d1043',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md':'4d56686ae98c33ee532f324b7fcdd4702c38da19401fa0b5d4ca894fa58c69ba',
    'Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v1.py':'790ab9b0884a14f5ed389e997c8a2bc65fc0f530ae0b1db502dd49c0e8d3008f',
    TRANSPORT+'summary.json':'0bf9482f7addd5fa1a1d66d4aff19b3562fd5cecc19e96f1b099040e5a658c2e',
    TRANSPORT+'equations.json':'01b75e280f4d23340d7e5fe87854b00981e0a5443ed45113270bfc594b47a18b',
    'Theory/Gates/RES-001/RES001_R4C1_NODE_VELOCITY_TRANSPORT_V2_REPORT_2026-10-18.md':'c4ae109ab38d7574d4755f03598aa5d55928ec4f9ee5975ac2a8f2fa581dd05d',
    'Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01/summary.json':'e66ac815aada3fa577db841cc99d55f095115dc203956426a9606fc9ba41ac8e',
    'Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01/certificates.json':'e02cef26c9776f1c4df2b827995ddf2e887038fad886be5f3034bc5133a17cce',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_REPORT_2026-10-18.md':'833dc0f5217a39b5017694d0a3fbd40fa8a4886bb0eb7a2634b1d0d2756b06ab',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_ENDPOINT_ADDENDUM_2026-10-18.md':'a901a269e762ba0e844f94edcfef103fcd84f50fa3b1e7b03d4bea4691266ff8'})


def sources():
    pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());meta={}
    for name,digest in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest:raise ValueError('source drift '+name)
        if sc.read_text().split()[0].lower()!=digest:raise ValueError('sidecar drift '+name)
        for v in (p,sc):
            raw=v.read_bytes();meta[v.relative_to(ROOT).as_posix()]=dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=v.stat().st_mtime_ns)
    return pins,meta


_WORKERS=1
_PROGRESS=None
_TRACE_DIR=None
_TRACE_FILES=[]
_TRACE_PID=None
_SPAWN=multiprocessing.get_context('spawn')


def progress(stage,**values):
    record=dict(stage=stage,**values)
    raw=json.dumps(record,sort_keys=True)+'\n'
    print(raw,end='',flush=True)
    if _PROGRESS is not None:
        with _PROGRESS.open('a',encoding='utf-8') as stream:stream.write(raw)


def trace_here(directory):
    global _TRACE_PID
    if directory is None or _TRACE_PID==os.getpid():return
    path=Path(directory)/('process-'+str(os.getpid())+'.log')
    stream=path.open('x',encoding='utf-8')
    _TRACE_FILES.append(stream);_TRACE_PID=os.getpid()
    faulthandler.enable(file=stream)
    # No periodic asynchronous stack dumps: V2's native crash cause is unconfirmed.


def numerical_init(directory=None):
    mp.mp.dps=100;iv.dps=80
    trace_here(directory)


def configure_progress(name):
    global _PROGRESS,_TRACE_DIR
    if name is None:return
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress must stay in ignored local context directory')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8'):pass
    _PROGRESS=path
    _TRACE_DIR=Path(str(path)+'.stacks');_TRACE_DIR.mkdir(exist_ok=False)
    trace_here(_TRACE_DIR)


def selected_workers(requested):
    usable=os.process_cpu_count() if hasattr(os,'process_cpu_count') else os.cpu_count()
    maximum=min(usable or 1,61 if os.name=='nt' else usable or 1)
    if requested<1:raise ValueError('workers must be positive')
    return min(requested,maximum)


def derivative_init(density,node,directory):
    global _DIFF_DENSITY,_DIFF_NODE
    _DIFF_DENSITY=density;_DIFF_NODE=node
    numerical_init(directory)


def derivative_job(key):
    # Atomic keys, no bound symbols, and no replacement values containing keys.
    # This is the same simultaneous nodal assignment, after differentiation.
    value=CLEAN(s.diff(_DIFF_DENSITY,*key).xreplace(_DIFF_NODE))
    return key,value,os.getpid()


def derivative_table(density,node,keys):
    if not all(isinstance(k,s.Symbol) for k in node):raise ValueError('non-atomic nodal replacement')
    if any(set(v.free_symbols)&set(node) for v in map(s.sympify,node.values())):
        raise ValueError('dependent nodal replacements require a different rule')
    ordered=sorted(set(keys),key=lambda k:(len(k),tuple(str(v) for v in k)))
    workers=min(_WORKERS,len(ordered));results={};pids=set()
    progress('derivatives_start',tasks=len(ordered),workers=workers)
    if workers==1:
        derivative_init(density,node,_TRACE_DIR)
        for key in ordered:
            key,value,pid=derivative_job(key);results[key]=value;pids.add(pid)
            progress('derivative_done',done=len(results),total=len(ordered),pid=pid,key=[str(k) for k in key])
    else:
        with ProcessPoolExecutor(max_workers=workers,mp_context=_SPAWN,initializer=derivative_init,
                                 initargs=(density,node,_TRACE_DIR)) as pool:
            jobs={pool.submit(derivative_job,key):key for key in ordered}
            for future in as_completed(jobs):
                key,value,pid=future.result()
                if key!=jobs[future] or key in results:raise ValueError('duplicate or mismatched derivative job')
                results[key]=value;pids.add(pid)
                progress('derivative_done',done=len(results),total=len(ordered),pid=pid,key=[str(k) for k in key])
    if set(results)!=set(ordered):raise ValueError('incomplete derivative table')
    progress('derivatives_complete',tasks=len(results),actual_worker_pids=sorted(pids))
    return results


def append_checks(ch,rows):
    for row in rows:ch.add(row['name'],row['passed'],row.get('value'),row.get('criterion','exact'))


def smoke_job(index):
    x=s.Symbol('smoke_x')
    expression=(x+index+1)**7
    value=s.diff(expression,x,3).subs(x,s.Rational(2,3))
    checksum=sum((j*j+index)%97 for j in range(300000))
    return index,str(value),checksum,os.getpid()


def parallel_smoke():
    tasks=list(range(48))
    serial=[smoke_job(i)[:3] for i in tasks]
    with ProcessPoolExecutor(max_workers=_WORKERS,mp_context=_SPAWN) as pool:
        parallel=list(pool.map(smoke_job,tasks,chunksize=1))
    if serial!=[r[:3] for r in parallel]:raise ValueError('serial/parallel smoke values differ')
    pids=sorted({r[3] for r in parallel})
    if _WORKERS>1 and len(pids)<2:raise ValueError('smoke did not exercise concurrent workers')
    progress('parallel_smoke_pass',tasks=len(tasks),configured_workers=_WORKERS,actual_worker_pids=pids)
    return 0


def frame_body(h,K,X,V,DV,mu,c1,c2,c3,c4):
    hi=h.inv();gam=s.sqrt(1+(V.T*h*V)[0]);B=s.zeros(4);a=X+hi*K*V
    B[0,0]=(V.T*h*a)[0]/gam
    for j in range(3):B[0,j+1]=a[j]
    for i in range(3):
        B[i+1,0]=sum((h*V)[j]*DV[i,j] for j in range(3))/gam+(K*V)[i]
        for j in range(3):B[i+1,j+1]=DV[i,j]+gam*(K*hi)[i,j]
    G=s.diag(-1,*[h[i,i] for i in range(3)]);Gi=G.inv();n=s.Matrix([gam]+list(V));acc=B.T*n
    I1=sum(Gi[i,i]*G[j,j]*B[i,j]**2 for i in range(4) for j in range(4))
    return -mu*(c1*I1+c2*s.trace(B)**2+c3*s.trace(B*B)-c4*(acc.T*G*acc)[0])/2,B


def derive(ch):
    print('DERIVE_ORIGINAL_ACTION_NODAL_METRIC_AND_FRAME_EULER_JETS',flush=True)
    names='MP2 MU2 c1 c2 c3 c4 K_Q b beta zeta Rc H H0 p D rd pot k pressure mass_source slope r1 rt ty1 ty3 R3 F alpha h2 u2 r2 rho0'
    u={n:s.Symbol(n,real=True) for n in names.split()}
    mp2,mu,c1,c2,c3,c4,H,HB,sl,r1,rt,k,pr,ms=[u[n] for n in ('MP2','MU2','c1','c2','c3','c4','H','H0','slope','r1','rt','k','pressure','mass_source')]
    hq=s.symbols('h0:3',positive=True);ht=s.symbols('ht0:3',real=True);hz=s.symbols('hz0:3',real=True)
    w,wt,wz,R,Rz,ty=s.symbols('w wt wz R Rz ty',real=True)
    variables=(*hq,*ht,*hz,w,wt,wz,R,Rz,ty)
    h=s.diag(*hq);hi=h.inv();dh=[s.zeros(3),s.zeros(3),s.diag(*hz)]
    conn=[[[sum(hi[j,l]*(dh[a][l,i]+dh[i][l,a]-dh[l][a,i]) for l in range(3))/2 for i in range(3)] for a in range(3)] for j in range(3)]
    V=s.Matrix([0,w,0]);DV=s.Matrix(3,3,lambda i,j:(wz if i==2 and j==1 else 0)+sum(conn[j][i][l]*V[l] for l in range(3)))
    sg=s.Matrix([0,ty,Rz]);lie=R*s.diag(*hz)
    for i in range(3):
        for j in range(3):lie[i,j]+=hq[j]*sg[j]*(1 if i==2 else 0)+hq[i]*sg[i]*(1 if j==2 else 0)
    K=(s.diag(*ht)-lie)/2;X=s.Matrix([0,wt-R*wz,0])
    lf,B=frame_body(h,K,X,V,DV,mu,c1,c2,c3,c4)
    km=hi*K;volume=s.sqrt(s.prod(hq))
    L=volume*(mp2*(s.trace(km*km)-s.trace(km)**2)/2+lf+pr+ms*hq[1]*w*w/2)
    node={**{v:1 for v in hq},**{v:2*H for v in ht},**{v:0 for v in hz},w:0,wt:0,wz:sl,R:0,Rz:r1,ty:u['ty1']}
    dd=s.symbols('hdd0:3',real=True);ddz=s.symbols('hddz0:3',real=True);tyt=s.Symbol('ty_time',real=True)
    dt={**{v:2*H for v in hq},**dict(zip(ht,dd)),wz:-HB*sl,Rz:rt,ty:tyt}
    dz={w:sl,wt:-HB*sl,R:r1}
    dtz={**dict(zip(ht,ddz)),w:-HB*sl,wt:u['F']*sl,R:rt}
    dzz={wz:-k*k*sl,Rz:u['R3'],ty:u['ty3']}

    keys=set()
    def need(*key):keys.add(tuple(sorted(key,key=str)))
    for i in range(3):
        need(hq[i])
        for v in dt:need(ht[i],v)
        for v in dz:need(hz[i],v)
    for v in dz:
        need(w,v)
        for q in dt:need(wt,v,q)
        for q in dz:need(wz,v,q)
    for v in dtz:need(wt,v)
    for v in dzz:need(wz,v)
    table=derivative_table(L,node,keys)
    def P(*key):
        canonical=tuple(sorted(key,key=str))
        if canonical not in table:raise ValueError('unregistered derivative key '+str(canonical))
        return table[canonical]
    metric=[]
    for i in range(3):
        metric.append(CLEAN(P(hq[i])-sum(P(ht[i],v)*a for v,a in dt.items())-sum(P(hz[i],v)*a for v,a in dz.items())))
    frame=CLEAN((sum(P(w,v)*a for v,a in dz.items())
                 -sum(P(wt,v,qq)*a*b for v,a in dz.items() for qq,b in dt.items())
                 -sum(P(wt,v)*a for v,a in dtz.items())
                 -sum(P(wz,v,qq)*a*b for v,a in dz.items() for qq,b in dz.items())
                 -sum(P(wz,v)*a for v,a in dzz.items()))/sl)
    ch.zero('frame_jet_has_no_unproved_metric_spatial_acceleration', [s.diff(frame,v) for v in ddz])
    ch.zero('frame_jet_has_no_transverse_shift_time_acceleration',s.diff(frame,tyt))
    progress('metric_rows_assembled')
    matrix=s.Matrix(3,3,lambda i,j:s.diff(metric[i],dd[j]));force=s.Matrix([e.subs(dict.fromkeys(dd,0)) for e in metric])
    metric_diag=-(mp2-mu*(c1+c3))/4
    metric_rank=(mp2+mu*c2)/4
    metric_volume=metric_diag+3*metric_rank
    ch.zero('original_metric_matrix_matches_exact_rank_one_form',
            matrix-metric_diag*s.eye(3)-metric_rank*s.ones(3))
    determinant=CLEAN(metric_diag**2*metric_volume)
    solution=-force/metric_diag+metric_rank*sum(force)/(metric_diag*metric_volume)*s.ones(3,1)
    progress('structured_metric_solve_complete')
    for i,e in enumerate(metric):ch.zero('coupled_metric_row_'+str(i),e.subs(dict(zip(dd,solution))))
    ch.add('metric_response_is_coupled_not_diagonal',any(matrix[i,j]!=0 for i in range(3) for j in range(3) if i!=j))
    ch.add('reject_fixed_metric_acceleration_in_frame_equation',any(s.diff(frame,d)!=0 for d in dd))
    ch.add('reject_omitted_shift_spatial_jet',s.diff(frame,u['ty3'])!=0)
    ch.add('reject_omitted_force_and_alignment_source',s.diff(frame,ms)!=0)
    ch.add('reject_metric_gradient_erasure_before_variation',any(sum(P(hz[i],v)*a for v,a in dz.items())!=0 for i in range(3)))
    reduced=CLEAN(frame.subs(dict(zip(dd,solution))))
    ch.zero('frame_acceleration_coefficient',s.diff(reduced,u['F'])+mu*(c1+c4))
    ch.zero('frame_acceleration_equation_is_affine',s.diff(reduced,u['F'],2))
    fsol=CLEAN(-reduced.xreplace({u['F']:s.Integer(0)})/s.diff(reduced,u['F']))
    ch.zero('coupled_frame_equation_solution',reduced.subs(u['F'],fsol))
    progress('metric_frame_elimination_complete')
    # Independently assemble the FULL six-metric/three-frame temporal block at h=I.
    kk=s.symbols('Kxx Kxy Kxz Kyy Kyz Kzz',real=True);xx=s.Matrix(s.symbols('Xx Xy Xz',real=True));ww=s.Symbol('ww',real=True)
    KM=s.Matrix([[kk[0],kk[1],kk[2]],[kk[1],kk[3],kk[4]],[kk[2],kk[4],kk[5]]]);DD=s.zeros(3);DD[2,1]=sl
    full,_=frame_body(s.eye(3),KM,xx,s.Matrix([0,ww,0]),DD,mu,c1,c2,c3,c4)
    full+=mp2*(s.trace(KM*KM)-s.trace(KM)**2)/2
    expected={kk[0]:-mu*c2,kk[3]:mu*(c1-c2-c3+2*c4),kk[5]:-mu*c2}
    for q in kk:
        ch.zero('full_temporal_frame_metric_slope_'+str(q),s.diff(full,xx[1],q,ww).subs(ww,0)-expected.get(q,0))
    for q in (xx[0],xx[2]):ch.zero('other_frame_acceleration_does_not_enter_slope_'+str(q),s.diff(full,xx[1],q).subs(ww,0))
    for q in (kk[0],kk[3],kk[5]):
        for z in (kk[1],kk[2],kk[4]):ch.zero('nodal_metric_diagonal_offdiagonal_block_'+str(q)+'_'+str(z),s.diff(full,q,z).subs(ww,0))
    # Regulator X-momentum on homogeneous psi is -b*Z*p*V_y; Z=U*V_y^2.
    zz,bb,pp,UU=s.symbols('Z b0 p0 U0',real=True)
    regmoment=-bb*UU*ww**3*pp
    ch.zero('regulator_frame_momentum_value_and_normal_jet', [regmoment.subs(ww,0),s.diff(regmoment,ww).subs(ww,0)])
    ch.zero('regulator_frame_metric_scalar_acceleration_slope',s.diff(regmoment,pp,ww).subs(ww,0))
    # The original frame cusp force is -3*A*p^3*w*|w|; its normal derivative vanishes.
    x,AA,ppos,sp=s.symbols('x A ppos spos',positive=True)
    for sign in (-1,1):ch.zero('original_cusp_first_frame_normal_jet_'+str(sign),s.limit(-3*AA*ppos**3*(sign*sp*x)*sp*x/(sign*sp*x),x,0,dir='+'))
    progress('full_temporal_block_controls_complete')
    # Substitute the exact transverse shift jet, without c13 division on B1.
    al=u['alpha'];c13=c1+c3;dt0=mp2-mu*c13;dt2=2*mu*(c4-c3)
    t1=-mu*c13*sl/dt0
    t3=-mu*sl/dt0*(-c13*k*k+2*sl*sl*(2*c3-c13/2-c13*dt2/dt0))
    P0=mu*(c1+c2+c3);W0=-mu*(c1+c2+c4)*sl*sl
    fprime=mu*sl*sl*(HB*(c1+2*c2+c4)-H*(3*c1+5*c2+c3+2*c4))
    r3=((W0-2*P0*sl*sl)*r1-fprime)/P0
    fphysical=CLEAN(fsol.subs({u['ty1']:t1,u['ty3']:t3,u['R3']:r3}).subs(sl*sl,k*k*al))
    ch.add('frame_slope_even_normal_orientation',not fphysical.has(sl))
    for v in (u['ty1'],u['ty3'],u['R3']):ch.add('exact_initial_shift_jet_substituted_'+str(v),not fphysical.has(v))
    progress('exact_shift_jets_substituted')
    # Background bridge: derive Hdot from the metric pressure equation before using the lapse constraint.
    M=mp2+mu*(c1+3*c2+c3)/2
    hd_pressure=-(3*M*HB*HB+pr)/(2*M)
    planar=READ(cop.PLANAR)
    cv=s.sympify(planar['generic_cV2'],locals=u)
    mass=s.sympify(planar['generic_frame_mass_squared'],locals={**u,'H':HB,'psi_dot':u['p'],'u0':u['Rc'],'v_dot':u['D'],'u_dot':s.Integer(0),'v0':s.Integer(0),'Hdot':hd_pressure})
    bg=CLEAN(fphysical.subs({H:HB,r1:0,rt:0,al:0}))
    # Check the explicit source rewrite against the frozen generic mass expression.
    mass_bg=(2*HB*HB*mu*(c1+c4)+hd_pressure*mu*(-3*c2-c3+c4)-ms)/(mu*(c1+c4))
    ch.zero('generic_mass_source_rewrite',mass-mass_bg.subs(ms,u['K_Q']*u['p']**2-u['zeta']*u['Rc']**2*u['D']**2))
    ch.zero('unchanged_background_frame_bridge',bg-(-cv*k*k-mass_bg+HB*HB-hd_pressure))
    # Scalar condition with the LOCAL beta*rho replaced only by the already-certified node equation.
    Kq,be,pp,rho0=[u[n] for n in ('K_Q','beta','p','rho0')]
    U,Ud=s.symbols('U Ud',real=True)
    beta_rho=(Kq+2*u['b']*k*k*al)*U-Kq*HB*pp-Kq*pp*r1
    acc=-U-(3*H-HB-2*r1)*pp
    trans=((1+2*u['b']*k*k*al/Kq)*Ud+(2*H-3*HB-r1)*acc
           +pp*(fphysical+HB*HB-8*H*HB+6*H*H-rt-4*r1*(H-HB))
           -(4*u['b']*H*U*k*k*al+(-3*H+r1+be*pp)*beta_rho)/Kq)
    ch.zero('arbitrary_shift_time_jet_cancels_from_final_test',s.diff(CLEAN(trans),rt))
    pr0=(Kq*pp**2+u['Rc']**2+u['rd']**2)/2-u['pot']
    ms0=Kq*pp**2-u['zeta']*u['Rc']**4
    bg0=bg.subs({pr:pr0,ms:ms0})
    aref=-3*HB*pp-be*rho0/Kq;rhoref=(-3*HB+be*pp)*rho0
    udref=CLEAN(HB*aref+be*rhoref/Kq-pp*bg0+pp*HB*HB)
    hh,uu,rr=u['h2'],u['u2'],u['r2']
    phase=u['Rc']/(1-u['zeta']*u['Rc']**2*al/2)
    substitutions={H:HB+al*hh,U:HB*pp+be*rho0/Kq+al*uu,r1:al*rr,rt:0,Ud:udref,
                   pr:(Kq*pp**2+phase**2+u['rd']**2)/2-u['pot'],ms:Kq*pp**2-u['zeta']*u['Rc']**2*phase**2}
    progress('amplitude_normalization_start')
    numerator,denominator=s.fraction(s.cancel(trans.subs(substitutions,simultaneous=True)))
    poly=s.Poly(s.expand(numerator),al)
    ch.zero('exact_removable_zero_before_amplitude_normalization',poly.coeff_monomial(1))
    scaled=CLEAN(sum(coef*al**(power[0]-1) for power,coef in poly.terms() if power[0]>0)/denominator)
    ch.add('no_division_by_amplitude_after_normalization',not s.denom(s.cancel(scaled)).subs(al,0).equals(0))
    # The old recipe is equivalent using the background lapse equation, not a new velocity choice.
    kin=Kq*pp**2+u['Rc']**2+u['rd']**2;hd_old=-(kin+rho0)/(2*M)
    hb2=(kin/2+u['pot']+rho0)/(3*M)
    ch.zero('pressure_Hdot_equals_old_constraint_recipe',CLEAN(hd_pressure.subs(pr,pr0)-hd_old).subs(HB**2,hb2))
    progress('symbolic_derivation_complete')
    equations=dict(restricted_nodal_density=str(L),metric_Euler=[str(e) for e in metric],
        metric_acceleration_matrix=str(matrix),metric_acceleration_determinant=str(determinant),metric_accelerations=[str(CLEAN(v)) for v in solution],
        frame_Euler_normal_jet=str(frame),frame_acceleration_slope_before_shift_substitution=str(fsol),
        actual_frame_slope=str(fphysical),transverse_shift_first_jet=str(t1),transverse_shift_third_jet=str(t3),
        longitudinal_shift_third_jet=str(r3),transport_defect=str(CLEAN(trans)),normalized_transport_defect=str(scaled),
        equivalent_old_Ud0=str(udref),background_slope=str(bg),background_Hdot_from_pressure=str(hd_pressure),
        density_scope='Exact for these nodal metric and first-normal frame Euler jets; intrinsic flat curvature and future-dust spatial pressure vanish only on this initial slice; cusp/regulator nodal jets are handled separately and retained in full controls.',
        full_action_scope='Necessary coupled nodal accelerations, not the entire constrained initial-value system or a physical validity window.',
        source_pressure='(K_Q*p^2+D_phase^2+rd^2)/2-pot',mass_source_definition='K_Q*p^2-zeta*Rc^2*D_phase^2; source, not cutoff')
    return u,dict(metric=metric,frame=frame,dd=dd,tyt=tyt,actual=fphysical,scaled=scaled,udref=udref,
                  determinant=determinant,cv=cv,background=bg),equations


def _coordinate_controls_impl(ch,u,ex,seed_values=(0,1)):
    print('INDEPENDENT_FULL_COORDINATE_FRAME_AND_METRIC_DENSITY_VARIATIONS',flush=True)
    records=[]
    for seed in seed_values:
        H=mp.mpf(2+seed)/7;HB=mp.mpf(3)/11;sl=mp.mpf(1 if seed==0 else -1)/3;k=mp.mpf(5)
        r1=mp.mpf(2)/29;rt=-mp.mpf(2)/41;t1=mp.mpf(3)/31;t3=-mp.mpf(2)/37;r3=mp.mpf(1)/43
        tyt=mp.mpf(1)/47;F=-mp.mpf(2+seed)/7
        hdd=mp.matrix([[mp.mpf(1+i+j+seed)/53 for j in range(3)] for i in range(3)])
        hddz=mp.matrix([[mp.mpf(2+i+j)/59 for j in range(3)] for i in range(3)])
        p=mp.mpf(1+seed)/9;D=mp.mpf(2)/13;rd=mp.mpf(1)/17;rc=mp.mpf(3)/19
        par={name:mp.mpf(value) for name,value in dict(MP2='1.2',MU2='0.4',c1='0.2',c2='0.1',c3='-0.07',c4='0.05',K_Q='0.6',A='0.13',b='0.15',zeta='0.03',beta='0.02').items()}
        pot=mp.mpf(2)/23;pressure=(par['K_Q']*p*p+D*D+rd*rd)/2-pot;mass=par['K_Q']*p*p-par['zeta']*rc*rc*D*D
        vals=dict(par,H=H,H0=HB,slope=sl,r1=r1,rt=rt,ty1=t1,ty3=t3,R3=r3,F=F,k=k,pressure=pressure,mass_source=mass,ty_time=tyt)
        vals.update({'hdd'+str(i):hdd[i,i] for i in range(3)})
        vals.update({'hddz'+str(i):hddz[i,i] for i in range(3)})
        metric_fn=base.Eval(ex['metric']);frame_fn=base.Eval([ex['frame']])
        expected_metric=metric_fn.numeric(vals);expected_frame=frame_fn.numeric(vals)[0]

        def initial(t,z):
            ww=sl*z-k*k*sl*z**3/6;wwz=sl-k*k*sl*z*z/2
            hm=hdd+z*hddz;h=(1+2*H*t)*mp.eye(3)+t*t*hm/2;ht=2*H*mp.eye(3)+t*hm;hz=t*t*hddz/2
            shift=mp.matrix([0,t1*z+t3*z**3/6+tyt*t*z,r1*z+r3*z**3/6+rt*t*z])
            st=mp.matrix([0,tyt*z,rt*z]);sz=mp.matrix([0,t1+t3*z*z/2+tyt*t,r1+r3*z*z/2+rt*t])
            fx=mp.mpf(1)/61;fz=-mp.mpf(2)/67
            V=mp.matrix([fx*sl*z*t*t/2,ww*(1-HB*t+F*t*t/2),fz*sl*z*t*t/2])
            vt=mp.matrix([fx*sl*z*t,ww*(-HB+F*t),fz*sl*z*t])
            vz=mp.matrix([fx*sl*t*t/2,wwz*(1-HB*t+F*t*t/2),fz*sl*t*t/2])
            return [h,ht,hz,V,vt,vz,shift,st,sz]

        def density(t,z,field,slot,value):
            h,ht,hz,V,vt,vz,shift,st,sz=initial(t,z)
            if field in (0,1,2):
                target=(h,ht,hz)[slot];target[field,field]=value
            else:(V,vt,vz)[slot][1]=value
            hi=h**-1;gam=mp.sqrt(1+(V.T*h*V)[0]);n=mp.matrix([gam]+list(V-gam*shift))
            g=mp.zeros(4);gi=mp.zeros(4);g[0,0]=-1+(shift.T*h*shift)[0];gi[0,0]=-1
            for i in range(3):
                g[0,i+1]=g[i+1,0]=(h*shift)[i];gi[0,i+1]=gi[i+1,0]=shift[i]
                for j in range(3):g[i+1,j+1]=h[i,j];gi[i+1,j+1]=hi[i,j]-shift[i]*shift[j]
            dg=[];dn=mp.zeros(4)
            for a in range(4):
                hh,sv,vv=(ht,st,vt) if a==0 else (hz,sz,vz) if a==3 else (mp.zeros(3),mp.zeros(3,1),mp.zeros(3,1))
                ga=((V.T*hh*V)[0]+2*(V.T*h*vv)[0])/(2*gam)
                gm=mp.zeros(4);gm[0,0]=2*(sv.T*h*shift)[0]+(shift.T*hh*shift)[0];hs=hh*shift+h*sv
                dn[a,0]=ga
                for i in range(3):
                    gm[0,i+1]=gm[i+1,0]=hs[i];dn[a,i+1]=vv[i]-ga*shift[i]-gam*sv[i]
                    for j in range(3):gm[i+1,j+1]=hh[i,j]
                dg.append(gm)
            conn=[[[sum(gi[c,l]*(dg[a][l,bb]+dg[bb][l,a]-dg[l][a,bb]) for l in range(4))/2 for bb in range(4)] for a in range(4)] for c in range(4)]
            B=mp.matrix(dn)
            for a in range(4):
                for j in range(4):B[a,j]+=sum(conn[j][a][l]*n[l] for l in range(4))
            hp=gi+n*n.T;acc=B.T*n;tr=lambda M:sum(M[i,i] for i in range(M.rows))
            frame=-par['MU2']*(par['c1']*tr(gi*B*g*B.T)+par['c2']*tr(B)**2+par['c3']*tr(B*B)-par['c4']*(acc.T*g*acc)[0])/2
            lie=shift[2]*hz
            for i in range(3):
                for j in range(3):lie[i,j]+=sum(h[l,j]*sz[l] for l in range(3))*(1 if i==2 else 0)+sum(h[i,l]*sz[l] for l in range(3))*(1 if j==2 else 0)
            KK=(ht-lie)/2;km=hi*KK;gravity=par['MP2']*(tr(km*km)-tr(km)**2)/2
            qp=mp.matrix([p+t/71,0,0,0]);qv=mp.matrix([D+t/73,0,0,0]);qu=mp.matrix([t/79,0,0,0]);qr=mp.matrix([rd+t/83,0,0,0])
            U=mp.mpf(3)/17;Ud=mp.mpf(2)/19;ww=sl*z-k*k*sl*z**3/6;wwz=sl-k*k*sl*z*z/2
            Z=U*ww*ww+Ud*t*ww*ww+t*t/89
            zg=mp.matrix([Ud*ww*ww+2*t/89,0,0,2*(U+Ud*t)*ww*wwz])
            Q=(n.T*qp)[0];Y=(qp.T*hp*qp)[0]
            force=par['K_Q']*Q*Q/2-par['A']*Y**mp.mpf('1.5')
            reg=par['b']*Z*Z/2-par['b']*(zg.T*hp*qp)[0]-par['b']*Z*(acc.T*qp)[0]
            uu=rc+t*t/158;vv=D*t+t*t/146;current=vv*qu-uu*qv
            align=-par['zeta']*(current.T*hp*current)[0]/2
            can=-((qu.T*gi*qu)[0]+(qv.T*gi*qv)[0]+(qr.T*gi*qr)[0])/2
            # The original varied dust pressure and intrinsic-flat-curvature force are zero at this slice.
            return mp.sqrt(mp.det(h))*(gravity+frame+force+reg+align+can-pot)

        def moment(t,z,field,slot):
            state=initial(t,z);value=state[slot][field,field] if field<3 else state[3+slot][1]
            return mp.diff(lambda v:density(t,z,field,slot,v),value)
        def euler(t,z,field):
            return moment(t,z,field,0)-mp.diff(lambda tt:moment(tt,z,field,1),t)-mp.diff(lambda zz:moment(t,zz,field,2),z)
        errs=[]
        for i in range(3):
            got=euler(0,0,i);er=abs(got-expected_metric[i])/(1+abs(got)+abs(expected_metric[i]));errs.append(SHOW(er))
            ch.small('coordinate_metric_Euler_'+str(seed)+'_'+str(i),er,'1e-40')
        probes=[]
        for step,tol in (('1e-12','1e-20'),('1e-18','1e-30')):
            x=mp.mpf(step);vals2=[]
            for sign in (-1,1):
                z=sign*x;ww=sl*z-k*k*sl*z**3/6;cusp=-3*par['A']*p**3*ww*abs(ww)
                vals2.append((euler(0,z,3)-cusp)/ww)
            got=sum(vals2)/2;er=abs(got-expected_frame)/(1+abs(got)+abs(expected_frame))
            ch.small('coordinate_frame_normal_jet_'+str(seed)+'_'+step,er,tol)
            probes.append(dict(normal_probe=step,normalized_error=SHOW(er),tolerance=tol))
        records.append(dict(seed=seed,metric_Euler_errors=errs,frame_probes=probes,all_metric_frame_second_time_jets_retained=True,original_regulator_and_cusp_retained=True))
    return records



def control_job(args):
    seed,u,ex=args
    ch=base.Checks()
    result=_coordinate_controls_impl(ch,u,ex,seed_values=(seed,))
    return seed,result,ch.rows,os.getpid()


def coordinate_controls(ch,u,ex):
    if _WORKERS==1:return _coordinate_controls_impl(ch,u,ex)
    results={}
    progress('coordinate_controls_start',seeds=2,workers=min(_WORKERS,2))
    with ProcessPoolExecutor(max_workers=min(_WORKERS,2),mp_context=_SPAWN,
                             initializer=numerical_init,initargs=(_TRACE_DIR,)) as pool:
        jobs={pool.submit(control_job,(seed,u,ex)):seed for seed in (0,1)}
        for future in as_completed(jobs):
            seed,records,rows,pid=future.result()
            if seed!=jobs[future] or seed in results:raise ValueError('coordinate seed mismatch')
            results[seed]=(records,rows)
            progress('coordinate_seed_complete',seed=seed,pid=pid)
    all_records=[]
    for seed in (0,1):
        records,rows=results[seed];all_records.extend(records);append_checks(ch,rows)
    return all_records


def _one_case(item,parent,fn,normalized,actual,udfn):
    ch=base.Checks();cases=[]
    if (item['family'],item['eta'])!=(parent['family'],parent['eta']):raise ValueError('family pairing drift')
    c=cop.make_case(item,fn);v=c['values'];H=c['Hall'];U=c['Uall'];al=v['alpha'];HB=v['H0'];M=v['M']
    attempt=[]
    for n in (16,32,64,128,256):
        mean=iv.mpf(0)
        for j in range(n):
            theta=iv.mpf([base.lo(iv.pi*j/(2*n)),base.hi(iv.pi*(j+1)/(2*n))])
            vv=cop.state(c,H,U,iv.cos(theta),iv.sin(theta),fn)
            mean+=fn['energy'].interval(vv)[0]/n
        node=cop.state(c,H,U,iv.mpf(0),iv.mpf(1),fn)
        phase_t=v['zeta']*v['Rc']**2/2
        phase_scaled=v['Rc']**2*(2*phase_t-phase_t**2*al)/(2*(1-phase_t*al)**2)
        h2=(mean+phase_scaled)/(3*M*(H+HB))
        u2=cop.unpack(parent['attempts'][-1]['regulator_coefficient_correction_over_e_squared'])
        vals=dict(v,H0=HB,H=HB+al*h2,h2=h2,u2=u2,r2=node['qs'],rho0=v['rho'],rt=iv.mpf(0))
        vals['r1']=al*node['qs'];vals['pressure']=(v['K_Q']*v['p']**2+node['D']**2+v['rd']**2)/2-v['pot']
        vals['mass_source']=v['K_Q']*v['p']**2-v['zeta']*v['Rc']**2*node['D']**2
        defect=normalized.interval(vals)[0];fvalue=actual.interval(vals)[0];udvalue=udfn.interval(vals)[0]
        oldud=v['zdc'];overlap=base.lo(udvalue)<=base.hi(oldud) and base.lo(oldud)<=base.hi(udvalue)
        sign='POSITIVE' if base.lo(defect)>0 else 'NEGATIVE' if base.hi(defect)<0 else 'UNRESOLVED'
        attempt.append(dict(boxes=n,normalized_transport_defect=base.pack(defect),actual_frame_slope=base.pack(fvalue),
                            H_correction_over_e_squared=base.pack(h2),U_correction_over_e_squared=base.pack(u2),
                            normalized_exact_shift_gradient=base.pack(node['qs']),old_velocity_equivalent_overlap=overlap,
                            disposition=sign))
        if sign!='UNRESOLVED':break
    ident=c['family']+'_'+c['eta'];dt=v['MP2']-v['MU2']*(v['c1']+v['c3'])
    ch.add('nodal_complement_invertible_'+ident,base.lo(v['MU2']*(v['c1']+v['c4']))>0 and base.lo(dt)>0 and base.lo(M)>0)
    ch.add('old_velocity_not_redefined_'+ident,overlap)
    ch.add('all_nodal_bounds_finite_'+ident,all(mp.isfinite(t) for e in (defect,fvalue,h2,u2) for t in (base.lo(e),base.hi(e))))
    cases.append(dict(family=c['family'],eta=c['eta'],amplitude_squared=base.pack(al),attempts=attempt,
                      disposition='REJECTED_SELECTED_SMOOTH_VELOCITY_CONTINUATION' if sign!='UNRESOLVED' else 'UNRESOLVED_BY_FROZEN_BOUNDS',
                      velocity_repair_adopted=False,full_initial_admission=False,
                      interpretation='Necessary scalar time condition with action-derived coupled nodal frame/metric accelerations; not persistence, a physical window, weak-solution or all-action no-go.'))
    print('CASE '+ident+' '+cases[-1]['disposition'],flush=True)
    return cases[0],ch.rows


def case_init(ex,directory):
    global _CASE_FN,_CASE_NORMALIZED,_CASE_ACTUAL,_CASE_UD
    numerical_init(directory)
    dummy=base.Checks();_,_CASE_FN,_=cop.symbolic(dummy)
    if not all(r['passed'] for r in dummy.rows):raise ValueError('frozen inverse utility failed')
    _CASE_NORMALIZED=base.Eval([ex['scaled']])
    _CASE_ACTUAL=base.Eval([ex['actual']])
    _CASE_UD=base.Eval([ex['udref']])


def case_job(args):
    index,item,parent=args
    record,rows=_one_case(item,parent,_CASE_FN,_CASE_NORMALIZED,_CASE_ACTUAL,_CASE_UD)
    return index,record,rows,os.getpid()


def case_bounds(ch,u,ex):
    progress('cases_start',cases=9,workers=min(_WORKERS,9))
    parents=READ('Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01/certificates.json')
    old=READ(cop.CERTS)
    if len(old)!=9 or len(parents)!=9:raise ValueError('registered case count drift')
    tasks=[(i,item,parent) for i,(item,parent) in enumerate(zip(old,parents))]
    results={}
    if _WORKERS==1:
        case_init(ex,_TRACE_DIR)
        for task in tasks:
            index,record,rows,pid=case_job(task);results[index]=(record,rows)
            progress('case_complete',index=index,pid=pid,disposition=record['disposition'])
    else:
        # Each worker owns its mpmath and compiled interval functions; no nested pools.
        payload={k:ex[k] for k in ('scaled','actual','udref')}
        with ProcessPoolExecutor(max_workers=min(_WORKERS,9),mp_context=_SPAWN,
                                 initializer=case_init,initargs=(payload,_TRACE_DIR)) as pool:
            jobs={pool.submit(case_job,task):task[0] for task in tasks}
            for future in as_completed(jobs):
                index,record,rows,pid=future.result()
                if index!=jobs[future] or index in results:raise ValueError('case job mismatch')
                results[index]=(record,rows)
                progress('case_complete',index=index,pid=pid,disposition=record['disposition'])
    if set(results)!=set(range(9)):raise ValueError('missing registered case')
    cases=[]
    for index in range(9):
        record,rows=results[index];cases.append(record);append_checks(ch,rows)
    ch.add('all_nine_registered_cases_retained',len(cases)==9)
    return cases


def calculate():
    mp.mp.dps=100;iv.dps=80
    pins,before=sources();ch=base.Checks()
    u,ex,equations=derive(ch);independent=coordinate_controls(ch,u,ex);cases=case_bounds(ch,u,ex)
    _,after=sources();ch.add('all_original_source_bytes_sidecars_metadata_unchanged',before==after)
    rejected=sum(r['disposition'].startswith('REJECTED_') for r in cases)
    summary=dict(validation='PASS_COUPLED_NODAL_ACCELERATION_AUDIT_ONLY' if all(r['passed'] for r in ch.rows) else 'FAIL_OR_UNRESOLVED_COUPLED_NODE_AUDIT',
        passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        tested_case_count=len(cases),rejected_selected_velocity_cases=rejected,scientifically_unresolved_case_count=len(cases)-rejected,
        full_initial_data_admission=False,state_adopted_or_evolved=False,action_no_go=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        status='COUPLED_NODAL_ACCELERATIONS_CALCULATED_VELOCITY_DISPOSITIONS_BOUNDED_FULL_DOMAIN_OPEN',
        missing_required_physics=['remaining compatible regulator velocity and higher rank-changing consistency',
            'full admission/persistence and physical reduced Hessian/Cauchy/energy domain',
            'nonlinear evolution remainder, physical window and healthy GR','both identifying microscopic matching inputs'])
    return {'summary.json':summary,'equations.json':equations,'independent.json':independent,'cases.json':cases}


def main():
    global _WORKERS
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output');parser.add_argument('--replay')
    parser.add_argument('--workers',type=int,default=16);parser.add_argument('--progress-log');parser.add_argument('--parallel-smoke',action='store_true')
    args=parser.parse_args();_WORKERS=selected_workers(args.workers);configure_progress(args.progress_log)
    progress('execution_start',requested_workers=args.workers,usable_workers=_WORKERS,python=sys.version.split()[0],sympy=s.__version__)
    if args.parallel_smoke:
        if args.output or args.replay:parser.error('smoke mode does not write science receipts')
        return parallel_smoke()
    if bool(args.output)==bool(args.replay):parser.error('choose exactly one output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science output root')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    before={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    results=calculate();payloads={name:ENC(v) for name,v in results.items()}
    progress('calculation_returned',passed=results['summary.json']['passed'],total=results['summary.json']['total'])
    for name,raw in list(payloads.items()):payloads[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(before)!=set(payloads):raise ValueError('replay file-set mismatch')
        for name,raw in payloads.items():
            p=dest/name
            if p.read_bytes()!=raw:raise ValueError('recomputed bytes differ '+name)
            if (SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)!=before[name]:raise ValueError('original metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payloads.items():
            with (dest/name).open('xb') as stream:stream.write(raw)
    su=results['summary.json'];print(json.dumps({n:su[n] for n in ('validation','passed','total','rejected_selected_velocity_cases','scientifically_unresolved_case_count','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1


if __name__=='__main__':raise SystemExit(main())

