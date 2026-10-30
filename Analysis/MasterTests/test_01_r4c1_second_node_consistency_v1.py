"""Second regulator-node identity and approximate trace; no certified exclusion."""
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
PRIMARY='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PSHA='2cbb055c8a4172ef9e75daa7b80a92c5f979aadc817e29d7cace6115adb47ec5'
PRIOR='Analysis/MasterTests/outputs/r4c1_joint_background_acceleration_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_SECOND_NODE_CONSISTENCY_V1_CONTRACT_2026-10-27.md'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_SECOND_NODE_CONSISTENCY_V1_COMPUTATIONAL_ADDENDUM_2026-10-27.md'
WORKING='Theory/Gates/RES-001/RES001_R4C1_SECOND_NODE_CONSISTENCY_WORKING_ALGEBRA_2026-10-27.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
SHOW=lambda x:mp.nstr(x,75)
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))


def geometric_control(case,orientation):
    mp.mp.dps=80;p=mp.mpf(2+case)/11;H=mp.mpf(1+case)/13;HB=mp.mpf(2)/17
    slope=orientation*mp.mpf(2+case)/7
    az=mp.mpf(5+case)/19;apsizz=mp.mpf(7+case)/23;avz1=mp.mpf(3+case)/29
    def fields(t,z):
        h=mp.eye(3)
        for j,(a,b) in enumerate(HM):
            value=(2*H*t if a==b else 0)+t*t*(mp.mpf(j+case+1)/31+mp.mpf(j+1)*z/37)/2
            h[a,b]+=value
            if a!=b:h[b,a]+=value
        S=mp.matrix([mp.mpf(1)/41*z,mp.mpf(2)/43*z,mp.mpf(3)/47*z+z**3/53])
        V=mp.matrix([t*t*(1+z)/59,
            slope*z*(1-HB*t)+t*t*(mp.mpf(1)/61+z/67)/2,
            t*t*(mp.mpf(1)/71+avz1*z)/2])
        gam=mp.sqrt(1+(V.T*h*V)[0]);g=mp.matrix(4);g[0,0]=-1+(S.T*h*S)[0]
        hs=h*S
        for i in range(3):
            g[0,i+1]=g[i+1,0]=hs[i]
            for j in range(3):g[i+1,j+1]=h[i,j]
        n=mp.matrix([gam]+list(V-gam*S))
        return g,n,mp.sqrt(mp.det(h))
    def psi(t,z):
        return p*t+t*t*(mp.mpf(1)/73+z/79+apsizz*z*z/2)/2+t**3/83+t**4/89
    def Z(t,z):return slope*slope*z*z/97+slope*slope*z*z*t/101+az*t*t/2+t**3/103
    def equation(t,z):
        g,n,vol=fields(t,z);gi=g**-1;hp=gi+n*n.T
        dg={0:mp.diff(lambda u:fields(u,z)[0],t),3:mp.diff(lambda u:fields(t,u)[0],z)}
        dn={0:mp.diff(lambda u:fields(u,z)[1],t),3:mp.diff(lambda u:fields(t,u)[1],z)}
        dhp={i:-gi*dg[i]*gi+dn[i]*n.T+n*dn[i].T for i in (0,3)}
        logs={i:sum((gi*dg[i])[j,j] for j in range(4))/2 for i in (0,3)}
        cov=n[0]*dg[0]*n+n[3]*dg[3]*n
        for i in (0,3):cov[i]-=(n.T*dg[i]*n)[0]/2
        acc=n[0]*dn[0]+n[3]*dn[3]+gi*cov
        grad={0:mp.diff(lambda u:psi(u,z),t),3:mp.diff(lambda u:psi(t,u),z)}
        hess={(0,0):mp.diff(lambda u:psi(u,z),t,2),
              (3,3):mp.diff(lambda u:psi(t,u),z,2),
              (0,3):mp.diff(lambda u:mp.diff(lambda v:psi(u,v),z),t)}
        hess[3,0]=hess[0,3]
        value=Z(t,z)+sum(hp[i,j]*hess[i,j] for i in (0,3) for j in (0,3))
        for j in (0,3):value+=(sum(dhp[i][i,j]+logs[i]*hp[i,j] for i in (0,3))-acc[j])*grad[j]
        return value
    got=mp.diff(lambda t:equation(t,mp.mpf(0)),mp.mpf(0),2)
    expected=az+apsizz+p*avz1;err=abs(got-expected)/(1+abs(got)+abs(expected))
    return dict(kind='geometry',case=case,orientation=orientation,got=SHOW(got),expected=SHOW(expected),
        checks=[dict(name='full_coordinate_second_node_identity',passed=bool(err<mp.mpf('1e-30')),value=SHOW(err),criterion='normalized < 1e-30')])


