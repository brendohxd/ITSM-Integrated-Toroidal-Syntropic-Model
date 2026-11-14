"""Compose the actual initial twenty-row remainder on compatible jets."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as sp
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_INITIAL_TWENTY_ROW_COMPOSITION_V2_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_physical_density_remainder_v2_20261114/receipt.json'
PARENTS={
    'state':'rtau_density_state_map_v1_20261114',
    'gradient':'rtau_ordinary_velocity_remainder_v2_20261104',
    'momentum':'rtau_ordinary_momentum_remainder_v3_20261104',
    'force':'rtau_actual_force_pair_v2_20261105',
    'density':'rtau_actual_corrected_density_v4_20261105',
    'mixed':'rtau_mixed_principal_assembly_v1_20261104',
}


def exact_controls():
    # Independent variable-coefficient matrix product rules in physical D.
    z=sp.symbols('z',real=True)
    E=sp.Matrix([1,-1]); R=E.T/2; tr=sp.Matrix([1,1])
    phi=2+sp.sin(z)+sp.cos(2*z)
    tau=3+sp.cos(z)/3
    q=E*phi+tr*tau
    w=4+sp.sin(2*z)
    Y=sp.Matrix([w,-sp.I*sp.diff(phi,z),1+sp.sin(z),2+sp.cos(3*z)])
    c=1+sp.sin(z)/7
    L=sp.zeros(2,4);L[:,1]=E;L[:,3]=sp.I*c*tr
    V=sp.Matrix(2,4,lambda i,j:sp.Rational(i+j+1,11+i+2*j)+sp.sin((j+1)*z)/(17+i+j))
    B=sp.Matrix([[1+sp.sin(z)/5,sp.cos(z)/7],[sp.sin(2*z)/11,2+sp.cos(z)/13]])
    G=sp.Matrix([[2+sp.cos(z)/5,sp.sin(z)/7],[sp.sin(z)/7,3+sp.cos(2*z)/11]])
    F=sp.Matrix([[sp.sin(z),1],[2,sp.cos(z)]])/19
    rv=sp.Matrix([sp.cos(2*z),sp.sin(3*z)])/23
    rq=sp.diff(q,z)-sp.I*L*Y
    velocity=V*Y+rv
    shift=1+sp.sin(z)/29
    # Canonical material field rate is velocity. Differentiating Q=-i D Rq
    # has the extra physical shift commutator.
    actual_gradient=-sp.I*R*sp.diff(velocity,z)-sp.I*sp.diff(shift,z)*R*sp.diff(q,z)
    gradient_principal=-sp.I*R*V*sp.diff(Y,z)
    gradient_remainder=-sp.I*R*sp.diff(V,z)*Y-sp.I*R*sp.diff(rv,z)+sp.diff(shift,z)*Y[1:2,0]
    flux=B.T*velocity+G*sp.diff(q,z)+F*q
    Flead=B.T*V+sp.I*G*L
    flux_remainder=B.T*rv+G*rq+F*q
    momentum_principal=-Flead*sp.diff(Y,z)
    momentum_remainder=-sp.diff(Flead,z)*Y-sp.diff(flux_remainder,z)
    ordinary_A1=sp.Matrix.vstack(sp.zeros(1,4),R*V,-sp.I*B.T*V+G*L)
    selected=sp.Matrix.vstack(sp.zeros(1,1),gradient_principal,momentum_principal)
    zero=lambda m:all(sp.expand_trig(sp.expand(x)).simplify()==0 for x in m)
    # Highest/first force blocks have fixed physical derivative signs.
    kap,ap,d,v,g,r,aq,zz,xx=sp.symbols('kap ap d v g r aq zz xx')
    A2=sp.Matrix([[0,kap*ap],[-d,0]])
    A1=sp.Matrix([[-sp.I*v,-sp.I*g],[sp.I*r,-sp.I*v]])
    fast=sp.Matrix([sp.Function('Z')(z),sp.Function('X')(z)])
    target=sp.Matrix([-kap*ap*sp.diff(fast[1],z,2)-v*sp.diff(fast[0],z)-g*sp.diff(fast[1],z),
                       d*sp.diff(fast[0],z,2)+r*sp.diff(fast[0],z)-v*sp.diff(fast[1],z)])
    return dict(exact_nonconstant_configuration_gradient_row=zero(actual_gradient-gradient_principal-gradient_remainder),
                exact_noncommuting_material_momentum_flux=zero(-sp.diff(flux,z)-momentum_principal-momentum_remainder),
                exact_fourier_to_physical_ordinary_signs=zero(selected+sp.I*ordinary_A1*sp.diff(Y,z)),
                exact_force_first_second_derivative_signs=zero(-A2*sp.diff(fast,z,2)-sp.I*A1*sp.diff(fast,z)-target),
                omitted_principal_coefficient_drift_changes_rows=not zero(sp.diff(Flead,z)*Y),
                omitted_material_gradient_commutator_changes_row=not zero(sp.diff(shift,z)*Y[1:2,0]),
                noncommuting_fixture_is_not_scalar=not zero(B*G-G*B),
                original_configuration_means_retained=R*q-(phi*sp.ones(1,1))==sp.zeros(1,1))


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    parent=read(PARENT)
    paths={k:OUT+v+'/receipt.json' for k,v in PARENTS.items()}
    data={k:read(p) for k,p in paths.items()}
    pins=dict(parent['source_pins'])
    for datum in data.values():
        inherited=datum.get('source_sha256')
        if not isinstance(inherited,dict): inherited=datum.get('source_pins',{})
        for rel,h in inherited.items():
            assert rel not in pins or pins[rel]==h,rel
            pins[rel]=h
    for rel in (CONTRACT,PARENT,*paths.values(),
                'Analysis/MasterTests/test_rtau_initial_twenty_row_composition_v1.py',
                'Analysis/MasterTests/outputs/rtau_initial_twenty_row_composition_v1_20261114/failure.json',
                Path(__file__).relative_to(ROOT).as_posix()):
        p=ROOT/rel;h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel;assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    assert all(c['passed'] for d in (parent,*data.values()) for c in d['checks'])
    order=data['density']['input_order']
    assert all(data[k]['input_order']==order for k in ('gradient','momentum','force'))
    assert parent['input_order']==order
    columns={
        'w':data['density']['bounds_binary']['initial_original_coordinate_density_source_L2'],
        'Q8':data['gradient']['bounds_binary']['eight_gradient_rows_L2_remainder'],
        'P9':data['momentum']['bounds_binary']['nine_momentum_rows_L2_remainder'],
        'zeta':data['force']['bounds_binary']['auxiliary_L2_remainder'],
        'xi':data['force']['bounds_binary']['force_momentum_L2_remainder'],
    }
    columns={k:list(map(decode,v)) for k,v in columns.items()}
    groups={'w':[0],'Q8':list(range(1,9)),'P9':list(range(9,18)),'zeta':[18],'xi':[19]}
    # Dimension factors are conservative even when a parent controls the entire
    # row group's vector norm. They require only the implied per-row bound.
    coefficients=[iv.sqrt(sum((len(groups[k])*v[j]**2 for k,v in columns.items()),iv.mpf(0))) for j in range(9)]
    C=iv.mpf(max(hi(x) for x in coefficients))
    integer=int(mp.ceil(hi(C)))
    Jmod=iv.exp(iv.mpf(4)/13000)*iv.sqrt(1+iv.mpf(4)/13000**2)
    bounds=dict(per_nine_input_sum=C,per_Y20=5*C,
                per_configuration_means=iv.sqrt(2)*C,per_metric_moduli=Jmod*C,
                per_force_mean=C,per_eliminated_mean_vector=iv.sqrt(3)*C,
                per_harmonic_velocity=C)
    checks=exact_controls()
    def zero_complex(v):
        return all(lo(decode(v[k]))==hi(decode(v[k]))==0 for k in ('real','imag'))
    M=data['mixed']
    aq=M['ordinary_to_force_binary']
    fo=M['force_to_ordinary_binary']
    checks.update(all_twenty_rows_accounted_once=sorted(i for v in groups.values() for i in v)==list(range(20)),
                  all_nine_input_columns_preserved=all(len(v)==9 for v in columns.values()),
                  principal_density_row_identically_zero=all(zero_complex(v) for key in ('highest_quartic_matrix_binary','first_mixed_matrix_binary') for v in M[key][0]),
                  reverse_force_coupling_retained=any(not zero_complex(v) for row in fo for v in row),
                  forward_force_coupling_retained=any(not zero_complex(v) for row in aq for v in row),
                  both_force_directions_have_remainder=all(any(hi(x)>0 for x in columns[k]) for k in ('zeta','xi')),
                  density_source_not_removed=any(hi(x)>0 for x in columns['w']),
                  all_global_input_columns_retained=all(hi(coefficients[j])>0 for j in range(4,9)),
                  finite_outward_constants=all(lo(x)>=0 and mp.isfinite(hi(x)) and hi(x)<=integer for x in coefficients),
                  physical_rho_remains_separate=parent['physical_density_principal']=='EXPLICIT_FIRST_AND_SECOND_DERIVATIVES_RETAINED',
                  immutable_sources=all((digest(f),f.stat().st_mtime_ns)==v for f,v in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_INITIAL_TWENTY_ROW_COMPOSITION_V2',
                source_pins=pins,pinned_files=len(pins),input_order=order,
                state_order=['w']+['Q'+str(i) for i in range(8)]+['P'+str(i) for i in range(9)]+['zeta','xi'],
                row_groups=groups,row_owners={k:paths[v] for k,v in [('w','density'),('Q8','gradient'),('P9','momentum'),('zeta','force'),('xi','force')]},
                principal_owner=paths['mixed'],
                principal_equation='Y_t-S*D*Y=-A2(z)*D^2*Y-i*A1(z)*D*Y+R_init',
                component_bound_rows_binary={k:[binary(x) for x in v] for k,v in columns.items()},
                remainder_coefficients_binary=[binary(x) for x in coefficients],
                bounds_binary={k:binary(v) for k,v in bounds.items()},
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                integer_uniform_certificate=integer,
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                domain='INHERITED_SMOOTH_COMPATIBLE_INITIAL_EULER_CONSTRAINT_AUXILIARY_JETS_ONLY',
                bounded_extension='ONLY_TO_NORM_CLOSURE_OF_THIS_INITIAL_DOMAIN',
                scope='CONDITIONAL_INITIAL_TWENTY_ROW_REMAINDER_BOUND',
                full_evolving_generator='OPEN',normal_form_time_derivative='OPEN',
                domain_persistence='OPEN',background_time_tube='OPEN',coupled_energy='OPEN',
                physical_rho_is_state_variable=False,review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args()
    raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw
        print('Byte-identical read-only twenty-row replay')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=False)
        with a.output.open('xb') as f:f.write(raw)
        print('Conditional initial twenty-row composition complete')


if __name__=='__main__':main()
