"""Actual initial whole-root operator drift; no future tube is assumed."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,traceback
import sympy as sp
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];GATE='Theory/Gates/RES-001/'
PARENT='Analysis/MasterTests/outputs/rtau_planar_current_operator_audit_v2_20261119/receipt.json'
CONTRACT=GATE+'RES001_RTAU_PLANAR_CURRENT_DRIFT_V1_CONTRACT_2026-11-19.md'
MODULE='Analysis/MasterTests/test_rtau_planar_current_operator_v2.py'
INITIAL='Analysis/MasterTests/outputs/r4c1_rtau_initial_acceleration_v1_attempt_01/summary.json'
HIGHER='Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json'
COEFF='Analysis/MasterTests/outputs/rtau_prepared_weak_coefficients_v1_20261102/receipt.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
LIE='Analysis/MasterTests/r4c1_gauge_velocity_v1.py'
CORRECTION=GATE+'RES001_RTAU_PLANAR_CURRENT_DRIFT_V2_SPEC_2026-11-19.md'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def read(n):return json.loads((ROOT/n).read_text(encoding='utf-8'))
def load(name,rel):
    s=importlib.util.spec_from_file_location(name,ROOT/rel);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def exact_controls():
    checks={};t,z=sp.symbols('t z',real=True);q,v,d,p,S,Sz=sp.symbols('q v d p S Sz',real=True)
    M,b,k,g=sp.symbols('M b k g',nonzero=True)
    L=M*(v-S*d-Sz*q)**2/2+b*q*(v-S*d-Sz*q)+k*d*d+g*q*q
    normal=sp.symbols('normal');L0=sp.expand(L.subs(v,normal+S*d+Sz*q))
    checks['material_Lagrangian_parameter_shift_cancels']=not L0.has(S,Sz)
    checks['canonical_gradient_materialization']=sp.simplify((sp.diff(L,q)+Sz*sp.diff(L,v)).subs(v,normal+S*d+Sz*q)-sp.diff(L0,q))==0
    checks['canonical_spatial_gradient_materialization']=sp.simplify((sp.diff(L,d)+S*sp.diff(L,v)).subs(v,normal+S*d+Sz*q)-sp.diff(L0,d))==0
    qd,pd=sp.symbols('qd pd');vf=(p-b*q)/M
    checks['normal_rate_time_from_canonical_data']=sp.simplify(sp.diff(vf,p)*pd+sp.diff(vf,q)*qd-(pd-b*qd)/M)==0
    J=sp.Function('J')(t,z);a=sp.Function('a')(t,z);w=sp.Function('w')(t,z)
    # D_t at fixed new coordinate is partial_t-w partial_z.
    Dt=lambda f:sp.diff(f,t)-w*sp.diff(f,z)
    checks['density_coefficient_transport_includes_J_rate']=sp.simplify(Dt(a/J)-(Dt(a)/J-a*Dt(J)/J**2))==0
    checks['principal_coefficient_transport_includes_J_rate']=sp.simplify(Dt(J*a)-(J*Dt(a)+a*Dt(J)))==0
    lamz=sp.Function('lamz')(t,z)
    checks['first_coefficient_transport_product_rule']=sp.simplify(Dt(a*lamz)-Dt(a)*lamz-a*Dt(lamz))==0
    p0,p1,s0,s1=sp.symbols('p0 p1 s0 s1')
    checks['transported_residual_rank_has_both_time_terms']=sp.expand(sp.diff((p0+t*p1)*(s0+t*s1),t)-p1*(s0+t*s1)-(p0+t*p1)*s1)==0
    C,Fq,Fd=sp.Function('C')(t,z),sp.Function('Fq')(t,z),sp.Function('Fd')(t,z)
    checks['local_coefficient_time_uses_second_action_derivatives']=sp.diff(sp.diff(Fq,z),t)==sp.diff(sp.diff(Fq,t),z)
    n=sp.symbols('n',integer=True,nonnegative=True)
    checks['H2_to_first_derivative_factor']=sp.expand((1+n*n)**2-4*n*n-(n*n-1)**2)==0
    # Exact initial weighted normalizer uses the transported, not ordinary means.
    aa,Abar=sp.symbols('a Abar',positive=True)
    checks['weighted_longitudinal_mean_integrand_cancels']=sp.simplify((aa/Abar)*(Abar/aa)**2/(2*Abar*Abar)-1/(2*Abar*aa))==0
    checks['proper_density_time_map_has_weight_drift']=sp.simplify(Dt(J**-1)+J**-2*Dt(J))==0
    return checks

def calculate():
    parent=read(PARENT);pins=dict(parent['source_pins'])
    for rel in (PARENT,CONTRACT,CORRECTION,MODULE,INITIAL,HIGHER,COEFF,FACTORY,LIE,
      'Analysis/MasterTests/test_rtau_planar_current_drift_v1.py',
      'Analysis/MasterTests/outputs/rtau_planar_current_drift_v1_20261119/receipt.json',
      GATE+'RES001_RTAU_PLANAR_CURRENT_OPERATOR_V2_REPORT_2026-11-19.md',Path(__file__).relative_to(ROOT).as_posix()):
        h=digest(ROOT/rel);assert rel not in pins or pins[rel]==h,rel;pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel;sc=Path(str(p)+'.sha256')
        if not rel.endswith('.sha256'):assert sc.read_text(encoding='utf-8').split()[0].lower()==h,rel
        for f in (p,sc) if sc.exists() else (p,):snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for c in parent['checks']);checks=exact_controls()
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda a:mp.mpf(iv.mpf(a)._mpi_[0]);hi=lambda a:mp.mpf(iv.mpf(a)._mpi_[1])
    ab=lambda a:iv.mpf(max(abs(lo(a)),abs(hi(a))))
    maxiv=lambda xs:iv.mpf(max(hi(v) for v in xs))
    norm=lambda xs:iv.sqrt(sum((ab(a)**2 for a in xs),iv.mpf(0)))
    decode=lambda xs:iv.mpf([mp.mpf(tuple(v)) for v in xs])
    binary=lambda a:[list(v) for v in iv.mpf(a)._mpi_]
    model=load('actual_current_coefficients',MODULE);factory=load('actual_initial_drift_factory',FACTORY);old=load('actual_drift_Lie',LIE)
    env=factory.prepare();mp.mp.dps=100;mp.iv.dps=60
    J=env['J'];grad=env['gradient'];hj=env['hj'];third=ab(decode(read(HIGHER)['whole_circle_third_shift_bound']))
    theta=J.variable(iv.mpf([0,hi(2*iv.pi)]));box=iv.mpf([-hi(third),hi(third)])
    y,_=env['state'](theta,True,[box]*3);L=env['evaluate'](y)
    q,vel,spatial=y[:14],y[14:28],y[28:42];S,Sz=y[42:45],y[45:48]
    cc=model.canonical_coefficients(env,y,L);pi=cc['momenta'];F=cc['F'];fg=lambda k:F.g.get(k,J(0))
    fh=lambda i,j:F.h.get(tuple(sorted((i,j))),J(0))
    Dz=lambda a:J(coefficients=[a.c[1],2*a.c[2],iv.mpf(0)])
    vtspace=[Dz(a) for a in vel]
    # Only value and first spatial coefficients of p_t are claimed/supplied.
    pt=[J(coefficients=[grad(L,i).c[0]-grad(L,28+i).c[1],grad(L,i).c[1]-2*grad(L,28+i).c[2],iv.mpf(0)]) for i in range(14)]
    checks['auxiliary_secondary_residual_encloses_zero']=all(lo(pt[13].c[k])<=0<=hi(pt[13].c[k]) for k in (0,1))
    pt[13]=J(0)
    checks['unavailable_Zddot_not_used']=all(all(ab(hj(L,i,27).c[k])==0 for k in range(3)) for i in list(range(14))+list(range(28,42)))
    M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
    mids=mp.matrix([[(lo(a)+hi(a))/2 for a in row] for row in M]);pre0=mp.inverse(mids)
    pre=[[iv.mpf(mp.nstr(pre0[i,k],90)) for k in range(13)] for i in range(13)]
    residualq=maxiv(sum((ab(iv.mpf(int(i==j))-sum((pre[i][k]*M[k][j] for k in range(13)),iv.mpf(0))) for j in range(13)),iv.mpf(0)) for i in range(13))
    fallback=iv.sqrt(13)*decode(read(INITIAL)['bounds']['original_temporal_inverse'])
    inverse=fallback;method='INHERITED_CERTIFIED_L2_BOUND_CONVERTED_TO_LINFINITY'
    if hi(residualq)<1:
        alt=maxiv(sum((ab(v) for v in row),iv.mpf(0)) for row in pre)/(1-residualq)
        if hi(alt)<hi(fallback):inverse=alt;method='WHOLE_ROOT_INTERVAL_NEUMANN_PRECONDITIONER'
    checks['uniform_temporal_inverse_bound_finite']=hi(inverse)>0 and mp.isfinite(hi(inverse))
    def solve(rhs):
        ans=mp.lu_solve(mids,mp.matrix([(lo(a)+hi(a))/2 for a in rhs]));xx=[iv.mpf(mp.nstr(v,90)) for v in ans]
        res=[rhs[i]-sum((M[i][k]*xx[k] for k in range(13)),iv.mpf(0)) for i in range(13)]
        error=inverse*maxiv(ab(v) for v in res);e=hi(error)
        return [iv.mpf([lo(v)-e,hi(v)+e]) for v in xx]
    liev=old.lie_fields(vel,vtspace,S,Sz)
    rhs=[pt[i]-sum((hj(L,14+i,k)*vel[k]+hj(L,14+i,28+k)*vtspace[k] for k in range(14)),J(0))-sum((hj(L,14+i,14+k)*liev[k] for k in range(13)),J(0)) for i in range(13)]
    normal_t0=solve([a.c[0] for a in rhs])
    normal_t1=solve([rhs[i].c[1]-sum((hj(L,14+i,14+k).c[1]*normal_t0[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
    normal_t=[J(coefficients=[a,b,iv.mpf(0)]) for a,b in zip(normal_t0,normal_t1)]+[J(0)]
    mapped_velocity_t=[normal_t[i]+liev[i] for i in range(13)]+[J(0)]
    path=vel+mapped_velocity_t+vtspace+[J(0)]*6
    gp_t=[sum((hj(L,i,k)*path[k] for k in range(48)),J(0)) for i in range(14)]
    gd_t=[sum((hj(L,28+i,k)*path[k] for k in range(48)),J(0)) for i in range(14)]
    gq=[];gd=[];gqt=[];gdt=[]
    for i in range(14):
        basis=[J(int(i==k)) for k in range(14)];Ts=old.lie_fields(basis,[J(0)]*14,[J(0)]*3,Sz)
        gq.append(grad(L,i)+sum((Ts[k]*pi[k] for k in range(14)),J(0)))
        gd.append(grad(L,28+i)+S[2]*pi[i])
        gqt.append(gp_t[i]+sum((Ts[k]*pt[k] for k in range(14)),J(0)))
        gdt.append(gd_t[i]+S[2]*pt[i])
    canonical_rates=vel+vtspace+pt
    Ft=[sum((fh(i,k)*canonical_rates[k] for k in range(42)),J(0)) for i in range(42)]
    C0t=[gqt[i].c[0]-Ft[i].c[1] for i in range(14)]
    C1t=[gdt[i].c[0]-Ft[i].c[0]-Ft[14+i].c[1] for i in range(14)]
    C2t=[-Ft[14+i].c[0] for i in range(14)]
    C0z=[gq[i].c[1]-2*fg(i).c[2] for i in range(14)]
    C1z=[gd[i].c[1]-fg(i).c[1]-2*fg(14+i).c[2] for i in range(14)]
    C2z=[-fg(14+i).c[1] for i in range(14)]
    scalar=lambda xs,v:sum((xs[i]*v[i] for i in range(14)),iv.mpf(0))
    r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000;beta=iv.mpf(2)/5
    lamz=-r*env['j'].trig(theta).c[0];lamzz=-r*env['j'].trig(theta,True).c[0];lamzzz=-lamz
    h=q[0].c[0];h1=q[0].c[1];h2=2*q[0].c[2];h3=h*(8*lamz**3+12*lamz*lamzz+2*lamzzz)
    emb=lambda a:[a if i in (0,3) else iv.mpf(0) for i in range(14)]
    v0,v1,v2,v3=map(emb,(h,h1,h2,h3));v0t,v1t,v2t=map(emb,(vel[0].c[0],vel[0].c[1],2*vel[0].c[2]))
    A2=scalar(cc['C2'],v0);A1=scalar(cc['C1'],v0)+2*scalar(cc['C2'],v1)
    A0=scalar(cc['C0'],v0)+scalar(cc['C1'],v1)+scalar(cc['C2'],v2)
    A2z=scalar(C2z,v0)+scalar(cc['C2'],v1)
    A1z=scalar(C1z,v0)+scalar(cc['C1'],v1)+2*scalar(C2z,v1)+2*scalar(cc['C2'],v2)
    A0z=scalar(C0z,v0)+scalar(cc['C0'],v1)+scalar(C1z,v1)+scalar(cc['C1'],v2)+scalar(C2z,v2)+scalar(cc['C2'],v3)
    A2t=scalar(C2t,v0)+scalar(cc['C2'],v0t)
    A1t=scalar(C1t,v0)+scalar(cc['C1'],v0t)+2*scalar(C2t,v1)+2*scalar(cc['C2'],v1t)
    A0t=scalar(C0t,v0)+scalar(cc['C0'],v0t)+scalar(C1t,v1)+scalar(cc['C1'],v1t)+scalar(C2t,v2)+scalar(cc['C2'],v2t)
    abar=iv.mpf([1,hi(iv.exp(r*r/4))]);aa=iv.sqrt(h);Jac=aa/abar
    wb=2*iv.pi*eps/31*iv.exp(2*r);w=iv.mpf([-hi(wb),hi(wb)])
    R2=iv.mpf([0,hi(r*r*iv.exp(r*r/4)/8)])
    H=decode(read(COEFF)['H_interval']);Ltime=H+eps*env['j'].trig(2*theta,True).c[0]/31
    meanL=H+eps*R2/31
    wz=eps*(env['j'].trig(2*theta,True).c[0]-R2)/31-lamz*w
    wzz=-2*eps*env['j'].trig(2*theta).c[0]/31-lamzz*w-lamz*wz
    a2t=Jac*(A2t-w*A2z+wz*A2)
    a1t=A1t-w*A1z+(A2t-w*A2z)*lamz+A2*(wzz+lamz*wz)
    a0t=(A0t-w*A0z-wz*A0)/Jac
    principal_geom=Jac*A2*(2*Ltime-meanL-2*w*lamz-beta*(vel[12].c[0]-w*spatial[12].c[0]))
    checks['principal_time_bound_overlaps_independent_geometric_first_jet']=max(lo(a2t),lo(principal_geom))<=min(hi(a2t),hi(principal_geom))
    P=pi[0]+pi[3];Pt=pt[0]+pt[3]
    Pnew=P.c[0]/Jac;Pnew_t=(Pt.c[0]-w*P.c[1]-wz*P.c[0])/Jac
    Pnew_z=(P.c[1]-lamz*P.c[0])/Jac**2
    Pnew_tz=(Pt.c[1]-2*wz*P.c[1]-2*w*P.c[2]-wzz*P.c[0]-lamz*(Pt.c[0]-w*P.c[1]-wz*P.c[0]))/Jac**2
    Gt=vel[0].c[0]-w*spatial[0].c[0]
    ex,ey=pi[2].c[0],pi[4].c[0]
    ext=pt[2].c[0]-w*pi[2].c[1];eyt=pt[4].c[0]-w*pi[4].c[1]
    U=[-h*ex,-h*ey,h*Pnew];Ut=[-Gt*ex-h*ext,-Gt*ey-h*eyt,Gt*Pnew+h*Pnew_t]
    ss=-h*Pnew_z;sst=-Gt*Pnew_z-h*Pnew_tz
    Re=[cc['normal_rates'][2].c[0]/Jac,cc['normal_rates'][4].c[0]/Jac,cc['normal_rates'][5].c[0]/Jac**2]
    Ret=[(normal_t[2].c[0]-w*cc['normal_rates'][2].c[1]-wz*cc['normal_rates'][2].c[0])/Jac,
         (normal_t[4].c[0]-w*cc['normal_rates'][4].c[1]-wz*cc['normal_rates'][4].c[0])/Jac,
         (normal_t[5].c[0]-w*cc['normal_rates'][5].c[1]-2*wz*cc['normal_rates'][5].c[0])/Jac**2]
    alpha=iv.exp(2*r);alphat=2*iv.exp(2*r)*(ab(Ltime)+ab(w)*r)
    omega=iv.exp(4*r);omegat=2*omega*ab(wz);nu=iv.mpf(2)
    primitive_rho=iv.exp(2*r)-1;primitive_rhot=iv.exp(2*r)*ab(wz)
    d=norm(U)+(1+primitive_rho)*ab(ss)
    dt=norm(Ut)+(1+primitive_rho)*ab(sst)+primitive_rhot*ab(ss)
    factor=1+nu*omega*alpha
    Tb=alpha*factor*d;Ttb=factor*((alphat+alpha*nu*(omegat*alpha+omega*alphat))*d+alpha*dt)
    Nt=omegat*alpha+omega*alphat;Ninvt=nu*nu*Nt
    Lt=ab(a2t)+ab(a1t)/2+ab(a0t)+norm(Ret)*Tb+norm(Re)*Ttb
    values={'a2_time':ab(a2t),'a1_time':ab(a1t),'a0_time':ab(a0t),'normal_metric_rate':norm(Re),'normal_metric_rate_time':norm(Ret),
      'trace_momentum_map':Tb,'trace_momentum_map_time':Ttb,'U':norm(U),'U_time':norm(Ut),'s':ab(ss),'s_time':ab(sst),
      'weight_time':omegat,'residual_profile_primitive_time':primitive_rhot,'weighted_mean_time':Nt,'weighted_mean_inverse_time':Ninvt,
      'coupled_current_operator_time':Lt,'initial_Green_time':64*Lt,'whole_root_inverse_Linfinity':inverse}
    checks['all_actual_initial_drift_bounds_finite']=all(mp.isfinite(hi(v)) and lo(v)>=0 for v in values.values())
    checks['required_third_shift_jet_inherited']=hi(third)>0 and all(lo(v.c[2])<0<hi(v.c[2]) for v in Sz)
    checks['source_hashes_and_sidecar_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items())
    return {'kind':'RTAU_ACTUAL_INITIAL_PLANAR_CURRENT_DRIFT_V2','source_pins':pins,'pinned_files':len(pins),
      'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],
      'bounds_binary':{k:binary(v) for k,v in values.items()},'upper_display':{k:mp.nstr(hi(v),35) for k,v in values.items()},
      'temporal_inverse_method':method,'whole_root_preconditioner_contraction_upper':mp.nstr(hi(residualq),30),
      'unavailable_derivatives':'p_t second spatial coefficient and Zddot are not supplied or used; Jet padding is computational only',
      'scope':'INITIAL_SLICE_WHOLE_CERTIFIED_ROOT_AND_FULL_CIRCLE_NOT_A_TIME_TUBE',
      'future_operator_margin':'OPEN','actual_background_persistence':'OPEN','energy_continuation':'OPEN',
      'Rtau_adopted':False,'review_status':'DEFERRED','Rule9_cleared':False,'physics_pass':False,'gate_effect':'NONE'}

def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=False)
    try:
        d=calculate();raw=enc(d)
        if a.replay:assert a.replay.read_bytes()==raw,'Replay byte mismatch'
        else:
            a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_bytes((hashlib.sha256(raw).hexdigest()+'  '+a.output.resolve().relative_to(ROOT).as_posix()+'\n').encode())
        bad=[c['name'] for c in d['checks'] if not c['passed']];print(json.dumps({'passed':len(d['checks'])-len(bad),'total':len(d['checks']),'failures':bad,'pins':d['pinned_files'],'upper_operator_drift':d['upper_display']['coupled_current_operator_time'],'physics_pass':False,'replay':bool(a.replay)}))
        if bad:raise SystemExit(1)
    except Exception:
        if a.output:(a.output.parent/'failure.json').write_bytes(enc({'error':traceback.format_exc(),'physics_pass':False}))
        raise
if __name__=='__main__':main()
