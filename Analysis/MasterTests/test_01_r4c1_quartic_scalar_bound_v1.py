"""Uniform initial acceleration bound; no temporal admission or IVP claim."""
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
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_ANALYTIC_FORCE_V1_CONTRACT_2026-10-27.md'
METHOD='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_SCALAR_BOUND_V1_METHOD_2026-10-27.md'
FORCE='Analysis/MasterTests/outputs/r4c1_quartic_complement_force_v3_attempt_01/summary.json'
SCALAR='Analysis/MasterTests/outputs/r4c1_quartic_scalar_quotient_v1_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
CUSP='Analysis/MasterTests/outputs/r4c1_quartic_cusp_remainder_v1_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        z=s.factor(s.cancel(expr));check(name,z==0,str(z))
    def progress(stage,**data):print(json.dumps(dict(stage=stage,**data)),flush=True)
    force=READ(FORCE);pins=dict(force['source_sha256']);pins[FORCE]='41d889e9a55a2a6f35c919c23c97c4b764094ea0c8c25b17ece4c6a4a3ddda61'
    for name in (CONTRACT,METHOD,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry drift '+name)
    spec=importlib.util.spec_from_file_location('scalar_bound_original',ROOT/ENGINE)
    en=importlib.util.module_from_spec(spec);spec.loader.exec_module(en);en.setup()
    mp.mp.dps=110;iv.dps=80;cop=en.body.lift.cop;base=cop.base;ic=base.interval_s
    eta=s.Symbol('eta');par={n:s.sympify(t,locals={'eta':eta}).subs(eta,s.Rational(1,4)) for n,t in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    tree=ast.parse((ROOT/en.body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in tree.body if isinstance(t,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='PARAMS' for v in t.targets))
    shared={v.arg:s.sympify(ast.unparse(v.value)) for v in call.keywords}
    for key,v in shared.items():
        if isinstance(v,s.Float):
            v=s.Rational(v)
            if v.q!=1:raise ValueError('nonintegral shared float')
            shared[key]=v
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    H,HB,U,Ud,W,w,wp,T,q,RR,QQ,C,S,x=s.symbols('H HB U Ud W w wp T q RR QQ C S xi',real=True)
    p=s.Rational(1,20);e=s.Rational(1,500);k=s.Integer(40);alpha=e*e;rc=s.Rational(1,2);rd=s.Rational(1,8)
    primary=READ(PRIMARY);scalar=READ(SCALAR);kinetic=READ(KINETIC)
    loc={str(v):v for v in (H,HB,U,Ud,W,RR,QQ,C,S)}
    delta=s.sympify(primary['formulas']['energy_delta'],locals=loc).subs({RR:w*T,QQ:q,C:w/e,S:-wp/(k*e)},simultaneous=True)
    fl=s.sympify(READ(cop.PREV)['lapse_flux_divergence'],locals=dict(par,vz=w,vz1=wp,vz2=-k*k*w))
    check('original_lapse_flux_only_spatial_inputs',fl.free_symbols<={w,wp})
    phase=rc/(1-par['zeta']*rc**2*alpha/2)
    potential=par['m2']*rc**2/2+par['lambda4']*rc**4/8+par['lambda6']*rc**6/(24*par['Lambda']**2)+par['mr2']*rc**2/2+par['lambda_r']*rc**4/4+par['g_r']*rc**4/4+par['rho_Lambda']
    M=par['MP2']+par['MU2']*(par['c1']+3*par['c2']+par['c3'])/2
    E0=-3*M*H*H+(par['K_Q']*p*p+phase*phase+rd*rd)/2+potential
    rho=s.cancel(-E0-delta-fl)
    names='H HB U Ud W p K b A beta w wp R rp rpp ty typ rho k'
    sym={n:s.Symbol(n,real=True) for n in names.split()};sym.update(H=H,HB=HB,U=U,Ud=Ud,W=W,w=w,wp=wp)
    mu=par['MU2'];b=par['b'];ss=par['c1']+par['c2']+par['c3']
    den=par['MP2']-mu*(par['c1']+par['c3']+2*par['c3']*w*w-2*par['c4']*(1+w*w)*w*w)
    ty=-mu*(par['c1']+par['c3']+2*par['c3']*w*w)*wp/(s.sqrt(1+w*w)*den)
    Dz=lambda f:s.diff(f,w)*wp-s.diff(f,wp)*k*k*w
    replacements={sym['p']:p,sym['K']:par['K_Q'],sym['b']:b,sym['A']:0,sym['beta']:par['beta'],sym['R']:w*T,sym['rp']:q,sym['ty']:ty,sym['typ']:Dz(ty),sym['rho']:rho,sym['k']:k}
    ap=s.cancel(s.sympify(scalar['formulas']['aPsi'],locals=sym).subs(replacements,simultaneous=True))
    fpsi=s.sympify(scalar['formulas']['fpsi'],locals=sym).subs(replacements,simultaneous=True)
    N=s.cancel(par['K_Q']*(1+w*w)*ap-fpsi)
    allowed={H,HB,U,Ud,W,w,wp,T,q}
    check('scalar_numerator_exact_inputs',N.free_symbols<=allowed)
    check('no_Float_in_exact_scalar_numerator',not bool(N.atoms(s.Float)))
    check('no_pure_node_denominator',s.fraction(N)[1].subs(w,0)!=0)
    zero('analytic_normal_reflection',N.subs(w,-w)-N)
    sigma=e*k;atnode={w:0,wp:sigma,T:q/sigma}
    G=(par['K_Q']+2*b*sigma*sigma)*U-par['K_Q']*HB*p-par['K_Q']*p*q-par['beta']*rho.subs(atnode,simultaneous=True)
    zero('node_cancellation_is_exact_G',N.subs(atnode,simultaneous=True)+G)
    variables=(w,wp,T,q);gradient=[s.diff(N,v) for v in variables]
    pairs=[(i,j) for i in range(4) for j in range(i,4)]
    hessian=[s.diff(gradient[i],variables[j]) for i,j in pairs]
    evaluator=base.Eval([N]+gradient+hessian)
    progress('scalar_normal_derivatives_built',operations=int(s.count_ops(N)))
    initial=next(t for t in READ(cop.CERTS) if t['family']=='new_B1_frame' and t['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);pp,ee,kk=ic(p),ic(e),ic(k);sig=kk*ee
    u0=hb*pp+ic(par['beta'])*ic(s.Rational(1,5))/ic(par['K_Q'])
    hbox=iv.mpf([base.lo(hb*ic(s.Rational(49,50))),base.hi(hb*ic(s.Rational(51,50)))])
    ubox=iv.mpf([base.lo(u0*ic(s.Rational(49,50))),base.hi(u0*ic(s.Rational(51,50)))])
    udbox=cop.unpack(force['Ud_box']);box=dict(H=hbox,HB=hb,U=ubox,Ud=udbox,W=iv.mpf([30,38]))
    Qmax=cop.unpack(READ(CUSP)['bounds']['Qmax']);Rmax=base.upper(Qmax*iv.pi/(2*kk))
    frameT=par['c4']+(par['c1']-(par['c2']+par['c3'])*w*w)/(1+w*w)
    P=mu*ss*(1+w*w)
    V=-mu*((par['c2']+frameT)*wp*wp-par['c2']*k*k*w*w)
    a0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*w*w
    ah=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*w*w
    source=mu*w*wp*(HB*a0-H*ah)/(1+w*w)+3*b*p*U*w**3*wp+5*b*p*W*w**5*wp
    domain=dict(box,w=base.box(ee),wp=base.box(sig))
    Pv,P1,P2,Vv,V1,Fv,F1=base.Eval([P,Dz(P),Dz(Dz(P)),V,Dz(V),source,Dz(source)]).interval(domain)
    Pmin=base.lower(Pv);check('global_half_cell_shift_principal_positive',base.lo(Pmin)>0)
    R2=base.upper((abs(Vv)*Rmax+abs(Fv)+abs(P1)*Qmax)/Pmin)
    R3=base.upper((abs(V1)*Rmax+abs(Vv)*Qmax+abs(F1)+abs(P2)*Qmax+2*abs(P1)*R2)/Pmin)
    D=base.upper(4/sig**2*(5*R3/6+2*Qmax*kk**2/3))
    Tmax=base.upper(2*Qmax/sig);Tpmax=base.upper(D*ee);Tppmax=base.upper(2*R3/sig+kk**2*Tmax+2*sig*D)
    domain.update(T=base.box(Tmax),q=base.box(Qmax))
    evaluated=evaluator.interval(domain)
    speeds=[sig,kk**2*ee,Tpmax,R2];accelerations=[kk**2*ee,kk**2*sig,Tppmax,R3]
    MN=sum(base.upper(abs(v))*a for v,a in zip(evaluated[1:5],accelerations))
    for value,(i,j) in zip(evaluated[5:],pairs):MN+=(1 if i==j else 2)*base.upper(abs(value))*speeds[i]*speeds[j]
    MN=base.upper(MN);quotient=base.upper(2*MN/(ic(b)*sig**2))
    away_gmin=base.lower(ic(b)*(ee/4)**2);away=base.upper(abs(evaluated[0])/away_gmin)
    umax=base.upper(abs(ubox));hmax=base.upper(abs(hbox));hbmax=base.upper(abs(hb));wmax=iv.mpf(38)
    apmax=base.upper(umax+wmax*ee**2+pp*(3*hmax+hbmax+3*Qmax))
    inv=cop.unpack(kinetic['attempts'][-1]['inverse_bound'])
    fymax=max(base.hi(cop.unpack(v)) for v in force['analytic_force_bounds'])
    Zmax=(umax+wmax*ee**2)*ee**2;Cmax=ic(b)*Zmax*ee
    ayanalytic=base.upper(inv*(iv.mpf(fymax)+Cmax*apmax))
    cbar=(ee+ee**2)*(umax+wmax*ee**2)
    azanalytic=base.upper(quotient+cbar*ayanalytic)
    A=ic(par['A']);c0=cop.unpack(READ(SCALAR)['cusp_coefficient_interval'])
    cuspR=base.upper(A/ic(b)*(6*pp*wmax+3*pp**2*D)+inv*3*A*pp**3*(umax+wmax*ee**2)*(1+ee))
    azfull=base.upper(azanalytic+base.upper(c0)*ee+cuspR*ee**3)
    ayfull=base.upper(ayanalytic+inv*3*A*pp**3*ee**2)
    bound_values=dict(Qmax=Qmax,Rmax=Rmax,Rsecond=R2,Rthird=R3,ratio_constant=D,Tmax=Tmax,Tprime=Tpmax,Tsecond=Tppmax,
        numerator_second=MN,analytic_scalar_quotient=quotient,away_gmin=away_gmin,away_quotient=away,aPsi=apmax,
        complement_analytic_acceleration=ayanalytic,complement_full_acceleration=ayfull,aZ_analytic=azanalytic,aZ_full=azfull)
    check('all_uniform_bounds_finite',all(mp.isfinite(base.hi(v)) and base.lo(v)>0 for v in bound_values.values()))
    # Independent physical chain differentiation on a smooth polynomial-shift representative.
    loc=dict(par,H=H,H0=HB,zc=U,p=p,k=k,xi=x)
    f=sum(alpha**(j+1)*s.sympify(v,locals=loc) for j,v in enumerate(READ(cop.PROOF)['polynomial_pieces']))
    f+=alpha**3*s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':x})
    Q=lambda z:(2*x-1)*z-2*x*(1-x)*s.diff(z,x)
    fe=base.Eval([C*S*f.subs(x,C*C),k*Q(f).subs(x,C*C)])
    point=primary['point'];pointbox=dict(H=mp.mpf(point['H']),HB=base.midpoint(hb),U=mp.mpf(point['U']),Ud=mp.mpf(point['Ud']),W=mp.mpf(point['W']))
    def curve(theta):
        wv=mp.cos(theta)/500;wpv=-40*mp.sin(theta)/500;rv,qv=fe.numeric(dict(pointbox,C=mp.cos(theta),S=mp.sin(theta)))
        return dict(pointbox,w=wv,wp=wpv,T=rv/wv,q=qv)
    def value(theta):return evaluator.numeric(curve(theta))[0]
    mixed_max=mp.mpf(0);controls=[]
    for theta in (mp.pi/4,3*mp.pi/4,5*mp.pi/4,7*mp.pi/4):
        current=curve(theta);vals=evaluator.numeric(current)
        vel=[current['wp'],-1600*current['w'],40*mp.diff(lambda t:curve(t)['T'],theta),40*mp.diff(lambda t:curve(t)['q'],theta)]
        acc=[-1600*current['w'],-1600*current['wp'],1600*mp.diff(lambda t:curve(t)['T'],theta,2),1600*mp.diff(lambda t:curve(t)['q'],theta,2)]
        chain=sum(a*z for a,z in zip(vals[1:5],acc));mixed=mp.mpf(0)
        for v,(i,j) in zip(vals[5:],pairs):
            term=(1 if i==j else 2)*v*vel[i]*vel[j];chain+=term
            if i!=j:mixed+=term
        independent=1600*mp.diff(value,theta,2);error=abs(chain-independent)/(1+abs(chain)+abs(independent))
        check('direct_physical_chain_'+mp.nstr(theta,25),error<mp.mpf('1e-18'),mp.nstr(error,65))
        mixed_max=max(mixed_max,abs(mixed));controls.append(dict(theta=mp.nstr(theta,65),chain=mp.nstr(chain,65),direct=mp.nstr(independent,65),error=mp.nstr(error,65),mixed=mp.nstr(mixed,65)))
    check('omitted_mixed_chain_terms_rejected',mixed_max>mp.mpf('1e-25'),mp.nstr(mixed_max,65))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit drift '+name)
    accepted=all(v['passed'] for v in checks)
    return dict(result_id='R4C1-QUARTIC-SCALAR-BOUND-V1',checks=checks,passed=sum(v['passed'] for v in checks),total=len(checks),source_sha256=pins,
        formulas=dict(analytic_N=str(N),aPsi=str(ap),original_local_rho=str(rho),normal_variables=[str(v) for v in variables],
        first_derivatives=[str(v) for v in gradient],second_derivatives=[dict(i=i,j=j,expression=str(v)) for v,(i,j) in zip(hessian,pairs)]),
        bounds={n:base.pack(v) for n,v in bound_values.items()},controls=controls,
        initial_acceleration_extension_certified=accepted,scope='Continuous initial fourteen-coordinate Euler acceleration extension with conservative magnitude bounds; not time evolution',
        time_evolution_certified=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',mpmath=mp.__version__,sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete','initial_acceleration_extension_certified')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
