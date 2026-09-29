"""R4C1-S3: exact Jordan obstruction and original-variable graph-norm diagnostic.

Neither a frozen symbol nor an asymptotic embedding proves the full IVP.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as s
from scipy.linalg import eigh

import test_01_r4c1_scalar_propagation as upstream
from test_01_r4c1_interacting_background import integrate,PARAMS

base=upstream.base;ROOT=base.ROOT;OUT=base.OUT
STEM='test_01_r4c1_zero_branch';sha=base.sha;write_json=base.write_json;Audit=upstream.Audit
a,H,u,ud,v,vd,r,rd,pd,rho,C,k=[getattr(base,z) for z in
                            ('a','H','u','ud','v','vd','r','rd','pd','rho','C','k')]
p=s.Symbol('physical_p',positive=True)
duration=s.Symbol('principal_duration',real=True)
PINS={
 'Theory/Gates/RES-001/RES001_R4C1_ZERO_BRANCH_CONTRACT_2026-09-26.md':
 'c1e4d5f72c3f354b8e43b1ed51b01b46e5da9d301125ac687cb723e1887ef49e',
 'Analysis/MasterTests/test_01_r4c1_scalar_propagation.py':
 '745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda',
 'Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_matrices.json':
 '6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70',
 'Analysis/MasterTests/outputs/test_01_r4c1_scalar_propagation_summary.json':
 '56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735',
 'Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md':
 '653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9',
 'Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json':
 '27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a',
}
SYMBOLS={str(z):z for z in vars(base).values() if isinstance(z,s.Symbol)}


def read_raw(name):
    return json.loads((OUT/name).read_text())


def parse_matrix(raw,key):
    return s.Matrix([[s.sympify(z,locals=SYMBOLS) for z in row] for row in raw[key]])


def tidy(matrix):
    return matrix.applyfunc(lambda z:s.factor(s.cancel(z)))


def jordan(audit,raw):
    LL=parse_matrix(raw,'slow_principal_V')[3:,3:]
    GG=parse_matrix(raw,'slow_principal_G')[3:,3:]
    A=s.BlockMatrix([[s.zeros(2),s.eye(2)],[-LL,-GG]]).as_explicit()
    e0=s.Matrix([0,1,0,0]);e1=s.Matrix([-6*s.sqrt(11),0,0,1])
    audit.exact('zero_eigenvector',A*e0)
    audit.exact('generalized_eigenvector',A*e1-e0)
    P=s.eye(4)+3*A*A;N=tidy(A*P)
    audit.exact('spectral_projector_idempotent',P*P-P)
    audit.exact('zero_sector_nilpotent',N*N)
    audit.test('nilpotent_not_zero',N!=s.zeros(4))
    audit.exact('projector_commutes',A*P-P*A)
    audit.exact('projector_contains_chain',P*s.Matrix.hstack(e0,e1)-s.Matrix.hstack(e0,e1))
    transfer=P+p*duration*N
    audit.exact('exact_zero_transfer_equation',s.diff(transfer,duration)-p*A*transfer)
    audit.exact('zero_transfer_initial',transfer.subs(duration,0)-P)
    evolved=transfer*e1/s.sqrt(397)
    audit.exact('unit_initial_sequence',(e1.T*e1)[0]/397-1)
    audit.exact('equal_order_growth_identity',(evolved.T*evolved)[0]-1-p*p*duration*duration/397)
    audit.test('reject_uniform_diagonalizer',4-A.rank()==1 and s.degree(A.charpoly().as_expr())==4)
    audit.test('reject_dropping_generalized_vector',A*e1!=s.zeros(4) and e1!=e0)
    return A,P,N,s.Matrix.hstack(e0,e1),evolved


def dust_control(audit):
    t,x=s.symbols('time space',real=True)
    tau=s.Function('delta_tau')(t,x);eps=s.Function('delta_epsilon')(t,x)
    eps0,C0=s.symbols('epsilon0 C0',positive=True)
    # Coefficient of perturbation order two, obtained before imposing tau_t=0.
    order=s.Symbol('order')
    exact=(eps0+order*eps)*C0**2*((C0+order*s.diff(tau,t))**2
                      -order**2*s.diff(tau,x)**2-C0**2)/2
    L=s.expand(exact).coeff(order,2)
    audit.exact('dust_quadratic_from_unconstrained_action',L-(eps0*C0**2*(s.diff(tau,t)**2-s.diff(tau,x)**2)/2
                       +C0**3*eps*s.diff(tau,t)))
    audit.exact('dust_multiplier_before_elimination',s.diff(L,eps)-C0**3*s.diff(tau,t))
    EL=s.diff(s.diff(L,s.diff(tau,t)),t)+s.diff(s.diff(L,s.diff(tau,x)),x)
    audit.exact('dust_continuity_before_constraint',EL-(C0**3*s.diff(eps,t)
                    +eps0*C0**2*(s.diff(tau,t,2)-s.diff(tau,x,2))))
    # On tau_t=0, delta rho=C0^4 eps and v=-tau_x/C0 give
    # delta rho_t+rho0*v_x=0, v_t=0, rho0=eps0*C0^4.
    delta_rho=C0**4*eps;vel=-s.diff(tau,x)/C0
    audit.exact('dust_density_velocity_equation',C0*EL.subs(s.diff(tau,t,2),0)
                       -(s.diff(delta_rho,t)+eps0*C0**4*s.diff(vel,x)))
    B=s.Matrix([[0,-p],[0,0]])
    E=s.eye(2)+duration*B;J=s.diag(1,p)
    weighted=J*E*J.inv()
    audit.exact('dust_nilpotent',B*B)
    audit.exact('one_extra_velocity_derivative',weighted-s.Matrix([[1,-duration],[0,1]]))
    audit.test('reject_equal_order_from_weighted_control',s.diff(E[0,1],p)!=0 and s.diff(weighted[0,1],p)==0)
    return dict(quadratic_density=str(L),equations=['delta_rho_dot+rho0*partial_x(v)=0','v_dot=0'],
        equal_order_transfer=base.matrix_strings(E),mixed_order_transfer=base.matrix_strings(weighted),
        scope='Fixed Minkowski and constant C/density irrotational dust control only; velocity needs one extra spatial derivative')


def reconstruction(audit,raw,Jchain):
    R=parse_matrix(raw,'q_from_x');W=parse_matrix(raw,'W')
    # Embedding of the T,W slow sector via the leading fast Schur relation.
    E=s.zeros(6,2);E[4,0]=1;E[5,1]=1
    denom=s.expand(W[3,3]).coeff(k,4)
    for col,index in enumerate((4,5)):
        E[3,col]=s.factor(-s.expand(W[3,index]).coeff(k,3)/(denom*k))
    audit.test('fast_embedding_not_discarded',any(z!=0 for z in E[3,:]))
    Q=s.Matrix.hstack(R*E/(k/a),s.zeros(6,2))
    Qd=s.Matrix.hstack((upstream.dtime(R)*E+R*upstream.dtime(E))/(k/a),R*E)
    Q=tidy(Q.subs(k,a*p));Qd=tidy(Qd.subs(k,a*p))
    upstream_raw=read_raw('test_01_r4c1_scalar_constraints_matrices.json')
    aux=s.Matrix([s.sympify(z,locals=SYMBOLS) for z in upstream_raw['auxiliary_solutions']]).subs(upstream.PARAMETER_SUBS)
    variables=list(base.qd)+list(base.q)
    derivative_map=aux.jacobian(variables)
    reconstructed=tidy((derivative_map.subs(k,a*p))*s.Matrix.vstack(Qd,Q))
    lapse,shift,deltaeps,z=[reconstructed[i,:] for i in range(4)]
    delta_density=tidy(C**4*deltaeps+s.Rational(8,5)*rho*Q[3,:])
    v_d=tidy(p*Q[4,:]/C)
    relative=tidy(Q[5,:]-v_d)
    audit.exact('dust_constraint_reconstruction',Qd[4,:]-C*lapse-s.Rational(2,5)*C*Q[3,:])
    audit.exact('relative_frame_velocity',relative-s.Matrix([[0,s.sqrt(6)/(a**s.Rational(3,2)*p),0,0]]))
    # U_m=-d tau/C on the constrained branch: first-order norm equals
    # 2(alpha+beta*dpsi-dtau_dot/C), independent of the shift.
    audit.exact('matter_unit_normalization',2*(lapse+s.Rational(2,5)*Q[3,:]-Qd[4,:]/C))
    delta=tidy(-p*p*Q[3,:]+pd*p*Q[5,:])
    audit.exact('regulator_auxiliary_reconstruction',z+delta)
    rows=[];names=[]
    for i,name in enumerate(('u','v','r')):
        rows.extend([Q[i,:],p*Q[i,:],Qd[i,:]])
        names.extend(['delta_'+name,'p_delta_'+name,'delta_'+name+'_dot'])
    rows.extend([s.sqrt(3)*Qd[3,:],s.sqrt(s.Rational(5,11))*delta,
                 Qd[5,:]/s.sqrt(6),p*Q[5,:]/s.sqrt(15),delta_density/rho,v_d])
    names.extend(['sqrtK_delta_psi_dot','sqrtb_delta_Delta','sqrtc14_w_dot','sqrtcL_p_w','density_contrast','dust_ADM_tilt'])
    F=tidy(s.Matrix.vstack(*rows)*Jchain)
    rescale=s.diag(1,1/p)
    scaled=tidy(F*rescale)
    limit=scaled.applyfunc(lambda z:s.limit(z,p,s.oo))
    finite=all(not z.has(s.oo,s.zoo,s.nan) for z in limit)
    audit.test('scaled_graph_limit_finite',finite)
    # Any two independent rows provide a lower bound for the full Gram matrix.
    minor=s.factor(limit.extract([12,13],[0,1]).det()) if finite else s.nan
    audit.test('original_frame_density_limit_independent',minor!=0 and minor!=s.nan,str(minor))
    powers=[]
    for col in range(2):
        entries=[]
        for row in range(F.rows):
            if F[row,col]==0: entries.append(None);continue
            num,den=s.cancel(F[row,col]).as_numer_denom()
            entries.append(int(s.degree(num,p)-s.degree(den,p)))
        powers.append(entries)
    return dict(Q=Q,Qdot=Qd,aux=reconstructed,density=delta_density,tilt=v_d,relative=relative,
        embedding=E,F=F,scaled=scaled,limit=limit,minor=minor,names=names,powers=powers)


def sample_norms(audit,rec,Jchain):
    args=list(upstream.FLOW)+[p]
    fF=s.lambdify(args,rec['F'],'numpy',cse=True)
    fLimit=s.lambdify(list(upstream.FLOW),rec['limit'],'numpy',cse=True)
    flow=integrate(PARAMS,'DOP853',1e-12,1e-14)
    audit.test('background_integration',flow.success,flow.message)
    samples=[];max_agreement=0.;min_rank=float('inf');max_weighted=0.
    chain=np.array(Jchain,float);canonical_metric=chain.T@chain
    for t0 in (0.,.5,1.,2.,3.,4.):
        background=upstream.background_args(flow.sol(t0),1.)[:-1]
        ll=np.asarray(fLimit(*background),float)
        limit_eig=np.linalg.eigvalsh(ll.T@ll)
        row=dict(background_t=t0,limit_Gram_eigenvalues=limit_eig.tolist(),samples=[])
        for j in range(9):
            pp=2*np.pi*2**j
            FF=np.asarray(fF(*background,pp),float);B=FF.T@FF
            eig=np.linalg.eigvalsh(B);min_rank=min(min_rank,float(eig[0]))
            if eig[0]<=0:
                audit.test(f'graph_rank_t{t0}_j{j}',False,eig.tolist());continue
            EE=np.array([[1.,pp],[0.,1.]])
            chol=np.linalg.cholesky(B).T
            amp=float(np.linalg.svd(chol@EE@np.linalg.inv(chol),compute_uv=False)[0])
            ev=eigh(EE.T@B@EE,B,eigvals_only=True)
            alternative=float(np.sqrt(max(ev)))
            max_agreement=max(max_agreement,abs(amp-alternative)/(1+abs(alternative)))
            canchol=np.linalg.cholesky(canonical_metric).T
            canonical_amp=float(np.linalg.svd(canchol@EE@np.linalg.inv(canchol),compute_uv=False)[0])
            rescale=np.diag([1.,1/pp]);scaled_metric=rescale@B@rescale
            limit_diff=float(np.linalg.norm(scaled_metric-ll.T@ll,2)/(1+np.linalg.norm(ll.T@ll,2)))
            max_weighted=max(max_weighted,amp)
            row['samples'].append(dict(p=pp,graph_amplification=amp,equal_order_amplification=canonical_amp,
                explicit_equal_order_sequence_norm=float(np.sqrt(1+pp*pp/397)),
                graph_eigenvalues=eig.tolist(),graph_condition=float(np.linalg.cond(B)),
                scaled_metric_eigenvalues=np.linalg.eigvalsh(scaled_metric).tolist(),
                scaled_metric_limit_relative_difference=limit_diff))
        samples.append(row)
    audit.test('positive_sampled_graph_metrics',min_rank>0,min_rank)
    audit.test('independent_amplification_agreement',max_agreement<1e-8,max_agreement,'relative <1e-8')
    audit.test('positive_sampled_graph_limits',all(min(row['limit_Gram_eigenvalues'])>0 for row in samples))
    return dict(samples=samples,max_graph_amplification=max_weighted,
                min_graph_eigenvalue=min_rank,max_method_discrepancy=max_agreement,
                domain='Frozen local principal system, duration=1; not full evolving modes or an IVP theorem')


def main():
    audit=Audit();inputs={path:sha(ROOT/path) for path in PINS}
    for path,digest in PINS.items():audit.test('pin_'+path,inputs[path]==digest,inputs[path])
    for name in ('test_01_r4c1_scalar_propagation_summary.json','test_01_r4c1_scalar_constraints_summary.json'):
        upstream_receipt=read_raw(name)
        for path,digest in {**upstream_receipt['inputs'],**upstream_receipt['artifacts']}.items():
            audit.test('transitive_'+name+'_'+path,sha(ROOT/path)==digest)
    if not all(c['passed'] for c in audit.checks):
        write_json(OUT/(STEM+'_summary.json'),dict(validation='FAIL_SOURCE_PIN',checks=audit.checks));return 1
    raw=read_raw('test_01_r4c1_scalar_propagation_matrices.json')
    print('Deriving zero-sector projector and independent dust control...',flush=True)
    A,P,N,Jchain,evolved=jordan(audit,raw);dust=dust_control(audit)
    print('Reconstructing original fields and density on the Jordan chain...',flush=True)
    rec=reconstruction(audit,raw,Jchain)
    print('Comparing registered graph norms...',flush=True)
    samples=sample_norms(audit,rec,Jchain)
    formulas=OUT/(STEM+'_matrices.json')
    write_json(formulas,dict(schema='r4c1-zero-branch-v1',A=base.matrix_strings(A),P0=base.matrix_strings(P),
        N=base.matrix_strings(N),Jordan_chain=base.matrix_strings(Jchain),
        unit_initial_evolution=list(map(str,evolved)),dust_control=dust,
        original_q_from_Z=base.matrix_strings(rec['Q']),original_qdot_from_Z=base.matrix_strings(rec['Qdot']),
        auxiliaries_from_Z=base.matrix_strings(rec['aux']),density_from_Z=base.matrix_strings(rec['density']),
        dust_tilt_from_Z=base.matrix_strings(rec['tilt']),relative_tilt_from_Z=base.matrix_strings(rec['relative']),
        graph_rows=rec['names'],graph_map_on_chain=base.matrix_strings(rec['F']),
        graph_leading_powers=rec['powers'],rescaled_graph_limit=base.matrix_strings(rec['limit']),
        frame_density_limit_minor=str(rec['minor']),
        scope='Leading fast-mode embedding and frozen zero-principal sector only; original full evolution remains distinct'))
    samplepath=OUT/(STEM+'_samples.json');write_json(samplepath,samples)
    passed=sum(c['passed'] for c in audit.checks);valid=passed==len(audit.checks)
    result=dict(schema='r4c1-zero-branch-summary-v1',validation='PASS' if valid else 'FAIL',passed=passed,total=len(audit.checks),
        status='EQUAL_ORDER_BOUND_REJECTED_ORIGINAL_GRAPH_REGULARITY_CONTROL_ONLY' if valid else 'UNVALIDATED',
        physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_SUBSTANTIVE_FOR_FAILED_USES',
        inherited_unreviewed_inputs=['R9-MT1-S2','R9-MT1-S1','R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=inputs,executable_sha256=sha(Path(__file__)),
        artifacts={str(path.relative_to(ROOT)):sha(path) for path in (formulas,samplepath)},
        canonical=dict(MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED'),
        equal_order_bound='REJECTED_IN_STATED_CANONICAL_NORM',
        original_graph_norm='DERIVATIVE_WEIGHTED_PRINCIPAL_CONTROL_ONLY',full_constrained_IVP='NOT_PROVED',
        summary=dict(max_graph_amplification=samples['max_graph_amplification'],
            min_graph_eigenvalue=samples['min_graph_eigenvalue'],method_discrepancy=samples['max_method_discrepancy'],
            frame_density_limit_minor=str(rec['minor'])),checks=audit.checks,
        remaining=['full coupled principal/subprincipal energy estimate in declared spaces',
          'homogeneous/singular sectors','causality and cutoff','healthy GR and physical weak-field matching'])
    write_json(OUT/(STEM+'_summary.json'),result)
    Path(__file__).with_name(Path(__file__).name+'.sha256').write_text(sha(Path(__file__))+'  '+Path(__file__).name+'\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('validation','passed','total','status','summary')}))
    return 0 if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
