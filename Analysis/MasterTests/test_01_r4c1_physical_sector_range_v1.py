"""Exact range-method controls; not physical-mode admission or stability."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sy

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_SECTOR_READINESS_V1_CONTRACT_2026-10-27.md'
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_SECTOR_RANGE_V1_ADDENDUM_2026-10-27.md'
PINS = {
    CONTRACT: '431bbe4379aa756d0b22dd7c15ede57d48f6909bc3c9f7ea349442da1e1ca7fc',
    'Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py':
        '99a71aa721140a59c0e27af4632e4c52c9ae30138a8ae9af53b690b5c2cee157',
    'Analysis/MasterTests/test_01_r4c1_material_seed_feasibility_v1.py':
        '4dca68f194c0a07087c808c06718bf871a8a78dcf1a264cb32293bb3ab06af75',
}
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENC = lambda value: (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def metadata():
    pins = dict(PINS)
    for name in (ADDENDUM, Path(__file__).relative_to(ROOT).as_posix()):
        pins[name] = SHA((ROOT/name).read_bytes())
    for name, wanted in pins.items():
        if SHA((ROOT/name).read_bytes()) != wanted:
            raise ValueError('source drift: '+name)
    return dict(source_hashes=pins, sympy=sy.__version__)


def calculate():
    checks = []
    def check(name, condition):
        checks.append(dict(name=name, passed=bool(condition)))
    def zero(matrix):
        return all(sy.simplify(x) == 0 for x in matrix)

    q1,q2,p1,p2,Z,s,b = sy.symbols('q1 q2 p1 p2 Z s b', real=True)
    X = sy.Matrix([q1,q2,p1,p2,Z,s]); g=b*(q1*q1+q2*q2)
    theta=sy.Matrix([p1,p2,0,0,-g*s,0])
    omega=sy.Matrix(6,6,lambda i,j:sy.diff(theta[j],X[i])-sy.diff(theta[i],X[j]))
    r=sy.Matrix(sy.symbols('r0:6'))
    dg=sy.diff(g,q1)*r[2]+sy.diff(g,q2)*r[3]
    v=sy.Matrix([r[2],r[3],-r[0]+s*sy.diff(g,q1)*r[5]/g,
                 -r[1]+s*sy.diff(g,q2)*r[5]/g,-r[5]/g,(r[4]-s*dg)/g])
    check('full_inverse_action_including_crosses',zero(omega*v-r))
    check('antisymmetric_two_form',zero(omega+omega.T))
    check('determinant_g_squared',sy.factor(omega.det()-g*g)==0)
    Y=sy.Matrix([q1,q2,p1,p2,Z,-g*s]); jac=Y.jacobian(X)
    J=sy.zeros(6)
    for i,j in ((0,2),(1,3),(4,5)):
        J[i,j]=-1; J[j,i]=1
    check('Darboux_pullback_full_crosses',zero(jac.T*J*jac-omega))
    check('Darboux_Jacobian_minus_g',sy.factor(jac.det()+g)==0)
    node=omega.subs({q1:0,q2:0})
    check('alignment_two_auxiliary_null_rows',zero(node[4:6,:]))
    check('alignment_rank_is_canonical_only',node.rank()==4)
    u=sy.Matrix(sy.symbols('u0:6')); T=sy.Matrix(sy.symbols('T0:6'))
    D=sy.Matrix.hstack(*[(omega.diff(x)*T) for x in X])
    H=sy.eye(6)+sy.ones(6)
    K=H-D; odot=sy.zeros(6)
    for x,t in zip(X,T):odot += omega.diff(x)*t
    check('retained_drift_balance',zero(K-K.T+odot))
    check('drift_not_identically_zero',not zero(odot))
    omitted=omega.copy()
    for i in range(4):omitted[i,4]=omitted[4,i]=0
    check('cross_deletion_rejected',not zero(omitted*v-r))

    x,t,k,e=sy.symbols('x t k e',positive=True)
    gx=b*e**2*sy.sin(k*x)**2
    check('nodal_quadratic_leading_order',sy.limit(gx/x**2,x,0)==b*e**2*k**2)
    for order in (0,1,2,3):
        power=2*order-4
        check('L2_monomial_order_'+str(order),(power>-1)==(order>=2))
    check('C1_borderline_double_trace_not_sufficient',2*sy.Rational(3,2)-4==-1)
    angle=sy.symbols('angle',real=True)
    for node_angle in (sy.pi/2,3*sy.pi/2):
        check('periodic_double_zero_'+str(node_angle),
              sy.cos(node_angle)**2==0 and
              sy.diff(sy.cos(angle)**2,angle).subs(angle,node_angle)==0)
        check('periodic_simple_zero_rejected_'+str(node_angle),
              sy.sin(2*node_angle)==0 and
              sy.diff(sy.sin(2*angle),angle).subs(angle,node_angle)!=0)
    moving=(x-t)**2
    dtrace=sy.diff(moving,x,t)+sy.diff(moving,x,2)
    check('moving_first_trace_transport_cancels',dtrace==0)
    check('omitting_node_transport_rejected',sy.diff(moving,x,t)==-2)
    G,PZ=sy.symbols('G PZ',nonzero=True)
    a,c,d=sy.symbols('a c d')
    F=a*s*s/2+c*s**3+d*s**4
    check('fixed_configuration_curvature_map',sy.simplify(
        sy.diff(F.subs(s,-PZ/G),PZ,2)-sy.diff(F,s,2).subs(s,-PZ/G)/G**2)==0)
    return dict(result_id='R4C1-PHYSICAL-SECTOR-RANGE-V1', metadata=metadata(),
        scope='Exact range/Darboux/nodal method controls; NOT full physical admission',
        checks=checks, passed=sum(c['passed'] for c in checks), total=len(checks),
        physics_pass=False, gate_effect='NONE', review_status='DEFERRED',
        physical_admission='UNRESOLVED', physical_normalization='UNRESOLVED',
        formulas=dict(g='b*sqrt(det h)*V^T*h*V', pZ='-g*s',
                      vZ='-r_s/g', vs='(r_Z-s*Dg[r_P])/g',
                      smooth_node_conditions='Phi=0 and partial_z Phi=0 at BOTH nodes',
                      regularity='C2 scalar sources; full remaining tangent conditions retained'))


def main():
    parser=argparse.ArgumentParser(); group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path)
    args=parser.parse_args(); result=calculate(); data=ENC(result)
    directory=args.replay or args.output
    if args.replay:
        if (directory/'summary.json').read_bytes()!=data:raise ValueError('replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False)
        path=directory/'summary.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('passed','total','physics_pass','physical_admission')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
