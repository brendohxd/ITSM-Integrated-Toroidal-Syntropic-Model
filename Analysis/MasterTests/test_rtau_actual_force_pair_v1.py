"""Actual initial force-pair L2 remainders in the corrected Sigma norm."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_ACTUAL_FORCE_PAIR_V1_SPEC_2026-11-05.md'
INPUTS='Theory/Gates/RES-001/RES001_RTAU_ACTUAL_FORCE_PAIR_V1_INPUTS_2026-11-04.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
BASE='Analysis/MasterTests/outputs/'
SOURCES={
 'lift':BASE+'rtau_strong_constraint_lift_v4_20261104/receipt.json',
 'force':BASE+'rtau_strong_force_coordinate_v3_20261104/receipt.json',
 'momentum':BASE+'rtau_momentum_rate_lift_v2_20261104/receipt.json',
 'ordinary':BASE+'rtau_ordinary_velocity_remainder_v2_20261104/receipt.json',
 'gauge':BASE+'rtau_paired_gauge_rate_v2_20261104/receipt.json',
 'velocity':BASE+'rtau_canonical_velocity_remainder_v1_20261104/receipt.json',
 'mixed':BASE+'r4c1_rtau_mixed_operator_v4_attempt_01/summary.json',
 'normal1':BASE+'rtau_strong_density_normal_form_v1_20261103/receipt.json',
 'normal2':BASE+'rtau_strong_density_normal_form_v2_20261103/receipt.json',
 'higher':BASE+'r4c1_rtau_clock_density_v3_attempt_01/summary.json',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    contains=lambda x:lo(x)<=0<=hi(x)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    manifest=json.loads((ROOT/INPUTS).read_text());pins=dict(manifest['source_sha256'])
    data={k:json.loads((ROOT/v).read_text()) for k,v in SOURCES.items()}
    for rel in [SPEC,INPUTS,FACTORY,'GEMINI.md','Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md',*SOURCES.values(),Path(__file__).relative_to(ROOT).as_posix()]:
        want=sha(ROOT/rel);assert rel not in pins or pins[rel]==want,rel;pins[rel]=want
    snapshot={}
    for rel,want in pins.items():
        p=ROOT/rel;assert sha(p)==want,rel
        for q in [p,Path(str(p)+'.sha256')]:
            if q.exists():snapshot[q]=(sha(q),q.stat().st_mtime_ns)
    check('corrected_Sigma_parents_only',all(data[k]['density_coordinate']=='Sigma=rho+e_force+b*Z**2/2' for k in ['lift','force','momentum','ordinary']))
    check('all_parent_controls_pass_in_registered_scope',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for k,d in data.items() if k!='higher'))
    # Generic exact canonical Legendre and regulator controls.
    z=sp.symbols('z');be=sp.symbols('beta')
    dd,ss,zz=[sp.Function(n)(z) for n in ['d','s','Z']]
    expr=sp.diff(dd*sp.diff(zz,z),z)-2*be*sp.diff(dd*ss*zz,z)+be*dd*ss*sp.diff(zz,z)
    target=dd*sp.diff(zz,z,2)+(sp.diff(dd,z)-be*dd*ss)*sp.diff(zz,z)-2*be*sp.diff(dd*ss,z)*zz
    check('exact_full_regulator_current',sp.expand(expr-target)==0)
    check('omitted_lapse_regulator_gradient_rejected',sp.expand(expr-target-be*dd*ss*sp.diff(zz,z))!=0)
    # Independent multivariate force derivative rule, before interval evaluation.
    pp,sg,ga,vw,kap,K,A=sp.symbols('p s gamma w kappa K A',positive=True)
    uu=ga*pp+vw*sg
    yy=(ga**2-1)*pp**2+2*ga*vw*pp*sg+(kap+vw**2)*sg**2
    ff=K*uu**2/2-A*yy**sp.Rational(3,2)
    for x,y in [(pp,pp),(pp,sg),(pp,ga),(pp,vw),(pp,kap),(sg,sg),(sg,ga),(sg,vw),(sg,kap)]:
        want=K*(sp.diff(uu,x)*sp.diff(uu,y)+uu*sp.diff(uu,x,y))-sp.Rational(3,2)*A*(sp.sqrt(yy)*sp.diff(yy,x,y)+sp.diff(yy,x)*sp.diff(yy,y)/(2*sp.sqrt(yy)))
        check('exact_full_force_second_'+str(x)+'_'+str(y),sp.simplify(sp.diff(ff,x,y)-want)==0)
    # Exact auxiliary linearization about a conformal INITIAL slice.
    a,ph,t0,t3,t5=[sp.Function(n)(z) for n in ['a','psi','hxx','hyy','hzz']]
    k=1/a**2;lam=sp.diff(a,z)/a;s=sp.diff(ph,z)
    dk=-t5/a**4;dlm=(t0+t3+t5)/(2*a**2)
    metric=-dk*sp.diff(s,z)-(sp.diff(dk,z)+k*sp.diff(dlm,z)+3*lam*dk)*s
    P0=lam*s/a**4;P5=sp.diff(s,z)/a**4;Q0=-s/(2*a**4);Q5=s/(2*a**4)
    wanted=P0*(t0+t3)+P5*t5+Q0*sp.diff(t0+t3,z)+Q5*sp.diff(t5,z)
    check('exact_full_auxiliary_metric_variation',sp.simplify(metric-wanted)==0)
    # Gauge cancellation retains both clock and metric variations.
    eps=sp.Function('eps')(z);chi_g=s*eps
    h0_g=2*a*sp.diff(a,z)*eps;h5_g=h0_g+2*a*a*sp.diff(eps,z)
    Zbg=-k*(sp.diff(s,z)+lam*s)
    gauge=-k*sp.diff(chi_g,z,2)-k*lam*sp.diff(chi_g,z)+P0*2*h0_g+P5*h5_g+Q0*sp.diff(2*h0_g,z)+Q5*sp.diff(h5_g,z)
    check('exact_auxiliary_scalar_gauge_covariance',sp.simplify(gauge-eps*sp.diff(Zbg,z))==0)
    check('dropping_metric_gauge_variation_rejected',sp.simplify(-k*sp.diff(chi_g,z,2)-k*lam*sp.diff(chi_g,z)-eps*sp.diff(Zbg,z))!=0)
    # Nonconstant periodic control with nonzero harmonic partner.
    control={a:2+sp.sin(z)/11,ph:sp.sin(2*z)/13,eps:3+sp.cos(z)/17}
    check('periodic_nonconstant_gauge_fixture',sp.simplify((gauge-eps*sp.diff(Zbg,z)).subs(control).doit())==0)
    # Differential-order control for auxiliary/material commutators.
    ka,ell,shift,chi=[sp.Function(n)(z) for n in ['kap','ell','S','chi']]
    op=lambda u:-ka*sp.diff(u,z,2)-ell*sp.diff(u,z)
    comm=op(shift*sp.diff(chi,z))-shift*sp.diff(op(chi),z)
    want=(shift*sp.diff(ka,z)-2*ka*sp.diff(shift,z))*sp.diff(chi,z,2)+(shift*sp.diff(ell,z)-ka*sp.diff(shift,z,2)-ell*sp.diff(shift,z))*sp.diff(chi,z)
    check('exact_auxiliary_material_commutator',sp.expand(comm-want)==0)
    # Same action setup, first geometry differential only; no new full Hessian.
    spec=importlib.util.spec_from_file_location('actual_force_pair_factory',ROOT/FACTORY)
    fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
    J,D=env['J'],env['D']
    def first_mul(self,other):
        other=self.cast(other);zero=self.scalar(0)
        g={i:self.g.get(i,zero)*other.c+other.g.get(i,zero)*self.c for i in self.g.keys()|other.g.keys()}
        return type(self)(self.c*other.c,{i:v for i,v in g.items() if v!=0})
    def first_unary(self,value,first,second):return type(self)(value,{i:first*v for i,v in self.g.items() if v!=0})
    D.__mul__=first_mul;D.__rmul__=first_mul;D.unary=first_unary
    third=decode(data['higher']['whole_circle_third_shift_bound']);box=iv.mpf([-hi(third),hi(third)])
    y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[box]*3)
    q,v,d,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
    Q=[D.var(x,i) for i,x in enumerate(q)]
    ND,MUD,GAMD,HD,_=env['geometry'](Q,[D(x) for x in d])
    N,mu,gam=ND.c,MUD.c,GAMD.c;kj=HD[2][2].c
    aa=q[0]**mp.mpf('.5');lamj=d[0]/(2*q[0]);ellj=kj*lamj
    p=(v[12]-S[2]*d[12])/N;ssj=d[12];wj=q[8]
    par=env['env']['env']['exact'];rat=lambda t:iv.mpf(int(t.p))/int(t.q)
    KQ,AA,b,beta=[rat(par[t]) for t in ['K_Q','A','b','beta']]
    cv=q[0]*sum((x**2 for x in q[6:9]),J(0))
    rest=[x*(p+wj*ssj/(gam+1))+(kj*ssj if i==2 else 0) for i,x in enumerate(q[6:9])]
    Y=q[0]*sum((x**2 for x in rest),J(0));check('actual_whole_root_positive_Y',lo(Y.c[0])>0);assert lo(Y.c[0])>0
    root=Y**mp.mpf('.5');U=gam*p+wj*ssj
    Up={'p':gam,'s':wj,'g':p,'w':ssj,'k':J(0)}
    Yp={'p':2*cv*p+2*gam*wj*ssj,'s':2*gam*wj*p+2*(kj+wj**2)*ssj,'g':2*gam*p**2+2*wj*p*ssj,'w':2*gam*p*ssj+2*wj*ssj**2,'k':ssj**2}
    Y2={('p','p'):2*cv,('p','s'):2*gam*wj,('p','g'):4*gam*p+2*wj*ssj,('p','w'):2*gam*ssj,('p','k'):J(0),('s','s'):2*(kj+wj**2),('s','g'):2*wj*p,('s','w'):2*gam*p+4*wj*ssj,('s','k'):2*ssj}
    def f1(t):return KQ*U*Up[t]-AA*root*Yp[t]*mp.mpf('1.5')
    def f2(t,u):
        ux=J(1) if (t,u) in [('p','g'),('s','w')] else J(0)
        return KQ*(Up[t]*Up[u]+U*ux)-AA*(root*Y2[t,u]+Yp[t]*Yp[u]/(2*root))*mp.mpf('1.5')
    fp,fs=f1('p'),f1('s');fpp,fps,fss=f2('p','p'),f2('p','s'),f2('s','s')
    check('actual_full_force_fpp_positive',lo(fpp.c[0])>0);assert lo(fpp.c[0])>0
    M=N*mu;dj=M*kj*b;mass=mu*fpp/N;ap=1/mass;vp=N*fps/fpp
    force=KQ*U**2/2-AA*Y**mp.mpf('1.5');energy=p*fp-force
    lm=[MUD.g.get(i,J(0))/mu for i in range(13)]
    lM=[lm[i]-(beta if i==12 else 0) for i in range(13)]
    dg=[GAMD.g.get(i,J(0)) for i in range(13)];dw=[J(int(i==8)) for i in range(13)];dk=[HD[2][2].g.get(i,J(0)) for i in range(13)]
    geom=lambda first,i:first('g')*dg[i]+first('w')*dw[i]+first('k')*dk[i]
    pgeom=lambda t:f2('p',t);sgeom=lambda t:f2('s',t)
    Bj=[-(N/fpp)*(fp*lm[i]+geom(pgeom,i))-(N*p*beta if i==12 else 0) for i in range(13)]
    fluxq=[M*(fs*lM[i]+geom(sgeom,i)-(fps/fpp)*(fp*lm[i]+geom(pgeom,i))) for i in range(13)]
    fluxs=M*(fss-fps**2/fpp)
    dc=[dj*(lM[i]+dk[i]/kj) for i in range(13)]
    H={tuple(row['ij']):(decode(row['value']),decode(row['dz'])) for row in data['mixed']['full_mixed_Hessian_upper_triangle']}
    get=lambda i,j,dz=False:H.get(tuple(sorted((i,j))),(iv.mpf(0),iv.mpf(0)))[int(dz)]
    check('closed_mass_and_advection_consistent_with_action',contains(mass.c[0]-get(26,26)) and contains(vp.c[0]-(get(26,40)+S[2].c[0]*get(26,26))/get(26,26)))
    check('all_canonical_clock_field_coefficients_consistent',all(contains(Bj[i].c[0]+ap.c[0]*get(26,i)) for i in range(13)))
    check('ordinary_temporal_force_cross_blocks_absent',all(get(26,14+i)==0 for i in range(12)))
    # Reuse corrected physical strong-data reconstruction and smoothing.
    F=[decode(x) for x in data['force']['constants_binary']['force_H2_inverse']]
    Qcan=[decode(x) for x in data['momentum']['constants_binary']['full_configuration_H1']]
    Pcan=[decode(x) for x in data['momentum']['constants_binary']['full_momentum_L2']]
    def compose(row):
        row=[decode(x) for x in row];base=[row[j] for j in [0,1,2]]+[iv.mpf(0)]*2+[row[j] for j in [4,5,6]]
        return [x+row[3]*f for x,f in zip(base,F)]
    metric=compose(data['lift']['constants_binary']['metric_gradient_principal_remainder_H1'])
    r=iv.mpf(1)/13000;modulus=(4*r+4*r*r)*iv.exp(8*r)
    Rq=[iv.sqrt(2)*m+modulus*q+f for m,q,f in zip(metric,Qcan,F)]
    rp=[[decode(x) for x in row] for row in data['momentum']['constants_binary']['eliminated_momentum_principal_remainder_H1']]
    Rp=[sum((row[j] for row in rp),iv.mpf(0)) for j in range(8)]
    vb={k:decode(val) for k,val in data['velocity']['bounds_binary'].items()}
    M0,M1=vb['temporal_inverse'],vb['temporal_inverse_spatial_derivative']
    A0=norm([get(i,j) for i in range(14,27) for j in range(14,27)])
    A1=vb['temporal_Hessian_spatial_derivative'];B0=norm([get(i,j) for i in range(14,27) for j in range(28,41)]);B1=norm([get(i,j,True) for i in range(14,27) for j in range(28,41)])
    S0,S1=up(S[2].c[0]),up(Sz[2].c[0]);Br0=B0+S0*A0;Br1=B1+S1*A0+S0*A1
    C0,C1=vb['configuration_zeroth_matrix'],vb['configuration_matrix_derivative']
    Rv=[(M0+M1)*(Rp[j]+(Br0+Br1)*Rq[j]+(C0+C1)*Qcan[j]) for j in range(8)]
    ls=[q[8]/q[0],q[8]/q[0],q[8]/(2*q[0])]
    Pi0=1+norm([iv.mpf(1)]*3+[x.c[0] for x in ls]);Pi1=norm([x.c[1] for x in ls])
    cc=gam/aa;L0=3+iv.sqrt(2)*up(cc.c[0]);L1=iv.sqrt(2)*up(cc.c[1])
    Z0=Pi0+Br0*L0;Z1=Pi1+Br1*L0+Br0*L1
    V0=M0*Z0;V1=M1*Z0+M0*Z1
    # Corrected background I_other, never I_total mislabeled as Sigma.
    io=[decode(c['compensated_current']) for c in data['lift']['cells']]
    Iother=iv.mpf([min(lo(x) for x in io),max(hi(x) for x in io)])
    cb=decode(data['normal1']['bounds_binary']['coefficient']);ab=decode(data['normal2']['bounds_binary']['alpha'])
    fluxQ=[-fluxq[i]+(d[13]-ssj*q[13]*(2*beta))*dc[i] for i in range(13)]
    fluxS=-fluxs-dj*q[13]*(2*beta)
    localQ=[(M.c[0]*energy.c[0]-Iother)*lM[i].c[0]*beta-M.c[0]*(p*fp*lm[i]+geom(f1,i)).c[0]*beta+(d[13]*ssj-q[13]*ssj**2*beta).c[0]*dc[i].c[0]*beta-(M*q[13]**2*lM[i]).c[0]*(beta*b/2) for i in range(13)]
    locS=dj*d[13]*beta-dj*q[13]*ssj*(2*beta**2)-M*fs*beta
    locZ=-2*beta*(dj.c[1]*ssj.c[0]+dj.c[0]*ssj.c[1])-beta*b*M.c[0]*q[13].c[0]-beta**2*dj.c[0]*ssj.c[0]**2
    njet=lambda xs,order=0:norm([x.c[order]*(2 if order==2 else 1) for x in xs])
    xiQ=njet(fluxQ)+njet(fluxQ,1)+norm(localQ)
    xiF=up(fluxS.c[0])+up(fluxS.c[1])+up(locS.c[0])/2+up(beta*M.c[0])*ab/2
    xiC=up(Sz[2].c[0]-vp.c[1]+(N*p).c[0]*beta)+up(beta*M.c[0])*cb
    xiR=[xiQ*q+xiF*f for q,f in zip(Qcan,F)];xiR[0]+=up(beta*M.c[0]);xiR[2]+=xiC;xiR[3]+=up(locZ)
    # Exact initial time derivatives of auxiliary coefficients. No future ansatz.
    ht=v[0]/(2*q[0]);st=v[12].c[1];szt=2*v[12].c[2]
    check('registered_initial_metric_velocity_conformal_only_at_this_instant',all(contains((v[i]-2*ht*q[i]).c[0]) for i in [0,3,5]))
    PA=[J(0)]*12;QA=[J(0)]*12;Pt=[iv.mpf(0)]*12;Qt=[iv.mpf(0)]*12
    for i in [0,3]:
        PA[i]=kj**2*lamj*ssj;QA[i]=-kj**2*ssj/2
        Pt[i]=(kj.c[0]**2)*(ht.c[1]*ssj.c[0]+lamj.c[0]*st-4*ht.c[0]*lamj.c[0]*ssj.c[0])
        Qt[i]=-(kj.c[0]**2)*(st-4*ht.c[0]*ssj.c[0])/2
    szj=J(coefficients=[ssj.c[1],2*ssj.c[2],iv.mpf(0)])
    PA[5]=kj**2*szj;QA[5]=kj**2*ssj/2
    Pt[5]=kj.c[0]**2*(szt-4*ht.c[0]*ssj.c[1]);Qt[5]=kj.c[0]**2*(st-4*ht.c[0]*ssj.c[0])/2
    PN,QN=njet(PA),njet(QA)
    Gq0=norm([Pt[i]-S[2].c[0]*PA[i].c[1] for i in range(12)])
    Gq1=norm([Qt[i]-S[2].c[0]*QA[i].c[1]+Sz[2].c[0]*QA[i].c[0] for i in range(12)])
    kt=-2*ht.c[0]*kj.c[0];ellt=kj.c[0]*(ht.c[1]-2*ht.c[0]*lamj.c[0])
    Gchi2=-kt+S[2].c[0]*kj.c[1]-2*kj.c[0]*Sz[2].c[0]
    Gchi1=-ellt+S[2].c[0]*ellj.c[1]-2*kj.c[0]*S[2].c[2]-ellj.c[0]*Sz[2].c[0]
    Bpsi=Bj[12];ko,el=kj.c[0],ellj.c[0]
    Rchi2=2*ko*vp.c[1]-vp.c[0]*kj.c[1]-ko*Bpsi.c[0]+Gchi2
    Rchi1=2*ko*vp.c[2]+el*vp.c[1]-vp.c[0]*ellj.c[1]-(2*ko*Bpsi.c[1]+el*Bpsi.c[0])+Gchi1
    Rchi0=-2*ko*Bpsi.c[2]-el*Bpsi.c[1]
    Rxi0=-2*ko*ap.c[2]-el*ap.c[1]
    BO=Bj[:12];BO0=njet(BO)
    ZQ=norm([2*ko*x.c[1]+el*x.c[0] for x in BO])+norm([2*ko*x.c[2]+el*x.c[1] for x in BO])
    ZQ+=up(vp.c[0])*(PN+njet(QA,1)+njet(PA,1))+Gq0+Gq1
    ZY=up(ko)*BO0*L1+PN*V0+QN*V1+up(vp.c[0])*QN*L1
    ZRq=up(ko)*BO0+up(vp.c[0])*QN
    ZF=up(Rchi2)+(up(Rchi1)/2)+up(Rchi0)
    ZR=[ZQ*q+ZRq*rq+(PN+QN)*rv+ZF*f for q,rq,rv,f in zip(Qcan,Rq,Rv,F)]
    for j in [0,1,2,3]:ZR[j]+=ZY
    ZR[2]+=up(Rxi0)
    # Complete paired gauge, including harmonic coordinate motion and pullback.
    gb={k:decode(val) for k,val in data['gauge']['bounds_binary'].items()}
    affine=[decode(x) for x in data['ordinary']['bounds_binary']['affine_field_L2']]
    pull=iv.exp(5*r)
    xiR=[x+pull*gb['paired_momentum_L2_per_affine_L2']*af for x,af in zip(xiR,affine)]+[pull*gb['paired_momentum_L2_per_harmonic']]
    ZR=[x+pull*gb['auxiliary_rate_H1_per_affine_L2']*af for x,af in zip(ZR,affine)]+[pull*gb['auxiliary_rate_H1_per_harmonic']]
    check('nine_global_and_strong_input_columns_retained',len(xiR)==len(ZR)==9)
    check('all_initial_force_pair_remainder_constants_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in [xiR,ZR] for x in row))
    # Q_aux*B_gauge=(0,0,kappa*s) enforces equality of raw and Schur forms.
    gaugeBg=sp.Matrix([[0,0,0],[0,0,0],[1,0,0],[0,0,0],[0,1,0],[0,0,2*sp.Symbol('a2')]])
    qaux=sp.Matrix([[0,0,0,0,0,sp.Symbol('kap')*sp.Symbol('s')/(2*sp.Symbol('a2'))]])
    check('exact_raw_projected_force_cross_coupling_equivalence',qaux*gaugeBg==sp.Matrix([[0,0,sp.Symbol('kap')*sp.Symbol('s')]]))
    check('registered_regulator_first_coefficient_identity',contains(dj.c[1]-dj.c[0]*(lamj.c[0]-beta*ssj.c[0])))
    check('original_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshot.items()))
    return dict(kind='RTAU_ACTUAL_FORCE_PAIR_V1',source_sha256=pins,passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
        input_order=data['force']['inverse_input_order']+['harmonic_coordinate_velocity_adapted'],
        bounds_binary={'auxiliary_L2_remainder':[binary(x) for x in ZR],'force_momentum_L2_remainder':[binary(x) for x in xiR]},
        upper_display={'auxiliary_L2_remainder':[mp.nstr(hi(x),28) for x in ZR],'force_momentum_L2_remainder':[mp.nstr(hi(x),28) for x in xiR]},
        coefficient_controls_binary={'positive_Y':binary(Y.c[0]),'force_temporal_mass':binary(mass.c[0]),'force_advection':binary(vp.c[0]),'raw_velocity_principal_norm':binary(V0),'raw_velocity_principal_derivative_norm':binary(V1),'auxiliary_metric_P_norm':binary(PN),'auxiliary_metric_Q_norm':binary(QN),'force_B_second_derivative_norm':binary(njet(Bj,2))},
        scope='INITIAL_ACTUAL_FORCE_PAIR_L2_REMAINDERS_WITH_REGISTERED_TWENTY_DIRECTION_PRINCIPAL_AND_CORRECTED_SIGMA_COMPATIBLE_LIFT_ONLY',
        density_coordinate='Sigma=rho+e_force+b*Z**2/2',density_actual_rate='NOT_ASSEMBLED',moving_Green_range_maps='NOT_ASSEMBLED',
        full_actual_generator='NOT_ASSEMBLED',full_prepared_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);a=ap.parse_args()
    if a.output:assert not a.output.parent.exists(),'Fresh receipt directory required'
    try:d=calculate()
    except Exception as e:
        if a.output:
            a.output.parent.mkdir(parents=True);p=a.output.parent/'failure.json';p.write_text(json.dumps({'error':repr(e),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n');Path(str(p)+'.sha256').write_text(sha(p)+'\n')
        raise
    raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if a.output:
        a.output.parent.mkdir(parents=True);a.output.write_bytes(raw);Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
    else:assert a.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'kind':d['kind'],'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'bounds':d['upper_display'],'physics_pass':False}))
    if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
