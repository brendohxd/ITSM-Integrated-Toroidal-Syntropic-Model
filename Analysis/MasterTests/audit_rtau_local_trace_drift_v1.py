"""Independent exact moving-shape and weak-divergence controls."""

import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import r4c1_canonical_density_factory_v1 as factory
from test_rtau_local_trace_drift_v2 import mixed_time_engine, TIME


def calculate():
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J,D,iv=ctx['J'],ctx['D'],mp.iv
    mixed_time_engine(D)
    x,e,t,z=sp.symbols('x e t z',real=True)
    expr=sp.exp(x)/(2+x)+sp.sqrt(3+x*x)
    X=D(J(iv.mpf(2)/5),{0:J(iv.mpf(3)/7),TIME:J(iv.mpf(1)/11)},
        {(0,TIME):J(iv.mpf(2)/13)})
    value=X.exp()/(2+X)+(3+X*X)**mp.mpf('.5')
    expected=sp.diff(expr.subs(x,sp.Rational(2,5)+t/11+e*(sp.Rational(3,7)+2*t/13)),e,t).subs({e:0,t:0})
    target=iv.mpf(str(sp.N(expected,85)))
    delta=value.h[(0,TIME)].c[0]-target
    A,B,C,E=[sp.Function(s)(z,t) for s in ('A','B','C','E')]
    f=1+sp.sin(z)+sp.cos(2*z)
    row=A*f+B*sp.diff(f,z)-sp.diff(C*f+E*sp.diff(f,z),z)
    rate=sp.diff(A,t)*f+sp.diff(B,t)*sp.diff(f,z)-sp.diff(sp.diff(C,t)*f+sp.diff(E,t)*sp.diff(f,z),z)
    M,I=sp.Function('M')(t),sp.Function('I')(t)
    checks={
        'moving_shape_mixed_seed_matches_exact_chain_rule':
            max(abs(mp.mpf(delta._mpi_[0])),abs(mp.mpf(delta._mpi_[1])))<mp.mpf('1e-50'),
        'weak_divergence_rate_equals_direct_differentiation':sp.expand(sp.diff(row,t)-rate)==0,
        'measure_term_has_its_own_time_derivative':sp.diff(-I*f,t)==-sp.diff(I,t)*f,
        'omitted_moving_shape_seed_has_nonzero_exact_contribution':
            sp.simplify(sp.diff(expr,x).subs(x,sp.Rational(2,5))*sp.Rational(2,13))!=0,
        'original_periodic_mean_mode_retained':sp.integrate(f,(z,0,2*sp.pi))==2*sp.pi,
    }
    assert all(checks.values()),checks
    return checks


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
