"""Actual-profile periodic gauge inverse and canonical coordinate controls."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_auxiliary_rate_v2_attempt_01/summary.json'
MODULE='Analysis/MasterTests/r4c1_gauge_velocity_v1.py'
FLOW='Analysis/MasterTests/r4c1_prepared_canonical_flow_v2.py'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
SPEC='Theory/Gates/RES-001/RES001_R4C1_RTAU_GAUGE_VELOCITY_V1_SPEC_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 d=json.loads((ROOT/PARENT).read_text());assert d['passed']==d['total']==21;pins=dict(d['source_sha256']);snap={}
 for rel in (SELF,PARENT,MODULE,FLOW,FACTORY,SPEC):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 ab=lambda x:max(abs(mp.mpf(t)) for t in x._mpi_);binary=lambda x:[list(v) for v in x._mpi_]
 gauge=load('gauge_velocity',MODULE);flow=load('canonical_gauge_flow',FLOW)
 ell=mp.mpf(1)/13000;Abar=mp.besseli(0,ell);a=lambda z:mp.exp(ell*mp.cos(z));Jac=lambda z:a(z)/Abar
 # Exact adapted mean and bounded analytic representation of coordinate zeta.
 mean=lambda f:mp.quad(lambda z:Jac(z)*f(z),[0,mp.pi,2*mp.pi])/(2*mp.pi)
 zeta_coeff=[2*mp.besseli(n,ell)/(n*Abar) for n in range(1,17)]
 zeta=lambda z:z+sum(zeta_coeff[n-1]*mp.sin(n*z) for n in range(1,17))
 zeta_tail=2*mp.exp(ell*ell/4)*(ell/2)**17/(17*mp.factorial(17))/(1-ell/36)
 check('coordinate_series_tail_bounded',zeta_tail<mp.mpf('1e-80'),mp.nstr(zeta_tail,40))
 def primitive(f):
  # Fubini converts the weighted mean of a primitive to one integral.
  mu=mp.quad(lambda z:(2*mp.pi-zeta(z))*Jac(z)*f(z),[0,mp.pi,2*mp.pi])/(2*mp.pi)
  return lambda z:mp.quad(lambda t:Jac(t)*f(t),[0,z])-mu
 phase2=mp.besseli(2,ell)/Abar
 target=[lambda z:mp.sin(z),lambda z:mp.cos(2*z)-phase2,lambda z:mp.sin(3*z)]
 slopes=[lambda z:mp.cos(z)/Jac(z),lambda z:-2*mp.sin(2*z)/Jac(z),lambda z:3*mp.cos(3*z)/Jac(z)]
 constants=[mp.mpf(1)/37,-mp.mpf(2)/41,mp.mpf(3)/43];harmonics=[mp.mpf(1)/7,-mp.mpf(1)/11,mp.mpf(1)/13]
 rates=[lambda z,i=i:constants[i]-(a(z)**2 if i<2 else 2*Abar*Abar)*slopes[i](z) for i in range(3)]
 result=gauge.solve(rates,lambda z:a(z)**2,lambda z:a(z)**2,Abar,mean,primitive,harmonics)
 check('actual_profile_weighted_modulus_rates',max(abs(x-y) for x,y in zip(constants,result['modulus_rates']))<mp.mpf('1e-40'))
 for z in (mp.mpf('.3'),mp.mpf('1.1'),mp.mpf('2.4')):
  err=max(abs(result['coordinate_velocity'][i](z)-target[i](z)-harmonics[i]) for i in range(3))
  check('both_parities_and_retained_harmonics_'+str(z),err<mp.mpf('1e-40'),mp.nstr(err,40))
  fixed=[rates[i](z)+(a(z)**2 if i<2 else 2*Abar*Abar)*result['coordinate_gradient'][i](z) for i in range(3)]
  check('corrected_metric_modulus_rates_'+str(z),max(abs(x-y) for x,y in zip(fixed,constants))<mp.mpf('1e-40'))
 check('omitted_periodic_integration_constant_rejected',abs(mean(lambda z:-rates[0](z)/a(z)**2))>mp.mpf('1e-10'))
 li=iv.mpf(1)/13000;hinv=iv.exp(2*li);ratio=iv.exp(4*li);hinvz=2*li*iv.exp(4*li)
 transverse_H1=iv.sqrt(2)*(1+ratio)*hinv;longitudinal_H1=hinv/iv.sqrt(2)
 transverse_FP_H2=(1+iv.sqrt(2))*(1+ratio)*hinv+hinv+(1+ratio)*hinvz;longitudinal_FP_H2=hinv
 check('whole_root_adapted_gauge_inverse_bounds_positive',all(mp.mpf(t._mpi_[0])>0 for t in (transverse_H1,longitudinal_H1,transverse_FP_H2,longitudinal_FP_H2)))
 ctx=load('gauge_prepared_point',FACTORY).point('0.3');J=ctx['J'];q=ctx['q'];dz=ctx['d'];p=ctx['pi'];L=ctx['L'];grad=ctx['gradient']
 xi=[J(coefficients=[iv.mpf(i+1)/37,-iv.mpf(i+2)/41,iv.mpf(i+1)/43]) for i in range(3)]
 xiz=[J(coefficients=[t.c[1],2*t.c[2],iv.mpf(0)]) for t in xi]
 zero=[J(0) for _ in range(14)]
 response=flow.apply(ctx,zero,zero,zero,xi,xiz);expected=gauge.lie_fields(q,dz,xi,xiz)
 err=max(ab((x-y).c[k]) for x,y in zip(response['field_rate'],expected[:13]) for k in range(3))
 check('actual_legendre_shift_kinematics_all_field_jets',err<mp.mpf('1e-28'),mp.nstr(err,40))
 pz=[J(coefficients=[t.c[1],2*t.c[2],iv.mpf(0)]) for t in p];dual=gauge.lie_momenta(p,pz,xi,xiz)
 err=max(ab(x-y.c[0]) for x,y in zip(response['momentum_rate'],dual))
 check('actual_canonical_momentum_density_shift_response',err<mp.mpf('1e-28'),mp.nstr(err,40))
 dq=[J(coefficients=[iv.mpf(i+1)/47,-iv.mpf(i+2)/53,iv.mpf(0)]) for i in range(14)];dd=[J(t.c[1]) for t in dq]
 lq=gauge.lie_fields(dq,dd,xi,xiz)
 pairing=sum((p[i]*lq[i]+dual[i]*dq[i] for i in range(14)),J(0)).c[0]
 divergence=(xi[2]*sum((p[i]*dq[i] for i in range(14)),J(0))).c[1]
 check('canonical_dual_lie_pairing_identity',ab(pairing-divergence)<mp.mpf('1e-28'))
 check('omitted_momentum_density_jacobian_rejected',ab(sum((xiz[2]*p[i]*dq[i] for i in range(14)),J(0)).c[0])>mp.mpf('1e-10'))
 z=mp.mpf('.3');lam=ell*mp.cos(z);lz=-ell*mp.sin(z);R2=mp.besseli(2,ell)/Abar;eps=mp.mpf(1)/1000
 w=mp.exp(-lam)*eps/31*mp.quad(lambda t:mp.exp(ell*mp.cos(t))*(mp.cos(2*t)-R2),[0,z]);wz=eps*(mp.cos(2*z)-R2)/31-lz*w;JJ=J(iv.mpf(str(Jac(z))));ww=J(iv.mpf(str(w)));wwz=J(iv.mpf(str(wz)))
 pdot=[grad(L,i).c[0]-grad(L,28+i).c[1] for i in range(14)]
 vn,pn=gauge.coordinate_rates(q,dz,p,pz,ctx['v'],[J(t) for t in pdot],ww,wwz,JJ)
 fct,pct=gauge.factors(JJ)
 check('all_metric_frame_scalar_canonical_coordinate_factors',max(ab((JJ*fct[i]*pct[i]-1).c[0]) for i in range(14))<mp.mpf('1e-28'))
 H=ctx['env']['numerical']['H'];expected_long=2*Abar*Abar*(mp.mpf(H)+eps*R2/31)
 check('actual_initial_longitudinal_gauge_velocity',ab(vn[5].c[0]-iv.mpf(str(expected_long)))<mp.mpf('1e-28'))
 check('unpaired_coordinate_rate_change_rejected',ab((fct[5]*ctx['v'][5]-vn[5]).c[0])>mp.mpf('1e-10'))
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_GAUGE_VELOCITY_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  bounds=dict(transverse_velocity_L2_H1=binary(transverse_H1),longitudinal_velocity_L2_H1=binary(longitudinal_H1),transverse_FP_L2_H2=binary(transverse_FP_H2),longitudinal_FP_L2_H2=binary(longitudinal_FP_H2)),coordinate_series_tail=mp.nstr(zeta_tail,40),
  scope='functional adapted gauge inverse and coordinate-rate maps with actual canonical-point response; density current row not yet closed',complete_prepared_evolution=False,current_density_closed=False,physical_norm='NOT_DERIVED',review='DEFERRED',physics_pass=False,gate_effect='NONE')
def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
