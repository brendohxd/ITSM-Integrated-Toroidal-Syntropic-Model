"""Action-derived dust observables, canonical density chart and formal bound."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_g3n5_nonzero_characteristic_attempt_02/'
PRECISION='Analysis/MasterTests/test_01_r4c1_g3n5_constraint_response_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_SLOW_DUST_WEIGHTED_CONTRACT_2026-10-11.md'
PINNED={
    'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py':'8c63194a678734917c5c9a9593da8023fb7ba946790cc0376c7cd3a9fa57c991',
    PRECISION:'6c1f2417b7a17ae5a07df07ae0957e6f66259d15398d8db9a39e9b57b3ffea9f',
    CONTRACT:'e01cb28d59c0244ad17a0cdf08579c64acbde4d1010efcbc06f4b756a95b2e4c',
    PARENT+'summary.json':'610b8b58037d60c694093b045a55745df0f39858b829447ac18d7d2e2bf88020',
    'Theory/Gates/RES-001/RES001_R4C1_G3N5_NONZERO_CHARACTERISTIC_REPORT_2026-10-11.md':'2bca36361ea542e51ec4b3b0c1ee8b57ebf98003f7c9076d4f625b33a3a47da5',
    'Theory/Gates/RES-001/RES001_R4C1_G3_ZERO_EVOLUTION_REPORT_2026-09-30.md':'d350c85fafb752502c017b7c93bc0223b4386ed72c39080c3e01126478d60f02',
    BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json':'ca95d2b2cf38facbcad6367aa6ef211c2ec9a2915d8b7aa8b33cba02256d0d8a'}
import hashlib
for rel in ('Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py',PRECISION):
    if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=PINNED[rel]:raise RuntimeError('Frozen imported source drift '+rel)
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import test_01_r4c1_g3n5_nonzero_characteristic_v1 as parent
import test_01_r4c1_g3n5_constraint_response_v2 as precision
old=parent.old;common=old.common
END=None  # Construct the exact decimal only after the requested precision is set.


def calculate():
    global END
    mp.mp.dps=70
    END=mp.mpf('0.05')
    pins=dict(PINNED);ps=common.read_json(PARENT+'summary.json')
    pins.update(ps['source_sha256'])
    for name,value in ps['artifacts'].items():pins[PARENT+name]=value
    pins[SELF]=common.sha((ROOT/SELF).read_bytes())
    absent=common.inspect_pins(pins)
    paths=[ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').is_file())
    before=parent.snapshot(paths);checks=common.Checks()
    checks.add('all_source_pins_before',True,{'pins':len(pins),'sidecars':len(pins)-len(absent),'absent':absent})
    checks.add('parent_complete_with_adverse_findings_retained',ps['passed']==121 and ps['total']==121 and
               ps['physics_pass'] is False and ps['wave_principal_complete'] is False and
               ps['formal_slow_time_coefficient']=='-11/6' and ps['Rule9_cleared'] is False)
    print('Reconstruct dust density/current from frozen full action',flush=True)
    op=old.Operator(checks);ell=s.Symbol('ell',positive=True);p=s.Symbol('p',positive=True)
    ch=op.chart(checks,(ell,0,0));a,H=op.bg[:2];rho,C=op.bg[-2:];psi=op.bg[8]
    vol=a**3;beta=old.PARAMS['beta'];Pt=vol*rho/C
    sy={**op.sy,'ell':ell,'p':p,'I':s.I,'sqrt':s.sqrt}
    data=common.read_json(PARENT+'matrices.json');fm=common.read_json(PARENT+'formulas.json')['formal_slow']
    q0=parent.import_matrix(data['slow_Q0'],sy);q1=parent.import_matrix(data['slow_Q1'],sy)
    A,R,K=(s.sympify(fm[key],locals=sy) for key in ('A','R','K'));d=-K
    E0,E1,E2=(s.sympify(fm[key],locals=sy) for key in ('E0','E1','E2'))
    N=s.Matrix([[0,1],[-E0/E2,-E1/E2]])
    exact=lambda name,expr:parent.exact(checks,name,expr)
    ex=parent.ex
    def dt(mat):return mat.applyfunc(lambda x:s.expand(op.dt(x)-H*p*s.diff(x,p)))
    def ph(mat):return ex(mat.subs(ell,a*p))
    def leading(mat,label):
        expanded=ex(mat)
        degrees=[term.as_powers_dict().get(p,0) for value in expanded for term in s.Add.make_args(value) if term!=0]
        checks.add(label+'_finite_large_p_limit',not degrees or max(degrees)<=0,str(max(degrees,default=0)),'maximum p degree <=0')
        return expanded.applyfunc(lambda x:x.coeff(p,0))
    O=s.eye(10);O[:3,:3]=s.Matrix([[1/s.sqrt(2),1/s.sqrt(2),0],[0,0,1],[1/s.sqrt(2),-1/s.sqrt(2),0]])
    embed=s.zeros(10,6)
    for j,i in enumerate((0,3,6,7,8,9)):embed[i,j]=1
    Ts=s.diag(1/p,1,1/p,1/p,1/p,1/p**2);Ts[5,1]=s.I*psi/p
    Y0,Y1=ex(O*embed*Ts*q0),ex(O*embed*Ts*q1)
    ys=Y0.row_join(Y1);yd=ex(dt(ys)+ys*N)
    qs=ex(ph(ch['symbolic']['Q0'])*ys+ph(ch['symbolic']['Q1'])*yd)
    qs[old.IDX['Em'],:]=ex(ph(ch['symbolic']['EmL'])*ys+ph(ch['symbolic']['EmM'])*yd)
    Pi=qs[old.IDX['Pi'],:];Em=qs[old.IDX['Em'],:]
    tr=sum((qs[old.IDX[k],:] for k in ('Mxx','Myy','Mzz')),s.zeros(1,2))
    drho=ex(C**4*Em+4*beta*rho*Pi)
    dPt=ex(vol*C**3*Em+Pt*(tr/2+3*beta*Pi))
    density=leading(drho/(s.I*p*rho),'density_weighted')
    charge=leading(dPt/(s.I*p*Pt),'charge_weighted')
    shift=leading(qs[old.IDX['Sx'],:],'shift')
    exact('density_equals_charge_leading_map',density-charge)
    exact('leading_shift_is_relative_velocity',shift-s.Matrix([[1,0]]))
    exact('relative_frame_velocity_retained',qs[old.IDX['Vx'],:]-s.Matrix([[1,0]]))
    exact('no_new_charge_restriction',op.dt(Pt))
    exact('dust_clock_and_norm_coordinates_still_fixed',qs[[old.IDX['T'],old.IDX['nu']],:])
    qd=ex(dt(qs)+qs*N);qdd=ex(dt(qd)+qd*N)
    ks=dict(zip(op.k,(ell,0,0)))
    momentum=vol*(ph(op.LK)*qd+ph(op.LBT.subs(ks))*qs)
    exact('dust_Noether_density_equals_unreduced_canonical_momentum',momentum[old.IDX['T'],:]-dPt)
    EA,EB,ED=(ph(mat.subs(ks)) for mat in (op.EA,op.EB,op.ED))
    eTau=ex((EA*qs+EB*qd+ED*qdd)[old.IDX['T'],:])
    conservation=ex(dt(dPt)+dPt*N-s.I*p*Pt*qs[old.IDX['Sx'],:])
    exact('full_dust_Euler_is_conserved_current_equation',vol*eTau+conservation)
    T=density.col_join(s.Matrix([[1,0]]))
    exact('observable_map_determinant',T.det()+d/rho)
    M=ex((op.dtm(T)+T*N)*T.inv()).applyfunc(s.cancel)
    exact('independent_leading_current_continuity',M[0,:]-s.Matrix([[H,1]]))
    exact('density_map_from_action_not_inserted',density-s.Matrix([[d*(H+beta*psi)/rho,d/rho]]))
    exact('weighted_matrix_simplification',M-s.Matrix([[H,1],[rho/d,-H-beta*psi]]))
    drift_missing=M[0,:]-s.Matrix([[0,1]])
    checks.add('reject_omitting_p_drift_in_current_equation',any(v!=0 for v in drift_missing),str(drift_missing),'nonzero symbolic residual')
    # Original slow phase space -> actual dust-observable canonical chart.
    print('Derive time-dependent canonical density Hamiltonians',flush=True)
    J=s.Matrix([[0,1],[-1,0]])
    velocity_map=s.Matrix([[1,0],[vol*R,vol*K]])
    Omega=s.cancel(vol*K/T.det())
    exact('weighted_symplectic_density',Omega-vol*rho)
    S=ex(s.diag(1,Omega)*T*velocity_map.inv())
    exact('canonical_density_map',S.T*J*S-J)
    HH=s.Matrix([[vol*(R*R/K-A),-R/K],[-R/K,1/(vol*K)]])
    GD=ex((op.dtm(S)+S*J*HH)*S.inv()).applyfunc(s.cancel)
    HD=ex(-J*GD).applyfunc(s.cancel)
    exact('weighted_density_Hamiltonian_complete',HD-s.Matrix([[-vol*rho*rho/d,H],[H,1/(vol*rho)]]))
    exact('weighted_symplectic_transport',op.dtm(Omega*J)+M.T*(Omega*J)+(Omega*J)*M)
    # Independent type-1 generating-function check in each real quadrature.
    vcoord,Dcoord,Pcoord=s.symbols('velocity_coordinate density_coordinate density_momentum',real=True)
    r=s.cancel(R-K*(H+beta*psi))
    F1=vol*r*vcoord**2/2-vol*rho*vcoord*Dcoord
    exact('type1_old_momentum',s.diff(F1,vcoord)-(vol*r*vcoord-vol*rho*Dcoord))
    exact('type1_new_momentum',-s.diff(F1,Dcoord)-vol*rho*vcoord)
    oldvec=s.Matrix([vcoord,s.diff(F1,vcoord)])
    after=s.expand((oldvec.T*HH*oldvec)[0]/2+op.dt(F1))
    after=s.cancel(after.subs(vcoord,Pcoord/(vol*rho)))
    newvec=s.Matrix([Dcoord,Pcoord])
    exact('type1_time_generator_complete_Hamiltonian',after-(newvec.T*HD*newvec)[0]/2)
    omitted=ex(J*HD-S*J*HH*S.inv())
    checks.add('reject_omitting_time_dependent_generator',any(v!=0 for v in omitted),True,'nonzero symbolic generator correction')
    # The i phase rotates the real sine/cosine quadratures, it does not fix phase.
    B=s.diag(s.I*p,s.I/p)
    exact('actual_density_Fourier_phase_canonical',B.conjugate().T*J*B-J)
    Gdelta=ex((dt(B)+B*GD)*B.inv())
    Hdelta=ex(-J*Gdelta)
    exact('actual_density_Hamiltonian',Hdelta-s.diag(-vol*rho*rho/(d*p*p),p*p/(vol*rho)))
    exact('density_growth_from_Hamiltonian',Gdelta-s.Matrix([[0,p*p/(vol*rho)],[vol*rho*rho/(d*p*p),0]]))
    mass=vol*rho/(p*p)
    drag=s.cancel((op.dt(mass)-H*p*s.diff(mass,p))/mass)
    exact('density_growth_drag',drag-2*H-beta*psi)
    exact('complete_density_energy_saddle',Hdelta.det()+rho/d)
    exact('negative_original_slow_K_retained',K+s.Rational(11,6))
    # A true finite-time leading-sector bound, independent of ell. Positive
    # control norm is NOT the indefinite canonical Hamiltonian above.
    MC=s.Rational(11,10)
    exact('Friedmann_positive_H_comparison',op.rates[1]+3*H*H-(op.potential+rho/2)/MC-op.constraint/MC)
    poly=s.Poly(op.potential,op.bg[2],op.bg[4],op.bg[6])
    checks.add('registered_potential_nonnegative',all(coef>0 and all(i%2==0 for i in powers) for powers,coef in poly.terms()),
               True,'positive coefficients and even powers')
    H0=mp.sqrt(mp.mpf(3469)/4620);Pmax=mp.sqrt(mp.mpf(11)/5)*H0
    rhomin=mp.mpf('0.2')*mp.exp(-(3*H0+mp.mpf('0.4')*Pmax)*END)
    rhomax=mp.mpf('0.2')*mp.exp(mp.mpf('0.4')*Pmax*END)
    lowerH=H0/(1+3*H0*END)
    Lambda=max(H0+1,mp.mpf(6)/11*rhomax+H0+mp.mpf('0.4')*Pmax)
    analytic=dict(H_max=str(H0),H_min=str(lowerH),psi_dot_absolute_max=str(Pmax),
                  rho_min=str(rhomin),rho_max=str(rhomax),a_min='1',a_max=str(mp.exp(H0*END)),
                  C_min=str(mp.exp(-mp.mpf('0.4')*Pmax*END)),C_max=str(mp.exp(mp.mpf('0.4')*Pmax*END)),
                  matrix_infinity_bound=str(Lambda),growth_bound=str(mp.exp(Lambda*END)),
                  norm='max(abs(delta_rho/rho_m)/p,abs(Vx)); formal leading sector only',
                  proof='Hdot<=0; Hdot>=-3H^2 by Friedmann and nonnegative potential; |psi_dot|<=sqrt(11/5)*H0; integrate rho and C; Gronwall for M')
    exact('rho_zero_observable_chart_singular',s.cancel(rho*T.det()).subs(rho,0)+d)
    exact('psi_dot_zero_does_not_remove_observable_map',T.det().subs(psi,0)+d/rho)
    checks.add('k_zero_not_inverted',True,'k=0 remains in separate mean chart; all transforms require p>0')
    print('Verify saved 70-digit background and slow fundamental transfer',flush=True)
    precision.controls(checks)
    saved=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    checks.add('same_saved_precision_and_degree',saved['digits']==70 and saved['degree']==40 and saved['background_order']==list(old.BG_NAMES))
    bg=[]
    for coeff in saved['background_coefficients']:
        q=precision.Series()
        if any(mp.mpf(x[1])!=0 for x in coeff):raise ValueError('Expected real background')
        q.c=[mp.mpf(x[0]) for x in coeff];bg.append(q)
    Series=precision.Series
    fM=s.lambdify([op.bg],list(M),'mpmath',cse=True)
    states=[Series(int(i==j)) for i in range(2) for j in range(2)]
    for order in range(40):
        Series.work=order;coef=fM(bg)
        for i in range(2):
            for j in range(2):
                rhs=sum((Series.wrap(coef[2*i+k])*states[2*k+j] for k in range(2)),Series())
                states[2*i+j].c[order+1]=rhs.c[order]/(order+1)
    Series.work=40
    def bg_at(t):return [q.evaluate(t) for q in bg]
    def rhs(t,y):
        vals=np.array([float(q) for q in fM(bg_at(mp.mpf(str(t))))]).reshape(2,2)
        return (vals@y.reshape(2,2)).ravel()
    solvers=[solve_ivp(rhs,(0,float(END)),np.eye(2).ravel(),method=method,
                       rtol=1e-11,atol=1e-13,dense_output=True) for method in ('DOP853','Radau')]
    checks.add('independent_transfer_solvers_completed',all(q.success and q.t[-1]==float(END) for q in solvers))
    rawbg=np.load(ROOT/(BASE+'r4c1_g3n5_constraint_response_attempt_01/background.npy'),allow_pickle=False)
    tail=mp.mpf(0);ode=mp.mpf(0);liouville=mp.mpf(0);bgerr=mp.mpf(0);agree=0.;normmax=mp.mpf(0);boundgap=mp.inf;domain=True
    transfers=[]
    for j in range(257):
        t=END*j/256;bt=bg_at(t)
        f=s.lambdify([op.bg],op.constraint,'mpmath',cse=True) if j==0 else f
        # Saved decimal coefficients are rounded; this is a 70-digit sample
        # evaluation allowance, not a change to the proven analytic domain.
        eps=mp.mpf('1e-60')
        domain=domain and 0<lowerH-eps<=bt[1]<=H0+eps and rhomin-eps<=bt[9]<=rhomax+eps and abs(bt[8])<=Pmax+eps and bt[10]>0
        vals=[q.evaluate(t) for q in states];der=[q.evaluate(t,derivative=1) for q in states]
        coarse=[q.evaluate(t,order=32) for q in states];mt=fM(bt)
        rate=[sum(mt[2*i+k]*vals[2*k+h] for k in range(2)) for i in range(2) for h in range(2)]
        tail=max(tail,max(abs(x-y) for x,y in zip(vals,coarse)))
        ode=max(ode,max(abs(x-y) for x,y in zip(der,rate))/max(sum(abs(x) for x in der+rate),mp.mpf('1e-20')))
        det=vals[0]*vals[3]-vals[1]*vals[2]
        liouville=max(liouville,abs(det*bt[10]-1))
        amp=max(abs(vals[0])+abs(vals[1]),abs(vals[2])+abs(vals[3]));normmax=max(normmax,amp)
        boundgap=min(boundgap,mp.exp(Lambda*t)-amp)
        bgerr=max(bgerr,max(abs(bt[k]-mp.mpf(str(rawbg[j,k])))/(1+abs(bt[k])) for k in range(11)))
        numerical=[q.sol(float(t)) for q in solvers]
        agree=max(agree,float(max(np.max(np.abs(numerical[0]-numerical[1])),np.max(np.abs(numerical[0]-np.array([float(x) for x in vals]))))))
        transfers.append(dict(t=str(t),Phi=[str(x) for x in vals],DOP853=numerical[0].tolist(),Radau=numerical[1].tolist()))
    for name,value,limit in [('true_Taylor_transfer_residual',ode,'1e-20'),('degree_32_40_transfer_tail',tail,'1e-20'),
                             ('Liouville_C_identity',liouville,'1e-20'),('original_background_agreement',bgerr,'1e-10')]:
        precision.numerical(checks,name,value,limit)
    checks.add('independent_transfer_agreement',agree<=1e-8,agree,'<=1e-8')
    checks.add('all_sampled_analytic_domains',bool(domain),True,'analytic bounds, not only positivity samples')
    checks.add('all_sampled_transfer_below_proven_bound',boundgap>=-mp.mpf('1e-60'),str(boundgap),'>=-1e-60 for roundoff at t=0')
    def export(mat):return parent.exports(mat)
    matrices={'weighted_observable_map':T,'weighted_flow':M,'original_slow_Hamiltonian':HH,
              'canonical_density_map':S,'weighted_density_Hamiltonian':HD,'actual_density_phase_map':B,
              'actual_density_Hamiltonian':Hdelta,'unreduced_slow_fields':qs,
              'dust_density_unweighted':drho,'dust_charge_unweighted':dPt}
    bundle={k:export(v) for k,v in matrices.items()}
    for name,mat in matrices.items():exact('serialized_roundtrip_'+name,parent.import_matrix(bundle[name],sy)-mat)
    checks.add('all_source_pins_after',common.inspect_pins(pins)==absent)
    checks.add('all_input_metadata_preserved',parent.snapshot(paths)==before,{'files':len(before),'hash_size_mtime_ns':True})
    formulas=dict(physical_density='delta_rho=C^4*Em+4*beta*rho_m*Pi',
                  weighted_state='D=delta_rho/(i*p*rho_m), V=relative_frame_velocity_x; leading sector',
                  conserved_density='delta_P_tau=a^3*C^3*Em+P_tau*(tr_M/2+3*beta*Pi)',
                  density_map=[str(x) for x in density],charge_map=[str(x) for x in charge],
                  shift_leading=[str(x) for x in shift],observable_determinant=str(s.factor(T.det())),
                  weighted_flow=[[str(x) for x in M.row(j)] for j in range(2)],
                  original_slow_K=str(K),symplectic_weight=str(Omega),type1_generator=str(F1),
                  density_equation='delta_ddot+(2*H+beta*psi_dot)*delta_dot-(6*rho_m/11)*delta=0',
                  actual_density_kinetic_weight=str(mass),actual_density_Hamiltonian_determinant=str(s.factor(Hdelta.det())),
                  analytic_bounds=analytic,assumptions=['Smooth registered B1 background, Friedmann constraint zero','rho_m,C,a>0,p>0',
                                                        'Formal leading slow sector; no arbitrary fast-wave data or remainder estimate'],
                  nonclaims=['No removal of original Jordan defect or negative slow K','No positive complete Hamiltonian',
                             'No physical no-ghost/cutoff/causality certificate','No calibrated G_eff, healthy full GR or matching'])
    diagnostics=dict(transfer_tail=str(tail),true_transfer_residual=str(ode),liouville_residual=str(liouville),
                     background_error=str(bgerr),independent_transfer_error=agree,max_transfer_infinity_norm=str(normmax),
                     inherited_parent_adverse_findings={'wave_principal_complete':False,'original_slow_K':'-11/6',
                                                        'negative_spatial_energy_retained':True},
                     preserved_failures=ps['preserved_main_v1'],review='DEFERRED; same-agent local calculations only')
    payloads={'matrices.json':common.encode(bundle),'formulas.json':common.encode(formulas),
              'transfer.json':common.encode({'row_major_Phi':True,'samples':transfers,
                                             'degree40_coefficients':[[str(x) for x in q.c] for q in states]}),
              'diagnostics.json':common.encode(diagnostics)}
    passed=sum(q['passed'] for q in checks.rows)
    summary=dict(schema='r4c1-g3n5-slow-dust-weighted-v1',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
                 passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='CONDITIONAL_FORMAL_SLOW_DUST_CANONICAL_WEIGHTED_ENTRY_CHECKED',
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                 ordinary_wave_Jordan_defect_removed=False,original_slow_time_coefficient='-11/6',
                 density_momentum_positive_on_stated_domain=True,complete_density_Hamiltonian_positive=False,
                 formal_leading_weighted_evolution_bound=True,full_finite_k_remainder_verified=False,
                 physical_Hessian_verified=False,physical_EFT_cutoff_derived=False,
                 canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
                 source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,
                 source_metadata_preserved=len(before),runtime=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__),
                 artifacts={k:common.sha(v) for k,v in payloads.items()},
                 review_dependencies=['B1/G3N4/full G3N5 constraints','Nonzero canonical/principal/slow-action audit','All inherited physics/review debt'])
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    payloads['summary.json']=common.encode(summary)
    return payloads,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_slow_dust_weighted_attempt_01');ap.add_argument('--replay')
    args=ap.parse_args();dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if not args.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    data,summary=calculate()
    if args.replay:
        for name,body in data.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():
                raise RuntimeError('Exact replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in data.items():
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',**{k:summary[k] for k in ('validation','passed','total','status','physics_pass','gate_effect')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
