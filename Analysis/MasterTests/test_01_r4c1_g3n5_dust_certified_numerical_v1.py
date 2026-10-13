"""Continuous full-state finite-mode defect certificate; all physical holds retained."""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
KERNEL='Analysis/MasterTests/dust_certified_arithmetic_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_CERTIFIED_NUMERICAL_V1_CONTRACT_2026-10-12.md'
sys.path.insert(0,str(ROOT/'Analysis/MasterTests'))
import dust_certified_arithmetic_v1 as k
import test_01_r4c1_g3n5_dust_remainder_v6 as old
import test_01_r4c1_g3n5_dust_finite_k_v1 as frozen
common=old.common
T=Fraction(1,20)
GLOBAL_DEGREE=40
DEGREE=24
MODES=(4,8,16,32,64)
PROGRESS=None


def progress(message):
    print(message,flush=True)
    if PROGRESS is not None:PROGRESS.write(message+'\n');PROGRESS.flush()


def evaluators(environment,degree=None):
    cache={}
    def evaluate(expr):
        if expr in cache:return cache[expr]
        if expr.is_Rational:
            ans=k.IV.rational(int(expr.p),int(expr.q))
            if degree is not None:ans=k.TM.constant(ans,degree)
        elif expr.is_Symbol:ans=environment[expr]
        elif expr.is_Add:ans=sum((evaluate(q) for q in expr.args),0)
        elif expr.is_Mul:
            ans=1
            for q in expr.args:ans=ans*evaluate(q)
        elif expr.is_Pow:
            if expr.exp.is_Integer:ans=evaluate(expr.base).power(int(expr.exp))
            elif expr.exp==s.Rational(1,2):
                if degree is not None:
                    if expr.base.free_symbols:raise ValueError('Variable Taylor square root unsupported')
                    val=evaluators({},None)(expr.base)
                    ans=k.TM.constant(val.sqrt(),degree)
                else:ans=evaluate(expr.base).sqrt()
            else:raise ValueError('Unsupported power '+str(expr))
        else:raise ValueError('Unsupported arithmetic node '+str(expr))
        cache[expr]=ans
        return ans
    return evaluate


def split_matrix(matrix):
    out=[]
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix[i,j]!=0:
                re,im=s.expand_complex(matrix[i,j]).as_real_imag()
                out.append((i,j,re,im))
    return out


def complex_add(a,b):return a[0]+b[0],a[1]+b[1]


def complex_mul(a,b):
    return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]


def complex_inverse(a):
    den=a[0].square()+a[1].square()
    return a[0]/den,-a[1]/den


def complex_scale(a,n,d=1):return a[0].scale(n,d),a[1].scale(n,d)


def complex_center(a):return a[0].center(),a[1].center()


def complex_abs_upper(a):return a[0].abs_upper()+a[1].abs_upper()


def iv_matrix_product(a,b):
    rows,inner,cols=len(a),len(b),len(b[0])
    return [[sum_complex(complex_mul(a[i][j],b[j][q]) for j in range(inner))
             for q in range(cols)] for i in range(rows)]


def sum_complex(values):
    ans=(k.ZERO,k.ZERO)
    for val in values:ans=complex_add(ans,val)
    return ans


def interval_matrix(matrix,evaluate):
    ans=[[(k.ZERO,k.ZERO) for _ in range(matrix.cols)] for _ in range(matrix.rows)]
    for i,j,re,im in split_matrix(matrix):ans[i][j]=(evaluate(re),evaluate(im))
    return ans


def matrix_norm(matrix,evaluate):
    rows=[0]*matrix.rows
    for i,j,re,im in split_matrix(matrix):
        rows[i]+=evaluate(re).abs_upper()+evaluate(im).abs_upper()
    return max(rows,default=0)


def matrix_lipschitz(matrix,bg,evaluate):
    rows=[0]*matrix.rows
    for i,j,re,im in split_matrix(matrix):
        for var in bg:
            if var in re.free_symbols:rows[i]+=evaluate(s.diff(re,var)).abs_upper()
            if var in im.free_symbols:rows[i]+=evaluate(s.diff(im,var)).abs_upper()
    return max(rows,default=0)


