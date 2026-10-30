"""Raw full-action derivative inputs. No reduced forcing or evolution claim."""
import argparse,hashlib,importlib.util,json,multiprocessing
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_principal_source_compatibility_v1_attempt_01/summary.json'
PSHA='7ff7adb23c832dc7bc801ad8dc4c4ec2ceb2ecdb66fd037b22aefa5de1a24f58'
CHARGE='Analysis/MasterTests/test_01_r4c1_quartic_charge_tangency_v2.py'
POINTS='Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v2_attempt_01/summary.json'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_UNREDUCED_JET_EXPORT_V1_CONTRACT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)
charge=None
weak=None


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def setup():
    global charge,weak
    charge=load('raw_jet_registered',CHARGE);charge.setup();mp.mp.dps=110
    backend=load('raw_jet_full_action',BACKEND);weak=backend.WeakAction(charge.en.body,charge.en.par)


def point(row):
    checks=[]
    def check(name,value):checks.append(dict(name=name,passed=bool(value<mp.mpf('1e-18')),error=show(value)))
    norm=lambda z:max(abs(t) for t in z)
    rel=lambda a,b:abs(a-b)/(1+abs(a)+abs(b))
    theta=mp.mpf(row['theta']);old,vd,dd,Sdd=charge.state(theta)
    rho=mp.mpf(row['values']['rho'])
    # epsilon=rho ONLY at the stored psi=0,C=1 slice. Its derivatives remain unspecified.
    A=old[:14]+[mp.mpf(0),rho]+old[14:28]+[mp.mpf(1),mp.mpf(0)]+old[28:42]+[mp.mpf(0)]*2+old[42:48]+[mp.mpf(1),mp.mpf(0)]
    ll,gg=weak.gradient(A);baseL,baseg=charge.en.gradient(old)
    check('original_initial_density',rel(ll,baseL))
    check('original_physical_momenta',norm(gg[16:30,0]-baseg[14:28,0])/(1+norm(baseg[14:28,0])))
    force=mp.matrix(baseg[:14,0]);force[12]-=charge.en.par['beta']*rho
    check('original_dust_scalar_force_partition',norm(gg[:14,0]-force)/(1+norm(force)))
    check('clock_momentum_initial_density',rel(gg[30],rho))
    check('unused_multiplier_derivative_gradient',max(abs(gg[j]) for j in (31,47)))
    hessians=[]
    for text in ('1e-20','1e-26'):
        cols=[]
        for j in range(56):
            direction=[mp.mpf(0)]*56;direction[j]=1
            cols.append(weak.hv(A,direction,mp.mpf(text)))
        H=mp.matrix([[cols[j][i] for j in range(56)] for i in range(56)])
        check('whole_Hessian_symmetry_'+text,norm(H-H.T)/(1+norm(H)))
        check('unused_multiplier_derivative_columns_'+text,max(abs(H[i,j]) for i in range(56) for j in (31,47)))
        hessians.append(H)
    H=hessians[-1]
    check('whole_Hessian_two_steps',norm(hessians[0]-H)/(1+norm(H)))
    direction=mp.matrix([mp.mpf(j%7-3)/(251+j) for j in range(56)])
    fn=lambda t:weak.density([a+t*d for a,d in zip(A,direction)])[0]
    check('independent_real_first_variation',rel(mp.diff(fn,0),(gg.T*direction)[0]))
    check('independent_real_second_variation',rel(mp.diff(fn,0,2),(direction.T*H*direction)[0]))
    return dict(label=row['label'],theta=row['theta'],checks=checks,
                original_first_jet=[show(t) for t in A],gradient=[show(t) for t in gg],
                full_Hessian=[[show(t) for t in rr] for rr in H.tolist()],
                original_spatial_auxiliary_inputs=dict(mixed_physical=[show(t) for t in vd],
                    second_spatial_physical=[show(t) for t in dd],shift_second_spatial=[show(t) for t in Sdd]),
                clock_multiplier_transport_jet='UNSPECIFIED; unused density slots are not values of a physical Euler transport direction',
                stored_parent_acceleration_NOT_a_closed_full_jet=row['values']['acc'],
                actual_reduced_source_exported=False,physical_admission=False)


def calculate(workers):
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify()
    rows=[r for r in READ(POINTS)['points'] if r['label'].startswith('interior_') or r['label'].endswith('_0.01')]
    assert len(rows)==6,'registered six point selection changed'
    results=[]
    if workers==1:
        setup()
        for row in rows:
            item=point(row);results.append(item);print(json.dumps(dict(completed=item['label'])),flush=True)
    else:
        with ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=setup) as pool:
            futures=[pool.submit(point,r) for r in rows]
            for future in as_completed(futures):
                item=future.result();results.append(item);print(json.dumps(dict(completed=item['label'])),flush=True)
    results.sort(key=lambda r:r['label'])
    files={item['label']+'.json':ENC(item) for item in results}
    checks=[dict(c,point=item['label']) for item in results for c in item['checks']]
    verify()
    summary=dict(result_id='R4C1-UNREDUCED-JET-EXPORT-V1',source_sha256=pins,
                 file_sha256={name:SHA(data) for name,data in files.items()},
                 layout='q16,v16,d16,S3,Sz3,N,Nz; q=h6,V3,u,v,r,psi,Z,tau,epsilon',
                 points=[dict(label=item['label'],theta=item['theta']) for item in results],
                 checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
                 working_digits=110,stored_digits=65,steps=['1e-20','1e-26'],mpmath=mp.__version__,
                 exact_node_data_exported=False,clock_multiplier_transport_jet_fixed=False,
                 actual_reduced_source_exported=False,admitted_weak_domain=False,time_evolution=False,
                 G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)
    files['summary.json']=ENC(summary)
    return summary,files


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    p.add_argument('--workers',type=int,choices=(1,2,3,4),default=2);a=p.parse_args()
    summary,files=calculate(a.workers)
    if a.replay:
        for name,data in files.items():
            f=a.replay/name
            if f.read_bytes()!=data or Path(str(f)+'.sha256').read_text().split()[0].lower()!=SHA(data):
                raise ValueError('immutable replay mismatch '+name)
        print('ALL_SEVEN_FILES_READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False)
        for name,data in files.items():
            f=a.output/name;f.write_bytes(data)
            Path(str(f)+'.sha256').write_text(SHA(data)+'  '+name+'\n',encoding='ascii')
    print(json.dumps({k:summary[k] for k in ('passed','total','actual_reduced_source_exported','G1_complete','physics_pass')}))
    raise SystemExit(0 if summary['passed']==summary['total'] else 2)


if __name__=='__main__':main()
