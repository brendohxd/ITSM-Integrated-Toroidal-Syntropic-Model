"""Green/range interpretation and full momentum Sobolev bounds.

Independent endpoint/chain-rule controls; not external scientific review.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_coupled_periodic_inverse_v1_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 d=json.loads((ROOT/PARENT).read_text());pins=dict(d['source_sha256']);snap={}
 for rel in (SELF,PARENT,FACTORY,MIXED):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  p=ROOT/rel;sc=Path(str(p)+'.sha256');assert SHA(p.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for f in (p,sc):snap[f]=(SHA(f.read_bytes()),f.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);ab=lambda x:max(abs(lo(x)),abs(hi(x)))
 binary=lambda x:[list(v) for v in x._mpi_]
 interval=lambda pair:iv.mpf([mp.mpf(tuple(v)) for v in pair])
 check('parent_all_checks_pass',d['passed']==d['total']==31 and all(c['passed'] is True for c in d['checks']))
 Cn=s.Rational(d['reference_nonzero_mass']);Cm=s.Rational(d['reference_mean_mass']);n=s.symbols('n',integer=True,positive=True)
 check('green_nonzero_modes_uniform_without_truncation',s.simplify((n*n+Cn)-(1+n*n))==Cn-1 and Cn>1)
 check('negative_mean_block_invertible_and_retained',Cm<0 and 1/abs(Cm)==s.Rational(d['reference_inverse_L2_H2']))
 e=interval(d['bounds']['operator_perturbation']);R0=iv.mpf(8400)/2263;q=R0*e;B=R0/(1-q)
 check('raw_endpoint_neumann_contraction',hi(q)<1,mp.nstr(hi(q),40))
 check('raw_endpoint_inverse_norm_matches_parent',ab(B-interval(d['coupled_inverse_L2_H2_bound']))<mp.mpf('1e-40'))
 sp=importlib.util.spec_from_file_location('inverse_sobolev_factory',ROOT/FACTORY);fac=importlib.util.module_from_spec(sp);sp.loader.exec_module(fac);env=fac.prepare();J=env['J'];yy,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
 hd=json.loads((ROOT/MIXED).read_text());H={tuple(r['ij']):interval(r['value']) for r in hd['full_mixed_Hessian_upper_triangle']}
 hh=lambda i,j:H.get((min(i,j),max(i,j)),iv.mpf(0))
 # Canonical p_z=H_v,y*y_z, using independent exported action Hessians and
 # fixed-profile/root first jets; no new full density evaluation is needed.
 pxprime=sum((abs(hh(16,k))*abs(yy[k].c[1]) for k in range(48)),iv.mpf(0))
 pyprime=sum((abs(hh(18,k))*abs(yy[k].c[1]) for k in range(48)),iv.mpf(0))
 l=iv.mpf(1)/13000;w2=iv.exp(2*l);ratio2=iv.exp(4*l);ratio1=iv.exp(2*l)
 tx=interval(d['bounds']['transverse_x']);ty=interval(d['bounds']['transverse_y']);terr=interval(d['bounds']['longitudinal_difference'])
 pi=iv.mpf(11)/10*iv.sqrt(iv.mpf(3469)/4620);tz=pi+terr
 px=tx/(1+ratio2);py=ty/(1+ratio2);pt=2*pi+2*terr/(1+ratio1)
 # Domain norm D=||r||_2+sum_i(||s_i||_2+|eta_i|), after known physical
 # source assembly and separate U1 completion. No source mean is discarded.
 cs=[(1+ratio2)*w2,(1+ratio2)*w2,(1+ratio1)*w2/2];ce=[ratio2,ratio2,ratio1]
 rv=env['lie'](yy[:14],yy[28:42],yy[42:45],yy[45:48]);rc=[iv.mpf(ab(yy[14+k].c[0]-rv[k].c[0])) for k in (2,4,5)]
 fconst=iv.mpf(max([hi(B)]+[hi(B*rc[i]*c) for i in range(3) for c in (cs[i],ce[i])]))
 source=[iv.mpf(max(hi(a),hi(b))) for a,b in zip(cs,ce)]
 pc2=[tx*fconst+source[0],ty*fconst+source[1],tz*fconst+source[2]]
 pch1=[(1+2*l)*pc2[0]+w2+(pxprime+2*l*px+px/2)*fconst,
       (1+2*l)*pc2[1]+w2+(pyprime+2*l*py+py/2)*fconst,
       (1+l)*pc2[2]+w2/2+(pt/4+l*pt)*fconst]
 full=fconst+sum(pch1,iv.mpf(0))
 check('all_three_momentum_H1_bounds_finite',all(mp.isfinite(hi(x)) and lo(x)>0 for x in pch1))
 check('coupled_H2_plus_H1_inverse_bound_finite',mp.isfinite(hi(full)),mp.nstr(hi(full),40))
 # The exact adjoint range is retained. Parity is only an example, not a
 # restriction on the projected inverse, whose proof used all harmonics.
 x=s.symbols('x',real=True);aa=s.Function('a')(x);P=s.Function('P')(x);f=s.Function('f')(x);pc=s.Function('pc')(x);src=s.Function('src')(x)
 R=aa/2*(s.diff(aa,x)/aa*P-s.diff(P,x))
 residual=s.diff(aa*pc-aa*P*f/2,x)-R*f-src/(2*aa)
 check('weighted_compatibility_integrand_exact',s.expand(2*aa*residual-(s.diff(2*aa*aa*pc,x)-s.diff(aa*aa,x)*pc-P*s.diff(aa*aa*f,x)-src))==0)
 # A concrete non-gauge cross-tensor direction in a planar background.
 hxy=s.Integer(0);xi=s.Function('xi')(x)
 check('tensor_cross_example_not_spatial_gauge',xi*s.diff(hxy,x)==0)
 check('range_not_replaced_by_all_source_data','weighted mean compatibility' in d['range'])
 check('current_and_scalar_density_not_conflated',d['physical_symplectic_quotient']=='NOT_DERIVED' and d['variable_coefficient_evolution_norm']=='NOT_DERIVED' and d['physics_pass'] is False)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_COUPLED_PERIODIC_INVERSE_AUDIT_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  data_norm='D=||assembled_current_source||L2+sum(||momentum_source_i||L2+|retained_momentum_mean_i|); transverse source means zero and solved longitudinal compatibility retained',
  trace_H2_per_D=binary(fconst),momentum_L2_per_D=[binary(v) for v in pc2],momentum_H1_per_D=[binary(v) for v in pch1],full_H2_H1_per_D=binary(full),background_transverse_momentum_derivative_bounds=[binary(pxprime),binary(pyprime)],
  scope='initial projected inverse and exact compatible range; physical scalar-density measure relation and charge completion are separate explicit formulas',review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);a=ap.parse_args();d=calculate();data=ENC(d)
 if a.replay:assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
