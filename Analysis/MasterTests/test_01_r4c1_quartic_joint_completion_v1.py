"""Restricted four-condition initial construction; not full admission/evolution."""
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
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda x:json.loads((ROOT/x).read_bytes())
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_JOINT_COMPLETION_V1_CONTRACT_2026-10-27.md'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_JOINT_COMPLETION_V1_COMPUTATIONAL_ADDENDUM_2026-10-27.md'
CERT='Analysis/MasterTests/outputs/r4c1_second_node_enclosure_v2_attempt_01/summary.json'
JOINT='Analysis/MasterTests/test_01_r4c1_joint_node_velocity_v2.py'
ACCEL='Analysis/MasterTests/test_01_r4c1_joint_background_acceleration_v1.py'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def progress(stage,**kw):print(json.dumps(dict(stage=stage,**kw)),flush=True)


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def num(x):return mp.nstr(x,70)
    expected={CONTRACT:'4e4834aff41237fc03235d48c9afa12ab0bc4ac1e0c2116b33f10cf72d03ab16',
        ADDENDUM:'ffd307da06f991688f22db9459904365e4b574d35a30df3d6d8724eed7a0bd73',
        CERT:'ad053bf3d816bad7983281ff9d16cf52671398face84249ced7e4f47b51afd24',
        JOINT:'e10bf2f7b20e871cd93fd10b00f1ed6f43f648f60b9282e15205e277d29e3d3d',
        ACCEL:'2cbb055c8a4172ef9e75daa7b80a92c5f979aadc817e29d7cace6115adb47ec5'}
    pins=dict(READ(CERT)['source_sha256']);pins.update(expected)
    pins[Path(__file__).relative_to(ROOT).as_posix()]=SHA(Path(__file__).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('entry source drift '+name)
    model=load('quartic_original_density',ACCEL);model.setup();mp.mp.dps=110;iv.dps=80
    joint=load('quartic_original_time_condition',JOINT);base=joint.base;cop=joint.cop
    inherited=base.Checks();pack,_=joint.build(inherited)
    if not all(c['passed'] for c in inherited.rows):raise ValueError('inherited algebra utility failed')
    exact_map=READ(cop.PLANAR)['families']['new_B1_frame']['parameter_map'];eta=sy.Symbol('eta')
    par={k:sy.sympify(v,locals={'eta':eta}).subs(eta,sy.Rational(1,4)) for k,v in exact_map.items()}
    tree=ast.parse((ROOT/model.body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PARAMS' for t in n.targets))
    shared={k.arg:sy.sympify(ast.unparse(k.value)) for k in call.keywords}
    for key,value in shared.items():
        if isinstance(value,sy.Float):
            q=sy.Rational(value)
            if q.q!=1:raise ValueError('nonintegral shared float')
            shared[key]=q
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    H,HB,U,Ud,W,x,al,C,S,RR,QQ,qn=sy.symbols('H HB U Ud W xi alpha C S RR QQ qn',real=True)
    e=sy.Rational(1,500);af=e*e;k=sy.Integer(40);p=sy.Rational(1,20);Rc=sy.Rational(1,2);rd=sy.Rational(1,8)
    phase=Rc/(1-par['zeta']*Rc**2*af/2);rho0=sy.Rational(1,5);K=par['K_Q'];b=par['b'];be=par['beta']
    check('phase_charge_exact_unchanged',sy.cancel(phase*(1-par['zeta']*Rc**2*af/2)-Rc)==0)
    check('scalar_velocity_elimination_coefficient_positive',1+2*b*k*k*af/K>0)
    M=par['MP2']+par['MU2']*(par['c1']+3*par['c2']+par['c3'])/2;s0=par['c1']+par['c2']+par['c3']
    pot=par['m2']*Rc**2/2+par['lambda4']*Rc**4/8+par['lambda6']*Rc**6/(24*par['Lambda']**2)\
        +par['mr2']*Rc**2/2+par['lambda_r']*Rc**4/4+par['g_r']*Rc**4/4+par['rho_Lambda']
    names='MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 vz vz1 vz2 R q p Z Zd Z1 Z2 D rd pot k alpha xi zc zdc rs qs CC SS eeabs rh qh ru qu'
    u={n:sy.Symbol(n,real=True) for n in names.split()};A=sy.Symbol('A',real=True)
    u.update(par);u.update(A=A,Rc=Rc,H=H,H0=HB,R=RR,q=QQ,p=p,D=phase,rd=rd,pot=pot,k=k,
                         alpha=al,xi=x,zc=U,zdc=Ud,CC=C,SS=S,eeabs=e)
    parse=lambda s:sy.sympify(s,locals=u)
    proof=READ(cop.PROOF);raw=READ(cop.PREV)
    f=sum(al**(j+1)*parse(text) for j,text in enumerate(proof['polynomial_pieces']))
    extra=-5*b*p*W/(par['MU2']*s0*k)*(x*x/36+5*x/144+sy.Rational(5,96))
    f+=al**3*extra
    Q=lambda a:(2*x-1)*a-2*x*(1-x)*sy.diff(a,x)
    J=lambda a:4*x*(1-x)*sy.diff(a,x,2)+6*(1-2*x)*sy.diff(a,x)-4*a
    T=par['c4']+(par['c1']-(par['c2']+par['c3'])*al*x)/(1+al*x)
    operator=-k*k*par['MU2']*s0*(1+al*x)*J(f)+2*k*k*par['MU2']*s0*al*Q(f)\
        -par['MU2']*al*k*k*((par['c2']+T)*(1-x)-par['c2']*x)*f
    a0=par['c1']+2*par['c2']+par['c4']+(par['c2']-par['c3']+par['c4'])*al*x
    ah=3*par['c1']+5*par['c2']+par['c3']+2*par['c4']+(2*par['c1']+4*par['c2']+2*par['c4'])*al*x
    source=-par['MU2']*k*al*(HB*a0-H*ah)/(1+al*x)-3*b*p*U*k*al**2*x-5*b*p*W*k*al**3*x*x
    N=sy.cancel((operator-source)*(1+al*x));poly=sy.Poly(N,al,x)
    check('new_shift_first_three_orders_cancel',min(powers[0] for powers,coef in poly.terms())>=4)
    check('new_shift_source_retains_quartic_term',sy.diff(source,W)==-5*b*p*k*al**3*x*x)
    fp=f.subs(al,af);rpoly=C*S*fp.subs(x,C*C);qpoly=k*Q(f).subs({al:af,x:C*C})
    r_expr=[rpoly,qpoly]
    for variable in (H,U,W):r_expr.extend([sy.diff(rpoly,variable),sy.diff(qpoly,variable)])
    fr=base.Eval(r_expr);coeffs=sy.Poly(N.subs(al,af),x).all_coeffs()
    residuals=[base.Eval([sy.diff(z,v) for z in coeffs]) if v is not None else base.Eval(coeffs) for v in (None,H,U,W)]
    ww=e*C;wp=-k*e*S;wpp=-k*k*ww
    subs={u['vz']:ww,u['vz1']:wp,u['vz2']:wpp,u['Z']:U*ww**2+W*ww**4,
          u['Zd']:Ud*ww**2,u['Z1']:2*U*ww*wp+4*W*ww**3*wp,
          u['Z2']:2*U*(wp**2+ww*wpp)+W*(12*ww**2*wp**2+4*ww**3*wpp)}
    energy0=parse(raw['energy_without_dust']);cusp=sy.factor(sy.diff(energy0,A))
    check('original_cusp_coefficient',sy.simplify(cusp+2*p**3*u['vz']**2*sy.Abs(u['vz']))==0)
    analytic=sy.cancel(energy0.subs(A,0).xreplace(subs))
    Ebase=-3*M*H*H+(K*p*p+phase*phase+rd*rd)/2+pot
    delta=sy.cancel(analytic-Ebase);flux=sy.cancel(parse(raw['lapse_flux_divergence']).xreplace(subs))
    check('local_flux_shift_and_profile_independent',not bool(flux.free_symbols&{H,U,W,Ud,RR,QQ}))
    fed=base.Eval([delta]+[sy.diff(delta,z) for z in (H,U,W,Ud,RR,QQ)])
    fj=base.Eval([flux]);feb=base.Eval([Ebase]);fcusp=base.Eval([-8*par['A']*p**3*e**3/(3*sy.pi)])
    replacements={**par,'H':H,'H0':HB,'zc':U,'alpha':af,'qs':qn/af,'p':p,'Rc':Rc,'D':phase,'rd':rd,'pot':pot,'k':k}
    velocity=pack['velocity'][0].xreplace({s:replacements[str(s)] for s in pack['velocity'][0].free_symbols if str(s) in replacements})
    velocity=sy.cancel(velocity);fv=base.Eval([velocity]+[sy.diff(velocity,z) for z in (H,U,qn)])
    check('velocity_elimination_has_expected_inputs',velocity.free_symbols<={H,HB,U,qn})
    q0=sy.sympify(READ(CERT)['formulas']['trace'],locals={'H':H,'HB':HB,'U':U,'r1':qn})
    gain=sy.Rational(4181,625);fQ=base.Eval([q0]+[sy.diff(q0,z) for z in (H,U,qn)])
    all_expr=[delta,flux,velocity,q0,N]
    check('exact_no_Float',not any(a.atoms(sy.Float) for a in all_expr))
    progress('quartic_original_expressions_built',energy_operations=int(sy.count_ops(delta)))

    init=next(a for a in READ(cop.CERTS) if a['family']=='new_B1_frame' and a['eta']=='1/4')
    hb=cop.unpack(init['H_background']);ivc=lambda z:base.interval_s(z)
    constants={name:ivc(value) for name,value in par.items()};kk=ivc(k);aa=ivc(af);pp=ivc(p);bb=ivc(b);beta=ivc(be);kq=ivc(K);mm=ivc(M)
    rrho=ivc(rho0);u0=hb*pp+beta*rrho/kq;dh=hb/50;du=u0/50;scales=[dh,du,iv.mpf(4)]
    Hbox=iv.mpf([base.lo(hb-dh),base.hi(hb+dh)]);Ubox=iv.mpf([base.lo(u0-du),base.hi(u0+du)]);Wbox=iv.mpf([30,38])
    boxvals={'H':Hbox,'HB':hb,'U':Ubox,'W':Wbox}
    Tmax=abs(constants['c4'])+abs(constants['c1'])+abs(constants['c2']+constants['c3'])*aa
    kap=ivc(s0)-aa*(2*abs(constants['c2'])+Tmax)/4;coerce=constants['MU2']*kap
    pmin=constants['MU2']*ivc(s0);wmax=constants['MU2']*kk**2*aa*(2*abs(constants['c2'])+Tmax)
    check('inherited_operator_coercive',base.lo(coerce)>0)
    errors=[]
    for evaluator in residuals:
        rs=sum(base.upper(abs(z)) for z in evaluator.interval(boxvals))/2
        re=base.upper((2/kk)*rs/(2*kk*coerce));qe=base.upper((2/kk)*(wmax*re+rs)/pmin)
        errors.append((re,qe))
    cuspmean=fcusp.interval({})[0];sig2=kk*kk*aa;gaini=ivc(gain)
    den=[-6*mm*hb*dh,kq*du,-4*gaini]
    def state(h,u,w,c,s):
        values={'H':h,'HB':hb,'U':u,'W':w,'C':c,'S':s}
        fields=fr.interval(values);node_fields=fr.interval(dict(values,C=iv.mpf(0),S=iv.mpf(1)))
        nodeq=node_fields[1]+base.box(errors[0][1]);node_der=[node_fields[3+2*j]+base.box(errors[j+1][1]) for j in range(3)]
        ve=fv.interval({'H':h,'HB':hb,'U':u,'qn':nodeq})
        vder=[ve[1]+ve[3]*node_der[0],ve[2]+ve[3]*node_der[1],ve[3]*node_der[2]]
        R=fields[0]+base.box(errors[0][0]);q=fields[1]+base.box(errors[0][1])
        values.update(RR=R,QQ=q,Ud=ve[0])
        ed=fed.interval(values);dR=[fields[2+2*j]+base.box(errors[j+1][0]) for j in range(3)]
        dq=[fields[3+2*j]+base.box(errors[j+1][1]) for j in range(3)]
        deriv=[ed[1+j]+ed[4]*vder[j]+ed[5]*dR[j]+ed[6]*dq[j] for j in range(3)]
        return values,ed[0],deriv,nodeq,node_der,ve[0]
    def enclosed(h,u,w,n):
        mean=[iv.mpf(0)]*4;floor=None
        for j in range(n):
            ang=iv.mpf([base.lo(iv.pi*j/(2*n)),base.hi(iv.pi*(j+1)/(2*n))]);c,s=iv.cos(ang),iv.sin(ang)
            vals,ed,der,_,_,_=state(h,u,w,c,s)
            for z,value in enumerate([ed]+der):mean[z]+=value/n
            local=-feb.interval(vals)[0]-ed+2*constants['A']*pp**3*(iv.mpf(1)/500)**3*c**3-fj.interval(vals)[0]
            lo=base.lo(local);floor=lo if floor is None else min(floor,lo)
        nv,edn,dn,nodeq,dq,vel=state(h,u,w,iv.mpf(0),iv.mpf(1));jn=fj.interval(nv)[0]
        # The exact odd-sector node value and all its sensitivities are zero.
        nv['RR']=iv.mpf(0);ene=fed.interval(nv)
        ev=fv.interval({'H':h,'HB':hb,'U':u,'qn':nodeq})
        uvder=[ev[1]+ev[3]*dq[0],ev[2]+ev[3]*dq[1],ev[3]*dq[2]]
        dn=[ene[1+j]+ene[4]*uvder[j]+ene[6]*dq[j] for j in range(3)];edn=ene[0]
        ff=feb.interval(nv)[0]+mean[0]+cuspmean+rrho
        bg=kq*(u-u0)+2*bb*sig2*u-kq*pp*nodeq+beta*(edn+jn-mean[0]-cuspmean)
        qq=fQ.interval({'H':h,'HB':hb,'U':u,'qn':nodeq})
        trace=qq[0]-gaini*w
        jac=[[-6*mm*h+mean[1],mean[2],mean[3]],
             [-kq*pp*dq[0]+beta*(dn[0]-mean[1]),kq+2*bb*sig2-kq*pp*dq[1]+beta*(dn[1]-mean[2]),-kq*pp*dq[2]+beta*(dn[2]-mean[3])],
             [qq[1]+qq[3]*dq[0],qq[2]+qq[3]*dq[1],qq[3]*dq[2]-gaini]]
        return [ff,bg,trace],jac,floor,vel
    attempts=[];certified=False
    for n in (16,32,64,128,256):
        values,jac,floor,velocity_box=enclosed(Hbox,Ubox,Wbox,n)
        center,_,_,_=enclosed(hb,u0,iv.mpf(34),n)
        rows=[];centres=[]
        for i in range(3):
            row=sum(base.upper(abs((1 if i==j else 0)-jac[i][j]*scales[j]/den[i])) for j in range(3))
            rows.append(row);centres.append(base.upper(abs(center[i]/den[i])))
        good=all(base.hi(r)<1 and base.hi(c+r)<1 for c,r in zip(centres,rows)) and floor>0
        attempts.append(dict(boxes=n,row_bounds=[base.pack(z) for z in rows],centre_bounds=[base.pack(z) for z in centres],
            self_map_bounds=[base.pack(c+r) for c,r in zip(centres,rows)],density_lower=num(floor),certified=bool(good)))
        progress('quartic_contraction_attempt',boxes=n,certified=bool(good))
        if good:certified=True;break
    check('fixed_box_contraction_and_positive_density',certified,attempts[-1])
    # Independent Fourier assembly for the new, unchanged-operator forcing.
    pv={name:mp.mpf(str(sy.N(value,100))) for name,value in par.items()};HBp=base.midpoint(hb)
    def fourier(modes):
        matrix=mp.matrix(modes);rhs=mp.matrix(modes,4)
        for j in range(64):
            a=2*mp.pi*j/64;wv=mp.cos(a)/500;wv1=-40*mp.sin(a)/500;wv2=-1600*wv
            P=pv['MU2']*(pv['c1']+pv['c2']+pv['c3'])*(1+wv*wv)
            tt=pv['c4']+(pv['c1']-(pv['c2']+pv['c3'])*wv*wv)/(1+wv*wv)
            opw=-pv['MU2']*((pv['c2']+tt)*wv1**2+pv['c2']*wv*wv2)
            A0=pv['c1']+2*pv['c2']+pv['c4']+(pv['c2']-pv['c3']+pv['c4'])*wv*wv
            AH=3*pv['c1']+5*pv['c2']+pv['c3']+2*pv['c4']+(2*pv['c1']+4*pv['c2']+2*pv['c4'])*wv*wv
            forcing=[-pv['MU2']*wv*wv1*AH/(1+wv*wv),pv['MU2']*wv*wv1*HBp*A0/(1+wv*wv),
                     3*pv['b']*mp.mpf(p)*wv**3*wv1,5*pv['b']*mp.mpf(p)*wv**5*wv1]
            sn=[mp.sin(2*(i+1)*a) for i in range(modes)];ds=[2*(i+1)*40*mp.cos(2*(i+1)*a) for i in range(modes)]
            for a1 in range(modes):
                for j1 in range(4):rhs[a1,j1]+=forcing[j1]*sn[a1]/64
                for b1 in range(modes):matrix[a1,b1]+=(P*ds[a1]*ds[b1]+opw*sn[a1]*sn[b1])/64
        columns=[mp.lu_solve(matrix,rhs[:,i]) for i in range(4)]
        def at(theta,h,u,w):
            coeff=columns[0]*h+columns[1]+columns[2]*u+columns[3]*w
            return sum(coeff[i]*mp.sin(2*(i+1)*theta) for i in range(modes)),sum(coeff[i]*2*(i+1)*40*mp.cos(2*(i+1)*theta) for i in range(modes))
        return at
    g8,g12=fourier(8),fourier(12);mp.mp.dps=100
    def point(h,u,ud,w):
        nodeq=g12(mp.pi/2,h,u,w)[1];mean=mp.mpf(0)
        for j in range(64):
            theta=2*mp.pi*j/64;c,s=mp.cos(theta),mp.sin(theta);r,q=g12(theta,h,u,w)
            vv={'H':h,'HB':HBp,'U':u,'W':w,'Ud':ud,'RR':r,'QQ':q,'C':c,'S':s}
            mean+=fed.numeric(vv)[0]/64
        cm=base.midpoint(cuspmean);rho=mp.mpf(rho0);kn=mp.mpf(K);bn=mp.mpf(b);pn=mp.mpf(p);betan=mp.mpf(be)
        nv={'H':h,'HB':HBp,'U':u,'W':w,'Ud':ud,'RR':mp.mpf(0),'QQ':nodeq,'C':mp.mpf(0),'S':mp.mpf(1)}
        eb=feb.numeric(nv)[0];rhnode=-eb-fed.numeric(nv)[0]-fj.numeric(nv)[0]
        F=eb+mean+cm+rho;G=(kn+2*bn*(mp.mpf(40)/500)**2)*u-kn*HBp*pn-kn*pn*nodeq-betan*rhnode
        vel=fv.numeric({'H':h,'HB':HBp,'U':u,'qn':nodeq})[0]
        Tn=(1+2*bn*(mp.mpf(40)/500)**2/kn)*(ud-vel)
        Qn=fQ.numeric({'H':h,'HB':HBp,'U':u,'qn':nodeq})[0]-mp.mpf(gain)*w
        return F,G,Tn,Qn
    start=(HBp,base.midpoint(u0),model.Ud,mp.mpf(34))
    root=mp.findroot(point,start,tol=mp.mpf('1e-55'),maxsteps=20,solver='mdnewton')
    residual=max(abs(z) for z in point(*root));check('independent_uneliminated_four_equation_point',residual<mp.mpf('1e-40'),num(residual))
    hp,up,udp,wpv=root
    check('independent_point_inside_fixed_box',base.lo(Hbox)<=hp<=base.hi(Hbox) and base.lo(Ubox)<=up<=base.hi(Ubox) and 30<=wpv<=38)
    galerkin_error=mp.mpf(0);poly_errors=[]
    for a in (mp.mpf(0),mp.pi/7,mp.pi/2):
        va,vb=g8(a,hp,up,wpv),g12(a,hp,up,wpv);galerkin_error=max(galerkin_error,*(abs(x-y)/(1+abs(x)+abs(y)) for x,y in zip(va,vb)))
        vv={'H':hp,'HB':HBp,'U':up,'W':wpv,'C':mp.cos(a),'S':mp.sin(a)};approx=fr.numeric(vv)
        pe=[abs(vb[i]-approx[i]) for i in range(2)];poly_errors.append([num(z) for z in pe])
        check('shift_within_recomputed_error_'+num(a),all(pe[i]<=base.hi(errors[0][i])+mp.mpf('1e-30') for i in range(2)))
    check('independent_8_12_shift',galerkin_error<mp.mpf('1e-25'),num(galerkin_error))
    for name in (cop.PROOF,cop.PREV):
        if name not in pins:raise ValueError('unregistered inherited source '+name)
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    return dict(result_id='R4C1-QUARTIC-JOINT-COMPLETION-V1',checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
        source_sha256=pins,formulas={'shift_extra':str(extra),'shift_residual':str(N),'velocity':str(velocity),'energy_delta':str(delta),'trace':'Q0(H,Hbg,U,r1)-4181*W/625'},
        attempts=attempts,shift_errors=[[base.pack(z) for z in row] for row in errors],
        point={name:num(value) for name,value in zip(('H','U','Ud','W'),root)},point_shift_errors=poly_errors,
        certificate_status='RESTRICTED_FOUR_CONDITION_ROOT_CERTIFIED' if certified else 'UNRESOLVED_IN_FIXED_BOX',
        interpretation='Necessary initial construction only; requires separate quartic scalar-current control; no full admission or evolution',
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',mpmath=mp.__version__,sympy=sy.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'summary.json';f.write_bytes(data);Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','certificate_status','G1_complete')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
