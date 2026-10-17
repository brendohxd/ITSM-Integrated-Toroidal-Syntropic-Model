"""Generic-action homogeneous kinetic comparison of two global charge ensembles.

No propagating-stability, conserved-energy, cutoff or GR acceptance claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
PARENT = BASE + 'r4c1_fixed_charge_retarded_comparison_attempt_03/'
KERNEL = BASE + 'r4c1_g3n5_attempt_02/kernel.json'
PLANAR = BASE + 'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V1_CONTRACT_2026-10-15.md'
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V1_NUMERICAL_ADDENDUM_2026-10-16.md'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
PINS = {
    CONTRACT: 'f071f31d7890e2b9e47650f30f9e216fbabf196a4f387a54bce078e8a3cc8d77',
    ADDENDUM: '51f64f1d43b821c8d4e49e1fb2026201f19b68857c0949349cd86c051702461f',
    KERNEL: 'cf30a7e334d154e492f8ca7bde92cf95754390b602f4914e5b6ba8fed90a74e3',
    PLANAR: '852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a',
    PARENT+'summary.json': '604109a460da50203d413676c0c728f656be373184f710a871066b46f52df6be',
    'Theory/Gates/RES-001/RES001_R4C1_G3N5_MEAN_MODE_ENERGY_REPORT_2026-10-11.md':
        '331b596dada0073ee1d50da69d3a8bbb8475c0b9cd7b8b246c5d03c7d536339f',
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_CHARGE_DOMAIN_V5_REPORT_2026-10-13.md':
        '582fab6ecdcee40b2aacd09c2388128d18d35f6c90d5c90e6dfd447c793ab1c9',
    'Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_RETARDED_V3_REPORT_2026-10-13.md':
        '002011c7c9092bca3de1f16797adab3cbbf4932665544ea6cfcad969dad24225',
}
PINS.update({
    'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V2_BINDING_ADDENDUM_2026-10-16.md':
        'bd25b346c74ebe44ce37adca4ecd4bd9a5148262eaf76f117fc616f89a489cad',
    'Analysis/MasterTests/test_01_r4c1_three_family_fixed_charge_kinetic_v1.py':
        '9d7c58ac068aec7f3546c2e9a45ed91feabfd05baf6663e3953c93ca3ec7cbbb',
    BASE+'r4c1_three_family_fixed_charge_kinetic_attempt_01/interrupted.json':
        '17a2632eed8823f68506c22310f4ace85687a4b41bdc0c0a0abea756c3052cb6',
    BASE+'r4c1_three_family_fixed_charge_kinetic_attempt_02/interrupted.json':
        'a401bda6e557d46f2c2402c6bcde8ea4c38794d89b1b6b8b5d1864516d85a6cd',
})
FIELDS = ('alpha','Sx','Sy','Sz','Mxx','Mxy','Mxz','Myy','Myz','Mzz',
          'Vx','Vy','Vz','du','dv','dr','Pi','T','Em','Z','nu','LambdaU')
IX = {n:i for i,n in enumerate(FIELDS)}
NAMES = FIELDS[4:16] + ('T',)
FAMILIES = ('archived_G3','new_B1_frame','new_hierarchical')
SHA = lambda b: hashlib.sha256(b).hexdigest()
READ = lambda p: json.loads((ROOT/p).read_bytes())
ENCODE = lambda obj: (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean = lambda e: s.factor(s.cancel(s.expand(e)))


def progress(stage):
    print(json.dumps(dict(stage=stage)),flush=True)


class Checks:
    def __init__(self): self.rows=[]; self.names=set()
    def add(self,name,ok,value=None,criterion='exact'):
        if name in self.names: raise ValueError('Duplicate check '+name)
        self.names.add(name)
        self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def exact(self,name,e,reduce=clean):
        values=list(e) if isinstance(e,(s.MatrixBase,list,tuple)) else [e]
        bad=[dict(index=i,residual=str(r)) for i,v in enumerate(values) if (r:=reduce(v))!=0]
        self.add(name,not bad,bad,'zero_exact')
    def small(self,name,value,tolerance):
        self.add(name,abs(value)<=mp.mpf(tolerance),float(value),'<= '+str(tolerance))


def inputs():
    parent=READ(PARENT+'summary.json')
    pins=dict(parent['source_sha256'])
    pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins.update(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes())
    absent=parent['inherited_sidecars_absent']
    for name,digest in pins.items():
        if SHA((ROOT/name).read_bytes())!=digest: raise RuntimeError('Frozen source drift: '+name)
    paths=[]
    for name,digest in pins.items():
        p=ROOT/name;paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text(encoding='utf-8').split()[0].lower()!=digest:
                raise RuntimeError('Frozen sidecar differs: '+name)
            paths.append(side)
        elif name not in absent: raise RuntimeError('Required sidecar absent: '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in paths]
    return pins,absent,snapshot


class Compiler:
    def __init__(self,ch):
        progress('GENERIC_22_FIELD_ACTION')
        data=READ(KERNEL);planar=READ(PLANAR)
        names=set('a H Hdot u0 u_dot v0 v_dot r0 r_dot psi_dot rho C eta'.split())
        names.update('MP2 MU2 c1 c2 c3 c4 K_Q b beta zeta m2 lambda4 lambda6 Lambda mr2 lambda_r g_r rho_Lambda epsilon0 lambda0'.split())
        for family in FAMILIES: names.update(planar['families'][family]['parameter_map'])
        for rec in data['entries']: names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',rec['value']))
        x={n:s.Symbol(n,real=True) for n in names if n not in ('sqrt','Abs','sign')}
        a,H,u,ud,v,vd,r,rd,pd,rho,C=[x[n] for n in ('a','H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho','C')]
        MP,MU,c1,c2,c3,c4,K,b,beta,zeta=[x[n] for n in ('MP2','MU2','c1','c2','c3','c4','K_Q','b','beta','zeta')]
        MC=MP+MU*(c1+3*c2+c3)/2;MT=MP-MU*(c1+c3);f2=MU*(c1+c4)
        vol=a**3;radius2=u*u+v*v;radius=s.sqrt(radius2);j=u*vd-v*ud
        pot=x['m2']*radius2/2+x['lambda4']*radius2**2/8+x['lambda6']*radius2**3/(24*x['Lambda']**2)
        pot+=x['mr2']*r*r/2+x['lambda_r']*r**4/4+x['g_r']*radius2*r*r/4+x['rho_Lambda']
        kin=ud*ud+vd*vd+rd*rd+K*pd*pd;Hd=-(kin+rho)/(2*MC)
        mass=x['m2']+x['lambda4']*radius2/2+x['lambda6']*radius2**2/(4*x['Lambda']**2)+x['g_r']*r*r/2
        rate={a:a*H,H:Hd,u:ud,ud:-3*H*ud-mass*u,v:vd,vd:-3*H*vd-mass*v,
              r:rd,rd:-3*H*rd-x['mr2']*r-x['lambda_r']*r**3-x['g_r']*radius2*r/2,
              pd:-3*H*pd-beta*rho/K,rho:(-3*H+beta*pd)*rho,C:beta*pd*C}
        def dt(e): return s.expand(sum(s.diff(e,z)*q for z,q in rate.items() if z in e.free_symbols))
        R0=s.Symbol('radius',positive=True);Rd=s.Symbol('radial_rate',real=True);Q=s.Symbol('Q',real=True)
        section={u:R0,v:s.Integer(0),ud:Rd,vd:Q/(vol*R0)}
        constraint=(3*MC*H*H-kin/2-pot-rho).subs(section,simultaneous=True)
        modulus=s.Poly(constraint,H,domain='EX')
        def project(e): return clean(e.subs(section,simultaneous=True))
        def shell(e):
            e=project(e)
            if e==0:return s.Integer(0)
            num,den=s.fraction(s.together(e))
            return clean(s.Poly(num,H,domain='EX').rem(modulus).as_expr()/den)
        background={x['epsilon0']:rho/C**4,x['lambda0']:3*MU*c2*Hd-3*MU*(c1+c3)*H**2,x['Hdot']:Hd}
        AA,LB,RR,KK=[s.zeros(22) for _ in range(4)]
        blocks={(0,0):AA,(0,1):LB,(1,0):RR,(1,1):KK}
        for rec in data['entries']:
            bi,i=divmod(rec['row'],22);bj,k=divmod(rec['column'],22)
            if (bi,bj) in blocks:blocks[bi,bj][i,k]=s.sympify(rec['value'],locals=x).subs(background)
        ch.exact('generic_value_block_symmetric',AA-AA.T)
        ch.exact('generic_velocity_block_symmetric',KK-KK.T)
        ch.exact('generic_mixed_blocks_transpose',LB-RR.T)
        ch.add('complete_field_order',tuple(planar['field_order'])==FIELDS)
        F=s.zeros(22,13);G=s.zeros(22,13)
        for i,n in enumerate(NAMES):F[IX[n],i]=1
        G[IX['alpha'],NAMES.index('T')]=1/C
        for n in ('alpha','Em','Z','LambdaU'):
            ch.exact(n+'_primary_has_no_velocity',KK.row(IX[n]))
        ch.exact('lapse_has_no_time_derivative_in_mixed_action',RR.row(IX['alpha']))
        ch.exact('density_constraint_value_after_clock',AA.row(IX['Em'])*F)
        ch.exact('density_constraint_velocity_after_clock',AA.row(IX['Em'])*G+LB.row(IX['Em'])*F)
        unit=s.zeros(1,22);unit[0,IX['nu']]=-1
        ch.exact('unit_constraint_is_nu_zero',AA.row(IX['LambdaU'])-unit)
        reg=s.zeros(1,22);reg[0,IX['Z']]=b
        ch.exact('zero_mode_regulator_equation_bZ',AA.row(IX['Z'])-reg)
        ch.exact('zero_mode_regulator_has_no_mixed_source',LB.row(IX['Z']))
        for n in ('Sx','Sy','Sz'):
            i=IX[n]
            ch.exact(n+'_homogeneous_primary',KK.row(i))
            ch.exact(n+'_homogeneous_value_gauge_row',AA.row(i)*F)
            ch.exact(n+'_homogeneous_velocity_gauge_row',AA.row(i)*G+LB.row(i)*F)
        normal=s.zeros(22,2)
        for n in ('Mxx','Myy','Mzz'):normal[IX[n],0]=s.Rational(2,3)
        normal[IX['nu'],1]=1
        normalK=s.Matrix([[-2*MC/3,-MU*c2],[-MU*c2,-MU*(c1+c2+c3+c4)]])
        ch.exact('full_normal_velocity_block',normal.T*KK*normal-normalK)
        detnormal=clean(normalK.det());hnu=clean(normalK.inv()[1,1]/vol)
        ch.exact('normal_inverse_domain',hnu+2*MC/(3*vol*detnormal))
        ch.exact('density_velocity_coefficient',KK[IX['T'],IX['T']]-rho/C**2)
        ch.exact('density_mixed_coefficient',RR[IX['T'],IX['Em']]-C**3)
        hEm=clean(vol*RR[IX['T'],IX['Em']]**2/KK[IX['T'],IX['T']])
        ch.exact('density_chain_nonzero_factor',hEm-vol*C**8/rho)
        A=F.T*AA*F;R=G.T*AA*F+F.T*RR*F
        Kp=F.T*KK*F+G.T*AA*G+F.T*RR*G+G.T*RR.T*F
        progress('EVOLVING_POLAR_MAP_AND_BOUNDARY')
        D=s.eye(13);i=NAMES.index('du');ang=NAMES.index('dv')
        D[i,i]=u/radius;D[i,ang]=-v;D[ang,i]=v/radius;D[ang,ang]=u
        dD=D.applyfunc(dt)
        Ap=D.T*A*D+D.T*R.T*dD+dD.T*R*D+dD.T*Kp*dD
        Rp=D.T*R*D+D.T*Kp*dD;Kp=D.T*Kp*D
        boundary=s.zeros(13)
        boundary[i,ang]=boundary[ang,i]=vol*j/radius
        boundary[ang,ang]=-vol*(u*ud+v*vd)
        Ap+=boundary.applyfunc(dt)/vol;Rp+=boundary/vol
        ch.exact('polar_angle_cyclic_value',Ap.row(ang),shell)
        ch.exact('polar_angle_cyclic_mixed',Rp[:,ang],shell)
        ch.exact('angular_kinetic_radius_squared',Kp[ang,ang]-radius2,project)
        ch.add('reject_omitted_polar_drift',any(q!=0 for q in dD))
        ch.add('reject_omitted_nonlinear_boundary',any(q!=0 for q in boundary))
        keep=[k for k in range(13) if k!=ang]
        row=Rp.extract([ang],keep);col=Kp.extract(keep,[ang]);ka=Kp[ang,ang]
        Au=Ap.extract(keep,keep)-row.T*row/ka
        Ru=Rp.extract(keep,keep)-col*row/ka
        Ku=Kp.extract(keep,keep)-col*Kp.extract([ang],keep)/ka
        remaining=[NAMES[k] for k in keep]
        P=s.zeros(12)
        for n in ('Mxx','Myy','Mzz'):P[remaining.index(n),0]=s.Rational(2,3)
        P[remaining.index('du'),1]=1;P[remaining.index('dr'),2]=1
        P[remaining.index('Mxx'),3]=1/s.sqrt(2);P[remaining.index('Myy'),3]=-1/s.sqrt(2)
        P[remaining.index('Mxx'),4]=P[remaining.index('Myy'),4]=1/s.sqrt(6)
        P[remaining.index('Mzz'),4]=-2/s.sqrt(6)
        for k,n in enumerate(('Mxy','Mxz','Myz'),5):P[remaining.index(n),k]=1/s.sqrt(2)
        for k,n in enumerate(('Vx','Vy','Vz'),8):P[remaining.index(n),k]=1
        P[remaining.index('T'),11]=1
        Au=(P.T*Au*P).applyfunc(project);Ru=(P.T*Ru*P).applyfunc(project);Ku=(P.T*Ku*P).applyfunc(project)
        ch.exact('dust_origin_cyclic_value',Au.row(11),shell)
        ch.exact('dust_origin_cyclic_mixed',Ru[:,11],shell)
        U=project(pot)+rho+Q**2/(2*vol**2*R0**2)
        W=3*MC*H*H-(Rd*Rd+rd*rd+K*pd*pd)/2
        diag=s.diag(-2*MC/3,1,1,*([MT/4]*5),*([f2]*3))
        bv=s.Matrix([2*MC*H,-Rd,-rd]+[0]*8)
        expected=s.BlockMatrix([[diag,bv/C],[bv.T/C,s.Matrix([[-2*W/C**2]])]]).as_explicit()
        ch.exact('generic_action_variable_dust_K_raw',Ku-expected)
        ch.exact('dust_cyclic_coefficient_on_shell',Ku[11,11]+2*U/C**2,shell)
        Kfixed=(Ku[:11,:11]-Ku[:11,11:12]*Ku[11:12,:11]/Ku[11,11]).applyfunc(clean)
        ch.exact('generic_action_fixed_both_K_raw',Kfixed-diag-bv*bv.T/(2*W))
        ch.exact('generic_action_fixed_both_K_on_shell',Kfixed-diag-bv*bv.T/(2*U),shell)
        triangle=s.eye(12)
        for k in range(11):triangle[11,k]=-Ku[11,k]/Ku[11,11]
        ch.exact('different_ensemble_exact_Schur_congruence',triangle.T*Ku*triangle-s.diag(Kfixed,Ku[11,11]))
        ch.exact('reject_omitted_dust_reduction_has_nonzero_trace_correction',
                 (Kfixed-diag)[0,0]-2*MC**2*H**2/W)
        ch.add('trace_correction_not_identically_zero',(Kfixed-diag)[0,0]!=0)
        ch.exact('archived_B1_normalized_trace_control',(-MC/2).subs({MP:1,MU:s.Rational(2,3),c1:s.Rational(1,5),c2:s.Rational(1,10),c3:-s.Rational(1,5),c4:s.Rational(1,20)})+s.Rational(11,20))
        uu,vv,pp,qq=s.symbols('u v pu pv',real=True);rr=s.sqrt(uu*uu+vv*vv)
        pR=(uu*pp+vv*qq)/rr;charge=uu*qq-vv*pp
        ch.exact('polar_canonical_one_form',[pR*uu/rr-charge*vv/rr**2-pp,pR*vv/rr+charge*uu/rr**2-qq])
        nv,rv,N,boost,zd,charge0=s.symbols('volume radius lapse boost2 theta_dot charge',positive=True)
        zt=s.Symbol('zeta',real=True);ac=nv*rv**2*(1-zt*rv**2*boost)/N
        angularL=ac*zd**2/2;routh=clean((angularL-charge0*zd).subs(zd,charge0/ac))
        ch.exact('full_alignment_dependent_Routh',routh+N*charge0**2/(2*nv*rv**2*(1-zt*rv**2*boost)))
        ch.exact('alignment_boost_curvature_retained',s.diff(routh,boost).subs(boost,0)+N*zt*charge0**2/(2*nv))
        ch.add('reject_wrong_Routh_sign',routh!=-routh)
        ch.add('reject_omitted_angular_alignment',s.diff(routh,zt)!=0)
        eta=x['eta'];t=s.Symbol('positive_interval_parameter',positive=True)
        families={}
        for family in FAMILIES:
            pars={x[n]:s.sympify(value,locals=x) for n,value in planar['families'][family]['parameter_map'].items()}
            values={n:clean(q.subs(pars)) for n,q in dict(MC=MC,MT=MT,f2=f2,K=K,normal_determinant=detnormal).items()}
            for n,q in values.items():
                num,den=s.fraction(s.factor(q.subs(eta,t/(1+4*t))))
                good=all(c>=0 for c in s.Poly(num,t).all_coeffs()+s.Poly(den,t).all_coeffs()) and num!=0 and den!=0
                ch.add(family+'_'+n+'_positive_interval',good and q.subs(eta,s.Rational(1,4))>0,str(q),'0<eta<=1/4, positive transformed polynomial coefficients')
            families[family]={k:str(v) for k,v in values.items()}
        ch.exact('eta_zero_frame_and_force_kinetics_degenerate',[f2.subs({x[n]:s.sympify(v,locals=x) for n,v in planar['families'][FAMILIES[0]]['parameter_map'].items()}).subs(eta,0),3*eta.subs(eta,0)])
        self.export=dict(field_order=FIELDS,coordinate_order=['x','R','r']+['shear'+str(i) for i in range(5)]+['frame'+str(i) for i in range(3)]+['T'],
            normal_block=[[str(q) for q in row] for row in normalK.tolist()],hnu=str(hnu),hEm=str(hEm),
            U=str(U),W=str(W),constraint=str(constraint),families=families,
            K_variable_raw=[[str(q) for q in row] for row in Ku.tolist()],
            K_fixed_raw=[[str(q) for q in row] for row in Kfixed.tolist()],
            derivative_order='Cartesian background derivatives before instantaneous polar section',
            angular_Routh=str(routh),ensemble_pairs=dict(fixed_U1=12,fixed_U1_and_dust=11))


def independent(ch):
    progress('INDEPENDENT_HOMOGENEOUS_LEGENDRE_AND_SIGN_PROOF')
    M,Tm,f2,K,v,U,pd,C,PT,N,eps=s.symbols('M Tm f2 K volume U pd C PT N epsilon',positive=True)
    H,Rd,rd=s.symbols('H Rdot rdot',real=True)
    G=s.diag(-2*M/3,1,1,*([Tm/4]*5),*([f2]*3));bv=s.Matrix([2*M*H,-Rd,-rd]+[0]*8)
    fixed=G+bv*bv.T/(2*U)
    hsq=(Rd**2+rd**2+K*pd**2+2*U)/(6*M)
    shell=lambda e:clean(s.expand(e).subs(H**2,hsq))
    minors=[M*(Rd**2+rd**2+K*pd**2)/(3*U),M*(rd**2+K*pd**2)/(3*U),M*K*pd**2/(3*U)]
    for i,expected in enumerate(minors,1):ch.exact('Sylvester_minor_'+str(i),fixed[:i,:i].det()-expected,shell)
    ch.add('strict_minors_from_declared_domain',all(q.is_positive for q in minors),[str(q) for q in minors])
    ch.exact('zero_clock_loses_strict_third_minor',minors[-1].subs(pd,0))
    velocities=s.Matrix(s.symbols('dx dR dr ds0:5 db0:3',real=True))
    momenta=s.Matrix(s.symbols('px pR pr ps0:5 pb0:3',real=True))
    L=(v*(velocities.T*G*velocities)[0])/(2*N)
    pderived=s.Matrix([s.diff(L,q) for q in velocities]);vdot=N*G.inv()*momenta/v
    Hderived=clean((momenta.dot(velocities)-L).subs(dict(zip(velocities,vdot)),simultaneous=True)/N)
    B=-G.inv()/(2*v)
    ch.exact('unfixed_lapse_full_11_velocity_Legendre',Hderived+(momenta.T*B*momenta)[0])
    td=s.Symbol('tau_dot',real=True);LD=v*eps*(C**2*td**2/N-N*C**4)/2
    charge=s.diff(LD,td);tdsol=PT*N/(v*eps*C**2)
    HD=clean((PT*td-LD).subs(td,tdsol)/N)
    ch.exact('dust_positive_density_branch',HD.subs(eps,PT/(v*C**3))-C*PT)
    psiD,psiP=s.symbols('psi_dot psi_p',real=True)
    ch.exact('force_scalar_unfixed_lapse_Legendre',
        (psiP*psiD-v*K*psiD**2/(2*N)).subs(psiD,N*psiP/(v*K))/N-psiP**2/(2*v*K))
    F=(momenta.T*B*momenta)[0]-v*U
    HP=-pd*s.sqrt(2*K*v*F)
    fstar=s.Symbol('positive_F',positive=True)
    hess=s.hessian(HP,list(momenta)).subs(F,fstar)
    bg={momenta[0]:-2*M*v*H,momenta[1]:v*Rd,momenta[2]:v*rd}
    bg.update({p:0 for p in momenta[3:]})
    ch.exact('positive_clock_radicand_on_shell',F.subs(bg)-v*K*pd**2/2,shell)
    hess=hess.subs(bg).subs(fstar,v*K*pd**2/2).applyfunc(s.simplify)
    expected=-2*B+4*(B*momenta).subs(bg)*(B*momenta).subs(bg).T/(K*v*pd**2)
    ch.exact('independently_differentiated_11_momentum_Hessian',hess-expected)
    ch.exact('Hamiltonian_Hessian_is_inverse_kinetic_over_volume',v*fixed*hess-s.eye(11),shell)
    MP=s.Symbol('M_P_squared',positive=True);px=s.Symbol('px',real=True)
    ch.exact('Einstein_dust_negative_homogeneous_volume_control',s.diff(-3*px**2/(4*MP*v),px,2)+3/(2*MP*v))
    B3=B[:3,:3];p3=momenta[:3,0]
    rest=s.Symbol('potential_and_angular_energy_density',real=True)
    F3=(p3.T*B3*p3)[0]-v*rest
    pT=s.Symbol('varying_Ptau',real=True)
    hvar=-pd*s.sqrt(2*K*v*(F3-C*pT))
    ca,cb=s.symbols('compact_A compact_B',positive=True)
    cd=s.Symbol('compact_D',real=True)
    compact_rad=ca*px**2-cb*pT+cd
    compact_h=-pd*s.sqrt(compact_rad)
    mixed=s.hessian(compact_h,(px,pT))
    det_explicit=mixed[0,0]*mixed[1,1]-mixed[0,1]*mixed[1,0]
    det_compact=-pd**2*ca*cb**2/(4*compact_rad**2)
    ch.exact('compact_mixed_Hessian_determinant_identity',det_explicit-det_compact)
    binding={ca:3*K/(2*M),cb:2*K*v*C,cd:-K*(momenta[1]**2+momenta[2]**2)-2*K*v**2*rest}
    ch.exact('compact_radical_binds_full_spectator_energy',compact_rad.subs(binding)-2*K*v*(F3-C*pT))
    fs=s.Symbol('positive_physical_F',positive=True)
    physical_det=det_compact.subs(compact_rad,s.Symbol('Z',positive=True)).subs({ca:3*K/(2*M),cb:2*K*v*C,s.Symbol('Z',positive=True):2*K*v*fs})
    ch.exact('variable_dust_mixed_hessian_remains_negative',physical_det+3*pd**2*C**2*K/(8*M*fs**2))
    return dict(principal_minors=list(map(str,minors)),independent_Hamiltonian=str(HP),
                independent_hessian=[[str(q) for q in row] for row in expected.tolist()],
                Einstein_dust_control='-3/(2*M_P_squared*volume)',
                sign_domain='M,Tm,f2,K,U,volume,C>0; pd>0; regular constraint blocks',
                conserved_perturbation_energy_claim=False)


def norm(m): return max(sum(abs(m[i,j]) for j in range(m.cols)) for i in range(m.rows))
def scalar(x): return mp.mpf(repr(x)) if isinstance(x,float) else mp.mpf(x)
def textnum(x): return mp.nstr(x,35)


def numeric(ch):
    progress('ARCHIVED_RAW_BACKGROUNDS_80_DIGIT_CONTROLS')
    mp.mp.dps=80;planar=READ(PLANAR);runs=READ(PARENT+'trajectories.json')['runs'];records=[]
    ch.add('all_registered_runs',len(runs)==18)
    def params(family,eta):
        e=s.Symbol('eta');return {n:mp.mpf(str(s.N(s.sympify(q,locals={'eta':e}).subs(e,s.Rational(eta)),85))) for n,q in planar['families'][family]['parameter_map'].items()}
    def matrices(M,Tm,f2,K,H,Rd,rd,U,C):
        G=mp.diag([-2*M/3,1,1]+[Tm/4]*5+[f2]*3);b=mp.matrix([2*M*H,-Rd,-rd]+[0]*8)
        fixed=G+b*b.T/(2*U);var=mp.matrix(12)
        for i in range(11):
            for j in range(11):var[i,j]=G[i,j]
            var[i,11]=var[11,i]=b[i]/C
        var[11,11]=-2*U/C**2
        return fixed,var,b
    def eigen(m,size):return list(mp.eigsy(m[:size,:size],eigvals_only=True))
    for run in runs:
        family=run['family'];eta=run['eta_exact'];p=params(family,eta);e=mp.mpf(str(s.Rational(eta).evalf(85)))
        M=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
        Tm=p['MP2']-p['MU2']*(p['c1']+p['c3']);f2=p['MU2']*(p['c1']+p['c4']);K=p['K_Q']
        rows=[];tag=family+'_'+eta+'_'+run['method']
        ch.add(tag+'_frozen_grid',len(run['times'])==len(run['first_order_states'])==21 and run['times'][0]==0 and run['times'][-1]==0.05 and run['k']==40)
        for i,raw in enumerate(run['first_order_states']):
            a,H,u,ud,v,vd,r,rd,psi,pd,rho=map(scalar,raw[:11]);vol=a**3;R2=u*u+v*v;Rd=(u*ud+v*vd)/mp.sqrt(R2)
            C=mp.exp(p['beta']*psi);j=u*vd-v*ud
            pot=R2/2+R2**2/24+R2**3/480+r*r+r**4/28+3*e*R2*r*r/28
            U=pot+rho+j*j/(2*R2);W=3*M*H*H-(Rd*Rd+rd*rd+K*pd*pd)/2;delta=W-U
            fixed,var,b=matrices(M,Tm,f2,K,H,Rd,rd,U,C)
            rawfixed,rawvar,_=matrices(M,Tm,f2,K,H,Rd,rd,W,C)
            correction=-delta*b*b.T/(2*U*W)
            identity=norm(rawfixed-fixed-correction)/max(1,norm(rawfixed),norm(fixed))
            ch.small(tag+'_'+str(i)+'_constraint_residual_correction_identity',identity,'1e-50')
            scaled=abs(delta)/(1+abs(U)+abs(W));ch.small(tag+'_'+str(i)+'_background_constraint',scaled,'1e-7')
            values=eigen(rawfixed,3)+[Tm/4]*5+[f2]*3
            # Active varying-charge coordinates are x,R,r,T, followed by the eight positive modes.
            active=mp.matrix([[rawvar[a,b] for b in (0,1,2,11)] for a in (0,1,2,11)])
            vv=list(mp.eigsy(active,eigvals_only=True))+[Tm/4]*5+[f2]*3
            eps=mp.mpf('1e-50')*max(1,*map(abs,values+vv))
            positive=sum(q>eps for q in values);inertia=[sum(q>eps for q in vv),sum(q<-eps for q in vv)]
            detnormal=mp.det(mp.matrix([[-2*M/3,-p['MU2']*p['c2']],[-p['MU2']*p['c2'],-p['MU2']*(p['c1']+p['c2']+p['c3']+p['c4'])]]))
            domain=min(a,C,R2,rho,M,Tm,f2,K,pd,U,W,detnormal)>0
            ch.add(tag+'_'+str(i)+'_regular_domain_and_charge_inertias',domain and positive==11 and inertia==[11,1],dict(fixed_positive=positive,variable=inertia))
            rows.append(dict(time=run['times'][i],fixed_eigenvalues=[textnum(q) for q in values],variable_eigenvalues=[textnum(q) for q in vv],
                raw_constraint=textnum(delta),constraint_scaled=textnum(scaled),constraint_relative_clock=textnum(abs(delta)/(K*pd*pd)),
                raw_shell_matrix_difference=textnum(norm(rawfixed-fixed)),raw_shell_bound=textnum(abs(delta)*norm(b*b.T)/(2*abs(U*W))),
                correction_identity_error=textnum(identity),clock_rate=textnum(pd),U=textnum(U),W=textnum(W)))
        records.append(dict(family=family,eta_exact=eta,method=run['method'],nodes=rows))
        progress('ARCHIVED_RUN_CHECKED_'+tag)
    for family in FAMILIES:
        for eta in ('1/4','1/64','1/1024'):
            pair=[q for q in records if q['family']==family and q['eta_exact']==eta];errors=[]
            ch.add(family+'_'+eta+'_both_methods',len(pair)==2 and {q['method'] for q in pair}=={'DOP853','Radau'})
            for left,right in zip(pair[0]['nodes'],pair[1]['nodes']):
                ch.add(family+'_'+eta+'_'+str(left['time'])+'_identical_time_grid',left['time']==right['time'])
                for key in ('fixed_eigenvalues','variable_eigenvalues'):
                    errors.extend(abs(mp.mpf(a)-mp.mpf(b))/(1+abs(mp.mpf(a))+abs(mp.mpf(b))) for a,b in zip(left[key],right[key]))
            ch.small(family+'_'+eta+'_two_method_kinetic_control',max(errors),'1e-7')
    progress('INDEPENDENT_FINITE_HAMILTONIAN_CONTROLS')
    finite=[]
    for family in FAMILIES:
        for eta in ('1/4','1/64','1/1024'):
            p=params(family,eta);e=mp.mpf(str(s.Rational(eta).evalf(85)));M=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
            Tm=p['MP2']-p['MU2']*(p['c1']+p['c3']);f2=p['MU2']*(p['c1']+p['c4']);K=p['K_Q']
            R=mp.sqrt(e);Rd=mp.mpf(0);rd=R/4;pd=e/5;rho=mp.mpf(1)/5
            pot=e/2+e*e/24+e**3/480+e+e*e/28+3*e**3/28
            U=pot+rho+e/2;H=mp.sqrt((Rd*Rd+rd*rd+K*pd*pd+2*U)/(6*M))
            fixed,_,_=matrices(M,Tm,f2,K,H,Rd,rd,U,mp.mpf(1));target=fixed**-1
            B=mp.matrix([3/(4*M),-mp.mpf(1)/2,-mp.mpf(1)/2]+[-2/Tm]*5+[-1/(2*f2)]*3)
            momenta=mp.matrix([-2*M*H,Rd,rd]+[0]*8)
            F=sum(B[i]*momenta[i]**2 for i in range(11))-U
            step=mp.mpf('1e-6')*F/(1+sum(abs(B[i]*momenta[i]) for i in range(11))+max(map(abs,B)))
            radicands=[]
            def energy(vec):
                ff=sum(B[i]*vec[i]**2 for i in range(11))-U;radicands.append(ff)
                if ff<=0: raise ValueError('Finite Hamiltonian probe leaves clock branch')
                return -pd*mp.sqrt(2*K*ff)
            errors=[]
            for h in (step,step/2):
                fd=mp.matrix(11);base=energy(momenta)
                for i in range(11):
                    ei=mp.matrix(11,1);ei[i]=h
                    fd[i,i]=(energy(momenta+ei)-2*base+energy(momenta-ei))/(h*h)
                    for j in range(i):
                        ej=mp.matrix(11,1);ej[j]=h
                        fd[i,j]=fd[j,i]=(energy(momenta+ei+ej)-energy(momenta+ei-ej)-energy(momenta-ei+ej)+energy(momenta-ei-ej))/(4*h*h)
                err=norm(fd-target)/max(1,norm(target));errors.append(err)
                ch.small(family+'_'+eta+'_finite_Hessian_step_'+str(len(errors)),err,'1e-10')
            ch.add(family+'_'+eta+'_finite_clock_probes_positive',min(radicands)>0)
            finite.append(dict(family=family,eta_exact=eta,step=textnum(step),errors=list(map(textnum,errors)),minimum_F=textnum(min(radicands)),
                background='independent exact initial recipe; not an adjusted archived node'))
    return dict(archived_runs=records,archived_nodes=sum(len(q['nodes']) for q in records),finite_controls=finite,decimal_precision=80)


def calculate():
    pins,absent,snapshot=inputs();before=snapshot();ch=Checks()
    compiler=Compiler(ch);proof=independent(ch)
    numerical=numeric(ch) if all(q['passed'] for q in ch.rows) else dict(skipped='Exact compiler or independent identity failure')
    ch.add('all_pinned_sources_and_sidecar_metadata_preserved',snapshot()==before)
    scope=dict(physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
        Stage4A='CLOSED',TOP_X4='UNCHANGED',Stage2='PHYSICAL_WINDOW_AND_HEALTHY_GR_OPEN',Stage3='NOT_ENTERED',
        physical_propagating_stability=False,conserved_perturbation_energy=False,physical_cutoff=False,full_potential_positive=False,
        continuous_finite_error_certificate=False,original_preparation_changed=False,prior_retarded_warning_erased=False,
        review_register_id='R9-MT1-THREE-FAMILY-FIXED-CHARGE-KINETIC-V2')
    passed=sum(q['passed'] for q in ch.rows);ok=passed==len(ch.rows)
    bodies={'formulas.json':ENCODE(dict(generic=compiler.export,independent=proof)),
            'numerics.json':ENCODE(numerical),'scope.json':ENCODE(scope),
            'verification.json':ENCODE(dict(passed=passed,total=len(ch.rows),checks=ch.rows))}
    summary=dict(schema='r4c1-three-family-fixed-charge-kinetic-v2',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',
        status='HOMOGENEOUS_ENSEMBLE_COMPARISON_CHECKED_PHYSICAL_WINDOW_OPEN' if ok else 'REQUIRES_DISPOSITION',
        passed=passed,total=len(ch.rows),checks=ch.rows,source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,
        source_metadata_preserved=len(before),runtime=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__),
        artifacts={n:SHA(v) for n,v in bodies.items()},**scope)
    bodies['summary.json']=ENCODE(summary)
    return bodies,summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default=BASE+'r4c1_three_family_fixed_charge_kinetic_attempt_03');p.add_argument('--replay');args=p.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    if not args.replay and dest.exists():raise FileExistsError('Fresh directory required')
    try:bodies,summary=calculate()
    except Exception as e:
        if not args.replay:
            dest.mkdir(parents=True,exist_ok=False)
            b=ENCODE(dict(status='EXECUTION_EXCEPTION',exception_type=type(e).__name__,message=str(e),script_sha256=SHA((ROOT/SELF).read_bytes()),physics_pass=False))
            (dest/'exception.json').write_bytes(b);(dest/'exception.json.sha256').write_text(SHA(b)+'  exception.json\n',encoding='utf-8',newline='\n')
        raise
    for name,body in bodies.items():
        side=(SHA(body)+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:raise RuntimeError('Replay differs: '+name)
        else:
            if not dest.exists():dest.mkdir(parents=True,exist_ok=False)
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write(side)
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row),flush=True)
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS',validation=summary['validation'],passed=summary['passed'],total=summary['total'],physics_pass=False)),flush=True)
    return 0 if summary['passed']==summary['total'] else 1


if __name__=='__main__':raise SystemExit(main())
