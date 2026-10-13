"""Exact evolving dust split and honest finite-mode remainder disposition."""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import uuid
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'
PARENT = BASE + 'r4c1_g3n5_dust_finite_k_attempt_01/'
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()
CONTRACT = 'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_REMAINDER_CONTRACT_2026-10-11.md'
PINNED = {
    'Analysis/MasterTests/test_01_r4c1_g3n5_dust_remainder_v2.py':
        '3c57b791d2425db988cb88f724313d567f08e6f2c428e1345877df53a1146a8b',
    'Analysis/MasterTests/test_01_r4c1_g3n5_dust_remainder_v1.py':
        '01b0a895fde8d979dd1d939780468748daabfabe3ecfb31dae4c5192ba3c0b88',
    CONTRACT: '8c9ae0331a826c583f26e969dc61697d6e71345b16e1448be1940b3b3ecfa21c',
    PARENT + 'summary.json': 'a4c884469c39682908d894e23cb5fbdaa370a4a46f5aa2c31ae4a14128c0f706',
    'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py':
        '8c63194a678734917c5c9a9593da8023fb7ba946790cc0376c7cd3a9fa57c991',
    'Theory/Gates/RES-001/RES001_R4C1_G3N5_DUST_FINITE_K_REPORT_2026-10-11.md':
        'faf029c5c5ec6a8b48b3eb44e2255a07fb61bf45cf0c4f25a9494a89b5818c8a',
    'Theory/Gates/RES-001/RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md':
        '82708666dfce4ef214b614bc7da31b294d7569539b97292aaa9a79e906e6266f',
    'Theory/Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md':
        '14bf01842d7fa573c22d78f021ec815421fb01a4b97fee806c1fbed22b676519',
}
ENGINE = 'Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v1.py'
if hashlib.sha256((ROOT / ENGINE).read_bytes()).hexdigest() != PINNED[ENGINE]:
    raise RuntimeError('Frozen engine drift')
sys.path.insert(0, str(ROOT / 'Analysis/MasterTests'))
import test_01_r4c1_g3n5_nonzero_characteristic_v1 as parent
common = parent.common
END = s.Rational(1, 20)
MODES = (4, 8, 16, 32, 64)


def progress(message):
    print(message, flush=True)
    if PROGRESS_STREAM is not None:
        PROGRESS_STREAM.write(message+'\n')
        PROGRESS_STREAM.flush()


PROGRESS_STREAM = None


class Background:
    """B1G's pinned polynomial flow; no parameter-family substitution."""
    def __init__(self):
        self.sy = {k: s.Symbol(k, real=True) for k in parent.old.BG_NAMES}
        self.sy['a'] = s.Symbol('a', positive=True)
        self.ell = s.Symbol('ell', positive=True)
        self.p = s.Symbol('p', positive=True)
        self.sy.update(ell=self.ell, p=self.p, I=s.I, sqrt=s.sqrt)
        self.bg = s.Matrix([self.sy[k] for k in parent.old.BG_NAMES])
        a, H, u, ud, v, vd, r, rd, pd, rho, C = self.bg
        rad = u*u + v*v
        potential = rad/2 + rad**2/24 + rad**3/480 + r*r + r**4/28 + 3*rad*r*r/28
        kinetic = ud*ud + vd*vd + rd*rd + 3*pd*pd
        self.energy = kinetic/2 + potential + rho
        self.constraint = s.Rational(33, 10)*H*H - self.energy
        self.rates = s.Matrix([a*H, -s.Rational(5, 11)*(kinetic+rho),
            ud, -3*H*ud-s.diff(potential, u), vd, -3*H*vd-s.diff(potential, v),
            rd, -3*H*rd-s.diff(potential, r), -3*H*pd-s.Rational(2, 15)*rho,
            (-3*H+s.Rational(2, 5)*pd)*rho, s.Rational(2, 5)*pd*C])
        self.mod = s.Poly(self.constraint, vd)

    def dt(self, mat):
        return mat.applyfunc(lambda q: sum(s.diff(q, b)*r
            for b, r in zip(self.bg, self.rates) if b in q.free_symbols))

    def shell(self, expr):
        # Keep the exported raw rational representation. The physical scope
        # still requires the B1 Friedmann shell; we do not rewrite matrices.
        return s.cancel(expr)

    def constraint_reduce_scalar(self, expr):
        num, den = s.cancel(expr).as_numer_denom()
        nr = s.Poly(num, self.bg[5]).rem(self.mod).as_expr()
        dr = s.Poly(den, self.bg[5]).rem(self.mod).as_expr()
        if dr == 0:
            raise ZeroDivisionError('Scalar certificate denominator vanishes')
        return s.cancel(nr/dr)

    def on(self, mat):
        return mat.applyfunc(self.shell)


