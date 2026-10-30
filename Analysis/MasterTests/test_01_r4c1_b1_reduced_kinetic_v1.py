"""Full instantaneous quadratic reduction on the old, admitted homogeneous B1 control.

Not admission of vortical data, an evolving stability result, or a physical cutoff.
"""
from __future__ import annotations
import argparse, ast, hashlib, importlib.util, json
from pathlib import Path
from types import SimpleNamespace
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_B1_REDUCED_KINETIC_V1_CONTRACT_2026-10-29.md'
BODY='Analysis/MasterTests/test_01_r4c1_nodal_momentum_tangency_v3.py'
BACKEND='Analysis/MasterTests/r4c1_full_weak_action_v1.py'
BG='Analysis/MasterTests/test_01_r4c1_interacting_background.py'
FIXED={
 BODY:'b887c7a52102b7abb43a2875cb6e01607ecb46d39a95f4abb4cefab9795a73c0',
 BACKEND:'330f25196806450238a71459873a3353036fac4ef15cab53da665ecbaa501105',
 BG:'1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f',
 'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md':'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
 'Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md':'82708666dfce4ef214b614bc7da31b294d7569539b97292aaa9a79e906e6266f',
}
SLOTS=(0,1,3,6,7,8,9,10,11,12,13)
NAMES=('gamma_xx','gamma_xy','gamma_yy','v_x','v_y','v_z','du','dv','dr','dpsi','dZ')
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda v:(json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))


class Jet:
    """Exact second-order forward differentiation; h entries are Hessians."""
    def __init__(self,c,g=None,h=None):
        self.c=s.sympify(c);self.g=g or {};self.h=h or {}
    @staticmethod
    def var(i):return Jet(0,{i:s.Integer(1)})
    @staticmethod
    def cast(v):return v if isinstance(v,Jet) else Jet(v)
    def __add__(self,z):
        z=self.cast(z)
        def add(a,b):
            out=a.copy()
            for k,v in b.items():out[k]=s.expand(out.get(k,0)+v)
            return {k:v for k,v in out.items() if v!=0}
        return Jet(self.c+z.c,add(self.g,z.g),add(self.h,z.h))
    __radd__=__add__
    def __neg__(self):return Jet(-self.c,{k:-v for k,v in self.g.items()},{k:-v for k,v in self.h.items()})
    def __sub__(self,z):return self+(-self.cast(z))
    def __rsub__(self,z):return self.cast(z)+(-self)
    def __mul__(self,z):
        z=self.cast(z);g={};h={}
        for a,b,c in ((self.g,z.g,g),(self.h,z.h,h)):
            for k in a.keys()|b.keys():
                v=s.expand(a.get(k,0)*z.c+b.get(k,0)*self.c)
                if v!=0:c[k]=v
        for i,a in self.g.items():
            for j,b in z.g.items():
                k=(min(i,j),max(i,j));h[k]=s.expand(h.get(k,0)+(2 if i==j else 1)*a*b)
        return Jet(self.c*z.c,g,{k:v for k,v in h.items() if v!=0})
    __rmul__=__mul__
    def unary(self,value,first,second):
        h={k:s.expand(first*v) for k,v in self.h.items()}
        keys=sorted(self.g)
        for ai,i in enumerate(keys):
            for j in keys[ai:]:
                key=(i,j);h[key]=s.expand(h.get(key,0)+second*self.g[i]*self.g[j])
        return Jet(value,{k:s.expand(first*v) for k,v in self.g.items()},
                   {k:v for k,v in h.items() if v!=0})
    def __pow__(self,p):
        p=s.Rational(str(p))
        if p==0:return Jet(1)
        return self.unary(self.c**p,p*self.c**(p-1),p*(p-1)*self.c**(p-2))
    def __truediv__(self,z):return self*self.cast(z)**(-1)
    def __rtruediv__(self,z):return self.cast(z)*self**(-1)


def jexp(x):
    if not isinstance(x,Jet):return s.exp(x)
    value=s.exp(x.c);return x.unary(value,value,value)


def jsqrt(x):return x**s.Rational(1,2) if isinstance(x,Jet) else s.sqrt(x)


