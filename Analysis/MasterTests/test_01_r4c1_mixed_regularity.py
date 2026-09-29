"""R4C1-S4B: test one extra dust-tilt derivative in the full scalar graph.

This is a new domain and a diagnostic of the unchanged conditional action.
No numerical sample is treated as a uniform PDE estimate.
"""
from __future__ import annotations

import json
import platform
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as s

import test_01_r4c1_coupled_graph as previous

prior, up, base = previous.prior, previous.up, previous.base
ROOT, OUT = base.ROOT, base.OUT
STEM = 'test_01_r4c1_mixed_regularity'
a, H, k = base.a, base.H, base.k

PINS = {
    'Theory/Gates/RES-001/RES001_R4C1_MIXED_REGULARITY_CONTRACT_2026-09-26.md':
        '7ba250c0afe826fca2af431260c2f9ea53d485a4ae197c6f5eced044d702bd22',
    'Theory/Gates/RES-001/RES001_R4C1_COUPLED_GRAPH_REPORT_2026-09-26.md':
        'e493a658e2c3ae357167a269c2b611d6ed7cd5ce7dea77296a4f62999c7421d2',
    'Analysis/MasterTests/test_01_r4c1_coupled_graph.py':
        '31b80572c618557674934ddb4a9d591aaa58959a497124f15f4198121db8f16a',
    'Analysis/MasterTests/outputs/test_01_r4c1_coupled_graph_summary.json':
        'cacd1b1bf9970399c89383e5ac6f2bbfe4614fa5cb6ebf04806bb700a0ae16c0',
    'Analysis/MasterTests/outputs/test_01_r4c1_coupled_graph_matrices.json':
        '7d815633d8ee583e0f4de2e0e198d27356a220dcc8abecb1613bc46ef7246c85',
    'Analysis/MasterTests/outputs/test_01_r4c1_coupled_graph_samples.json':
        '9203ada102243051a0dfb4788ab83ee93190bb8d299ec4dbdf9b1a2b9d876907',
    'Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json':
        '6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70',
    'Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_transfers.json':
        '8f85326eaec6cbc8c14a42fffb776869f374e0edb63ec9045fa0b40ca0119330',
}


def verify(audit):
    observed = previous.verify_sources(audit)
    for name, expected in PINS.items():
        file = ROOT/name
        actual = base.sha(file)
        audit.test('S4B_pin:'+name, actual == expected, actual)
        sidecar = file.with_name(file.name+'.sha256')
        audit.test('S4B_sidecar:'+name,
                   sidecar.exists() and sidecar.read_text().split()[0] == actual)
        observed[name] = actual
    receipt = prior.read_raw('test_01_r4c1_coupled_graph_summary.json')
    audit.test('S4A_scope', receipt['validation']=='PASS' and
               receipt['physics_pass'] is False and receipt['Rule9_cleared'] is False and
               receipt['status']=='FIXED_GRAPH_DIFFERENTIAL_BOUND_REJECTED_FULL_IVP_OPEN')
    audit.test('S4A_transitive_artifacts', all(
        base.sha(ROOT/name) == digest for name, digest in receipt['artifacts'].items()))
    return observed


def derive(audit):
    old = prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    s2 = prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    F0 = prior.parse_matrix(old, 'graph_map')
    G, W, Mc, Vc = [prior.parse_matrix(s2, name) for name in ('G','W','Mc','Vc')]
    A = s.BlockMatrix([[s.zeros(6),s.eye(6)],[-W,-G]]).as_explicit()
    p = k/a
    F = F0.col_join(p*F0[14,:])
    Fdot = up.dtime(F)
    audit.test('full_new_graph_shape', F.shape==(16,12) and F0.shape==(15,12))
    audit.exact('new_row_exactly_one_dust_derivative', F[15,:]-p*F0[14,:])
    audit.exact('differentiated_physical_p_at_fixed_k', up.dtime(p)+H*p)
    audit.exact('new_row_time_derivative', Fdot[15,:]-p*(up.dtime(F0[14,:])-H*F0[14,:]))
    audit.test('reject_missing_pdot', any(s.cancel(z)!=0 for z in H*p*F0[14,:]))
    audit.test('reject_old_graph_reuse', F[15,:] != F0[14,:])
    audit.exact('Mcdot_kept_in_generator', W-Vc-up.dtime(Mc))
    audit.test('reject_missing_Fdot', any(s.cancel(z)!=0 for z in Fdot))
    audit.test('S4A_rank_subminor_preserved',
               old['selected_minor_rows']==[0,2,3,5,6,8,9,10,11,12,13,14] and
               old['full_canonical_minor'] != '0')
    return F0,F,Fdot,A


