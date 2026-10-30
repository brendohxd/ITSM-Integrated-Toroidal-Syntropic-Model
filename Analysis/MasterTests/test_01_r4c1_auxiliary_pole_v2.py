"""Exact initial cusp source balance and conservative local remainder proof.

Conditional on the pinned action, initial preparation and inherited bounds;
not an exclusion of every weak solution or physical clearance.
"""
import argparse,ast,hashlib,importlib.util,inspect,json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_time_tangent_v1_attempt_01/summary.json'
PSHA='9f31eb918c2ef34ccbbc372d6d9e99a44c528385e65cb94a58f985592cc23555'
KIN='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
SCALAR='Analysis/MasterTests/outputs/r4c1_quartic_scalar_bound_v1_attempt_01/summary.json'
TOTAL='Analysis/MasterTests/outputs/r4c1_quartic_total_jerk_v1_attempt_01/summary.json'
FORCES='Analysis/MasterTests/outputs/r4c1_quartic_complement_force_v3_attempt_01/summary.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
DISK='Analysis/MasterTests/r4c1_cauchy_disk_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_AUXILIARY_POLE_V1_CONTRACT_2026-10-29.md'
CLOCK='Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json'
V1='Analysis/MasterTests/test_01_r4c1_auxiliary_pole_v1.py'
FAILED='Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v1_attempt_01/summary.json'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_AUXILIARY_POLE_V2_IMPLEMENTATION_NOTE_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda v:mp.nstr(v,65)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def endpoint(q):
    sign,man,exponent,_=q
    return F((-1 if sign else 1)*man)*F(2)**exponent


def upper(record):return endpoint(record['exact_binary_endpoints'][1])


def rational(x):return F(int(x.p),int(x.q))


def reg_coefficients(w,H,HB,Zb,Zd,Zz,wp,R,Rp,b):
    # Restrict only field VALUES to diagonal h,V=(0,u,0); vary before insertion.
    h1,h2,h3,u,zz=s.symbols('h1 h2 h3 u zz',positive=True)
    v1,v2,v3,vu,vz,vn,vhyz=s.symbols('v1 v2 v3 vu vz vn vhyz')
    d1,d2,d3,du,dz,dn,dhyz,sy=s.symbols('d1 d2 d3 du dz dn dhyz sy')
    vol=s.sqrt(h1*h2*h3);c=h2*u*u;gam=s.sqrt(1+c)
    a0=h2*u*(vu-R*du)+u*u*(v2-R*d2)
    an=gam*(vn-R*dn)+gam*u*(vhyz-R*dhyz-h2*sy)/h3-u*u*d2/(2*h3)
    pi0=-b*vol*(c*vz-c*R*dz+zz*a0)
    piz=-b*vol*(-c*R*vz+(1/h3+c*R*R)*dz+zz*(an-R*a0))
    coords=(h1,h2,h3,u,zz);vel=(v1,v2,v3,vu,vz);space=(d1,d2,d3,du,dz)
    C=[s.diff(pi0,v) for v in vel];D=[s.diff(piz,v) for v in vel]
    Dt=lambda expr:sum(s.diff(expr,q)*v for q,v in zip(coords,vel))
    Dz=lambda expr:sum(s.diff(expr,q)*d for q,d in zip(coords,space))+s.diff(expr,R)*Rp
    sub={h1:1,h2:1,h3:1,u:w,zz:Zb,v1:2*H,v2:2*H,v3:2*H,vu:-HB*w,vz:Zd,vn:0,vhyz:0,
         d1:0,d2:0,d3:0,du:wp,dz:Zz,dn:0,dhyz:0,sy:0}
    clean=lambda expr:s.factor(s.cancel(expr.subs(sub)))
    AA=[clean(s.diff(pi0,q)+2*Dt(ci)+Dz(di)) for q,ci,di in zip(coords,C,D)]
    BB=[clean(s.diff(pi0,d)+di) for d,di in zip(space,D)]
    CC=[clean(ci) for ci in C]
    return AA,BB,CC,dict(pi0=str(pi0),piz=str(piz))


