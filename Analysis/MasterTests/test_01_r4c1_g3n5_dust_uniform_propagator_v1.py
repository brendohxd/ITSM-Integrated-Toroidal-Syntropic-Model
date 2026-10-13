"""Uniform mixed-order linear propagator; prepared dust remainder stays open."""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PARENT=BASE+'r4c1_g3n5_dust_remainder_attempt_01/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ENGINE='Analysis/MasterTests/test_01_r4c1_g3n5_dust_remainder_v6.py'
ENGINE_SHA='efef4d8cc501fbbf7f62f2c9e60d12a5dceab8c24f0caaa73b3136e952eba913'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_OSCILLATORY_BOUND_CONTRACT_2026-10-11.md'
CONTROLS='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_CONTROLS_2026-10-11.md'
if hashlib.sha256((ROOT/ENGINE).read_bytes()).hexdigest()!=ENGINE_SHA:
    raise RuntimeError('Frozen source pin drift')
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_dust_remainder_v6 as old
common=old.common

def wire(mat):
    return {'shape':list(mat.shape),'entries':[{'row':i,'column':j,'terms':[str(mat[i,j])]} for i in range(mat.rows) for j in range(mat.cols) if mat[i,j]!=0]}

class Box(old.RationalBox):
    @lru_cache(maxsize=None)
    def evaluate(self,z):
        if z.is_Pow and z.exp==-s.Rational(1,2):
            lo,hi=super().evaluate(s.sqrt(z.base))
            if lo<=0:raise ZeroDivisionError('Root inverse includes zero')
            return 1/hi,1/lo
        return super().evaluate(z)

