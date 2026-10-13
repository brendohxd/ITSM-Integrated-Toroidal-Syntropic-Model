"""V3 explicit single-indeterminate algebra for charge/density drift continuation.

No old ODE integrations, ensemble changes, physical cutoff or gate promotion.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

import mpmath as mp
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
PARENT = BASE + 'r4c1_retarded_cubic_backreaction_attempt_02/'
PLANAR = BASE + 'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
KERNEL = BASE + 'r4c1_g3n5_attempt_02/kernel.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_DOMAIN_V1_CONTRACT_2026-10-13.md'
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_GR_CONTROL_ADDENDUM_2026-10-13.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PINS = {CONTRACT: '904f67b4889f8872eb95a057c3126db7de848a264b6c016513aa810a0c546bac',
        ADDENDUM: '27d5b01a90b7b6b320f8b0ff08520664f24ee6ac92a1190ac97eb3d01bc01286',
        'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_DOMAIN_V2_BINDING_ADDENDUM_2026-10-13.md':
        'e77f4c6802358dc0870e72b487431abdfcdd336702cad288778448c545e8ddaa',
        'Analysis/MasterTests/test_01_r4c1_three_family_charge_domain_v1.py':
        'd79224d5ba19f8e19894d1c26e643826d23375358551de1eae977e3b54f8a783',
        'Analysis/MasterTests/test_01_r4c1_three_family_charge_domain_v2.py':
        '061aeef8707f16790bfc25b8dd8e5a108e78bf71accb73f2a32e6d128e9817ea',
        'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_DOMAIN_V3_ALGEBRA_ADDENDUM_2026-10-13.md':
        '0bb5b67993f501f1cb5d96a6602dcbe91c1688bf79cd40c30f13fcedb3b015a6',
        PARENT+'summary.json': '40424d9dca24ff5d6b9107432545b839274b0fa72238256ba4994c71e1522038',
        'Theory/Gates/RES-001/RES001_R4C1_RETARDED_CUBIC_BACKREACTION_V2_REPORT_2026-10-13.md':
        '782ee5d6a21bcabfeb2b99947c54e9c1b048cfcfd67e11bdcaa1f3ca34cfcd99',
        'Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_REPORT_2026-10-11.md':
        '331b596dada0073ee1d50da69d3a8bbb8475c0b9cd7b8b246c5d03c7d536339f'}
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz','Vx','Vy','Vz',
          'du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IDX = {n:i for i,n in enumerate(FIELDS)}
DYN = FIELDS[4:10] + FIELDS[10:17]
FAMILIES = ('archived_G3','new_B1_frame','new_hierarchical')
sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda n: json.loads((ROOT/n).read_bytes())
encode = lambda x: (json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
unpack = lambda x: np.asarray(x)[...,0]+1j*np.asarray(x)[...,1]
PROGRESS = None


def progress(**row):
    print(json.dumps(row,sort_keys=True),flush=True)
    if PROGRESS:
        with PROGRESS.open('a',encoding='utf-8') as f:
            f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n')


def clean(x):
    return s.factor(s.cancel(s.expand(x)))


class Checks:
    def __init__(self): self.rows=[]; self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names: raise ValueError('Duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def exact(self,name,x,expanded=False):
        vals=list(x) if isinstance(x,(s.MatrixBase,list,tuple)) else [x]
        bad=[]
        for i,v in enumerate(vals):
            r=s.expand(v) if expanded else clean(v)
            if r!=0: bad.append(dict(index=i,residual=str(r)))
        self.add(name,not bad,bad,'zero_exact')


def collect():
    ps=read(PARENT+'summary.json'); pins=dict(ps['source_sha256'])
    pins.update({PARENT+n:h for n,h in ps['artifacts'].items()});pins.update(PINS)
    pins[SELF]=sha((ROOT/SELF).read_bytes())
    for n,h in pins.items():
        if sha((ROOT/n).read_bytes())!=h: raise RuntimeError('Frozen source drift '+n)
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import test_01_r4c1_retarded_cubic_backreaction_v2 as ret
    common,prior,time,entry,generic,_,_=ret.imports_and_pins()
    absent=common.inspect_pins(pins)
    paths=[ROOT/n for n in pins]
    paths += [Path(str(p)+'.sha256') for p in list(paths) if Path(str(p)+'.sha256').exists()]
    snapshot=lambda: [(str(p.relative_to(ROOT)),sha(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in paths]
    return common,ret,prior,time,entry,generic,pins,absent,snapshot


def variational_currents(checks):
    u,v,d,zeta,eps,C=s.symbols('u v density zeta epsilon C',real=True)
    uj=s.symbols('u_t u_x u_y u_z',real=True); vj=s.symbols('v_t v_x v_y v_z',real=True)
    tj=s.symbols('tau_t tau_x tau_y tau_z',real=True)
    g=s.zeros(4);h=s.zeros(4)
    for i in range(4):
        for j in range(i,4):
            g[i,j]=g[j,i]=s.Symbol('g%d%d'%(i,j),real=True)
            h[i,j]=h[j,i]=s.Symbol('h%d%d'%(i,j),real=True)
    J=s.Matrix([v*a-u*b for a,b in zip(uj,vj)])
    uu,vv,tt=map(s.Matrix,(uj,vj,tj))
    m,l4,l6,scale,portal,r=s.symbols('m2 lambda4 lambda6 Lambda g_r reservoir',real=True)
    radius2=u*u+v*v
    pot=m*radius2/2+l4*radius2**2/8+l6*radius2**3/(24*scale**2)+portal*radius2*r*r/4
    L=-d*((uu.T*g*uu)[0]+(vv.T*g*vv)[0])/2-d*zeta*(J.T*h*J)[0]/2-d*pot
    pu=s.Matrix([s.diff(L,q) for q in uj]);pv=s.Matrix([s.diff(L,q) for q in vj])
    current=-v*pu+u*pv
    checks.exact('direct_rotation_momenta_vs_full_tensor_current',current-d*(g+zeta*radius2*h)*J,True)
    dpiu=s.symbols('dt_pi_u dx_pi_u dy_pi_u dz_pi_u',real=True)
    dpiv=s.symbols('dt_pi_v dx_pi_v dy_pi_v dz_pi_v',real=True)
    Eu=s.diff(L,u)-sum(dpiu);Ev=s.diff(L,v)-sum(dpiv)
    divergence=sum(-vj[i]*pu[i]-v*dpiu[i]+uj[i]*pv[i]+u*dpiv[i] for i in range(4))
    checks.exact('off_shell_rotation_Noether_with_arbitrary_momentum_coefficient_drift',divergence-v*Eu+u*Ev,True)
    Lm=-d*eps*(C*C*(tt.T*g*tt)[0]+C**4)/2
    pt=s.Matrix([s.diff(Lm,q) for q in tj])
    checks.exact('direct_dust_momenta_vs_full_tensor_current',pt+d*eps*C*C*g*tt,True)
    dpit=s.symbols('dt_pi_tau dx_pi_tau dy_pi_tau dz_pi_tau',real=True)
    checks.exact('off_shell_dust_shift_Noether',s.diff(Lm,s.Symbol('tau',real=True))-sum(dpit)+sum(dpit),True)
    e,vol,tr,alpha,beta,pi,w,co=s.symbols('e volume trace alpha beta Pi w cos_wave',real=True)
    du,dv,dud,dvd,ud,vd,E,Td,rho=s.symbols('du dv du_dot dv_dot u_dot v_dot Em T_dot rho',real=True)
    j=u*vd-v*ud
    qexpr=vol*(1+e*e*tr/2)/(1+e*e*alpha)*(1-zeta*((u+e*e*du)**2+(v+e*e*dv)**2)*e*e*w*w*co*co)
    qexpr *= (u+e*e*du)*(vd+e*e*dvd)-(v+e*e*dv)*(ud+e*e*dud)
    q2=s.expand(s.series(qexpr,e,0,3).removeO().coeff(e,2)).subs(co**2,s.Rational(1,2))
    expected=vol*(u*dvd+du*vd-v*dud-dv*ud+(tr/2-alpha)*j-zeta*radius2*j*w*w/2)
    checks.exact('formal_second_order_periodic_U1_current',q2-expected)
    pexpr=vol*(1+e*e*tr/2)*(eps+e*e*E)*(C*s.exp(beta*e*e*pi))**2*(C+e*e*Td)/(1+e*e*alpha)
    p2=s.expand(s.series(pexpr,e,0,3).removeO().coeff(e,2)).subs(eps,rho/C**4)
    expectedP=vol*C**3*E+vol*rho/C*(tr/2-alpha+2*beta*pi+Td/C)
    checks.exact('formal_second_order_full_dust_current',p2-expectedP)
    checks.exact('dust_clock_weight_is_THREE_beta',expectedP.subs({alpha:-beta*pi,Td:0})-vol*C**3*E-vol*rho/C*(tr/2+3*beta*pi))
    eta=s.Symbol('eta',positive=True)
    initial=expected.subs({vol:1,u:s.sqrt(eta),v:0,ud:0,vd:s.sqrt(eta),du:0,dv:0,dud:0,dvd:0,tr:0,alpha:0,w:1,zeta:eta/13})
    checks.exact('initial_exact_recipe_charge_shift',initial+eta**3/26)
    checks.add('reject_omitted_alignment_current',clean(s.diff(expected,zeta))!=0)
    checks.add('reject_omitted_mean_volume_or_density',s.diff(expected,tr)!=0 and s.diff(expectedP,E)!=0)
    return dict(rotation_current=[str(q) for q in current],dust_current=[str(q) for q in pt],
                Q2=str(expected),P2=str(expectedP),initial_Q2=str(initial),
                drift_scope='Momentum derivatives arbitrary: full product-rule off-shell Noether identity, not set to zero')


class Compiler:
    def __init__(self,generic,checks):
        progress(stage='GENERIC_MEAN_ACTION_AND_CHARGE_COMPILER')
        kernel=generic.GenericKernel();data=read(PLANAR)
        checks.add('field_order_is_complete_bijection',tuple(data['field_order'])==FIELDS==tuple(generic.FIELDS))
        names=set(kernel.sy)
        for row in data['response_coefficients'].values():
            for text in row.values(): names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',text))
        names.update('rho eta w wd k Hdot MP2 MU2 c1 c2 c3 c4 K_Q b beta zeta m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda'.split())
        names.update('W W_t W_x W_z B B_t B_x B_z'.split())
        x={n:s.Symbol(n,real=True) for n in names};self.x=x
        a,H,u,ud,v,vd,r,rd,pd,rho,C=[x[n] for n in ('a','H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho','C')]
        MP,MU,c1,c2,c3,c4,K,b,beta,zeta=[x[n] for n in ('MP2','MU2','c1','c2','c3','c4','K_Q','b','beta','zeta')]
        MC=MP+MU*(c1+3*c2+c3)/2;MT=MP-MU*(c1+c3);f2=MU*(c1+c4)
        vol=a**3;radius2=u*u+v*v;j=u*vd-v*ud
        pot=x['m2']*radius2/2+x['lambda4']*radius2**2/8+x['lambda6']*radius2**3/(24*x['Lambda']**2)
        pot+=x['mr2']*r*r/2+x['lambda_r']*r**4/4+x['g_r']*radius2*r*r/4+x['rho_Lambda']
        kin=ud*ud+vd*vd+rd*rd+K*pd*pd
        Hd=-(kin+rho)/(2*MC)
        mass=x['m2']+x['lambda4']*radius2/2+x['lambda6']*radius2**2/(4*x['Lambda']**2)+x['g_r']*r*r/2
        rate={a:a*H,H:Hd,u:ud,ud:-3*H*ud-mass*u,v:vd,vd:-3*H*vd-mass*v,
              r:rd,rd:-3*H*rd-x['mr2']*r-x['lambda_r']*r**3-x['g_r']*radius2*r/2,
              pd:-3*H*pd-beta*rho/K,rho:(-3*H+beta*pd)*rho,C:beta*pd*C}
        frame_mass=-(3*c2+c3-c4)/(c1+c4)*Hd+2*H*H-K*pd*pd/f2+zeta*j*j/f2
        cv=(MU*c1+MU**2*(c1+c3)**2/(2*MT))/f2
        w,wd,k=x['w'],x['wd'],x['k'];rate.update({w:wd,wd:-3*H*wd-(cv*k*k/a**2+frame_mass)*w})
        dt=lambda q:s.expand(sum(s.diff(q,z)*value for z,value in rate.items() if z in q.free_symbols))
        self.dt=dt
        background={x['epsilon0']:rho/C**4,x['lambda0']:3*MU*c2*Hd-3*MU*(c1+c3)*H**2,x['Hdot']:Hd}
        blocks=[s.zeros(22) for _ in range(4)]
        for rec in kernel.records:
            bi,i=divmod(rec['row'],22);bj,jj=divmod(rec['column'],22)
            slot={(0,0):0,(0,1):1,(1,0):2,(1,1):3}.get((bi,bj))
            if slot is not None:
                blocks[slot][i,jj]=s.sympify(rec['value'],locals=x).subs(background)
        LA,LB,LBT,LK=blocks
        F=s.zeros(22,13)
        for n,name in enumerate(DYN):F[IDX[name],n]=1
        F[IDX['alpha'],DYN.index('Pi')]=-beta
        iz=IDX['Z'];alpha=IDX['alpha'];em=IDX['Em']
        checks.exact('lapse_has_no_velocity_momentum',LBT.row(alpha))
        checks.exact('mean_Z_value_and_velocity_couplings_before_elimination',list((LA.row(iz)*F))+list((LB.row(iz)*F)))
        checks.exact('mean_density_not_in_projected_physical_equations',F.T*LA[:,em])
        checks.exact('mean_regulator_not_in_projected_physical_equations',list(F.T*LA[:,iz])+list(F.T*LB[:,iz])+list(F.T*LBT[:,iz]))
        checks.exact('lapse_density_coefficient',LA[alpha,em]+C**4)
        checks.exact('no_density_velocity_or_acceleration_in_lapse',list(LB.row(alpha)[:,[em]])+list(LK.row(alpha)))
        Kphys=F.T*LK*F
        P=s.eye(13);P[:6,:6]=s.zeros(6)
        for name in ('Mxx','Myy','Mzz'):P[DYN.index(name),0]=s.Rational(2,3)
        P[DYN.index('Mxx'),1]=1/s.sqrt(2);P[DYN.index('Myy'),1]=-1/s.sqrt(2)
        P[DYN.index('Mxx'),2]=P[DYN.index('Myy'),2]=1/s.sqrt(6);P[DYN.index('Mzz'),2]=-2/s.sqrt(6)
        for col,name in enumerate(('Mxy','Mxz','Myz'),3):P[DYN.index(name),col]=1/s.sqrt(2)
        diag=[-2*MC/3]+[MT/4]*5+[f2]*3+[1,1,1,K]
        checks.exact('generic_full13_mean_kinetic_congruence',P.T*Kphys*P-s.diag(*diag))
        inv=P*s.diag(*(1/q for q in diag))*P.T
        checks.exact('generic_kinetic_inverse',Kphys*inv-s.eye(13))
        norm=s.Matrix([[-2*MC/3,-MU*c2],[-MU*c2,-MU*(c1+c2+c3+c4)]])
        B=s.zeros(22,2)
        for name in ('Mxx','Myy','Mzz'):B[IDX[name],0]=s.Rational(2,3)
        B[IDX['nu'],1]=1
        checks.exact('generic_normal_principal_block_before_constraint',B.T*LK*B-norm)
        detnorm=clean(norm.det());hnu=clean(-2*MC/(3*vol*detnorm))
        checks.exact('normal_domain_recovers_oldB1_only_as_control',hnu.subs({MP:1,MU:s.Rational(2,3),c1:s.Rational(1,5),c2:s.Rational(1,10),c3:-s.Rational(1,5),c4:s.Rational(1,20)})+s.Rational(330,31)/vol)
        EA=LA-LBT.applyfunc(dt)-3*H*LBT;EB=LB-LBT-LK.applyfunc(dt)-3*H*LK
        Ar=F.T*EA*F;Br=F.T*EB*F
        co,si=s.symbols('wave_cos wave_sin',real=True);sigma=-MU*(c1+c3)/MT
        wave={x['W']:w*co,x['W_t']:wd*co,x['W_x']:0,x['W_z']:-k*w*si,
              x['B']:sigma*w*co,x['B_t']:sigma*wd*co,x['B_x']:0,x['B_z']:-sigma*k*w*si}
        def average(expr):
            pol=s.Poly(s.expand(expr.subs(wave).subs(background)),co,si)
            if any(sum(power)!=2 for power,value in pol.terms() if value!=0):
                raise ValueError('Unexpected nonquadratic source harmonic')
            return clean((pol.coeff_monomial(co**2)+pol.coeff_monomial(si**2))/2)
        sources=[]
        for field in FIELDS:
            row=data['response_coefficients'][field]
            av0=average(s.sympify(row['value'],locals=x));avt=average(s.sympify(row['t'],locals=x))
            sources.append(clean(av0-dt(avt)-3*H*avt))
            progress(stage='MEAN_SOURCE_COMPILED',field=field)
        source=s.Matrix(sources);force=F.T*source
        aq=s.zeros(1,13);bq=s.zeros(1,13)
        for name in ('Mxx','Myy','Mzz'):aq[0,DYN.index(name)]=vol*j/2
        aq[0,DYN.index('Pi')]=vol*beta*j;aq[0,DYN.index('du')]=vol*vd;aq[0,DYN.index('dv')]=-vol*ud
        bq[0,DYN.index('du')]=-vol*v;bq[0,DYN.index('dv')]=vol*u
        oq=-vol*zeta*radius2*j*w*w/2
        ae=LA.row(alpha)*F/C**4;be=LB.row(alpha)*F/C**4;oe=source[alpha]/C**4
        ap=vol*C**3*ae;bp=vol*C**3*be
        for name in ('Mxx','Myy','Mzz'):ap[0,DYN.index(name)]+=vol*rho/C/2
        ap[0,DYN.index('Pi')]+=3*vol*rho/C*beta
        op=vol*source[alpha]/C
        constraint=3*MC*H*H-kin/2-pot-rho
        constraint_poly=s.Poly(constraint,H,domain='EX')
        def shell(expr):
            if expr==0:return s.Integer(0)
            num,den=s.fraction(s.together(expr))
            return clean(s.Poly(num,H,domain='EX').rem(constraint_poly).as_expr()/den)
        self.shell=shell
        for label,aa,bb,off in (('U1',aq,bq,oq),('dust',ap,bp,op)):
            for i,q in enumerate(list(aa.applyfunc(dt)+bb*inv*Ar)+list(aa+bb.applyfunc(dt)+bb*inv*Br)):
                progress(stage='CONSERVATION_ROW_START',charge=label,row=i)
                checks.exact(label+'_generic_conservation_row_'+str(i),shell(q))
                progress(stage='CONSERVATION_ROW_COMPLETE',charge=label,row=i,passed=checks.rows[-1]['passed'])
            progress(stage='FORCED_CONSERVATION_START',charge=label)
            checks.exact(label+'_generic_forced_conservation',shell((bb*inv*force)[0]+dt(off)))
            progress(stage='FORCED_CONSERVATION_COMPLETE',charge=label,passed=checks.rows[-1]['passed'])
        px,pr,prr=s.symbols('px pR pr',real=True)
        volx,MCx,Kx,pp,pt,Cx,cb,xr,Q,V,pclock=s.symbols('volume MC K ppsi ptau C Cbg radius Q V psi_clock_rate',positive=True)
        other=-3*px**2/(4*MCx*volx)+pr**2/(2*volx)+prr**2/(2*volx)+pp**2/(2*Kx*volx)+Q**2/(2*volx*xr**2)+volx*V
        Hd=cb*other/Cx
        hp=-pclock*s.sqrt(2*Kx*volx*(-other+pp**2/(2*Kx*volx)-Cx*pt))
        mixed=s.hessian(hp,(px,pt));radicand=2*Kx*volx*(-other+pp**2/(2*Kx*volx)-Cx*pt)
        checks.exact('generic_dust_clock_negative_volume_curvature',s.diff(Hd,px,2)+3*cb/(2*MCx*volx*Cx))
        checks.exact('generic_force_clock_mixed_negative_determinant',mixed.det()+3*pclock**2*Cx**2*Kx**3*volx**2/(2*MCx*radicand**2))
        checks.exact('exact_GR_dust_negative_volume_countercontrol',s.diff((-3*px**2/(4*MCx*volx)),px,2)+3/(2*MCx*volx))
        self.functions={};domain={}
        packs=dict(Q=s.Matrix([[*list(aq),*list(bq),oq]]),P=s.Matrix([[*list(ap),*list(bp),op]]),
                   E=s.Matrix([[*list(ae),*list(be),oe]]))
        const={x['m2']:1,x['lambda4']:s.Rational(1,3),x['lambda6']:s.Rational(1,5),x['Lambda']:2,
               x['mr2']:2,x['lambda_r']:s.Rational(1,7),x['g_r']:3*x['eta']/7,x['rho_Lambda']:0}
        for family in FAMILIES:
            progress(stage='FAMILY_CHARGE_AND_DOMAIN_START',family=family)
            sub={x[n]:s.sympify(vv,locals=x) for n,vv in data['families'][family]['parameter_map'].items()};sub.update(const)
            values={n:clean(q.subs(sub)) for n,q in dict(Mcos2=MC,MT2=MT,f2=f2,forceK=K,normal_determinant=detnorm,h_nu=hnu).items()}
            domain[family]={n:str(q) for n,q in values.items()}
            for name,expr in packs.items():
                full=list(expr)+[dt(q) for q in expr]
                full=[clean(q.subs(sub)) for q in full]
                order=sorted({str(z) for q in full for z in q.free_symbols})
                self.functions[family,name]=(order,s.lambdify([[x[n] for n in order]],full,'numpy',cse=True))
            for eta in (s.Rational(1,4),s.Rational(1,64),s.Rational(1,1024)):
                checks.add(family+'_registered_positive_domains_'+str(eta),all(values[n].subs(x['eta'],eta)>0 for n in ('Mcos2','MT2','f2','forceK','normal_determinant')))
            interval_var=s.Symbol('positive_interval_coordinate',positive=True)
            for n in ('Mcos2','MT2','f2','forceK','normal_determinant'):
                num,den=s.fraction(s.cancel(values[n].subs(x['eta'],interval_var/(4*(1+interval_var)))))
                positive=lambda expr:all(q>=0 for q in s.Poly(expr,interval_var).all_coeffs()) and expr!=0
                checks.add(family+'_continuous_domain_0_eta_le_1_over_4_'+n,
                           positive(num) and positive(den) and values[n].subs(x['eta'],s.Rational(1,4))>0,
                           dict(numerator=str(num),denominator=str(den)))
            checks.exact(family+'_GR_metric_principal_control_only',
                         [s.limit(values['Mcos2'],x['eta'],0,dir='+')-1,
                          s.limit(values['MT2'],x['eta'],0,dir='+')-1])
            checks.exact(family+'_singular_extra_sectors_at_eta_zero',
                         [values[n].subs(x['eta'],0) for n in ('f2','forceK','normal_determinant')])
            progress(stage='FAMILY_CHARGE_AND_DOMAIN_COMPLETE',family=family)
        self.export=dict(physical_fields=list(DYN),Mcos2=str(MC),MT2=str(MT),f2=str(f2),
            kinetic_congruence=list(map(str,diag)),normal_block=str(norm),normal_determinant=str(detnorm),
            h_nu=str(hnu),domain_families=domain,source_alpha_mean=str(source[alpha]),
            Q2_affine=str(packs['Q']),P2_affine=str(packs['P']),Em_constraint_affine=str(packs['E']),
            background_constraint=str(constraint),generic_dust_clock_H=str(Hd),generic_force_clock_H=str(hp),
            GR_negative_volume_control='Same varying-dust homogeneous sign, not a local propagating ghost criterion',
            full_22_source_order=list(FIELDS),root_scope='Exact generic identity includes root; no unexported root background is interpolated')

    def affine(self,family,name,raw):
        order,fun=self.functions[family,name]
        vals=np.asarray(fun([raw[n] for n in order]),complex).reshape(2,27)
        return vals[0,:26],vals[0,26],vals[1,:26],vals[1,26]


def finite_current(profile,e,angle,p,b):
    mp.mp.dps=80
    cv=lambda v:mp.mpf(repr(float(v)))
    if angle not in (0,np.pi/2):raise ValueError('Only the exact quadratic two-angle control is registered')
    phase=1 if angle==0 else -1
    q=profile[0]+2*(profile[1]*phase).real
    qd=profile[2]+2*(profile[3]*phase).real
    qz=2*(2j*40*profile[1]*phase).real
    a,u,ud,v,vd,psi,rho,w=map(cv,(b[0],b[2],b[3],b[4],b[5],b[8],b[10],b[12]))
    ee=mp.mpf(str(e));co=mp.mpf(1) if angle==0 else mp.mpf(0);beta=cv(p['beta']);zeta=cv(p['zeta'])
    get=lambda name:cv(q[IDX[name]].real)
    h=mp.eye(3);mn=(('Mxx','Mxy','Mxz'),('Mxy','Myy','Myz'),('Mxz','Myz','Mzz'))
    for i in range(3):
        for j in range(3):h[i,j]=a*a*((1 if i==j else 0)+ee*ee*get(mn[i][j]))
    Cbg=mp.exp(beta*psi);Ct=Cbg*mp.exp(beta*ee*ee*get('Pi'));N=Cbg/Ct
    sigma=-cv(p['MU2']*(p['c1']+p['c3']))/cv(p['MP2']-p['MU2']*(p['c1']+p['c3']))
    sh=mp.matrix([ee*ee*get(n)/a for n in ('Sx','Sy','Sz')]);sh[1]+=ee*sigma*w*co/a
    vel=mp.matrix([ee*ee*get(n)/a for n in ('Vx','Vy','Vz')]);vel[1]+=ee*w*co/a
    gamma=mp.sqrt(1+(vel.T*h*vel)[0]);normal=mp.matrix([gamma/N,*list(vel-sh*gamma/N)])
    gi=mp.matrix(4);gi[0,0]=-1/(N*N);hi=h**-1
    for i in range(3):
        gi[0,i+1]=gi[i+1,0]=sh[i]/(N*N)
        for j in range(3):gi[i+1,j+1]=hi[i,j]-sh[i]*sh[j]/(N*N)
    uu=u+ee*ee*get('du');vv=v+ee*ee*get('dv')
    uj=mp.matrix([ud+ee*ee*cv(qd[IDX['du']].real),0,0,ee*ee*cv(qz[IDX['du']].real)])
    vj=mp.matrix([vd+ee*ee*cv(qd[IDX['dv']].real),0,0,ee*ee*cv(qz[IDX['dv']].real)])
    J=vv*uj-uu*vj;dens=mp.sqrt(mp.det(h))*N
    Qcur=dens*sum((gi[0,j]+zeta*(uu*uu+vv*vv)*(gi[0,j]+normal[0]*normal[j]))*J[j] for j in range(4))
    eps=rho/Cbg**4+ee*ee*get('Em');Pcur=-dens*eps*Ct**2*gi[0,0]*Cbg
    return Qcur,Pcur


def numerical(compiler,ret,prior,time,entry,generic,checks):
    mp.mp.dps=80
    ctx=ret.Context(time,prior,generic);red=time.EvolvingReduction(prior,generic)
    records=[];old=read(PARENT+'trajectories.json')['runs']
    for run in old:
        name=run['family'];eta=float(Fraction(run['eta_exact']));p,_=entry.initial_conditions(generic,name,eta)
        states=unpack(run['scaled_response_and_third_states']);rows=[];tag=name+'_'+run['eta_exact']+'_'+run['method']
        for i,(t,b,zfull) in enumerate(zip(run['times'],np.asarray(run['first_order_states']),states)):
            context=ctx.at(name,eta,b[:12],p,b[12],b[13]);s0,_=ctx.fourier(name,context)
            data=red.at(b[:12],p,0,s0[:22],s0[22:]);field=red.reconstruct(data,zfull[:26],p)
            z=zfull[:26];flow=data['G']@z+data['g'];q,qd=field['q'],field['qd']
            raw={**context['raw'],'rho':b[10],'w':b[12],'wd':b[13],'k':40}
            vals={}
            for label in ('Q','P','E'):
                L,o,Ld,od=compiler.affine(name,label,raw)
                value=L@z+o;derivative=Ld@z+L@flow+od
                row= Ld+L@data['G'];forcing=L@data['g']+od
                scale=abs(o)+float(np.sum(abs(L*z)))+eta**3
                if label!='E':
                    checks.add(tag+'_'+str(i)+'_'+label+'_coefficient_row_identity',np.max(abs(row))/(1+np.max(abs(Ld))+np.max(abs(L@data['G'])))<=1e-7,float(np.max(abs(row))))
                    checks.add(tag+'_'+str(i)+'_'+label+'_forced_identity',abs(forcing)/(1+abs(od)+abs(L@data['g']))<=1e-7,float(abs(forcing)))
                vals[label]=dict(value=float(value.real),derivative=float(derivative.real),scale=float(scale))
                checks.add(tag+'_'+str(i)+'_'+label+'_real_mean_current',abs(value.imag)<=1e-10,float(abs(value.imag)))
            tr=sum(q[IDX[n]] for n in ('Mxx','Myy','Mzz'));j=b[2]*b[5]-b[4]*b[3];vol=b[0]**3;C=np.exp(p['beta']*b[8])
            directQ=vol*(b[2]*qd[IDX['dv']]+q[IDX['du']]*b[5]-b[4]*qd[IDX['du']]-q[IDX['dv']]*b[3]+(tr/2-q[0])*j-p['zeta']*(b[2]**2+b[4]**2)*j*b[12]**2/2)
            directP=vol*C**3*q[IDX['Em']]+vol*b[10]/C*(tr/2-q[0]+2*p['beta']*q[IDX['Pi']]+qd[IDX['T']]/C)
            checks.add(tag+'_'+str(i)+'_direct_current_vs_affine_constraint',max(abs(directQ-vals['Q']['value'])/(1+abs(directQ)),abs(directP-vals['P']['value'])/(1+abs(directP)))<=1e-7)
            checkE=abs(vals['E']['value']-q[IDX['Em']])/(1+abs(q[IDX['Em']]))
            driftE=abs(vals['E']['derivative']-qd[IDX['Em']])/(1+abs(qd[IDX['Em']]))
            checks.add(tag+'_'+str(i)+'_independent_constraint_density_value',checkE<=1e-7,float(checkE))
            checks.add(tag+'_'+str(i)+'_INDEPENDENT_constraint_density_drift_vs_assigned_Euler',driftE<=1e-7,float(driftE))
            if i in (0,10,20):
                archived=next(v for v in run['events'] if abs(v['time']-t)<1e-15)
                profile=(unpack(archived['full_response']['mean']['response']),unpack(archived['full_response']['second']['response']),
                         unpack(archived['full_response']['mean']['velocity']),unpack(archived['full_response']['second']['velocity']))
                controls={}
                for label in (0,1):
                    errors=[]
                    for amp in ('0.000001','0.0000005','0.00000025'):
                        aa=mp.mpf(amp);zero=sum(finite_current(profile,0,ang,p,b)[label] for ang in (0,np.pi/2))/2
                        central=sum((finite_current(profile,amp,ang,p,b)[label]+finite_current(profile,'-'+amp,ang,p,b)[label])/2 for ang in (0,np.pi/2))/2
                        coefficient=(central-zero)/(aa*aa);target=vals[('Q','P')[label]]['value']
                        errors.append(float(abs(coefficient-target)/(1+abs(target))))
                    checks.add(tag+'_'+str(i)+'_unexpanded_current_coefficient_'+str(label),errors[-1]<=1e-7,errors,'finite analytic-profile remainder, not exact nonlinear charge')
                    controls[('Q','P')[label]]=errors
            else:controls=None
            rows.append(dict(time=t,charges=vals,independent_Em_value_error=float(checkE),independent_Em_drift_error=float(driftE),finite_controls=controls))
        q0=rows[0]['charges']['Q']['value'];p0=rows[0]['charges']['P']['value']
        checks.add(tag+'_exact_recipe_initial_Q2',abs(q0+eta**3/26)/eta**3<=1e-12,float((q0+eta**3/26)/eta**3))
        for label in ('Q','P'):
            start=rows[0]['charges'][label]['value']
            err=max(abs(row['charges'][label]['value']-start)/(row['charges'][label]['scale']+rows[0]['charges'][label]['scale']) for row in rows)
            checks.add(tag+'_'+label+'_conservation_cancellation_scaled',err<=1e-7,float(err))
        records.append(dict(family=name,eta_exact=run['eta_exact'],method=run['method'],nodes=rows,
            initial_Q2=q0,initial_P2=p0,Q2_per_xi_squared=q0/(eta/6),P2_per_xi_squared=p0/(eta/6),
            Q2_absolute_drift=max(abs(q['charges']['Q']['value']-q0) for q in rows),
            Q2_eta_cubed_relative_drift=max(abs(q['charges']['Q']['value']-q0)/eta**3 for q in rows),
            root_background_independent_numeric_comparison='UNAVAILABLE_NO_EXPORTED_ROOT_BACKGROUND; generic all-time identity covers its domain'))
        progress(stage='CHARGE_RECORD_COMPLETE',family=name,eta=eta,method=run['method'],initial_Q2=q0,initial_P2=p0)
    for family in FAMILIES:
        for eta in ('1/4','1/64','1/1024'):
            pair=[r for r in records if r['family']==family and r['eta_exact']==eta]
            check=max(abs(pair[0][k]-pair[1][k])/(1+abs(pair[0][k])+abs(pair[1][k])) for k in ('initial_Q2','initial_P2'))
            checks.add(family+'_'+eta+'_two_method_prepared_charge_agreement',check<=1e-7,float(check))
    return records


def calculate(compiler_only=False):
    common,ret,prior,time,entry,generic,pins,absent,snapshot=collect();before=snapshot();checks=Checks()
    currents=variational_currents(checks);compiler=Compiler(generic,checks)
    if compiler_only:
        summary=dict(action='COMPILER_ONLY_CONTROL',passed=sum(c['passed'] for c in checks.rows),total=len(checks.rows),failed=[c for c in checks.rows if not c['passed']],physics_pass=False,goal_complete=False)
        print(json.dumps(summary));return None,summary
    records=numerical(compiler,ret,prior,time,entry,generic,checks) if all(c['passed'] for c in checks.rows) else []
    checks.add('all_source_and_sidecar_metadata_unchanged',snapshot()==before)
    checks.add('all_source_pins_and_known_absences_after',common.inspect_pins(pins)==absent)
    scope=dict(classification='CONDITIONAL_HOMOGENEOUS_CHARGE_AND_DENSITY_DRIFT_CONTINUATION',
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        Stage2='INCOMPLETE_STOP_AND_ASSESS_DOMAIN_UNRESOLVED',Stage3='NOT_ENTERED_IDENTIFYING_MATCHING_MISSING',
        physical_frequency_window=False,physical_propagating_ghost_identified=False,physical_GR_recovery=False,
        ensemble_changed=False,old_ODE_integrations=0,finite_numerical_error_certified=False,full_nonlinear_remainder_certified=False,
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        root_numeric_background='UNEXPORTED_NOT_INTERPOLATED; exact generic identities retain root in domain',
        review_register_id='R9-MT1-THREE-FAMILY-CHARGE-DOMAIN-V3')
    passed=sum(c['passed'] for c in checks.rows);ok=passed==len(checks.rows)
    bodies={'formulas.json':encode(currents),'canonical.json':encode(compiler.export),'charge_records.json':encode(dict(runs=records)),
            'scope.json':encode(scope),'verification.json':encode(dict(passed=passed,total=len(checks.rows),checks=checks.rows,**scope))}
    summary=dict(schema='r4c1-three-family-charge-domain-v3',passed=passed,total=len(checks.rows),checks=checks.rows,
        validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',status='CHARGE_AND_DENSITY_DRIFT_CHECKED_PHYSICAL_WINDOW_OPEN' if ok else 'CHARGE_DOMAIN_REQUIRES_DISPOSITION',
        source_sha256=dict(sorted(pins.items())),script_sha256=pins[SELF],inherited_sidecars_absent=absent,source_metadata_preserved=len(before),
        artifacts={n:sha(v) for n,v in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,mpmath=mp.__version__),**scope)
    bodies['summary.json']=encode(summary);return bodies,summary


def main():
    global PROGRESS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_three_family_charge_domain_attempt_03')
    parser.add_argument('--replay');parser.add_argument('--progress');parser.add_argument('--compiler-check-only',action='store_true')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and args.compiler_check_only:raise ValueError('Compiler control is not scientific replay')
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay directory absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if args.progress:
        PROGRESS=(ROOT/args.progress).resolve();PROGRESS.relative_to((ROOT/'.local/itsm-context').resolve())
        with PROGRESS.open('x',encoding='utf-8') as f:f.write(json.dumps(dict(state='STARTED',mode='replay' if args.replay else 'new'))+'\n')
    bodies,summary=calculate(args.compiler_check_only)
    if args.compiler_check_only:return 0 if summary['passed']==summary['total'] else 1
    if args.replay:
        for n,v in bodies.items():
            if (dest/n).read_bytes()!=v or (dest/(n+'.sha256')).read_text(encoding='utf-8')!=sha(v)+'  '+n+'\n':
                raise RuntimeError('Replay differs '+n)
        action='READ_ONLY_REPLAY_EXACT'
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for n,v in bodies.items():
            with (dest/n).open('xb') as f:f.write(v)
            with (dest/(n+'.sha256')).open('xb') as f:f.write((sha(v)+'  '+n+'\n').encode())
        action='NEW_RECEIPTS_WRITTEN'
    progress(stage=action,passed=summary['passed'],total=summary['total'],validation=summary['validation'],physics_pass=False)
    for c in summary['checks']:
        if not c['passed']:print(json.dumps(c))
    return 0 if summary['passed']==summary['total'] else 1


if __name__=='__main__':raise SystemExit(main())
