"""Initial density-sector H^-1 logarithmic bound; not a coupled time theorem."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_TRANSPORT_V2_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
RATE='Analysis/MasterTests/outputs/rtau_compensated_rate_v1_20261103/receipt.json'
RATE_SOURCE='Analysis/MasterTests/test_rtau_compensated_rate_v1.py'
CHART='Analysis/MasterTests/outputs/rtau_compensated_source_chart_v1_20261103/receipt.json'
GAUGE='Analysis/MasterTests/outputs/rtau_initial_gauge_composition_v2_20261103/receipt.json'
MAP='Analysis/MasterTests/outputs/r4c1_rtau_spatial_gauge_v1_attempt_01/summary.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result

def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,FACTORY,RATE,RATE_SOURCE,CHART,GAUGE,MAP,
                'Analysis/MasterTests/test_rtau_compensated_transport_v1.py',
                'Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_TRANSPORT_V1_SPEC_2026-11-03.md',
                'Analysis/MasterTests/outputs/rtau_compensated_transport_v1_20261103/failure.json',
                'Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_SOURCE_CHART_V1_REPORT_2026-11-03.md'):
        pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel in pins:
        for p in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if p.exists():snapshot[p]=(sha(p),p.stat().st_mtime_ns)
    check('all_219_original_hashes_match',len(original)==219)
    rate,chart,gauge,mapping=[json.loads((ROOT/rel).read_text()) for rel in (RATE,CHART,GAUGE,MAP)]
    check('all_parent_owners_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (rate,chart,gauge,mapping)))

    # Verify extraction against the frozen producer's actual lift formula.
    tree=ast.parse((ROOT/RATE_SOURCE).read_text());outer=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    fn=copy.deepcopy(next(n for n in outer.body if isinstance(n,ast.FunctionDef) and n.name=='lift'))
    rs=sp.symbols('r0:5');ss=sp.symbols('s0:4');pl,ql=sp.symbols('pl ql')
    namespace={'sigma':ss,'plift':pl,'qlift':ql}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<frozen-compensated-rate-lift>','exec'),namespace)
    lifted=namespace['lift'](rs)
    selected=[lifted[i] for i in (2,1,3,4)]
    expected=[rs[0]+rs[3]*ss[0],rs[1]+rs[3]*ss[1],rs[2]+rs[3]*ss[2],rs[3]*ss[3]]
    check('canonical_material_columns_follow_exact_frozen_lift',all(sp.expand(a-b)==0 for a,b in zip(selected,expected)))

    # Exact scalar transport pairing, retaining the second derivative of B.
    z=sp.symbols('z');v,B=[sp.Function(n)(z) for n in ('v','B')]
    u=v-sp.diff(v,z,2)
    remainder=-sp.diff(B,z)*v*v/2-3*sp.diff(B,z)*sp.diff(v,z)**2/2-sp.diff(B,z,2)*v*sp.diff(v,z)
    flux=B*v*v/2-B*v*sp.diff(v,z,2)+B*sp.diff(v,z)**2/2+sp.diff(B,z)*v*sp.diff(v,z)
    check('Hminus1_scalar_transport_energy_identity',sp.expand(v*B*sp.diff(u,z)-remainder-sp.diff(flux,z))==0)
    vt=1+sp.cos(z)/3;bt=sp.sin(z)
    direct=sp.integrate(vt*bt*sp.diff(vt-sp.diff(vt,z,2),z),(z,0,2*sp.pi))
    paired=sp.integrate(remainder.subs({v:vt,B:bt}).doit(),(z,0,2*sp.pi))
    check('independent_nonconstant_transport_pair',sp.simplify(direct-paired)==0)
    omitted=sp.integrate(sp.diff(bt,z,2)*vt*sp.diff(vt,z),(z,0,2*sp.pi))
    check('omitting_B_second_derivative_rejected',sp.simplify(omitted)==sp.pi/3)
    lam,S,w=[sp.Function(n)(z) for n in ('lam','S','w')];Jf=sp.exp(lam);bf=Jf*(S-w)
    first=sp.diff(lam,z)*(S-w)+sp.diff(S-w,z)
    second=(sp.diff(lam,z,2)*(S-w)+sp.diff(lam,z)*sp.diff(S-w,z)+sp.diff(S-w,z,2))/Jf
    check('adapted_transport_first_derivative',sp.simplify(sp.diff(bf,z)/Jf-first)==0)
    check('adapted_transport_second_derivative',sp.simplify(sp.diff(sp.diff(bf,z)/Jf,z)/Jf-second)==0)

    bounds=mapping['bounds'];j=iv.mpf(lo(decode(bounds['J_lower_binary'])));ju=iv.mpf(hi(decode(bounds['J_upper_binary'])))
    W=iv.mpf(hi(decode(bounds['drift_upper_binary'])));P=iv.mpf(hi(decode(bounds['drift_derivative_upper_binary'])))
    r=iv.mpf(1)/13000;eps=iv.mpf(1)/1000
    env=load('compensated_transport_profiles',FACTORY).prepare();JJ=env['J']
    y,_=env['state'](JJ.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q,vv,dd,shift,shiftz=y[:14],y[14:28],y[28:42],y[42:45],y[45:48]
    N,mu,_,H,_=env['geometry'](q,dd);lie=env['lie'](q,dd,shift,shiftz)
    kv=[(a-b)/(2*N) for a,b in zip(vv[:6],lie[:6])]
    K=[[kv[0],kv[1],kv[2]],[kv[1],kv[3],kv[4]],[kv[2],kv[4],kv[5]]]
    trK=sum((H[i][k]*K[k][i] for i in range(3) for k in range(3)),JJ(0))
    exact=env['env']['env']['exact'];beta=iv.mpf(int(exact['beta'].p))/int(exact['beta'].q)
    normalp=(vv[12]-shift[2]*dd[12])/N
    C=N*(normalp*beta-trK)
    s0,s1,s2=up(shift[2].c[0]),up(shift[2].c[1]),up(2*shift[2].c[2])
    w2=2*eps/31+r*(W+P)
    b1=r*(s0+W)+s1+P
    b2=(r*(s0+W)+r*(s1+P)+s2+w2)/j
    gammaB=3*b1/2+b2/2
    c0,c1=up(C.c[0]),up(C.c[1])/j
    reaction=c0+c1
    scalar_forward=ju*(iv.mpf(max(mp.mpf(1),hi(ju)))+r)/iv.sqrt(j)
    scalar_reverse=(1+r)/(j**mp.mpf('1.5'))
    check('Jacobian_bounds_enclose_positive_normalized_map',0<lo(j)<=1<=hi(ju))
    check('whole_root_transport_and_reaction_coefficients_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for x in (b1,b2,gammaB,reaction,scalar_forward,scalar_reverse)))
    material=[decode(rate['constants_binary']['full_material_rate'][i]) for i in (2,1,3,4)]
    sigma=[decode(x) for x in gauge['canonical_input_constants_binary']['corrective_shift_H1_original']]
    bg=decode(rate['background_compensator_binary'])
    # delta S * Sigma_background,z is controlled weakly, never pointwise.
    source=[scalar_forward*(a+2*bg*b) for a,b in zip(material,sigma)]
    Q=[decode(x) for x in chart['rows_binary']['configuration_H1']]
    Pi=[decode(x) for x in chart['rows_binary']['momentum_L2']]
    out=[source[0]*p+source[1]*q for p,q in zip(Pi,Q)]
    out[0]*=scalar_reverse
    out +=[source[2],source[3]]
    out[0]+=gammaB+reaction
    check('full_source_reaction_transport_chart_constants_finite',all(lo(x)>=0 and mp.isfinite(hi(x)) for x in out))
    check('force_H2_and_harmonic_velocity_controls_retained',hi(out[4])>0 and hi(out[5])>0)
    check('no_Sigma_L2_control_inserted',len(out)==6 and chart['input_order'][0]=='Sigma_Hminus1_original')
    # Exact C*distribution dual pairing needs W1, not a C2 root estimate.
    cf,tf=[sp.Function(n)(z) for n in ('C','test')]
    check('reaction_multiplier_first_derivative_identity',sp.expand(sp.diff(cf*tf,z)-cf*sp.diff(tf,z)-sp.diff(cf,z)*tf)==0)
    check('all_source_sidecar_bytes_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==t for p,(h,t) in snapshot.items()))
    values=dict(adapted_advection_first=b1,adapted_advection_second=b2,advection_log_bound=gammaB,
                reaction_value=c0,reaction_first=c1,reaction_multiplier=reaction,
                scalar_pullback_forward=scalar_forward,scalar_pullback_reverse=scalar_reverse)
    return dict(kind='RTAU_INITIAL_COMPENSATED_DENSITY_HMINUS1_TRANSPORT_V2',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,
                source_sha256=pins,inherited_source_count=len(original),bounds_binary={k:binary(v) for k,v in values.items()},
                density_norm_rate_binary=[binary(x) for x in out],upper_display={k:mp.nstr(hi(v),24) for k,v in values.items()},
                density_norm_rate_upper=[mp.nstr(hi(v),24) for v in out],
                input_order=['Sigma_Hminus1_adapted','Qfree_H1_original','Pfree_L2_original','original_momentum_means_l1','force_configuration_H2_original','harmonic_coordinate_velocity_adapted'],
                scope='INITIAL_DENSITY_SECTOR_LOGARITHMIC_NORM_ON_EXACT_COMPATIBLE_PLANAR_RANGE',
                stronger_density_L2_required=False,full_coupled_physical_energy='NOT_DERIVED',evolving_chart='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
                Rtau_adopted=False,review='DEFERRED',physics_pass=False,gate_effect='NONE')

def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    try:d=calculate()
    except Exception as error:
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=False)
            (args.output.parent/'failure.json').write_text(json.dumps({'status':'FAILED_ATTEMPT','error':repr(error),'source_sha256':sha(Path(__file__)),'physics_pass':False},indent=2)+'\n')
        raise
    raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(raw)
        with Path(str(args.output)+'.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],
                      'density_rate':d['density_norm_rate_upper'],'coefficient_bounds':d['upper_display']},indent=2))
    return 0 if d['passed']==d['total'] else 1

if __name__=='__main__':raise SystemExit(main())
