"""Exact unreduced kinetic blocks and certified complement; not full admission."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_KINETIC_EXTENSION_V1_CONTRACT_2026-10-27.md'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())


def calculate():
    mp.mp.dps=100;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expression):
        values=list(expression) if isinstance(expression,s.MatrixBase) else [expression]
        bad=[str(t) for x in values if (t:=s.factor(s.cancel(x)))!=0]
        check(name,not bad,bad)
    primary=READ(PRIMARY);pins=dict(primary['source_sha256'])
    pins[PRIMARY]='2df2eb08f06243ca1ef60152a17921d17c7755bbca18fbd59bc33ab27f45acb0'
    for name in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry source drift '+name)
    spec=importlib.util.spec_from_file_location('quartic_kinetic_original',ROOT/ENGINE)
    engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine);engine.setup()
    mp.mp.dps=100;iv.dps=80;body=engine.body;base=body.lift.cop.base
    eta=s.Symbol('eta');par={k:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
                          for k,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    tree=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PARAMS' for t in n.targets))
    shared={k.arg:s.sympify(ast.unparse(k.value)) for k in call.keywords}
    for k,v in shared.items():
        if isinstance(v,s.Float):
            q=s.Rational(v)
            if q.q!=1:raise ValueError('nonintegral shared float')
            shared[k]=q
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    physical_A=par['A'];analytic_par=dict(par,A=s.Integer(0))
    w,wp,Z,Zp,sp,zh=s.symbols('w wp Z Zp sp zh',real=True)
    y=s.symbols('y0:12',real=True);I=s.Integer;rc=s.Rational(1,2);p=s.Rational(1,20)
    q=[I(0)]*15;dq=q.copy()
    for i in (0,3,5):q[i]=I(1)
    q[7]=w;q[9]=q[11]=rc;q[13]=Z;dq[7]=wp;dq[13]=Zp
    previous=body.sqrt;body.sqrt=s.sqrt
    try:
        L=body.body(q,dq,list(y),sp,analytic_par)-par['b']*zh*w*w*sp
        # This initial Y depends on w and sp only, never on any y_j.
        Y=sp*sp*w*w
        zero('cusp_has_no_complement_velocity_derivatives',s.Matrix([s.diff(Y,v) for v in y]))
        Bproper=s.hessian(L,y).applyfunc(s.cancel)
        transform=s.diag(*([s.Rational(1,2)]*6+[I(1)]*6))
        B=(transform*Bproper*transform).applyfunc(s.cancel)
        C=(transform*s.Matrix([s.diff(L,v,sp) for v in y])).applyfunc(s.cancel)
        scalar=s.cancel(s.diff(L,sp,2))
        g=par['b']*w*w
        expectedC=s.zeros(12,1);expectedC[3]=-par['b']*Z*w*w;expectedC[7]=-par['b']*Z*w
        zero('full_scalar_cross_from_original_density',C-expectedC)
        zero('analytic_scalar_diagonal',scalar-par['K_Q']*(1+w*w))
        zero('original_scalar_regulator_cross',s.diff(L,sp,zh)+g)
        zero('regulator_diagonal_zero',s.diff(L,zh,2))
        zero('complement_regulator_cross_zero',s.Matrix([s.diff(L,v,zh) for v in y]))
        check('complement_depends_only_on_frame',set().union(*(v.free_symbols for v in B))<={w})
        check('exact_complement_has_no_Float',not any(v.atoms(s.Float) for v in B))
        zero('exact_complement_symmetry',B-B.T)
    finally:body.sqrt=previous
    a,t=s.symbols('a t',positive=True)
    force=par['K_Q']*(1+a*a)*t*t/2-physical_A*(a*a*t*t)**s.Rational(3,2)
    dpos=s.diff(force,t,2).subs({a:w,t:p})
    zero('full_cusp_diagonal_retained',dpos-(par['K_Q']*(1+w*w)-6*physical_A*p*w**3))
    B0=B.subs(w,0);C0=B0.inv();eigen=B0.eigenvals()
    inertia=[sum(n for value,n in eigen.items() if value.is_positive),sum(n for value,n in eigen.items() if value.is_negative),sum(n for value,n in eigen.items() if value==0)]
    check('complement_node_has_no_zero_eigenvalue',sum(inertia)==12 and inertia[2]==0)
    print(json.dumps(dict(stage='exact_original_kinetic_blocks_derived',inertia=inertia)),flush=True)
    fe=base.Eval(list(B));Civ=[[base.interval_s(C0[i,j]) for j in range(12)] for i in range(12)]
    cnorm=max(sum(abs(C0[i,j]) for j in range(12)) for i in range(12));attempts=[];certified=False
    for n in (16,32,64,128,256):
        worst=iv.mpf(0)
        for j in range(n):
            lo=s.Rational(-1,500)+s.Rational(2*j,500*n);hi=lo+s.Rational(2,500*n)
            domain=iv.mpf([base.lo(base.interval_s(lo)),base.hi(base.interval_s(hi))])
            flat=fe.interval({'w':domain});block=[flat[12*i:12*i+12] for i in range(12)]
            rows=[]
            for i in range(12):
                rows.append(sum(base.upper(abs((1 if i==k else 0)-sum(Civ[i][j1]*block[j1][k] for j1 in range(12)))) for k in range(12)))
            current=max(base.hi(v) for v in rows);worst=base.upper(iv.mpf(max(base.hi(worst),current)))
        certified=base.hi(worst)<1
        inverse=base.upper(base.interval_s(cnorm)/(1-worst)) if certified else None
        attempts.append(dict(partitions=n,contraction=base.pack(worst),inverse_bound=base.pack(inverse) if inverse is not None else None,certified=bool(certified)))
        print(json.dumps(dict(stage='uniform_complement_attempt',partitions=n,certified=bool(certified))),flush=True)
        if certified:break
    check('uniform_complement_inverse_whole_profile',certified,attempts[-1])
    U,W=s.symbols('U W',real=True);profile=U*w*w+W*w**4
    cbar=s.zeros(12,1);cbar[3]=-profile;cbar[7]=-w*(U+W*w*w)
    zero('scalar_cross_regular_quotient',C.subs(Z,profile)-g*cbar)
    zero('scalar_cross_quotient_zero_at_node',cbar.subs(w,0))
    # Universal block solution: verify the equations without presuming a force quotient limit.
    bv,cv,dv,gv,fy,fp,fz=s.symbols('B C d g fy fpsi fZ',nonzero=True)
    ap=-fz/gv;ay=(fy-cv*ap)/bv;az=(cv*ay+dv*ap-fp)/gv
    zero('Schur_complement_equation',bv*ay+cv*ap-fy)
    zero('Schur_scalar_equation',cv*ay+dv*ap-gv*az-fp)
    zero('Schur_regulator_equation',-gv*ap-fz)
    zero('Schur_determinant_structure',s.Matrix([[bv,cv,0],[cv,dv,-gv],[0,-gv,0]]).det()+bv*gv*gv)
    engine.H=mp.mpf(primary['point']['H']);engine.U=mp.mpf(primary['point']['U']);engine.Ud=mp.mpf(primary['point']['Ud'])
    wpnt=mp.mpf(primary['point']['W']);points=[]
    for ratio in (-1,s.Rational(-1,2),0,s.Rational(1,2),1):
        value=mp.mpf(str(s.N(ratio/500,95)));angle=mp.acos(value*500)
        state,_,_,_=engine.initial(angle)
        state[7]=value;state[13]=engine.U*value**2+wpnt*value**4
        state[41]=2*engine.U*value*state[35]+4*wpnt*value**3*state[35]
        state[27]=engine.Ud*value**2
        # The Hessian is independent of affine shift/spatial offsets; keep the original nonzero controls.
        flat=fe.numeric({'w':value});expected=mp.matrix(14)
        for i in range(12):
            for j in range(12):expected[i,j]=flat[12*i+j]
        bp=engine.par['b'];Kp=engine.par['K_Q'];Ap=engine.par['A'];pnum=state[26]
        expected[3,12]=expected[12,3]=-bp*state[13]*value**2
        expected[7,12]=expected[12,7]=-bp*state[13]*value
        expected[12,12]=Kp*(1+value**2)-6*Ap*pnum*abs(value)**3
        expected[12,13]=expected[13,12]=-bp*value**2
        for step in ('1e-20','1e-26'):
            columns=[]
            for j in range(14):
                seed=[mp.mpf(0)]*48;seed[14+j]=1
                columns.append(engine.hv(state,seed,mp.mpf(step))[14:28,0])
            measured=mp.matrix([[columns[j][i] for j in range(14)] for i in range(14)])
            error=engine.relative(measured,expected)
            check('original_full_Hessian_'+str(ratio)+'_'+step,error<mp.mpf('1e-18'),mp.nstr(error,60))
            points.append(dict(ratio=str(ratio),step=step,error=mp.nstr(error,60)))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit source drift '+name)
    return dict(result_id='R4C1-QUARTIC-KINETIC-EXTENSION-V1',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
        source_sha256=pins,formulas=dict(B=[[str(B[i,j]) for j in range(12)] for i in range(12)],
        B0_inverse=[[str(C0[i,j]) for j in range(12)] for i in range(12)],C=[str(v) for v in C],g=str(g),
        scalar_diagonal='K_Q*(1+w^2)-6*A*p*abs(w)^3',cross_quotient=[str(v) for v in cbar],
        Schur='aPsi=-fZ/g; ay=B^-1*(fy-C*aPsi); aZ=(C.T*ay+d*aPsi-fpsi)/g'),
        attempts=attempts,unreduced_complement_inertia=inertia,original_operator_controls=points,
        full_acceleration_extension_certified=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
        interpretation='Uniform unreduced complement and exact kinetic normal form only; full force quotients and persistence remain open',
        mpmath=mp.__version__,sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','full_acceleration_extension_certified')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
