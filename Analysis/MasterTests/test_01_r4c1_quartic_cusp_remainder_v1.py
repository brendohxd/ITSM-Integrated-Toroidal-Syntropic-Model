"""Certified leading cusp and coupled remainder on the quartic initial slice."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_CUSP_REMAINDER_V1_CONTRACT_2026-10-27.md'
SCALAR='Analysis/MasterTests/outputs/r4c1_quartic_scalar_quotient_v1_attempt_01/summary.json'
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
    pins=dict(READ(SCALAR)['source_sha256']);pins[SCALAR]='0f8f49732d09fe5e2095c120ef7d2d6e479888ba157863eef156d5dd2a0b11dd'
    for name in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    spec=importlib.util.spec_from_file_location('cusp_bound_original',ROOT/ENGINE)
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model);model.setup()
    mp.mp.dps=110;iv.dps=80;cop=model.body.lift.cop;base=cop.base
    eta=s.Symbol('eta');par={n:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
        for n,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    p=s.Rational(1,20);k=s.Integer(40);e=s.Rational(1,500);alpha=e*e;A=par['A'];b=par['b']
    w=s.Symbol('w',positive=True);hh=s.symbols('h0:6',real=True);vv=s.symbols('v0:3',real=True)
    h=s.Matrix([[hh[0],hh[1],hh[2]],[hh[1],hh[3],hh[4]],[hh[2],hh[4],hh[5]]]);V=s.Matrix(vv)
    L=-A*s.sqrt(h.det())*(p*p*(V.T*h*V)[0])**s.Rational(3,2)
    reference={hh[0]:1,hh[1]:0,hh[2]:0,hh[3]:1,hh[4]:0,hh[5]:1,vv[0]:0,vv[1]:w,vv[2]:0}
    force=s.Matrix([s.simplify(s.diff(L,v).subs(reference,simultaneous=True)) for v in (*hh,*vv)]+[0,0,0])
    expected=s.zeros(12,1)
    for j in (0,5):expected[j]=-A*p**3*w**3/2
    expected[3]=-2*A*p**3*w**3;expected[7]=-3*A*p**3*w*w
    zero('all_complement_cusp_forces_from_original_density',force-expected)
    # w>0 formulas transport to w<0 as |w|^3 and w*|w|.
    H,HB,U,W,x=s.symbols('H HB U W xi',real=True)
    loc=dict(par,H=H,H0=HB,zc=U,p=p,k=k,xi=x)
    primary=READ(PRIMARY);kinetic=READ(KINETIC)
    f=sum(alpha**(j+1)*s.sympify(expr,locals=loc) for j,expr in enumerate(READ(cop.PROOF)['polynomial_pieces']))
    f+=alpha**3*s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':x})
    Q=lambda t:(2*x-1)*t-2*x*(1-x)*s.diff(t,x)
    qcoeff=s.Poly(k*Q(f),x).all_coeffs()
    initial=next(t for t in READ(cop.CERTS) if t['family']=='new_B1_frame' and t['eta']=='1/4')
    hb=cop.unpack(initial['H_background']);ic=base.interval_s
    pp=ic(p);kk=ic(k);ee=ic(e);sig=kk*ee;aa=ic(A);bb=ic(b)
    u0=hb*pp+ic(par['beta'])*ic(s.Rational(1,5))/ic(par['K_Q'])
    hbox=iv.mpf([base.lo(hb*ic(s.Rational(49,50))),base.hi(hb*ic(s.Rational(51,50)))])
    ubox=iv.mpf([base.lo(u0*ic(s.Rational(49,50))),base.hi(u0*ic(s.Rational(51,50)))])
    variables=dict(H=hbox,HB=hb,U=ubox,W=iv.mpf([30,38]))
    qmax=sum(base.upper(abs(v)) for v in base.Eval(qcoeff).interval(variables))+cop.unpack(primary['shift_errors'][0][1])
    qmax=base.upper(qmax);rmax=base.upper(qmax*iv.pi/(6*kk))
    z,zp=s.symbols('z zp',real=True)
    ss=par['c1']+par['c2']+par['c3'];mu=par['MU2']
    P=mu*ss*(1+z*z)
    T=par['c4']+(par['c1']-(par['c2']+par['c3'])*z*z)/(1+z*z)
    pot=-mu*((par['c2']+T)*zp*zp-par['c2']*k*k*z*z)
    a0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*z*z
    ah=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*z*z
    src=mu*z*zp*(HB*a0-H*ah)/(1+z*z)+3*b*p*U*z**3*zp+5*b*p*W*z**5*zp
    Dz=lambda t:s.diff(t,z)*zp-s.diff(t,zp)*k*k*z
    expressions=[P,Dz(P),Dz(Dz(P)),pot,Dz(pot),src,Dz(src)]
    check('shift_bound_coefficients_no_Float',not any(t.atoms(s.Float) for t in expressions+qcoeff))
    variables.update(z=iv.mpf([-base.hi(ee/2),base.hi(ee/2)]),zp=iv.mpf([-base.hi(sig),base.hi(sig)]))
    pv,p1,p2,vv,v1,srcv,src1=base.Eval(expressions).interval(variables)
    pmin=base.lower(pv);check('local_shift_principal_positive',base.lo(pmin)>0)
    r2=base.upper((abs(vv)*rmax+abs(srcv)+abs(p1)*qmax)/pmin)
    m3=base.upper((abs(v1)*rmax+abs(vv)*qmax+abs(src1)+abs(p2)*qmax+2*abs(p1)*r2)/pmin)
    D=base.upper(4/(sig*sig)*(5*m3/6+2*qmax*kk*kk/3))
    umax=base.upper(abs(ubox));wmax=iv.mpf(38)
    inv=cop.unpack(kinetic['attempts'][-1]['inverse_bound'])
    scalar_remainder=base.upper(aa/bb*(6*pp*wmax+3*pp*pp*D))
    complement_remainder=base.upper(inv*3*aa*pp**3*(umax+wmax*ee*ee)*(1+ee))
    total=base.upper(scalar_remainder+complement_remainder)
    check('all_bounds_finite_positive',all(base.lo(v)>0 and mp.isfinite(base.hi(v)) for v in (qmax,rmax,r2,m3,D,total)))
    # This generic identity supplies the scalar remainder after the node condition.
    pa,qa,ra,ha,ua,wa,be=s.symbols('p q r HB U W beta',real=True)
    ap=-ua-wa*z*z-pa*(3*H-ha-qa)+pa*ra
    raw=-6*pa*ap+2*be*pa**3-9*pa**2*(2*H-ha)+3*pa**2*qa+9*pa**2*ra
    compact=6*pa*ua+3*ha*pa**2+2*be*pa**3+6*pa*wa*z*z+3*pa**2*(ra-qa)
    zero('exact_scalar_cusp_remainder_identity',raw-compact)
    coefficient=cop.unpack(READ(SCALAR)['cusp_coefficient_interval'])
    check('nonzero_leading_cusp_preserved',base.lo(coefficient)>0)
    # Bound relative remainder on a declared smaller subdomain; no sampled fit.
    relative=base.upper(total*(ee/2)**2/base.lower(coefficient))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit source drift '+name)
    return dict(result_id='R4C1-QUARTIC-CUSP-REMAINDER-V1',checks=checks,passed=sum(v['passed'] for v in checks),total=len(checks),source_sha256=pins,
        complement_cusp_positive_w=[str(v) for v in force],
        bounds={n:base.pack(v) for n,v in dict(Qmax=qmax,Rmax=rmax,Rsecond=r2,Rthird=m3,ratio_difference_constant=D,
            scalar_remainder_constant=scalar_remainder,complement_remainder_constant=complement_remainder,
            full_cusp_remainder_constant=total,leading_coefficient=coefficient,relative_remainder_on_half_profile=relative).items()},
        domain='both nodes, |w|<=e/2=1/1000, |kx|<=pi/6; entire frozen quartic root box',
        conclusion='aZ_cusp=c0*abs(w)+remainder, |remainder|<=C*abs(w)^3; coupled complement cannot cancel c0',
        analytic_force_uniform_remainder_certified=False,full_acceleration_extension_certified=False,G1_complete=False,
        physics_pass=False,gate_effect='NONE',review_status='DEFERRED',mpmath=mp.__version__,sympy=s.__version__)


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
