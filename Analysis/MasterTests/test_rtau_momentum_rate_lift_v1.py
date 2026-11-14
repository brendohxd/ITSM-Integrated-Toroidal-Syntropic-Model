"""H1 remainder in the actual constraint momentum lift; rate bundle open."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_MOMENTUM_RATE_LIFT_V1_SPEC_2026-11-04.md'
LIFT='Analysis/MasterTests/outputs/rtau_strong_constraint_lift_v2_20261104/receipt.json'
FORCE='Analysis/MasterTests/outputs/rtau_strong_force_coordinate_v2_20261104/receipt.json'
RATES='Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json'
FACTORY='Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calculate():
    mp.mp.dps=100;mp.iv.dps=60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    up=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(t)) for t in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    norm=lambda xs:iv.sqrt(sum((up(x)**2 for x in xs),iv.mpf(0)))
    lift,force,rates=[json.loads((ROOT/p).read_text()) for p in (LIFT,FORCE,RATES)]
    pins=dict(force['source_sha256'])
    for rel in (SPEC,LIFT,FORCE,RATES,FACTORY,Path(__file__).resolve().relative_to(ROOT).as_posix()):pins[rel]=sha(ROOT/rel)
    snapshots={}
    for rel,h in pins.items():
        p=ROOT/rel;assert sha(p)==h,rel
        for q in (p,Path(str(p)+'.sha256')):
            if q.exists():snapshots[q]=(sha(q),q.stat().st_mtime_ns)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    check('strong_reconstruction_parents_complete_in_scope',lift['passed']==lift['total']==79 and force['passed']==force['total']==20)
    spec=importlib.util.spec_from_file_location('momentum_lift_profile_factory',ROOT/FACTORY)
    fac=importlib.util.module_from_spec(spec);spec.loader.exec_module(fac);env=fac.prepare()
    y,_=env['state'](env['J'].variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    p=[decode(x) for x in rates['background_binary']['momentum']]
    pz=[decode(x) for x in rates['background_binary']['momentum_z']]
    qznorm=norm([x.c[0] for x in y[28:41]]);pnorm=norm(p)
    F=[decode(x) for x in force['constants_binary']['force_H2_inverse']]
    trace=[decode(x) for x in force['constants_binary']['trace_H1_after_force_inverse']]
    def compose(row):
        row=[decode(x) for x in row]
        base=[row[j] for j in (0,1,2)]+[iv.mpf(0),iv.mpf(0)]+[row[j] for j in (4,5,6)]
        return [x+row[3]*f for x,f in zip(base,F)]
    eliminated=[compose(lift['constants_binary'][key]) for key in ('eliminated_px_L2','eliminated_py_L2','eliminated_pz_L2')]
    r=iv.mpf(1)/13000;trace_factor=iv.sqrt(2)*iv.exp(2*r)*(1+2*r)
    Q=[trace_factor*t+f for t,f in zip(trace,F)];Q[1]+=1
    P=[sum((row[j] for row in eliminated),iv.mpf(0)) for j in range(8)];P[2]+=1
    z=sp.symbols('z');m,V,b,pc,kq,rr=[sp.Function(s)(z) for s in ('m','V','b','pc','kq','r')]
    residual=sp.diff(m*b-V*pc+kq,z)-rr
    rem=b-V*pc/m
    check('exact_variable_coefficient_constraint_identity',sp.expand(residual-(sp.diff(m*rem+kq,z)-rr))==0)
    # Constant integration partner is fixed by the original momentum mean.
    eta,mean_lpc,mean_ukq,mean_ur,mean_u=sp.symbols('eta ml mk mr mu')
    const=(eta-mean_lpc+mean_ukq-mean_ur)/mean_u
    check('retained_weighted_mean_constant_exact',sp.expand(mean_lpc-mean_ukq+mean_ur+mean_u*const-eta)==0)
    n=sp.symbols('n',integer=True,positive=True)
    check('primitive_L2_to_H1_all_harmonics',sp.expand(2*n*n-(1+n*n))==n*n-1)
    ell=sp.Rational(1,37)
    check('omitted_leading_frame_lift_unbounded_in_H1',sp.limit((1+n*n)*ell**2/n**2,n,sp.oo)==ell**2)
    # Variable coefficient/nonzero mean fixture: choose R and compute the
    # complete constraint source without a finite Fourier projection.
    mm=2+sp.sin(z)/9;vv=sp.cos(2*z)/11;pp=3+sp.sin(3*z)/13;R=5+sp.cos(z)/17;K=sp.sin(2*z)/19
    bb=vv*pp/mm+R;source=sp.diff(mm*R+K,z)
    check('independent_nonconstant_constraint_fixture',sp.simplify(sp.diff(mm*bb-vv*pp+K,z)-source)==0)
    check('fixture_retains_nonzero_constant_partner',sp.integrate(source,(z,-sp.pi,sp.pi))==0 and R.subs(z,0)!=0)
    rows=[];details=[]
    # K_i(delta q)=delta B_i^T*p_background. Nonzero metric slots and the
    # independent-frame Vz slot come directly from the canonical generator.
    entries=[[(0,2,1),(1,4,1),(2,5,2),(8,6,-1)],[(1,2,1),(3,4,1),(4,5,2),(8,7,-1)],[(2,2,1),(4,4,1),(5,5,2),(8,8,-1)]]
    for i,terms in enumerate(entries):
        kv=[iv.mpf(0)]*13;kz=[iv.mpf(0)]*13
        for qslot,pslot,mult in terms:kv[qslot]+=p[pslot]*mult;kz[qslot]+=pz[pslot]*mult
        k0,k1=norm(kv),norm(kz)
        mj=y[0]*(2 if i==2 else 1);uj=1/mj;lj=y[8]/mj
        u0,u1=up(uj.c[0]),up(uj.c[1]);uH=u0+u1
        assert lo(uj.c[0])>0
        denom=1/iv.mpf(lo(uj.c[0]));ell0=up(lj.c[0])
        cq=uH*(k0+k1+denom*u0*k0)
        cp=uH*denom*ell0
        if i==2:
            cq+=uH*(iv.sqrt(2)+denom*u0)*pnorm
            cp+=uH*(iv.sqrt(2)+denom*u0)*qznorm
        row=[cq*q+cp*pp for q,pp in zip(Q,P)]
        row[5+i]+=uH*denom
        rows.append(row)
        check('finite_H1_momentum_lift_constants_'+str(i),all(lo(v)>=0 and mp.isfinite(hi(v)) for v in row))
        details.append(dict(K_value=binary(k0),K_derivative=binary(k1),inverse_weight=binary(u0),inverse_weight_derivative=binary(u1),leading_frame_ratio=binary(lj.c[0])))
    check('all_sources_sidecars_timestamps_preserved',all(sha(p)==h and p.stat().st_mtime_ns==tm for p,(h,tm) in snapshots.items()))
    return dict(kind='RTAU_MOMENTUM_RATE_LIFT_V1',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,source_sha256=pins,
      input_order=force['inverse_input_order'],constants_binary={'full_configuration_H1':[binary(x) for x in Q],'full_momentum_L2':[binary(x) for x in P],'eliminated_momentum_principal_remainder_H1':[[binary(x) for x in row] for row in rows]},
      upper_display={'eliminated_momentum_principal_remainder_H1':[[mp.nstr(hi(x),26) for x in row] for row in rows]},coefficient_details=details,
      principal_lift='p_hxz=(Vz/a^2)*p_Vx+Rx; p_hyz=(Vz/a^2)*p_Vy+Ry; p_hzz=(Vz/(2*a^2))*p_Vz+Rz',
      compatible_domain='Original exact momentum constraints, weighted longitudinal compatibility, retained means and both charges; not arbitrary tuples',
      scope='INITIAL_H1_REMAINDER_IN_THE_ACTUAL_CONSTRAINT_MOMENTUM_LIFT_ONLY',full_actual_generator='NOT_ASSEMBLED',actual_time_tube='NOT_ESTABLISHED',review='DEFERRED',physics_pass=False,gate_effect='NONE',Rtau_adopted=False,G1_G6='INCOMPLETE')
def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--output',type=Path);group.add_argument('--verify',type=Path);args=parser.parse_args()
    if args.output:assert not args.output.parent.exists()
    d=calculate();raw=(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=False);args.output.write_bytes(raw);Path(str(args.output)+'.sha256').write_text(sha(args.output)+'\n')
    else:assert args.verify.read_bytes()==raw,'Immutable replay differs'
    print(json.dumps({'passed':d['passed'],'total':d['total'],'failed':[c for c in d['checks'] if not c['passed']],'physics_pass':False}))
    if d['passed']!=d['total']:raise SystemExit(1)
if __name__=='__main__':main()
