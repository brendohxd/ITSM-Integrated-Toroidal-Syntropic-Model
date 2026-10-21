"""Pinned read-only mass-degree audit of the pre-chart coupled-node equations."""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_DIMENSIONAL_AUDIT_V1_CONTRACT_2026-10-19.md'
OUT='Analysis/MasterTests/outputs/r4c1_coupled_node_acceleration_attempt_04/'
PINS={
CONTRACT:'33ee6d9d644f22b5fd08cd2912933946d2bb9824bea7801b835f26dcdf81c543',
'Analysis/MasterTests/test_01_r4c1_coupled_node_acceleration_v4.py':'c6a7e31c2f63d8e6481d2e5a4b4f2725ce376f3de05ab639594a7b9e991f1ae7',
'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md':'4d56686ae98c33ee532f324b7fcdd4702c38da19401fa0b5d4ca894fa58c69ba',
'Theory/Gates/RES-001/RES001_R4C1_COUPLED_NODE_ACCELERATION_V4_ALGEBRA_ADDENDUM_2026-10-19.md':'64f2fe71410a9a2e3c70bffbb3955bc9ba4774fa73ba33d567820e4a88f8efd6',
OUT+'equations.json':'4aa8b6ff0abea3840a4aaededdd6a4a713a89a9c29477d23f1585ee8042723857',
OUT+'summary.json':'9f8d5fce14a4fadf3052eafdf4ec5d0e4adbe3937be991d344ff126fa49f6019',
}
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda obj:(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def record(path):
    raw=path.read_bytes()
    return dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=path.stat().st_mtime_ns)
def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,digest in pins.items():
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=digest or side.read_text().split()[0].lower()!=digest:
            raise ValueError('pinned source/sidecar drift: '+name)
        for q in (p,side):meta[q.relative_to(ROOT).as_posix()]=record(q)
    return pins,meta

DIMS={}
for degree,names in [
(0,'w R h0 h1 h2 c1 c2 c3 c4 b beta alpha'),
(1,'H H0 k p slope r1 ty1 wt wz Rz ty ht0 ht1 ht2 hz0 hz1 hz2'),
(2,'MP2 MU2 K_Q U rt F ty_time hdd0 hdd1 hdd2'),
(3,'Ud ty3 R3 hddz0 hddz1 hddz2'),
(4,'pressure mass_source rho0')]:
    DIMS.update({n:s.Rational(degree) for n in names.split()})
LOCALS={n:s.Symbol(n,real=True) for n in DIMS}
LOCALS['Matrix']=s.Matrix
class DimensionError(ValueError):pass

@lru_cache(maxsize=None)
def degree(expr):
    if expr==0:return None
    if expr.atoms(s.Float):raise DimensionError('approximate constant')
    if expr.is_Number:return s.Integer(0)
    if expr.is_Symbol:
        if str(expr) not in DIMS:raise DimensionError('unmapped symbol '+str(expr))
        return DIMS[str(expr)]
    if expr.is_Add:
        weights={degree(q) for q in expr.args}-{None}
        if len(weights)>1:raise DimensionError('inconsistent additive degrees '+str(sorted(weights)))
        return next(iter(weights)) if weights else None
    if expr.is_Mul:
        values=[degree(q) for q in expr.args]
        return None if None in values else sum(values,s.Integer(0))
    if expr.is_Pow:
        base,exponent=expr.args
        if not exponent.is_Rational:raise DimensionError('unsupported dimensionful/nonrational exponent')
        value=degree(base)
        return None if value is None else value*exponent
    if expr.func==s.Abs:return degree(expr.args[0])
    raise DimensionError('unsupported expression '+str(expr.func))

def calculate():
    pins,before=sources();eq=json.loads((ROOT/(OUT+'equations.json')).read_bytes())
    targets={'restricted_nodal_density':4,'metric_Euler':4,'metric_acceleration_matrix':2,
        'metric_acceleration_determinant':6,'metric_accelerations':2,'frame_Euler_normal_jet':4,
        'frame_acceleration_slope_before_shift_substitution':2,'actual_frame_slope':2,
        'transverse_shift_first_jet':1,'transverse_shift_third_jet':3,'longitudinal_shift_third_jet':3,
        'background_slope':2,'background_Hdot_from_pressure':2,'transport_defect':3}
    checks=[];results={}
    def add(name,passed,value=None):
        checks.append(dict(name=name,passed=bool(passed),value=value,criterion='exact mass-degree arithmetic'))
    for name,want in targets.items():
        raw=eq[name];parts=raw if isinstance(raw,list) else [raw];weights=[]
        for i,text in enumerate(parts):
            parsed=s.sympify(text,locals=LOCALS);terms=list(parsed) if isinstance(parsed,s.MatrixBase) else [parsed]
            for j,expr in enumerate(terms):
                try:
                    got=degree(expr);ok=got is None or got==want
                    add(name+'_'+str(i)+'_'+str(j),ok,'zero' if got is None else str(got))
                    weights.append('zero' if got is None else str(got))
                except DimensionError as exc:add(name+'_'+str(i)+'_'+str(j),False,str(exc))
        results[name]=dict(expected=want,recorded=weights)
    for name,expr in [('acceleration_plus_dimensionless',LOCALS['F']+1),
                      ('density_plus_hubble',LOCALS['pressure']+LOCALS['H']),
                      ('unmapped_symbol',s.Symbol('unregistered_scale'))]:
        caught=False
        try:degree(expr)
        except DimensionError:caught=True
        add('reject_'+name,caught)
    # Independent scaling control, separate from structural degree recursion.
    lam=s.Symbol('unit_scale',positive=True)
    F=s.sympify(eq['frame_Euler_normal_jet'],locals=LOCALS)
    example={symbol:s.Rational(i+2,i+3) for i,symbol in enumerate(sorted(F.free_symbols,key=str))}
    lifted={q:example[q]*lam**DIMS[str(q)] for q in example}
    add('independent_exact_unit_rescaling_frame_equation',
        s.cancel(F.xreplace(lifted)-lam**4*F.xreplace(example))==0)
    _,after=sources();add('all_original_bytes_sidecars_metadata_unchanged',before==after)
    passed=sum(r['passed'] for r in checks)
    return dict(validation='PASS_PRE_CHART_DIMENSIONS_ONLY' if passed==len(checks) else 'FAIL_DIMENSION_AUDIT',
        passed=passed,total=len(checks),checks=checks,source_sha256=pins,source_metadata=before,
        mass_degrees={n:str(v) for n,v in DIMS.items()},targets=results,
        scope='Pre-chart action/metric/frame/transport equations only. Reference-chart charge substitution and physical scale identification are not certified by this audit.',
        physical_unit_map_supplied=False,full_initial_admission=False,stage2_complete=False,
        stage3_entered=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output');p.add_argument('--replay');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose exactly one output or replay')
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside receipt root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    before={q.name:record(q) for q in dest.iterdir()} if a.replay else None
    result=calculate();raw=ENC(result);payload={'audit.json':raw,'audit.json.sha256':(SHA(raw)+'  audit.json\n').encode()}
    if a.replay:
        if set(before)!=set(payload):raise ValueError('replay file set changed')
        for name,value in payload.items():
            if (dest/name).read_bytes()!=value or record(dest/name)!=before[name]:
                raise ValueError('replay bytes/metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT')
    else:
        for name,value in payload.items():
            with (dest/name).open('xb') as stream:stream.write(value)
    print(json.dumps({k:result[k] for k in ('validation','passed','total','physics_pass')}))
    return 0 if result['passed']==result['total'] else 1
if __name__=='__main__':raise SystemExit(main())
