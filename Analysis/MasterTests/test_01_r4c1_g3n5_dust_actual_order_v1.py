"""Full retained-response and mathematical original-dust error-order certificate."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback
import math
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
import scipy
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v4.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='21419587770e4fad695d1d7c86f5038b0110d6de560a363e78fb78cf2a72b391':raise RuntimeError('Frozen V4 drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_corrected_dust_remainder_v4 as engine
old=engine.old;prior=engine.prior;common=engine.common
PARENT=BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_04/'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_ACTUAL_ORDER_CONTRACT_2026-10-12.md'
PROGRESS=None

def progress(message):
    print(message,flush=True)
    if PROGRESS is not None:PROGRESS.write(message+'\n');PROGRESS.flush()

def exp_upper(x):
    # e<3 follows from 1/n!<=1/2^(n-1) for n>=2, strictly for n>=3.
    # Thus exp(x)<=3^ceil(x), x>=0. Never convert a huge bound to float.
    if x<0:raise ValueError('Negative exponential argument')
    return s.Integer(3)**int(s.ceiling(x))

def calculate():
    ps=common.read_json(PARENT+'summary.json')
    if common.sha((ROOT/(PARENT+'summary.json')).read_bytes())!='f8ad05b485f7b384cdde29e5ab5e0227f074fee6c626555006ef010601c6496f':raise RuntimeError('Parent receipt drift')
    pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()})
    pins[PARENT+'summary.json']='f8ad05b485f7b384cdde29e5ab5e0227f074fee6c626555006ef010601c6496f'
    for rel in (SELF,CONTRACT,
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_REFERENCE_REMAINDER_REPORT_2026-10-12.md',
                'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_REFERENCE_REPLAY_NOTE_2026-10-12.md'):
        pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/p for p in pins]
    paths.extend(Path(str(p)+'.sha256') for p in list(paths) if Path(str(p)+'.sha256').exists())
    before=old.parent.snapshot(paths)
    checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell
    eps=s.Symbol('eps',positive=True);sy={**bg.sy,'eps':eps}
    on=lambda mat:mat.applyfunc(s.cancel)
    exact=lambda name,mat:old.parent.exact(checks,name,on(mat) if isinstance(mat,s.MatrixBase) else s.cancel(mat))
    shell=lambda mat:mat.applyfunc(lambda val:bg.constraint_reduce_scalar(val) if val!=0 else s.Integer(0))
    checks.add('parent_complete_scoped_lemma_not_physical_closure',ps['passed']==ps['total']==100 and ps['corrected_reference_forced_remainder_proved'] and not ps['physics_pass'] and not ps['full_prepared_high_p_remainder_proved'])
    un=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    maps={name:old.parent.import_matrix(obj,bg.sy) for name,obj in common.read_json(un['general_exact_maps_source'])['matrices'].items()}
    F,L,Q,drift,R0,R1,R2,U,Tw,Twi=[maps[k] for k in ('dispersive_principal_F','ordinary_wave_principal_L','positive_evolution_Q','wave_drift','residual_numerator_0','residual_numerator_1','residual_numerator_2','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi')]
    g=s.Rational(-22,375)*a*a;den=1-g*eps**2
    exact('fast_map_cubic_identity',U**3-g*U)
    exact('fast_principal_Q_skew',F.conjugate().T*Q+Q*F)
    exact('wave_principal_Q_skew',L.conjugate().T*Q+Q*L)
    Ps=s.zeros(20);Ps[3,3]=Ps[13,13]=1
    Pf=s.zeros(20);Pf[9,9]=Pf[19,19]=1
    Pw=s.eye(20)-Ps-Pf
    for name,p in (('slow',Ps),('wave',Pw),('fast',Pf)):
        exact('Q_partition_'+name,Q*p-p*Q)
    B0=on(drift+R0)
    Bf=on(B0-Pf*B0*(Ps+Pw)-(Ps+Pw)*B0*Pf)
    V=old.parent.import_matrix(common.read_json(BASE+'r4c1_g3n5_dust_fast_transfer_attempt_01/formulas.json')['matrices']['second_fast_map_V'],bg.sy)
    Li=s.zeros(20)
    for pos,vel,c2 in ((0,10,s.Rational(1,3)),(1,11,1),(2,12,1),(4,14,s.Rational(4,5)),(5,15,s.Rational(4,5)),(8,18,1)):
        Li[pos,vel]=-a/c2;Li[vel,pos]=a
    P=s.eye(2)+s.Matrix([v,-u])*s.Matrix([[v,-u]])/13
    Li[6:8,16:18]=on(-a*P.inv());Li[16:18,6:8]=a*s.eye(2)
    off=Ps*Bf*Pw+Pw*Bf*Ps
    Sw=on(Ps*off*Li-Li*off*Ps);Bc=on(Bf-off)
    nr1=on(L*V-V*L+R1+Bf*Sw-Sw*Bc-bg.dt(Sw))
    off1=on(Ps*nr1*Pf+Pf*nr1*Ps)
    Fi=s.zeros(20);Fi[9,19]=-33*a*a/5;Fi[19,9]=a*a
    Sf=on(Ps*off1*Fi-Fi*off1*Ps)
    exact('wave_inverse',L*Li-Pw)
    exact('wave_slow_separation',L*Sw-Sw*L+off)
    exact('wave_map_commutes_fast',F*Sw-Sw*F)
    exact('fast_slow_separation',F*Sf-Sf*F+off1)
    checks.add('omitted_wave_separation_rejected',any(z!=0 for z in Ps*off*Pw))
    checks.add('omitted_fast_separation_rejected',any(z!=0 for z in Ps*off1*Pf))
    for name,p in (('slow',Ps),('wave',Pw),('fast',Pf)):
        exact('order_zero_partition_'+name,Bc*p-p*Bc)
    progress('All-state separation identities and Q-skew principals verified')
    Tc={0:s.eye(20),1:Sw,2:V,3:V*Sw+Sf,4:Sw*Sf,5:V*Sf,6:V*Sw*Sf}
    base={};K={}
    def add(target,power,mat):target[power]=target.get(power,s.zeros(20))+mat
    for j,Tj in Tc.items():
        add(base,j-2,F*Tj-Tj*F);add(base,j-1,L*Tj-Tj*L)
        add(base,j,drift*Tj-Tj*Bc-bg.dt(Tj))
    for j,Bj in base.items():add(K,j,Bj);add(K,j+2,-g*Bj)
    for j,Tj in Tc.items():
        for k,Rk in enumerate((R0,R1,R2)):add(K,j+k,Rk*Tj)
    weights=[3 if i in (3,13) else 1 if i in (9,19) else 2 for i in range(20)]
    weightedT={};weightedK={}
    for source,target,label in ((Tc,weightedT,'transform'),(K,weightedK,'remainder')):
        bad=[]
        for j,mat in source.items():
            for i in range(20):
                for k in range(20):
                    val=mat[i,k]
                    if val==0:continue
                    power=j+weights[k]-weights[i]
                    if power<0:
                        if s.cancel(val)!=0:bad.append((power,i,k))
                    else:target.setdefault(power,s.zeros(20))[i,k]+=val
        checks.add('no_negative_weighted_'+label+'_powers',not bad,bad)
    T0=on(weightedT[0]);Ni=T0-s.eye(20);Ti0=s.eye(20)-Ni
    exact('weighted_constant_nilpotent',Ni*Ni)
    exact('weighted_constant_inverse',T0*Ti0-s.eye(20))
    checks.add('omitted_transform_drift_rejected',any(val!=0 for val in bg.dt(Sw)))
    boxes={bg.sy[k]:(s.sympify(z[0]),s.sympify(z[1])) for k,z in un['background_boxes'].items()}
    box=engine.EnclosureBox(boxes)
    norm=lambda mat:max(box.norm(mat),box.norm(mat.T))
    tnorm={j:norm(mat) for j,mat in weightedT.items()}
    knorm={j:norm(mat) for j,mat in weightedK.items()}
    ni=norm(Ti0);m=16
    dev=lambda kval:ni*sum(val/s.Integer(kval)**j for j,val in tnorm.items() if j>0)
    while dev(m)>s.Rational(1,2):m*=2
    inv=2*ni;kt=sum(val/s.Integer(m)**j for j,val in tnorm.items())
    kk=sum(val/s.Integer(m)**j for j,val in knorm.items())
    qmin,qmax=s.Rational(5,33),s.Rational(9,8)
    gamma=s.cancel((norm(bg.dt(Q))+2*qmax*(norm(Bc)+inv*kk))/(2*qmin))
    checks.add('whole_box_neumann_domain',dev(m)<=s.Rational(1,2),{'ell_min':m})
    checks.add('inherited_metric_condition_ratio',9*qmin>=qmax)
    checks.add('fast_denominator_positive',g.subs(a,boxes[a][0])<0 and boxes[a][0]>0)
    progress('Exact weighted propagator constants derived: sufficient ell>='+str(m))
    raw=common.read_json(old.PARENT+'matrices.json')
    obs,bi,Az,M=[old.parent.import_matrix(raw[k],bg.sy) for k in ('actual_dust_observable','balancing_map_inverse','balanced_generator','leading_dust_generator')]
    cm=maps['longitudinal_velocity_scaling_C']
    Ci=s.eye(20);Ci[13,13]=a/ell
    Oc=on(obs*bi*Ci).subs(ell,1/eps).applyfunc(s.cancel)
    Ow=on(Oc*(s.eye(20)+eps*U)*Twi)
    Os=s.Matrix(2,20,lambda i,k:s.cancel(Ow[i,k]*eps**(weights[k]-3)))
    checks.add('observation_order_three_factor',all(s.denom(z).subs(eps,0)!=0 for z in Os if z!=0))
    ebox=engine.EnclosureBox({**boxes,eps:(s.Integer(0),s.Rational(1,m))})
    ko=max(ebox.norm(Os),ebox.norm(Os.T))
    prep=common.read_json(BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json')
    hs={j:old.parent.import_matrix(prep['matrices']['comparison_lift_H'+str(j)],bg.sy) for j in range(4)}
    parent_form=common.read_json(PARENT+'formulas.json')
    q3,h4,n2=[old.parent.import_matrix(parent_form['matrices'][k],bg.sy) for k in ('wave_addition_q3','fast_addition_H4','lift_generator_N2')]
    hc={**hs,3:hs[3]+q3,4:h4}
    Jpoly=on(Oc*sum((mat*eps**j for j,mat in hc.items()),s.zeros(20,2)))
    degree=max(s.Poly(z,eps).degree() for z in Jpoly if z!=0)
    jc={j:Jpoly.applyfunc(lambda z:s.Poly(z,eps).nth(j)) for j in range(int(degree)+1)}
    exact('leading_observation_identity',shell(jc[0]-s.eye(2)))
    exact('first_observation_coefficient_zero',shell(jc.get(1,s.zeros(2))))
    init={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    d1=old.parent.import_matrix(prep['matrices']['initial_fast_mismatch'],bg.sy)
    d2=old.parent.import_matrix(prep['matrices']['initial_remainder'],sy)
    hold0=sum((mat.subs(init)*eps**j for j,mat in hs.items()),s.zeros(20,2))
    original=hold0+eps*d1.subs(init)+eps**2*d2.subs(init)
    exact('original_initial_dust_normalization',Oc.subs(init)*original-s.eye(2))
    h0c=sum((mat.subs(init)*eps**j for j,mat in hc.items()),s.zeros(20,2))
    j0c=Jpoly.subs(init)
    U0=U.subs(init);Cw0=Tw.subs(init)*(s.eye(20)-eps*U0/den.subs(init)+eps**2*U0**2/den.subs(init))
    initial_num=Cw0*(original*j0c-h0c)
    weighted_init=s.Matrix(20,2,lambda i,k:s.cancel(initial_num[i,k]/eps**weights[i]))
    checks.add('complete_corrected_initial_weighted_regular',all(s.denom(z).subs(eps,0)!=0 for z in weighted_init if z!=0))
    pointbox=engine.EnclosureBox({eps:(s.Integer(0),s.Rational(1,m))})
    initial_bound=max(pointbox.norm(weighted_init),pointbox.norm(weighted_init.T))
    cret=s.cancel(12*ko*kt*inv*initial_bound)
    progress('FULL corrected original-data bound and retained-response prefactor derived')
    formal=common.read_json(BASE+'r4c1_g3n5_observable_correction_attempt_01/formulas.json')
    nobs=old.parent.import_matrix(formal['matrices']['observable_correction_N2'],bg.sy)
    j2=jc[2];mu=s.Rational(21,10);T=s.Rational(1,20)
    exact('normalized_observable_coefficient',shell(n2+bg.dt(j2)+j2*M-M*j2-nobs))
    checks.add('leading_reference_norm',norm(M)<=mu)
    nn=norm(n2);checks.add('corrected_reference_growth',mu+nn/s.Integer(m)**2<=30)
    jp={j:norm(mat) for j,mat in jc.items() if j>=2}
    constbox=engine.EnclosureBox({})
    jp0={j:max(constbox.norm(mat.subs(init)),constbox.norm(mat.subs(init).T)) for j,mat in jc.items() if j>=2}
    initial_dev=sum(val/s.Integer(m)**j for j,val in jp0.items())
    checks.add('actual_initial_normalization_neumann',initial_dev<=s.Rational(1,2))
    kj3=sum(val/s.Integer(m)**(j-3) for j,val in jp.items() if j>=3)
    kji=sum(val/s.Integer(m)**(j-2) for j,val in jp0.items())
    kji3=sum(val/s.Integer(m)**(j-3) for j,val in jp0.items() if j>=3)
    kinverse3=kji3+2*kji*kji/m
    e_mu,e30,e_gamma=exp_upper(mu*T),exp_upper(30*T),exp_upper(gamma*T)
    f2=nn*T*e_mu;f4=nn*nn*T*T*e30/2
    kj2,kj20=jp[2],jp0[2]
    cref=s.cancel(2*kj3*e30+2*(1+kj2/m**2)*f4/m
        +(1+kj2/m**2)*(e_mu+f2/m**2)*kinverse3
        +(kj2*f2+kj2*e_mu*kj20+f2*kj20)/m+kj2*f2*kj20/m**3)
    cforced=s.Rational(parent_form['continuum']['C3'])*T*e30
    ctotal=s.cancel(cref+cforced+cret*e_gamma)
    b=s.cancel(nobs.subs(init)[0,0])
    checks.add('nonzero_blind_observable_witness',b.is_Rational and b>0,{'computed_exact':str(b)})
    exact('witness_matches_frozen_operator_not_target',b-old.parent.import_matrix(formal['matrices']['observable_N2_initial'],bg.sy)[0,0])
    knobs=norm(nobs);kndot=norm(bg.dt(nobs));kmdot=norm(bg.dt(M))
    zdd=s.cancel(((kmdot+mu*mu)*knobs*T+2*mu*knobs+kndot)*e_mu)
    witness=min(T,b/(zdd+1));lower=s.cancel(b*witness/4)
    sharp_min=max(m,int(s.ceiling(ctotal/lower)))
    checks.add('rational_witness_time',witness.is_Rational and 0<witness<=T and zdd*witness<=b)
    checks.add('explicit_total_order_two_lower_domain',ctotal/s.Integer(sharp_min)<=lower)
    checks.add('total_cubic_order_rejected_by_nonzero_second_coefficient',b!=0 and lower>0)
    sharper=common.read_json(BASE+'r4c1_g3n5_prepared_dust_sharper_attempt_01/formulas.json')
    upper=s.sympify(sharper['error_coefficient_exact'])
    checks.add('inherited_order_two_upper_positive',upper.is_real and upper>0)
    progress('Complete expansion and explicit nonzero lower-witness domain derived')
    # Independent numeric controls for the complete transformed generator;
    # no stiff high-ell trajectory is substituted for an analytic bound.
    tpoly=sum((mat*eps**j for j,mat in Tc.items()),s.zeros(20))
    kpoly=sum((mat*eps**j for j,mat in K.items()),s.zeros(20))
    principal=F/eps**2+L/eps
    bw=principal+drift+(R0+eps*R1+eps**2*R2)/den
    Cw=Tw*(s.eye(20)-eps*U/den+eps**2*U**2/den)
    Cwi=(s.eye(20)+eps*U)*Twi
    Ac=on((bg.dt(cm)+cm*Az)*Ci).subs(ell,1/eps)
    rawBw=bg.dt(Cw)*Cwi+Cw*Ac*Cwi
    numeric_mp=s.lambdify([bg.bg,eps],(tpoly,bg.dt(tpoly),kpoly,rawBw,principal+Bc,den),'mpmath',cse=True)
    energy_mp=s.lambdify([bg.bg],bg.energy,'mpmath',cse=True)
    coefficient_numeric=s.lambdify([bg.bg],(M,nobs),'numpy',cse=True)
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    matrix_controls=[]
    with mp.workdps(70):
        mpnorm=lambda mat:max(sum(abs(mat[i,j]) for j in range(mat.cols)) for i in range(mat.rows))
        for kval in (m,2*m):
            for t in (0.,.025,.05):
                point=[mp.mpf(str(z)) for z in np.polynomial.polynomial.polyval(t,bc.T)]
                # Algebraic ON-SHELL points, not projected trajectory evolution.
                # Only the identity control evaluates H from its declared shell;
                # no original data or coefficient evolution is changed.
                point[1]=mp.sqrt(mp.mpf(10)*energy_mp(point)/33)
                tn,td,kn,bn,bcn,dn=numeric_mp(point,mp.mpf(1)/kval)
                residual=float(mpnorm((bn*tn-tn*bcn-td)*dn-kn)/max(mp.mpf(1),mpnorm(kn)))
                checks.add('full_raw_generator_control_'+str(kval)+'_'+str(t),residual<=1e-30,residual,'<=1e-30; 70-digit shell control')
                matrix_controls.append(dict(ell=kval,time=t,residual=residual,precision=70,control='algebraic shell point only, no evolution projection'))
    times=np.unique(np.concatenate((np.linspace(0.,.05,257),[float(witness)])))
    def zrhs(t,y):
        vals=coefficient_numeric(np.polynomial.polynomial.polyval(t,bc.T))
        mm,nn0=np.asarray(vals[0],complex),np.asarray(vals[1],complex)
        zc=y[:8]+1j*y[8:];phi=zc[:4].reshape(2,2);zz=zc[4:].reshape(2,2)
        rhs=np.concatenate(((mm@phi).ravel(),(mm@zz+nn0@phi).ravel()))
        return np.concatenate((rhs.real,rhs.imag))
    z0=np.concatenate((np.eye(2).ravel(),np.zeros(12)))
    sols=[solve_ivp(zrhs,(0.,.05),z0,t_eval=times,method=method,rtol=rt,atol=at,max_step=.05/512) for method,rt,at in (('DOP853',1e-11,1e-13),('Radau',1e-12,1e-14))]
    checks.add('independent_observable_coefficient_integrations',all(sol.success for sol in sols))
    if not all(sol.success for sol in sols):raise RuntimeError('Coefficient solver failed')
    disagreement=float(np.max(np.sum(np.abs(sols[0].y-sols[1].y),axis=0)))
    checks.add('two_method_coefficient_agreement',disagreement<=1e-8,disagreement,'<=1e-8')
    ix=int(np.flatnonzero(times==float(witness))[0]);zw=float(sols[1].y[4,ix])
    checks.add('independent_nonzero_witness_control',zw>=float(b*witness/2)-1e-10,zw)
    arch=common.read_json(old.PARENT+'trajectories.json')
    checks.add('all_original_modes_and_four_columns_retained',sorted(x['ell'] for x in arch['modes'])==list(old.MODES) and all(np.array(x['initial_balanced']).shape==(20,4,2) for x in arch['modes']))
    checks.add('exact_nonnegative_constants',all(val.is_Rational and val>=0 for val in (inv,initial_bound,cret,gamma,cref,cforced,ctotal,lower,zdd)))
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    constants=dict(ell_retained_min=m,weighted_inverse=str(inv),weighted_transform=str(kt),weighted_initial=str(initial_bound),weighted_observation=str(ko),weighted_rate=str(gamma),retained_prefactor=str(cret),reference_remainder=str(cref),forced_remainder=str(cforced),total_expansion_remainder=str(ctotal),Z_second_derivative=str(zdd),blind_second_coefficient=str(b),witness_time=str(witness),lower_coefficient=str(lower),sharp_order_min=str(sharp_min),inherited_upper_coefficient=str(upper))
    formulas=dict(constants=constants,
        matrices={'S_wave':prior.wire(Sw),'S_fast':prior.wire(Sf),'weighted_initial_numerator':prior.wire(weighted_init),'observable_J2':prior.wire(j2)},
        weighted_transform_bounds={str(j):str(val) for j,val in tnorm.items()},weighted_numerator_bounds={str(j):str(val) for j,val in knorm.items()},
        inequalities=['||W_retained||_infinity<=C_ret eps^3 exp(gamma t)||W0||_infinity','||W_full-Phi_M W0-eps^2 Z W0||_infinity<=C_total eps^3 ||W0||_infinity','sup_[0,T]||W_full-Phi_M W0||_infinity>=c_lower eps^2 ||W0||_infinity for W0=e1, ell>=ell_sharp_min'],
        proof='Exact full-state weighted coefficient identities, Neumann inverse, inherited Q metric bounds and Q-skew principals including Qdot give retained-response control. Actual corrected-data numerator is bounded, not replaced by its limit. Exact normalized reference expansion and replayed positive Duhamel remainder give the complete expansion. Z(0)=0, Zdot(0)[0,0]=b>0 and whole-box Zdd give Z00(t_w)>=b t_w/2. At ell>=ell_sharp_min the order-three expansion remainder is <=(b t_w/4)eps^2. Inherited leading order-two upper bound and this nonzero prepared column prove uniform mathematical sharp order two.',
        domain='Registered linear rotating B1 shell only, 0<=t<=1/20, nonzero ell; separate ell_retained_min/ell_sharp_min. These are sufficient mathematical thresholds, NOT physical cutoffs or accessible EFT bands.',
        practical_accuracy_proved=False,physical_window_proved=False)
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(dict(matrix_controls=matrix_controls,coefficient_solver_disagreement=disagreement,numerical_witness=zw,sharp_threshold_digits=len(str(sharp_min)),weighted_rate_display=float(gamma),original_five_modes_preserved=True,new_original_trajectory_runs=False))}
    summary=dict(schema='r4c1-g3n5-dust-actual-order-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='MATHEMATICAL_ORDER_TWO_CHECKED_USEFUL_DOMAIN_OPEN' if ok else 'ACTUAL_ORDER_NOT_VERIFIED',mathematical_asymptotic_order=2 if ok else 'NOT_PROVED',full_retained_response_bound_proved=ok,complete_original_error_expansion_proved=ok,full_dust_milestone_complete=False,useful_finite_mode_accuracy_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={name:common.sha(body) for name,body in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__,mpmath=mp.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary

def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_actual_order_attempt_01')
    ap.add_argument('--replay');ap.add_argument('--progress-file');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.progress_file and not args.replay:
        path=(ROOT/args.progress_file).resolve();path.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS=path.open('x',encoding='utf-8')
    try:bodies,summary=calculate()
    except BaseException:
        if PROGRESS is not None:traceback.print_exc(file=PROGRESS);PROGRESS.flush()
        raise
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'status':summary['status'],'physics_pass':False}))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    if PROGRESS is not None:PROGRESS.close()
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
