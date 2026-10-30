"""Exact selected Euler jets V2: load shared potential constants from their source."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as sy

ROOT=Path(__file__).resolve().parents[2]
PRIMARY='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'
PRIOR='Analysis/MasterTests/outputs/r4c1_second_node_consistency_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_SECOND_NODE_ENCLOSURE_V1_CONTRACT_2026-10-27.md'
JOINT='Analysis/MasterTests/outputs/r4c1_joint_node_velocity_attempt_02/'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
SHA=lambda x:hashlib.sha256(x).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda x:json.loads((ROOT/x).read_bytes())


def progress(name,**kw):print(json.dumps(dict(stage=name,**kw)),flush=True)


def calculate():
    mp.mp.dps=110;mp.iv.dps=80
    expected={PRIOR:'2fe36ca4652b276172fe3473897655d41c9e4a4f18be3f4e915e5f363cef23e2',
              PRIMARY:'2cbb055c8a4172ef9e75daa7b80a92c5f979aadc817e29d7cace6115adb47ec5',
              CONTRACT:'46b35c581954ed6f788bea574446eb6e53abc4289858e015d332e3fa83c11278'}
    for name,wanted in expected.items():
        if SHA((ROOT/name).read_bytes())!=wanted:raise ValueError('frozen entry pin drift '+name)
    spec=importlib.util.spec_from_file_location('nodal_certificate_original',ROOT/PRIMARY)
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model);model.setup();mp.mp.dps=110
    bdy=model.body;checks=[]
    def check(name,condition,value=None):checks.append(dict(name=name,passed=bool(condition),value=value))
    eta=sy.Symbol('eta');raw=READ(PLANAR)['families']['new_B1_frame']['parameter_map']
    par={name:sy.sympify(text,locals={'eta':eta}).subs(eta,sy.Rational(1,4)) for name,text in raw.items()}
    background_ast=ast.parse((ROOT/bdy.canonical.BG).read_text(encoding='utf-8-sig'))
    parameter_call=next(node.value for node in background_ast.body if isinstance(node,ast.Assign)
        and any(isinstance(target,ast.Name) and target.id=='PARAMS' for target in node.targets))
    shared={kw.arg:sy.sympify(ast.unparse(kw.value)) for kw in parameter_call.keywords}
    for name,value in shared.items():
        if isinstance(value,sy.Float):
            exact=sy.Rational(value)
            if exact.q!=1:raise ValueError('nonintegral shared Float needs an explicit exact chart')
            shared[name]=exact
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    par['A']=sy.Integer(0)  # only the proven selected-row/low-normal-order coefficients
    Rc=sy.Rational(1,2);p0=sy.Rational(1,20);rd=sy.Rational(1,8);k=sy.Integer(40);e=sy.Rational(1,500)
    phase=Rc/(1-par['zeta']*Rc**2*e**2/2)
    names='ax ay az dx dy dz m mt mz w wt wz v vt vz Z Zd Zz R rp rpp ty typ p H HB U Ud Ah av Fy D0 D1 D2 ap Az'
    u={name:sy.Symbol(name,real=True) for name in names.split()}
    ax,ay,az,dx,dy,dz,m,mt,mz,w,wt,wz,v,vt,vz,Z,Zd,Zz,R,rp,rpp,ty,typ,p,H,HB,U,Ud,Ah,av,Fy,D0,D1,D2,ap,Az=[u[x] for x in names.split()]
    q=[ax,0,0,ay,m,az,0,w,v,Rc,0,Rc,0,Z,0]
    dq=[0,0,0,0,mz,0,0,wz,vz,0,0,0,0,Zz,0]
    y=[dx/2,0,0,dy/2,(mt-R*mz-ay*ty-m*rp)/2,dz/2-m*ty-az*rp,
       0,wt-R*wz+v*ty,vt-R*vz+v*rp,0,phase,rd]
    original_sqrt=bdy.sqrt;bdy.sqrt=sy.sqrt
    try:
        vol=sy.sqrt(ax*(ay*az-m*m));c=ay*w*w+2*m*w*v+az*v*v
        L=vol*(bdy.body(q,dq,y,p,par)-par['b']*(Zd-R*Zz)*c*p)
        progress('symbolic_original_density',operations=int(sy.count_ops(L)))
        zero={m:0,mt:0,mz:0,v:0,vt:0,vz:0}
        initial={ax:1,ay:1,az:1,dx:2*H,dy:2*H,dz:2*H,wt:-HB*w,
                 Z:U*w*w,Zd:Ud*w*w,Zz:2*U*w*wz}
        def at_initial(expr):return expr.xreplace(zero).xreplace(initial)
        time_rates={ax:2*H,ay:2*H,az:2*H,dx:D0,dy:D1,dz:D2,w:-HB*w,
                    wt:Fy*w,wz:-HB*wz,Z:Ud*w*w,Zd:Az,Zz:2*Ud*w*wz,p:ap}
        def row(field,velocity,gradient):
            Pi=sy.diff(L,velocity);restricted=Pi.xreplace(zero)
            dt=sum(sy.diff(restricted,key)*value for key,value in time_rates.items())
            dt+=sy.diff(Pi,mt).xreplace(zero)*Ah+sy.diff(Pi,vt).xreplace(zero)*av
            dt=at_initial(dt)
            flux=at_initial(sy.diff(L,gradient))
            ds=sy.diff(flux,w)*wz-sy.diff(flux,wz)*k*k*w+sy.diff(flux,R)*rp\
                +sy.diff(flux,rp)*rpp+sy.diff(flux,ty)*typ
            out=at_initial(sy.diff(L,field))-dt-ds
            progress('selected_row_formed',field=str(field),operations=int(sy.count_ops(out)))
            return out
        em=row(m,mt,mz);ev=row(v,vt,vz)
        den=par['MP2']-par['MU2']*(par['c1']+par['c3']+2*par['c3']*w*w-2*par['c4']*(1+w*w)*w*w)
        ty_expr=-par['MU2']*(par['c1']+par['c3']+2*par['c3']*w*w)*wz/(sy.sqrt(1+w*w)*den)
        typ_expr=sy.diff(ty_expr,w)*wz-sy.diff(ty_expr,wz)*k*k*w
        slope,r1,r3,Fz=sy.symbols('slope r1 r3 Fz',real=True)
        node={w:0,wz:slope,R:0,rp:r1,rpp:0,ty:0,typ:0,av:0,p:p0}
        metric_eq=sy.cancel(em.xreplace(node))
        metric_acc=sy.cancel(sy.solve(metric_eq,Ah)[0])
        ev=ev.xreplace({ty:ty_expr,typ:typ_expr})
        normal=sy.diff(ev,w)*slope+sy.diff(ev,R)*r1+sy.diff(ev,rpp)*r3+sy.diff(ev,av)*Fz
        normal=sy.cancel(normal.xreplace(node).subs(Ah,metric_acc))
        frame_slope=sy.cancel(sy.solve(normal,Fz)[0])
        unused={Fy,D0,D1,D2,ap,Az}
        check('unfixed_other_accelerations_cancel',not bool((metric_acc.free_symbols|frame_slope.free_symbols)&unused))
        check('metric_equation_reconstructed',sy.cancel(metric_eq.subs(Ah,metric_acc))==0)
        check('frame_equation_reconstructed',sy.cancel(normal.subs(Fz,frame_slope))==0)
        progress('coupled_selected_accelerations_derived')

        lam,Xz=sy.symbols('lam Xz',real=True)
        qq=[1,0,0,1,0,1,0,w,0,Rc,0,Rc,0,U*w*w,0]
        dd=[0,0,0,0,0,0,0,wz,0,0,0,0,0,2*U*w*wz,0]
        qq=[sy.sympify(x) for x in qq];dd=[sy.sympify(x) for x in dd]
        yy=[H,0,0,H,-ty/2,H-rp,0,-HB*w-R*wz,Xz,0,phase,rd]
        yy_scaled=[lam*x for x in yy]
        lp=bdy.body(qq,dd,yy_scaled,lam*p,par)-par['b']*lam*(Ud*w*w-R*2*U*w*wz)*w*w*lam*p
        energy=(lam*sy.diff(lp,lam)-lp).subs({lam:1,Xz:0})
        flux=sy.sqrt(1+w*w)*sy.diff(lp,Xz).subs({lam:1,Xz:0})
        flux=sy.cancel(flux.subs(ty,ty_expr))
        check('local_flux_independent_shift_jets',not bool(flux.free_symbols&{R,rp}))
        flux_prime=sy.diff(flux,w)*wz-sy.diff(flux,wz)*k*k*w
        rho=sy.cancel(-energy.subs(ty,ty_expr)-flux_prime)
        rho2=(sy.diff(rho,w,2)*slope*slope+2*sy.diff(rho,w,R)*slope*r1
              +sy.diff(rho,R,2)*r1*r1-sy.diff(rho,wz)*k*k*slope+sy.diff(rho,rp)*r3)/2
        rho2=sy.cancel(rho2.subs({w:0,wz:slope,R:0,rp:r1,p:p0}))
        a0=-U-(3*H-HB-2*r1)*p0;a2=p0*(2*r3-r1*k*k)/3;ss=slope*slope
        ty0=sy.cancel(ty_expr.subs({w:0,wz:slope}))
        aznode=(par['K_Q']*(a2+ss*a0)+par['K_Q']*p0*(-r3/2+(5*H-2*HB-3*r1)*ss)
                +4*par['b']*U*ss*k*k+3*par['b']*U*ty0*slope**3+par['beta']*rho2)/(par['b']*ss)
        Q=sy.cancel(aznode+2*a2+p0*frame_slope)
        s0=par['c1']+par['c2']+par['c3']
        r3_rule=-ss*(HB*(par['c1']+2*par['c2']+par['c4'])-H*(3*par['c1']+5*par['c2']+par['c3']+2*par['c4'])
                    +(par['c1']+par['c2']+par['c4']+2*s0)*r1)/s0
        Q=sy.factor(Q.subs(r3,r3_rule).subs(slope,e*k))
        check('exact_expressions_have_no_Float',not any(x.atoms(sy.Float) for x in (metric_acc,frame_slope,rho2,Q)))
        check('trace_has_only_enclosed_inputs',Q.free_symbols<={H,HB,U,r1})
        progress('exact_trace_derived',operations=int(sy.count_ops(Q)))
    finally:bdy.sqrt=original_sqrt

    prior=READ(PRIOR);point=next(x for x in prior['results'] if x['kind']=='approximate_trace' and x['orientation']==1)
    reference=point['coefficients'][-1]
    subs={H:sy.Float(str(model.H),100),HB:sy.Float(str(model.vals['H0']),100),U:sy.Float(str(model.U),100),
          r1:sy.Float(point['r1'],100),r3:sy.Float(point['r3'],100),slope:sy.Rational(2,25),p:p0}
    for name,expr in [('rho2',rho2),('avz1',frame_slope),('Q',Q)]:
        got=mp.mpf(str(expr.evalf(100,subs=subs)));wanted=mp.mpf(reference[name]);error=abs(got-wanted)/(1+abs(got)+abs(wanted))
        check('independent_numeric_'+name,error<mp.mpf('1e-18'),mp.nstr(error,60))
    cop=model.body.lift.cop;base=cop.base
    joint=next(x for x in READ(JOINT+'certificates.json') if x['family']=='new_B1_frame' and x['eta']=='1/4')
    initial=next(x for x in READ(cop.CERTS) if x['family']=='new_B1_frame' and x['eta']=='1/4')
    boxes={'H':cop.unpack(joint['H_bracket']),'HB':cop.unpack(initial['H_background']),
           'U':cop.unpack(joint['U_bracket']),'r1':cop.unpack(joint['attempts'][-1]['core']['r2'])/250000}
    enclosure=base.Eval([Q]).interval(boxes)[0]
    low,high=base.lo(enclosure),base.hi(enclosure)
    strict=low>0 or high<0
    check('trace_interval_is_finite',mp.isfinite(low) and mp.isfinite(high))
    check('trace_interval_excludes_zero',strict,{'lower':mp.nstr(low,60),'upper':mp.nstr(high,60)})
    pins=dict(READ(PRIOR)['source_sha256'])
    for name in (PRIMARY,PRIOR,CONTRACT,JOINT+'certificates.json',cop.CERTS,PLANAR,Path(__file__).relative_to(ROOT).as_posix()):pins[name]=SHA((ROOT/name).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    return dict(result_id='R4C1-SECOND-NODE-ENCLOSURE-V1',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
        formulas={'metric_equation':str(metric_eq),'metric_acceleration':str(metric_acc),'frame_normal_equation':str(normal),
                  'frame_acceleration_slope':str(frame_slope),'rho2':str(rho2),'trace':str(Q),'shift_r3':str(r3_rule)},
        input_boxes={name:base.pack(value) for name,value in boxes.items()},trace_enclosure=base.pack(enclosure),
        conditional_incompatibility_certified=bool(strict and all(c['passed'] for c in checks)),
        source_sha256=pins,sympy=sy.__version__,mpmath=mp.__version__,interval_digits=80,
        scope='Specified quadratic-profile joint initial continuation under stated strong joint time/normal regularity only',
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);a=parser.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);p=directory/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','conditional_incompatibility_certified','G1_complete')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
