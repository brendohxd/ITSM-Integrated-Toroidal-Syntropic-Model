"""Exact orientation controls for the whole-circle initial extension proof."""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BOUND='Analysis/MasterTests/outputs/r4c1_quartic_scalar_bound_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def calculate():
    parent=json.loads((ROOT/BOUND).read_bytes());pins=dict(parent['source_sha256'])
    pins[BOUND]='f74df107b91e466e2c8d3c9d79107d968e2456beee16b26210adde7d43b1d756'
    pins[Path(__file__).relative_to(ROOT).as_posix()]=SHA(Path(__file__).read_bytes())
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('source drift '+name)
    u={n:s.Symbol(n,real=True) for n in 'H HB U Ud W w wp T q'.split()}
    N=s.sympify(parent['formulas']['analytic_N'],locals=u);w,wp,T,q=[u[n] for n in ('w','wp','T','q')]
    checks=[]
    def zero(name,e):
        z=s.factor(s.cancel(e));checks.append(dict(name=name,passed=bool(z==0),value=str(z)))
    zero('local_normal_reflection',N.subs(w,-w)-N)
    zero('orientation_reversal',N.subs({wp:-wp,T:-T},simultaneous=True)-N)
    sigma=s.Rational(2,25)
    plus=N.subs({w:0,wp:sigma,T:q/sigma},simultaneous=True)
    minus=N.subs({w:0,wp:-sigma,T:-q/sigma},simultaneous=True)
    zero('both_node_numerators_identical',plus-minus)
    checks.append(dict(name='parent_scope_and_checks',passed=bool(parent['initial_acceleration_extension_certified'] and
        parent['passed']==parent['total'] and not parent['G1_complete'] and not parent['time_evolution_certified'])))
    for name,want in pins.items():
        if SHA((ROOT/name).read_bytes())!=want:raise ValueError('exit drift '+name)
    return dict(result_id='R4C1-QUARTIC-INITIAL-EXTENSION-ORIENTATION-V1',checks=checks,
        passed=sum(v['passed'] for v in checks),total=len(checks),source_sha256=pins,
        G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    d=calculate();data=ENC(d);directory=a.replay or a.output
    if a.replay:
        if (directory/'independent.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);f=directory/'independent.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  independent.json\n',encoding='ascii')
    print(json.dumps({k:d[k] for k in ('passed','total','G1_complete')}))
    raise SystemExit(0 if d['passed']==d['total'] else 2)


if __name__=='__main__':main()