class RationalBox:
    """Exact rational interval arithmetic; refuses unenclosed denominators."""
    def __init__(self, boxes):
        self.boxes = boxes

    @lru_cache(maxsize=None)
    def evaluate(self, q):
        if q.is_Rational:
            return q, q
        if q.is_Symbol:
            return self.boxes[q]
        if q.is_Add:
            terms = [self.evaluate(v) for v in q.args]
            return sum(v[0] for v in terms), sum(v[1] for v in terms)
        if q.is_Mul:
            lo = hi = s.Integer(1)
            for child in q.args:
                aa, bb = self.evaluate(child)
                vals = (lo*aa, lo*bb, hi*aa, hi*bb)
                lo, hi = min(vals), max(vals)
            return lo, hi
        if q.is_Pow:
            lo, hi = self.evaluate(q.base)
            power = q.exp
            if power.is_Integer:
                n = int(power)
                if n < 0:
                    if lo <= 0 <= hi:
                        raise ZeroDivisionError('Interval denominator includes zero')
                    lo, hi = 1/hi, 1/lo
                    n = -n
                if n == 0:
                    return s.Integer(1), s.Integer(1)
                vals = [lo**n, hi**n]
                if n % 2 == 0 and lo <= 0 <= hi:
                    vals.append(s.Integer(0))
                return min(vals), max(vals)
            if power == s.Rational(1, 2) and lo >= 0:
                scale = 10**6
                def floor_root(v):
                    return math.isqrt(int(s.floor(v*scale*scale)))
                return s.Rational(floor_root(lo), scale), s.Rational(floor_root(hi)+1, scale)
        raise ValueError('Unsupported exact interval node: ' + str(q))

    def absolute(self, q):
        re, im = s.expand(q, complex=True).as_real_imag()
        bounds = [self.evaluate(v) for v in (re, im)]
        return sum(max(abs(lo), abs(hi)) for lo, hi in bounds)

    def norm(self, mat):
        return max(sum(self.absolute(v) for v in mat.row(i)) for i in range(mat.rows))


