"""R4C1-S2: time-dependent canonical scalar equations, symbol and transfer.

No new action, parameter fitting or gate promotion. S1 constraints are inherited.
"""
from __future__ import annotations

import json
import platform
import time
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment

import test_01_r4c1_scalar_constraints as base
from test_01_r4c1_interacting_background import integrate,PARAMS,NAMES

ROOT=base.ROOT; OUT=base.OUT; STEM='test_01_r4c1_scalar_propagation'
sha=base.sha; write_json=base.write_json


class Audit(base.Audit):
    def exact(self,name,value):
        # SymPy factor can leave an unevaluated 0*sqrt(n). Expand the exact
        # algebraic residual before equality; do not use a numeric tolerance.
        if isinstance(value,s.MatrixBase):
            value=value.applyfunc(lambda x:s.expand(s.factor(x)))
        else:value=s.expand(s.factor(value))
        super().exact(name,value)


PINS={
    'Theory/Gates/RES-001/RES001_R4C1_SCALAR_PROPAGATION_CONTRACT_2026-09-26.md':
        'b4ecbc81119dd23b9597df3ca39b680cf44d07ae1a0a5564be78145b951354dd',
    'Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json':
        '27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a',
    'Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_summary.json':
        '10bdc2ac1faeb30203cd75f5015ab41e64dd19b6cef37193f6987baf85bfc033',
    'Analysis/MasterTests/test_01_r4c1_scalar_constraints.py':
        '977138ff89690608d21feb6e7f436ca0898ca86d1f9f702d536b2191648018ed',
    'Theory/Gates/RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md':
        '0b5f06aa3ca91876895c0f1ab521093fa44034f04ce62d605d676f9190824b1b',
    'Analysis/MasterTests/test_01_r4c1_interacting_background.py':
        '1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv':
        '0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa',
}

a,H,u,ud,v,vd,r,rd,pd,rho,C,k=[getattr(base,x) for x in
                           ('a','H','u','ud','v','vd','r','rd','pd','rho','C','k')]
PARAMETER_SUBS={base.MP:1,base.MU:s.Rational(2,3),base.c1:s.Rational(1,5),base.c2:s.Rational(1,10),
    base.c3:-s.Rational(1,5),base.c4:s.Rational(1,20),base.KQ:3,base.b:s.Rational(5,11),
    base.zeta:s.Rational(1,13),base.beta:s.Rational(2,5),base.m2:1,base.l4:s.Rational(1,3),
    base.l6:s.Rational(1,5),base.Lambda:2,base.mr2:2,base.lr:s.Rational(1,7),base.gr:s.Rational(3,7)}
radius=u*u+v*v
mass=1+radius/6+radius**2/80+3*r*r/14
FLOW={a:a*H,H:-s.Rational(5,11)*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho),
    u:ud,ud:-3*H*ud-mass*u,v:vd,vd:-3*H*vd-mass*v,
    r:rd,rd:-3*H*rd-2*r-r**3/7-3*radius*r/14,
    pd:-3*H*pd-2*rho/15,rho:(-3*H+2*pd/5)*rho,C:2*pd*C/5}
ARGS=list(FLOW)+[k]


def tidy(mat):
    return mat.applyfunc(s.cancel)


def dtime(expr):
    if isinstance(expr,s.MatrixBase): return expr.applyfunc(dtime)
    return s.Add(*(s.diff(expr,x)*fx for x,fx in FLOW.items() if expr.has(x)))


def load_matrices():
    raw=json.loads((OUT/'test_01_r4c1_scalar_constraints_matrices.json').read_text())
    symbols={str(x):x for x in vars(base).values() if isinstance(x,s.Symbol)}
    return [s.Matrix([[s.sympify(val,locals=symbols) for val in row] for row in raw[key]])
            .subs(PARAMETER_SUBS) for key in ('K','M','V')]


