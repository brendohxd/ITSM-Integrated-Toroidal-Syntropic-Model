"""Exact retained-branch source map; not a nonlinear weak-evolution proof."""
import argparse,hashlib,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_finite_band_domain_v1_attempt_01/summary.json'
PSHA='41761b47e4256e48fad9d06fbad531c84c2b02a82f346432469c3cda2a074868'
OPERATOR='Analysis/MasterTests/outputs/r4c1_constrained_principal_v1_attempt_01/summary.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_PRINCIPAL_SOURCE_COMPATIBILITY_V1_CONTRACT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda z:mp.nstr(z,65)


def calculate():
    mp.mp.dps=160;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,value):
        rows=list(value) if isinstance(value,s.MatrixBase) else [value]
        bad=[str(t) for z in rows if (t:=s.factor(s.cancel(z)))!=0]
        check(name,not bad,bad)
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    pins=dict(READ(PARENT)['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify()
    w=s.Symbol('w',real=True,nonzero=True);c=s.Symbol('c',real=True);Z=s.Symbol('Z_background',real=True)
    P=s.Matrix([[s.sympify(z,locals={'w':w,'c':c,'Z_background':Z}) for z in row]
                for row in READ(OPERATOR)['formulas']['reduced_pencil']])
    b=-P[9,10].subs(c,0);r=b*(1+w*w*c*c)
    zero('original_auxiliary_column',P[:,10]-s.Matrix([0]*9+[-r,0]))
    zero('original_pencil_symmetry',P-P.T)
    M=P.diff(c,2)/2;C=P.diff(c).subs(c,0);G=P.subs(c,0)
    ez=s.eye(11)[:,10]
    block=(0,2,4,5);other=(1,3,6,7,8)
    formulas=[]
    for branch in (-1,1):
        c0=branch*s.I/w;Q=P.subs(c,c0).applyfunc(s.factor)
        # Algebraic congruence at a complex frequency; not a physical field chart.
        D=s.eye(9);D[5,5]=s.I/s.sqrt(1+w*w)
        B=(D.T*Q[:9,:9]*D).applyfunc(s.factor);d=(D.T*Q[:9,9]).applyfunc(s.factor)
        zero('isolated_four_block_'+str(branch),B.extract(block,other))
        zero('isolated_other_scalar_sources_'+str(branch),d.extract(other,(0,)))
        det4=s.factor(B.extract(block,block).det(method='domain-ge'))
        det2=s.factor(B.extract((1,3),(1,3)).det(method='domain-ge'))
        zero('four_block_determinant_'+str(branch),det4+205/(256*w**8*(w**4+5*w*w+60)))
        zero('two_block_determinant_'+str(branch),det2-(1+w*w)**2/(48*w**4))
        for j in (6,7,8):zero('scalar_diagonal_'+str(branch)+'_'+str(j),B[j,j]+(1+w*w)/w**2)
        rebuilt=s.zeros(9)
        for slots in (block,(1,3),(6,),(7,),(8,)):
            for i in slots:
                for j in slots:rebuilt[i,j]=B[i,j]
        zero('complete_nine_field_block_structure_'+str(branch),B-rebuilt)
        detB=s.factor(det4*det2*s.prod(B[j,j] for j in (6,7,8))/D.det()**2)
        zero('complete_branch_block_determinant_'+str(branch),detB+205*(1+w*w)**6/(12288*w**18*(w**4+5*w*w+60)))
        x0=B.extract(block,block).inv(method='DM')*d.extract(block,(0,));x=s.zeros(9,1)
        for j,value in zip(block,x0):x[j]=value
        x=(D*x).applyfunc(s.factor)
        zero('full_nine_field_source_dressing_'+str(branch),Q[:9,:9]*x-Q[:9,9])
        expected=s.zeros(9,1);expected[4]=-30*Z*w/11
        expected[5]=-branch*s.I*w*(1200*Z+11*w*w+11)/(440*s.sqrt(1+w*w))
        zero('exact_dressed_source_covector_'+str(branch),x-expected)
        aeff=s.factor(s.cancel(Q[9,9]-(Q[9,:9]*x)[0]))
        target=3*(w*w*s.Abs(w)-140*w*w-140)/(560*w*w)
        zero('effective_scalar_independent_of_background_Z_'+str(branch),aeff-target)
        # On 0<|w|<=1/500 the remaining term is strictly negative.
        zero('effective_scalar_sign_identity_'+str(branch),aeff+3/(4*w*w)-3*(s.Abs(w)-140)/560)
        rp=s.diff(r,c).subs(c,c0)
        q1=s.zeros(11,1);q1[9]=rp/aeff
        for j in range(9):q1[j]=-x[j]*q1[9]
        zero('full_quadratic_generalized_chain_'+str(branch),Q*q1+P.diff(c).subs(c,c0)*ez)
        left_top=ez.T*(C+c0*M);left_bottom=ez.T*M
        zero('left_companion_identity_first_'+str(branch),-ez.T*G-c0*left_top)
        zero('left_companion_identity_second_'+str(branch),left_top-ez.T*C-c0*left_bottom)
        zero('direct_left_right_pairing_zero_'+str(branch),(left_top*ez+c0*left_bottom*ez)[0])
        formulas.append(dict(branch=branch,branch_frequency=str(c0),nine_block_determinant=str(detB),
                             dressed_source_covector=[str(v) for v in x],effective_scalar=str(aeff),
                             generalized_configuration_vector=[str(s.factor(v)) for v in q1]))
    # Verify the general inverse-source identity without solving a new physical source.
    RR,aa=s.symbols('r a',nonzero=True);FF=s.symbols('FZ');fps=s.symbols('Fpsi')
    # In scalar-reduced form H=d^T B^-1 F9 and K=d^T B^-1 d.
    HH,KK=s.symbols('H K');psi=-FF/RR
    projected_y=HH+KK*FF/RR
    z=(HH-fps)/RR-(aa-KK)*FF/RR**2
    zero('general_auxiliary_source_equation',-RR*psi-FF)
    zero('general_scalar_source_equation',projected_y+aa*psi-RR*z-fps)

    Pnum=s.lambdify((w,Z,c),P,modules='mpmath')
    controls=[]
    for sign in (-1,1):
        ww=mp.mpf(sign)/1000
        for zztext in ('0','0.00001'):
            zz=mp.mpf(zztext)
            for branch in (-1,1):
                cv=branch*mp.j/ww;cc=cv+mp.mpf(1)/7;full=mp.matrix(Pnum(ww,zz,cc))
                bb=full[:9,:9];dd=full[:9,9];an=full[9,9];rn=-full[9,10]
                xx=mp.lu_solve(bb,dd);effective=an-(dd.T*xx)[0]
                for fztext in ('0','0.076923076923076923076923076923'):
                    source=mp.matrix([mp.mpf((-1)**j*(j+1))/17 for j in range(10)]+[mp.mpf(fztext)])
                    y0=mp.lu_solve(bb,source[:9,:]);ps=-source[10]/rn
                    yy=y0+xx*source[10]/rn
                    az=((dd.T*y0)[0]-source[9])/rn-effective*source[10]/rn**2
                    predicted=mp.matrix(list(yy)+[ps,az]);observed=mp.lu_solve(full,source)
                    error=max(abs(t) for t in predicted-observed)/(1+max(abs(t) for t in observed))
                    name=f'full_eleven_solve_w{sign}_Z{zztext}_branch{branch}_FZ{fztext}'
                    check(name,error<mp.mpf('1e-30'),show(error))
                    controls.append(dict(test=name,error=show(error)))
                # A SYNTHETIC Vz covector: direct FZ=0, yet the Z simple pole is nonzero.
                near=cv+mp.mpf('1e-35');pn=mp.matrix(Pnum(ww,zz,near))
                force=mp.matrix([mp.mpf(0)]*11);force[5]=1
                solved=mp.lu_solve(pn,force);rr=-pn[9,10]
                expected=-branch*mp.j*ww*(1200*zz+11*ww*ww+11)/(440*mp.sqrt(1+ww*ww))
                error=abs(rr*solved[10]-expected)/(1+abs(expected))
                check(f'nonzero_simple_pole_w{sign}_Z{zztext}_branch{branch}',error<mp.mpf('1e-25') and abs(expected)>mp.mpf('1e-10'),show(error))
                force[5]=0;force[10]=1;solved=mp.lu_solve(pn,force)
                ae=3*(ww*ww*abs(ww)-140*ww*ww-140)/(560*ww*ww)
                error=abs(rr**2*solved[10]+ae)/(1+abs(ae))
                check(f'nonzero_double_pole_w{sign}_Z{zztext}_branch{branch}',error<mp.mpf('1e-25'),show(error))
    verify();ok=all(t['passed'] for t in checks)
    return dict(result_id='R4C1-PRINCIPAL-SOURCE-COMPATIBILITY-V1',source_sha256=pins,
                checks=checks,passed=sum(t['passed'] for t in checks),total=len(checks),
                formulas=dict(b=str(b),branches=formulas,
                    inverse_source='psi=-FZ/r; y=B^-1*F9+B^-1*d*FZ/r; Z=(d^T*B^-1*F9-Fpsi)/r-a_eff*FZ/r^2',
                    homogeneous_auxiliary_source_compatibility='FZ identically zero near c0; require Fpsi(c0)=x(c0)^T*F9(c0) for a regular response',
                    domain='real 0<abs(w)<=1/500, any finite real Z_background; branch block nonsingular, a_eff< -3/(4*w^2)'),
                controls=controls,probe_scope='SYNTHETIC_PRINCIPAL_SOURCES_ONLY',
                direct_left_pairing_sufficient=False,actual_nonlinear_cusp_projection_computed=False,
                admitted_prepared_weak_domain=False,physical_finite_frequency_spectrum_derived=False,
                time_evolution=False,G1_complete=False,physics_pass=False,gate_effect='NONE',
                review_status='DEFERRED',Rule9_cleared=False,working_digits=160,sympy=s.__version__,mpmath=mp.__version__,
                validation='PASS' if ok else 'FAIL')


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    result=calculate();data=ENC(result)
    if a.replay:
        if (a.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);f=a.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','validation','actual_nonlinear_cusp_projection_computed','G1_complete','physics_pass')}))
    raise SystemExit(0 if result['validation']=='PASS' else 2)


if __name__=='__main__':main()