def evaluate(audit,F0,F,Fdot,A):
    mp.mp.dps=60
    args=up.ARGS
    f0=s.lambdify(args,F0,'mpmath',cse=True)
    f=s.lambdify(args,F,'mpmath',cse=True)
    fd=s.lambdify(args,Fdot,'mpmath',cse=True)
    fa=s.lambdify(args,A,'mpmath',cse=True)
    flow=prior.integrate(prior.PARAMS,'DOP853',1e-12,1e-14)
    audit.test('B1_background_integrates', flow.success)
    rows=[]
    old_samples=prior.read_raw('test_01_r4c1_coupled_graph_samples.json')['local_rates']
    for t in (0.,.5,1.,2.,3.,4.):
        print('S4B local rates t=',t,flush=True)
        for j in range(9):
            pval=2*np.pi*2**j
            wave=pval*float(flow.sol(t)[0])
            mp_args=previous.mp_args(flow,t,wave)
            fm,dm,am=mp.matrix(f(*mp_args)),mp.matrix(fd(*mp_args)),mp.matrix(fa(*mp_args))
            S,chol,eigen=previous.metric_data(fm)
            Lm=dm+fm*am
            E=Lm.T*fm+fm.T*Lm
            inv=chol**-1
            sym=inv.T*E*inv
            mu=float(max(mp.eigsy((sym+sym.T)/2,eigvals_only=True))/2)
            oldrow=old_samples[len(rows)]
            audit.test(f'grid_match_t{t}_j{j}',
                       abs(oldrow['t']-t)<1e-15 and abs(oldrow['p']-pval)<1e-11)
            rows.append(dict(t=t,p=pval,mu=mu,old_mu=oldrow['mu'],
                             min_metric_eigenvalue=float(eigen[0]),
                             metric_condition=float(eigen[eigen.rows-1]/eigen[0])))
    audit.test('positive_sampled_new_metrics',len(rows)==54 and
               all(r['min_metric_eigenvalue']>0 and np.isfinite(r['mu']) for r in rows))

    # Full matrix centered derivative along the B1 trajectory, fixed comoving k.
    t0,h,wave=1.,1e-6,2*np.pi
    fixed=previous.mp_args(flow,t0,wave)
    fm,dm,am=mp.matrix(f(*fixed)),mp.matrix(fd(*fixed)),mp.matrix(fa(*fixed))
    E=(dm+fm*am).T*fm+fm.T*(dm+fm*am)
    fp=mp.matrix(f(*previous.mp_args(flow,t0+h,wave)))*(mp.eye(12)+h*am)
    fmminus=mp.matrix(f(*previous.mp_args(flow,t0-h,wave)))*(mp.eye(12)-h*am)
    centered=(fp.T*fp-fmminus.T*fmminus)/(2*h)
    derivative_error=float(mp.norm(centered-E)/(1+mp.norm(E)))
    audit.test('new_full_energy_derivative',derivative_error<1e-5,derivative_error)
    wrong=(fm*am).T*fm+fm.T*(fm*am)
    audit.test('reject_omitted_new_Fdot',mp.norm(E-wrong)/(1+mp.norm(E))>mp.mpf('1e-8'))

    transfers=prior.read_raw('test_01_r4c1_scalar_propagation_transfers.json')
    audit.test('inherited_modes',[z['n'] for z in transfers]==[1,2,4,8])
    endpoints=[]
    worst_independent=0.
    for row in transfers:
        wave=2*np.pi*row['n']
        Fstart=mp.matrix(f(*previous.mp_args(flow,0.,wave)))
        Fend=mp.matrix(f(*previous.mp_args(flow,4.,wave)))
        S0,_,_=previous.metric_data(Fstart)
        S1,_,_=previous.metric_data(Fend)
        methods=[]
        for method in row['methods']:
            audit.test(f'inherited_{method["method"]}_success_n{row["n"]}',method['success'])
            gain,discrepancy=previous.amplify(S0,S1,mp.matrix(method['endpoint_transfer']))
            worst_independent=max(worst_independent,float(discrepancy))
            methods.append(dict(method=method['method'],amplification=float(gain),
                                independent_discrepancy=float(discrepancy)))
        diff=abs(methods[0]['amplification']-methods[1]['amplification'])/(1+abs(methods[1]['amplification']))
        audit.test(f'two_solver_graph_agreement_n{row["n"]}',diff<1e-5,diff)
        endpoints.append(dict(n=row['n'],methods=methods,two_solver_discrepancy=diff))
    audit.test('independent_norm_method_agreement',worst_independent<1e-8,worst_independent)
    return dict(local_rates=rows,endpoint_transfers=endpoints,
                b1_initial_state=list(map(float,flow.sol(0.))),
                derivative_error=derivative_error,
                independent_norm_discrepancy=worst_independent,
                arithmetic='60 decimal digits for graph evaluation; inherited B1 and S2 dynamics keep their original accuracy',
                interpretation='Finite grid only; no uniform PDE energy theorem')


