"""Exact complete canonical block structure; no eigenvalue or physical admission claim."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json
from collections import defaultdict,Counter
from decimal import Decimal,localcontext,Inexact,Rounded
from pathlib import Path
import sympy as sy
ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_canonical_conditioning_v1.py'
PSHA='013f84f8a342b68d8d2c86c18eeb3e9552599709b9f5ee5cd2462704992aef89'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_EXACT_CANONICAL_BLOCKS_V1_CONTRACT_2026-10-20.md'
CSHA='46e26cee361e321254d05389f8c096bd93d5f61968b8323d67c369cb277762cc'
BASE='Analysis/MasterTests/outputs/r4c1_canonical_conditioning_v1_n17_attempt_01/'
INDEX=BASE+'independent.json'
ISHA='af0e99c5de4cd96c3b23319bfba99a9dc251e73656f7f52afa9f5fe894d44334'
PILOT='Analysis/MasterTests/outputs/r4c1_mp_schur_pilot_v1_attempt_01/summary.json'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PARENT).read_bytes())!=PSHA or SHA((ROOT/INDEX).read_bytes())!=ISHA:raise ValueError('parent/index drift')
spec=importlib.util.spec_from_file_location('frozen_conditioning',ROOT/PARENT)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
pv=old.pv
ENTRIES={tuple(r['key']):r for r in json.loads((ROOT/INDEX).read_bytes())}
PINS={**old.PINS,PARENT:PSHA,CONTRACT:CSHA,INDEX:ISHA,
 'Analysis/MasterTests/test_01_r4c1_mp_schur_pilot_v1.py':'6ed31d6064e96a1564d572cd4027e118d93e9a42de6acfc2b99acc4e53e4dece',
 'Theory/Gates/RES-001/RES001_R4C1_MP_SCHUR_PILOT_V1_CONTRACT_2026-10-20.md':'13d1a6b7af9b65faa75f232db679be52ffc2cd1e3d1fbb1cce19d576deae1725',
 PILOT:'e7752cbb575cc85b787247f9b494ad79fd706cd8a9e39802d6a40803c52c2586'}
for k,r in ENTRIES.items():PINS[BASE+old.shear_name(k)]=r['transform_sha256']

def sources():
    pins={**PINS,SELF:SHA((ROOT/SELF).read_bytes())};meta={}
    for name,want in pins.items():
        p=ROOT/name;sc=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=want or sc.read_text().split()[0]!=want:raise ValueError('source drift '+name)
        for f in (p,sc):
            b=f.read_bytes();meta[f.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=f.stat().st_mtime_ns)
    return pins,meta

class Union:
    def __init__(self,n):self.p=list(range(n))
    def find(self,x):
        while self.p[x]!=x:self.p[x]=self.p[self.p[x]];x=self.p[x]
        return x
    def join(self,a,b):
        a,b=self.find(a),self.find(b)
        if a!=b:self.p[b]=a

def omega(i,j,d):return -1 if i<d and j==i+d else 1 if j<d and i==j+d else 0

def decompose(raw,ch):
    D=len(raw);d=D//2
    if D%2 or any(len(r)!=D for r in raw):raise ValueError('non-square/noncanonical dimension')
    S=[[Decimal(x) for x in r] for r in raw]
    if any(not x.is_finite() for r in S for x in r):raise ValueError('nonfinite input')
    u=Union(D);v=Union(D)
    for i in range(d):u.join(i,d+i);v.join(i,d+i)
    for i in range(D):
        for j in range(D):
            if not S[i][j].is_zero():u.join(i,j)
            if not S[(i+d)%D][j].is_zero():v.join(i,j)
    groups=defaultdict(list);g2=defaultdict(list)
    for i in range(D):groups[u.find(i)].append(i);g2[v.find(i)].append(i)
    qgroups=sorted(([i for i in g if i<d] for g in groups.values()),key=lambda a:a[0])
    supports=[q+[d+i for i in q] for q in qgroups]
    ch.add('complete_disjoint_coordinate_coverage',sorted(i for g in supports for i in g)==list(range(D)))
    ch.add('canonical_partners_retained',all(set(g)==set(q+[d+i for i in q]) for q,g in zip(qgroups,supports)))
    ch.add('independent_generator_components_identical',sorted(sorted(g) for g in groups.values())==sorted(sorted(g) for g in g2.values()))
    qorder=[i for q in qgroups for i in q];perm=qorder+[d+i for i in qorder]
    ch.add('full_permutation_symplectic_exact',all(omega(perm[i],perm[j],d)==omega(i,j,d) for i in range(D) for j in range(D)))
    ch.add('all_offblock_form_and_generator_entries_exact_zero',all(S[i][j].is_zero() and S[(i+d)%D][j].is_zero() for i in range(D) for j in range(D) if u.find(i)!=u.find(j)))
    blocks=[dict(indices=g,q_indices=q,quadratic_form=[[raw[i][j] for j in g] for i in g]) for q,g in zip(qgroups,supports)]
    rebuild=[['0.0']*D for _ in range(D)];exceptions=[]
    for b in blocks:
        for a,i in enumerate(b['indices']):
            for c,j in enumerate(b['indices']):rebuild[i][j]=b['quadratic_form'][a][c]
    for i in range(D):
        for j in range(D):
            if u.find(i)!=u.find(j) and raw[i][j]!='0.0':exceptions.append([i,j,raw[i][j]]);rebuild[i][j]=raw[i][j]
    ch.add('complete_serialized_matrix_reconstruction',rebuild==raw and SHA(ENC(rebuild))==SHA(ENC(raw)))
    nz=[x for r in S for x in r if not x.is_zero()]
    prec=max(100,max((x.adjusted() for x in nz),default=0)-min((x.as_tuple().exponent for x in nz),default=0)+20)
    with localcontext() as ctx:
        ctx.prec=prec;ctx.clear_flags();agree=True
        for seed in (0,1):
            x=[Decimal(((i*(seed+1)+3*seed)%17)-8) for i in range(D)]
            full=[sum((S[i][j]*x[j] for j in range(D)),Decimal(0)) for i in range(D)];assembled=[Decimal(0)]*D
            for b in blocks:
                g=b['indices']
                for i in g:assembled[i]=sum((Decimal(raw[i][j])*x[j] for j in g),Decimal(0))
            agree=agree and full==assembled
        exact=not ctx.flags[Inexact] and not ctx.flags[Rounded]
    ch.add('complete_coordinate_independent_matvec',agree)
    ch.add('finite_decimal_matvec_no_rounding',exact)
    return dict(dimension=D,canonical_permutation=perm,blocks=blocks,block_dimensions=[len(g) for g in supports],
      offblock_zero_spelling_exceptions=exceptions,serialized_matrix_payload_sha256=SHA(ENC(raw)),matvec_decimal_precision=prec,
      no_thresholds_or_modes_removed=True,high_precision_schur_completed=False,physical_window_established=False)

def smoke(ch):
    S=sy.diag(3,-2,0,5,1,-1,0,1);S[0,1]=S[1,0]=1
    p=[2,0,3,1,6,4,7,5];S=S.extract(p,p)
    raw=[[str(S[i,j]) for j in range(8)] for i in range(8)];loc=pv.base.Checks();a=decompose(raw,loc)
    pv.nodal.reg.joint.merge_checks(ch,loc.rows,'signed_zero_')
    ch.add('signed_and_zero_blocks_retained',sorted(a['block_dimensions'])==[2,2,4])
    J=sy.zeros(8);J[:4,4:]=sy.eye(4);J[4:,:4]=-sy.eye(4);z=sy.Symbol('z');full=(z*sy.eye(8)-J*S).det();product=sy.Integer(1)
    for b in a['blocks']:
        T=sy.Matrix(b['quadratic_form']);n=T.rows//2;K=sy.zeros(2*n);K[:n,n:]=sy.eye(n);K[n:,:n]=-sy.eye(n)
        product*= (z*sy.eye(2*n)-K*T).det()
    ch.add('exact_characteristic_polynomial_factorization',sy.expand(full-product)==0)
    # Find two distinct nonzero-supported components, and couple them by a tiny exact value.
    raw2=[r.copy() for r in raw];q0=a['blocks'][0]['q_indices'][0];q1=a['blocks'][1]['q_indices'][0]
    raw2[q0][q1]='1e-300';loc=pv.base.Checks();b=decompose(raw2,loc)
    pv.nodal.reg.joint.merge_checks(ch,loc.rows,'tiny_nonzero_')
    ch.add('arbitrarily_small_nonzero_coupling_not_dropped',len(b['blocks'])==len(a['blocks'])-1)
    raw3=[r.copy() for r in raw];raw3[q0][q1]='-0.0';loc=pv.base.Checks();c=decompose(raw3,loc)
    pv.nodal.reg.joint.merge_checks(ch,loc.rows,'zero_spelling_')
    ch.add('zero_spelling_preserved_without_numerical_blocker',c['block_dimensions']==a['block_dimensions'] and bool(c['offblock_zero_spelling_exceptions']))

def execute(args,dest):
    pins,before=sources();ch=pv.base.Checks();smoke(ch);manifest=ENC(dict(source_sha256=pins,source_metadata=before,keys=[list(k) for k in sorted(ENTRIES)]))
    runsha=SHA(manifest)
    if args.output:old.old.num.write_pair(dest,'run_inputs.json',manifest)
    else:old.old.num.check_pair(dest,'run_inputs.json',manifest)
    index=[]
    for key in sorted(ENTRIES):
        p=ROOT/(BASE+old.shear_name(key));src=json.loads(p.read_bytes());local=pv.base.Checks()
        data=decompose(src['data']['transformed_forms']['100'],local)
        origin=old.INPUT+old.ENTRIES[key]['matrix_file'];labels=json.loads((ROOT/origin).read_bytes())['data']['labels']
        for b in data['blocks']:b['original_q_labels']=[labels[i] for i in b['q_indices']]
        obj=dict(key=list(key),run_input_sha256=runsha,input_sha256=PINS[p.relative_to(ROOT).as_posix()],data=data,checks=local.rows)
        name=old.case_name(key)
        if args.replay:old.old.num.check_pair(dest,name,ENC(obj))
        else:old.old.num.write_pair(dest,name,ENC(obj))
        pv.nodal.reg.joint.merge_checks(ch,local.rows,'_'.join(map(str,key))+'_')
        index.append(dict(key=list(key),file=name,sha256=SHA(ENC(obj)),block_dimensions=data['block_dimensions']))
        print(json.dumps(dict(stage='complete_case_sealed',key=key,block_dimensions=data['block_dimensions'])),flush=True)
    _,after=sources();ch.add('source_sidecar_metadata_unchanged',before==after)
    n=sum(r['passed'] for r in ch.rows);summary=dict(validation='PASS_EXACT_COMPLETE_BLOCK_STRUCTURE_ONLY' if n==len(ch.rows) else 'FAIL_EXACT_BLOCK_STRUCTURE',
      passed=n,total=len(ch.rows),checks=ch.rows,source_sha256=pins,source_metadata=before,complete_coarse_case_coverage=len(index)==18,
      all_modes_retained=True,new_schur_or_precision_result=False,stage2_complete=False,stage3_entered=False,physics_pass=False,
      Rule9_cleared=False,review_status='DEFERRED',gate_effect='NONE')
    formulas=dict(structure='Exact decimal nonzeros plus canonical-pair unions; P=diag(U,U); every block retained',
      holds='No new eigenvalues or physical modes; complete multiprecision block solver, domain, nonlinear interactions, healthy GR and matching remain open')
    for name,obj in (('summary.json',summary),('independent.json',index),('formulas.json',formulas)):
        if args.replay:old.old.num.check_pair(dest,name,ENC(obj))
        else:old.old.num.write_pair(dest,name,ENC(obj))
    print(json.dumps({k:summary[k] for k in ('validation','passed','total','complete_coarse_case_coverage')}),flush=True);return 0 if n==len(ch.rows) else 1

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output');p.add_argument('--replay');a=p.parse_args()
    if bool(a.output)==bool(a.replay):p.error('choose fresh output or read-only replay')
    dest=(ROOT/(a.output or a.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside output root')
    if a.output:dest.mkdir(parents=True,exist_ok=False)
    before={f.name:old.old.num.file_metadata(f) for f in dest.iterdir()} if a.replay else None
    rc=execute(a,dest)
    if a.replay:
        if before!={f.name:old.old.num.file_metadata(f) for f in dest.iterdir()}:raise ValueError('replay byte/metadata/set mutation')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    return rc
if __name__=='__main__':raise SystemExit(main())
