"""Additive wave-zero controls for the unchanged continuous lower-tail proof."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import math
import sympy as s
import test_01_r4c1_cusp_odd_response_tail_v1 as parent

ROOT,BASE,SHA,READ,ENCODE=parent.ROOT,parent.BASE,parent.SHA,parent.READ,parent.ENCODE
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PREV=BASE+'r4c1_cusp_odd_response_tail_attempt_01/'


def calculate():
    proof=READ(PREV+'summary.json')
    pins=dict(proof['source_sha256'])
    pins.update({PREV+n:h for n,h in proof['artifacts'].items()})
    pins.update({PREV+'summary.json':'c908e715864be379d28445c3f5e32d173d23986b5db291c79eb1836dc94ed602',
                 SELF:SHA((ROOT/SELF).read_bytes())})
    paths=[];absent=proof['inherited_sidecars_absent']
    for name,digest in pins.items():
        p=ROOT/name
        if SHA(p.read_bytes())!=digest:raise RuntimeError('Source drift '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise RuntimeError('Sidecar drift '+name)
            paths.append(side)
        elif name not in absent:raise RuntimeError('Required sidecar absent '+name)
    snapshot=lambda:[(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                     for p in sorted(set(paths))]
    before=snapshot();ch=parent.Checks()
    f=READ(PREV+'formulas.json');runs=READ(parent.PARENT+'trajectories.json')['runs']
    cv={(q['family'],q['eta_exact']):float(s.Rational(q['cV2'])) for q in f['families']}
    P=float(s.Rational(f['Duhamel_scaled_constant']))
    ch.add('parent_proof_local_controls_complete',proof['passed']==proof['total']==199)
    ch.add('all18_root_cases',len(runs)==18,len(runs))
    records=[]
    for i,q in enumerate(runs):
        ch.add(str(i)+'_root_in_registered_time',0<=q['root']<=.05,q['root'])
        lam=cv[(q['family'],q['eta_exact'])]
        for j,n in enumerate((1,3)):
            # a>=1, hence this uses an upper position weight without interpolating a.
            z=q['root_state_scaled']
            upper=math.hypot(z[2*j+1],math.sqrt(lam*(40*n)**2+1)*z[2*j])
            cn=-4*(-1)**((n-1)//2)/(math.pi*n*(n*n-4))
            bound=P*abs(cn)
            excess=max(0.,upper-bound)/(1+upper+bound)
            ch.add(str(i)+'_root_mode_'+str(n),excess<=1e-9,excess,'<=1e-9')
            records.append(dict(family=q['family'],eta=q['eta_exact'],method=q['method'],
                root=q['root'],mode=n,energy_norm_upper=upper,proved_bound=bound,excess=excess))
    ch.add('all36_root_mode_controls',len(records)==36,len(records))
    ch.add('source_hash_size_mtime_preserved',before==snapshot())
    passed=sum(row['passed'] for row in ch.rows)
    complete=passed==len(ch.rows)
    verification=ENCODE(dict(checks=ch.rows,records=records,passed=passed,total=len(ch.rows),
        root_position_weight='a=1 is conservative because continuous background proves a>=1',
        new_integrations=False,interpolation_used=False))
    summary=dict(schema='r4c1-cusp-odd-response-root-audit-v1',
        validation='PASS_LOCAL_ROOT_CONTROL' if complete else 'FAIL_LOCAL_ROOT_CONTROL',
        passed=passed,total=len(ch.rows),checks=ch.rows,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',Rule9_cleared=False,parent_proof_unchanged=True,
        full_coupled_tail_bound=False,stage2_complete=False,stage3_entered=False,
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,artifacts={'verification.json':SHA(verification)})
    return {'verification.json':verification,'summary.json':ENCODE(summary)},summary


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    dest=ROOT/(BASE+'r4c1_cusp_odd_response_root_audit_attempt_01')
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('No overwrite')
    else:dest.mkdir(parents=True)
    bodies,summary=calculate()
    for name,body in bodies.items():
        side=(SHA(body)+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:raise RuntimeError('Replay drift '+name)
        else:
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write(side)
    if args.replay:
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay metadata changed')
        print('READ_ONLY_REPLAY_EXACT')
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','physics_pass')}))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
