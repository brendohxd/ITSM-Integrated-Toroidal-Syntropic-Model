"""Original analytic complement Euler forces with real interval directional AD."""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_ANALYTIC_FORCE_V1_CONTRACT_2026-10-27.md'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_ANALYTIC_FORCE_V1_COMPUTATIONAL_ADDENDUM_2026-10-27.md'
PRIOR='Analysis/MasterTests/outputs/r4c1_quartic_cusp_remainder_v1_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())


class Dual:
    """One real direction, evaluated in mp or outward iv scalar arithmetic."""
    __slots__=('v','d')
    def __init__(self,value,direction=0):self.v=value;self.d=direction
    @staticmethod
    def cast(x):return x if isinstance(x,Dual) else Dual(x,0)
    @staticmethod
    def align(a,b):
        b=Dual.cast(b)
        if any(hasattr(v,'_mpi_') for v in (a.v,a.d,b.v,b.d)):
            return Dual(mp.iv.mpf(a.v),mp.iv.mpf(a.d)),Dual(mp.iv.mpf(b.v),mp.iv.mpf(b.d))
        return a,b
    def __add__(self,x):
        a,x=self.align(self,x);return Dual(a.v+x.v,a.d+x.d)
    __radd__=__add__
    def __neg__(self):return Dual(-self.v,-self.d)
    def __sub__(self,x):return self+-self.cast(x)
    def __rsub__(self,x):return self.cast(x)+-self
    def __mul__(self,x):
        a,x=self.align(self,x);return Dual(a.v*x.v,a.d*x.v+a.v*x.d)
    __rmul__=__mul__
    def __truediv__(self,x):
        a,x=self.align(self,x);v=a.v/x.v;return Dual(v,(a.d-v*x.d)/x.v)
    def __rtruediv__(self,x):return self.cast(x)/self
    def __pow__(self,e):
        if e==0:return Dual(1,0)
        if any(hasattr(v,'_mpi_') for v in (self.v,self.d)):e=mp.iv.mpf(e)
        v=self.v**e
        return Dual(v,0 if self.d==0 else e*self.v**(e-1)*self.d)
    def __eq__(self,x):
        x=self.cast(x);return bool(self.v==x.v and self.d==x.d)
    def __bool__(self):return not self==0


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    pins=dict(READ(PRIOR)['source_sha256']);pins[PRIOR]='c662c4261cd6496b053979ab6927b7be7fec87520556d7cbffadf453a883879f'
    for name in (CONTRACT,ADDENDUM,'Theory/Gates/RES-001/RES001_R4C1_QUARTIC_COMPLEMENT_FORCE_V2_IMPLEMENTATION_NOTE_2026-10-27.md','Analysis/MasterTests/test_01_r4c1_quartic_complement_force_v1.py',Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry source drift '+name)
    spec=importlib.util.spec_from_file_location('analytic_force_original',ROOT/ENGINE)
    en=importlib.util.module_from_spec(spec);spec.loader.exec_module(en);en.setup()
    mp.mp.dps=110;iv.dps=80;body=en.body;cop=body.lift.cop;base=cop.base
    original=body.body;tree=ast.parse(inspect.getsource(original));function=tree.body[0]
    force=next(t for t in function.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='force' for z in t.targets))
    expected=ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body
    if ast.dump(force.value)!=ast.dump(expected):raise ValueError('original force assignment changed')
    force.value=copy.deepcopy(force.value.left);function.name='body_analytic_partition'
    ast.fix_missing_locations(tree);exec(compile(tree,'<pinned-original-analytic-partition>','exec'),body.__dict__)
    analytic=body.body_analytic_partition
    check('exact_original_AST_partition_verified',True,SHA(ast.dump(tree).encode()))
    def gradient_direction(state,direction):
        tape=body.Tape();variables=[tape.var(Dual(v,d)) for v,d in zip(state,direction)]
        L,_=en.density(variables);grad=tape.grad(L,variables)
        return [Dual.cast(v) for v in grad]
    def forcing(state,vd,dd,Sdd):
        Wt=state[14:28]+[0]*14+vd+[0]*6;Wz=state[28:42]+vd+dd+state[45:48]+Sdd
        gt=gradient_direction(state,Wt);gz=gradient_direction(state,Wz)
        return [gt[i].v-gt[14+i].d-gz[28+i].d for i in range(12)]
    eta=s.Symbol('eta');par={n:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
        for n,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    bg=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in bg.body if isinstance(t,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='PARAMS' for v in t.targets))
    shared={v.arg:s.sympify(ast.unparse(v.value)) for v in call.keywords}
    for key,v in shared.items():
        if isinstance(v,s.Float):
            value=s.Rational(v)
            if value.q!=1:raise ValueError('nonintegral shared float')
            shared[key]=value
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    H,HB,U,Ud,W,x,C,S,w,wp,qn=s.symbols('H HB U Ud W xi C S w wp qn',real=True)
    p=s.Rational(1,20);e=s.Rational(1,500);k=s.Integer(40);alpha=e*e;rc=s.Rational(1,2);rd=s.Rational(1,8)
    loc=dict(par,H=H,H0=HB,zc=U,p=p,k=k,xi=x)
    primary=READ(PRIMARY)
    f=sum(alpha**(j+1)*s.sympify(t,locals=loc) for j,t in enumerate(READ(cop.PROOF)['polynomial_pieces']))
    f+=alpha**3*s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':x})
    Q=lambda t:(2*x-1)*t-2*x*(1-x)*s.diff(t,x)
    fields=base.Eval([C*S*f.subs(x,C*C),k*Q(f).subs(x,C*C)])
    velocity=base.Eval([s.sympify(primary['formulas']['velocity'],locals={str(z):z for z in (H,HB,U,qn)})])
    ss=par['c1']+par['c2']+par['c3'];mu=par['MU2'];b=par['b']
    T=par['c4']+(par['c1']-(par['c2']+par['c3'])*w*w)/(1+w*w)
    P=mu*ss*(1+w*w);Pp=s.diff(P,w)*wp
    pot=-mu*((par['c2']+T)*wp*wp-par['c2']*k*k*w*w)
    a0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*w*w
    ah=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*w*w
    src=mu*w*wp*(HB*a0-H*ah)/(1+w*w)+3*b*p*U*w**3*wp+5*b*p*W*w**5*wp
    den=par['MP2']-mu*(par['c1']+par['c3']+2*par['c3']*w*w-2*par['c4']*(1+w*w)*w*w)
    ty=-mu*(par['c1']+par['c3']+2*par['c3']*w*w)*wp/(s.sqrt(1+w*w)*den)
    typ=s.diff(ty,w)*wp-s.diff(ty,wp)*k*k*w
    geom=base.Eval([P,Pp,pot,src,ty,typ])
    point=primary['point'];num=lambda z:mp.mpf(str(s.N(z,105)))
    en.H=mp.mpf(point['H']);en.U=mp.mpf(point['U']);en.Ud=mp.mpf(point['Ud']);wn=mp.mpf(point['W'])
    pointparams={str(H):en.H,str(HB):en.vals['H0'],str(U):en.U,str(W):wn}
    def newshift(theta):
        return tuple(fields.numeric(dict(pointparams,C=mp.cos(theta),S=mp.sin(theta))))
    en.shift=newshift
    controls=[]
    angles=[mp.mpf(0),mp.pi/4,3*mp.pi/4,mp.pi]+[node*mp.pi/2+side*mp.mpf(delta) for node in (1,3) for delta in ('0.01','0.001') for side in (-1,1)]
    for angle in angles:
        state,vd,dd,Sdd=en.initial(angle);wv,wv1=state[7],state[35];wv2=dd[7]
        state[13]=en.U*wv**2+wn*wv**4;state[41]=(2*en.U*wv+4*wn*wv**3)*wv1
        dd[13]=2*en.U*(wv1**2+wv*wv2)+wn*(12*wv**2*wv1**2+4*wv**3*wv2)
        body.body=analytic;actual=forcing(state,vd,dd,Sdd)
        for step in ('1e-20','1e-26'):
            _,grad=en.gradient(state);ht=en.hv(state,state[14:28]+[mp.mpf(0)]*14+vd+[mp.mpf(0)]*6,mp.mpf(step))
            hz=en.hv(state,state[28:42]+vd+dd+state[45:48]+Sdd,mp.mpf(step))
            reference=[grad[i]-ht[14+i]-hz[28+i] for i in range(12)]
            error=max(abs(a-z)/(1+abs(a)+abs(z)) for a,z in zip(actual,reference))
            check('directional_original_control_'+mp.nstr(angle,25)+'_'+step,error<mp.mpf('1e-18'),mp.nstr(error,65))
        body.body=original;_,physical_grad=en.gradient(state);body.body=analytic;_,analytic_grad=en.gradient(state)
        cusp=[mp.mpf(0)]*12;ac=en.par['A']*state[26]**3
        cusp[0]=cusp[5]=-ac*abs(wv)**3/2;cusp[3]=-2*ac*abs(wv)**3;cusp[7]=-3*ac*wv*abs(wv)
        error=max(abs(physical_grad[i]-analytic_grad[i]-cusp[i])/(1+abs(cusp[i])) for i in range(12))
        check('physical_partition_control_'+mp.nstr(angle,25),error<mp.mpf('1e-18'),mp.nstr(error,65))
        controls.append(dict(theta=mp.nstr(angle,65),source=[mp.nstr(v,65) for v in actual]))
    ic=base.interval_s;initial=next(t for t in READ(cop.CERTS) if t['family']=='new_B1_frame' and t['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);pp,ee,kk=ic(p),ic(e),ic(k)
    u0=hb*pp+ic(par['beta'])*ic(s.Rational(1,5))/ic(par['K_Q'])
    hbox=iv.mpf([base.lo(hb*ic(s.Rational(49,50))),base.hi(hb*ic(s.Rational(51,50)))])
    ubox=iv.mpf([base.lo(u0*ic(s.Rational(49,50))),base.hi(u0*ic(s.Rational(51,50)))])
    box=dict(H=hbox,HB=hb,U=ubox,W=iv.mpf([30,38]));errors=primary['shift_errors'][0]
    rerr,qerr=[cop.unpack(z) for z in errors]
    nq=fields.interval(dict(box,C=iv.mpf(0),S=iv.mpf(1)))[1]+base.box(qerr)
    udbox=velocity.interval(dict(box,qn=nq))[0]
    phase=ic(rc)/(1-ic(par['zeta'])*ic(rc)**2*ee**2/2)
    en.par={key:ic(value) for key,value in par.items()};body.body=analytic
    def box_state(angle):
        cc,st=iv.cos(angle),iv.sin(angle);wv=ee*cc;wv1=-kk*ee*st;wv2=-kk*kk*wv
        rr,qr=fields.interval(dict(box,C=cc,S=st));rr+=base.box(rerr);qr+=base.box(qerr)
        P0,P1,V0,F0,ty0,typ0=geom.interval(dict(box,w=wv,wp=wv1))
        r2=(V0*rr-F0-P1*qr)/P0
        q=[iv.mpf(0) for _ in range(14)];v=q.copy();d=q.copy();dd=q.copy();vd=q.copy()
        for i in (0,3,5):q[i]=iv.mpf(1);v[i]=2*hbox
        q[7]=wv;q[9]=q[11]=ic(rc);q[13]=ubox*wv**2+box['W']*wv**4
        v[7]=-hb*wv;v[10]=phase;v[11]=ic(rd);v[12]=pp;v[13]=udbox*wv**2
        d[7]=wv1;d[13]=(2*ubox*wv+4*box['W']*wv**3)*wv1
        dd[7]=wv2;dd[13]=2*ubox*(wv1**2+wv*wv2)+box['W']*(12*wv**2*wv1**2+4*wv**3*wv2)
        vd[7]=-hb*wv1;vd[13]=2*udbox*wv*wv1
        return q+v+d+[iv.mpf(0),iv.mpf(0),rr]+[iv.mpf(0),ty0,qr],vd,dd,[iv.mpf(0),typ0,r2]
    attempts=[];bounds=None
    try:
        for n in (16,32,64,128,256):
            candidates=[iv.mpf(0) for _ in range(12)]
            for j in range(n):
                angle=iv.mpf([base.lo(2*iv.pi*j/n),base.hi(2*iv.pi*(j+1)/n)])
                values=forcing(*box_state(angle))
                candidates=[base.upper(iv.mpf(max(base.hi(old),base.hi(abs(value))))) for old,value in zip(candidates,values)]
            finite=all(mp.isfinite(base.hi(v)) for v in candidates)
            contained=all(abs(mp.mpf(v))<=base.hi(candidates[i]) for row in controls for i,v in enumerate(row['source']))
            attempts.append(dict(partitions=n,finite=bool(finite),controls_contained=bool(contained)))
            print(json.dumps(dict(stage='whole_circle_analytic_force_bound',partitions=n,finite=bool(finite),controls_contained=bool(contained))),flush=True)
            if finite and contained:bounds=candidates;break
    finally:body.body=original
    check('whole_circle_uniform_complement_forces',bounds is not None,attempts)
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit source drift '+name)
    return dict(result_id='R4C1-QUARTIC-COMPLEMENT-FORCE-V2',checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),source_sha256=pins,
        attempts=attempts,analytic_force_bounds=[base.pack(v) for v in bounds] if bounds is not None else None,
        Ud_box=base.pack(udbox),controls=controls,full_acceleration_extension_certified=False,scalar_analytic_quotient_bound_certified=False,
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',mpmath=mp.__version__,sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','scalar_analytic_quotient_bound_certified')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
