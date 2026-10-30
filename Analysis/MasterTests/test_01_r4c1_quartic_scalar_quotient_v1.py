"""Full initial scalar forcing and cusp quotient; no full IVP claim."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_SCALAR_QUOTIENT_V1_CONTRACT_2026-10-27.md'
KINETIC='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
ENGINE='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())


def calculate():
    mp.mp.dps=100;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,x):
        value=s.factor(s.cancel(x));check(name,value==0,str(value))
    pins=dict(READ(KINETIC)['source_sha256'])
    pins[KINETIC]='18d56b68030c19c7c48bf27c670deed597a57c1d2f2432b5e459156af3a06765'
    for name in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    spec=importlib.util.spec_from_file_location('quartic_scalar_original',ROOT/ENGINE)
    engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine);engine.setup()
    mp.mp.dps=100;iv.dps=80;cop=engine.body.lift.cop;base=cop.base
    names='H HB U Ud W p K b A beta w wp R rp rpp ty typ rho k'
    u={n:s.Symbol(n,real=True) for n in names.split()}
    H,HB,U,Ud,W,p,K,b,A,beta,w,wp,R,rp,rpp,ty,typ,rho,k=[u[n] for n in names.split()]
    Z=U*w*w+W*w**4;Zp=s.diff(Z,w)*wp;Zpp=s.diff(Zp,w)*wp-s.diff(Zp,wp)*k*k*w
    acc0=(2*H-HB)*w*w-R*w*wp
    acc0t=(HB*HB-6*H*HB)*w*w+2*(HB-H)*R*w*wp
    ct=2*(H-HB)*w*w;zh=Ud*w*w-R*Zp;zht=-R*2*Ud*w*wp
    Pi=K*(1+w*w)*p-3*A*p*p*w**3-b*Z*acc0-b*zh*w*w
    dtPi=3*H*Pi+K*ct*p-9*A*p*p*(H-HB)*w**3-b*(Ud*w*w*acc0+Z*acc0t)-b*(ct*zh+w*w*zht)
    gamma=s.sqrt(1+w*w)
    Dz=lambda f:s.diff(f,w)*wp-s.diff(f,wp)*k*k*w+s.diff(f,R)*rp+s.diff(f,rp)*rpp+s.diff(f,ty)*typ
    flux=-R*Pi-b*(Zp-Z*gamma*w*ty)
    fpsi=-beta*rho-dtPi-Dz(flux)
    ap=s.cancel(-Z/(w*w)-p*(3*H-HB-rp)+p*R*wp/w)
    d=K*(1+w*w)-6*A*p*w**3
    N=s.expand(d*ap-fpsi)
    sigma,r1,rho0,rhoa=s.symbols('sigma r1 rho0 rhoa',nonzero=True,real=True)
    near={R:w*r1/sigma,wp:sigma,rp:r1,ty:0,typ:0,rho:rho0}
    n0=s.limit(s.cancel(N.subs(near,simultaneous=True)),w,0)
    G=(K+2*b*sigma*sigma)*U-K*HB*p-K*p*r1-beta*rho0
    zero('constant_schur_numerator_is_negative_node_condition',n0+G)
    cusp=s.diff(N.subs(rho,rhoa+2*A*p**3*w**3),A)
    lead=s.cancel(s.limit((cusp/w**3).subs(near,simultaneous=True),w,0))
    expected=6*p*U+3*HB*p*p+2*beta*p**3
    zero('leading_scalar_quotient_cusp_coefficient',lead-expected)
    n= N.subs({A:0,rho:rhoa},simultaneous=True)
    reflected=n.subs({w:-w,R:-R,typ:-typ},simultaneous=True)
    zero('analytic_schur_numerator_even_under_node_reflection',reflected-n)
    # Nonzero |w| coefficient is distinct from a differentiable signed w term.
    zero('regulator_regular_node_trace',s.limit(ap.subs(near,simultaneous=True),w,0)+U+(3*H-HB-2*r1)*p)
    fe=base.Eval([ap,fpsi]);primary=READ(PRIMARY)
    eta=s.Symbol('eta');par={n:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
        for n,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    sx=s.Symbol('xi');point=primary['point']
    loc=dict(par,H=s.Float(point['H'],100),H0=s.Float(str(engine.vals['H0']),100),
        zc=s.Float(point['U'],100),p=s.Rational(1,20),k=s.Integer(40),xi=sx)
    pieces=READ(cop.PROOF)['polynomial_pieces']
    poly=sum(s.Rational(1,250000)**(j+1)*s.sympify(expr,locals=loc) for j,expr in enumerate(pieces))
    poly+=s.Rational(1,250000)**3*s.sympify(primary['formulas']['shift_extra'],locals={'W':s.Float(point['W'],100),'xi':sx})
    check('new_shift_has_only_spatial_argument',poly.free_symbols<={sx})
    Q=lambda f:(2*sx-1)*f-2*sx*(1-sx)*s.diff(f,sx)
    Jr=lambda f:4*sx*(1-sx)*s.diff(f,sx,2)+6*(1-2*sx)*s.diff(f,sx)-4*f
    shift=s.lambdify(sx,[poly,Q(poly),Jr(poly)],'mpmath',cse=True)
    def newshift(theta):
        c,st=mp.cos(theta),mp.sin(theta);f,q,j=shift(c*c)
        return c*st*f,40*q
    engine.shift=newshift;engine.H=mp.mpf(point['H']);engine.U=mp.mpf(point['U']);engine.Ud=mp.mpf(point['Ud']);wn=mp.mpf(point['W'])
    angles=[mp.mpf(0),mp.pi/4,3*mp.pi/4]+[mp.pi/2+side*mp.mpf(delta) for delta in ('0.1','0.01','0.001') for side in (-1,1)]
    controls=[]
    for angle in angles:
        state,vd,dd,Sdd=engine.initial(angle);wv=state[7];wv1=state[35];wv2=dd[7]
        state[13]=engine.U*wv**2+wn*wv**4
        state[41]=2*engine.U*wv*wv1+4*wn*wv**3*wv1
        dd[13]=2*engine.U*(wv1**2+wv*wv2)+wn*(12*wv**2*wv1**2+4*wv**3*wv2)
        L,gradient=engine.gradient(state)
        Wt=state[14:28]+[mp.mpf(0)]*14+vd+[mp.mpf(0)]*6
        Wz=state[28:42]+vd+dd+state[45:48]+Sdd
        for step in ('1e-20','1e-26'):
            ht=engine.hv(state,Wt,mp.mpf(step));hz=engine.hv(state,Wz,mp.mpf(step))
            _,normal=engine.density(state);energy=sum(gradient[14+j]*normal[j] for j in range(14))-L
            fluxnum=mp.sqrt(1+wv*wv)*hz[22]+wv*wv1*gradient[22]/mp.sqrt(1+wv*wv)
            density=-energy-fluxnum
            rhs=mp.matrix([gradient[j]-ht[14+j]-hz[28+j] for j in range(14)]);rhs[12]-=engine.par['beta']*density
            values=dict(H=engine.H,HB=engine.vals['H0'],U=engine.U,Ud=engine.Ud,W=wn,p=state[26],
                K=engine.par['K_Q'],b=engine.par['b'],A=engine.par['A']*(1 if wv>0 else -1),beta=engine.par['beta'],
                w=wv,wp=wv1,R=state[44],rp=state[47],rpp=Sdd[2],ty=state[46],typ=Sdd[1],rho=density,k=mp.mpf(40))
            predicted=fe.numeric(values);original=[-rhs[13]/(engine.par['b']*wv*wv),rhs[12]]
            errors=[abs(a-bb)/(1+abs(a)+abs(bb)) for a,bb in zip(predicted,original)]
            for label,error in zip(('aPsi','fpsi'),errors):check(label+'_'+mp.nstr(angle,30)+'_'+step,error<mp.mpf('1e-18'),mp.nstr(error,65))
            controls.append(dict(theta=mp.nstr(angle,65),step=step,aPsi=mp.nstr(predicted[0],65),
                fpsi=mp.nstr(predicted[1],65),errors=[mp.nstr(v,65) for v in errors],exact_background_error_certified=False))
    initial=next(item for item in READ(cop.CERTS) if item['family']=='new_B1_frame' and item['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);p0=base.interval_s(s.Rational(1,20));bb=base.interval_s(par['b']);aa=base.interval_s(par['A']);betai=base.interval_s(par['beta'])
    u0=hb*p0+betai*base.interval_s(s.Rational(1,5))/base.interval_s(par['K_Q'])
    ubox=iv.mpf([base.lo(u0*base.interval_s(s.Rational(49,50))),base.hi(u0*base.interval_s(s.Rational(51,50)))])
    coefficient=aa/bb*(6*p0*ubox+3*hb*p0*p0+2*betai*p0**3)
    check('leading_cusp_coefficient_strictly_positive',base.lo(coefficient)>0,base.pack(coefficient))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit drift '+name)
    return dict(result_id='R4C1-QUARTIC-SCALAR-QUOTIENT-V1',checks=checks,passed=sum(v['passed'] for v in checks),total=len(checks),source_sha256=pins,
        formulas=dict(aPsi=str(ap),Pi=str(Pi),dtPi_zero_acceleration=str(dtPi),spatial_flux=str(flux),fpsi=str(fpsi),
        node_numerator=str(n0),leading_cusp_coefficient='A/b*(6*p*U+3*HB*p^2+2*beta*p^3)'),
        cusp_coefficient_interval=base.pack(coefficient),controls=controls,
        interpretation='Exact initial scalar forcing and its isolated cusp quotient; full complement force/remainder and regularity clearance remain open',
        full_acceleration_extension_certified=False,G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
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
