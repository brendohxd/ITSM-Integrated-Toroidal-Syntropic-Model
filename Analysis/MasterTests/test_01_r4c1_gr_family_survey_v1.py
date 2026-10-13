"""Two new R4C1 families: generic-action entry checks, not EFT clearance."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_g3n5_dust_finite_k_attempt_01/'
KERNEL=BASE+'r4c1_g3n5_attempt_02/kernel.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_GR_FAMILY_SURVEY_CONTRACT_2026-10-11.md'
PINNED={CONTRACT:'aa3a8ced3935b2ca0a8f72ee56bcf22a17049e4ff80b8f3e527113cdddeb29b1',
    KERNEL:'cf30a7e334d154e492f8ca7bde92cf95754390b602f4914e5b6ba8fed90a74e3',
    PARENT+'summary.json':'a4c884469c39682908d894e23cb5fbdaa370a4a46f5aa2c31ae4a14128c0f706',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py':'8c63194a678734917c5c9a9593da8023fb7ba946790cc0376c7cd3a9fa57c991',
    'Theory/Gates/RES-001/RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md':'1b9fbc4185b61d1e37d7865baa811994e235523eb9ecc22432c733b4bc38aa04',
    'Theory/Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_REPORT_2026-10-08.md':'035d1480904b2459b6a4e8b6df91d381065a653fdeb49583fcdb3dbfc4ac49f4',
    'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':'14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519'}
for name in ('Analysis/MasterTests/test_01_r4c1_interacting_background.py','Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py'):
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=PINNED[name]:
        raise RuntimeError('Frozen imported source drift '+name)
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_interacting_background as bg
import test_01_r4c1_g3n5_nonzero_characteristic_v1 as parent
common=parent.common
ETAS=(1.,.25,.0625,.015625,.00390625,.0009765625)
FIELDS=parent.old.FIELDS
IDX=parent.old.IDX


def families(eta):
    a1=s.Rational(2,15)*eta; a14=eta/6
    return {'archived_G3':(a1,eta/8,-7*eta/72,a14),
        'new_B1_frame':(a1,s.Integer(0),eta/15,a14),
        'new_hierarchical':(a1,eta**2/8,eta/15,a14)}


def parameters(name,eta):
    p=bg.PARAMS.copy()
    p['c2']=.1
    p['c3']=-.2 if name=='new_B1_frame' else -.2+3*eta/16
    for key in ('MU2','zeta','K','b','gr'):p[key]*=eta
    p['A']*=eta**1.5
    p['beta']*=eta**2
    return p


class GenericKernel:
    """Unspecialized Hessian, with all metric/frame/matter source fields."""
    def __init__(self):
        kernel=common.read_json(KERNEL)
        self.records=kernel['entries']
        names=sorted(set(q for row in self.records for q in re.findall(r'[A-Za-z_][A-Za-z_0-9]*',row['value'])))
        self.sy={q:s.Symbol(q,real=True) for q in names}
        self.order=names
        self.expr=[s.sympify(row['value'],locals=self.sy) for row in self.records]
        self.fun=s.lambdify([[self.sy[q] for q in names]],self.expr,'numpy',cse=True)

    def values(self,y,p):
        a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=y
        ph=bg.physics(y,p)
        values={**p,'a':a,'H':H,'u0':u,'u_dot':ud,'v0':v,'v_dot':vd,
            'r0':r,'r_dot':rd,'psi_dot':pd,'C':np.exp(p['beta']*psi),
            'epsilon0':rho*np.exp(-4*p['beta']*psi),'lambda0':ph['lambda_U'],
            'K_Q':p['K'],'lambda4':p['l4'],'lambda6':p['l6'],
            'Lambda':p['cutoff'],'lambda_r':p['lr'],'g_r':p['gr'],'rho_Lambda':p['vacuum']}
        return [values[q] for q in self.order]

    def blocks(self,y,p,k):
        vals=self.fun(self.values(y,p))
        LA,LB,LBT,LK=[np.zeros((22,22),dtype=complex) for _ in range(4)]
        weights=(1.,None,1j*k,0.,0.)
        for row,value in zip(self.records,vals):
            bi,i=divmod(row['row'],22);bj,j=divmod(row['column'],22)
            if bi!=1 and bj!=1:LA[i,j]+=np.conj(weights[bi])*value*weights[bj]
            elif bi!=1:LB[i,j]+=np.conj(weights[bi])*value
            elif bj!=1:LBT[i,j]+=value*weights[bj]
            else:LK[i,j]+=value
        return LA,LB,LBT,LK

    def reduce(self,y,p,k):
        LA,LB,LBT,LK=self.blocks(y,p,k)
        metric=('Myy','Myz','Mzz') if k else tuple(FIELDS[4:10])
        dyn=metric+tuple(FIELDS[10:17])
        aux=('Sx','Sy','Sz','Z') if k else ('Z',)
        F=np.zeros((22,len(dyn)),dtype=complex);U=np.zeros((22,len(aux)),dtype=complex)
        for j,name in enumerate(dyn):F[IDX[name],j]=1
        F[IDX['alpha'],dyn.index('Pi')]=-p['beta']
        for j,name in enumerate(aux):U[IDX[name],j]=1
        a=y[0];MT=p['MP2']-p['MU2']*(p['c1']+p['c3'])
        cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
        inv=np.diag((-a*a/(cL*k*k),2*a*a/(MT*k*k),2*a*a/(MT*k*k),1/p['b'])) if k else np.array([[1/p['b']]])
        D=U.conj().T@LA@U;Ys=U.conj().T@LA@F;Vs=U.conj().T@LB@F
        A=F.conj().T@LA@F-Ys.conj().T@inv@Ys
        R=F.conj().T@LB@F-Ys.conj().T@inv@Vs
        K=F.conj().T@LK@F-Vs.conj().T@inv@Vs
        residual=max(float(np.linalg.norm(LA-LA.conj().T,np.inf)/max(1.,np.linalg.norm(LA,np.inf))),
            float(np.linalg.norm(LBT-LB.conj().T,np.inf)/max(1.,np.linalg.norm(LB,np.inf))),
            float(np.linalg.norm(D@inv-np.eye(len(aux)),np.inf)),
            float(np.linalg.norm(LK@U,np.inf)),float(np.linalg.norm(LB@U,np.inf)),
            float(np.linalg.norm(K-K.conj().T,np.inf)/max(1.,np.linalg.norm(K,np.inf))))
        return {'coordinates':list(dyn),'auxiliaries':list(aux),'A':A,'R':R,'K':K,
            'auxiliary_D':D,'auxiliary_inverse':inv,'reconstruction_error':residual,
            'kinetic_eigenvalues':np.linalg.eigvalsh(K).tolist(),
            'scope':'instantaneous reduced action; not full EOM/characteristic/energy-residue or fixed-charge reduction'}


def calculate():
    ps=common.read_json(PARENT+'summary.json');pins=dict(ps['source_sha256'])
    pins.update({PARENT+k:v for k,v in ps['artifacts'].items()})
    for name,value in PINNED.items():
        if name in pins and pins[name]!=value:raise ValueError('Conflicting pin '+name)
        pins[name]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins);paths=[ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=parent.snapshot(paths);checks=common.Checks()
    exact=lambda name,q:parent.exact(checks,name,q)
    eta=s.Symbol('eta',positive=True);forms={}
    kernel=GenericKernel()
    tt=next(q for row,q in zip(kernel.records,kernel.expr) if row['row']==row['column']==30)
    grad=next(q for row,q in zip(kernel.records,kernel.expr) if row['row']==row['column']==52)
    sy=kernel.sy
    exact('generic_TT_kinetic_from_full_action',tt-(sy['MP2']-sy['MU2']*(sy['c1']+sy['c3']))/2)
    exact('generic_TT_gradient_from_full_action',grad+sy['MP2']/(2*sy['a']**2))
    upper=s.Rational(7,10**16)
    max_a13=1-(1+upper)**-2
    for name,(a1,a13,a2,a14) in families(eta).items():
        a3=a13-a1;a4=a14-a1;aL=a13+a2
        mc=1+(a13+3*a2)/2;mt=1-a13
        cv=(a1+a13*a13/(2*mt))/a14
        pn1=s.factor(-8*(a3*a3+a1*a4)/(2*a1-a1*a1+a3*a3))
        pn2=s.factor(pn1/2-(a1+2*a3-a4)*(2*a1+3*a2+a3+a4)/(aL*(2-a14)))
        obj={'alpha1':a1,'alpha13':a13,'alpha2':a2,'alpha14':a14,'alphaL':aL,
            'G_cos_over_G_static':s.factor((1-a14/2)/mc),'M_cos2':mc,'M_tensor2':mt,
            'K_vector':a14,'K_force':3*eta,'c_tensor_squared':1/mt,
            'c_vector_squared_control':cv,'scalar_D_over_H_squared':s.factor(4*mc*mt/aL),
            'PPN1_scalar_free_comparator':pn1,'PPN2_scalar_free_comparator':pn2,
            'canonical_cubic':2*s.sqrt(3)/63,'canonical_matter':2*s.sqrt(3)*eta**s.Rational(3,2)/15,
            'probe_frame_normalization_squared':eta/6}
        for label in ('G_cos_over_G_static','c_tensor_squared'):
            exact(name+'_'+label+'_GR_endpoint',s.limit(obj[label],eta,0)-1)
        exact(name+'_frame_rank_loss',s.limit(a14,eta,0))
        exact(name+'_force_rank_loss',s.limit(3*eta,eta,0))
        obj['tensor_speed_comparator_parameter_bound']=('all eta: luminal principal tensor' if name=='new_B1_frame'
            else ('eta <= '+str(8*max_a13) if name=='archived_G3' else 'eta^2 <= '+str(8*max_a13)))
        # Exact vacuum-vector normalized speed identity, not finite-density stability.
        exact(name+'_vector_speed_normalization',(a1-a1*a1/2+a3*a3/2)/(a14*(1-a13))-cv)
        forms[name]={k:str(v) for k,v in obj.items()}
    checks.add('new_families_distinct_from_frozen_G1',True,'A scales eta^(3/2); old G1 remains unchanged')
    time=np.linspace(0.,4.,801);hg=np.sqrt(.2/3)
    gr=np.array([(1+1.5*hg*time)**(2/3),hg/(1+1.5*hg*time),.2/(1+1.5*hg*time)**2])
    rows=[];snapshots=[]
    for name in ('new_B1_frame','new_hierarchical'):
        for et in ETAS:
            p=parameters(name,et);y0=bg.initial(p)
            for idx in (2,5,6,7):y0[idx]*=np.sqrt(et)
            y0[9]*=et;y0[1]=np.sqrt(bg.physics(y0,p)['energy']/(3*bg.effective_mass(p)))
            states=[];runs=[]
            for method in ('DOP853','Radau'):
                sol=solve_ivp(lambda t,y:bg.rhs(t,y,p),(0.,4.),y0,method=method,rtol=1e-11,atol=1e-13,dense_output=True)
                yy=sol.sol(time);ph=bg.physics(yy,p)
                vals={'method':method,'completed':bool(sol.success and sol.t[-1]==4.),
                    'Friedmann':float(np.max(ph['constraint_norm'])),
                    'charge_drift':float(np.max(np.abs(ph['charge']-ph['charge'][0]))),
                    'dust_drift':float(np.max(np.abs(ph['dust_integral']-ph['dust_integral'][0]))),
                    'minimum_a_H_rho':[float(q.min()) for q in yy[[0,1,10]]]}
                key=name+'_'+str(et)+'_'+method
                checks.add(key+'_completed',vals['completed'])
                checks.add(key+'_finite_positive_domain',bool(np.isfinite(yy).all() and min(vals['minimum_a_H_rho'])>0))
                for label in ('Friedmann','charge_drift','dust_drift'):
                    checks.add(key+'_'+label,vals[label]<1e-8,vals[label],'<1e-8')
                states.append(yy);runs.append(vals)
            disagreement=float(np.max(np.abs(states[0]-states[1])/(1+np.abs(states[0]))))
            checks.add(name+'_'+str(et)+'_two_method_agreement',disagreement<1e-8,disagreement,'<1e-8')
            checks.add(name+'_'+str(et)+'_charge_initial',abs(bg.physics(y0,p)['charge']-et)<1e-14)
            datum={k:float(s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(str(et)))) for k,v in forms[name].items()
                if k in ('G_cos_over_G_static','c_tensor_squared','PPN1_scalar_free_comparator','PPN2_scalar_free_comparator')}
            cT=np.sqrt(datum['c_tensor_squared'])
            # Stable expression (sqrt(cT^2)-1) = (cT^2-1)/(sqrt(cT^2)+1).
            delta_c=(datum['c_tensor_squared']-1)/(cT+1)
            row={'family':name,'eta':et,'parameters_assumed_not_derived':p,'runs':runs,
                'normalized_metric_dust_error':float(np.max(np.abs(states[0][[0,1,10]]-gr)/(1+np.abs(gr)))),
                'two_method_disagreement':disagreement,'coefficient_comparators':datum,
                'tensor_speed_comparator_matches':-3e-15<delta_c<7e-16,
                'PPN2018_scalar_free_comparator_matches':abs(datum['PPN1_scalar_free_comparator'])<=1e-4 and abs(datum['PPN2_scalar_free_comparator'])<=1e-7,
                'physical_candidate_admitted':False}
            rows.append(row)
            for ti in (0,200,800):
                yy=states[0][:,ti]
                for k in (0,20,40,80):
                    snap=kernel.reduce(yy,p,k)
                    checks.add(name+'_'+str(et)+'_t'+str(ti)+'_k'+str(k)+'_generic_action_reduction',
                        snap['reconstruction_error']<=1e-9,snap['reconstruction_error'],'<=1e-9')
                    snapshots.append({'family':name,'eta':et,'time':float(time[ti]),'coordinate_mode':k,
                        **{key:(np.stack((value.real,value.imag),axis=-1).tolist() if isinstance(value,np.ndarray) else value) for key,value in snap.items()}})
            print(json.dumps({'family':name,'eta':et,'method_error':disagreement,
                'GW_comparator':row['tensor_speed_comparator_matches'],'PPN_comparator':row['PPN2018_scalar_free_comparator_matches']}),flush=True)
    checks.add('zero_mode_not_shift_inverted',all(q['auxiliaries']==['Z'] for q in snapshots if q['coordinate_mode']==0))
    checks.add('all_kinetic_eigenvalues_exported_including_negative',len(snapshots)==144,
        {'snapshots':len(snapshots),'negative_eigenvalue_snapshots':sum(min(q['kinetic_eigenvalues'])<0 for q in snapshots)})
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('all_original_hash_size_mtime_preserved',parent.snapshot(paths)==before,{'files':len(before)})
    formulas={'families':forms,'generic_TT_Hessian':str(tt),'generic_TT_gradient':str(grad),
        'eta_grid':list(ETAS),'source_dimensions':'alpha_i,eta,beta,c_i dimensionless; K_Q dimension2,A dimension1; input reference M_P=1; no physical torus radius or observational calibration',
        'auxiliary_nonzero_eigenvalues':['-(alpha13+alpha2) k^2/a^2','(1-alpha13) k^2/(2a^2) twice','b'],
        'external_sources':['https://arxiv.org/abs/1710.05834','https://arxiv.org/pdf/gr-qc/0509083','https://arxiv.org/pdf/1802.04303'],
        'compatibility_scope':'non-dispersive TT principal and scalar-free Einstein-aether PPN comparators only; physical-band applicability and full conformal-matter PPN unproved'}
    unknowns=['Full finite-density physical-eigenstate cubic/quartic interactions and the effect of metric/matter constraints on G3I probe scale',
        'Controlled nonempty physical frequency/momentum band including quartic branch and background scales',
        'Complete coupled gradients, characteristics and Cauchy/domain estimate for each new family',
        'Zero/singular/fixed-charge endpoint reduction and healthy full GR limit','Full conformal-matter/force PPN and microscopic matching']
    diag={'new_family_backgrounds':rows,'archived_G3_reused_not_reintegrated':True,'physical_go':False,
        'substantive_unknowns':unknowns,'decision':'STOP_AND_ASSESS_DOMAIN_UNRESOLVED',
        'not_an_all_action_no_go':True,'negative_mean_kinetic_eigenvalues_are_not_automatically_physical_ghosts':True}
    bodies={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag),
        'matrices.json':common.encode({'complex_storage':'last axis [real,imag]','snapshots':snapshots})}
    passed=sum(q['passed'] for q in checks.rows)
    summary=dict(schema='r4c1-gr-family-survey-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(checks.rows),checks=checks.rows,status='CONDITIONAL_GENERIC_ACTION_FAMILY_ENTRY_PHYSICAL_DOMAIN_OPEN',
        physical_decision=diag['decision'],physical_go=False,physical_candidate_admitted=False,
        full_coupled_interactions_computed=False,physical_EFT_cutoff_derived=False,healthy_full_GR_verified=False,
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
        substantive_unknowns=unknowns,stage3_entered=False,source_sha256=dict(sorted(pins.items())),
        source_metadata_preserved=len(before),inherited_sidecars_absent=absent,
        artifacts={k:common.sha(v) for k,v in bodies.items()},review_dependencies=['G1/G2/G3/S1/G3I','Complete generic R4C1 variation and G3N5','All inherited deferred review'],
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_gr_family_survey_attempt_01');ap.add_argument('--replay')
    args=ap.parse_args();dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
        **{k:summary[k] for k in ('validation','passed','total','status','physical_decision','physics_pass')}}))
    for q in summary['checks']:
        if not q['passed']:print(json.dumps(q))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
