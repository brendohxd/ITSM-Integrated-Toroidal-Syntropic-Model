"""Initial canonical/gauge rate bound, not a full physical norm."""
from pathlib import Path
import argparse,hashlib,json
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
FILES={
 'mixed':'Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json',
 'initial':'Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json',
 'gauge':'Analysis/MasterTests/outputs/r4c1_rtau_gauge_velocity_v1_attempt_01/summary.json',
 'map':'Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json',
 'aux':'Analysis/MasterTests/outputs/rtau_coupled_auxiliary_variation_v1_20261102/receipt.json',
 'spec':'Theory/Gates/RES-001/RES001_RTAU_CANONICAL_AUXILIARY_PULLBACK_V2_SPEC_2026-11-02.md',
 'original_spec':'Theory/Gates/RES-001/RES001_RTAU_CANONICAL_AUXILIARY_PULLBACK_V1_SPEC_2026-11-02.md'}


def run():
 mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv;checks=[]
 def check(n,ok):checks.append(dict(name=n,passed=bool(ok)))
 d={k:json.loads((ROOT/p).read_text()) for k,p in FILES.items() if not k.endswith('spec')}
 decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
 hi=lambda x:mp.mpf(x._mpi_[1]);lo=lambda x:mp.mpf(x._mpi_[0])
 upper=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
 H={tuple(x['ij']):decode(x['value']) for x in d['mixed']['full_mixed_Hessian_upper_triangle']}
 get=lambda i,j:H.get(tuple(sorted((i,j))),iv.mpf(0))
 check('auxiliary_columns_exactly_absent',all(tuple(sorted((i,j))) not in H for i in range(14,27) for j in (13,41)))
 assert checks[-1]['passed']
 norms={}
 for name,cols in [('A',range(13)),('B',range(28,41))]:
  mat=[[upper(get(i,j)) for j in cols] for i in range(14,27)]
  frob=iv.sqrt(sum((x*x for row in mat for x in row),iv.mpf(0)))
  row=max(hi(sum(v,iv.mpf(0))) for v in mat)
  col=max(hi(sum((mat[i][j] for i in range(13)),iv.mpf(0))) for j in range(13))
  norms[name]=frob;norms[name+'_row_column']=iv.sqrt(iv.mpf(row)*col)
  check(name+'_norms_finite',mp.isfinite(hi(frob)) and mp.isfinite(hi(norms[name+'_row_column'])))
 Minv=decode(d['initial']['bounds']['original_temporal_inverse'])
 b=d['map']['bounds'];j=iv.mpf(lo(decode(b['J_lower_binary'])));ju=iv.mpf(hi(decode(b['J_upper_binary'])))
 W=iv.mpf(hi(decode(b['drift_upper_binary'])));P=iv.mpf(hi(decode(b['drift_derivative_upper_binary'])))
 r=iv.mpf(1)/13000;F=iv.mpf(max(mp.mpf(1),hi(ju),hi(1/j**2)))
 F=F*iv.sqrt(ju)
 diagonal=iv.mpf(max(mp.mpf(1),hi(ju),hi(1/j)))
 Cback=(diagonal+r/j)/iv.sqrt(j)
 Cxi=iv.mpf(max(hi(decode(d['gauge']['bounds'][k])) for k in ['transverse_velocity_L2_H1','longitudinal_velocity_L2_H1']))
 check('pullback_covers_transverse_matrix',hi(Cback)>=hi(ju/iv.sqrt(j)))
 check('pullback_covers_longitudinal_matrix',hi(Cback)>=hi((1/j+r/j)/iv.sqrt(j)))
 x=s.symbols('x');f=s.Function('f');zeta=s.Function('zeta')(x);JJ=s.diff(zeta,x)
 check('longitudinal_pullback_chain_rule',s.simplify(s.diff(f(zeta)/JJ,x)-(s.Subs(s.diff(f(x),x),x,zeta)-f(zeta)*s.diff(JJ,x)/JJ**2))==0)
 Ch=2*iv.exp(2*r)*(1+iv.sqrt(3)*r);S1=iv.mpf(1)/1000*(iv.mpf(1)/29+iv.mpf(2)/31)
 aux={k:decode(v) for k,v in d['aux']['constants_binary'].items()}
 R=aux['eta']*S1+aux['metric_velocity']*Ch
 U=aux['eta']+iv.sqrt(2)*aux['metric_velocity']+R*Cback*Cxi*F
 C=dict(momentum=U*Minv,configuration=U*Minv*norms['A']+2*P*R*Cback*Cxi*F+iv.sqrt(2)*aux['metric'],
        configuration_z=U*Minv*norms['B']+W*R*Cback*Cxi*F+aux['chi_z'],harmonic_velocity=R*Cback)
 check('harmonic_contribution_retained',lo(C['harmonic_velocity'])>0)
 check('actual_map_constants_positive_finite',all(lo(x)>0 and mp.isfinite(hi(x)) for x in C.values()))
 vals=[s.Rational(i+1,17) for i in range(6)]
 m=s.Matrix([[vals[0],vals[1],vals[2]],[vals[1],vals[3],vals[4]],[vals[2],vals[4],vals[5]]])
 check('full_matrix_slot_factor',s.trace(m.T*m)<=2*sum(x*x for x in vals))
 rr=s.Rational(1,13000);xi=s.Matrix([1,2,3])/17;xp=s.Matrix([-2,4,1])/19;ez=s.Matrix([0,0,1])
 lie=2*rr*xi[2]*s.eye(3)+ez*xp.T+xp*ez.T
 check('metric_Lie_probe_bound',s.trace(lie.T*lie)<=4*(1+s.sqrt(3)*rr)**2*(xi.dot(xi)+xp.dot(xp)))
 sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES.values()}
 sources[Path(__file__).resolve().relative_to(ROOT).as_posix()]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
 return dict(scope='INITIAL_CANONICAL_GAUGE_AUXILIARY_MAP_ONLY',physics_pass=False,physical_norm='NOT_DERIVED',
   checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),
   constants_binary={k:[list(t) for t in v._mpi_] for k,v in C.items()},
   upper_display={k:mp.nstr(hi(v),16) for k,v in C.items()},
   legendre_block_bounds={k:[list(t) for t in v._mpi_] for k,v in norms.items()},
   constraint_time_persistence=False,source_sha256=sources)


if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=p.parse_args()
 d=run();raw=(json.dumps(d,indent=2,sort_keys=True)+'\n').encode()
 if a.output:
  a.output.parent.mkdir(parents=True,exist_ok=True)
  with a.output.open('xb') as f:f.write(raw)
 else:assert a.verify.read_bytes()==raw
 print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[x for x in d['checks'] if not x['passed']],'bounds':d['upper_display']},indent=2))
 raise SystemExit(0 if d['passed']==d['total'] else 1)
