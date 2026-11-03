"""Continue the 54 flagged full-SPARC jobs, without changing their target density."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='1'
import argparse
from concurrent.futures import ProcessPoolExecutor,as_completed
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import shutil
import numpy as np
import emcee
import sparc_real_mcmc_v3 as base

ROOT=base.ROOT
PARENT=ROOT/'Analysis/STAT/STAT-001/outputs/full_sparc_real_v3_20261101'


def work(args):
    row,e,out=args
    old=PARENT/row['Name']/str(e)
    folder=Path(out)/row['Name']/str(e)
    folder.mkdir(parents=True,exist_ok=False)
    data=base.load(row)
    with np.load(old/'block_010000.npz') as q:
        rs=('MT19937',q['random_keys'],int(q['random_pos']),int(q['has_gauss']),float(q['cached_gauss']))
        state=emcee.State(q['positions'],log_prob=q['last_log_probability'],random_state=rs)
    assert np.allclose(base.logpost(state.coords,data),state.log_prob,rtol=0,atol=1e-10)
    sampler=emcee.EnsembleSampler(64,state.coords.shape[1],base.logpost,args=(data,),vectorize=True)
    sampler.random_state=rs
    accepts=[]
    for begin in range(10000,20000,1000):
        state=sampler.run_mcmc(state,1000,progress=False)
        rs=state.random_state
        accepts.append(sampler.acceptance_fraction.copy())
        with (folder/f'block_{begin+1000:06d}.npz').open('xb') as f:
            np.savez_compressed(f,chain=sampler.get_chain(),log_probability=sampler.get_log_prob(),
                positions=state.coords,last_log_probability=state.log_prob,end=begin+1000,
                random_keys=rs[1],random_pos=rs[2],has_gauss=rs[3],cached_gauss=rs[4],acceptance=sampler.acceptance_fraction)
        sampler.reset()
    arrays=[]
    for p in sorted(old.glob('block_*.npz'))+sorted(folder.glob('block_*.npz')):
        with np.load(p) as q:
            arrays.append(q['chain'])
    chain=np.concatenate(arrays)[2000:]
    quant=np.quantile(chain.reshape(-1,chain.shape[-1]),[.025,.5,.975],axis=0)
    original=json.loads((old/'result.json').read_text())
    v=base.prediction(quant[1],data)[0][0]
    result=dict(name=row['Name'],ensemble=e,pid=os.getpid(),original_seed=original['seed'],
        parameters=original['parameters'],median=quant[1].tolist(),q025=quant[0].tolist(),q975=quant[2].tolist(),
        added_segment_acceptance=float(np.mean(accepts)),raw_chi2_at_marginal_medians=float(np.sum(((v-data['v'])/data['error'])**2)))
    base.write_new(folder/'result.json',result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    contract=json.loads((PARENT/'run_contract.json').read_text())
    diagnostics=json.loads((PARENT/'diagnostics.json').read_text())
    names=diagnostics['not_accepted']
    assert len(names)==54 and diagnostics['accepted']==121
    assert all(base.digest(ROOT/k)==v for k,v in contract['pins'].items())
    rows=[r for r in contract['rows'] if r['Name'] in names]
    assert len(rows)==54
    manifest=json.loads((PARENT/'artifact_manifest.json').read_text())
    # Verify the selected parent evidence before consuming it.
    for name in names:
        for e in range(4):
            for f in (PARENT/name/str(e)).iterdir():
                assert base.digest(f)==manifest[f.relative_to(PARENT).as_posix()]
    if shutil.disk_usage(ROOT).free<9*1024**3:
        raise SystemExit('Need 9 GiB free including reserve')
    a.output.mkdir(parents=True,exist_ok=False)
    base.write_new(a.output/'continuation_contract.json',dict(parent=str(PARENT.relative_to(ROOT)),
        parent_manifest_sha256=base.digest(PARENT/'artifact_manifest.json'),parent_diagnostics_sha256=base.digest(PARENT/'diagnostics.json'),
        source_sha256=base.digest(Path(__file__)),names=names,from_steps=10000,to_steps=20000,burn=2000,
        selection='All 54 pre-existing diagnostic failures; passing 121 untouched',unchanged_target=True))
    (a.output/'.gitignore').write_text('*.npz\n')
    failures=[]; count=0
    with ProcessPoolExecutor(max_workers=16,mp_context=mp.get_context('spawn')) as pool:
        fs={pool.submit(work,(r,e,str(a.output.resolve()))):(r['Name'],e) for r in rows for e in range(4)}
        for f in as_completed(fs):
            try:
                r=f.result();count+=1
                print(f"Completed {count}/216 {r['name']} ensemble {r['ensemble']}",flush=True)
            except Exception as exc:
                failures.append(dict(job=fs[f],error=repr(exc)))
    if failures:
        base.write_new(a.output/'failures.json',failures)
        raise SystemExit('Continuation jobs failed; evidence retained')
    results=[]
    for row in rows:
        ch=[]
        for e in range(4):
            arr=[]
            for folder in (PARENT/row['Name']/str(e),a.output/row['Name']/str(e)):
                for f in sorted(folder.glob('block_*.npz')):
                    with np.load(f) as q:
                        arr.append(q['chain'][:,0,:])
            ch.append(np.concatenate(arr)[2000:])
        ch=np.array(ch)
        rh=base.rhat(ch)
        taus=np.array([emcee.autocorr.integrated_time(c[:,None,:],tol=0,quiet=True) for c in ch])
        ess=np.sum(ch.shape[1]/taus,axis=0)
        met=bool(np.all(np.isfinite(taus)) and np.all(taus>0) and np.all(rh<1.01) and np.all(ess>=400) and np.all(ch.shape[1]>=50*taus))
        results.append(dict(name=row['Name'],rank_folded_split_rhat=rh.tolist(),fixed_walker_ess=ess.tolist(),
                            length_check=bool(np.all(ch.shape[1]>=50*taus)),criteria_met=met))
    base.write_new(a.output/'diagnostics.json',dict(physics_pass=False,continued=54,original_passing_untouched=121,
        newly_meeting_criteria=sum(r['criteria_met'] for r in results),still_not_accepted=[r['name'] for r in results if not r['criteria_met']],
        diagnostics=results))
    print('Continuation and diagnostics complete',flush=True)


if __name__=='__main__':
    main()
