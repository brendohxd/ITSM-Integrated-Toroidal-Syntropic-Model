"""Correct general geometry; preserve V1 and its initial-only transport result."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
PRIOR='Analysis/MasterTests/test_01_r4c1_node_velocity_transport_v1.py'
PRIOR_SHA='2b5bee3d625fcd08299cf2c5b553bf8259b9a1635d7d174d5f0950b31131d6e1'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_NODE_VELOCITY_TRANSPORT_V2_GEOMETRY_ADDENDUM_2026-10-18.md'
PREVIOUS='Analysis/MasterTests/outputs/r4c1_node_velocity_transport_attempt_01/'
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
ENC=lambda data:(json.dumps(data,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
if SHA((ROOT/PRIOR).read_bytes())!=PRIOR_SHA:raise ValueError('V1 source drift before utility import')
spec=importlib.util.spec_from_file_location('frozen_node_transport_v1',ROOT/PRIOR)
v1=importlib.util.module_from_spec(spec);spec.loader.exec_module(v1)
PINS=dict(v1.PINS)
PINS.update({PRIOR:PRIOR_SHA,
    CONTRACT:'8fd754f649fb34829018745bb933347035b4c73f7c6b43112140e0b1eeb471e9',
    PREVIOUS+'summary.json':'a538aebe507842eaca7e0cc912a1683ba4fe0901bc4db242715867313fa770b4',
    PREVIOUS+'equations.json':'de011d87cb18405e1bb690ea17830ffb66fb613eeb40ffc1f3ad03ba70978588',
    PREVIOUS+'independent.json':'f9c32607bfa222ccde1cadd0890c5670e058bbbe0137249ca84bc8ba25b1b6da',
    PREVIOUS+'cases.json':'9fbc226db2b9bdd983bad2b2e4f3a6b64c28469700d944a04e73a5f44c626c39'})


def sources():
    pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());metadata={}
    for name,digest in pins.items():
        path=ROOT/name;side=Path(str(path)+'.sha256')
        if SHA(path.read_bytes())!=digest:raise ValueError('source hash drift '+name)
        if side.read_text().split()[0].lower()!=digest:raise ValueError('source sidecar mismatch '+name)
        for p in (path,side):
            raw=p.read_bytes();metadata[p.relative_to(ROOT).as_posix()]=dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=p.stat().st_mtime_ns)
    return pins,metadata


def general_geometry(ch,equations):
    print('CORRECT_GENERAL_VOLUME_GRADIENT_BEFORE_INITIAL_RESTRICTION',flush=True)
    c,ct,cz,lt,lz,g,R,Rz,vz,vzz,kvv=s.symbols('c c_t c_z volume_t volume_z gamma R R_z Vz Vz_z KVV',real=True)
    divergence=ct+c*lt-R*cz-c*Rz+cz*vz/(2*g)+g*vzz+lz*(-c*R+g*vz)
    acceleration=ct/2-R*cz/2+vz*cz/(2*g)+kvv
    complete=ct/2+c*(lt-Rz)-R*cz/2+g*vzz-kvv+(g*vz-c*R)*lz
    ch.zero('arbitrary_first_jet_full_volume_product_rule',divergence-acceleration-complete)
    old=complete-(g*vz-c*R)*lz
    ch.add('reject_general_volume_gradient_deletion',s.diff(complete-old,lz)!=0)
    lzt,Bt=s.symbols('volume_zt prefactor_t',real=True)
    ch.zero('omitted_term_and_time_jet_vanish_only_on_registered_slice',[
        ((g*vz-c*R)*lz).subs(lz,0),(Bt*lz+(g*vz-c*R)*lzt).subs({lz:0,lzt:0})])
    equations['C_initial_restricted']=equations.pop('C_general')
    equations['C_general']=str(complete)
    equations['V1_general_label_error']='V1 omitted (gamma*Vz-V^2*R)*partial_z(log sqrt(h)); V1 source and receipts are preserved, not relabeled as a valid general expression.'
    equations['initial_geometry_restriction']='volume_z=volume_zt=0 because h_z=h_dot_z=0 initially; no such restriction is imposed during future evolution.'


def general_coordinate_controls(ch):
    print('ARBITRARY_METRIC_FIRST_JETS_INDEPENDENT_CONNECTION_CONTROLS',flush=True)
    records=[]
    for seed in (0,1):
        for orientation in (-1,1):
            h=mp.matrix([[mp.mpf(4+i)/3 if i==j else mp.mpf(i+j+1)/47 for j in range(3)] for i in range(3)])
            hi=h**-1
            ht=mp.matrix([[mp.mpf(1+i+j+seed)/19 for j in range(3)] for i in range(3)])
            hz=mp.matrix([[mp.mpf(2+i+j)/23 for j in range(3)] for i in range(3)])
            shift=mp.matrix([mp.mpf(1)/13,-mp.mpf(2)/17,mp.mpf(3)/29])
            st=mp.matrix([mp.mpf(2)/31,mp.mpf(1)/37,-mp.mpf(3)/41])
            sz=mp.matrix([-mp.mpf(2)/43,mp.mpf(1)/47,mp.mpf(3)/53])
            V=mp.matrix([mp.mpf(1)/5,mp.mpf(orientation)/7,mp.mpf(2+seed)/11])
            vt=mp.matrix([mp.mpf(1)/17,-mp.mpf(2)/19,mp.mpf(1)/23])
            vz=mp.matrix([mp.mpf(2)/29,mp.mpf(1)/31,-mp.mpf(2)/37])
            c=(V.T*h*V)[0];gam=mp.sqrt(1+c);n=mp.matrix([gam]+list(V-gam*shift))
            g=mp.zeros(4);gi=mp.zeros(4);g[0,0]=-1+(shift.T*h*shift)[0];gi[0,0]=-1
            for i in range(3):
                g[0,i+1]=g[i+1,0]=(h*shift)[i];gi[0,i+1]=gi[i+1,0]=shift[i]
                for j in range(3):g[i+1,j+1]=h[i,j];gi[i+1,j+1]=hi[i,j]-shift[i]*shift[j]
            dg=[];dn=mp.zeros(4)
            for mu in range(4):
                hh,sv,vv=(ht,st,vt) if mu==0 else (hz,sz,vz) if mu==3 else (mp.zeros(3),mp.zeros(3,1),mp.zeros(3,1))
                gm=((V.T*hh*V)[0]+2*(V.T*h*vv)[0])/(2*gam)
                dm=mp.zeros(4);dm[0,0]=2*(sv.T*h*shift)[0]+(shift.T*hh*shift)[0]
                hs=hh*shift+h*sv;dn[mu,0]=gm
                for i in range(3):
                    dm[0,i+1]=dm[i+1,0]=hs[i];dn[mu,i+1]=vv[i]-gm*shift[i]-gam*sv[i]
                    for j in range(3):dm[i+1,j+1]=hh[i,j]
                dg.append(dm)
            conn=[[[sum(gi[k,l]*(dg[a][l,b]+dg[b][l,a]-dg[l][a,b]) for l in range(4))/2 for b in range(4)] for a in range(4)] for k in range(4)]
            theta=sum(dn[a,a]+sum(conn[a][a][b]*n[b] for b in range(4)) for a in range(4))
            hp=gi+n*n.T
            actual=theta*gam-sum(hp[a,b]*conn[0][a][b] for a in range(4) for b in range(4))
            lt=sum((hi*ht)[i,i] for i in range(3))/2
            lz=sum((hi*hz)[i,i] for i in range(3))/2
            ct=(V.T*ht*V)[0]+2*(V.T*h*vt)[0];cz=(V.T*hz*V)[0]+2*(V.T*h*vz)[0]
            lie=shift[2]*hz
            for i in range(3):
                for j in range(3):lie[i,j]+=sum(h[k,j]*sz[k] for k in range(3))*(1 if i==2 else 0)+sum(h[i,k]*sz[k] for k in range(3))*(1 if j==2 else 0)
            K=(ht-lie)/2;term=(gam*V[2]-c*shift[2])*lz
            expected=ct/2+c*(lt-sz[2])-shift[2]*cz/2+gam*vz[2]-(V.T*K*V)[0]+term
            error=abs(actual-expected)/(1+abs(actual)+abs(expected))
            ch.small('full_coordinate_general_C_'+str(seed)+'_'+str(orientation),error,'1e-60')
            ch.add('nonzero_volume_term_exercises_rejection_'+str(seed)+'_'+str(orientation),abs(term)>mp.mpf('1e-5'))
            records.append(dict(seed=seed,orientation=orientation,normalized_error=v1.SHOW(error),previously_omitted_term=v1.SHOW(term)))
    return records


def calculate():
    mp.mp.dps=100;mp.iv.dps=80
    pins,before=sources();ch=v1.base.Checks()
    equations=v1.derive(ch);general_geometry(ch,equations)
    control=v1.coordinate_controls(ch);general=general_coordinate_controls(ch);cases=v1.required_case_enclosures(ch)
    ch.add('V1_initial_coordinate_controls_recomputed_exact',ENC(control)==(ROOT/(PREVIOUS+'independent.json')).read_bytes())
    ch.add('V1_necessary_slope_enclosures_recomputed_exact',ENC(cases)==(ROOT/(PREVIOUS+'cases.json')).read_bytes())
    _,after=sources();ch.add('all_source_bytes_sidecars_metadata_unchanged',before==after)
    summary=v1.READ(PREVIOUS+'summary.json')
    summary.update(validation='PASS_CORRECTED_NODE_VELOCITY_TRANSPORT_ONLY' if all(r['passed'] for r in ch.rows) else 'FAIL_OR_UNRESOLVED_NODE_TRANSPORT_V2',
                   passed=sum(r['passed'] for r in ch.rows),total=len(ch.rows),checks=ch.rows,
                   source_sha256=pins,source_metadata=before,V1_general_label_error_preserved_and_corrected=True)
    return {'summary.json':summary,'equations.json':equations,'independent.json':dict(initial_time_controls=control,general_first_jet_controls=general),'cases.json':cases}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output');parser.add_argument('--replay');args=parser.parse_args()
    if bool(args.output)==bool(args.replay):parser.error('choose exactly one output or read-only replay')
    dest=(ROOT/(args.output or args.replay)).resolve()
    if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside science output root')
    if args.output:dest.mkdir(parents=True,exist_ok=False)
    original={p.name:(SHA(p.read_bytes()),p.stat().st_size,p.stat().st_mtime_ns) for p in dest.iterdir()} if args.replay else None
    results=calculate();payloads={name:ENC(value) for name,value in results.items()}
    for name,raw in list(payloads.items()):payloads[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode('ascii')
    if args.replay:
        if set(original)!=set(payloads):raise ValueError('replay file-set mismatch')
        for name,raw in payloads.items():
            path=dest/name
            if path.read_bytes()!=raw:raise ValueError('recomputed bytes differ '+name)
            if (SHA(path.read_bytes()),path.stat().st_size,path.stat().st_mtime_ns)!=original[name]:raise ValueError('original metadata changed '+name)
        print('READ_ONLY_REPLAY_EXACT',flush=True)
    else:
        for name,raw in payloads.items():
            with (dest/name).open('xb') as stream:stream.write(raw)
    su=results['summary.json'];print(json.dumps({n:su[n] for n in ('validation','passed','total','selected_regulator_velocity','status')}),flush=True)
    return 0 if su['passed']==su['total'] else 1


if __name__=='__main__':raise SystemExit(main())