def coefficient_control(orientation):
    mp.mp.dps=100
    if SHA((ROOT/PRIMARY).read_bytes())!=PSHA:raise ValueError('prior acceleration source drift')
    spec=importlib.util.spec_from_file_location('node_trace_acceleration',ROOT/PRIMARY)
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model);model.setup();mp.mp.dps=100
    bdy=model.body;par=model.par;H,U,Ud=model.H,model.U,model.Ud;HB=model.vals['H0'];p=model.vals['p']
    k=mp.mpf(40);e=mp.mpf(1)/500;slope=orientation*e*k
    r1=model.shift(mp.pi/2)[1]
    r3_galerkin=k*k*mp.diff(lambda a:model.shift(a)[1],mp.pi/2,2)
    s0=par['c1']+par['c2']+par['c3'];ss=slope*slope
    A00=par['c1']+2*par['c2']+par['c4'];AH=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']
    r3=-ss*(HB*A00-H*AH+(par['c1']+par['c2']+par['c4']+2*s0)*r1)/s0
    ty0=-par['MU2']*(par['c1']+par['c3'])*slope/(par['MP2']-par['MU2']*(par['c1']+par['c3']))
    saved_A=par['A'];par['A']=mp.mpf(0)  # ONLY the stated low-order normal coefficients.
    def state(x,W):
        w=orientation*e*mp.sin(k*x);wp=slope*mp.cos(k*x);wpp=-k*k*w
        R=r1*x+r3*x**3/6;Rp=r1+r3*x*x/2;Rpp=r3*x
        def ty(y):
            ww=orientation*e*mp.sin(k*y);wwp=slope*mp.cos(k*y)
            den=par['MP2']-par['MU2']*(par['c1']+par['c3']+2*par['c3']*ww**2-2*par['c4']*(1+ww**2)*ww**2)
            return -par['MU2']*(par['c1']+par['c3']+2*par['c3']*ww**2)*wwp/(mp.sqrt(1+ww**2)*den)
        q=[mp.mpf(0)]*14;v=q.copy();d=q.copy();dd=q.copy();vd=q.copy()
        for i in (0,3,5):q[i]=1;v[i]=2*H
        q[7]=w;q[9]=q[11]=model.vals['Rc'];q[13]=U*w*w+W*w**4
        v[7]=-HB*w;v[10]=model.vals['Rc']/(1-par['zeta']*model.vals['Rc']**2*e*e/2)
        v[11]=model.vals['rd'];v[12]=p;v[13]=Ud*w*w
        d[7]=wp;d[13]=2*U*w*wp+4*W*w**3*wp
        dd[7]=wpp;dd[13]=2*U*(wp*wp+w*wpp)+W*(12*w*w*wp*wp+4*w**3*wpp)
        vd[7]=-HB*wp;vd[13]=2*Ud*w*wp
        A=q+v+d+[mp.mpf(0),mp.mpf(0),R]+[mp.mpf(0),ty(x),Rp]
        Wt=v+[mp.mpf(0)]*14+vd+[mp.mpf(0)]*6
        Wz=d+vd+dd+[mp.mpf(0),ty(x),Rp]+[mp.mpf(0),mp.diff(ty,x),Rpp]
        ratio=(r1+r3*x*x/6)*mp.cos(k*x)/mp.sinc(k*x)
        apsi=-U-W*w*w-(3*H-HB-Rp)*p+p*ratio
        return A,Wt,Wz,apsi
    def engine(x,W,step):
        A,Wt,Wz,apsi=state(x,W);L,grad=model.gradient(A)
        ht=model.hv(A,Wt,step);hz=model.hv(A,Wz,step);columns=[]
        for j in range(12):
            direction=[mp.mpf(0)]*48;direction[14+j]=1
            columns.append(model.hv(A,direction,step)[14:26,0])
        R=mp.matrix([[columns[j][i] for j in range(12)] for i in range(12)])
        direction=[mp.mpf(0)]*48;direction[26]=1;cross=model.hv(A,direction,step)[14:26,0]
        rhs=mp.matrix([grad[j]-ht[14+j]-hz[28+j] for j in range(12)])-cross*apsi
        ay=mp.lu_solve(R,rhs)
        _,normal=model.density(A);energy=sum(grad[14+j]*normal[j] for j in range(14))-L
        w=A[7];wp=A[35];gam=mp.sqrt(1+w*w)
        rho=-energy-gam*hz[22]-w*wp*grad[22]/gam
        return rho,ay
    checks=[];rows=[]
    def check(name,err):checks.append(dict(name=name,passed=bool(err<mp.mpf('1e-18')),value=SHOW(err),criterion='normalized < 1e-18'))
    try:
        for step_text in ('1e-25','1e-30'):
            step=mp.mpf(step_text)
            rho2=mp.diff(lambda x:engine(x,mp.mpf(0),step)[0],mp.mpf(0),2)/2
            avz1=mp.diff(lambda x:engine(x,mp.mpf(0),step)[1][8],mp.mpf(0))
            a0=-U-(3*H-HB-2*r1)*p;a2=p*(2*r3-r1*k*k)/3
            az=(par['K_Q']*(a2+ss*a0)+par['K_Q']*p*(-r3/2+(5*H-2*HB-3*r1)*ss)
                +4*par['b']*U*ss*k*k+3*par['b']*U*ty0*slope**3+par['beta']*rho2)/(par['b']*ss)
            Q=az+2*a2+p*avz1
            rows.append(dict(step=step_text,rho2=rho2,avz1=avz1,a0=a0,a2=a2,az=az,Q=Q))
        for key in ('rho2','avz1','az','Q'):
            check('two_step_'+key,abs(rows[0][key]-rows[1][key])/(1+abs(rows[0][key])+abs(rows[1][key])))
        check('original_shift_third_jet',abs(r3-r3_galerkin)/(1+abs(r3)+abs(r3_galerkin)))
        step=mp.mpf('1e-30')
        rho2W=mp.diff(lambda x:engine(x,mp.mpf(1),step)[0],mp.mpf(0),2)/2
        avz1W=mp.diff(lambda x:engine(x,mp.mpf(1),step)[1][8],mp.mpf(0))
        check('quartic_profile_local_rho2_invariance',abs(rho2W-rows[1]['rho2'])/(1+abs(rho2W)+abs(rows[1]['rho2'])))
        check('quartic_profile_local_frame_slope_invariance',abs(avz1W-rows[1]['avz1'])/(1+abs(avz1W)+abs(rows[1]['avz1'])))
        gain=-(par['K_Q']/par['b']+14*ss)
        return dict(kind='approximate_trace',orientation=orientation,checks=checks,
            coefficients=[{key:SHOW(value) if key!='step' else value for key,value in row.items()} for row in rows],
            r1=SHOW(r1),r3=SHOW(r3),partial_quartic_gain=SHOW(gain),
            Q_sign_certified_at_exact_joint_root=False,
            physical_admission=False,cusp_scope='Only low-order coefficient extraction; original nonzero A retained outside this device')
    finally:par['A']=saved_A


