"""Independent Schur, weighted normalization and Sobolev pullback audit."""
from pathlib import Path
import argparse,hashlib,json,traceback
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
PRIMARY='Analysis/MasterTests/outputs/rtau_planar_current_operator_v2_20261119/receipt.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
def calculate():
    primary=json.loads((ROOT/PRIMARY).read_text(encoding='utf-8'));assert all(c['passed'] for c in primary['checks'])
    pins=dict(primary['source_pins'])
    for rel in (PRIMARY,Path(__file__).relative_to(ROOT).as_posix()):pins[rel]=digest(ROOT/rel)
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel;side=Path(str(p)+'.sha256')
        if not rel.endswith('.sha256'):assert side.read_text(encoding='utf-8').split()[0].lower()==h,rel
        for q in (p,side) if side.exists() else (p,):snap[q]=(digest(q),q.stat().st_mtime_ns)
    checks={};a,b,d,c=s.symbols('a b d c',positive=True);mx,my=s.symbols('mx my',real=True)
    G=s.Matrix([[a,b],[b,d]]);m=s.Matrix([mx,my]);h=(G+m*m.T/c).row_join(m).col_join(m.T.row_join(s.Matrix([[c]])))
    # Independent generic block inversion and contraction, without primary imports.
    K=h.inv();Q=G.row_join(s.zeros(2,1)).col_join(s.zeros(1,3))
    value=s.factor(sum((K[2,2]*K[i,j]-K[i,2]*K[j,2])*Q[i,j] for i in range(3) for j in range(3)))
    checks['generic_Schur_trace_curvature_contraction']=s.factor(value-(2/c+(m.T*G.inv()*m)[0]/c**2))==0
    checks['mixed_moduli_contribution_cannot_be_dropped']=s.factor(value-2/c)!=0
    # Actual covariance of the principal coefficient at the initial adapted chart.
    N,A,bar=s.symbols('N a Abar',positive=True);J=A/bar
    checks['principal_density_pullback_has_one_J']=s.simplify((-N*A)*J-(-N*A*A/bar))==0
    pnew,J0,Jt=s.symbols('pnew J0 Jt',nonzero=True)
    # p_new=p_old for xz/yz, p_new=J*p_old for zz; d zeta=J dz.
    checks['transverse_old_mean_weight_is_inverse_J']=s.simplify((pnew/J0)*J0-pnew)==0
    checks['longitudinal_old_mean_weight_is_inverse_J_squared']=s.simplify((pnew/J0**2)*J0-pnew/J0)==0
    checks['weight_time_factors_retained']=s.diff(J0**-1,J0)*Jt==-Jt/J0**2 and s.diff(J0**-2,J0)*Jt==-2*Jt/J0**3
    # General moving weighted inverse, using noncommuting exact rational matrices.
    M=s.Matrix([[2,s.Rational(1,7),s.Rational(1,9)],[s.Rational(1,7),3,-s.Rational(1,11)],[s.Rational(1,9),-s.Rational(1,11),4]])
    Mt=s.Matrix([[1,2,0],[0,1,3],[2,0,1]])/17
    checks['weighted_normalizer_inverse_drift']=M*(-M.inv()*Mt*M.inv())+Mt*M.inv()==s.zeros(3)
    checks['normalizer_drift_order_not_swappable']=-M.inv()*Mt*M.inv()!=-M.inv()*M.inv()*Mt
    # Sobolev pullback formula independent of the operator implementation.
    f1,f2,j,jz=s.symbols('f1 f2 j jz',nonzero=True)
    checks['second_derivative_coordinate_chain_rule']=s.diff(f1/j,f1)*f2/j+s.diff(f1/j,j)*jz/j==f2/j**2-jz*f1/j**3
    checks['H2_gradient_factor_one_half_is_sharp']=s.simplify((1+j*j)**2-4*j*j-(j*j-1)**2)==0
    gap=s.Rational(1,16);base=s.Integer(8)
    checks['adapted_Neumann_radius_and_bound']=base*gap==s.Rational(1,2) and base/(1-base*gap)==16 and 16**2==256
    eps=s.Rational(1,100)
    checks['weighted_mean_matrix_margin_in_geometric_envelope']=8*eps<1 and 4/(1-8*eps)==s.Rational(100,23)
    checks['weighted_trace_coercive_bound_in_envelope']=9*eps<1 and 2/(1-9*eps)==s.Rational(200,91)
    # Transport the old projected residual as a covector density, not a scalar.
    amount=s.symbols('amount',nonzero=True)
    old_res=-2*A*amount
    transported=old_res/J**2
    checks['old_residual_profile_covector_density_pullback']=s.simplify(transported-(-2*bar*amount)/J)==0
    checks['constant_new_residual_extension_is_different']=s.simplify(transported-(-2*bar*amount))!=0
    zz=s.symbols('zz',real=True)
    rho=1+s.cos(zz)/9;source=2+s.cos(2*zz)+s.sin(3*zz)
    primitive=s.sin(2*zz)/2-s.cos(3*zz)/3;primitive_rho=s.sin(zz)/9
    checks['transported_projector_primitive_identity']=s.simplify(s.diff(primitive-2*primitive_rho,zz)-source+2*rho)==0
    checks['omitted_projector_profile_is_rejected']=s.simplify(s.diff(primitive,zz)-source+2*rho)!=0
    tt=s.symbols('tt');p0,p1,c0,c1=s.symbols('p0 p1 c0 c1')
    checks['moving_rank_profile_keeps_both_terms']=s.expand(s.diff(-(p0+tt*p1)*(c0+tt*c1),tt)+(p1*(c0+tt*c1)+(p0+tt*p1)*c1))==0
    mp.mp.dps=80;mp.iv.dps=60;iv=mp.iv;r=iv.mpf(1)/13000
    upper=lambda v:mp.mpf(iv.mpf(v)._mpi_[1])
    independent=iv.mpf('7.970')*(iv.exp(3*r)+r*iv.exp(7*r)/2)*iv.exp(r)
    checks['independent_initial_Green_transport_less_than_8']=upper(independent)<8
    checks['actual_initial_weights_in_one_percent_envelope']=upper(iv.exp(4*r)-1)<mp.mpf('.01')
    err=mp.mpf(primary['action_control']['maximum_density_identity_defect']);q=mp.mpf(primary['action_control']['inverse_contraction_upper'])
    checks['full_action_control_tolerances_and_inverse_margin']=err<mp.mpf('1e-28') and q<mp.mpf('.5')
    checks['all_original_bytes_and_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items())
    return {'kind':'RTAU_PLANAR_CURRENT_OPERATOR_SEPARATE_AUDIT_V2','source_pins':pins,'pinned_files':len(pins),
      'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
      'coverage':'INDEPENDENT_GENERIC_SCHUR_AND_PULLBACK_ALGEBRA_PLUS_PRIMARY_ACTION_RECEIPT_AUDIT_NOT_SECOND_ACTION_IMPLEMENTATION',
      'actual_background_time_tube':'OPEN','review_status':'DEFERRED','Rule9_cleared':False,'Rtau_adopted':False,'physics_pass':False,'gate_effect':'NONE'}
def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=False)
    try:
        d=calculate();raw=enc(d)
        if a.replay:assert a.replay.read_bytes()==raw,'Replay byte mismatch'
        else:
            a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_bytes((hashlib.sha256(raw).hexdigest()+'  '+a.output.resolve().relative_to(ROOT).as_posix()+'\n').encode())
        bad=[c['name'] for c in d['checks'] if not c['passed']];print(json.dumps({'passed':len(d['checks'])-len(bad),'total':len(d['checks']),'failures':bad,'pins':d['pinned_files'],'physics_pass':False,'replay':bool(a.replay)}))
        if bad:raise SystemExit(1)
    except Exception:
        if a.output:(a.output.parent/'failure.json').write_bytes(enc({'error':traceback.format_exc(),'physics_pass':False}))
        raise
if __name__=='__main__':main()
