"""Prepared-data planar constrained ordinary/quartic principal calculation.

This is a frozen principal symbol, not a full PDE symmetrizer or evolution
certificate. Global means/charges are not discarded by a nonzero-covector test.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as s
ROOT=Path(__file__).resolve().parents[2];SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_clock_identity_v2_attempt_01/summary.json'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_prepared_operator_factory_v2.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_PREPARED_PRINCIPAL_V1_CONTRACT_2026-11-01.md'
SHA=lambda b:hashlib.sha256(b).hexdigest();ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
DYN=[0,1,3,6,7,8,9,10,11,12];SLOW=DYN[:-1]

def calculate():
 mp.mp.dps=100;mp.iv.dps=50;iv=mp.iv;checks=[]
 def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
 parent=json.loads((ROOT/PARENT).read_text());assert SHA((ROOT/PARENT).read_bytes())=='fa72a504e953901fb132483638a33cf97dc2c81ba9e87664bc208012046b8559'
 pins=dict(parent['source_sha256']);snap={}
 for rel in (SELF,PARENT,MIXED,FACTORY,CONTRACT):pins[rel]=SHA((ROOT/rel).read_bytes())
 for rel,h in pins.items():
  f=ROOT/rel;sc=Path(str(f)+'.sha256');assert SHA(f.read_bytes())==h and sc.read_text().split()[0].lower()==h
  for p in (f,sc):snap[p]=(SHA(p.read_bytes()),p.stat().st_mtime_ns)
 lo=lambda x:mp.mpf(x._mpi_[0]);hi=lambda x:mp.mpf(x._mpi_[1]);ab=lambda x:max(abs(lo(x)),abs(hi(x)));mid=lambda x:(lo(x)+hi(x))/2
 binary=lambda x:[list(t) for t in x._mpi_]
 interval=lambda pair:iv.mpf([mp.mpf(tuple(x)) for x in pair])
 zero=iv.mpf(0)
 def tr(a):return [list(row) for row in zip(*a)]
 def mat(n,m):return [[iv.mpf(0) for _ in range(m)] for _ in range(n)]
 def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),zero) for j in range(len(b[0]))] for i in range(len(a))]
 def add(a,b,sign=1):return [[x+sign*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
 def identity(n):return [[iv.mpf(int(i==j)) for j in range(n)] for i in range(n)]
 def inf(a):return max(sum(ab(x) for x in row) for row in a)
 def sub(h,rows,cols):return [[h(i,j) for j in cols] for i in rows]
 kref=[[iv.mpf(1)/2,zero,zero],[zero,iv.mpf(1)/2,zero],[zero,zero,-iv.mpf(1)/15]]
 kinvref=[[iv.mpf(2),zero,zero],[zero,iv.mpf(2),zero],[zero,zero,-iv.mpf(15)]]
 def inverse_shift(K):
  E=mul(kinvref,add(K,kref,-1));delta=inf(E);assert delta<1
  power=identity(3);series=identity(3)
  for n in range(1,6):power=mul(power,E);series=add(series,power,(-1)**n)
  ki=mul(series,kinvref);error=iv.mpf(delta)**6/(1-iv.mpf(delta))*15
  ki=[[x+iv.mpf([-hi(error),hi(error)]) for x in row] for row in ki]
  return ki,delta,error
 def reduce(h):
  vv=[14+i for i in DYN];dd=[28+i for i in DYN];ww=[45,46,47]
  K=sub(h,ww,ww);ki,delta,error=inverse_shift(K)
  C=sub(h,vv,ww);D=sub(h,dd,ww)
  M=add(sub(h,vv,vv),mul(mul(C,ki),tr(C)),-1)
  B=add(sub(h,vv,dd),mul(mul(C,ki),tr(D)),-1)
  G=add(sub(h,dd,dd),mul(mul(D,ki),tr(D)),-1)
  return M,B,G,ki,delta,error
 def mp_matrix(a):return mp.matrix([[mid(x) for x in row] for row in a])
 def block9(a):return [row[:9] for row in a[:9]]
 sp=importlib.util.spec_from_file_location('prepared_principal_factory',ROOT/FACTORY);factory=importlib.util.module_from_spec(sp);sp.loader.exec_module(factory);env=factory.prepare(order=1)
 J=env['J'];j=env['j'];D=env['D'];density=env['density'];lifted=env['lifted'];hj=env['hj']
 def evaluate(values):
  y=[J.cast(v) for v in values];return y,density(lifted([D.var(v,i) for i,v in enumerate(y)]))[0]
 def accessor(L):return lambda i,k:hj(L,i,k).c[0]
 # Off-shell reference is an action-coefficient control, not a background.
 # Nonzero psi_z avoids evaluating third derivatives of |grad psi|^3 at zero.
 ref=[J(0) for _ in range(48)]
 for i in (0,3,5,9,11):ref[i]=J(1)
 ref[26]=J(iv.mpf(1)/5);ref[40]=J(iv.mpf(1)/1000)
 y,L=evaluate(ref);M0,B0,G0,_,_,_=reduce(accessor(L))
 def rational(a):
  out=[];good=True
  for row in a:
   rr=[]
   for x in row:
    v=s.Rational(str(mid(x))).limit_denominator(1000000);q=iv.mpf(int(v.p))/int(v.q)
    good=good and ab(x-q)<mp.mpf('1e-40');rr.append(v)
   out.append(rr)
  return s.Matrix(out),good
 MR,mok=rational(M0);BR,bok=rational(B0);GR,gok=rational(G0)
 check('reference_rational_coefficients_enclosed',mok and bok and gok)
 check('reference_reduced_kinetic_gap_at_least_one_eighth',all((MR-s.eye(10)/8)[:i,:i].det()>0 for i in range(1,11)))
 c=s.symbols('c');MS=MR[:9,:9];BS=BR[:9,:9];GS=GR[:9,:9]
 pencil=c*c*MS-c*(BS+BS.T)+GS
 poly=s.Poly(s.factor(pencil.det(method='domain-ge')/MS.det()),c)
 expected=s.Poly(c*c*(c*c-s.Rational(1,3))*(c*c-s.Rational(4,5))**2*(c*c-1)**5,c)
 check('fresh_reference_ordinary_polynomial',poly==expected,str(s.factor(poly.as_expr())))
 check('ordinary_zero_root_is_defective_in_equal_order_balancing',s.Poly(poly,c).as_expr().coeff(c,0)==0 and GS.nullspace() and len(GS.nullspace())==1)
 check('reference_zero_root_algebraic_multiplicity_two',s.expand(poly.as_expr()).coeff(c,2)!=0 and s.expand(poly.as_expr()).coeff(c,1)==0)
 # Full certified-root uncertainty is inherited from the immutable exported Hessian.
 mixed=json.loads((ROOT/MIXED).read_text());whole={tuple(r['ij']):interval(r['value']) for r in mixed['full_mixed_Hessian_upper_triangle']}
 wh=lambda i,k:whole.get((min(i,k),max(i,k)),zero)
 MW,BW,GW,KI,delta,err=reduce(wh)
 mref=[[iv.mpf(int(MR[i,k].p))/int(MR[i,k].q) for k in range(10)] for i in range(10)]
 difference=inf(add(MW,mref,-1));gap=iv.mpf(1)/8-iv.mpf(difference)
 check('whole_root_shift_principal_inverse_controlled',delta<1,mp.nstr(delta,40))
 check('whole_root_reduced_kinetic_positive',lo(gap)>0,mp.nstr(lo(gap),40))
 # Derivative-level zeros justify ordinary/fast separation in this actual action.
 check('force_velocity_not_mixed_with_other_principal_velocities',all(wh(26,14+i)==0 for i in SLOW) and all(wh(26,k)==0 for k in (45,46,47)))
 check('auxiliary_has_no_time_derivative_or_shift_gradient_couplings',all(wh(27,i)==0 for i in range(48)) and all(wh(41,i)==0 for i in list(range(14,28))+[45,46,47]))
 check('auxiliary_gradient_couples_to_no_other_field_gradient',all(wh(41,28+i)==0 for i in SLOW))
 check('auxiliary_mass_and_force_gradient_coefficient_nonsingular',lo(wh(13,13))>0 and hi(wh(41,40))<0)
 # Quartic branch: omega^2/k^4=C_Zpsi^2/(L_ZZ*M_psi_psi).
 fast=wh(41,40)**2/(wh(13,13)*MW[9][9])
 check('whole_root_quartic_coefficient_positive',lo(fast)>0,[mp.nstr(lo(fast),40),mp.nstr(hi(fast),40)])
 points=[];omission=False
 def verify(label,y,L):
  h=accessor(L);M,B,G,_,de,_=reduce(h);ms=mp_matrix(block9(M));bs=mp_matrix(block9(B));gs=mp_matrix(block9(G))
  a=mp.sqrt(mid(y[0].c[0]));N=mp.exp(-mp.mpf(2)/5*mid(y[12].c[0]));shift=mid(y[44].c[0]);V=[a*mid(t.c[0]) for t in y[6:9]];gamma=mp.sqrt(1+sum(v*v for v in V))
  # Nineteen distinct evaluation points compare two degree-18 polynomials.
  errors=[]
  for index in range(19):
   cn=mp.mpf(-19)/10+mp.mpf(index)/5;cc=-shift+N/a*cn
   actual=mp.det(cc*cc*ms-cc*(bs+bs.T)+gs)/mp.det(ms)*(a/N)**18
   cone=lambda v:cn*cn-1+(1/v-1)*(gamma*cn-V[2])**2
   # Normalize the aether cone quadratics to monic in cn.
   want=cn*cn*(cn*cn-1)**5*cone(mp.mpf(1)/3)/(1+2*gamma*gamma)*(cone(mp.mpf(4)/5)/(1+gamma*gamma/4))**2
   errors.append(abs(actual-want)/(1+abs(want)))
  check('prepared_covariant_ordinary_factors_'+label,max(errors)<mp.mpf('1e-28'),mp.nstr(max(errors),40))
  # Independent auxiliary-field Schur algebra: fast psi adjustment cancels
  # the induced k^2 slow term. Deleting k^3 mixing leaves that term behind.
  A=[h(41,i) for i in SLOW];Zmass=h(13,13);C=h(41,40)
  spurious=[[x*v/Zmass for v in A] for x in A]
  cancellation=inf([[x*v/Zmass-(x*C/Zmass)*(C*v/Zmass)/(C*C/Zmass) for v in A] for x in A])
  check('auxiliary_fast_response_cancels_induced_slow_stiffness_'+label,cancellation<mp.mpf('1e-28'))
  if label=='0.3':omission=inf(spurious)>mp.mpf('1e-18')
  # Return a value instead of mutating a surrounding certificate.
  return dict(label=label,maximum_polynomial_relative_defect=mp.nstr(max(errors),40),shift_neumann_delta=mp.nstr(de,40),omitted_fast_mixing_spurious_stiffness=mp.nstr(inf(spurious),40),physical_frame=[mp.nstr(v,40) for v in V],lapse=mp.nstr(N,40),scale=mp.nstr(a,40))
 for zs in ('0.3','1.1','2.4'):
  vals,LL,_=env['second_at'](J.variable(iv.mpf(zs)),False);yy=[J.cast(v) for v in vals]
  row=verify(zs,yy,LL);points.append(row)
  if zs=='0.3':omission=mp.mpf(row['omitted_fast_mixing_spurious_stiffness'])>mp.mpf('1e-18')
 tilted=list(ref)
 for i,k in enumerate((100,200,300)):tilted[6+i]=J(iv.mpf(k)/4993)
 yy,LL=evaluate(tilted);points.append(verify('rational_tilt_control',yy,LL))
 check('omitted_k_cubed_fast_mixing_rejected',omission)
 for f,(h,t) in snap.items():assert SHA(f.read_bytes())==h and f.stat().st_mtime_ns==t
 check('all_source_bytes_and_mtimes_preserved',True,len(snap))
 return dict(kind='R4C1_RTAU_PREPARED_PRINCIPAL_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
  dynamic_slots=DYN,ordinary_slots=SLOW,reference_kinetic=[[str(x) for x in row] for row in MR.tolist()],reference_mixed=[[str(x) for x in row] for row in BR.tolist()],reference_gradient=[[str(x) for x in row] for row in GR.tolist()],reference_ordinary_polynomial=str(s.factor(poly.as_expr())),reference_zero_geometric_multiplicity=len(GS.nullspace()),reference_zero_algebraic_multiplicity=2,
  whole_root_shift_inverse=[[binary(x) for x in row] for row in KI],whole_root_shift_neumann_delta=mp.nstr(delta,40),whole_root_kinetic_reference_error=mp.nstr(difference,40),whole_root_kinetic_lower_bound=binary(gap),whole_root_coordinate_quartic_coefficient=binary(fast),point_controls=points,
  principal_scope='initial planar nonzero covector; frozen constrained derivative pencil; means and both charges remain separate',physical_symplectic_quotient='NOT_DERIVED',strong_hyperbolicity='NOT_ESTABLISHED',nonlinear_time_evolution=False,physical_window_demonstrated=False,review='DEFERRED',physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE',canonical_parent_adopted=False)

def main():
 ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);args=ap.parse_args();d=calculate();data=ENC(d)
 if args.replay:assert args.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
 else:
  args.output_dir.mkdir(parents=True,exist_ok=False);p=args.output_dir/'summary.json';p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n');print(json.dumps(dict(passed=d['passed'],total=d['total'],receipt=str(p))))
 return 0 if d['passed']==d['total'] else 1
if __name__=='__main__':raise SystemExit(main())
