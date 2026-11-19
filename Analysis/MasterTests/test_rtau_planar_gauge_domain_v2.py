"""Conditional general-planar gauge/momentum inverses; not a background tube."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, traceback
import sympy as sp
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
GATE='Theory/Gates/RES-001/'
PARENT='Analysis/MasterTests/outputs/rtau_initial_energy_assembly_v1_20261114/receipt.json'
COEFF='Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'
CONTRACT=GATE+'RES001_RTAU_PLANAR_GAUGE_DOMAIN_V1_CONTRACT_2026-11-19.md'
CORRECTION=GATE+'RES001_RTAU_PLANAR_GAUGE_DOMAIN_V2_SPEC_2026-11-19.md'
PREP=GATE+'RES001_RTAU_HARMONIC_DOMAIN_CONTINUATION_V1_PREPARATION_2026-11-19.md'
LIE='Analysis/MasterTests/r4c1_gauge_velocity_v1.py'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

def exact_controls():
    x=sp.symbols('x',nonzero=True);I=sp.I;Q=sp.Rational
    expand=lambda a:sp.expand(sp.cancel(a))
    D=lambda a:expand(I*x*sp.diff(a,x))
    def terms(a):
        return [(int(v.as_powers_dict().get(x,0)),v) for v in sp.Add.make_args(expand(a))]
    mean=lambda a:expand(sum(v for n,v in terms(a) if n==0))
    P=lambda a:expand(sum(v/(I*n) for n,v in terms(a) if n))
    em=lambda a:a.applyfunc(expand)
    dm=lambda a:a.applyfunc(D)
    mm=lambda a:a.applyfunc(mean)
    pm=lambda a:a.applyfunc(P)
    zero=lambda a:all(expand(v)==0 for v in a)
    checks={}
    spec=importlib.util.spec_from_file_location('registered_planar_lie',ROOT/LIE)
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    f=(x+1/x)/20
    ft=(x-1/x)/(30*I)
    # Schur complement has constant determinant, giving a lossless Laurent inverse.
    H=sp.Matrix([[2,2*f],[2*f,3+2*f*f]])
    Ht=sp.Matrix([[0,2*ft],[2*ft,4*f*ft]])
    c=Q(3,2);ct=Q(1,7);m=sp.Matrix([Q(1,7),-Q(1,9)]);mt=sp.Matrix([Q(1,11),Q(1,13)])
    h=H+m*m.T/c;ht=Ht+(mt*m.T+m*mt.T)/c-m*m.T*ct/c**2
    h=h.row_join(m).col_join(m.T.row_join(sp.Matrix([[c]])))
    ht=ht.row_join(mt).col_join(mt.T.row_join(sp.Matrix([[ct]])))
    h,ht=em(h),em(ht)
    Ki=sp.Matrix([[Q(1,2)+f*f/3,-f/3],[-f/3,Q(1,3)]])
    K=Ki.row_join(-Ki*m/c).col_join((-m.T*Ki/c).row_join(sp.Matrix([[1/c+(m.T*Ki*m)[0]/c**2]])))
    K=em(K);Kt=em(-K*ht*K);M=mm(K);W=sp.diag(1,1,2);R=sp.diag(1,1,Q(1,2));B=W*h
    checks['exact_nonconformal_full_metric_inverse']=zero(h*K-sp.eye(3))
    checks['nonconstant_transverse_and_constant_nonzero_mixed_moduli']=D(h[0,1])!=0 and h[0,0]!=h[1,1] and all(D(h[i,2])==0 for i in range(3)) and h[0,2]!=0 and h[1,2]!=0
    q=[h[0,0],h[0,1],h[0,2],h[1,1],h[1,2],h[2,2]]+[1+Q(i+1,23)*(x+1/x)+Q(i+2,29)*(x-1/x)/I for i in range(8)]
    dz=list(map(D,q));elm=[2,4,5]
    Bg=sp.Matrix(14,3,lambda i,j:old.lie_fields(q,[0]*14,[0]*3,[int(k==j) for k in range(3)])[i])
    checks['actual_registered_metric_lie_block_is_W_h']=zero(Bg.extract(elm,[0,1,2])-B)
    checks['swapped_metric_block_rejected']=not zero(B-h*W)
    b=sp.Matrix([1+(x+1/x)/7,2+(x-1/x)/(11*I),3+(x*x+x**-2)/13])
    bt=sp.Matrix([Q(1,17)+(x-1/x)/(19*I),Q(2,23)+(x+1/x)/29,Q(3,31)+(x*x-x**-2)/(37*I)])
    d=M.inv()*mm(K*R*b);s=em(K*(d-R*b));vel=pm(s)
    checks['matrix_weighted_mean_slope_zero']=zero(mm(s))
    checks['full_gauge_corrected_modulus_rates_constant']=zero(b+B*s-W*d)
    checks['periodic_primitive_derivative']=zero(dm(vel)-s) and zero(mm(vel))
    checks['omitted_modulus_constants_rejected']=not zero(mm(-K*R*b))
    checks['unweighted_modulus_mean_rejected']=not zero(mm(K*(R*mm(b)-R*b)))
    dt=em(M.inv()*(mm(Kt*R*b+K*R*bt)-mm(Kt)*d))
    dt_direct=em(M.inv()*mm(K*(ht*s+R*bt)))
    st=em(Kt*(d-R*b)+K*(dt-R*bt))
    checks['moving_matrix_mean_and_inverse_drift']=zero(dt-dt_direct)
    checks['full_differentiated_gauge_equation']=zero(ht*s+h*st+R*bt-dt) and zero(mm(st))
    checks['omitted_coefficient_drift_rejected']=not zero(ht*s)
    checks['gauge_energy_cancellation']=mean((s.T*h*s+s.T*R*b)[0])==0
    checks['gauge_rate_energy_cancellation']=mean((st.T*h*st+st.T*(ht*s+R*bt))[0])==0
    harmonic=sp.Matrix([Q(1,7),-Q(1,11),Q(1,13)])
    harmonic_rate=sp.Matrix([Q(1,17),Q(2,19),-Q(1,23)])
    checks['arbitrary_harmonic_values_and_rates_in_kernel']=zero(dm(harmonic)) and zero(dm(harmonic_rate)) and zero(dm(B*dm(harmonic)))
    checks['transverse_harmonics_act_trivially_on_planar_fields']=all(v==0 for j in (0,1) for v in old.lie_fields(q,dz,[int(k==j) for k in range(3)],[0]*3))
    checks['longitudinal_harmonic_is_retained_translation']=all(expand(a-b)==0 for a,b in zip(old.lie_fields(q,dz,[0,0,1],[0]*3),dz)) and any(v!=0 for v in dz)
    # Original gauge inverse is recovered exactly, with variable diagonal coefficients.
    kd=[2+(x+1/x)/20,3+(x-1/x)/(40*I),Q(16,25)]
    diagonal=sp.diag(*kd);Md=mm(diagonal)
    sd=em(diagonal*(Md.inv()*mm(diagonal*R*b)-R*b))
    mean_cb=lambda fun:mean(fun(x))
    def primitive_cb(fun):
        p=P(fun(x));return lambda z:p.subs(x,z)
    older=old.solve([lambda z,i=i:b[i].subs(x,z) for i in range(3)],lambda z:1/kd[0].subs(x,z),lambda z:1/kd[1].subs(x,z),Q(5,4),mean_cb,primitive_cb,list(harmonic))
    checks['registered_diagonal_solve_recovered']=all(expand(older['coordinate_gradient'][i](x)-sd[i])==0 for i in range(3))
    # Complete canonical spatial momentum map, with no specialized trace ansatz.
    p=[Q(i+1,41)+(x+1/x)/(43+i)+(x-1/x)/((47+i)*I) for i in range(14)];p[13]=0
    j=sp.Matrix([0,0,sum(p[i]*dz[i] for i in range(14) if i not in elm)])
    ell=-q[8]*sp.Matrix(p[6:9])
    full_free_flux=Bg.T*sp.Matrix([0 if i in elm else p[i] for i in range(14)])
    checks['actual_free_shift_flux_is_frame_flux']=zero(full_free_flux-ell)
    residual=-mm(j)+sp.Matrix([(x+1/x)/17,(x-1/x)/(19*I),(x*x+x**-2)/23])
    v=em(pm(j+residual)-ell);eta=sp.Matrix([Q(1,31),-Q(2,37),Q(3,41)])
    A=R*K;AM=R*M;constant=AM.inv()*(eta-mm(A*v));e=em(A*(v+constant))
    for i,index in enumerate(elm):p[index]=e[i]
    canonical=em(dm(Bg.T*sp.Matrix(p))-sp.Matrix([0,0,sum(p[i]*dz[i] for i in range(14))]))
    checks['full_canonical_constraint_inverse']=zero(canonical-residual)
    checks['three_nonzero_momentum_means_retained']=zero(mm(e)-eta)
    checks['residual_translation_compatibility_retained']=zero(mm(j+residual)) and mean(j[2])!=0
    checks['omitted_frame_flux_rejected']=not zero(dm(ell))
    checks['omitted_momentum_normalization_rejected']=not zero(mm(A*v)-eta)
    # Exact periodic adjoint of the full covector-density Ward transport.
    S=sp.Matrix([1+(x+1/x)/7,2+(x-1/x)/(11*I),3+(x*x+x**-2)/13])
    C=sp.Matrix([1+(x-1/x)/(17*I),2+(x+1/x)/19,3+(x*x-x**-2)/(23*I)])
    rho=sp.Matrix([1+(x+1/x)/29,2+(x-1/x)/(31*I),3+(x*x+x**-2)/37])
    rhot=sp.Matrix([Q(1,41),Q(1,43),Q(1,47)])
    deltaS=sp.Matrix([1+(x-1/x)/(53*I),2+(x+1/x)/59,3+(x*x-x**-2)/(61*I)])
    lie=lambda V,X:em(V[2]*dm(X)+D(V[2])*X+sp.Matrix([0,0,(X.T*dm(V))[0]]))
    adjoint=em(rhot-S[2]*dm(rho)+rho[2]*dm(S))
    checks['full_weak_Ward_pairing']=mean((rhot.T*C+rho.T*lie(S,C)-adjoint.T*C)[0])==0
    finite_source=mean((rho.T*lie(deltaS,C))[0])
    checks['finite_background_Ward_residual_rejected_if_omitted']=finite_source!=0
    checks['omitted_covector_density_index_term_rejected']=mean((rho[2]*(C.T*dm(S))[0]))!=0
    return checks

def calculate():
    parent=read(PARENT);pins=dict(parent['source_pins'])
    extras=[CONTRACT,CORRECTION,PREP,LIE,COEFF,PARENT,Path(__file__).relative_to(ROOT).as_posix(),
      GATE+'RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_REPORT_2026-11-01.md',
      GATE+'RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md',
      GATE+'RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md',
      GATE+'RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_REPORT_2026-11-01.md']
    for rel in extras:
        h=digest(ROOT/rel);assert rel not in pins or pins[rel]==h,rel;pins[rel]=h
    snap={}
    for rel,h in pins.items():
        path=ROOT/rel;assert digest(path)==h,rel
        side=Path(str(path)+'.sha256')
        if rel.endswith('.sha256'):
            snap[path]=(digest(path),path.stat().st_mtime_ns)
        else:
            assert side.read_text(encoding='utf-8').split()[0].lower()==h,rel
            for f in (path,side):snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks'])
    checks=exact_controls()
    mp.mp.dps=80;mp.iv.dps=60;iv=mp.iv
    upper=lambda a:mp.mpf(iv.mpf(a)._mpi_[1]);lower=lambda a:mp.mpf(iv.mpf(a)._mpi_[0])
    decode=lambda a:iv.mpf([mp.mpf(tuple(t)) for t in a])
    H=decode(read(COEFF)['H_interval']);r=iv.mpf(1)/13000
    hmin=iv.exp(-2*r);hmax=iv.exp(2*r)
    hz=2*r*iv.exp(4*r);w=2*iv.pi/31000*iv.exp(2*r)
    ht=2*iv.exp(2*r)*(max(abs(lower(H)),abs(upper(H)))+iv.mpf(1)/31000+r*w)
    checks['actual_initial_metric_in_conditional_geometric_envelope']=lower(hmin)>mp.mpf('.5') and upper(hmax)<2 and upper(hz)<mp.mpf('.1') and upper(ht)<2
    k,K,L,T=sp.Rational(1,2),sp.Integer(2),sp.Rational(1,10),sp.Integer(2)
    bounds={'gauge_H1_per_Rb':2*sp.sqrt(2),'FP_H2_per_Rg':2*sp.sqrt(sp.Rational(111,25)),
      'gauge_rate_H1_per_Rbt':2*sp.sqrt(2),'gauge_rate_H1_per_Rb':8*sp.sqrt(2),
      'momentum_L2_per_mean':1+2*K/k,'momentum_L2_per_v':1/k,
      'momentum_D_per_source':1/k,'momentum_D_per_momentum':2*L/k,
      'green_inverse_radius':sp.Rational(50,797),'green_inverse_bound':sp.Rational(797,50),
      'green_drift_factor':sp.Rational(797,50)**2}
    checks['Neumann_half_gap_exact']=sp.Rational(797,100)*bounds['green_inverse_radius']==sp.Rational(1,2)
    checks['Green_bound_keeps_mean_mode']=sp.Rational(797,100)/(1-sp.Rational(1,2))==bounds['green_inverse_bound']
    checks['source_bytes_and_sidecar_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items())
    return {'kind':'RTAU_GENERAL_PLANAR_GAUGE_DOMAIN_V2','source_pins':pins,'pinned_files':len(pins),
      'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
      'bounds_exact':{n:str(v) for n,v in bounds.items()},
      'initial_envelope_bounds_binary':{n:[list(t) for t in a._mpi_] for n,a in {'metric_lower':hmin,'metric_upper':hmax,'metric_spatial_upper':hz,'metric_time_upper':ht}.items()},
      'harmonic_history':'REMAINS_EXTERNAL_COORDINATE_CONTROL_NOT_AN_ACTION_RATE_LAW',
      'scope':'CONDITIONAL_GENERAL_PLANAR_GAUGE_AND_MOMENTUM_DOMAIN_COMPONENT',
      'actual_background_time_tube':'OPEN','coupled_current_operator_tube':'OPEN','energy_continuation':'OPEN',
      'Rtau_adopted':False,'matching_inputs_identified':False,'review_status':'DEFERRED','Rule9_cleared':False,
      'physics_pass':False,'gate_effect':'NONE'}

def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=False)
    try:
        d=calculate();raw=enc(d)
        if a.replay:assert a.replay.read_bytes()==raw,'Replay byte mismatch'
        else:
            a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_bytes((hashlib.sha256(raw).hexdigest()+'  '+a.output.resolve().relative_to(ROOT).as_posix()+'\n').encode())
        failures=[c['name'] for c in d['checks'] if not c['passed']]
        print(json.dumps({'passed':len(d['checks'])-len(failures),'total':len(d['checks']),'failures':failures,'pins':d['pinned_files'],'physics_pass':False,'replay':bool(a.replay)}))
        if failures:raise SystemExit(1)
    except Exception:
        if a.output:(a.output.parent/'failure.json').write_bytes(enc({'error':traceback.format_exc(),'physics_pass':False,'gate_effect':'NONE'}))
        raise
if __name__=='__main__':main()
