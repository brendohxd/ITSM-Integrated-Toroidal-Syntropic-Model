"""Direct canonical graph/current time transport, retaining centre defects."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json,traceback
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
SOURCE='Analysis/MasterTests/test_01_r4c1_rtau_current_transport_v2.py'
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_current_transport_v2_attempt_01/summary.json'
MODULE='Analysis/MasterTests/r4c1_density_time_transport_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_DENSITY_TIME_TRANSPORT_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def prepared_point(zs):
 mod=load('frozen_current_transport_point',SOURCE);tree=ast.parse((ROOT/SOURCE).read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate'))
 idx=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='zs')
 loop=fn.body[idx];assert isinstance(loop.body[-1],ast.Expr) and isinstance(loop.body[-1].value,ast.Call) and loop.body[-1].value.func.id=='print'
 fn.name='prepared_current_point';fn.args.args=[ast.arg(arg='zs')];fn.body=fn.body[:idx]+loop.body[:-1]+[ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-current-transport-point>','exec'),mod.__dict__)
 return mod.prepared_current_point(zs)
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[];records=[]
 check=lambda n,ok,v=None:checks.append(dict(name=n,passed=bool(ok),value=v))
 parent=json.loads((ROOT/PARENT).read_text());assert parent['passed']==parent['total']==46
 assert SHA((ROOT/PARENT).read_bytes())=='8ff36131f3058e32200ab8f7b3c8247d2a2ea66d8ea272ee1ebc8215dd22a322'
 pins=dict(parent['source_sha256']);snap={}
 for rel in (SELF,SOURCE,PARENT,MODULE,SPEC):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 ab=lambda x:max(abs(mp.mpf(t)) for t in x._mpi_);binary=lambda x:[list(t) for t in x._mpi_]
 module=load('direct_density_time',MODULE);omitted_reg=False;omitted_improvement=False;omitted_drift=False;centre_defect=False
 for zs in ('0.3','1.1','2.4'):
  env=prepared_point(zs);ctx=env['ctx'];J=env['J'];D=ctx['D'];q=ctx['q'];d=ctx['d'];v=ctx['v'];p=ctx['pi'];S=ctx['S'];Sz=ctx['Sz'];dq=env['dq'];dd=env['dd'];dp=env['dp'];dv=env['dv'];w=env['w'];wz=env['wz'];pd=env['pd'];dpd=env['dpd'];ar=env['ar'];L=ctx['L'];LR=ctx['LR'];grad=ctx['gradient'];hj=ctx['hj'];current=env['current']
  check('all_embedded_current_point_controls_'+zs,all(c['passed'] for c in env['checks']))
  result=module.evaluate(ctx,dq,dd,dp,dv,w,wz,pd,dpd,ar['Zdot'],ar['delta_Zdot'])
  I=result['density'];deltaI=result['delta_density']
  row=current.linearized(ctx,q,d,v,S,Sz,dq,dd,dv,w,wz,I,deltaI)
  BN=ctx['n']*grad(LR,49);rv=[a-b for a,b in zip(v,ctx['lie'](q,d,S,Sz))];hat=L.c-sum((p[i]*rv[i] for i in range(14)),J(0))
  raw=J(coefficients=[hat.c[0]-BN.c[1],hat.c[1]-2*BN.c[2],iv.mpf(0)])
  check('canonical_secondary_density_equals_raw_lapse_map_'+zs,max(ab((raw-I).c[k]) for k in (0,1))<mp.mpf('1e-28'))
  dy=dq+dv+dd+w+wz;dn=-ctx['beta']*ctx['n']*dq[12];dnz=-ctx['beta']*(dn*d[12]+ctx['n']*dd[12]);rawdy=dy+[dn,dnz]
  dBN=dn*grad(LR,49)+ctx['n']*sum((hj(LR,49,k)*rawdy[k] for k in range(50)),J(0))
  drv=[a-b-c for a,b,c in zip(dv,ctx['lie'](dq,dd,S,Sz),ctx['lie'](q,d,w,wz))]
  dhat=sum((grad(L,k)*dy[k] for k in range(48)),J(0))-sum((dp[i]*rv[i]+p[i]*drv[i] for i in range(14)),J(0))
  rawdelta=J(coefficients=[dhat.c[0]-dBN.c[1],dhat.c[1]-2*dBN.c[2],iv.mpf(0)])
  check('canonical_secondary_density_tangent_equals_raw_lapse_map_'+zs,max(ab((rawdelta-deltaI).c[k]) for k in (0,1))<mp.mpf('1e-28'))
  n,_,_,hi,_=ctx['geometry']([D(x,{0:y}) for x,y in zip(q,dq)],[D(x,{0:y}) for x,y in zip(d,dd)])
  W=[n*n*hi[i][2] for i in range(3)];C=env['C'];dC=env['dC']
  defect=sum((W[i].c*C[i] for i in range(3)),J(0)).c[1]
  delta_defect=sum((W[i].c*dC[i]+W[i].g.get(0,J(0))*C[i] for i in range(3)),J(0)).c[1]
  bg_res=result['density_rate']-(S[2]*I+row['background_flux'][2]).c[1]
  delta_res=result['delta_density_rate']-row['density_rate']
  err=ab(bg_res-defect);derr=ab(delta_res-delta_defect)
  check('direct_canonical_density_time_equals_action_current_Ward_'+zs,err<mp.mpf('1e-28'),mp.nstr(err,40))
  check('direct_canonical_density_time_tangent_equals_action_current_Ward_'+zs,derr<mp.mpf('1e-28'),mp.nstr(derr,40))
  centre_defect=centre_defect or ab(defect)>mp.mpf('1e-16')
  omitted_reg=omitted_reg or ab(result['delta_regulator_time'])>mp.mpf('1e-10')
  omitted_improvement=omitted_improvement or ab(result['delta_improvement'].c[1])>mp.mpf('1e-10')
  # Actual old/adapted J,w, with density Jacobian and moving-map term.
  z=mp.mpf(zs);ell=mp.mpf(1)/13000;Abar=mp.besseli(0,ell);lam=ell*mp.cos(z);lz=-ell*mp.sin(z);eps=mp.mpf(1)/1000;R2=mp.besseli(2,ell)/Abar
  wval=mp.exp(-lam)*eps/31*mp.quad(lambda t:mp.exp(ell*mp.cos(t))*(mp.cos(2*t)-R2),[0,z]);wgrad=eps*(mp.cos(2*z)-R2)/31-lz*wval
  Jac=J(coefficients=[iv.mpf(str(mp.exp(lam)/Abar)),iv.mpf(str(lz*mp.exp(lam)/Abar)),iv.mpf(0)])
  ww=J(coefficients=[iv.mpf(str(wval)),iv.mpf(str(wgrad)),iv.mpf(0)])
  newI=I/Jac;newdI=deltaI/Jac;newS=Jac*(S[2]-ww);newdS=Jac*w[2]
  newrow=(newS*newdI+newI*newdS+row['delta_flux'][2]).c[1]/Jac.c[0]
  old_to_new=(row['density_rate']-(ww*deltaI).c[1])/Jac.c[0]
  check('paired_moving_density_current_row_'+zs,ab(newrow-old_to_new)<mp.mpf('1e-28'))
  omitted_drift=omitted_drift or ab((ww*deltaI).c[1]/Jac.c[0])>mp.mpf('1e-12')
  records.append(dict(z=zs,direct_clock_residual=binary(bg_res),background_Ward_defect=binary(defect),direct_tangent_residual=binary(delta_res),tangent_Ward_defect=binary(delta_defect),direct_error=mp.nstr(err,40),tangent_error=mp.nstr(derr,40)))
  print('DIRECT_DENSITY_POINT_COMPLETED',zs,flush=True)
 check('nonzero_finite_centre_clock_defect_retained',centre_defect)
 check('omitted_regulator_density_time_rejected',omitted_reg)
 check('omitted_lapse_improvement_rejected',omitted_improvement)
 check('omitted_moving_density_drift_rejected',omitted_drift)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_DENSITY_TIME_TRANSPORT_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,point_controls=records,
  density_operator='direct current row agrees with time derivative of canonical density map, retaining momentum defects',operator_domain='smooth planar periodic compatible canonical data; local point controls only',
  complete_prepared_evolution=False,physical_norm='NOT_DERIVED',controlled_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',canonical_parent_adopted=False,G1_G6='INCOMPLETE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args()
 try:d=calculate();data=ENC(d)
 except Exception:
  if a.output_dir:
   a.output_dir.mkdir(parents=True,exist_ok=False);data=ENC(dict(error=traceback.format_exc(),script_sha256=SHA((ROOT/SELF).read_bytes())));p=a.output_dir/'failure.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n')
  raise
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