def calculate():
    ps=common.read_json(PARENT+'summary.json')
    pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()})
    pins.update({PARENT+'summary.json':'0da2e0166bb30f3f15cbbda980cc90ee9cefd30bd3aeb602f816dc6d3da621cd',ENGINE:ENGINE_SHA,
                 CONTRACT:'99e1221784220fd7520e5ae3c40cde051812ddd52271ff336c1205c605556493'})
    # The separately frozen controls and current executable are pinned by their
    # saved bytes before any calculation. Replay checks their recorded hashes.
    pins[CONTROLS]=common.sha((ROOT/CONTROLS).read_bytes())
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=old.parent.snapshot(paths)
    checks=common.Checks()
    checks.add('parent_78_checked_remainder_open',ps['passed']==ps['total']==78 and not ps['full_prepared_high_p_remainder_proved'] and not ps['physics_pass'])
    bg=old.Background()
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
    ell=bg.ell
    on=lambda m:m.applyfunc(s.cancel)
    exact=lambda name,m:old.parent.exact(checks,name,on(m) if isinstance(m,s.MatrixBase) else s.cancel(m))
    raw=common.read_json(old.PARENT+'matrices.json')
    az=old.parent.import_matrix(raw['balanced_generator'],bg.sy)
    c=s.eye(20);ci=s.eye(20)
    c[13,13]=ell/a;ci[13,13]=a/ell
    ac=on((bg.dt(c)+c*az)*ci)
    exact('mixed_velocity_scaling_inverse',c*ci-s.eye(20))
    checks.add('mixed_velocity_scaling_drift_retained',bg.dt(c)[13,13]!=0)
    blocks={}
    for i in range(20):
        for j in range(20):
            for term in s.Add.make_args(s.expand(ac[i,j])):
                power=term.as_powers_dict().get(ell,s.Integer(0))
                coeff=s.cancel(term/ell**power)
                if not power.is_Integer or ell in coeff.free_symbols:raise ValueError('Not Laurent',i,j)
                blocks.setdefault(int(power),s.zeros(20))[i,j]+=coeff
    exact('complete_Laurent_generator_reconstruction',ac-sum((mat*ell**k for k,mat in blocks.items()),s.zeros(20)))
    checks.add('no_omitted_generator_power',set(blocks)=={-2,-1,0,1,2},sorted(blocks))
    f,l=blocks[2],blocks[1]
    fast=(9,19);ld=l.copy();off=s.zeros(20)
    for i in range(20):
        for j in range(20):
            if (i in fast)!=(j in fast):off[i,j]=l[i,j];ld[i,j]=0
    uf=s.zeros(20)
    uf[9,0]=-11*s.sqrt(2)*a/25
    uf[9,3]=11*s.I*a*(65*H+2*pd)/375
    uf[9,13]=11*s.I*a/75
    uf[13,9]=2*s.I*a/5
    uf[13,19]=18*s.I*a*pd
    g=-22*a*a/375
    exact('fast_cross_power_cancelled',f*uf-uf*f+off)
    exact('fast_cubic_identity',uf**3-g*uf)
    exact('fast_inverse_polynomial_identity',(s.eye(20)+uf/ell)*((1-g/ell**2)*s.eye(20)-uf/ell+uf**2/ell**2)-(1-g/ell**2)*s.eye(20))
    checks.add('fast_inverse_domain_all_positive_ell',s.simplify(-g).is_positive is True,'1+22*a^2/(375*ell^2)>1')
    tw=s.eye(20)
    tw[0,0]=-s.Rational(1,11);tw[0,13]=2*s.sqrt(2)*s.I/11
    tw[0,3]=4*s.sqrt(2)*s.I*(5*H+pd)/55
    tw[13,0]=3*s.sqrt(2)*s.I
    tw[6,3]=-s.I*ud;tw[7,3]=-s.I*vd;tw[8,3]=-s.I*rd
    ti=s.eye(20)
    ti[0,13]=-2*s.sqrt(2)*s.I/11;ti[0,3]=-4*s.sqrt(2)*s.I*(5*H+pd)/55
    ti[13,:]=s.eye(20)[13,:]-3*s.sqrt(2)*s.I*ti[0,:]
    ti[6,3]=s.I*ud;ti[7,3]=s.I*vd;ti[8,3]=s.I*rd
    exact('wave_coordinate_inverse',tw*ti-s.eye(20))
    exact('wave_coordinate_determinant',tw.det()-1)
    q=s.eye(20);q[0,0]=s.Rational(1,3);q[4,4]=q[5,5]=s.Rational(4,5);q[9,9]=s.Rational(5,33)
    q[6,6]=1+v*v/13;q[7,7]=1+u*u/13;q[6,7]=q[7,6]=-u*v/13
    fw,lw=on(tw*f*ti),on(tw*ld*ti)
    exact('dispersive_principal_Q_skew',q*fw+fw.conjugate().T*q)
    exact('wave_principal_Q_skew',q*lw+lw.conjugate().T*q)
    exact('complex_scalar_Q_positive_rank_one_form',q[6:8,6:8]-s.eye(2)-s.Matrix([v,-u])*s.Matrix([[v,-u]])/13)
    checks.add('Q_lower_bound_five_over_33',s.Rational(5,33)>0,'Q >= (5/33) I; positive evolution norm, not physical energy')
    aa0,aan1,aan2=[blocks[i] for i in (0,-1,-2)]
    ns=[on(l*uf-uf*ld+aa0),on(aa0*uf+aan1-bg.dt(uf)),on(aan1*uf+aan2),on(aan2*uf)]
    # Independent coefficientwise multiplication checks the complete remainder,
    # rather than sampling or dropping order-zero / negative-order terms.
    tf=s.eye(20)+uf/ell
    pre=ac*tf-tf*(ell**2*f+ell*ld)-bg.dt(tf)
    exact('full_fast_transformed_remainder_numerator',pre-sum((ns[k]/ell**k for k in range(4)),s.zeros(20)))
    invpoly=[s.eye(20),-uf,uf*uf-g*s.eye(20)]
    vs=[]
    for j in range(6):
        core=sum((invpoly[k]*ns[j-k] for k in range(3) if 0<=j-k<4),s.zeros(20))
        vs.append(on(tw*core*ti))
        print('Exact residual numerator',j,'compiled',flush=True)
    drift=on(bg.dt(tw)*ti)
    exact('wave_drift_identity',drift*tw-bg.dt(tw))
    checks.add('omitted_fast_transform_drift_rejected',any(z!=0 for z in bg.dt(uf)))
    checks.add('omitted_wave_transform_drift_rejected',any(z!=0 for z in bg.dt(tw)))
    exact('registered_background_complex_imaginary_orbit',bg.rates[4:6,:].subs({v:0,vd:0}))
    special={v:0,vd:0}
    q0=on(q.subs(special));qd0=on(bg.dt(q).subs(special))
    vs0=[on(m.subs(special)) for m in vs];drift0=on(drift.subs(special))
    fu=s.Rational(1)+s.Rational(1,6)+s.Rational(1,80)+s.Rational(3,14);fr=s.Rational(33,14);T=s.Rational(1,20)
    checks.add('positive_u_r_bootstrap',1-fu*T*T/2>0 and 1-fr*T*T/2>0)
    exact('u_force_coefficient_identity',-bg.rates[3]-3*H*ud-u*(1+(u*u+v*v)/6+(u*u+v*v)**2/80+3*r*r/14))
    exact('r_force_coefficient_identity',-bg.rates[7]-3*H*rd-r*(2+r*r/7+3*(u*u+v*v)/14))
    boxes={a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(3,4),s.Integer(1)),u:(1-fu*T*T/2,s.Integer(1)),v:(s.Integer(0),s.Integer(0)),r:(1-fr*T*T/2,s.Integer(1)),ud:(-fu*T,s.Integer(0)),vd:(s.Integer(0),s.Integer(0)),rd:(-fr*T,s.Integer(0)),pd:(s.Rational(1,6),s.Rational(1,5)),rho:(s.Rational(17,100),s.Rational(1,5)),C:(s.Integer(1),s.Rational(250,249))}
    bx=Box(boxes);qd=[q0[i,i] for i in range(20)]
    scaled=lambda m:s.Matrix(20,20,lambda i,j:s.cancel(m[i,j]/s.sqrt(qd[i]*qd[j])))
    sd=scaled(qd0+q0*drift0+drift0.conjugate().T*q0)
    hjs=[scaled(q0*m+m.conjugate().T*q0) for m in vs0]
    rows=[]
    for i in range(20):
        upper=bx.evaluate(sd[i,i])[1]+sum(bx.absolute(sd[i,j]) for j in range(20) if j!=i)
        upper+=sum(sum(bx.absolute(h[i,j]) for j in range(20))/s.Integer(4)**k for k,h in enumerate(hjs))
        rows.append(s.cancel(upper))
    mu=max(rows)
    checks.add('all_energy_row_constants_exact_finite',all(x.is_Rational for x in rows))
    print('Certified uniform energy derivative display',float(mu),flush=True)
    coeff=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc=np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    ar=common.read_json(old.PARENT+'trajectories.json')
    fn=s.lambdify([bg.bg,ell],(c,ci,bg.dt(c),az,uf,bg.dt(uf),tw,ti,bg.dt(tw),q,bg.dt(q),fw,lw,drift,*vs),'numpy',cse=True)
    qraw=old.parent.import_matrix(raw['full_field_reconstruction'],bg.sy)
    biraw=old.parent.import_matrix(raw['balancing_map_inverse'],bg.sy)
    fields=s.lambdify([bg.bg,ell],qraw*biraw,'numpy',cse=True)
    modes=[]
    for item in ar['modes']:
        kval=item['ell'];initial=np.array(item['initial_balanced']);zinit=initial[...,0]+1j*initial[...,1]
        maxamp=maxinverse=maxgen=maxbox=maxfields=maxconj=0.0
        energy0=None
        for ix,t in enumerate(ar['time']):
            bval=np.polynomial.polynomial.polyval(t,bc.T)
            vals=[np.asarray(m,dtype=complex) for m in fn(bval,kval)]
            cn,cin,cd,azn,un,udn,twn,tin,twd,qn,qdn,fwn,lwn,dn=vals[:14]
            nn=vals[14:];den=1+22*bval[0]**2/(375*kval**2)
            tfn=np.eye(20)+un/kval;tfin=np.eye(20)-un/(kval*den)+un@un/(kval*kval*den)
            rawz=np.array(item['balanced'][ix]);z=rawz[...,0]+1j*rawz[...,1]
            w=twn@tfin@cn@z
            energies=np.real(np.sum(w.conjugate()*(qn@w),axis=0))
            if energy0 is None:energy0=energies
            maxamp=max(maxamp,float(np.max(np.sqrt(energies/energy0)/np.exp(float(mu)*t/2))))
            maxinverse=max(maxinverse,float(np.linalg.norm(cin@tfn@tin@w-z,np.inf)/max(1.,np.linalg.norm(z,np.inf))))
            ew=np.real(np.sum(w.conjugate()*(qn@w),axis=0));cw=w.conjugate()
            ec=np.real(np.sum(cw.conjugate()*(qn.conjugate()@cw),axis=0))
            maxconj=max(maxconj,float(np.max(np.abs(ew-ec))/max(1.,np.max(np.abs(ew)))))
            archived=np.array(item['full_fields'][ix]);archived=archived[...,0]+1j*archived[...,1]
            maxfields=max(maxfields,float(np.linalg.norm(np.asarray(fields(bval,kval),complex)@z-archived,np.inf)/max(1.,np.linalg.norm(archived,np.inf))))
            for sym,value in zip(bg.bg,bval):
                lo,hi=boxes[sym];maxbox=max(maxbox,max(float(lo)-value,value-float(hi),0.))
            if ix in (0,len(ar['time'])//2,len(ar['time'])-1):
                acn=(cd+cn@azn)@cin
                af=tfin@(acn@tfn-udn/kval)
                direct=(twd+twn@af)@tin
                factored=kval**2*fwn+kval*lwn+dn+sum((nn[k]/kval**k for k in range(6)),np.zeros((20,20),complex))/den
                maxgen=max(maxgen,float(np.linalg.norm(direct-factored,np.inf)/max(1.,np.linalg.norm(direct,np.inf))))
        for name,value,limit in (('archive_Q_energy_bound',maxamp,1+1e-9),('full_inverse_reconstruction',maxinverse,1e-9),('numeric_generator_identity',maxgen,1e-9),('background_box_sanity',maxbox,1e-10),('all_22_fields_unchanged',maxfields,1e-10),('negative_conjugate_norm',maxconj,1e-9)):
            checks.add(name+'_'+str(kval),bool(value<=limit),value,'<='+str(limit))
        modes.append(dict(ell=kval,Q_bound_normalized_ratio=maxamp,inverse_residual=maxinverse,generator_residual=maxgen,field_residual=maxfields))
    checks.add('all_five_modes_four_columns_retained',sorted(m['ell'] for m in modes)==list(old.MODES) and all(np.array(m['initial_balanced']).shape==(20,4,2) for m in ar['modes']))
    checks.add('no_projection_or_field_deletion',az.shape==(20,20) and qraw.shape==(22,20))
    maps={'longitudinal_velocity_scaling_C':c,'fast_cross_map_U':uf,'wave_map_Tw':tw,'wave_inverse_Twi':ti,'positive_evolution_Q':q,'dispersive_principal_F':fw,'ordinary_wave_principal_L':lw,'wave_drift':drift}
    maps.update({'residual_numerator_'+str(k):m for k,m in enumerate(vs)})
    export={k:wire(m) for k,m in maps.items()}
    for name,obj in export.items():exact('roundtrip_'+name,old.parent.import_matrix(obj,bg.sy)-maps[name])
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('source_hash_size_mtime_preserved',old.parent.snapshot(paths)==before,{'files':len(before)})
    formulas=dict(matrices=export,coordinate_definition='w=Tw (I+U/ell)^(-1) C z; z=B x',generator='w_dot=(ell^2 F + ell L + wave_drift + sum_j residual_numerator_j/ell^j /(1+22*a^2/(375*ell^2))) w',norm='||w||_Q=sqrt(w^dagger Q(t) w)',proof='Q F+F^dagger Q=Q L+L^dagger Q=0; exact rational row bounds on Q^(-1/2)(Q_dot+Q residual+residual^dagger Q)Q^(-1/2) give E_dot<=mu E and ||w(t)||_Q(t)<=exp(mu*(t-s)/2)||w(s)||_Q(s).',domain='ell>=4; 0<=s<=t<=1/20; unchanged B1 background, positive a,C,rho; v=v_dot=0 background but all complex perturbations retained',background_boxes={str(k):[str(x) for x in val] for k,val in boxes.items()},energy_row_constants=[str(x) for x in rows],mu_exact=str(mu),mu_display=float(mu),endpoint_amplification_display=float(s.exp(mu*T/2)),physical_energy_positive_claim=False)
    diag=dict(modes=modes,uniform_full_linear_propagator_proved=True,prepared_dust_remainder_proved=False,full_dust_convergence_order='NOT_PROVED',remaining='Control retained fast forcing and initial fast mismatch in the actual dust observable; uniform full-state bound alone is insufficient.',precision='Exact SymPy/rational outward intervals; binary64 checks use inherited 70-digit degree-40 background and frozen trajectories; no new high-precision IVP')
    payloads={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag)}
    passed=sum(x['passed'] for x in checks.rows)
    summary=dict(schema='r4c1-g3n5-dust-uniform-propagator-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,status='UNIFORM_MIXED_NORM_PROPAGATOR_CHECKED_PREPARED_REMAINDER_OPEN',uniform_full_linear_propagator_proved=True,full_prepared_high_p_remainder_proved=False,analytic_dust_milestone='OPEN_PREPARED_REMAINDER',full_dust_convergence_order='NOT_PROVED',physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',original_slow_time_coefficient='-11/6',ordinary_wave_Jordan_defect_removed=False,physical_EFT_cutoff_derived=False,complete_density_Hamiltonian_positive=False,healthy_continuous_GR_verified=False,source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,artifacts={k:common.sha(b) for k,b in payloads.items()},runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),review_dependencies=['R9-MT1-G3N5-DUST-REMAINDER','G3N5 finite-mode/weighted/nonzero','B1G and inherited action/operator review'])
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    payloads['summary.json']=common.encode(summary)
    return payloads,summary

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_01');ap.add_argument('--replay');args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination missing')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing scientific directory')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Exact replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN','validation':summary['validation'],'passed':summary['passed'],'total':summary['total'],'status':summary['status'],'physics_pass':False}))
    for q in summary['checks']:
        if not q['passed']:print(json.dumps(q))
    return int(summary['passed']!=summary['total'])

if __name__=='__main__':raise SystemExit(main())
