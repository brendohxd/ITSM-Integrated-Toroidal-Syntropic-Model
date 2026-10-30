"""Total initial jerk quotient and weak interface terms, not an evolved solution."""
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
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_GRADED_TRANSPORT_V1_CONTRACT_2026-10-27.md'
METHOD='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_TOTAL_JERK_V1_METHOD_2026-10-28.md'
PARENT='Analysis/MasterTests/outputs/r4c1_quartic_jerk_transport_v2_attempt_01/summary.json'
FORCE='Analysis/MasterTests/outputs/r4c1_quartic_complement_force_v3_attempt_01/summary.json'
BOUND='Analysis/MasterTests/outputs/r4c1_quartic_scalar_bound_v1_attempt_01/summary.json'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        rows=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(z) for v in rows if (z:=s.factor(s.cancel(v)))!=0];check(name,not bad,bad)
    def progress(stage,**data):print(json.dumps(dict(stage=stage,**data)),flush=True)
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]='426c6e781f7f113771d9afd92a9fc83aa968409246360a7f367ab8f1ab252e63'
    for name in (CONTRACT,METHOD,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry source drift '+name)
    spec=importlib.util.spec_from_file_location('total_jerk_original',ROOT/ENGINE)
    en=importlib.util.module_from_spec(spec);spec.loader.exec_module(en);en.setup()
    mp.mp.dps=110;iv.dps=80;bdy=en.body;cop=bdy.lift.cop;base=cop.base;ic=base.interval_s
    eta=s.Symbol('eta');par={n:s.sympify(t,locals={'eta':eta}).subs(eta,s.Rational(1,4)) for n,t in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    bg=ast.parse((ROOT/bdy.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in bg.body if isinstance(t,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='PARAMS' for v in t.targets))
    shared={v.arg:s.sympify(ast.unparse(v.value)) for v in call.keywords}
    for key,v in shared.items():
        if isinstance(v,s.Float):
            v=s.Rational(v)
            if v.q!=1:raise ValueError('nonintegral shared float')
            shared[key]=v
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    A=par['A'];analytic_par=dict(par,A=s.Integer(0));p0=s.Rational(1,20);rc=s.Rational(1,2);rd=s.Rational(1,8);e=s.Rational(1,500);k=s.Integer(40)
    phase=rc/(1-par['zeta']*rc**2*e**2/2)
    names='ax ay az dx dy dz m mt mz w wt wp v vt vz Z Zd Zp R rp rpp ty typ p H HB U Ud W T q xi C S'
    u={n:s.Symbol(n,real=True) for n in names.split()}
    ax,ay,az,dx,dy,dz,m,mt,mz,w,wt,wp,v,vt,vz,Z,Zd,Zp,R,rp,rpp,ty,typ,p,H,HB,U,Ud,W,T,q,x,C,S=[u[n] for n in names.split()]
    fields=[ax,0,0,ay,m,az,0,w,v,rc,0,rc,0,Z,0]
    spatial=[0,0,0,0,mz,0,0,wp,vz,0,0,0,0,Zp,0]
    proper=[dx/2,0,0,dy/2,(mt-R*mz-ay*ty-m*rp)/2,dz/2-m*ty-az*rp,
            0,wt-R*wp+v*ty,vt-R*vz+v*rp,0,phase,rd]
    oldsqrt=bdy.sqrt;bdy.sqrt=s.sqrt
    try:
        vol=s.sqrt(ax*(ay*az-m*m));c=ay*w*w+2*m*w*v+az*v*v
        L=vol*(bdy.body(fields,spatial,proper,p,analytic_par)-par['b']*(Zd-R*Zp)*c*p)
        zero_fields={m:0,mt:0,mz:0,v:0,vt:0,vz:0}
        initial={ax:1,ay:1,az:1,dx:2*H,dy:2*H,dz:2*H,wt:-HB*w,
                 Z:U*w*w+W*w**4,Zd:Ud*w*w,Zp:(2*U*w+4*W*w**3)*wp,p:p0}
        at=lambda expr:expr.xreplace(zero_fields).xreplace(initial)
        Pi=s.diff(L,wt).xreplace(zero_fields)
        rates={ax:2*H,ay:2*H,az:2*H,w:-HB*w,wp:-HB*wp,Z:Ud*w*w,Zp:2*Ud*w*wp}
        dt=at(sum(s.diff(Pi,key)*value for key,value in rates.items()))
        flux=at(s.diff(L,wp))
        ds=s.diff(flux,w)*wp-s.diff(flux,wp)*k*k*w+s.diff(flux,R)*rp+s.diff(flux,rp)*rpp+s.diff(flux,ty)*typ
        raw=s.cancel(at(s.diff(L,w))-dt-ds)
    finally:bdy.sqrt=oldsqrt
    progress('original_analytic_frame_source_built',operations=int(s.count_ops(raw)))
    mu=par['MU2'];b=par['b'];ss=par['c1']+par['c2']+par['c3']
    den=par['MP2']-mu*(par['c1']+par['c3']+2*par['c3']*w*w-2*par['c4']*(1+w*w)*w*w)
    tyexpr=-mu*(par['c1']+par['c3']+2*par['c3']*w*w)*wp/(s.sqrt(1+w*w)*den)
    Dz=lambda f:s.diff(f,w)*wp-s.diff(f,wp)*k*k*w
    P=mu*ss*(1+w*w);PP=Dz(P)
    ft=par['c4']+(par['c1']-(par['c2']+par['c3'])*w*w)/(1+w*w)
    VP=-mu*((par['c2']+ft)*wp*wp-par['c2']*k*k*w*w)
    a0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*w*w
    ah=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*w*w
    source=mu*w*wp*(HB*a0-H*ah)/(1+w*w)+3*b*p0*U*w**3*wp+5*b*p0*W*w**5*wp
    Rsecond=(VP*R-source-PP*rp)/P
    restricted=s.cancel(raw.subs({ty:tyexpr,typ:Dz(tyexpr),rpp:Rsecond},simultaneous=True).subs({R:w*T,rp:q},simultaneous=True))
    divided=s.cancel(restricted/w)
    zero('exact_frame_force_odd',restricted.subs(w,-w)+restricted)
    zero('divided_force_even',divided.subs(w,-w)-divided)
    check('no_remaining_node_denominator',s.fraction(divided)[1].subs(w,0)!=0)
    check('exact_divided_force_no_Float',not bool(divided.atoms(s.Float)))
    zero('zero_node_frame_force',restricted.subs(w,0))
    allowed={H,HB,U,Ud,W,w,wp,T,q}
    check('divided_force_inputs',divided.free_symbols<=allowed,[str(v) for v in divided.free_symbols-allowed])
    kinetic=READ(KINETIC);B=s.Matrix([[s.sympify(t,locals={'w':w}) for t in row] for row in kinetic['formulas']['B']])
    sector=(0,3,5,7);other=tuple(i for i in range(12) if i not in sector)
    zero('complete_kinetic_sector_isolation',B.extract(sector,other))
    signs=s.diag(1,-1,1,1,-1,1,1,-1,1,1,1,1)
    zero('kinetic_orientation_conjugation',B.subs(w,-w)-signs*B*signs)
    C0=B.subs(w,0).inv();zero('node_inverse_Vy_metric_crosses',s.Matrix([C0[7,j] for j in (0,3,5)]))
    primary=READ(PRIMARY);force=READ(FORCE);bound=READ(BOUND)
    loc=dict(par,H=H,H0=HB,zc=U,p=p0,k=k,xi=x)
    f=sum((e*e)**(j+1)*s.sympify(t,locals=loc) for j,t in enumerate(READ(cop.PROOF)['polynomial_pieces']))
    f+=e**6*s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':x})
    Q=lambda f:(2*x-1)*f-2*x*(1-x)*s.diff(f,x)
    J=lambda f:4*x*(1-x)*s.diff(f,x,2)+6*(1-2*x)*s.diff(f,x)-4*f
    Rfunctions=base.Eval([C*S*f.subs(x,C*C),k*Q(f).subs(x,C*C),k*k*C*S*J(f).subs(x,C*C)])
    raw_eval=base.Eval([raw.subs({ty:tyexpr,typ:Dz(tyexpr)},simultaneous=True)])
    point=primary['point'];pv=dict(H=mp.mpf(point['H']),HB=en.vals['H0'],U=mp.mpf(point['U']),Ud=mp.mpf(point['Ud']),W=mp.mpf(point['W']))
    controls=[]
    for row in force['controls']:
        theta=mp.mpf(row['theta']);wv=mp.cos(theta)/500;wpv=-40*mp.sin(theta)/500
        rv,qv,r2v=Rfunctions.numeric(dict(pv,C=mp.cos(theta),S=mp.sin(theta)))
        predicted=raw_eval.numeric(dict(pv,w=wv,wp=wpv,R=rv,rp=qv,rpp=r2v))[0];reference=mp.mpf(row['source'][7])
        err=abs(predicted-reference)/(1+abs(predicted)+abs(reference))
        check('independent_full_generator_'+row['theta'][:28],err<mp.mpf('1e-18'),mp.nstr(err,65))
        controls.append(dict(theta=row['theta'],predicted=mp.nstr(predicted,65),reference=row['source'][7],error=mp.nstr(err,65)))
    initial=next(t for t in READ(cop.CERTS) if t['family']=='new_B1_frame' and t['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);pp=ic(p0);ee=ic(e);kk=ic(k);radius=ee/2;sig=ee*kk
    u0=hb*pp+ic(par['beta'])*ic(s.Rational(1,5))/ic(par['K_Q'])
    hbox=iv.mpf([base.lo(hb*ic(s.Rational(49,50))),base.hi(hb*ic(s.Rational(51,50)))])
    ubox=iv.mpf([base.lo(u0*ic(s.Rational(49,50))),base.hi(u0*ic(s.Rational(51,50)))])
    box=dict(H=hbox,HB=hb,U=ubox,Ud=cop.unpack(force['Ud_box']),W=iv.mpf([30,38]),w=base.box(radius),wp=base.box(sig),
        T=base.box(cop.unpack(bound['bounds']['Tmax'])),q=base.box(cop.unpack(bound['bounds']['Qmax'])))
    fquotient=base.upper(abs(iv.mpf(base.Eval([divided]).interval(box)[0])))
    inv=cop.unpack(kinetic['attempts'][-1]['inverse_bound']);inv1=cop.unpack(parent['bounds']['inverse_first'])
    apmax=cop.unpack(bound['bounds']['aPsi']);ayanamax=cop.unpack(bound['bounds']['complement_analytic_acceleration'])
    ayfull=cop.unpack(bound['bounds']['complement_full_acceleration']);Qmax=cop.unpack(bound['bounds']['Qmax'])
    Tmax=cop.unpack(bound['bounds']['Tmax']);Tp=cop.unpack(bound['bounds']['Tprime']);R2=cop.unpack(bound['bounds']['Rsecond']);Rmax=cop.unpack(bound['bounds']['Rmax'])
    umax=base.upper(abs(ubox));wmax=iv.mpf(38);hmax=base.upper(abs(hbox));hbmax=base.upper(abs(hb));udmax=base.upper(abs(box['Ud']))
    Zmax=(umax+wmax*radius**2)*radius**2
    diagforces=sum(base.upper(abs(cop.unpack(force['analytic_force_bounds'][j]))) for j in (0,3,5))
    velocity_quotient=base.upper(inv*(fquotient+ic(b)*Zmax*apmax)+inv1*(diagforces+ic(b)*Zmax*radius**2*apmax))
    apzmax=base.upper(2*wmax*ee*sig+pp*(R2+Tp*sig+Tmax*kk**2*ee))
    common=udmax+(5*hmax+3*hbmax+Qmax+Tmax*sig)*apmax+2*Rmax*apzmax
    geometry=hbmax**2+8*hmax*hbmax+2*(hmax+hbmax)*(Qmax+Tmax*sig)
    jerk_analytic=base.upper(common+pp*(velocity_quotient+3*ayanamax/2+geometry))
    cusp_coefficient=cop.unpack(parent['bounds']['leading_coefficient']);cusp_remainder=cop.unpack(parent['bounds']['cubic_remainder'])
    jerk_near=base.upper(jerk_analytic+base.upper(cusp_coefficient)*radius+cusp_remainder*radius**3)
    jerk_away=base.upper(common+pp*(ayfull/(ee/4)+3*ayfull/2+geometry))
    check('finite_total_jerk_bounds',all(mp.isfinite(base.hi(t)) and base.lo(t)>0 for t in (fquotient,velocity_quotient,jerk_near,jerk_away)))
    # Exact actual cusp component, including every metric response in its isolated sector.
    Bs=B.extract(sector,sector);fsp=s.Matrix([-A*p0**3*w**3/2,-2*A*p0**3*w**3,-A*p0**3*w**3/2,-3*A*p0**3*w*w])
    cusp_vector=Bs.inv()*fsp
    positive=s.cancel(-p0*(cusp_vector[3]/w+(cusp_vector[0]+cusp_vector[1]+cusp_vector[2])/2))
    analytic_coefficient=s.cancel(positive/w)
    zero('actual_cusp_coefficient_even',analytic_coefficient.subs(w,-w)-analytic_coefficient)
    leading=s.cancel(analytic_coefficient.subs(w,0))
    zero('actual_cusp_leading_coefficient',leading-s.Rational(9,560000))
    check('actual_cusp_no_node_denominator',s.fraction(analytic_coefficient)[1].subs(w,0)!=0)
    kernel=base.Eval([positive,s.diff(positive,w),s.diff(positive,w,2)])
    mp.mp.dps=90;kn=mp.mpf(40);en0=mp.mpf(1)/500;leadn=mp.mpf(9)/560000
    segments=((mp.mpf(0),mp.pi/2,1),(mp.pi/2,3*mp.pi/2,-1),(3*mp.pi/2,2*mp.pi,1))
    weak_controls=[];missing_max=mp.mpf(0)
    for name,test,test2 in [('constant',lambda t:mp.mpf(1),lambda t:mp.mpf(0)),('cos2',lambda t:mp.cos(2*t),lambda t:-4*mp.cos(2*t))]:
        def left(theta,sign):return sign*kernel.numeric({'w':en0*mp.cos(theta)})[0]*test2(theta)
        def regular(theta,sign):
            vals=kernel.numeric({'w':en0*mp.cos(theta)});wtheta=-en0*mp.sin(theta);wtheta2=-en0*mp.cos(theta)
            return sign*(vals[2]*wtheta*wtheta+vals[1]*wtheta2)*test(theta)
        lhs=kn*sum(mp.quad(lambda t:left(t,sign),[a,z]) for a,z,sign in segments)
        rhs_regular=kn*sum(mp.quad(lambda t:regular(t,sign),[a,z]) for a,z,sign in segments)
        jump=2*kn*en0*leadn*(test(mp.pi/2)+test(3*mp.pi/2))
        error=abs(lhs-rhs_regular-jump)/(1+abs(lhs)+abs(rhs_regular)+abs(jump))
        check('weak_interface_'+name,error<mp.mpf('1e-30'),mp.nstr(error,65));missing_max=max(missing_max,abs(lhs-rhs_regular))
        weak_controls.append(dict(test=name,lhs=mp.nstr(lhs,65),regular=mp.nstr(rhs_regular,65),jump=mp.nstr(jump,65),error=mp.nstr(error,65)))
    check('omitted_node_jumps_rejected',missing_max>mp.mpf('1e-25'),mp.nstr(missing_max,65))
    jump_exact=s.cancel(2*k*e*leading);zero('normal_weak_jump_coefficient',jump_exact-s.Rational(9,3500000))
    zero('weighted_delta_coefficient_vanishes',(b*w*w).subs(w,0)*jump_exact)
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit source drift '+name)
    accepted=all(t['passed'] for t in checks)
    return dict(result_id='R4C1-QUARTIC-TOTAL-JERK-V1',checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),source_sha256=pins,
        formulas=dict(original_frame_force=str(raw),divided_analytic_frame_force=str(divided),actual_cusp_positive_branch=str(positive),
        normal_delta_coefficient=str(jump_exact)),controls=controls,weak_controls=weak_controls,
        bounds={n:base.pack(t) for n,t in dict(divided_frame_force=fquotient,analytic_frame_acceleration_quotient=velocity_quotient,
        aPsi_normal_derivative=apzmax,analytic_jerk_near=jerk_analytic,total_jerk_near=jerk_near,total_jerk_away=jerk_away).items()},
        total_initial_jerk_extension_certified=accepted,initial_spatial_jerk_H1=accepted,initial_spatial_jerk_H2=False if accepted else None,
        constraint_transport_certified=False,time_evolution_certified=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
        scope='Bounded continuous locally Lipschitz initial jerk and its explicit weak interface; not a weak evolution theorem',mpmath=mp.__version__,sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','total_initial_jerk_extension_certified')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
