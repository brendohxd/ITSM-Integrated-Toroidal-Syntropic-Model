"""Complete initial planar momentum flow and first node tangency, not admission."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import traceback
import mpmath as mp
import numpy as np
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/test_01_r4c1_global_nodal_lift_v2.py'
PARENT_SHA = '8ff1ccdd3c47c151276c21f968e355d032ec75698a300918546d19ffe0892cce'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_NODAL_MOMENTUM_TANGENCY_V1_CONTRACT_2026-10-20.md'
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda x: (json.dumps(x, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes()) != PARENT_SHA:
    raise ValueError('parent drift')
spec = importlib.util.spec_from_file_location('frozen_global_nodal_lift', ROOT/PARENT)
lift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lift)
nodal, canonical, planar, base = lift.nodal, lift.canonical, lift.planar, lift.base
PINS = dict(lift.PINS)
PINS.update({PARENT: PARENT_SHA,
    CONTRACT: 'ff588ca6e50798fd25242d2976d71ed58e562a37a8558be03266c18a986ede2b',
    'Theory/Gates/RES-001/RES001_R4C1_GLOBAL_NODAL_LIFT_V2_REPORT_2026-10-20.md':
    '88549485969e0d85ed216afb0ab5ba2c7ab8a577c65bd096fe969f1172024793',
    'Analysis/MasterTests/outputs/r4c1_global_nodal_lift_attempt_02/summary.json':
    '28ec677f75404d9e48431d1c1c7dc8ffcce99f70e18dfc9b66f0be7cd6f3778d'})
NAMES = ('Gxx','Gxy','Gyy','Vx','Vy','Vz','radius','phase','reservoir','dust','Z','s')
STEPS = (1e-18, 1e-22)
_PROGRESS = None

def progress(stage, **kw):
    line = json.dumps(dict(stage=stage, **kw), sort_keys=True)
    print(line, flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a', encoding='utf-8') as f:
            f.write(line+'\n')

def sources():
    pins = {**PINS, SELF: SHA((ROOT/SELF).read_bytes())}
    records = {}
    for name, expected in pins.items():
        p = ROOT/name
        sidecar = Path(str(p)+'.sha256')
        if SHA(p.read_bytes()) != expected or sidecar.read_text().split()[0].lower() != expected:
            raise ValueError('source/sidecar drift '+name)
        for f in (p, sidecar):
            raw = f.read_bytes()
            records[f.relative_to(ROOT).as_posix()] = dict(
                sha256=SHA(raw), bytes=len(raw), mtime_ns=f.stat().st_mtime_ns)
    return pins, records

def chart(raw, out):
    q, p = out['q'], out['p']
    n = len(q)
    X = dict(Q=np.zeros((n,12)), P=np.zeros((n,10)),
             M=q[0,[2,4,5]].copy(), PM=raw['mean_pi']*np.array([2,2,1]))
    X['Q'][:,:3] = q[:,[0,1,3]]
    X['P'][:,:3] = p[:,[0,1,3]]
    X['Q'][:,3:6], X['P'][:,3:6] = q[:,6:9], p[:,6:9]
    sine = np.sin(raw['theta'])
    X['P'][:,4] -= sine*np.mean(sine*X['P'][:,4])/np.mean(sine*sine)
    radius = np.sqrt(q[:,9]**2+q[:,10]**2)
    X['Q'][:,6], X['Q'][:,7] = radius, np.arctan2(q[:,10],q[:,9])
    X['P'][:,6] = (q[:,9]*p[:,9]+q[:,10]*p[:,10])/radius
    X['P'][:,7] = q[:,9]*p[:,10]-q[:,10]*p[:,9]-raw['Qtheta']
    X['Q'][:,8:11], X['P'][:,8] = q[:,[11,14,13]], p[:,11]
    X['P'][:,9] = p[:,14]-raw['Qdust']
    X['Q'][:,11] = raw['s']
    return X

def copy_chart(X):
    return {k: v.astype(complex).copy() for k,v in X.items()}

def coordinates(X, raw, tau):
    dtype = np.result_type(*X.values(), tau)
    q = raw['q'].astype(dtype)
    q[:,[0,1,3]], q[:,[2,4,5]] = X['Q'][:,:3], X['M']
    q[:,6:9] = X['Q'][:,3:6]
    angle = X['Q'][:,7]-np.mean(X['Q'][:,7])
    q[:,9], q[:,10] = X['Q'][:,6]*np.cos(angle), X['Q'][:,6]*np.sin(angle)
    q[:,11], q[:,13] = X['Q'][:,8], X['Q'][:,10]
    q[:,14], q[:,12] = X['Q'][:,9]-np.mean(X['Q'][:,9]), tau
    if np.min(np.real(X['Q'][:,6])) <= 0:
        raise ValueError('nonpositive polar radius')
    return q, angle

def decode(X, raw, tau=0):
    q, angle = coordinates(X, raw, tau)
    p = raw['p'].astype(q.dtype)
    p[:,[0,1,3]], p[:,6:9] = X['P'][:,:3], X['P'][:,3:6]
    pR = X['P'][:,6]
    pt = raw['Qtheta']+X['P'][:,7]-np.mean(X['P'][:,7])
    radius = X['Q'][:,6]
    p[:,9] = pR*np.cos(angle)-pt*np.sin(angle)/radius
    p[:,10] = pR*np.sin(angle)+pt*np.cos(angle)/radius
    p[:,11] = X['P'][:,8]
    p[:,14] = raw['Qdust']+X['P'][:,9]-np.mean(X['P'][:,9])
    return dict(raw, q=q, p=p, s=X['Q'][:,11],
                mean_pi=X['PM']*np.array([.5,.5,1]))

def reduced(X, raw, par, tau=0, first_gradient=False):
    out = lift.restore_undivided(decode(X,raw,tau), par)
    if first_gradient:
        # ONLY the flat constant-lapse first variation: curvature's integrated
        # variation is an exact periodic divergence. Never a Hessian evaluator.
        E,F,blocks = nodal.partial_blocks(out['q'],np.linalg.inv(canonical.tensor_h(out['q'])),
            out['grad'],out['DV'],out['p'],par,np.zeros(len(out['q'])),X['Q'][:,11])
        out = dict(out,E=E,F=F,blocks=blocks,
            H=np.mean(E/X['Q'][:,11]-F*(raw['D']@(1/X['Q'][:,11]))))
    return out

def direction(raw, kind, j):
    n = len(raw['q'])
    v = np.eye(n)[j].copy()
    if kind in (7,9):
        v -= 1/n
    elif kind == 4:
        sine = np.sin(raw['theta'])
        v -= sine*sine[j]/np.sum(sine*sine)
    return v

def position_variation(X,raw,kind,j,step):
    Y = copy_chart(X)
    if kind == 'M':
        Y['M'][j] += 1j*step
    else:
        Y['Q'][:,kind] += 1j*step*direction(raw,kind,j)
    return Y

def reference_context(raw,out,Ud):
    rate = raw['rate']
    shift = np.zeros((len(raw['q']),3))
    shift[:,2] = raw['shift']/rate
    shift[:,1] = (raw['I']@(-2*raw['y'][:,4]))/rate
    zhat = float(Ud)*raw['q'][:,7]**2-raw['shift']*(raw['D']@raw['q'][:,13])
    return dict(out=out,shift=shift,zhat=zhat)

def original_generator(X,raw,par,ref,omit_multiplier=False):
    # Do NOT restore the varied spatial momenta: independent canonical variables
    # are held fixed until AFTER varying this original first-order generator.
    q, angle = coordinates(X,raw,0)
    p = ref['out']['p'].astype(q.dtype)
    pR = ref['out']['p'][:,9]  # initial angle is exactly zero
    pt = ref['out']['q'][:,9]*ref['out']['p'][:,10]
    radius = X['Q'][:,6]
    p[:,9] = pR*np.cos(angle)-pt*np.sin(angle)/radius
    p[:,10] = pR*np.sin(angle)+pt*np.cos(angle)/radius
    _,hi,grad,DV,_ = canonical.spatial_geometry(q,raw['D'])
    E,F,co = nodal.partial_blocks(q,hi,grad,DV,p,par,np.zeros(len(q)),raw['s'])
    multiplier = 0 if omit_multiplier else (p[:,13]+co['g']*raw['s'])*ref['zhat']
    N = np.full(len(q),1/raw['rate'])
    return (np.mean(N*(E+p[:,12]*raw['s']+multiplier)-(raw['D']@N)*F)
        +canonical.diffeo(q,p,ref['shift'],raw['D'])/(2*np.pi))

def initial_tangent(X,raw):
    T = {k: np.zeros_like(v) for k,v in X.items()}
    p,H,HB = raw['rate'],raw['H'],raw['HB']
    T['Q'][:,0] = T['Q'][:,2] = 2*H/p
    T['M'][2] = 2*H/p
    T['Q'][:,4] = -HB*raw['q'][:,7]/p
    T['Q'][:,8] = raw['Rc']/(4*p)
    T['Q'][:,10] = raw['Zdot']
    w,wp,R,Rp = raw['q'][:,7],raw['wp'],raw['shift'],raw['shiftprime']
    ratio = np.empty(len(w))
    ratio[0] = Rp[0]
    ratio[1:] = R[1:]*wp[1:]/w[1:]
    U = raw['q'][1,13]/w[1]**2
    T['Q'][:,11] = (-U-(3*H-HB-Rp)*p+p*ratio)/p
    return T

def crosses(raw,out,par):
    h = canonical.tensor_h(out['q'])
    hi = np.linalg.inv(h)
    V = out['q'][:,6:9]
    vol = out['blocks']['volume']
    c = np.einsum('ni,nij,nj->n',V,h,V)
    gh = []
    for i,j in canonical.HM:
        E = np.zeros((3,3));E[i,j]=E[j,i]=1
        gh.append(par['b']*vol*(c*np.einsum('nij,ji->n',hi,E)/2
            +np.einsum('ni,ij,nj->n',V,E,V)))
    gh = np.array(gh).T
    gv = 2*par['b']*vol[:,None]*np.einsum('nij,nj->ni',h,V)
    factor = raw['s']*raw['Zdot']
    field = np.zeros((len(V),10))
    field[:,:3],field[:,3:6] = gh[:,[0,1,3]],gv
    field *= factor[:,None]
    mean = np.mean(gh[:,[2,4,5]]*factor[:,None],axis=0)
    return field,mean

def project_force(F,raw):
    F=F.copy()
    for j in (7,9):F[:,j]-=np.mean(F[:,j])
    sine=np.sin(raw['theta'])
    F[:,4]-=sine*np.mean(sine*F[:,4])/np.mean(sine*sine)
    return F

def gradients(X,raw,par,ref,step):
    n=len(raw['q'])
    Hq=np.zeros((n,12));original=np.zeros((n,10))
    for kind in range(12):
        for j in range(n):
            Y=position_variation(X,raw,kind,j,step)
            Hq[j,kind]=n*np.imag(reduced(Y,raw,par,first_gradient=True)['H'])/step
            if kind<10:
                original[j,kind]=-n*np.imag(original_generator(Y,raw,par,ref))/step
    Hm=np.zeros(3);original_mean=np.zeros(3)
    for j in range(3):
        Y=position_variation(X,raw,'M',j,step)
        Hm[j]=np.imag(reduced(Y,raw,par,first_gradient=True)['H'])/step
        original_mean[j]=-np.imag(original_generator(Y,raw,par,ref))/step
    return Hq,Hm,original,original_mean

def exact_controls(ch):
    a,b,z,s,g,zd,sd,gd=sy.symbols('a b z s g zd sd gd')
    Hq,Hp,gq=sy.symbols('Hq Hp gq')
    ch.zero('presymplectic_energy_balance',Hq*Hp+Hp*(-Hq-s*gq*zd)
        +(-g*zd)*sd+(g*sd+s*gd)*zd-s*(gd-gq*Hp)*zd)
    # Linearized scalar curvature is a total divergence on the closed flat torus.
    xx,yy,zz=sy.symbols('delta_hxx_second delta_hyy_second delta_hzz_second')
    ch.zero('flat_planar_linear_Ricci',zz-(xx+yy+zz)+xx+yy)
    rad,phase,pR,pt,dR,dt=sy.symbols('rad phase pR ptheta dR dtheta',nonzero=True)
    u,v=rad*sy.cos(phase),rad*sy.sin(phase)
    pu,pv=pR*sy.cos(phase)-pt*sy.sin(phase)/rad,pR*sy.sin(phase)+pt*sy.cos(phase)/rad
    ch.zero('finite_polar_canonical_one_form',pu*(sy.diff(u,rad)*dR+sy.diff(u,phase)*dt)
        +pv*(sy.diff(v,rad)*dR+sy.diff(v,phase)*dt)-pR*dR-pt*dt)
    pmx,pmy,pl,dx,dy,dl=sy.symbols('pi_xz pi_yz pi_zz dmx dmy dL')
    ch.zero('mean_metric_canonical_factors',2*pmx*dx+2*pmy*dy+pl*dl
        -(2*pmx)*dx-(2*pmy)*dy-pl*dl)
    # Exact nonzero second variation for diag(exp(2a),exp(-2a),1).
    t=sy.symbols('z',real=True);f=sy.Function('a')(t)
    h=sy.diag(sy.exp(2*f),sy.exp(-2*f),1);hi=h.inv()
    dh=lambda i,j,k:sy.diff(h[j,k],t) if i==2 else 0
    G=[[[sy.simplify(sum(hi[k,l]*(dh(i,l,j)+dh(j,l,i)-dh(l,i,j))/2
        for l in range(3))) for j in range(3)] for i in range(3)] for k in range(3)]
    Ric=sy.zeros(3)
    for i in range(3):
        for j in range(3):
            Ric[i,j]=sum((sy.diff(G[k][i][j],t) if k==2 else 0)
                -(sy.diff(G[k][i][k],t) if j==2 else 0)
                +sum(G[k][k][l]*G[l][i][j]-G[k][j][l]*G[l][i][k]
                     for l in range(3)) for k in range(3))
    R=sy.simplify(sy.trace(hi*Ric))
    ch.zero('nonzero_curvature_second_variation',R+2*sy.diff(f,t)**2)
    ch.add('curvature_not_identically_absent',R!=0)
    return dict(two_form='Theta_other-g*s*dZ; includes -s*dg wedge dZ',
        momentum='Pdot=-H_Q-s*g_Q*Zdot; mean coordinates retain canonical factors',
        regulator='H_Z-g*sdot-s*gdot; gdot=g*(5H-2Hbg)/p on initial slice',
        first_variation_only='delta integral sqrt(h)*R3/s=0 at flat constant-lapse slice',
        retained_curvature_second_variation=str(R),
        node_energy='E0+Edust+divF+sqrt(h)*K_Q*s^2 at node; E0 includes -sqrt(h)*K_Q*s^2/2',
        temporal_scope='Initial first tangent only; no state evolution or full nodal hierarchy')

def grid_case(ch,n,offset,parmp,vals,H,U,Ud,shift):
    par={k:float(v) for k,v in parmp.items()}
    raw=lift.initial_lift(n,offset,parmp,vals,H,U,Ud,shift)
    initial=lift.restore_undivided(raw,par)
    X=chart(raw,initial);out=reduced(X,raw,par)
    ch.add('flat_constant_lapse_first_variation_domain',
        np.array_equal(canonical.tensor_h(raw['q']),np.broadcast_to(np.eye(3),(n,3,3)))
        and np.max(abs(raw['s']-raw['s'][0]))==0)
    ch.small('chart_roundtrip',np.max(abs(out['p'][:,:12]-initial['p'][:,:12])/(1+abs(initial['p'][:,:12]))),'1e-8')
    ch.add('both_node_orientation_controls',out['q'][0,7]==0 and out['g'][0]==0)
    ref=reference_context(raw,out,Ud)
    cross,mcross=crosses(raw,out,par)
    all_steps=[];previous=None
    for step in STEPS:
        Hq,Hm,Fref,Mref=gradients(X,raw,par,ref,step)
        force=project_force(-Hq[:,:10]-cross,raw);mforce=-Hm-mcross
        referr=max(np.max(abs(force-Fref)/(1+abs(force)+abs(Fref))),
                   np.max(abs(mforce-Mref)/(1+abs(mforce)+abs(Mref))))
        ch.small('original_full_generator_'+repr(step),referr,'1e-7')
        currents={}
        for name,j,pj in (('phase',7,out['q'][:,9]*out['p'][:,10]),('dust',9,out['p'][:,14])):
            want=raw['D']@(raw['shift']*pj)/raw['rate']
            error=float(np.max(abs(force[:,j]-want)))
            amplitude=float(np.max(abs(want)))
            if amplitude==0:raise ValueError('unexpected zero current control')
            rel=error/amplitude
            ch.small(name+'_original_current_'+repr(step),rel,'1e-4')
            currents[name]=dict(max_absolute_error=repr(error),current_amplitude=repr(amplitude),relative_error=repr(rel))
        T=initial_tangent(X,raw);T['P']=force;T['PM']=mforce
        gdot=out['g']*(5*raw['H']-2*raw['HB'])/raw['rate']
        residual=Hq[:,10]-out['g']*T['Q'][:,11]-raw['s']*gdot
        scale=par['b']*(1/500)**2*(1+np.max(abs(T['Q'][:,11]))+abs(5*raw['H']-2*raw['HB']))
        regulator=float(np.max(abs(residual)))/scale
        Y={k:X[k].astype(complex)+1j*step*T[k] for k in X}
        tangent_out=reduced(Y,raw,par,tau=1j*step)
        s=Y['Q'][:,11]
        CE=tangent_out['E'][0]+tangent_out['divF'][0]+tangent_out['blocks']['volume'][0]*par['K_Q']*s[0]**2
        chi=tangent_out['q'][0,13]+s[0]*np.trace(tangent_out['DV'][0])
        CE_dot=float(np.imag(CE)/step);chi_dot=float(np.imag(chi)/step)
        CE_scale=par['K_Q']*raw['rate']*max(abs(raw['H']),float(np.max(abs(T['Q'][:,11]))))
        CE_relative=abs(CE_dot)/CE_scale
        directional=(np.mean(np.sum(Hq*T['Q'],axis=1)+np.sum(T['Q'][:,:10]*force,axis=1))
                     +np.sum(Hm*T['M'])+np.sum(T['M']*mforce))
        clock_Y=copy_chart(X)
        Htau=float(np.imag(reduced(clock_Y,raw,par,tau=1j*step)['H'])/step)
        Htau_expected=par['beta']*raw['Qdust']/raw['rate']
        ch.small('explicit_clock_matter_rate_'+repr(step),abs(Htau-Htau_expected)/(1+abs(Htau_expected)),'1e-7')
        actual_energy_rate=float(np.imag(tangent_out['H'])/step)
        chain_error=abs(actual_energy_rate-directional-Htau)/(1+abs(actual_energy_rate)+abs(Htau))
        ch.small('full_directional_energy_chain_rule_'+repr(step),chain_error,'1e-7')
        initialCE=out['E'][0]+out['divF'][0]+out['blocks']['volume'][0]*par['K_Q']*raw['rate']**2
        record=dict(step=repr(step),reference_generator_error=repr(float(referr)),currents=currents,
            full_regulator_row_max=repr(float(np.max(abs(residual)))),regulator_reference_scaled=repr(regulator),
            node_CE_initial=repr(float(initialCE)),node_CE_dot=repr(CE_dot),node_CE_dot_scale=repr(CE_scale),
            node_CE_dot_relative=repr(CE_relative),node_chi_dot=repr(chi_dot),
            energy_directional_defect=repr(float(directional)),H_tau=repr(Htau),H_tau_expected=repr(Htau_expected),
            actual_energy_rate=repr(actual_energy_rate),energy_chain_error=repr(float(chain_error)),
            node_tangency_disposition='SAMPLED_FIRST_TANGENT_CONSISTENT' if CE_relative<=1e-4 and abs(chi_dot)<=1e-8 else 'WARNING_NODE_FIRST_TANGENCY_UNRESOLVED',
            full_regulator_disposition='SAMPLED_ROW_CONSISTENT' if regulator<=1e-4 else 'WARNING_FULL_REGULATOR_ROW_UNRESOLVED')
        if previous is not None:
            fdiff=max(float(np.max(abs(force-previous[0])/(1+abs(force)+abs(previous[0])))),
                      float(np.max(abs(mforce-previous[1])/(1+abs(mforce)+abs(previous[1])))))
            ch.small('two_step_force_agreement',fdiff,'1e-10')
            ddiff=abs(CE_dot-previous[2])/(CE_scale+abs(CE_dot)+abs(previous[2]))
            ch.small('two_step_tangency_derivative_agreement',ddiff,'1e-7')
            record['two_step_force_discrepancy']=repr(fdiff)
            record['two_step_tangency_discrepancy']=repr(ddiff)
        previous=(force.copy(),mforce.copy(),CE_dot)
        all_steps.append(record)
    crossmax=max(float(np.max(abs(project_force(cross,raw)))),float(np.max(abs(mcross))))
    ch.add('nonzero_omitted_metric_frame_cross',crossmax>0,repr(crossmax))
    # This algebraic magnitude is recorded, not claimed resolved if below roundoff.
    return dict(grid=n,node_orientation=offset,steps=all_steps,
        maximum_cross_force=repr(crossmax),cross_above_binary64_relative_floor=bool(crossmax>np.finfo(float).eps*(1+np.max(abs(force)))),
        initial_momenta={name:[repr(float(v)) for v in force[:,j]] for j,name in enumerate(NAMES[:10])},
        mean_momentum_rates=[repr(float(v)) for v in mforce],
        full_admission=False,state_adopted_or_evolved=False)

def case_job(task):
    index,point,initial=task
    mp.mp.dps=100;mp.iv.dps=80
    ch=base.Checks();records=[]
    try:
        par,vals,H,U,Ud,g8,g12=lift.setup(point,initial)
        error=max(abs(a-b)/(1+abs(a)+abs(b)) for t in (0,mp.pi/7,mp.pi/2)
                  for a,b in zip(g8(t),g12(t)))
        ch.small('original_8_12_shift_control',error,'1e-30')
        for n in (17,25,33):
            for offset in (0,1):
                local=base.Checks()
                records.append(grid_case(local,n,offset,par,vals,H,U,Ud,g12))
                nodal.reg.joint.merge_checks(ch,local.rows,f'{n}_{offset}_')
    except Exception:
        ch.add('unexpected_case_exception',False,traceback.format_exc())
    return index,dict(family=point['family'],eta=point['eta'],controls=records),ch.rows

def calculate(workers):
    pins,before=sources();ch=base.Checks();form=exact_controls(ch)
    points=lift.READ(nodal.reg.JOINT+'independent.json');initial=lift.READ(lift.cop.CERTS)
    if len(points)!=9 or len(initial)!=9 or any(a['family']!=b['family'] or a['eta']!=b['eta'] for a,b in zip(points,initial)):
        raise ValueError('input count/order')
    tasks=[(i,a,b) for i,(a,b) in enumerate(zip(points,initial))];out={}
    progress('momentum_tangency_cases',cases=9,workers=min(workers,9))
    if workers==1:
        for task in tasks:
            result=case_job(task);out[result[0]]=result;progress('case_complete',index=result[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn')) as pool:
            jobs={pool.submit(case_job,task):task[0] for task in tasks}
            for future in as_completed(jobs):
                result=future.result()
                if result[0]!=jobs[future] or result[0] in out:raise ValueError('case identity')
                out[result[0]]=result;progress('case_complete',index=result[0])
    records=[]
    for i in range(9):
        _,record,rows=out[i];records.append(record)
        nodal.reg.joint.merge_checks(ch,rows,record['family']+'_'+record['eta']+'_')
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    all_steps=[s for r in records for g in r['controls'] for s in g['steps']]
    complete=len(all_steps)==108
    nodes=complete and all(s['node_tangency_disposition']=='SAMPLED_FIRST_TANGENT_CONSISTENT' for s in all_steps)
    regulator=complete and all(s['full_regulator_disposition']=='SAMPLED_ROW_CONSISTENT' for s in all_steps)
    passed=sum(row['passed'] for row in ch.rows)
    summary=dict(validation='PASS_INITIAL_MOMENTUM_IMPLEMENTATION_ONLY' if passed==len(ch.rows) and complete else 'FAIL_OR_UNRESOLVED_INITIAL_MOMENTUM_IMPLEMENTATION',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        sampled_first_node_tangency=bool(nodes),sampled_full_regulator_row=bool(regulator),
        status='INITIAL_MOMENTUM_CALCULATED_NODE_PRESERVATION_'+('SAMPLED_CONSISTENT' if nodes and regulator else 'UNRESOLVED'),
        full_nodal_hierarchy_verified=False,full_initial_admission=False,physical_spectrum_computed=False,
        physical_frequency_window_established=False,state_adopted_or_evolved=False,
        stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    return {'summary.json':summary,'formulas.json':form,'independent.json':records}

def main():
    global _PROGRESS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output');parser.add_argument('--replay')
    parser.add_argument('--workers',type=int,default=16);parser.add_argument('--progress-log')
    args=parser.parse_args()
    if bool(args.output)==bool(args.replay):parser.error('choose output or replay')
    if args.progress_log:
        _PROGRESS=(ROOT/args.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific output root')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    metadata=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:metadata(f) for f in dest.iterdir()} if args.replay else None
    data=calculate(nodal.v4.selected_workers(args.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode()
    if args.replay:
        if set(before)!=set(payload):raise ValueError('replay set drift')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or metadata(f)!=before[name]:raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    summary=data['summary.json']
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','sampled_first_node_tangency','sampled_full_regulator_row')}),flush=True)
    return 0 if summary['passed']==summary['total'] else 1

if __name__=='__main__':raise SystemExit(main())
