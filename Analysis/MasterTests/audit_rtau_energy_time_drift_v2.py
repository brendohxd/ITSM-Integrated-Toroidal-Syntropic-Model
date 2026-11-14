"""Independent gradient formulas and exact energy-time bound aggregation."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import mpmath as mp
import r4c1_canonical_density_factory_v1 as factory

ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/outputs/rtau_energy_time_drift_v2_20261114/receipt.json'
PERIODIC='Analysis/MasterTests/outputs/rtau_periodic_principal_composition_v2_20261104/receipt.json'
TIME='Analysis/MasterTests/outputs/rtau_normal_form_time_drift_v1_20261114/receipt.json'


def exact(t):
    s,n,e,b=t
    assert n>=0 and (n.bit_length()==b or n==b==0)
    return (-1 if s else 1)*Fraction(n)*Fraction(2)**e


def calculate():
    p=ROOT/SOURCE;raw=p.read_bytes();d=json.loads(raw)
    periodic=json.loads((ROOT/PERIODIC).read_bytes());td=json.loads((ROOT/TIME).read_bytes())
    ctx=factory.prepare();mp.mp.dps,mp.iv.dps=100,60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    J=ctx['J'];y,_=ctx['state'](J.variable(iv.mpf([0,hi(2*iv.pi)])),True,[0,0,0])
    q=[J(coefficients=[x.c[0],v.c[0],iv.mpf(0)]) for x,v in zip(y[:14],y[14:28])]
    N,mu,gamma,H,_=ctx['geometry'](q,[J(0)]*14)
    pars=ctx['env']['env']['exact'];rat=lambda x:iv.mpf(int(x.p))/int(x.q)
    zeta,MU,c1,c2,c3,c4=[rat(pars[k]) for k in ('zeta','MU2','c1','c2','c3','c4')]
    base=N*mu;kap=H[2][2];extra=kap+q[8]**2
    scalar={(8,8):-base*kap,
            (6,6):-base*(kap+extra*q[10]**2*zeta),
            (7,7):-base*(kap+extra*q[9]**2*zeta),
            (6,7):base*extra*q[9]*q[10]*zeta}
    h=[[q[0],q[1],q[2]],[q[1],q[3],q[4]],[q[2],q[4],q[5]]]
    hv=[sum((h[i][j]*q[6+j] for j in range(3)),J(0)) for i in range(3)]
    a=kap*c1-q[8]**2*c4
    frame={(3+i,3+j):-base*(a*(h[i][j]-hv[i]*hv[j]/gamma**2)+(c2+c3)*int(i==j==2))*MU for i in range(3) for j in range(3)}
    G=d['gradient_block_value_time_binary']
    overlap=lambda x,e:max(lo(x),lo(decode(e)))<=min(hi(x),hi(decode(e)))
    consistent=lambda entries:all(overlap(jet.c[k],G[i][j][k]) for (i,j),jet in entries.items() for k in (0,1))
    B=d['bounds_binary'];upper=lambda k:exact(B[k][1])
    bound_of=lambda name:sum(max(abs(exact(x)) for x in z['real'])**2+max(abs(exact(x)) for x in z['imag'])**2 for row in d[name] for z in row)
    f,ft,l,lt,eh=map(upper,['chart','chart_time','stationary_row','stationary_row_time','seed_energy'])
    terms=d['contribution_bounds_binary'];pu={k:exact(v[1]) for k,v in terms.items()}
    stationary=(upper('stationary_drive_time')+l*upper('complement_generator_time'))*upper('complement_inverse')
    t0=exact(periodic['values_binary']['global_T_norm'][1]);tt=exact(td['bounds_binary']['T_time'][1])
    fast=max(max(abs(exact(v)) for v in row[1]) for row in d['fast_energy_value_time_binary'])
    checks=dict(independent_scalar_gradient_value_and_time_rates=consistent(scalar),
                independent_frame_gradient_value_and_time_rates=consistent(frame),
                nonzero_scalar_gradient_rate_not_discarded=lo(scalar[8,8].c[1])>0 or hi(scalar[8,8].c[1])<0,
                exact_complement_energy_frobenius_rounding=upper('complement_energy_time')**2>=bound_of('complement_energy_time_binary'),
                exact_complement_generator_frobenius_rounding=upper('complement_generator_time')**2>=bound_of('complement_generator_time_binary'),
                exact_stationary_drive_frobenius_rounding=upper('stationary_drive_time')**2>=bound_of('stationary_drive_time_binary'),
                exact_stationary_row_rate_aggregation=lt>=stationary,
                exact_three_energy_terms=pu['chart_time']>=2*f*ft*(1+l)**2*eh
                    and pu['stationary_row_time']>=2*f*f*(1+l)*lt*eh
                    and pu['complement_energy_time']>=f*f*(1+l)**2*upper('complement_energy_time'),
                exact_ordinary_energy_time_sum=upper('ordinary_energy_time')>=sum(pu.values()),
                exact_fast_and_diagonal_energy_time=upper('fast_energy_time')>=fast
                    and upper('diagonal_energy_time')>=max(upper('ordinary_energy_time'),upper('fast_energy_time')),
                exact_pulled_back_energy_time=upper('pulled_back_energy_time')>=t0*t0*upper('diagonal_energy_time')+2*t0*upper('diagonal_energy')*tt,
                full_evolution_holds_retained=d['full_coupled_energy_inequality']=='OPEN'
                    and d['domain_persistence']=='OPEN' and d['background_time_tube']=='OPEN' and d['physics_pass'] is False)
    assert all(checks.values()),checks
    assert p.read_bytes()==raw
    return dict(kind='RTAU_ENERGY_TIME_INDEPENDENT_AUDIT_V2',receipt=SOURCE,
                receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Independent energy-time audit replay')
    else:
        with a.output.open('xb') as f:f.write(raw)
        print('Independent gradient and exact energy-time audit passed')


if __name__=='__main__':main()