def original_body(quadratic):
    tree=ast.parse((ROOT/BODY).read_text(encoding='utf-8-sig'))
    names={'dot','mv','tr','trans','mm','det3','inv3','tensor','geometry','body'}
    tree.body=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names]
    fn=next(node for node in tree.body if node.name=='body')
    if quadratic:
        force=next(node for node in fn.body if isinstance(node,ast.Assign)
                   and any(isinstance(v,ast.Name) and v.id=='force' for v in node.targets))
        expected=ast.parse("par['K_Q']*dot(n,gp)**2/2-par['A']*Y**mp.mpf('1.5')",mode='eval').body
        assert ast.dump(force.value)==ast.dump(expected)
        force.value=force.value.left  # Only C2 Taylor coefficient, not an adopted A=0 action.
    ast.fix_missing_locations(tree)
    glob=dict(mp=mp,sqrt=jsqrt if quadratic else mp.sqrt,exp=jexp if quadratic else mp.exp)
    exec(compile(tree,'<pinned-original-body-C2>' if quadratic else '<pinned-original-body>', 'exec'),glob)
    return SimpleNamespace(**glob)


def parameters():
    tree=ast.parse((ROOT/BG).read_text(encoding='utf-8-sig'))
    node=next(v.value for v in tree.body if isinstance(v,ast.Assign)
              and any(isinstance(z,ast.Name) and z.id=='PARAMS' for z in v.targets))
    old={v.arg:s.nsimplify(s.sympify(ast.unparse(v.value)),rational=True) for v in node.keywords}
    return dict(MP2=old['MP2'],MU2=old['MU2'],c1=old['c1'],c2=old['c2'],c3=old['c3'],c4=old['c4'],
                K_Q=old['K'],A=old['A'],b=old['b'],zeta=old['zeta'],beta=old['beta'],
                m2=old['m2'],lambda4=old['l4'],lambda6=old['l6'],Lambda=old['cutoff'],
                mr2=old['mr2'],lambda_r=old['lr'],g_r=old['gr'],rho_Lambda=old['vacuum'])


def state(x,H,par,exp):
    """Physical amplitudes at a=1; their moving-basis derivatives are retained."""
    q=list(map(s.Rational,(1,0,0,1,0,1,0,0,0,1,0,1,0,0,0)))+[s.Rational(1,5)]
    v=[0]*16;d=[0]*16
    for slot in (0,3,5):v[slot]=2*H
    v[10]=1;v[11]=s.Rational(1,4);v[12]=s.Rational(1,5);v[14]=1
    for i,slot in enumerate(SLOTS):
        q[slot]+=x[i];v[slot]+=x[11+i];d[slot]=x[22+i]
        if i<3:v[slot]+=2*H*x[i]
        elif i<6:v[slot]-=H*x[i]
    NN=exp(-par['beta']*x[9])
    return q+v+d+list(x[33:36])+list(x[36:39])+[NN,-par['beta']*NN*x[31]]


