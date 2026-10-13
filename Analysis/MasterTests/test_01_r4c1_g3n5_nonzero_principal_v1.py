"""Separate real-space principal-density derivation; no full-kernel import."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
BASE = 'Analysis/MasterTests/outputs/'


def derive():
    p = s.Symbol('p', positive=True)
    w, c, sig = s.symbols('omega c sigma', real=True)
    u, v, ps = s.symbols('u0 v0 psi_dot', real=True)
    h, V, Pi, ht, Vt, Pit, hx, Vx, Pix, Pixx, sx, z = s.symbols(
        'h V Pi ht Vt Pit hx Vx Pix Pixx sx z', real=True)
    MP, mu123, mu14, beta, b, K = (s.Rational(x) for x in
                                  ('1', '1/15', '1/6', '2/5', '5/11', '3'))
    # Spatially flat gauge M_xi=0; h=(M_yy+M_zz)/sqrt(2), T=0.
    # sx means d_x S_x/a. Variation w.r.t. S_x allows this algebraic
    # equation ONLY for nonzero Fourier modes; no k=0 inference is made.
    EH = -MP*ht**2/8 + MP*ht*sx/s.sqrt(2) + MP*hx**2/8 - MP*beta*hx*Pix/s.sqrt(2)
    frame = mu14*(Vt-beta*Pix)**2/2 - mu123*(ht/s.sqrt(2)+Vx-sx)**2/2
    force = K*Pit**2/2
    # Exact periodic integration by parts of -b Z_x(Pi_x+psi_dot V).
    reg = b*z**2/2 + b*z*(Pixx+ps*Vx)
    before = EH + frame + force + reg
    sx_sol = s.solve(s.diff(before, sx), sx)[0]
    z_sol = s.solve(s.diff(before, z), z)[0]
    density = s.expand(before.subs({sx: sx_sol, z: z_sol}))
    jets = (h, V, Pi, ht, Vt, Pit, hx, Vx, Pix, Pixx)
    Hess = s.hessian(density, jets)
    Q, D = s.zeros(10, 3), s.zeros(10, 3)
    for j in range(3):
        Q[j, j] = 1
        D[j+3, j] = 1
        Q[j+6, j] = s.I*p
    Q[9, 2] = -p*p
    A = s.expand(Q.conjugate().T*Hess*Q)
    R = s.expand(D.conjugate().T*Hess*Q)
    KK = D.T*Hess*D
    pencil = s.expand(KK*w*w - s.I*w*(R.conjugate().T-R) + A)
    det = s.factor(pencil.det())
    wave = s.factor(s.expand(det.subs(w, c*p)).coeff(p, 8))
    fast = s.factor(s.expand(det.subs(w, sig*p*p)).coeff(p, 12))
    # Slow chi=Pi-i*psi_dot*V/p removes only the leading regulator square.
    # For omega~p the chi block is eliminated at leading order, not dropped.
    wave2 = s.Matrix([[s.Rational(33,4)*c*c+s.Rational(1,4), -c/s.sqrt(2)],
                      [-c/s.sqrt(2), c*c/6]])
    Kw = s.diag(s.Rational(33,4), s.Rational(1,6))
    Aw = s.diag(s.Rational(1,4), 0)
    Gw = s.Matrix([[0, -s.I/s.sqrt(2)], [-s.I/s.sqrt(2), 0]])
    companion = s.zeros(4)
    companion[:2,2:] = s.eye(2)
    companion[2:,:2] = -Kw.inv()*Aw
    companion[2:,2:] = s.I*Kw.inv()*Gw
    # V_0 is the zero-speed eigenvector. This exact chain proves a defect.
    e0 = s.Matrix([0, 1, 0, 0])
    e1 = s.Matrix([2*s.sqrt(2), 0, 0, 1])
    # Pure TT and transverse-frame densities give their K/A coefficients.
    Kother = s.diag(s.Rational(1,4), s.Rational(1,2), s.Rational(1,6),
                    s.Rational(1,6), 1, 1, 1)
    Gmatter = s.Matrix([[1+v*v/13, -u*v/13, 0],
                       [-u*v/13, 1+u*u/13, 0], [0,0,1]])
    Aother = s.diag(-p*p/4, -p*p/2, -2*p*p/15, -2*p*p/15, -Gmatter*p*p)
    return dict(p=p,omega=w,c=c,sigma=sig,u=u,v=v,psi_dot=ps,
                density_before=before,density=density,shift_solution=sx_sol,
                regulator_solution=z_sol,A=A,R=R,K=KK,pencil=pencil,
                determinant=det,wave_leading=wave,fast_leading=fast,
                wave2=wave2,companion=companion,zero=e0,generalized=e1,
                Kother=Kother,Aother=Aother,Gmatter=Gmatter)


def encode(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def calculate():
    d = derive()
    rows=[]
    def exact(name, expr):
        values = list(expr) if isinstance(expr,s.MatrixBase) else [expr]
        bad=[str(s.simplify(q)) for q in values if s.simplify(q)!=0]
        rows.append(dict(name=name,passed=not bad,value=bad,criterion='zero_exact'))
    p,c,sig=d['p'],d['c'],d['sigma']
    exact('scalar_wave_factor', d['wave_leading'] + s.Rational(5,24)*c*c*(3*c*c-1))
    exact('scalar_fast_factor', d['fast_leading'] - s.Rational(11,8)*sig**4*(3*sig*sig-s.Rational(5,11)))
    exact('wave_pencil_determinant',d['wave2'].det()-s.Rational(11,24)*c*c*(3*c*c-1))
    exact('companion_characteristic_factor',d['companion'].charpoly(c).as_expr()-c*c*(c*c-s.Rational(1,3)))
    exact('zero_eigenvector',d['companion']*d['zero'])
    exact('nontrivial_Jordan_chain',d['companion']*d['generalized']-d['zero'])
    exact('matter_characteristic_factor',d['Gmatter'].charpoly(c).as_expr()-(c-1)**2*(c-1-(d['u']**2+d['v']**2)/13))
    rows.append(dict(name='zero_geometric_multiplicity',passed=len(d['companion'].nullspace())==1,value=1,criterion='1 with algebraic multiplicity 2'))
    exact('slow_effective_time_coefficient',d['K'][1,1]-s.Rational(1,2)/s.Rational(1,4)+s.Rational(11,6))
    payload = {k:(str(v) if not isinstance(v,s.MatrixBase) else
                    {'shape':list(v.shape),'entries':[[str(x) for x in v.row(i)] for i in range(v.rows)]})
               for k,v in d.items() if k not in ('p','omega','c','sigma','u','v','psi_dot')}
    summary=dict(schema='r4c1-g3n5-nonzero-principal-v1',passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,
                 physics_pass=False,gate_effect='NONE',Rule9_cleared=False,review_status='DEFERRED',
                 status='LOCAL_PRINCIPAL_DENSITY_WITH_ZERO_SPEED_JORDAN_OBSTRUCTION',
                 source_sha256={SELF:hashlib.sha256((ROOT/SELF).read_bytes()).hexdigest()},
                 nonclaim='Separate local derivation by the same agent, not an external reviewer')
    summary['validation']='PASS_LOCAL_CHECKS' if summary['passed']==summary['total'] else 'FAIL_LOCAL_CHECKS'
    data={'formulas.json':encode(payload)}
    summary['artifacts']={k:hashlib.sha256(v).hexdigest() for k,v in data.items()}
    data['summary.json']=encode(summary)
    return data,summary


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_nonzero_principal_attempt_01')
    ap.add_argument('--replay')
    a=ap.parse_args(); dest=(ROOT/(a.replay or a.output)).resolve();dest.relative_to((ROOT/BASE).resolve())
    if not a.replay and dest.exists():raise FileExistsError('Refuse existing output')
    if a.replay and not dest.is_dir():raise FileNotFoundError('Replay absent')
    data,summary=calculate()
    if a.replay:
        for name,body in data.items():
            assert (dest/name).read_bytes()==body
            assert (dest/(name+'.sha256')).read_bytes()==(hashlib.sha256(body).hexdigest()+'  '+name+'\n').encode()
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in data.items():
            with (dest/name).open('xb') as f:f.write(body)
            with (dest/(name+'.sha256')).open('xb') as f:f.write((hashlib.sha256(body).hexdigest()+'  '+name+'\n').encode())
    print(json.dumps(dict(action='READ_ONLY_REPLAY_EXACT' if a.replay else 'NEW_RECEIPTS_WRITTEN',**{k:summary[k] for k in ('passed','total','validation','status','physics_pass','gate_effect')})))
    for row in summary['checks']:
        if not row['passed']:print(json.dumps(row))
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':raise SystemExit(main())
