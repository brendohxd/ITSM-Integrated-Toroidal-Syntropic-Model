"""Constrained homogeneous tilt diagnostic and actual nonzero-mode kinetic reduction.

No adoption of a tilted cosmology, physical cutoff, or new G1 preparation.
"""
from __future__ import annotations
import argparse,ast,hashlib,importlib.util,json
from pathlib import Path
from types import SimpleNamespace
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_b1_propagator_v1_attempt_01/summary.json'
PSHA='93c5d85618d4546b61b6a74961d04d93da35e2ad95dc20d3b57b4ce4e38dce10'
SOURCE='Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_B1_ALIGNMENT_DOMAIN_V1_CONTRACT_2026-10-29.md'
REPORT='Theory/Gates/RES-001/RES001_R4C1_B1_PROPAGATOR_V1_REPORT_2026-10-29.md'
CANONICAL='Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_V2_REPORT_2026-10-17.md'
KERNEL='Analysis/MasterTests/dust_certified_arithmetic_v1.py'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda v:(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())
clean=lambda z:s.factor(s.cancel(z))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def components(matrix):
    todo=set(range(matrix.rows));out=[]
    while todo:
        seed=min(todo);todo.remove(seed);block=[seed];stack=[seed]
        while stack:
            i=stack.pop()
            adjacent=[j for j in sorted(todo) if matrix[i,j]!=0 or matrix[j,i]!=0]
            for j in adjacent:todo.remove(j);stack.append(j);block.append(j)
        out.append(sorted(block))
    return out


def determinant(matrix):
    return clean(s.prod(matrix.extract(part,part).det(method='domain-ge') for part in components(matrix)))


def physical_ad_body(path):
    tree=ast.parse((ROOT/path).read_text(encoding='utf-8-sig'))
    names={'val','unary','sqrt','sin','cos','exp','dot','mv','tr','trans','mm','det3','inv3','tensor','geometry','body'}
    tree.body=[z for z in tree.body if isinstance(z,ast.FunctionDef) and z.name in names
               or isinstance(z,ast.ClassDef) and z.name in {'Tape','Node'}]
    glob=dict(mp=mp);exec(compile(tree,'<pinned-original-physical-AD>','exec'),glob)
    return SimpleNamespace(**glob)


