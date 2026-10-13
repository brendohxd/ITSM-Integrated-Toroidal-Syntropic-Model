"""V2 fixes assumption-qualified charpoly generator comparison; v1 retained."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s
import test_01_r4c1_g3n5_nonzero_principal_v1 as v1

ROOT=v1.ROOT
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
V1_SHA='09b3ad3fa6045fbbc283f46d479565adf9f2497748793e6102896698281f28eb'
if hashlib.sha256((ROOT/v1.SELF).read_bytes()).hexdigest()!=V1_SHA:
    raise RuntimeError('Frozen independent v1 drift')
derive=v1.derive


def calculate():
    data,summary=v1.calculate()  # in-memory only; never call its writing main
    d=derive()
    changes={
        'companion_characteristic_factor':(d['companion'],lambda x:x*x*(x*x-s.Rational(1,3))),
        'matter_characteristic_factor':(d['Gmatter'],lambda x:(x-1)**2*(x-1-(d['u']**2+d['v']**2)/13)),
    }
    for row in summary['checks']:
        if row['name'] in changes:
            mat,target=changes[row['name']]
            poly=mat.charpoly()
            # charpoly's formal generator is authoritative; same printed name
            # with different assumptions does not make two Symbols equal.
            residual=s.factor(poly.as_expr()-target(poly.gen))
            row.update(passed=residual==0,value=[] if residual==0 else [str(residual)])
    summary.update(schema='r4c1-g3n5-nonzero-principal-v2',
                   source_sha256={v1.SELF:V1_SHA,SELF:hashlib.sha256((ROOT/SELF).read_bytes()).hexdigest()},
                   preserved_v1_failure={'validation':'FAIL_LOCAL_CHECKS','passed':7,'total':9,
                       'checks':list(changes),'cause':'Distinct assumption-qualified Symbols used in charpoly assertions; density derivation unchanged'})
    summary['passed']=sum(r['passed'] for r in summary['checks'])
    summary['validation']='PASS_LOCAL_CHECKS' if summary['passed']==summary['total'] else 'FAIL_LOCAL_CHECKS'
    data['summary.json']=v1.encode(summary)
    return data,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=v1.BASE+'r4c1_g3n5_nonzero_principal_attempt_02')
    ap.add_argument('--replay')
    a=ap.parse_args();dest=(ROOT/(a.replay or a.output)).resolve();dest.relative_to((ROOT/v1.BASE).resolve())
    if not a.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if a.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    data,summary=calculate()
    if a.replay:
        for name,body in data.items():
            assert (dest/name).read_bytes()==body
            assert (dest/(name+'.sha256')).read_bytes()==(hashlib.sha256(body).hexdigest()+'  '+name+'\n').encode()
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in data.items():
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((hashlib.sha256(body).hexdigest()+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if a.replay else 'NEW_RECEIPTS_WRITTEN',**{k:summary[k] for k in ('passed','total','validation','status','physics_pass','gate_effect')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