def arithmetic_controls(checks):
    qs=[Fraction(0),Fraction(1),Fraction(-1),Fraction(125,89),Fraction(-17,31),Fraction(1,10**60)]
    for i,a in enumerate(qs):
        aa=k.IV.fraction(a)
        checks.add('rational_conversion_'+str(i),aa.contains(a))
        for j,b in enumerate(qs):
            bb=k.IV.fraction(b)
            checks.add('exact_primitive_'+str(i)+'_'+str(j),
                       (aa+bb).contains(a+b) and (aa-bb).contains(a-b) and (aa*bb).contains(a*b)
                       and (b==0 or (aa/bb).contains(a/b)))
    root=k.IV.rational(3469,4620).sqrt()
    checks.add('integer_square_root_outward',root.lo**2*4620<=3469*k.SCALE**2<=root.hi**2*4620)
    try:k.IV(-1,1).inverse()
    except ZeroDivisionError:reject=True
    else:reject=False
    checks.add('zero_denominator_rejected',reject)
    p=k.TM([k.ONE,k.IV.rational(1,4),k.ZERO,k.ZERO])
    inv=p.inverse()
    checks.add('inverse_tail_nonzero_retained',inv.radius>0)
    checks.add('inverse_exact_rational_points',all(inv.at(i,16).contains(Fraction(64,64+i)) for i in range(17)))
    q=k.TM([k.ZERO]*5+[k.ONE])
    restricted=q.restrict(1,2,2)
    checks.add('restriction_higher_tail_retained',restricted.radius>0 and restricted.at().contains(Fraction(1)))
    # A coefficient-one linear approximant with zero RHS has defect exactly one.
    omitted=k.TM([k.ONE,k.ONE,k.ZERO]).derivative(Fraction(1))
    checks.add('omitted_defect_rejected',omitted.sup()>=k.SCALE)
    # Independent analytic alternating-series enclosures at omega*h=1/2.
    x=Fraction(1,2)
    c=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(25)),Fraction(0))
    ss=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range(25)),Fraction(0))
    cr=x**50/factorial(50);sr=x**51/factorial(51)
    tc=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(13)),Fraction(0))
    ts=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range(12)),Fraction(0))
    # These analytic intervals are deliberately checked against an independently
    # derived, higher-order rational enclosure, not floating-point sin/cos.
    rc=x**26/factorial(26);rs=x**25/factorial(25)
    checks.add('skew_rotation_analytic_remainder',tc-rc<=c-cr<=c+cr<=tc+rc and ts-rs<=ss-sr<=ss+sr<=ts+rs)


def exact_initial(bg,mats,mode):
    a,H,u,ud,v,vd,r,rd,pd,rho,C=bg.bg
    init={a:k.ONE,H:k.IV.rational(3469,4620).sqrt(),u:k.ONE,ud:k.ZERO,
          v:k.ZERO,vd:k.ONE,r:k.ONE,rd:k.IV.rational(1,4),
          pd:k.IV.rational(1,5),rho:k.IV.rational(1,5),C:k.ONE,bg.ell:k.IV.rational(mode)}
    evaluate=evaluators(init)
    bi=interval_matrix(mats['balancing_map_inverse'],evaluate)
    b=interval_matrix(mats['balancing_map'],evaluate)
    graph=interval_matrix(mats['formal_slow_lift'],evaluate)
    obs=interval_matrix(mats['actual_dust_observable'],evaluate)
    norm=iv_matrix_product(obs,graph)
    det=complex_add(complex_mul(norm[0][0],norm[1][1]),
                    tuple(-x for x in complex_mul(norm[0][1],norm[1][0])))
    di=complex_inverse(det)
    inverse=[[complex_mul(norm[1][1],di),complex_mul(tuple(-x for x in norm[0][1]),di)],
             [complex_mul(tuple(-x for x in norm[1][0]),di),complex_mul(norm[0][0],di)]]
    prepared=iv_matrix_product(iv_matrix_product(b,graph),inverse)
    oz=iv_matrix_product(obs,bi)
    columns=[[prepared[i][j] for i in range(20)] for j in range(2)]
    for index in (9,19):
        observed=[oz[i][index] for i in range(2)]
        seed=[]
        for i in range(20):
            projected=sum_complex(complex_mul(prepared[i][j],observed[j]) for j in range(2))
            val=(k.ONE if i==index else k.ZERO,k.ZERO)
            seed.append(complex_add(val,tuple(-x for x in projected)))
        lengths=[(z[0].square()+z[1].square()).sqrt() for z in seed]
        magnitude=k.IV(max(q.lo for q in lengths),max(q.hi for q in lengths))
        if magnitude.lo<=0:raise ValueError('Degenerate original complementary seed')
        columns.append([(z[0]/magnitude,z[1]/magnitude) for z in seed])
    nominal=[[complex_center(columns[c][i]) for c in range(4)] for i in range(20)]
    discrepancy=max(complex_abs_upper((nominal[i][c][0]-columns[c][i][0],
                                       nominal[i][c][1]-columns[c][i][1])) for i in range(20) for c in range(4))
    return nominal,discrepancy,init


