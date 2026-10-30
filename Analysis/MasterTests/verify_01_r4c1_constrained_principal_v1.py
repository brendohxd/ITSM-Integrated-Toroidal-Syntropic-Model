"""Independent exact reconstruction of the frozen constrained-pencil receipt."""
import argparse,hashlib,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/outputs/r4c1_constrained_principal_v1_attempt_01/summary.json'
EXPECTED='652ae6656487c2cee1fbbc1a8e353f7681ccd83e993294e3e1ea11f178888824'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda d:(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()


def calculate():
    data=(ROOT/SOURCE).read_bytes()
    if SHA(data)!=EXPECTED:raise ValueError('source receipt drift')
    original=json.loads(data);pins=dict(original['source_sha256']);pins[SOURCE]=EXPECTED
    self=Path(__file__).resolve().relative_to(ROOT).as_posix();pins[self]=SHA((ROOT/self).read_bytes())
    def verify():
        for path,want in pins.items():
            file=ROOT/path
            if SHA(file.read_bytes())!=want or Path(str(file)+'.sha256').read_text().split()[0].lower()!=want:raise ValueError('source drift '+path)
    verify();w=s.Symbol('w',real=True,nonzero=True);Z=s.Symbol('Z_background',real=True);c=s.Symbol('c',real=True)
    P=s.Matrix([[s.sympify(x,locals={'w':w,'Z_background':Z,'c':c}) for x in row] for row in original['formulas']['reduced_pencil']])
    checks=[]
    def zero(name,matrix):
        rows=list(matrix) if isinstance(matrix,s.MatrixBase) else [matrix]
        bad=[str(z) for x in rows if (z:=s.factor(s.cancel(x)))!=0]
        checks.append(dict(name=name,passed=not bad,value=bad))
    parity=s.diag(1,-1,1,1,-1,1,1,1,1,1,1)
    zero('complete_y_reflection_conjugation',P.subs(w,-w)-parity*P*parity)
    M=P.diff(c,2)/2;B=M[:9,:9]
    detB=s.factor(B.det(method='domain-ge'))
    zero('registered_exact_mass_matches',detB.subs(w,s.Rational(1,1000))-s.sympify(original['formulas']['registered_remaining_mass_det']))
    zero('opposite_tilt_exact_mass_matches',detB.subs(w,-s.Rational(1,1000))-s.sympify(original['formulas']['registered_remaining_mass_det']))
    ez=s.zeros(11,1);ez[10]=1
    for sign in (-1,1):zero('reconstructed_full_principal_eigenvector_'+str(sign),P.subs(c,sign*s.I/w)*ez)
    verify()
    return dict(result_id='R4C1-CONSTRAINED-PRINCIPAL-INDEPENDENT-V1',source_sha256=pins,
                checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),general_remaining_mass_determinant=str(detB),
                interpretation='Exact receipt reconstruction and tilt parity; same-author verification, not peer review',
                G1_complete=False,physics_pass=False,gate_effect='NONE',review_status='DEFERRED',sympy=s.__version__)


def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path);a=p.parse_args();r=calculate();b=ENC(r)
    if a.replay:
        if (a.replay/'independent.json').read_bytes()!=b:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        a.output.mkdir(parents=True,exist_ok=False);f=a.output/'independent.json';f.write_bytes(b)
        Path(str(f)+'.sha256').write_text(SHA(b)+'  independent.json\n',encoding='ascii')
    print(json.dumps({k:r[k] for k in ('passed','total','general_remaining_mass_determinant')}))
    raise SystemExit(0 if r['passed']==r['total'] else 2)


if __name__=='__main__':main()
