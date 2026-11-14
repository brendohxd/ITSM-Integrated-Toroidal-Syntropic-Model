"""Extend the reproduced initial density row with physical-rho bounds."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
BASE = 'Analysis/MasterTests/outputs/'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT/rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def calculate():
    source = 'Analysis/MasterTests/test_rtau_actual_corrected_density_v1.py'
    result = load(source, 'density_actual_v1').calculate()
    mp.mp.dps = 100
    mp.iv.dps = 60
    iv = mp.iv
    lo = lambda x: mp.mpf(iv.mpf(x)._mpi_[0])
    hi = lambda x: mp.mpf(iv.mpf(x)._mpi_[1])
    up = lambda x: iv.mpf(max(abs(lo(x)), abs(hi(x))))
    norm = lambda xs: iv.sqrt(sum((up(x)**2 for x in xs), iv.mpf(0)))
    decode = lambda v: iv.mpf([mp.mpf(tuple(t)) for t in v])
    binary = lambda v: [list(t) for t in iv.mpf(v)._mpi_]
    paths = dict(momentum=BASE+'rtau_momentum_rate_lift_v2_20261104/receipt.json',
                 force=BASE+'rtau_strong_force_coordinate_v3_20261104/receipt.json',
                 normal=BASE+'rtau_strong_density_normal_form_v1_20261103/receipt.json',
                 raw=BASE+'rtau_strong_density_l2_source_v1_20261104/receipt.json')
    data = {k: json.loads((ROOT/p).read_text()) for k, p in paths.items()}
    factory = 'Analysis/MasterTests/r4c1_canonical_density_factory_v1.py'
    for rel in [source, factory, *paths.values(), Path(__file__).relative_to(ROOT).as_posix()]:
        result['source_sha256'][rel] = sha(ROOT/rel)
    snap = {}
    for rel, h in result['source_sha256'].items():
        p = ROOT/rel
        assert sha(p) == h, rel
        for q in [p, Path(str(p)+'.sha256')]:
            if q.exists():
                snap[q] = sha(q), q.stat().st_mtime_ns
    checks = result['checks']
    def check(name, ok):
        checks.append(dict(name=name, passed=bool(ok)))
    env = load(factory, 'physical_density_coefficients').prepare()
    J, D = env['J'], env['D']
    y, _ = env['state'](J.variable(iv.mpf([0, hi(2*iv.pi)])), True, [0, 0, 0])
    # Only zeroth spatial jets are used here, so unused third-shift slots do
    # not impose any physical zero third derivative on the background.
    Q = [D.var(x, i) for i, x in enumerate(y[:14])]
    N, mu, gamma, inverse, _ = env['geometry'](Q, [D(0)]*14)
    p0 = (y[26]-y[44]*y[40])/N.c
    p = D.var(p0, 100)
    spatial = D.var(y[40], 101)
    h = [[Q[0], Q[1], Q[2]], [Q[1], Q[3], Q[4]], [Q[2], Q[4], Q[5]]]
    rest = [inverse[i][2]*spatial+Q[6+i]*(p+Q[8]*spatial/(gamma+1)) for i in range(3)]
    Y = sum((h[i][j]*rest[i]*rest[j] for i in range(3) for j in range(3)), D(0))
    pars = env['env']['env']['exact']
    rational = lambda r: iv.mpf(int(r.p))/int(r.q)
    KQ, A, b = [rational(pars[k]) for k in ['K_Q', 'A', 'b']]
    branch_path = BASE+'rtau_actual_force_pair_v2_20261105/receipt.json'
    branch_data = json.loads((ROOT/branch_path).read_text())
    result['source_sha256'][branch_path] = sha(ROOT/branch_path)
    certified_Y = decode(branch_data['coefficient_controls_binary']['positive_Y'])
    assert lo(certified_Y) > 0
    root = iv.sqrt(certified_Y)
    U = gamma*p+Q[8]*spatial
    uc = U.c.c[0]
    def first(i):
        return KQ*uc*U.g.get(i,J(0)).c[0]-3*A*root*Y.g.get(i,J(0)).c[0]/2
    check('physical_map_retains_certified_positive_force_branch', lo(certified_Y) > 0 and lo(mu.c.c[0]) > 0)
    value = lambda d: d.c.c[0]
    pc, muc = value(p), value(mu)
    fp = first(100)
    fps = KQ*(U.g[100].c[0]*U.g[101].c[0]+uc*U.h.get((100,101),J(0)).c[0])-3*A*(root*Y.h.get((100,101),J(0)).c[0]+Y.g[100].c[0]*Y.g[101].c[0]/(2*root))/2
    fq = [first(i) for i in range(13)]
    mupartials = [mu.g.get(i, J(0)).c[0] for i in range(13)]
    # rho variation = w+c Pxi-p f_ps Dchi-(p/mu)xi
    #                 +(p f_p/mu)delta mu+sum f_q delta q-b Z zeta.
    c = decode(data['normal']['bounds_binary']['coefficient'])
    coefP = c+up(pc/muc)
    coefQ = up(pc*fp/muc)*norm(mupartials)+norm(fq)
    coefF = up(pc*fps)
    coefZ = up(b*y[13].c[0])
    Qbounds = list(map(decode, data['momentum']['constants_binary']['full_configuration_H1']))
    Pbounds = list(map(decode, data['momentum']['constants_binary']['full_momentum_L2']))
    Fbounds = list(map(decode, data['force']['constants_binary']['force_H2_inverse']))
    physical = [coefQ*q+coefP*p+coefF*f for q, p, f in zip(Qbounds, Pbounds, Fbounds)]
    physical[0] += 1
    physical[3] += coefZ
    check('physical_density_bound_finite_in_all_eight_strong_global_inputs',
          len(physical) == 8 and all(mp.isfinite(hi(x)) and lo(x) >= 0 for x in physical))
    # Complete source bound before scalar L2 transport, in the same corrected
    # nine-input order, not an adapted or old held lifted estimate.
    raw_source = list(map(decode, data['raw']['rows_binary']['gauge_closed_source']))
    density_source = [raw_source[1]*q+raw_source[2]*p+raw_source[3]*f
                      for q, p, f in zip(Qbounds, Pbounds, Fbounds)]
    density_source[0] += raw_source[0]
    density_source += [raw_source[4]]
    check('source_row_keeps_separate_harmonic_velocity', hi(density_source[-1]) > 0)
    check('new_source_bounds_preserve_strong_density_order', all(mp.isfinite(hi(x)) for x in density_source))
    check('all_inputs_and_sidecars_preserved', all(sha(p) == h and p.stat().st_mtime_ns == tm for p, (h, tm) in snap.items()))
    result['kind'] = 'RTAU_ACTUAL_CORRECTED_DENSITY_V4'
    result['bounds_binary']['physical_rho_L2'] = list(map(binary, physical))
    result['bounds_binary']['initial_original_coordinate_density_source_L2'] = list(map(binary, density_source))
    result['upper_display']['physical_rho_L2'] = [mp.nstr(hi(x), 30) for x in physical]
    result['upper_display']['initial_original_coordinate_density_source_L2'] = [mp.nstr(hi(x), 30) for x in density_source]
    result['force_branch_evaluation'] = 'Exact generic partial formulas with pinned conformal-background sum-of-squares Y enclosure; no clipping or projection of negative interval dependency overestimate'
    result['physical_rho_numeric_reconstruction_constants'] = 'EXPORTED_INITIAL_ONLY'
    result['physical_map_coefficient_upper'] = {k: mp.nstr(hi(v), 30) for k, v in dict(P=coefP, Q=coefQ, force=coefF, auxiliary=coefZ).items()}
    result['task_status'] = 'INITIAL_ROW_AND_PHYSICAL_MAP_BOUND_COMPLETE_SCOPED; TWENTY_DIRECTION_COMPARISON_OPEN'
    result['passed'] = sum(c['passed'] for c in checks)
    result['total'] = len(checks)
    return result


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output', type=Path)
    group.add_argument('--verify', type=Path)
    a = parser.parse_args()
    if a.output:
        assert not a.output.parent.exists()
    data = calculate()
    raw = (json.dumps(data, sort_keys=True, indent=2)+'\n').encode()
    if a.output:
        a.output.parent.mkdir(parents=True)
        a.output.write_bytes(raw)
        Path(str(a.output)+'.sha256').write_text(sha(a.output)+'\n')
    else:
        assert a.verify.read_bytes() == raw, 'Replay differs'
    print(json.dumps({k: data[k] for k in ['passed', 'total', 'task_status', 'physics_pass']}))
    assert data['passed'] == data['total'], [c for c in data['checks'] if not c['passed']]


if __name__ == '__main__':
    main()
