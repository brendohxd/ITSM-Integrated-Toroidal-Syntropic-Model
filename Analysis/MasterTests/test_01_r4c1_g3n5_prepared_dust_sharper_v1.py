"""Compressed-energy prepared-dust upper bound; sharp order remains open."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_SHARPER_DUST_BOUND_CONTRACT_2026-10-11.md'
PARENT=BASE+'r4c1_g3n5_prepared_dust_error_attempt_01/'
FINITE=BASE+'r4c1_g3n5_prepared_finite_constants_attempt_01/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_prepared_dust_error_v1.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='1a9e162f5985c8f2a7ee00ffc6eea227106bcf49afb238fd7dbaa55202096748':
    raise RuntimeError('Frozen prepared engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_prepared_dust_error_v1 as prior
old=prior.old
common=prior.common

def progress(message): print(message,flush=True)

def calculate():
    ps=common.read_json(PARENT+'summary.json')
    fs=common.read_json(FINITE+'summary.json')
    pins=dict(fs['source_sha256'])
    pins.update({FINITE+k:v for k,v in fs['artifacts'].items()})
    pins[FINITE+'summary.json']='7d0f2235bbd2d419ae3457b5dfc591c755c1d548584329d3f5dd1e259378cd03'
    for rel in (CONTRACT,SELF): pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists())
    before=old.parent.snapshot(paths)
    checks=common.Checks()
    bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
    ell=bg.ell
    on=lambda mat: mat.applyfunc(s.cancel)
    shell=lambda mat: mat.applyfunc(lambda z: bg.constraint_reduce_scalar(z) if z!=0 else s.Integer(0))
    exact=lambda name,mat: old.parent.exact(checks,name,on(mat) if isinstance(mat,s.MatrixBase) else s.cancel(mat))
    checks.add('prepared_parent_verified_upper_only',ps['passed']==ps['total']==67 and ps['prepared_error_upper_bound_proved'] and not ps['full_prepared_high_p_remainder_proved'])
    checks.add('finite_parent_verified',fs['passed']==fs['total']==7 and not fs['physics_pass'])
    uniform=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    fast=common.read_json(BASE+'r4c1_g3n5_dust_fast_transfer_attempt_01/formulas.json')
    prepared=common.read_json(PARENT+'formulas.json')
    original=common.read_json(uniform['general_exact_maps_source'])['matrices']
    maps={k:old.parent.import_matrix(val,bg.sy) for k,val in original.items()}
    f,l,q,drift,cm,um,tw,twi=[maps[k] for k in ('dispersive_principal_F','ordinary_wave_principal_L','positive_evolution_Q','wave_drift','longitudinal_velocity_scaling_C','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi')]
    vs=[maps['residual_numerator_'+str(j)] for j in range(6)]
    vm=old.parent.import_matrix(fast['matrices']['second_fast_map_V'],bg.sy)
    pf=s.zeros(20);pf[9,9]=pf[19,19]=1
    po=s.eye(20)-pf
    diag=lambda mat: pf*mat*pf+po*mat*po
    off=lambda mat: pf*mat*po+po*mat*pf
    b0=on(drift+vs[0]);bd=diag(b0);bof=off(b0)
    for name,mat in (('Q_partition',q*pf-pf*q),('Q_dot_partition',bg.dt(q)*pf-pf*bg.dt(q)),('F_partition',f*pf-pf*f),('L_partition',l*pf-pf*l),('F_Q_skew',q*f+f.conjugate().T*q),('L_Q_skew',q*l+l.conjugate().T*q),('V_off_only',diag(vm)),('fast_cross_cancellation',f*vm-vm*f+bof)):
        exact(name,mat)
    comm=on(l*vm-vm*l)
    h2=on(b0*vm-vm*bd-bg.dt(vm))
    exact('ordinary_commutator_off_only',diag(comm))
    exact('value_drift_diagonal_is_cross_product',diag(h2)-bof*vm)
    checks.add('omitted_V_dot_rejected',any(x!=0 for x in bg.dt(vm)))
    checks.add('omitted_fast_cross_rejected',any(x!=0 for x in comm)+any(x!=0 for x in bof)>0)
    g=-22*a*a/375
    rem=[vs[1],on(vs[2]+g*vs[0]),*vs[3:]]
    rb=sum((mat/ell**(j+1) for j,mat in enumerate(rem)),s.zeros(20))/(1-g/ell**2)
    aw=ell**2*f+ell*l+b0+rb
    a0=ell**2*f+ell*l+bd
    tt=s.eye(20)+vm/ell**2
    residual=comm/ell+h2/ell**2+rb*tt
    delta_rhs=comm/ell+h2/ell**2+(rb*vm-vm*rb)/ell**2
    exact('full_second_generator_factored',aw*tt-tt*a0-bg.dt(tt)-residual)
    exact('diagonal_perturbation_factored',residual-tt*rb-delta_rhs)
    energy=bg.dt(q)+q*(b0+rb)+(b0+rb).conjugate().T*q
    compressed=bg.dt(q)+q*diag(b0+rb)+diag(b0+rb).conjugate().T*q
    exact('compressed_full_energy_identity',compressed-diag(energy))
    checks.add('inherited_energy_mu_below_60',s.sympify(uniform['mu_exact'])<60)
    boxes={bg.sy[k]:(s.sympify(val[0]),s.sympify(val[1])) for k,val in uniform['background_boxes'].items()}
    bx=old.RationalBox(boxes)
    n2=lambda mat: max(bx.norm(mat),bx.norm(mat.T))
    emin=15
    vb=n2(vm);vq=3*vb;rstar=vq/s.Integer(emin)**2
    checks.add('same_derived_inverse_domain',s.Integer(emin)**2>=6*vb and rstar<1,{'ell_min':emin,'r_upper':str(rstar)})
    checks.add('Q_norm_conversion_bound',s.Rational(9,8)/(s.Rational(5,33))<9)
    cq=3*n2(comm);hdq=3*n2(diag(h2));hoq=3*n2(off(h2))
    krd=3*sum(n2(diag(mat))/s.Integer(emin)**j for j,mat in enumerate(rem))
    kro=3*sum(n2(off(mat))/s.Integer(emin)**j for j,mat in enumerate(rem))
    denom=1-rstar**2
    delta=s.cancel((hdq+(2*kro*vq+vq*cq)/emin+vq*hoq/s.Integer(emin)**2+2*krd*vq**2/s.Integer(emin)**3)/(s.Integer(emin)**2*denom))
    kappa=s.cancel((cq+kro+hoq/emin+2*vq*krd/s.Integer(emin)**2+vq*hdq/s.Integer(emin)**3+vq**2*kro/s.Integer(emin)**4)/denom)
    gamma=30+delta
    progress('Compressed diagonal energy and even/odd inverse bounds derived')
    raw=common.read_json(old.PARENT+'matrices.json')
    az,bi,obs,mm,qfields=[old.parent.import_matrix(raw[k],bg.sy) for k in ('balanced_generator','balancing_map_inverse','actual_dust_observable','leading_dust_generator','full_field_reconstruction')]
    ci=s.eye(20);ci[13,13]=a/ell
    ac=on((bg.dt(cm)+cm*az)*ci)
    oc=on(obs*bi*ci)
    coeffs={}
    for i in range(20):
        for j in range(20):
            for term in s.Add.make_args(s.expand(ac[i,j])):
                power=term.as_powers_dict().get(ell,s.Integer(0));val=s.cancel(term/ell**power)
                if not power.is_Integer or ell in val.free_symbols: raise ValueError('Not Laurent')
                coeffs.setdefault(int(power),s.zeros(20))[i,j]+=val
    exact('full_generator_Laurent_identity',ac-sum((mat*ell**d for d,mat in coeffs.items()),s.zeros(20)))
    lifts={j:old.parent.import_matrix(prepared['matrices']['comparison_lift_H'+str(j)],bg.sy) for j in range(4)}
    dots={j:bg.dt(mat) for j,mat in lifts.items()}
    def source(power):
        val=sum((mat*lifts[d-power] for d,mat in coeffs.items() if d-power in lifts),s.zeros(20,2))
        if -power in lifts: val-=dots[-power]+lifts[-power]*mm
        return on(val)
    for power in (2,1,0,-1): exact('retained_lift_low_residual_'+str(power),shell(source(power)))
    rs={j:shell(source(-j)) for j in range(2,6)}
    rn={j:n2(mat) for j,mat in rs.items()}
    def source_bound(k): return sum(rn[j]/s.Integer(k)**(j-2) for j in rn)
    ks=source_bound(emin)
    checks.add('omitted_residual_source_rejected',any(x!=0 for x in rs[2]))
    hc=sum((mat/ell**j for j,mat in lifts.items()),s.zeros(20,2))
    rh=sum((mat/ell**j for j,mat in rs.items()),s.zeros(20,2))
    exact('retained_source_complete_on_shell',shell(on(ac*hc-bg.dt(hc)-hc*mm-rh)))
    progress('Exact complete residual coefficients bounded on the preserved shell')
    pc={k:s.sympify(val) for k,val in prepared['constants'].items()}
    ko,kof,kw,co,cf,kho=[pc[k] for k in ('K_O','K_Of','K_W','C_other','C_fast','K_observation')]
    def high_bound(t):
        return s.Rational(3,2)*(ko*(3*s.exp(30*t)*(co+2*kw*ks*t)+3*kappa*t*s.exp(gamma*t)*cf)+3*kof*s.exp(30*t)*cf+kho*s.exp(s.Rational(21,10)*t))
    T=s.Rational(1,20);c2=high_bound(T)
    low={row['ell']:row for row in common.read_json(FINITE+'finite_bounds.json')['finite_mode_bounds']}
    progress('Prepared upper coefficient display '+str(float(c2))+'; diagonal exponent '+str(float(gamma)))
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    ar=common.read_json(old.PARENT+'trajectories.json');phi=np.asarray(ar['leading_Phi'],complex)
    checks.add('original_reference_shape',phi.shape==(len(ar['time']),2,2))
    fn=s.lambdify([bg.bg,ell],(vm,bg.dt(vm),aw,f,l,bd,residual,rb,q,cm,um,tw,twi,oc,ci,hc,bg.dt(hc),ac,mm,qfields*bi,rh),'numpy',cse=True)
    qdotfn=s.lambdify([bg.bg],bg.dt(q),'numpy',cse=True)
    modes=[]
    for item in ar['modes']:
        kval=item['ell'];mf=mo=me=mg=ms=md=mc=men=0.;mv=msource=coupling_max=0.
        for ix,t in enumerate(ar['time']):
            bval=np.polynomial.polynomial.polyval(t,bc.T)
            vv,vvd,aa,ff,ll,bb,rr,rbn,qn,cc,uu,twn,twin,oo,cin,hh,hd,acn,mn,qfn,rhn=[np.asarray(val,complex) for val in fn(bval,kval)]
            z=prior.complex_array(item['balanced'][ix]);w=oo@np.linalg.inv(cin)@z
            oldw=prior.complex_array(item['dust_observables'][ix]);af=prior.complex_array(item['full_fields'][ix])
            mo=max(mo,float(np.linalg.norm(w-oldw,np.inf)/max(1.,np.linalg.norm(oldw,np.inf))))
            mf=max(mf,float(np.linalg.norm(qfn@z-af,np.inf)/max(1.,np.linalg.norm(af,np.inf))))
            err=float(np.linalg.norm(w[:,:2]-phi[ix],np.inf));me=max(me,err)
            tr=s.Rational(str(t))
            if kval>=emin:
                bound=float(high_bound(tr)/kval**2)
            else:
                # Retain the previously certified full-propagator low-mode
                # inequality; this is not a use of T2 outside its domain.
                kd=s.sympify(low[kval]['initial_remainder_constant'])
                kow=s.sympify(low[kval]['observation_constant'])
                bound=float(s.Rational(3,2)*(kow*pc['K_W_low']*s.exp(30*tr)*(pc['K_initial_fast']/kval+(kd+pc['K_source_low']*tr)/kval**2)+pc['K_observation_low']*s.exp(s.Rational(21,10)*tr)/kval**2))
            mv=max(mv,err-bound-1e-9*(1+abs(bound)))
            if ix not in (0,len(ar['time'])//2,len(ar['time'])-1): continue
            direct=acn@hh-hd-hh@mn
            ms=max(ms,float(np.linalg.norm(direct-rhn,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
            allowed=float(source_bound(kval)/kval**2)
            actual_source=float(np.linalg.norm(direct,2))
            mc=max(mc,actual_source/allowed if allowed>0 else 0.)
            msource=max(msource,actual_source-allowed-1e-9*(1+allowed))
            if kval<emin: continue
            pn=np.diag([1. if i in (9,19) else 0. for i in range(20)]);pon=np.eye(20)-pn
            dmat=lambda mat: pn@mat@pn+pon@mat@pon
            omat=lambda mat: mat-dmat(mat)
            t2=np.eye(20)+vv/kval**2;t2i=np.linalg.inv(t2)
            ay=t2i@(aa@t2-vvd/kval**2)
            factored=kval*kval*ff+kval*ll+bb+t2i@rr
            mg=max(mg,float(np.linalg.norm(ay-factored,np.inf)/max(1.,np.linalg.norm(ay,np.inf))))
            eig,vec=np.linalg.eigh(qn);sq=(vec*np.sqrt(eig))@vec.conjugate().T;si=(vec/np.sqrt(eig))@vec.conjugate().T
            md=max(md,float(np.linalg.norm(sq@(dmat(ay)-dmat(aa))@si,2)))
            mcoupling=float(np.linalg.norm(sq@omat(ay)@si,2)*kval)
            # qdot is evaluated from the unchanged rotating background flow.
            qdot=np.asarray(qdotfn(bval),complex)
            ed=qdot+qn@dmat(ay)+dmat(ay).conjugate().T@qn
            men=max(men,float(np.max(np.linalg.eigvalsh((si@ed@si+(si@ed@si).conjugate().T)/2))))
            coupling_max=max(coupling_max,mcoupling)
        checks.add('actual_prepared_bound_'+str(kval),mv<=0,mv,'frozen roundoff only')
        checks.add('actual_observable_unchanged_'+str(kval),mo<=1e-10,mo,'<=1e-10')
        checks.add('all_22_fields_unchanged_'+str(kval),mf<=1e-10,mf,'<=1e-10')
        checks.add('direct_source_identity_'+str(kval),ms<=1e-9,ms,'<=1e-9')
        checks.add('exact_source_interval_control_'+str(kval),msource<=0,msource,'frozen 1e-9 absolute plus relative roundoff only')
        if kval>=emin:
            checks.add('full_transformed_generator_'+str(kval),mg<=1e-9,mg,'<=1e-9')
            checks.add('diagonal_deviation_interval_'+str(kval),md<=float(delta)*(1+1e-9)+1e-9,md,'<=delta with roundoff only')
            checks.add('off_coupling_interval_'+str(kval),coupling_max<=float(kappa)*(1+1e-9)+1e-9,coupling_max,'<=kappa with roundoff only')
            checks.add('diagonal_energy_control_'+str(kval),men<=2*float(gamma)*(1+1e-9)+1e-9,men,'<=2 gamma with roundoff only')
        modes.append(dict(ell=kval,domain='IN_HIGH_MODE_THEOREM' if kval>=emin else 'UNCHANGED_SEPARATE_FINITE_BOUND',actual_error=me,bound_endpoint=float(c2/kval**2) if kval>=emin else None,observable_residual=mo,field_residual=mf,generator_residual=mg if kval>=emin else None,source_identity=ms,source_majorant_ratio=mc,diagonal_deviation=md if kval>=emin else None,coupling_times_ell=coupling_max if kval>=emin else None,diagonal_energy=men if kval>=emin else None))
    checks.add('all_five_modes_original_four_columns',sorted(m['ell'] for m in modes)==list(old.MODES) and all(np.array(item['initial_balanced']).shape==(20,4,2) for item in ar['modes']))
    checks.add('positive_exact_constants',all(val.is_Rational and val>=0 for val in (vb,rstar,cq,hdq,hoq,krd,kro,delta,kappa,gamma,ks)))
    exported={'exact_source_R'+str(j):prior.wire(mat) for j,mat in rs.items()}
    for j,mat in rs.items(): exact('source_roundtrip_'+str(j),old.parent.import_matrix(exported['exact_source_R'+str(j)],bg.sy)-mat)
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(row['passed'] for row in checks.rows);ok=passed==len(checks.rows)
    constants={k:str(val) for k,val in dict(V_2=vb,V_Q=vq,r_upper=rstar,K_comm_Q=cq,K_h2_diagonal_Q=hdq,K_h2_off_Q=hoq,K_Brem_diagonal_Q=krd,K_Brem_off_Q=kro,delta_diagonal=delta,kappa=kappa,gamma=gamma,K_source=ks).items()}
    formulas=dict(domain='ell>=15; rotating B1 J=1, preserved shell, 0<=t<=1/20; unchanged separate ell=4,8 bounds',constants=constants,matrices=exported,source_coefficient_bounds={str(j):str(val) for j,val in rn.items()},error_coefficient_exact=str(c2),error_coefficient_endpoint_display=float(c2),old_coefficient_endpoint_display=prepared['error_coefficient_endpoint_display'],coefficient_definition='C2(t)=(3/2)[K_O{3 exp(30t)(C_other+2 K_W K_source t)+3 kappa t exp(gamma t) C_fast}+3 K_Of exp(30t) C_fast+K_observation exp(21t/10)]',reused_constants_source=PARENT+'formulas.json',inverse_proof='For off-block V, T2^-1=(I-V/ell^2)(I-V^2/ell^4)^-1. Q-block even and odd inverse norms are <=1/(1-r^2) and r/(1-r^2); r<=r_upper<1.',compressed_energy_proof='Q and Qdot commute with Pf. The diagonal energy form is the compression of the full energy form, hence <=mu Q. D(Ay)-D(Aw) has Q norm <=delta_diagonal. The comparison propagator has norm <=exp((30+delta_diagonal) dt), without a similarity prefactor.',fast_transfer_proof='Actual full Phi_y has Q norm <=3 exp(30 dt). Variation of constants using the diagonal comparison and retained full fast response gives ||y_other(t)||_Q<=3 kappa t exp(gamma t)||y_fast(0)||_Q/ell for a mathematical initial fast component; physical initial data are not changed.',source_proof='Exact Laurent source coefficients reconstructed from complete Ac,H,Hdot,M and reduced only on the preserved Friedmann shell, then enclosed by rational whole-interval boxes.',physical_window_proved=False,sharp_order_proved=False)
    diagnostics=dict(modes=modes,original_initial_data_retained=True,complementary_nonmonotonic_data_unchanged=True,upper_order=2,sharp_order='NOT_PROVED',finite_accuracy_usefulness='NOT_CLAIMED',full_generator_never_projected=True)
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diagnostics)}
    summary=dict(schema='r4c1-g3n5-prepared-dust-sharper-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='SHARPER_PREPARED_UPPER_BOUND_SHARPNESS_OPEN' if ok else 'SHARPER_PREPARED_UPPER_BOUND_NOT_VERIFIED',prepared_error_upper_bound_proved=ok,convergence_upper_order=2 if ok else 'NOT_PROVED',full_dust_convergence_order='SHARP_ORDER_NOT_PROVED',full_prepared_high_p_remainder_proved=False,analytic_dust_milestone='OPEN_SHARPNESS_AND_USEFULNESS',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(val) for k,val in bodies.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_prepared_dust_sharper_attempt_01')
    ap.add_argument('--replay')
    args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir(): raise FileNotFoundError('Replay destination missing')
    if not args.replay and dest.exists(): raise FileExistsError('Refuse existing receipt directory')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode(): raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream: stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream: stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'status':summary['status'],'physics_pass':False}))
    for row in summary['checks']:
        if not row['passed']: print(json.dumps(row))
    return int(summary['passed']!=summary['total'])

if __name__=='__main__': raise SystemExit(main())
