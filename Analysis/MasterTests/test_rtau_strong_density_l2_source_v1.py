"""Complete initial strong-density L2 source; full coupled energy is open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_L2_SOURCE_V1_CONTRACT_2026-11-04.md'
SPEC='Theory/Gates/RES-001/RES001_RTAU_STRONG_DENSITY_L2_SOURCE_V1_EXECUTION_SPEC_2026-11-04.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
BASE='Analysis/MasterTests/outputs/'
SOURCES={
 'normal1':BASE+'rtau_strong_density_normal_form_v1_20261103/receipt.json',
 'normal2':BASE+'rtau_strong_density_normal_form_v2_20261103/receipt.json',
 'lapse':BASE+'rtau_other_sector_lapse_identity_v1_20261103/receipt.json',
 'canonical':BASE+'rtau_weak_canonical_rate_v2_20261103/receipt.json',
 'gauge':BASE+'rtau_initial_gauge_composition_v2_20261103/receipt.json',
 'map':BASE+'r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json',
 'higher':BASE+'r4c1_rtau_clock_density_v3_attempt_01/summary.json',
 'advection':BASE+'rtau_compensated_transport_v2_20261103/receipt.json'}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    parents={key:json.loads((ROOT/rel).read_text()) for key,rel in SOURCES.items()}
    for d in parents.values():
        for rel,h in d['source_sha256'].items():
            assert sha(ROOT/rel)==h,rel
            assert rel not in pins or pins[rel]==h,rel
            pins[rel]=h
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),CONTRACT,SPEC,MANIFEST,FACTORY,*SOURCES.values()):pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snapshot[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_and_all_parent_pins_match',len(original)==219)
    check('all_parent_checks_pass_in_their_scopes',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in parents.values()))
    check('exact_other_lapse_identity_available',parents['lapse']['exact_identity']=='E_other=-beta*N*E_N,other=-beta*I_other=-beta*M*Sigma')

    # Exact local force-gradient decomposition, before taking any norms.
    N,mu,Mz,fs,fsq,fsp,fss,p,qz,pz,sz,Nz,Sz,s=sp.symbols('N mu Mz fs fsq fsp fss p qz pz sz Nz Sz s')
    lhs=-(p/mu)*(Mz*fs+N*mu*(fsq*qz+fsp*pz+fss*sz))-fs*(Nz*p+N*pz)-fs*Sz*s
    rhs=-N*(p*fsp+fs)*pz-(p/mu)*Mz*fs-N*p*fsq*qz-N*p*fss*sz-fs*Nz*p-fs*Sz*s
    check('complete_force_gradient_remainder_identity',sp.expand(lhs-rhs)==0)
    fac=load('strong_density_L2_source_factory',FACTORY);env=fac.prepare();J,D=env['J'],env['D']
    par=env['env']['env']['exact'];KQ,A,b,beta=[rational(par[k]) for k in ('K_Q','A','b','beta')]

    def partial(expr,i):
        # Exact first-variation lift. No second derivative of this lift is used.
        gs={}
        for key,val in expr.h.items():
            if key[0]==i:gs[key[1]]=val
            if key[1]==i:gs[key[0]]=val
        return D(expr.g.get(i,J(0)),gs)

    def force(Q,pp,ss):
        N,mu,gamma,H,_=env['geometry'](Q,[D(0)]*14)
        h=[[Q[0],Q[1],Q[2]],[Q[1],Q[3],Q[4]],[Q[2],Q[4],Q[5]]]
        rest=[H[i][2]*ss+Q[6+i]*(pp+Q[8]*ss/(gamma+1)) for i in range(3)]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0,'No force derivatives inferred at the Y=0 cusp'
        F=(gamma*pp+Q[8]*ss)**2*KQ/2-Y**mp.mpf('1.5')*A
        B=gamma*Q[8]*pp+(H[2][2]+Q[8]**2)*ss
        Fs=Q[8]*(gamma*pp+Q[8]*ss)*KQ-Y**mp.mpf('.5')*B*(3*A)
        return dict(N=N,mu=mu,gamma=gamma,H=H,Y=Y,F=F,Fs=Fs)

    # Independent third-force-derivative control: rational tilted coefficient
    # data only, never a new physical initial state or fit.
    hsym,psym,ssym=sp.symbols('h p s',positive=True)
    v1,v3=sp.Rational(1,29),sp.Rational(1,31)
    tilt=hsym*v1*v1+v3*v3;gam=sp.sqrt(1+tilt)
    yy=tilt*psym**2+2*gam*v3*psym*ssym+(1+v3*v3)*ssym**2
    symbolic=par['K_Q']*(gam*psym+v3*ssym)**2/2-par['A']*yy**sp.Rational(3,2)
    qc=[J(0) for _ in range(14)]
    for i in (0,3,5):qc[i]=J(1)
    qc[6]=J(rational(v1));qc[8]=J(rational(v3))
    testforce=force([D.var(q,i) for i,q in enumerate(qc)],D.var(J(iv.mpf(1)/5),100),D.var(J(iv.mpf(1)/37),101))
    sub={hsym:1,psym:sp.Rational(1,5),ssym:sp.Rational(1,37)}
    coords={0:hsym,100:psym,101:ssym}
    for i,k in ((100,100),(100,101),(101,101),(0,100),(0,101),(0,0)):
        exact=sp.diff(symbolic,ssym,coords[i],coords[k]).subs(sub)
        expected=iv.mpf(str(sp.N(exact,85)))
        actual=testforce['Fs'].h.get(tuple(sorted((i,k))),J(0)).c[0]
        check('independent_third_force_partial_'+str(i)+'_'+str(k),hi(up(actual-expected))<mp.mpf('1e-38'))

    third=decode(parents['higher']['whole_circle_third_shift_bound']);thirdbox=iv.mpf([-hi(third),hi(third)])
    y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[thirdbox]*3)
    q0,v0,d0,S0,Sz0=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
    N0=env['geometry'](q0,d0)[0];pn=(v0[12]-S0[2]*d0[12])/N0
    Q=[D.var(q,i) for i,q in enumerate(q0)]
    pp=D.var(pn,100);ss=D.var(d0[12],101)
    dd=[D.var(q,200+i) for i,q in enumerate(d0)]
    dd[12]=ss;dd[13]=D(d0[13])  # fast delta Z_z was isolated exactly
    szz=D.var(J(coefficients=[d0[12].c[1],2*d0[12].c[2],iv.mpf(0)]),300)
    vv=[D.var(q,500+i) for i,q in enumerate(v0[:13])]+[D(0)]
    S=[D.var(q,400+i) for i,q in enumerate(S0)];SZ=[D.var(q,410+i) for i,q in enumerate(Sz0)]
    data=force(Q,pp,ss);N,mu,H,F,Fs=data['N'],data['mu'],data['H'],data['F'],data['Fs']
    M=N*mu;kap=H[2][2]
    fp=partial(F,100);fpp=F.h.get((100,100),J(0)).c[0]
    check('whole_root_normal_force_kinetic_positive',lo(fpp)>0)
    denominator=mu.c.c[0]*fpp
    Bp=up(1/denominator)
    gp=[mu.g.get(i,J(0)).c[0]*F.g.get(100,J(0)).c[0]+mu.c.c[0]*F.h.get(tuple(sorted((100,i))),J(0)).c[0] for i in range(13)]
    Bq=(norm(gp)+up(mu.c.c[0])*up(F.h.get((100,101),J(0)).c[0]))*Bp
    alpha=-(pp*partial(Fs,100)+Fs)
    Nz=-N*ss*beta
    muz=sum((partial(mu,i)*dd[i] for i in range(6)),D(0))
    Mz=Nz*mu+N*muz
    rv=[a-c for a,c in zip(vv,env['lie'](Q,dd,S,SZ))]
    kv=[rv[i]/(2*N) for i in range(6)]
    K=[[kv[0],kv[1],kv[2]],[kv[1],kv[3],kv[4]],[kv[2],kv[4],kv[5]]]
    trK=sum((H[i][k]*K[k][i] for i in range(3) for k in range(3)),D(0))
    kup=sum((H[2][i]*K[i][k]*H[k][2] for i in range(3) for k in range(3)),D(0))
    T=kap*trK-2*kup;acoef=N*T*ss*b;dcoef=M*kap*b;rcoef=dcoef*ss*beta
    C=-N*trK
    fg=-(pp/mu)*Mz*Fs-N*pp*sum((partial(Fs,i)*dd[i] for i in range(9)),D(0))
    fg-=N*pp*partial(Fs,101)*szz+Fs*Nz*pp+Fs*SZ[2]*ss
    Wf=sum((partial(F,i)*(vv[i]-S[2]*dd[i]) for i in range(9)),D(0))
    reglow=-acoef*ss*Q[13]*beta-N*trK*Q[13]**2*(b/2)
    bg=parents['normal1']['bounds_binary'];sigabs=decode(bg['background_Sigma']);sigzabs=decode(bg['background_Sigma_z'])
    Sigma=D.var(J(iv.mpf([-hi(sigabs),hi(sigabs)])),600)
    pibg=mu.c.c[0]*F.g.get(100,J(0)).c[0]
    Jrem=S[2]*pibg+dcoef*D(d0[13])-M*Fs-dcoef*Q[13]*ss*(2*beta)
    ereg=pp*fp-F
    reg=M*Q[13]**2*(b/2)-dcoef*ss*D(d0[13])+dcoef*Q[13]*ss**2*beta
    Rrem=M*(ereg-Sigma)*beta-reg*beta
    vel=[decode(x) for x in parents['canonical']['coefficients_binary']['field_rate_L2']]
    aux=[decode(x) for x in parents['canonical']['coefficients_binary']['auxiliary_L2']]
    zero=lambda:[iv.mpf(0) for _ in range(5)]
    add=lambda *rows:[sum(xs,iv.mpf(0)) for xs in zip(*rows)]
    scale=lambda a,row:[a*x for x in row]
    # Pre-closure order: Sigma_L2, Q_H1, P_L2, force_H2, caller_shift_H1.
    normalp=[iv.mpf(0),Bq,Bp,iv.mpf(0),iv.mpf(0)]
    auxrow=[iv.mpf(0),aux[1],aux[0],aux[2],aux[3]]
    velrow=[iv.mpf(0),vel[1],vel[0],vel[2],vel[3]]
    allowed=set(range(14))|{100,101,300,600}|set(range(200,212))|set(range(400,403))|set(range(410,413))|set(range(500,513))
    def local(expr):
        assert set(expr.g)<=allowed,sorted(set(expr.g)-allowed)
        gs=lambda inds:norm([expr.g.get(i,J(0)).c[0] for i in inds])
        row=add(scale(up(expr.g.get(100,J(0)).c[0]),normalp),
                scale(up(expr.g.get(13,J(0)).c[0]),auxrow),scale(gs(range(500,513)),velrow))
        row[0]+=up(expr.g.get(600,J(0)).c[0])
        row[1]+=gs(range(13))+gs(range(200,212))+up(expr.g.get(101,J(0)).c[0])
        row[3]+=up(expr.g.get(300,J(0)).c[0])
        row[4]+=gs(range(400,403))+gs(range(410,413))
        return row
    components=dict(reaction_coefficient=scale(sigabs,local(C)),force_local=local(-N*trK*F),
                    force_gradient_regular=local(fg),force_gradient_coefficient=scale(up(pn.c[1]),local(N*alpha)),
                    full_metric_frame_work=local(Wf),regulator_coefficient=scale(up(d0[13].c[0]),local(acoef)),
                    regulator_local=local(reglow),current_remainder=local(Jrem),local_momentum_remainder=local(Rrem))
    F0row=add(*(components[k] for k in ('reaction_coefficient','force_local','force_gradient_regular','force_gradient_coefficient','full_metric_frame_work','regulator_coefficient','regulator_local')))
    F0row[4]+=sigzabs
    cabs,czabs,ctabs=[decode(bg[k]) for k in ('coefficient','coefficient_z','coefficient_time')]
    aabs,azabs,atabs=[decode(parents['normal2']['bounds_binary'][k]) for k in ('alpha','alpha_z','alpha_time')]
    Cabs=up(C.c.c[0]);sabs=up(S0[2].c[0]);szabs=up(Sz0[2].c[0])
    kc=Cabs*cabs+ctabs+sabs*czabs
    ka=Cabs*aabs+atabs+sabs*azabs+aabs*szabs
    total=add(F0row,scale(cabs,components['current_remainder']),scale(cabs,components['local_momentum_remainder']))
    total=add(total,scale(cabs*(up(dcoef.c.c[1])+up(rcoef.c.c[0])+up(rcoef.c.c[1])),auxrow),
              scale(aabs*up(Nz.c.c[0]),normalp))
    total[1]+=ka+aabs*beta*(up((N.c*pn).c[1])+up((N.c*pn).c[0]))
    total[2]+=kc+2*cabs*sabs
    total[4]+=aabs*(up(d0[12].c[0])+up(d0[12].c[1]))
    # Close original Sigma by the exact same-strength triangular inverse.
    closed=[Cabs+total[0],total[1]+total[0]*aabs,total[2]+total[0]*cabs,total[3],total[4]]
    sigma=[decode(x) for x in parents['gauge']['canonical_input_constants_binary']['corrective_shift_H1_original']]
    caller=closed.copy()
    # Post-gauge order: w_L2, Q_H1_original, P_L2_original, force_H2_original, harmonic_velocity_adapted.
    source=[closed[0],closed[1]+closed[4]*sigma[1],closed[2]+closed[4]*sigma[0],closed[3]+closed[4]*sigma[2],closed[4]*sigma[3]]
    original_rate=source.copy();original_rate[0]+=szabs/2
    mb=parents['map']['bounds'];j=iv.mpf(lo(decode(mb['J_lower_binary'])));ju=iv.mpf(hi(decode(mb['J_upper_binary'])))
    badv=decode(parents['advection']['bounds_binary']['adapted_advection_first'])
    adapted=[iv.sqrt(ju)*x for x in source];adapted[0]=iv.sqrt(ju/j)*source[0]+badv/2
    check('all_complete_component_and_rate_bounds_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in (*components.values(),F0row,caller,source,original_rate,adapted) for x in row))
    check('all_required_remainders_exported',len(components)==9 and len(adapted)==5)
    check('momentum_mean_transport_and_weighted_means_retained',hi(2*cabs*sabs)>0 and hi(cabs*up(dcoef.c.c[1]))>0)
    check('harmonic_coordinate_velocity_not_removed',hi(adapted[4])>0)
    check('density_strength_is_L2_with_force_H2_retained',hi(adapted[0])>0 and hi(adapted[3])>0)

    zz=sp.symbols('z');vv,sspeed=[sp.Function(n)(zz) for n in ('v','S')]
    check('exact_scalar_L2_transport_identity',sp.expand(vv*sspeed*sp.diff(vv,zz)+sp.diff(sspeed,zz)*vv*vv/2-sp.diff(sspeed*vv*vv/2,zz))==0)
    ut,uz,Jc,sc,wc=sp.symbols('ut uz J S w',nonzero=True)
    check('whole_normal_form_scalar_coordinate_transport',sp.expand(ut-wc*uz-Jc*(sc-wc)*(uz/Jc)-(ut-sc*uz))==0)
    # In the adapted state the original primitive is CONJUGATED. Its nonzero
    # rank-two transport commutator is not replaced by a new mean condition.
    pit=1+sp.cos(zz)/17;wt=sp.cos(zz)/47
    mean=lambda f:sp.simplify(sp.integrate(f,(zz,0,2*sp.pi))/(2*sp.pi))
    def primitive(f):
        raw=sp.integrate(sp.expand_trig(f-mean(f)),zz)
        return sp.simplify(raw-mean(raw))
    comm=primitive(sp.diff(wt*pit,zz))-wt*(pit-mean(pit))
    expected=wt*mean(pit)-mean(wt*pit)
    check('conjugated_primitive_nonzero_coordinate_commutator',sp.trigsimp(comm-expected)==0 and sp.trigsimp(expected)!=0)
    check('all_sources_and_sidecar_bytes_timestamps_preserved',all(sha(path)==h and path.stat().st_mtime_ns==t for path,(h,t) in snapshot.items()))
    rows={**components,'complete_F0':F0row,'caller_shift_closed_density':caller,'gauge_closed_source':source,
          'original_L2_norm_rate':original_rate,'adapted_L2_norm_rate':adapted}
    return dict(kind='RTAU_COMPLETE_INITIAL_STRONG_DENSITY_L2_SOURCE_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),rows_binary={k:[binary(x) for x in row] for k,row in rows.items()},
                upper_display={k:[mp.nstr(hi(x),24) for x in row] for k,row in rows.items()},
                normal_p_bounds_binary={'P':binary(Bp),'Q':binary(Bq)},
                local_row_order=['Sigma_L2_original','Q_H1_original','P_L2_original','force_H2_original','caller_shift_H1_original'],
                output_order=['corrected_density_L2_in_named_coordinates','Q_H1_original','P_L2_original','force_H2_original','harmonic_coordinate_velocity_adapted'],
                adapted_definition='Scalar pullback of entire original strong normal form, with conjugated original primitive; no new adapted zero-mean prescription',
                scope='COMPLETE_INITIAL_COMPATIBLE_PLANAR_STRONG_DENSITY_SECTOR_ONLY',density_strength='L2',
                full_coupled_energy='NOT_DERIVED',moving_full_symplectic_Green_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--verify',type=Path);args=parser.parse_args()
    try:data=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps({'status':'FAILED_ATTEMPT','error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n')
        raise
    raw=(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':data['passed'],'total':data['total'],'failed':[c for c in data['checks'] if not c['passed']],
                      'adapted_rate':data['upper_display']['adapted_L2_norm_rate'],'original_rate':data['upper_display']['original_L2_norm_rate'],
                      'full_coupled_energy':data['full_coupled_energy']},indent=2))
    return 0 if data['passed']==data['total'] else 1

if __name__=='__main__':raise SystemExit(main())
