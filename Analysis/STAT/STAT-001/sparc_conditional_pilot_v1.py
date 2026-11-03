"""Conditional algebraic SPARC sampler validation. Synthetic data only in v1."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import sys
import numpy as np
import scipy
from scipy.stats import rankdata, norm
import emcee

A0 = 1.2e-10  # empirical comparator input, not an ITSM derivation
KPC = 3.085677581491367e19


def prediction(theta, data):
    """theta=(log10 U_disk, distance ratio, inclination degrees[, log10 U_bulge])."""
    t = np.atleast_2d(theta)
    ud, d, inc = 10**t[:, 0], t[:, 1], np.deg2rad(t[:, 2])
    ub = 10**t[:, 3] if t.shape[1] == 4 else np.zeros(len(t))
    r, gas, disk, bulge = (data[k][None, :] for k in ('r', 'gas', 'disk', 'bulge'))
    b2 = d[:, None] * (gas * np.abs(gas) + ud[:, None]*disk*np.abs(disk) + ub[:, None]*bulge*np.abs(bulge))
    with np.errstate(invalid='ignore', divide='ignore'):
        gn = b2 * 1e6 / (r*d[:, None]*KPC)
        gt = (gn + np.sqrt(gn*gn + 4*gn*A0))/2
        v = np.sqrt(gt*r*d[:, None]*KPC)/1000
        nominal_velocity = v*np.sin(inc[:, None])/np.sin(np.deg2rad(data['i0']))
    return nominal_velocity, np.all(b2 > 0, axis=1)


def logpost(theta, data):
    t = np.atleast_2d(theta)
    v, inward = prediction(t, data)
    valid = inward & (t[:, 1] > 0) & (t[:, 2] > 0) & (t[:, 2] < 90)
    z = np.column_stack(((t[:, 0]-np.log10(.5))/.1,
                         (t[:, 1]-1)/data['d_sigma'], (t[:, 2]-data['i0'])/data['i_sigma']))
    if t.shape[1] == 4:
        z = np.column_stack((z, (t[:, 3]-np.log10(.7))/.1))
    # Prior is Gaussian in the declared coordinates; distance/i are truncated
    # to physical support. Its parameter-independent normalizers cancel here.
    ll = -.5*np.sum(((v-data['v'])/data['error'])**2 + np.log(2*np.pi*data['error']**2), axis=1)
    ans = ll-.5*np.sum(z*z, axis=1)
    return np.where(valid & np.isfinite(ans), ans, -np.inf)


def synthetic(case):
    # Independent simulated observations; no real catalogue errors are assumed.
    rng = np.random.default_rng(18700+case)
    r = np.linspace(.5, 20, 32)
    data = dict(r=r, gas=25*np.sqrt(r/(r+2)), disk=110*np.sqrt(r/3)*np.exp(-r/10),
                bulge=60*np.sqrt(r)/(r+1) if case % 2 else np.zeros_like(r),
                i0=45. if case < 2 else 70., d_sigma=.07, i_sigma=3., error=np.full(len(r),2.5))
    truth = np.array([np.log10(.5), 1., data['i0']] + ([np.log10(.7)] if case % 2 else []))
    data['v'] = prediction(truth, data)[0][0]+rng.normal(0, data['error'])
    return data, truth


def worker(job):
    case, ensemble, steps, burn, out = job
    data, truth = synthetic(case)
    seed = 910000+case*100+ensemble
    rng = np.random.default_rng(seed)
    scales = np.array([.1,.07,3.] + ([.1] if len(truth)==4 else []))
    start = truth+rng.normal(size=(64,len(truth)))*scales
    assert np.all(np.isfinite(logpost(start, data)))
    sampler = emcee.EnsembleSampler(64,len(truth), logpost, args=(data,), vectorize=True)
    sampler.random_state = np.random.RandomState(seed).get_state()
    state = start
    for end in range(0, steps, 1000):
        state = sampler.run_mcmc(state,min(1000,steps-end),progress=False)
        rs = state.random_state
        path = Path(out)/f'case{case}_ensemble{ensemble}_step{sampler.iteration}.npz'
        # Exclusive checkpoints preserve full chains and MT19937 state without pickle.
        with path.open('xb') as stream:
            np.savez_compressed(stream,chain=sampler.get_chain(),log_probability=sampler.get_log_prob(),
                positions=state.coords,random_keys=rs[1],random_pos=rs[2],has_gauss=rs[3],cached_gauss=rs[4])
    chain = sampler.get_chain(discard=burn)
    q = np.quantile(chain.reshape(-1,len(truth)),[.025,.5,.975],axis=0)
    return dict(case=case,ensemble=ensemble,seed=seed,pid=os.getpid(),acceptance=float(np.mean(sampler.acceptance_fraction)),
                truth=truth.tolist(),q025=q[0].tolist(),median=q[1].tolist(),q975=q[2].tolist(),
                covered95=((q[0]<=truth)&(truth<=q[2])).tolist())


def rhat(chains):
    # One preselected walker per INDEPENDENT ensemble, never treating walkers
    # in the same interacting ensemble as independent chains.
    n = chains.shape[1]//2
    x = np.concatenate((chains[:,:n],chains[:,-n:]),axis=0)
    def basic(a):
        w = np.mean(np.var(a,axis=1,ddof=1),axis=0)
        b = n*np.var(np.mean(a,axis=1),axis=0,ddof=1)
        return np.sqrt(((n-1)*w/n+b/n)/w)
    def ranked(a):
        return np.stack([norm.ppf((rankdata(a[:,:,j])-.375)/(a.shape[0]*n+.25)).reshape(a.shape[:2])
                         for j in range(a.shape[2])],axis=2)
    return np.maximum(basic(ranked(x)),basic(ranked(np.abs(x-np.median(x,axis=(0,1))))))


def controls():
    data, truth = synthetic(1)
    v = prediction(truth,data)[0][0]
    # Independent scalar nu expression, nominal distance/inclination.
    ref=[]
    for r,g,d,b in zip(data['r'],data['gas'],data['disk'],data['bulge']):
        s=g*abs(g)+.5*d*abs(d)+.7*b*abs(b)
        gn=s*1e6/(r*KPC)
        ref.append(np.sqrt(s*(.5+np.sqrt(.25+A0/gn))))
    assert np.allclose(v,ref,rtol=2e-14)
    data['v']=v.copy()
    lp=logpost(truth,data)[0]
    displaced=truth.copy();displaced[2]+=10
    assert logpost(displaced,data)[0]<lp
    bad=truth.copy();bad[1]=-1
    assert np.isneginf(logpost(bad,data)[0])
    bad=truth.copy();bad[2]=0
    assert np.isneginf(logpost(bad,data)[0])
    # Same likelihood in line-of-sight coordinates, including fixed Jacobian.
    s=np.sin(np.deg2rad(data['i0']))
    los=-.5*np.sum(np.log(2*np.pi*(data['error']*s)**2))
    assert np.isclose(lp,los+len(v)*np.log(s))
    return 'PASS_SCALAR_FORMULA_SUPPORT_AND_FIXED_COORDINATE_JACOBIAN'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--steps',type=int,default=10000)
    p.add_argument('--burn',type=int,default=2000)
    args=p.parse_args()
    assert args.steps>args.burn>=0
    control=controls()
    args.output.mkdir(parents=True,exist_ok=False)
    jobs=[(c,e,args.steps,args.burn,str(args.output.resolve())) for c in range(4) for e in range(4)]
    with ProcessPoolExecutor(max_workers=16,mp_context=mp.get_context('spawn')) as pool:
        rows=list(pool.map(worker,jobs))
    diagnostics=[]
    for case in range(4):
        chains=np.array([np.load(args.output/f'case{case}_ensemble{e}_step{args.steps}.npz')['chain'][args.burn:,0,:] for e in range(4)])
        rh=rhat(chains)
        taus=np.array([emcee.autocorr.integrated_time(ch[:,None,:],tol=0,quiet=True) for ch in chains])
        ess=np.sum(chains.shape[1]/taus,axis=0)
        ok=bool(np.all(np.isfinite(taus)) and np.all(taus>0) and np.all(rh<1.01) and np.all(ess>=400) and np.all(chains.shape[1]>=50*taus))
        diagnostics.append(dict(case=case,rank_folded_split_rhat=rh.tolist(),fixed_walker_ess_estimate=ess.tolist(),
                                enough_length=bool(np.all(chains.shape[1]>=50*taus)),convergence_criteria_met=ok))
    result=dict(scope='SYNTHETIC_SAMPLER_VALIDATION_ONLY',physics_pass=False,gate_effect='NONE',
                controls=control,steps=args.steps,burn=args.burn,walkers=64,workers_requested=16,
                worker_pids=sorted(set(r['pid'] for r in rows)),jobs=rows,diagnostics=diagnostics,
                versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,emcee=emcee.__version__),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (args.output/'receipt.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ('scope','controls','worker_pids','diagnostics')},indent=2))


if __name__=='__main__':
    main()
