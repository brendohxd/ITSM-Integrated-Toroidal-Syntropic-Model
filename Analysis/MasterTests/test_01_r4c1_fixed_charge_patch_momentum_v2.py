"""Constrained fixed-charge instantaneous momentum form, not physical modes."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib, importlib.util, json, multiprocessing
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT = 'Analysis/MasterTests/test_01_r4c1_regulator_acceleration_regularity_v1.py'
PSHA = 'd5c17a544394aa3d46b51ef467fe9d1ddfbc650bb07feb63d4467d0adc2b502a'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_PATCH_MOMENTUM_V1_CONTRACT_2026-10-19.md'
SHA = lambda raw: hashlib.sha256(raw).hexdigest()
ENC = lambda obj: (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)+chr(10)).encode()
READ = lambda name: json.loads((ROOT/name).read_bytes())
if SHA((ROOT/PARENT).read_bytes()) != PSHA:
    raise ValueError('parent drift before import')
spec = importlib.util.spec_from_file_location('frozen_regulator_density', ROOT/PARENT)
reg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reg)
joint, cop, canonical, base, v4 = reg.joint, reg.cop, reg.canonical, reg.base, reg.v4
iv = mp.iv
PINS = dict(reg.PINS)
PINS.update({
    PARENT: PSHA,
    'Analysis/MasterTests/test_01_r4c1_fixed_charge_patch_momentum_v1.py':
        'e8e8837e6c70b6f8cb8db2a1daefca0054b2da9e95a0aaf189edf348e6b6c661',
    'Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_PATCH_MOMENTUM_V2_TYPE_ADDENDUM_2026-10-19.md':
        '90ab0c2ffa684c459af1a66c14e95e02e7c7805481eae2d7e34c2019c31d1d5e',
    CONTRACT: '0f10ec33f71edfc11965286a08a96feb317b00e813716cbfae246856826baf09',
    'Theory/Gates/RES-001/RES001_R4C1_REGULATOR_ACCELERATION_REGULARITY_V1_REPORT_2026-10-19.md':
        'fb0e6a0af5ce70e4fb5bc34541dd99fa4274f44b915c3070097745e81566105f',
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V3_REPORT_2026-10-16.md':
        'a5acbb6d2f659f9c2e4719f32f91ef9f8a4c2cc2c9bdd1fff8635d46fc1199c3'})
_PROGRESS = None
def progress(stage, **kw):
    line = json.dumps(dict(stage=stage, **kw), sort_keys=True)
    print(line, flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a', encoding='utf-8') as f: f.write(line+chr(10))

def sources():
    pins = {**PINS, SELF: SHA((ROOT/SELF).read_bytes())}
    meta = {}
    for name, digest in pins.items():
        p = ROOT/name
        side = Path(str(p)+'.sha256')
        if SHA(p.read_bytes()) != digest or side.read_text().split()[0].lower() != digest:
            raise ValueError('source/sidecar drift '+name)
        for q in (p, side):
            raw = q.read_bytes()
            meta[q.relative_to(ROOT).as_posix()] = dict(
                sha256=SHA(raw), bytes=len(raw), mtime_ns=q.stat().st_mtime_ns)
    return pins, meta

def build(ch):
    # Reuse only pure, pinned action/coefficient utilities; do not rerun old audits.
    jp, _ = joint.build(ch)
    names = 'MP2 MU2 c1 c2 c3 c4 K_Q A b zeta Rc U w wp'
    u = {n: s.Symbol(n, real=True) for n in names.split()}
    p = s.Symbol('p', positive=True)
    MP, mu, c1, c2, c3, c4, Kq, A, b, ze, Rc, U, w, wp = [u[n] for n in names.split()]
    kk = s.symbols('Kxx Kxy Kxz Kyy Kyz Kzz', real=True)
    xx = s.Matrix(s.symbols('Xx Xy Xz', real=True))
    cart = s.symbols('u_hat v_hat r_hat', real=True)
    y = list(kk)+list(xx)+list(cart)
    KM = s.Matrix([[kk[0],kk[1],kk[2]],[kk[1],kk[3],kk[4]],[kk[2],kk[4],kk[5]]])
    DV = s.zeros(3); DV[2,1] = wp
    frame, BB = v4.frame_body(s.eye(3), KM, xx, s.Matrix([0,w,0]), DV, mu,c1,c2,c3,c4)
    acc = BB.T*s.Matrix([s.sqrt(1+w*w),0,w,0])
    lag = MP*(s.trace(KM*KM)-s.trace(KM)**2)/2+frame
    lag += (sum(v*v for v in cart)-ze*Rc*Rc*w*w*cart[1]**2)/2
    lag += Kq*(1+w*w)*p*p/2-A*p**3*s.Abs(w)**3
    lag += b*U**2*w**4/2-b*U*w*w*acc[0]*p
    R = s.Matrix(12,12,lambda i,j: base.CLEAN(s.diff(lag,y[i],y[j])))
    mix = s.Matrix([base.CLEAN(s.diff(lag,v,p)) for v in y])
    want = s.zeros(12,1); want[3] = -2*b*U*w**4; want[7] = -b*U*w**3
    ch.zero('original_full_complement_scalar_mixing', mix-want)
    ch.add('R_independent_scalar_velocity_spatial_jet_regulator', not any(
        e.has(p,wp,U,A,b) for e in R))
    ch.zero('radial_canonical_block', R[:,9]-s.eye(12)[:,9])
    DT = MP-mu*(c1+c3); D = MP+mu*c2; M = (3*D-DT)/2
    R0i = s.zeros(12)
    for i in (0,3,5):
        for j in (0,3,5):
            R0i[i,j] = (1 if i==j else 0)/DT-D/(2*M*DT)
    for i in (1,2,4): R0i[i,i] = 1/(2*DT)
    for i in (6,7,8): R0i[i,i] = 1/(mu*(c1+c4))
    for i in (9,10,11): R0i[i,i] = 1
    ch.zero('exact_nodal_complement_inverse', R.subs(w,0)*R0i-s.eye(12))
    # Keep the orientation from the canonical action, not a guessed clock sign.
    t, cc = s.symbols('s c', positive=True)
    W,L,D2,hY,f1,f2,mixsq,Zh = s.symbols('W L D2 hY f1 f2 mixsq Zhat', real=True)
    Hp = (W+L*t+D2*t*t+A*cc**s.Rational(3,2)*t**3)/t
    pp = hY+f1+2*f2*t-3*A*cc**s.Rational(3,2)*t*t-b*cc*Zh
    lrule = -hY-t*mixsq-f1
    drule = mixsq/2-f2
    wshell = s.expand(-pp*t-lrule*t-drule*t*t-A*cc**s.Rational(3,2)*t**3)
    on_shell = s.diff(Hp,t,2).subs(W,wshell)
    B = (2*f2-mixsq)/t-6*A*cc**s.Rational(3,2)-2*b*cc*Zh/t**2
    ch.zero('clock_Hamiltonian_minus_s_s_on_shell', on_shell+B)
    ch.zero('nonzero_off_shell_lapse_witness', s.diff(Hp,t,2)+B-2*(W-wshell)/t**3)
    ch.add('on_shell_replacement_not_off_shell_identity', s.diff(Hp,t,2)+B != 0)
    flux,shift,Zprime = s.symbols('flux Rshift Zprime', real=True)
    ch.zero('retained_lapse_flux_clock_curvature',s.diff(flux/t,t,2)-2*flux/t**3)
    ch.add('reject_deleting_local_lapse_flux',s.diff(flux/t,t,2)!=0)
    ch.zero('retained_regulator_shift_drift',
        B.subs(Zh,Zh-shift*Zprime)-B-2*b*cc*shift*Zprime/t**2)
    ch.add('reject_dropping_regulator_drift',2*b*cc*shift*Zprime/t**2!=0)
    d, zz, FF, chi, ur, vv = s.symbols('d Zprime Fprime chi u v', real=True)
    ch.zero('original_longitudinal_constraint_compensation', -FF+(FF/zz)*zz)
    ch.add('reject_missing_metric_momentum_compensation', FF/zz*zz != 0)
    ch.zero('phase_charge_fixed_v_zero', (-vv*chi).subs(vv,0))
    ch.zero('nonzero_mode_spatial_gauge_determinant', s.det(s.diag(d,d,2*d))-2*d**3)
    ch.add('zero_mode_gauge_not_inverted', s.det(s.diag(d,d,2*d)).subs(d,0)==0)
    # Young: B0*x^2-D0*x*y-A0*y^2 >= B0*x^2/2-(A0+D0^2/(2B0))*y^2.
    B0 = s.Symbol('B0', positive=True)
    a0,d0,xx0,yy0 = s.symbols('a0 d0 x y', real=True)
    diff = B0*xx0**2-d0*xx0*yy0-a0*yy0**2-(
        B0*xx0**2/2-(a0+d0*d0/(2*B0))*yy0**2)
    ch.zero('exact_Young_remainder_square', diff-(B0*xx0-d0*yy0)**2/(2*B0))
    return dict(R=list(R),R0i=list(R0i),mix=list(mix),velocity=jp['velocity']), dict(
        clock='psi=tau after variation; N=1/s>0; Hpsi=-p_psi=+(E0+p_T+flux)/s',
        dust_time_not_fixed=True,
        complement='R full 12x12 from original action; ell(s)=ell0+s*h',
        lapse_flux='partial_i(gamma*p_V^i) retained, unchanged under these momentum variations',
        minus_Hss='B=[K_Q*(1+w^2)-h^T R^-1*h]/p-6*A*abs(w)^3-2*b*w^2*Zhat/p^2',
        regulator_drift='Zhat=Ud*w^2-Rshift*Z_z; Ud is not U_dot',
        force_regulator_momentum='p_Z=-b*w^2*s on psi_i=0',
        constraint_curve='delta p_Z=Fprime/Z_z, delta pi_zz=F/2, all configurations/p_V/p_T/p_v fixed; solve p_psi from true H_perp',
        charges='Qdust and Q_U1 fixed exactly; p_u direction is radial at v=0',
        symplectic_pullback='delta psi=delta h_iz=0; solved p_psi and pi_iz drop from canonical one-form; remaining p_Z dZ and p_u du persist',
        negative_F_form='-Q_F=-(Rinv)_zzzz*F^2/p+2*[Rinv(P-ell0)]_zz*F*delta_s/p^2+B*delta_s^2',
        positive_radial_form='Q_u=int chi^2/p; mixed F/chi term zero at u_hat=0',
        sufficient_patch_ratio='a^4*[9*N_R*b^2*Uu^2*k^2/(8*p*Bmin)+27*b^2*Y^2*Uu^4*k^2/(p^4*Ul^2*Bmin^2)]',
        patch_poincare='36*k^2 on interval length pi/(6*k); compact supports avoid nodes',
        classification='Instantaneous constrained fixed-charge planar momentum inertia only; not physical ghost/mode/cutoff or arbitrary3D closure')

_EX = None
_FN = None
def initialize(pack):
    global _EX,_FN
    mp.mp.dps=110; iv.dps=80
    _EX={k:base.Eval(v) for k,v in pack.items()}
    checks=base.Checks(); _,_FN,_=cop.symbolic(checks)
    if not all(r['passed'] for r in checks.rows): raise ValueError('coefficient utility failure')

def maxupper(values):
    return base.point(max(base.hi(abs(iv.mpf(v))) for v in values))

def independent(ch, par, point, eta):
    p=mp.mpf(eta.p)/(5*eta.q); e=mp.mpf(1)/500
    H,U,Ud=[mp.mpf(point[k]) for k in ('H','U','Ud')]
    Rc=mp.sqrt(mp.mpf(eta.p)/eta.q)
    errors=[]; hessian_errors=[]; observations=[]
    for sign in (-1,1):
        w=sign*e*mp.cos(mp.pi/7); wp=-sign*e*40*mp.sin(mp.pi/7)
        c=w*w; zh=Ud*c
        # Independent coordinate density: nonzero shift and Z_z retained.
        def body(y,ss,zhat):
            adjusted_Ud=zhat/c+(mp.mpf(3)/41)*2*U*wp/w
            return reg.coordinate_body(y,ss,par,w,wp,U,adjusted_Ud,Rc)
        zero=mp.zeros(12,1); basis=[mp.matrix([int(i==j) for i in range(12)]) for j in range(12)]
        fn=lambda y,ss:body(y,ss,0)
        f=lambda ss:fn(zero,ss)
        ell=lambda ss:mp.matrix([(fn(v,ss)-fn(-v,ss))/2 for v in basis])
        fi=[fn(v,p) for v in basis]; f0=f(p)
        RR=mp.matrix([[fn(basis[i]+basis[j],p)-fi[i]-fi[j]+f0 for j in range(12)] for i in range(12)])
        Rinv=RR**-1
        values=dict(par,Rc=Rc,U=U,w=w,wp=wp,p=p)
        pred=_EX['R'].numeric(values); hh=mp.matrix(_EX['mix'].numeric(values))
        errors += [abs(RR[i,j]-pred[12*i+j])/(1+abs(RR[i,j])+abs(pred[12*i+j])) for i in range(12) for j in range(12)]
        ell0=ell(0); ellp=ell(p)
        errors += [abs(ellp[i]-ell0[i]-hh[i]*p)/(1+abs(ellp[i])) for i in range(12)]
        y=mp.matrix([H,0,0,H,0,H,0,-mp.mpf(point['H'])*w,0,0,Rc,Rc/4])
        PY=RR*y+ellp
        ppsi=mp.diff(lambda ss:body(y,ss,zh),p)
        pZ=mp.diff(lambda z:body(y,p,z),zh)
        errors.append(abs(pZ+par['b']*c*p)/(1+abs(pZ)))
        direct=(PY.T*y)[0]+ppsi*p+pZ*zh-body(y,p,zh)
        E0=((PY-ellp).T*Rinv*(PY-ellp))[0]/2-f(p)
        errors.append(abs(direct-E0-ppsi*p)/(1+abs(direct)))
        flux=mp.mpf(1)/997  # A nonzero local first-jet control, NOT a profile replacement.
        rho=-direct-flux
        ch.add('positive_control_dust_'+str(sign),rho>0,base.SHOW(rho))
        def Hclock(a,z):
            ss=-(pZ+z)/(par['b']*c)
            P=mp.matrix(PY); P[9]+=a
            ee=ell(ss); E=((P-ee).T*Rinv*(P-ee))[0]/2-f(ss)
            return (E+rho+flux)/ss
        err0=abs(Hclock(0,0)+ppsi)/(1+abs(ppsi))
        radial=mp.diff(lambda a:Hclock(a,0),0,2)
        zz=mp.diff(lambda z:Hclock(0,z),0,2)
        az=mp.diff(lambda a:mp.diff(lambda z:Hclock(a,z),0),0)
        B=(par['K_Q']*(1+c)-(hh.T*Rinv*hh)[0])/p-6*par['A']*abs(w)**3-2*par['b']*c*zh/p**2
        expected=-B/(par['b']*c)**2
        hessian_errors += [err0,abs(radial-1/p)/(1+abs(radial)+1/p),
            abs(zz-expected)/(1+abs(zz)+abs(expected)),abs(az)/(1+abs(zz)+abs(radial))]
        observations.append(dict(sign=sign,radial_entry=base.SHOW(radial),regulator_entry=base.SHOW(zz),
            cross_entry=base.SHOW(az),control_dust=base.SHOW(rho),minus_clock_s_s=base.SHOW(B)))
    ch.small('original_coordinate_all_R_affine_momenta_Legendre',max(errors),'1e-45')
    ch.small('independent_original_coordinate_clock_Hessian',max(hessian_errors),'1e-45')
    return dict(matrix_energy_error=base.SHOW(max(errors)),Hessian_error=base.SHOW(max(hessian_errors)),points=observations,
        interpretation='Approximate independent original-density first-jet controls; not new admitted/evolved states.')

def case_job(task):
    index,cert,point,initial=task; ch=base.Checks()
    c=cop.make_case(initial,_FN); v=c['values']
    H,U=cop.unpack(cert['H_bracket']),cop.unpack(cert['U_bracket'])
    node=cop.state(c,H,U,iv.mpf(0),iv.mpf(1),_FN)
    Ud=_EX['velocity'].interval(node)[0]
    state=cop.state(c,H,U,iv.mpf([0,1]),iv.mpf([0,1]),_FN)
    a=base.point(base.hi(v['alpha'])); e=base.point(base.hi(v['eeabs']))
    vals=dict(v,U=U,w=iv.mpf([-base.hi(e),base.hi(e)]),wp=iv.mpf(0))
    RR=_EX['R'].interval(vals); I=_EX['R0i'].interval(vals); hh=_EX['mix'].interval(vals)
    Rzero=_EX['R'].interval(dict(vals,w=iv.mpf(0)))
    norm0=maxupper([sum(abs(I[12*i+j]) for j in range(12)) for i in range(12)])
    Delta=[RR[k]-Rzero[k] for k in range(144)]
    relative=[sum(I[12*i+k]*Delta[12*k+j] for k in range(12)) for i in range(12) for j in range(12)]
    q=maxupper([sum(abs(relative[12*i+j]) for j in range(12)) for i in range(12)])
    ch.add('uniform_full_complement_Neumann_regular',base.hi(q)<1,base.pack(q),'q<1 over all signed amplitudes')
    if base.hi(q)>=1: raise ValueError('Neumann bound unresolved')
    norm=norm0/(1-q); hm=maxupper(hh); h1=sum(abs(t) for t in hh)
    mixbound=norm*hm*h1
    # Rshift=a*rs, Z_z=-2*U*k*a*C*S. Keep the drift, including its sign.
    Zhat=Ud*v['alpha']*iv.mpf([0,1])+2*U*v['k']*v['alpha']**2*state['rs']*iv.mpf([0,1])
    B=v['K_Q']*(1+iv.mpf([0,base.hi(a)]))/v['p']+base.box(mixbound)/v['p']
    B-=6*v['A']*iv.mpf([0,base.hi(e**3)])+2*v['b']*iv.mpf([0,base.hi(a)])*Zhat/v['p']**2
    ch.add('negative_clock_s_s_uniform',base.lo(B)>0,base.pack(B),'B=-Hss>0; not a ghost classification')
    if base.lo(B)<=0: raise ValueError('clock curvature sign unresolved')
    Bmin=base.point(base.lo(B)); Ul=base.point(base.lo(U)); Uu=base.point(base.hi(U))
    Y=maxupper([H])+a*maxupper([state['qs']])+v['p']*norm*hm
    threshold=a**4*(9*norm*v['b']**2*Uu**2*v['k']**2/(8*v['p']*Bmin)
        +27*v['b']**2*Y**2*Uu**4*v['k']**2/(v['p']**4*Ul**2*Bmin**2))
    gap=36*v['k']**2-threshold
    ch.add('original_patch_negative_F_direction',base.lo(gap)>0,base.pack(gap),'Poincare 36*k^2 exceeds Young threshold')
    ch.add('fixed_charge_radial_positive',base.lo(1/v['p'])>0,base.pack(1/v['p']))
    par=canonical.parameters(cert['family'],cert['eta'],'mp')
    control=independent(ch,par,point,s.Rational(cert['eta']))
    return index,dict(family=cert['family'],eta=cert['eta'],Neumann_q=base.pack(q),
        inverse_norm_bound=base.pack(norm),minus_clock_s_s=base.pack(B),full_regulator_proper_velocity=base.pack(Zhat),
        compensated_metric_velocity_bound=base.pack(Y),Young_ratio_threshold=base.pack(threshold),
        Poincare_gap=base.pack(gap),status='OPPOSITE_CONSTRAINED_FIXED_CHARGE_MOMENTUM_SIGNS_ON_REGULAR_PATCH',
        full_physical_Hessian=False,physical_ghost_classified=False,below_cutoff_instability_proved=False),control,ch.rows

def calculate(workers):
    mp.mp.dps=110; iv.dps=80
    pins,before=sources(); ch=base.Checks(); pack,form=build(ch)
    if not all(r['passed'] for r in ch.rows): raise ValueError('exact identity failure '+repr([r for r in ch.rows if not r['passed']]))
    certs=READ(reg.JOINT+'certificates.json'); points=READ(reg.JOINT+'independent.json'); initial=READ(cop.CERTS)
    if not (len(certs)==len(points)==len(initial)==9): raise ValueError('case count')
    tasks=[(i,a,b,c) for i,(a,b,c) in enumerate(zip(certs,points,initial))]
    results={}; progress('fixed_charge_patch_cases',workers=min(workers,9),cases=9)
    if workers==1:
        initialize(pack)
        for task in tasks:
            rr=case_job(task); results[rr[0]]=rr; progress('patch_case_complete',index=rr[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn'),
                initializer=initialize,initargs=(pack,)) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for future in as_completed(jobs):
                rr=future.result()
                if rr[0]!=jobs[future] or rr[0] in results: raise ValueError('case identity')
                results[rr[0]]=rr; progress('patch_case_complete',index=rr[0])
    records=[]; controls=[]
    for i in range(9):
        _,record,control,rows=results[i]; records.append(record); controls.append(control)
        joint.merge_checks(ch,rows,record['family']+'_'+record['eta']+'_')
    _,after=sources(); ch.add('source_sidecar_bytes_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_CONSTRAINED_PATCH_MOMENTUM_ONLY' if passed==len(ch.rows) else 'FAIL_OR_UNRESOLVED_PATCH_MOMENTUM',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='INDEFINITE_FIXED_CHARGE_PATCH_MOMENTUM_FORM_PHYSICAL_MODES_WINDOW_OPEN',
        full_initial_admission=False,state_adopted_or_evolved=False,arbitrary3D_constraint_closure_proved=False,
        physical_ghost_classified=False,physical_frequency_window_established=False,action_no_go=False,
        stage2_complete=False,stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    return {'summary.json':summary,'formulas.json':form,'certificates.json':records,'independent.json':controls}

def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output'); p.add_argument('--replay'); p.add_argument('--workers',type=int,default=16)
    p.add_argument('--progress-log'); a=p.parse_args()
    if bool(a.output)==bool(a.replay): p.error('choose output or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'): raise ValueError('progress outside ignored root')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'): pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'): raise ValueError('outside scientific output root')
    if a.output: dest.mkdir(parents=True,exist_ok=False)
    meta=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    before={f.name:meta(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(v4.selected_workers(a.workers)); payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()): payload[name+'.sha256']=(SHA(raw)+'  '+name+chr(10)).encode()
    if a.replay:
        if set(before)!=set(payload): raise ValueError('replay set changed')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or meta(f)!=before[name]: raise ValueError('replay bytes/metadata drift '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f: f.write(raw)
    su=data['summary.json']
    print(json.dumps({k:su[k] for k in ('validation','passed','total','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1
if __name__=='__main__': raise SystemExit(main())
