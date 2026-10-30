"""Original Vz/metric forcing and conditional all-frame initial node jets."""
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
PARENT='Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v2_attempt_01/summary.json'
PSHA='d9879aa6c6c5e13ef4a5a7c0a60a54127e6a8d09c6d209976c496ede566fa359'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_VECTOR_NODE_JETS_V1_CONTRACT_2026-10-28.md'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
FORCE='Analysis/MasterTests/outputs/r4c1_quartic_complement_force_v3_attempt_01/summary.json'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
BOUND='Analysis/MasterTests/outputs/r4c1_quartic_scalar_bound_v1_attempt_01/summary.json'
JERK='Analysis/MasterTests/outputs/r4c1_quartic_total_jerk_v1_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
READ=lambda p:json.loads((ROOT/p).read_bytes())
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def verify(pins):
    for path,want in pins.items():
        file=ROOT/path
        if SHA(file.read_bytes())!=want:
            raise ValueError('source drift '+path)
        if Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
            raise ValueError('sidecar drift '+path)


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):
        checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        expressions=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(t) for x in expressions if (t:=s.factor(s.cancel(x)))!=0]
        check(name,not bad,bad)
    def progress(stage,**kw):
        print(json.dumps(dict(stage=stage,**kw)),flush=True)
    if SHA((ROOT/PARENT).read_bytes())!=PSHA:
        raise ValueError('owning receipt drift')
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):
        pins[path]=SHA((ROOT/path).read_bytes())
    verify(pins)
    en=load('node_jets_original',ENGINE);en.setup()
    mp.mp.dps=110;iv.dps=80;body=en.body;cop=body.lift.cop;base=cop.base;ic=base.interval_s
    eta=s.Symbol('eta')
    par={n:s.sympify(t,locals={'eta':eta}).subs(eta,s.Rational(1,4))
         for n,t in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    tree=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in tree.body if isinstance(t,ast.Assign)
              and any(isinstance(v,ast.Name) and v.id=='PARAMS' for v in t.targets))
    shared={v.arg:s.sympify(ast.unparse(v.value)) for v in call.keywords}
    for key,val in shared.items():
        if isinstance(val,s.Float):
            val=s.Rational(val)
            if val.q!=1:raise ValueError('nonintegral shared float')
            shared[key]=val
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
               mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    p0=s.Rational(1,20);rc=s.Rational(1,2);rd=s.Rational(1,8);e=s.Rational(1,500);k=s.Integer(40)
    phase=rc/(1-par['zeta']*rc**2*e**2/2)
    names='ax ay az dx dy dz m mt mz w wt wp v vt vz Z Zd Zp R rp rpp ty typ p H HB U Ud W T q xi C S'
    syms={n:s.Symbol(n,real=True) for n in names.split()}
    ax,ay,az,dx,dy,dz,m,mt,mz,w,wt,wp,v,vt,vz,Z,Zd,Zp,R,rp,rpp,ty,typ,p,H,HB,U,Ud,W,T,q,x,C,S=[syms[n] for n in names.split()]
    fields=[ax,0,0,ay,m,az,0,w,v,rc,0,rc,0,Z,0]
    spatial=[0,0,0,0,mz,0,0,wp,vz,0,0,0,0,Zp,0]
    proper=[dx/2,0,0,dy/2,(mt-R*mz-ay*ty-m*rp)/2,dz/2-m*ty-az*rp,
            0,wt-R*wp+v*ty,vt-R*vz+v*rp,0,phase,rd]
    oldsqrt=body.sqrt;body.sqrt=s.sqrt
    raw=[]
    try:
        vol=s.sqrt(ax*(ay*az-m*m));cc=ay*w*w+2*m*w*v+az*v*v
        L=vol*(body.body(fields,spatial,proper,p,dict(par,A=s.Integer(0)))
               -par['b']*(Zd-R*Zp)*cc*p)
        zeros={m:0,mt:0,mz:0,v:0,vt:0,vz:0}
        initial={ax:1,ay:1,az:1,dx:2*H,dy:2*H,dz:2*H,wt:-HB*w,
                 Z:U*w*w+W*w**4,Zd:Ud*w*w,Zp:(2*U*w+4*W*w**3)*wp,p:p0}
        at=lambda f:f.xreplace(zeros).xreplace(initial)
        rates={ax:2*H,ay:2*H,az:2*H,w:-HB*w,wp:-HB*wp,Z:Ud*w*w,Zp:2*Ud*w*wp}
        for label,coord,vel,deriv in (('h_yz',m,mt,mz),('Vz',v,vt,vz)):
            momentum=s.diff(L,vel).xreplace(zeros)
            dt=at(sum(s.diff(momentum,key)*value for key,value in rates.items()))
            flux=at(s.diff(L,deriv))
            ds=(s.diff(flux,w)*wp-s.diff(flux,wp)*k*k*w+s.diff(flux,R)*rp
                +s.diff(flux,rp)*rpp+s.diff(flux,ty)*typ)
            raw.append(s.cancel(at(s.diff(L,coord))-dt-ds))
            progress('original_row_derived',row=label,operations=int(s.count_ops(raw[-1])))
    finally:body.sqrt=oldsqrt
    mu=par['MU2'];b=par['b'];ss=par['c1']+par['c2']+par['c3']
    den=par['MP2']-mu*(par['c1']+par['c3']+2*par['c3']*w*w-2*par['c4']*(1+w*w)*w*w)
    tyexpr=-mu*(par['c1']+par['c3']+2*par['c3']*w*w)*wp/(s.sqrt(1+w*w)*den)
    Dz=lambda f:s.diff(f,w)*wp-s.diff(f,wp)*k*k*w
    P=mu*ss*(1+w*w)
    tt=par['c4']+(par['c1']-(par['c2']+par['c3'])*w*w)/(1+w*w)
    VP=-mu*((par['c2']+tt)*wp*wp-par['c2']*k*k*w*w)
    A0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*w*w
    AH=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*w*w
    source=mu*w*wp*(HB*A0-H*AH)/(1+w*w)+3*b*p0*U*w**3*wp+5*b*p0*W*w**5*wp
    Rsecond=(VP*R-source-Dz(P)*rp)/P
    prepared=[s.cancel(f.subs({ty:tyexpr,typ:Dz(tyexpr)},simultaneous=True)) for f in raw]
    restricted=[s.cancel(f.subs({rpp:Rsecond},simultaneous=True).subs({R:w*T,rp:q},simultaneous=True)) for f in prepared]
    zero('exact_Vz_node_force',restricted[1].subs(w,0))
    quotient=s.cancel(restricted[1]/w)
    check('Vz_force_quotient_no_node_denominator',s.fraction(quotient)[1].subs(w,0)!=0)
    B=s.Matrix([[s.sympify(t,locals={'w':w}) for t in row] for row in READ(KINETIC)['formulas']['B']])
    bx=(1,6);bz=(4,8)
    zero('complete_Vx_sector_isolation',B.extract(bx,tuple(i for i in range(12) if i not in bx)))
    zero('complete_Vz_sector_isolation',B.extract(bz,tuple(i for i in range(12) if i not in bz)))
    cross=s.zeros(12,1);cross[3]=-b*(U*w*w+W*w**4)*w*w;cross[7]=-b*(U*w*w+W*w**4)*w
    zero('Vx_Vz_scalar_crosses',cross.extract((*bx,*bz),(0,)))
    cusp=s.zeros(12,1);cusp[0]=cusp[5]=-par['A']*p0**3*w**3/2
    cusp[3]=-2*par['A']*p0**3*w**3;cusp[7]=-3*par['A']*p0**3*w*w
    zero('physical_cusp_selected_sector_forcing',cusp.extract((*bx,*bz),(0,)))
    # Cusp is velocity independent in these rows; exact isolation forbids
    # a response from its other metric/Vy components in these sectors.
    Vz_acc=s.cancel((B.extract(bz,bz).inv()*s.Matrix(restricted))[1])
    Vz_acc_over_w=s.cancel(Vz_acc/w)
    check('Vz_acceleration_quotient_no_node_denominator',s.fraction(Vz_acc_over_w)[1].subs(w,0)!=0)
    zero('Vz_acceleration_node_limit',Vz_acc.subs(w,0))
    B0inv=B.subs(w,0).inv()
    for idx in (6,7,8):
        zero('node_frame_inverse_crosses_'+str(idx),s.Matrix([B0inv[idx,j] for j in range(12) if j!=idx]))
    force=READ(FORCE)
    for idx in bx:
        enclosure=cop.unpack(force['analytic_force_bounds'][idx])
        check('reuse_original_force_zero_'+str(idx),base.lo(enclosure)==0 and base.hi(enclosure)==0)
    jerk=READ(JERK)
    check('reuse_exact_Vy_node_source',next(c['passed'] for c in jerk['checks'] if c['name']=='zero_node_frame_force'))
    node_accelerations=B0inv.extract((6,7,8),(6,7,8))*s.Matrix([0,0,restricted[1].subs(w,0)])
    zero('all_frame_initial_node_accelerations',node_accelerations)
    allowed={H,HB,U,Ud,W,w,wp,T,q}
    check('acceleration_quotient_inputs',Vz_acc_over_w.free_symbols<=allowed,
          [str(t) for t in Vz_acc_over_w.free_symbols-allowed])
    check('exact_expressions_no_Float',not bool(Vz_acc_over_w.atoms(s.Float)))
    progress('node_sources_and_full_sector_proved')
    # New symbolic rows versus previously computed original directional AD.
    primary=READ(PRIMARY);loc=dict(par,H=H,H0=HB,zc=U,p=p0,k=k,xi=x)
    f=sum((e*e)**(j+1)*s.sympify(t,locals=loc) for j,t in enumerate(READ(cop.PROOF)['polynomial_pieces']))
    f+=e**6*s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':x})
    Q=lambda a:(2*x-1)*a-2*x*(1-x)*s.diff(a,x)
    JJ=lambda a:4*x*(1-x)*s.diff(a,x,2)+6*(1-2*x)*s.diff(a,x)-4*a
    geometry=base.Eval([C*S*f.subs(x,C*C),k*Q(f).subs(x,C*C),k*k*C*S*JJ(f).subs(x,C*C)])
    original_eval=base.Eval(prepared)
    point=primary['point'];pv=dict(H=mp.mpf(point['H']),HB=en.vals['H0'],U=mp.mpf(point['U']),Ud=mp.mpf(point['Ud']),W=mp.mpf(point['W']))
    comparisons=[]
    for row in force['controls']:
        theta=mp.mpf(row['theta']);wv=mp.cos(theta)/500;wpv=-40*mp.sin(theta)/500
        rv,qv,r2v=geometry.numeric(dict(pv,C=mp.cos(theta),S=mp.sin(theta)))
        predicted=original_eval.numeric(dict(pv,w=wv,wp=wpv,R=rv,rp=qv,rpp=r2v))
        errors=[abs(z-mp.mpf(row['source'][idx]))/(1+abs(z)+abs(mp.mpf(row['source'][idx])))
                for z,idx in zip(predicted,bz)]
        check('original_AD_rows_'+row['theta'][:25],max(errors)<mp.mpf('1e-18'),mp.nstr(max(errors),65))
        comparisons.append(dict(theta=row['theta'],row_errors=[mp.nstr(z,65) for z in errors]))
    # Compare with all14-coordinate physical acceleration, on its own Fourier shift.
    charge=load('node_jets_charge_controls',CHARGE);charge.setup();mp.mp.dps=110
    raw_acc=(B.extract(bz,bz).inv()*s.Matrix(prepared))[1]
    acceleration_eval=base.Eval([raw_acc]);acceleration_controls=[]
    for row in parent['points']:
        theta=mp.mpf(row['theta']);rv,qv=charge.shift_at(theta)
        r2v=40*mp.diff(lambda a:charge.shift_at(a)[1],theta)
        vals=dict(pv,w=mp.cos(theta)/500,wp=-40*mp.sin(theta)/500,R=rv,rp=qv,rpp=r2v)
        predicted=acceleration_eval.numeric(vals)[0];reference=mp.mpf(row['values']['acc'][8])
        error=abs(predicted-reference)/(1+abs(predicted)+abs(reference))
        check('full14_Vz_acceleration_'+row['label'],error<mp.mpf('1e-18'),mp.nstr(error,65))
        acceleration_controls.append(dict(label=row['label'],error=mp.nstr(error,65),predicted=mp.nstr(predicted,65),reference=mp.nstr(reference,65)))
    # Whole registered root box, not merely the nominal numerical representative.
    initial=next(t for t in READ(cop.CERTS) if t['family']=='new_B1_frame' and t['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);u0=hb*ic(p0)+ic(par['beta'])*ic(s.Rational(1,5))/ic(par['K_Q'])
    hbox=iv.mpf([base.lo(hb*ic(s.Rational(49,50))),base.hi(hb*ic(s.Rational(51,50)))])
    ubox=iv.mpf([base.lo(u0*ic(s.Rational(49,50))),base.hi(u0*ic(s.Rational(51,50)))])
    bound=READ(BOUND)
    box=dict(H=hbox,HB=hb,U=ubox,Ud=cop.unpack(force['Ud_box']),W=iv.mpf([30,38]),
             w=base.box(ic(e/2)),wp=base.box(ic(e*k)),
             T=base.box(cop.unpack(bound['bounds']['Tmax'])),q=base.box(cop.unpack(bound['bounds']['Qmax'])))
    force_bound=base.upper(abs(iv.mpf(base.Eval([quotient]).interval(box)[0])))
    acc_bound=base.upper(abs(iv.mpf(base.Eval([Vz_acc_over_w]).interval(box)[0])))
    check('finite_Vz_force_and_acceleration_quotients',all(mp.isfinite(base.hi(z)) for z in (force_bound,acc_bound)))
    # Exact conditional implicit-node chain rule and a rejection of persistence.
    sigma,zd,zdd,Vt,Vtt,Vtz,Vzz=s.symbols('sigma zd zdd Vt Vtt Vtz Vzz',real=True)
    first=s.solve(Vt+sigma*zd,zd)[0]
    second=s.solve(Vtt+2*Vtz*zd+Vzz*zd**2+sigma*zdd,zdd)[0]
    zero('conditional_initial_node_velocity',first.subs(Vt,0))
    zero('conditional_initial_node_acceleration',second.subs({Vt:0,Vtt:0,zd:0}))
    check('both_node_slopes_nonzero',e*k!=0)
    tt,xx,aa,bb=s.symbols('tt xx aa bb',real=True)
    toy_y=sigma*xx+aa*tt**3;toy_z=bb*tt**3;toy_path=-aa*tt**3/sigma
    zero('kinematic_node_is_zero_of_Vy',toy_y.subs(xx,toy_path))
    for order in (0,1,2):
        zero('finite_jets_do_not_detect_later_misalignment_'+str(order),s.diff(toy_z,tt,order).subs(tt,0))
    zero('third_jet_misalignment_nonzero_when_b_nonzero',s.diff(toy_z,tt,3)-6*bb)
    verify(pins)
    return dict(result_id='R4C1-QUARTIC-VECTOR-NODE-JETS-V1',source_sha256=pins,
                checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
                formulas=dict(raw_hyz_force=str(prepared[0]),raw_Vz_force=str(prepared[1]),
                              restricted_Vz_force=str(restricted[1]),Vz_force_over_w=str(quotient),
                              full_Vz_acceleration=str(Vz_acc),Vz_acceleration_over_w=str(Vz_acc_over_w),
                              conditional_node_velocity=str(first),conditional_node_acceleration=str(second)),
                bounds=dict(Vz_force_quotient=base.pack(force_bound),Vz_acceleration_quotient=base.pack(acc_bound)),
                original_source_controls=comparisons,full14_acceleration_controls=acceleration_controls,
                working_digits=110,interval_digits=80,mpmath=mp.__version__,sympy=s.__version__,
                initial_frame_accelerations_at_nodes=[str(s.cancel(z)) for z in node_accelerations],
                interpretation='Exact initial all-frame node jets; implicit motion conditional on an existing C2 continuation',
                alignment_persistence_certified=False,constraint_transport_certified=False,
                time_evolution=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        if (args.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);path=args.output/'summary.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
