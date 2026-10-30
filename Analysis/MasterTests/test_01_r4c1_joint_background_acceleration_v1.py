"""Full initial-slice Euler acceleration diagnostic; G1 admission remains open."""
from __future__ import annotations
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import traceback
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
BODY='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
BSHA='b887c7a52102b7abb43a2875cb6e01607ecb46d39a95f4abb4cefab9795a73c0'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_JOINT_BACKGROUND_ACCELERATION_V1_CONTRACT_2026-10-27.md'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_JOINT_BACKGROUND_ACCELERATION_V1_COMPUTATIONAL_ADDENDUM_2026-10-27.md'
JOINT='Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))
STEPS=('1e-20','1e-26');TOL='1e-18'
body=None;par=None;vals=None;H=None;U=None;Ud=None;shift=None


def setup():
    global body,par,vals,H,U,Ud,shift
    mp.mp.dps=90
    if SHA((ROOT/BODY).read_bytes())!=BSHA:raise ValueError('original body drift')
    spec=importlib.util.spec_from_file_location('joint_acceleration_original',ROOT/BODY)
    body=importlib.util.module_from_spec(spec);spec.loader.exec_module(body)
    point=next(x for x in READ(JOINT+'independent.json') if x['family']=='new_B1_frame' and x['eta']=='1/4')
    initial=next(x for x in READ(body.lift.cop.CERTS) if x['family']=='new_B1_frame' and x['eta']=='1/4')
    par,vals,H,U,Ud,_,shift=body.lift.setup(point,initial)


def density(A):
    q=A[:14];v=A[14:28];d=A[28:42];S=A[42:45];Sd=A[45:48]
    h=body.tensor(q);R=S[2]
    K=[]
    for n,(i,j) in enumerate(HM):
        lie=R*d[n]+(sum(h[i][a]*Sd[a] for a in range(3)) if j==2 else 0)\
            +(sum(h[j][a]*Sd[a] for a in range(3)) if i==2 else 0)
        K.append((v[n]-lie)/2)
    X=[v[6+i]-R*d[6+i]+q[8]*Sd[i] for i in range(3)]
    y=K+X+[v[i]-R*d[i] for i in (9,10,11)]
    s=v[12]-R*d[12];zh=v[13]-R*d[13]
    c=body.dot(q[6:9],body.mv(h,q[6:9]));vol=body.sqrt(body.det3(h));gam=body.sqrt(1+c)
    local=body.body(q+[mp.mpf(0)],d+[mp.mpf(0)],y,s,par)
    temporal=-par['b']*zh*(c*s+gam*q[8]*d[12])
    return vol*(local+temporal),[2*x for x in K]+X+y[9:12]+[s,zh]


def gradient(A):
    tape=body.Tape();variables=[tape.var(x) for x in A]
    L,_=density(variables)
    return body.val(L),mp.matrix(tape.grad(L,variables))


def hv(A,W,step):
    _,g=gradient([a+mp.j*step*w for a,w in zip(A,W)])
    return mp.matrix([mp.im(x)/step for x in g])


def norm(A):return max(abs(x) for x in A)
def relative(A,B):return norm(A-B)/(1+norm(A)+norm(B))
def show(x):return mp.nstr(x,70)


def initial(angle):
    e=mp.mpf(1)/500;k=mp.mpf(40);w=e*mp.cos(angle);wp=-e*k*mp.sin(angle);wpp=-k*k*w
    R,Rp=shift(angle)
    Rpp=k*mp.diff(lambda t:shift(t)[1],angle)
    def ty_at(t):
        ww=e*mp.cos(t);wwp=-k*e*mp.sin(t)
        den=par['MP2']-par['MU2']*(par['c1']+par['c3']+2*par['c3']*ww**2-2*par['c4']*(1+ww**2)*ww**2)
        return -par['MU2']*(par['c1']+par['c3']+2*par['c3']*ww**2)*wwp/(mp.sqrt(1+ww**2)*den)
    ty=ty_at(angle);typ=k*mp.diff(ty_at,angle)
    q=[mp.mpf(0)]*14;v=q.copy();d=q.copy();dd=q.copy();vd=q.copy()
    for i in (0,3,5):q[i]=1;v[i]=2*H
    q[7]=w;q[9]=q[11]=vals['Rc'];q[13]=U*w*w
    v[7]=-vals['H0']*w;v[10]=vals['Rc']/(1-par['zeta']*vals['Rc']**2*e*e/2)
    v[11]=vals['rd'];v[12]=vals['p'];v[13]=Ud*w*w
    d[7]=wp;d[13]=2*U*w*wp
    dd[7]=wpp;dd[13]=2*U*(wp*wp+w*wpp)
    vd[7]=-vals['H0']*wp;vd[13]=2*Ud*w*wp
    S=[mp.mpf(0),mp.mpf(0),R];Sd=[mp.mpf(0),ty,Rp];Sdd=[mp.mpf(0),typ,Rpp]
    return q+v+d+S+Sd,vd,dd,Sdd


