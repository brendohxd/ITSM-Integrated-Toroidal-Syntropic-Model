"""Independent material/coordinate calculus and drift-envelope arithmetic."""
from pathlib import Path
import argparse,hashlib,json,traceback
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
PRIMARY='Analysis/MasterTests/outputs/rtau_planar_current_drift_v2_20261119/receipt.json'
COEFF='Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def calculate():
    primary=json.loads((ROOT/PRIMARY).read_text(encoding='utf-8'));assert all(c['passed'] for c in primary['checks'])
    pins=dict(primary['source_pins'])
    for rel in (PRIMARY,Path(__file__).relative_to(ROOT).as_posix()):pins[rel]=digest(ROOT/rel)
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel;side=Path(str(p)+'.sha256')
        if not rel.endswith('.sha256'):assert side.read_text(encoding='utf-8').split()[0].lower()==h,rel
        for f in (p,side) if side.exists() else (p,):snap[f]=(digest(f),f.stat().st_mtime_ns)
    checks={};q=s.Matrix(s.symbols('q1 q2'));d=s.Matrix(s.symbols('d1 d2'));v=s.Matrix(s.symbols('v1 v2'));u=s.Matrix(s.symbols('u1 u2'))
    S,Sz=s.symbols('S Sz');T=s.Matrix([[1,s.Rational(1,3)],[-s.Rational(1,5),2]])*Sz
    M=s.Matrix([[2+q[0]**2,q[0]*q[1]/7],[q[0]*q[1]/7,3+q[1]**2]])
    normal=v-S*d-T*q
    def lag(rate):return (rate.T*M*rate)[0]/2+rate[0]**3/11+q[0]*d[1]*rate[1]+q[0]**2*d[1]**2
    L=lag(normal);L0=lag(u);sub={v[i]:u[i]+(S*d+T*q)[i] for i in range(2)}
    p=s.Matrix([s.diff(L,x) for x in v])
    checks['independent_two_field_material_gradient']=all(s.simplify((s.diff(L,q[i])+(T.T*p)[i]).subs(sub)-s.diff(L0,q[i]))==0 for i in range(2))
    checks['independent_two_field_material_spatial_gradient']=all(s.simplify((s.diff(L,d[i])+S*p[i]).subs(sub)-s.diff(L0,d[i]))==0 for i in range(2))
    checks['velocity_nonlinearity_not_assumed_absent']=s.diff(L0,u[0],3)!=0
    z,t=s.symbols('z t',real=True);J=s.Function('J')(t,z);w=s.Function('w')(t,z)
    A0,A1,A2=[s.Function(n)(t,z) for n in ('A0','A1','A2')]
    Dt=lambda f:s.diff(f,t)-w*s.diff(f,z)
    Jt=s.diff(J*w,z);jz=s.diff(J,z)/J
    def reduce(f):return s.simplify(s.expand(f).subs(s.diff(J,t,z),s.diff(Jt,z)).subs(s.diff(J,t),Jt).doit())
    checks['independent_second_order_coefficient_transport']=reduce(Dt(J*A2)-J*(Dt(A2)+s.diff(w,z)*A2))==0
    checks['independent_first_order_coefficient_transport']=reduce(Dt(A1+A2*jz)-Dt(A1)-Dt(A2)*jz-A2*(s.diff(w,z,2)+jz*s.diff(w,z)))==0
    checks['independent_zeroth_order_density_transport']=reduce(Dt(A0/J)-(Dt(A0)-s.diff(w,z)*A0)/J)==0
    f=s.Function('f')(t,z)
    checks['coordinate_and_time_derivative_do_not_commute_by_default']=s.simplify(Dt(s.diff(f,z))-s.diff(Dt(f),z)-s.diff(w,z)*s.diff(f,z))==0
    p0,p1,a0,a1=s.symbols('p0 p1 a0 a1')
    checks['finite_rank_profile_drift_has_two_terms']=s.expand(s.diff((p0+t*p1)*(a0+t*a1),t)-p1*(a0+t*a1)-(p0+t*p1)*a1)==0
    # The weighted normalizer's exact initial value is checked by distinct
    # quadrature and Bessel identities; samples do not prove a continuum bound.
    mp.mp.dps=100;mp.iv.dps=60;r=mp.mpf(1)/13000;abar=mp.besseli(0,r)
    for count in (32,64):
        means=[mp.mpf(0),mp.mpf(0)]
        for k in range(count):
            a=mp.exp(r*mp.cos(2*mp.pi*k/count));jac=a/abar
            means[0]+=jac*(abar/a)*a**-2/count
            means[1]+=jac*(abar/a)**2/(2*abar**2)/count
        checks['initial_weighted_normalizer_Bessel_'+str(count)]=abs(means[0]-mp.besseli(0,2*r))<mp.mpf('1e-80') and abs(means[1]-mp.mpf('.5'))<mp.mpf('1e-80')
    iv=mp.iv;decode=lambda a:iv.mpf([mp.mpf(tuple(v)) for v in a]);lo=lambda a:mp.mpf(iv.mpf(a)._mpi_[0]);hi=lambda a:mp.mpf(iv.mpf(a)._mpi_[1])
    b={k:decode(v) for k,v in primary['bounds_binary'].items()}
    assembled=b['a2_time']+b['a1_time']/2+b['a0_time']+b['normal_metric_rate_time']*b['trace_momentum_map']+b['normal_metric_rate']*b['trace_momentum_map_time']
    def overlap(x,y):return max(lo(x),lo(y))<=min(hi(x),hi(y))
    checks['full_Lt_bound_composed_from_all_sectors']=overlap(assembled,b['coupled_current_operator_time'])
    checks['initial_Green_drift_uses_actual_initial_8_squared']=overlap(64*b['coupled_current_operator_time'],b['initial_Green_time'])
    checks['finite_rank_time_omission_would_change_bound']=hi(b['residual_profile_primitive_time']*b['s'])>0
    # A first-event derivative cannot be integrated as a uniform future bound.
    B0=s.symbols('B0',nonnegative=True);growth=B0+100*t
    checks['initial_derivative_alone_does_not_control_future_margin']=growth.subs(t,0)==B0 and s.integrate(growth,(t,0,s.Rational(1,20)))>s.Rational(1,16)
    checks['all_original_source_hashes_and_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items())
    return {'kind':'ACTUAL_INITIAL_CURRENT_DRIFT_SEPARATE_AUDIT_V2','source_pins':pins,'pinned_files':len(pins),
      'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
      'coverage':'INDEPENDENT_MATERIAL_AND_COORDINATE_IDENTITIES_BESSEL_CONTROL_AND_PRIMARY_BOUND_AUDIT_NOT_SECOND_FULL_ACTION_EXPORT',
      'future_operator_margin':'OPEN','actual_background_persistence':'OPEN','energy_continuation':'OPEN',
      'review_status':'DEFERRED','Rule9_cleared':False,'physics_pass':False,'gate_effect':'NONE','Rtau_adopted':False}
def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=False)
    try:
        data=calculate();raw=enc(data)
        if a.replay:assert a.replay.read_bytes()==raw,'Replay byte mismatch'
        else:
            a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_bytes((hashlib.sha256(raw).hexdigest()+'  '+a.output.resolve().relative_to(ROOT).as_posix()+'\n').encode())
        bad=[c['name'] for c in data['checks'] if not c['passed']];print(json.dumps({'passed':len(data['checks'])-len(bad),'total':len(data['checks']),'failures':bad,'pins':data['pinned_files'],'physics_pass':False,'replay':bool(a.replay)}))
        if bad:raise SystemExit(1)
    except Exception:
        if a.output:(a.output.parent/'failure.json').write_bytes(enc({'error':traceback.format_exc(),'physics_pass':False}))
        raise
if __name__=='__main__':main()
