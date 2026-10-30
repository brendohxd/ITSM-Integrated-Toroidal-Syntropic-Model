"""Actual initial time-tangent forcing. Point diagnostics do not certify node limits."""
import argparse,hashlib,importlib.util,json,multiprocessing
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_full_initial_jacobi_v1_attempt_01/summary.json'
PSHA='a431db3471b5ec87cf0d25313feb90016f4cf9c9990f997a3320839b8f29d1a1'
CLOCK='Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json'
JERK='Analysis/MasterTests/outputs/r4c1_quartic_total_jerk_v1_attempt_01/summary.json'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_TIME_TANGENT_V1_CONTRACT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)
norm=lambda a:max(abs(z) for z in a)
pack=lambda a:[[show(z) for z in row] for row in a.tolist()]
ch=None
backend=None
physical_A=None


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def setup():
    global ch,backend,physical_A
    ch=load('time_tangent_registered',CHARGE);ch.setup();mp.mp.dps=140
    backend=load('time_tangent_full_action',BACKEND);physical_A=ch.en.par['A']


def values(theta):
    v=ch.solve(theta,mp.mpf('1e-26'),False)
    v['epsilon_dot']=v['rho_dot']-4*ch.en.par['beta']*ch.en.vals['p']*v['rho']
    return v


def euler(weak,A,Dt,Dz):
    _,g=weak.gradient(A);gt=weak.hv(A,Dt,mp.mpf('1e-26'));gz=weak.hv(A,Dz,mp.mpf('1e-26'))
    return mp.matrix([g[i]-gt[16+i]-gz[32+i] for i in range(16)]+
                     [g[48+i]-gz[51+i] for i in range(3)]+[g[54]-gz[55]])