def interval(expr,box):
    if expr.is_Rational:return mp.iv.mpf(int(expr.p))/int(expr.q)
    if expr.is_Symbol:return box[expr]
    if expr.is_Add:return sum((interval(t,box) for t in expr.args),mp.iv.mpf(0))
    if expr.is_Mul:
        out=mp.iv.mpf(1)
        for t in expr.args:out*=interval(t,box)
        return out
    if expr.is_Pow and expr.exp.is_Integer:return interval(expr.base,box)**int(expr.exp)
    raise ValueError('unverified interval expression '+str(expr))


def bound(expr,box,disk):
    val=abs(interval(s.cancel(expr),box));return disk.outward(endpoint(val._mpi_[1]),64)


def calculate():
    mp.mp.dps=140;mp.iv.dps=80;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        rows=list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(z) for v in rows if (z:=s.factor(s.cancel(v)))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name,want in parent['file_sha256'].items():pins[(Path(PARENT).parent/name).as_posix()]=want
    for path in (CONTRACT,DISK,V1,FAILED,ADDENDUM,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify();ch=load('pole_original_registered',CHARGE);ch.setup();mp.mp.dps=140
    disk=load('pole_exact_disk',DISK)
    eta=s.Symbol('eta');par={key:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
          for key,v in READ(PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    bg=ast.parse((ROOT/ch.en.body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in bg.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='PARAMS' for z in t.targets))
    shared={v.arg:s.Rational(s.sympify(ast.unparse(v.value))) for v in call.keywords}
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
               mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    check('parameters_exact_rationals',all(v.is_Rational for v in par.values()))
    K,A,b,beta=[par[key] for key in ('K_Q','A','b','beta')];p=s.Rational(1,20);radius=F(1,1000)
    # Verify inherited envelopes from exact binary endpoints, not displayed decimals.
    scalar=READ(SCALAR)['bounds'];total=READ(TOTAL)['bounds']
    for name,key,want in [('aPsi','aPsi',F(13,100)),('complement','complement_full_acceleration',F(30)),
                         ('T','Tmax',F(21,100000)),('Tprime','Tprime',F(1,20)),
                         ('Rprime','Qmax',F(9,1000000)),('Rsecond','Rsecond',F(1,1000))]:
        check('inherited_envelope_'+name,upper(scalar[key])<want)
    check('inherited_envelope_aPsi_z',upper(total['aPsi_normal_derivative'])<F(13,1000))
    check('inherited_envelope_scalar_jerk',upper(total['total_jerk_near'])<134)
    check('inherited_envelope_complement_inverse',upper(READ(KIN)['attempts'][-1]['inverse_bound'])<25)
    check('inherited_envelope_Ud',max(abs(endpoint(x)) for x in READ(FORCES)['Ud_box']['exact_binary_endpoints'])<100)
    certs=READ(ch.en.body.lift.cop.CERTS);cert=next(row for row in certs if row['family']=='new_B1_frame' and row['eta']=='1/4')
    HBupper=upper(cert['H_background']);check('inherited_H_HB_U_envelopes',F(51,50)*HBupper<1 and F(51,50)*(HBupper*F(1,20)+rational(beta)*F(1,5)/rational(K))<1)
    phase=s.Rational(1,2)/(1-par['zeta']*s.Rational(1,4)*s.Rational(1,500)**2/2)
    check('polydisc_contains_registered_first_jets',phase<1 and (2*radius+4*38*radius**3)*F(2,25)<1 and radius**2*(1+38*radius**2)<F(1,1000))
    # Exact AST partition: remove only the nonanalytic cubic summand.
    body=ch.en.body;tree=ast.parse(inspect.getsource(body.body));fun=tree.body[0]
    force=next(t for t in fun.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='force' for z in t.targets))
    expected=ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body
    assert ast.dump(force.value)==ast.dump(expected),'original force assignment drift'
    regnode=next(t for t in fun.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='reg' for z in t.targets))
    regexpected=ast.parse("par['b']*q[13]**2/2-par['b']*(dot(gz,mv(hp,gp))+q[13]*dot(acc,gp))",mode='eval').body
    check('original_regulator_assignment',ast.dump(regnode.value)==ast.dump(regexpected))
    force.value=force.value.left;fun.name='pole_bound_analytic_body';ast.fix_missing_locations(tree)
    exec(compile(tree,'<pinned-original-analytic-majorant>','exec'),body.__dict__)
    oldbody,oldsqrt,oldpar=body.body,body.sqrt,ch.en.par
    try:
        body.body=body.pole_bound_analytic_body;body.sqrt=lambda x:x.sqrt() if isinstance(x,disk.Disk) else oldsqrt(x)
        ch.en.par={key:rational(v) for key,v in par.items()};ch.en.par['A']=F(0)
        disk.reset();Lball=ch.en.density(disk.initial_polydisc())[0];majorant=disk.summary(Lball)
    finally:body.body=oldbody;body.sqrt=oldsqrt;ch.en.par=oldpar
    check('majorant_all_complex_denominators_and_branches_safe',F(majorant['minimum_inverse_margin'])>0 and F(majorant['minimum_sqrt_margin'])>0)
    Baction=F(majorant['integer_upper']);delta=F(1,1000)
    H2=2*Baction/delta**2;H3=6*Baction/delta**3
    Acoef=2*H2+84*H3;Bcoef=2*H2
    w,H,HB,U,Ud,W,T,Rp,wp,aa,az,jj,vy,hy,tr,Tp,Rpp=s.symbols('w H HB U Ud W T Rp wp aPsi aPsi_z jPsi aVy_over_w aHyy trace_a Tprime Rsecond',real=True)
    Zb=w*w*(U+W*w*w);Zd=Ud*w*w;Zz=2*w*(U+2*W*w*w)*wp;R=s.Symbol('R',real=True)
    AR,BR,CR,currents=reg_coefficients(w,H,HB,Zb,Zd,Zz,wp,R,Rp,b)
    AR=[s.factor(v.subs(R,w*T)) for v in AR];BR=[s.factor(v.subs(R,w*T)) for v in BR];CR=[s.factor(v.subs(R,w*T)) for v in CR]
    C=s.zeros(12,1);C[3]=CR[1];C[7]=CR[3]
    originalC=s.Matrix([s.sympify(z,locals={'w':w,'Z':s.Symbol('Z')}).subs(s.Symbol('Z'),Zb) for z in READ(KIN)['formulas']['C']])
    zero('generic_regulator_current_matches_full_mass_crosses',C-originalC)
    zero('regulator_auxiliary_current_coefficients',s.Matrix([CR[4]+b*w*w,AR[4]-b*w*w*(-12*H+5*HB+Rp+3*T*wp),BR[4]-2*b*w**3*T]))
    # Complete initial cusp response, all metric crosses retained.
    BB=s.Matrix([[s.sympify(z,locals={'w':w}) for z in row] for row in READ(KIN)['formulas']['B']])
    idx=(0,3,5,7);r=s.zeros(12,1)
    f=s.Matrix([-A*p**3*w**3/2,-2*A*p**3*w**3,-A*p**3*w**3/2,-3*A*p**3*w*w])
    rr=(BB.extract(idx,idx).inv(method='DM')*f).applyfunc(s.cancel)
    for i,val in zip(idx,rr):r[i]=val
    allf=s.zeros(12,1)
    for i,val in zip(idx,f):allf[i]=val
    zero('full_complement_cusp_response',BB*r-allf)
    jpos=s.cancel(-p*(r[7]/w+(r[0]+r[3]+r[5])/2));lead=s.Rational(9,560000)
    zero('exact_scalar_cusp_leading_coefficient',s.limit(jpos/w,w,0)-lead)
    Qz=s.cancel((C.T*r)[0]/(b*w**3)+A/b*(2*beta*p**3-3*p*p*(6*H-3*HB-3*T*wp-Rp)-6*p*aa))
    Qzz=s.cancel(s.diff(Qz,w)*wp-s.diff(Qz,wp)*1600*w+s.diff(Qz,T)*Tp+s.diff(Qz,Rp)*Rpp+s.diff(Qz,aa)*az)
    RK=s.cancel(K*((1+w*w)*jpos+p*(w*w*r[3]+2*w*r[7])+(1+w*w)*p*(r[0]+r[3]+r[5])/2-lead*w)/w**3)
    # Exact cubic-current derivative, formed after differentiating the generic projector current.
    D=H-HB;uu=hy-8*H*HB+2*HB**2+2*vy
    root=p*w;st=w*(p*D+aa);sz=p*wp;stz=wp*(p*D+aa)+w*az
    stt=w*(jj+2*D*aa+p*(uu/2-D**2)-w*T*az)
    q0=w*w*p;q0t=w*w*(2*D*p+aa);q0tt=w*w*(p*uu+4*D*aa+jj-w*T*az)
    qz=-w**3*T*p;qzz=-p*w*w*(2*T*wp+Rp);qzt=-w**3*T*(2*D*p+aa)
    qztz=-w*w*((2*T*wp+Rp)*(2*D*p+aa)+w*T*az)
    cubic=s.cancel(3*A*((3*H*H+tr/2)*root*q0+6*H*(st*q0+root*q0t)+stt*q0+2*st*q0t+root*q0tt
            +3*H*(sz*qz+root*qzz)+stz*qz+st*qzz+sz*qzt+root*qztz)/w**3)
    normalized=[jpos/w,RK,Qz,Qzz]+[s.cancel(r[i]/w**2) for i in idx]+[s.cancel(s.diff(r[i],w)/w) for i in idx]
    normalized +=[s.cancel(x/w) for x in AR[:4]]+[s.cancel(x/w**2) for x in BR[:4]]+[s.cancel(C[i]/w**2) for i in idx]
    originals=normalized
    normalized=[s.cancel(v) for v in originals]
    zero('exact_normalization_preserves_all_source_functions',s.Matrix([a-b for a,b in zip(originals,normalized)]))
    check('all_normalized_source_denominators_removable',all(s.denom(v).subs(w,0)!=0 for v in normalized))
    def ivpair(lo,hi):
        lower=mp.iv.mpf(lo.numerator)/lo.denominator;higher=mp.iv.mpf(hi.numerator)/hi.denominator
        return mp.iv.mpf([lower.a,higher.b])
    ranges={H:(0,1),HB:(0,1),U:(0,1),Ud:(-100,100),W:(-38,38),T:(-F(21,100000),F(21,100000)),
        Rp:(-F(9,1000000),F(9,1000000)),wp:(-F(2,25),F(2,25)),aa:(-F(13,100),F(13,100)),az:(-F(13,1000),F(13,1000)),
        jj:(-134,134),vy:(-1341,1341),hy:(-30,30),tr:(-90,90),Tp:(-F(1,20),F(1,20)),Rpp:(-F(1,1000),F(1,1000)),w:(-radius,radius)}
    box={var:ivpair(F(lo),F(hi)) for var,(lo,hi) in ranges.items()}
    bd=lambda expr:bound(expr,box,disk)
    Ma=max(bd(s.cancel(r[i]/w**2)) for i in idx)
    Md=F(2,25)*max(bd(s.cancel(s.diff(r[i],w)/w)) for i in idx)
    Mz=bd(Qz);Mzz=F(2,25)*Mz+radius*bd(Qzz)
    CF=sum(bd(s.cancel(C[i]/w**2)) for i in idx);JF=bd(s.cancel(jpos/w))
    check('inherited_full_frame_quotient_envelope',upper(total['analytic_frame_acceleration_quotient'])+Ma*radius<1341)
    forceH=2*rational(A*p*p)*(3*F(13,100)+rational(p)*(4+3))
    forceV=3*rational(A*p*p)*(3*F(13,100)+rational(p)*(6+2))
    Fc=forceH*radius**2+forceV*radius
    Mj=25*(14*Acoef*(Ma*radius+Mz)+12*Bcoef*Md+Fc+CF*radius**2*JF)
    reg=sum(bd(s.cancel(v/w)) for v in AR[:4])*Ma+sum(bd(s.cancel(v/w**2)) for v in BR[:4])*Md
    reg+=bd(s.cancel(AR[4]/w**2))*Mz+2*rational(b)*F(21,100000)*Mzz
    matter=2*rational(beta*A*p**3)*(3*F(21,100000)*F(2,25)+F(9,1000000)+rational(beta*p))
    pieces=dict(quadratic=bd(RK),cubic=bd(cubic),regulator_acceleration=reg,
                matter=matter,all_complement_jerks=CF*Mj)
    remainder=sum(pieces.values());numerator_lead=rational(K*lead);coefficient=rational(K*lead/b)
    n=0
    while F(1,2**n)>radius or 2*remainder*F(1,2**n)**2>numerator_lead:n+=1
    certified=F(1,2**n)
    check('strict_positive_certified_numerator',remainder>0 and numerator_lead>0 and 2*remainder*certified**2<=numerator_lead)
    check('exact_candidate_coefficient',coefficient==F(297,2800000),str(coefficient))
    # Independent full-action datasets check the complete source identity.
    variables=(w,H,HB,U,Ud,W,T,Rp,wp,aa,az,jj,vy,hy,tr,Tp,Rpp)
    evA=s.lambdify(variables,AR,modules='mpmath');evB=s.lambdify(variables,BR,modules='mpmath')
    evC=s.lambdify(variables,C,modules='mpmath');evQ=s.lambdify(variables,[Qz,Qzz,cubic,RK],modules='mpmath')
    pairs={}
    for name in parent['file_sha256']:
        row=READ((Path(PARENT).parent/name).as_posix());pairs.setdefault(row['label'],{})[row['partition_lambda']]=row
    controls=[]
    def mn(z):return mp.mpf(str(s.N(z,135)))
    kn,an,bn,betan,pn=map(mn,(K,A,b,beta,p))
    for label,pair in sorted(pairs.items()):
        old,new=pair[0],pair[1];wv=mp.mpf(new['w']);absw=abs(wv)
        first,_,_,sdd=ch.state(mp.mpf(new['theta']));rv=first[44];rpv=first[47];wpv=first[35]
        tv=rv/wv;tpv=(rpv*wv-rv*wpv)/wv**2
        acc0=mp.matrix(list(map(mp.mpf,old['actual_fourteen_accelerations'])))
        acc1=mp.matrix(list(map(mp.mpf,new['actual_fourteen_accelerations'])))
        ddacc=acc1-acc0
        j0=mp.matrix(list(map(mp.mpf,old['actual_fourteen_third_time_jets'])))
        j1=mp.matrix(list(map(mp.mpf,new['actual_fourteen_third_time_jets'])))
        dj=j1-j0
        az0=mp.matrix(list(map(mp.mpf,old['actual_acceleration_spatial_derivative'])))
        az1=mp.matrix(list(map(mp.mpf,new['actual_acceleration_spatial_derivative'])))
        daz=az1-az0
        val=(wv,ch.en.H,ch.en.vals['H0'],ch.en.U,ch.en.Ud,ch.W4,tv,rpv,wpv,
             acc1[12],az1[12],j1[12],acc1[7]/wv,acc1[3],sum(acc1[i] for i in (0,3,5)),tpv,sdd[2])
        av=mp.matrix(evA(*val));bv=mp.matrix(evB(*val));cv=mp.matrix(evC(*val));qv=evQ(*val)
        quadratic=kn*((1+wv*wv)*dj[12]+pn*(wv*wv*ddacc[3]+2*wv*ddacc[7])+(1+wv*wv)*pn*sum(ddacc[i] for i in (0,3,5))/2)
        regsource=sum(av[k]*ddacc[i]+bv[k]*daz[i] for k,i in enumerate(idx))+av[4]*ddacc[13]+bv[4]*daz[13]
        complement=(cv.T*dj[:12,0])[0]
        rhot=mp.mpf(new['physical_density_rate'])-mp.mpf(old['physical_density_rate'])
        epsdt=mp.mpf(new['multiplier_rate'])-mp.mpf(old['multiplier_rate'])
        density=(rhot-epsdt)/(4*betan*pn)
        matter_source=betan*(rhot+3*ch.en.H*density)
        physical_cubic=absw**3*qv[2]
        right=quadratic-physical_cubic+regsource+complement+matter_source
        left=bn*wv*wv*dj[13]
        err=abs(left-right)/(1+abs(left)+abs(right))
        check('complete_original_scalar_source_identity_'+label,err<mp.mpf('1e-18'),show(err))
        qerr=abs(ddacc[13]-absw*qv[0])/(1+abs(ddacc[13]))
        check('initial_auxiliary_cusp_identity_'+label,qerr<mp.mpf('1e-18'),show(qerr))
        derivative=mp.sign(wv)*wpv*qv[0]+absw*qv[1]
        qderr=abs(daz[13]-derivative)/(1+abs(daz[13]))
        check('initial_auxiliary_cusp_spatial_identity_'+label,qderr<mp.mpf('1e-18'),show(qderr))
        expected_density=2*an*pn**3*absw**3
        expected_rate=expected_density*(3*tv*wpv-3*ch.en.H+rpv+betan*pn)
        merr=max(abs(density-expected_density),abs(rhot-expected_rate))/(1+abs(density)+abs(rhot))
        check('independent_Hamiltonian_matter_cusp_current_'+label,merr<mp.mpf('1e-18'),show(merr))
        controls.append(dict(label=label,source_identity_error=show(err),auxiliary_identity_error=show(qerr),
                             auxiliary_spatial_identity_error=show(qderr),matter_identity_error=show(merr)))
    # Generic mixed-Z channel absence is structural: only psi derivatives pair with grad Z.
    # Verify it also on the original full-action Hessians, without a reduced field truncation.
    for row in READ(CLOCK)['points']:
        raw=READ(row['raw_point_source']);hh=raw['full_Hessian']
        defect=max(abs(mp.mpf(hh[16+i][45]))+abs(mp.mpf(hh[32+i][29])) for i in range(12))
        check('complete_complement_mixed_Z_channel_absent_'+row['label'],defect==0,show(defect))
        gauge=max(abs(mp.mpf(hh[29][j])) for j in range(48,54))
        check('auxiliary_row_free_shift_source_zero_'+row['label'],gauge==0,show(gauge))
    gauge_ratio=s.cancel((w*w*Zz+Zb*w*wp)/(w*w))
    zero('free_shift_scalar_source_regular_quotient',gauge_ratio-w*(3*U+5*W*w*w)*wp)
    acoef=s.Symbol('residue',real=True);positive_lead=s.Rational(297,2800000)
    check('two_sided_meromorphic_residue_cannot_cancel_cusp',s.solve([acoef+positive_lead,acoef-positive_lead],[acoef])==[])
    small=s.Symbol('small',positive=True)
    check('inverse_distance_not_locally_integrable',s.limit(-s.log(small),small,0,dir='+')==s.oo)
    verify()
    result=dict(result_id='R4C1-AUXILIARY-POLE-V2',source_sha256=pins,checks=checks,
        majorant=majorant,cauchy=dict(radius=str(delta),action_bound=str(Baction),second_derivative_bound=str(H2),third_derivative_bound=str(H3)),
        envelopes={key:str(value) for key,value in dict(Ma=Ma,Md=Md,Mz=Mz,Mzz=Mzz,CF=CF,JF=JF,Mj=Mj).items()},
        remainder_pieces={key:str(value) for key,value in pieces.items()},remainder_B=str(remainder),
        numerator_coefficient=str(numerator_lead),pole_coefficient=str(coefficient),certified_radius=str(certified),certified_radius_power=n,
        formulas=dict(regulator_A=[str(v) for v in AR],regulator_B=[str(v) for v in BR],mass_crosses=[str(v) for v in C],
          quadratic_remainder=str(RK),cubic_normalized=str(cubic),initial_auxiliary_cusp_quotient=str(Qz),initial_auxiliary_cusp_quotient_derivative=str(Qzz),
          scalar_cusp_positive_branch=str(jpos),original_regulator_currents=currents),
        normalized_source_balance='abs(b*w^2*delta(jZ)-K_Q*(9/560000)*abs(w))<=B*abs(w)^3',
        controls=controls,auxiliary_partition_pole_certified=all(c['passed'] for c in checks),
        physical_third_time_locally_L1_class_excluded=all(c['passed'] for c in checks),
        regularity_scope='Registered initial data; differentiated Euler equations valid off nodes; original unit lapse and bounded second-time shift jets. No all-C2/distributional weak-solution exclusion.',
        all_weak_solutions_excluded=False,time_evolution=False,
        working_digits=140,interval_digits=80,physics_pass=False,gate_effect='NONE',G1_complete=False,review_status='DEFERRED',Rule9_cleared=False)
    return result


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args();r=calculate();r['passed']=sum(c['passed'] for c in r['checks']);r['total']=len(r['checks']);data=ENC(r)
    if a.replay:
        if (a.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);f=a.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    message={key:r[key] for key in ('passed','total','certified_radius','pole_coefficient','auxiliary_partition_pole_certified','G1_complete','physics_pass')}
    fb=F(r['remainder_B']);message['remainder_B_decimal']=mp.nstr(mp.mpf(fb.numerator)/fb.denominator,12)
    print(json.dumps(message))
    raise SystemExit(0 if r['passed']==r['total'] else 2)


if __name__=='__main__':main()
