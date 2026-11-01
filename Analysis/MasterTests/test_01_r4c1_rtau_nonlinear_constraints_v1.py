"""Exact nonlinear dust reconstruction and arbitrary-tilt shift principal block."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_nonlinear_regulator_v2_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_NONLINEAR_CONSTRAINTS_V1_CONTRACT_2026-10-31.md'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))
def calculate():
 mp.mp.dps=100;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 def zero(n,z):
  vals=list(z) if isinstance(z,s.MatrixBase) else [z]
  bad=[str(v) for x in vals if (v:=clean(x))!=0];check(n,not bad,bad)
 assert SHA((ROOT/PARENT).read_bytes())=='ebf0bb4708ca1167bbbf4f3049ee8d418bfb76b0e992686ed6b85bca923f3d46'
 parent=json.loads((ROOT/PARENT).read_text());pins=dict(parent['source_sha256'])
 for path in (SELF,PARENT,CONTRACT):pins[path]=SHA((ROOT/path).read_bytes())
 snapshots={}
 for path,h in pins.items():
  f=ROOT/path;sc=Path(str(f)+'.sha256');assert SHA(f.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for q in (f,sc):snapshots[q]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
 N,C,V,eps,td=s.symbols('N C volume epsilon tau_dot',positive=True)
 dust=eps*V*(C*C*td*td/N-N*C**4)/2
 mult=s.diff(dust,eps);branch={N:td/C}
 zero('positive_clock_branch_satisfies_multiplier',mult.subs(branch))
 zero('nonlinear_lapse_density_coefficient',s.diff(s.diff(dust,N),eps).subs(branch)+V*C**4)
 EN=s.Symbol('E_N_nonmatter',real=True)
 reconstructed=EN/(V*C**4)
 zero('full_lapse_reconstruction',s.diff(dust,N).subs(branch).subs(eps,reconstructed)+EN)
 check('nonsingular_positive_lapse_density_patch',(-V*C**4).is_nonzero)
 spec=importlib.util.spec_from_file_location('shift_principal_backend',ROOT/BACKEND)
 backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
 types=backend.load('shift_principal_types',backend.QUADRATIC);par=types.parameters()
 action=backend.ClockGaugeAction('R-tau',par)
 action.body.sqrt=types.jsqrt;action.body.exp=types.jexp
 action.body.body.__globals__.update(sqrt=types.jsqrt,exp=types.jexp)
 vx,vy,vz=s.symbols('vx vy vz',real=True);vs=(vx,vy,vz)
 q=[1,0,0,1,0,1,vx,vy,vz,1,0,1,0,0,0,s.Rational(1,5)]
 vel=[0]*16;vel[14]=1
 state=q+vel+[0]*16+[0]*3+[types.Jet.var(i) for i in range(3)]+[1,0]
 out=action.density(state)[0];K=s.zeros(3)
 for (i,j),z in out.h.items():K[i,j]=K[j,i]=clean(z)
 base=s.diag(s.Rational(1,2),s.Rational(1,2),-s.Rational(1,15))
 zero('fresh_all_tilt_shift_block_symmetric',K-K.T)
 zero('aligned_shift_principal_recovered',K.subs(dict.fromkeys(vs,0))-base)
 delta=s.Rational(1,500);vv=vx*vx+vy*vy+vz*vz
 bounds=s.zeros(3)
 for i in range(3):
  for j in range(3):
   num,den=s.fraction(clean(K[i,j]-base[i,j]));coef,factors=s.factor_list(den)
   denominator_lower=abs(coef)
   for fac,power in factors:
    if clean(fac-(1+vv))!=0:raise ValueError('unregistered principal denominator '+str(fac))
   bounds[i,j]=clean(sum(abs(c)*delta**sum(mon) for mon,c in s.Poly(num,*vs).terms())/denominator_lower)
 bound=clean(sum(bounds));lower=clean(s.Rational(1,15)-bound)
 check('uniform_all_direction_small_tilt_principal_inverse',bound<s.Rational(1,30),str(bound))
 check('uniform_min_singular_value_positive',lower>0,str(lower))
 print('EXACT_ALL_TILT_PRINCIPAL_AND_DUST_ROWS_COMPLETE',flush=True)
 conv=lambda z:mp.mpf(str(s.N(z,98)))
 physicalpar={k:conv(z) for k,z in par.items()};physical=backend.ClockGaugeAction('R-tau',physicalpar,physical=True)
 samples=[(s.Rational(1,1000),-s.Rational(1,2000),s.Rational(1,2000)),
          (-s.Rational(1,1500),s.Rational(1,1200),s.Rational(1,1300)),(0,0,0)]
 controls=[]
 for seed,tilt in enumerate(samples):
  aa=[mp.mpf(0)]*56
  for j in (0,3,5):aa[j]=1;aa[16+j]=mp.mpf('0.2')
  for j,t in enumerate(tilt):aa[6+j]=conv(t);aa[22+j]=mp.mpf(j+1)/37;aa[38+j]=mp.mpf(j-1)/41
  aa[9]=mp.mpf('1.1');aa[10]=mp.mpf('.1');aa[11]=mp.mpf('.9');aa[12]=mp.mpf('.03')
  aa[13]=mp.mpf('.02');aa[15]=mp.mpf('.2');aa[25]=mp.mpf('.03');aa[26]=1;aa[27]=mp.mpf('.25')
  aa[28]=mp.mpf('.2');aa[30]=mp.exp(physicalpar['beta']*aa[12])
  aa[41]=mp.mpf('.05');aa[42]=mp.mpf('.06');aa[43]=mp.mpf('.07');aa[44]=mp.mpf('.08')
  aa[54]=1;aa[55]=mp.mpf('.01')
  mat=K.subs(dict(zip(vs,tilt)));expected=mp.matrix([[conv(z) for z in row] for row in mat.tolist()])
  def value(z):
   state=aa.copy()
   for i in range(3):state[51+i]=z[i]
   return physical.density(state)[0]
  zero_value=value([0,0,0]);errors=[]
  for hs in ('1e-12','1e-18'):
   h=mp.mpf(hs);numeric=mp.matrix(3)
   for i in range(3):
    for j in range(i,3):
     ei=[mp.mpf(0)]*3;ej=ei.copy();ei[i]=h;ej[j]=h
     if i==j:val=(value(ei)+value([-x for x in ei])-2*zero_value)/(h*h)
     else:val=(value([x+y for x,y in zip(ei,ej)])-value([x-y for x,y in zip(ei,ej)])-value([-x+y for x,y in zip(ei,ej)])+value([-x-y for x,y in zip(ei,ej)]))/(4*h*h)
     numeric[i,j]=numeric[j,i]=val
   err=max(abs(z) for z in numeric-expected)/(1+max(abs(z) for z in expected))
   check('independent_full_physical_shift_Hessian_'+str(seed)+'_'+hs,err<mp.mpf('1e-30'),mp.nstr(err,50));errors.append(mp.nstr(err,50))
  controls.append(dict(tilt=[str(z) for z in tilt],errors=errors))
 for f,(h,m) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==m
 check('inputs_and_sidecars_unchanged',True,len(snapshots))
 return dict(kind='R4C1_RTAU_NONLINEAR_CONSTRAINTS_V1',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,source_sha256=pins,
  dust=dict(multiplier=str(mult),lapse='N=tau_dot/C on positive timelike-clock branch',epsilon='E_N_nonmatter/(sqrt(h)*C^4)',rho='E_N_nonmatter/sqrt(h)',Euler_flux='E_N_nonmatter=L_N-d_z(L_Nz); do not omit flux'),
  shift=dict(orthonormal_N1_principal=[[str(z) for z in row] for row in K.tolist()],perturbation_entry_bounds=[[str(z) for z in row] for row in bounds.tolist()],perturbation_norm_bound=str(bound),minimum_singular_value_bound=str(lower),domain='physical |V|<=1/500, positive lapse and positive spatial metric; local principal symbol only',inertia=[2,1,0],global_periodic_inverse=False,strong_positive_coercivity=False),
  controls=controls,full_nonlinear_constraint_solve='INCOMPLETE',reduced_coupled_interactions='INCOMPLETE',physical_window_demonstrated=False,canonical_parent_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
