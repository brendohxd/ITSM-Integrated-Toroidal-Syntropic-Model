"""Exact flat auxiliary control, not a prepared physical-norm theorem."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
k=s.symbols('k',positive=True,integer=True)
identity=s.factor(1-k*k/(1+k*k))
assert identity==1/(1+k*k) and identity.is_positive
rows=[dict(k=n,strong_L2=n*n,weak_Hminus2=str(s.Rational(n*n,1+n*n))) for n in [1,2,8,32,128,512]]
assert all(s.Rational(r['weak_Hminus2'])<=1 for r in rows)
paths=[Path(__file__),ROOT/'Theory/Gates/RES-001/RES001_RTAU_AUXILIARY_WEAK_RATE_V1_2026-11-02.md']
r=dict(scope='EXACT_FLAT_AUXILIARY_CONTROL_NOT_PREPARED_EVOLUTION',physics_pass=False,
 identity=str(identity),rows=rows,actual_background_coefficient_bounds='NOT_SUPPLIED',physical_norm='NOT_DERIVED',
 source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
payload=(json.dumps(r,indent=2,sort_keys=True)+'\n').encode()
if a.output:
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open('xb') as f:f.write(payload)
else:
 assert a.verify.read_bytes()==payload
print('Exact Fourier identity controls passed; no physical clearance')
