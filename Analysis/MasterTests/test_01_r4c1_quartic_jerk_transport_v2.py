"""Original regulator time consistency and a bounded scalar-jerk cusp."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_JERK_TRANSPORT_V1_CONTRACT_2026-10-27.md'
PARENT='Analysis/MasterTests/outputs/r4c1_quartic_initial_extension_orientation_v1_attempt_01/independent.json'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))


def calculate():
    mp.mp.dps=100;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expression):
        values=list(expression) if isinstance(expression,s.MatrixBase) else [expression]
        bad=[str(z) for v in values if (z:=s.factor(s.cancel(v)))!=0];check(name,not bad,bad)
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]='07b5687ba7f7eec31ab20dffdd638729ed2d9b4f5ee2d5c12e243642e9a481a2'
    for name in (CONTRACT,'Theory/Gates/RES-001/RES001_R4C1_QUARTIC_JERK_TRANSPORT_V2_IMPLEMENTATION_NOTE_2026-10-27.md','Analysis/MasterTests/test_01_r4c1_quartic_jerk_transport_v1.py',Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry drift '+name)
    spec=importlib.util.spec_from_file_location('jerk_transport_original',ROOT/ENGINE)
    en=importlib.util.module_from_spec(spec);spec.loader.exec_module(en);en.setup()
    mp.mp.dps=100;iv.dps=80;cop=en.body.lift.cop;base=cop.base;ic=base.interval_s
    eta=s.Symbol('eta');par={n:s.sympify(t,locals={'eta':eta}).subs(eta,s.Rational(1,4)) for n,t in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    w=s.Symbol('w',real=True);p=s.Rational(1,20);e=s.Rational(1,500);A=par['A']
    kinetic=READ(KINETIC);B=s.Matrix([[s.sympify(t,locals={'w':w}) for t in row] for row in kinetic['formulas']['B']])
    B0=B.subs(w,0);C0=B0.inv()
    signs=[1,-1,1,1,-1,1,1,-1,1,1,1,1];D=s.diag(*signs)
    zero('exact_kinetic_orientation_conjugation',B.subs(w,-w)-D*B*D)
    zero('node_metric_frame_inverse_crosses',s.Matrix([C0[7,j] for j in (0,3,5)]))
    zero('node_frame_inverse',C0[7,7]-24)
    hyy,vy,tr,j=s.symbols('delta_hyy delta_Vy delta_trace delta_j',real=True)
    delta_ctt=w*w*hyy+2*w*vy
    delta_Ct=s.cancel(delta_ctt/2+w*w*tr/2-w*w*hyy/2)
    response=-p*(vy/w+tr/2)
    zero('full_volume_metric_cancellation',delta_Ct-w*vy-w*w*tr/2)
    zero('differentiated_regulator_response',w*w*response+p*delta_Ct)
    check('omitted_volume_trace_rejected',s.cancel(w*w*(-p*vy/w)+p*delta_Ct)!=0)
    leading=3*A*p**4*C0[7,7]
    zero('leading_jerk_coefficient',leading-72*A*p**4)
    inv=cop.unpack(kinetic['attempts'][-1]['inverse_bound'])
    derivative=[iv.mpf(v) for v in base.Eval(list(B.diff(w))+list(B.diff(w,2))).interval({'w':base.box(ic(e)/2)})]
    norms=[]
    for offset in (0,144):
        rows=[sum(base.upper(abs(v)) for v in derivative[offset+12*i:offset+12*i+12]) for i in range(12)]
        norms.append(base.upper(iv.mpf(max(base.hi(v) for v in rows))))
    first=base.upper(inv**2*norms[0]);second=base.upper(2*inv**3*norms[0]**2+inv**2*norms[1])
    remainder=base.upper(ic(A)*ic(p)**4*(3*second/2+15*first/2+9*inv/2))
    coefficient=ic(leading)
    check('leading_interval_strictly_positive',base.lo(coefficient)>0,base.pack(coefficient))
    check('finite_cubic_remainder',mp.isfinite(base.hi(remainder)) and base.lo(remainder)>0,base.pack(remainder))
    be=base.Eval(list(B));num=lambda x:mp.mpf(str(s.N(x,95)));an=num(A);pn=num(p)
    def cusp_acc(wv):
        flat=be.numeric({'w':wv});matrix=mp.matrix([[flat[12*i+j] for j in range(12)] for i in range(12)])
        force=mp.matrix(12,1)
        force[0]=force[5]=-an*pn**3*abs(wv)**3/2;force[3]=-2*an*pn**3*abs(wv)**3;force[7]=-3*an*pn**3*wv*abs(wv)
        return mp.lu_solve(matrix,force)
    point=READ(PRIMARY)['point'];H=mp.mpf(point['H']);HB=en.vals['H0'];U=mp.mpf(point['U']);Ud=mp.mpf(point['Ud']);W=mp.mpf(point['W'])
    def coordinate_time_equation(wv,wpv,acc,jvalue):
        R=mp.mpf(1)/47;rp=mp.mpf(1)/53;ty=mp.mpf(1)/59
        ap=mp.mpf(1)/71;apz=mp.mpf(1)/73;apzz=mp.mpf(1)/79
        Z0=U*wv**2+W*wv**4;Z1=(2*U*wv+4*W*wv**3)*wpv;Zd=Ud*wv**2
        def fields(t,z):
            h=mp.eye(3)
            for i,(a,c) in enumerate(HM):
                h[a,c]+=(2*H*t if a==c else 0)+t*t*(acc[i]+mp.mpf(i+1)*z/97)/2
                if a!=c:h[c,a]=h[a,c]
            V=mp.matrix([t*t*(acc[6]+z/101)/2,
                wv+wpv*z-HB*(wv+wpv*z)*t+t*t*(acc[7]+z/103)/2,
                t*t*(acc[8]+z/107)/2])
            shift=mp.matrix([mp.mpf(0),ty*z+z*z/109,R+rp*z+z*z/113])
            gamma=mp.sqrt(1+(V.T*h*V)[0]);g=mp.matrix(4);g[0,0]=-1+(shift.T*h*shift)[0];hs=h*shift
            for a in range(3):
                g[0,a+1]=g[a+1,0]=hs[a]
                for c in range(3):g[a+1,c+1]=h[a,c]
            return g,mp.matrix([gamma]+list(V-gamma*shift)),mp.sqrt(mp.det(h))
        def psi(t,z):return pn*t+(ap+apz*z+apzz*z*z/2)*t*t/2+jvalue*t**3/6
        def kernel(t,z):
            g,n,vol=fields(t,z);gi=g**-1;hp=gi+n*n.T
            gp=mp.matrix([mp.diff(lambda u:psi(u,z),t),0,0,mp.diff(lambda u:psi(t,u),z)])
            return vol*(hp*gp),gp,gi,n,vol
        def equation(t,z):
            flux,gp,gi,n,vol=kernel(t,z)
            dg={0:mp.diff(lambda u:fields(u,z)[0],t),3:mp.diff(lambda u:fields(t,u)[0],z)}
            dn={0:mp.diff(lambda u:fields(u,z)[1],t),3:mp.diff(lambda u:fields(t,u)[1],z)}
            cov=n[0]*dg[0]*n+n[3]*dg[3]*n
            for i in (0,3):cov[i]-=(n.T*dg[i]*n)[0]/2
            acceleration=n[0]*dn[0]+n[3]*dn[3]+gi*cov
            divergence=mp.diff(lambda u:kernel(u,z)[0][0],t)+mp.diff(lambda u:kernel(t,u)[0][3],z)
            Z=Z0+Z1*z+Zd*t+t*t/127+z*t/131
            return Z+divergence/vol-(acceleration.T*gp)[0]
        got=mp.diff(lambda t:equation(t,mp.mpf(0)),mp.mpf(0))
        trace=acc[0]+acc[3]+acc[5]
        ratio=R*wpv/wv
        expected=Zd+wv*wv*(jvalue+(5*H-3*HB-rp-ratio)*ap-2*R*apz
            +pn*(acc[7]/wv+trace/2+HB**2-8*H*HB-2*(H-HB)*(rp+ratio)))
        return got,expected
    controls=[];omitted_max=mp.mpf(0)
    for ratio in ('-1','-0.5','0.5','1'):
        for orientation in (-1,1):
            wv=mp.mpf(ratio)/500;wpv=orientation*mp.mpf(2)/25*mp.sqrt(1-mp.mpf(ratio)**2)
            delta=cusp_acc(wv);trace=delta[0]+delta[3]+delta[5];dj=-pn*(delta[7]/wv+trace/2)
            base_acc=mp.matrix([mp.mpf(i+1)/137 for i in range(12)]);j0=mp.mpf(1)/139
            original,formula=coordinate_time_equation(wv,wpv,base_acc,j0)
            raw,_=coordinate_time_equation(wv,wpv,base_acc+delta,j0)
            corrected,_=coordinate_time_equation(wv,wpv,base_acc+delta,j0+dj)
            error=abs(original-formula)/(1+abs(original)+abs(formula))
            corrected_error=abs(corrected-original)/(1+abs(original)+abs(corrected))
            predicted_change=-wv*wv*dj
            response_error=abs(raw-original-predicted_change)/(1+abs(original)+abs(raw))
            label=ratio+'_'+str(orientation)
            check('full_coordinate_regulator_time_'+label,error<mp.mpf('1e-30'),mp.nstr(error,65))
            check('full_coordinate_response_'+label,response_error<mp.mpf('1e-30'),mp.nstr(response_error,65))
            check('compensated_time_equation_'+label,corrected_error<mp.mpf('1e-30'),mp.nstr(corrected_error,65))
            omitted_max=max(omitted_max,abs(raw-original))
            if abs(mp.mpf(ratio))<=mp.mpf('0.5'):
                rem=abs(dj-num(leading)*abs(wv));check('cubic_remainder_control_'+label,rem<=base.hi(remainder)*abs(wv)**3,mp.nstr(rem,65))
            controls.append(dict(ratio=ratio,orientation=orientation,jerk_response=mp.nstr(dj,65),original=mp.nstr(original,65),raw=mp.nstr(raw,65),corrected=mp.nstr(corrected,65)))
            print(json.dumps(dict(stage='coordinate_jerk_control',ratio=ratio,orientation=orientation)),flush=True)
    check('omitted_compensating_jerk_rejected',omitted_max>mp.mpf('1e-25'),mp.nstr(omitted_max,65))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit drift '+name)
    accepted=all(t['passed'] for t in checks)
    return dict(result_id='R4C1-QUARTIC-JERK-TRANSPORT-V2',checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),source_sha256=pins,
        formulas=dict(delta_Ct=str(delta_Ct),jerk_response=str(response),leading_coefficient=str(leading),
        full_initial_jerk='-Ud-(5H-3HB-rp-R*wp/w)*aPsi+2R*partial_z(aPsi)-p*(ayVy/w+trace(ay_hdiag)/2+HB^2-8H*HB-2*(H-HB)*(rp+R*wp/w))'),
        bounds={n:base.pack(v) for n,v in dict(Bprime=norms[0],Bsecond=norms[1],inverse_first=first,inverse_second=second,
        leading_coefficient=coefficient,cubic_remainder=remainder).items()},controls=controls,
        scalar_jerk_cusp_verified=accepted,strong_C4_scalar_compatible=False if accepted else None,
        scope='Registered initial data/gauge; scalar jerk has nonzero abs(w) cusp. Weaker solution existence is not established.',
        initial_acceleration_certificate_unchanged=True,weaker_time_evolution_certified=False,G1_complete=False,physics_pass=False,
        gate_effect='NONE',review_status='DEFERRED',mpmath=mp.__version__,sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','scalar_jerk_cusp_verified')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
