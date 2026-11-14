"""Exact rational audit of the certified physical-advection norm bounds."""
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SOURCE='Analysis/MasterTests/outputs/rtau_physical_advection_composition_v1_20261114/receipt.json'


def exact(t):
    s,n,e,b=t
    assert n>=0 and (n.bit_length()==b or n==b==0)
    return (-1 if s else 1)*Fraction(n)*Fraction(2)**e


def calculate():
    p=ROOT/SOURCE;raw=p.read_bytes();d=json.loads(raw)
    hi=lambda key:exact(d['bounds_binary'][key][1])
    v,c,vz,cz=map(hi,['physical_shift','normal_form_C','physical_shift_z','normal_form_C_z'])
    terms=d['contribution_bounds_binary']
    sufficient=2*v*c+v*cz+vz*c
    checks=dict(exact_commutator_rounding=hi('advection_commutator')>=sufficient,
                exact_inverse_composition_rounding=hi('additional_transformed_advection')>=hi('advection_commutator')*hi('normal_form_inverse'),
                exact_report_commutator_certificate=hi('advection_commutator')<Fraction(4641,10**6),
                exact_report_transformed_certificate=hi('additional_transformed_advection')<Fraction(11657,10**6),
                three_contributions_accounted=hi('advection_commutator')>=sum(exact(x[1]) for x in terms.values()),
                moving_evolution_holds_retained=d['normal_form_time_derivative']=='OPEN'
                  and d['energy_time_derivative']=='OPEN' and d['background_time_tube']=='OPEN'
                  and d['domain_persistence']=='OPEN' and d['physics_pass'] is False)
    assert all(checks.values()),checks
    assert p.read_bytes()==raw
    return dict(kind='RTAU_PHYSICAL_ADVECTION_EXACT_AUDIT_V1',receipt=SOURCE,
                receipt_sha256=hashlib.sha256(raw).hexdigest(),
                checks=[dict(name=k,passed=v) for k,v in checks.items()],
                review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path);g.add_argument('--replay',type=Path)
    a=p.parse_args();raw=(json.dumps(calculate(),indent=2)+'\n').encode()
    if a.replay:
        assert a.replay.read_bytes()==raw;print('Exact physical-advection audit replay')
    else:
        with a.output.open('xb') as f:f.write(raw)
        print('Exact rational physical-advection audit passed')


if __name__=='__main__':main()