def canonical(audit):
    K,M,V=load_matrices()
    J=s.eye(6)
    J[:,4]=s.Matrix([ud,vd,rd,pd,C,k/a])
    expected=s.diag(1,1,1,3,66*H*H,s.Rational(1,6))
    audit.exact('intermediate_diagonal_kinetic',J.T*K*J-expected)
    R=J*s.diag(1,1,1,1/s.sqrt(3),1/(s.sqrt(66)*H),s.sqrt(6))/a**s.Rational(3,2)
    Rt=dtime(R);Rtt=dtime(Rt)
    audit.exact('unit_full_action_kinetic',a**3*R.T*K*R-s.eye(6))
    Mc=tidy(a**3*(R.T*K*Rt+R.T*M*R))
    Vc=tidy(a**3*(R.T*V*R-Rt.T*K*Rt-Rt.T*M*R-R.T*M.T*Rt))
    G=tidy(Mc-Mc.T);W=tidy(Vc+dtime(Mc))
    audit.exact('canonical_potential_symmetric',Vc-Vc.T)
    audit.exact('gyroscopic_antisymmetry',G+G.T)
    audit.exact('time_dependent_variational_identity',W-W.T-dtime(G))
    B=dtime(K)+3*H*K+M-M.T
    D=dtime(M)+3*H*M+V
    audit.exact('original_equation_velocity_transform',a**3*R.T*(2*K*Rt+B*R)-G)
    audit.exact('original_equation_position_transform',a**3*R.T*(K*Rtt+B*Rt+D*R)-W)
    wrong=tidy(a**3*R.T*D*R-W)
    audit.test('reject_omitted_transformation_derivatives',any(x!=0 for x in wrong))
    # Test the differential background dictionary against the pinned pure RHS.
    vals=background_args(integrate(PARAMS,'DOP853',1e-12,1e-14).y[:,0],2*np.pi)
    from test_01_r4c1_interacting_background import rhs
    yy=integrate(PARAMS,'DOP853',1e-12,1e-14).y[:,0]
    rhsvals=rhs(0.,yy,PARAMS)
    desired=[rhsvals[i] for i in (0,1,2,3,4,5,6,7,9,10)]+[PARAMS['beta']*yy[9]*np.exp(PARAMS['beta']*yy[8])]
    got=np.array(s.lambdify(ARGS,list(FLOW.values()),'numpy')(*vals),float)
    err=float(np.max(abs(got-desired)))
    audit.test('background_flow_matches_pinned_RHS',err<1e-13,err,'<1e-13 at independent initial state')
    return R,Mc,Vc,G,W


def coefficients(audit,Vc,G,W):
    p=s.Symbol('p',real=True)
    def coeffs(mat):
        replaced=mat.subs(k,a*p).applyfunc(s.cancel)
        polys=[s.Poly(x,p) for x in replaced]
        degree=max(poly.degree() for poly in polys if not poly.is_zero)
        return [s.Matrix(6,6,[poly.nth(j) for poly in polys]) for j in range(degree+1)]
    vp=coeffs(Vc);gp=coeffs(G);wp=coeffs(W)
    audit.test('spatial_polynomial_degree',len(vp)==5 and len(gp)<=2 and len(wp)==5,
               dict(V_degree=len(vp)-1,G_degree=len(gp)-1,W_degree=len(wp)-1))
    audit.exact('highest_spatial_rank_one',vp[4]-s.diag(0,0,0,s.Rational(5,33),0,0))
    audit.exact('EOM_highest_spatial_matches_action',wp[4]-vp[4])
    slow=[0,1,2,4,5]; fast=3
    # The physical EOM coefficient is W=Vc+Mcdot. Mc has a symmetric p^2
    # term whose derivative contributes at leading order. Freezing Vc alone
    # gave a genuine diagnostic omission in preserved attempt 01.
    audit.exact('EOM_cubic_matches_action',wp[3]-vp[3])
    cross=wp[3].extract(slow,[fast]);v4=wp[4][fast,fast]
    leading=tidy(wp[2].extract(slow,slow)-cross*cross.T/v4)
    gyro=gp[1].extract(slow,slow) if len(gp)>1 else s.zeros(5)
    audit.test('reject_omitted_cubic_Schur',any(s.factor(x)!=0 for x in cross*cross.T/v4))
    audit.exact('slow_principal_symmetric',leading-leading.T)
    audit.exact('slow_gyro_antisymmetric',gyro+gyro.T)
    audit.test('reject_missing_Mcdot_principal_term',any(s.factor(x)!=0 for x in wp[2]-vp[2]))
    nu=s.Symbol('scaled_growth_exponent')
    pencil=nu*nu*s.eye(5)+nu*gyro+leading
    char=s.factor(pencil[:2,:2].det()*pencil[2,2]*pencil[3:,3:].det())
    expected=nu**2*(nu**2+1)**2*(nu**2+1+(u*u+v*v)/13)*(nu**2+s.Rational(1,3))
    audit.exact('exact_slow_characteristic_polynomial',char-expected)
    A=s.BlockMatrix([[s.zeros(5),s.eye(5)],[-leading,-gyro]]).as_explicit()
    nullity=10-A.rank()
    audit.test('zero_branch_geometric_multiplicity',nullity==1,int(nullity),
               'algebraic multiplicity two but geometric multiplicity one; not a strong-hyperbolicity pass')
    print('Leading scalar symbol extracted',flush=True)
    return dict(Vp=vp,Gp=gp,Wp=wp,slow=slow,leading=leading,gyro=gyro,v4=v4,
                characteristic=char,zero_geometric_multiplicity=int(nullity))


