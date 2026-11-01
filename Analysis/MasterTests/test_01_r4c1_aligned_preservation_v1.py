"""Actual moving-row preservation test; input verification is a separate nonphysics mode."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_ALIGNED_PRESERVATION_V1_CONTRACT_2026-10-30.md'
PARENT='Analysis/MasterTests/outputs/r4c1_aligned_tangency_v2_attempt_01/summary.json'
PSHA='836f9e718212d689a86cad0eec22657bdce293b5fb422e693c7abcb43545dc9c'
DRIFT='Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json'
DUST='Analysis/MasterTests/outputs/r4c1_b1_dust_reconstruction_v1_attempt_01/summary.json'
OWNER='Theory/Gates/RES-001/RES001_R4C1_ALIGNED_TANGENCY_V2_REPORT_2026-10-30.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))

def verify_inputs():
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent receipt changed'
    parent=json.loads((ROOT/PARENT).read_bytes())
    assert parent['passed']==parent['total']==71 and not parent['physics_pass']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name in (SELF,CONTRACT,OWNER):
        pins[name]=SHA((ROOT/name).read_bytes())
    snapshots={}
    for name,want in pins.items():
        f=ROOT/name;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want,name
        assert sc.read_text().split()[0].lower()==want,name
        for z in (f,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    drift=json.loads((ROOT/DRIFT).read_bytes())
    assert set(('M','B','Q','M_dot','B_dot','background_flow','initial'))<=set(drift['formulas'])
    assert len(drift['formulas']['M'])==10
    assert len(drift['formulas']['background_flow'])==11
    assert len(parent['formulas']['necessary_frame_acceleration'])==3
    return parent,pins,snapshots

def inputs_result(parent,pins):
    return dict(kind='R4C1_ALIGNED_PRESERVATION_V1_INPUTS_ONLY',
        source_sha256=pins,direct_source_pins=len(pins),parent_receipt_verified=True,
        parent_checks=dict(passed=parent['passed'],total=parent['total']),
        scientific_calculation='NOT_RUN',physical_result='NOT_EVALUATED',
        physical_window_demonstrated=False,physics_pass=False,gate_effect='NONE',
        review='DEFERRED',Rule9_cleared=False,G1_G6='INCOMPLETE')

def calculate(parent,pins,snapshots):
    mp.mp.dps=100;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for e in entries if (v:=s.expand(clean(e)))!=0]
        check(name,not bad,bad)
    a=s.Symbol('a',positive=True);H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    u,v,r,du,dv,dr,p,psi,rho=s.symbols('u v r du dv dr p psi rho',real=True)
    variables=(a,H,u,v,r,du,dv,dr,p,psi,rho)
    loc={str(z):z for z in variables+(k,)}
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=loc) for z in row] for row in rows])
    drift=json.loads((ROOT/DRIFT).read_bytes())['formulas']
    initial={loc[z]:s.sympify(val,locals=loc) for z,val in drift['initial'].items()}
    flow=s.Matrix([s.sympify(z,locals=loc) for z in drift['background_flow']])
    dt=lambda z:sum(s.diff(z,w)*f for w,f in zip(variables,flow))
    M,B,Q,Md,Bd=(parse(drift[n]) for n in ('M','B','Q','M_dot','B_dot'))
    zero('actual_M_drift',M.applyfunc(dt)-Md);zero('actual_B_drift',B.applyfunc(dt)-Bd)
    G=s.zeros(20);G[:10,10:20]=s.eye(10)
    G[10:20,:10]=-M.inv()*(Bd-Q)
    G[10:20,10:20]=-M.inv()*(Md+B-B.conjugate().T)
    G=G.applyfunc(clean);Gi=G.subs(initial).applyfunc(clean)
    zero('parent_initial_full_generator',Gi-parse(drift['initial_generator']))
    selectors=(3,4,5,13,14,15)
    P=s.eye(20)
    for j in selectors:P[j,j]=0
    L=(G[15,:]*P).applyfunc(clean)
    Eparent=parse(parent['formulas']['aligned_embedding'])
    zero('previous_longitudinal_equation_recovered',L*Eparent-parse(parent['formulas']['necessary_frame_acceleration'])[2,:])
    R=s.zeros(7,20)
    for i,j in enumerate(selectors):R[i,j]=1
    R[6,:]=L
    Rd=R.applyfunc(dt).applyfunc(clean)
    T=(Rd+R*G).applyfunc(clean)
    Ri=R.subs(initial).applyfunc(clean);Rdi=Rd.subs(initial).applyfunc(clean)
    Ti=T.subs(initial).applyfunc(clean)
    # Eliminate sigma_dot via its nonzero ik coefficient, without setting sigma to zero.
    pivot=19;pv=clean(Ri[6,pivot])
    check('nonzero_k_pivot',pv!=0,str(pv))
    free=[j for j in range(20) if j not in selectors+(pivot,)]
    E=s.zeros(20,len(free))
    for j,slot in enumerate(free):
        E[slot,j]=1;E[pivot,j]=clean(-Ri[6,slot]/pv)
    zero('candidate_kernel_exact',Ri*E)
    check('candidate_rank_seven',Ri.rank()==7,Ri.rank())
    check('candidate_contains_force_displacement_direction',9 in free)
    defect=(Ti*E).applyfunc(clean)
    zero('first_six_constraint_derivatives',defect[:6,:])
    closure=all(s.expand(z)==0 for z in defect)
    # A result may be either closure at this instant or a counterexample; neither proves a full domain.
    witnesses=[]
    solve=parse(drift['constraint_solution']).subs(initial)
    dd=json.loads((ROOT/DUST).read_bytes())['formulas']
    density=parse(dd['density_row']).subs(initial)
    eps=parse(dd['epsilon_scaled_row']).subs(initial)
    for j,slot in enumerate(free):
        response=defect[:,j]
        if all(s.expand(z)==0 for z in response):continue
        seed=E[:,j];xdot=Gi*seed
        zero('witness_initial_candidate_'+str(slot),Ri*seed)
        zero('witness_initial_frame_acceleration_'+str(slot),Gi[13:16,:]*seed)
        zero('witness_exact_moving_row_response_'+str(slot),Rdi*seed+Ri*xdot-response)
        rec=(solve*seed).applyfunc(clean)
        dens=clean((density*seed)[0]);epsilon=clean((eps*seed)[0])
        check('finite_reconstruction_'+str(slot),
            all(not z.has(s.zoo,s.oo,s.nan) for z in list(rec)+[dens,epsilon]))
        witnesses.append(dict(free_coordinate=slot,seed=[str(clean(z)) for z in seed],
            defect=[str(clean(z)) for z in response],constraint_solution=[str(z) for z in rec],
            delta_rho=str(dens),delta_epsilon=str(epsilon),nonlinear_admission=False))
    check('failure_has_explicit_witness',closure or bool(witnesses),len(witnesses))
    zero('moving_row_Fourier_reality',R.subs(k,-k)-R.conjugate())
    zero('moving_defect_Fourier_reality',T.subs(k,-k)-T.conjugate())
    omitted=(Ri*Gi*E).applyfunc(clean)
    drift_contribution=(Rdi*E).applyfunc(clean)
    zero('drift_partition_exact',defect-omitted-drift_contribution)
    # A differently assembled numerical time difference, not frozen-generator powers.
    args=variables+(k,);rf=s.lambdify(args,R,modules='mpmath');tf=s.lambdify(args,T,modules='mpmath')
    gf=s.lambdify(args,G,modules='mpmath')
    vals=[mp.mpf(str(s.N(initial[z],98))) for z in variables]
    velocity=[mp.mpf(str(s.N(z,98))) for z in flow.subs(initial)]
    controls=[]
    for kval in (1,7,40):
        errs=[]
        for hs in ('1e-14','1e-22'):
            h=mp.mpf(hs);plus=[z+h*f for z,f in zip(vals,velocity)];minus=[z-h*f for z,f in zip(vals,velocity)]
            numeric=(rf(*plus,kval)-rf(*minus,kval))/(2*h)+rf(*vals,kval)*gf(*vals,kval)
            target=tf(*vals,kval)
            err=max(abs(z) for z in numeric-target)/(1+max(abs(z) for z in target))
            check(f'independent_moving_rows_k{kval}_{hs}',err<1000*h*h,mp.nstr(err,65));errs.append(mp.nstr(err,65))
        controls.append(dict(k=kval,steps=['1e-14','1e-22'],normalized_errors=errs))
    for name,(digest,mtime) in snapshots.items():
        fp=ROOT/name;assert SHA(fp.read_bytes())==digest and fp.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_preserved',True,len(snapshots))
    encode=lambda mat:[[str(clean(z)) for z in row] for row in mat.tolist()]
    return dict(kind='R4C1_ALIGNED_PRESERVATION_V1',scientific_calculation='RUN',
        passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        source_sha256=pins,independent_controls=controls,
        result='INITIAL_MOVING_ROW_CLOSURE_ONLY' if closure else 'SEVEN_ROW_ALIGNED_CANDIDATE_NOT_INVARIANT',
        initial_candidate_rank=7,initial_kernel_dimension=len(free),
        initial_moving_defect_zero=closure,witnesses=witnesses,
        formulas=dict(R=encode(R),R_dot=encode(Rd),initial_R=encode(Ri),initial_R_dot=encode(Rdi),
            initial_defect=encode(Ti),initial_kernel=encode(E),initial_kernel_defect=encode(defect),
            free_coordinates=free,omitted_R_dot_changes_test=any(z!=0 for z in drift_contribution)),
        physical_domain_admitted=False,nonlinear_domain_admitted=False,
        physical_window_demonstrated=False,all_aligned_domains_rejected=False,
        G1_G6='INCOMPLETE',MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
        physics_pass=False,gate_effect='NONE',review='DEFERRED',Rule9_cleared=False)

def main():
    ap=argparse.ArgumentParser()
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify-inputs',action='store_true')
    mode.add_argument('--calculate',action='store_true')
    dest=ap.add_mutually_exclusive_group(required=True)
    dest.add_argument('--output-dir',type=Path);dest.add_argument('--replay',type=Path)
    args=ap.parse_args();parent,pins,snapshots=verify_inputs()
    result=inputs_result(parent,pins) if args.verify_inputs else calculate(parent,pins,snapshots)
    payload=ENC(result)
    if args.replay:
        assert args.replay.read_bytes()==payload,'replay differs'
        print('READ_ONLY_REPLAY_EXACT',SHA(payload))
    else:
        args.output_dir.mkdir(parents=True,exist_ok=False);p=args.output_dir/'summary.json'
        p.write_bytes(payload);Path(str(p)+'.sha256').write_text(SHA(payload)+'\n',encoding='ascii')
        print(json.dumps(dict(kind=result['kind'],scientific_calculation=result['scientific_calculation'],
            passed=result.get('passed'),total=result.get('total'),physics_pass=False,receipt=str(p))))
    return 0 if args.verify_inputs or result['passed']==result['total'] else 1

if __name__=='__main__':
    raise SystemExit(main())

