"""Exact rational audit of the initial twenty-row bound and row retention."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RECEIPT='Analysis/MasterTests/outputs/rtau_initial_twenty_row_composition_v3_20261114/receipt.json'
KEYS={'w':'initial_original_coordinate_density_source_L2',
      'Q8':'eight_gradient_rows_L2_remainder',
      'P9':'nine_momentum_rows_L2_remainder',
      'zeta':'auxiliary_L2_remainder','xi':'force_momentum_L2_remainder'}


def exact(v):
    sign,man,exp,bc=v
    assert man>=0 and (man.bit_length()==bc or man==bc==0)
    return (-1 if sign else 1)*Fraction(man)*Fraction(2)**exp


def calculate():
    path=ROOT/RECEIPT;raw=path.read_bytes();d=json.loads(raw)
    groups=d['row_groups'];rows=d['component_bound_rows_binary']
    parent_rows_match=True
    for k,owner in d['row_owners'].items():
        parent=json.loads((ROOT/owner).read_bytes())
        parent_rows_match &= rows[k]==parent['bounds_binary'][KEYS[k]]
    qs=[]
    for j in range(9):
        squared=sum((len(groups[k])*exact(v[j][1])**2 for k,v in rows.items()),Fraction(0))
        upper=exact(d['remainder_coefficients_binary'][j][1])
        qs.append(squared<=upper**2<=d['integer_uniform_certificate']**2)
    coverage=[sum(i in idx for idx in groups.values()) for i in range(20)]
    # Every deleted coordinate, including either inherited zero-speed direction,
    # destroys identity coverage; no spectral claim is inferred from this test.
    deletion_checks=all([int(i!=omit) for i in range(20)]!=coverage for omit in range(20))
    ward_path='Analysis/MasterTests/outputs/rtau_ordinary_ward_energy_v4_20261104/receipt.json'
    ward=json.loads((ROOT/ward_path).read_bytes())
    zero_checks={c['name']:c['passed'] for c in ward['checks']}
    checks=dict(row_bounds_match_action_derived_parent_receipts=parent_rows_match,
                exact_rational_squared_aggregation=all(qs),
                twenty_rows_have_identity_coverage=coverage==[1]*20,
                deleting_any_coordinate_is_detected=deletion_checks,
                inherited_zero_chart_evidence_preserved=zero_checks['exact_zero_direction_not_removed']
                   and zero_checks['full_18_direction_zero_complement_chart_inverse_exact']
                   and d['source_pins'].get(ward_path)==hashlib.sha256((ROOT/ward_path).read_bytes()).hexdigest(),
                original_global_partners_retained=all(exact(v[1])>0 for k,v in d['bounds_binary'].items() if k.startswith('per_') and k not in ('per_Y20','per_nine_input_sum')),
                no_instantaneous_to_time_tube_promotion=d['background_time_tube']=='OPEN'
                   and d['coupled_energy']=='OPEN' and d['domain_persistence']=='OPEN'
                   and d['normal_form_time_derivative']=='OPEN' and d['physics_pass'] is False)
    assert all(checks.values()),checks
    assert path.read_bytes()==raw
    return dict(kind='RTAU_INITIAL_TWENTY_ROW_EXACT_AUDIT_V1',receipt=RECEIPT,
                receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Exact twenty-row audit replay')
    else:
        with a.output.open('xb') as f:f.write(raw)
        print('Exact rational and row-retention audit passed')


if __name__=='__main__':main()