def restrict_entries(entries,tile,steps,degree=DEGREE):
    return [(i,j,re.restrict(tile,steps,degree),im.restrict(tile,steps,degree)) for i,j,re,im in entries]


def state_polynomial(entries,initial,h):
    """Exact dyadic coefficients; low-order interval discrepancies not discarded."""
    coeff=[[[initial[i][c]] for c in range(4)] for i in range(20)]
    residual=[[0]*4 for _ in range(20)]
    for n in range(DEGREE):
        rhs=[[(k.ZERO,k.ZERO) for _ in range(4)] for _ in range(20)]
        for i,j,re,im in entries:
            for c in range(4):
                for p in range(n+1):
                    a=(re.coeff[p],im.coeff[p])
                    if a[0].is_zero() and a[1].is_zero():continue
                    rhs[i][c]=complex_add(rhs[i][c],complex_mul(a,coeff[j][c][n-p]))
        for i in range(20):
            for c in range(4):
                new=complex_center(complex_scale(rhs[i][c],h.numerator,h.denominator*(n+1)))
                coeff[i][c].append(new)
                actual=complex_scale(new,(n+1)*h.denominator,h.numerator)
                diff=(actual[0]-rhs[i][c][0],actual[1]-rhs[i][c][1])
                residual[i][c]+=complex_abs_upper(diff)
    # Bound ALL RHS polynomial coefficients of degrees >=N, together with
    # the inherited operator Taylor remainder. Low-order coefficients above
    # use the same outward-rounded convolution, retaining their discrepancies.
    for i,j,re,im in entries:
        a_abs=[re.coeff[p].abs_upper()+im.coeff[p].abs_upper() for p in range(DEGREE+1)]
        ar=re.radius+im.radius
        for c in range(4):
            z_abs=[complex_abs_upper(z) for z in coeff[j][c]]
            upper=0
            for p,value in enumerate(a_abs):
                if value:
                    upper+=sum(k.upprod(value,z_abs[q]) for q in range(max(0,DEGREE-p),DEGREE+1))
            upper+=k.upprod(ar,sum(z_abs))
            residual[i][c]+=upper
    models=[[(k.TM([z[0] for z in coeff[i][c]]),k.TM([z[1] for z in coeff[i][c]]))
             for c in range(4)] for i in range(20)]
    endpoint=[[sum_complex(coeff[i][c]) for c in range(4)] for i in range(20)]
    # All centers are point dyadics. Summation is exact: no inter-tile jump.
    if not all(x.lo==x.hi for row in endpoint for z in row for x in z):
        raise RuntimeError('Non-point endpoint: jump cannot be ignored')
    amplitude=max(sum(complex_abs_upper(z) for z in coeff[i][c]) for i in range(20) for c in range(4))
    return models,endpoint,max(max(row) for row in residual),amplitude


def apply_models(entries,states,rows):
    zero=k.TM.constant(k.ZERO,DEGREE)
    out=[[(zero,zero) for _ in range(4)] for _ in range(rows)]
    for i,j,re,im in entries:
        for c in range(4):
            out[i][c]=complex_add(out[i][c],complex_mul((re,im),states[j][c]))
    return out


def numeric_at(models,x=Fraction(1)):
    return np.array([[complex(float(Fraction(z[0].at(x.numerator,x.denominator).center().lo,k.SCALE)),
                              float(Fraction(z[1].at(x.numerator,x.denominator).center().lo,k.SCALE)))
                      for z in row] for row in models])


