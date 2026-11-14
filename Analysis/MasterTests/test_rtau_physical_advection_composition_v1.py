"""Exact periodic advection commutator and certified initial L2 bound."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_PHYSICAL_ADVECTION_COMPOSITION_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_initial_twenty_row_composition_v3_20261114/receipt.json'
PERIODIC=OUT+'rtau_periodic_principal_composition_v2_20261104/receipt.json'
MIXED=OUT+'rtau_mixed_principal_assembly_v1_20261104/receipt.json'
SHIFT=OUT+'rtau_physical_density_remainder_v2_20261114/receipt.json'


def fourier_controls():
    """Exact sparse Fourier convolution; no sampled grid or truncation."""
    rat=sp.Rational
    C={0:sp.Matrix([[0,0,0],[0,rat(1,3),rat(2,7)],[0,-rat(1,5),rat(1,11)]]),
       1:sp.Matrix([[0,0,0],[0,0,rat(1,13)],[0,rat(1,17),0]]),
       -2:sp.Matrix([[0,0,0],[0,rat(2,19),0],[0,0,-rat(1,23)]])}
    v={0:rat(2,5),1:rat(1,7),-1:rat(1,11),2:rat(1,13)}
    u={0:sp.Matrix([1,2,3]),1:sp.Matrix([rat(2,3),-rat(1,7),rat(1,11)]),
       -3:sp.Matrix([rat(1,5),rat(2,13),-rat(3,17)])}
    def simplify(x):
        return x.applyfunc(sp.expand) if isinstance(x,sp.MatrixBase) else sp.expand(x)
    def nonzero(x):
        return x!=sp.zeros(*x.shape) if isinstance(x,sp.MatrixBase) else x!=0
    def clean(a):return {n:simplify(x) for n,x in a.items() if nonzero(simplify(x))}
    def add(*terms):
        out={}
        for a in terms:
            for n,x in a.items():out[n]=out[n]+x if n in out else x
        return clean(out)
    def scale(a,c):return clean({n:c*x for n,x in a.items()})
    def mul(a,b):
        out={}
        for n,x in a.items():
            for m,y in b.items():
                out[n+m]=out[n+m]+x*y if n+m in out else x*y
        return clean(out)
    def D(a):return clean({n:sp.I*n*x for n,x in a.items() if n})
    def P(a):return clean({n:x/(sp.I*n) for n,x in a.items() if n})
    def mean(a):return {0:a[0]} if 0 in a else {}
    T=lambda f:add(f,scale(P(mul(C,f)),sp.I))
    adv=lambda f:mul(v,D(f))
    def identity(f):
        lhs=add(T(adv(f)),scale(adv(T(f)),-1))
        a=mul(v,mean(mul(C,f)))
        b=mean(mul(v,mul(C,f)))
        c=P(mul(mul(v,D(C)),f))
        d=P(mul(mul(D(v),C),f))
        rhs=scale(add(a,scale(b,-1),scale(c,-1),scale(d,-1)),sp.I)
        return lhs,rhs,(a,b,c,d)
    lhs,rhs,terms=identity(u)
    zero_lhs,zero_rhs,_=identity({0:u[0]})
    expected_mean=scale(add(mul(mean(v),mean(mul(C,u))),scale(mean(mul(v,mul(C,u))),-1)),sp.I)
    density_row_zero=all(x[0]==0 for x in lhs.values())
    return dict(exact_nonconstant_matrix_fourier_commutator=not add(lhs,scale(rhs,-1)),
                original_zero_mode_identity=not add(zero_lhs,scale(zero_rhs,-1)),
                zero_mode_commutator_not_discarded=bool(zero_lhs),
                derivative_primitive_original_mean=not add(D(P(u)),scale(add(u,scale(mean(u),-1)),-1)),
                primitive_derivative_original_mean=not add(P(D(u)),scale(add(u,scale(mean(u),-1)),-1)),
                omitted_first_mean_rejected=bool(terms[0]),
                omitted_second_mean_rejected=bool(terms[1]),
                omitted_coefficient_gradient_rejected=bool(terms[2]),
                omitted_shift_gradient_rejected=bool(terms[3]),
                mean_of_commutator_retained=not add(mean(lhs),scale(expected_mean,-1)) and bool(expected_mean),
                normal_form_density_row_unchanged=density_row_zero,
                varying_matrix_fixture_noncommuting=C[0]*C[1]!=C[1]*C[0])


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    parent=read(PARENT)
    data={k:read(p) for k,p in [('periodic',PERIODIC),('mixed',MIXED),('shift',SHIFT)]}
    pins=dict(parent['source_pins'])
    for d in data.values():
        inherited=d.get('source_pins',d.get('source_sha256',{}))
        assert isinstance(inherited,dict)
        for rel,h in inherited.items():
            assert rel not in pins or pins[rel]==h,rel
            pins[rel]=h
    for rel in (CONTRACT,PARENT,PERIODIC,MIXED,SHIFT,Path(__file__).relative_to(ROOT).as_posix()):
        p=ROOT/rel;h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for d in (parent,*data.values()) for c in d['checks'])
    C0=decode(data['mixed']['values_binary']['S_norm_bound'])
    C1=decode(data['periodic']['values_binary']['S_z_norm'])
    v0=decode(data['shift']['coefficient_bounds_binary']['S'])
    v1=decode(data['shift']['coefficient_bounds_binary']['Sz'])
    inverse=decode(data['periodic']['values_binary']['global_T_inverse_norm'])
    contributions=dict(two_original_mean_terms=2*v0*C0,
                       normal_form_coefficient_gradient=v0*C1,
                       physical_shift_gradient=v1*C0)
    comm=sum(contributions.values(),iv.mpf(0))
    transformed=comm*inverse
    checks=fourier_controls()
    checks.update(initial_all_mode_constants_positive_finite=all(lo(x)>=0 and mp.isfinite(hi(x)) for x in [comm,transformed]),
                  inverse_uses_registered_global_domain=hi(C0)<1 and hi(inverse)>1,
                  original_physical_shift_used=v0!=decode(data['shift']['coefficient_bounds_binary']['v']),
                  original_source_bytes_and_timestamps_preserved=all((digest(f),f.stat().st_mtime_ns)==value for f,value in snap.items()))
    assert all(checks.values()),checks
    bounds=dict(normal_form_C=C0,normal_form_C_z=C1,physical_shift=v0,
                physical_shift_z=v1,normal_form_inverse=inverse,
                advection_commutator=comm,additional_transformed_advection=transformed)
    return dict(kind='RTAU_INITIAL_PHYSICAL_ADVECTION_COMPOSITION_V1',source_pins=pins,pinned_files=len(pins),
                exact_commutator='[T,vD]f=i(v*mean(Cf)-mean(vCf)-P((v*C_z+v_z*C)f))',
                transformed_advection='T*(vD)*T^-1=vD+[T,vD]*T^-1',
                primitive='ORIGINAL_COORDINATE_D_INVERSE_P0',
                bounds_binary={k:binary(v) for k,v in bounds.items()},
                contribution_bounds_binary={k:binary(v) for k,v in contributions.items()},
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                scope='CONDITIONAL_INITIAL_PHYSICAL_ADVECTION_COMPONENT_ONLY',
                normal_form_time_derivative='OPEN',energy_time_derivative='OPEN',
                domain_persistence='OPEN',background_time_tube='OPEN',
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Byte-identical physical-advection replay')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=False)
        with a.output.open('xb') as f:f.write(raw)
        print('Initial physical-advection commutator verified')


if __name__=='__main__':main()
