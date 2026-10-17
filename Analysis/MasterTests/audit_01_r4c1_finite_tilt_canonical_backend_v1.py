"""Bridge the frozen vectorized Hamiltonian to its original 80-digit density."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import mpmath as mp
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PARENT='Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_FINITE_TILT_CANONICAL_BACKEND_V1_ADDENDUM_2026-10-17.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda o:(json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
EXPECTED='4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada'
if SHA((ROOT/PARENT).read_bytes())!=EXPECTED:raise ValueError('parent source drift')
spec=importlib.util.spec_from_file_location('finite_tilt_canonical_frozen_v2',ROOT/PARENT)
parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)

def inputs():
    pins,meta=parent.inputs()
    for name,expected in ((ADDENDUM,'709837f95506893169451cdf3f0352b91af2c6662c27119798ff513cda004846'),(SELF,SHA((ROOT/SELF).read_bytes()))):
        p=ROOT/name;side=Path(str(p)+'.sha256')
        if SHA(p.read_bytes())!=expected or side.read_text().split()[0].lower()!=expected:raise ValueError('audit source drift '+name)
        pins[name]=expected
        for q in (p,side):
            b=q.read_bytes();st=q.stat();meta[q.relative_to(ROOT).as_posix()]=dict(sha256=SHA(b),bytes=len(b),mtime_ns=st.st_mtime_ns)
    return pins,meta

def compare(ch,name,observed,target,tolerance='1e-10'):
    a=np.asarray(observed,dtype=float);b=np.asarray(target,dtype=float)
    residual=float(np.max(np.abs(a-b))/max(1.,np.max(np.abs(b))))
    ch.add(name,residual<float(tolerance),residual,'normalized<'+tolerance+'; binary64 vs80digits')
    return residual

def calculate():
    mp.mp.dps=80;pins,before=inputs();ch=parent.Checks();cases=[]
    for seed in (0,1):
        c=parent.mp_geometry(seed)
        y=mp.matrix([c['K'][i,j] for i,j in parent.HM]+list(c['X'])+[c['proper'][n] for n in ('u','v','r')])
        for family in parent.FAMILIES:
            for eta in parent.ETAS:
                print('BACKEND_BRIDGE '+str(seed)+' '+family+' '+eta,flush=True)
                par=parent.parameters(family,eta,'mp');pn=parent.parameters(family,eta)
                ps=c['proper']['psi'];zs=c['proper']['Z']
                fn=lambda yy,pp=ps,zz=0:parent.mp_body(c,par,yy,pp,zz,include_dust=False)
                zero=mp.matrix(12,1);base=fn(zero)
                unit=[mp.matrix([int(i==j) for i in range(12)]) for j in range(12)]
                plus=[fn(e) for e in unit];minus=[fn(-e) for e in unit]
                ell=mp.matrix([(a-b)/2 for a,b in zip(plus,minus)]);R=mp.matrix(12)
                for i in range(12):
                    R[i,i]=plus[i]+minus[i]-2*base
                    for j in range(i):R[i,j]=R[j,i]=fn(unit[i]+unit[j])-plus[i]-plus[j]+base
                P=R*y+ell
                forward=[]
                for i in range(12):
                    def at(v):yy=mp.matrix(y);yy[i]=v;return fn(yy,ps,zs)
                    forward.append(mp.diff(at,y[i]))
                ref_error=max(abs(forward[i]-P[i]) for i in range(12))
                tag=str(seed)+'_'+family+'_'+eta
                ch.small(tag+'_reference_polarization_momenta',ref_error,'1e-50')
                pz=mp.diff(lambda zz:fn(y,ps,zz),zs);pps=mp.diff(lambda pp:fn(y,pp,zs),ps)
                volume=mp.sqrt(mp.det(c['h']));C=mp.exp(par['beta']*c['psi']);tg=c['spatial']['T']
                td=mp.sqrt(C*C+(tg.T*c['hi']*tg)[0]);pt=c['epsilon']*C*C*c['proper']['T']
                qvalues=[c['h'][i,j] for i,j in parent.HM]+list(c['V'])+[c[n] for n in ('u','v','r','psi','Z')]+[mp.mpf(0)]
                pvalues=[volume*P[i]/2 for i in range(6)]+[volume*P[i] for i in range(6,12)]+[volume*pps,volume*pz,volume*pt]
                q=np.array([[float(v) for v in qvalues]])
                p=np.array([[float(v) for v in pvalues]])
                hi=np.linalg.inv(parent.tensor_h(q));grad=np.zeros((1,15,3))
                for j,name in enumerate(('u','v','r','psi','Z','T')):grad[0,9+j]=[float(v) for v in c['spatial'][name]]
                DV=np.array([[[float(c['DV'][i,j]) for j in range(3)] for i in range(3)]])
                R3=np.array([float(c['R3'])])
                energy,flux,data=parent.full_blocks(q,hi,grad,DV,p,pn,R3)
                Ereference=volume*((P.T*y)[0]+pps*ps+pz*zs-fn(y,ps,zs)+pt*td)
                fluxreference=c['gamma']*(c['hi']*mp.matrix(pvalues[6:9]))[2]
                errs=[]
                errs.append(compare(ch,tag+'_all144_complement_entries',data['R'][0],[[float(R[i,j]) for j in range(12)] for i in range(12)]))
                errs.append(compare(ch,tag+'_all12_affine_entries',data['ell'][0],[float(v) for v in ell]))
                errs.append(compare(ch,tag+'_all12_velocities',data['y'][0],[float(v) for v in y]))
                errs.append(compare(ch,tag+'_psi_velocity',data['psi_hat'][0],float(ps)))
                errs.append(compare(ch,tag+'_full_energy_including_eliminated_dust',energy[0],float(Ereference)))
                errs.append(compare(ch,tag+'_lapse_gradient_flux',flux[0],float(fluxreference)))
                expected=[2*c['K'][i,j] for i,j in parent.HM]+list(c['X'])+[c['proper'][n] for n in ('u','v','r')]+[ps,zs,td]
                for j in range(15):
                    perturbed=p.astype(complex);perturbed[0,j]+=1j*1e-20
                    ep=parent.full_blocks(q,hi,grad,DV,perturbed,pn,R3)[0][0]
                    observed=np.imag(ep)/1e-20
                    errs.append(compare(ch,tag+'_canonical_momentum_derivative_'+parent.FIELDS[j],observed,float(expected[j])))
                cases.append(dict(seed=seed,family=family,eta=eta,maximum_binary64_discrepancy=max(errs),
                    reference_momentum_error=mp.nstr(ref_error,45),scope='independent full density to numerical Hamiltonian bridge; not physical initial-data admission'))
    _,after=inputs();ch.add('all_original_metadata_preserved',before==after)
    ok=all(r['passed'] for r in ch.rows)
    summary=dict(validation='PASS_ORIGINAL_DENSITY_BACKEND_BRIDGE_ONLY' if ok else 'FAIL_ORIGINAL_DENSITY_BACKEND_BRIDGE',
        passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,cases=cases,
        source_sha256=pins,source_metadata=before,precision_reference=80,tolerance_binary64='1e-10',
        physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
        stage2_complete=False,stage3_entered=False,general_3D_constraint_closure_proved=False,
        status='BACKEND_IDENTIFICATION_ONLY_PHYSICAL_REDUCTION_AND_DOMAIN_OPEN')
    return summary

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');ap.add_argument('--replay');args=ap.parse_args()
    if bool(args.output)==bool(args.replay):ap.error('choose one fresh output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('unsafe output path')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    original={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    su=calculate();b=ENC(su);payloads={'verification.json':b,'verification.json.sha256':(SHA(b)+'  verification.json\n').encode()}
    for name,data in payloads.items():
        p=dest/name
        if args.replay:
            if p.read_bytes()!=data:raise ValueError('replay mismatch '+name)
            if (SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns)!=original[name]:raise ValueError('metadata changed '+name)
        else:
            with p.open('xb') as f:f.write(data)
    if args.replay:
        if set(original)!=set(payloads):raise ValueError('replay set mismatch')
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    print(json.dumps({k:su[k] for k in ('validation','passed','total','physics_pass')}),flush=True)
    return int(su['passed']!=su['total'])

if __name__=='__main__':raise SystemExit(main())
