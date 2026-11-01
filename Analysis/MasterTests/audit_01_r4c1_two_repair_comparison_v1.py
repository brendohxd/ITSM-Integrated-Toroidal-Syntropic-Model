"""Additional independent identities for the first two-repair comparison bundle."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/outputs/r4c1_two_repair_comparison_v2_attempt_01/summary.json'
EXPECTED='964c24a88923a3326902eb8f5b37fa23a0f3ab6ee8964c60406e52211ea52f91'
BACKEND='Analysis/MasterTests/r4c1_two_repair_actions_v2.py'
OLD='Analysis/MasterTests/outputs/r4c1_b1_alignment_domain_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
clean=lambda z:s.factor(s.cancel(z))

def calculate():
    assert SHA((ROOT/PARENT).read_bytes())==EXPECTED
    parent=json.loads((ROOT/PARENT).read_bytes());assert parent['passed']==parent['total']==70
    pins=dict(parent['source_sha256']);pins[PARENT]=EXPECTED;pins[SELF]=SHA((ROOT/SELF).read_bytes())
    snapshots={}
    for name,want in pins.items():
        f=ROOT/name;sc=Path(str(f)+'.sha256')
        assert SHA(f.read_bytes())==want and sc.read_text().split()[0].lower()==want,name
        for z in (f,sc):snapshots[z.relative_to(ROOT).as_posix()]=(SHA(z.read_bytes()),z.stat().st_mtime_ns)
    checks=[]
    def check(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    def zero(name,z):
        entries=list(z) if isinstance(z,s.MatrixBase) else [z]
        bad=[str(v) for a in entries if (v:=s.expand(clean(a)))!=0]
        check(name,not bad,bad)
    spec=importlib.util.spec_from_file_location('two_repair_audit_backend',ROOT/BACKEND)
    backend=importlib.util.module_from_spec(spec);spec.loader.exec_module(backend)
    old=backend.load('two_repair_audit_exact',backend.QUADRATIC);par=old.parameters()
    w=s.Symbol('w',real=True);H=s.Symbol('H',real=True);k=s.Symbol('k',real=True,nonzero=True)
    parse=lambda rows:s.Matrix([[s.sympify(z,locals={'w':w,'H':H,'k':k}) for z in row] for row in rows])
    oldparent=json.loads((ROOT/OLD).read_bytes())
    DR=parse(parent['candidates']['R-tau']['shift_block'])
    DF=parse(parent['candidates']['F-tau']['shift_block'])
    zero('actual_R_shift_block_matches_pinned_interval_proof',DR-parse(oldparent['formulas']['shift_block']))
    zero('R_shift_determinant_exact',DR.det()+(1+w*w)*(w**4+5*w*w+15)/900)
    zero('F_shift_determinant_exact',DF.det()+s.Rational(1,60))
    check('nonzero_k_shift_constraints_regular',
          int(oldparent['bounds']['shift_determinant'][1])<0)
    mf=parse(parent['candidates']['F-tau']['reduced_kinetic'])
    zero('F_kinetic_determinant',mf.det()-s.Rational(99,32))
    check('F_minimum_kinetic_eigenvalue_exact',min(mf.eigenvals())==s.Rational(1,4))
    # Full, ungauged-normal frame invariants in the (-+++) convention.
    K11,K12,K13,K22,K23,K33=s.symbols('K11 K12 K13 K22 K23 K33',real=True)
    av=s.Matrix(s.symbols('a1:4',real=True))
    K=s.Matrix([[K11,K12,K13],[K12,K22,K23],[K13,K23,K33]])
    B=s.zeros(4);B[0,1:4]=av.T;B[1:4,1:4]=K
    g=s.diag(-1,1,1,1)
    I1=s.trace(g*B*g*B.T);I2=s.trace(B)**2;I3=s.trace(B*B)
    n=s.Matrix([1,0,0,0]);acc=B.T*n;I4=(acc.T*g*acc)[0]
    zero('hypersurface_normal_I1',I1-s.trace(K*K)+(av.T*av)[0])
    zero('hypersurface_normal_I2',I2-s.trace(K)**2)
    zero('hypersurface_normal_I3',I3-s.trace(K*K))
    zero('hypersurface_normal_I4',I4-(av.T*av)[0])
    c1,c2,c3,c4,MU2=s.symbols('c1 c2 c3 c4 MU2',real=True)
    Lu=-MU2*(c1*I1+c2*I2+c3*I3-c4*I4)/2
    adm=-MU2*((c1+c3)*s.trace(K*K)+c2*s.trace(K)**2-(c1+c4)*(av.T*av)[0])/2
    zero('F_frame_action_ADM_identity',Lu-adm)
    # Lapse coefficient of the dust multiplier is not a vacuum constraint.
    N,C,vol,taudot=s.symbols('N C vol taudot',positive=True);eps=s.Symbol('eps',real=True)
    Ldust=vol*eps*(C*C*taudot**2/N-N*C**4)/2
    coef=s.diff(Ldust,N,eps).subs(taudot,N*C)
    zero('dust_lapse_density_coefficient',coef+vol*C**4)
    check('dust_density_locally_reconstructible',(-coef).is_positive)
    # Recompute R-tau homogeneous Routh energy identity, keeping every metric/frame velocity.
    action=backend.ClockGaugeAction('R-tau',par);phase=1/(1-w*w/13);p=s.Rational(1,5)
    q=list(map(s.Rational,[1,0,0,1,0,1,0,0,0,1,0,1,0,0,0]))+[s.Rational(1,5)];q[7]=w
    vel=[s.Integer(0)]*16;dz=vel.copy()
    for j in (0,3,5):vel[j]=2*H
    vel[7]=-H*w;vel[10]=phase;vel[11]=s.Rational(1,4);vel[12]=p;vel[14]=1
    x=[old.Jet.var(i) for i in range(18)]
    vv=[z+(x[i] if i<13 else 0) for i,z in enumerate(vel)];vv[14]+=x[14]
    hom=action.density(q+vv+dz+x[15:18]+[0,0,0]+[1+x[13],0])[0]
    moments=[hom.g.get(i,0)-(3*par['A']*p*p*s.Abs(w)**3 if i==12 else 0) for i in range(13)]
    Lrouth=hom.c-par['A']*p**3*s.Abs(w)**3-s.Rational(1,5)
    energy=clean(sum(vel[i]*moments[i] for i in range(13))-Lrouth)
    lapse=clean(hom.g.get(13,0)+2*par['A']*p**3*s.Abs(w)**3)
    zero('R_full_Routh_energy_equals_minus_unfixed_lapse',energy+lapse)
    zero('R_homogeneous_shift_values_unforced',s.Matrix([hom.g.get(i,0) for i in range(15,18)]))
    zero('R_homogeneous_dust_charge',hom.g.get(14,0)-s.Rational(1,5))
    zero('R_homogeneous_scalar_charge',hom.g.get(10,0)-1)
    for path,(digest,mtime) in snapshots.items():
        f=ROOT/path;assert SHA(f.read_bytes())==digest and f.stat().st_mtime_ns==mtime,path
    check('original_bytes_and_mtimes_preserved',True,len(snapshots))
    return dict(kind='R4C1_TWO_REPAIR_ADDITIONAL_IDENTITIES_V1',passed=sum(z['passed'] for z in checks),
        total=len(checks),checks=checks,source_sha256=pins,
        formulas=dict(R_routh_energy=str(energy),R_lapse=str(lapse),
            R_lapse_preservation='Autonomous homogeneous Routh equations conserve this energy on their nonsingular local solution; spatial momentum constraints vanish by homogeneity',
            background_limit='Local admission is not uniform lifetime, nonlinear perturbation stability or a physical window'),
        physics_pass=False,gate_effect='NONE',review='DEFERRED',Rule9_cleared=False,adopted_action=False)

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--output-dir',type=Path);g.add_argument('--replay',type=Path)
    a=ap.parse_args();r=calculate();data=ENC(r)
    if a.replay:
        assert a.replay.read_bytes()==data;print('READ_ONLY_REPLAY_EXACT',SHA(data))
    else:
        a.output_dir.mkdir(parents=True,exist_ok=False);p=a.output_dir/'summary.json'
        p.write_bytes(data);Path(str(p)+'.sha256').write_text(SHA(data)+'\n',encoding='ascii')
        print(json.dumps(dict(passed=r['passed'],total=r['total'],physics_pass=False,receipt=str(p))))
    return 0 if r['passed']==r['total'] else 1

if __name__=='__main__':raise SystemExit(main())

