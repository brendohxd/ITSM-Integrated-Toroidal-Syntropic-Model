"""Uniform component-transfer lemma; complete prepared dust error remains open."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2];BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/'
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_dust_uniform_propagator_v2.py'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!='bda5fcb42e6fec850093075d681c712972b951fc08107f3f70eed52420898ca3':raise RuntimeError('Engine drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_uniform_propagator_v2 as engine
old=engine.old;common=old.common
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_PREPARED_DUST_ERROR_CONTRACT_2026-10-11.md'
CONTROL='Theory/Gates/RES-001/RES001_R4C1_G3N5_FAST_TRANSFER_CONTROLS_2026-10-11.md'

def wire(mat):return {'shape':list(mat.shape),'entries':[{'row':i,'column':j,'terms':[str(mat[i,j])]} for i in range(mat.rows) for j in range(mat.cols) if mat[i,j]!=0]}

def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()});pins[PARENT+'summary.json']='ba2c19f2ee923816ca4ae0bf2de6a2cf4d898975c468cd0529d6cbc9f2dc1356'
    for rel in (CONTRACT,CONTROL,SELF):pins[rel]=common.sha((ROOT/rel).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/x for x in pins]
    paths.extend(Path(str(x)+'.sha256') for x in list(paths) if Path(str(x)+'.sha256').exists())
    before=old.parent.snapshot(paths);checks=common.Checks();bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg;ell=bg.ell;on=lambda m:m.applyfunc(s.cancel)
    exact=lambda name,m:old.parent.exact(checks,name,on(m) if isinstance(m,s.MatrixBase) else s.cancel(m))
    cert=common.read_json(PARENT+'formulas.json')
    checks.add('validated_rotating_background_parent',ps['passed']==ps['total']==66 and ps['uniform_full_linear_propagator_proved'] and not ps['physics_pass'])
    checks.add('parent_mu_below_60',s.sympify(cert['mu_exact'])<60)
    raw=common.read_json(cert['general_exact_maps_source'])['matrices'];maps={k:old.parent.import_matrix(x,bg.sy) for k,x in raw.items()}
    f,l,q,drift=[maps[k] for k in ('dispersive_principal_F','ordinary_wave_principal_L','positive_evolution_Q','wave_drift')]
    vs=[maps['residual_numerator_'+str(j)] for j in range(6)];b0=on(drift+vs[0]);fast=(9,19)
    pf=s.zeros(20);pf[9,9]=pf[19,19]=1;po=s.eye(20)-pf
    off=pf*b0*po+po*b0*pf;bd=b0-off
    exact('principal_fast_partition_F',f*pf-pf*f);exact('principal_fast_partition_L',l*pf-pf*l);exact('Q_orthogonal_partition',q*pf-pf*q)
    fi=s.zeros(20);fi[9,19]=-33*a*a/5;fi[19,9]=a*a
    exact('fast_inverse_on_declared_subspace',f*fi-pf)
    vf=on(po*off*fi-fi*off*po)
    exact('second_fast_cross_cancellation',f*vf-vf*f+off)
    exact('new_map_is_off_block',pf*vf*pf+po*vf*po)
    boxes={bg.sy[k]:(s.sympify(z[0]),s.sympify(z[1])) for k,z in cert['background_boxes'].items()};bx=old.RationalBox(boxes)
    n2=lambda mat:max(bx.norm(mat),bx.norm(mat.T))
    vb=n2(vf);emin=4
    while s.Integer(emin)**2<6*vb:emin+=1
    checks.add('derived_Neumann_domain',s.Integer(emin)**2>=6*vb,{'ell_min':emin,'V_2norm_bound':str(vb)})
    checks.add('Q_upper_bound_and_norm_conversion',1+boxes[u][1]**2/13+boxes[v][1]**2/13<=s.Rational(9,8) and s.Rational(9,8)/(s.Rational(5,33))<9)
    comm=on(l*vf-vf*l);h2=on(b0*vf-vf*bd-bg.dt(vf));g=-22*a*a/375
    rem=[vs[1],on(vs[2]+g*vs[0]),*vs[3:]]
    kb=sum(n2(mat)/s.Integer(emin)**j for j,mat in enumerate(rem));kl,kh=n2(comm),n2(h2)
    kappa=s.cancel(6*(kl+kh/emin+kb*(1+vb/s.Integer(emin)**2)));gamma=s.cancel(30+3*kappa/emin)
    tt=s.eye(20)+vf/ell**2;aw=ell**2*f+ell*l+b0+sum((rem[j]/ell**(j+1) for j in range(5)),s.zeros(20))/(1-g/ell**2)
    remainder=comm/ell+h2/ell**2+(sum((rem[j]/ell**(j+1) for j in range(5)),s.zeros(20))/(1-g/ell**2))*tt
    exact('complete_second_generator_factored',aw*tt-tt*(ell**2*f+ell*l+bd)-bg.dt(tt)-remainder)
    checks.add('new_coordinate_drift_not_omitted',any(x!=0 for x in bg.dt(vf)))
    print('Derived ell minimum',emin,'coupling display',float(kappa),'propagator exponent display',float(gamma),flush=True)
    co=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json');bc=np.array([[float(x[0]) for x in row] for row in co['background_coefficients']])
    ar=common.read_json(old.PARENT+'trajectories.json')
    cn,un,twn,tin=[maps[k] for k in ('longitudinal_velocity_scaling_C','fast_cross_map_U','wave_map_Tw','wave_inverse_Twi')]
    rawold=common.read_json(old.PARENT+'matrices.json');qq=old.parent.import_matrix(rawold['full_field_reconstruction'],bg.sy)*old.parent.import_matrix(rawold['balancing_map_inverse'],bg.sy)
    fn=s.lambdify([bg.bg,ell],(vf,bg.dt(vf),aw,f,l,bd,remainder,q,cn,un,twn,tin,qq),'numpy',cse=True);modes=[]
    for item in ar['modes']:
        kval=item['ell'];maxinverse=maxgen=maxcoupling=maxfields=0.
        for ix in (0,len(ar['time'])//2,len(ar['time'])-1):
            bval=np.polynomial.polynomial.polyval(ar['time'][ix],bc.T);vv,vvd,aa,ff,ll,bdd,rr,qn,cc,uu,tw,twi,qfields=[np.asarray(x,complex) for x in fn(bval,kval)]
            rawz=np.array(item['balanced'][ix]);z=rawz[...,0]+1j*rawz[...,1];af=np.array(item['full_fields'][ix]);af=af[...,0]+1j*af[...,1]
            maxfields=max(maxfields,float(np.linalg.norm(qfields@z-af,np.inf)/max(1.,np.linalg.norm(af,np.inf))))
            if kval<emin:continue
            t2=np.eye(20)+vv/kval**2;t2i=np.linalg.inv(t2);den=1+22*bval[0]**2/(375*kval**2)
            t1=np.eye(20)+uu/kval;t1i=np.eye(20)-uu/(kval*den)+uu@uu/(kval*kval*den)
            w=tw@t1i@cc@z;y=t2i@w
            maxinverse=max(maxinverse,float(np.linalg.norm(t2@y-w,np.inf)/max(1.,np.linalg.norm(w,np.inf))))
            direct=t2i@(aa@t2-vvd/kval**2);factored=kval*kval*ff+kval*ll+bdd+t2i@rr
            maxgen=max(maxgen,float(np.linalg.norm(direct-factored,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
            ev,evec=np.linalg.eigh(qn);sq=(evec*np.sqrt(ev))@evec.conjugate().T;si=(evec/np.sqrt(ev))@evec.conjugate().T
            offn=np.zeros((20,20),complex)
            for i in range(20):
                for j in range(20):
                    if (i in fast)!=(j in fast):offn[i,j]=direct[i,j]
            maxcoupling=max(maxcoupling,float(np.linalg.norm(sq@offn@si,2)*kval))
        checks.add('all_22_fields_retained_'+str(kval),maxfields<=1e-10,maxfields,'<=1e-10')
        if kval>=emin:
            checks.add('inverse_identity_'+str(kval),maxinverse<=1e-9,maxinverse,'<=1e-9')
            checks.add('generator_identity_'+str(kval),maxgen<=1e-9,maxgen,'<=1e-9')
            checks.add('coupling_interval_control_'+str(kval),maxcoupling<=float(kappa)*(1+1e-9),maxcoupling,'<=kappa with relative roundoff only')
        modes.append(dict(ell=kval,domain='IN' if kval>=emin else 'OUTSIDE_NEW_LEMMA_ORIGINAL_ARCHIVE_RETAINED',inverse_residual=maxinverse,generator_residual=maxgen,coupling_times_ell=maxcoupling,field_residual=maxfields))
    checks.add('all_five_modes_four_original_columns',sorted(x['ell'] for x in modes)==list(old.MODES) and all(np.array(x['initial_balanced']).shape==(20,4,2) for x in ar['modes']))
    export={name:wire(mat) for name,mat in {'second_fast_map_V':vf,'order_zero_block_diagonal':bd,'commutator_ordinary_wave':comm,'second_drift_and_value':h2}.items()}
    for name,obj in export.items():exact('roundtrip_'+name,old.parent.import_matrix(obj,bg.sy)-{'second_fast_map_V':vf,'order_zero_block_diagonal':bd,'commutator_ordinary_wave':comm,'second_drift_and_value':h2}[name])
    checks.add('pins_after',common.inspect_pins(pins)==absent);checks.add('input_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    passed=sum(x['passed'] for x in checks.rows);ok=passed==len(checks.rows)
    formulas=dict(matrices=export,coordinate_definition='y=(I+V/ell^2)^(-1)w, with original full w transform retained',domain=f'ell>={emin}; 0<=s<=t<=1/20; rotating B1 J=1',constants={k:str(x) for k,x in dict(V_norm=vb,K_Brem=kb,K_commutator=kl,K_value_drift=kh,kappa=kappa,gamma_diagonal=gamma).items()},kappa_display=float(kappa),gamma_display=float(gamma),full_propagator='||Phi_y(t,s)||_Q(t)<-Q(s)<=3 exp(30*(t-s))',diagonal_propagator='||Phi_diag(t,s)||<=3 exp((30+3*kappa/ell_min)*(t-s))',off_block='||off_f(A_y)||_Q<=kappa/ell',fast_initial_transfer='For y_other(0)=0: ||y_other(t)||_Q(t)<=9*kappa*t*exp(gamma_diagonal*t)*||y_fast(0)||_Q(0)/ell',proof='Q>=5I/33,Q<=9I/8 imply norm conversion<=3; ell^2>=6V_norm gives T2 Qnorm<=3/2,inverse<=2. Exact cross cancellation and residual bounds give off-block<=kappa/ell. Similarity of prior uniform propagator gives 3 exp(30 dt); bounded-perturbation Volterra inequality gives diagonal propagator. Variation of constants with full retained fast response yields the component-transfer bound.',not_old_probe_replacement=True)
    diag=dict(modes=modes,sharp_prepared_dust_order='NOT_PROVED',prepared_initial_mismatch_bound='NOT_YET_COMBINED',all_original_modes_retained=True)
    payloads={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag)}
    summary=dict(schema='r4c1-g3n5-dust-fast-transfer-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='FAST_COMPONENT_TRANSFER_CHECKED_PREPARED_DUST_ERROR_OPEN' if ok else 'FAST_COMPONENT_TRANSFER_NOT_VERIFIED',fast_component_transfer_proved=ok,ell_min=emin,full_prepared_high_p_remainder_proved=False,full_dust_convergence_order='NOT_PROVED',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',ordinary_wave_Jordan_defect_removed=False,complete_density_Hamiltonian_positive=False,physical_EFT_cutoff_derived=False,healthy_continuous_GR_verified=False,source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(x) for k,x in payloads.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'});payloads['summary.json']=common.encode(summary);return payloads,summary

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_fast_transfer_attempt_01');ap.add_argument('--replay');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'ell_min':summary['ell_min'],'physics_pass':False}))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