def prepared_model_bound(observed,phi):
    rows=[]
    for i in range(2):
        bound=0
        for c in range(2):
            re=observed[i][c][0]-phi[i*2+c]
            im=observed[i][c][1]
            bound+=re.range().abs_upper()+im.range().abs_upper()
        rows.append(bound)
    return max(rows)


def run_mode(mode,bg,mats,global_background,phi_global,boxes,checks,archive):
    expressions={name:matrix.subs(bg.ell,mode) for name,matrix in mats.items()}
    evaluate=evaluators({symbol:model for symbol,model in zip(bg.bg,global_background)},GLOBAL_DEGREE)
    az=split_matrix(expressions['balanced_generator'])
    ozmatrix=expressions['actual_dust_observable']*expressions['balancing_map_inverse']
    fzmatrix=expressions['full_field_reconstruction']*expressions['balancing_map_inverse']
    globals_={name:[(i,j,evaluate(re),evaluate(im)) for i,j,re,im in split_matrix(matrix)]
              for name,matrix in (('Az',expressions['balanced_generator']),('Oz',ozmatrix),('Fz',fzmatrix))}
    arows=[0]*20
    for i,j,re,im in globals_['Az']:arows[i]+=re.sup()+im.sup()
    norm_a=max(arows)
    steps=32
    while norm_a>steps*20*k.SCALE:steps*=2
    if steps>32768:raise RuntimeError('Declared tile budget exceeded')
    h=T/steps
    progress(f'ell={mode}: global operators enclosed; {steps} full-state tiles')
    bound_eval=evaluators(boxes)
    variables=bg.bg
    la=matrix_lipschitz(expressions['balanced_generator'],variables,bound_eval)
    lo=matrix_lipschitz(ozmatrix,variables,bound_eval)
    lf=matrix_lipschitz(fzmatrix,variables,bound_eval)
    un=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    maps={name:old.parent.import_matrix(obj,bg.sy) for name,obj in common.read_json(un['general_exact_maps_source'])['matrices'].items()}
    Tw,Twi,U,cm=[maps[name] for name in ('wave_map_Tw','wave_inverse_Twi','fast_cross_map_U','longitudinal_velocity_scaling_C')]
    a=bg.bg[0]
    den=1+s.Rational(22,375)*a*a/mode**2
    cw=Tw*(s.eye(20)-U/(mode*den)+U*U/(mode**2*den))
    cwi=(s.eye(20)+U/mode)*Twi
    cmi=s.eye(20);cmi[13,13]=a/mode
    transform=(cw*cm).subs(bg.ell,mode)
    inverse=(cmi*cwi).subs(bg.ell,mode)
    kt=5*matrix_norm(transform,bound_eval)
    kz=3*matrix_norm(inverse,bound_eval)
    ko=3*matrix_norm(ozmatrix*inverse,bound_eval)
    kf=3*matrix_norm(fzmatrix*inverse,bound_eval)
    state,initial_error,_=exact_initial(bg,mats,mode)
    max_defect=max_amplitude=max_model=0
    tiles=[];comparisons=[]
    initial_float=np.array([[complex(float(Fraction(z[0].lo,k.SCALE)),float(Fraction(z[1].lo,k.SCALE))) for z in row] for row in state])
    archived_initial=np.asarray(archive['initial_balanced'],float)
    archived_initial=archived_initial[...,0]+1j*archived_initial[...,1]
    initial_difference=float(np.max(np.abs(initial_float-archived_initial)))
    checks.add('original_initial_recipe_agreement_'+str(mode),initial_difference<=1e-10,initial_difference,'<=1e-10 diagnostic; exact initial discrepancy separately enclosed')
    chain=hashlib.sha256()
    for tile in range(steps):
        local_a=restrict_entries(globals_['Az'],tile,steps)
        models,end,defect,amplitude=state_polynomial(local_a,state,h)
        observed=apply_models(restrict_entries(globals_['Oz'],tile,steps),models,2)
        leading=[p.restrict(tile,steps,DEGREE) for p in phi_global]
        model_bound=prepared_model_bound(observed,leading)
        max_defect=max(max_defect,defect);max_amplitude=max(max_amplitude,amplitude);max_model=max(max_model,model_bound)
        body=common.encode([[[[x[0].lo,x[1].lo] for x in zip(z[0].coeff,z[1].coeff)] for z in row] for row in models])
        digest=hashlib.sha256(body).hexdigest();chain.update(bytes.fromhex(digest))
        tiles.append(dict(tile=tile,polynomial_sha256=digest,defect_upper=str(defect),state_amplitude_upper=str(amplitude),prepared_difference_upper=str(model_bound)))
        # All 257 original archive times are checked, including interior tiles.
        for index in range(257):
            numerator=index*steps-256*tile
            if 0<=numerator<256 or (tile==steps-1 and numerator==256):
                x=Fraction(numerator,256)
                fields=apply_models(restrict_entries(globals_['Fz'],tile,steps),models,22)
                old_w=np.asarray(archive['dust_observables'][index],float)
                old_f=np.asarray(archive['full_fields'][index],float)
                old_w=old_w[...,0]+1j*old_w[...,1];old_f=old_f[...,0]+1j*old_f[...,1]
                comparisons.append(dict(index=index,dust_difference=float(np.max(np.abs(numeric_at(observed,x)-old_w))),field_difference=float(np.max(np.abs(numeric_at(fields,x)-old_f)))))
        state=end
        if tile==0 or (tile+1)%64==0 or tile==steps-1:progress(f'ell={mode}: tile {tile+1}/{steps}, outward defect <= {k.display(max_defect):.6g}')
    checks.add('all_archive_times_four_columns_22_fields_'+str(mode),len(comparisons)==257 and max(row['dust_difference'] for row in comparisons)<=1e-8 and max(row['field_difference'] for row in comparisons)<=1e-8,
               dict(samples=len(comparisons),dust=max(row['dust_difference'] for row in comparisons),fields=max(row['field_difference'] for row in comparisons)), 'solver comparisons are diagnostic, not certificate')
    return dict(ell=mode,steps=steps,Az_infinity_majorant=k.upper_fraction(norm_a),initial_error_upper=k.upper_fraction(initial_error),state_defect_upper=k.upper_fraction(max_defect),state_amplitude_upper=k.upper_fraction(max_amplitude),prepared_approximant_difference_upper=k.upper_fraction(max_model),
                constants={name:k.upper_fraction(value) for name,value in (('L_Az',la),('L_Oz',lo),('L_Fz',lf),('K_T_infinity_to_Q',kt),('K_inverse_Q_to_infinity',kz),('K_observation_Q',ko),('K_fields_Q',kf))},
                final_state=[[[str(z[0].lo),str(z[1].lo)] for z in row] for row in state],tile_chain_sha256=chain.hexdigest(),archive_comparisons=comparisons),tiles


