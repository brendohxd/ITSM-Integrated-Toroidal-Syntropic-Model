"""Distinct exact background-lifespan and generic principal/norm controls."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v2_attempt_01/summary.json'
PSHA='2a4e72ceef0a7681c8ee3fc38028d9dcb86b2ebd9999af6b0bdb58b0a3e80533'
OLD='Analysis/MasterTests/outputs/r4c1_rtau_physical_norm_v1_attempt_01/summary.json'
ORIGINAL='Analysis/MasterTests/outputs/r4c1_two_repair_characteristics_v3_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_RTAU_NORM_EXTENSION_V1_CONTRACT_2026-10-31.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda z:(json.dumps(z,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def calculate():
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    d=json.loads((ROOT/PARENT).read_bytes());assert d['passed']==d['total']==58
    pins=dict(d['source_sha256']);pins[PARENT]=PSHA
    for path in (SELF,OLD,CONTRACT,ORIGINAL):pins[path]=SHA((ROOT/path).read_bytes())
    snapshots={}
    for path,want in pins.items():
        f=ROOT/path;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,path
        for p in (f,sc):snapshots[p.relative_to(ROOT).as_posix()]=(SHA(p.read_bytes()),p.stat().st_mtime_ns)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,mat):check(name,all(s.simplify(z)==0 for z in mat))
    old=json.loads((ROOT/OLD).read_bytes())
    keys=set(d)-{'checks','source_sha256','kind','passed'}
    check('all_V1_V2_scientific_exports_identical',all(old[k]==d[k] for k in keys),len(keys))
    bad=[z for z in old['checks'] if not z['passed']]
    check('old_failure_retained_only_trace_slice',len(bad)==1 and bad[0]['name']=='trace_frame_trace_below_110',bad)
    # Extend the certified box inclusion using the actual density equation.
    row=next(z['value'] for z in d['checks'] if z['name']=='background_box_strict_exit_bound')
    bounds=[s.sympify(z) for z in row['flow_bounds']]
    margins=[s.sympify(z) for z in row['margins']]
    time=s.Rational(1,20)
    for j in range(10):check('background_coordinate_'+str(j)+'_strict_exit_control',bounds[j]*time<margins[j])
    rate=s.Rational(34,5);x=rate*time;rh0=s.Rational(1,5)
    check('positive_density_exponential_control_domain',0<=x<1,str(x))
    lower=rh0*(1-x);upper=rh0/(1-x)
    check('positive_density_stays_strictly_in_same_box',s.Rational(1,20)<lower<=upper<2,[str(lower),str(upper)])
    original=json.loads((ROOT/ORIGINAL).read_bytes())
    # Same symbol identities as the source, including positive a and kappa.
    names=d['variables'];loc={z:s.Symbol(z,real=True) for z in names};loc['a']=s.Symbol('a',positive=True)
    kap=s.Symbol('kappa',positive=True);loc['kappa']=kap
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=loc) for z in row] for row in rows])
    u,v=loc['u'],loc['v'];H=loc['H']
    A1=parse(d['scalar']['A1']);A2=parse(d['scalar']['A2']);E=parse(d['scalar']['energy_form'])
    ix=list(range(5))+list(range(6,11));A=A1.extract(ix,ix);lam=s.Symbol('lambda')
    poly=s.factor(A.charpoly(lam).as_expr())
    expected=lam**2*(lam**2+s.Rational(1,3))*(lam**2+1)**2*(lam**2+1+(u*u+v*v)/13)
    check('generic_ordinary_full_characteristic_polynomial',s.expand(poly-expected)==0,str(poly))
    ker=s.zeros(10,2);ker[0,0]=1;ker[1,1]=1;ker[5,1]=2*s.I/33
    zero('two_physical_zero_vectors_retained',A*ker)
    check('two_zero_vectors_independent',ker.rank()==2)
    keep=[i for i in range(10) if i not in (0,1)]
    minor=s.factor(A.extract(keep,keep).det())
    check('ordinary_rank_eight_on_entire_real_box',s.simplify(minor+(13+u*u+v*v)/429)==0,str(minor))
    zero('independent_full_principal_energy_identity_A1',A1.conjugate().T*E+E*A1)
    zero('independent_full_principal_energy_identity_A2',A2.conjugate().T*E+E*A2)
    check('fixed_positive_energy_rate_formula',s.sympify(d['scalar']['energy_growth_rate'])==
          330*(s.Rational(16,13)+220*s.sympify(d['scalar']['remainder_norm_bound'])))
    # Map the old limiting Jordan chain, rather than discarding its matter density.
    initial={loc[z]:s.sympify(value) for z,value in original['initial'].items()}
    T=parse(d['scalar']['T']).subs(initial);ev=E.subs(initial)
    e=s.zeros(12,1);e[1]=1/kap
    g=s.zeros(12,1);g[0]=2*s.I/kap;g[7]=1
    ye=T*e;yg=T*g
    ee=s.simplify((ye.conjugate().T*ev*ye)[0]);eg=s.simplify((yg.conjugate().T*ev*yg)[0])
    eg_lead=s.simplify(s.limit(eg/kap**2,kap,s.oo));ee_limit=s.simplify(s.limit(ee,kap,s.oo))
    check('old_generalized_chain_has_physical_density_cost',eg_lead==s.Rational(121,36),str(eg_lead))
    check('old_zero_vector_physical_norm_stays_finite',ee_limit.is_finite and ee_limit>0,str(ee_limit))
    check('nonzero_density_not_silently_set_to_zero',s.simplify(yg[0]-11*s.I*kap/6)==0,str(yg[0]))
    for path,(digest,mtime) in snapshots.items():
        f=ROOT/path;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,path
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    return dict(kind='R4C1_RTAU_NORM_EXTENSION_V1',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,
        source_sha256=pins,time_interval=['0','1/20'],rho_bound=[str(lower),str(upper)],
        generic_ordinary_characteristic_polynomial=str(poly),ordinary_nonzero_minor=str(minor),
        old_chain_physical_energy=str(eg),old_zero_vector_physical_energy=str(ee),
        scalar_energy_growth_rate=d['scalar']['energy_growth_rate'],
        validity='linear control estimate for the registered planar mode family and separate homogeneous mode; same background box and kappa>=1/2',
        numerical_accuracy_certified=False,nonlinear_Cauchy_theorem=False,physical_window_demonstrated=False,
        canonical_parent_adopted=False,review='DEFERRED',Rule9_cleared=False,physics_pass=False,gate_effect='NONE',G1_G6='INCOMPLETE')

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path);args=ap.parse_args()
    result=calculate();data=ENC(result)
    if args.replay:
        assert args.replay.read_bytes()==data,'immutable replay differs';print('READ_ONLY_REPLAY_EXACT',SHA(data))
    else:
        args.output_dir.mkdir(parents=True,exist_ok=False);p=args.output_dir/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=result['passed'],total=result['total'],physics_pass=False,receipt=str(p))))
    return 0 if result['passed']==result['total'] else 1

if __name__=='__main__':raise SystemExit(main())
