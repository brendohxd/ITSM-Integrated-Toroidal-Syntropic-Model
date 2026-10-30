"""Full initial Euler descriptor with correctly converted dust clock/density jets."""
import argparse,hashlib,json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_unreduced_jet_v1_attempt_01/summary.json'
PSHA='ddc97689a189fb07c5fffe8e4a4052694f6d7bf9d67a35e26ec95c6a3b5fbde4'
POINTS='Analysis/MasterTests/outputs/r4c1_quartic_charge_tangency_v2_attempt_01/summary.json'
PLANAR='Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/formulas.json'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_CLOCK_DENSITY_SOURCE_V1_CONTRACT_2026-10-29.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
READ=lambda p:json.loads((ROOT/p).read_bytes())
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
show=lambda x:mp.nstr(x,65)


def calculate():
    mp.mp.dps=110;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def close(name,error):check(name,error<mp.mpf('1e-18'),show(error))
    def zero(name,z):check(name,s.factor(s.cancel(z))==0,str(s.factor(s.cancel(z))))
    assert SHA((ROOT/PARENT).read_bytes())==PSHA,'parent drift'
    parent=READ(PARENT);pins=dict(parent['source_sha256']);pins[PARENT]=PSHA
    for name,want in parent['file_sha256'].items():pins[(Path(PARENT).parent/name).as_posix()]=want
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:
                raise ValueError('source drift '+path)
    verify()
    C,N,V,eps,rho,td,beta=s.symbols('C N volume epsilon rho tau_dot beta',positive=True)
    p,rd,Hh,R,Rp,rz=s.symbols('p rho_dot H R Rprime rho_z',real=True)
    L=V*eps*(C*C*td*td/N-N*C**4)/2
    on=lambda expr:s.cancel(expr.subs(td,N*C).subs(eps,rho/C**4))
    zero('future_clock_root',s.diff(L,eps).subs(td,N*C))
    zero('physical_density_from_lapse',on(-s.diff(L,N)/V)-rho)
    zero('original_scalar_dust_force',on(beta*C*s.diff(L,C))+beta*N*V*rho)
    zero('original_clock_momentum',on(s.diff(L,td))-V*rho/C)
    zero('physical_density_multiplier_identity',(eps*C**4).subs(eps,rho/C**4)-rho)
    # Differentiate rho=epsilon*C^4 before setting C=1.
    erd=s.cancel((rd-4*beta*p*rho)/C**4)
    zero('multiplier_density_rate',C**4*erd+4*beta*p*rho-rd)
    psi,t=s.symbols('psi t',real=True)
    zero('future_clock_acceleration',s.diff(s.exp(beta*(psi+p*t)),t).subs({t:0,psi:0})-beta*p)
    zero('clock_current_physical_density_rate',
         (rd+3*Hh*rho-beta*p*rho)-(rd-(R*rz+(-3*Hh+Rp+beta*p)*rho))-R*rz-Rp*rho)
    eta=s.Symbol('eta');bexact=s.sympify(READ(PLANAR)['families']['new_B1_frame']['parameter_map']['beta'],locals={'eta':eta}).subs(eta,s.Rational(1,4))
    bn=mp.mpf(str(s.N(bexact,105)))
    originals={row['label']:row for row in READ(POINTS)['points']};results=[]
    for name in sorted(parent['file_sha256']):
        raw=READ((Path(PARENT).parent/name).as_posix());label=raw['label'];old=originals[label]['values']
        A=list(map(mp.mpf,raw['original_first_jet']));g=mp.matrix(list(map(mp.mpf,raw['gradient'])))
        K=mp.matrix([[mp.mpf(z) for z in rr] for rr in raw['full_Hessian']])
        inp=raw['original_spatial_auxiliary_inputs'];vd=list(map(mp.mpf,inp['mixed_physical']))
        dd=list(map(mp.mpf,inp['second_spatial_physical']));Sdd=list(map(mp.mpf,inp['shift_second_spatial']))
        acc=mp.matrix(list(map(mp.mpf,old['acc'])));rr=mp.mpf(old['rho']);rrt=mp.mpf(old['rho_dot']);rrz=mp.mpf(old['rho_z'])
        epst=rrt-4*bn*A[28]*rr;clockacc=bn*A[28]
        Dt=mp.matrix(A[16:32]+list(acc)+[clockacc,mp.mpf(0)]+vd+[mp.mpf(0)]*2+[mp.mpf(0)]*8)
        Dt[15]=epst
        Dz=mp.matrix(A[32:48]+vd+[mp.mpf(0)]*2+dd+[mp.mpf(0)]*2+A[51:54]+Sdd+[mp.mpf(0)]*2)
        Dz[15]=rrz
        assert len(Dt)==len(Dz)==56
        gt=K*Dt;gz=K*Dz
        E=mp.matrix([g[i]-gt[16+i]-gz[32+i] for i in range(16)])
        errors=[abs(E[i])/(1+abs(g[i])+abs(gt[16+i])+abs(gz[32+i])) for i in range(16)]
        lapse=g[54]-gz[55];shifts=[g[48+i]-gz[51+i] for i in range(3)]
        close(label+'_full_fourteen_initial_Euler',max(errors[:14]))
        close(label+'_clock_Euler',errors[14]);close(label+'_multiplier_Euler',errors[15])
        close(label+'_lapse_constraint',abs(lapse)/(1+abs(g[54])+abs(gz[55])))
        close(label+'_three_shift_constraints',max(abs(shifts[i])/(1+abs(g[48+i])+abs(gz[51+i])) for i in range(3)))
        mult_dt=(K[15,:]*Dt)[0]
        close(label+'_first_multiplier_tangency',abs(mult_dt)/(1+abs(clockacc)))
        volrate=sum(A[16+j] for j in (0,3,5))/2
        current=rrt+volrate*rr-bn*A[28]*rr-A[50]*rrz-A[53]*rr
        close(label+'_independent_clock_current',abs(E[14]+current)/(1+abs(E[14])+abs(current)))
        bad=mp.matrix(Dt);bad[15]=rrt;badclock=g[14]-(K*bad)[30]-gz[46]
        omission=abs(badclock-E[14])/(1+abs(badclock)+abs(E[14]))
        check(label+'_reject_multiplier_equals_physical_density_rate',omission>mp.mpf('1e-18'),show(omission))
        bad=mp.matrix(Dt);bad[30]=0
        omission=abs((K[15,:]*bad)[0])/(1+abs(clockacc))
        check(label+'_reject_missing_clock_acceleration',omission>mp.mpf('1e-18'),show(omission))
        Dt0=mp.matrix(Dt)
        for i in range(14):Dt0[16+i]=0
        gt0=K*Dt0;F=mp.matrix([g[i]-gt0[16+i]-gz[32+i] for i in range(16)])
        M=K[16:30,16:30];diff=F[:14,0]-M*acc-E[:14,0]
        close(label+'_complete_initial_descriptor_identity',max(abs(z) for z in diff)/(1+max(abs(z) for z in F)))
        results.append(dict(label=label,theta=raw['theta'],epsilon_equals_rho_only_on_initial_slice=True,
            rho=show(rr),physical_density_rate=show(rrt),multiplier_rate=show(epst),clock_acceleration=show(clockacc),
            complete_time_direction=[show(z) for z in Dt],complete_spatial_direction=[show(z) for z in Dz],
            fourteen_accelerations=[show(z) for z in acc],initial_descriptor_F16=[show(z) for z in F],
            actual_initial_Euler16=[show(z) for z in E],normalized_Euler16=[show(z) for z in errors],
            initial_lapse_residual=show(lapse),initial_shift_residuals=[show(z) for z in shifts],
            raw_point_source=(Path(PARENT).parent/name).as_posix()))
    verify()
    return dict(result_id='R4C1-CLOCK-DENSITY-SOURCE-V1',source_sha256=pins,checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),points=results,
                identities=dict(rho='epsilon*C^4',future_clock='tau_dot=C at N=1,tau_z=0',
                    clock_momentum='sqrt(h)*rho/C',initial_multiplier_rate='rho_dot-4*beta*p*rho',
                    initial_clock_acceleration='beta*p; original unit-lapse chart',
                    descriptor='E16=F16-M_physical*acc14; known clock and density derivatives retained'),
                working_digits=110,mpmath=mp.__version__,sympy=s.__version__,
                initial_unreduced_Euler_descriptor_exported=True,principal_frequency_source_exported=False,
                actual_nonlinear_cusp_projection_computed=False,exact_node_equations_verified=False,
                continuum_constraint_transport_certified=False,time_evolution=False,G1_complete=False,
                physics_pass=False,gate_effect='NONE',review_status='DEFERRED',Rule9_cleared=False)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args()
    r=calculate();data=ENC(r)
    if a.replay:
        if (a.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);f=a.output/'summary.json';f.write_bytes(data)
        Path(str(f)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:r[k] for k in ('passed','total','initial_unreduced_Euler_descriptor_exported','principal_frequency_source_exported','G1_complete','physics_pass')}))
    raise SystemExit(0 if r['passed']==r['total'] else 2)


if __name__=='__main__':main()
