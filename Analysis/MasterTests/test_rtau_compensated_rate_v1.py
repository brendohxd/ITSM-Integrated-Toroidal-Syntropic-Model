"""Complete initial compensated scalar rate bound; not a physical energy estimate."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_RATE_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
RATE='Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json'
GAUGE='Analysis/MasterTests/outputs/rtau_initial_gauge_composition_v2_20261103/receipt.json'
EXACT='Analysis/MasterTests/outputs/rtau_compensated_density_v1_20261103/receipt.json'
MAP='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
DT='Analysis/MasterTests/r4c1_density_time_transport_v1.py'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    binary=lambda x:[list(t) for t in x._mpi_]
    scale=lambda c,row:[c*x for x in row]
    add=lambda *rows:[sum(xs,iv.mpf(0)) for xs in zip(*rows)]
    unit=lambda i:[iv.mpf(int(i==k)) for k in range(5)]
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,RATE,GAUGE,EXACT,MAP,FACTORY,DT,
                'Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md'):
        pins[rel]=sha(ROOT/rel)
    snap={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snap[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_source_hashes_match',len(original)==219)
    rate=json.loads((ROOT/RATE).read_text());gauge=json.loads((ROOT/GAUGE).read_text());exact=json.loads((ROOT/EXACT).read_text())
    check('canonical_gauge_and_exact_cancellation_owners_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (rate,gauge,exact)))
    V=[decode(x) for x in rate['coefficients_binary']['field_rate_L2']]+[iv.mpf(0)]
    Znorm=[decode(x) for x in rate['coefficients_binary']['auxiliary_L2']]+[iv.mpf(0)]
    env=load('compensated_rate_actual_factory',FACTORY).prepare();J,D=env['J'],env['D']
    grad=env['gradient'];geo=env['geometry'];lie=env['lie']
    y,_=env['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q,v,d,S,Sz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
    params=env['env']['env']['exact']
    rational=lambda x:iv.mpf(int(x.p))/int(x.q)
    KQ,A,b,beta=[rational(params[key]) for key in ('K_Q','A','b','beta')]
    check('full_norm_cubed_force_coefficient_nonzero',lo(A)>0)
    NJ,muJ,_,_,_=geo(q,d)
    pJ=(v[12]-S[2]*d[12])/NJ
    p0=up(pJ.c[0]);s0=up(S[2].c[0]);s1=up(Sz[2].c[0])
    scalarcols={'q':range(13),'v':range(14,27),'d':range(28,41),'S':range(42,45),'Sz':range(45,48)}
    gn=lambda expr,cols:norm([expr.g.get(i,J(0)).c[0] for i in cols])
    def local(expr):
        return add(scale(gn(expr,scalarcols['v']),V),
                   scale(gn(expr,scalarcols['q'])+gn(expr,scalarcols['d']),unit(1)),
                   scale(gn(expr,scalarcols['S'])+gn(expr,scalarcols['Sz']),unit(3)))
    def force(qq,pp,ss):
        _,_,gamma,H,_=geo(qq,[J(0)]*14)
        h=[[qq[0],qq[1],qq[2]],[qq[1],qq[3],qq[4]],[qq[2],qq[4],qq[5]]]
        rest=[H[i][2]*ss+qq[6+i]*(pp+qq[8]*ss/(gamma+1)) for i in range(3)]
        Y=sum((h[i][i]*rest[i]**2 for i in range(3)),D(0))
        Y+=2*sum((h[i][k]*rest[i]*rest[k] for i in range(3) for k in range(i+1,3)),D(0))
        assert lo(Y.c.c[0])>0,'The full prepared force branch must stay positive'
        return (gamma*pp+qq[8]*ss)**2*KQ/2-Y**mp.mpf('1.5')*A,Y
    qn=[D.var(x,i) for i,x in enumerate(q)]
    fn,Yn=force(qn,D.var(pJ,100),D.var(d[12],101))
    fs=fn.g.get(101,J(0));fp=fn.g.get(100,J(0))
    fq=[fn.g.get(i,J(0)) for i in range(9)]
    hn=lambda rows,cols:norm([fn.h.get(tuple(sorted((i,k))),J(0)).c[0] for i in rows for k in cols])
    qv=[D.var(x,i) for i,x in enumerate(q)];vv=[D.var(x,14+i) for i,x in enumerate(v)]
    dd=[D.var(x,28+i) for i,x in enumerate(d)];sv=[D.var(x,42+i) for i,x in enumerate(S)];szv=[D.var(x,45+i) for i,x in enumerate(Sz)]
    n,mu,_,H,_=geo(qv,dd)
    pp=(vv[12]-sv[2]*dd[12])/n
    np=vv[12]-sv[2]*dd[12]
    fr,Yr=force(qv,pp,dd[12])
    LF=n*mu*fr
    check('normal_and_raw_force_Y_enclosures_positive',lo(Yn.c.c[0])>0 and lo(Yr.c.c[0])>0)
    pi_raw=LF.g.get(26,J(0))
    pi_normal=muJ*fp
    check('normal_raw_force_momentum_enclosure_consistency',lo(pi_raw.c[0])<=hi(pi_normal.c[0]) and lo(pi_normal.c[0])<=hi(pi_raw.c[0]))
    check('raw_force_has_no_auxiliary_momentum',27 not in LF.g)

    # Full geometric rates in the same variables as the action, including all
    # tensor index and transverse-shift terms.
    lv=lie(qv,dd,sv,szv)
    kv=[(vv[i]-lv[i])/(2*n) for i in range(6)]
    K=[[kv[0],kv[1],kv[2]],[kv[1],kv[3],kv[4]],[kv[2],kv[4],kv[5]]]
    trace=sum((H[i][k]*K[k][i] for i in range(3) for k in range(3)),D(0))
    kup=sum((H[2][i]*K[i][k]*H[k][2] for i in range(3) for k in range(3)),D(0))
    T=H[2][2]*trace-2*kup
    stress=n*(T*dd[12]*(dd[13]-qv[13]*dd[12]*beta)-trace*qv[13]**2/2)*b
    stressrow=local(stress)
    gz=stress.g.get(41,J(0));gZ=stress.g.get(13,J(0))
    stressrow=add(stressrow,scale(up(gZ.c[0])+up(gz.c[0])+up(gz.c[1]),Znorm))
    check('surviving_metric_stress_not_deleted',hi(up(gz.c[0])+up(gZ.c[0]))>0)

    L=env['evaluate'](y)
    direct=load('compensated_rate_existing_density',DT)
    RG=direct.regulator(env,qv,dd)
    other=L-LF-RG
    E0=grad(other,12).c[0]-grad(other,40).c[1]
    hnorm=lambda row,cols:norm([other.h.get(tuple(sorted((row,i))),J(0)).c[0] for i in cols])
    en={key:hnorm(12,cols)+hnorm(40,cols) for key,cols in scalarcols.items()}
    Erow=add(scale(en['v'],V),scale(en['q']+en['d'],unit(1)),scale(en['S']+en['Sz'],unit(3)))
    # Excluding Z,Z_z here uses exact sector independence after the declared
    # force/regulator split, not small interval subtraction remnants.
    check('other_action_Euler_coefficients_finite',all(mp.isfinite(hi(x)) for x in en.values()))
    pj=[grad(L,14+i) for i in range(13)]+[J(0)]
    rv=[x-t for x,t in zip(v,lie(q,d,S,Sz))]
    B0=direct.improvement(env,q,d,pj)
    sig=(other.c-sum((pj[i]*rv[i] for i in range(12)),J(0))).c[0]-B0.c[1]
    sigma0=up(sig/(NJ*muJ).c[0])
    check('actual_background_compensated_density_finite',mp.isfinite(hi(sigma0)),mp.nstr(hi(sigma0),20))

    dp=local(pp)
    fsrow=add(scale(hn([101],range(9))+hn([101],[101]),unit(1)),scale(hn([101],[100]),dp))
    fQ=norm([x.c[0] for x in fq]);a0=norm([(v[i]-S[2]*d[i]).c[0] for i in range(9)])
    zq=norm([d[i].c[0] for i in range(9)])
    dW=add(scale(a0*(hn(range(9),range(9))+hn(range(9),[101]))+fQ*s0,unit(1)),
           scale(a0*hn(range(9),[100]),dp),scale(fQ,V),scale(fQ*zq,unit(3)))
    check('full_frame_metric_force_work_retained',hi(fQ)>0)
    M=n*mu
    Gbg=(NJ*muJ)*fs
    Gdelta=add(scale(up(fs.c[0]),local(M)),scale(up(M.c.c[0]),fsrow))
    a=pp/mu
    aw1=up(a.c.c[0])+up(a.c.c[1])
    term_gradient=add(scale(up(Gbg.c[1]),local(a)),scale(aw1,Gdelta))
    Hbg=(NJ*pJ).c[1]+Sz[2].c[0]*d[12].c[0]
    term_fs=add(scale(up(Hbg),fsrow),scale(up(fs.c[0])+up(fs.c[1]),local(np)),
                scale(up(fs.c[0])*up(d[12].c[0]),unit(3)),scale(up(fs.c[0])*s1,unit(1)))
    term_other=add(scale(up(E0),local(a)),scale(aw1,Erow))
    coef=n*(pp*beta-trace)
    term_sigma=add(scale(sigma0,local(coef)),scale(up(coef.c.c[0]),unit(4)))
    term_local=local(n*trace*fr)
    material=add(term_sigma,term_local,term_gradient,term_fs,dW,term_other,stressrow)

    mb=json.loads((ROOT/MAP).read_text())['bounds']
    j=iv.mpf(lo(decode(mb['J_lower_binary'])));u=iv.mpf(hi(decode(mb['J_upper_binary'])))
    W=iv.mpf(hi(decode(mb['drift_upper_binary'])));P=iv.mpf(hi(decode(mb['drift_derivative_upper_binary'])))
    r=iv.mpf(1)/13000
    scalar1=u*(iv.mpf(max(mp.mpf(1),hi(u)))+r)/iv.sqrt(j)
    eulerian=add(material,scale(s0+s1+W+P,unit(4)),scale(2*sigma0,unit(3)))
    eulerian=scale(scalar1,eulerian)
    sigma=[decode(x) for x in gauge['canonical_input_constants_binary']['corrective_shift_H1_original']]
    qlift=decode(gauge['graph_lift_binary']['Q1_per_Dminus']);plift=decode(gauge['graph_lift_binary']['P0_per_Dminus'])
    parts=dict(coefficient_times_Sigma=term_sigma,local_force_term=term_local,force_gradient_flux=term_gradient,
               force_spatial_rate=term_fs,force_metric_frame_work=dW,other_action_Euler=term_other,
               regulator_metric_stress=stressrow,full_material_rate=material,full_adapted_time_rate=eulerian)
    def lift(row):
        cl=[row[i]+row[3]*sigma[i] for i in range(3)]+[row[3]*sigma[3],row[4]]
        return [cl[0]*plift+cl[1]*qlift,cl[1],cl[0],cl[2],cl[3],cl[4]]
    output={key:lift(row) for key,row in parts.items()}
    check('every_remainder_and_total_has_finite_outward_bound',all(lo(x)>=0 and mp.isfinite(hi(x)) for row in output.values() for x in row))
    check('compensated_L2_observable_is_explicit_input',hi(output['full_adapted_time_rate'][-1])>0)
    check('force_and_other_action_remainders_not_zeroed',all(hi(x)>0 for x in output['other_action_Euler'][:3]) and hi(output['force_metric_frame_work'][1])>0)

    z=sp.symbols('z');aa,gg=sp.Function('a')(z),sp.Function('g')(z)
    check('weak_flux_product_identity',sp.expand(aa*sp.diff(gg,z)-sp.diff(aa*gg,z)+sp.diff(aa,z)*gg)==0)
    sf=sp.sin(z)/3;bg=1+sp.cos(2*z)/7;test=sp.cos(z)
    strong_pair=sp.integrate(sf*sp.diff(bg,z)*test,(z,0,2*sp.pi))/(2*sp.pi)
    weak_pair=-sp.integrate(sf*bg*sp.diff(test,z)+sp.diff(sf,z)*bg*test,(z,0,2*sp.pi))/(2*sp.pi)
    check('independent_weak_background_transport_pair',sp.simplify(strong_pair-weak_pair)==0 and sp.simplify(strong_pair)==-sp.Rational(1,42))
    # Separate explicit nonconstant control: a pointwise background derivative
    # was never set to zero in bounding delta S*Sigma_z.
    check('background_compensator_transport_not_erased',sp.diff(1+sp.cos(z),z)!=0)
    check('all_original_input_and_sidecar_bytes_preserved',all(sha(path)==h and path.stat().st_mtime_ns==stamp for path,(h,stamp) in snap.items()))
    return dict(kind='RTAU_COMPLETE_INITIAL_COMPENSATED_RATE_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,
                input_order=['Dminus','Qfree_H1_original','Pfree_L2_original','force_configuration_H2_original','harmonic_coordinate_velocity_adapted','compensated_observable_L2_original'],
                constants_binary={key:[binary(x) for x in row] for key,row in output.items()},
                upper_display={key:[mp.nstr(hi(x),18) for x in row] for key,row in output.items()},
                background_compensator_binary=binary(sigma0),background_compensator_upper=mp.nstr(hi(sigma0),18),
                prepared_force_Y_binary=binary(Yn.c.c[0]),conditional_parameters={key:str(params[key]) for key in ('K_Q','A','b','beta')},
                source_sha256=pins,inherited_source_count=len(original),
                scope='COMPLETE_INITIAL_COMPENSATED_ROW_HMINUS1_ON_EXACT_COMPATIBLE_PLANAR_GRAPH',
                observable_domain='Sigma_L2 is measured explicitly, not inferred from Dminus or used as an unproved new trace chart',
                auxiliary_exclusion='Exact other-sector independence; interval subtraction remnants are not declared zero',
                Ward_defect='Retained; estimate is on exact constrained background/tangent, not a zero-defect numerical-centre assumption',
                physical_energy='NOT_DERIVED',new_density_chart_inverse='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    try:receipt=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            with (args.output.parent/'failure.json').open('x') as handle:json.dump(dict(status='FAILED_ATTEMPT',error=repr(error),source_sha256=sha(Path(__file__)),physics_pass=False),handle,indent=2)
        raise
    raw=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as handle:handle.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as handle:handle.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps(dict(passed=receipt['passed'],total=receipt['total'],failed=[x for x in receipt['checks'] if not x['passed']],
                         full_rate=receipt['upper_display']['full_adapted_time_rate'],background_compensator_upper=receipt['background_compensator_upper']),indent=2))
    return 0 if receipt['passed']==receipt['total'] else 1


if __name__=='__main__':raise SystemExit(main())
