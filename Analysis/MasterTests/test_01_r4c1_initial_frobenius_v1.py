"""Registered initial Frobenius test; no all-formulation exclusion."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
PARENT='Analysis/MasterTests/outputs/r4c1_constrained_principal_v1_attempt_01/summary.json'
PSHA='652ae6656487c2cee1fbbc1a8e353f7681ccd83e993294e3e1ea11f178888824'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_FROBENIUS_INITIAL_V1_CONTRACT_2026-10-28.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()


def calculate():
    mp.mp.dps=110;mp.iv.dps=80;iv=mp.iv
    file=ROOT/PARENT
    if SHA(file.read_bytes())!=PSHA:raise ValueError('parent drift')
    pins=dict(json.loads(file.read_bytes())['source_sha256']);pins[PARENT]=PSHA
    for path in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix()):pins[path]=SHA((ROOT/path).read_bytes())
    def verify():
        for path,want in pins.items():
            f=ROOT/path
            if SHA(f.read_bytes())!=want or Path(str(f)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();checks=[]
    def zero(name,expr):
        val=s.factor(s.cancel(expr));checks.append(dict(name=name,passed=bool(val==0),remainder=str(val)))
    w,wp,Sy,ty=s.symbols('w wp Sy ty',real=True)
    gamma=s.sqrt(1+w*w);alpha_t=-gamma+w*Sy;alpha_y=w
    alpha_t_z=s.diff(alpha_t,w)*wp+s.diff(alpha_t,Sy)*ty
    # alpha_z=0 and alpha_z,t=hdot_zy*w+Vz_dot=0 in the registered jets.
    frob=-alpha_t*wp+alpha_y*alpha_t_z
    zero('arbitrary_shift_value_cancels',frob-(wp/gamma+w*w*ty))
    den=1-(2*s.Rational(-1,30)*w*w-2*s.Rational(1,120)*(1+w*w)*w*w)
    oldty=-2*s.Rational(-1,30)*w*w*wp/(gamma*den)
    closed=5*wp*(w**4+w*w+12)/(gamma*(w**4+5*w*w+60))
    zero('original_B1_shift_derivative',oldty-4*w*w*wp/(gamma*(w**4+5*w*w+60)))
    zero('full_initial_Frobenius_coefficient',frob.subs(ty,oldty)-closed)
    for sign in (-1,1):zero('exact_node_orientation_'+str(sign),closed.subs({w:0,wp:s.Rational(sign*2,25)})-s.Rational(sign*2,25))
    # On |w|<=e/2, cosine-profile slopes obey |wp|>=sqrt(3)*e*k/2.
    e=iv.mpf(1)/500;k=iv.mpf(40)
    lower=iv.sqrt(iv.mpf(3))*e*k/(2*iv.sqrt(1+(e/2)**2))
    comparison=iv.mpf(69281)/1000000
    checks.append(dict(name='positive_both_node_neighbourhood_lower_bound',passed=bool(lower.a>comparison.b),value=str(lower),criterion='>0.069281'))
    verify()
    return dict(result_id='R4C1-INITIAL-FROBENIUS-V1',source_sha256=pins,checks=checks,
                passed=sum(c['passed'] for c in checks),total=len(checks),
                formulas=dict(alpha='(-gamma+w*S_y)dt+w dy on registered h=I,N=1,V=(0,w,0)',
                              wedge_tyz=str(closed),node_values=['-2/25','2/25'],
                              near_node_lower_bound=str(lower),domain='|w|<=1/1000, both initial node orientations'),
                n_orthogonal_foliation_through_registered_node_jets=False,
                other_formulations_or_prepared_solutions_excluded=False,
                G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
                sympy=s.__version__,mpmath=mp.__version__)


def main():
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=parser.parse_args();r=calculate();data=ENC(r)
    if a.replay:
        if (a.replay/'summary.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);p=a.output/'summary.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  summary.json\n',encoding='ascii')
    print(json.dumps({k:r[k] for k in ('passed','total','n_orthogonal_foliation_through_registered_node_jets')}))
    raise SystemExit(0 if r['passed']==r['total'] else 2)


if __name__=='__main__':main()
