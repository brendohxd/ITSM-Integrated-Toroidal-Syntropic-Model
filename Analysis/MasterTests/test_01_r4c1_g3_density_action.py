"""G3D: density coordinate, canonical boundary identity and signed action.

Formal slow branch only; no full physical cutoff, quantum or eta-rank claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Analysis/MasterTests/outputs'
PINS={
    "Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_REPORT_2026-09-30.md": "25b39464948805df96eeded13cc96fa04c87e767e1781113514f85d5fd957771",
    "Analysis/MasterTests/outputs/r4c1_g3f_attempt_01/summary.json": "3c3241a44e43b986971c8c340643b6b9c87ca97c803347cb9da5c0a934fa05e1",
    "Theory/Gates/RES-001/RES001_R4C1_G3_DENSITY_ACTION_CONTRACT_2026-09-30.md": "0ff843db7c1887fea71e307fd8801841427628d0426bf8f9bd83e4b78e9c5758",
    "Analysis/MasterTests/test_01_r4c1_g3_finite_k.py": "24ef13486d8477cb021dc4931d6e64c6d6fcc8fa52a330c106515c4507624504"
}
TIMES=(0.,.5,1.,2.,3.,4.)
KS=(20.,40.,80.)


def sha(data):return hashlib.sha256(data).hexdigest()


def verify(pins):
    for name,digest in pins.items():
        if sha((ROOT/name).read_bytes())!=digest:
            raise RuntimeError('FROZEN_INPUT_HASH_MISMATCH: '+name)


def tidy(expr):
    if isinstance(expr,s.MatrixBase):return expr.applyfunc(tidy)
    return s.factor(s.cancel(expr))


def derive(audit):
    import test_01_r4c1_scalar_constraints as b
    eta=s.Symbol('eta',positive=True)
    chi,v=s.symbols('chi v_chi',real=True)
    cd,vd=s.symbols('chi_path_dot v_path_dot',real=True)
    D,Dd,Ddd,P=s.symbols('D Ddot Dddot P_D',real=True)
    symbols={str(z):z for z in vars(b).values() if isinstance(z,s.Symbol)}
    symbols.update(eta=eta)
    parse=lambda val:s.sympify(val,locals=symbols)
    raw=json.loads((OUT/'r4c1_g3s_attempt_01/matrices.json').read_bytes())
    previous=json.loads((OUT/'r4c1_g3e_attempt_01/formulas.json').read_bytes())
    flow={parse(key):parse(val) for key,val in raw['flow'].items()}
    def dt(expr):
        if isinstance(expr,s.MatrixBase):return expr.applyfunc(dt)
        return sum(s.diff(expr,z)*value for z,value in flow.items() if expr.has(z))
    mass=parse(previous['normalized_coefficients'][0])
    kappa=tidy(eta*parse(previous['kinetic_prefactor'])/b.k**2)
    f,g=[tidy(s.sqrt(eta)*parse(value)) for value in previous['physical_leading_maps']['density_contrast']]
    beta=2*eta**2/5;Mc2=1-eta/12
    B=s.Matrix([[0,1],[-mass,0]])
    h=tidy(dt(f)-g*mass);j=tidy(f+dt(g))
    T=s.Matrix([[f,g],[h,j]]);delta=tidy(T.det())
    audit.exact('density_velocity_coefficient_cancels',j)
    audit.exact('density_derivative_position_coefficient',h-s.sqrt(6)/b.a**s.Rational(5,2))
    audit.exact('density_phase_determinant',delta+(12-eta)/(b.a**5*b.rho))
    inv=T.adjugate()/delta
    transformed=tidy((dt(T)+T*B)*inv)
    audit.exact('density_generator_position_row',transformed[0,:]-s.Matrix([[0,1]]))
    friction=tidy(-transformed[1,1]);density_mass=tidy(-transformed[1,0])
    audit.exact('density_friction_from_generator',friction-2*b.H-beta*b.pd)
    audit.exact('density_mass_from_generator',density_mass+b.rho/(2*Mc2))
    K=tidy(kappa/delta)
    audit.exact('density_kinetic_from_inherited_symplectic_form',K-b.a**5*b.rho/b.k**2)
    audit.exact('density_kinetic_log_derivative',dt(K)/K-friction)
    audit.exact('phase_symplectic_pullback',T.T*s.Matrix([[0,K],[-K,0]])*T-s.Matrix([[0,kappa],[-kappa,0]]))
    audit.test('positive_density_kinetic_on_declared_domain',tidy(K/(b.a**5*b.rho/b.k**2))==1,
               'a,rho_m,k>0 imply K_D>0; no global positive-energy claim')
    audit.test('density_map_rank_on_declared_domain',tidy(delta/(-(12-eta)/(b.a**5*b.rho)))==1,
               '0<eta<=1,a,rho_m>0 imply det(T)<0; inherited singular boundaries retained')
    q=f*chi+g*v;V=h*chi+j*v;newP=K*V
    boundary=tidy(-kappa*(f*h*chi**2+2*g*h*chi*v+g*j*v**2)/(2*delta))
    one_form=s.Matrix([kappa*v-newP*f,-newP*g])
    audit.exact('canonical_one_form_boundary_gradient',one_form-s.Matrix([s.diff(boundary,chi),s.diff(boundary,v)]))
    canonical=s.Matrix([q,newP]).jacobian([chi,v])
    audit.exact('canonical_phase_transform',canonical.T*s.Matrix([[0,1],[-1,0]])*canonical-s.Matrix([[0,kappa],[-kappa,0]]))
    oldH=kappa*(v**2+mass*chi**2)/2
    newH=tidy(K*(V**2+density_mass*q**2)/2)
    map_t=dt(f)*chi+dt(g)*v
    boundary_t=tidy(dt(boundary))
    audit.exact('time_dependent_Hamiltonian_boundary_identity',newH-oldH-newP*map_t-boundary_t)
    oldL=kappa*v*cd-oldH
    newL=newP*(f*cd+g*vd+map_t)-newH
    full_boundary=s.diff(boundary,chi)*cd+s.diff(boundary,v)*vd+boundary_t
    audit.exact('off_shell_first_order_action_identity',oldL-newL-full_boundary)
    Ldust=K*(Dd**2-density_mass*D**2)/2
    Hdust=P**2/(2*K)+K*density_mass*D**2/2
    audit.exact('density_momentum_elimination',s.diff(Ldust,Dd)-K*Dd)
    audit.exact('density_Legendre_transform',Hdust-(Dd*s.diff(Ldust,Dd)-Ldust).subs(Dd,P/K))
    Euler=K*Ddd+dt(K)*Dd-s.diff(Ldust,D)
    audit.exact('density_Euler_equation',Euler-K*(Ddd+friction*Dd+density_mass*D))
    Hvel=K*(Dd**2+density_mass*D**2)/2
    energy_rate=dt(Hvel)+s.diff(Hvel,D)*Dd+s.diff(Hvel,Dd)*(-friction*Dd-density_mass*D)
    expected_rate=-dt(K)*Dd**2/2+dt(K*density_mass)*D**2/2
    audit.exact('density_time_dependent_energy_balance',energy_rate-expected_rate)
    audit.exact('density_Hamiltonian_Hessian_determinant',s.det(s.hessian(Hdust,[P,D]))-density_mass)
    # Independent rational coefficient-jet test; it is not a cosmological
    # initial state and does not impose chi_path_dot=v off shell.
    event={b.a:s.Rational(7,5),b.H:s.Rational(3,5),b.u:s.Rational(2,3),b.ud:s.Rational(1,7),
        b.v:s.Rational(1,5),b.vd:s.Rational(2,7),b.r:s.Rational(1,4),b.rd:-s.Rational(1,9),
        b.pd:s.Rational(1,8),b.rho:s.Rational(1,10),b.C:s.Rational(6,5),eta:s.Rational(1,4),b.k:40,
        chi:s.Rational(2,7),v:-s.Rational(1,9),cd:s.Rational(3,11),vd:-s.Rational(2,13)}
    audit.exact('independent_rational_first_order_action_identity',(oldL-newL-full_boundary).subs(event))
    audit.exact('independent_rational_canonical_map',(canonical.T*s.Matrix([[0,1],[-1,0]])*canonical).subs(event)-s.Matrix([[0,kappa],[-kappa,0]]).subs(event))
    # Formal GR dust coefficient control only; original eta=0 rank is not
    # inverted. Zero scalar/force velocities and rho_m=3H^2 are declared.
    gr={eta:0,b.ud:0,b.vd:0,b.rd:0,b.pd:0,b.rho:3*b.H**2}
    Kgr=tidy(K.subs(gr));fgr=tidy(friction.subs(gr));mgr=tidy(density_mass.subs(gr))
    def dgr(expr):return s.diff(expr,b.a)*b.a*b.H+s.diff(expr,b.H)*(-3*b.H**2/2)
    audit.exact('GR_dust_positive_kinetic_coefficient',Kgr-3*b.a**5*b.H**2/b.k**2)
    audit.exact('GR_dust_kinetic_log_derivative',dgr(Kgr)/Kgr-2*b.H)
    audit.exact('GR_dust_friction',fgr-2*b.H)
    audit.exact('GR_dust_mass',mgr+3*b.H**2/2)
    for name,mode in [('growing',b.a),('decaying',b.a**(-s.Rational(3,2)))]:
        audit.exact('GR_density_'+name+'_mode',dgr(dgr(mode))+fgr*dgr(mode)+mgr*mode)
    return dict(base=b,eta=eta,args=list(flow)+[eta,b.k],phase_args=[chi,v],
        f=f,g=g,h=h,j=j,delta=delta,kappa=kappa,K=K,friction=friction,mass=density_mass,
        T=T,transformed=transformed,boundary=boundary,oldH=oldH,newH=newH,newP=newP,
        map_t=map_t,boundary_t=boundary_t,Ldust=Ldust,Hdust=Hdust,energy_rate=tidy(expected_rate),
        GR_K=Kgr,GR_friction=fgr,GR_mass=mgr)


def numerical(audit,d):
    family=json.loads((OUT/'r4c1_g3_attempt_01/summary.json').read_bytes())
    tr=np.load(OUT/'r4c1_g3_attempt_01/trajectories.npy',allow_pickle=False)
    keys=('K','delta','friction','mass','oldH','newH','newP','map_t','boundary_t')
    fun={key:s.lambdify(d['args']+d['phase_args'],d[key],'numpy',cse=True) for key in keys}
    rows=[];worst_identity=worst_coefficient=0.
    for ie,member in enumerate(family['family']):
        eta=member['eta'];params=member['parameters']
        for im,method in enumerate(family['trajectory']['methods']):
            for k in KS:
                group=[]
                for t in TIMES:
                    a,H,u,ud,v,vd,r,rd,psi,pd,rho,tau=tr[ie,im,1:,int(round(t*200))]
                    args=[a,H,u,ud,v,vd,r,rd,pd,rho,np.exp(params['beta']*psi),eta,k,.3,-.2]
                    values={key:float(fn(*args)) for key,fn in fun.items()}
                    beta=params['beta'];Mc2=1-eta/12
                    expected=[a**5*rho/k**2,-(12-eta)/(a**5*rho),2*H+beta*pd,-rho/(2*Mc2)]
                    actual=[values[key] for key in ('K','delta','friction','mass')]
                    coefficient_error=float(max(abs(x-y)/(1+abs(y)) for x,y in zip(actual,expected)))
                    identity_error=abs(values['newH']-values['oldH']-values['newP']*values['map_t']-values['boundary_t'])/(1+abs(values['newH'])+abs(values['oldH']))
                    worst_identity=max(worst_identity,identity_error);worst_coefficient=max(worst_coefficient,coefficient_error)
                    row=dict(eta=eta,method=method,k=k,t=t,K_D=values['K'],density_phase_determinant=values['delta'],
                        friction=values['friction'],density_mass=values['mass'],
                        density_Hamiltonian_Hessian=[1/values['K'],values['K']*values['mass']],
                        coefficient_error=coefficient_error,Hamiltonian_boundary_error=identity_error,
                        energy_signature='INDEFINITE_WITH_POSITIVE_KINETIC' if values['K']>0 and values['mass']<0 else 'UNEXPECTED')
                    rows.append(row);group.append(row)
                label=f'eta_{eta}_{method}_k_{k}'
                audit.test(label+'_regular_density_phase',all(v['K_D']>0 and v['density_phase_determinant']<0 for v in group))
                audit.test(label+'_indefinite_Hamiltonian_positive_kinetic',all(v['energy_signature']=='INDEFINITE_WITH_POSITIVE_KINETIC' for v in group))
                err=max(v['coefficient_error'] for v in group)
                audit.test(label+'_coefficient_agreement',err<=1e-12,err,'normalized <=1e-12')
                err=max(v['Hamiltonian_boundary_error'] for v in group)
                audit.test(label+'_Hamiltonian_boundary_identity',err<=1e-12,err,'normalized <=1e-12')
    return dict(rows=rows,events=len(rows),worst_coefficient_error=worst_coefficient,
        worst_Hamiltonian_boundary_error=worst_identity,min_K_D=min(v['K_D'] for v in rows),
        max_density_mass=max(v['density_mass'] for v in rows),min_friction=min(v['friction'] for v in rows))


def evaluate():
    verify(PINS)
    parent=json.loads((OUT/'r4c1_g3f_attempt_01/summary.json').read_bytes())
    inherited={**parent['source_sha256'],**parent['transitive_source_sha256']};verify(inherited)
    import test_01_r4c1_equal_newton_scalar as gs
    audit=gs.Audit();data=derive(audit);samples=numerical(audit,data)
    keys=('f','g','h','j','delta','kappa','K','friction','mass','boundary','Ldust','Hdust','energy_rate','GR_K','GR_friction','GR_mass')
    formulas={key:str(data[key]) for key in keys}
    formulas['density_phase_map']=[[str(v) for v in row] for row in data['T'].tolist()]
    formulas['density_generator']=[[str(v) for v in row] for row in data['transformed'].tolist()]
    formulas['singular_domains']=['rho_m=0','a=0','k=0','inherited H=0 gauge boundary','inherited eta=0 auxiliary rank change']
    formulas['scope']='Equivalent formal slow action only; not full physical energy/cutoff or eta endpoint theorem'
    payload=(json.dumps(formulas,indent=2,allow_nan=False)+'\n').encode()
    passed=sum(c['passed'] for c in audit.checks)
    result=dict(schema='r4c1-g3d-v1',validation='PASS_LOCAL_CHECKS' if passed==len(audit.checks) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(audit.checks),checks=audit.checks,source_sha256=PINS,transitive_source_sha256=inherited,
        script_sha256=sha(Path(__file__).read_bytes()),artifacts={'formulas.json':sha(payload)},samples=samples,
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__),
        status='CONDITIONAL_POSITIVE_DENSITY_KINETIC_FORMAL_GR_DUST_CONTROL_FULL_THEORY_HOLD' if passed==len(audit.checks) else 'DENSITY_ACTION_FAILURES_REQUIRE_DISPOSITION',
        original_frame_kinetic_sign_changed=False,positive_definite_density_Hamiltonian=False,
        physical_EFT_cutoff='NOT_DERIVED',stationary_quantum_norm_verified=False,full_all_sector_kinetic_verified=False,
        healthy_continuous_full_GR_limit_verified=False,canonical_Test1_pass=False,canonical_Test2_pass=False,canonical_Test3_pass=False,
        physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False,
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED')
    return result,payload


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default='Analysis/MasterTests/outputs/r4c1_g3d_attempt_01')
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args();directory=(ROOT/args.output_dir).resolve()
    if not directory.is_relative_to(OUT.resolve()):raise RuntimeError('OUTPUT_OUTSIDE_MASTER_TESTS')
    verify(PINS)
    if not args.replay and directory.exists():raise RuntimeError('OUTPUT_ALREADY_EXISTS_USE_REPLAY_OR_NEW_ATTEMPT')
    result,payload=evaluate();encoded=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode()
    identical=None
    if args.replay:
        identical=(directory/'summary.json').read_bytes()==encoded and (directory/'formulas.json').read_bytes()==payload
        print(json.dumps(dict(replay=True,byte_identical=identical,summary_sha256=sha(encoded))))
    else:
        directory.mkdir(parents=True,exist_ok=False)
        for name,value in (('summary.json',encoded),('formulas.json',payload)):
            (directory/name).write_bytes(value)
            (directory/(name+'.sha256')).write_text(sha(value)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('validation','passed','total','status','physics_pass')}))
    for check in result['checks']:
        if not check['passed']:print(json.dumps(check))
    if args.replay and not identical:return 2
    return 0 if result['passed']==result['total'] else 1


if __name__=='__main__':raise SystemExit(main())

