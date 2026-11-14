"""Exact initial twenty-direction state map and density-row norm comparison."""

import argparse,json
from pathlib import Path
import mpmath as mp
import sympy as sp
from test_rtau_nonlocal_trace_drift_v1 import ROOT,GATE,OUT,digest,read

CONTRACT=GATE+'RES001_RTAU_DENSITY_STATE_MAP_V1_CONTRACT_2026-11-14.md'
PARENT=OUT+'rtau_trace_source_composition_v1_20261114/receipt.json'
MIXED=OUT+'rtau_mixed_principal_assembly_v1_20261104/receipt.json'
PERIODIC=OUT+'rtau_periodic_principal_composition_v2_20261104/receipt.json'
DENSITY=OUT+'rtau_actual_corrected_density_v4_20261105/receipt.json'
SLOTS=[0,1,3,6,7,8,9,10,11]


def calculate():
    mp.mp.dps,mp.iv.dps=100,60
    iv=mp.iv
    lo=lambda x:mp.mpf(iv.mpf(x)._mpi_[0])
    hi=lambda x:mp.mpf(iv.mpf(x)._mpi_[1])
    decode=lambda x:iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary=lambda x:[list(v) for v in iv.mpf(x)._mpi_]
    pins=dict(read(PARENT)['source_pins'])
    for rel in (CONTRACT,PARENT,MIXED,PERIODIC,DENSITY):
        p=ROOT/rel
        h=Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel]==h,rel
        pins[rel]=h
    snap={}
    for rel,h in pins.items():
        p=ROOT/rel
        assert digest(p)==h,rel
        for f in (p,Path(str(p)+'.sha256')):
            if f.exists():snap[f]=(digest(f),f.stat().st_mtime_ns)
    data=[read(p) for p in (MIXED,PERIODIC,DENSITY)]
    assert all(c['passed'] for d in data for c in d['checks'])
    mixed,periodic,density=data
    E=sp.zeros(9,8)
    E[0,0],E[2,0],E[1,1]=1,-1,1
    for j in range(2,8):E[j+1,j]=1
    R=(E.T*E).inv()*E.T
    trace=sp.Matrix([1,0,1,0,0,0,0,0,0])
    tr=trace.T/2
    def zero_complex(v):
        return all(lo(decode(v[k]))==hi(decode(v[k]))==0 for k in ('real','imag'))
    S=mixed['cross_normal_form_matrix_binary']
    A=mixed['highest_quartic_matrix_binary']
    B=mixed['first_mixed_matrix_binary']
    density_zero=all(zero_complex(v) for matrix in (A,B,S) for v in matrix[0])
    # Exact periodic recovery, including the original constant mode.
    z=sp.symbols('z',real=True)
    phi=3+sp.exp(sp.I*z)+2*sp.exp(-2*sp.I*z)
    Q=-sp.I*sp.diff(phi,z)
    primitive=sp.integrate(Q,z)
    primitive-=sp.integrate(primitive,(z,0,2*sp.pi))/(2*sp.pi)
    recovered=3+sp.I*primitive
    Cw=iv.mpf(max(hi(decode(v)) for v in density['bounds_binary']['initial_original_coordinate_density_source_L2']))
    Tinv=decode(periodic['values_binary']['global_T_inverse_norm'])
    r=iv.mpf(1)/13000
    Jmod=iv.exp(4*r)*iv.sqrt(1+4*r*r)
    bounds=dict(source_per_nine_input_sum=Cw,
                ordinary_free_configuration_per_Q8=iv.mpf(2),
                ordinary_free_configuration_per_mean=iv.sqrt(2),
                metric_modulus_H1_weight=Jmod,
                material_density_row_per_Y20=5*Cw,
                material_density_row_per_normal_form_state=5*Cw*Tinv,
                material_density_row_per_configuration_means=iv.sqrt(2)*Cw,
                material_density_row_per_metric_moduli=Jmod*Cw,
                material_density_row_per_force_mean=Cw,
                material_density_row_per_eliminated_mean_vector=iv.sqrt(3)*Cw,
                material_density_row_per_harmonic_velocity=Cw)
    checks=dict(exact_eight_configuration_complement=R*E==sp.eye(8),
                exact_trace_complement_zero=R*trace==sp.zeros(8,1),
                exact_nine_configuration_decomposition=E*R+trace*tr==sp.eye(9),
                all_twenty_state_directions_retained=1+E.cols+len(SLOTS)+2==20,
                stored_material_density_and_normal_form_rows_zero=density_zero,
                exact_original_mean_retained=sp.simplify(sp.integrate(Q,(z,0,2*sp.pi)))==0 and sp.simplify(phi-recovered)==0,
                all_partners_have_positive_finite_bounds=all(lo(v)>0 and mp.isfinite(hi(v)) for v in bounds.values()),
                original_sources_and_sidecars_preserved=all((digest(p),p.stat().st_mtime_ns)==v for p,v in snap.items()))
    assert all(checks.values()),checks
    return dict(kind='RTAU_DENSITY_STATE_MAP_V1',source_sha256=digest(Path(__file__)),source_pins=pins,pinned_sources=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                canonical_ordinary_slots=SLOTS,state_order=['w']+['Q'+str(i) for i in range(8)]+['P'+str(i) for i in SLOTS]+['zeta','xi'],
                finite_partner_groups=['original_mean_phi_8','metric_modulus_3','force_mean_1','eliminated_momentum_mean_3','harmonic_velocity_3'],
                bounds_binary={k:binary(v) for k,v in bounds.items()},upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items()},
                scope='CONDITIONAL_INITIAL_CORRECTED_DENSITY_ROW_STATE_COMPARISON',physical_rho_total_remainder='OPEN',
                remaining_generator_rows='OPEN',coupled_evolution='OPEN',review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path)
    group.add_argument('--replay',type=Path)
    args=parser.parse_args()
    payload=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if args.replay:
        assert args.replay.read_bytes()==payload
        print('Byte-identical read-only replay')
    else:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f:f.write(payload)
        print('Initial density state-map controls complete')


if __name__=='__main__':main()