def background_args(y,wavenumber):
    aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi,psi_d,rm,tau=y
    return [aa,hh,uu,uu_d,vv,vv_d,rr,rr_d,psi_d,rm,np.exp(PARAMS['beta']*psi),wavenumber]


def complex_list(values):
    return [[float(z.real),float(z.imag)] for z in values]


def generator(G,W):
    n=len(G)
    return np.block([[np.zeros((n,n)),np.eye(n)],[-W,-G]])


def symbol_scan(audit,flow,G,W,coefs):
    fl=s.lambdify(ARGS,coefs['leading'],'numpy',cse=True)
    fg=s.lambdify(ARGS,coefs['gyro'],'numpy',cse=True)
    fG=s.lambdify(ARGS,G,'numpy',cse=True);fW=s.lambdify(ARGS,W,'numpy',cse=True)
    records=[]; worst_resid=0.;worst_last=0.; instabilities=[]
    for t in (0.,.5,1.,2.,3.,4.):
        state=flow.sol(t); args=background_args(state,1.)
        LL=np.asarray(fl(*args),float);GG=np.asarray(fg(*args),float)
        lam=np.linalg.eigvals(generator(GG,LL))
        positive_phase=np.sort(np.imag(lam)[np.imag(lam)>1e-7])
        real_rate=float(np.max(abs(np.real(lam))))
        # A defective zero branch can acquire O(sqrt(roundoff)) apparent roots.
        unstable=real_rate>1e-6
        if unstable:instabilities.append(dict(t=t,scaled_exponents=complex_list(lam)))
        row=dict(t=t,leading_exponents=complex_list(lam),linear_branch_speeds=positive_phase.tolist(),
                 zero_exponents=int(np.sum(abs(lam)<1e-6)),formal_UV_growth=unstable,samples=[])
        for p in (20.,40.,80.,160.):
            args=background_args(state,p*state[0]);gg=np.asarray(fG(*args),float);ww=np.asarray(fW(*args),float)
            A=generator(gg,ww)
            eig,vec=np.linalg.eig(A)
            residual=0.
            for j,val in enumerate(eig):
                position=vec[:6,j]
                res=(val*val*np.eye(6)+val*gg+ww)@position
                denom=(abs(val)**2+abs(val)*np.linalg.norm(gg,2)+np.linalg.norm(ww,2))*np.linalg.norm(position)
                residual=max(residual,float(np.linalg.norm(res)/max(denom,1e-300)))
            worst_resid=max(worst_resid,residual)
            # The largest oscillatory pair is the single p^4 branch.
            positive=np.sort(np.imag(eig)[np.imag(eig)>1e-7])
            fast=float(positive[-1]/p**2) if len(positive) else None
            fast_error=abs(fast-np.sqrt(float(coefs['v4'])))/np.sqrt(float(coefs['v4'])) if fast is not None else 1e99
            candidates=positive[:-1]/p
            if len(positive_phase) and len(candidates)>=len(positive_phase):
                cost=abs(positive_phase[:,None]-candidates[None,:])
                ii,jj=linear_sum_assignment(cost)
                errors=cost[ii,jj]/np.maximum(abs(positive_phase[ii]),1e-15)
                err=float(np.max(errors));matched=candidates[jj].tolist()
            else:err=1e99;matched=[]
            if p==160.:worst_last=max(worst_last,fast_error,err)
            row['samples'].append(dict(p=p,fast_omega_over_p2=fast,fast_relative_error=fast_error,
                matched_linear_speeds=matched,linear_max_relative_error=err,pencil_residual=residual,
                max_instantaneous_real_exponent=float(max(np.real(eig))),exponents=complex_list(eig)))
        records.append(row)
    audit.test('frequency_pencil_residuals',worst_resid<1e-8,worst_resid,'<1e-8')
    # Asymptotic reach is a scientific diagnostic, not an implementation assertion.
    status='ASYMPTOTIC_CHECK_SUPPORTED' if worst_last<.05 else 'NONASYMPTOTIC_OR_UNRESOLVED'
    return dict(status=status,worst_final_relative_coefficient_error=worst_last,
        formal_UV_growth_detected=bool(instabilities),instabilities=instabilities,records=records)


