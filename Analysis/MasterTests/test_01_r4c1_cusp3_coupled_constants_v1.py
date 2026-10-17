"""Independent all-domain constant proof for the full V3 cusp response."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sympy as s
import test_01_r4c1_three_family_weighted_evolution_v4 as weighted

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SOURCE='Analysis/MasterTests/test_01_r4c1_cusp3_coupled_tail_v3.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CUSP3_COUPLED_TAIL_CONSTANTS_V1_ADDENDUM_2026-10-17.md'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT=BASE+'r4c1_cusp3_coupled_tail_attempt_03/'
PARENT_HASH='a9645d8477a2693514181be81df293360f22b37ec6574701f9b6c5898c30012c'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENCODE=lambda q:(json.dumps(q,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()


def calculate():
    parent=json.loads((ROOT/(PARENT+'summary.json')).read_bytes())
    if SHA((ROOT/(PARENT+'summary.json')).read_bytes())!=PARENT_HASH:
        raise ValueError('Frozen complete V3 summary mismatch')
    if parent['passed']!=parent['total'] or len(parent['cases'])!=9:
        raise ValueError('V3 did not complete all nine cases')
    pins={SOURCE:'4753b2a55745ef774e310853ed866575d821a0aeebfe8485c9887af0ecd3efc2',
          CONTRACT:SHA((ROOT/CONTRACT).read_bytes()),SELF:SHA((ROOT/SELF).read_bytes())}
    pins.update(parent['source_sha256'])
    pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins[PARENT+'summary.json']=PARENT_HASH
    absent=parent['inherited_sidecars_absent']
    paths=[]
    for name,digest in pins.items():
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest:raise ValueError('Frozen source mismatch '+name)
        paths.append(p)
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise ValueError('Frozen sidecar mismatch '+name)
            paths.append(side)
        elif name not in absent:raise ValueError('Unregistered absent sidecar '+name)
    snapshot=lambda:[(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                     for p in sorted(paths)]
    before=snapshot();checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def exact(name,q):check(name,s.cancel(q)==0,str(s.cancel(q)))
    tree=ast.parse((ROOT/SOURCE).read_text())
    cls=next(q for q in tree.body if isinstance(q,ast.ClassDef) and q.name=='Case')
    method=next(q for q in cls.body if isinstance(q,ast.FunctionDef) and q.name=='bounds')
    assignments={q.targets[0].id:q.value for q in ast.walk(method) if isinstance(q,ast.Assign)
                 and len(q.targets)==1 and isinstance(q.targets[0],ast.Name)}
    want=ast.parse('s.Rational(45,10108)',mode='eval').body
    check('V3_actual_lower_response_P_AST_bound',
          ast.dump(assignments['P'],include_attributes=False)==ast.dump(want,include_attributes=False))
    want=ast.parse("[64*P/27,128*P/9,64*P/27,128*P/9,s.Rational(128,9),s.Rational(128,9),s.Rational(1024,105)]",
                   mode='eval').body
    check('V3_actual_input_constants_AST_bound',
          ast.dump(assignments['constants'],include_attributes=False)==ast.dump(want,include_attributes=False))
    want=ast.parse('[4,3,4,3,3,3,4]',mode='eval').body
    check('V3_actual_input_decay_AST_bound',
          ast.dump(assignments['decays'],include_attributes=False)==ast.dump(want,include_attributes=False))
    want=ast.parse('[P/27,P*4/9,P/27,P*4/9,s.Rational(4,9),s.Rational(4,9),s.Rational(4,9)]',
                   mode='eval').body
    check('V3_actual_mean_input_constants_AST_bound',
          ast.dump(assignments['mean_inputs'],include_attributes=False)==ast.dump(want,include_attributes=False))
    x=s.Symbol('x',nonnegative=True);n=s.Symbol('n',positive=True);m=s.Symbol('m',positive=True)
    P=s.Rational(45,10108)
    identity=36/(5*n**3)-4/(n*(n*n-4))-16*(n*n-9)/(5*n**3*(n*n-4))
    exact('all_odd_n_ge3_coefficient_identity',identity)
    def positive_polynomial(q,strict=False):
        values=s.Poly(s.expand(q),x).all_coeffs()
        return all(v>=0 for v in values) and (not strict or s.expand(q).subs(x,0)>0)
    check('coefficient_difference_nonnegative_for_all_n_ge3',
          positive_polynomial(16*((x+3)**2-9)))
    check('coefficient_denominator_positive_for_all_n_ge3',
          positive_polynomial(5*(x+3)**3*((x+3)**2-4),True))
    exact('first_n3_edge_is_sharp',s.Rational(36,5)/3**3-s.Rational(4,15))
    check('do_not_extend_old_n_ge4_bound_to_n3',s.Rational(4,15)>s.Rational(16,81))
    check('both_neighbours_ge_three_quarters_m',
          positive_polynomial((m-1-3*m/4).subs(m,x+4))
          and positive_polynomial((m+1-3*m/4).subs(m,x+4)))
    c=s.Rational(36,15)*s.Rational(4,3)**3
    r=P*s.Rational(36,15)*s.Rational(4,3)**4/12
    exact('all_neighbour_coefficient_constant',c-s.Rational(256,45))
    exact('all_neighbour_displacement_constant',r-256*P/405)
    check('V3_coefficient_constant_outward',c<=s.Rational(128,9))
    check('V3_velocity_constant_outward',P*c<=128*P/9)
    check('V3_displacement_constant_outward',r<=64*P/27)
    check('lower_modified_energy_displacement_conversion',s.Rational(5,722)<s.Rational(1,144))
    numerator,denominator=s.cancel(s.Rational(1024,35)/m**4
                                    -12/((m*m-1)*(m*m-9))).as_numer_denom()
    check('direct_even_coefficient_bound_all_m_ge4',
          positive_polynomial(numerator.subs(m,x+4))
          and positive_polynomial(denominator.subs(m,x+4),True))
    exact('pi_greater_than3_outward_direct_constant',s.Rational(1024,35)/3-s.Rational(1024,105))
    exact('mean_complex_c1_and_h0',s.Rational(4,3)-12/s.Integer(9))
    check('mean_coefficient_outward_using_pi_ge3',s.Rational(4,3)/3<=s.Rational(4,9))
    check('leading_frequency_strictly_above12',s.Rational(38**2,10)>12**2)
    check('leading_mass_cross_energy_bound_below8',s.Rational(9,12)<8)
    exact('leading_exponential_majorant',1/(1-s.Rational(1,5))-s.Rational(5,4))
    exact('leading_amplitude_majorant',s.Rational(20,19)*s.Rational(5,4)-s.Rational(25,19))
    check('leading_velocity_majorant',40*s.Rational(5,4)<s.Rational(205,4))
    kernel=json.loads((ROOT/(BASE+'r4c1_g3n5_attempt_02/kernel.json')).read_bytes())
    time_lambda=[q for q in kernel['entries'] if
                 (q['row']%22==21 or q['column']%22==21)
                 and (q['row']//22==1 or q['column']//22==1)]
    check('LambdaU_has_no_time_jet_in_full_generic_action',not time_lambda,time_lambda)
    finite=[]
    for index in range(9):
        case=json.loads((ROOT/(PARENT+'case_'+str(index).zfill(2)+'.json')).read_bytes())
        linear=json.loads((ROOT/(BASE+'r4c1_low_rank_inverse_attempt_02/case_'+str(index).zfill(2)+'.json')).read_bytes())
        x={n:s.Symbol(n,positive=True) if n in ('a','C') else s.Symbol(n,real=True)
           for n in 'a H u0 u_dot v0 v_dot r0 r_dot psi_dot rho C w wd aw m'.split()}
        def matrix(wire):
            return s.Matrix([[s.sympify(q,locals={**x,'I':s.I,'sqrt':s.sqrt}) for q in row]
                             for row in wire['entries']]).subs(x['m'],2)
        box=weighted.RationalBox({
            **{x[n]:tuple(map(s.Rational,b)) for n,b in linear['bounds']['background_box'].items()},
            x['w']:(-s.Rational(25,19),s.Rational(25,19)),
            x['wd']:(-s.Rational(205,4),s.Rational(205,4)),x['aw']:(s.Integer(0),s.Rational(25,19))})
        inputs2=[P/27,4*P/9,P/405,4*P/45,s.Rational(4,9),s.Rational(4,45),s.Rational(4,15)]
        force=matrix(case['formulas']['forced_numerator'])
        Q=matrix(linear['formulas']['matrices']['Q'])
        qmax=max(sum(box.absolute(Q[i,j]) for j in range(20)) for i in range(20))
        fmax=max(sum(box.absolute(force[i,j])*inputs2[j] for j in range(7)) for i in range(20))
        Fc=box.absolute(s.sqrt(20*qmax))*fmax
        mu=s.Rational(linear['bounds']['mu_exact']);state=Fc*s.exp(mu/40)/5
        components=[]
        for kind,key,skey in [('field','coupled_field_from_weighted','qsource'),
                              ('field_rate','coupled_rate_from_weighted','qdsource')]:
            full=matrix(case['formulas'][key])
            direct=matrix(case['formulas']['nonzero'][skey])
            for i,name in enumerate(case['formulas']['source_order'][:22]):
                if kind=='field_rate' and name=='LambdaU':
                    components.append(dict(kind='unused_Euler_velocity_slot',field=name,
                        value='0 is a permitted representative; actual LambdaU_dot NOT_BOUNDED'))
                    continue
                value=sum(box.absolute(full[i,j]) for j in range(20))*state
                value+=sum(box.absolute(direct[i,j])*inputs2[j] for j in range(7))
                components.append(dict(kind=kind,field=name,absolute_bound=str(value)))
        check(str(index)+'_retained_pair_finite_constant',Fc.is_Rational and Fc>0 and mu.is_Rational)
        check(str(index)+'_retained_pair_all22_fields_and_Euler_velocity_slots',len(components)==44)
        finite.append(dict(index=index,family=case['family'],eta_exact=case['eta_exact'],
            mode='m=+-2; ell=+-80',input_majorants=list(map(str,inputs2)),
            forcing_Q_constant=str(Fc),mu_exact=str(mu),
            weighted_energy_bound='E_2<=(F2/20)^2 exp(mu/20)',
            pointwise_state_inf_bound=str(state),components=components,
            initial='zero free coupled state; retain sourced auxiliaries/density',
            time='0<=t<=1/20',physical_window=False,useful_accuracy=False))
    check('source_hash_size_mtime_preserved',before==snapshot())
    passed=sum(q['passed'] for q in checks)
    return dict(schema='r4c1-cusp3-coupled-constants-v1',validation='PASS' if passed==len(checks) else 'FAIL',
        passed=passed,total=len(checks),checks=checks,source_sha256=pins,source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,retained_pair_bounds=finite,
        domain='signed even |m|>=4 tail plus retained m=+-2; separate mean; registered background on [0,1/20]',
        claim_status='Conditional',review_status='DEFERRED',physics_pass=False,gate_effect='NONE',
        physical_window_admitted=False,full_nonlinear_remainder=False)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    dest=ROOT/(BASE+'r4c1_cusp3_coupled_constants_attempt_01')
    if args.replay:
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse overwrite')
    else:dest.mkdir(parents=True)
    out=calculate();body=ENCODE(out);side=(SHA(body)+'  summary.json\n').encode()
    if args.replay:
        if (dest/'summary.json').read_bytes()!=body or (dest/'summary.json.sha256').read_bytes()!=side:
            raise ValueError('Read-only replay drift')
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise ValueError('Metadata changed')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        with (dest/'summary.json').open('xb') as f:f.write(body)
        with (dest/'summary.json.sha256').open('xb') as f:f.write(side)
    print(json.dumps({k:out[k] for k in ('validation','passed','total','physics_pass')}))
    for q in out['checks']:
        if not q['passed']:print(json.dumps(q))
    return int(out['passed']!=out['total'])


if __name__=='__main__':raise SystemExit(main())
