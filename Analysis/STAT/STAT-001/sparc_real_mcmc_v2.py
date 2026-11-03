"""Full-sample conditional algebraic comparator. No ITSM physical clearance."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import shutil
import sys
import numpy as np
import scipy
from scipy.stats import truncnorm
import emcee
from sparc_conditional_pilot_v1 import prediction, logpost, controls, rhat

ROOT=Path(__file__).resolve().parents[3]
CAT=ROOT/'Data/SPARC_catalogue_archive_candidate_v1_20261101/nuisance_inputs.csv'
PILOT=('CamB','NGC7814','NGC5907','UGC01281')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_new(p,obj):
    with p.open('x',encoding='utf-8') as f:
        json.dump(obj,f,indent=2,allow_nan=False)
        f.write('\n')


def load(row):
    a=np.loadtxt(ROOT/'Data/SPARC_data'/f"{row['Name']}_rotmod.dat")
    assert a.ndim==2 and a.shape[1]==8 and np.all(np.isfinite(a))
    assert np.all(a[:,0]>0) and np.all(a[:,2]>0) and np.all(np.diff(a[:,0])>0)
    data=dict(r=a[:,0],v=a[:,1],error=a[:,2],gas=a[:,3],disk=a[:,4],bulge=a[:,5],
              i0=float(row['i']),i_sigma=float(row['e_i']),d_sigma=float(row['e_Dist'])/float(row['Dist']))
    assert data['i_sigma']>0 and data['d_sigma']>0
    return data


def job(args):
    row,e,steps,burn,out,seed=args
    folder=Path(out)/row['Name']/str(e)
    folder.mkdir(parents=True,exist_ok=True)
    result_path=folder/'result.json'
    if result_path.exists():
        return json.loads(result_path.read_text())
    data=load(row)
    bulge=bool(np.any(data['bulge']!=0))
    center=np.array([np.log10(.5),1.,data['i0']]+([np.log10(.7)] if bulge else []))
    scales=np.array([.1,data['d_sigma'],data['i_sigma']]+([.1] if bulge else []))
    rng=np.random.default_rng(seed)
    good=[]
    for attempt in range(100):
        proposed=center+rng.normal(size=(128,len(center)))*scales
        proposed[:,1]=truncnorm.rvs(-1/scales[1],np.inf,loc=1,scale=scales[1],size=128,random_state=rng)
        proposed[:,2]=truncnorm.rvs(-center[2]/scales[2],(90-center[2])/scales[2],loc=center[2],scale=scales[2],size=128,random_state=rng)
        # Initialization only: analytically find the inward-support lower bound
        # on U_disk for each proposed U_bulge, then sample the stable normal tail.
        disk2=data['disk']*np.abs(data['disk'])
        assert np.all(disk2>0),'Nonpositive disk template requires a separate support chart'
        ub=10**proposed[:,3] if bulge else np.zeros(128)
        lower=np.max((-data['gas']*np.abs(data['gas'])-ub[:,None]*data['bulge']*np.abs(data['bulge']))/disk2,axis=1)
        loglower=np.full(128,-np.inf)
        loglower[lower>0]=np.log10(lower[lower>0])
        proposed[:,0]=truncnorm.rvs((loglower-center[0])/scales[0],np.inf,loc=center[0],scale=scales[0],random_state=rng)
        accepted=proposed[np.isfinite(logpost(proposed,data))]
        good.extend(accepted.tolist())
        if len(good)>=64:
            break
    if len(good)<64:
        raise ValueError(f"No sufficient physical initial support: {row['Name']}")
    sampler=emcee.EnsembleSampler(64,len(center),logpost,args=(data,),vectorize=True)
    sampler.random_state=np.random.RandomState(seed).get_state()
    state=np.array(good[:64]); start=0
    blocks=sorted(folder.glob('block_*.npz'))
    if blocks:
        with np.load(blocks[-1]) as q:
            rs=('MT19937',q['random_keys'],int(q['random_pos']),int(q['has_gauss']),float(q['cached_gauss']))
            state=emcee.State(q['positions'],log_prob=q['last_log_probability'],random_state=rs)
            start=int(q['end'])
    for begin in range(start,steps,1000):
        count=min(1000,steps-begin)
        state=sampler.run_mcmc(state,count,progress=False)
        rs=state.random_state
        with (folder/f'block_{begin+count:06d}.npz').open('xb') as f:
            np.savez_compressed(f,chain=sampler.get_chain(),log_probability=sampler.get_log_prob(),
                positions=state.coords,last_log_probability=state.log_prob,end=begin+count,
                random_keys=rs[1],random_pos=rs[2],has_gauss=rs[3],cached_gauss=rs[4],
                acceptance=sampler.acceptance_fraction)
        sampler.reset()
    chunks=[]; accepts=[]
    for p in sorted(folder.glob('block_*.npz')):
        with np.load(p) as q:
            chunks.append(q['chain']); accepts.append(q['acceptance'])
    chain=np.concatenate(chunks,axis=0)[burn:]
    quant=np.quantile(chain.reshape(-1,len(center)),[.025,.5,.975],axis=0)
    v=prediction(quant[1],data)[0][0]
    result=dict(name=row['Name'],ensemble=e,seed=seed,pid=os.getpid(),quality=int(row['Qual']),i0=data['i0'],
        parameters=['log10_Udisk','D_over_D0','inclination_deg']+(['log10_Ubulge'] if bulge else []),
        q025=quant[0].tolist(),median=quant[1].tolist(),q975=quant[2].tolist(),
        acceptance=float(np.mean(accepts)),raw_chi2_at_marginal_medians=float(np.sum(((v-data['v'])/data['error'])**2)),
        n_points=len(data['r']))
    write_new(result_path,result)
    return result


def summarize(out,rows,steps,burn):
    results=[]
    for row in rows:
        folder=out/row['Name']; chains=[]
        for e in range(4):
            chunks=[]
            for p in sorted((folder/str(e)).glob('block_*.npz')):
                with np.load(p) as q:
                    chunks.append(q['chain'][:,0,:])
            chains.append(np.concatenate(chunks,axis=0)[burn:])
        chains=np.array(chains)
        rh=rhat(chains)
        tau=np.array([emcee.autocorr.integrated_time(ch[:,None,:],tol=0,quiet=True) for ch in chains])
        ess=np.sum(chains.shape[1]/tau,axis=0)
        met=bool(np.all(np.isfinite(tau)) and np.all(tau>0) and np.all(rh<1.01) and np.all(ess>=400) and np.all(chains.shape[1]>=50*tau))
        results.append(dict(name=row['Name'],quality=int(row['Qual']),i0=float(row['i']),
                            rank_folded_split_rhat=rh.tolist(),fixed_walker_ess=ess.tolist(),criteria_met=met))
    write_new(out/'diagnostics.json',dict(scope='CONDITIONAL_ALGEBRAIC_COMPARATOR',physics_pass=False,
        galaxies=len(rows),steps=steps,burn=burn,diagnostics=results,
        accepted=sum(r['criteria_met'] for r in results),not_accepted=[r['name'] for r in results if not r['criteria_met']]))
    print(json.dumps({'galaxies':len(rows),'criteria_met':sum(r['criteria_met'] for r in results)},flush=True))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--pilot',action='store_true')
    p.add_argument('--resume',action='store_true')
    p.add_argument('--steps',type=int,default=10000)
    p.add_argument('--burn',type=int,default=2000)
    a=p.parse_args(); assert a.steps>a.burn>=0
    controls()
    with CAT.open(newline='') as f:
        rows=sorted(list(csv.DictReader(f)),key=lambda r:r['Name'])
    assert len(rows)==175 and len({r['Name'] for r in rows})==175
    if a.pilot:
        rows=[r for r in rows if r['Name'] in PILOT]
        assert len(rows)==4
    pins={str(CAT.relative_to(ROOT)):digest(CAT),
          str(Path(__file__).relative_to(ROOT)):digest(Path(__file__)),
          'Analysis/STAT/STAT-001/sparc_conditional_pilot_v1.py':digest(Path(__file__).with_name('sparc_conditional_pilot_v1.py'))}
    for row in rows:
        load(row)
        path=ROOT/'Data/SPARC_data'/f"{row['Name']}_rotmod.dat"
        pins[str(path.relative_to(ROOT))]=digest(path)
    config=dict(steps=a.steps,burn=a.burn,walkers=64,ensembles=4,workers=16,
                rows=rows,pins=pins,versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,emcee=emcee.__version__))
    # Conservative float64 storage allowance, including log densities and overhead.
    need=len(rows)*4*a.steps*64*5*8*1.3
    if shutil.disk_usage(ROOT).free<need+3*1024**3:
        raise SystemExit('Insufficient free disk for conservative chain storage plus 3 GiB reserve')
    if a.resume:
        assert json.loads((a.output/'run_contract.json').read_text())==config,'Resume contract mismatch'
        assert not (a.output/'diagnostics.json').exists(),'Run already summarized'
    else:
        a.output.mkdir(parents=True,exist_ok=False)
        write_new(a.output/'run_contract.json',config)
        (a.output/'.gitignore').write_text('*.npz\n')
    jobs=[(r,e,a.steps,a.burn,str(a.output.resolve()),720000+idx*10+e) for idx,r in enumerate(rows) for e in range(4)]
    failures=[]; done=0
    with ProcessPoolExecutor(max_workers=16,mp_context=mp.get_context('spawn')) as pool:
        futures={pool.submit(job,j):j for j in jobs}
        for fut in as_completed(futures):
            try:
                result=fut.result(); done+=1
                print(f"Finished {done}/{len(jobs)} {result['name']} ensemble {result['ensemble']}",flush=True)
            except Exception as exc:
                j=futures[fut]
                failures.append(dict(name=j[0]['Name'],ensemble=j[1],error=repr(exc)))
    if failures:
        write_new(a.output/f'failures_{os.getpid()}.json',failures)
        raise SystemExit('Job failures retained; do not summarize as a complete run')
    summarize(a.output,rows,a.steps,a.burn)


if __name__=='__main__':
    main()
