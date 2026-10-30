"""Continuous full twenty-state finite-mode B1 certificate, not nonlinear admission."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,traceback
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_B1_PROPAGATOR_V1_CONTRACT_2026-10-29.md'
PARENT='Analysis/MasterTests/outputs/r4c1_b1_dust_reconstruction_v1_attempt_01/summary.json'
PSHA='7f4134defc9dd25b6a831d154f195a308a17b8d3ee01c29643a764b088c51e4a'
DRIFT='Analysis/MasterTests/outputs/r4c1_b1_kinetic_drift_v1_attempt_01/summary.json'
INSTANT='Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json'
KERNEL='Analysis/MasterTests/dust_certified_arithmetic_v1.py'
KSHA='f868032dcd939a52c3299ac66d5f4c18d02c5681bac7391bcce67732bc026599'
REPORT='Theory/Gates/RES-001/RES001_R4C1_B1_DUST_RECONSTRUCTION_V1_REPORT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda v:(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
READ=lambda p:json.loads((ROOT/p).read_bytes())
clean=lambda z:s.factor(s.cancel(z))
T=F(1,20);BGDEG=32;DEG=24;STEPS=64;MODES=(1,7,40);DIM=20


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj


k=load('B1_certified_integer_kernel',KERNEL)
IV,TM=k.IV,k.TM
Z,O,SCALE=k.ZERO,k.ONE,k.SCALE
mulup=k.upprod
pack=lambda v:str(F(int(v),SCALE))
display=lambda v:float(F(int(v),SCALE))


def normup(values):
    total=sum(int(v)**2 for v in values);q=isqrt(total)
    return q+(q*q<total)


def expup(value):
    value=max(0,int(value));bits=0
    while value>(SCALE<<bits):bits+=1
    ans=k.exp_upper(IV(value).scale(1,1<<bits))
    for _ in range(bits):ans=mulup(ans,ans)
    return ans


def evaluator(env,degree=None):
    cache={}
    def ev(expr):
        if expr in cache:return cache[expr]
        if expr.is_Rational:
            ans=IV.rational(int(expr.p),int(expr.q))
            if degree is not None:ans=TM.constant(ans,degree)
        elif expr.is_Symbol:ans=env[expr]
        elif expr.is_Add:ans=sum((ev(q) for q in expr.args),0)
        elif expr.is_Mul:
            ans=1
            for q in expr.args:ans=ans*ev(q)
        elif expr.is_Pow and expr.exp.is_Integer:ans=ev(expr.base).power(int(expr.exp))
        elif expr.is_Pow and expr.exp==s.Rational(1,2) and not expr.base.free_symbols:
            ans=evaluator({})(expr.base).sqrt()
            if degree is not None:ans=TM.constant(ans,degree)
        else:raise ValueError('unsupported proof arithmetic '+str(expr))
        cache[expr]=ans;return ans
    return ev


def intervals(matrix,ev):return [[ev(z) for z in row] for row in matrix.tolist()]
def matnorm(matrix,ev):return normup(ev(z).abs_upper() for z in matrix)
def vectornorm(values):return normup(z.abs_upper() for z in values)


def symbolic_inputs():
    a=s.Symbol('a',positive=True);H=s.Symbol('H',real=True);wave=s.Symbol('k',real=True,nonzero=True)
    rest=s.symbols('u v r du dv dr p psi rho',real=True);variables=(a,H)+rest
    loc={str(v):v for v in variables+(wave,)}
    parse=lambda rows:s.Matrix([[s.sympify(z,locals=loc) for z in row] for row in rows])
    f=READ(DRIFT)['formulas'];dust=READ(PARENT)['formulas'];instant=READ(INSTANT)['formulas']
    M,B,Q,Md,Bd=[parse(f[n]) for n in ('M','B','Q','M_dot','B_dot')]
    G=s.zeros(20);G[:10,10:20]=s.eye(10)
    G[10:20,:10]=-M.inv()*(Bd-Q);G[10:20,10:20]=-M.inv()*(Md+B-B.conjugate().T)
    G=G.applyfunc(clean)
    flow=s.Matrix([s.sympify(z,locals=loc) for z in f['background_flow']])
    initial=[s.sympify(f['initial'][str(v)],locals=loc) for v in variables]
    rec=parse(f['constraint_solution']).col_join(parse(dust['density_row'])).col_join(parse(dust['epsilon_scaled_row']))
    return variables,wave,flow,initial,G,parse(instant['normalization']),rec


def background_certificate(variables,flow,initial,check):
    ev=evaluator({});exact=[ev(z) for z in initial];centers=[z.center() for z in exact]
    radii=list(map(F,('1/10','1/10','1/50','7/100','1/25','1/5','3/10','3/10','1/10','1/50','1/10')))
    box=[c+IV(-IV.fraction(rad).hi,IV.fraction(rad).hi) for c,rad in zip(centers,radii)]
    be=evaluator(dict(zip(variables,box)));fr=[be(z) for z in flow]
    margins=[]
    for i,(rad,rate,raw,center) in enumerate(zip(radii,fr,exact,centers)):
        initerr=max(center.lo-raw.lo,raw.hi-center.hi)
        need=IV(rate.abs_upper()).scale(T.numerator,T.denominator).hi+initerr
        limit=IV.fraction(rad).lo;check('background_strict_tube_'+str(i),need<limit)
        margins.append(pack(limit-need))
    jac=flow.jacobian(variables)
    lip=max(sum(be(jac[i,j]).abs_upper() for j in range(len(variables))) for i in range(len(variables)))
    polys=[TM.constant(c,BGDEG) for c in centers]
    for n in range(BGDEG):
        pe=evaluator(dict(zip(variables,polys)),BGDEG);rates=[pe(z) for z in flow]
        new=[]
        for poly,rate in zip(polys,rates):
            coeff=list(poly.coeff);coeff[n+1]=rate.coeff[n].scale(T.numerator,T.denominator*(n+1)).center()
            new.append(TM(coeff))
        polys=new
    pe=evaluator(dict(zip(variables,polys)),BGDEG)
    residual=max((poly.derivative(T)-pe(rate)).sup() for poly,rate in zip(polys,flow))
    initial_error=max(max(c.lo-v.lo,v.hi-c.hi) for c,v in zip(centers,exact))
    for i,(poly,bb) in enumerate(zip(polys,box)):
        rr=poly.range();check('background_polynomial_in_convex_tube_'+str(i),bb.lo<=rr.lo<=rr.hi<=bb.hi)
    error=mulup(initial_error+IV(residual).scale(T.numerator,T.denominator).hi,
                expup(IV(lip).scale(T.numerator,T.denominator).hi))
    # True existence follows from the sealed B1 theorem; strict tube gives these sharper bounds.
    check('background_positive_a_and_rho',box[0].lo>0 and box[-1].lo>0)
    check('background_expanding',box[1].lo>0)
    check('physical_norm_scale_bound',(F(6,5)**2)>F(11,10)**3)
    check('background_accuracy_useful',error<IV.rational(1,10**20).lo)
    return polys,box,error,dict(degree=BGDEG,tube=[z.encode() for z in box],strict_margins=margins,
        initial_error=pack(initial_error),residual=pack(residual),Lipschitz=pack(lip),
        accumulated_error=pack(error),polynomial=[z.encode() for z in polys])


def phase_matrix(G):
    edges=[[] for _ in range(DIM)];bits=[None]*DIM
    for i in range(DIM):
        for j in range(DIM):
            z=G[i,j]
            if z==0:continue
            real,imag=s.expand_complex(z).as_real_imag();real,imag=clean(real),clean(imag)
            if real!=0 and imag!=0:raise ValueError('mixed Fourier parity entry')
            parity=int(imag!=0);edges[i].append((j,parity));edges[j].append((i,parity))
    for seed in range(DIM):
        if bits[seed] is not None:continue
        bits[seed]=0;todo=[seed]
        while todo:
            i=todo.pop()
            for j,parity in edges[i]:
                wanted=bits[i]^parity
                if bits[j] is None:bits[j]=wanted;todo.append(j)
                elif bits[j]!=wanted:raise ValueError('inconsistent Fourier parity')
    return s.diag(*[s.I**z for z in bits]),bits


def run_mode(wavenumber,variables,wave,G,R0,reconstruction,bg,box,bg_error,check):
    print('B1_PROPAGATOR_MODE_START '+str(wavenumber),flush=True)
    phase,bits=phase_matrix(G);realG=(phase.conjugate().T*G*phase).applyfunc(clean)
    check('mode_phase_reality_'+str(wavenumber),all(clean(s.im(z))==0 for z in realG))
    check('mode_phase_q_velocity_agree_'+str(wavenumber),bits[:10]==bits[10:])
    check('mode_phase_commutes_kinetic_'+str(wavenumber),R0*phase[:10,:10]==phase[:10,:10]*R0)
    W=s.diag(*([s.Integer(wavenumber)]*9+[1+s.Rational(2,5)*wavenumber**2]))
    balance=s.diag(W*R0,R0);transform=balance*phase.conjugate().T
    inverse=phase*balance.inv()
    check('mode_transform_inverse_'+str(wavenumber),all(clean(z)==0 for z in transform*inverse-s.eye(DIM)))
    C=(transform*G.subs(wave,wavenumber)*inverse).applyfunc(clean)
    check('mode_full_generator_real_'+str(wavenumber),all(clean(s.im(z))==0 for z in C))
    sym=((C+C.T)/2).applyfunc(clean)
    entries=[(i,j,C[i,j]) for i in range(DIM) for j in range(DIM) if C[i,j]!=0]
    boxev=evaluator(dict(zip(variables,box)))
    LA=sum(matnorm(C.diff(v),boxev) for v in variables)
    coefficient_error=mulup(LA,bg_error)
    # Output phase is unitary; density and scaled epsilon rows remain real.
    outputphase=s.diag(1,1,1,-s.I,1,1)
    rec=(outputphase*reconstruction.subs(wave,wavenumber)*inverse).applyfunc(clean)
    check('mode_reconstruction_real_'+str(wavenumber),all(clean(s.im(z))==0 for z in rec))
    rec_norm=matnorm(rec,boxev)
    rec_lip=sum(matnorm(rec.diff(v),boxev) for v in variables)
    density_norm=matnorm(rec[4,:],boxev)
    h=T/STEPS;phi0=[[O if i==j else Z for j in range(DIM)] for i in range(DIM)]
    rows=[];sum_defect=0;sum_jumps=0;max_mu=0;max_phi=0;nonzero_tails=0
    for tile in range(STEPS):
        localbg=[p.restrict(tile,STEPS,DEG) for p in bg]
        ev=evaluator(dict(zip(variables,localbg)),DEG)
        models=[(i,j,ev(expr)) for i,j,expr in entries]
        actual_box=[p.range()+IV(-bg_error,bg_error) for p in localbg]
        # The actual background error has already been proved in the common convex tube.
        ae=evaluator(dict(zip(variables,actual_box)))
        mu=max(0,max(ae(sym[i,i]).hi+sum(ae(sym[i,j]).abs_upper() for j in range(DIM) if i!=j)
                     for i in range(DIM)))
        max_mu=max(max_mu,mu)
        coefficients=[phi0];low_defect=0
        # Global propagator is continued from its own endpoint, never reset/projected.
        for n in range(DEG):
            sums=[[Z for _ in range(DIM)] for _ in range(DIM)]
            for i,j,model in models:
                for ell in range(n+1):
                    av=model.coeff[ell]
                    if av.is_zero():continue
                    prior=coefficients[n-ell][j]
                    for col,pv in enumerate(prior):
                        if not pv.is_zero():sums[i][col]=sums[i][col]+av*pv
            nxt=[];errors=[]
            for row in sums:
                nr=[]
                for val in row:
                    scaled=val.scale(h.numerator,h.denominator*(n+1));center=scaled.center()
                    nr.append(center);errors.append(max(center.lo-scaled.lo,scaled.hi-center.hi))
                nxt.append(nr)
            low_defect+=IV(normup(errors)).scale((n+1)*h.denominator,h.numerator).hi
            coefficients.append(nxt)
        anorms=[normup(model.coeff[j].abs_upper() for _,_,model in models) for j in range(DEG+1)]
        pnorms=[normup(v.abs_upper() for row in coeff for v in row) for coeff in coefficients]
        tail=sum(mulup(anorms[j],pnorms[ell]) for j in range(DEG+1)
                 for ell in range(DEG+1) if j+ell>=DEG)
        remainder=mulup(normup(model.radius for _,_,model in models),sum(pnorms))
        uncertain=mulup(coefficient_error,sum(pnorms));defect=low_defect+tail+remainder+uncertain
        sum_defect+=IV(defect).scale(h.numerator,h.denominator).hi
        nonzero_tails+=int(tail>0);max_phi=max(max_phi,sum(pnorms))
        endpoint=[];jump=[]
        for i in range(DIM):
            out=[]
            for j in range(DIM):
                value=sum((mat[i][j] for mat in coefficients),Z);center=value.center();out.append(center)
                jump.append(max(center.lo-value.lo,value.hi-center.hi))
            endpoint.append(out)
        jnorm=normup(jump);sum_jumps+=jnorm;phi0=endpoint
        coeffhash=SHA(ENC([[[v.encode() for v in row] for row in mat] for mat in coefficients]))
        rows.append(dict(tile=tile,mu=pack(mu),low_defect=pack(low_defect),high_tail=pack(tail),
            coefficient_remainder=pack(remainder),background_forcing=pack(uncertain),
            total_defect=pack(defect),interface_jump=pack(jnorm),polynomial_sha256=coeffhash))
        if tile%8==7:print('B1_PROPAGATOR_TILE '+str(wavenumber)+' '+str(tile+1)+'/'+str(STEPS),flush=True)
    growth=expup(IV(max_mu).scale(T.numerator,T.denominator).hi)
    error=mulup(growth,sum_defect+sum_jumps)
    maxW=max(W.diagonal());maxWf=F(int(maxW.p),int(maxW.q))
    conversion=F(6,5)*maxWf;physical=IV(error).scale(conversion.numerator,conversion.denominator).hi
    reconstruction_error=mulup(rec_norm,error)+mulup(mulup(rec_lip,bg_error),max_phi)
    density_gain=mulup(density_norm,max_phi+error)
    density_gain=IV(density_gain).scale(maxWf.numerator,maxWf.denominator).hi
    amplitude=(IV(box[-1].lo)/IV(2*density_gain)).lo
    check('mode_nonzero_convolution_tails_retained_'+str(wavenumber),nonzero_tails==STEPS)
    check('mode_continuous_physical_error_'+str(wavenumber),physical<=IV.rational(1,10**8).lo,pack(physical))
    check('mode_positive_linear_density_amplitude_'+str(wavenumber),amplitude>0,pack(amplitude))
    # This independent solver is a diagnostic only; proof constants above use integer intervals.
    fn=s.lambdify(variables,C,modules='numpy',cse=True)
    syms,w,flow,initial,_,_,_=symbolic_inputs();ff=s.lambdify(variables,flow,modules='numpy',cse=True)
    initial_num=np.asarray([float(z) for z in initial],dtype=float)
    def rhs(t,yy):
        b=yy[:len(variables)];mat=yy[len(variables):].reshape(DIM,DIM)
        return np.concatenate((np.asarray(ff(*b),dtype=float).reshape(-1),
                               (np.asarray(fn(*b),dtype=float)@mat).reshape(-1)))
    numeric=solve_ivp(rhs,(0,float(T)),np.concatenate((initial_num,np.eye(DIM).reshape(-1))),
                      method='DOP853',rtol=2e-12,atol=2e-14)
    approx=np.asarray([[display(z.lo) for z in row] for row in phi0])
    difference=float(np.max(np.abs(approx-numeric.y[len(variables):,-1].reshape(DIM,DIM))))
    check('mode_independent_DOP853_diagnostic_'+str(wavenumber),numeric.success and difference<1e-8,format(difference,'.10e'))
    print('B1_PROPAGATOR_MODE_COMPLETE '+str(wavenumber)+' error='+format(display(physical),'.8e'),flush=True)
    return dict(k=wavenumber,degree=DEG,tiles=STEPS,phase_bits=bits,
        norm=dict(R0=[[str(v) for v in row] for row in R0.tolist()],W=[str(z) for z in W.diagonal()],
                  physical_conversion=str(conversion),input='initial physical kinetic norm'),
        coefficient_Lipschitz=pack(LA),background_coefficient_error=pack(coefficient_error),
        logarithmic_norm=pack(max_mu),growth=pack(growth),integrated_defect=pack(sum_defect),interface_jumps=pack(sum_jumps),
        continuous_transformed_error=pack(error),continuous_physical_relative_error=pack(physical),
        approximate_propagator_sup=pack(max_phi),reconstruction_norm=pack(rec_norm),reconstruction_Lipschitz=pack(rec_lip),
        reconstruction_error_per_unit_transformed_input=pack(reconstruction_error),
        linear_density_gain_per_unit_initial_kinetic_norm=pack(density_gain),
        linear_density_amplitude_limit=pack(amplitude),final_matrix=[[z.encode() for z in row] for row in phi0],
        tile_certificates=rows,independent_diagnostic=dict(method='DOP853',max_entry_difference=format(difference,'.10e')))


def calculate():
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA
    parent=READ(PARENT);assert parent['passed']==parent['total'] and parent['exact_clock_conservation']
    pins=dict(parent['source_sha256']);pins[PARENT]=PSHA;pins[KERNEL]=KSHA
    for name in (SELF,CONTRACT,REPORT):pins[name]=SHA((ROOT/name).read_bytes())
    snapshots={}
    for name,want in pins.items():
        path=ROOT/name;sc=Path(str(path)+'.sha256')
        assert SHA(path.read_bytes())==want and sc.read_text().split()[0].lower()==want,name
        for z in (path,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    check('arithmetic_rational_enclosure',IV.rational(1,3).contains(F(1,3)))
    rt=IV.rational(2).sqrt();check('arithmetic_sqrt_outward',rt.lo**2<=2*SCALE**2<=rt.hi**2)
    den=TM([IV.rational(2),O]+[Z]*3);identity=den*den.inverse()-1
    check('arithmetic_Taylor_inverse_residual',identity.range().contains(0))
    variables,wave,flow,initial,G,R0,rec=symbolic_inputs()
    check('full_state_dimension_preserved',G.shape==(20,20) and rec.shape==(6,20))
    instant=READ(INSTANT)['formulas'];M0=s.Matrix([[s.sympify(v) for v in row] for row in instant['reduced_kinetic']])
    check('physical_kinetic_normalization_exact',all(clean(z)==0 for z in R0.T*R0-M0))
    bg,box,bg_error,bgcert=background_certificate(variables,flow,initial,check)
    print('B1_PROPAGATOR_BACKGROUND_CERTIFIED error='+format(display(bg_error),'.8e'),flush=True)
    modes=[run_mode(mode,variables,wave,G,R0,rec,bg,box,bg_error,check) for mode in MODES]
    for name,(digest,mtime) in snapshots.items():
        p=ROOT/name;assert SHA(p.read_bytes())==digest and p.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    return dict(kind='R4C1_B1_PROPAGATOR_V1',passed=sum(v['passed'] for v in checks),total=len(checks),checks=checks,
        source_sha256=pins,arithmetic=dict(bits=k.BITS,endpoint_unit='2^-256',rounding='integer OUTWARD floor/ceiling'),
        time_interval=['0','1/20'],background=bgcert,modes=modes,
        accepted=all(F(v['continuous_physical_relative_error'])<=F(1,10**8) for v in modes)
                 and all(v['passed'] for v in checks),
        scope='Full finite-mode LINEAR old homogeneous B1 control only; no slow-graph projection',
        all_frequency_estimate=False,nonlinear_admission=False,nodal_G1_admitted=False,physical_window_demonstrated=False,
        physics_pass=False,gate_effect='NONE',review='DEFERRED',G1='INCOMPLETE',G2='INCOMPLETE',G3='INCOMPLETE',
        G4='INCOMPLETE',G5='INCOMPLETE',G6='INCOMPLETE',MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED')


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--out');g.add_argument('--replay');args=parser.parse_args()
    out=None
    if args.out:out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False)
    try:result=calculate()
    except Exception:
        if out is not None:
            data=ENC(dict(kind='R4C1_B1_PROPAGATOR_V1_FAILED',traceback=traceback.format_exc(),physics_pass=False))
            f=out/'failure.json';f.write_bytes(data);Path(str(f)+'.sha256').write_text(SHA(data)+'  failure.json\n',encoding='ascii')
        raise
    data=ENC(result)
    if args.replay:
        target=ROOT/args.replay;assert target.read_bytes()==data,'immutable replay mismatch'
        assert Path(str(target)+'.sha256').read_text().split()[0]==SHA(data);print('IMMUTABLE_REPLAY_EXACT',flush=True)
    else:
        f=out/'summary.json';f.write_bytes(data);Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({z:result[z] for z in ('passed','total','accepted','physics_pass')}))
    raise SystemExit(0 if result['accepted'] else 2)


if __name__=='__main__':main()