def transfers(audit,flow,Mc,G,W):
    fM=s.lambdify(ARGS,Mc,'numpy',cse=True);fG=s.lambdify(ARGS,G,'numpy',cse=True)
    fW=s.lambdify(ARGS,W,'numpy',cse=True)
    grid=np.linspace(0.,4.,101);rows=[]
    symplectic=np.block([[np.zeros((6,6)),np.eye(6)],[-np.eye(6),np.zeros((6,6))]])
    for n in (1,2,4,8):
        solutions=[];stats=[]
        def coeff(t):
            args=background_args(flow.sol(t),2*np.pi*n)
            return np.asarray(fG(*args),float),np.asarray(fW(*args),float)
        def rhs(t,flat):
            gg,ww=coeff(t); FF=flat.reshape(12,12)
            return np.vstack((FF[6:],-ww@FF[:6]-gg@FF[6:])).ravel()
        # Dense exact linear Jacobian avoids 144 separate finite-difference calls.
        def jac(t,flat):
            gg,ww=coeff(t)
            return np.kron(generator(gg,ww),np.eye(12))
        for method in ('DOP853','Radau'):
            print(f'Evolving n={n}, {method}',flush=True)
            started=time.monotonic()
            options=dict(jac=jac) if method=='Radau' else {}
            sol=solve_ivp(rhs,(0.,4.),np.eye(12).ravel(),method=method,rtol=1e-9,atol=1e-11,t_eval=grid,**options)
            ok=sol.success and sol.t[-1]==4. and np.all(np.isfinite(sol.y))
            audit.test(f'transfer_solver_n{n}_{method}',ok,sol.message)
            if not ok:
                stats.append(dict(method=method,success=False,message=sol.message));continue
            ff=sol.y.T.reshape(-1,12,12);solutions.append(ff)
            m0=np.asarray(fM(*background_args(flow.sol(0.),2*np.pi*n)),float)
            T0=np.block([[np.eye(6),np.zeros((6,6))],[m0,np.eye(6)]])
            worst_sym=0.;amps=[];canamps=[]
            for it,tt in enumerate(grid):
                mt=np.asarray(fM(*background_args(flow.sol(tt),2*np.pi*n)),float)
                Tt=np.block([[np.eye(6),np.zeros((6,6))],[mt,np.eye(6)]])
                can=Tt@ff[it]@np.linalg.inv(T0)
                residual=float(np.linalg.norm(can.T@symplectic@can-symplectic,2)/(1+np.linalg.norm(can,2)**2))
                worst_sym=max(worst_sym,residual)
                amps.append(float(np.linalg.svd(ff[it],compute_uv=False)[0]))
                canamps.append(float(np.linalg.svd(can,compute_uv=False)[0]))
            audit.test(f'canonical_symplectic_n{n}_{method}',worst_sym<1e-6,worst_sym,'norm residual/(1+norm(F)^2)<1e-6')
            stats.append(dict(method=method,success=True,nfev=sol.nfev,njev=sol.njev,nlu=sol.nlu,
                seconds=time.monotonic()-started,max_symplectic_residual=worst_sym,
                endpoint_chart_amplification=amps[-1],max_chart_amplification=max(amps),
                max_canonical_chart_amplification=max(canamps),sample_amplifications=amps,
                endpoint_transfer=ff[-1].tolist()))
        discrepancy=None
        if len(solutions)==2:
            discrepancy=float(np.max(abs(solutions[0]-solutions[1]))/(1+np.max(abs(solutions[1]))))
            audit.test(f'two_solver_transfer_agreement_n{n}',discrepancy<1e-5,discrepancy,'<1e-5')
        rows.append(dict(n=n,comparison=discrepancy,methods=stats))
    return rows


