"""Initial physical-rho remainder with explicit derivative terms retained."""

import argparse
import ast
import inspect
import json
from pathlib import Path

import mpmath as mp
import sympy as sp

import test_rtau_actual_force_pair_v2 as force_module
from test_rtau_nonlocal_trace_drift_v1 import ROOT, GATE, OUT, digest, read
from test_rtau_physical_density_rate_v1 import fourier_controls

CONTRACT = GATE+'RES001_RTAU_PHYSICAL_DENSITY_REMAINDER_V1_CONTRACT_2026-11-14.md'
PARENT = OUT+'rtau_density_state_map_v1_20261114/receipt.json'
SOURCES = {
    'drift': 'rtau_density_operator_drift_v3_20261114',
    'force': 'rtau_actual_force_pair_v2_20261105',
    'density': 'rtau_actual_corrected_density_v4_20261105',
    'lift': 'rtau_momentum_rate_lift_v2_20261104',
    'inverse': 'rtau_strong_force_coordinate_v3_20261104',
    'weak': 'rtau_weak_canonical_rate_v2_20261103',
    'gauge': 'rtau_gauge_mean_trace_rate_v2_20261109',
    'normal': 'rtau_strong_density_normal_form_v1_20261103',
    'periodic': 'rtau_periodic_principal_composition_v2_20261104',
}


def coefficient_environment():
    """Reuse only the pinned generic spatial-jet setup, before the Hessian rows.

    The AST boundary is an assertion against accidental expansion of scope.
    First field differentials retain their full spatial Taylor jets.
    """
    tree = ast.parse(inspect.getsource(force_module.calculate))
    fn = tree.body[0]
    # Original lines 20..49 are setup/pins; 92..165 are the generic force jets.
    body = [n for n in fn.body if (2 <= n.lineno <= 31 or 74 <= n.lineno <= 147)]
    assert isinstance(body[-1], ast.Assign) and body[-1].targets[0].id == 'dc'
    fn.name = '_coefficient_environment'
    fn.body = body+[ast.Return(ast.Call(ast.Name('locals', ast.Load()), [], []))]
    env = vars(force_module).copy()
    exec(compile(ast.fix_missing_locations(tree), str(ROOT/force_module.__file__), 'exec'), env)
    return env[fn.name]()


