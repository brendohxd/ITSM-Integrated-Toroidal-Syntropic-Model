"""Independent exact arithmetic and geometric checks for the rho remainder."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
RECEIPT='Analysis/MasterTests/outputs/rtau_physical_density_remainder_v2_20261114/receipt.json'


def exact_mpf(v):
    sign,man,exp,bc=v
    assert man>=0 and (man.bit_length()==bc or man==bc==0)
    return (-1 if sign else 1)*Fraction(man)*(Fraction(2)**exp)


def calculate():
    p=ROOT/RECEIPT
    raw=p.read_bytes()
    d=json.loads(raw)
    rows=d['contributions_binary']
    total=d['bounds_binary']['initial_remainder_per_input']
    certificates=[]
    for i in range(9):
        exact_sum=sum((exact_mpf(v[i][1]) for v in rows.values()),Fraction(0))
        certificates.append(exact_sum<=exact_mpf(total[i][1])<=d['integer_uniform_certificate'])
    gamma,pn,s,w,k=sp.symbols('gamma p s w k')
    aa=pn+w*s/(gamma+1)
    rest_norm=(gamma**2-1)*aa**2+2*w*s*aa+k*s**2
    invariant=(gamma**2-1)*pn**2+2*gamma*w*pn*s+(k+w**2)*s**2
    # These identities justify differentiation via gamma,w,k even for
    # generic metric and frame variations, rather than a conformal shortcut.
    geometry=sp.factor(rest_norm-invariant)==0
    beta,L,Z=sp.symbols('beta L Z')
    geometric_rate=-2*L*Z-sp.Symbol('laplacian_rate')
    old_rate=2*L*Z-sp.Symbol('laplacian_rate')
    defect=sp.expand(old_rate-geometric_rate)
    # Independent finite-dimensional Legendre differential for clock rate.
    mu,N,fp,fpp,fps,vol,fi,xi,dq,dchi=sp.symbols('mu N fp fpp fps vol fi xi dq dchi',nonzero=True)
    delta_pi=mu*(fpp*sp.Symbol('delta_p')+fps*dchi+(fi+fp*vol)*dq)
    solved=sp.solve(sp.Eq(delta_pi,xi),sp.Symbol('delta_p'))[0]
    kclock=-N*(fi+fp*vol)/fpp-beta*N*pn
    target=N*xi/(mu*fpp)-N*fps*dchi/fpp+kclock*dq
    derived=N*solved-beta*N*pn*dq
    checks=dict(exact_rational_upper_sums=all(certificates),
                invariant_force_geometry=geometry,
                negative_scale_rate_defect=defect==4*L*Z and defect!=0,
                independent_legendre_clock_row=sp.expand(derived-target)==0,
                nine_inputs_and_eight_contributions=len(total)==9 and len(rows)==8,
                holds_retained=d['physics_pass'] is False and d['gate_effect']=='NONE'
                    and d['coupled_evolution']=='OPEN')
    assert all(checks.values()),checks
    assert p.read_bytes()==raw
    return dict(kind='RTAU_PHYSICAL_DENSITY_REMAINDER_INDEPENDENT_AUDIT_V1',
                receipt=RECEIPT,receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=v) for k,v in checks.items()],
                physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path)
    g.add_argument('--replay',type=Path)
    a=p.parse_args()
    raw=(json.dumps(calculate(),indent=2)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw
        print('Byte-identical independent-audit replay')
    else:
        assert a.output.parent.is_dir()
        with a.output.open('xb') as f:f.write(raw)
        print('Independent exact audit passed')


if __name__=='__main__':main()
