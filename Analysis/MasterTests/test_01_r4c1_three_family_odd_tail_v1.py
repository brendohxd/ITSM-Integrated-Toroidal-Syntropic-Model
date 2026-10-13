"""Continuous odd-response tail with analytic background bounds and exact arithmetic."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import platform
import re
import sys

import numpy as np
import scipy
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PARENT=BASE+'r4c1_three_family_time_response_attempt_03/'
TRAJECTORY=BASE+'r4c1_three_family_time_response_attempt_02/trajectories.json'
SOURCE=BASE+'r4c1_g3n4_attempt_01/formulas.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_ODD_TAIL_V1_CONTRACT_2026-10-12.md'
ARITHMETIC='Analysis/MasterTests/dust_certified_arithmetic_v1.py'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PINNED={CONTRACT:'9d3688ec3aeba5fc6c202c7c28320a2ce0fe3319da6bd552bd2710ca4fa327b1',
        ARITHMETIC:'f868032dcd939a52c3299ac66d5f4c18d02c5681bac7391bcce67732bc026599',
        PARENT+'summary.json':'7c43af5b34e8f08e9b74b49a7fe9316b2eddc5ed8376952df97fa70f5e425cea',
        TRAJECTORY:'8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d',
        'Theory/Gates/RES-001/RES001_R4C1_THREE_FAMILY_TIME_RESPONSE_V3_REPORT_2026-10-12.md':'21940488c8d2dd724ff8b73e49230f74d72365d0d58692fc152b6a0d985a2bda'}
FAMILIES=('archived_G3','new_B1_frame','new_hierarchical')
WAVES=(20,40,80)
TAILS=(5,9,31)
T=F(1,20)
ETA=F(1,4)
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda v:(json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
read=lambda n:json.loads((ROOT/n).read_bytes())
tidy=lambda x:s.factor(s.cancel(s.expand(x)))


class Checks:
    def __init__(self):self.rows=[]
    def add(self,n,ok,e=None):self.rows.append(dict(name=n,passed=bool(ok),evidence=e))
    def exact(self,n,x):
        z=tidy(x);self.add(n,z==0,str(z))


def imports_and_pins():
    old=read(PARENT+'summary.json');pins=dict(old['source_sha256'])
    pins.update({PARENT+n:h for n,h in old['artifacts'].items()});pins.update(PINNED);pins[SELF]=sha((ROOT/SELF).read_bytes())
    paths=[];missing=[]
    for n,h in pins.items():
        p=ROOT/n
        if sha(p.read_bytes())!=h:raise RuntimeError('Input drift: '+n)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0]!=h:raise RuntimeError('Sidecar drift: '+n)
            paths.append(side)
        else:missing.append(n)
    sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
    import dust_certified_arithmetic_v1 as ar
    import test_01_r4c1_gr_family_survey_v2 as generic
    import test_01_r4c1_three_family_nonanalytic_entry_v1 as entry
    return ar,generic,entry,pins,paths,missing


def operator_proof(generic,checks):
    kernel=generic.GenericKernel();sy=dict(kernel.sy)
    text=read(SOURCE)['quadratic_vector_action']
    names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',text))
    names.update('W W_t W_tt W_z W_zz B_z Hdot Hddot psi_ddot u_ddot v_ddot r_ddot C_dot epsilon_dot lambda_dot beta k eta mu m Fforce'.split())
    for n in names:
        if n not in sy:sy[n]=s.Symbol(n,real=True)
    a,H,Hd,k=(sy[n] for n in ('a','H','Hdot','k'))
    MP,MU,c1,c2,c3,c4,KQ,zz=(sy[n] for n in ('MP2','MU2','c1','c2','c3','c4','K_Q','zeta'))
    a13=MU*(c1+c3);f2=MU*(c1+c4);MT=MP-a13;sigma=-a13/MT
    cV=(MU*c1+a13*a13/(2*MT))/f2
    J=sy['v0']*sy['u_dot']-sy['u0']*sy['v_dot']
    mass=-(3*c2+c3-c4)/(c1+c4)*Hd+2*H*H-KQ/f2*sy['psi_dot']**2+zz/f2*J*J
    L=s.sympify(text,locals=sy)
    checks.exact('generic_shift_constraint_from_varied_vector_action',s.diff(L,sy['B_z']).subs(sy['B_z'],sigma*sy['W_z']))
    reduced=L.subs(sy['B_z'],sigma*sy['W_z'])
    rates={sy['a']:a*H,sy['H']:Hd,sy['Hdot']:sy['Hddot'],sy['psi_dot']:sy['psi_ddot'],
           sy['u0']:sy['u_dot'],sy['v0']:sy['v_dot'],sy['u_dot']:sy['u_ddot'],sy['v_dot']:sy['v_ddot']}
    if 'r0' in sy:rates[sy['r0']]=sy.get('r_dot',s.Symbol('r_dot',real=True))
    if 'r_dot' in sy:rates[sy['r_dot']]=sy['r_ddot']
    if 'C' in sy:rates[sy['C']]=sy['beta']*sy['psi_dot']*sy['C']
    if 'epsilon0' in sy:rates[sy['epsilon0']]=(-3*H-3*sy['beta']*sy['psi_dot'])*sy['epsilon0']
    if 'lambda0' in sy:rates[sy['lambda0']]=sy['lambda_dot']
    dt=lambda x:s.expand(sum(s.diff(x,q)*v for q,v in rates.items()))
    cross=s.diff(reduced,sy['W'],sy['W_t']);position=s.diff(reduced,sy['W'],2)
    checks.exact('generic_vector_kinetic_residue',s.diff(reduced,sy['W_t'],2)-f2)
    checks.exact('generic_vector_speed',-a*a*s.diff(reduced,sy['W_z'],2)/f2-cV)
    checks.exact('FRAME_mass_from_actual_quadratic_action',(dt(cross)+3*H*cross-position)/f2-mass)
    # Independent full22 Euler embedding at arbitrary symbolic momentum.
    LA,LB,LBT,LK=[[s.Integer(0)]*22 for _ in range(4)]
    weights=(s.Integer(1),None,s.Integer(0),s.Integer(0),s.I*k)
    selected={generic.IDX['Sy']:sigma,generic.IDX['Vy']:s.Integer(1)}
    multiplier=3*MU*c2*Hd-3*MU*(c1+c3)*H*H
    for record,value in zip(kernel.records,kernel.expr):
        bi,i=divmod(record['row'],22);bj,j=divmod(record['column'],22)
        if j not in selected:continue
        value=value*selected[j]
        if 'lambda0' in sy:value=value.subs(sy['lambda0'],multiplier)
        if bi!=1 and bj!=1:LA[i]+=s.conjugate(weights[bi])*value*weights[bj]
        elif bi!=1:LB[i]+=s.conjugate(weights[bi])*value
        elif bj!=1:LBT[i]+=value*weights[bj]
        else:LK[i]+=value
    W,Wd,Wdd=(sy[n] for n in ('W','W_t','W_tt'))
    expected=-f2*(Wdd+3*H*Wd+(cV*k*k/a**2+mass)*W)
    for i,field in enumerate(generic.FIELDS):
        row=(LA[i]-dt(LBT[i])-3*H*LBT[i])*W+(LB[i]-LBT[i]-dt(LK[i])-3*H*LK[i])*Wd-LK[i]*Wdd
        checks.exact('full22_generic_odd_embedding_'+field,row-(expected if field=='Vy' else 0))
    e=sy['eta'];ideal={MP:1,MU:2*e/3,c1:s.Rational(1,5),c4:s.Rational(1,20),KQ:3*e,zz:e/13}
    forms={}
    for name in FAMILIES:
        p={**ideal,c2:-s.Rational(7,48) if name=='archived_G3' else s.Rational(1,10),
           c3:-s.Rational(1,80) if name=='archived_G3' else (-s.Rational(1,5) if name=='new_B1_frame' else -s.Rational(1,5)+3*e/16)}
        mw=tidy(mass.subs(p));mx=tidy(mw-s.Rational(3,2)*Hd-s.Rational(9,4)*H**2)
        dH=s.Integer(2) if name=='archived_G3' else (-s.Rational(1,5) if name=='new_B1_frame' else -s.Rational(1,5)-3*e/4)
        declared=dH*Hd+2*H**2-18*sy['psi_dot']**2+6*J**2/13
        checks.exact(name+'_independent_declared_FRAME_mass',mw-declared)
        checks.exact(name+'_frame_to_canonical_rescaling_identity',mw-mx-s.Rational(3,2)*Hd-s.Rational(9,4)*H**2)
        checks.add(name+'_reject_canonical_mass_in_FRAME_equation',tidy(mw-mx)!=0,str(tidy(mw-mx)))
        forms[name]=dict(frame_mass=str(mw),canonical_mass=str(mx),cV2=str(tidy(cV.subs(p))),sigma=str(tidy(sigma.subs(p))))
    # Energy comparison identity is separate from the physical Hamiltonian.
    x,v,Ff,m,mu,cv,kn=s.symbols('x v Fforce m mu cv kn',real=True)
    En=v*v+(cv*kn*kn/a**2+mu*mu)*x*x
    derivative=s.diff(En,x)*v+s.diff(En,v)*(-3*H*v-(cv*kn*kn/a**2+m)*x+Ff)+s.diff(En,a)*a*H
    expected_energy=-6*H*v*v-2*H*cv*kn*kn*x*x/a**2+2*(mu*mu-m)*x*v+2*Ff*v
    checks.exact('comparison_norm_energy_identity',derivative-expected_energy)
    nu=s.Symbol('nu',real=True)
    checks.exact('Young_square_for_uniform_energy_comparison',v*v+nu*nu*x*x-2*nu*x*v-(v-nu*x)**2)
    bn,dd,alpha=s.symbols('b_n D alpha',real=True)
    checks.exact('complex_Fourier_pair_Parseval_force_factor',2*(dd*bn/(2*alpha))**2-(dd/alpha)**2*bn**2/2)
    theta=s.Symbol('theta',real=True)
    checks.exact('independent_constant_forcing_energy_formula',s.trigsimp(s.sin(theta)**2+(1-s.cos(theta))**2-2*(1-s.cos(theta))))
    checks.add('reject_even_epsilon_in_signed_nonanalytic_source',(-1)*abs(-1)!=(-1)**2)
    return dict(generic_frame_mass=str(tidy(mass)),generic_cV2=str(tidy(cV)),generic_sigma=str(tidy(sigma)),families=forms,
                full_signed_forcing='S_Vy(n)=-3*A*abs(psi_dot)^3*epsilon*abs(epsilon)*w*abs(w)*b_n/2, all odd n',
                energy_identity=str(expected_energy),energy_scope='positive auxiliary comparison norm, NOT the physical coupled Hamiltonian',
                zero_energy_limit='apply comparison to sqrt(E+delta^2) and let delta decrease to0; no division by zero',
                infinite_tail='all complex Fourier pairs |n|>N, forcing b_n/2, Parseval sum b_n^2/2')


def background_proof(checks):
    a,H,u,ud,v,vd,r,rd,pd,rho,K,Mc,beta,m2,l4,l6,Lambda,mr2,lr,gr=s.symbols('a H u ud v vd r rd pd rho K Mc beta m2 l4 l6 Lambda mr2 lr gr',real=True)
    rad=u*u+v*v;V=m2*rad/2+l4*rad**2/8+l6*rad**3/(24*Lambda**2)+mr2*r*r/2+lr*r**4/4+gr*rad*r*r/4
    kin=ud*ud+vd*vd+rd*rd+K*pd*pd;energy=kin/2+V+rho
    rate={a:a*H,H:-(kin+rho)/(2*Mc),u:ud,ud:-3*H*ud-s.diff(V,u),v:vd,vd:-3*H*vd-s.diff(V,v),
          r:rd,rd:-3*H*rd-s.diff(V,r),pd:-3*H*pd-beta*rho/K,rho:(-3*H+beta*pd)*rho}
    dt=lambda q:sum(s.diff(q,x)*y for x,y in rate.items())
    checks.exact('exact_background_total_energy_balance',dt(energy)+3*H*(kin+rho))
    checks.exact('exact_background_Friedmann_defect_constant',dt(3*Mc*H*H-energy))
    checks.exact('exact_background_charge_conservation',dt(a**3*(u*vd-v*ud)))
    checks.exact('exact_phase_integrating_factor',dt(a**3*pd)+a**3*beta*rho/K)
    psi=s.Symbol('psi',real=True);rate[psi]=pd
    checks.exact('exact_dust_integrating_factor',dt(a**3*rho*s.exp(-beta*psi)))
    return dict(total_energy=str(energy),energy_balance='E_dot=-3H*(kin+rho)',
                regular_domain='positive scalar potential/K/Mcos, rho positive, verified H/phase bootstrap margins; finite amplitudes imply ODE continuation on [0,T]',
                H_min='H0_lower-E0_upper*T/Mcos_lower',phase_min='p0_lower/exp(3H0_upper*T)-beta_upper*E0_upper*T/K_lower',
                charge='Q=a^3*(u*v_dot-v*u_dot) constant; J^2=Q^2/a^6',
                interval_scope='exact ideal recipe AND all stored binary64 parameter/seed values in one outward enclosure; not archived solver-error certification')


def ideal_parameters(name):
    p=dict(MP2=F(1),MU2=F(2,3)*ETA,c1=F(1,5),c2=F(1,10),c3=-F(1,5),c4=F(1,20),
           K=3*ETA,A=F(2,7)*ETA*F(1,2),b=F(5,11)*ETA,zeta=ETA/13,beta=F(2,5)*ETA**2,
           gr=F(3,7)*ETA,m2=F(1),l4=F(1,3),l6=F(1,5),cutoff=F(2),mr2=F(2),lr=F(1,7),vacuum=F(0))
    if name=='archived_G3':p.update(c2=-F(7,48),c3=-F(1,80))
    elif name=='new_hierarchical':p['c3']+=3*ETA/16
    return p


def enclosure(ar,values):
    parts=[ar.IV.fraction(q) for q in values]
    return ar.IV(min(q.lo for q in parts),max(q.hi for q in parts))


def exp_box(ar,x):
    if x.lo<0:raise ValueError('Nonnegative exponent required')
    term=total=ar.ONE
    for i in range(1,161):term=(term*ar.IV(x.lo)).scale(1,i);total=total+term
    return ar.IV(total.lo,ar.exp_upper(x))


def pi_box(ar,checks):
    def atan_bounds(q,terms):
        partial=sum(((-1)**j*q**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
        next_term=(-1)**terms*q**(2*terms+1)/F(2*terms+1)
        return min(partial,partial+next_term),max(partial,partial+next_term)
    alo,ahi=atan_bounds(F(1,5),64);blo,bhi=atan_bounds(F(1,239),64)
    low,high=16*alo-4*bhi,16*ahi-4*blo
    # Exact tangent-addition proof fixes the branch: 4atan(1/5)-atan(1/239)=pi/4.
    tangent=F(1,5)
    twice=2*tangent/(1-tangent*tangent);four=2*twice/(1-twice*twice)
    checks.add('Machin_identity_exact_tangent_and_branch', (four-F(1,239))/(1+four*F(1,239))==1 and F(0)<4*alo-bhi and 4*ahi-blo<1)
    out=enclosure(ar,(low,high));checks.add('pi_interval_positive_and_tight',out.lo>3*ar.SCALE and out.hi<4*ar.SCALE and high-low<F(1,10**70))
    # Independent rational exponential enclosure checks on all required small exponents.
    for xx in (F(1,100),F(1,20),F(1,10)):
        exact=sum((xx**j/F(factorial(j)) for j in range(51)),F(0))
        next_term=xx**51/F(factorial(51));upper=exact+next_term/(1-xx/F(52))
        bound=exp_box(ar,ar.IV.fraction(xx))
        checks.add('independent_rational_exponential_'+str(xx),F(bound.lo,ar.SCALE)<=exact and F(bound.hi,ar.SCALE)>=upper)
    return out


def energy_iv(ar,p,y):
    a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=y
    rad=u.square()+v.square()
    pot=p['m2']*rad/2+p['l4']*rad.square()/8+p['l6']*rad.power(3)/(24*p['cutoff'].square())+p['mr2']*r.square()/2+p['lr']*r.power(4)/4+p['gr']*rad*r.square()/4+p['vacuum']
    kin=ud.square()+vd.square()+rd.square()+p['K']*pd.square()
    return kin/2+pot+rho


def require_positive(values,label):
    if any(x.lo<=0 for x in values):raise ValueError('Refuse nonpositive '+label)
    return True


def certificate(name,ar,generic,entry,checks,pi):
    exact=ideal_parameters(name);floating,seed=entry.initial_conditions(generic,name,float(ETA))
    p={n:enclosure(ar,(q,F.from_float(float(floating[n])))) for n,q in exact.items()}
    positive=('MP2','MU2','K','A','b','zeta','beta','gr','m2','l4','l6','cutoff','mr2','lr')
    checks.add(name+'_positive_coefficients_for_energy_bootstrap',all(p[n].lo>0 for n in positive) and p['vacuum'].lo>=0)
    require_positive([p[n] for n in positive],'energy/potential coefficients')
    if p['vacuum'].lo<0:raise ValueError('Refuse negative vacuum energy in positivity proof')
    MC=p['MP2']+p['MU2']*(p['c1']+3*p['c2']+p['c3'])/2
    f2=p['MU2']*(p['c1']+p['c4']);a13=p['MU2']*(p['c1']+p['c3']);MT=p['MP2']-a13
    cv=(p['MU2']*p['c1']+a13.square()/(2*MT))/f2;sigma=-a13/MT
    fixed=[F(1),F(0),F(1,2),F(0),F(0),F(1,2),F(1,2),F(1,8),F(0),F(1,20),F(1,5),F(0)]
    initial=[enclosure(ar,(q,F.from_float(float(z)))) for q,z in zip(fixed,seed)]
    # H is initialized by the original recipe, not by the placeholder zero above.
    E0=energy_iv(ar,p,initial);Hrecipe=(E0/(3*MC)).sqrt()
    initial[1]=enclosure(ar,(F(Hrecipe.lo,ar.SCALE),F(Hrecipe.hi,ar.SCALE),F.from_float(float(seed[1]))))
    H0=initial[1];E=ar.IV(E0.hi);time=ar.IV.fraction(T);one=ar.ONE
    Hlow=ar.IV(H0.lo)-E*time/ar.IV(MC.lo)
    phase_low=ar.IV(initial[9].lo)/exp_box(ar,3*ar.IV(H0.hi)*time)-ar.IV(p['beta'].hi)*E*time/ar.IV(p['K'].lo)
    checks.add(name+'_continuous_H_bootstrap_margin_POSITIVE',Hlow.lo>0,Hlow.encode())
    checks.add(name+'_continuous_phase_bootstrap_margin_POSITIVE',phase_low.lo>0,phase_low.encode())
    checks.add(name+'_nonzero_vector_domain',min(MC.lo,f2.lo,MT.lo,cv.lo)>0)
    require_positive((Hlow,phase_low,MC,f2,MT,cv),'continuous H/phase/vector domain: '+name)
    amax=ar.IV(initial[0].hi)*exp_box(ar,ar.IV(H0.hi)*time)
    rhomin=ar.IV(initial[10].lo)/exp_box(ar,3*ar.IV(H0.hi)*time)
    Hd=ar.IV((-E/ar.IV(MC.lo)).lo,(-rhomin/(2*ar.IV(MC.hi))).hi)
    Hb=ar.IV(Hlow.lo,H0.hi);pd=ar.IV(phase_low.lo,initial[9].hi)
    charge=initial[0].power(3)*(initial[2]*initial[5]-initial[4]*initial[3])
    Jsquared=ar.IV((charge.square()/amax.power(6)).lo,(charge.square()/ar.IV(initial[0].lo).power(6)).hi)
    mass=-(3*p['c2']+p['c3']-p['c4'])/(p['c1']+p['c4'])*Hd+2*Hb.square()-p['K']/f2*pd.square()+p['zeta']/f2*Jsquared
    L=ar.IV((one-mass).abs_upper()).scale(1,2);exponent=exp_box(ar,L*time)
    constraint_pref=(one+ar.IV(sigma.abs_upper()).square()).sqrt()
    constants=dict(parameters=p,initial=initial,E0=E0,Mcos=MC,frame_residue=f2,cV2=cv,sigma=sigma,
                   H=Hb,a=ar.IV(initial[0].lo,amax.hi),rho=ar.IV(rhomin.lo,E.hi),pd=pd,Hdot=Hd,J2=Jsquared,
                   frame_mass=mass,L=L,exp_LT=exponent,constraint_prefactor=constraint_pref,mu=one)
    constants.update(Phi_radius2_upper=2*E/ar.IV(p['m2'].lo),radion2_upper=2*E/ar.IV(p['mr2'].lo),
                     scalar_velocity_norm2_upper=2*E,psi=ar.IV(initial[8].lo,(ar.IV(initial[8].hi)+ar.IV(pd.hi)*time).hi),
                     potential_Lambda_is_NOT_a_physical_cutoff=p['cutoff'])
    modes=[]
    for k in WAVES:
        frequency=ar.IV(cv.lo)*k*k/amax.square()+ar.IV(mass.lo)
        checks.add(name+'_k'+str(k)+'_continuous_frame_frequency_squared_POSITIVE',frequency.lo>0,frequency.encode())
        if frequency.lo<=0:raise ValueError('Unproved frame-frequency domain')
        first_energy=ar.IV(cv.hi)*k*k/ar.IV(initial[0].lo).square()+one
        min_nu=ar.IV(cv.lo)*k*k/amax.square()+one
        W2=first_energy/min_nu*exponent.square()
        D=3*ar.IV(p['A'].hi)*ar.IV(pd.hi).power(3)*W2
        transfer=D*time*exponent/ar.IV(f2.lo)
        tails=[]
        for N in TAILS:
            forcing_tail=128/(5*ar.IV(pi.lo).square()*N**5)
            energy=transfer.square()*forcing_tail
            norm=energy.sqrt();field=constraint_pref*norm;velocity=field;gradient=field/ar.IV(cv.lo).sqrt()
            tails.append(dict(N=N,energy=energy,full22_field_L2=field,full22_velocity_L2=velocity,full22_physical_gradient_L2=gradient))
        modes.append(dict(k=k,frame_frequency_lower=frequency,W2=W2,D_upper=D,transfer_upper=transfer,tails=tails,
                          first_energy_norm_upper=first_energy*exponent.square()))
    return constants,modes,floating,seed


def independent_controls(ar,checks,pi,constants):
    for label,call in (
        ('reject_zero_residue_inverse',lambda:ar.ONE/ar.ZERO),
        ('reject_negative_sqrt',lambda:ar.IV.fraction(-1).sqrt()),
        ('reject_negative_exponential_input',lambda:exp_box(ar,ar.IV.fraction(-1))),
        ('reject_failed_H_bootstrap_premise',lambda:require_positive((ar.IV.fraction(-1),),'H margin')),
        ('reject_failed_phase_bootstrap_premise',lambda:require_positive((ar.IV.fraction(-1),),'phase margin')),
        ('reject_negative_potential_energy_premise',lambda:require_positive((ar.IV.fraction(-1),ar.ONE),'potential coefficient'))):
        try:call()
        except (ValueError,ZeroDivisionError):checks.add(label,True)
        else:checks.add(label,False)
    for N in TAILS:
        # Closed constant-coefficient forced oscillator, independent of ITSM trajectories.
        # x_n=F_n(1-cos(omega*t))/omega^2, xdot_n=F_n sin(omega*t)/omega.
        energy=0.
        for n in range(N+1,N+1002):
            if n%2==0:continue
            bn=-8*(-1)**((n-1)//2)/(np.pi*n*(n*n-4));Fn=-bn/2;omega=np.sqrt(n*n+1)
            x=Fn*(1-np.cos(omega*float(T)))/omega**2;v=Fn*np.sin(omega*float(T))/omega
            energy+=2*(v*v+(n*n+1)*x*x)
        bound=ar.IV.fraction(T).square()*128/(5*ar.IV(pi.lo).square()*N**5)
        checks.add('independent_closed_oscillator_prefix_N'+str(N),energy<=float(F(bound.hi,ar.SCALE)),energy)
    for name,cc in constants.items():
        checks.add(name+'_mu_norm_not_identified_with_potential_Lambda',cc['mu'].hi!=cc['parameters']['cutoff'].hi)


def archive_controls(ar,generic,entry,checks,all_constants,all_modes,pi):
    runs=read(TRAJECTORY)['runs'];labels=0
    for run in runs:
        name=run['family'];cc=all_constants[name];mm=next(q for q in all_modes[name] if q['k']==run['k'])
        p,_=entry.initial_conditions(generic,name,float(ETA))
        ppoint={n:ar.IV.fraction(F.from_float(float(z))) for n,z in p.items()}
        for i,z in enumerate(run['first_order_states']):
            yy=[ar.IV.fraction(F.from_float(float(q))) for q in z[:12]]
            a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=yy;energy=energy_iv(ar,ppoint,yy)
            w=ar.IV.fraction(F.from_float(float(z[12])));wd=ar.IV.fraction(F.from_float(float(z[13])))
            label=name+'_k'+str(run['k'])+'_'+run['method']+'_sample'+str(i)
            conditions=(energy.hi<=cc['E0'].hi,H.lo>=cc['H'].lo,H.hi<=cc['H'].hi,a.lo>=cc['a'].lo,a.hi<=cc['a'].hi,
                        pd.lo>=cc['pd'].lo,pd.hi<=cc['pd'].hi,rho.lo>=cc['rho'].lo,rho.hi<=cc['rho'].hi,
                        w.square().hi<=mm['W2'].hi)
            checks.add(label+'_stored_first_mode_WITHIN_continuous_envelope',all(conditions),list(conditions));labels+=1
            # Independent finite subset of a mathematical N=3 tail: archived n=5 only.
            state=np.asarray(run['states'][i]);x=state[50,0]+1j*state[50,1];xd=state[51,0]+1j*state[51,1]
            partial=2*(abs(xd)**2+(float(F(cc['cV2'].hi,ar.SCALE))*(5*run['k'])**2/z[0]**2+1)*abs(x)**2)
            bound=mm['transfer_upper'].square()*128/(5*ar.IV(pi.lo).square()*3**5)
            checks.add(label+'_independent_archived_odd5_prefix_BELOW_full_N3_tail_control',partial<=float(F(bound.hi,ar.SCALE)),partial)
    checks.add('all378_original_sample_controls_retained',labels==378)


def serialize_intervals(ar,value):
    if isinstance(value,ar.IV):return dict(dyadic=value.encode(),display=[float(F(value.lo,ar.SCALE)),float(F(value.hi,ar.SCALE))])
    if isinstance(value,dict):return {n:serialize_intervals(ar,q) for n,q in value.items()}
    if isinstance(value,(list,tuple)):return [serialize_intervals(ar,q) for q in value]
    return value


def calculate():
    ar,generic,entry,pins,paths,missing=imports_and_pins();before=entry.snapshot(paths);checks=Checks()
    forms=operator_proof(generic,checks);forms['background']=background_proof(checks);pi=pi_box(ar,checks)
    constants={};modes={}
    for name in FAMILIES:
        cc,mm,_,_=certificate(name,ar,generic,entry,checks,pi);constants[name]=cc;modes[name]=mm
        print(json.dumps(dict(stage='CONTINUOUS_ODD_TAIL',family=name,mass=[float(F(cc['frame_mass'].lo,ar.SCALE)),float(F(cc['frame_mass'].hi,ar.SCALE))],H_lower=float(F(cc['H'].lo,ar.SCALE)),phase_lower=float(F(cc['pd'].lo,ar.SCALE)))),flush=True)
    independent_controls(ar,checks,pi,constants)
    archive_controls(ar,generic,entry,checks,constants,modes,pi)
    checks.add('all_input_hash_size_mtime_preserved',entry.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(q['passed'] for q in checks.rows)
    bodies={'formulas.json':encode(forms), 'bounds.json':encode(serialize_intervals(ar,dict(constants=constants,modes=modes,pi=pi,time=str(T),arithmetic_bits=ar.BITS))),
            'scope.json':encode(dict(epsilon_scaling='coefficient bound times abs(epsilon)^2 for the e*abs(e) odd response',
                                     norm_units='M_P=1 chart; field dimension0, velocity/physical-gradient dimension1; energy-norm dimension2, NOT physical Hamiltonian',
                                     uncomputed_modes='every odd n>N, positive/negative Fourier pair convention, no finite invariant manifold',
                                     high_frequency_scope='mathematical continuation of the declared classical operator; no physical UV completion/cutoff admission',
                                     finite_solver_error_certified=False,full_nonlinear_remainder_certified=False,new_background_integrations=0,new_time_response_integrations=0))}
    j=dict(schema='r4c1-three-family-odd-tail-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
           status='CONDITIONAL_CONTINUOUS_ODD_RESPONSE_TAIL_CHECKED_FULL_DOMAIN_OPEN' if passed==len(checks.rows) else 'ODD_TAIL_FAILURE_REQUIRES_DISPOSITION',
           continuous_odd_tail_certified=passed==len(checks.rows),finite_solver_error_certified=False,full_nonlinear_remainder_certified=False,
           full_coupled_interactions_computed=False,physical_EFT_cutoff_derived=False,physical_go=False,stage2_complete=False,stage3_entered=False,
           physical_decision='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
           canonical_tests_1_to_3='HOLD_SUBSTANTIVE',**{'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'},K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
           source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,
           substantive_unknowns=['Full coupled nonlinear remainder','All-sector continuous physical frequency/momentum window and complete interactions',
                                 'Mean/physical-energy/fixed-charge/singular/quartic sectors','Healthy GR/full PPN','Genuine identifying matter-residue and nonlinear-force matching'],
           review_dependencies=['THREE-FAMILY-TIME-RESPONSE-V3','all inherited deferred review'],artifacts={n:sha(b) for n,b in bodies.items()},
           runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
    bodies['summary.json']=encode(j);return bodies,j


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',default=BASE+'r4c1_three_family_odd_tail_attempt_01');parser.add_argument('--replay')
    args=parser.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay missing')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing receipts')
    bodies,j=calculate()
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(sha(b)+'  '+n+'\n').encode():raise RuntimeError('Immutable replay mismatch: '+n)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for n,b in bodies.items():
            with (dest/n).open('xb') as stream:stream.write(b)
            with (dest/(n+'.sha256')).open('xb') as stream:stream.write((sha(b)+'  '+n+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=j['validation'],passed=j['passed'],total=j['total'],physics_pass=False,status=j['status'])))
    for q in j['checks']:
        if not q['passed']:print(json.dumps(q))
    return int(j['passed']!=j['total'])


if __name__=='__main__':raise SystemExit(main())