def point(job):
    label,theta_text,partition,jacobi_file=job
    ch.en.par['A']=physical_A*partition
    weak=backend.WeakAction(ch.en.body,dict(ch.en.par));theta=mp.mpf(theta_text);checks=[]
    def close(name,error):checks.append(dict(name=name,passed=bool(error<mp.mpf('1e-18')),error=show(error)))
    base=values(theta);old,vd,dd,Sdd=ch.state(theta)
    acc=base['acc'];rho=base['rho'];beta=ch.en.par['beta'];p=ch.en.vals['p']
    A=old[:14]+[mp.mpf(0),rho]+old[14:28]+[mp.mpf(1),mp.mpf(0)]+old[28:42]+[mp.mpf(0)]*2+old[42:48]+[mp.mpf(1),mp.mpf(0)]
    Dt=mp.matrix(A[16:32]+list(acc)+[beta*p,mp.mpf(0)]+vd+[mp.mpf(0)]*2+[mp.mpf(0)]*8);Dt[15]=base['epsilon_dot']
    Dz=mp.matrix(A[32:48]+vd+[mp.mpf(0)]*2+dd+[mp.mpf(0)]*2+A[51:54]+Sdd+[mp.mpf(0)]*2);Dz[15]=base['rho_z']
    close('complete_initial_twenty_Euler',norm(euler(weak,A,Dt,Dz))/(1+norm(acc)))
    spatial=[]
    for eps in ('1e-18','1e-22'):
        h=mp.mpf(eps);plus=values(theta+h);minus=values(theta-h)
        az=40*(plus['acc']-minus['acc'])/(2*h)
        etz=40*(plus['epsilon_dot']-minus['epsilon_dot'])/(2*h)
        vzz=mp.matrix([40*(ch.state(theta+h)[1][j]-ch.state(theta-h)[1][j])/(2*h) for j in range(14)])
        spatial.append((az,etz,vzz))
    az,etz,vzz=spatial[-1]
    close('actual_acceleration_spatial_derivative_steps',norm(spatial[0][0]-az)/(1+norm(az)))
    close('Hamiltonian_multiplier_rate_spatial_derivative_steps',abs(spatial[0][1]-etz)/(1+abs(etz)))
    close('initial_velocity_second_spatial_derivative_steps',norm(spatial[0][2]-vzz)/(1+norm(vzz)))
    # Free second-time shift jets and their spatial derivatives remain explicit response channels.
    columns=[]
    for j in list(range(16,30))+[15]+list(range(48,54)):
        direction=mp.matrix(56,1);direction[j]=1
        columns.append(weak.hv(A,direction,mp.mpf('1e-26'))[16:32,0])
    M16=mp.matrix([[columns[j][i] for j in range(14)] for i in range(16)])
    M=M16[:14,:14];density_column=columns[14]
    gauge=mp.matrix([[columns[15+j][i] for j in range(6)] for i in range(16)])
    close('time_mass_symmetry',norm(M-M.T)/(1+norm(M)))
    close('physical_jerks_independent_of_second_multiplier_rate',norm(density_column[:14,0]))
    close('current_second_multiplier_coefficient',abs(density_column[14]-1))
    response=mp.matrix(14,6)
    for j in range(6):response[:,j]=mp.lu_solve(M,-gauge[:14,j])
    close('scalar_jerk_shift_gauge_response_zero',max(abs(response[12,j]) for j in range(6)))
    clock3=beta*acc[12]+beta**2*p**2
    Dtt=mp.matrix(list(acc)+[beta*p,mp.mpf(0)]+[mp.mpf(0)]*14+[clock3,mp.mpf(0)]+list(az)+[mp.mpf(0)]*2+[mp.mpf(0)]*8)
    Dtz=mp.matrix(vd+[mp.mpf(0),etz]+list(az)+[mp.mpf(0)]*2+list(vzz)+[mp.mpf(0)]*2+[mp.mpf(0)]*8)
    assert len(Dtt)==len(Dtz)==56
    def derivative(dtt,eps):
        h=mp.mpf(eps)/(1+max(norm(Dt),norm(dtt),norm(Dtz)))
        plus=euler(weak,[a+h*v for a,v in zip(A,Dt)],Dt+h*dtt,Dz+h*Dtz)
        minus=euler(weak,[a-h*v for a,v in zip(A,Dt)],Dt-h*dtt,Dz-h*Dtz)
        return (plus-minus)/(2*h)
    sources=[derivative(Dtt,eps) for eps in ('1e-16','1e-20')]
    close('actual_time_tangent_forcing_steps',norm(sources[0]-sources[1])/(1+norm(sources[1])))
    jerks=[mp.lu_solve(M,src[:14,0]) for src in sources];jerk=jerks[-1]
    close('unweighted_fourteen_jerk_steps',norm(jerks[0]-jerk)/(1+norm(jerk)))
    epsilon2=(sources[-1][14]-(M16[14,:]*jerk)[0])/density_column[14]
    complete=mp.matrix(Dtt);complete[15]=epsilon2
    for j in range(14):complete[16+j]=jerk[j]
    direct=derivative(complete,'1e-20')
    close('complete_twenty_time_tangent_equations',norm(direct)/(1+norm(sources[-1])))
    close('independent_lapse_time_tangency',abs(direct[19])/(1+abs(sources[-1][19])))
    close('independent_three_shift_time_tangencies',max(abs(direct[i])/(1+abs(sources[-1][i])) for i in range(16,19)))
    H=ch.en.H;HB=ch.en.vals['H0'];w=A[7];wp=A[39];R=A[50];rp=A[53];ratio=R*wp/w
    expected=(-ch.en.Ud-(5*H-3*HB-rp-ratio)*acc[12]+2*R*az[12]
              -p*(acc[7]/w+(acc[0]+acc[3]+acc[5])/2+HB**2-8*H*HB-2*(H-HB)*(rp+ratio)))
    close('independent_original_regulator_scalar_jerk',abs(jerk[12]-expected)/(1+abs(jerk[12])+abs(expected)))
    if partition==1 and jacobi_file:
        op=READ(jacobi_file)['full_twenty_coefficients'];J={key:mp.matrix([[mp.mpf(v) for v in rr] for rr in val]) for key,val in op.items()}
        u=mp.matrix(list(Dt[:16,0])+list(Dt[48:51,0])+[Dt[54]])
        ut=mp.matrix(list(complete[:16,0])+list(complete[48:51,0])+[complete[54]])
        uz=mp.matrix(list(Dtz[:16,0])+list(Dtz[48:51,0])+[Dtz[54]])
        utt=mp.matrix(list(complete[16:32,0])+[mp.mpf(0)]*4)
        utz=mp.matrix(list(Dtz[16:32,0])+[mp.mpf(0)]*4)
        uzz=mp.matrix(list(Dtz[32:48,0])+list(Dtz[51:54,0])+[Dtz[55]])
        predicted=J['zero']*u+J['time']*ut+J['space']*uz+J['time_time']*utt+J['time_space']*utz+J['space_space']*uzz
        close('sealed_full_twenty_Jacobi_time_tangent_bridge',norm(predicted-direct)/(1+norm(sources[-1])))
    result=dict(label=label,theta=theta_text,partition_lambda=partition,checks=checks,w=show(w),
                actual_fourteen_accelerations=[show(v) for v in acc],actual_fourteen_third_time_jets=[show(v) for v in jerk],
                actual_acceleration_spatial_derivative=[show(v) for v in az],
                independent_scalar_jerk=show(expected),time_tangent_forcing20=[show(v) for v in sources[-1]],
                nonzero_time_tangent_residuals20=[show(v) for v in direct],
                physical_density_rate=show(base['rho_dot']),multiplier_rate=show(base['epsilon_dot']),
                multiplier_rate_spatial_derivative=show(etz),second_multiplier_time_jet=show(epsilon2),third_clock_time_jet=show(clock3),
                free_shift_second_time_and_spatial_response=pack(response),gauge_representative='S_tt=0,S_tt_z=0, with all six linear response channels retained',
                alternate_background_adopted=False,exact_node_limit_certified=False)
    ch.en.par['A']=physical_A
    return result


