"""Exact adequacy screen for density-only weakening of a preserved control."""
from pathlib import Path
import argparse,hashlib,json
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_WEAK_DENSITY_ENERGY_SCREEN_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v2_attempt_01/summary.json'
OLD_REPORT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PHYSICAL_NORM_V2_REPORT_2026-10-31.md'
CHART='Analysis/MasterTests/outputs/rtau_compensated_source_chart_v1_20261103/receipt.json'
TRANSPORT='Analysis/MasterTests/outputs/rtau_compensated_transport_v2_20261103/receipt.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def calculate():
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    clean=lambda x:sp.factor(sp.cancel(x))
    zero=lambda m:all(clean(v)==0 for v in m)
    encode=lambda m:[[str(clean(x)) for x in row] for row in m.tolist()]
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    parent=json.loads((ROOT/PARENT).read_text())
    for rel,h in parent['source_sha256'].items():
        assert sha(ROOT/rel)==h,rel
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,PARENT,OLD_REPORT,CHART,TRANSPORT):pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel in pins:
        for p in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if p.exists():snapshot[p]=(sha(p),p.stat().st_mtime_ns)
    check('all_219_current_and_original_control_source_hashes_match',len(original)==219)
    for label,d in [('original_full_energy',parent),('initial_chart',json.loads((ROOT/CHART).read_text())),('density_sector',json.loads((ROOT/TRANSPORT).read_text()))]:
        check(label+'_owner_passes',d['passed']==d['total'] and all(c['passed'] for c in d['checks']))
    names=parent['variables'];variables=sp.symbols(' '.join(names),real=True)
    loc=dict(zip(names,variables));k=sp.Symbol('kappa',positive=True);loc['kappa']=k
    parse=lambda rows:sp.Matrix([[sp.sympify(x,locals=loc) for x in row] for row in rows])
    a,H,u,v,r,du,dv,dr,p,psi,rho=variables
    initial=dict(zip(variables,[1,sp.sqrt(sp.Rational(3469,4620)),1,0,1,0,1,sp.Rational(1,4),sp.Rational(1,5),0,sp.Rational(1,5)]))
    G=parse(parent['scalar']['physical_generator']).subs(initial).applyfunc(clean)
    E=parse(parent['scalar']['energy_form']).subs(initial).applyfunc(clean)
    A2old=parse(parent['scalar']['A2']).subs(initial).applyfunc(clean)
    A1old=parse(parent['scalar']['A1']).subs(initial).applyfunc(clean)
    check('original_principal_quartic_energy_identity',zero(A2old.conjugate().T*E+E*A2old))
    check('original_principal_ordinary_energy_identity',zero(A1old.conjugate().T*E+E*A1old))
    check('original_energy_positive_at_declared_control',all(clean(E[:i,:i].det())>0 for i in range(1,13)))

    W=sp.eye(12);W[0,0]=1/k
    Wdot=sp.zeros(12);Wdot[0,0]=initial[H]/k
    GW=((Wdot+W*G)*W.inv()).applyfunc(clean)
    check('complete_weakening_conjugacy_includes_Wdot',zero(GW*W-W*G-Wdot))
    check('dropping_weakening_drift_rejected',Wdot[0,0]!=0 and clean(GW[0,0]+2*initial[H])==0)
    A2=GW.applyfunc(lambda x:clean(sp.limit(x/k**2,k,sp.oo)))
    A1=(GW-k*k*A2).applyfunc(lambda x:clean(sp.limit(x/k,k,sp.oo)))
    check('mixed_principal_limits_are_finite',not (A2.has(sp.oo,sp.zoo,sp.nan) or A1.has(sp.oo,sp.zoo,sp.nan)))
    fast=[5,11];ordinary=[0,1,2,3,4,6,7,8,9,10]
    check('quartic_pair_retained_unchanged',zero(A2-A2old) and A2.extract(fast,fast).det()!=0)
    check('ordinary_fast_A2_cross_blocks_zero',zero(A2.extract(ordinary,list(range(12)))) and zero(A2.extract(fast,ordinary)))
    check('ordinary_to_fast_feedback_absent_at_order_k',zero(A1.extract(ordinary,fast)))
    # The fast<-ordinary order-k block is retained. The fast inverse is
    # O(k^-2) at ordinary frequencies; its Schur feedback is subleading.
    check('fast_forcing_is_not_deleted',any(x!=0 for x in A1.extract(fast,ordinary)))
    O=A1.extract(ordinary,ordinary);Oold=A1old.extract(ordinary,ordinary)
    lam=sp.Symbol('lambda')
    poly=sp.factor(O.charpoly(lam).as_expr());oldpoly=sp.factor(Oold.charpoly(lam).as_expr())
    check('original_zero_pair_semisimple',len(Oold.nullspace())==2)
    check('ordinary_characteristic_polynomial_unchanged',clean(poly-oldpoly)==0)
    multiplicity=min(j for (j,),coefficient in sp.Poly(poly,lam).terms() if coefficient!=0)
    check('weakened_zero_root_algebraic_two_geometric_one',multiplicity==2 and len(O.nullspace())==1)
    r0=sp.zeros(10,1);r1=sp.zeros(10,1)
    r0[1]=-18*sp.I;r0[5]=sp.Rational(12,11)
    r1[0]=33;r1[6]=-18*sp.I
    check('exact_ordinary_Jordan_zero_vector',zero(O*r0))
    check('exact_ordinary_Jordan_generalized_vector',zero(O*r1-r0))
    check('Jordan_vectors_independent',sp.Matrix.hstack(r0,r1).rank()==2)
    Eold=E.extract(ordinary,ordinary)
    check('old_positive_energy_does_not_make_zero_vector_null',clean((r0.conjugate().T*Eold*r0)[0])==1)

    # Independent closed principal representation in (density/k,D,X,Pi_vz).
    R=sp.zeros(4,10);R[0,0]=1;R[1,1]=-sp.I/198;R[1,5]=1
    R[2,1]=sp.Rational(12,11);R[2,5]=18*sp.I;R[3,6]=1
    S=sp.Matrix([[0,0,0,0],[sp.Rational(1,33),0,0,0],[6*sp.I/11,0,0,1],[0,0,-sp.Rational(1,3),0]])
    check('independent_D_X_principal_representation',zero(R*O-S*R))
    t=sp.Symbol('t',real=True)
    check('principal_chain_solution_has_k_t_term',zero(sp.diff(r1+k*t*r0,t)-k*O*(r1+k*t*r0)))
    aa,xx,yy,dd=sp.symbols('a x y d',real=True)
    h=sp.Matrix([[aa,xx+sp.I*yy],[xx-sp.I*yy,dd]]);N=sp.Matrix([[0,1],[0,0]])
    skew=h*N+N.T*h
    check('Hermitian_Jordan_skewness_forces_null_energy',clean(skew[0,1]-aa)==0 and clean(skew[1,0]-aa)==0)
    check('Bessel_Hminus1_and_k_inverse_weights_uniformly_equivalent',sp.simplify((1+k*k)/k**2-1)==1/k**2)
    check('all_source_sidecar_bytes_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snapshot.items()))
    return dict(kind='RTAU_WEAK_DENSITY_ENERGY_ADEQUACY_CONTROL_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),background='Original declared homogeneous control only; not registered vortical prepared root',
                old_state_order=parent['physical_variables'],weakening='sigma -> sigma/kappa only, with actual Wdot; all other variables retained',
                quartic_principal=encode(A2),ordinary_principal=encode(O),ordinary_polynomial=str(poly),
                independent_principal_block=encode(S),zero_vector=encode(r0),generalized_vector=encode(r1),
                zero_algebraic_multiplicity=multiplicity,zero_geometric_multiplicity=len(O.nullspace()),
                scientific_disposition='DENSITY_ONLY_WEAKENING_REJECTED_AS_UNIFORMLY_POSITIVE_ORDER_ZERO_PRINCIPAL_ENERGY_IN_ORIGINAL_CONTROL',
                initial_chart_and_density_sector='Remain valid in their declared initial/component scope; neither was a full evolution theorem',
                prepared_inhomogeneous_conclusion='NOT_ESTABLISHED_BY_THIS_CONTROL',full_weak_propagator_illposedness='NOT_CLAIMED',
                next_route='Retain physical density strength or derive a genuinely equivalent complete action-observable norm; do not infer coupled energy from the weak static chart',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')

def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps({'status':'FAILED_ATTEMPT','error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n')
        raise
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],
                      'disposition':data['scientific_disposition'],'zero_multiplicities':[data['zero_algebraic_multiplicity'],data['zero_geometric_multiplicity']]},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