def run_job(job):
    try:return geometric_control(job[1],job[2]) if job[0]=='geometry' else coefficient_control(job[2])
    except Exception:return dict(kind=job[0],orientation=job[2],checks=[dict(name='unexpected_exception',passed=False,traceback=traceback.format_exc())])


def calculate(workers):
    pins=dict(json.loads((ROOT/PRIOR).read_bytes())['source_sha256'])
    for name in (PRIMARY,PRIOR,CONTRACT,ADDENDUM,WORKING,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    if pins[PRIMARY]!=PSHA:raise ValueError('primary pin drift')
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    jobs=[('geometry',case,orientation) for case in (0,1) for orientation in (-1,1)]+[('trace',0,x) for x in (-1,1)]
    results=[]
    with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn')) as pool:
        futures=[pool.submit(run_job,job) for job in jobs]
        for future in as_completed(futures):
            row=future.result();results.append(row)
            print(json.dumps({'completed':row['kind'],'orientation':row['orientation'],'passed':all(c['passed'] for c in row['checks'])}),flush=True)
    results.sort(key=lambda x:(x['kind'],x.get('case',0),x['orientation']))
    checks=[dict(c,kind=r['kind'],orientation=r['orientation']) for r in results for c in r['checks']]
    return dict(result_id='R4C1-SECOND-NODE-CONSISTENCY-V1',source_sha256=pins,checks=checks,
        passed=sum(c['passed'] for c in checks),total=len(checks),results=results,mpmath=mp.__version__,
        physical_admission=False,G1_complete=False,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',interpretation='Identity and approximate trace only; no certified sign or physical exclusion')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);parser.add_argument('--workers',type=int,default=4)
    a=parser.parse_args()
    if not 1<=a.workers<=4:raise ValueError('workers 1..4 required')
    result=calculate(a.workers);data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);p=directory/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
