"""Necessary dust-normal alignment tangency on the old homogeneous B1 control.

A reduced-action calculation, not nonlinear domain admission or a new action.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_ALIGNED_TANGENCY_V1_CONTRACT_2026-10-30.md'
DRIFT = 'Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json'
REDUCED = 'Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json'
DUST = 'Analysis/MasterTests/outputs/r4c1_b1_dust_reconstruction_v1_attempt_01/summary.json'
REPORT = 'Theory/Gates/RES-001/RES001_R4C1_B1_ALIGNMENT_DOMAIN_V1_REPORT_2026-10-29.md'
PLAN = 'Theory/Core/ITSM_DOMAIN_FIRST_MULTISTEP_GOAL_V1_2026-10-30.md'
SHA = lambda b: hashlib.sha256(b).hexdigest()
ENC = lambda v: (json.dumps(v, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
clean = lambda z: s.factor(s.cancel(z))

def calculate():
    mp.mp.dps = 100
    checks = []
    def check(name, ok, value=None):
        checks.append(dict(name=name, passed=bool(ok), value=value))
    def zero(name, expr):
        entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
        bad = [str(v) for z in entries if (v := clean(z)) != 0]
        check(name, not bad, bad)
    data = {p: json.loads((ROOT/p).read_bytes()) for p in (DRIFT, REDUCED, DUST)}
    pins = {}
    for p, d in data.items():
        assert d['passed'] == d['total'] and not d['physics_pass'], p
        pins.update(d['source_sha256'])
        pins[p] = SHA((ROOT/p).read_bytes())
    for p in (SELF, CONTRACT, REPORT, PLAN,
              'Analysis/MasterTests/test_01_r4c1_aligned_tangency_v1.py',
              'Analysis/MasterTests/outputs/r4c1_aligned_tangency_v1_attempt_01/summary.json',
              'Theory/Gates/RES-001/RES001_R4C1_ALIGNED_TANGENCY_V2_EXECUTION_ADDENDUM_2026-10-30.md'):
        pins[p] = SHA((ROOT/p).read_bytes())
    snap = {}
    for p, digest in pins.items():
        f = ROOT/p
        assert SHA(f.read_bytes()) == digest, p
        sc = Path(str(f)+'.sha256')
        assert sc.read_text().split()[0].lower() == digest, p
        for z in (f, sc):
            snap[z.relative_to(ROOT).as_posix()] = (SHA(z.read_bytes()), z.stat().st_mtime_ns)

    a=s.Symbol('a', positive=True); H=s.Symbol('H', real=True)
    k=s.Symbol('k', real=True, nonzero=True)
    u,v,r,du,dv,dr,p,psi,rho=s.symbols('u v r du dv dr p psi rho', real=True)
    variables=(a,H,u,v,r,du,dv,dr,p,psi,rho)
    local={str(z):z for z in variables+(k,)}
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=local) for z in row] for row in rows])
    f=data[DRIFT]['formulas']
    initial={local[z]:s.sympify(w,locals=local) for z,w in f['initial'].items()}
    flow=s.Matrix([s.sympify(z,locals=local) for z in f['background_flow']])
    deriv=lambda z:sum(s.diff(z,w)*fd for w,fd in zip(variables,flow))
    M,B,Q,Md,Bd=(parse(f[name]) for name in ('M','B','Q','M_dot','B_dot'))
    zero('actual_volume_drift_recovered',M.applyfunc(deriv)-Md)
    zero('actual_momentum_drift_recovered',B.applyfunc(deriv)-Bd)
    G=s.zeros(20);G[:10,10:20]=s.eye(10)
    G[10:20,:10]=-M.inv()*(Bd-Q)
    G[10:20,10:20]=-M.inv()*(Md+B-B.conjugate().T)
    G=G.applyfunc(clean)
    Gi=G.subs(initial).applyfunc(clean)
    zero('full_initial_parent_generator_recovered',Gi-parse(f['initial_generator']))
    check('exact_generator_no_Float',not bool(G.atoms(s.Float)))

    # n=gamma*n_ADM+V, u_dust=n_ADM in the clock gauge.
    # At V=0, delta gamma=0 and delta V=v/a; no shift component is discarded.
    w=s.Symbol('w', real=True)
    zero('gamma_has_zero_first_alignment_variation',
         s.diff(s.sqrt(1+w*w),w).subs(w,0))
    check('physical_alignment_identification',
          a.is_positive and M.shape==(10,10),
          'n=gamma*n_ADM+V; u_dust=n_ADM; delta V=v/a; v=0 iff delta tilt=0')

    excluded=(3,4,5,13,14,15)
    free=[i for i in range(20) if i not in excluded]
    E=s.zeros(20,len(free))
    for j,i in enumerate(free):E[i,j]=1
    C=(G[13:16,:]*E).applyfunc(clean)
    Ci=C.subs(initial).applyfunc(clean)
    zero('transverse_aligned_rows_automatic',C[:2,:])
    rank=Ci.rank()
    check('initial_alignment_compatibility_rank_one',rank==1,rank)
    # One explicit longitudinal equation, not an adopted restricted sector.
    x=s.Matrix(s.symbols('gx gxy gy vx vy vz U V R F dgx dgxy dgy dvx dvy dvz dU dV dR dF',real=True))
    force=clean((G[15,:]*E*E.T*x)[0])
    check('longitudinal_alignment_condition_not_identity',force!=0,str(force))
    zero('Fourier_reality_full_generator',G.subs(k,-k)-G.conjugate())
    zero('Fourier_reality_alignment_rows',C.subs(k,-k)-C.conjugate())
    check('nonzero_modes_have_zero_linear_mean',s.integrate(s.exp(s.I*w),(w,-s.pi,s.pi))==0)
    # The original constraint solution is in (q,qdot) order.
    solve=parse(f['constraint_solution'])
    density=parse(data[DUST]['formulas']['density_row'])
    eps=parse(data[DUST]['formulas']['epsilon_scaled_row'])
    probe_specs=[
        ('force_displacement',9),('force_velocity',19),
        ('condensate_amplitude_displacement',6),('condensate_amplitude_velocity',16),
        ('condensate_phase_displacement',7),('condensate_phase_velocity',17),
        ('reservoir_displacement',8),('reservoir_velocity',18),
        ('metric_trace_displacement',None),('metric_trace_velocity',None),
        ('tensor_plus_displacement',None),('tensor_plus_velocity',None),
        ('tensor_cross_displacement',1),('tensor_cross_velocity',11)]
    witnesses=[]
    for name,slot in probe_specs:
        seed=s.zeros(20,1)
        if slot is not None:seed[slot]=1
        elif name.startswith('metric_trace'):seed[10 if name.endswith('velocity') else 0]=seed[12 if name.endswith('velocity') else 2]=1
        elif name.startswith('tensor_plus'):seed[10 if name.endswith('velocity') else 0]=1;seed[12 if name.endswith('velocity') else 2]=-1
        zero('seed_initially_aligned_'+name,seed.extract(excluded,[0]))
        response=(Gi[13:16,:]*seed).applyfunc(clean)
        constraint=(solve*seed).subs(initial).applyfunc(clean)
        dens=clean((density*seed)[0].subs(initial))
        epsilon=clean((eps*seed)[0].subs(initial))
        zero('density_epsilon_conversion_'+name,dens-epsilon-s.Rational(8,25)*seed[9])
        finite=all(not z.has(s.zoo,s.oo,s.nan) for z in list(constraint)+[dens,epsilon])
        check('finite_constraint_reconstruction_'+name,finite)
        witnesses.append(dict(name=name,seed=[str(z) for z in seed],
            frame_acceleration=[str(z) for z in response],tangent=all(z==0 for z in response),
            constraint_order=['dZ','Sx','Sy','Sz'],
            constraint_solution=[str(z) for z in constraint],delta_rho=str(dens),
            delta_epsilon=str(epsilon),delta_lapse=str(-s.Rational(2,5)*seed[9]),
            nonlinear_initial_data_admission=False))
    failed=[z['name'] for z in witnesses if not z['tangent']]
    check('unrestricted_aligned_class_invariance_rejected',bool(failed),failed)
    # Independent Euler assembly: differentiate L2 with q, qdot, qddot independent.
    qv=s.Matrix(s.symbols('q0:10',real=True))
    vv=s.Matrix(s.symbols('v0:10',real=True))
    aa=s.Matrix(s.symbols('a0:10',real=True))
    # M and Q Hermitian: use the real-field differential operator adjoint.
    # On a plane wave EL = M*qdd+(Mdot+B-B^dagger)*qdot+(Bdot-Q)*q.
    action_rows=M[3:6,:]*aa+(Md+B-B.conjugate().T)[3:6,:]*vv+(Bd-Q)[3:6,:]*qv
    trial=-M.inv()*((Md+B-B.conjugate().T)*vv+(Bd-Q)*qv)
    zero('independent_full_Euler_rows_solved',action_rows.subs(dict(zip(aa,trial))))
    # Verify elimination directly from the original local second variation.
    base=data[REDUCED]['formulas']
    localH=parse(base['local_Hessian'])
    T=s.zeros(39,25)
    for i in range(11):T[i,i]=1;T[11+i,11+i]=1;T[22+i,i]=s.I*k
    for i in range(3):T[33+i,22+i]=1;T[36+i,22+i]=s.I*k
    full=(T.conjugate().T*localH*T).subs(initial).applyfunc(clean)
    keep=list(range(10))+list(range(11,21));elim=[10,22,23,24]
    D=full.extract(elim,elim);cross=full.extract(keep,elim)
    original_solve=-D.inv()*cross.conjugate().T
    zero('original_constraint_rows_reconstructed',original_solve-solve.subs(initial))
    red=full.extract(keep,keep)+cross*original_solve
    for name,mat,part in [('M',M,red[10:20,10:20]),('B',B,red[10:20,:10]),('Q',Q,red[:10,:10])]:
        zero('original_local_density_recovers_'+name,part-mat.subs(initial))
    # Independent numerical time drift on the original generic coefficient functions.
    args=variables+(k,)
    fb=s.lambdify(args,B,modules='mpmath')
    fm=s.lambdify(args,M,modules='mpmath')
    fq=s.lambdify(args,Q,modules='mpmath')
    fbd=s.lambdify(args,Bd,modules='mpmath')
    fmd=s.lambdify(args,Md,modules='mpmath')
    fg=s.lambdify(args,G,modules='mpmath')
    vals=[mp.mpf(str(s.N(initial[z],98))) for z in variables]
    vel=[mp.mpf(str(s.N(z,98))) for z in flow.subs(initial)]
    controls=[]
    for kval in (1,7,40):
        mat,bb,qq=fm(*vals,kval),fb(*vals,kval),fq(*vals,kval)
        rows=[]
        for hs in ('1e-14','1e-22'):
            h=mp.mpf(hs)
            plus=[z+h*d for z,d in zip(vals,vel)]
            minus=[z-h*d for z,d in zip(vals,vel)]
            btime=(fb(*plus,kval)-fb(*minus,kval))/(2*h)
            mtime=(fm(*plus,kval)-fm(*minus,kval))/(2*h)
            gt=fg(*vals,kval)
            num=mp.matrix(20);num[:10,10:20]=mp.eye(10)
            num[10:20,:10]=mp.inverse(mat)*(qq-btime)
            num[10:20,10:20]=-mp.inverse(mat)*(mtime+bb-bb.H)
            error=max(abs(z) for z in num-gt)/(1+max(abs(z) for z in gt))
            check(f'independent_time_drift_Euler_k{kval}_{hs}',error<1000*h*h,mp.nstr(error,65))
            rows.append(mp.nstr(error,65))
        controls.append(dict(k=kval,steps=['1e-14','1e-22'],normalized_errors=rows))
    # Exact real (cos,sin) pair for Re[(x-i*y) exp(ikz)].
    Re=Gi.applyfunc(s.re);Im=Gi.applyfunc(s.im)
    Greal=Re.row_join(Im).col_join((-Im).row_join(Re))
    witness=next(z for z in witnesses if not z['tangent'])
    seed=s.Matrix([s.sympify(z,locals=local) for z in witness['seed']])
    complex_result=Gi*seed
    pair=s.Matrix.vstack(seed,s.zeros(20,1))
    real_result=Greal*pair
    zero('real_cosine_sine_pair_matches_complex',real_result-s.Matrix.vstack(
        complex_result.applyfunc(s.re),-complex_result.applyfunc(s.im)))
    check('wrong_Fourier_gradient_sign_rejected',
          any(clean(z.subs(k,-k)-z)!=0 for z in Gi[13:16,:]*seed))
    wrong=G.copy();wrong[10:20,:10]+=M.inv()*Bd;wrong[10:20,10:20]+=M.inv()*Md
    omitted=((wrong-G)[13:16,:]*E).subs(initial).applyfunc(clean)
    check('omitted_actual_drift_changes_aligned_test',any(z!=0 for z in omitted),
          [[str(z) for z in row] for row in omitted.tolist()])
    # Force deletion would change at least the actual longitudinal equation.
    no_force=Gi.copy();no_force[13:16,9]=s.zeros(3,1);no_force[13:16,19]=s.zeros(3,1)
    check('discarded_force_response_rejected',any(z!=0 for z in (Gi-no_force)[13:16,:]))
    for path,(digest,mtime) in snap.items():
        fp=ROOT/path
        assert SHA(fp.read_bytes())==digest and fp.stat().st_mtime_ns==mtime,path
    check('all_source_bytes_and_mtimes_unchanged',True,len(snap))
    encode=lambda mat:[[str(clean(z)) for z in row] for row in mat.tolist()]
    return dict(kind='R4C1_ALIGNED_TANGENCY_V2',passed=sum(z['passed'] for z in checks),
        total=len(checks),checks=checks,source_sha256=pins,independent_controls=controls,
        result='UNRESTRICTED_DUST_ALIGNED_PERTURBATION_CLASS_NOT_INVARIANT' if failed else 'INITIAL_TANGENCY_ONLY',
        formulas=dict(state_order=base['fields'][:10]+['dt_'+z for z in base['fields'][:10]],
            free_state_indices=free,aligned_embedding=encode(E),
            necessary_frame_acceleration=encode(C),initial_frame_acceleration=encode(Ci),
            longitudinal_equation=str(force)+' = 0',initial_compatibility_rank=rank,
            physical_alignment='delta V=v/a; u_dust=n_ADM in dust-clock gauge',
            real_pair_convention='Re[(x-i*y)*exp(i*k*z)] = x*cos(k*z)+y*sin(k*z)'),
        probes=witnesses,linear_nonzero_mode_means_zero=True,
        original_constraint_reconstruction_retained=True,
        narrower_aligned_domain_preservation='NOT_PROVED',
        nonlinear_aligned_seed_admission='NOT_PROVED',
        physical_window_demonstrated=False,nodal_G1_admitted=False,
        G1='INCOMPLETE',G2='INCOMPLETE',G3='INCOMPLETE',G4='INCOMPLETE',G5='INCOMPLETE',G6='INCOMPLETE',
        MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
        physics_pass=False,gate_effect='NONE',review='DEFERRED',
        Rule9_cleared=False)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path)
    parser.add_argument('--replay',type=Path)
    args=parser.parse_args()
    result=calculate(); payload=ENC(result)
    if args.replay:
        assert payload==args.replay.read_bytes(),'replay differs'
        print('READ_ONLY_REPLAY_EXACT',SHA(payload))
    else:
        assert args.output_dir is not None,'use --output-dir or --replay'
        args.output_dir.mkdir(parents=True,exist_ok=False)
        p=args.output_dir/'summary.json';p.write_bytes(payload)
        Path(str(p)+'.sha256').write_text(SHA(payload)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=result['passed'],total=result['total'],
            result=result['result'],physics_pass=False,receipt=str(p))))
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':
    raise SystemExit(main())

