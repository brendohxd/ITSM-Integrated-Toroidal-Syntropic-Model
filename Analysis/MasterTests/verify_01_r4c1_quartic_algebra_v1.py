"""Exact source/reflection/trace controls; no admission claim."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_QUARTIC_ALGEBRA_CONTROL_V1_CONTRACT_2026-10-27.md'
PRIMARY='Analysis/MasterTests/outputs/r4c1_quartic_joint_completion_v1_attempt_01/summary.json'
SCALAR='Analysis/MasterTests/outputs/r4c1_quartic_scalar_trace_independent_v1_attempt_01/independent.json'
GENERIC='Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01/formulas.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def calculate():
    primary=json.loads((ROOT/PRIMARY).read_bytes())
    pins=dict(primary['source_sha256'])
    pins.update({PRIMARY:'2df2eb08f06243ca1ef60152a17921d17c7755bbca18fbd59bc33ab27f45acb0'})
    for name in (SCALAR,CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):
        pins[name]=SHA((ROOT/name).read_bytes())
    for name,digest in pins.items():
        if SHA((ROOT/name).read_bytes())!=digest:raise ValueError('source drift '+name)
    raw=json.loads((ROOT/GENERIC).read_bytes())
    scalar=json.loads((ROOT/SCALAR).read_bytes())
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):
        got=s.factor(s.cancel(expr));check(name,got==0,str(got))
    check('independent_nonzero_W_current_controls_pass',scalar['passed']==scalar['total']==4)
    names='MP2 MU2 c1 c2 c3 c4 K_Q A b beta zeta Rc H H0 vz vz1 vz2 R q p Z Zd Z1 Z2 D rd pot k alpha xi zc zdc rs qs CC SS eeabs rh qh ru qu'
    u={name:s.Symbol(name,real=True) for name in names.split()}
    parse=lambda text:s.sympify(text,locals=u)
    w,v,w2,R,Z,Z1=[u[n] for n in ('vz','vz1','vz2','R','Z','Z1')]
    U,W,sigma=s.symbols('U W sigma',real=True)
    b,p,K=[u[n] for n in ('b','p','K_Q')]
    f=parse(raw['longitudinal']['f'])
    field=U*w*w+W*w**4
    source=f.subs({Z:field,Z1:s.diff(field,w)*v},simultaneous=True)
    difference=s.cancel(source-source.subs(W,0))
    zero('quartic_shift_source_from_generic_momentum',difference-5*b*p*W*w**5*v)
    check('omitted_quartic_shift_source_rejected',difference!=0)
    for name in ('energy_without_dust','lapse_flux_divergence'):
        expression=parse(raw[name])
        for label,reflection in (
            ('cosine',{w:-w,w2:-w2,R:-R,Z1:-Z1}),
            ('sine',{v:-v,R:-R,Z1:-Z1})):
            zero(name+'_'+label+'_reflection',expression.subs(reflection,simultaneous=True)-expression)
    # hp00=-1+gamma^2=w^2 on N=1,h=I, initial transverse V=w.
    zero('initial_regulator_acceleration_coefficient',-1+(1+w*w)-w*w)
    da2=-W*sigma*sigma
    daZ=s.cancel((K*da2-12*b*W*sigma**4)/(b*sigma*sigma))
    dQ=s.factor(daZ+2*da2)
    zero('quartic_trace_gain_from_regulator_and_scalar',dQ+(K/b+14*sigma*sigma)*W)
    zero('fixed_case_gain',dQ.subs({K:s.Rational(3,4),b:s.Rational(5,44),sigma:s.Rational(2,25)})+s.Rational(4181,625)*W)
    check('omitted_scalar_acceleration_trace_rejected',s.cancel(daZ-dQ)!=0)
    zero('leading_shift_response_not_frozen',s.diff(s.sympify(primary['formulas']['shift_extra'],locals={'W':W,'xi':s.Symbol('xi')}),W)
         +s.Rational(15,352)*(s.Symbol('xi')**2/36+5*s.Symbol('xi')/144+s.Rational(5,96)))
    # Generic formulas retain exact rational coefficients throughout.
    check('generic_inputs_no_Float',not any(parse(raw[n]).atoms(s.Float) for n in ('energy_without_dust','lapse_flux_divergence')))
    for name,digest in pins.items():
        if SHA((ROOT/name).read_bytes())!=digest:raise ValueError('source drift '+name)
    return dict(result_id='R4C1-QUARTIC-ALGEBRA-CONTROL-V1',checks=checks,
        passed=sum(c['passed'] for c in checks),total=len(checks),source_sha256=pins,
        formulas={'shift_source_change':str(difference),'trace_change':str(dQ)},
        physics_pass=False,G1_complete=False,gate_effect='NONE',review_status='DEFERRED',sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'independent.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'independent.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  independent.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
