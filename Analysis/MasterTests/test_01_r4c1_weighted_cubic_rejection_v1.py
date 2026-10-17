"""Preserve the first failed cubic-inverse prerequisite; no weighted bound."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s
import test_01_r4c1_three_family_weighted_evolution_v4 as old

ev=old.ev;ROOT=old.ROOT;BASE=old.BASE
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
FROZEN='b33fdfd1907ec42c34119d855b58b3eb41c5fc4f164ac6b21c96c93e1a72d0c7'


def calculate():
    source='Analysis/MasterTests/test_01_r4c1_three_family_weighted_evolution_v4.py'
    if ev.SHA((ROOT/source).read_bytes())!=FROZEN:raise RuntimeError('V4 drift')
    pins,absent,snapshot,*_=old.inputs();before=snapshot()
    pins.update({SELF:ev.SHA((ROOT/SELF).read_bytes())})
    side=Path(str(ROOT/SELF)+'.sha256')
    if side.read_text().split()[0]!=pins[SELF]:raise RuntimeError('Canary sidecar mismatch')
    own_before=[(str(p),ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in (ROOT/SELF,side)]
    checks=old.Checks();der=old.Derivation(checks,'archived_G3',s.Rational(1,4))
    failed=[r for r in checks.rows if not r['passed']]
    if len(checks.rows)!=38 or len(failed)!=1 or failed[0]['name']!='generic_fast_cubic_inverse_identity':
        raise RuntimeError('Unexpected first-case disposition; do not accept stale diagnosis')
    residual=old.ON(der.U**3-der.g*der.U)
    run=next(r for r in ev.READ(old.parent.PARENT+'trajectories.json')['runs'] if r['family']=='archived_G3' and r['eta_exact']=='1/4')
    b=np.asarray(run['first_order_states'][0][:12],float)
    names=('a','H','u0','u_dot','v0','v_dot','r0','r_dot','psi_dot','rho','C')
    values=[*b[:8],b[9],b[10],np.exp(float(der.x['beta'])*b[8])]
    point={der.x[n]:val for n,val in zip(names,values)}
    U=np.asarray(der.U.subs(point),complex);g=float(der.g.subs(point));witnesses=[]
    for ell in (4,80):
        den=1-g/ell**2
        assumed=np.eye(20)-U/(ell*den)+U@U/(ell**2*den)
        error=float(np.linalg.norm((np.eye(20)+U/ell)@assumed-np.eye(20),np.inf))
        if not error>1e-12:raise RuntimeError('Missing independent inverse rejection witness')
        witnesses.append(dict(ell=ell,absolute_matrix_inverse_residual=error,criterion='>1e-12; rejection, not acceptance'))
    own_after=[(str(p),ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in (ROOT/SELF,side)]
    if before!=snapshot() or own_before!=own_after:raise RuntimeError('Source metadata changed')
    verification=dict(checks=checks.rows,passed=37,total=38,validation='FAIL_LOCAL_ESTIMATE',
        rejected_prerequisite='U^3=g*U is false in the complete drifting chart',
        independent_inverse_rejection_witnesses=witnesses,source_metadata_preserved=True)
    bodies={'verification.json':ev.ENCODE(verification),'formulas.json':ev.ENCODE(der.export()),
        'cubic_residual.json':ev.ENCODE(old.parent.MAT(residual))}
    summary=dict(schema='r4c1-weighted-cubic-rejection-v1',status='CUBIC_INVERSE_CANDIDATE_REJECTED_WEIGHTED_BOUND_OPEN',
        validation='FAIL_LOCAL_ESTIMATE',passed=37,total=38,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',Rule9_cleared=False,weighted_linear_estimate_verified=False,
        remaining_eight_cases_not_computed=True,no_action_rejection=True,native_goal_resumed=False,
        checks=checks.rows,source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,
        source_metadata_preserved=len(before)+2,artifacts={n:ev.SHA(b) for n,b in bodies.items()},
        review_dependencies=['THREE-FAMILY-FINITE-K-V3','CUSP3-EVOLUTION-V1','all inherited deferred debt'])
    bodies['summary.json']=ev.ENCODE(summary)
    return bodies,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay',action='store_true');args=parser.parse_args()
    dest=ROOT/(BASE+'r4c1_weighted_cubic_rejection_attempt_01')
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse overwrite')
    else:dest.mkdir(parents=True)
    bodies,summary=calculate()
    if args.replay:
        for n,b in bodies.items():
            if (dest/n).read_bytes()!=b or (dest/(n+'.sha256')).read_bytes()!=(ev.SHA(b)+'  '+n+'\n').encode():raise RuntimeError('Failed-receipt replay drift '+n)
        after=[(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise RuntimeError('Replay metadata drift')
        print('READ_ONLY_FAILED_RECEIPT_REPLAY_EXACT',flush=True)
    else:
        for n,b in bodies.items():
            with (dest/n).open('xb') as f:f.write(b)
            with (dest/(n+'.sha256')).open('xb') as f:f.write((ev.SHA(b)+'  '+n+'\n').encode())
    print(json.dumps({n:summary[n] for n in ('validation','passed','total','status','physics_pass')}),flush=True)
    return 1  # Reproducing the expected failure does not turn it into a pass.


if __name__=='__main__':raise SystemExit(main())
