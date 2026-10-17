"""V3: exact compact-coefficient principal proof; full generic finite-k action retained."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import re
import sys

import numpy as np
import scipy
from scipy.linalg import eig
import sympy as s

import test_01_r4c1_cusp3_evolution_v1 as ev

ROOT=ev.ROOT;BASE=ev.BASE;FIELDS=ev.FIELDS;IX=ev.IX
PARENT=BASE+'r4c1_cusp3_evolution_attempt_01/'
KERNEL=BASE+'r4c1_g3n5_attempt_02/kernel.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FINITE_K_V1_CONTRACT_2026-10-16.md'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
FROZEN={
 'Theory/Gates/RES-001/RES001_R4C1_CUSP3_EVOLUTION_V1_REPORT_2026-10-16.md':'af0878a2d20c48d9a99189940952ef8714f68bd0f99dc2ae09ecb056d05cd186',
 'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V3_REPORT_2026-10-16.md':'a5acbb6d2f659f9c2e4719f32f91ef9f8a4c2cc2c9bdd1fff8635d46fc1199c3',
 'Theory/Gates/RES-001/RES001_R4C1_G3N5_NONZERO_CHARACTERISTIC_REPORT_2026-10-11.md':'2bca36361ea542e51ec4b3b0c1ee8b57ebf98003f7c9076d4f625b33a3a47da5',
 'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_principal_v1.py':'09b3ad3fa6045fbbc283f46d479565adf9f2497748793e6102896698281f28eb',
}
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FINITE_K_V2_COMPUTE_ADDENDUM_2026-10-16.md'
FROZEN['Analysis/MasterTests/test_01_r4c1_three_family_finite_k_v1.py']='b8313ded09dbf8c72611ca9e93ef0396c471e9ab8f09f4a4e173ff5456e50c58'
FROZEN[BASE+'r4c1_three_family_finite_k_attempt_01/interrupted_by_runner.json']='0b30c2343299d0362ac0f0b376be08cb86a2b54cfe2165bed1668e5ef458b2b1'
FROZEN[BASE+'r4c1_three_family_finite_k_attempt_02/interrupted_by_runner.json']='136efda763d9e42fd12d25a59abc5edb0c8c21f749cecfe722188eacb3178b40'
COMPACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_FINITE_K_V3_COMPACT_ADDENDUM_2026-10-16.md'
FROZEN['Analysis/MasterTests/test_01_r4c1_three_family_finite_k_v2.py']='ff942ce9d9312cda921fcca44b1b933d64177f0f82f1dfea63009a873e6da1fc'
FROZEN[BASE+'r4c1_three_family_finite_k_attempt_03/interrupted_by_runner.json']='d03296e94ebbd0d75c2a430154871e55062bc6c8c91bab958ff2f4cf5e92aac1'
CLEAN=lambda e:s.factor(s.cancel(e))


class Checks(ev.Checks):
    def exact(self,name,value):
        values=list(value) if isinstance(value,(list,tuple,s.MatrixBase)) else [value]
        bad=[dict(index=i,residual=str(v)) for i,q in enumerate(values) if (v:=CLEAN(q))!=0]
        self.add(name,not bad,bad,'zero_exact_rational')
MAT=lambda m:dict(shape=list(m.shape),entries=[[str(q) for q in m.row(i)] for i in range(m.rows)])
NORM=lambda m:float(np.linalg.norm(m,np.inf))


def inputs():
    parent=ev.READ(PARENT+'summary.json')
    if ev.SHA((ROOT/(PARENT+'summary.json')).read_bytes())!='b9f8e6b17bf3cfaf01fac6ea1f400e645c36a21585c4d56c3b47f8c64c998fad':raise RuntimeError('Parent summary drift')
    pins=dict(parent['source_sha256']);pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins[PARENT+'summary.json']='b9f8e6b17bf3cfaf01fac6ea1f400e645c36a21585c4d56c3b47f8c64c998fad'
    pins.update(FROZEN);pins.update({n:ev.SHA((ROOT/n).read_bytes()) for n in (SELF,CONTRACT,ADDENDUM,COMPACT)})
    paths=[];absent=parent['inherited_sidecars_absent']
    for n,h in pins.items():
        p=ROOT/n
        if ev.SHA(p.read_bytes())!=h:raise RuntimeError('Frozen source drift: '+n)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=h:raise RuntimeError('Sidecar drift: '+n)
            paths.append(side)
        elif n not in absent:raise RuntimeError('Required sidecar absent: '+n)
    def snapshot():return [(p.relative_to(ROOT).as_posix(),ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(set(paths))]
    import test_01_r4c1_gr_family_survey_v2 as generic
    import test_01_r4c1_three_family_response_entry_v2 as prior
    import test_01_r4c1_three_family_time_response_v2 as time
    import test_01_r4c1_g3n5_nonzero_principal_v1 as old_control
    return pins,absent,snapshot,generic,prior,time,old_control


def interval_positive(expr,eta):
    """Exact Bernstein certificate on 0<eta<=1/4, allowing endpoint eta powers."""
    num,den=s.fraction(s.factor(expr));mid=s.Rational(1,8)
    if num.subs(eta,mid)<0 and den.subs(eta,mid)<0:num,den=-num,-den
    records=[];valid=True
    for label,polyexpr in [('numerator',num),('denominator',den)]:
        poly=s.Poly(polyexpr,eta);power=min(m[0] for m,c in poly.terms() if c!=0)
        reduced=s.Poly(s.cancel(polyexpr/eta**power).subs(eta,eta/4),eta);degree=reduced.degree()
        bern=[s.factor(sum(reduced.nth(i)*s.binomial(k,i)/s.binomial(degree,i) for i in range(k+1))) for k in range(degree+1)]
        valid=valid and all(q>0 for q in bern)
        records.append(dict(part=label,eta_power=int(power),bernstein=list(map(str,bern))))
    return bool(valid),records


class Compiler:
    def __init__(self,ch,old):
        print('Derive unspecialized 22-field finite-z action',flush=True)
        data=ev.READ(KERNEL);texts=[r['value'] for r in data['entries']]
        names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',' '.join(texts)))
        names.update('ell p eta A MP2 MU2 c1 c2 c3 c4 K_Q beta b zeta a H psi_dot u0 v0'.split())
        self.x=x={n:s.Symbol(n,positive=True) if n in ('ell','p','a','eta') else s.Symbol(n,real=True) for n in names}
        ell,p=x['ell'],x['p'];I=s.I
        ch.add('generic110_jet_order',data['jet_order']==[n+suffix for suffix in ('','_t','_x','_y','_z') for n in FIELDS])
        LA,LB,LBT,LK=[s.zeros(22) for _ in range(4)];weights=(1,0,0,0,I*ell)
        for r in data['entries']:
            bi,i=divmod(r['row'],22);bj,j=divmod(r['column'],22);val=s.sympify(r['value'],locals=x)
            if bi!=1 and bj!=1:LA[i,j]+=s.conjugate(weights[bi])*val*weights[bj]
            elif bi!=1:LB[i,j]+=s.conjugate(weights[bi])*val
            elif bj!=1:LBT[i,j]+=val*weights[bj]
            else:LK[i,j]+=val
        dyn=('Mxx','Mxy','Myy','Vx','Vy','Vz','du','dv','dr','Pi');aux=('Sx','Sy','Sz','Z')
        F=s.zeros(22,10);U=s.zeros(22,4)
        for j,n in enumerate(dyn):F[IX[n],j]=1
        F[IX['alpha'],9]=-x['beta']
        for j,n in enumerate(aux):U[IX[n],j]=1
        MT=x['MP2']-x['MU2']*(x['c1']+x['c3']);f2=x['MU2']*(x['c1']+x['c4'])
        cL=x['MU2']*(x['c1']+x['c2']+x['c3']);MC=x['MP2']+x['MU2']*(x['c1']+3*x['c2']+x['c3'])/2
        inv=s.diag(2*x['a']**2/(MT*ell**2),2*x['a']**2/(MT*ell**2),-x['a']**2/(cL*ell**2),1/x['b'])
        D=U.T*LA*U;Y=U.T*LA*F;V=U.T*LB*F
        ch.exact('generic_auxiliary_inverse',D*inv-s.eye(4))
        ch.exact('auxiliary_velocity_momenta_absent',U.T*LK)
        ch.exact('auxiliary_mixed_momenta_absent',U.T*LBT)
        clean=lambda m:m.applyfunc(CLEAN)
        self.A=clean(F.T*LA*F-Y.conjugate().T*inv*Y)
        self.R=clean(F.T*LBT*F-V.conjugate().T*inv*Y)
        self.K=clean(F.T*LK*F-V.conjugate().T*inv*V)
        self.F=F;self.U=U;self.inverse=inv;self.dyn=dyn
        # Original coordinates <- h,TT+,TTx,V_long,V_trans1,V_trans2,du,dv,dr,Pi.
        O=s.zeros(10);sq=s.sqrt(2)
        O[0,0]=O[0,1]=O[2,0]=1/sq;O[2,1]=-1/sq;O[1,2]=1
        O[5,3]=O[3,4]=O[4,5]=1
        for j in range(6,10):O[j,j]=1
        ch.exact('residual_SO2_map_orthogonal',O.T*O-s.eye(10))
        phys=lambda m:clean((O.T*m*O).subs(ell,x['a']*p))
        Ap,Rp,Kp=map(phys,(self.A,self.R,self.K))
        Apr=Ap.applyfunc(lambda e:s.expand(e).coeff(p,2)*p**2+s.expand(e).coeff(p,3)*p**3+s.expand(e).coeff(p,4)*p**4)
        Rpr=Rp.applyfunc(lambda e:s.expand(e).coeff(p,1)*p)
        kh=CLEAN(MT*MC/(2*cL))
        ch.exact('generic_nonzero_kinetic_diagonal',Kp-s.diag(kh,MT/4,MT/2,f2,f2,f2,1,1,1,x['K_Q']))
        for name,m in [('A',self.A),('K',self.K)]:ch.exact('full_'+name+'_Hermitian',m-m.conjugate().T)
        groups=((1,),(2,),(4,),(5,),(0,3,6,7,8,9))
        for name,m in [('A',Ap),('R',Rp),('K',Kp)]:
            remainder=m.copy()
            for group in groups:
                for i in group:
                    for j in group:remainder[i,j]=0
            ch.exact('complete_SO2_separation_'+name,remainder)
        print('Independent generic ADM/frame/regulator scalar density',flush=True)
        h,vl,pi,ht,vt,pit,hz,vz,piz,pizz,sz,z=s.symbols('h vl pi ht vt pit hz vz piz pizz sz z',real=True)
        MP=x['MP2'];mu13=x['MU2']*(x['c1']+x['c3']);mu2=x['MU2']*x['c2']
        before=-MP*ht**2/8+MP*ht*sz/sq+MP*hz**2/8-MP*x['beta']*hz*piz/sq
        before+=f2*(vt-x['beta']*piz)**2/2-mu13*ht**2/8-mu2*ht**2/4
        before-=cL*(vz-sz)**2/2+mu2*ht*(vz-sz)/sq
        before+=x['K_Q']*pit**2/2+x['b']*z*z/2+x['b']*z*(pizz+x['psi_dot']*vz)
        szsol=s.solve(s.diff(before,sz),sz)[0];zsol=-(pizz+x['psi_dot']*vz)
        density=s.expand(before.subs({sz:szsol,z:zsol}))
        jets=(h,vl,pi,ht,vt,pit,hz,vz,piz,pizz);Hess=s.hessian(density,jets)
        Q=s.zeros(10,3);T=s.zeros(10,3)
        for j in range(3):Q[j,j]=1;T[j+3,j]=1;Q[j+6,j]=I*p
        Q[9,2]=-p*p
        independent=[clean(Q.conjugate().T*Hess*Q),clean(T.T*Hess*Q),clean(T.T*Hess*T)]
        ids=[0,3,9]
        for name,m,expected in zip(('A','R','K'),(Apr,Rpr,Kp),independent):ch.exact('independent_generic_scalar_'+name,m.extract(ids,ids)-expected)
        cv=s.sympify(ev.READ(ev.PLANAR)['generic_cV2'],locals=x)
        Gm=s.Matrix([[1+x['zeta']*x['v0']**2,-x['zeta']*x['u0']*x['v0'],0],
                     [-x['zeta']*x['u0']*x['v0'],1+x['zeta']*x['u0']**2,0],[0,0,1]])
        others=[1,2,4,5,6,7,8]
        otherA=s.diag(-MP*p*p/4,-MP*p*p/2,-f2*cv*p*p,-f2*cv*p*p,-Gm*p*p)
        ch.exact('independent_tensor_vector_matter_principal',Apr.extract(others,others)-otherA)
        ch.exact('principal_scalar_other_value_separation',Apr.extract(ids,others))
        residue=Rpr.copy()
        for i in ids:
            for j in ids:residue[i,j]=0
        ch.exact('other_principal_mixed_terms_absent',residue)
        omega,c,sig=s.symbols('omega c sigma',real=True)
        # Bind compact coefficients exactly before doing any determinant algebra.
        mh,th,fh,khh,kqh,bh,betah,pdh,vch,zh,uh,vh=s.symbols('mhat that fhat khat kqhat bhat betahat pdhat cvhat zhat uhat vhat',real=True)
        definitions={mh:MP,th:MT,fh:f2,khh:kh,kqh:x['K_Q'],bh:x['b'],betah:x['beta'],pdh:x['psi_dot'],vch:cv,zh:x['zeta'],uh:x['u0'],vh:x['v0']}
        Ac=s.Matrix([[mh*p*p/4,0,-mh*betah*p*p/sq],
                     [0,-bh*pdh*pdh*p*p,-I*bh*pdh*p**3],
                     [-mh*betah*p*p/sq,I*bh*pdh*p**3,fh*betah*betah*p*p-bh*p**4]])
        Rc=s.Matrix([[0,I*mh*p/sq,0],[0,0,-I*fh*betah*p],[0,0,0]])
        Kc=s.diag(khh,fh,kqh)
        for name,actual,abstract in [('A',Apr.extract(ids,ids),Ac),('R',Rpr.extract(ids,ids),Rc),('K',Kp.extract(ids,ids),Kc)]:
            ch.exact('compact_scalar_exact_binding_'+name,actual-abstract.subs(definitions))
        Pc=Kc*omega**2-I*omega*(Rc.conjugate().T-Rc)+Ac
        dc=s.factor(Pc.det())
        sw=s.factor(s.Poly(dc.subs(omega,c*p),p).nth(8))
        sf=s.factor(s.Poly(dc.subs(omega,sig*p*p),p).nth(12))
        ch.add('compact_scalar_wave_degree',s.Poly(dc.subs(omega,c*p),p).degree()==8)
        ch.add('compact_scalar_fast_degree',s.Poly(dc.subs(omega,sig*p*p),p).degree()==12)
        csh=mh*(2*mh-fh)/(4*khh*fh)
        cph=1+zh*(uh*uh+vh*vh)
        gm=s.Matrix([[1+zh*vh*vh,-zh*uh*vh,0],[-zh*uh*vh,1+zh*uh*uh,0],[0,0,1]])
        mdet=s.factor((c*c*s.eye(3)-gm).det())
        ch.exact('compact_matter_characteristic',mdet-(c*c-1)**2*(c*c-cph))
        detkc=khh*th*th*fh**3*kqh/8
        wc=sw*(th*(c*c-mh/th)/4)*(th*(c*c-mh/th)/2)*fh**2*(c*c-vch)**2*mdet
        fc=sf*th**2*fh**2*sig**14/8
        tc=-detkc*(bh/kqh)*c*c*(c*c-mh/th)**2*(c*c-vch)**2*(c*c-1)**2*(c*c-cph)*(c*c-csh)
        tf=detkc*sig**18*(sig*sig-bh/kqh)
        ch.exact('complete_wave_determinant_all_multiplicities',wc/tc-1)
        ch.add('reject_doubled_wave_determinant_normalization',CLEAN(wc/(2*tc)-1)!=0)
        ch.exact('complete_quartic_determinant_all_multiplicities',fc/tf-1)
        # Substitution follows the compact polynomial identity; no expanded primitive-coupling comparison.
        wave=tc.subs(definitions);fast=tf.subs(definitions)
        cs=CLEAN(csh.subs(definitions));ct=MP/MT;cp=1+x['zeta']*(x['u0']**2+x['v0']**2);ratio=x['b']/x['K_Q']
        Cc=s.Matrix([[0,0,1,0],[0,0,0,1],[-mh/(4*khh),0,0,mh/(sq*khh)],[0,0,mh/(sq*fh),0]])
        Kw=s.diag(kh,f2);Aw=s.diag(MP/4,0);Gw=s.Matrix([[0,-I*MP/sq],[-I*MP/sq,0]])
        C=s.zeros(4);C[:2,2:]=s.eye(2);C[2:,:2]=-Kw.inv()*Aw;C[2:,2:]=I*Kw.inv()*Gw
        ch.exact('compact_companion_exact_binding',C-Cc.subs(definitions))
        poly=Cc.charpoly();zero=s.Matrix([0,1,0,0]);general=s.Matrix([2*sq,0,0,1])
        ch.exact('generic_wave_companion_charpoly',poly.as_expr()-poly.gen**2*(poly.gen**2-csh))
        ch.exact('retained_zero_eigenvector',C*zero)
        ch.exact('retained_zero_Jordan_chain',C*general-zero)
        ch.exact('zero_column_rank_upper_bound',C[:,1])
        ch.exact('rank_three_minor_nonzero_on_regular_domain',Cc.extract([0,1,2],[0,2,3]).det()+mh/(4*khh))
        ch.exact('negative_trace_principal_energy_coefficient',Apr[0,0]-MP*p*p/4)
        ch.add('quartic_regulator_omission_witness',s.diff(Apr[9,9],p,4)!=0)
        # Do not label this frozen principal coefficient a complete evolving slow action.
        slow=CLEAN(f2-(MP/sq)**2/(MP/4))
        ch.exact('formal_frozen_principal_slow_time_coefficient',slow-f2+2*MP)
        radial=s.Matrix([x['u0'],x['v0'],0]);phase=s.Matrix([x['v0'],-x['u0'],0])
        ch.exact('matter_radial_unit_speed',Gm*radial-radial)
        ch.exact('matter_phase_speed',Gm*phase-cp*phase)
        olddata=old.derive();b1={x[n]:s.sympify(v) for n,v in ev.READ(ev.PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
        b1={q:val.subs(s.Symbol('eta'),1) for q,val in b1.items()}
        oldmap={olddata['p']:p,olddata['u']:x['u0'],olddata['v']:x['v0'],olddata['psi_dot']:x['psi_dot']}
        for name,m,key in [('A',Apr.extract(ids,ids),'A'),('R',Rpr.extract(ids,ids),'R'),('K',Kp.extract(ids,ids),'K')]:
            ch.exact('legacy_B1_eta1_normalization_control_'+name,m.subs(b1)-olddata[key].subs(oldmap))
        self.family={};eta=x['eta']
        for name,fam in ev.READ(ev.PLANAR)['families'].items():
            sub={x[n]:s.sympify(v,locals={'eta':eta}) for n,v in fam['parameter_map'].items()}
            ch.exact(name+'_positive_phase_speed_map',cp.subs(sub)-1-eta*(x['u0']**2+x['v0']**2)/13)
            vals={k:CLEAN(v.subs(sub)) for k,v in dict(M=MC,MT=MT,f2=f2,cL=cL,Kh=kh,K=x['K_Q'],b=x['b'],
                  tensor_c2=ct,vector_c2=cv,scalar_c2=cs,fast_sigma2=ratio,negative_slow_magnitude=-slow).items()}
            proofs={}
            for key,value in vals.items():
                ok,proof=interval_positive(value,eta);proofs[key]=proof
                ch.add(name+'_positive_'+key+'_on_open_eta_interval',ok,proof)
            vals.update(phase_c2='1+eta*(u0^2+v0^2)/13',zero_speed_Jordan_defect=True,
                        formal_frozen_principal_slow_K=str(slow.subs(sub)))
            self.family[name]={k:str(v) if isinstance(v,s.Basic) else v for k,v in vals.items()}
            self.family[name]['interval_proofs']=proofs
        print('Compile complete generic finite-k action for immutable numerical controls',flush=True)
        self.order=sorted({str(z) for m in (self.A,self.R,self.K) for e in m for z in e.free_symbols})
        self.fun=s.lambdify([[x[n] for n in self.order]],list(self.A)+list(self.R)+list(self.K),'numpy',cse=True)
        self.export=dict(field_order=list(FIELDS),physical_order=list(dyn),SO2_order=['h','TT+','TTx','Vlong','Vtrans1','Vtrans2','du','dv','dr','Pi'],
            A=MAT(self.A),R=MAT(self.R),K=MAT(self.K),SO2_map=MAT(O),principal_A=MAT(Apr),principal_R=MAT(Rpr),principal_K=MAT(Kp),
            independent_density_before=str(before),independent_density_after=str(density),shift_solution=str(szsol),regulator_solution=str(zsol),
            wave_determinant=str(wave),fast_determinant=str(fast),tensor_c2=str(ct),vector_c2=str(cv),scalar_c2=str(cs),
            phase_c2=str(cp),fast_sigma2=str(ratio),scalar_wave_companion=MAT(C),zero=MAT(zero),generalized=MAT(general),
            zero_algebraic_multiplicity=2,zero_geometric_multiplicity=1,
            principal_trace_energy='-a^3*MP2*p^2*abs(h)^2/8 at zero velocity',
            frozen_principal_slow_K=str(slow),full_evolving_slow_action_derived=False,families=self.family,
            ensemble='Inherited nonzero dust-clock chart; no new local fixed-charge restriction',
            Hamiltonian=dict(Hyy='a^3*(R.H*K.inv()*R-A)',Hyp='-R.H*K.inv()',Hpp='K.inv()/a^3'))


def action_numeric(red,b,p,ell):
    data=red.at(b,p,ell,np.zeros(22),np.zeros(4))
    LA,LB,LBT,LK=red.blocks(data['raw'],ell);dLA,dLB,dLBT,dLK=red.blocks(data['coefficient_dt'],ell)
    F,U,inv=(data[n] for n in ('F','U','inverse'));invd=2*b[1]*inv;invd[-1,-1]=0
    Y=U.conj().T@LA@F;V=U.conj().T@LB@F;Yd=U.conj().T@dLA@F;Vd=U.conj().T@dLB@F
    A=F.conj().T@LA@F-Y.conj().T@inv@Y
    R=F.conj().T@LBT@F-V.conj().T@inv@Y
    K=F.conj().T@LK@F-V.conj().T@inv@V
    Rd=F.conj().T@dLBT@F-Vd.conj().T@inv@Y-V.conj().T@invd@Y-V.conj().T@inv@Yd
    Kd=F.conj().T@dLK@F-Vd.conj().T@inv@V-V.conj().T@invd@V-V.conj().T@inv@Vd
    return data,(A,R,K),(Rd,Kd),(LBT,LK)


def numeric(ch,compiler,g,prior,time):
    red=time.EvolvingReduction(prior,g);records=[];spectra=[]
    J=np.block([[np.zeros((10,10)),np.eye(10)],[-np.eye(10),np.zeros((10,10))]])
    for ir,run in enumerate(ev.READ(PARENT+'trajectories.json')['runs']):
        eta=float(s.Rational(run['eta_exact']));p=g.bg.PARAMS.copy()
        for n,expr in ev.READ(ev.PLANAR)['families'][run['family']]['parameter_map'].items():
            p['K' if n=='K_Q' else n]=float(s.sympify(expr).subs(s.Symbol('eta'),s.Rational(run['eta_exact'])))
        p['gr']=3*eta/7;label=str(ir)
        print(json.dumps(dict(stage='FINITE_K_NODES',family=run['family'],eta=run['eta_exact'],method=run['method'])),flush=True)
        maxima=dict(binding=0.,canonical=0.,one_form=0.,auxiliary=0.,omitted_drift=0.)
        for it,bfull in enumerate(run['first_order_states']):
            b=np.asarray(bfull[:12],float);ell=80
            data,(A,R,K),(Rd,Kd),(LBT,LK)=action_numeric(red,b,p,ell);vol=b[0]**3;Ki=np.linalg.inv(K)
            raw=dict(zip(red.op.kernel.order,red.op.kernel.values(b,p)));raw['ell']=ell
            sym=np.asarray(compiler.fun([raw[n] for n in compiler.order]),complex).reshape(3,10,10)
            binding=max(NORM(actual-ref)/(1+NORM(actual)+NORM(ref)) for actual,ref in zip(sym,(A,R,K)))
            HH=np.block([[vol*(R.conj().T@Ki@R-A),-R.conj().T@Ki],[-Ki@R,Ki/vol]])
            M=np.block([[np.eye(10),np.zeros((10,10))],[vol*R,vol*K]])
            Md=np.block([[np.zeros((10,20))],[vol*(Rd+3*b[1]*R),vol*(Kd+3*b[1]*K)]])
            terms=(J@HH@M,-M@data['G'],-Md)
            canonical=NORM(sum(terms))/(sum(NORM(q) for q in terms)+1e-30)
            C0=LK@data['Q0d']+LBT@data['Q0'];C1=LK@(data['Q0']+data['Q1d'])+LBT@data['Q1']
            F,U=data['F'],data['U']
            form=max(NORM(F.conj().T@C0-R)/(1+NORM(R)),NORM(F.conj().T@C1-K)/(1+NORM(K)),
                     NORM(LK@data['Q1'])/(1+NORM(LK)))
            aux=max(NORM(U.conj().T@C0),NORM(U.conj().T@C1),NORM(data['D']@data['inverse']-np.eye(4)))
            omitted=NORM(terms[0]+terms[1])/(sum(NORM(q) for q in terms[:2])+1e-30)
            for key,value in dict(binding=binding,canonical=canonical,one_form=form,auxiliary=aux).items():maxima[key]=max(maxima[key],value)
            maxima['omitted_drift']=max(maxima['omitted_drift'],omitted)
            records.append(dict(run=ir,node=it,ell=ell,binding=binding,canonical=canonical,one_form=form,auxiliary=aux,
                omitted_drift_witness=omitted,kinetic_eigenvalues=np.linalg.eigvalsh(K).tolist()))
            if it in (0,10,20):
                for q in (4,40,80,128):
                    dd,(aa,rr,kk),_,_=action_numeric(red,b,p,q);ki=np.linalg.inv(kk)
                    hh=np.block([[vol*(rr.conj().T@ki@rr-aa),-rr.conj().T@ki],[-ki@rr,ki/vol]])
                    vals,vecs=eig(J@hh);growth=J@hh
                    res=max(NORM(growth@vecs[:,j]-vals[j]*vecs[:,j])/(NORM(growth)*NORM(vecs[:,j])+abs(vals[j])*NORM(vecs[:,j])+1e-30) for j in range(20))
                    direction=np.zeros(10);direction[0]=direction[2]=1/np.sqrt(2)
                    canonical_state=np.r_[direction,vol*rr@direction]
                    energy=float(np.real(canonical_state.conj()@hh@canonical_state/2))
                    expected=float(np.real(-vol*direction@aa@direction/2))
                    error=abs(energy-expected)/(1+abs(energy)+abs(expected))
                    tag=label+'_'+str(it)+'_'+str(q)
                    ch.small(tag+'_full_frozen_eigenpair_residual',res,1e-9)
                    ch.small(tag+'_zero_velocity_energy_identity',error,1e-9)
                    spectra.append(dict(run=ir,node=it,ell=q,physical_coordinate_p=q/b[0],
                        eigenpair_residual=res,frozen_canonical_generator_eigenvalues=ev.SER(sorted(vals,key=lambda z:(float(z.real),float(z.imag)))),
                        zero_velocity_trace_energy=energy,trace_energy_identity_error=error,
                        full_H_inertia=[int(np.sum(np.linalg.eigvalsh(hh)>0)),int(np.sum(np.linalg.eigvalsh(hh)<0))],
                        instantaneous_only=True))
        for key in ('binding','canonical','one_form','auxiliary'):ch.small(label+'_all21_'+key,maxima[key],1e-9)
        ch.add(label+'_reject_omitted_canonical_map_drift',maxima['omitted_drift']>1e-12,maxima['omitted_drift'])
    return dict(nodes=records,spectra=spectra,full_frozen_spectra_are_not_evolved_stability=True)


def calculate():
    pins,absent,snapshot,g,prior,time,old=inputs();before=snapshot();ch=Checks()
    compiler=Compiler(ch,old)
    numbers=numeric(ch,compiler,g,prior,time) if all(r['passed'] for r in ch.rows) else dict(skipped='Exact prerequisite failed')
    ch.add('source_sidecar_metadata_preserved',before==snapshot())
    scope=dict(claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,physics_pass=False,gate_effect='NONE',
        stage2_complete=False,stage3_entered=False,physical_window_admitted=False,principal_wave_basis_complete=False,
        inherited_clock_ensemble_unchanged=True,full_fixed_charge_energy_theorem=False,full_evolving_slow_action_derived=False,
        native_goal_resumed=False,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',
        K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        substantive_obstructions=['Generic zero-speed Jordan defect in declared wave-scale formulation',
            'Negative principal trace energy in the inherited instantaneous canonical chart',
            'Weighted mixed-order well-posedness and a physical window remain unresolved',
            'Full nonlinear/fixed-charge admission, healthy GR/local gravity and genuine matching remain open'])
    verification=dict(checks=ch.rows,total=len(ch.rows),passed=sum(r['passed'] for r in ch.rows))
    verification['validation']='PASS_LOCAL_DERIVATION' if verification['passed']==verification['total'] else 'FAIL_LOCAL_DERIVATION'
    bodies={'formulas.json':ev.ENCODE(compiler.export),'numerics.json':ev.ENCODE(numbers),
            'scope.json':ev.ENCODE(scope),'verification.json':ev.ENCODE(verification)}
    summary=dict(schema='r4c1-three-family-finite-k-v3',**verification,**scope,
        status='CONDITIONAL_GENERIC_CANONICAL_PRINCIPAL_AUDIT_WITH_RETAINED_OBSTRUCTIONS' if verification['passed']==verification['total'] else 'FINITE_K_AUDIT_UNRESOLVED',
        source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,source_metadata_preserved=len(before),
        artifacts={n:ev.SHA(b) for n,b in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
        review_id='R9-MT1-THREE-FAMILY-FINITE-K-V3',review_dependencies=['CUSP3-EVOLUTION-V1','THREE-FAMILY-FIXED-CHARGE-KINETIC-V3',
            'B1-NONZERO-CHARACTERISTIC','GENERIC-KERNEL/EVOLVING-REDUCTION','all transitive debt'])
    bodies['summary.json']=ev.ENCODE(summary);return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_three_family_finite_k_attempt_04');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse existing evidence')
    else:dest.mkdir(parents=True)
    try:bodies,summary=calculate()
    except BaseException as exc:
        if not args.replay:
            with (dest/'interrupted.json').open('xb') as f:f.write(ev.ENCODE(dict(validation='INTERRUPTED_NO_ACCEPTED_RECEIPT',error_type=type(exc).__name__,error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(ev.SHA(b)+'  '+n+'\n').encode():raise RuntimeError('Read-only replay differs: '+n)
        after=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay metadata changed')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for n,b in bodies.items():
            with (dest/n).open('xb') as f:f.write(b)
            with (dest/(n+'.sha256')).open('xb') as f:f.write((ev.SHA(b)+'  '+n+'\n').encode())
    print(json.dumps({n:summary[n] for n in ('validation','passed','total','status','physics_pass')}),flush=True)
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