def calculate():
    mp.mp.dps, mp.iv.dps = 100, 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    ab = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    decode = lambda x: iv.mpf([mp.mpf(tuple(v)) for v in x])
    binary = lambda x: [list(v) for v in iv.mpf(x)._mpi_]
    parent = read(PARENT)
    pins = dict(parent['source_pins'])
    paths = {k: OUT+v+'/receipt.json' for k,v in SOURCES.items()}
    extra = [CONTRACT, PARENT, *paths.values(),
             'Analysis/MasterTests/test_rtau_density_operator_drift_v3.py',
             'Analysis/MasterTests/test_rtau_physical_density_rate_v1.py',
             'Analysis/MasterTests/test_rtau_actual_force_pair_v2.py',
             GATE+'RES001_RTAU_OBSERVABLE_DRIFT_SIGN_REPAIR_V1_REPORT_2026-11-14.md',
             Path(__file__).relative_to(ROOT).as_posix()]
    for rel in extra:
        p = ROOT/rel
        h = Path(str(p)+'.sha256').read_text().split()[0].lower()
        assert rel not in pins or pins[rel] == h, rel
        pins[rel] = h
    snap = {}
    for rel,h in pins.items():
        p = ROOT/rel
        assert digest(p) == h, rel
        for f in (p, Path(str(p)+'.sha256')):
            if f.exists(): snap[f] = (digest(f), f.stat().st_mtime_ns)
    data = {k: read(p) for k,p in paths.items()}
    assert all(c['passed'] for d in (parent,*data.values()) for c in d['checks'])
    ctx = coefficient_environment()
    # The factory mutates differential classes only in this process.
    mp.mp.dps, mp.iv.dps = 100, 60
    J = ctx['J']
    q, grad = ctx['q'], ctx['d']
    N, mu, p, fp, fps = [ctx[k] for k in ('N','mu','p','fp','fps')]
    vp, ap, dj, beta = [ctx[k] for k in ('vp','ap','dj','beta')]
    Kchi, S = ctx['Bj'], ctx['S'][2]
    norm = lambda xs: iv.sqrt(sum((ab(x)**2 for x in xs), iv.mpf(0)))
    # B_i = partial_i f|p,s + p f_p partial_i log(mu).
    B = [ctx['geom'](ctx['f1'], i)+p*fp*ctx['lm'][i] for i in range(13)]
    arho, h, j = p/mu, p*fps, ctx['b']*q[13]
    normal = data['normal']['bounds_binary']
    c, cz = map(decode, (normal['coefficient'],normal['coefficient_z']))
    r = J(coefficients=[dj.c[1],2*dj.c[2],iv.mpf(0)])-beta*dj*grad[12]
    coeff = {
        'S': ab(S.c[0]), 'Sz': ab(S.c[1]),
        'c': ab(c), 'cz': ab(cz),
        'a_rho': ab(arho.c[0]), 'a_rho_z': ab(arho.c[1]),
        'h': ab(h.c[0]), 'hz': ab(h.c[1]),
        'j': ab(j.c[0]), 'jz': ab(j.c[1]),
        'B': norm([x.c[0] for x in B]), 'Bz': norm([x.c[1] for x in B]),
        'v': ab(vp.c[0]), 'vz': ab(vp.c[1]),
        'a_phi_z': ab(ap.c[1]),
        'dz': ab(dj.c[1]), 'dzz': ab(2*dj.c[2]),
        'r': ab(r.c[0]), 'rz': ab(r.c[1]),
        'K_chi': norm([x.c[0] for x in Kchi]),
        'K_chi_z': norm([x.c[1] for x in Kchi]),
        'clock_gauge_H1_multiplier': ab(grad[12].c[0])+ab(grad[12].c[1]),
    }
    C = coeff
    vector = lambda xs: list(map(decode,xs))
    nine = lambda xs: vector(xs)+[iv.mpf(0)]
    P = nine(data['lift']['constants_binary']['full_momentum_L2'])
    Q = nine(data['lift']['constants_binary']['full_configuration_H1'])
    F = nine(data['inverse']['constants_binary']['force_H2_inverse'])
    unit = lambda j: [iv.mpf(int(i==j)) for i in range(9)]
    Z = unit(3)
    shift = vector(data['gauge']['bounds_binary']['corrective_shift_H1'])
    wc = vector(data['weak']['coefficients_binary']['field_rate_L2'])
    qt = [wc[0]*pp+wc[1]*qq+wc[2]*ff+wc[3]*ss for pp,qq,ff,ss in zip(P,Q,F,shift)]
    material_q = [t+C['S']*qq for t,qq in zip(qt,Q)]
    Rw = vector(data['density']['bounds_binary']['initial_original_coordinate_density_source_L2'])
    Rx = vector(data['force']['bounds_binary']['force_momentum_L2_remainder'])
    Rz = vector(data['force']['bounds_binary']['auxiliary_L2_remainder'])
    # Corrected V3 max 88.5158... is separated generously from integer 89.
    drift_max = max(mp.mpf(x) for x in data['drift']['drift_input_coefficients'])
    time = [iv.mpf(89)]*8+[iv.mpf(0)]
    spatial = [C['S']*((C['cz']+C['a_rho_z'])*pp+C['hz']*ff+C['Bz']*qq+C['jz']*zz)
               for pp,ff,qq,zz in zip(P,F,Q,Z)]
    Axi = 2*C['S']+C['Sz']+2*C['v']+C['vz']
    Azeta = 3*C['dz']+C['dzz']+2*C['r']+C['rz']
    primitive = [C['c']*(Axi*pp+Azeta*zz+rr) for pp,zz,rr in zip(P,Z,Rx)]
    clock = [C['h']*(C['a_phi_z']*pp+(C['v']+C['Sz']+C['vz'])*ff
                    +(C['K_chi']+C['K_chi_z'])*qq+C['clock_gauge_H1_multiplier']*ss)
             for pp,ff,qq,ss in zip(P,F,Q,shift)]
    pieces = dict(corrected_density_source=Rw, coefficient_time=time,
                  coefficient_spatial_advection=spatial, primitive_commutator=primitive,
                  momentum_remainder=[C['a_rho']*v for v in Rx],
                  auxiliary_remainder=[C['j']*v for v in Rz],
                  clock_commutator=clock, ordinary_material_velocity=[C['B']*v for v in material_q])
    total = [sum((v[i] for v in pieces.values()),iv.mpf(0)) for i in range(9)]
    maximum = iv.mpf(max(hi(v) for v in total))
    # Single integer certificate avoids any decimal-display rounding ambiguity.
    integer = int(mp.ceil(hi(maximum)))
    Tinv = decode(data['periodic']['values_binary']['global_T_inverse_norm'])
    Jmod = iv.exp(iv.mpf(4)/13000)*iv.sqrt(1+iv.mpf(4)/13000**2)
    bounds = dict(initial_remainder_per_input=total,
                  uniform_remainder_per_nine_input_sum=maximum,
                  per_Y20=5*maximum, per_normal_form_state=5*maximum*Tinv,
                  per_configuration_means=iv.sqrt(2)*maximum,
                  per_metric_moduli=Jmod*maximum, per_force_mean=maximum,
                  per_eliminated_mean_vector=iv.sqrt(3)*maximum,
                  per_harmonic_velocity=maximum)
    checks = fourier_controls()
    checks.update(corrected_time_drift_below_integer_certificate=drift_max<89,
                  bare_clock_volume_coefficient_zero=all(x==0 for x in B[12].c),
                  complete_nine_input_rows=all(len(v)==9 for v in pieces.values()),
                  positive_finite_aggregate=all(lo(v)>0 and mp.isfinite(hi(v)) for v in total),
                  integer_uniform_certificate=all(hi(v)<=integer for v in total),
                  all_contributions_retained=len(pieces)==8,
                  input_hashes_and_mtimes_preserved=all((digest(f),f.stat().st_mtime_ns)==v for f,v in snap.items()))
    assert all(checks.values()), checks
    def encode_rows(values):
        return {k: [binary(x) for x in v] if isinstance(v,list) else binary(v) for k,v in values.items()}
    return dict(kind='RTAU_INITIAL_PHYSICAL_DENSITY_REMAINDER_V1',
                input_order=data['density']['input_order'], source_pins=pins, pinned_files=len(pins),
                checks=[dict(name=k,passed=bool(v)) for k,v in checks.items()],
                coefficient_bounds_binary={k:binary(v) for k,v in C.items()},
                contributions_binary=encode_rows(pieces), bounds_binary=encode_rows(bounds),
                integer_uniform_certificate=integer,
                upper_display={k:mp.nstr(hi(v),30) for k,v in bounds.items() if not isinstance(v,list)},
                physical_density_principal='EXPLICIT_FIRST_AND_SECOND_DERIVATIVES_RETAINED',
                scope='INITIAL_COMPATIBLE_JETS_ONLY', remaining_generator_rows='OPEN',
                coupled_evolution='OPEN', review_status='DEFERRED',physics_pass=False,gate_effect='NONE')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--output',type=Path)
    g.add_argument('--replay',type=Path)
    args=p.parse_args()
    payload=(json.dumps(calculate(),indent=2,allow_nan=False)+'\n').encode()
    if args.replay:
        assert args.replay.read_bytes()==payload
        print('Byte-identical read-only replay')
    else:
        args.output.parent.mkdir(parents=True,exist_ok=False)
        with args.output.open('xb') as f: f.write(payload)
        print('Initial physical-density remainder controls complete')


if __name__=='__main__': main()
