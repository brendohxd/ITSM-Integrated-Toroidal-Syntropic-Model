"""V2: unchanged Schur/action algebra with exact, high-precision omission control."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as s
import platform

import test_01_r4c1_low_rank_inverse_v1 as first

ev, ROOT, BASE = first.ev, first.ROOT, first.BASE
Checks, CLEAN, ON = first.Checks, first.CLEAN, first.ON
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
ADDENDUM = 'Theory/Gates/RES-001/RES001_R4C1_LOW_RANK_INVERSE_V2_OMISSION_ADDENDUM_2026-10-17.md'
V1_BASE = BASE+'r4c1_low_rank_inverse_attempt_01/'
V1_HASH = 'e6083de8559360d9d42c0445ea8f3bda76524b331a902548d0bdc89c59e5c158'
V1_SUMMARY_HASH = '25016a8308b1681d02d5e1421ec28548a55508b1d8b8a0afa7af3f2d422f6bf3'


def inputs():
    pins, absent, _, generic, prior, time = first.inputs()
    if pins[first.SELF] != V1_HASH:
        raise RuntimeError('V1 scientific source changed')
    previous = ev.READ(V1_BASE+'summary.json')
    pins.update({V1_BASE+'summary.json':V1_SUMMARY_HASH,
                 ADDENDUM:ev.SHA((ROOT/ADDENDUM).read_bytes()),
                 SELF:ev.SHA((ROOT/SELF).read_bytes())})
    pins.update({V1_BASE+n:h for n,h in previous['artifacts'].items()})
    paths = []
    for name,digest in pins.items():
        p = ROOT/name
        if ev.SHA(p.read_bytes()) != digest:
            raise RuntimeError('Frozen input drift: '+name)
        paths.append(p)
        side = Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:
                raise RuntimeError('Sidecar drift: '+name)
            paths.append(side)
        elif name not in absent:
            raise RuntimeError('Required sidecar absent: '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),ev.SHA(p.read_bytes()),
                 p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(set(paths))]
    return pins,absent,snapshot,generic,prior,time


class Derivation(first.Derivation):
    # __init__ and bounds are inherited verbatim from the hash-pinned V1 source.
    def numeric(self,ch,generic,prior,time):
        former = Checks()
        result = super().numeric(former,generic,prior,time)
        for row in former.rows:
            if row['name']=='reject_omitted_extra_inverse':
                result['binary64_extra_inverse_visibility'] = row
            else:
                ch.add(row['name'],row['passed'],row['value'],row['criterion'])
        ell = self.x['ell']
        full = sum((Pj/ell**j for j,Pj in self.inverse_coeff.items()),s.zeros(20))/self.den
        rejected = s.eye(20)-self.U/(ell*self.den)+self.U**2/(ell**2*self.den)
        self.extra_inverse = ON(full-rejected)
        nonzero = [(i,j,str(self.extra_inverse[i,j])) for i in range(20)
                   for j in range(20) if self.extra_inverse[i,j]!=0]
        ch.add('exact_extra_inverse_is_nonzero',bool(nonzero),nonzero,
               'exact symbolic nonzero; no absolute visibility threshold')
        a,H,u,ud,v,vd,r,rd,pd,rho,C = self.bg
        eta = self.eta
        point = {a:1,u:s.sqrt(eta),ud:0,v:0,vd:s.sqrt(eta),
                 r:s.sqrt(eta),rd:s.sqrt(eta)/4,pd:eta/5,
                 rho:s.Rational(1,5),C:1}
        E0 = CLEAN(self.energy.subs(point))
        point[H] = s.sqrt(E0/(3*self.MC))
        controls = []
        with mp.workdps(90):
            def convert(m):
                return mp.matrix([[mp.mpc(str(s.re(q).evalf(95)),
                                         str(s.im(q).evalf(95))) for q in row]
                                  for row in m.tolist()])
            def norm(m):
                return max(sum(abs(m[i,j]) for j in range(m.cols))
                           for i in range(m.rows))
            U = convert(self.U.subs(point))
            for mode in (4,80):
                tf = mp.eye(20)+U/mode
                dense = tf**-1
                declared = convert(full.subs({**point,ell:mode}))
                old_inverse = convert(rejected.subs({**point,ell:mode}))
                expected = convert(self.extra_inverse.subs({**point,ell:mode}))
                delta = dense-old_inverse
                size = norm(expected)
                relative = norm(delta-expected)/size if size else mp.inf
                product = max(norm(tf*declared-mp.eye(20)),
                              norm(declared*tf-mp.eye(20)))
                inverse_error = norm(dense-declared)/(1+norm(dense)+norm(declared))
                row = dict(ell=mode,dps=90,
                    symbolic_correction_absolute=mp.nstr(size,65),
                    independent_inverse_correction_absolute=mp.nstr(norm(delta),65),
                    relative_correction_discrepancy=mp.nstr(relative,65),
                    full_inverse_product_residual=mp.nstr(product,65),
                    dense_inverse_discrepancy=mp.nstr(inverse_error,65))
                controls.append(row)
                ch.add('mp90_extra_inverse_nonzero_'+str(mode),size>0 and norm(delta)>0,
                       row,'strictly nonzero exact and independent high-precision correction')
                ch.add('mp90_extra_inverse_relative_'+str(mode),relative<=mp.mpf('1e-50'),
                       row['relative_correction_discrepancy'],'<=1e-50')
                ch.add('mp90_corrected_inverse_product_'+str(mode),product<=mp.mpf('1e-60'),
                       row['full_inverse_product_residual'],'<=1e-60')
                ch.add('mp90_dense_inverse_binding_'+str(mode),inverse_error<=mp.mpf('1e-60'),
                       row['dense_inverse_discrepancy'],'<=1e-60')
        result['exact_extra_inverse_entries'] = nonzero
        result['high_precision_omission_controls'] = controls
        return result

    def export(self):
        record = super().export()
        if hasattr(self,'extra_inverse'):
            record['matrices']['extra_inverse_over_rejected_cubic'] = first.old.parent.MAT(self.extra_inverse)
        return record


def calculate(emit_case):
    pins,absent,snapshot,generic,prior,time = inputs()
    before = snapshot()
    checks,cases = [],[]
    inherited = Checks()
    inherited.add('V1_derivation_inherited_without_override',
                  Derivation.__init__ is first.Derivation.__init__)
    inherited.add('V1_background_and_energy_bounds_inherited_without_override',
                  Derivation.bounds is first.Derivation.bounds)
    checks.extend(inherited.rows)
    for index,(family,eta) in enumerate(first.CASES):
        ch = Checks()
        der = Derivation(ch,family,eta)
        good = lambda:all(row['passed'] for row in ch.rows)
        numbers = der.numeric(ch,generic,prior,time) if good() else dict(
            skipped='Exact inverse/generator prerequisite failed')
        bounds = der.bounds(ch) if good() else dict(
            skipped='Exact/independent numerical prerequisite failed')
        record = dict(index=index,family=family,eta_exact=str(eta),accepted=good(),
                      checks=ch.rows,bounds=bounds,formulas=der.export(),numerics=numbers)
        emit_case('case_'+str(index).zfill(2)+'.json',ev.ENCODE(record))
        cases.append(dict(index=index,family=family,eta_exact=str(eta),accepted=good(),
            mu_exact=bounds.get('mu_exact'),mu_display=bounds.get('mu_display'),
            action_probes=len(numbers.get('records',[])),
            former_absolute_visibility=numbers.get('binary64_extra_inverse_visibility')))
        for row in ch.rows:
            checks.append(dict(row,name=family+'|'+str(eta)+'|'+row['name']))
        print('CASE_COMPLETE',index,good(),bounds.get('mu_display'),flush=True)
        if not good():
            break
    ch = Checks()
    ch.add('all_nine_exact_cases_present',len(cases)==9,len(cases))
    ch.add('all_756_independent_full_action_probes',
           sum(c['action_probes'] for c in cases)==756,
           sum(c['action_probes'] for c in cases))
    ch.add('source_hash_size_mtime_preserved',before==snapshot())
    checks.extend(ch.rows)
    passed = sum(row['passed'] for row in checks)
    complete = passed==len(checks) and len(cases)==9
    return dict(schema='r4c1-low-rank-inverse-v2',
        validation='PASS_LOCAL_LINEAR_ESTIMATE' if complete else 'FAIL_LOCAL_LINEAR_ESTIMATE',
        status='EXACT_SCHUR_INVERSE_FULL_GENERATOR_WEIGHTED_LINEAR_ESTIMATE' if complete
               else 'INVERSE_OR_WEIGHTED_ESTIMATE_UNRESOLVED',
        passed=passed,total=len(checks),checks=checks,cases=cases,
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),
        inherited_sidecars_absent=absent,claim_status='Conditional',
        weighted_linear_estimate_verified=complete,physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',Rule9_cleared=False,
        canonical_energy_positive=False,physical_window_admitted=False,
        full_nonlinear_fixed_charge_admission=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',
        MAT_001='BLOCKED',UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',
        Stage4A='CLOSED',TOP_X4='UNCHANGED',native_goal_active=True,
        runtime=dict(python=platform.python_version(),numpy=np.__version__,
                     sympy=s.__version__,mpmath=mp.__version__),
        V1_receipt_preserved_as_failed=True,
        review_dependencies=['THREE-FAMILY-FINITE-K-V3','WEIGHTED-CUBIC-REJECTION-V1',
            'CUSP3-EVOLUTION-V1','THREE-FAMILY-FIXED-CHARGE-KINETIC-V3',
            'GENERIC-KERNEL/EVOLVING-REDUCTION','LOW-RANK-INVERSE-V1','all transitive debt'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_low_rank_inverse_attempt_02')
    ap.add_argument('--replay')
    args = ap.parse_args()
    dest = (ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():
            raise FileNotFoundError('Replay absent')
        before = [(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                  for p in sorted(dest.iterdir())]
    elif dest.exists():
        raise FileExistsError('Refuse overwrite of existing evidence')
    else:
        dest.mkdir(parents=True)
    artifacts = {}
    def emit(name,body):
        digest = ev.SHA(body)
        side = (digest+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:
                raise RuntimeError('Read-only replay drift: '+name)
        else:
            with (dest/name).open('xb') as f:
                f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:
                f.write(side)
        artifacts[name] = digest
    try:
        summary = calculate(emit)
        summary['artifacts'] = dict(artifacts)
        emit('summary.json',ev.ENCODE(summary))
    except BaseException as exc:
        if not args.replay:
            emit('interrupted.json',ev.ENCODE(dict(validation='INTERRUPTED_NO_ACCEPTED_ESTIMATE',
                error_type=type(exc).__name__,error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        after = [(p.name,ev.SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                 for p in sorted(dest.iterdir())]
        if before!=after:
            raise RuntimeError('Replay changed artifact metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:summary[k] for k in
        ('validation','passed','total','status','physics_pass')}),flush=True)
    for row in summary['checks']:
        if not row['passed']:
            print(json.dumps(row),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':
    raise SystemExit(main())
