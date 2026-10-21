"""Original-action coupled cusp contribution to regulator acceleration at a node."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib,importlib.util,json,multiprocessing
from pathlib import Path
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v2.py'
PSHA='e10bf2f7b20e871cd93fd10b00f1ed6f43f648f60b9282e15205e277d29e3d3d'
CAN='Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py'
CSHA='4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_REGULATOR_ACCELERATION_REGULARITY_V1_CONTRACT_2026-10-19.md'
JOINT='Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda name:json.loads((ROOT/name).read_bytes())
def module(path,digest,name):
    if SHA((ROOT/path).read_bytes())!=digest:raise ValueError('source drift before import '+path)
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out
joint=module(PARENT,PSHA,'frozen_joint_profile')
canonical=module(CAN,CSHA,'frozen_original_coordinate_density')
base=joint.base;cop=joint.cop;v4=joint.parent;iv=mp.iv
PINS=dict(joint.PINS)
PINS.update({PARENT:PSHA,CAN:CSHA,CONTRACT:'59462dfb66d34db504ccf152addffcbbfbc8afa8ba58618f982bf8961ece2b06',
 JOINT+'summary.json':'f1d662d6d9a44eb03df285a541950b0886119c7fc02223408f73855725e7e6f9',
 JOINT+'certificates.json':'76b4870fda66c9a85c85dcc282d4934a8ac09337a81c469d3a152f89511963cf',
 JOINT+'independent.json':'b399814e46e660b7ad52ef03f5c2e4ce262c5e3f815162ad3f9f35be47d0459e',
 'Theory/Gates/RES-001/RES001_R4C1_JOINT_NODE_VELOCITY_V2_REPORT_2026-10-19.md':'55c4f55a51cec51f5c9b0e731165c47546bed1daa1f8b7a06167af3ef99e51ea'})
_PROGRESS=None
def progress(stage,**kw):
    line=json.dumps(dict(stage=stage,**kw),sort_keys=True);print(line,flush=True)
    if _PROGRESS:
        with _PROGRESS.open('a',encoding='utf-8') as f:f.write(line+'\n')
def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,digest in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest or sc.read_text().split()[0].lower()!=digest:raise ValueError('source/sidecar drift '+name)
        for q in (p,sc):
            raw=q.read_bytes();meta[q.relative_to(ROOT).as_posix()]=dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=q.stat().st_mtime_ns)
    return pins,meta
def build(ch):
    names='MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 U w wp R q Zhat'
    u={n:s.Symbol(n,real=True) for n in names.split()};p=s.Symbol('p',positive=True);u['p']=p
    MP,mu,c1,c2,c3,c4,Kq,A,b,be,ze,Rc,H,HB,U,w,wp,R,q,zh=[u[n] for n in names.split()]
    kk=s.symbols('Kxx Kxy Kxz Kyy Kyz Kzz',real=True);xx=s.Matrix(s.symbols('Xx Xy Xz',real=True))
    cart=s.symbols('u_hat v_hat r_hat',real=True);y=list(kk)+list(xx)+list(cart)
    KM=s.Matrix([[kk[0],kk[1],kk[2]],[kk[1],kk[3],kk[4]],[kk[2],kk[4],kk[5]]])
    DV=s.zeros(3);DV[2,1]=wp
    frame,B=v4.frame_body(s.eye(3),KM,xx,s.Matrix([0,w,0]),DV,mu,c1,c2,c3,c4)
    gam=s.sqrt(1+w*w);acc=B.T*s.Matrix([gam,0,w,0])
    reg=b*U**2*w**4/2-b*zh*w*w*p-b*U*w*w*acc[0]*p
    lag=MP*(s.trace(KM*KM)-s.trace(KM)**2)/2+frame\
        +(sum(v*v for v in cart)-ze*Rc*Rc*w*w*cart[1]**2)/2\
        +Kq*(1+w*w)*p*p/2-A*p**3*s.Abs(w)**3+reg
    Rmat=s.Matrix(12,12,lambda i,j:base.CLEAN(s.diff(lag,y[i],y[j])))
    mix=s.Matrix([base.CLEAN(s.diff(lag,v,p)) for v in y])
    hz=s.Matrix([s.diff(lag,v,zh) for v in y])
    ch.zero('no_complement_regulator_velocity_mixing',hz)
    ch.zero('scalar_regulator_temporal_coefficient',s.diff(lag,p,zh)+b*w*w)
    expected=s.zeros(12,1);expected[3]=-2*b*U*w**4;expected[7]=-b*U*w**3
    ch.zero('exact_scalar_complement_mixing',mix-expected)
    DT=MP-mu*(c1+c3);M=MP+mu*(c1+3*c2+c3)/2
    zero=Rmat.subs(w,0);target=s.zeros(12)
    diag=(0,3,5)
    for i in diag:
        for j in diag:target[i,j]=(DT if i==j else 0)-(MP+mu*c2)
    for i in (1,2,4):target[i,i]=2*DT
    for i in (6,7,8):target[i,i]=mu*(c1+c4)
    for i in (9,10,11):target[i,i]=1
    ch.zero('original_full_nodal_complement_matrix',zero-target)
    determinant=-16*M*DT**5*(mu*(c1+c4))**3
    ch.zero('original_nodal_complement_determinant',zero.det()-determinant)
    ch.add('complement_analytic_no_absolute_cusp',not any(e.has(s.Abs,s.sign) for e in list(Rmat)+list(mix)))
    c=w*w;aw=s.Abs(w);ct=2*(H-HB)*c;cz=2*w*wp
    apsi=-U-(3*H-HB-q)*p+p*R*wp/w
    E=3*A*(2*p*apsi*c*aw+s.Rational(3,2)*p*p*aw*ct+3*H*p*p*c*aw\
           -p*p*(q*c*aw+s.Rational(3,2)*R*aw*cz))
    expectedE=3*A*c*aw*(-2*p*U-HB*p*p+p*p*(q-R*wp/w))
    ch.zero('undivided_original_cusp_scalar_current',E-expectedE)
    lapse=s.Symbol('N',positive=True);Lc=-A*p**3*aw**3/lapse**2
    drho=s.diff(Lc,lapse).subs(lapse,1)
    ch.zero('local_lapse_density_cusp',drho-2*A*p**3*aw**3)
    psi=s.Symbol('psi',real=True);dust=-drho*(-s.exp(2*be*psi)+s.exp(4*be*psi))/2
    matter=s.diff(dust,psi).subs(psi,0)
    ch.zero('independently_varied_future_dust_source',matter+be*drho)
    leading=A*(6*p*U+3*HB*p*p+2*be*p**3)/b
    ch.zero('leading_coefficient_not_mean_density_replacement',s.diff(leading,be)-2*A*p**3/b)
    direct=base.CLEAN(-(E+matter)/(b*w*w))
    x,sl=s.symbols('x spos',positive=True);r1,r3,w3=s.symbols('r1 r3 w3',real=True)
    for orientation in (-1,1):
        ww=orientation*sl*x+w3*x**3/6;rr=r1*x+r3*x**3/6
        limit=s.limit((q-R*wp/w).subs({q:s.diff(rr,x),R:rr,w:ww,wp:s.diff(ww,x)}),x,0,dir='+')
        ch.zero('exact_reflection_node_ratio_'+str(orientation),limit)
    ch.zero('leading_two_sided_cusp_coefficient',direct/aw-leading+3*A*p*p*(q-R*wp/w)/b)
    force=s.zeros(12,1)
    force[0]=-A*p**3*aw**3;force[3]=-4*A*p**3*aw**3;force[5]=-A*p**3*aw**3
    force[7]=-3*A*p**3*w*aw
    for sign in (-1,1):
        ch.add('mix_divisible_third_order_'+str(sign),
            all(s.limit(e.subs(w,sign*x)/x**3,x,0,dir='+').is_finite for e in mix))
        ch.add('cusp_force_second_order_'+str(sign),
            all(s.limit(e.subs(w,sign*x)/x**2,x,0,dir='+').is_finite for e in force))
    ch.add('coupled_feedback_retained',mix!=s.zeros(12,1) and force!=s.zeros(12,1))
    ch.add('metric_drift_omission_changes_current',base.CLEAN(3*A*s.Rational(3,2)*p*p*aw*(-2*H*c))!=0)
    return dict(R=list(Rmat),mix=list(mix),force=list(force)),dict(
        original_nodal_complement_determinant=str(determinant),scalar_complement_mixing=[str(e) for e in mix],
        scalar_cusp_current=str(base.CLEAN(E)),local_density_cusp=str(drho),leading_acceleration_coefficient=str(leading),
        exact_direct_cusp_acceleration=str(direct),
        feedback='delta_Ztt=(h^T R^-1 f_cusp-Epsi_cusp+beta*delta_rho)/(b*w^2)',
        proof='R is analytic and det R(0)!=0. h=O(w^3),f_cusp=O(|w|^2), so coupled feedback is O(|w|^3) after division by b*w^2. Analytic shift reflection gives q-R*wprime/w ->0. Therefore delta_Ztt/|w| -> K0.',
        derivative_jump='2*K0*abs(partial_z w(node))',
        interpretation='Nonzero K0 obstructs C1 spatial regularity of Ztt and hence C3 spacetime Z in this registered profile class. It does not rule out C2/weak existence or the whole action.')
_EX=None
def initialize(pack):
    global _EX
    mp.mp.dps=110;iv.dps=80;_EX={k:base.Eval(v) for k,v in pack.items()}
def coordinate_body(y,p,par,w,wp,U,Ud,Rc):
    # Independent four-coordinate metric/vector first jets; all twelve velocities vary.
    K=mp.matrix([[y[0],y[1],y[2]],[y[1],y[3],y[4]],[y[2],y[4],y[5]]]);X=mp.matrix(y[6:9])
    V=mp.matrix([0,w,0]);Vz=mp.matrix([0,wp,0]);shift=mp.matrix([0,mp.mpf(2)/37,mp.mpf(3)/41])
    ds=mp.matrix([0,mp.mpf(1)/43,mp.mpf(2)/47])
    lie=mp.matrix([[ (ds[j] if i==2 else 0)+(ds[i] if j==2 else 0) for j in range(3)] for i in range(3)])
    ht=2*K+lie;vt=X+shift[2]*Vz;gam=mp.sqrt(1+w*w)
    gt=(V.T*ht*V)[0]/(2*gam)+(V.T*vt)[0]/gam;gz=w*wp/gam
    g=mp.zeros(4);g[0,0]=-1+(shift.T*shift)[0]
    for i in range(3):
        g[0,i+1]=g[i+1,0]=shift[i];g[i+1,i+1]=1
    gi=g**-1;dg=[mp.zeros(4) for _ in range(4)]
    dg[0][0,0]=(shift.T*ht*shift)[0];dg[3][0,0]=2*(shift.T*ds)[0]
    for i in range(3):
        dg[0][0,i+1]=dg[0][i+1,0]=(ht*shift)[i]
        dg[3][0,i+1]=dg[3][i+1,0]=ds[i]
        for j in range(3):dg[0][i+1,j+1]=ht[i,j]
    n=mp.matrix([gam]+list(V-gam*shift));dn=[mp.matrix([0,0,0,0]) for _ in range(4)]
    dn[0]=mp.matrix([gt]+list(vt-gt*shift));dn[3]=mp.matrix([gz]+list(Vz-gz*shift-gam*ds))
    DN=mp.zeros(4)
    for a in range(4):
        for b in range(4):
            DN[a,b]=dn[a][b]+sum(sum(gi[b,l]*(dg[a][l,j]+dg[j][l,a]-dg[l][a,j])/2 for l in range(4))*n[j] for j in range(4))
    Z=U*w*w;Zz=2*U*w*wp;Zhat=Ud*w*w-shift[2]*Zz
    grads={name:mp.matrix([y[9+i],0,0,0]) for i,name in enumerate(('u','v','r'))}
    grads.update(psi=mp.matrix([p,0,0,0]),Z=mp.matrix([Zhat+shift[2]*Zz,0,0,Zz]),T=mp.matrix([1,0,0,0]))
    config=dict(DN=DN,g=g,gi=gi,n=n,Kraw=K,h=mp.eye(3),hi=mp.eye(3),
                Z=Z,u=Rc,v=mp.mpf(0),r=Rc,psi=mp.mpf(0),epsilon=mp.mpf(1)/5,R3=mp.mpf(0),coord_grad=grads)
    return canonical.mp_body(config,par,y,p,Zhat,coordinate=True,include_dust=False)
def current_control(x,sign,v,r1,r3,t1,t3):
    p,H,HB,U,k,e=[v[n] for n in ('p','H','H0','U','k','e')]
    w=lambda z:sign*e*mp.sin(k*z)
    wz=lambda z:sign*e*k*mp.cos(k*z)
    R=lambda z:r1*z+r3*z**3/6
    q=lambda z:r1+r3*z*z/2
    a=lambda z:-U-(3*H-HB-q(z))*p+p*R(z)*wz(z)/w(z)
    def current(t,z):
        scale=mp.exp(2*H*t);ww=mp.exp(-HB*t)*w(z)
        S=mp.matrix([0,t1*z+t3*z**3/6,R(z)]);g=mp.zeros(4)
        g[0,0]=-1+scale*(S.T*S)[0]
        for i in range(3):
            g[0,i+1]=g[i+1,0]=scale*S[i];g[i+1,i+1]=scale
        gam=mp.sqrt(1+scale*ww*ww);n=mp.matrix([gam,-gam*S[0],ww-gam*S[1],-gam*S[2]])
        hp=g**-1+n*n.T;grad=mp.matrix([p+a(z)*t,0,0,mp.diff(a,z)*t*t/2])
        Y=(grad.T*hp*grad)[0];return mp.exp(3*H*t)*mp.sqrt(Y)*(hp*grad)
    E=3*v['A']*(mp.diff(lambda t:current(t,x)[0],0)+mp.diff(lambda z:current(0,z)[3],x))
    ww=w(x);rr=R(x);qq=q(x);aa=a(x)
    expected=3*v['A']*abs(ww)**3*(-2*p*U-HB*p*p+p*p*(qq-rr*wz(x)/ww))
    drho=mp.diff(lambda N:-v['A']*p**3*abs(ww)**3/N**2,mp.mpf(1))
    matter=mp.diff(lambda ps:-drho*(-mp.exp(2*v['beta']*ps)+mp.exp(4*v['beta']*ps))/2,mp.mpf(0))
    vv=dict(v,w=ww,wp=wz(x),R=rr,q=qq,Zhat=v['Ud']*ww**2-rr*2*U*ww*wz(x))
    mat=_EX['R'].numeric(vv);mix=mp.matrix(_EX['mix'].numeric(vv));force=mp.matrix(_EX['force'].numeric(vv))
    matrix=mp.matrix([[mat[12*i+j] for j in range(12)] for i in range(12)])
    response=mp.lu_solve(matrix,force);feedback=(mix.T*response)[0]
    ztt=(feedback-E-matter)/(v['b']*ww*ww)
    K0=v['A']*(6*p*U+3*HB*p*p+2*v['beta']*p**3)/v['b']
    return dict(current_error=abs(E-expected)/(1+abs(E)+abs(expected)),
        normalized_limit_error=abs(ztt/abs(ww)-K0)/(1+abs(K0)),
        normalized_coupled_feedback=abs(feedback/(v['b']*ww**2*abs(ww))),
        ztt_cusp=ztt,leading=K0)
def case_job(task):
    index,cert,point,initial=task;ch=base.Checks()
    eta=s.Rational(cert['eta']);es=s.Symbol('eta')
    raw=READ(cop.PLANAR)['families'][cert['family']]['parameter_map']
    vv={n:base.interval_s(s.sympify(text,locals={'eta':es}).subs(es,eta)) for n,text in raw.items()}
    vv.update(p=base.interval_s(eta/5),H0=cop.unpack(initial['H_background']),U=cop.unpack(cert['U_bracket']))
    DT=vv['MP2']-vv['MU2']*(vv['c1']+vv['c3']);M=vv['MP2']+vv['MU2']*(vv['c1']+3*vv['c2']+vv['c3'])/2
    lower=vv['A']*(6*vv['p']*vv['U']+3*vv['H0']*vv['p']**2+2*vv['beta']*vv['p']**3)/vv['b']
    ch.add('nodal_complement_nonsingular',all(base.lo(t)>0 for t in (DT,M,vv['MU2']*(vv['c1']+vv['c4']))))
    ch.add('leading_absolute_cusp_strictly_positive',base.lo(lower)>0)
    par=canonical.parameters(cert['family'],cert['eta'],'mp');rc=mp.sqrt(mp.mpf(eta.p)/eta.q)
    v=dict(par,Rc=rc,p=mp.mpf(eta.p)/(5*eta.q),H=mp.mpf(point['H']),H0=base.midpoint(vv['H0']),
           U=mp.mpf(point['U']),Ud=mp.mpf(point['Ud']),k=mp.mpf(40),e=mp.mpf(1)/500)
    errors=[];mixerrors=[]
    for sign in (-1,1):
        w=sign*v['e']*mp.cos(mp.pi/7);wp=-sign*v['e']*v['k']*mp.sin(mp.pi/7)
        state=dict(v,w=w,wp=wp,R=mp.mpf(0),q=mp.mpf(0),Zhat=v['Ud']*w*w)
        analytic=_EX['R'].numeric(state);hmix=_EX['mix'].numeric(state)
        zero=[mp.mpf(0)]*12
        body=lambda y,p:coordinate_body(y,p,par,w,wp,v['U'],v['Ud'],rc)
        f0=body(zero,v['p']);fi=[]
        for i in range(12):
            yp=list(zero);yp[i]=1;fi.append(body(yp,v['p']))
        for i in range(12):
            for j in range(12):
                y=list(zero);y[i]+=1;y[j]+=1
                got=body(y,v['p'])-fi[i]-fi[j]+f0
                # f(2e_i)-2f(e_i)+f(0)=R_ii; cross polarization gives R_ij.
                want=analytic[12*i+j]
                errors.append(abs(got-want)/(1+abs(got)+abs(want)))
        dp=v['p']/2;fp=body(zero,v['p']+dp)
        for i in range(12):
            y=list(zero);y[i]=1
            got=(body(y,v['p']+dp)-fi[i]-fp+f0)/dp
            mixerrors.append(abs(got-hmix[i])/(1+abs(got)+abs(hmix[i])))
    ch.small('all144_original_coordinate_complement_entries_both_signs',max(errors),'1e-50')
    ch.small('all12_original_coordinate_scalar_mixings_both_signs',max(mixerrors),'1e-50')
    r2=base.midpoint(cop.unpack(cert['attempts'][-1]['core']['r2']));r1=v['e']**2*r2
    p0=par['MU2']*(par['c1']+par['c2']+par['c3'])
    slope=v['k']*v['e'];W0=-par['MU2']*(par['c1']+par['c2']+par['c4'])*slope**2
    fprime=par['MU2']*slope**2*(v['H0']*(par['c1']+2*par['c2']+par['c4'])-v['H']*(3*par['c1']+5*par['c2']+par['c3']+2*par['c4']))
    r3=((W0-2*p0*slope**2)*r1-fprime)/p0
    records=[]
    for orient in (-1,1):
        c13=par['c1']+par['c3'];den=par['MP2']-par['MU2']*c13;ss=orient*slope
        t1=-par['MU2']*c13*ss/den
        t3=-par['MU2']*ss/den*(-c13*v['k']**2+2*ss**2*(2*par['c3']-c13/2-c13*2*par['MU2']*(par['c4']-par['c3'])/den))
        for delta,tol in (('1e-12','1e-20'),('1e-18','1e-30')):
            for side in (-1,1):
                result=current_control(side*mp.mpf(delta),orient,v,r1,r3,t1,t3)
                tag=f'{orient}_{side}_{delta}'
                ch.small('coordinate_cusp_current_'+tag,result['current_error'],tol)
                ch.small('full_coupled_node_limit_'+tag,result['normalized_limit_error'],tol)
                records.append(dict(orientation=orient,side=side,normal_probe=delta,
                                    **{k:base.SHOW(z) for k,z in result.items()}))
    return index,dict(family=cert['family'],eta=cert['eta'],leading_coefficient=base.pack(lower),
        jump_per_absolute_slope=base.pack(2*lower),status='NONZERO_REGULATOR_ACCELERATION_CUSP',
        C3_regulator_extension_obstructed=True,C2_or_weak_existence_tested=False),dict(
        family=cert['family'],eta=cert['eta'],coordinate_matrix_error=base.SHOW(max(errors)),
        coordinate_mixing_error=base.SHOW(max(mixerrors)),probes=records),ch.rows
def calculate(workers):
    mp.mp.dps=110;iv.dps=80;pins,before=sources();ch=base.Checks();pack,form=build(ch)
    if not all(r['passed'] for r in ch.rows):raise ValueError('exact derivation failure '+repr([r for r in ch.rows if not r['passed']]))
    certs=READ(JOINT+'certificates.json');points=READ(JOINT+'independent.json');initial=READ(cop.CERTS)
    if len(certs)!=9 or len(points)!=9 or len(initial)!=9:raise ValueError('case count mismatch')
    tasks=[(i,a,b,c) for i,(a,b,c) in enumerate(zip(certs,points,initial))];results={}
    progress('regularity_cases_start',cases=9,workers=min(workers,9))
    if workers==1:
        initialize(pack)
        for t in tasks:
            r=case_job(t);results[r[0]]=r;progress('regularity_case_complete',index=r[0])
    else:
        with ProcessPoolExecutor(max_workers=min(workers,9),mp_context=multiprocessing.get_context('spawn'),initializer=initialize,initargs=(pack,)) as pool:
            jobs={pool.submit(case_job,t):t[0] for t in tasks}
            for future in as_completed(jobs):
                r=future.result()
                if r[0]!=jobs[future] or r[0] in results:raise ValueError('case identity mismatch')
                results[r[0]]=r;progress('regularity_case_complete',index=r[0])
    out=[];controls=[]
    for i in range(9):
        _,record,control,checks=results[i];out.append(record);controls.append(control)
        joint.merge_checks(ch,checks,record['family']+'_'+record['eta']+'_')
    _,after=sources();ch.add('all_original_bytes_sidecars_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_REGULATOR_CUSP_AUDIT_ONLY' if passed==len(ch.rows) else 'FAIL_OR_UNRESOLVED_REGULATOR_CUSP_AUDIT',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,
        status='C3_REGULATOR_EXTENSION_OBSTRUCTED_C2_WEAK_AND_PHYSICAL_DOMAIN_OPEN',
        full_initial_acceleration_solution_constructed=False,full_initial_admission=False,state_adopted_or_evolved=False,
        C2_or_weak_existence_proved=False,action_no_go=False,stage2_complete=False,stage3_entered=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')
    return {'summary.json':summary,'formulas.json':form,'certificates.json':out,'independent.json':controls}
def main():
    global _PROGRESS
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay');p.add_argument('--workers',type=int,default=16);p.add_argument('--progress-log');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose one output or replay')
    if a.progress_log:
        _PROGRESS=(ROOT/a.progress_log).resolve()
        if not _PROGRESS.is_relative_to(ROOT/'.local/itsm-context'):raise ValueError('progress outside ignored context')
        _PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        with _PROGRESS.open('x',encoding='utf-8'):pass
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    rec=lambda f:(SHA(f.read_bytes()),f.stat().st_size,f.stat().st_mtime_ns)
    old={f.name:rec(f) for f in dest.iterdir()} if a.replay else None
    data=calculate(v4.selected_workers(a.workers));payload={n:ENC(v) for n,v in data.items()}
    for name,raw in list(payload.items()):payload[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode()
    if a.replay:
        if set(old)!=set(payload):raise ValueError('replay file set mismatch')
        for name,raw in payload.items():
            f=dest/name
            if f.read_bytes()!=raw or rec(f)!=old[name]:raise ValueError('replay bytes/metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payload.items():
            with (dest/name).open('xb') as f:f.write(raw)
    su=data['summary.json'];print(json.dumps({k:su[k] for k in ('validation','passed','total','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1
if __name__=='__main__':raise SystemExit(main())
