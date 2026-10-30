"""Independent one-form controls V2: fixes V1 vector allocation only."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
ENC=lambda x:(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_SECTOR_READINESS_V1_CONTRACT_2026-10-27.md'
ADDENDUM='Theory/Gates/RES-001/RES001_R4C1_PHYSICAL_SECTOR_RANGE_V1_ADDENDUM_2026-10-27.md'
HM=((0,0),(0,1),(0,2),(1,1),(1,2),(2,2))


def geometry(X):
    h=mp.matrix(3)
    for value,(i,j) in zip(X[:6],HM):h[i,j]=h[j,i]=value
    V=mp.matrix(X[6:9]);return h,V


def one_form(X,b):
    h,V=geometry(X);g=b*mp.sqrt(mp.det(h))*(V.T*h*V)[0]
    return mp.matrix(list(X[9:18])+[mp.mpf(0)]*9+[-g*X[19],mp.mpf(0)])


def assembled(X,b):
    h,V=geometry(X);hi=h**-1;vol=mp.sqrt(mp.det(h));c=(V.T*h*V)[0]
    g=b*vol*c;grad=[]
    for i,j in HM:
        E=mp.matrix(3);E[i,j]=E[j,i]=1
        trace=sum(hi[a,z]*E[z,a] for a in range(3) for z in range(3))
        grad.append(b*vol*(c*trace/2+(V.T*E*V)[0]))
    grad+=list(2*b*vol*h*V)
    O=mp.matrix(20)
    for i in range(9):
        O[i,9+i]=-1;O[9+i,i]=1
        O[i,18]=-X[19]*grad[i];O[18,i]=X[19]*grad[i]
    O[18,19]=g;O[19,18]=-g
    return O,g,grad


def shifted(X,v,step):return [x+step*y for x,y in zip(X,v)]
def norm(A):return max(abs(x) for x in A)
def error(A,B):return norm(A-B)/(1+norm(A)+norm(B))


def calculate():
    mp.mp.dps=70;checks=[];records=[];tol=mp.mpf('1e-8')
    def check(name,passed,value):
        checks.append(dict(name=name,passed=bool(passed),value=mp.nstr(value,35)))
    for case in range(3):
        L=mp.matrix([[1+mp.mpf(case)/10,0,0],[mp.mpf(1)/11,1,0],
                     [-mp.mpf(1)/13,mp.mpf(1)/17,1+mp.mpf(case)/20]])
        h=L*L.T;V=[mp.mpf(1+case)/5,-mp.mpf(1)/7,mp.mpf(1)/9]
        X=[h[i,j] for i,j in HM]+V+[mp.mpf(j+1)/31 for j in range(9)]+[mp.mpf(2)/7,mp.mpf(1)/20]
        b=mp.mpf(case+1)/3;O,g,grad=assembled(X,b)
        r=mp.matrix([mp.mpf((-1)**j*(j+1))/23 for j in range(20)])
        v=mp.matrix(20,1)
        for j in range(9):
            v[j]=r[9+j];v[9+j]=-r[j]+X[19]*grad[j]*r[19]/g
        v[18]=-r[19]/g
        v[19]=(r[18]-X[19]*sum(grad[j]*r[9+j] for j in range(9)))/g
        T=mp.matrix([mp.mpf((-1)**(j+1)*(j+2))/71 for j in range(20)])
        H=mp.eye(20)
        for i in range(20):
            for j in range(20):H[i,j]+=mp.mpf((-1)**(i+j)*(i+1)*(j+1))/1000
        for step_text in ('1e-5','1e-6'):
            step=mp.mpf(step_text);columns=[];drift_columns=[]
            for j in range(20):
                unit=[mp.mpf(0)]*20;unit[j]=1
                xp=shifted(X,unit,step);xm=shifted(X,unit,-step)
                columns.append((one_form(xp,b)-one_form(xm,b))/(2*step))
                drift_columns.append((assembled(xp,b)[0]-assembled(xm,b)[0])*T/(2*step))
            jac=mp.matrix([[columns[j][i] for j in range(20)] for i in range(20)])
            fd=jac.T-jac
            direct=mp.lu_solve(fd,r)
            D=mp.matrix([[drift_columns[j][i] for j in range(20)] for i in range(20)])
            odot=(assembled(shifted(X,T,step),b)[0]-assembled(shifted(X,T,-step),b)[0])/(2*step)
            K=H-D
            values=dict(two_form=error(fd,O),inverse=error(direct,v),
                        drift_balance=norm(K-K.T+odot)/(1+norm(K)+norm(odot)))
            for name,value in values.items():check(f'{case}_{step_text}_{name}',value<tol,value)
            records.append(dict(case=case,step=step_text,
                errors={name:mp.nstr(value,35) for name,value in values.items()}))
        cross=O.copy()
        for j in range(18):cross[j,18]=cross[18,j]=0
        cross_error=norm(cross*v-r)
        check(f'{case}_cross_deletion_rejected',cross_error>tol,cross_error)
        check(f'{case}_drift_deletion_rejected',norm(odot)>tol,norm(odot))
        aligned=X.copy();aligned[6:9]=[mp.mpf(0)]*3
        On,gn,_=assembled(aligned,b)
        null=max(abs(On[i,j]) for i in (18,19) for j in range(20))
        check(f'{case}_alignment_null_rows',gn==0 and null==0,null)
    names=[CONTRACT,ADDENDUM,Path(__file__).relative_to(ROOT).as_posix(),
           'Analysis/MasterTests/test_01_r4c1_coupled_descriptor_action_v1.py',
           'Analysis/MasterTests/test_01_r4c1_material_seed_feasibility_v1.py']
    return dict(result_id='R4C1-PHYSICAL-SECTOR-RANGE-V1-INDEPENDENT',
        scope='Local full-metric geometry method controls, NOT a restored on-shell R4C1 perturbation',
        source_hashes={name:SHA((ROOT/name).read_bytes()) for name in names},
        mpmath=mp.__version__,checks=checks,records=records,
        passed=sum(c['passed'] for c in checks),total=len(checks),physics_pass=False,
        gate_effect='NONE',review_status='DEFERRED')


def main():
    parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path);group.add_argument('--replay',type=Path)
    args=parser.parse_args();result=calculate();data=ENC(result);directory=args.replay or args.output
    if args.replay:
        if (directory/'independent.json').read_bytes()!=data:raise ValueError('replay mismatch')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        directory.mkdir(parents=True,exist_ok=False)
        path=directory/'independent.json';path.write_bytes(data)
        Path(str(path)+'.sha256').write_text(SHA(data)+'  independent.json\n',encoding='ascii')
    print(json.dumps({key:result[key] for key in ('passed','total','physics_pass')}))
    raise SystemExit(0 if result['passed']==result['total'] else 2)


if __name__=='__main__':main()
