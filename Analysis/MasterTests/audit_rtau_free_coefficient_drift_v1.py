"""Exact controls for ordinary free-slot measure and flux differentiation."""

import json
import mpmath as mp
import sympy as sp
import r4c1_canonical_density_factory_v1 as factory
from test_rtau_free_coefficient_drift_v1 import mixed_time_engine,TIME


def calculate():
    ctx=factory.prepare()
    mp.mp.dps,mp.iv.dps=100,60
    J,D,iv=ctx['J'],ctx['D'],mp.iv
    mixed_time_engine(D)
    q= D(J(iv.mpf(2)/5),{0:J(1),TIME:J(iv.mpf(3)/7)})
    p= D(J(iv.mpf(1)/3),{1:J(1),TIME:J(iv.mpf(2)/11)})
    measure=q.exp()*(2+q*q)
    flux=q*p/(2+q*q)
    g=lambda f,i:f.g.get(i,J(0))
    h=lambda f,i:f.h.get((i,TIME),J(0))
    x,y,t=sp.symbols('x y t')
    M=sp.exp(x)*(2+x*x)
    F=x*y/(2+x*x)
    substitution={x:sp.Rational(2,5),y:sp.Rational(1,3)}
    time=lambda f:sp.diff(f,x)*sp.Rational(3,7)+sp.diff(f,y)*sp.Rational(2,11)
    ell_t=h(measure,0)/measure.c-g(measure,0)*g(measure,TIME)/measure.c**2
    expected=[time(sp.diff(M,x)/M),time(sp.diff(F,x)),time(sp.diff(F,y))]
    actual=[ell_t.c[0],h(flux,0).c[0],h(flux,1).c[0]]
    controls={}
    for name,a,e in zip(('measure_log_row_rate','canonical_flux_configuration_rate','canonical_flux_momentum_rate'),actual,expected):
        target=iv.mpf(str(sp.N(e.subs(substitution),85)))
        delta=a-target
        controls[name]=max(abs(mp.mpf(delta._mpi_[0])),abs(mp.mpf(delta._mpi_[1])))<mp.mpf('1e-50')
    I,ell=sp.Function('I')(t),sp.Function('ell')(t)
    controls['measure_current_rate_retains_both_factors']=sp.diff(-I*ell,t)==-sp.diff(I,t)*ell-I*sp.diff(ell,t)
    controls['momentum_rate_changes_canonical_flux_partial']=sp.diff(F,x,y).subs(substitution)!=0
    assert all(controls.values()),controls
    return controls


if __name__=='__main__':
    print(json.dumps(calculate(),indent=2))