def exact_high_p_witness(audit,F,Fdot,A,b1_initial_state):
    """Post-scan analytic strengthening of the frozen F1-norm diagnostic."""
    old=prior.read_raw('test_01_r4c1_coupled_graph_matrices.json')
    s2=prior.read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    Fq=prior.parse_matrix(old,'original_graph_map')
    R=prior.parse_matrix(s2,'q_from_x')
    Rdot=up.dtime(R)
    p=s.Symbol('p',positive=True)
    fixed={base.a:1,base.C:1,base.u:1,base.ud:0,base.v:0,base.vd:1,
           base.r:1,base.rd:s.Rational(1,4),base.pd:s.Rational(1,5),
           base.rho:s.Rational(1,5),base.k:p}
    expected_initial=[1.,None,1.,0.,0.,1.,1.,.25,0.,.2,.2,0.]
    audit.test('witness_exact_B1_initial_coefficients',
               len(b1_initial_state)==12 and b1_initial_state[1]>0 and
               all(abs(b1_initial_state[i]-v)<1e-15 for i,v in enumerate(expected_initial)
                   if v is not None),b1_initial_state)
    F,Fdot,A,Fq,R,Rdot=[M.subs(fixed) for M in (F,Fdot,A,Fq,R,Rdot)]
    density_coefficient=(79200*H**2+200*p**2+1419)/240
    audit.exact('witness_positive_density_velocity_coefficient',
                Fq[13,10]-density_coefficient)
    # The denominator is positive for physical H>0 and p>0.
    y=s.zeros(12,1)
    y[4]=1/p**2
    y[11]=s.sqrt(6)
    y[10]=-s.cancel((Fq[13,4]*y[4]+Fq[13,11]*y[11])/Fq[13,10])
    audit.exact('witness_density_constraint',(Fq[13,:]*y)[0])
    Rinv=R.inv()
    x=Rinv*y[:6,0]
    z=s.Matrix.vstack(x,Rinv*(y[6:,0]-Rdot*x))
    graph=(F*z).applyfunc(s.cancel)
    expected=s.zeros(16,1)
    expected[11],expected[14],expected[15]=1,1/p,1
    audit.exact('witness_full_graph_support',graph-expected)
    norm2=s.cancel((graph.T*graph)[0])
    audit.exact('witness_graph_norm_squared',norm2-(2*p**2+1)/p**2)
    limits={}
    for row,target in ((11,0),(14,0),(15,s.sqrt(6)/2)):
        evolution=s.cancel((Fdot[row,:]*z)[0]+(F[row,:]*A*z)[0])
        contribution=s.cancel(graph[row]*evolution/norm2)
        limits[row]=s.factor(s.limit(contribution/p,p,s.oo))
        audit.exact(f'witness_row_{row}_rate_over_p',limits[row]-target)
    total=s.factor(sum(limits.values()))
    audit.exact('witness_full_rate_over_p',total-s.sqrt(6)/2)
    audit.test('witness_rate_independent_of_H',not total.has(H))
    return dict(original_chart_data={
                    'delta_tau':'1/p**2','delta_w_dot':'sqrt(6)',
                    'delta_tau_dot':'-(Fq[13,4]/p**2+sqrt(6)*Fq[13,11])/Fq[13,10]'},
                density_velocity_coefficient=str(density_coefficient),
                graph_nonzero={'11':'1','14':'1/p','15':'1'},
                graph_norm_squared=str(s.factor(norm2)),
                row_rate_over_p_limits={str(row):str(value) for row,value in limits.items()},
                full_rate_over_p_limit=str(total),
                provenance='Post-scan analytic strengthening after preserved 159-check run; action, F1 norm, B1 initial data and thresholds unchanged')


