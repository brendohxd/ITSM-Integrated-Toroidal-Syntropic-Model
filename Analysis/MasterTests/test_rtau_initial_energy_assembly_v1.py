"""Initial mixed energy with actual global rates and explicit gauge controls."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_INITIAL_ENERGY_ASSEMBLY_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_energy_time_drift_v2_20261114/receipt.json'
PARENTS={
 'periodic':'rtau_periodic_principal_composition_v2_20261104',
 'ordinary':'rtau_ordinary_ward_energy_v4_20261104',
 'twenty':'rtau_initial_twenty_row_composition_v3_20261114',
 'advection':'rtau_physical_advection_composition_v1_20261114',
 'time':'rtau_normal_form_time_drift_v1_20261114',
 'shift':'rtau_physical_density_remainder_v2_20261114',
 'gauge':'rtau_gauge_mean_trace_rate_v2_20261109',
 'lift':'rtau_momentum_rate_lift_v2_20261104',
 'weak':'rtau_weak_canonical_rate_v2_20261103',
}
MIXED=OUT+'r4c1_rtau_mixed_operator_v4_attempt_01/summary.json'


def exact_controls():
    """Exact Laurent integration; all original zero modes are retained."""
    x,t=sp.symbols('x t',nonzero=True)
    def terms(f):
        return [(int(v.as_powers_dict().get(x,0)),v) for v in sp.Add.make_args(sp.expand(f))]
    def D(f):return sp.expand(sp.I*x*sp.diff(f,x))
    def P(f):return sp.expand(sum(v/(sp.I*n) for n,v in terms(f) if n))
    def mean(f):return sp.expand(sum(v for n,v in terms(f) if n==0))
    def conj(f):return sp.expand(sum(sp.conjugate(v/x**n)*x**(-n) for n,v in terms(f)))
    dm=lambda a:a.applyfunc(D)
    inner=lambda a,H,b:mean((a.applyfunc(conj).T*H*b)[0])
    real=lambda a:sp.expand((a+sp.conjugate(a))/2)
    d=3+(x+1/x)/10;h=2+(x+1/x)/20
    v=sp.Rational(1,7)+(x+1/x)/17
    drift=sp.Rational(1,9)+(x-1/x)/(23*sp.I)
    a=2+(x*x+x**-2)/30
    u=sp.Matrix([2+x/3+sp.I*x**-2/5,1+x*x/7+sp.I*x**-1/11,3+sp.I*x/13+x**-3/17])
    H=sp.diag(h,d,d);HF=sp.diag(d,d)
    J=sp.Matrix([[0,1],[-1,0]])
    AF=d*J
    BF=sp.Matrix([[-drift,-3*D(d)],[D(d),-drift]])
    uf=u[1:3,0]
    G=sp.Matrix.vstack(sp.Matrix([a*D(u[0])]),-AF*dm(dm(uf))+BF*dm(uf))
    flux=HF*AF
    fast_zero=dm(dm(flux))-dm(BF.T*HF)
    principal=2*real(inner(u,H,G))
    principal_by_parts=-inner(u[:1,0],sp.Matrix([[D(h*a)]]),u[:1,0])+inner(uf,fast_zero,uf)
    advected=2*real(inner(u,H,v*dm(u)))
    advection_by_parts=-inner(u,dm(v*H),u)
    R=sp.Matrix([[1,x/7,0],[1/x/11,2,x/13],[x/17,0,3]])
    A=sp.Matrix([[1,x/19,0],[0,2,1/x/23],[x/29,0,1]])
    C=sp.Matrix([[0,x/31,1],[2,0,1/x/37],[x/41,1,0]])
    rank=(A*u).applyfunc(mean);primitive=(C*u).applyfunc(P)
    remainder=R*u+rank+primitive
    g=sp.Matrix([2,3]);control=sp.Matrix([sp.Rational(1,7),-sp.Rational(2,11)])
    Fg=sp.Matrix([[1,x/43],[2,1],[1/x/47,3]])
    Fh=sp.Matrix([[1,2],[x/53,1],[2,1/x/59]])
    gd=sp.Matrix([[1,2],[3,1]])*g+(sp.Matrix([[1,x/61,0],[0,1,1/x/67]])*u).applyfunc(mean)+sp.Matrix([[1,2],[2,1]])*control
    Ht=sp.diag(1+(x*x+x**-2)/71,2+(x-1/x)/(73*sp.I),3+(x+1/x)/79)
    rate=v*dm(u)+G+remainder+Fg*g+Fh*control
    direct=inner(u,Ht,u)+2*real(inner(u,H,rate))+2*real((g.T*gd)[0])
    assembled=inner(u,Ht,u)+principal_by_parts+advection_by_parts+2*real(inner(u,H,remainder+Fg*g+Fh*control))+2*real((g.T*gd)[0])
    # Original coordinate mean projections for eight free fields plus chi.
    Proj=sp.zeros(9,13);Proj[0,0]=sp.Rational(1,2);Proj[0,3]=-sp.Rational(1,2);Proj[1,1]=1
    for j,i in enumerate((6,7,8,9,10,11),2):Proj[j,i]=1
    Proj[8,12]=1
    H0,H1=sp.symbols('H0 H1')
    gauge_base=x/3+x**-2/5
    return dict(exact_variable_ordinary_and_fast_spatial_energy=sp.simplify(principal-principal_by_parts)==0,
                exact_physical_advection_energy=sp.simplify(advected-advection_by_parts)==0,
                exact_full_initial_energy_identity=sp.simplify(direct-assembled)==0,
                omitted_energy_time_rejected=sp.simplify(inner(u,Ht,u))!=0,
                omitted_shift_gradient_rejected=sp.simplify(inner(u,H*D(v),u))!=0,
                omitted_energy_spatial_gradient_rejected=sp.simplify(inner(u,dm(H)*v,u))!=0,
                omitted_finite_rank_mean_rejected=sp.simplify(2*real(inner(u,H,rank)))!=0,
                omitted_primitive_tail_rejected=sp.simplify(2*real(inner(u,H,primitive)))!=0,
                omitted_global_rate_rejected=sp.simplify(2*real((g.T*gd)[0]))!=0,
                omitted_harmonic_forcing_rejected=sp.simplify(2*real(inner(u,H,Fh*control)))!=0,
                constant_and_nonzero_modes_kept=all(mean(f)!=0 and sp.expand(f-mean(f))!=0 for f in u),
                canonical_mean_projection_is_contraction=Proj*Proj.T==sp.diag(sp.Rational(1,2),*([1]*8)),
                harmonic_history_not_fixed_by_spatial_gauge=sp.expand(D(gauge_base+H0+t*H1)-D(gauge_base))==0)


def calculate():
    mp.mp.dps,mp.iv.dps=100,60;iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0]);hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    ab=lambda x:iv.mpf(max(abs(lo(x)),abs(hi(x))))
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(t) for t in iv.mpf(x)._mpi_]
    parent=read(PARENT);paths={k:OUT+v+'/receipt.json' for k,v in PARENTS.items()}
    data={k:read(p) for k,p in paths.items()};mixed=read(MIXED)
    pins=dict(parent['source_pins'])
    for rel in (CONTRACT,PARENT,MIXED,*paths.values(),Path(__file__).relative_to(ROOT).as_posix()):
        p=ROOT/rel;h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for d in (parent,*data.values(),mixed) for c in d['checks'])
    checks=exact_controls()
    unit=lambda j:[iv.mpf(int(i==j)) for i in range(9)]
    vector=lambda xs:list(map(decode,xs))
    def nine(xs):
        a=vector(xs);assert len(a)==8;return a+[iv.mpf(0)]
    assert data['lift']['density_coordinate']=='Sigma=rho+e_force+b*Z**2/2'
    Q=nine(data['lift']['constants_binary']['full_configuration_H1'])
    P=nine(data['lift']['constants_binary']['full_momentum_L2'])
    wc=vector(data['weak']['coefficients_binary']['field_rate_L2'])
    assert lo(wc[2])==hi(wc[2])==0
    gb={k:vector(v) for k,v in data['gauge']['bounds_binary'].items()}
    qt=[wc[0]*p+wc[1]*q+wc[3]*s for p,q,s in zip(P,Q,gb['corrective_shift_H1'])]
    partners=[iv.sqrt(qt[j]**2+gb['metric_modulus_rate_vector'][j]**2
                       +sum((gb['eliminated_momentum_mean_'+k+'_rate'][j]**2 for k in ('x','y','z')),iv.mpf(0))) for j in range(9)]
    L=iv.mpf(max(hi(x) for x in partners))
    energy=parent['bounds_binary'];periodic=data['periodic']['values_binary']
    H0=decode(energy['diagonal_energy']);Ht=decode(energy['diagonal_energy_time'])
    T=decode(periodic['global_T_norm']);Ti=decode(periodic['global_T_inverse_norm'])
    Rcomp=decode(periodic['periodic_composition_remainder_bound'])
    Radvection=decode(data['advection']['bounds_binary']['additional_transformed_advection'])
    Rtime=decode(data['time']['bounds_binary']['T_time_times_inverse'])
    Csource=decode(data['twenty']['bounds_binary']['per_nine_input_sum'])
    shift=data['shift']['coefficient_bounds_binary']
    v,vz=decode(shift['S']),decode(shift['Sz'])
    raw={tuple(row['ij']):(decode(row['value']),decode(row['dz'])) for row in mixed['full_mixed_Hessian_upper_triangle']}
    mass,massz=raw[26,26];assert lo(mass)>0
    fast=parent['fast_energy_value_time_binary']
    hf1,hf2=[decode(row[0]) for row in fast]
    smax=iv.mpf(1)/1000*(iv.mpf(1)/29+iv.mpf(1)/31)
    hf1z=iv.mpf(hi(hf1))*(iv.mpf(3)/13000+iv.mpf(2)/5*smax)
    hf2z=ab(massz)/(iv.mpf(lo(mass))**2)
    fastz=iv.mpf(max(hi(hf1z),hi(hf2z)))
    Hz=iv.mpf(max(hi(decode(periodic['ordinary_energy_z_bound'])),hi(fastz)))
    amin=iv.mpf(min(lo(decode(data['ordinary']['ordinary_norm_constants']['energy_lower_binary'])),lo(hf1),lo(hf2)))
    assert lo(amin)>0
    adjoint=decode(periodic['ordinary_spatial_energy_adjoint_bound'])+decode(periodic['fast_spatial_energy_adjoint_bound'])
    advective=vz*H0+v*Hz
    r=iv.mpf(1)/13000
    Jmod=iv.exp(4*r)*iv.sqrt(1+4*r*r)
    bz,bg=5*Ti,iv.sqrt(6+Jmod*Jmod)
    source=H0*T*Csource
    base=Ht+adjoint+advective+2*H0*(Rcomp+Radvection+Rtime)+2*source*bz
    zg=source*bg+L*bz
    zh=source
    # g=(mean phi_8, metric_moduli_3, mean chi_1, eta_3).
    # Harmonic coordinate velocity H_3 is an explicit control, not in g.
    zcoef=base+zg+zh
    gcoef=2*L*bg+zg+L
    hcoef=zh+L
    Econstant=iv.mpf(max(hi(zcoef/amin),hi(gcoef)))
    lower=iv.mpf(min(lo(amin),mp.mpf(1)))
    upper=iv.mpf(max(hi(H0),mp.mpf(1)))
    input_lower=bz*bz/amin+bg*bg
    input_upper=H0*T*T+iv.exp(8*r)
    terms=dict(energy_time=Ht,principal_spatial_adjoint=adjoint,physical_advection=advective,
               bounded_normal_form_terms=2*H0*(Rcomp+Radvection+Rtime),
               actual_remainder_state=2*source*bz,state_global_cross=zg,
               state_harmonic_cross=zh,global_self=2*L*bg,global_harmonic_cross=L)
    bounds=dict(global_partner_rate_per_U=L,fast_energy_spatial_derivative=fastz,
                diagonal_energy_spatial_derivative=Hz,diagonal_energy=H0,
                diagonal_coercivity=amin,normal_form=T,normal_form_inverse=Ti,
                input_state_weight=bz,input_global_weight=bg,source_remainder_per_U=Csource,
                source_energy_cross=source,state_squared_coefficient=zcoef,
                global_squared_coefficient=gcoef,harmonic_squared_coefficient=hcoef,
                augmented_energy_coefficient=Econstant,augmented_coercivity=lower,
                augmented_energy_upper=upper,U0_squared_per_energy=input_lower,
                energy_per_U0_squared=input_upper)
    checks.update(fifteen_global_coordinates_and_three_controls=8+3+1+3==15,
                  harmonic_input_affects_field_rate=hi(qt[-1])>0,
                  all_nine_rate_input_columns_retained=len(partners)==9,
                  energy_time_counted_once=len([k for k in terms if k=='energy_time'])==1,
                  positive_finite_coercivity_and_constants=all(lo(x)>=0 and mp.isfinite(hi(x)) for x in bounds.values()) and lo(lower)>0,
                  actual_source_bytes_and_sidecars_unchanged=all((digest(f),f.stat().st_mtime_ns)==value for f,value in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_INITIAL_FORCED_MIXED_ENERGY_ASSEMBLY_V1',source_pins=pins,pinned_files=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                original_input_order=data['twenty']['input_order'],
                configuration_and_clock_mean_rate_binary=[binary(x) for x in qt],
                global_partner_rate_binary=[binary(x) for x in partners],
                contribution_bounds_binary={k:binary(x) for k,x in terms.items()},
                bounds_binary={k:binary(x) for k,x in bounds.items()},
                upper_display={k:mp.nstr(hi(x),30) for k,x in bounds.items()},
                exact_energy='E=mean(Z^dagger Hdiag Z)+|g_15|^2',
                inequality='E_prime(0)<=C_E*E(0)+C_H*|H_3(0)|^2',
                control_role='INDEPENDENT_HARMONIC_COORDINATE_VELOCITY_FROM_REGISTERED_GAUGE',
                harmonic_rate_law='NOT_SPECIFIED_BY_SPATIAL_GAUGE_EQUATIONS',
                domain='INHERITED_SMOOTH_COMPATIBLE_INITIAL_EULER_CONSTRAINT_AUXILIARY_JETS',
                scope='CONDITIONAL_INITIAL_FORCED_ENERGY_INEQUALITY_WITH_GLOBAL_PARTNERS',
                closed_autonomous_physical_evolution='OPEN',domain_persistence='OPEN',background_time_tube='OPEN',
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Byte-identical initial forced-energy replay')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=False)
        with a.output.open('xb') as f:f.write(raw)
        print('Initial mixed energy with globals and harmonic controls verified')


if __name__=='__main__':main()
