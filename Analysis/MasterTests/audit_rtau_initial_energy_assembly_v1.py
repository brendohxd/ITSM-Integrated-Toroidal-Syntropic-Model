"""Independent exact arithmetic audit of the initial forced energy bound."""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
BASE='Analysis/MasterTests/outputs/'
SOURCE=BASE+'rtau_initial_energy_assembly_v1_20261114/receipt.json'


def exact(t):
    s,n,e,b=t
    assert n>=0 and (n.bit_length()==b or n==b==0)
    return (-1 if s else 1)*F(n)*F(2)**e


def calculate():
    p=ROOT/SOURCE;raw=p.read_bytes();d=json.loads(raw)
    read=lambda n:json.loads((ROOT/BASE/n/'receipt.json').read_bytes())
    periodic=read('rtau_periodic_principal_composition_v2_20261104')
    gauge=read('rtau_gauge_mean_trace_rate_v2_20261109')
    weak=read('rtau_weak_canonical_rate_v2_20261103')
    lift=read('rtau_momentum_rate_lift_v2_20261104')
    ordinary=read('rtau_ordinary_ward_energy_v4_20261104')
    energy=read('rtau_energy_time_drift_v2_20261114')
    shift=read('rtau_physical_density_remainder_v2_20261114')
    adv=read('rtau_physical_advection_composition_v1_20261114')
    time=read('rtau_normal_form_time_drift_v1_20261114')
    upper=lambda pair:exact(pair[1]);lower=lambda pair:exact(pair[0])
    hi=lambda key:upper(d['bounds_binary'][key])
    term=lambda key:upper(d['contribution_bounds_binary'][key])
    PV=periodic['values_binary'];gb=gauge['bounds_binary']
    qw=weak['coefficients_binary']['field_rate_L2']
    Lq=lift['constants_binary']['full_configuration_H1']
    Lp=lift['constants_binary']['full_momentum_L2']
    qbounds=[]
    for j in range(9):
        q=upper(Lq[j]) if j<8 else F(0)
        pp=upper(Lp[j]) if j<8 else F(0)
        rhs=upper(qw[0])*pp+upper(qw[1])*q+upper(qw[3])*upper(gb['corrective_shift_H1'][j])
        qbounds.append(upper(d['configuration_and_clock_mean_rate_binary'][j])>=rhs)
    partner=[]
    for j in range(9):
        squared=upper(d['configuration_and_clock_mean_rate_binary'][j])**2+upper(gb['metric_modulus_rate_vector'][j])**2
        squared+=sum(upper(gb['eliminated_momentum_mean_'+k+'_rate'][j])**2 for k in ('x','y','z'))
        partner.append(upper(d['global_partner_rate_binary'][j])**2>=squared)
    H0=hi('diagonal_energy');bz=hi('input_state_weight');bg=hi('input_global_weight')
    L=hi('global_partner_rate_per_U');source=hi('source_energy_cross');alpha=lower(d['bounds_binary']['diagonal_coercivity'])
    minimum=min(lower(ordinary['ordinary_norm_constants']['energy_lower_binary']),*(lower(row[0]) for row in energy['fast_energy_value_time_binary']))
    mp.mp.dps,mp.iv.dps=100,80
    iv=mp.iv;r=iv.mpf(1)/13000
    jmod=iv.exp(4*r)*iv.sqrt(1+4*r*r)
    norm_g=exact(jmod._mpi_[1])
    exp8=exact(iv.exp(8*r)._mpi_[1])
    z,g,h,a,b,c=sp.symbols('z g h a b c',real=True)
    difference=(a+b)*z*z+(a+c)*g*g+(b+c)*h*h-2*a*z*g-2*b*z*h-2*c*g*h
    checks=dict(exact_canonical_mean_rate_aggregation=all(qbounds),
                exact_global_partner_rate_norm=all(partner),
                exact_uniform_partner_rate=L>=max(upper(x) for x in d['global_partner_rate_binary']),
                positive_inherited_energy_coercivity=F(0)<alpha<=minimum,
                actual_energy_time_counted_once=term('energy_time')>=upper(energy['bounds_binary']['diagonal_energy_time']),
                exact_spatial_adjoint_aggregation=term('principal_spatial_adjoint')>=upper(PV['ordinary_spatial_energy_adjoint_bound'])+upper(PV['fast_spatial_energy_adjoint_bound']),
                exact_advection_energy_aggregation=term('physical_advection')>=upper(shift['coefficient_bounds_binary']['Sz'])*H0+upper(shift['coefficient_bounds_binary']['S'])*hi('diagonal_energy_spatial_derivative'),
                exact_bounded_transformation_aggregation=term('bounded_normal_form_terms')>=2*H0*(upper(PV['periodic_composition_remainder_bound'])+upper(adv['bounds_binary']['additional_transformed_advection'])+upper(time['bounds_binary']['T_time_times_inverse'])),
                exact_actual_remainder_aggregation=source>=H0*hi('normal_form')*hi('source_remainder_per_U') and term('actual_remainder_state')>=2*source*bz,
                exact_cross_term_aggregation=term('state_global_cross')>=source*bg+L*bz and term('state_harmonic_cross')>=source and term('global_self')>=2*L*bg and term('global_harmonic_cross')>=L,
                exact_Young_identity=sp.expand(difference-a*(z-g)**2-b*(z-h)**2-c*(g-h)**2)==0,
                exact_state_coefficient=hi('state_squared_coefficient')>=sum(term(k) for k in ('energy_time','principal_spatial_adjoint','physical_advection','bounded_normal_form_terms','actual_remainder_state','state_global_cross','state_harmonic_cross')),
                exact_global_and_forcing_coefficients=hi('global_squared_coefficient')>=term('global_self')+term('state_global_cross')+term('global_harmonic_cross') and hi('harmonic_squared_coefficient')>=term('state_harmonic_cross')+term('global_harmonic_cross'),
                exact_energy_coefficient=hi('augmented_energy_coefficient')>=max(hi('state_squared_coefficient')/alpha,hi('global_squared_coefficient')),
                norm_global_weight_has_independent_high_precision_control=bg*bg>=6+norm_g*norm_g,
                exact_input_norm_equivalence=hi('U0_squared_per_energy')>=bz*bz/alpha+bg*bg and hi('energy_per_U0_squared')>=H0*hi('normal_form')**2+exp8,
                forcing_not_removed_and_time_claims_held=hi('harmonic_squared_coefficient')>0 and d['harmonic_rate_law']=='NOT_SPECIFIED_BY_SPATIAL_GAUGE_EQUATIONS' and d['closed_autonomous_physical_evolution']=='OPEN' and d['background_time_tube']=='OPEN' and d['physics_pass'] is False)
    assert all(checks.values()),checks
    assert p.read_bytes()==raw
    return dict(kind='RTAU_INITIAL_ENERGY_EXACT_AUDIT_V1',receipt=SOURCE,
                receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Exact initial forced-energy audit replay')
    else:
        with a.output.open('xb') as f:f.write(raw)
        print('Exact initial energy aggregation and coercivity audit passed')


if __name__=='__main__':main()
