"""G3F: registered finite-k full evolution of a truncated slow phase plane.

No physical cutoff, uniform eta endpoint, quantum-ghost or full PDE claim.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
    'Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_CONTRACT_2026-09-30.md':
        '75050556086b27f794b2378ac389f6bb864ae03e4441c395ff5fc64538b1cd55',
    'Theory/Gates/RES-001/RES001_R4C1_G3_SLOW_ACTION_REPORT_2026-09-30.md':
        '2158f16970e883eb661aaabd04a1014aef3d8a47e6346ad7cb27453f464db83c',
    'Analysis/MasterTests/outputs/r4c1_g3a_attempt_03/summary.json':
        '3c46b9834c6805c0ae46aeb0ff6226ec2abf814db873abc1d8fc104b8eacab72',
    'Analysis/MasterTests/outputs/r4c1_g3a_attempt_03/formulas.json':
        'f4b7a2e69c7a51ebf33d25b94e03a60f7ca2680fecb481e42d4258cf9219ace6',
    'Analysis/MasterTests/test_01_r4c1_g3_slow_action.py':
        '64e59e69851734cd24a4abbd31d7b02b17490395b1d841b1a0f06bd246681b90',
}
ETAS=(1.,.25,.0625)
KS=(20.,40.,80.)
METHODS=('DOP853','Radau')
GRID=np.linspace(0.,1.,101)


def sha(data):return hashlib.sha256(data).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:
            raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: '+name)


def tidy(expr):
    if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))


def model(audit):
    import test_01_r4c1_scalar_constraints as b
    eta=s.Symbol('eta',positive=True)
    X,Xd=s.symbols('X Xdot',real=True)
    nxt=s.symbols('next_u next_v next_r next_T',real=True)
    symbols={str(v):v for v in vars(b).values() if isinstance(v,s.Symbol)}
    symbols.update({str(v):v for v in [eta,X,Xd,*nxt]})
    parse=lambda value:s.sympify(value,locals=symbols)
    raw=json.loads((OUT/'r4c1_g3s_attempt_01/matrices.json').read_bytes())
    slow=json.loads((OUT/'r4c1_g3e_attempt_01/formulas.json').read_bytes())
    matrix=lambda key:s.Matrix([[parse(v) for v in row] for row in raw[key]])
    G,W=matrix('G'),matrix('W')
    flow={parse(key):parse(val) for key,val in raw['flow'].items()}
    def dt(expr):
        if isinstance(expr,s.MatrixBase):return expr.applyfunc(dt)
        return sum(s.diff(expr,z)*v for z,v in flow.items() if expr.has(z))
    I=s.eye(6);Z=s.zeros(6)
    A=Z.row_join(I).col_join((-W).row_join(-G))
    J=G.row_join(I).col_join((-I).row_join(Z))
    audit.exact('full_canonical_two_form_transport_identity',dt(J)+A.T*J+J*A)
    audit.exact('full_canonical_two_form_antisymmetric',J+J.T)
    mass=parse(slow['normalized_coefficients'][0]);B=s.Matrix([[0,1],[-mass,0]])
    Y=[parse(v).subs(dict.fromkeys(nxt,0)) for v in slow['propagating_embedding']]
    F=[parse(v).subs(dict.fromkeys(nxt,0)) for v in slow['force_embedding']]
    x=s.Matrix([Y[0]/b.k,Y[1]/b.k,Y[2]/b.k,
                F[0]/b.k+F[1]/b.k**2+F[2]/b.k**3,Y[3]/b.k,X])
    Eq=x.jacobian([X,Xd])
    audit.exact('embedding_linear_in_slow_phase',x-Eq*s.Matrix([X,Xd]))
    Ev=tidy(dt(Eq)+Eq*B)
    E=Eq.col_join(Ev)
    residual=tidy(-W*Eq-G*Ev-dt(Ev)-Ev*B)
    audit.exact('phase_embedding_position_defect_zero',Ev-dt(Eq)-Eq*B)
    args=[getattr(b,key) for key in ('a','H','u','ud','v','vd','r','rd','pd','rho','C')]+[eta,b.k]
    functions={key:s.lambdify(args,expr,'numpy',cse=True)
               for key,expr in dict(G=G,W=W,E=E,residual=residual,mass=mass).items()}
    embedding={key:[[str(v) for v in row] for row in value.tolist()]
               for key,value in dict(E_q=Eq,E_v=Ev).items()}
    embedding.update(coordinates=['X','Xdot'],phase_order=['x[0:6]','xdot[0:6]'],
        uncomputed_next_propagating_amplitudes='SET_TO_ZERO_TRUNCATION',
        fixed_comoving_k=True,physical_EFT_cutoff='NOT_DERIVED')
    return functions,embedding


def discrepancy(first,second):
    return float(np.max(np.abs(first-second)/(1+np.abs(second))))


def numerical(audit,functions):
    import test_01_r4c1_interacting_background as bg
    family=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())
    parent=np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
    rows=[];backgrounds=[];traces=[]
    for eta in ETAS:
        ie=next(i for i,v in enumerate(family['family']) if v['eta']==eta)
        params=family['family'][ie]['parameters'];initial=parent[ie,0,1:,0]
        backgrounds_pair=[]
        for method in METHODS:
            sol=solve_ivp(lambda t,y:bg.rhs(t,y,params),(0.,1.),initial,
                method=method,rtol=1e-11,atol=1e-13,dense_output=True)
            audit.test(f'eta_{eta}_{method}_background_success',sol.success and sol.t[-1]==1.,sol.message)
            if not sol.success:raise RuntimeError('BACKGROUND_INTEGRATION_FAILED: '+sol.message)
            backgrounds_pair.append(sol)
        bd=discrepancy(backgrounds_pair[0].sol(GRID),backgrounds_pair[1].sol(GRID))
        audit.test(f'eta_{eta}_background_method_agreement',bd<=1e-10,bd,'normalized <=1e-10')
        reference=backgrounds_pair[0]
        bv=reference.sol(GRID)
        domain=bool(np.all(bv[[0,1,10]]>0))
        audit.test(f'eta_{eta}_background_domain',domain)
        backgrounds.append(dict(eta=eta,method_discrepancy=bd,min_a=float(bv[0].min()),
            min_H=float(bv[1].min()),min_rho_m=float(bv[10].min())))
        def arguments(t,k):
            a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=reference.sol(t)
            return [a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params['beta']*psi),eta,k]
        def get(key,t,k):return np.asarray(functions[key](*arguments(t,k)),dtype=float)
        def generator(t,k):
            return np.block([[np.zeros((6,6)),np.eye(6)],[-get('W',t,k),-get('G',t,k)]])
        def two_form(t,k):
            return np.block([[get('G',t,k),np.eye(6)],[-np.eye(6),np.zeros((6,6))]])
        def slow_rhs(t,value):
            mass=float(get('mass',t,20.))
            return (np.array([[0.,1.],[-mass,0.]])@value.reshape(2,2)).ravel()
        slow=solve_ivp(slow_rhs,(0.,1.),np.eye(2).ravel(),method='DOP853',
                      rtol=1e-11,atol=1e-13,dense_output=True)
        audit.test(f'eta_{eta}_slow_reference_success',slow.success and slow.t[-1]==1.,slow.message)
        if not slow.success:raise RuntimeError('SLOW_REFERENCE_FAILED: '+slow.message)
        slow_values=slow.sol(GRID).T.reshape(-1,2,2)
        members=[];eta_traces=[]
        for k in KS:
            E0=get('E',0.,k);omega0=E0.T@two_form(0.,k)@E0
            coefficient=float(omega0[0,1]);K=1-12/eta
            initial_error=abs(coefficient-K)/abs(K)
            audit.test(f'eta_{eta}_k_{k}_negative_initial_symplectic_coefficient',coefficient<0,coefficient)
            predicted=np.stack([get('E',t,k)@F for t,F in zip(GRID,slow_values)])
            defects=np.array([np.linalg.norm(get('residual',t,k))/(1+np.linalg.norm(get('E',t,k))) for t in GRID])
            runs=[];method_rows=[]
            for method in METHODS:
                print(f'Full coupled evolution: eta={eta}, k={k}, method={method}',flush=True)
                def rhs(t,value):return (generator(t,k)@value.reshape(12,2)).ravel()
                kwargs={'jac':lambda t,value:np.kron(generator(t,k),np.eye(2))} if method=='Radau' else {}
                sol=solve_ivp(rhs,(0.,1.),E0.ravel(),method=method,rtol=1e-9,atol=1e-11,
                              dense_output=True,**kwargs)
                audit.test(f'eta_{eta}_k_{k}_{method}_full_integration_success',sol.success and sol.t[-1]==1.,sol.message)
                if not sol.success:raise RuntimeError('FULL_INTEGRATION_FAILED: '+sol.message)
                values=sol.sol(GRID).T.reshape(-1,12,2);runs.append(values)
                audit.test(f'eta_{eta}_k_{k}_{method}_finite_full_columns',bool(np.isfinite(values).all()))
                transported=np.stack([v.T@two_form(t,k)@v for t,v in zip(GRID,values)])
                drift=float(np.max(np.abs(transported-omega0))/abs(coefficient))
                audit.test(f'eta_{eta}_k_{k}_{method}_symplectic_transport',drift<=1e-7,drift,'relative <=1e-7')
                error=float(np.max(np.linalg.norm(values-predicted,axis=(1,2))/(1+np.linalg.norm(predicted,axis=(1,2)))))
                slow_error=float(np.max(np.linalg.norm(values[:,[5,11]]-slow_values,axis=(1,2))/(1+np.linalg.norm(slow_values,axis=(1,2)))))
                method_rows.append(dict(method=method,nfev=int(sol.nfev),njev=int(sol.njev),
                    max_full_column_approximation_error=error,max_slow_coordinate_velocity_error=slow_error,
                    max_relative_symplectic_transport_drift=drift,final_full_columns=values[-1].tolist()))
            md=discrepancy(runs[0],runs[1])
            audit.test(f'eta_{eta}_k_{k}_full_method_agreement',md<=1e-7,md,'normalized <=1e-7')
            member=dict(eta=eta,k=k,min_k_over_a=float(np.min(k/bv[0])),
                initial_symplectic_coefficient=coefficient,formal_symplectic_coefficient=K,
                initial_relative_symplectic_asymptotic_error=initial_error,
                max_normalized_embedding_defect=float(defects.max()),method_discrepancy=md,
                max_full_column_approximation_error=max(v['max_full_column_approximation_error'] for v in method_rows),
                methods=method_rows)
            rows.append(member);members.append(member)
            eta_traces.append(np.stack([*runs,predicted]))
        for low,high in zip(members,members[1:]):
            label=f'eta_{eta}_k_{low["k"]}_to_{high["k"]}'
            ratio=high['max_full_column_approximation_error']/low['max_full_column_approximation_error']
            audit.test(label+'_approximation_error_decreases',ratio<1,ratio,'high/low <1')
            sr=high['initial_relative_symplectic_asymptotic_error']/low['initial_relative_symplectic_asymptotic_error']
            audit.test(label+'_symplectic_asymptotic_error_decreases',sr<1,sr,'high/low <1')
        error80=members[-1]['max_full_column_approximation_error']
        audit.test(f'eta_{eta}_k_80_registered_approximation_target',error80<=.05,error80,'<=0.05; diagnostic only')
        traces.append(np.stack(eta_traces))
    return dict(rows=rows,backgrounds=backgrounds),np.stack(traces)


def evaluate():
    verify(PINS)
    previous=json.loads((OUT/'r4c1_g3a_attempt_03/summary.json').read_bytes())
    inherited={**previous['source_sha256'],**previous['transitive_source_sha256']}
    verify(inherited)
    import test_01_r4c1_equal_newton_scalar as gs
    audit=gs.Audit();functions,embedding=model(audit)
    results,traces=numerical(audit,functions)
    buffer=io.BytesIO();np.save(buffer,traces,allow_pickle=False)
    payloads={'embedding.json':(json.dumps(embedding,indent=2,allow_nan=False)+'\n').encode(),
              'columns.npy':buffer.getvalue()}
    passed=sum(c['passed'] for c in audit.checks)
    record=dict(schema='r4c1-g3f-v1',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,
        transitive_source_sha256=inherited,script_sha256=sha(Path(__file__).read_bytes()),
        artifacts={name:sha(value) for name,value in payloads.items()},numerical=results,
        trajectory=dict(file='columns.npy',shape=list(traces.shape),etas=list(ETAS),ks=list(KS),
            runs=[*METHODS,'TRUNCATED_SLOW_REFERENCE'],grid=GRID.tolist(),
            axes=['eta','k','run','sample','phase_component','initial_column']),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__),
        status='CONDITIONAL_FINITE_K_DIAGNOSTICS_PHYSICAL_WINDOW_OPEN' if passed==len(audit.checks) else 'FINITE_K_DIAGNOSTIC_FAILURES_REQUIRE_DISPOSITION',
        finite_k_symplectic_plane_negative=all(row['initial_symplectic_coefficient']<0 for row in results['rows']),
        physical_EFT_cutoff='NOT_DERIVED',physical_validity_window_verified=False,
        stationary_quantum_ghost_verified=False,uniform_eta_endpoint_verified=False,full_PDE_verified=False,
        healthy_continuous_GR_limit_verified=False,all_action_no_go=False,physics_pass=False,
        canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        review_status='DEFERRED',Rule9_cleared=False,gate_effect='NONE',
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
    return record,payloads


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3f_attempt_01')
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError('OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT')
    record,payloads=evaluate()
    payloads['summary.json']=(json.dumps(record,indent=2,allow_nan=False)+'\n').encode()
    identical=None
    if args.replay:
        identical=all((directory/name).read_bytes()==value for name,value in payloads.items())
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,value in payloads.items():
            (directory/name).write_bytes(value)
            (directory/(name+'.sha256')).write_text(sha(value)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({key:record[key] for key in ('validation','passed','total','status','physics_pass')}))
    for check in record['checks']:
        if not check['passed']:print(json.dumps(check))
    if args.replay and not identical:return 2
    return 0 if record['passed']==record['total'] else 1


if __name__=='__main__':raise SystemExit(main())