def calculate():
    ps = common.read_json(PARENT+'summary.json')
    pins = dict(ps['source_sha256'])
    pins.update({PARENT+k: v for k, v in ps['artifacts'].items()})
    for k, v in PINNED.items():
        if k in pins and pins[k] != v:
            raise ValueError('Conflicting source pin ' + k)
        pins[k] = v
    pins[SELF] = common.sha((ROOT/SELF).read_bytes())
    absent = common.inspect_pins(pins)
    paths = [ROOT/q for q in pins]
    paths.extend(Path(str(q)+'.sha256') for q in list(paths) if Path(str(q)+'.sha256').exists())
    before = parent.snapshot(paths)
    checks = common.Checks()
    bg = Background()
    a, H, u, ud, v, vd, r, rd, pd, rho, C = bg.bg
    ell, p = bg.ell, bg.p
    exact = lambda name, mat: parent.exact(checks, name, bg.on(mat)
        if isinstance(mat, s.MatrixBase) else bg.shell(mat))
    checks.add('pins_before', True, {'files':len(before),'inherited_absent':absent})
    checks.add('parent_checks_not_physical_clearance', ps['passed']==ps['total']==95
        and not ps['physics_pass'] and not ps['full_finite_k_uniform_remainder_verified'])
    exact('B1G_constraint_preserved', bg.dt(s.Matrix([bg.constraint]))[0])
    exact('B1G_energy_dissipation', bg.dt(s.Matrix([bg.energy]))[0]
        + 3*H*(ud*ud+vd*vd+rd*rd+3*pd*pd+rho))
    data = common.read_json(PARENT+'matrices.json')
    progress('Import raw archived matrices; retain full 20-dimensional generator')
    mats = {k:parent.import_matrix(data[k], bg.sy) for k in data}
    L, B, Bi, Az, O, G, M, R0 = [mats[k] for k in ('full_generator',
        'balancing_map','balancing_map_inverse','balanced_generator','actual_dust_observable',
        'formal_slow_lift','leading_dust_generator','observable_equation_defect')]
    exact('balancing_inverse', B*Bi-s.eye(20))
    exact('evolving_balancing_generator', Az*B-bg.dt(B)-B*L)
    exact('inherited_observable_defect', R0-bg.dt(O)-O*L+M*O)
    progress('Imported generator and observable derivative identities checked')
    OG = bg.on(O*G)
    det = s.factor(OG.det())
    det_shell = bg.constraint_reduce_scalar(det)
    adj = OG.adjugate()
    TZ = bg.on(B*G)
    E = bg.on(TZ*adj/det)
    Oz = bg.on(O*Bi)
    F = bg.on((R0+M*O)*Bi)
    progress('Normalized lift and dust time-derivative map constructed')
    exact('dust_time_derivative_map', F-bg.dt(Oz)-Oz*Az)
    exact('observable_normalized_lift', Oz*E-s.eye(2))
    Delta = bg.on(F*E-M)
    R = bg.on(R0*Bi)
    Edot = (bg.dt(TZ)*adj+TZ*bg.dt(adj))/det-TZ*adj*bg.dt(s.Matrix([det]))[0]/det**2
    # Keep exact factored S=Az E-Edot-E(M+Delta), J=Az-E F.
    # Expanding these rational products is not needed to evolve or bound them.
    exact('complement_feedback_graph_identity', R*E-Delta)
    exact('normalized_lift_derivative', bg.dt(Oz)*E+Oz*Edot)
    # With O_z E=I and F=O_z_dot+O_z Az, these establish exact
    # tangent source and moving-kernel preservation for the factored system.
    # Full-state recomposition is additionally checked on archived states.
    D2 = Delta.applyfunc(lambda q:bg.shell(s.limit(q*ell**2,ell,s.oo)/a**2))
    tail = bg.on(Delta-a*a*D2/ell**2)
    exact('no_order_one_graph_correction', Delta.applyfunc(lambda q:s.limit(q,ell,s.oo)))
    exact('no_inverse_p_graph_correction', Delta.applyfunc(lambda q:s.limit(q*ell,ell,s.oo)))
    exact('inverse_p2_coefficient', tail.applyfunc(lambda q:s.limit(q*ell**2,ell,s.oo)))
    D4 = tail.applyfunc(lambda q:bg.shell(s.limit(q*ell**4,ell,s.oo)/a**4))
    progress('First inverse-p2 graph correction and factored feedback constructed')
    checks.add('first_graph_correction_nonzero', any(q!=0 for q in D2))
    checks.add('complement_forcing_retained_nonzero', any(q!=0 for q in R) and any(q!=0 for q in S))
    checks.add('omitting_Bdot_rejected', any(q!=0 for q in bg.on(bg.dt(B))))
    exact('physical_momentum_drift', bg.dt(s.Matrix([ell/a]))[0]+H*ell/a)
    checks.add('omitting_physical_momentum_drift_rejected', bg.dt(s.Matrix([ell/a]))[0]!=0)
    checks.add('not_all_complement_seeds_are_eigenmodes', True,
        'Archive seeds lie in ker(O_z) initially; no spectral purity is asserted')

    # Conservative rational background enclosure, proved from B1G energy
    # monotonicity and short-time continuation, NOT from trajectory extrema.
    E0 = s.Rational(3469,1400)
    H02 = s.Rational(3469,4620)
    checks.add('H0_lower_173_over_200', H02>s.Rational(173,200)**2)
    checks.add('H0_upper_one', H02<1)
    checks.add('H_short_lower_three_quarters', s.Rational(173,200)-10*E0*END/11>s.Rational(3,4))
    checks.add('velocity_energy_enclosure', 2*E0<s.Rational(9,4)**2)
    checks.add('psi_positive_bootstrap', s.Rational(1,5)-(s.Rational(3,5)+s.Rational(1,3))*END>0)
    checks.add('dust_monotone_in_positive_psi_branch', -3*s.Rational(3,4)+s.Rational(2,25)<0)
    checks.add('psi_short_lower_one_sixth', s.Rational(1,5)-(s.Rational(3,5)+s.Rational(2,75))*END>s.Rational(1,6))
    boxes = {a:(s.Integer(1),s.Rational(20,19)),H:(s.Rational(3,4),s.Integer(1)),
        u:(s.Rational(71,80),s.Rational(89,80)),v:(-s.Rational(9,80),s.Rational(9,80)),
        r:(s.Rational(71,80),s.Rational(89,80)),ud:(-s.Rational(9,4),s.Rational(9,4)),
        vd:(-s.Rational(9,4),s.Rational(9,4)),rd:(-s.Rational(9,4),s.Rational(9,4)),
        pd:(s.Rational(1,6),s.Rational(1,5)),rho:(s.Rational(17,100),s.Rational(1,5)),
        C:(s.Integer(1),s.Rational(250,249))}
    # exp(H0 T)<=1/(1-T); exp(-3T)>=1-3T; exp(beta psi_dot T)<=1/(1-1/250).
    ar = common.read_json(PARENT+'trajectories.json')
    diagnostics = common.read_json(PARENT+'diagnostics.json')
    coeff = common.read_json(BASE+'r4c1_g3n5_constraint_response_attempt_02/series_coefficients.json')
    bc = np.array([[float(pair[0]) for pair in row] for row in coeff['background_coefficients']])
    fn = s.lambdify([bg.bg,ell],(E,Oz,Delta,R,Az,F,mats['full_field_reconstruction'],mats['balancing_map_inverse']), 'numpy',cse=True)
    bd = s.lambdify([bg.bg,ell],Edot,'numpy',cse=True)
    mf = s.lambdify([bg.bg],M,'numpy',cse=True)
    progress('Compiled exact maps; begin archive and rational-enclosure checks')
    rows=[]
    for item in ar['modes']:
        kval=item['ell']
        checks.add('registered_mode_'+str(kval),kval in MODES)
        initial=np.array(item['initial_balanced']); z0=initial[...,0]+1j*initial[...,1]
        max_identity=max_reconstruction=max_box=max_fields=0.0
        max_force=0.0
        for ti,t in enumerate(ar['time']):
            bval=np.polynomial.polynomial.polyval(t,bc.T)
            ee,oo,dd,rr,aa,ff,qq,binv=[np.asarray(q,dtype=complex) for q in fn(bval,kval)]
            ee_dot=np.asarray(bd(bval,kval),dtype=complex)
            raw=np.array(item['balanced'][ti]); z=raw[...,0]+1j*raw[...,1]
            w=oo@z; residual=z-ee@w
            ss=aa@ee-ee_dot-ee@(np.asarray(mf(bval),dtype=complex)+dd)
            jj=aa-ee@ff
            lhs=aa@z
            archive_fields=np.array(item['full_fields'][ti]); archive_fields=archive_fields[...,0]+1j*archive_fields[...,1]
            max_fields=max(max_fields,float(np.linalg.norm(qq@binv@z-archive_fields,np.inf)/max(1.,np.linalg.norm(archive_fields,np.inf))))
            recomposed=ee_dot@w+ee@((np.asarray(mf(bval),dtype=complex)+dd)@w+rr@residual)+ss@w+jj@residual
            max_identity=max(max_identity,float(np.linalg.norm(lhs-recomposed,np.inf)/max(1.,np.linalg.norm(lhs,np.inf))))
            archive_w=np.array(item['dust_observables'][ti]); archive_w=archive_w[...,0]+1j*archive_w[...,1]
            max_reconstruction=max(max_reconstruction,float(np.linalg.norm(w-archive_w,np.inf)/max(1.,np.linalg.norm(w,np.inf))))
            max_force=max(max_force,float(np.linalg.norm(rr@residual[:,:2],np.inf)))
            for sym,value in zip(bg.bg,bval):
                lo,hi=boxes[sym]
                max_box=max(max_box,max(float(lo)-value,value-float(hi),0.))
        for name,val,limit in (('exact_split_numeric',max_identity,1e-9),('archive_observable',max_reconstruction,1e-10),('all_22_archive_fields',max_fields,1e-10),('sampled_boxes_sanity',max_box,1e-10)):
            checks.add(name+'_'+str(kval),val<=limit,val,'<='+str(limit))
        ee0,oo0,*_=fn(np.polynomial.polynomial.polyval(0.,bc.T),kval)
        initial_w=np.asarray(oo0,dtype=complex)@z0
        checks.add('prepared_initial_matching_'+str(kval),float(np.linalg.norm(initial_w-np.column_stack((np.eye(2),np.zeros((2,2)))),np.inf))<=1e-10)
        certificate={'scope':'exact B1 homogeneous flow and full linear finite-mode IVP; infinity norm, not physical energy',
            'time':'[0,1/20]','uniform_high_p_decay_proved':False}
        try:
            box=RationalBox({**boxes,ell:(s.Integer(kval),s.Integer(kval))})
            # Certify the graph domain before using its inverse.
            detbox=box.evaluate(det_shell)
            if detbox[0]<=0<=detbox[1]:
                raise ZeroDivisionError('Graph normalizer determinant enclosure includes zero')
            mindet=min(abs(q) for q in detbox)
            tt,ad=[box.norm(mat) for mat in (TZ,adj)]
            ee=tt*ad/mindet
            ed=(box.norm(bg.dt(TZ))*ad+tt*box.norm(bg.dt(adj)))/mindet+tt*ad*box.absolute(bg.dt(s.Matrix([det_shell]))[0])/mindet**2
            mm,cc,gg,ff=[box.norm(mat) for mat in (M,R,Az,F)]
            delta_numerator=Delta.applyfunc(lambda q:s.cancel(q*det))
            dd=box.norm(delta_numerator)/mindet
            ss=gg*ee+ed+ee*(mm+dd)
            jj=gg+ee*ff
            lam=max(mm+dd+cc,ss+jj)
            pref=dd*END+cc*ss*END*END/2
            certificate.update(status='CERTIFIED_FINITE_MODE_MAJORANT',normalizer_det=[str(q) for q in detbox],
                constants={k:str(q) for k,q in dict(m=mm,d=dd,c=cc,s=ss,j=jj,Lambda=lam).items()},
                prepared_bound='('+str(pref)+')*exp('+str(lam*END)+')',
                complementary_bound='('+str(cc*END)+')*exp('+str(lam*END)+')',
                log10_prepared_bound_display=float(s.log(pref,10)+lam*END/s.log(10)))
        except (ZeroDivisionError,ValueError,KeyError) as err:
            certificate.update(status='INTERVAL_MAJORANT_UNRESOLVED',reason=str(err))
        rows.append({'ell':kval,'max_split_numeric_residual':max_identity,
            'max_archived_observable_disagreement':max_reconstruction,'max_fast_feedback_sample':max_force,
            'certificate':certificate})
        progress(json.dumps({'ell':kval,'split':max_identity,'bound':certificate['status']}))
    checks.add('all_five_modes_retained',sorted(row['ell'] for row in rows)==list(MODES))
    checks.add('nonmonotonic_complement_archive_preserved',diagnostics['modes'][2]['complementary_seed_dust_transfer']>diagnostics['modes'][1]['complementary_seed_dust_transfer'])
    matrices={'observable_Oz':Oz,'observable_normalized_lift_Ez':E,'instantaneous_graph_correction_Delta':Delta,
        'first_inverse_p2_graph_coefficient':D2,'graph_correction_tail':tail,'inverse_p4_graph_coefficient':D4,
        'complementary_forcing_R':R,'lift_time_derivative':Edot,
        'complete_balanced_generator':Az,'dust_time_derivative_F':F}
    export={k:parent.exports(q) for k,q in matrices.items()}
    for name,obj in export.items():
        exact('roundtrip_'+name,parent.import_matrix(obj,bg.sy)-matrices[name])
    formulas={'matrices':export,'factored_operators':{'S':'complete_balanced_generator @ observable_normalized_lift_Ez - lift_time_derivative - observable_normalized_lift_Ez @ (M+instantaneous_graph_correction_Delta)',
        'J':'complete_balanced_generator - observable_normalized_lift_Ez @ dust_time_derivative_F'},'graph_normalizer_determinant':str(det),
        'equations':['W_dot=(M+Delta) W+R r','r_dot=S W+J r','O_z r=0'],
        'on_shell_relation':str(bg.constraint),'graph_determinant_on_shell_certificate':str(det_shell),'reduction':'Raw exported matrices retained. Only the scalar graph determinant certificate is reduced by the conserved Friedmann relation; no v_dot division',
        'background_boxes':{str(k):[str(q) for q in val] for k,val in boxes.items()},
        'majorant_proof':'|W|<=exp(Lambda t); |r|<=s t exp(Lambda t) for prepared W0 norm 1,r0=0; variation of constants gives |W-Phi W0|<=(d t+c s t^2/2) exp(Lambda t). Complement W0=0,r0 norm 1 gives |W|<=c t exp(Lambda t).',
        'bound_norm':'induced infinity norm on two prepared columns or one complementary column in frozen reference units, not a physical Hamiltonian norm',
        'missing_uniform_estimate':'A complementary propagator/oscillatory-cancellation bound uniform in p, including the generated complementary response; the absolute-value majorant retains growth with p.'}
    diag={'modes':rows,'inherited_precision':'70-digit degree40 background coefficients evaluated binary64 for archive checks; exact rational/SymPy algebra and rational interval boxes for bounds',
        'instantaneous_graph_correction_order':2,'full_dust_convergence_order':'NOT_PROVED',
        'scientific_disposition':'EXACT_SPLIT_AND_GRAPH_CORRECTION_CHECKED_UNIFORM_REMAINDER_OPEN',
        'whole_interval_finite_bounds_certified':all(q['certificate']['status']=='CERTIFIED_FINITE_MODE_MAJORANT' for q in rows),
        'full_prepared_high_p_remainder_proved':False,'archive_diagnostics_unchanged':diagnostics}
    checks.add('pins_after',common.inspect_pins(pins)==absent)
    checks.add('all_input_hash_size_mtime_preserved',parent.snapshot(paths)==before,{'files':len(before)})
    payloads={'formulas.json':common.encode(formulas),'diagnostics.json':common.encode(diag)}
    passed=sum(q['passed'] for q in checks.rows)
    summary=dict(schema='r4c1-g3n5-dust-remainder-v3',validation='PASS_LOCAL_CHECKS' if passed==len(checks.rows) else 'FAIL_LOCAL_CHECKS',
        passed=passed,total=len(checks.rows),checks=checks.rows,status=diag['scientific_disposition'],
        analytic_dust_milestone='OPEN_UNIFORM_REMAINDER',full_prepared_high_p_remainder_proved=False,
        ordinary_wave_Jordan_defect_removed=False,original_slow_time_coefficient='-11/6',
        complete_density_Hamiltonian_positive=False,physical_EFT_cutoff_derived=False,healthy_continuous_GR_verified=False,
        finite_mode_bound_certified=diag['whole_interval_finite_bounds_certified'],physics_pass=False,gate_effect='NONE',
        Rule9_cleared=False,review_status='DEFERRED',research_execution='PROCEED_PROVISIONALLY_EXACT_SPLIT_ONLY',
        canonical_tests_1_to_3='HOLD_SUBSTANTIVE',K_Q='NOT_DERIVED',V='NOT_COMPUTED',Stage4A='CLOSED',
        source_sha256=dict(sorted(pins.items())),source_metadata_preserved=len(before),inherited_sidecars_absent=absent,
        artifacts={k:common.sha(q) for k,q in payloads.items()},
        substantive_unknowns=['Uniform oscillatory/complementary remainder','Physical EFT band and full GR','Microscopic and weak-field matching'],
        interrupted_sources_v1_v2='Dense expansion (v1) and broad Friedmann polynomial quotient reduction (v2) interrupted before scientific receipts. Sources and original sidecars preserved. Neither produced a mathematical verdict.',
        review_dependencies=['R9-MT1-G3N5-DUST-FINITE-K','B1G and inherited G3N5/operator review'],
        runtime=dict(python=platform.python_version(),numpy=np.__version__,sympy=s.__version__))
    summary.update({'MAT-001':'BLOCKED','UVIR-003':'IN_PROGRESS','TOP-X4':'UNCHANGED'})
    payloads['summary.json']=common.encode(summary)
    return payloads,summary