def calculate():
    mp.mp.dps=100;checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for q in entries if (v:=clean(q))!=0];check(name,not bad,bad)
    pins=dict(FIXED)
    for name in (CONTRACT,SELF):pins[name]=SHA((ROOT/name).read_bytes())
    snapshots={}
    for name,want in pins.items():
        path=ROOT/name
        assert SHA(path.read_bytes())==want,name
        sidecar=Path(str(path)+'.sha256');assert sidecar.read_text().split()[0].lower()==want,name
        for item in (path,sidecar):snapshots[item.relative_to(ROOT).as_posix()]=(SHA(item.read_bytes()),item.stat().st_mtime_ns)
    par=parameters();check('old_B1_unscaled_portal',par['g_r']==s.Rational(3,7))
    spec=importlib.util.spec_from_file_location('B1_original_weak',ROOT/BACKEND)
    backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
    H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    exact=backend.WeakAction(original_body(True),par)
    jets=[Jet.var(i) for i in range(39)]
    result=exact.density(state(jets,H,par,jexp))[0]
    local=s.zeros(39)
    for (i,j),v in result.h.items():local[i,j]=local[j,i]=clean(v)
    check('exact_quadratic_no_Float',not bool(local.atoms(s.Float)))
    zero('local_Hessian_symmetric',local-local.T)
    rho=s.Rational(1,5);K0=1+s.Rational(1,16)+3*s.Rational(1,25)
    potential=s.Rational(1,2)+s.Rational(1,24)+s.Rational(1,480)+1+s.Rational(1,28)+s.Rational(3,28)
    E=K0/2+potential+rho
    zero('registered_B1_energy',E-s.Rational(3469,1400))
    zero('unfixed_background_density',result.c-(-s.Rational(33,10)*H**2+K0/2-potential))
    radius=s.Symbol('radius',positive=True)
    zero('norm_cubed_radial_C2_limit',s.limit(s.diff(radius**3,radius,2),radius,0))
    zero('norm_cubed_transverse_C2_limit',s.limit(s.diff(radius**3,radius)/radius,radius,0))
    NN,tt,pp,eps=s.symbols('N tau_dot psi epsilon',positive=True)
    Ldust=eps*(s.exp(2*par['beta']*pp)*tt**2/NN-NN*s.exp(4*par['beta']*pp))/2
    zero('positive_dust_constraint_solves_lapse',s.diff(Ldust,eps).subs(NN,tt*s.exp(-par['beta']*pp)))
    check('density_recovered_by_lapse_equation',s.diff(Ldust,eps,NN).subs({NN:1,tt:1,pp:0})==-1)
    T=s.zeros(39,25)
    for i in range(11):T[i,i]=1;T[11+i,11+i]=1;T[22+i,i]=s.I*k
    for i in range(3):T[33+i,22+i]=1;T[36+i,22+i]=s.I*k
    full=(T.conjugate().T*local*T).applyfunc(clean)
    zero('full_Fourier_Hermitian',full-full.conjugate().T)
    zero('Z_velocity_row_zero',full[21,:])
    keep=list(range(10))+list(range(11,21));elim=[10,22,23,24]
    A=full.extract(keep,keep);B=full.extract(keep,elim);D=full.extract(elim,elim)
    detD=clean(D.det());check('nonzero_mode_constraint_block_regular',detD!=0,str(detD))
    zero('constraint_block_diagonal',D-s.diag(*D.diagonal()))
    inverse=s.diag(*[1/z for z in D.diagonal()])
    solve=(-inverse*B.conjugate().T).applyfunc(clean)
    red=(A+B*solve).applyfunc(clean)
    zero('all_eliminated_equations_solved',D*solve+B.conjugate().T)
    zero('reduced_Hermitian',red-red.conjugate().T)
    M=red[10:20,10:20];Bv=red[10:20,:10];Q=red[:10,:10]
    zero('kinetic_independent_H',M.diff(H));zero('kinetic_independent_nonzero_k',M.diff(k))
    LL,DD=M.LDLdecomposition(hermitian=False)
    zero('exact_LDL',M-LL*DD*LL.T)
    signature=[s.sign(z) for z in DD.diagonal()]
    check('kinetic_pivots_all_decided',all(z in (-1,0,1) for z in signature),[str(z) for z in DD.diagonal()])
    R=s.diag(*[s.sqrt(abs(z)) for z in DD.diagonal()])*LL.T
    zero('canonical_kinetic_congruence',R.T*s.diag(*signature)*R-M)
    Omega=(Bv-Bv.conjugate().T).row_join(M).col_join((-M).row_join(s.zeros(10)))
    zero('instantaneous_symplectic_skew_Hermitian',Omega+Omega.conjugate().T)
    Cmap=s.eye(20);Cmap[10:20,:10]=Bv;Cmap[10:20,10:20]=M
    J=s.zeros(20);J[:10,10:20]=s.eye(10);J[10:20,:10]=-s.eye(10)
    zero('canonical_pullback_including_magnetic_term',Omega-Cmap.conjugate().T*J*Cmap)
    check('symplectic_non_degenerate',clean(M.det())!=0,str(clean(M.det())**2))
    # Verify elimination by full stationary quadratic substitution, retaining odd-k terms.
    pull=s.zeros(25,20)
    for i,j in enumerate(keep):pull[j,i]=1
    for i,j in enumerate(elim):pull[j,:]=solve[i,:]
    zero('full_quadratic_stationary_pullback',pull.conjugate().T*full*pull-red)
    check('odd_spatial_mix_retained',any(s.im(v)!=0 for v in Bv),sum(s.im(v)!=0 for v in Bv))
    print('EXACT_FULL_QUADRATIC_AND_CONSTRAINT_REDUCTION',flush=True)
    H0=s.sqrt(s.Rational(3469,4620));h0=mp.sqrt(mp.mpf(3469)/4620)
    physical_par={n:mp.mpf(str(v.p))/int(v.q) for n,v in par.items()}
    physical=backend.WeakAction(original_body(False),physical_par)
    # Original physical density, real perturbations: cubic is retained, not differentiated at a cusp.
    zero39=[mp.mpf(0)]*39
    f0=physical.density(state(zero39,h0,physical_par,mp.exp))[0]
    controls=[]
    for seed in (1,2,3):
        direction=[s.Rational(((j+1)*(seed+2))%11-5,13+seed) for j in range(39)]
        ds=s.Matrix(direction);expected=clean((ds.T*local*ds)[0]).subs(H,H0).evalf(95)
        expected=mp.mpf(str(expected));direction=[mp.mpf(str(z.p))/int(z.q) for z in direction]
        row=[]
        for hs in ('1e-12','1e-16'):
            hh=mp.mpf(hs)
            fp=physical.density(state([hh*z for z in direction],h0,physical_par,mp.exp))[0]
            fm=physical.density(state([-hh*z for z in direction],h0,physical_par,mp.exp))[0]
            observed=(fp+fm-2*f0)/hh**2;error=abs(observed-expected)/(1+abs(expected))
            check(f'original_density_C2_control_{seed}_{hs}',error<50*hh,mp.nstr(error,65))
            row.append(error)
        check(f'physical_cubic_remainder_converges_{seed}',row[1]<row[0]/1000)
        controls.append(dict(seed=seed,normalized_errors=[mp.nstr(v,65) for v in row]))
    # Separate real-quadrature assembly, explicitly averaging both sine and cosine.
    for kval in (1,7,40):
        qv=s.Matrix([s.Rational((j*7+3)%13-6,17) for j in range(25)])
        uv=s.Matrix([s.Rational((j*5+1)%11-5,19) for j in range(25)])
        real=(T.subs(k,kval)*qv).applyfunc(s.re);imag=(T.subs(k,kval)*qv).applyfunc(s.im)
        # For complex amplitude qv+i uv, real and imaginary local jets mix independently.
        tj=T.subs(k,kval)*(qv+s.I*uv);rr=tj.applyfunc(s.re);ii=tj.applyfunc(s.im)
        herm=(qv-s.I*uv).T*full.subs(k,kval)*(qv+s.I*uv)
        zero(f'real_two_quadrature_assembly_k{kval}',(rr.T*local*rr+ii.T*local*ii-herm)[0])
        numerical_M=M.subs(H,H0)
        check(f'positive_kinetic_control_k{kval}',min(float(v) for v in DD.diagonal())>0)
    for name,(want,mtime) in snapshots.items():
        path=ROOT/name;assert SHA(path.read_bytes())==want and path.stat().st_mtime_ns==mtime,name
    check('all_input_bytes_and_mtimes_unchanged',True,len(snapshots))
    encode_matrix=lambda mat:[[str(clean(v)) for v in row] for row in mat.tolist()]
    formulas=dict(fields=list(NAMES[:10]),parameters={n:str(v) for n,v in par.items()},
                  H_initial=str(H0),local_order=['q11','qdot11','q_z11','S3','S_z3'],
                  local_Hessian=encode_matrix(local),constraint_order=['dZ','Sx','Sy','Sz'],
                  constraint_block=encode_matrix(D),constraint_determinant=str(detD),
                  constraint_solution=encode_matrix(solve),reduced_kinetic=encode_matrix(M),
                  reduced_velocity_field=encode_matrix(Bv),reduced_field_field=encode_matrix(Q),
                  kinetic_L=encode_matrix(LL),kinetic_D=encode_matrix(DD),normalization=encode_matrix(R),
                  momentum='pi=M*qdot+B*q; B=reduced_velocity_field',
                  Hamiltonian='(pi-B*q)^dagger*M^(-1)*(pi-B*q)/2-q^dagger*Q*q/2',
                  two_form='[[B-B^dagger,M],[-M,0]]; frozen event, realified Fourier pair')
    return dict(kind='R4C1_B1_REDUCED_KINETIC_V1',passed=sum(v['passed'] for v in checks),total=len(checks),
                checks=checks,source_sha256=pins,formulas=formulas,independent_controls=controls,
                kinetic_inertia=dict(positive=signature.count(1),negative=signature.count(-1),zero=signature.count(0)),
                scope='Old homogeneous B1 at t=0, nonzero planar Fourier modes; full instantaneous quadratic reduction only',
                physical_window_demonstrated=False,nodal_G1_admitted=False,physics_pass=False,gate_effect='NONE',
                review='DEFERRED',G1='INCOMPLETE',G2='INCOMPLETE',G3='INCOMPLETE',G4='INCOMPLETE',
                G5='INCOMPLETE',G6='INCOMPLETE',MAT001='BLOCKED',K_Q='NOT_DERIVED',V='NOT_COMPUTED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out');group.add_argument('--replay');args=parser.parse_args()
    if args.out and (ROOT/args.out).exists():raise FileExistsError(args.out)
    result=calculate();data=ENC(result)
    if args.replay:
        target=ROOT/args.replay;assert target.read_bytes()==data,'immutable replay mismatch'
        assert Path(str(target)+'.sha256').read_text().split()[0]==SHA(data)
        print('IMMUTABLE_REPLAY_EXACT',flush=True)
    else:
        out=ROOT/args.out;out.mkdir(parents=True,exist_ok=False);file=out/'summary.json'
        file.write_bytes(data);Path(str(file)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','kinetic_inertia','physical_window_demonstrated','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