def calculate(workers):
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name,want in parent['file_sha256'].items():pins[(Path(PARENT).parent/name).as_posix()]=want
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify();mp.mp.dps=140
    stored=READ(CLOCK)['points'];items=[(r['label'],r['theta'],(Path(PARENT).parent/(r['label']+'.json')).as_posix()) for r in stored]
    for node in (1,3):
        for side in (-1,1):items.append((f'node{node}_{side}_0.001',mp.nstr(node*mp.pi/2+side*mp.mpf('0.001'),135),None))
    jobs=[(label,theta,partition,jfile) for label,theta,jfile in items for partition in (0,1)]
    results=[]
    if workers==1:
        setup()
        for job in jobs:
            val=point(job);results.append(val);print(json.dumps(dict(completed=val['label'],partition=val['partition_lambda'])),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=setup) as pool:
            futures=[pool.submit(point,job) for job in jobs]
            for future in as_completed(futures):
                val=future.result();results.append(val);print(json.dumps(dict(completed=val['label'],partition=val['partition_lambda'])),flush=True)
    results.sort(key=lambda r:(r['label'],r['partition_lambda']))
    checks=[dict(c,point=r['label'],partition=r['partition_lambda']) for r in results for c in r['checks']]
    pairs={r['label']:{} for r in results}
    for r in results:pairs[r['label']][r['partition_lambda']]=r
    w=s.Symbol('w',real=True)
    kernel=s.lambdify(w,s.sympify(READ(JERK)['formulas']['actual_cusp_positive_branch'],locals={'w':w}),modules='mpmath')
    comparisons=[]
    for label,pair in sorted(pairs.items()):
        a,b=pair[0],pair[1];wv=mp.mpf(b['w'])
        delta=mp.matrix([mp.mpf(v)-mp.mpf(u) for u,v in zip(a['actual_fourteen_third_time_jets'],b['actual_fourteen_third_time_jets'])])
        expected=mp.sign(wv)*kernel(wv);error=abs(delta[12]-expected)/(1+abs(expected)+abs(delta[12]))
        checks.append(dict(name='exact_parent_scalar_cusp_kernel',point=label,passed=bool(error<mp.mpf('1e-18')),error=show(error)))
        response0=mp.matrix([[mp.mpf(z) for z in row] for row in a['free_shift_second_time_and_spatial_response']])
        response1=mp.matrix([[mp.mpf(z) for z in row] for row in b['free_shift_second_time_and_spatial_response']])
        error=norm(response1-response0)/(1+norm(response1)+norm(response0))
        checks.append(dict(name='cusp_partition_free_shift_response_invariance',point=label,passed=bool(error<mp.mpf('1e-18')),error=show(error)))
        comparisons.append(dict(label=label,w=show(wv),scalar_jerk_cusp=show(delta[12]),auxiliary_jerk_difference=show(delta[13]),
                                abs_w_times_auxiliary_jerk_difference=show(abs(wv)*delta[13])))
    eta=s.Symbol('eta');pm=READ(PLANAR)['families']['new_B1_frame']['parameter_map']
    kr=s.sympify(pm['K_Q'],locals={'eta':eta}).subs(eta,s.Rational(1,4))
    br=s.sympify(pm['b'],locals={'eta':eta}).subs(eta,s.Rational(1,4))
    candidate=s.factor(kr/br*s.Rational(9,560000))
    verify();files={r['label']+'_lambda'+str(r['partition_lambda'])+'.json':ENC(r) for r in results}
    summary=dict(result_id='R4C1-TIME-TANGENT-V1',source_sha256=pins,file_sha256={name:SHA(data) for name,data in files.items()},
                 checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),cusp_comparisons=comparisons,
                 partition_scope='A=0 is analytic bookkeeping on the fixed physical root/fields/shift; no alternate mean-charge solution or parent adopted',
                 expected_source_order_pole_coefficient=str(candidate),candidate_coefficient_scope='(K_Q/b)*(9/560000); pending exact source/remainder proof',
                 auxiliary_jerk_pole_certified=False,nodal_time_tangent_compatibility_certified=False,
                 working_digits=140,mpmath=mp.__version__,sympy=s.__version__,
                 actual_point_time_tangent_forcing_exported=True,time_evolution=False,G1_complete=False,
                 physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)
    files['summary.json']=ENC(summary);return summary,files


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    p.add_argument('--workers',type=int,choices=(1,2,3,4),default=3);a=p.parse_args();summary,files=calculate(a.workers)
    if a.replay:
        for name,data in files.items():
            f=a.replay/name
            if f.read_bytes()!=data or Path(str(f)+'.sha256').read_text().split()[0].lower()!=SHA(data):raise ValueError('immutable replay mismatch '+name)
        print('ALL_TIME_TANGENT_FILES_READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False)
        for name,data in files.items():
            f=a.output/name;f.write_bytes(data);Path(str(f)+'.sha256').write_text(SHA(data)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({k:summary[k] for k in ('passed','total','actual_point_time_tangent_forcing_exported','auxiliary_jerk_pole_certified','G1_complete','physics_pass')}))
    raise SystemExit(0 if summary['passed']==summary['total'] else 2)


if __name__=='__main__':main()
