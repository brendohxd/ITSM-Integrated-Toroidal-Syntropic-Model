"""G3DF: reconstruct finite-k physical density on archived prepared G3F planes.

No universal density-only closure, physical EFT window, PDE bound or gate pass.
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
import sympy as s
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Analysis/MasterTests/outputs'
PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_DENSITY_CONTRACT_2026-10-08.md': '26ecfebc6d7792c0a5d6e065b8512f803d5ddd6e6316d01300d83ad7ef2769ce',
    'Theory/Gates/RES-001/RES001_R4C1_G3_DENSITY_ACTION_REPORT_2026-09-30.md': '8a1c2245fc02307c5e70c7b4c1064872e82464c4c411d3095e97575c730b1876',
    'Analysis/MasterTests/test_01_r4c1_g3_density_action.py': '1a855ad2a5bbafbee0ad7164604a210f5a236529896cbbab5a62173d6e822fc8',
    'Analysis/MasterTests/outputs/r4c1_g3d_attempt_01/summary.json': 'c309ec0fbd3e3c3bff9ac05c86c4c0fe5f5e37edd5cc66a2a37cabb9bc6e5b72',
    'Analysis/MasterTests/outputs/r4c1_g3d_attempt_01/formulas.json': '68aaddb629ba729aa197804d46f8228d509111195757288221d21bb7f7a692e8',
    'Analysis/MasterTests/outputs/r4c1_g3f_attempt_01/summary.json': '3c3241a44e43b986971c8c340643b6b9c87ca97c803347cb9da5c0a934fa05e1',
    'Analysis/MasterTests/outputs/r4c1_g3f_attempt_01/columns.npy': '2a7df2c3ca35f5d438f54520241c880692c9804d03f3bf1bf696cf183345bccc',
    'Analysis/MasterTests/outputs/r4c1_g3f_attempt_01/embedding.json': 'c235d8c9f81314f01ade15dddd215263fc22754efa6caee485d793f85e432300',
    'Analysis/MasterTests/outputs/r4c1_g3s_attempt_01/matrices.json': '1877c4b4412e37b15ed6297d099ff12302c59cdad929858085b97178eae47355',
}
ETAS = (1., .25, .0625)
KS = (20., 40., 80.)
METHODS = ('DOP853', 'Radau')
GRID = np.linspace(0., 1., 101)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def verify(pins):
    for name, digest in pins.items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: '+name)

def tidy(expr):
    if isinstance(expr, s.MatrixBase):
        return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))

def model(audit):
    import test_01_r4c1_scalar_constraints as b
    eta = s.Symbol('eta', positive=True)
    symbols = {str(v):v for v in vars(b).values() if isinstance(v,s.Symbol)}
    symbols['eta'] = eta
    parse = lambda value:s.sympify(value,locals=symbols)
    raw = json.loads((OUT/'r4c1_g3s_attempt_01/matrices.json').read_bytes())
    emb = json.loads((OUT/'r4c1_g3f_attempt_01/embedding.json').read_bytes())
    dust = json.loads((OUT/'r4c1_g3d_attempt_01/formulas.json').read_bytes())
    mat = lambda data,key:s.Matrix([[parse(v) for v in row] for row in data[key]])
    R,G,W = (mat(raw,key) for key in ('R','G','W'))
    flow = {parse(key):parse(val) for key,val in raw['flow'].items()}
    def dt(expr):
        if isinstance(expr,s.MatrixBase):
            return expr.applyfunc(dt)
        return sum(s.diff(expr,z)*value for z,value in flow.items() if expr.has(z))
    beta = 2*eta**2/5
    subs = {b.MP:1,b.MU:2*eta/3,b.c1:s.Rational(1,5),b.c2:-s.Rational(7,48),
        b.c3:-s.Rational(1,80),b.c4:s.Rational(1,20),b.KQ:3*eta,b.b:5*eta/11,
        b.zeta:eta/13,b.beta:beta,b.m2:1,b.l4:s.Rational(1,3),
        b.l6:s.Rational(1,5),b.Lambda:2,b.mr2:2,b.lr:s.Rational(1,7),b.gr:3*eta/7}
    source = json.loads((OUT/'test_01_r4c1_scalar_constraints_matrices.json').read_bytes())
    aux = s.Matrix([parse(value) for value in source['auxiliary_solutions']]).subs(subs)
    phase = s.Matrix(s.symbols('x0:6 xd0:6',real=True))
    q,qd = R*phase[:6,0],dt(R)*phase[:6,0]+R*phase[6:,0]
    rec = tidy(aux.subs(dict(zip(list(b.qd)+list(b.q),list(qd)+list(q))),simultaneous=True))
    lapse,shift,de,z = rec
    audit.exact('full_reconstructed_dust_normalization',qd[4]-b.C*lapse-beta*b.C*q[3])
    audit.exact('full_reconstructed_regulator_constraint',z-b.k**2*q[3]/b.a**2+b.pd*b.k*q[5]/b.a)
    D = tidy((b.C**4*de+4*beta*b.rho*q[3])/b.rho)
    L0 = tidy(s.Matrix([D]).jacobian(phase))
    audit.exact('physical_density_linear_row',D-(L0*phase)[0])
    A = s.zeros(6).row_join(s.eye(6)).col_join((-W).row_join(-G))
    print('Reconstructing exact density derivative rows...',flush=True)
    L1 = tidy(dt(L0)+L0*A)
    L2 = tidy(dt(L1)+L1*A)
    E = mat(emb,'E_q').col_join(mat(emb,'E_v'))*s.sqrt(eta)/b.k
    T = mat(dust,'density_phase_map')
    leading = tidy(L0.col_join(L1)*E)
    limit = leading.applyfunc(lambda value:tidy(s.limit(value,b.k,s.oo)))
    audit.exact('physical_phase_embedding_large_k_limit',limit-T)
    audit.exact('leading_density_phase_determinant',T.det()+(12-eta)/(b.a**5*b.rho))
    audit.exact('leading_density_generator',mat(dust,'density_generator')-
        s.Matrix([[0,1],[b.rho/(2*(1-eta/12)),-2*b.H-beta*b.pd]]))
    args = [getattr(b,key) for key in ('a','H','u','ud','v','vd','r','rd','pd','rho','C')]+[eta,b.k]
    exprs = dict(L0=L0,L1=L1,L2=L2,G=G,E=E,T=T)
    functions = {key:s.lambdify(args,expr,'numpy',cse=True) for key,expr in exprs.items()}
    exported = {key:[[str(v) for v in row] for row in value.tolist()] for key,value in exprs.items() if key!='G'}
    exported.update(phase_order=['x[0:6]','xdot[0:6]'],density_definition=str(D),
        density_derivative_provenance='L1=dt(L0)+L0*A; L2=dt(L1)+L1*A; full background flow',
        scope='Prepared solution-plane restriction; not generic density-only full-system closure')
    return functions,exported

def discrepancy(a,b):
    return float(np.max(np.abs(a-b)/(1+np.abs(b))))

def row_error(a,b):
    return float(np.max(np.linalg.norm(a-b,axis=(-2,-1))/(1+np.linalg.norm(b,axis=(-2,-1)))))

def numerical(audit,functions):
    import test_01_r4c1_interacting_background as bg
    family = json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())
    old = np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
    archive = np.load(OUT/'r4c1_g3f_attempt_01/columns.npy',allow_pickle=False)
    meta = json.loads((OUT/'r4c1_g3f_attempt_01/summary.json').read_bytes())['trajectory']
    audit.test('archived_grid_and_axes_match_contract',
        meta['etas']==list(ETAS) and meta['ks']==list(KS) and meta['grid']==GRID.tolist()
        and meta['runs']==[*METHODS,'TRUNCATED_SLOW_REFERENCE']
        and archive.shape==(3,3,3,101,12,2))
    rows,backgrounds,transfers = [],[],[]
    j2 = np.array([[0.,1.],[-1.,0.]])
    for ie,eta in enumerate(ETAS):
        ix = next(i for i,v in enumerate(family['family']) if v['eta']==eta)
        params = family['family'][ix]['parameters']
        sols = []
        for method in METHODS:
            sol = solve_ivp(lambda t,y:bg.rhs(t,y,params),(0.,1.),old[ix,0,1:,0],
                method=method,rtol=1e-11,atol=1e-13,dense_output=True)
            audit.test(f'eta_{eta}_{method}_background_success',sol.success and sol.t[-1]==1.,sol.message)
            if not sol.success:
                raise RuntimeError('BACKGROUND_FAILED: '+sol.message)
            sols.append(sol)
        bv = sols[0].sol(GRID)
        bd = discrepancy(bv,sols[1].sol(GRID))
        prior = discrepancy(bv,old[ix,0,1:,:201:2])
        audit.test(f'eta_{eta}_background_method_agreement',bd<=1e-10,bd,'<=1e-10 normalized')
        audit.test(f'eta_{eta}_background_archive_agreement',prior<=1e-8,prior,'<=1e-8 normalized')
        audit.test(f'eta_{eta}_background_domain',bool(np.all(bv[[0,1,10]]>0)))
        backgrounds.append(dict(eta=eta,method_error=bd,archived_error=prior))
        def arguments(t,k):
            a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau = sols[0].sol(t)
            return [a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params['beta']*psi),eta,k]
        def get(key,t,k):
            return np.asarray(functions[key](*arguments(t,k)),float)
        beta = params['beta']
        def dust_rhs(t,value):
            a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau = sols[0].sol(t)
            B = np.array([[0.,1.],[rho/(2*(1-eta/12)),-2*H-beta*pd]])
            return (B@value.reshape(2,2)).ravel()
        direct = solve_ivp(dust_rhs,(0.,1.),np.eye(2).ravel(),method='DOP853',
            rtol=1e-11,atol=1e-13,dense_output=True)
        audit.test(f'eta_{eta}_direct_dust_success',direct.success and direct.t[-1]==1.,direct.message)
        if not direct.success:
            raise RuntimeError('DIRECT_DUST_FAILED')
        T = np.stack([get('T',t,20.) for t in GRID])
        sf = archive[ie,0,2][:,[5,11],:]
        expected = T@sf@np.linalg.inv(T[0])
        de = discrepancy(expected,direct.sol(GRID).T.reshape(-1,2,2))
        audit.test(f'eta_{eta}_independent_leading_density_transfer',de<=1e-9,de,'<=1e-9 normalized')
        members = []
        for ik,k in enumerate(KS):
            label = f'eta_{eta}_k_{k}'
            print('Density projection: '+label,flush=True)
            L = np.stack([np.vstack([get('L0',t,k),get('L1',t,k)]) for t in GRID])
            Ldot = np.stack([np.vstack([get('L1',t,k),get('L2',t,k)]) for t in GRID])
            G = np.stack([get('G',t,k) for t in GRID])
            Js = np.stack([np.block([[g,np.eye(6)],[-np.eye(6),np.zeros((6,6))]]) for g in G])
            E0 = get('E',0.,k)
            initial = L[0]@E0
            cond0 = float(np.linalg.cond(initial))
            audit.test(label+'_initial_density_chart',np.isfinite(cond0) and cond0<1e8 and np.linalg.det(initial)<0,
                dict(condition=cond0,determinant=float(np.linalg.det(initial))))
            if not np.isfinite(cond0) or cond0>=1e8 or np.linalg.det(initial)==0:
                rows.append(dict(eta=eta,k=k,status='INITIAL_RANK_FAILURE'));continue
            N = np.linalg.inv(initial)
            omega0 = N.T@E0.T@Js[0]@E0@N
            weight = float(omega0[0,1])
            Kslow = bv[0]**5*bv[10]/k**2
            runs,method_rows = [],[]
            for im,method in enumerate(METHODS):
                Y = archive[ie,ik,im]*np.sqrt(eta)/k
                initerr = discrepancy(Y[0],E0)
                audit.test(label+'_'+method+'_archive_initial_embedding',initerr<=1e-12,initerr)
                Z = Y@N
                F = L@Z
                runs.append(F)
                determinants = np.linalg.det(F)
                conditions = np.array([np.linalg.cond(v) for v in F])
                regular = bool(np.isfinite(F).all() and np.all(determinants>0) and np.max(conditions)<1e8)
                audit.test(label+'_'+method+'_sampled_density_rank',regular,
                    dict(min_det=float(determinants.min()),max_condition=float(conditions.max())))
                transported = np.transpose(Z,(0,2,1))@Js@Z
                drift = float(np.max(abs(transported-omega0))/max(abs(weight),1e-300))
                audit.test(label+'_'+method+'_two_form_transport',drift<=1e-7,drift,'<=1e-7 relative')
                audit.test(label+'_'+method+'_identity_initial_density_transfer',discrepancy(F[0],np.eye(2))<=1e-12)
                metrics = dict(method=method,min_density_transfer_determinant=float(determinants.min()),
                    max_density_transfer_condition=float(conditions.max()),symplectic_drift=drift,
                    density_error=row_error(F[:,:1,:],expected[:,:1,:]),
                    density_derivative_error=row_error(F[:,1:,:],expected[:,1:,:]),
                    density_phase_error=row_error(F,expected))
                if regular:
                    K = weight/determinants
                    B = (Ldot@Z)@np.linalg.inv(F)
                    friction,mass = -B[:,1,1],-B[:,1,0]
                    first = discrepancy(B[:,0,:],np.tile([0.,1.],(len(GRID),1)))
                    pullback = np.transpose(F,(0,2,1))@(K[:,None,None]*j2)@F
                    pe = float(np.max(abs(pullback-transported))/max(abs(weight),1e-300))
                    audit.test(label+'_'+method+'_positive_plane_density_kinetic',bool(np.all(K>0)),float(K.min()))
                    audit.test(label+'_'+method+'_generator_first_row',first<=1e-7,first)
                    audit.test(label+'_'+method+'_density_symplectic_pullback',pe<=1e-7,pe,'<=1e-7 relative')
                    leading_friction = 2*bv[1]+beta*bv[9]
                    leading_mass = -bv[10]/(2*(1-eta/12))
                    metrics.update(min_K_plane=float(K.min()),kinetic_ratio_range=[float((K/Kslow).min()),float((K/Kslow).max())],
                        max_relative_kinetic_error=float(np.max(abs(K/Kslow-1))),
                        friction_range=[float(friction.min()),float(friction.max())],
                        mass_range=[float(mass.min()),float(mass.max())],
                        max_normalized_friction_error=discrepancy(friction,leading_friction),
                        max_normalized_mass_error=discrepancy(mass,leading_mass),
                        generator_first_row_error=first,pullback_error=pe)
                    transfers.append(dict(eta=eta,k=k,method=method,grid=GRID.tolist(),transfer=F.tolist(),
                        K_plane=K.tolist(),friction=friction.tolist(),mass=mass.tolist()))
                method_rows.append(metrics)
            md = discrepancy(runs[0],runs[1])
            audit.test(label+'_density_method_agreement',md<=1e-7,md,'<=1e-7 normalized')
            row = dict(eta=eta,k=k,initial_physical_phase_map=initial.tolist(),leading_initial_map=T[0].tolist(),
                initial_phase_discrepancy=discrepancy(initial,T[0]),initial_normalization=N.tolist(),
                initial_density_symplectic_coefficient=weight,method_discrepancy=md,
                density_phase_error=max(v['density_phase_error'] for v in method_rows),methods=method_rows)
            rows.append(row);members.append(row)
        for low,high in zip(members,members[1:]):
            ratio = high['density_phase_error']/max(low['density_phase_error'],1e-300)
            audit.test(f'eta_{eta}_k_{low["k"]}_to_{high["k"]}_density_error_decreases',
                ratio<1,ratio,'high/low <1')
        target = members[-1]['density_phase_error'] if len(members)==3 else 1e99
        audit.test(f'eta_{eta}_k_80_density_target',target<=.05,target,'<=0.05 sampled diagnostic')
    audit.test('all_nine_grid_members_evaluated',len(rows)==9 and all('methods' in v for v in rows))
    return dict(rows=rows,backgrounds=backgrounds),transfers

def encode(value):
    return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()

def evaluate():
    verify(PINS)
    previous = json.loads((OUT/'r4c1_g3d_attempt_01/summary.json').read_bytes())
    inherited = {**previous['source_sha256'],**previous['transitive_source_sha256']}
    verify(inherited)
    import test_01_r4c1_equal_newton_scalar as gs
    audit = gs.Audit()
    functions,formulas = model(audit)
    numerical_data,transfers = numerical(audit,functions)
    payloads = {'formulas.json':encode(formulas),'density_transfers.json':encode(transfers)}
    passed = sum(c['passed'] for c in audit.checks)
    result = dict(schema='r4c1-g3df-v1',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=inherited,
        script_sha256=sha(Path(__file__).read_bytes()),artifacts={name:sha(value) for name,value in payloads.items()},
        numerical=numerical_data,runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__,scipy=scipy.__version__),
        status='CONDITIONAL_SAMPLED_PREPARED_DENSITY_PLANE' if passed==len(audit.checks) else 'DENSITY_DIAGNOSTIC_FAILURES_REQUIRE_DISPOSITION',
        new_full_system_integrations=0,archived_full_system_runs_projected=18,
        universal_density_only_closure_verified=False,continuous_time_error_bound=False,
        physical_EFT_cutoff='NOT_DERIVED',physical_validity_window_verified=False,
        arbitrary_fast_wave_data_verified=False,uniform_eta_endpoint_verified=False,full_PDE_verified=False,
        healthy_continuous_full_GR_limit_verified=False,positive_definite_energy_verified=False,
        physics_pass=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
    return result,payloads

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3df_attempt_01')
    parser.add_argument('--replay',action='store_true')
    args = parser.parse_args()
    directory = (ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):
        raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
    verify(PINS)
    if not args.replay and directory.exists():
        raise RuntimeError('OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT')
    result,payloads = evaluate()
    payloads['summary.json'] = encode(result)
    identical = None
    if args.replay:
        identical = all((directory/name).read_bytes()==value for name,value in payloads.items())
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(payloads['summary.json']))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,value in payloads.items():
            (directory/name).write_bytes(value)
            (directory/(name+'.sha256')).write_text(sha(value)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('validation','passed','total','status','physics_pass')}))
    for check in result['checks']:
        if not check['passed']:
            print(json.dumps(check))
    if args.replay and not identical:
        return 2
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':
    raise SystemExit(main())
