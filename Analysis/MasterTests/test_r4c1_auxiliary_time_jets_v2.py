"""Independent symbolic controls and immutable replay of local auxiliary jets."""
import argparse
from pathlib import Path
import hashlib,json
import sympy as s
from r4c1_auxiliary_time_jets_v1 import calculate

ROOT=Path(__file__).resolve().parents[2]
SOURCES=[Path(__file__),Path(__file__).with_name('r4c1_auxiliary_time_jets_v1.py'),
 ROOT/'Theory/Gates/RES-001/RES001_RTAU_AUXILIARY_TIME_JETS_V1_CONTRACT_2026-11-02.md']


def run():
 z,t=s.symbols('z t',real=True); at=s.Rational(1,7)
 checks=[];records=[]
 def check(name,ok):
  checks.append(dict(name=name,ok=bool(ok)))
 def jets(expr,n):
  return [s.diff(expr,z,k).subs({z:at,t:0}) for k in range(n+1)]
 L=s.Matrix([[1,0,0],[z/5+t/11,1,0],[(1+z*z)/7+t*z/13,(z+1)/6+t/17,1]])
 c=1+z*z+t*(1+z)/10
 h=c*c*L.T*L
 psi=z*z/3+z**3/5+t*(z**4/7+2*z)
 # Independent direct Laplace-Beltrami expression: sqrt(det h)=c^3 locally.
 Z=-s.diff(c**3*h.inv()[2,2]*s.diff(psi,z),z)/c**3
 out=calculate(jets(h,3),jets(s.diff(h,t),3),jets(psi,4),jets(s.diff(psi,t),4))
 for k in range(3):
  ref=s.diff(Z,z,k).subs({z:at,t:0})
  rt=s.diff(Z,t,z,k).subs({z:at,t:0})
  check(f'full_metric_Z_dz{k}',s.simplify(out['Z'][k]-ref)==0)
  check(f'full_metric_Zt_dz{k}',s.simplify(out['Zt'][k]-rt)==0)
  records.append(dict(order=k,Z=str(out['Z'][k]),Zt=str(out['Zt'][k])))
 # Naturality of scalar Laplacian under a spatial diffeomorphism, including
 # tensor index terms rather than advecting metric entries as scalars.
 h0=h.subs(t,0);p0=psi.subs(t,0);w=1+z+z*z/9
 ht=w*s.diff(h0,z)
 for i in range(3):
  for j in range(3):
   ht[i,j]+=s.diff(w,z)*(h0[2,j]*int(i==2)+h0[i,2]*int(j==2))
 moved=calculate(jets(h0,3),jets(ht,3),jets(p0,4),jets(w*s.diff(p0,z),4))
 for k in range(3):
  target=s.diff(w*s.diff(Z.subs(t,0),z),z,k).subs(z,at)
  check(f'Lie_transport_order{k}',s.simplify(moved['Zt'][k]-target)==0)
 flat=calculate([s.eye(3)]+[s.zeros(3)]*3,[s.zeros(3)]*4,jets(p0,4),jets(z**4,4))
 check('flat_time_second_spatial',flat['Zt'][2]==-24)
 for label,args in [('missing_metric', (jets(h,3)[:3],jets(s.diff(h,t),3),jets(psi,4),jets(s.diff(psi,t),4))),
                    ('missing_scalar_time',(jets(h,3),jets(s.diff(h,t),3),jets(psi,4),jets(s.diff(psi,t),3))),
                    ('indefinite_metric',([s.diag(1,1,-1)]+[s.zeros(3)]*3,[s.zeros(3)]*4,jets(p0,4),jets(z**4,4)))]:
  try:
   calculate(*args);rejected=False
  except ValueError:
   rejected=True
  check(label+'_rejected',rejected)
 return dict(scope='LOCAL_EXACT_AUXILIARY_JETS_ONLY',physics_pass=False,physical_norm='NOT_DERIVED',
  checks=checks,passed=sum(c['ok'] for c in checks),total=len(checks),records=records,
  source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCES})


if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 r=run();payload=(json.dumps(r,indent=2,sort_keys=True)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True,exist_ok=True)
  with a.output.open('xb') as f:f.write(payload)
 else:
  assert a.verify.read_bytes()==payload,'Immutable replay mismatch'
 print(json.dumps(dict(passed=r['passed'],total=r['total'],failed=[c for c in r['checks'] if not c['ok']])))
 raise SystemExit(0 if r['passed']==r['total'] else 1)
