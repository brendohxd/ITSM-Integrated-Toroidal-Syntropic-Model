"""Independent force/current bindings and integrity audit of CUSP3 evolution V1."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
import sympy as s

import test_01_r4c1_cusp3_evolution_v1 as ev

ROOT=ev.ROOT
FORCE=ev.BASE+'r4c1_g3n4_force_attempt_01/formulas.json'
CHARGE=ev.BASE+'r4c1_three_family_charge_domain_attempt_05/canonical.json'
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()


def calculate(directory):
    summary=ev.READ(directory+'/summary.json');checks=ev.Checks()
    checks.add('all18_required_not_canary',not summary['canary_only'] and summary['case_count']==18)
    checks.add('accepted_primary_controls',summary['passed']==summary['total'])
    records=ev.READ(directory+'/trajectories.json')['runs']
    for name,digest in {**summary['source_sha256'],**{directory+'/'+n:h for n,h in summary['artifacts'].items()}}.items():
        actual=ev.SHA((ROOT/name).read_bytes())
        checks.add('hash_'+name,actual==digest,actual)
    # Direct force uses the original nonanalytic Euler export, not a copied source formula.
    force=ev.READ(FORCE);x={n:s.Symbol(n,real=True) for n in ('A','W','Wt','p','pdd','H','e')}
    force_expr=[s.sympify(force['Euler_sources'][n],locals={**x,'Abs':s.Abs}).subs(x['e'],1)
                if force['directional_degree'][n]==3 else s.Integer(0) for n in ev.FIELDS]
    fun=s.lambdify([x[n] for n in ('A','W','Wt','p','pdd','H')],force_expr,'numpy',cse=True)
    pins,absent,snapshot,g,prior,time=ev.inputs();before=snapshot()
    src=ev.Sources(checks);red=time.EvolvingReduction(prior,g)
    for ir,run in enumerate(records):
        p=g.bg.PARAMS.copy();ef=float(s.Rational(run['eta_exact']))
        for n,expr in ev.READ(ev.PLANAR)['families'][run['family']]['parameter_map'].items():
            p['K' if n=='K_Q' else n]=float(s.sympify(expr).subs(s.Symbol('eta'),s.Rational(run['eta_exact'])))
        p['gr']=3*ef/7
        maxima=0.
        for inode in (0,10,20):
            b=np.asarray(run['first_order_states'][inode],float)
            c=src.context(g,red,b,p)
            expected=np.asarray(fun(p['A'],b[12],b[13],b[9],c['rate'][9],b[1]),complex)
            for mode in (0,2):
                _,_,extra=src.source(c,b,p,mode,ef**3.5)
                m=mode//2;hm=12*(-1)**m/(np.pi*(4*m*m-1)*(4*m*m-9))
                actual=extra['direct'][:22]*(ef**3.5)/hm
                maxima=max(maxima,float(np.max(abs(actual-expected)/(1e-30+abs(actual)+abs(expected)))))
        checks.small('run'+str(ir)+'_original_force_export_both_signs',maxima,1e-12)
    # Bind the angular-current expression from the sealed canonical affine row.
    # The homogeneous metric response is unrestricted; subtract the explicit
    # leading-W^2 current offset before comparing the entire 26-vector.
    canonical=ev.READ(CHARGE)
    checks.add('canonical13_field_order',tuple(canonical['physical_fields'])==ev.FIELDS[4:17])
    names=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*',canonical['Q2_affine']))-{'Matrix'}
    names.update('a u0 v0 u_dot v_dot beta psi_dot H C rho w zeta'.split())
    qx={n:s.Symbol(n,real=True) for n in names}
    row=s.sympify(canonical['Q2_affine'],locals={**qx,'Matrix':s.Matrix})
    z=s.symbols('z0:26',real=True);dyn=ev.FIELDS[4:17]
    pos=dict(zip(dyn,z[:13]));vel=dict(zip(dyn,z[13:]));J=qx['u0']*qx['v_dot']-qx['v0']*qx['u_dot']
    trace=sum(pos[n] for n in ('Mxx','Myy','Mzz'))/2
    expected=qx['a']**3*(qx['u0']*vel['dv']+pos['du']*qx['v_dot']-
        qx['v0']*vel['du']-pos['dv']*qx['u_dot']+(trace+qx['beta']*pos['Pi'])*J)
    checks.exact('independent_angular_linear_current_from_canonical_row',(row[:,:26]*s.Matrix(z))[0]-expected)
    # Cross term is polarization of the original quadratic angular offset.
    w,r=s.symbols('w r',real=True)
    mixed=2*s.diff(row[26],qx['w'],2)*w*r
    desired=-2*qx['a']**3*qx['zeta']*(qx['u0']**2+qx['v0']**2)*J*w*r
    checks.exact('mixed_current_from_original_cosine_normalized_offset',mixed-desired)
    checks.add('scope_remains_physics_hold',summary['physics_pass'] is False and summary['gate_effect']=='NONE' and not summary['stage2_complete'])
    checks.add('no_goal_resume',summary['native_goal_resumed'] is False)
    checks.add('sources_metadata_unchanged',before==snapshot())
    tree=ast.parse((ROOT/ev.SELF).read_text())
    system=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='System')
    rhs=next(n for n in system.body if isinstance(n,ast.FunctionDef) and n.name=='rhs')
    checks.add('rhs_is_affine_flow_not_charge_reset',isinstance(rhs.body[-1],ast.Return) and
               ast.unparse(rhs.body[-1].value)=="data['G'] @ z + data['force']")
    verification=dict(total=len(checks.rows),passed=sum(r['passed'] for r in checks.rows),checks=checks.rows)
    verification['validation']='PASS' if verification['total']==verification['passed'] else 'FAIL'
    verification.update(physics_pass=False,gate_effect='NONE',review_status='DEFERRED',
        primary_summary_sha256=ev.SHA((ROOT/directory/'summary.json').read_bytes()),
        source_sha256={ev.SELF:ev.SHA((ROOT/ev.SELF).read_bytes()),SELF:ev.SHA((ROOT/SELF).read_bytes()),
                       FORCE:ev.SHA((ROOT/FORCE).read_bytes()),CHARGE:ev.SHA((ROOT/CHARGE).read_bytes())})
    return ev.ENCODE(verification),verification


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',default=ev.BASE+'r4c1_cusp3_evolution_attempt_01')
    parser.add_argument('--output',default=ev.BASE+'r4c1_cusp3_evolution_independent_audit_attempt_01')
    parser.add_argument('--replay');args=parser.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve();dest.relative_to((ROOT/ev.BASE).resolve())
    if not args.replay and dest.exists():raise FileExistsError('Preserve existing outputs')
    body,result=calculate(args.input)
    if args.replay:
        if (dest/'verification.json').read_bytes()!=body:raise RuntimeError('Read-only replay differs')
        print('READ_ONLY_REPLAY_EXACT')
    else:
        dest.mkdir(parents=True)
        with (dest/'verification.json').open('xb') as f:f.write(body)
        with (dest/'verification.json.sha256').open('x') as f:f.write(ev.SHA(body)+'  verification.json\n')
    print(json.dumps({n:result[n] for n in ('validation','passed','total','physics_pass')}))
    return 0 if result['validation']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