def calculate():
    parent=BASE+'r4c1_g3n5_dust_finite_energy_attempt_04/'
    digest='5310e9194079d2291a20e6857290f9a8f48ef9d33747e11b663139ea06dd08c7'
    if common.sha((ROOT/(parent+'summary.json')).read_bytes())!=digest:raise RuntimeError('Frozen parent receipt drift')
    ps=common.read_json(parent+'summary.json')
    pins=dict(ps['source_sha256'])
    pins.update({parent+name:value for name,value in ps['artifacts'].items()});pins[parent+'summary.json']=digest
    for rel in (SELF,KERNEL,CONTRACT,'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_ENERGY_REPORT_2026-10-12.md'):
        pins[rel]=common.sha((ROOT/rel).read_bytes())
    missing=common.inspect_pins(pins)
    paths=[ROOT/rel for rel in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before=old.parent.snapshot(paths)
    checks=common.Checks()
    arithmetic_controls(checks)
    checks.add('parent_complete_bounds_not_useful_accuracy',ps['passed']==ps['total']==89 and ps['finite_mode_error_bounds_proved'] and not ps['useful_finite_mode_accuracy_proved'] and not ps['physics_pass'])
    bg=old.Background()
    mats={name:old.parent.import_matrix(obj,bg.sy) for name,obj in common.read_json(old.PARENT+'matrices.json').items()}
    bc=common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    checks.add('saved_background_exact_written_approximant',bc['degree']==40 and bc['digits']==70 and bc['background_order']==[str(q) for q in bg.bg])
    background=[k.TM([k.IV.fraction(Fraction(pair[0])*T**j) for j,pair in enumerate(row)]) for row in bc['background_coefficients']]
    if any(Fraction(pair[1])!=0 for row in bc['background_coefficients'] for pair in row):raise ValueError('Complex background unsupported')
    transfer=common.read_json(frozen.PARENT+'transfer.json')
    phi=[k.TM([k.IV.fraction(Fraction(value)*T**j) for j,value in enumerate(row)]) for row in transfer['degree40_coefficients']]
    checks.add('global_polynomial_degrees',all(q.degree==GLOBAL_DEGREE and q.radius==0 for q in background+phi))
    evaluate=evaluators(dict(zip(bg.bg,background)),GLOBAL_DEGREE)
    rb=[background[i].derivative(T)-evaluate(bg.rates[i]) for i in range(11)]
    db=max(q.sup() for q in rb)
    true0=[k.ONE,k.IV.rational(3469,4620).sqrt(),k.ONE,k.ZERO,k.ZERO,k.ONE,k.ONE,k.IV.rational(1,4),k.IV.rational(1,5),k.IV.rational(1,5),k.ONE]
    eb0=max((q.coeff[0]-init).abs_upper() for q,init in zip(background,true0))
    un=common.read_json(BASE+'r4c1_g3n5_dust_uniform_propagator_attempt_02/formulas.json')
    boxes={bg.sy[name]:k.IV(k.IV.fraction(Fraction(values[0])-Fraction(1,100)).lo,
                           k.IV.fraction(Fraction(values[1])+Fraction(1,100)).hi)
           for name,values in un['background_boxes'].items()}
    evaluate_box=evaluators(boxes)
    lb=matrix_lipschitz(bg.rates,bg.bg,evaluate_box)
    eb=k.upprod(k.exp_upper(k.IV(lb).scale(T.numerator,T.denominator)),eb0+k.IV(db).scale(T.numerator,T.denominator).hi)
    margins=[min(poly.range().lo-boxes[var].lo,boxes[var].hi-poly.range().hi) for var,poly in zip(bg.bg,background)]
    checks.add('background_continuation_margin',min(margins)>eb,dict(margin=k.upper_fraction(min(margins)),error=k.upper_fraction(eb)))
    checks.add('positive_background_denominators',all(boxes[bg.bg[i]].lo>0 for i in (0,9,10)))
    checks.add('continuous_background_defect_not_sampled',db<k.IV.rational(1,10**20).lo,dict(defect=k.upper_fraction(db),initial=k.upper_fraction(eb0),error=k.upper_fraction(eb)))
    init_s={var:s.Rational(1) for var in bg.bg}
    init_s.update({bg.bg[1]:s.sqrt(s.Rational(3469,4620)),bg.bg[3]:s.Integer(0),bg.bg[4]:s.Integer(0),bg.bg[7]:s.Rational(1,4),bg.bg[8]:s.Rational(1,5),bg.bg[9]:s.Rational(1,5)})
    charge=bg.bg[0]**3*(bg.bg[2]*bg.bg[5]-bg.bg[4]*bg.bg[3])
    checks.add('exact_background_constraints_no_projection',s.simplify(bg.constraint.subs(init_s))==0 and s.simplify(bg.dt(s.Matrix([bg.constraint,charge]))[0])==0 and s.simplify(bg.dt(s.Matrix([charge]))[0])==0 and charge.subs(init_s)==1)
    m=mats['leading_dust_generator']
    mg=[[evaluate(m[i,j]) for j in range(2)] for i in range(2)]
    rphi=[]
    for i in range(2):
        for c in range(2):rphi.append(phi[i*2+c].derivative(T)-sum((mg[i][j]*phi[j*2+c] for j in range(2)),k.TM.constant(k.ZERO,GLOBAL_DEGREE)))
    dp=max(sum(rphi[i*2+c].sup() for c in range(2)) for i in range(2))
    phi_norm=max(sum(phi[i*2+c].sup() for c in range(2)) for i in range(2))
    lm=matrix_lipschitz(m,bg.bg,evaluate_box)
    phi0=max(sum((phi[i*2+c].coeff[0]-(k.ONE if i==c else k.ZERO)).abs_upper() for c in range(2)) for i in range(2))
    ep=k.upprod(k.exp_upper(k.IV.rational(21,10).scale(T.numerator,T.denominator)),phi0+k.IV(dp+k.upprod(k.upprod(lm,eb),phi_norm)).scale(T.numerator,T.denominator).hi)
    checks.add('continuous_leading_transfer_enclosed',ep<k.IV.rational(1,10**20).lo,dict(error=k.upper_fraction(ep),defect=k.upper_fraction(dp)))
    checks.add('Q_norm_constants_not_Hamiltonian',all(Fraction(value)>=Fraction(1,9) for value in un['lower_metric_diagonal']) and Fraction(un['mu_exact'])<60 and Fraction(20)*Fraction(9,8)<25)
    if not all(row['passed'] for row in checks.rows):raise RuntimeError('Arithmetic/background preflight failed: '+json.dumps([row for row in checks.rows if not row['passed']]))
    progress('Outward arithmetic, continuous background/leading defects and continuation verified')
    ar=common.read_json(old.PARENT+'trajectories.json')
    rows=[];all_tiles={}
    amplification=k.exp_upper(k.IV.rational(3,2))
    for mode in MODES:
        row,tiles=run_mode(mode,bg,mats,background,phi,boxes,checks,next(q for q in ar['modes'] if q['ell']==mode))
        value=lambda key: k.IV.fraction(Fraction(row[key])).hi
        const=lambda key:k.IV.fraction(Fraction(row['constants'][key])).hi
        forcing=value('state_defect_upper')+k.upprod(k.upprod(const('L_Az'),eb),value('state_amplitude_upper'))
        ew=k.upprod(amplification,k.upprod(const('K_T_infinity_to_Q'),value('initial_error_upper')+k.IV(forcing).scale(T.numerator,T.denominator).hi))
        ew_obs=k.upprod(const('K_observation_Q'),ew)+k.upprod(k.upprod(const('L_Oz'),eb),value('state_amplitude_upper'))
        ew_fields=k.upprod(const('K_fields_Q'),ew)+k.upprod(k.upprod(const('L_Fz'),eb),value('state_amplitude_upper'))
        model=value('prepared_approximant_difference_upper')+2*ew_obs+ep
        row.update(Q_state_error_upper=k.upper_fraction(ew),dust_numerical_error_upper=k.upper_fraction(ew_obs),field_numerical_error_upper=k.upper_fraction(ew_fields),prepared_true_model_error_upper=k.upper_fraction(model),
                   display=dict(dust_numerical_error=k.display(ew_obs),field_numerical_error=k.display(ew_fields),prepared_model_error=k.display(model)))
        checks.add('continuous_full_numerical_accuracy_'+str(mode),max(ew_obs,ew_fields)<=k.IV.rational(1,10**8).lo,row['display'],'<=1e-8 all four columns/22 fields throughout interval')
        checks.add('useful_prepared_model_error_'+str(mode),model<=k.IV.rational(1,100).lo,k.display(model),'<=1/100 whole interval, original two-column input span')
        checks.add('full_coupled_columns_retained_'+str(mode),len(row['final_state'])==20 and all(len(q)==4 for q in row['final_state']) and len(tiles)==row['steps'])
        rows.append(row);all_tiles[str(mode)]=tiles
        progress(f'ell={mode}: certified numerical field error <= {k.display(ew_fields):.6g}; prepared model error <= {k.display(model):.6g}')
    checks.add('input_pins_after',common.inspect_pins(pins)==missing)
    checks.add('source_size_mtime_hash_preserved',old.parent.snapshot(paths)==before,dict(files=len(before)))
    passed=sum(q['passed'] for q in checks.rows);ok=passed==len(checks.rows)
    numerical=all(q['passed'] for q in checks.rows if q['name'].startswith('continuous_full_numerical_accuracy_'))
    useful=all(q['passed'] for q in checks.rows if q['name'].startswith('useful_prepared_model_error_'))
    certificate=dict(arithmetic=dict(bits=k.BITS,endpoint_unit='2^-256',rounding='integer floor/ceiling OUTWARD',global_degree=GLOBAL_DEGREE,local_degree=DEGREE),
                     background=dict(defect=k.upper_fraction(db),initial_error=k.upper_fraction(eb0),Lipschitz=k.upper_fraction(lb),error=k.upper_fraction(eb),continuation_margin=k.upper_fraction(min(margins))),
                     leading=dict(defect=k.upper_fraction(dp),Lipschitz=k.upper_fraction(lm),amplitude=k.upper_fraction(phi_norm),error=k.upper_fraction(ep)),modes=rows,
                     inequalities=['eb <= exp(Lb*T)(eb0+T db)','ew <= exp(30T) K_T (ez0+T[dz+L_A eb amplitude])',
                                   'observable/field error <= K_Q ew + L_map eb amplitude','prepared model error <= approximant difference + 2*observable numerical error + leading error'],
                     domain='ell=4,8,16,32,64; 0<=t<=1/20; original B1 shell/J=1, original prepared/complementary initial recipe; all 20 states/four columns/22 fields',
                     no_projection_during_evolution=True,physical_window_proved=False,physics_pass=False)
    bodies={'certificate.json':common.encode(certificate),'tile_certificates.json':common.encode(all_tiles)}
    summary=dict(schema='r4c1-g3n5-dust-certified-numerical-v1',validation='PASS_LOCAL_CHECKS' if ok else 'FAIL_LOCAL_CHECKS',passed=passed,total=len(checks.rows),checks=checks.rows,
                 status='CERTIFIED_FINITE_MODE_NUMERICAL_AND_USEFUL_ERROR' if ok else 'CERTIFIED_NUMERICAL_ROUTE_ACCEPTANCE_UNMET',
                 continuous_finite_mode_numerical_accuracy_proved=numerical,useful_finite_mode_accuracy_proved=useful and numerical,full_dust_milestone_complete=False,
                 physical_validity_window_proved=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',
                 K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=missing,
                 artifacts={name:common.sha(body) for name,body in bodies.items()},runtime=dict(python=platform.python_version(),sympy=s.__version__,numpy=np.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED','Stage2':'STOP_AND_ASSESS_DOMAIN_UNRESOLVED','Stage3':'NOT_ENTERED'})
    bodies['summary.json']=common.encode(summary)
    return bodies,summary


def main():
    global PROGRESS
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default=BASE+'r4c1_g3n5_dust_certified_numerical_attempt_01')
    parser.add_argument('--replay')
    parser.add_argument('--progress-file')
    args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():raise FileExistsError('Refuse overwrite')
    if args.progress_file and not args.replay:
        pp=(ROOT/args.progress_file).resolve();pp.relative_to((ROOT/'.local/itsm-context').resolve())
        PROGRESS=pp.open('x',encoding='utf-8')
    try:bodies,summary=calculate()
    except Exception as exc:
        if PROGRESS is not None:traceback.print_exc(file=PROGRESS);PROGRESS.flush()
        summary=dict(schema='r4c1-g3n5-dust-certified-numerical-v1',validation='COMPUTATION_INCOMPLETE',
                     passed=None,total=None,status='CERTIFICATE_NOT_ESTABLISHED',
                     exception_type=type(exc).__name__,exception_message=str(exc),
                     continuous_finite_mode_numerical_accuracy_proved=False,useful_finite_mode_accuracy_proved=False,
                     full_dust_milestone_complete=False,physics_pass=False,gate_effect='NONE',Rule9_cleared=False,
                     review_status='DEFERRED',canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
                     Stage4A='CLOSED',Stage2='STOP_AND_ASSESS_DOMAIN_UNRESOLVED',Stage3='NOT_ENTERED',
                     source_sha256={rel:common.sha((ROOT/rel).read_bytes()) for rel in (SELF,KERNEL,CONTRACT)},
                     checks=[],artifacts={})
        bodies={'summary.json':common.encode(summary)}
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',validation=summary['validation'],passed=summary['passed'],total=summary['total'],physics_pass=False)))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    if PROGRESS is not None:PROGRESS.close()
    return int(summary['validation']!='PASS_LOCAL_CHECKS')


if __name__=='__main__':raise SystemExit(main())