def independent_euler(A,vd,dd,Sdd,acc,index):
    q=A[:14];v=A[14:28];d=A[28:42];S=A[42:45];Sd=A[45:48]
    def fields(t,z):
        qt=[q[j]+v[j]*t+d[j]*z+acc[j]*t*t/2+vd[j]*t*z+dd[j]*z*z/2 for j in range(14)]
        vt=[v[j]+acc[j]*t+vd[j]*z for j in range(14)]
        dt=[d[j]+vd[j]*t+dd[j]*z for j in range(14)]
        st=[S[j]+Sd[j]*z+Sdd[j]*z*z/2 for j in range(3)]
        sdt=[Sd[j]+Sdd[j]*z for j in range(3)]
        return qt+vt+dt+st+sdt
    def derivative(t,z,slot):
        state=fields(t,z);value=state[slot]
        def varied(x):
            changed=state.copy();changed[slot]=x;return density(changed)[0]
        return mp.diff(varied,value)
    return derivative(0,0,index)-mp.diff(lambda t:derivative(t,0,14+index),0)\
        -mp.diff(lambda z:derivative(0,z,28+index),0)


def task(item):
    label,angle_text,independent=item;angle=mp.mpf(angle_text);checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value<mp.mpf(TOL)),value=show(value),criterion='normalized < '+TOL))
    try:
        A,vd,dd,Sdd=initial(angle);L,grad=gradient(A)
        Wt=A[14:28]+[mp.mpf(0)]*14+vd+[mp.mpf(0)]*6
        Wz=A[28:42]+vd+dd+A[45:48]+Sdd
        steps=[]
        for step_text in STEPS:
            step=mp.mpf(step_text);ht=hv(A,Wt,step);hz=hv(A,Wz,step);columns=[]
            for j in range(14):
                W=[mp.mpf(0)]*48;W[14+j]=1;columns.append(hv(A,W,step)[14:28,0])
            M=mp.matrix([[columns[j][i] for j in range(14)] for i in range(14)])
            _,normal=density(A);E=sum(grad[14+j]*normal[j] for j in range(14))-L
            w=A[7];wp=A[35];gam=mp.sqrt(1+w*w)
            flux=gam*hz[22]+w*wp*grad[22]/gam
            rho=-E-flux
            rhs=mp.matrix([grad[j]-ht[14+j]-hz[28+j] for j in range(14)])
            rhs[12]-=par['beta']*rho
            acc=mp.lu_solve(M,rhs);g=par['b']*w*w
            check(step_text+'_Hessian_symmetry',relative(M,M.T))
            check(step_text+'_scalar_regulator_cross',abs(M[12,13]+g)/(1+abs(g)))
            check(step_text+'_regulator_diagonal',abs(M[13,13]))
            check(step_text+'_complement_regulator_cross',max(abs(M[j,13]) for j in range(12)))
            check(step_text+'_Euler_solve',relative(M*acc,rhs))
            steps.append(dict(acc=acc,rho=rho,M=M,rhs=rhs))
        check('two_step_acceleration',relative(steps[0]['acc'],steps[1]['acc']))
        check('two_step_local_density',abs(steps[0]['rho']-steps[1]['rho'])/(1+abs(steps[1]['rho'])))
        if independent:
            for j in (0,7,12,13):
                value=independent_euler(A,vd,dd,Sdd,steps[1]['acc'],j)
                if j==12:value-=par['beta']*steps[1]['rho']
                scale=1+norm(steps[1]['rhs'])+norm(steps[1]['M']*steps[1]['acc'])
                check('independent_real_Euler_'+str(j),abs(value)/scale)
        result=dict(label=label,theta=angle_text,frame=show(w),g=show(g),rho=show(steps[1]['rho']),
            acceleration=[show(x) for x in steps[1]['acc']],checks=checks,
            physical_admission=False,background_error_certified=False)
    except Exception:
        checks.append(dict(name='unexpected_exception',passed=False,traceback=traceback.format_exc()))
        result=dict(label=label,theta=angle_text,checks=checks,physical_admission=False)
    return result


def calculate(workers):
    setup();pins=dict(READ(JOINT+'summary.json')['source_sha256'])
    pins.update(body.PINS);pins[BODY]=BSHA
    for name in (CONTRACT,ADDENDUM,JOINT+'independent.json',body.lift.cop.CERTS,Path(__file__).relative_to(ROOT).as_posix()):
        pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    jobs=[('control_0',show(mp.mpf(0)),True),('control_pi4',show(mp.pi/4),True)]
    for node in (1,3):
        for delta in ('0.1','0.01','0.001'):
            for side in (-1,1):jobs.append((f'node{node}_{side}_{delta}',show(node*mp.pi/2+side*mp.mpf(delta)),False))
    results=[]
    if workers==1:
        for job in jobs:
            result=task(job);results.append(result);print(json.dumps({'completed':result['label'],'passed':all(x['passed'] for x in result['checks'])}),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=min(workers,4),mp_context=multiprocessing.get_context('spawn'),initializer=setup) as pool:
            futures=[pool.submit(task,job) for job in jobs]
            for f in as_completed(futures):
                result=f.result();results.append(result);print(json.dumps({'completed':result['label'],'passed':all(x['passed'] for x in result['checks'])}),flush=True)
    results.sort(key=lambda x:x['label']);checks=[dict(c,point=r['label']) for r in results for c in r['checks']]
    return dict(result_id='R4C1-JOINT-BACKGROUND-ACCELERATION-V1',source_sha256=pins,
        mpmath=mp.__version__,working_digits=90,steps=STEPS,checks=checks,
        passed=sum(c['passed'] for c in checks),total=len(checks),points=results,
        interpretation='Full initial-slice Euler diagnostic on an approximate joint representative; continuum/root-error and nodal continuation unproved',
        physical_admission=False,background_error_certified=False,physics_pass=False,
        G1_complete=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);p.add_argument('--workers',type=int,default=4)
    a=p.parse_args()
    if not 1<=a.workers<=4:raise ValueError('workers must be 1..4')
    result=calculate(a.workers);data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);path=directory/'summary.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
