"""Complete initial nodal current bounds; no time-dependent weak admission."""
import argparse,ast,hashlib,importlib.util,inspect,json,types
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_weighted_node_v1_attempt_01/summary.json'
PSHA='bfc845002c91896139f2b9bbe1eb4cd6b138db755134e00e1287ce6a034b34e3'
POLE='Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v2_attempt_01/summary.json'
TIME='Analysis/MasterTests/outputs/r4c1_time_tangent_v1_attempt_01/summary.json'
CLOCK='Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json'
SCALAR='Analysis/MasterTests/outputs/r4c1_quartic_scalar_bound_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FULL_NODE_CURRENT_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_WEIGHTED_NODE_V1_REPORT_2026-10-29.md'
ENGINE='Analysis/MasterTests/test_01_r4c1_auxiliary_pole_v2.py'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)
norm=lambda x:max(abs(v) for v in x)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def calculate():
    mp.mp.dps=140;mp.iv.dps=80;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,expr):check(name,s.factor(s.cancel(expr))==0,str(s.factor(s.cancel(expr))))
    def close(name,error):check(name,error<mp.mpf('1e-18'),show(error))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,REPORT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            assert SHA(file.read_bytes())==want and Path(str(file)+'.sha256').read_text().split()[0].lower()==want,path
    verify();en=load('node_current_bounds',ENGINE);disk=load('node_current_disk',en.DISK)
    ch=en.load('node_current_registered',en.CHARGE);ch.setup();mp.mp.dps=140
    backend=load('node_current_original_full_action',BACKEND);body=ch.en.body
    eta=s.Symbol('eta');par={key:s.sympify(v,locals={'eta':eta}).subs(eta,s.Rational(1,4))
        for key,v in READ(en.PLANAR)['families']['new_B1_frame']['parameter_map'].items()}
    tree=ast.parse((ROOT/body.canonical.BG).read_text(encoding='utf-8-sig'))
    call=next(t.value for t in tree.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='PARAMS' for z in t.targets))
    shared={v.arg:s.Rational(s.sympify(ast.unparse(v.value))) for v in call.keywords}
    par.update(m2=shared['m2'],lambda4=shared['l4'],lambda6=shared['l6'],Lambda=shared['cutoff'],
        mr2=shared['mr2'],lambda_r=shared['lr'],g_r=shared['gr']/4,rho_Lambda=shared['vacuum'])
    exact={key:en.rational(value) for key,value in par.items()};check('all_majorant_parameters_exact',all(v.is_Rational for v in par.values()))
    # Exact partitions of original code; curvature, lapse and lapse gradient remain.
    local=ast.parse(inspect.getsource(body.body));fun=local.body[0]
    force=next(t for t in fun.body if isinstance(t,ast.Assign) and any(isinstance(z,ast.Name) and z.id=='force' for z in t.targets))
    assert ast.dump(force.value)==ast.dump(ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body)
    force.value=force.value.left;fun.name='node_current_analytic_body';ast.fix_missing_locations(local)
    exec(compile(local,'<original-analytic-current-partition>','exec'),body.__dict__)
    full=ast.parse(inspect.getsource(backend.WeakAction.density).strip());ff=full.body[0]
    assignments={t.targets[0].id:t for t in ff.body if isinstance(t,ast.Assign) and len(t.targets)==1 and isinstance(t.targets[0],ast.Name)}
    assert ast.dump(assignments['dust'].value)==ast.dump(ast.parse("-q[15]*(C*C*(-tauhat*tauhat+hi[2][2]*d[14]**2)+C**4)/2",mode='eval').body)
    check('conformal_factor_used_only_for_dust',sum(isinstance(t,ast.Name) and t.id=='C' and isinstance(t.ctx,ast.Load) for t in ast.walk(ff))==3)
    assignments['C'].value=ast.Constant(1);assignments['dust'].value=ast.Constant(0)
    ff.name='node_current_analytic_density';ast.fix_missing_locations(full)
    exec(compile(full,'<original-physical-density-excluding-separate-dust>','exec'),backend.__dict__)
    oldbody,oldsqrt=body.body,body.sqrt
    try:
        body.body=body.node_current_analytic_body
        body.sqrt=lambda x:x.sqrt() if isinstance(x,disk.Disk) else oldsqrt(x)
        weak=backend.WeakAction(body,exact);weak.density=types.MethodType(backend.node_current_analytic_density,weak)
        q=disk.initial_polydisc();delta=F(1,1000)
        jets=q[:14]+[disk.Disk(0,delta),disk.Disk(0,delta)]+q[14:28]+[disk.Disk(1,delta),disk.Disk(0,delta)]
        jets+=q[28:42]+[disk.Disk(0,delta),disk.Disk(0,delta)]+q[42:48]+[disk.Disk(1,delta),disk.Disk(0,delta)]
        disk.reset();majorant=disk.summary(weak.density(jets)[0])
    finally:body.body=oldbody;body.sqrt=oldsqrt
    check('full_56_density_complex_domains_safe',F(majorant['minimum_inverse_margin'])>0 and F(majorant['minimum_sqrt_margin'])>0)
    Baction=F(majorant['integer_upper']);H2=2*Baction/delta**2;H3=6*Baction/delta**3
    po=READ(POLE);env={key:F(v) for key,v in po['envelopes'].items()};r=F(1,1000)
    K,A,b,beta,p=F(3,4),F(1,28),F(5,44),F(1,40),F(1,20)
    T,Tz,Rp,Rpp,wp,az,amax=F(21,100000),F(1,20),F(9,1000000),F(1,1000),F(2,25),F(13,1000),F(13,100)
    scalar=READ(SCALAR)['bounds']
    check('both_analytic_and_physical_auxiliary_accelerations_below_3200',all(en.upper(scalar[q])<3200 for q in ('aZ_analytic','aZ_full')))
    check('both_complement_acceleration_bounds_below_30',all(en.upper(scalar[q])<30 for q in ('complement_analytic_acceleration','complement_full_acceleration')))
    check('effective_time_direction_l1_below_4000',32+12*30+amax+3200+1<4000 and abs(ch.en.vals['rd'])<2)
    # The coefficient drift only needs q,S,N gradients: analytic first-jet
    # Hessians in derivative slots are independent of derivative-slot values.
    check('B1_transverse_shift_coarse_envelope',exact['c1']+exact['c3']==0 and exact['MP2']>=1
          and all(abs(exact[q])<=1 for q in ('MU2','c3','c4'))
          and 1-2*r*r-2*(1+r*r)*r*r>F(9,10) and 2*r*r*wp/F(9,10)<1)
    check('coefficient_spatial_drift_l1_envelope',wp+2*r*(1+76*r*r)*wp+3<20)
    Da=12*env['Ma']*r+env['Mz'];J=3*T*wp+Rp;Jz=3*Tz*wp+3*T*1600*r+Rpp
    Drho=2*A*p**3;Fcur=p*p*(6+3)+2*p*amax
    cub_flux_dz=3*A*(4*wp*T*Fcur+r*(Tz*Fcur+2*p*T*az))
    dust_flux_dz=Drho*(4*wp*T*J+r*(Tz*J+T*Jz))
    bounds={
      'spatial_flux_initial_over_absw3':3*A*p*p*T*r+Drho*T*r,
      'spatial_flux_time_over_w2':12*H2*env['Ma']+r*r*(b*T*env['Mz']+3*A*T*Fcur+Drho*T*J),
      'spatial_flux_time_normal_over_absw':240*H3*env['Ma']*r+12*H2*env['Md']+r*r*(
          b*(3*wp*T*env['Mz']+r*Tz*env['Mz']+T*env['Mzz'])+cub_flux_dz+dust_flux_dz),
      'local_source_time_over_absw':H2*Da+r*max(3*A*p*p*(3*amax+p*(6+2)),
          2*A*p*p*(3*amax+p*(4+3))*r,2*A*p*p*(3*amax+p*(6+3))*r)+Drho*(J+beta*p)*r*r,
      'temporal_current_second_time_over_absw':F(parent['uniform_weighted_jerk_bound'])+6*A*p*env['JF']*r**3+
          H2*(Da+12*env['Md'])+b*T*env['Mzz']*r*r+8000*H3*Da+
          (F(po['remainder_pieces']['cubic'])+cub_flux_dz+Drho*(J*J+r*T*Jz))*r*r,
    }
    check('uniform_current_bounds_finite_positive',all(v>0 for v in bounds.values()))
    # Exact off-node identities and normal traces; no distribution extension.
    w,tt,wwp,pp,aa,H,HB,aaz,ttz,rrp,rrpp=s.symbols('w T wp p aPsi H HB aPsi_z T_z Rp Rpp',real=True)
    amp=s.Rational(1,28);bn=s.Rational(5,44);pn=s.Rational(1,20)
    cubic_flux_t=3*amp*tt*w**3*s.Abs(w)*(pp**2*(6*H-3*HB)+2*pp*aa)
    # Normal differentiation off the two node orientations is retained exactly.
    for sign in (-1,1):
        pos=cubic_flux_t.subs(s.Abs(w),sign*w)
        normal=s.diff(pos,w)*wwp+s.diff(pos,tt)*ttz+s.diff(pos,aa)*aaz
        expected=3*amp*((4*sign*w**3*wwp*tt+w**3*sign*w*ttz)*(pp**2*(6*H-3*HB)+2*pp*aa)+2*pp*tt*w**3*sign*w*aaz)
        zero('exact_cubic_spatial_flux_normal_branch_'+str(sign),normal-expected)
    # The twenty-row auxiliary-jerk column has no constraint or clock entry.
    full_column=s.zeros(20,1);full_column[12]=-bn*w*w
    temporal_column=s.zeros(20,1);temporal_column[12]=-bn*w*w
    spatial_column=s.zeros(20,1);spatial_column[12]=bn*w**3*tt
    test=s.Function('test')(w)
    for order in (0,1):
        check('full_twenty_time_tangent_column_kernel_'+str(order),all(s.diff(v*test,w,order).subs(w,0)==0 for v in full_column))
        check('both_canonical_current_columns_kernel_'+str(order),all(s.diff(v*test,w,order).subs(w,0)==0 for v in list(temporal_column)+list(spatial_column)))
    # Reuse original six profiles; newly differentiate complete currents and
    # all20 source/flux rows, retaining multiplier/clock conversion and jets.
    time=READ(TIME);points={}
    for name in time['file_sha256']:
        row=READ((Path(TIME).parent/name).as_posix());points.setdefault(row['label'],{})[row['partition_lambda']]=row
    exports=[];original_A=ch.en.par['A']
    for row in READ(CLOCK)['points']:
        raw=READ(row['raw_point_source']);base=list(map(mp.mpf,raw['original_first_jet']));u=abs(base[7]);wv=base[7];pv=base[28]
        rho_delta=2*original_A*pv**3*u**3;rho_z_delta=6*original_A*pv**3*mp.sign(wv)*u*u*base[39]
        current_data={}
        for part in (0,1):
            actual=points[row['label']][part];parnum=dict(ch.en.par);parnum['A']=original_A*part
            weak=backend.WeakAction(body,parnum);jet=mp.matrix(base);jet[15]-=(1-part)*rho_delta
            dt=mp.matrix(list(map(mp.mpf,row['complete_time_direction'])));dz=mp.matrix(list(map(mp.mpf,row['complete_spatial_direction'])))
            for j,v in enumerate(actual['actual_fourteen_accelerations']):dt[16+j]=mp.mpf(v)
            dt[15]=mp.mpf(actual['multiplier_rate']);dz[15]-=(1-part)*rho_z_delta
            _,g=weak.gradient(jet);gt=weak.hv(jet,dt,mp.mpf('1e-26'));gz=weak.hv(jet,dz,mp.mpf('1e-26'))
            src=mp.matrix(list(g[:16,0])+list(g[48:51,0])+[g[54]])
            pt=mp.matrix(list(g[16:32,0])+[mp.mpf(0)]*4)
            pz=mp.matrix(list(g[32:48,0])+list(g[51:54,0])+[g[55]])
            ptt=mp.matrix(list(gt[16:32,0])+[mp.mpf(0)]*4)
            pzt=mp.matrix(list(gt[32:48,0])+list(gt[51:54,0])+[gt[55]])
            et=src-ptt-mp.matrix(list(gz[32:48,0])+list(gz[51:54,0])+[gz[55]])
            close('complete_twenty_initial_balance_'+row['label']+'_lambda'+str(part),norm(et)/(1+norm(src)+norm(ptt)))
            dtt=mp.matrix(56,1)
            for j,v in enumerate(actual['actual_fourteen_accelerations']):dtt[j]=mp.mpf(v)
            dtt[14]=parnum['beta']*pv;dtt[15]=mp.mpf(actual['second_multiplier_time_jet'])
            for j,v in enumerate(actual['actual_fourteen_third_time_jets']):dtt[16+j]=mp.mpf(v)
            dtt[30]=mp.mpf(actual['third_clock_time_jet'])
            for j,v in enumerate(actual['actual_acceleration_spatial_derivative']):dtt[32+j]=mp.mpf(v)
            # Only the clock current needs an independently differentiated
            # second-time value; other second-current bounds use exact sources.
            clock2=[]
            for eps in ('1e-18','1e-22'):
                h=mp.mpf(eps)/(1+norm(dt)+norm(dtt))
                gp=weak.gradient(jet+h*dt+h*h*dtt/2)[1]
                gm=weak.gradient(jet-h*dt+h*h*dtt/2)[1]
                clock2.append((gp[30]-2*g[30]+gm[30])/(h*h))
            close('clock_second_current_steps_'+row['label']+'_lambda'+str(part),abs(clock2[0]-clock2[1])/(1+abs(clock2[-1])))
            current_data[part]=dict(source=src,temporal=pt,spatial=pz,temporal_time=ptt,spatial_time=pzt,clock_second=clock2[-1])
            exports.append(dict(label=row['label'],partition=part,source20=list(map(show,src)),temporal20=list(map(show,pt)),
                spatial20=list(map(show,pz)),temporal_time20=list(map(show,ptt)),spatial_time20=list(map(show,pzt)),
                clock_second_time=show(clock2[-1]),nonzero_Euler20=list(map(show,et))))
        delta_current={key:current_data[1][key]-current_data[0][key] for key in current_data[0]}
        tv=base[50]/wv;rpv=base[53];wpv=base[39];hh=ch.en.H;hb=ch.en.vals['H0'];ap=mp.mpf(points[row['label']][1]['actual_fourteen_accelerations'][12])
        expected=3*original_A*tv*wv**3*u*(pv**2*(6*hh-3*hb)+2*pv*ap)
        # Analytic current differences enter too; isolate the cubic current
        # by its exact Hessian coefficient in the separately checked formula.
        close('clock_initial_current_partition_'+row['label'],abs(delta_current['temporal'][14]-rho_delta)/(abs(rho_delta)+mp.mpf('1e-100')))
        jv=3*tv*wpv+rpv;expected_clock_t=rho_delta*jv
        close('clock_time_current_partition_'+row['label'],abs(delta_current['temporal_time'][14]-expected_clock_t)/(abs(expected_clock_t)+mp.mpf('1e-100')))
        tpv=(rpv*wv-base[50]*wpv)/wv**2
        rpp=mp.mpf(raw['original_spatial_auxiliary_inputs']['shift_second_spatial'][2])
        jzv=3*tpv*wpv-4800*tv*wv+rpp
        expected_clock_tt=rho_delta*(jv*jv+wv*tv*jzv)
        close('clock_second_current_partition_'+row['label'],abs(delta_current['clock_second']-expected_clock_tt)/(abs(expected_clock_tt)+mp.mpf('1e-100')))
        if u<=mp.mpf('0.001'):
            bnval=lambda x:mp.mpf(x.numerator)/x.denominator
            check('uniform_spatial_current_trace_'+row['label'],norm(delta_current['spatial'])<=bnval(bounds['spatial_flux_initial_over_absw3'])*u**3)
            check('uniform_spatial_current_time_trace_'+row['label'],norm(delta_current['spatial_time'])<=bnval(bounds['spatial_flux_time_over_w2'])*u*u)
        # Original full-Hessian auxiliary column includes all clock, shift,
        # lapse and spatial-current directions, rather than the physical14 only.
        hess=raw['full_Hessian'];hcol=[mp.mpf(hess[i][29]) for i in range(56)]
        expected_col=[mp.mpf(0)]*56;expected_col[28]=-parnum['b']*wv*wv;expected_col[44]=parnum['b']*wv**2*base[50]
        close('complete_current_auxiliary_column_'+row['label'],max(abs(hcol[i]-expected_col[i]) for i in list(range(16,48))+list(range(51,54))+[55]))
    verify()
    return dict(result_id='R4C1-FULL-NODE-CURRENT-V1',source_sha256=pins,checks=checks,majorant=majorant,
        cauchy=dict(action_bound=str(Baction),radius=str(delta),second=str(H2),third=str(H3)),
        uniform_bounds={key:str(value) for key,value in bounds.items()},exports=exports,
        formulas=dict(cubic_spatial_current_time=str(cubic_flux_t),clock_second_partition='2*A*p^3*abs(w)^3*(J^2+w*T*J_z)',
            J='3*T*wprime+Rprime',J_z='3*T_z*wprime-4800*T*w+Rsecond'),
        nodal_spatial_flux_jump_absent=all(c['passed'] for c in checks),initial_time_tangent_column_kernel_retained=all(c['passed'] for c in checks),
        full_weak_existence_or_uniqueness_proved=False,time_compatible_distribution_extension_selected=False,
        physical_weak_solution_admitted=False,time_evolution=False,G1_complete=False,physics_pass=False,
        gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();result['passed']=sum(c['passed'] for c in result['checks']);result['total']=len(result['checks']);data=ENC(result)
    if args.replay:
        assert (args.replay/'summary.json').read_bytes()==data,'immutable replay mismatch';print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);f=args.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','nodal_spatial_flux_jump_absent','physical_weak_solution_admitted','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