def main():
    audit=up.Audit()
    inputs=verify(audit)
    if not all(c['passed'] for c in audit.checks):
        print(json.dumps(dict(validation='FAIL_SOURCE_PIN',
                              failed=[c for c in audit.checks if not c['passed']])))
        return 1
    print('Constructing fixed mixed-regularity metric...',flush=True)
    F0,F,Fdot,A=derive(audit)
    evidence=evaluate(audit,F0,F,Fdot,A)
    witness=exact_high_p_witness(audit,F,Fdot,A,evidence['b1_initial_state'])
    matrixpath=OUT/(STEM+'_matrices.json')
    samplepath=OUT/(STEM+'_samples.json')
    base.write_json(matrixpath,dict(schema='r4c1-mixed-regularity-matrices-v1',
        new_graph_row='physical_p*dust_ADM_tilt',
        full_graph_map=base.matrix_strings(F),
        full_graph_map_derivative=base.matrix_strings(Fdot),
        exact_high_p_witness=witness,
        generator_source='test_01_r4c1_scalar_propagation_matrices.json:G,W',
        definition='S=F.T*F; E=(Fdot+F*A).T*F+F.T*(Fdot+F*A)',
        domain='One extra spatial derivative of dust tilt; not uniformly equivalent to S4A'))
    base.write_json(samplepath,evidence)
    passed=sum(c['passed'] for c in audit.checks)
    valid=passed==len(audit.checks)
    summary=dict(schema='r4c1-mixed-regularity-summary-v1',
        validation='PASS' if valid else 'FAIL',passed=passed,total=len(audit.checks),
        status='ONE_EXTRA_DUST_DERIVATIVE_FIXED_GRAPH_BOUND_REJECTED_FULL_IVP_OPEN' if valid else 'UNVALIDATED',
        physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_VALIDATION',
        inherited_unreviewed_inputs=['R9-MT1-S4A','R9-MT1-S3','R9-MT1-S2','R9-MT1-S1',
                                     'R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=inputs,executable_sha256=base.sha(Path(__file__)),
        artifacts={path.relative_to(ROOT).as_posix():base.sha(path) for path in (matrixpath,samplepath)},
        full_constrained_IVP='NOT_PROVED',uniform_energy_estimate='NOT_ESTABLISHED',
        fixed_metric_differential_bound='REJECTED_BY_EXACT_FRAME_DUST_WITNESS' if valid else 'UNVALIDATED',
        canonical=dict(MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',
                       V='NOT_COMPUTED',Stage4A='CLOSED'),
        summary=dict(local_max_rate=max(r['mu'] for r in evidence['local_rates']),
                     local_last_p_rates=[dict(t=r['t'],mu=r['mu']) for r in evidence['local_rates'] if r['p']>1600],
                     endpoint_amplifications=[dict(n=x['n'],gain=x['methods'][0]['amplification'])
                                              for x in evidence['endpoint_transfers']],
                     max_metric_condition=max(r['metric_condition'] for r in evidence['local_rates']),
                     norm_method_discrepancy=evidence['independent_norm_discrepancy'],
                     centered_derivative_error=evidence['derivative_error'],
                     exact_witness_rate_over_p=witness['full_rate_over_p_limit']),
        versions=dict(python=platform.python_version(),sympy=s.__version__,mpmath=mp.__version__),
        checks=audit.checks)
    base.write_json(OUT/(STEM+'_summary.json'),summary)
    print(json.dumps({z:summary[z] for z in ('validation','passed','total','status','summary')}))
    return 0 if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
