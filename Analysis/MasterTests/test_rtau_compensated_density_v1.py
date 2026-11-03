"""Full-action force Legendre normalization and regulator stress remainder.

Exact initial/operator identities, not a coercive physical energy theorem.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json

import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
SPEC='Theory/Gates/RES-001/RES001_RTAU_COMPENSATED_DENSITY_V1_SPEC_2026-11-03.md'
MANIFEST='Theory/Verification/ITSM_RTAU_PHYSICAL_NORM_V2_INPUTS_2026-11-01.json'
BODY='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
REPAIR='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
MIXED='Analysis/MasterTests/outputs/r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'
DENSITY='Analysis/MasterTests/outputs/rtau_weak_density_row_v2_20261103/receipt.json'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    mp.mp.dps=100;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    original=json.loads((ROOT/MANIFEST).read_text())['source_sha256'];pins=dict(original)
    for rel,h in original.items():assert sha(ROOT/rel)==h,rel
    for rel in (Path(__file__).resolve().relative_to(ROOT).as_posix(),SPEC,MANIFEST,BODY,REPAIR,MIXED,DENSITY,
                'Theory/Gates/RES-001/RES001_RTAU_WEAK_DENSITY_ROW_V2_REPORT_2026-11-03.md',
                'Theory/Gates/RES-001/RES001_R4C1_RTAU_PHYSICAL_NORM_V2_REPORT_2026-10-31.md'):
        pins[rel]=sha(ROOT/rel)
    snapshot={}
    for rel in pins:
        for path in (ROOT/rel,Path(str(ROOT/rel)+'.sha256')):
            if path.exists():snapshot[path]=(sha(path),path.stat().st_mtime_ns)
    check('all_219_original_hashes_match',len(original)==219)
    mixed=json.loads((ROOT/MIXED).read_text());density=json.loads((ROOT/DENSITY).read_text())
    check('owning_mixed_density_controls_pass',all(d['passed']==d['total'] and all(c['passed'] for c in d['checks']) for d in (mixed,density)))
    low=min(mp.mpf(tuple(x)) for x in mixed['rest_gradient_squared_lower'])
    check('actual_prepared_force_Y_strictly_positive',low>0,mp.nstr(low,25))

    tree=ast.parse((ROOT/BODY).read_text(encoding='utf-8-sig'))
    body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='body')
    force=next(n.value for n in body.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='force' for t in n.targets))
    expected=ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body
    check('actual_force_source_retains_frame_and_norm_cubed',ast.dump(force)==ast.dump(expected))
    tainted={'s'}
    for node in body.body:
        if isinstance(node,ast.Assign) and {x.id for x in ast.walk(node.value) if isinstance(x,ast.Name)}&tainted:
            tainted.update(t.id for t in node.targets if isinstance(t,ast.Name))
    check('force_clock_velocity_dependency_isolated',tainted=={'s','gp','Y','force','reg'},sorted(tainted))
    rt=ast.parse((ROOT/REPAIR).read_text())
    cls=next(n for n in rt.body if isinstance(n,ast.ClassDef) and n.name=='ClockGaugeAction')
    fn=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='density')
    reg=next(n.value for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='reg_clock' for t in n.targets))
    check('Rtau_regulator_has_no_temporal_scalar_rate',not ({'ps','zh'}&{x.id for x in ast.walk(reg) if isinstance(x,ast.Name)}))
    final=next(n.value for n in reversed(fn.body) if isinstance(n,ast.Return))
    expected_return=ast.parse('old+N*vol*(reg_clock-temporal),flow',mode='eval').body
    check('old_temporal_regulator_explicitly_removed',ast.dump(final)==ast.dump(expected_return))

    p,s,c,g,w,k,Q,A,b,beta,N,mu,S,v=sp.symbols('p s c gamma w kappa KQ A b beta N mu S v',positive=True)
    Y=c*p*p+2*g*w*p*s+(k+w*w)*s*s
    f=Q*(g*p+w*s)**2/2-A*Y**sp.Rational(3,2)
    fp=Q*g*(g*p+w*s)-3*A*(c*p+g*w*s)*sp.sqrt(Y)
    check('full_force_Legendre_derivative',sp.simplify(sp.diff(f,p)-fp)==0)
    # The coordinate force momentum has one volume factor, not N*mu.
    Lforce=N*mu*f.subs(p,(v-S*s)/N)
    check('canonical_force_momentum_is_mu_times_fp',sp.simplify(sp.diff(Lforce,v)-mu*fp.subs(p,(v-S*s)/N))==0)
    energy=sp.expand(p*fp-f)
    energy_formula=Q*(g*g*p*p-w*w*s*s)/2+A*sp.sqrt(Y)*(Y-3*p*(c*p+g*w*s))
    check('full_force_normal_clock_Legendre_energy',sp.simplify(energy-energy_formula)==0)
    naive=energy.subs({Q:3,A:sp.Rational(2,17),c:sp.Rational(9,16),g:sp.Rational(5,4),w:sp.Rational(3,4),k:1,p:sp.Rational(2,5),s:sp.Rational(1,7)})-sp.Rational(3,2)*sp.Rational(2,5)**2
    check('naive_clock_only_kinetic_energy_rejected',sp.simplify(naive)!=0,str(sp.simplify(naive)))
    rest=energy.subs({c:0,g:1,w:0,s:0})
    check('old_homogeneous_rest_energy_limit_retained',sp.simplify(rest-Q*p*p/2)==0)
    other,Z=sp.symbols('other Z')
    rho=other+f-p*fp-b*Z*Z/2
    sigma=rho+energy+b*Z*Z/2
    check('static_compensated_density_exact_cancellation',sp.simplify(sigma-other)==0)
    rhos=sp.symbols('rho')
    check('observable_change_invertible_in_density',sp.diff(rhos+energy+b*Z*Z/2,rhos)==1)
    sig,trace,work,eo,qflux,dsdt,rs=sp.symbols('Sigma trace work Eother Qflux Dts Rstress')
    fs=sp.diff(f,s)
    chain=N*(beta*p-trace)*(sig-energy-b*Z*Z/2)
    chain+=beta*N*p*energy-N*trace*p*fp-p*qflux/mu-work-fs*dsdt+p*eo/mu
    chain+=rs+b*N*(beta*p-trace)*Z*Z/2
    completed=N*(beta*p-trace)*sig-N*trace*f-p*qflux/mu-work-fs*dsdt+p*eo/mu+rs
    check('full_compensated_material_row_algebra',sp.simplify(sp.expand(chain-completed))==0)

    z,t=sp.symbols('z t',real=True)
    nf,mf,kf,pf,sf,zf,tr,up=[sp.Function(name)(z) for name in ('N','mu','kappa','p','s','Z','trK','Kupzz')]
    T=kf*tr-2*up
    F=b*nf*nf*mf*(zf*kf*sp.diff(pf,z)+zf*T*sf-pf*kf*sp.diff(zf,z))
    Lreg=b*nf*mf*(zf*zf/2-kf*sp.diff(zf,z)*sf+beta*zf*kf*sf*sf)
    Ereg=-beta*Lreg-sp.diff(b*nf*mf*(-kf*sp.diff(zf,z)+2*beta*zf*kf*sf),z)
    check('regulator_Euler_row_from_declared_density',sp.expand(Ereg-(-beta*nf*sp.diff(Lreg,nf)-sp.diff(sp.diff(Lreg,sf),z)))==0)
    DtZ=-nf*tr*zf-sp.diff(mf*nf*T*sf+mf*kf*sp.diff(nf*pf,z),z)/mf
    residual=sp.diff(F,z)/(nf*mf)+pf*Ereg/mf+b*zf*DtZ-b*nf*(beta*pf-tr)*zf*zf/2
    expanded=sp.expand(residual)
    expanded=expanded.subs(sp.diff(nf,z,2),nf*(beta*beta*sf*sf-beta*sp.diff(sf,z)))
    expanded=sp.expand(expanded.subs(sp.diff(nf,z),-beta*nf*sf))
    check('quartic_Zzz_and_pzz_terms_cancel',sp.simplify(expanded.coeff(sp.diff(zf,z,2)))==0 and sp.simplify(expanded.coeff(sp.diff(pf,z,2)))==0)
    secondary=-zf/kf-(sp.diff(mf,z)/mf+sp.diff(kf,z)/kf)*sf
    reduced=sp.factor(sp.cancel(expanded.subs(sp.diff(sf,z),secondary)))
    expected_stress=b*nf*(T*sf*(sp.diff(zf,z)-beta*sf*zf)-tr*zf*zf/2)
    check('complete_regulator_stress_remainder_exact',sp.simplify(sp.expand(reduced-expected_stress))==0)
    check('surviving_Zz_stress_retained',sp.simplify(sp.expand(reduced).coeff(sp.diff(zf,z))-b*nf*T*sf)==0)
    check('fixed_metric_regulator_work_vanishes',sp.simplify(reduced.subs({tr:0,up:0}))==0)
    stress_probe=expected_stress.subs({b:sp.Rational(5,11),beta:sp.Rational(2,5),nf:1,tr:2,up:sp.Rational(1,5),kf:3,sf:sp.Rational(1,7),zf:-sp.Rational(1,11),sp.diff(zf,z):sp.Rational(2,13)})
    check('omitted_metric_regulator_stress_rejected',sp.simplify(stress_probe)!=0,str(sp.simplify(stress_probe)))

    # Independent positive periodic profile; no new physical state is adopted.
    mup=2+sp.sin(z)/7;kap=3+sp.cos(z)/11;psi=sp.sin(z)/13
    ss=sp.diff(psi,z);nn=sp.exp(-beta*psi)
    zz=-sp.diff(mup*kap*ss,z)/mup
    subst={mf:mup,kf:kap,nf:nn,sf:ss,zf:zz,pf:sp.Rational(1,5)+sp.cos(2*z)/17,
           tr:sp.Rational(2,3)+sp.sin(z)/19,up:sp.Rational(1,7)+sp.cos(z)/23}
    direct=residual.subs(subst,simultaneous=True).doit().subs({z:0,beta:sp.Rational(2,5),b:sp.Rational(5,11)})
    stress=expected_stress.subs(subst,simultaneous=True).doit().subs({z:0,beta:sp.Rational(2,5),b:sp.Rational(5,11)})
    check('independent_periodic_profile_stress_identity',sp.simplify(direct-stress)==0)

    # Full metric identities: volume and inverse-metric transport. The
    # transverse shifts and all symmetric metric/extrinsic entries are nonzero.
    h=sp.Matrix([[2,sp.Rational(1,7),sp.Rational(1,11)],[sp.Rational(1,7),3,sp.Rational(1,13)],[sp.Rational(1,11),sp.Rational(1,13),4]])
    hz=sp.Matrix([[1,2,3],[2,4,5],[3,5,6]])/37
    K=sp.Matrix([[3,-2,1],[-2,5,2],[1,2,4]])/17
    shift=sp.Matrix([1,-2,3])/31;shiftz=sp.Matrix([2,1,-1])/41;ez=sp.Matrix([0,0,1]);n0=sp.Rational(7,9)
    lie=shift[2]*hz+(h*shiftz)*ez.T+ez*(h*shiftz).T
    ht=2*n0*K+lie;H=h.inv()
    check('full_metric_volume_transport',sp.simplify(sp.trace(H*ht)/2-n0*sp.trace(H*K)-shift[2]*sp.trace(H*hz)/2-shiftz[2])==0)
    check('full_inverse_metric_transport',sp.simplify(-(H*ht*H)[2,2]+shift[2]*(H*hz*H)[2,2]+2*H[2,2]*shiftz[2]+2*n0*(H*K*H)[2,2])==0)
    # Material derivative commutator and cancellation of coordinate-index terms.
    X,sv=sp.Function('X')(t,z),sp.Function('S')(t,z)
    Dt=lambda x:sp.diff(x,t)-sv*sp.diff(x,z)
    check('material_derivative_spatial_commutator',sp.expand(Dt(sp.diff(X,z))-sp.diff(Dt(X),z)-sp.diff(sv,z)*sp.diff(X,z))==0)
    spr=sp.Function('S')(z)
    inner=mf*((nf*tr+sp.diff(spr,z))*kf*sf+(-2*nf*up-2*kf*sp.diff(spr,z))*sf+kf*(sp.diff(nf*pf,z)+sp.diff(spr,z)*sf))
    check('auxiliary_material_rate_keeps_metric_work',sp.expand(inner-mf*(nf*T*sf+kf*sp.diff(nf*pf,z)))==0)
    check('all_source_bytes_sidecars_and_mtimes_preserved',all(sha(path)==hsh and path.stat().st_mtime_ns==stamp for path,(hsh,stamp) in snapshot.items()))
    return dict(kind='RTAU_ACTION_COMPENSATED_DENSITY_V1',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,
                formulas={
                    'force_f':str(f),'force_fp':str(fp),'force_Legendre_energy':str(energy_formula),
                    'compensated_density':'Sigma=rho+(p*f_p-f)+b*Z^2/2',
                    'regulator_stress_remainder':str(expected_stress),
                    'full_material_row':'Dt Sigma=N*(beta*p-trK)*Sigma-N*trK*f-(p/mu)*Dz(N*mu*f_s)-f_s*((N*p)_z+S_z*s)-W_f+(p/mu)*E_other+R_stress+Ward_defect/(N*mu)',
                    'force_work':'W_f=sum_metric_frame(f_q*Dt q), holding normal p and spatial s fixed',
                    'other_Euler':'E_other=L_other,psi-Dz(L_other,psi_z), all frame/metric/matter/lapse sectors retained'},
                source_sha256=pins,inherited_source_count=len(original),
                scope='EXACT_PLANAR_FORCE_NORMALIZATION_AND_HIGHEST_REGULATOR_CANCELLATION',
                fourth_order_regulator_terms='CANCEL_IN_COMPENSATED_ROW',remaining_metric_stress='RETAINED_NOT_ZERO',
                quantitative_compensated_rate='NOT_ESTABLISHED',physical_energy='NOT_DERIVED',actual_time_tube='NOT_ESTABLISHED',
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
                         regulator_stress=receipt['formulas']['regulator_stress_remainder']),indent=2))
    return 0 if receipt['passed']==receipt['total'] else 1


if __name__=='__main__':raise SystemExit(main())
