"""Full-action planar current coefficients and weighted coupled trace map."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,traceback
import sympy as sp
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];GATE='Theory/Gates/RES-001/'
PARENT='Analysis/MasterTests/outputs/rtau_planar_gauge_domain_audit_v1_20261119/receipt.json'
CONTRACT=GATE+'RES001_RTAU_PLANAR_CURRENT_OPERATOR_V1_CONTRACT_2026-11-19.md'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
LIE='Analysis/MasterTests/r4c1_gauge_velocity_v1.py'
CORRECTION=GATE+'RES001_RTAU_PLANAR_CURRENT_OPERATOR_V2_SPEC_2026-11-19.md'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(d):return (json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def exact_controls():
    x=sp.symbols('x',nonzero=True);I=sp.I;Q=sp.Rational
    E=lambda a:sp.expand(sp.cancel(a));D=lambda a:E(I*x*sp.diff(a,x))
    def terms(a):return [(int(v.as_powers_dict().get(x,0)),v) for v in sp.Add.make_args(E(a))]
    mean=lambda a:E(sum(v for n,v in terms(a) if n==0))
    P=lambda a:E(sum(v/(I*n) for n,v in terms(a) if n))
    em=lambda a:a.applyfunc(E);mm=lambda a:a.applyfunc(mean);pm=lambda a:a.applyfunc(P);dm=lambda a:a.applyfunc(D)
    zero=lambda a:all(E(v)==0 for v in a);checks={}
    f0=(x+1/x)/20;G=sp.Matrix([[2,2*f0],[2*f0,3+2*f0*f0]])
    Gi=sp.Matrix([[Q(1,2)+f0*f0/3,-f0/3],[-f0/3,Q(1,3)]])
    c=Q(3,2);m=sp.Matrix([Q(1,7),-Q(1,9)])
    h=(G+m*m.T/c).row_join(m).col_join(m.T.row_join(sp.Matrix([[c]])))
    K=Gi.row_join(-Gi*m/c).col_join((-m.T*Gi/c).row_join(sp.Matrix([[1/c+(m.T*Gi*m)[0]/c**2]])))
    K=em(K);R=sp.diag(1,1,Q(1,2));W=sp.diag(1,1,2);B=W*h;A=R*K
    w=1+(x+1/x)/100;weights=sp.diag(w,w,w*w);N=mm(weights*A)
    checks['weighted_mean_matrix_nonsingular']=N.det()!=0
    scalar=(x+1/x)/7+(x*x-x**-2)/(11*I)
    pT=sp.Matrix([1+(x-1/x)/(13*I),2+(x+1/x)/17,3+(x*x+x**-2)/19])
    embed=sp.Matrix([G[0,0],G[0,1],G[1,1]])
    t=E((pT.T*embed)[0]);u=E((pT.T*dm(embed))[0]);s=E(u-D(t))
    background_e=sp.Matrix([1+(x+1/x)/23,2+(x-1/x)/(29*I),3+(x*x+x**-2)/31])
    Qmetric=G.row_join(sp.zeros(2,1)).col_join(sp.zeros(1,3))
    kvec=em(Qmetric*W*background_e);ez=sp.Matrix([0,0,1])
    projected=lambda v:em(A*(v-N.inv()*mm(weights*A*v)))
    delta_j=ez*E(t*D(scalar)+u*scalar)
    rho=w
    direct=projected(pm(delta_j)-ez*P(rho)*mean(delta_j[2])-kvec*scalar)
    U=em(ez*t-kvec)
    bounded=projected(U*scalar+ez*(P(s*scalar)-P(rho)*mean(s*scalar)))
    checks['full_weighted_momentum_trace_map']=zero(direct-bounded)
    checks['transported_momentum_means_retained']=zero(mm(weights*direct))
    checks['ordinary_mean_is_a_different_coordinate']=not zero(mm(direct))
    checks['full_linearized_constraint_with_range']=zero(dm(B.T*direct+kvec*scalar)-delta_j+rho*mm(delta_j))
    checks['global_translation_range_not_projected_away']=not zero(mm(delta_j))
    checks['primitive_to_zero_order_identity']=E(P(t*D(scalar)+u*scalar)-(t*scalar-mean(t*scalar)+P(s*scalar)))==0
    checks['primitive_feedback_not_omitted']=not zero(projected(ez*P(s*scalar)))
    natural=projected(pm(delta_j)-kvec*scalar)
    checks['transported_residual_profile_mean_is_one']=mean(rho)==1
    checks['omitted_transported_projector_rank_term_rejected']=not zero(natural-direct)
    checks['range_rank_correction_has_exact_sign']=zero(direct-natural+projected(ez*P(rho))*mean(delta_j[2]))
    checks['weighted_normalizer_annihilates_constant_input']=zero(projected(sp.Matrix([1,2,3])))
    # The geometric principal coefficient comes from the actual full metric flux.
    metric=[h[0,0],h[0,1],h[0,2],h[1,1],h[1,2],h[2,2]]
    dh=dm(h);zeroM=sp.zeros(3);Gamma=[]
    for k in range(3):
        Gamma.append(sp.Matrix(3,3,lambda i,j:sp.Rational(1,2)*sum(K[k,l]*((dh[l,j] if i==2 else 0)+(dh[l,i] if j==2 else 0)-(dh[i,j] if l==2 else 0)) for l in range(3))))
    flux_over_vol=sum(K[i,j]*Gamma[2][i,j] for i in range(3) for j in range(3))-sum(K[i,2]*Gamma[j][i,j] for i in range(3) for j in range(3))
    curvature_tensor=K[2,2]*K-K[:,2]*K[2,:]
    checks['independent_full_curvature_flux_contraction']=E(flux_over_vol+sum(curvature_tensor[i,j]*dh[i,j] for i in range(3) for j in range(3)))==0
    contraction=E(sum(curvature_tensor[i,j]*Qmetric[i,j] for i in range(3) for j in range(3)))
    checks['general_Schur_trace_principal_coefficient']=E(contraction-(2/c+(m.T*Gi*m)[0]/c**2))==0
    checks['mixed_modulus_principal_correction_retained']=E(contraction-2/c)!=0
    # Noncommuting moving weighted normalization: retain both weight and metric drift.
    At=dm(A)/17;Wt=sp.diag((x-1/x)/(37*I),(x-1/x)/(37*I),2*w*(x-1/x)/(37*I))
    vt=sp.Matrix([1+(x+1/x)/41,2+(x-1/x)/(43*I),3+(x*x+x**-2)/47])
    v=U*scalar+ez*(P(s*scalar)-P(rho)*mean(s*scalar));eta=sp.Matrix([Q(1,53),-Q(2,59),Q(3,61)]);etat=sp.Matrix([Q(1,67),Q(2,71),-Q(1,73)])
    kk=N.inv()*(eta-mm(weights*A*v));ee=em(A*(v+kk));Nt=mm(Wt*A+weights*At)
    kt=N.inv()*(etat-mm((Wt*A+weights*At)*(v+kk)+weights*A*vt))
    et=em(At*(v+kk)+A*(vt+kt))
    checks['moving_weighted_canonical_mean_identity']=zero(mm(Wt*ee+weights*et)-etat)
    checks['omitted_weight_drift_rejected']=not zero(mm(Wt*ee))
    checks['normalizer_inverse_time_order']=zero(N*(-N.inv()*Nt*N.inv())+Nt*N.inv())
    return checks

def canonical_coefficients(env,y,L):
    """Coefficients of delta I at fixed canonical q,p, from the full action."""
    J,D=env['J'],env['D'];grad=env['gradient'];q=y[:14];d=y[28:42];v=y[14:28];S=y[42:45];Sz=y[45:48]
    momenta=[grad(L,14+i) for i in range(14)]
    qq=[D.var(t,i) for i,t in enumerate(q)];dd=[D.var(t,14+i) for i,t in enumerate(d)]
    pp=[D.var(t,28+i) for i,t in enumerate(momenta)]
    n,vol,gamma,hinv,flux=env['geometry'](qq,dd)
    F=n*gamma*sum((hinv[i][2]*pp[6+i] for i in range(3)),D(J(0)))-n*flux/2-env['b']*n*vol*qq[13]*hinv[2][2]*dd[12]
    fg=lambda k:F.g.get(k,J(0))
    lie=env['lie'];rv=[a-b for a,b in zip(v,lie(q,d,S,Sz))]
    C0=[];C1=[];C2=[];D0=[];D1=[]
    for i in range(14):
        basis=[J(int(i==k)) for k in range(14)];T=lie(basis,[J(0)]*14,S,Sz)
        C0.append(grad(L,i).c[0]+sum(momenta[k].c[0]*T[k].c[0] for k in range(14))-fg(i).c[1])
        C1.append(grad(L,28+i).c[0]+S[2].c[0]*momenta[i].c[0]-fg(i).c[0]-fg(14+i).c[1])
        C2.append(-fg(14+i).c[0]);D0.append(-rv[i].c[0]-fg(28+i).c[1]);D1.append(-fg(28+i).c[0])
    return dict(C0=C0,C1=C1,C2=C2,D0=D0,D1=D1,F=F,momenta=momenta,normal_rates=rv)

def action_controls():
    mp.mp.dps=90;mp.iv.dps=55;iv=mp.iv;checks={}
    lo=lambda a:mp.mpf(iv.mpf(a)._mpi_[0]);hi=lambda a:mp.mpf(iv.mpf(a)._mpi_[1]);ab=lambda a:max(abs(lo(a)),abs(hi(a)))
    factory=load('general_current_action',FACTORY);env=factory.prepare();J=env['J'];D=env['D'];grad=env['gradient'];hj=env['hj'];evalL=env['evaluate']
    y,_=env['state'](J.variable(iv.mpf('0.3')),False)
    entries=[iv.mpf(6)/5,iv.mpf(1)/23,iv.mpf(1)/31,iv.mpf(7)/6,-iv.mpf(1)/37,iv.mpf(5)/4]
    for i,val in enumerate(entries):y[i]=J(val);y[28+i]=J(0)
    L=evalL(y);LR=evalL(y,True);q=y[:14];d=y[28:42];S=y[42:45];Sz=y[45:48]
    cc=canonical_coefficients(env,y,L);pi=cc['momenta'];n,vol,gamma,K,flux=env['geometry'](q,d)
    PNcan=gamma*sum((K[i][2]*pi[6+i] for i in range(3)),J(0))-flux/2-env['b']*vol*q[13]*K[2][2]*d[12]
    tol=mp.mpf('1e-28');checks['full_raw_action_lapse_flux_at_nonconformal_metric']=max(ab((grad(LR,49)-PNcan).c[k]) for k in (0,1))<tol
    M=[[hj(L,14+i,14+k).c[0] for k in range(13)] for i in range(13)]
    Minv=mp.inverse(mp.matrix([[(lo(a)+hi(a))/2 for a in row] for row in M]))
    pre=[[iv.mpf(mp.nstr(Minv[i,k],85)) for k in range(13)] for i in range(13)]
    gap=max(sum(ab(iv.mpf(int(i==j))-sum((pre[i][k]*M[k][j] for k in range(13)),iv.mpf(0))) for j in range(13)) for i in range(13))
    assert gap<mp.mpf('.5');bound=iv.mpf(max(sum(ab(a) for a in row) for row in pre))/(1-iv.mpf(gap))
    checks['new_full_action_temporal_inverse_validated']=gap<mp.mpf('.5')
    def solve(rhs):
        sol=mp.lu_solve(mp.matrix([[(lo(a)+hi(a))/2 for a in row] for row in M]),mp.matrix([(lo(a)+hi(a))/2 for a in rhs]))
        candidate=[iv.mpf(mp.nstr(a,85)) for a in sol]
        error=bound*iv.mpf(max(ab(rhs[i]-sum((M[i][k]*candidate[k] for k in range(13)),iv.mpf(0))) for i in range(13)))
        e=hi(error);return [iv.mpf([lo(a)-e,hi(a)+e]) for a in candidate]
    mm=[[q[0].c[0],q[1].c[0],q[2].c[0]],[q[1].c[0],q[3].c[0],q[4].c[0]],[q[2].c[0],q[4].c[0],q[5].c[0]]]
    c=mm[2][2];m=[mm[0][2],mm[1][2]];G=[[mm[i][j]-m[i]*m[j]/c for j in range(2)] for i in range(2)]
    trace=[G[0][0],G[0][1],iv.mpf(0),G[1][1],iv.mpf(0),iv.mpf(0)]+[iv.mpf(0)]*8
    rho2=sum(K[i][j].c[0]*m[i]*m[j] for i in range(2) for j in range(2))
    expected=-n.c[0]*vol.c[0]*(2/c+rho2/c**2)/2
    direct_a2=sum((cc['C2'][i]*trace[i] for i in range(14)),iv.mpf(0))
    checks['actual_action_general_trace_principal_coefficient']=ab(direct_a2-expected)<tol
    checks['eliminated_metric_momenta_have_no_derivative_in_density']=all(ab(cc['D1'][i])==0 for i in (2,4,5))
    checks['all_three_frame_momentum_derivatives_retained']=all(ab(cc['D1'][6+i]+(n*gamma*K[i][2]).c[0])<tol for i in range(3)) and all(ab(cc['D1'][6+i])>0 for i in range(3))
    errors=[]
    for label in ('trace_second','all_canonical_slots'):
        if label=='trace_second':dq=[J(coefficients=[iv.mpf(0),iv.mpf(0),a/2]) for a in trace];dp=[J(0) for _ in range(14)]
        else:
            dq=[J(coefficients=[iv.mpf(i+1)/101,-iv.mpf(i+2)/103,iv.mpf(i+3)/214]) for i in range(14)]
            dp=[J(coefficients=[iv.mpf(i+1)/109,-iv.mpf(i+2)/113,iv.mpf(0)]) for i in range(13)]+[J(0)]
        dd=[J(coefficients=[a.c[1],2*a.c[2],iv.mpf(0)]) for a in dq]
        rhs=[dp[i]-sum((hj(L,14+i,k)*dq[k]+hj(L,14+i,28+k)*dd[k] for k in range(14)),J(0)) for i in range(13)]
        v0=solve([a.c[0] for a in rhs]);v1=solve([rhs[i].c[1]-sum((hj(L,14+i,14+k).c[1]*v0[k] for k in range(13)),iv.mpf(0)) for i in range(13)])
        dv=[J(coefficients=[a,b,iv.mpf(0)]) for a,b in zip(v0,v1)]+[J(0)];dy=dq+dv+dd+[J(0)]*6
        dpc=[sum((hj(L,14+i,k)*dy[k] for k in range(48)),J(0)) for i in range(14)]
        checks['canonical_inverse_'+label]=max(ab((dpc[i]-dp[i]).c[k]) for i in range(14) for k in (0,1))<tol
        dn=-env['beta']*n*dq[12];dnz=-env['beta']*(n*dd[12]+(-env['beta']*n*d[12])*dq[12])
        draw=dy+[dn,dnz];dF=dn*grad(LR,49)+n*sum((hj(LR,49,k)*draw[k] for k in range(50)),J(0))
        dl=env['lie'](dq,dd,S,Sz)
        dihat=sum((grad(L,k)*dy[k] for k in range(48)),J(0))-sum((dpc[i]*cc['normal_rates'][i]+pi[i]*(dv[i]-dl[i]) for i in range(14)),J(0))
        raw=dihat.c[0]-dF.c[1]
        assembled=sum((cc['C0'][i]*dq[i].c[0]+cc['C1'][i]*dq[i].c[1]+cc['C2'][i]*2*dq[i].c[2]+cc['D0'][i]*dp[i].c[0]+cc['D1'][i]*dp[i].c[1] for i in range(14)),iv.mpf(0))
        error=ab(raw-assembled);errors.append(error);checks['full_raw_density_operator_'+label]=error<tol
        if label=='trace_second':checks['raw_second_trace_matches_closed_principal']=ab(raw-expected)<tol
    return checks,{'raw_action_metric_entries':[mp.nstr(a,25) for a in entries],
       'inverse_contraction_upper':mp.nstr(gap,30),'maximum_density_identity_defect':mp.nstr(max(errors),30),
       'trace_principal_interval':[[list(t) for t in iv.mpf(expected)._mpi_]],
       'scope':'LOCAL_OFF_SHELL_FULL_ACTION_CONTROL_NOT_BACKGROUND_ADMISSION'}

def calculate():
    parent=json.loads((ROOT/PARENT).read_text(encoding='utf-8'));pins=dict(parent['source_pins'])
    for rel in (PARENT,CONTRACT,CORRECTION,FACTORY,LIE,
      'Analysis/MasterTests/test_rtau_planar_current_operator_v1.py',
      'Analysis/MasterTests/audit_rtau_planar_current_operator_v1.py',
      'Analysis/MasterTests/outputs/rtau_planar_current_operator_v1_20261119/receipt.json',
      'Analysis/MasterTests/outputs/rtau_planar_current_operator_audit_v1_20261119/receipt.json',
      GATE+'RES001_RTAU_PLANAR_CURRENT_OPERATOR_V1_REPORT_2026-11-19.md',Path(__file__).relative_to(ROOT).as_posix(),GATE+'RES001_RTAU_PLANAR_GAUGE_DOMAIN_V3_REPORT_2026-11-19.md'):
        value=digest(ROOT/rel);assert rel not in pins or pins[rel]==value,rel;pins[rel]=value
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel;side=Path(str(p)+'.sha256')
        if not rel.endswith('.sha256'):assert side.read_text(encoding='utf-8').split()[0].lower()==h,rel
        for f in (p,side) if side.exists() else (p,):snap[f]=(digest(f),f.stat().st_mtime_ns)
    checks=exact_controls();more,records=action_controls();checks.update(more)
    iv=mp.iv;r=iv.mpf(1)/13000;upper=lambda a:mp.mpf(iv.mpf(a)._mpi_[1])
    green=iv.mpf(797)/100*(iv.exp(4*r)+r*iv.exp(8*r)/2)
    eps=iv.exp(4*r)-1;q=8*eps
    checks['initial_chart_transport_Green_bound_less_than_8']=upper(green)<8
    checks['initial_weighted_normalization_has_positive_margin']=upper(q)<1
    checks['conditional_adapted_Green_half_gap']=sp.Rational(8,16)==sp.Rational(1,2)
    checks['all_source_bytes_sidecar_mtimes_preserved']=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items())
    return {'kind':'RTAU_PLANAR_CURRENT_OPERATOR_V2','source_pins':pins,'pinned_files':len(pins),
       'checks':[{'name':n,'passed':bool(v)} for n,v in checks.items()],'action_control':records,
       'bounds_binary':{k:[list(t) for t in v._mpi_] for k,v in {'initial_adapted_Green_upper':green,'weight_deviation_upper':eps,'weighted_mean_contraction_upper':q}.items()},
       'adapted_Green_bound':8,'conditional_operator_radius':'1/16','conditional_Green_bound':16,'conditional_Green_drift_factor':256,
       'transported_range_profile':'rho=1/J; mean_new(rho)=1; residual=-rho*mean(delta_j)',
       'scope':'FULL_ACTION_LOCAL_COEFFICIENTS_WEIGHTED_MEANS_AND_TRANSPORTED_RANGE_TRACE_OPERATOR',
       'actual_operator_time_tube':'OPEN','actual_background_persistence':'OPEN','energy_continuation':'OPEN',
       'review_status':'DEFERRED','Rule9_cleared':False,'Rtau_adopted':False,'physics_pass':False,'gate_effect':'NONE'}

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
