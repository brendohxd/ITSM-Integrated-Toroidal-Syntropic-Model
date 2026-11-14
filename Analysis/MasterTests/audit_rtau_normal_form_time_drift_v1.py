"""Independent kinetic/forward-block formulas and exact time-bound rounding."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import r4c1_canonical_density_factory_v1 as factory

ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/outputs/rtau_normal_form_time_drift_v1_20261114/receipt.json'
PERIODIC='Analysis/MasterTests/outputs/rtau_periodic_principal_composition_v2_20261104/receipt.json'
ORD=[0,1,3,6,7,8,9,10,11]


def exact(t):
    s,n,e,b=t
    assert n>=0 and (n.bit_length()==b or n==b==0)
    return (-1 if s else 1)*Fraction(n)*Fraction(2)**e


def calculate():
    path=ROOT/SOURCE;raw=path.read_bytes();d=json.loads(raw)
    periodic=json.loads((ROOT/PERIODIC).read_bytes())
    ctx=factory.prepare();mp.mp.dps,mp.iv.dps=100,60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    J=ctx['J'];y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    qtime=[J(coefficients=[x.c[0],v.c[0],iv.mpf(0)]) for x,v in zip(y[:14],y[14:28])]
    N,mu,gam,H,_=ctx['geometry'](qtime,[J(0)]*14)
    par=ctx['env']['env']['exact']
    rat=lambda x:iv.mpf(int(x.p))/int(x.q)
    zeta,MU,c1,c2,c3,c4=[rat(par[k]) for k in ('zeta','MU2','c1','c2','c3','c4')]
    alpha=mu/N
    # Canonical plus alignment scalar Hessian; frame derivatives do not enter.
    cv=gam**2-1
    scalar={(8,8):alpha,
            (6,6):alpha*(1-cv*(qtime[10]**2)*zeta),
            (7,7):alpha*(1-cv*(qtime[9]**2)*zeta),
            (6,7):alpha*cv*qtime[9]*qtime[10]*zeta}
    h=[[qtime[0],qtime[1],qtime[2]],[qtime[1],qtime[3],qtime[4]],[qtime[2],qtime[4],qtime[5]]]
    hv=[sum((h[i][j]*qtime[6+j] for j in range(3)),J(0)) for i in range(3)]
    a=gam**2*c4+c1;bb=a+c2+c3
    frame={(3+i,3+j):alpha*(a*h[i][j]-bb*hv[i]*hv[j]/(gam**2))*MU for i in range(3) for j in range(3)}
    A=d['material_blocks_value_time_binary']['A']
    overlap=lambda x,e:max(lo(x),lo(decode(e)))<=min(hi(x),hi(decode(e)))
    def consistent(entries):
        return all(overlap(jet.c[k],A[i][j][k]) for (i,j),jet in entries.items() for k in (0,1))
    s=J(coefficients=[y[40].c[0],y[26].c[1],iv.mpf(0)])
    kappa=H[2][2]
    # Generic metric derivatives, specialized only after taking the time jet.
    logs=[H[0][0]/2,H[0][1],H[1][1]/2]+[J(0)]*6
    ks=[-(H[2][0]**2),-2*H[2][0]*H[2][1],-(H[2][1]**2)]+[J(0)]*6
    forward=[-s*(l+k/kappa) for l,k in zip(logs,ks)]
    cross=d['cross_matrix_time_binary']
    forward_ok=all(overlap(jet.c[1],cross[9+i][19]['imag']) and overlap(iv.mpf(0),cross[9+i][19]['real']) for i,jet in enumerate(forward))
    def maximum_endpoint(pair):return max(abs(exact(t)) for t in pair)
    squared=sum(maximum_endpoint(z['real'])**2+maximum_endpoint(z['imag'])**2 for row in cross for z in row)
    bound=d['bounds_binary'];C=exact(bound['C_time'][1]);Tinv=exact(periodic['values_binary']['global_T_inverse_norm'][1])
    transformed=exact(bound['T_time_times_inverse'][1])
    checks=dict(independent_scalar_kinetic_value_and_time_rates=consistent(scalar),
                independent_frame_kinetic_value_and_time_rates=consistent(frame),
                nonzero_scalar_time_rate_is_not_discarded=lo(alpha.c[1])>0 or hi(alpha.c[1])<0,
                independent_generic_forward_block_time_rates=forward_ok,
                exact_frobenius_time_bound_rounding=C*C>=squared,
                exact_inverse_composition_rounding=transformed>=C*Tinv,
                physical_evolution_holds_retained=d['energy_time_derivative']=='OPEN'
                  and d['domain_persistence']=='OPEN' and d['background_time_tube']=='OPEN'
                  and d['physics_pass'] is False)
    assert all(checks.values()),checks
    assert path.read_bytes()==raw
    return dict(kind='RTAU_NORMAL_FORM_TIME_DRIFT_INDEPENDENT_AUDIT_V1',receipt=SOURCE,
                receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Independent time-drift audit replay')
    else:
        with a.output.open('xb') as f:f.write(raw)
        print('Independent kinetic, forward-block and rational audit passed')


if __name__=='__main__':main()
