"""V2 full cusp tail: retain failed V1; conjugate the complex Schur map."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import platform
import sys
import traceback
import numpy as np
import sympy as s
import test_01_r4c1_cusp3_coupled_tail_v1 as first

ROOT,BASE=first.ROOT,first.BASE
READ,ENCODE,SHA,CLEAN,MAT=first.READ,first.ENCODE,first.SHA,first.CLEAN,first.MAT
FIELDS,IX,K=first.FIELDS,first.IX,first.K
Checks=first.Checks
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_CUSP3_COUPLED_TAIL_V2_CONJUGATION_ADDENDUM_2026-10-17.md'
FAILED=BASE+'r4c1_cusp3_coupled_tail_attempt_01/'


def inputs():
    pins,absent,_,=first.inputs()
    old=READ(FAILED+'summary.json')
    pins.update({FAILED+'summary.json':'cf7c7ecfb63ddf738833b7392b57074edf40c5047b30710c10d134063619692a',
                 **{FAILED+n:h for n,h in old['artifacts'].items()},
                 ADDENDUM:SHA((ROOT/ADDENDUM).read_bytes()),
                 SELF:SHA((ROOT/SELF).read_bytes())})
    paths=[]
    for name,digest in sorted(pins.items()):
        p=ROOT/name
        if SHA(p.read_bytes())!=digest:raise ValueError('V2 frozen input drift '+name)
        paths.append(p);side=Path(str(p)+'.sha256')
        if side.exists():
            if side.read_text().split()[0].lower()!=digest:raise ValueError('V2 sidecar drift '+name)
            paths.append(side)
        elif name not in absent:raise ValueError('V2 missing sidecar '+name)
    def snapshot():
        return [(p.relative_to(ROOT).as_posix(),SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)
                for p in sorted(set(paths))]
    return pins,absent,snapshot


class Case(first.Case):
    def reduction(self,mean):
        first.progress(stage='ACTION_REDUCTION_V2',index=self.index,mean=mean)
        ell=self.ell;H=self.H;a=self.a;p=self.fixed
        replace={ell:0} if mean else {ell:K*self.m}
        LA,LB,LK,EA,EB,ED=[M.subs(replace) for M in
                           (self.LA,self.LB,self.LK,self.EA,self.EB,self.ED)]
        dyn=FIELDS[4:10] if mean else ('Mxx','Mxy','Myy')
        dyn=(*dyn,*FIELDS[10:17]);aux=('Z',) if mean else ('Sx','Sy','Sz','Z')
        F=s.zeros(22,len(dyn));U=s.zeros(22,len(aux))
        for j,n in enumerate(dyn):F[IX[n],j]=1
        F[0,dyn.index('Pi')]=-p['beta']
        for j,n in enumerate(aux):U[IX[n],j]=1
        MT=p['MP2']-p['MU2']*(p['c1']+p['c3'])
        cL=p['MU2']*(p['c1']+p['c2']+p['c3'])
        inv=s.Matrix([[1/p['b']]]) if mean else s.diag(
            2*a*a/(MT*(K*self.m)**2),2*a*a/(MT*(K*self.m)**2),
            -a*a/(cL*(K*self.m)**2),1/p['b'])
        invd=self.dtm(inv)
        Y=U.conjugate().T*LA*F;VV=U.conjugate().T*LB*F
        Q0=(F-U*inv*Y).applyfunc(CLEAN);Q1=(-U*inv*VV).applyfunc(CLEAN)
        Q0d=self.dtm(Q0);Q1d=self.dtm(Q1)
        kin=(F.conjugate().T*LK*F-VV.conjugate().T*inv*VV).applyfunc(CLEAN)
        tag='mean' if mean else 'nonzero'
        self.ch.exact_matrix(tag+'_regular_auxiliary_inverse',
                             U.conjugate().T*LA*U*inv-s.eye(len(aux)))
        self.ch.exact_matrix(tag+'_kinetic_Hermiticity',kin-kin.conjugate().T)
        if not mean:
            defect=(VV.conjugate().T*inv*VV-VV.T*inv*VV).applyfunc(CLEAN)
            self.ch.add('reject_wrong_complex_transpose',any(q!=0 for q in defect),
                        MAT(defect))
        self.ch.add(tag+'_kinetic_is_constant',not kin.free_symbols,sorted(map(str,kin.free_symbols)))
        if kin.free_symbols:raise ValueError('Unexpected nonconstant kinetic inverse')
        ki=kin.inv()
        self.ch.exact_matrix(tag+'_full_kinetic_inverse',kin*ki-s.eye(len(dyn)))
        src=self.source.subs(self.m,0) if mean else self.source
        ai=[IX[n] for n in aux];di=[23+first.ev.AUX.index(n) for n in aux]
        us=(-U*inv*src[ai,:]).applyfunc(CLEAN)
        usd=(-U*(invd*src[ai,:]+inv*src[di,:])).applyfunc(CLEAN)
        acc=(ki*F.conjugate().T*(src[:22,:]+EA*us+EB*usd)).applyfunc(CLEAN)
        AA=(ki*F.conjugate().T*(EA*Q0+EB*Q0d)).applyfunc(CLEAN)
        BB=(ki*F.conjugate().T*(EA*Q1+EB*(Q0+Q1d))).applyfunc(CLEAN)
        n=len(dyn);G=s.zeros(2*n);G[:n,n:]=s.eye(n);G[n:,:n]=AA;G[n:,n:]=BB
        qstate=Q0.row_join(Q1)
        qdstate=(Q0d+Q1*AA).row_join(Q0+Q1d+Q1*BB)
        qddstate=(F*AA).row_join(F*BB)
        qsource=us.copy();qdsource=Q1*acc+usd;qddsource=F*acc
        for target,row in [('Em','alpha'),('LambdaU','nu')]:
            for qm,qdm,qddm,sm in [(qstate,qdstate,qddstate,s.zeros(22,2*n)),
                                   (qsource,qdsource,qddsource,src[:22,:])]:
                res=EA*qm+EB*qdm+ED*qddm+sm
                qm[IX[target],:]=-res[IX[row],:]/EA[IX[row],IX[target]]
        for qm,qdm,qddm,sm in [(qstate,qdstate,qddstate,s.zeros(22,2*n)),
                               (qsource,qdsource,qddsource,src[:22,:])]:
            res=EA*qm+EB*qdm+ED*qddm+sm
            qdm[IX['Em'],:]=-res[IX['T'],:]/EB[IX['T'],IX['Em']]
        self.ch.exact_matrix(tag+'_acceleration_reduction',
                             F.conjugate().T*(EB*Q1+ED*F)+kin)
        return dict(G=G,acc=acc,us=us,usd=usd,source=src,kinetic=kin,
                    qstate=qstate.applyfunc(CLEAN),qsource=qsource.applyfunc(CLEAN),
                    qdstate=qdstate.applyfunc(CLEAN),qdsource=qdsource.applyfunc(CLEAN))


def calculate(emit):
    pins,absent,snapshot=inputs();before=snapshot();checks=[];cases=[]
    red=first.evolving.EvolvingReduction(first.prior,first.generic)
    for index in range(9):
        ch=Checks()
        try:
            der=Case(index,ch);record=der.run(red)
            accepted=all(q['passed'] for q in ch.rows);record['accepted']=accepted
        except Exception as exc:
            ch.add('calculation_completed',False,dict(type=type(exc).__name__,message=str(exc)))
            record=dict(index=index,accepted=False,checks=ch.rows,error=str(exc),traceback=traceback.format_exc())
            accepted=False
        emit('case_'+str(index).zfill(2)+'.json',ENCODE(record))
        cases.append(dict(index=index,accepted=accepted,
            forcing_power=record.get('bounds',{}).get('forcing_power'),
            action_probes=record.get('numerics',{}).get('action_probes',0)))
        checks.extend(dict(q,name=str(index)+'|'+q['name']) for q in ch.rows)
        if not accepted:break
    ch=Checks();ch.add('all_nine_cases',len(cases)==9,len(cases))
    ch.add('all2646_independent_action_probes',sum(q['action_probes'] for q in cases)==2646)
    ch.add('source_hash_size_mtime_preserved',before==snapshot());checks+=ch.rows
    passed=sum(q['passed'] for q in checks);complete=passed==len(checks)
    return dict(schema='r4c1-cusp3-coupled-tail-v2',
        validation='PASS_LOCAL_COUPLED_ORDER3_BOUND' if complete else 'FAIL_LOCAL_COUPLED_ORDER3_BOUND',
        status='COUPLED_ORDER3_BOUND_COMPLETE' if complete else 'COUPLED_ORDER3_BOUND_UNRESOLVED',
        passed=passed,total=len(checks),checks=checks,cases=cases,
        source_sha256=dict(sorted(pins.items())),inherited_sidecars_absent=absent,
        source_metadata_preserved=len(before),claim_status='Conditional',review_status='DEFERRED',
        Rule9_cleared=False,physics_pass=False,gate_effect='NONE',physical_window_admitted=False,
        useful_error_control=False,full_nonlinear_remainder=False,healthy_GR_verified=False,
        stage2_complete=False,stage3_entered=False,Tests1_3='HOLD_SUBSTANTIVE',MAT_001='BLOCKED',
        UVIR_003='IN_PROGRESS',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',TOP_X4='UNCHANGED',
        V1_failed_receipt_preserved=True,
        review_dependencies=['CUSP3-EVOLUTION-V1','LOW-RANK-WEIGHTED-EVOLUTION-V2',
          'CUSP-ODD-RESPONSE-TAIL-V1','CUSP-ODD-RESPONSE-ROOT-AUDIT-V1',
          'THREE-FAMILY-FINITE-K-V3','generic action/evolving reduction','all transitive debt'],
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_cusp3_coupled_tail_attempt_02')
    ap.add_argument('--replay');ap.add_argument('--progress');args=ap.parse_args()
    if args.progress:
        first.PROGRESS=(ROOT/args.progress).resolve()
        first.PROGRESS.relative_to((ROOT/'.local/itsm-context').resolve())
        first.PROGRESS.parent.mkdir(parents=True,exist_ok=True)
        if first.PROGRESS.exists():raise FileExistsError('Refuse progress overwrite')
        first.PROGRESS.touch()
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay:
        if not dest.is_dir():raise FileNotFoundError('Replay absent')
        before=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
    elif dest.exists():raise FileExistsError('Refuse evidence overwrite')
    else:dest.mkdir(parents=True)
    artifacts={}
    def emit(name,body):
        digest=SHA(body);side=(digest+'  '+name+'\n').encode()
        if args.replay:
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=side:
                raise ValueError('Immutable replay drift '+name)
        else:
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write(side)
        artifacts[name]=digest
    try:
        summary=calculate(emit);summary['artifacts']=dict(artifacts);emit('summary.json',ENCODE(summary))
    except BaseException as exc:
        if not args.replay:emit('interrupted.json',ENCODE(dict(error=str(exc),physics_pass=False)))
        raise
    if args.replay:
        after=[(p.name,SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in sorted(dest.iterdir())]
        if before!=after:raise ValueError('Replay changed artifact metadata')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','status','physics_pass')}),flush=True)
    for q in summary['checks']:
        if not q['passed']:print(json.dumps(q),flush=True)
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':
    sys.exit(main())
