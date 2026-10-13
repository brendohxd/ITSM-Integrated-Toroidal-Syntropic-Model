"""V2: exact assertion corrections; unchanged v1 science and adverse findings."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sympy as s
import test_01_r4c1_g3n5_nonzero_characteristic_v1 as v1

ROOT=v1.ROOT
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_G3N5_NONZERO_ASSERTION_V2_ADDENDUM_2026-10-11.md'
V1_SHA='8c63194a678734917c5c9a9593da8023fb7ba946790cc0376c7cd3a9fa57c991'
if v1.common.sha((ROOT/v1.SELF).read_bytes())!=V1_SHA:raise RuntimeError('Frozen main v1 drift')


def calculate():
    newpins={SELF:v1.common.sha((ROOT/SELF).read_bytes()),
             ADDENDUM:v1.common.sha((ROOT/ADDENDUM).read_bytes())}
    oldrel=v1.BASE+'r4c1_g3n5_nonzero_characteristic_attempt_01/'
    oldsummary=v1.common.read_json(oldrel+'summary.json')
    newpins[oldrel+'summary.json']=v1.common.sha((ROOT/(oldrel+'summary.json')).read_bytes())
    newpins.update({oldrel+k:v for k,v in oldsummary['artifacts'].items()})
    tracked=[ROOT/q for q in newpins]
    tracked.extend(Path(str(q)+'.sha256') for q in list(tracked) if Path(str(q)+'.sha256').is_file())
    before=v1.snapshot(tracked)
    data,summary=v1.calculate()  # recompute in memory; do not invoke v1.main
    matrices=json.loads(data['matrices.json']);formulas=json.loads(data['formulas.json'])
    sy={}
    names=set()
    for mat in matrices.values():
        for row in mat['entries']:
            for text in row['terms']:
                import re
                names.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',text))
    for name in names:sy[name]=s.Symbol(name,positive=True) if name in ('a','ell','p') else s.Symbol(name,real=True)
    sy.update(I=s.I,sqrt=s.sqrt)
    mats={k:v1.import_matrix(v,sy) for k,v in matrices.items()}
    K=mats['K'];c=s.Symbol('c',real=True);sig=s.Symbol('sigma',real=True)
    u,v=sy['u0'],sy['v0'];detK=s.factor(K.det());ratio=s.Rational(5,33)
    corrections=v1.common.Checks()
    zero=[v1.old.IDX[q] for q in ('alpha','Em','LambdaU')]
    C0,C1=mats['unreduced_momentum_value'],mats['unreduced_momentum_velocity']
    v1.exact(corrections,'eliminated_gauge_multiplier_coordinates_have_no_one_form',
             C0[zero,:].row_join(C1[zero,:]))
    saved=v1.common.read_json(v1.BASE+'r4c1_g3n5_constraint_response_attempt_01/coefficients.json')
    ref=next(q for q in saved['charts'] if q['mode']==[1,0,0])
    q0=v1.import_matrix(ref['matrices']['Q0'],sy);q1=v1.import_matrix(ref['matrices']['Q1'],sy)
    fixed=[v1.old.IDX[q] for q in ('T','nu')]
    v1.exact(corrections,'fixed_T_nu_have_zero_coordinate_one_form_pullback',q0[fixed,:].row_join(q1[fixed,:]))
    v1.exact(corrections,'complete_chart_determinant_normalization',detK-s.Rational(11,768))
    wave=s.sympify(formulas['wave_scale_factor'],locals={**sy,'c':c})
    fast=s.sympify(formulas['fast_scale_factor'],locals={**sy,'sigma':sig})
    wave_target=-detK*ratio*c*c*(c*c-1)**4*(c*c-s.Rational(4,5))**2*(c*c-s.Rational(1,3))*(c*c-1-(u*u+v*v)/13)
    fast_target=detK*sig**18*(sig*sig-ratio)
    v1.exact(corrections,'all_wave_scale_root_multiplicities',wave-wave_target)
    v1.exact(corrections,'all_fast_scale_root_multiplicities',fast-fast_target)
    original=[q for q in summary['checks'] if not q['passed']]
    byname={q['name']:q for q in corrections.rows}
    if {q['name'] for q in original}!={
            'eliminated_gauge_multiplier_coordinates_have_no_one_form',
            'all_wave_scale_root_multiplicities','all_fast_scale_root_multiplicities'}:
        raise RuntimeError('Unexpected v1 failure; do not silently mask it')
    summary['checks']=[byname.get(q['name'],q) for q in summary['checks']]
    used={q['name'] for q in summary['checks']}
    extra=v1.common.Checks()
    principal=v1.separate.derive()
    Cwave=s.diag(principal['companion'],s.Matrix([[0,1],[1,0]]),s.Matrix([[0,1],[1,0]]),
                  s.Matrix([[0,1],[s.Rational(4,5),0]]),s.Matrix([[0,1],[s.Rational(4,5),0]]),
                  s.zeros(6))
    Cwave[12:15,15:18]=s.eye(3)
    Cwave[15:18,12:15]=principal['Gmatter']
    poly=Cwave.charpoly();x=poly.gen
    target=x*x*(x*x-s.Rational(1,3))*(x*x-1)**4*(x*x-s.Rational(4,5))**2*(x*x-1-(u*u+v*v)/13)
    v1.exact(extra,'complete_18_state_wave_companion',poly.as_expr()-target)
    extra.add('complete_wave_zero_eigenspace_defective',len(Cwave.nullspace())==1,1,'algebraic 2, geometric 1')
    e0=principal['zero'].col_join(s.zeros(14,1));e1=principal['generalized'].col_join(s.zeros(14,1))
    v1.exact(extra,'full_wave_companion_Jordan_chain',Cwave*e1-e0)
    for label,eig in [('positive',s.sqrt(3)/3),('negative',-s.sqrt(3)/3)]:
        extra.add('nonzero_scalar_wave_eigenspace_'+label,
                  len((principal['companion']-eig*s.eye(4)).nullspace())==1,1,'one eigenvector for simple root')
    G=principal['Gmatter']
    radial=s.Matrix([u,v,0]);phase=s.Matrix([v,-u,0]);rr=s.Matrix([0,0,1])
    v1.exact(extra,'matter_radial_characteristic',G*radial-radial)
    v1.exact(extra,'matter_phase_characteristic',G*phase-(1+(u*u+v*v)/13)*phase)
    v1.exact(extra,'matter_r_characteristic',G*rr-rr)
    v1.exact(extra,'matter_characteristics_at_zero_radius',G.subs({u:0,v:0})-s.eye(3))
    Cfast=s.Matrix([[0,1],[ratio,0]])
    for label,eig in [('positive',s.sqrt(ratio)),('negative',-s.sqrt(ratio))]:
        extra.add('fast_companion_eigenspace_'+label,len((Cfast-eig*s.eye(2)).nullspace())==1,1,'one for each distinct real root')
    extra.add('independent_v1_formulas_preserved_byte_identical',
              (ROOT/(v1.BASE+'r4c1_g3n5_nonzero_principal_attempt_01/formulas.json')).read_bytes()==
              (ROOT/(v1.BASE+'r4c1_g3n5_nonzero_principal_attempt_02/formulas.json')).read_bytes())
    summary['checks'].extend(q for q in corrections.rows if q['name'] not in used)
    summary['checks'].extend(extra.rows)
    pins=summary['source_sha256']
    for name,value in newpins.items():
        if name in pins and pins[name]!=value:raise ValueError('Input drift '+name)
        pins[name]=value
    missing=v1.common.inspect_pins(pins)
    summary['checks'].append(dict(name='v2_added_pins_and_metadata_preserved',passed=v1.snapshot(tracked)==before,
                                 value={'added_pins':len(newpins),'files':len(before),'inherited_absent':missing},criterion='hash/size/mtime_ns unchanged'))
    formulas.update(complete_wave_companion=v1.exports(Cwave),fast_companion=v1.exports(Cfast),
                    determinant_normalization=str(detK),canonical_one_form_note='Fixed T/nu have dT=dnu=0, not p_T=p_nu=0; no new dust-charge restriction')
    data['formulas.json']=v1.common.encode(formulas)
    diag=json.loads(data['diagnostics.json'])
    diag['preserved_main_v1_failed_assertions']=original
    data['diagnostics.json']=v1.common.encode(diag)
    summary.update(schema='r4c1-g3n5-nonzero-characteristic-v2',
                   preserved_main_v1={'passed':103,'total':106,'validation':'FAIL_LOCAL_CHECKS','failures':original},
                   source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=missing,
                   source_metadata_preserved=summary['source_metadata_preserved']+len(before))
    summary['passed']=sum(q['passed'] for q in summary['checks']);summary['total']=len(summary['checks'])
    summary['validation']='PASS_LOCAL_CHECKS' if summary['passed']==summary['total'] else 'FAIL_LOCAL_CHECKS'
    summary['artifacts']={k:v1.common.sha(v) for k,v in data.items() if k!='summary.json'}
    data['summary.json']=v1.common.encode(summary)
    return data,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=v1.BASE+'r4c1_g3n5_nonzero_characteristic_attempt_02')
    ap.add_argument('--replay');a=ap.parse_args()
    dest=(ROOT/(a.replay or a.output)).resolve();dest.relative_to((ROOT/v1.BASE).resolve())
    if not a.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if a.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    data,summary=calculate()
    if a.replay:
        for name,body in data.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(v1.common.sha(body)+'  '+name+'\n').encode():
                raise RuntimeError('Exact replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in data.items():
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((v1.common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if a.replay else 'NEW_RECEIPTS_WRITTEN',**{k:summary[k] for k in ('validation','passed','total','status','physics_pass','gate_effect')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
