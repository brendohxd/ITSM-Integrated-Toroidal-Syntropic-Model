"""Independent coordinate-current check of the scalar quadratic normal trace."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_SECOND_NODE_SCALAR_TRACE_VERIFIER_V1_CONTRACT_2026-10-27.md'
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))


def control(case,orientation):
    mp.mp.dps=80
    H=mp.mpf(case+2)/17;HB=mp.mpf(case+1)/19;U=mp.mpf(3+case)/23;Ud=mp.mpf(5+case)/29
    p=mp.mpf(2+case)/31;K=mp.mpf(4+case)/37;b=mp.mpf(3)/41;beta=mp.mpf(2)/43
    slope=orientation*mp.mpf(2+case)/7;k=mp.mpf(3+case)
    r1=mp.mpf(1)/47;r3=mp.mpf(2)/53;ty=mp.mpf(3)/59
    a0=mp.mpf(4)/61;a2=mp.mpf(5)/67;az=mp.mpf(6)/71;rho2=mp.mpf(7)/73
    def psi(t,z):return p*t+(a0+a2*z*z)*t*t/2+t**3/79+t**4/83
    def Z(t,z):
        w=slope*mp.sin(k*z)/k
        return U*w*w+Ud*w*w*t+az*t*t/2+t**3/89
    def fields(t,z):
        h=mp.eye(3)
        for j,(a,c) in enumerate(HM):
            value=(2*H*t if a==c else 0)+t*t*(mp.mpf(j+case+1)/97+mp.mpf(j+1)*z/101)/2
            h[a,c]+=value
            if a!=c:h[c,a]+=value
        S=mp.matrix([z/103,ty*z+z**3/107,r1*z+r3*z**3/6])
        w=slope*mp.sin(k*z)/k
        V=mp.matrix([t*t*(1+z)/109,w*(1-HB*t)+t*t*(mp.mpf(1)/113+z/127)/2,
                     t*t*(mp.mpf(1)/131+z/137)/2])
        gam=mp.sqrt(1+(V.T*h*V)[0]);g=mp.matrix(4);g[0,0]=-1+(S.T*h*S)[0];hs=h*S
        for i in range(3):
            g[0,i+1]=g[i+1,0]=hs[i]
            for j in range(3):g[i+1,j+1]=h[i,j]
        return g,mp.matrix([gam]+list(V-gam*S)),mp.sqrt(mp.det(h))
    def current(t,z):
        g,n,vol=fields(t,z);gi=g**-1;hp=gi+n*n.T
        dg={0:mp.diff(lambda u:fields(u,z)[0],t),3:mp.diff(lambda u:fields(t,u)[0],z)}
        dn={0:mp.diff(lambda u:fields(u,z)[1],t),3:mp.diff(lambda u:fields(t,u)[1],z)}
        cov=n[0]*dg[0]*n+n[3]*dg[3]*n
        for i in (0,3):cov[i]-=(n.T*dg[i]*n)[0]/2
        acc=n[0]*dn[0]+n[3]*dn[3]+gi*cov
        gp=mp.matrix([mp.diff(lambda u:psi(u,z),t),0,0,mp.diff(lambda u:psi(t,u),z)])
        gz=mp.matrix([mp.diff(lambda u:Z(u,z),t),0,0,mp.diff(lambda u:Z(t,u),z)])
        J=K*n*(n.T*gp)[0]-b*(hp*gz+Z(t,z)*acc)
        return vol*J,vol
    def equation(t,z):
        divergence=mp.diff(lambda u:current(u,z)[0][0],t)+mp.diff(lambda u:current(t,u)[0][3],z)
        return -divergence/current(t,z)[1]-beta*(mp.mpf(11)/139+rho2*z*z)
    got=mp.diff(lambda z:equation(mp.mpf(0),z),mp.mpf(0),2)/2
    ss=slope*slope
    expected=b*ss*az-K*(a2+ss*a0)-K*p*(-r3/2+(5*H-2*HB-3*r1)*ss)\
        -4*b*U*ss*k*k-3*b*U*ty*slope**3-beta*rho2
    err=abs(got-expected)/(1+abs(got)+abs(expected))
    return dict(case=case,orientation=orientation,got=mp.nstr(got,65),expected=mp.nstr(expected,65),
        passed=bool(err<mp.mpf('1e-30')),normalized_error=mp.nstr(err,65))


def calculate():
    rows=[control(case,orientation) for case in (0,1) for orientation in (-1,1)]
    checks=[dict(name=f'original_scalar_normal_trace_{r["case"]}_{r["orientation"]}',
                 passed=r['passed'],value=r['normalized_error'],criterion='normalized < 1e-30') for r in rows]
    return dict(result_id='R4C1-SECOND-NODE-SCALAR-TRACE-INDEPENDENT-V1',checks=checks,
        passed=sum(c['passed'] for c in checks),total=len(checks),controls=rows,
        source_sha256={name:SHA((ROOT/name).read_bytes()) for name in (CONTRACT,Path(__file__).relative_to(ROOT).as_posix())},
        mpmath=mp.__version__,physics_pass=False,G1_complete=False,gate_effect='NONE',review_status='DEFERRED',
        scope='Original scalar current quadratic normal coefficient; cusp composite order >=3; no physical admission')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path);a=parser.parse_args()
    result=calculate();data=ENC(result);directory=a.replay or a.output
    if a.replay:
        if (directory/'independent.json').read_bytes()!=data:raise ValueError('immutable replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False);p=directory/'independent.json';p.write_bytes(data)
        Path(str(p)+'.sha256').write_text(SHA(data)+'  independent.json\n',encoding='ascii')
    print(json.dumps({k:result[k] for k in ('passed','total','G1_complete')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
