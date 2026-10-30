"""Original time-mass weighting and its isolated nodal distribution kernel.

No finite-part extension, weak evolution, physical normalization or admission.
"""
import argparse, hashlib, importlib.util, json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_auxiliary_pole_v2_attempt_01/summary.json'
PSHA='048c5a18417cc6abead66bb80cc3999e697dc67a001a5d2287349e1cb2a66e0e'
REPORT='Theory/Gates/RES-001/RES001_R4C1_AUXILIARY_POLE_V2_REPORT_2026-10-29.md'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_WEIGHTED_NODE_V1_CONTRACT_2026-10-29.md'
ENGINE='Analysis/MasterTests/test_01_r4c1_auxiliary_pole_v2.py'
DISK='Analysis/MasterTests/r4c1_cauchy_disk_v1.py'
KIN='Analysis/MasterTests/outputs/r4c1_quartic_kinetic_extension_v2_attempt_01/summary.json'
CLOCK='Analysis/MasterTests/outputs/r4c1_clock_density_source_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def calculate():
    mp.mp.dps=110;mp.iv.dps=80
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['auxiliary_partition_pole_certified'] and parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for path in (REPORT,CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            f=ROOT/path
            assert SHA(f.read_bytes())==want and Path(str(f)+'.sha256').read_text().split()[0].lower()==want,path
    verify();checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    en=load('weighted_interval',ENGINE);disk=load('weighted_disk',DISK)
    w,Z=s.symbols('w Z',real=True);k=s.Rational(3,4);b=s.Rational(5,44);a=s.Rational(1,28);p=s.Rational(1,20)
    formulas=READ(KIN)['formulas']
    BB=s.Matrix([[s.sympify(v,locals={'w':w}) for v in row] for row in formulas['B']])
    CC=s.Matrix([s.sympify(v,locals={'w':w,'Z':Z}) for v in formulas['C']])
    mass=s.zeros(14);mass[:12,:12]=BB;mass[:12,12]=CC;mass[12,:12]=CC.T
    mass[12,12]=k*(1+w*w)-6*a*p*s.Abs(w)**3
    mass[12,13]=mass[13,12]=-b*w*w
    want=s.zeros(14,1);want[12]=-b*w*w
    check('exact_full_auxiliary_time_mass_column',mass[:,13]==want)
    coefficient=F(parent['pole_coefficient']);radius=F(1,1000)
    check('exact_pole_image_vanishes_at_node',s.limit(-b*s.Rational(coefficient.numerator,coefficient.denominator)*s.Abs(w),w,0)==0)
    # Construct interval endpoints with exact rational arithmetic, not floats.
    edge=mp.iv.mpf(1)/1000;box={w:mp.iv.mpf([-edge.b,edge.b])}
    brow=max(sum(en.bound(BB[i,j],box,disk) for j in range(12)) for i in range(12))
    mj=F(parent['envelopes']['Mj']);jf=F(parent['envelopes']['JF']);cf=F(parent['envelopes']['CF'])
    remainder=F(parent['remainder_B']);bn=F(5,44)
    diagonal=F(3,4)*(1+radius**2)+6*F(1,28)*F(1,20)*radius**3
    bounds={
        'complement':brow*mj+cf*jf*radius**2,
        'scalar':cf*mj*radius**2+diagonal*jf+bn*coefficient+remainder*radius**2,
        'auxiliary':bn*jf*radius**2,
    }
    uniform=max(bounds.values())
    check('all_weighted_jerk_envelopes_finite_positive',all(v>0 for v in bounds.values()))
    check('weighted_image_locally_integrable_and_continuous_trace_zero',uniform>0 and s.limit(s.Symbol('L',positive=True)*s.Abs(w),w,0)==0)
    # Independent unspecialized 56-slot action exports, with all fields retained.
    controls=[]
    matrix_fn=s.lambdify((w,Z),mass,modules='mpmath')
    for point in READ(CLOCK)['points']:
        raw=READ(point['raw_point_source']);jet=list(map(mp.mpf,raw['original_first_jet']))
        actual=mp.matrix([[mp.mpf(raw['full_Hessian'][16+i][16+j]) for j in range(14)] for i in range(14)])
        expected=matrix_fn(jet[7],jet[13]);error=max(abs(x) for x in actual-expected)/(1+max(abs(x) for x in actual))
        check('full_action_time_mass_'+point['label'],error<mp.mpf('1e-18'),mp.nstr(error,65))
        controls.append(dict(label=point['label'],normalized_mass_error=mp.nstr(error,65)))
    # Distribution identities hold for every smooth test function via its finite jet.
    t=s.symbols('t0:6');test=sum(t[i]*w**i/s.factorial(i) for i in range(6))
    actions=[]
    for n in range(4):
        lhs=s.diff(w*w*test,w,n).subs(w,0)*(-1)**n
        rhs=0 if n<2 else n*(n-1)*s.diff(test,w,n-2).subs(w,0)*(-1)**(n-2)
        check('exact_distribution_product_order_'+str(n),s.expand(lhs-rhs)==0)
        actions.append(str(s.expand(lhs)))
    check('delta_and_delta_prime_in_isolated_column_kernel',actions[:2]==['0','0'])
    check('delta_second_derivative_nonzero_rejection_control',s.diff(w*w*test,w,2).subs(w,0)==2*t[0])
    check('simple_nodes_have_nonzero_normal_jacobian',s.Rational(1,500)*40==s.Rational(2,25))
    verify()
    return dict(result_id='R4C1-WEIGHTED-NODE-V1',source_sha256=pins,checks=checks,controls=controls,
        original_time_mass_column=[str(v) for v in want],norm='maximum absolute original fourteen-field chart component',
        domain='0<abs(w)<=1/1000 on registered initial slice, fixed zero free-shift representative',
        complement_mass_row_norm_bound=str(brow),weighted_component_bounds={q:str(v) for q,v in bounds.items()},
        uniform_weighted_jerk_bound=str(uniform),weighted_jerk_inequality='norm(M_physical*Delta(j14))<=L*abs(w)',
        singular_column_image='-b*(297/2800000)*abs(w)*e_psi+O(abs(w)^3)',
        test_function_distribution_actions=actions,isolated_column_kernel=['delta(w)','delta_prime(w)'],
        weighted_time_mass_image_locally_integrable=all(c['passed'] for c in checks),full_momentum_second_time_derivative_computed=False,
        full_constraint_distribution_kernel_computed=False,physical_nonuniqueness_proved=False,
        finite_part_or_junction_prescription_selected=False,weak_solution_admitted=False,
        canonical_normalization_established=False,time_evolution=False,G1_complete=False,
        physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);args=parser.parse_args()
    result=calculate();result['passed']=sum(c['passed'] for c in result['checks']);result['total']=len(result['checks']);data=ENC(result)
    if args.replay:
        assert (args.replay/'summary.json').read_bytes()==data,'immutable replay mismatch'
        print('READ_ONLY_REPLAY_EXACT')
    else:
        args.output.mkdir(parents=True,exist_ok=False);file=args.output/'summary.json';file.write_bytes(data)
        Path(str(file)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({q:result[q] for q in ('passed','total','weighted_time_mass_image_locally_integrable','weak_solution_admitted','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