def calculate():
    mp.mp.dps=120;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        rows=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for q in rows if (v:=clean(q))!=0];check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['accepted'] and parent['passed']==parent['total']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name in (SELF,CONTRACT,REPORT,CANONICAL):pins[name]=SHA((ROOT/name).read_bytes())
    snapshots={}
    for name,want in pins.items():
        f=ROOT/name;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,name
        for q in (f,sc):snapshots[q.relative_to(ROOT).as_posix()]=(SHA(q.read_bytes()),q.stat().st_mtime_ns)
    old=load('B1_alignment_quadratic',SOURCE);backend=load('B1_alignment_original_weak',old.BACKEND)
    kernel=load('B1_alignment_interval_kernel',KERNEL);IV=kernel.IV
    par=old.parameters();w=s.Symbol('w',real=True);H=s.Symbol('H',positive=True)
    phase=s.Symbol('v_dot',real=True);p=s.Rational(1,5);b=par['b'];A=par['A']
    weak=backend.WeakAction(old.original_body(True),par)
    q=list(map(s.Rational,(1,0,0,1,0,1,0,0,0,1,0,1,0,0,0)))+[s.Rational(1,5)];q[7]=w
    vv=[s.Integer(0)]*16;dd=vv.copy()
    for j in (0,3,5):vv[j]=2*H
    vv[7]=-H*w;vv[10]=phase;vv[11]=s.Rational(1,4);vv[12]=p;vv[14]=1
    # All fourteen homogeneous coordinate velocities are independent variations.
    # Three constant shifts are also varied; their spatial-divergence terms vanish on homogeneous data.
    jets=[old.Jet.var(i) for i in range(19)]
    hv=[v+(jets[i] if i<14 else 0) for i,v in enumerate(vv)]
    hv[14]+=jets[15]
    hom=weak.density(q+hv+dd+jets[16:19]+[0,0,0]+[1+jets[14],0])[0]
    charge=clean(hom.g.get(10,0))
    zero('original_U1_charge_formula',charge-(1-w*w/13)*phase)
    phasecurve=1/(1-w*w/13)
    zero('charge_preserved_exactly',charge.subs(phase,phasecurve)-1)
    zero('dust_charge_preserved_exactly',hom.g.get(15,0)-s.Rational(1,5))
    zero('constant_shift_variation_zero',s.Matrix([hom.g.get(i,0) for i in range(16,19)]))
    lapse=clean(hom.g.get(14,0)+2*A*p**3*s.Abs(w)**3)
    E0=s.Rational(3469,1400)
    C=s.Rational(33,10)+s.Rational(13,60)*w*w
    energy=E0-s.Rational(1,2)+1/(2*(1-w*w/13))+s.Rational(3,50)*w*w-s.Rational(4,875)*s.Abs(w)**3
    zero('full_original_lapse_curve_equation',lapse.subs(phase,phasecurve)-(C*H*H-energy))
    H2=clean(energy/C)
    zero('aligned_background_endpoint',H2.subs(w,0)-s.Rational(3469,4620))
    zero('charge_curve_reflection',phasecurve.subs(w,-w)-phasecurve)
    zero('lapse_curve_reflection',H2.subs(w,-w)-H2)
    # Homogeneous Routh action at fixed p_tau=1/5 is L_rest-p_tau*C(psi).
    # At this event C=1. Its temporal Hessian equals that of L_rest.
    homogeneous_L=hom.c-A*p**3*s.Abs(w)**3-s.Rational(1,5)
    momenta=[hom.g.get(i,0)-(3*A*p*p*s.Abs(w)**3 if i==12 else 0) for i in range(14)]
    canonical_energy=clean(sum(vv[i]*momenta[i] for i in range(14))-homogeneous_L)
    zero('unfixed_lapse_equals_negative_homogeneous_energy',canonical_energy+lapse)
    Mh=s.zeros(14)
    for (i,j),z in hom.h.items():
        if i<14 and j<14:Mh[i,j]=Mh[j,i]=clean(z.subs(phase,phasecurve))
    Mh[12,12]-=6*A*p*s.Abs(w)**3
    R=Mh[:12,:12];detR=determinant(R)
    expect=s.zeros(14,1);expect[12]=-b*w*w
    zero('homogeneous_auxiliary_velocity_column',Mh[:,13]-expect)
    # Expand the determinant in its last row/column, without a singular inversion at alignment.
    detMh=-b*b*w**4*detR
    check('full_homogeneous_complement_no_Float',not bool(R.atoms(s.Float)))
    print('B1_CONSTRAINED_HOMOGENEOUS_TILT_CURVE',flush=True)
    # Full original derivative block at the SAME constrained diagnostic initial events.
    vvar=[old.Jet.var(i) for i in range(11)];dvar=[old.Jet.var(11+i) for i in range(11)]
    sigma=[old.Jet.var(22+i) for i in range(3)]
    v0=[z.subs(phase,phasecurve) if isinstance(z,s.Basic) else z for z in vv];d0=dd.copy()
    for i,j in enumerate(old.SLOTS):v0[j]+=vvar[i];d0[j]=dvar[i]
    L=weak.density(q+v0+d0+[0,0,0]+sigma+[1,-par['beta']*dvar[9]])[0]
    full=s.zeros(25)
    for (i,j),z in L.h.items():full[i,j]=full[j,i]=clean(z)
    full[9,9]-=6*A*p*s.Abs(w)**3;full[20,20]-=3*A*p*s.Abs(w)
    zero('full_derivative_Hessian_symmetric',full-full.T)
    D=full[22:25,22:25];detD=determinant(D)
    reduced=(full[:11,:11]-full[:11,22:25]*D.inv()*full[22:25,:11]).applyfunc(clean)
    zero('kinetic_independent_initial_H',reduced.diff(H))
    zero('kinetic_auxiliary_column',reduced[:,10]-s.Matrix([0]*9+[-b*w*w,0]))
    B9=reduced[:9,:9];coupling=reduced[:9,9];f_eff=clean(reduced[9,9]-(coupling.T*B9.inv()*coupling)[0])
    LL,DD=B9.LDLdecomposition(hermitian=False)
    zero('B9_exact_LDL',B9-LL*DD*LL.T)
    zero('regulator_mixing_unchanged',reduced[9,10]+b*w*w)
    zero('aligned_auxiliary_velocity_vanishes',reduced[:,10].subs(w,0))
    aligned=READ('Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json')['formulas']['reduced_kinetic']
    zero('aligned_ten_field_kinetic_recovered',reduced[:10,:10].subs(w,0)-s.Matrix([[s.sympify(z) for z in row] for row in aligned]))
    zero('reduced_determinant_factor',determinant(reduced)+b*b*w**4*determinant(B9))
    reflect=s.diag(*([1,-1,1,1,-1,1,1,1,1,1,1]*2+[1,-1,1]))
    zero('full_block_tilt_reflection',full.subs(w,-w)-reflect*full*reflect)
    # Outward-rounded bounds on the entire closed |w| interval, including the regular complements at zero.
    bound=IV.rational(1,500);wi=IV(0,bound.hi);cache={}
    def ev(expr):
        if expr in cache:return cache[expr]
        if expr==w:ans=wi
        elif expr.is_Rational:ans=IV.rational(int(expr.p),int(expr.q))
        elif expr.is_Add:ans=sum((ev(z) for z in expr.args),0)
        elif expr.is_Mul:
            ans=1
            for z in expr.args:ans=ans*ev(z)
        elif expr.is_Pow and expr.exp.is_Integer:ans=ev(expr.base).power(int(expr.exp))
        elif expr.is_Pow and expr.exp==s.Rational(1,2):ans=ev(expr.base).sqrt()
        elif expr.func==s.Abs:
            value=ev(expr.args[0]);ans=IV(value.abs_lower(),value.abs_upper())
        else:raise ValueError('unsupported interval node '+str(expr))
        cache[expr]=ans;return ans
    interval=lambda z:ev(clean(z))
    rdet=interval(detR);sdet=interval(detD);hi=interval(H2);fi=interval(f_eff)
    check('homogeneous_complement_regular_uniformly',rdet.abs_lower()>0,rdet.encode())
    check('nonzero_mode_shift_block_regular_uniformly',sdet.abs_lower()>0,sdet.encode())
    check('constraint_H_positive_bounded',IV.rational(3,4).hi<hi.lo and hi.hi<IV.rational(1).lo,hi.encode())
    check('charge_denominator_positive',interval(1-w*w/13).lo>0)
    for i,pivot in enumerate(DD.diagonal()):check('B9_positive_pivot_'+str(i),interval(pivot).lo>0,interval(pivot).encode())
    check('effective_psi_kinetic_positive',fi.lo>0,fi.encode())
    negative_coefficient=clean(b*b/f_eff)
    check('negative_Z_Schur_coefficient_strict',interval(negative_coefficient).lo>0,interval(negative_coefficient).encode())
    # Exact congruence after the positive B9 elimination: f_eff and -b^2*w^4/f_eff.
    psiZ=s.Matrix([[f_eff,-b*w*w],[-b*w*w,0]])
    triangular=s.Matrix([[1,-b*w*w/f_eff],[0,1]])
    zero('reduced_psi_Z_signed_square',psiZ-triangular.T*s.diag(f_eff,-b*b*w**4/f_eff)*triangular)
    print('B1_REDUCED_ALIGNMENT_KINETIC_SIGNATURE',flush=True)
    physical=backend.WeakAction(physical_ad_body(old.BODY),{n:mp.mpf(int(z.p))/int(z.q) for n,z in par.items()})
    fullnum=s.lambdify((w,H),full,modules='mpmath');homnum=s.lambdify((w,H),Mh,modules='mpmath')
    hcurve=s.lambdify(w,s.sqrt(H2),modules='mpmath');vcurve=s.lambdify(w,phasecurve,modules='mpmath')
    controls=[]
    for sign in (-1,1):
        wp=mp.mpf(sign)/1000;hp=hcurve(wp);cp=vcurve(wp)
        qq=[mp.mpf(z) if not isinstance(z,s.Basic) else mp.mpf(str(z)) for z in [1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,mp.mpf(1)/5]];qq[7]=wp
        vel=[mp.mpf(0)]*16;dz=vel.copy()
        for j in (0,3,5):vel[j]=2*hp
        vel[7]=-hp*wp;vel[10]=cp;vel[11]=mp.mpf(1)/4;vel[12]=mp.mpf(1)/5;vel[14]=1
        point=qq+vel+dz+[mp.mpf(0)]*6+[mp.mpf(1),mp.mpf(0)]
        _,gradient=physical.gradient(point)
        check('original_lapse_constraint_'+str(sign),abs(gradient[54])<mp.mpf('1e-100'),mp.nstr(abs(gradient[54]),65))
        check('original_U1_charge_'+str(sign),abs(gradient[26]-1)<mp.mpf('1e-100'))
        check('original_dust_charge_'+str(sign),abs(gradient[30]-mp.mpf(1)/5)<mp.mpf('1e-100'))
        check('homogeneous_shift_values_'+str(sign),max(abs(gradient[j]) for j in range(48,51))<mp.mpf('1e-100'))
        expected=mp.matrix(fullnum(wp,hp));expected_hom=mp.matrix(homnum(wp,hp))
        directions=[]
        for j in range(25):
            direction=[mp.mpf(0)]*56
            if j<11:direction[16+old.SLOTS[j]]=1
            elif j<22:
                qi=old.SLOTS[j-11];direction[32+qi]=1
                if qi==12:direction[55]=-mp.mpf(2)/5
            else:direction[51+j-22]=1
            directions.append(direction)
        for hs in ('1e-20','1e-26'):
            cols=[]
            for direction in directions:
                hv=physical.hv(point,direction,mp.mpf(hs))
                cols.append([sum(v0*hv[i] for i,v0 in enumerate(test)) for test in directions])
            observed=mp.matrix([[cols[j][i] for j in range(25)] for i in range(25)])
            error=max(abs(z) for z in observed-expected)/(1+max(abs(z) for z in expected))
            check(f'full_physical_derivative_block_{sign}_{hs}',error<mp.mpf('1e-18'),mp.nstr(error,65))
            cols=[]
            for j in range(14):
                direction=[mp.mpf(0)]*56;direction[16+j]=1
                hv=physical.hv(point,direction,mp.mpf(hs));cols.append([hv[16+i] for i in range(14)])
            observed=mp.matrix([[cols[j][i] for j in range(14)] for i in range(14)])
            error_h=max(abs(z) for z in observed-expected_hom)/(1+max(abs(z) for z in expected_hom))
            check(f'full_homogeneous_physical_mass_{sign}_{hs}',error_h<mp.mpf('1e-18'),mp.nstr(error_h,65))
            controls.append(dict(sign=sign,step=hs,derivative_block_error=mp.nstr(error,65),homogeneous_mass_error=mp.nstr(error_h,65)))
    for name,(digest,mtime) in snapshots.items():
        f=ROOT/name;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    encode=lambda mat:[[str(clean(z)) for z in row] for row in mat.tolist()]
    return dict(kind='R4C1_B1_ALIGNMENT_DOMAIN_V1',passed=sum(z['passed'] for z in checks),total=len(checks),checks=checks,
        source_sha256=pins,independent_controls=controls,
        formulas=dict(parameter='0<abs(w)<=1/500',phase_velocity=str(phasecurve),H_squared=str(H2),
            lapse_H_coefficient=str(C),lapse_energy=str(energy),homogeneous_complement=encode(R),
            homogeneous_complement_determinant=str(detR),homogeneous_determinant=str(detMh),
            full_derivative_Hessian=encode(full),shift_block=encode(D),shift_determinant=str(detD),
            reduced_kinetic=encode(reduced),positive_B9_L=encode(LL),positive_B9_D=encode(DD),
            effective_psi_mass=str(f_eff),negative_Z_mass=str(-b*b*w**4/f_eff),
            Z_canonical_scale=str(b*w*w/s.sqrt(f_eff))),
        bounds=dict(H_squared=hi.encode(),homogeneous_complement_determinant=rdet.encode(),
            shift_determinant=sdet.encode(),effective_psi_mass=fi.encode(),negative_coefficient_over_w4=interval(negative_coefficient).encode(),
            arithmetic_bits=kernel.BITS),
        diagnostic_homogeneous_local_admission=rdet.abs_lower()>0 and hi.lo>0,
        reduced_kinetic_inertia=dict(positive=10,negative=1,zero=0),aligned_reduced_inertia=dict(positive=10,negative=0,zero=0),
        uniform_alignment_neighbourhood_cleared=False,uniform_lifespan_proved=False,physical_cutoff_identified=False,
        frame_harmonic_varied=True,adopted_new_state=False,nodal_G1_admitted=False,physical_window_demonstrated=False,
        physics_pass=False,gate_effect='NONE',review='DEFERRED',G1='INCOMPLETE',G2='INCOMPLETE',G3='INCOMPLETE',
        G4='INCOMPLETE',G5='INCOMPLETE',G6='INCOMPLETE',MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--out');g.add_argument('--replay');args=parser.parse_args()
    if args.out and (ROOT/args.out).exists():raise FileExistsError(args.out)
    result=calculate();data=ENC(result)
    if args.replay:
        target=ROOT/args.replay;assert target.read_bytes()==data,'immutable replay mismatch'
        assert Path(str(target)+'.sha256').read_text().split()[0]==SHA(data);print('IMMUTABLE_REPLAY_EXACT',flush=True)
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);f=out/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({z:result[z] for z in ('passed','total','diagnostic_homogeneous_local_admission','reduced_kinetic_inertia','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