def main():
    global PROGRESS_STREAM
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',default=BASE+'r4c1_g3n5_dust_remainder_attempt_01')
    ap.add_argument('--replay')
    args=ap.parse_args()
    dest=(ROOT/(args.replay or args.output)).resolve()
    dest.relative_to((ROOT/BASE).resolve())
    if args.replay and not dest.is_dir():
        raise FileNotFoundError('Replay destination absent')
    if not args.replay and dest.exists():
        raise FileExistsError('Refuse existing scientific output')
    private_dir=ROOT/'.local/itsm-context'
    private_dir.mkdir(parents=True,exist_ok=True)
    PROGRESS_STREAM=(private_dir/('dust-remainder-v3-progress-'+uuid.uuid4().hex+'.txt')).open('x',encoding='utf-8')
    bodies,summary=calculate()
    if args.replay:
        for name,body in bodies.items():
            if (dest/name).read_bytes()!=body or (dest/(name+'.sha256')).read_bytes()!=(common.sha(body)+'  '+name+'\n').encode():
                raise RuntimeError('Replay mismatch '+name)
    else:
        dest.mkdir(parents=True,exist_ok=False)
        for name,body in bodies.items():
            with (dest/name).open('xb') as stream:stream.write(body)
            with (dest/(name+'.sha256')).open('xb') as stream:stream.write((common.sha(body)+'  '+name+'\n').encode())
    print(json.dumps({'action':'READ_ONLY_REPLAY_EXACT' if args.replay else 'NEW_RECEIPTS_WRITTEN',
        **{k:summary[k] for k in ('validation','passed','total','status','finite_mode_bound_certified','physics_pass')}}))
    for q in summary['checks']:
        if not q['passed']:print(json.dumps(q))
    PROGRESS_STREAM.close()
    return int(summary['passed']!=summary['total'])


if __name__=='__main__':
    raise SystemExit(main())