def main():
    audit=Audit();observed={p:sha(ROOT/p) for p in PINS}
    for p,digest in PINS.items():audit.test('pin_'+p,observed[p]==digest,observed[p])
    receipt=json.loads((OUT/'test_01_r4c1_scalar_constraints_summary.json').read_text())
    for p,digest in {**receipt['inputs'],**receipt['artifacts']}.items():
        audit.test('S1_transitive_pin_'+p,sha(ROOT/p)==digest)
    if not all(x['passed'] for x in audit.checks):
        write_json(OUT/(STEM+'_summary.json'),dict(validation='FAIL_SOURCE_PIN',checks=audit.checks));return 1
    print('Deriving full time-dependent canonical action...',flush=True)
    R,Mc,Vc,G,W=canonical(audit)
    coefs=coefficients(audit,Vc,G,W)
    formulas=OUT/(STEM+'_matrices.json')
    write_json(formulas,dict(schema='r4c1-canonical-propagation-v1',background_order=list(map(str,ARGS)),
        q_from_x=base.matrix_strings(R),Mc=base.matrix_strings(Mc),Vc=base.matrix_strings(Vc),
        G=base.matrix_strings(G),W=base.matrix_strings(W),
        slow_principal_V=base.matrix_strings(coefs['leading']),slow_principal_G=base.matrix_strings(coefs['gyro']),
        quartic_omega_squared_over_p4=str(coefs['v4']),slow_indices=coefs['slow'],
        slow_characteristic=str(coefs['characteristic']),
        zero_branch=dict(algebraic_multiplicity=2,geometric_multiplicity=coefs['zero_geometric_multiplicity'],
            interpretation='Defective leading symbol in this scaled chart; no uniform strong-hyperbolicity certificate'),
        interpretation='Classical expanding-chart formal symbol; no EFT or uniform well-posedness certificate'))
    flow=integrate(PARAMS,'DOP853',1e-12,1e-14)
    pinned=np.genfromtxt(ROOT/'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv',delimiter=',',names=True)
    reference=np.vstack([pinned[name] for name in NAMES]);current=flow.sol(pinned['t'])
    err=float(np.max(abs(current-reference)/(1+abs(reference))))
    audit.test('background_for_evolution',flow.success and err<1e-8,err,'<1e-8')
    print('Scanning short-wavelength symbol...',flush=True)
    symbol=symbol_scan(audit,flow,G,W,coefs)
    # Save interim scientific evidence before potentially expensive integrations.
    symbol_path=OUT/(STEM+'_symbol.json');write_json(symbol_path,symbol)
    evolution=transfers(audit,flow,Mc,G,W)
    transfer_path=OUT/(STEM+'_transfers.json');write_json(transfer_path,evolution)
    passed=sum(c['passed'] for c in audit.checks);valid=passed==len(audit.checks)
    outcome='UNVALIDATED' if not valid else ('FORMAL_UV_GROWTH_DETECTED' if symbol['formal_UV_growth_detected'] else
        'SCALAR_PROPAGATION_SUPPORTED_ZERO_BRANCH_WELLPOSEDNESS_OPEN')
    result=dict(schema='r4c1-scalar-propagation-v1',validation='PASS' if valid else 'FAIL',passed=passed,total=len(audit.checks),
        status=outcome,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        research_execution='PROCEED_PROVISIONALLY' if valid else 'HOLD_SUBSTANTIVE_FOR_FAILED_USES',
        inherited_unreviewed_inputs=['R9-MT1-S1','R9-MT1-B1','R9-MT1-VARIATION'],
        inputs=observed,executable_sha256=sha(Path(__file__)),
        artifacts={str(p.relative_to(ROOT)):sha(p) for p in (formulas,symbol_path,transfer_path)},
        canonical=dict(MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED'),
        versions=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__),
        symbol_status=symbol['status'],formal_UV_growth_detected=symbol['formal_UV_growth_detected'],
        quartic_coefficient=str(coefs['v4']),checks=audit.checks,
        zero_branch=dict(algebraic_multiplicity=2,geometric_multiplicity=coefs['zero_geometric_multiplicity'],
            wellposedness='NOT_ESTABLISHED'),
        preserved_attempt_01=dict(summary='Analysis/MasterTests/outputs/r4c1_s2_attempt_01/test_01_r4c1_scalar_propagation_summary.json',
            sha256='9d5c84aa198cf942795bd96e1bd9c723be10fc490682c85c4b3ef160fa232e76',
            disposition='Superseded implementation: exact-zero normalization and missing Mcdot leading symbol corrected; action/thresholds unchanged'),
        limitations=['finite time and fixed B1 parameters','zero-speed branches require subleading and well-posedness analysis',
            'k=0 and singular charts excluded','amplification is chart dependent, not a stability verdict',
            'formal UV not a certified EFT domain','all-sector and nonlinear stability not established'])
    write_json(OUT/(STEM+'_summary.json'),result)
    Path(__file__).with_name(Path(__file__).name+'.sha256').write_text(sha(Path(__file__))+'  '+Path(__file__).name+'\n',encoding='ascii')
    print(json.dumps(dict(validation=result['validation'],passed=passed,total=len(audit.checks),status=outcome,
                        symbol_status=symbol['status'],quartic_coefficient=str(coefs['v4']))))
    return 0 if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
