"""Corrected dust reference plus full retained response and controlled remainder."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
from scipy.integrate import solve_ivp
import scipy
import sympy as s

ROOT=Path(__file__).resolve().parents[2];BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V4_CONTRACT_2026-10-12.md'
PARENT=BASE+'r4c1_g3n5_prepared_dust_sharper_attempt_01/'
FORMAL=BASE+'r4c1_g3n5_observable_correction_attempt_01/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_error_v1.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='1a9e162f5985c8f2a7ee00ffc6eea227106bcf49afb238fd7dbaa55202096748':raise RuntimeError('Frozen engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_prepared_dust_error_v1 as prior
old=prior.old;common=prior.common;PROGRESS=None

class EnclosureBox(old.RationalBox):
    """Same exact interval arithmetic, without global complex expansion."""
    def absolute(self,value):
        re,im=value.as_real_imag(deep=True)
        bounds=[self.evaluate(part) for part in (re,im)]
        return sum(max(abs(lo),abs(hi)) for lo,hi in bounds)

def progress(message):
    print(message,flush=True)
    if PROGRESS is not None:PROGRESS.write(message+'\n');PROGRESS.flush()

def calculate():
    ps=common.read_json(PARENT+'summary.json');fs=common.read_json(FORMAL+'summary.json')
    pins=dict(ps['source_sha256']);pins.update(fs['source_sha256'])
    for folder,data,digest in ((PARENT,ps,'34d6f2504c82bf3264fd4625947fa66dc28f533c5c3501115e492898175f22e8'),(FORMAL,fs,'105fb82583080699e300027737e2e6c117827ba4b273b2d03494f099d0491cbc')):
        pins.update({folder+k:v for k,v in data['artifacts'].items()});pins[folder+'summary.json']=digest
    retained_failure=('Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v1.py',
        'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_CONTRACT_2026-10-12.md',
        BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_01/interruption.json',
        'Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v2.py',
        'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V2_CONTRACT_2026-10-12.md',
        BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_02/interruption.json',
        'Analysis/MasterTests/test_01_r4c1_g3n5_corrected_dust_remainder_v3.py',
        'Theory/Gates/RES-001/RES001_R4C1_G3N5_CORRECTED_DUST_REMAINDER_V3_CONTRACT_2026-10-12.md',
        BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_03/interruption.json')
    for rel in (CONTRACT,SELF,*retained_failure):pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;eps=s.Symbol('eps',positive=True)
    on=lambda mat:mat.applyfunc(s.cancel)
    shell=lambda mat:mat.applyfunc(lambda val:bg.constraint_reduce_scalar(val) if val!=0 else s.Integer(0))
    exact=lambda name,mat:old.parent.exact(checks,name,on(mat) if isinstance(mat,s.MatrixBase) else s.cancel(mat))
    checks.add('parents_bounded_and_formal_not_complete',ps['passed']==ps['total']==73 and fs['passed']==fs['total']==29 and ps['prepared_error_upper_bound_proved'] and fs['formal_observable_correction_checked'] and not fs['corrected_system_remainder_proved'])
    tt=s.Symbol('sign_test_t',real=True);ee=s.exp(tt)-1
    exact('positive_forcing_scalar_regression',s.diff(ee,tt)-ee-1)
    checks.add('negative_forcing_scalar_rejected',s.simplify(s.diff(ee,tt)-ee+1)!=0)
    generic=lambda name:s.Matrix(2,2,lambda i,j:s.Symbol(f'{name}_{i}_{j}'))
    aa,hh,hd,mc0,pphi,er=[generic(name) for name in ('regA','regH','regHdot','regM','regPhi','regE')]
    regR=aa*hh-hd-hh*mc0
    exact('positive_forcing_matrix_decomposition',aa*(hh*pphi+er)-(hd*pphi+hh*mc0*pphi+aa*er+regR*pphi))
    checks.add('negative_forcing_matrix_rejected',any(val!=0 for val in on(aa*(hh*pphi+er)-(hd*pphi+hh*mc0*pphi+aa*er-regR*pphi))))
    raw=common.read_json(old.PARENT+'matrices.json')
    az,bi,obs,mm,qfields=[old.parent.import_matrix(raw[k],bg.sy) for k in ('balanced_generator','balancing_map_inverse','actual_dust_observable','leading_dust_generator','full_field_reconstruction')]
    uniform=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    maps=common.read_json(uniform['general_exact_maps_source'])['matrices']
    cm,um,tw,twi,lw=[old.parent.import_matrix(maps[k],bg.sy) for k in ('longitudinal_velocity_scaling_C','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi','ordinary_wave_principal_L')]
    ci=s.eye(20);ci[13,13]=a/ell;ac=on((bg.dt(cm)+cm*az)*ci);oc=on(obs*bi*ci)
    blocks={}
    for i in range(20):
        for j in range(20):
            for term in s.Add.make_args(s.expand(ac[i,j])):
                power=term.as_powers_dict().get(ell,s.Integer(0));val=s.cancel(term/ell**power)
                if not power.is_Integer or ell in val.free_symbols:raise ValueError('Not Laurent')
                blocks.setdefault(int(power),s.zeros(20))[i,j]+=val
    exact('full_generator_Laurent',ac-sum((mat*ell**power for power,mat in blocks.items()),s.zeros(20)))
    prep=common.read_json(BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/formulas.json')
    hs={j:old.parent.import_matrix(prep['matrices']['comparison_lift_H'+str(j)],bg.sy) for j in range(4)}
    stored=common.read_json(PARENT+'formulas.json')
    rs={j:old.parent.import_matrix(stored['matrices']['exact_source_R'+str(j)],bg.sy) for j in range(2,6)}
    formal=common.read_json(FORMAL+'formulas.json')
    n2=old.parent.import_matrix(formal['matrices']['lift_correction_N2'],bg.sy)
    nobs=old.parent.import_matrix(formal['matrices']['observable_correction_N2'],bg.sy)
    fi=s.zeros(20);fi[9,19]=-33*a*a/5;fi[19,9]=a*a
    pw=s.eye(20)
    for ix in (3,13,9,19):pw[ix,ix]=0
    r2c=shell(on(rs[2]-hs[0]*n2));rw=on(tw*r2c)
    wf=s.zeros(20,2)
    for pos,vel,c2 in ((0,10,s.Rational(1,3)),(1,11,1),(2,12,1),(4,14,s.Rational(4,5)),(5,15,s.Rational(4,5)),(8,18,1)):
        wf[pos,:]=a*rw[vel,:]/c2;wf[vel,:]=-a*rw[pos,:]
    pp=s.eye(2)+s.Matrix([v,-u])*s.Matrix([[v,-u]])/13
    wf[6:8,:]=on(a*pp.inv()*rw[16:18,:]);wf[16:18,:]=-a*rw[6:8,:]
    exact('ordinary_wave_inverse_correction',lw*wf+pw*rw)
    q3=on(twi*wf);f4=on(-fi*shell(on(r2c+blocks[1]*q3)))
    exact('wave_addition_keeps_lower_orders',blocks[2]*q3)
    exact('complete_order_two_cancellation',shell(on(r2c+blocks[1]*q3+blocks[2]*f4)))
    corrected={**hs,3:on(hs[3]+q3),4:f4}
    progress('Complete first-correction lift derived from stored exact R2; all wave/fast states retained')
    dq3,df4=bg.dt(q3),bg.dt(f4)
    progress('Exact factored correction derivatives computed once; no global fraction cancellation')
    # Exact coefficient updates. Preserve their factorization so no giant
    # full-momentum fraction is required for proof or interval enclosures.
    rc={
        3:rs[3]+blocks[0]*q3+blocks[1]*f4-dq3-q3*mm-hs[1]*n2,
        4:rs[4]+blocks[-1]*q3+blocks[0]*f4-df4-f4*mm-hs[2]*n2,
        5:rs[5]+blocks[-2]*q3+blocks[-1]*f4-corrected[3]*n2,
        6:blocks[-2]*f4-f4*n2}
    additions={3:q3,4:f4}
    for j in range(3,7):
        update=(rs[j] if j in rs else s.zeros(20,2))+sum((mat*additions[d+j] for d,mat in blocks.items() if d+j in additions),s.zeros(20,2))
        if j in additions:update-={3:dq3,4:df4}[j]+additions[j]*mm
        if j-2 in corrected:update-=corrected[j-2]*n2
        exact('complete_source_coefficient_update_'+str(j),rc[j]-update)
        progress('Exact complete residual coefficient '+str(j)+' verified')
    checks.add('omitted_correction_drift_rejected',any(val!=0 for val in dq3) or any(val!=0 for val in df4))
    boxes={bg.sy[k]:(s.sympify(val[0]),s.sympify(val[1])) for k,val in uniform['background_boxes'].items()}
    bx=EnclosureBox(boxes);nrm=lambda mat:max(bx.norm(mat),bx.norm(mat.T))
    for label,value in (('real',a/H),('imaginary',s.I*a/H),('mixed',(2+s.I)*a/H)):
        re,im=value.as_real_imag(deep=True)
        exact('factored_decomposition_'+label,re+s.I*im-value)
        checks.add('factored_nonnegative_'+label,bx.absolute(value)>=0)
    badbox=EnclosureBox({a:(s.Integer(-1),s.Integer(1))})
    rejected=False
    try:badbox.absolute(1/a)
    except ZeroDivisionError:rejected=True
    checks.add('factored_zero_denominator_rejected',rejected)
    toy=(2+s.I)*(a*a-H*H)/(a*H)
    toy_dot=bg.dt(s.Matrix([toy]))[0]
    ad,hd=bg.rates[:2,0]
    exact('factored_background_derivative_quotient_rule',toy_dot-(2+s.I)*(ad/H-a*hd/H**2-hd/a+H*ad/a**2))
    checks.add('factored_derivative_bound_exact_rational',bx.absolute(toy_dot).is_Rational and bx.absolute(toy_dot)>=0)
    an={j:nrm(mat) for j,mat in blocks.items()};hn={j:nrm(mat) for j,mat in hs.items()}
    progress('Generator and original-lift interval norms derived')
    qn,fn,qd,fd,nn=[nrm(mat) for mat in (q3,f4,dq3,df4,n2)]
    progress('Correction and factored-derivative whole-interval norms derived')
    mu=s.Rational(21,10);checks.add('leading_reference_norm',nrm(mm)<=mu)
    rn={3:nrm(rs[3])+an[0]*qn+an[1]*fn+qd+qn*mu+hn[1]*nn,
        4:nrm(rs[4])+an[-1]*qn+an[0]*fn+fd+fn*mu+hn[2]*nn,
        5:nrm(rs[5])+an[-2]*qn+an[-1]*fn+(hn[3]+qn)*nn,
        6:(an[-2]+nn)*fn}
    ks=lambda kval:sum(rn[j]/s.Integer(kval)**(j-3) for j in rn)
    hc=sum((mat/ell**j for j,mat in corrected.items()),s.zeros(20,2))
    rh=sum((mat/ell**j for j,mat in rc.items()),s.zeros(20,2))
    mc=mm+n2/ell**2
    je=on(oc*hc).subs(ell,1/eps).applyfunc(s.cancel)
    j2=je.applyfunc(lambda val:s.diff(val,eps,2).subs(eps,0)/2)
    exact('same_first_observable_correction',shell(on(n2+bg.dt(j2)+j2*mm-mm*j2-nobs)))
    init={a:1,H:s.sqrt(s.Rational(3469,4620)),u:1,ud:0,v:0,vd:1,r:1,rd:s.Rational(1,4),pd:s.Rational(1,5),rho:s.Rational(1,5),C:1}
    ji=on(je.subs(init));jdiff=on(ji-s.eye(2))
    degree=max(s.Poly(val,eps).degree() for val in jdiff if val!=0)
    constantbox=EnclosureBox({})
    initial_coeff={j:max(constantbox.norm(jdiff.applyfunc(lambda val:s.Poly(val,eps).nth(j))),constantbox.norm(jdiff.applyfunc(lambda val:s.Poly(val,eps).nth(j)).T)) for j in range(1,int(degree)+1)}
    jdev=lambda kval:sum(val/s.Integer(kval)**j for j,val in initial_coeff.items())
    emin=4
    while jdev(emin)>s.Rational(1,2) or mu+nn/s.Integer(emin)**2>30:emin+=1
    checks.add('derived_continuum_initial_inverse',jdev(emin)<=s.Rational(1,2),{'ell_min':emin,'initial_deviation_bound':str(jdev(emin))})
    checks.add('reference_continuum_growth_bound',mu+nn/s.Integer(emin)**2<=30)
    ub,u2b,twb=[nrm(mat) for mat in (um,on(um*um),tw)]
    def kw(kval):return s.Rational(3,2)*twb*(1+ub/s.Integer(kval)+u2b/s.Integer(kval)**2)
    ow=on(oc*(s.eye(20)+um/ell)*twi).subs(ell,1/eps).applyfunc(s.cancel)
    def ko(kval,point=False):
        bbox=EnclosureBox({**boxes,eps:(s.Rational(1,kval),s.Rational(1,kval)) if point else (s.Integer(0),s.Rational(1,kval))})
        return 3*max(bbox.norm(ow),bbox.norm(ow.T))
    coeff_cont=s.cancel(3*ko(emin)*kw(emin)*ks(emin))
    # The factor 3 = infinity conversion <=3/2 times J(0)^-1 <=2.
    progress('Whole-interval source bounds and continuum inverse domain derived: ell>='+str(emin))
    epssy={**bg.sy,'eps':eps}
    delta1=old.parent.import_matrix(prep['matrices']['initial_fast_mismatch'],epssy)
    delta2=old.parent.import_matrix(prep['matrices']['initial_remainder'],epssy)
    eorig=sum((mat.subs(init)/ell**j for j,mat in hs.items()),s.zeros(20,2))+delta1/ell+delta2.subs(eps,1/ell)/ell**2
    ar=common.read_json(old.PARENT+'trajectories.json');times=np.asarray(ar['time'],float)
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    numeric=s.lambdify([bg.bg,ell],(ac,oc,hc,rh,mc,cm,qfields*bi,bg.dt(hc),mm),'numpy',cse=True)
    bvalues=np.polynomial.polynomial.polyval(times,bc.T).T
    modes=[];point_constants={};T=s.Rational(1,20)
    for item in ar['modes']:
        kval=item['ell'];j0=on(ji.subs(eps,s.Rational(1,kval)))
        checks.add('registered_initial_inverse_'+str(kval),j0.det()!=0,{'determinant':str(s.cancel(j0.det()))})
        if j0.det()==0:
            modes.append(dict(ell=kval,domain='SINGULAR_COMPARISON_CHART_ORIGINAL_DATA_RETAINED'));continue
        j0inv=on(j0.inv());invbound=max(constantbox.norm(j0inv),constantbox.norm(j0inv.T))
        lam=mu+nn/s.Integer(kval)**2;growth=max(s.Integer(30),lam)
        c3=s.cancel(s.Rational(3,2)*ko(kval,True)*kw(kval)*ks(kval)*invbound)
        point_constants[str(kval)]={k:str(val) for k,val in dict(J0_inverse=invbound,K_source=ks(kval),K_observation=ko(kval,True),K_to_w=kw(kval),reference_rate=lam,remainder_rate=growth,C3=c3).items()}
        jn=np.array(j0inv.tolist(),complex);ei=np.array(on(eorig.subs(ell,kval)).tolist(),complex)
        val0=[np.asarray(val,complex) for val in numeric(bvalues[0],kval)]
        e0ref=val0[2]@jn;delt=ei-e0ref
        z0=prior.complex_array(item['initial_balanced'])
        checks.add('original_initial_data_'+str(kval),float(np.linalg.norm(val0[5]@z0[:,:2]-ei,np.inf))<=1e-10)
        def rhs(t,yy):
            bval=np.polynomial.polynomial.polyval(t,bc.T)
            aa,oo,hh,rr,mn,*_=numeric(bval,kval)
            phi=yy[:4].reshape(2,2);ret=yy[4:44].reshape(20,2);forced=yy[44:].reshape(20,2)
            return np.concatenate(((mn@phi).ravel(),(aa@ret).ravel(),(aa@forced+rr@phi@jn).ravel()))
        y0=np.concatenate((np.eye(2,dtype=complex).ravel(),delt.ravel(),np.zeros(40,dtype=complex)))
        sols=[solve_ivp(rhs,(0.,.05),y0,method='DOP853',t_eval=times,rtol=rt,atol=at,max_step=step) for rt,at,step in ((1e-12,1e-14,.05/512),(1e-13,1e-15,.05/1024))]
        checks.add('complete_coupled_control_solvers_'+str(kval),all(sol.success and sol.y.shape==(84,len(times)) for sol in sols),[sol.message for sol in sols])
        if not all(sol.success and sol.y.shape==(84,len(times)) for sol in sols):raise RuntimeError('Control solver failed; do not adopt this certificate')
        pair=float(np.max(np.sum(np.abs(sols[0].y-sols[1].y),axis=0)/np.maximum(1.,np.sum(np.abs(sols[1].y),axis=0))))
        checks.add('independent_solver_refinement_'+str(kval),pair<=1e-8,pair,'<=1e-8')
        mf=mo=md=ms=mr=mforced=0.;violation=0.
        for ix,t in enumerate(times):
            aa,oo,hh,rr,mn,cc,qq,hd,_=[np.asarray(val,complex) for val in numeric(bvalues[ix],kval)]
            zz=prior.complex_array(item['balanced'][ix]);ff=prior.complex_array(item['full_fields'][ix]);ww=prior.complex_array(item['dust_observables'][ix])
            mf=max(mf,float(np.linalg.norm(qq@zz-ff,np.inf)/max(1.,np.linalg.norm(ff,np.inf))))
            mo=max(mo,float(np.linalg.norm(oo@cc@zz-ww,np.inf)/max(1.,np.linalg.norm(ww,np.inf))))
            yy=sols[1].y[:,ix];phi=yy[:4].reshape(2,2);ret=yy[4:44].reshape(20,2);forced=yy[44:].reshape(20,2)
            full=hh@phi@jn+ret+forced;original=cc@zz[:,:2]
            md=max(md,float(np.linalg.norm(full-original,np.inf)/max(1.,np.linalg.norm(original,np.inf))))
            fields=qq@np.linalg.solve(cc,full)
            ms=max(ms,float(np.linalg.norm(fields-ff[:,:2],np.inf)/max(1.,np.linalg.norm(ff[:,:2],np.inf))))
            error=float(np.linalg.norm(oo@forced,np.inf));mforced=max(mforced,error)
            bound=float(c3*s.Rational(str(t))*s.exp(growth*s.Rational(str(t)))/kval**3)
            violation=max(violation,error-bound-1e-8*(1+abs(bound)))
            if ix in (0,len(times)//2,len(times)-1):
                direct=aa@hh-hd-hh@mn
                mr=max(mr,float(np.linalg.norm(direct-rr,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
                allowed=float(ks(kval)/kval**3)
                checks.add('source_majorant_'+str(kval)+'_'+str(ix),float(np.linalg.norm(direct,2))<=allowed+1e-9*(1+allowed))
        for name,value,limit in (('all_four_column_22_fields_unchanged',mf,1e-10),('actual_observable_unchanged',mo,1e-10),('full_retained_forced_decomposition',md,1e-8),('all_22_prepared_fields_decomposition',ms,1e-8),('direct_source_update_identity',mr,1e-9),('controlled_observable_remainder',violation,0.)):
            checks.add(name+'_'+str(kval),value<=limit,value,'<='+str(limit))
        modes.append(dict(ell=kval,domain='CONTINUUM_AND_POINT' if kval>=emin else 'SEPARATE_EXACT_POINT_INVERSE',initial_inverse_bound=str(invbound),remainder_max=mforced,remainder_endpoint_display=float(c3*T*s.exp(growth*T)/kval**3),state_decomposition_residual=md,prepared_fields_residual=ms,source_identity=mr,solver_disagreement=pair,archive_fields_residual=mf,archive_observable_residual=mo))
        progress('Full retained/forced control completed for original ell='+str(kval))
    checks.add('all_five_modes_four_original_columns',sorted(item['ell'] for item in modes)==list(old.MODES) and all(np.array(item['initial_balanced']).shape==(20,4,2) for item in ar['modes']))
    checks.add('exact_nonnegative_constants',all(val.is_Rational and val>=0 for val in (nn,coeff_cont,*rn.values())))
    exported={name:prior.wire(mat) for name,mat in dict(wave_addition_q3=q3,fast_addition_H4=f4,corrected_H3=corrected[3],lift_generator_N2=n2).items()}
    for name,obj in exported.items():exact('roundtrip_'+name,old.parent.import_matrix(obj,bg.sy)-dict(wave_addition_q3=q3,fast_addition_H4=f4,corrected_H3=corrected[3],lift_generator_N2=n2)[name])
    checks.add('pins_after',common.inspect_pins(pins)==absent);checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    formulas=dict(matrices=exported,source_coefficient_bounds={str(j):str(val) for j,val in rn.items()},point_constants=point_constants,continuum=dict(ell_min=emin,C3=str(coeff_cont),inequality='||W_full-W_ref-W_retained||_infinity<=C3*t*exp(30*t)*||W0||_infinity/ell^3',initial_inverse_bound='2',domain='registered rotating B1 shell, 0<=t<=1/20, ell>=ell_min, a,C,rho_m>0, J=1'),definition='W_ref=J(t) Phi_(M+N2/ell^2) J(0)^-1 W0; W_retained=O_c Gamma_c [E_orig-H(0)J(0)^-1]W0; full coupled forced remainder retained',proof='Complete order-two cancellation; exact R3-R6 updates; rational interval source norms. Parent full w propagator <=exp(30 dt), x_c->w and w->actual-observation bounds, initial normalization inverse and corrected 2-state reference norm bound give the Duhamel integral inequality. The retained homogeneous response is not discarded or claimed small.',scope='Controlled first-correction remainder AFTER full original mismatch response; not sharp order or useful accuracy of a closed dust law')
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(dict(modes=modes,full_actual_order='NOT_PROVED',retained_response_not_discarded=True,physical_window_proved=False,precision='Exact identities/interval constants, independent paired full-coupled DOP853 controls; no new physical initial data'))}
    summary=dict(schema='r4c1-g3n5-corrected-dust-remainder-v4',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='CORRECTED_REFERENCE_REMAINDER_CHECKED_ACTUAL_ORDER_OPEN' if ok else 'CORRECTED_REFERENCE_REMAINDER_NOT_VERIFIED',corrected_reference_forced_remainder_proved=ok,controlled_remainder_upper_order=3 if ok else 'NOT_PROVED',retained_original_response=True,full_dust_convergence_order='SHARP_ORDER_NOT_PROVED',full_prepared_high_p_remainder_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={name:common.sha(body) for name,body in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'});bodies['summary.json']=common.encode(summary)
    return bodies,summary

def main():
    global PROGRESS
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_corrected_dust_remainder_attempt_04');ap.add_argument('--replay');ap.add_argument('--progress-file');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.progress_file and not args.replay:
        path=(ROOT/args.progress_file).resolve();path.relative_to((ROOT/'.local/itsm-context').resolve());PROGRESS=path.open('x',encoding='utf-8')
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
