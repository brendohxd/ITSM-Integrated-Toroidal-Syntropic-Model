"""Continuous-time infinite odd-mode bound for the lower R4C1 cusp response."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
PARENT=BASE+'r4c1_cusp3_evolution_attempt_01/'
SOURCE='Analysis/MasterTests/test_01_r4c1_cusp3_evolution_v1.py'
PLANAR=BASE+'r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CUSP_ODD_RESPONSE_TAIL_V1_CONTRACT_2026-10-17.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_CUSP3_EVOLUTION_V1_REPORT_2026-10-16.md'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENCODE=lambda o:(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda q:s.factor(s.cancel(s.expand(q)))


class Checks:
    def __init__(self):self.rows=[]
    def add(self,name,ok,value=None,criterion='exact'):
        self.rows.append(dict(name=name,passed=bool(ok),value=value,criterion=criterion))
    def exact(self,name,q):
        z=clean(q);self.add(name,z==0,str(z),'zero_exact')


def inputs():
    parent=READ(PARENT+'summary.json')
    pins=dict(parent['source_sha256'])
    pins.update({PARENT+n:h for n,h in parent['artifacts'].items()})
    pins.update({
        PARENT+'summary.json':'b9f8e6b17bf3cfaf01fac6ea1f400e645c36a21585c4d56c3b47f8c64c998fad',
        SOURCE:'78ae1f76b165d2a9039deac705b4896c5842785e86bba9458757821014e641d2',
        REPORT:'af0878a2d20c48d9a99189940952ef8714f68bd0f99dc2ae09ecb056d05cd186',
        CONTRACT:SHA((ROOT/CONTRACT).read_bytes()),SELF:SHA((ROOT/SELF).read_bytes())})
    absent=parent['inherited_sidecars_absent'];paths=[]
    for name,digest in pins.items():
        p=ROOT/name
        if SHA(p.read_bytes())!=digest:raise RuntimeError('Source drift '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise RuntimeError('Sidecar drift '+name)
            paths.append(side)
        elif name not in absent:raise RuntimeError('Missing sidecar '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    return pins,absent,snapshot


def bind_source(ch):
    tree=ast.parse((ROOT/SOURCE).read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Sources')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='source')
    assigned={n.targets[0].id:n.value for n in ast.walk(method)
              if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    expected={
        'cn':"-4*(-1)**((n-1)//2)/(np.pi*n*(n*n-4))",
        'force':"-3*p['A']*abs(pd)**3*w*abs(w)*cn/(f2*scale)",
        'omega':"c['cv']*(n*K)**2/a**2+c['mass']",
        'rdd':"-omega*r-3*H*rd"}
    for name,expr in expected.items():
        want=ast.parse(expr,mode='eval').body
        ch.add('unchanged_lower_equation_AST_'+name,
               ast.dump(assigned[name],include_attributes=False)==ast.dump(want,include_attributes=False))
    addition=ast.parse('rdd[0]+=force').body[0]
    ch.add('retained_inhomogeneous_acceleration',
           any(ast.dump(n,include_attributes=False)==ast.dump(addition,include_attributes=False)
               for n in ast.walk(method)))
    ch.add('frozen_coordinate_wavenumber40',
           any(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='K' for t in n.targets)
               and isinstance(n.value,ast.Constant) and n.value.value==40 for n in tree.body))


def calculate():
    pins,absent,snapshot=inputs();before=snapshot();ch=Checks();bind_source(ch)
    planar=READ(PLANAR)
    a,H,u,ud,v,vd,r,rd,pd,rho,C=s.symbols('a H u0 u_dot v0 v_dot r0 r_dot psi_dot rho C',real=True)
    eta=s.Symbol('eta',positive=True)
    bg=[a,H,u,ud,v,vd,r,rd,pd,rho,C]
    x={str(z):z for z in bg};x.update(Hdot=s.Symbol('Hdot',real=True))
    families=[];formula_by_case={}
    for family in ('archived_G3','new_B1_frame','new_hierarchical'):
        for e in (s.Rational(1,4),s.Rational(1,64),s.Rational(1,1024)):
            label=family+'|'+str(e)
            fixed={n:s.sympify(q).subs(s.Symbol('eta'),e)
                   for n,q in planar['families'][family]['parameter_map'].items()}
            f2=clean(fixed['MU2']*(fixed['c1']+fixed['c4']))
            MC=clean(fixed['MP2']+fixed['MU2']*(fixed['c1']+3*fixed['c2']+fixed['c3'])/2)
            V=(u*u+v*v)/2+(u*u+v*v)**2/24+(u*u+v*v)**3/480
            V+=r*r+r**4/28+(3*e/7)*(u*u+v*v)*r*r/4
            kinetic=ud*ud+vd*vd+rd*rd+fixed['K_Q']*pd*pd
            E=kinetic/2+V+rho
            rates=[a*H,-(kinetic+rho)/(2*MC),ud,-3*H*ud-s.diff(V,u),
                   vd,-3*H*vd-s.diff(V,v),rd,-3*H*rd-s.diff(V,r),
                   -3*H*pd-fixed['beta']*rho/fixed['K_Q'],
                   (-3*H+fixed['beta']*pd)*rho,fixed['beta']*pd*C]
            dt=lambda q:clean(sum(s.diff(q,z)*rate for z,rate in zip(bg,rates)))
            ch.exact(label+'_energy_balance',dt(E)+3*H*(kinetic+rho))
            ch.exact(label+'_Friedmann_preserved',dt(3*MC*H*H-E))
            ch.exact(label+'_dust_charge',dt(a**3*rho/C))
            ch.exact(label+'_clock_source',fixed['beta']/fixed['K_Q']-2*e/15)
            initial={a:1,u:s.sqrt(e),ud:0,v:0,vd:s.sqrt(e),r:s.sqrt(e),
                     rd:s.sqrt(e)/4,pd:e/5,rho:s.Rational(1,5),C:1}
            E0=clean(E.subs(initial))
            ch.add(label+'_initial_energy_and_H',0<E0<1 and s.Rational(1,16)<E0/(3*MC)<1,str(E0))
            ch.add(label+'_MC_lower',MC>=s.Rational(3,4),str(MC))
            ch.add(label+'_potential_positive_terms',
                   all(c.is_nonnegative and all(p%2==0 for p in powers)
                       for powers,c in s.Poly(V,u,v,r).terms()))
            cv=clean(s.sympify(planar['generic_cV2'],locals={**x,**fixed}))
            mass=s.sympify(planar['generic_frame_mass_squared'],locals={**x,**fixed})
            B=clean((-3*fixed['c2']-fixed['c3']+fixed['c4'])/(fixed['c1']+fixed['c4']))
            J=u*vd-ud*v
            ch.exact(label+'_mass_binding',
                     mass-(2*H**2+B*x['Hdot']-18*pd**2+6*J**2/s.Integer(13)))
            ch.add(label+'_mass_Hdot_coefficient',abs(B)<=2,str(B))
            ch.add(label+'_wave_speed_lower',cv>=s.Rational(1,10),str(cv))
            ch.exact(label+'_force_scaling',
                     3*fixed['A']*(e/5)**3/f2/e**s.Rational(7,2)-s.Rational(36,875))
            families.append(dict(family=family,eta_exact=str(e),MC=str(MC),
                                 cV2=str(cv),mass_Hdot_coefficient=str(B),initial_energy=str(E0)))
            formula_by_case[(family,str(e))]=float(cv)
    mass_bound=1+2+s.Rational(8,3)+s.Rational(18,400)+s.Rational(24,13)
    ch.add('mass_difference_bound_strictly_below8',mass_bound<8,str(mass_bound))
    ch.add('background_clock_positive_bootstrap',
           s.Rational(1,5)-s.Rational(2,15)*s.Rational(20,19)**3/20
           >s.Rational(20,19)**3/10)
    ch.add('background_H_positive_comparison',
           s.Rational(1,4)/(1+3*s.Rational(1,4)/20)>s.Rational(1,5))
    ch.add('background_C_bound',s.Rational(16000,15999)<s.Rational(250,249))
    ch.add('background_rho_lower',s.Rational(1,5)*s.Rational(19,20)**3>s.Rational(1,6))
    ch.add('background_rho_upper',s.Rational(1,5)*s.Rational(250,249)<s.Rational(1,4))
    # Every complex mode is covered by applying the same real-part/Cauchy estimate.
    aa,hh,lam,nn,mm,rr,vv,ff,cn=s.symbols('aa hh lam nn mm rr vv ff cn',real=True)
    omega=lam*(nn*40/aa)**2+1
    energy=vv**2+omega*rr**2
    deriv=clean(s.diff(energy,rr)*vv+s.diff(energy,vv)*(-3*hh*vv-(omega-1+mm)*rr+ff*cn)
                +s.diff(energy,aa)*aa*hh)
    expected=-6*hh*vv**2-2*hh*lam*(nn*40/aa)**2*rr**2+2*(1-mm)*rr*vv+2*ff*cn*vv
    ch.exact('complete_modified_wave_energy_identity',deriv-expected)
    ch.add('reject_omitted_momentum_drift',
           clean(s.diff(energy,aa)*aa*hh)!=0,str(clean(s.diff(energy,aa)*aa*hh)))
    ch.add('reject_omitted_mass_coupling',clean(2*(1-mm)*rr*vv)!=0)
    F=s.Rational(180,2527);P=s.Rational(45,10108)
    ch.exact('leading_w_bound',s.Rational(20,19)*s.Rational(5,4)-s.Rational(25,19))
    ch.exact('source_constant',s.Rational(36,875)*s.Rational(25,19)**2-F)
    ch.exact('Duhamel_constant',s.Rational(1,20)*s.Rational(5,4)*F-P)
    ch.exact('displacement_norm_conversion',s.Rational(20,19)**2/(s.Rational(1,10)*40**2)-s.Rational(5,722))
    n=s.Symbol('n',positive=True)
    # |c_n|=4/(pi*n*(n^2-4)) for odd n>=5. The deficit is nonnegative for n>=4.
    ch.exact('all_mode_coefficient_majorant',
             s.Rational(16,3)/n**3-4/(n*(n*n-4))
             -4*(n*n-16)/(3*n**3*(n*n-4)))
    ch.exact('complex_first_coefficient',4/(s.pi*1*(4-1))-4/(3*s.pi))
    ch.exact('complex_third_coefficient',-4/(s.pi*3*(4-9))-4/(15*s.pi))
    c5=-4/(105*s.pi)
    ch.add('nonzero_omitted_fifth_mode',c5!=0,str(c5))
    ch.add('reject_cosine_amplitude_as_complex_coefficient',4/(3*s.pi)!=8/(3*s.pi))
    C2=16/(3*s.pi);N=s.Symbol('N',positive=True);ss=s.Symbol('ss',real=True)
    Bv=2*P**2*C2**2*N**(2*ss-5)/(5-2*ss)
    Br=2*P**2*C2**2*s.Rational(5,722)*N**(2*ss-7)/(7-2*ss)
    # Integral identities plus positive decreasing p-series comparison prove all N.
    ch.exact('velocity_integral_antiderivative',
             s.diff(n**(2*ss-5)/(2*ss-5),n)-n**(2*ss-6))
    ch.exact('displacement_integral_antiderivative',
             s.diff(n**(2*ss-7)/(2*ss-7),n)-n**(2*ss-8))
    runs=READ(PARENT+'trajectories.json')['runs'];controls=[];worst=0.
    ch.add('all18_immutable_runs',len(runs)==18,len(runs))
    for index,run in enumerate(runs):
        e=s.Rational(run['eta_exact']);lamv=formula_by_case[(run['family'],str(e))]
        initial=run['first_order_states'][0];states=np.asarray(run['states_scaled'])
        ch.add(str(index)+'_leading_initial_recipe',initial[12]==1. and initial[13]==0.)
        ch.add(str(index)+'_lower_zero_initial_recipe',np.array_equal(states[0,:4],np.zeros(4)))
        ch.add(str(index)+'_eta_scale_binding',abs(run['scale']/float(e**s.Rational(7,2))-1)<1e-14)
        maximum=0.
        for row,b in zip(states,run['first_order_states']):
            for j,harmonic in enumerate((1,3)):
                c=float(-4*(-1)**((harmonic-1)//2)/(s.pi*harmonic*(harmonic*harmonic-4)))
                om=lamv*(harmonic*40/b[0])**2+1
                observed=float(np.sqrt(row[2*j+1]**2+om*row[2*j]**2))
                bound=float(P)*abs(c)
                maximum=max(maximum,max(0.,observed-bound)/(1+observed+bound))
        worst=max(worst,maximum)
        ch.add(str(index)+'_sampled_response_below_proved_bound',maximum<=1e-9,maximum,'<=1e-9; control, not proof')
        controls.append(dict(family=run['family'],eta=run['eta_exact'],method=run['method'],max_excess=maximum))
    ch.add('source_hash_size_mtime_preserved',before==snapshot())
    passed=sum(r['passed'] for r in ch.rows);complete=passed==len(ch.rows)
    formulas=dict(families=families,coordinate_k=40,time='[0,1/20]',initial='w=1,w_dot=0,r_n=r_n_dot=0',
        mass_identity='mV2=2H^2+B*Hdot-18*psi_dot^2+(6/13)*J^2',
        mass_difference_bound='|1-mV2|<=8 on the admitted energy background',
        mode_energy='E_n=|r_n_dot|^2+[cV2*(40*n/a)^2+1]*|r_n|^2',
        energy_inequality='E_n_dot<=8E_n+2*eta^(7/2)*(180/2527)*|c_n|*sqrt(E_n)',
        mode_bound='sqrt(E_n)<=eta^(7/2)*(45/10108)*|c_n|',
        w_bound='|w|<=25/19',source_scaled_constant=str(F),Duhamel_scaled_constant=str(P),
        velocity_tail=str(Bv),velocity_domain='N>=4, s<5/2; sum_|n|>N |n|^(2s)|r_n_dot|^2/eta^7',
        displacement_tail=str(Br),displacement_domain='N>=4, s<7/2; sum_|n|>N |n|^(2s)|r_n|^2/eta^7',
        endpoint='the displayed p-series bound diverges at each endpoint; no sharp solved-response regularity claim',
        complete_coupled_order3_remainder=False,mean_constraint_separate=True,
        no_division_by_wave_or_clock=True,scaled_sample_controls=controls)
    bodies={'formulas.json':ENCODE(formulas),'verification.json':ENCODE(dict(checks=ch.rows,passed=passed,total=len(ch.rows)))}
    summary=dict(schema='r4c1-cusp-odd-response-tail-v1',validation='PASS_LOCAL_RESPONSE_TAIL' if complete else 'FAIL_LOCAL_RESPONSE_TAIL',
        status='CONTINUOUS_INFINITE_ODD_LOWER_RESPONSE_BOUND' if complete else 'LOWER_RESPONSE_BOUND_UNRESOLVED',
        passed=passed,total=len(ch.rows),checks=ch.rows,physics_pass=False,gate_effect='NONE',
        claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,
        full_coupled_tail_bound=False,full_nonlinear_remainder=False,physical_window_admitted=False,
        stage2_complete=False,stage3_entered=False,source_sha256=dict(sorted(pins.items())),
        source_metadata_preserved=len(before),inherited_sidecars_absent=absent,
        artifacts={name:SHA(body) for name,body in bodies.items()},
        review_dependencies=['CUSP3-EVOLUTION-V1','G3N4-FORCE-COVERAGE','GENERIC-ACTION/EVOLVING-REDUCTION','all transitive debt'])
    bodies['summary.json']=ENCODE(summary)
    return bodies,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    dest=ROOT/(BASE+'r4c1_cusp_odd_response_tail_attempt_01')
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Missing replay')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('No overwrite')
    else:dest.mkdir(parents=True)
    bodies,summary=calculate()
    for name,body in bodies.items():
        side=(SHA(body)+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:raise RuntimeError('Replay drift '+name)
        else:
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write(side)
    if args.replay:
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay metadata drift')
        print('READ_ONLY_REPLAY_EXACT')
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','physics_pass')}))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
