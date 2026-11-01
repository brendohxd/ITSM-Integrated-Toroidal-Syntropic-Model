"""Re-evaluate one frozen nonlinear candidate, without refitting, off grid."""
from pathlib import Path
import argparse,ast,hashlib,importlib.util,json
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json'
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_PERIODIC_OFFGRID_V1_SPEC_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
 mp.mp.dps=40;checks=[]
 def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
 assert SHA((ROOT/PARENT).read_bytes())=='58fc8db6b8d10ee57f2974e0415685ded3cfe9e80745044b19b551b7827c0d60'
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256'])
 for p in (SELF,PARENT,SPEC):pins[p]=SHA((ROOT/p).read_bytes())
 snapshots={}
 for rel,h in pins.items():
  f=ROOT/rel;sc=Path(str(f)+'.sha256');assert SHA(f.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for q in (f,sc):snapshots[q]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
 spec=importlib.util.spec_from_file_location('offgrid_physical_backend',ROOT/'Analysis/MasterTests/r4c1_two_repair_actions_v2.py')
 backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
 old=backend.load('offgrid_params',backend.QUADRATIC)
 par={k:mp.mpf(str(v.p))/int(v.q) for k,v in old.parameters().items()}
 action=backend.ClockGaugeAction('R-tau',par,physical=True)
 tree=ast.parse((ROOT/SOURCE).read_text());calc=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
 defs=[n for n in calc.body if isinstance(n,ast.FunctionDef) and n.name in ('profiles','local')]
 assert len(defs)==2
 scope=dict(mp=mp,np=np,e=mp.mpf(1)/1000,beta=par['beta'],b=action.body,action=action)
 module=ast.fix_missing_locations(ast.Module(body=defs,type_ignores=[]));exec(compile(module,'<pinned-profile-evaluation>','exec'),scope)
 profiles,local=scope['profiles'],scope['local'];candidate=d['results'][-1]
 coeff=np.array(candidate['shift_coefficients']);H=candidate['H'];omega=candidate['omega'];results=[]
 for count in (65,129):
  theta=2*np.pi*(np.arange(count)+.37)/count;size=(count-1)//2
  B=np.column_stack([fn(n*theta) for n in range(1,size+1) for fn in (np.cos,np.sin)])
  Bz=np.column_stack([n*fn(n*theta) for n in range(1,size+1) for fn in (lambda t:-np.sin(t),np.cos)])
  D=(2/count)*Bz@B.T;S=B[:,:32]@coeff.T;Sz=Bz[:,:32]@coeff.T
  prof=[profiles(2*mp.pi*(j+mp.mpf('.37'))/count) for j in range(count)]
  grads=np.array([local(p,S[j],Sz[j],H,omega) for j,p in enumerate(prof)])
  ES=grads[:,:3]-D@grads[:,3:6];EN=grads[:,6]-D@grads[:,7]
  C=np.array([float(p['C']) for p in prof]);vol=np.array([float(p['volume']) for p in prof])
  rho=EN/vol;I=float(np.mean(EN/C));Q=float(np.mean([float(p['q'][9])*grads[j,9]-float(p['q'][10])*grads[j,8] for j,p in enumerate(prof)]))
  residual=float(np.max(np.abs(ES)));momentum=np.mean(ES,axis=0);noflux=float(np.mean(grads[:,6]/C))
  check(str(count)+'_full_offgrid_residual',residual<1e-9,residual)
  check(str(count)+'_fixed_charges',max(abs(I-.2),abs(Q-1))<1e-9,[I,Q])
  check(str(count)+'_positive_sampled_density',np.min(rho)>0,float(np.min(rho)))
  check(str(count)+'_momentum_means_retained',np.max(np.abs(momentum))<1e-9,momentum.tolist())
  check(str(count)+'_omitted_lapse_flux_rejected',abs(noflux-I)>1e-11,noflux-I)
  fourier=(2/count)*B.T@ES;tail=float(np.max(np.abs(fourier[32:,:])))
  results.append(dict(nodes=count,offset='.37',H=H,omega=omega,residual_max=residual,rho_min=float(np.min(rho)),rho_max=float(np.max(rho)),
                      clock_charge=I,U1_charge=Q,integrated_momentum=momentum.tolist(),sampled_residual_harmonics_above_16=tail,omitted_flux_clock_charge=noflux))
 check('fine_charge_quadratures_agree',max(abs(results[0][key]-results[1][key]) for key in ('clock_charge','U1_charge'))<1e-10)
 for f,(h,t) in snapshots.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_pinned_sources_and_mtimes_preserved',True,len(snapshots))
 return dict(kind='R4C1_RTAU_PERIODIC_OFFGRID_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,source_sha256=pins,
             results=results,refit_performed=False,continuum_tail_bound='NOT_SUPPLIED',validated_nonlinear_inverse='NOT_SUPPLIED',continuum_preparation_admitted=False,
             review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
