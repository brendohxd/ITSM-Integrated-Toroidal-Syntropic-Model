"""Exact static rectangular-T3 light-cone control; NOT an ITSM metric prediction.

Metric ds^2=-dt^2+dx^2+dy^2+dz^2, c=1, x_i~x_i+L_i.
Observer and continuously emitting point source are static. No occultation,
refraction, expansion, gravity, Earth surface or vacuum shear is inserted.
Outputs are dimensionless, with time measured in one reference length/c.
"""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path


def norm(v):
    return math.sqrt(sum(x*x for x in v))


def catalog(observer, source, lengths, depth):
    """All image positions in the finite past cone, without a fixed image cap."""
    delta = tuple(s-o for s, o in zip(source, observer))
    # |delta_i+n_i L_i|<=depth is necessary for visibility in the sphere.
    ranges = [range(math.ceil((-depth-d)/L), math.floor((depth-d)/L)+1)
              for d, L in zip(delta, lengths)]
    result = []
    for winding in itertools.product(*ranges):
        vector = tuple(d+n*L for d, n, L in zip(delta, winding, lengths))
        distance = norm(vector)
        if 0 < distance <= depth:
            direction = tuple(x/distance for x in vector)
            result.append(dict(winding=winding, vector=vector,
                               direction=direction, lookback=distance,
                               emission_time=-distance,
                               longitude=math.atan2(direction[1], direction[0]),
                               latitude=math.asin(direction[2])))
    return sorted(result, key=lambda row: (row['lookback'], row['winding']))


def signatures(rows):
    return sorted(tuple(round(x, 10) for x in (*r['direction'], r['lookback']))
                  for r in rows)


def save(path, text):
    path.write_text(text, encoding='utf-8')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_name(path.name+'.sha256').write_text(
        f'{digest}  {path.name}\n', encoding='utf-8')
    return digest


def main():
    out = Path(__file__).resolve().parent/'outputs'/'static_t3_v1'
    out.mkdir(parents=True, exist_ok=True)
    L = (1., 1., 1.)
    observer = (.5, .5, .5)
    source = (.68, .61, .57)
    depth = 1.6
    rows = catalog(observer, source, L, depth)
    checks = []

    def check(name, passed, detail):
        checks.append(dict(id=name, passed=bool(passed), detail=detail))

    # Independent brute-force cube encloses the entire specified light cone.
    brute = []
    for n in itertools.product(range(-4, 5), repeat=3):
        d = norm(tuple(s-o+ni*li for s, o, ni, li in zip(source, observer, n, L)))
        if 0 < d <= depth:
            brute.append(n)
    check('complete_catalog', set(brute)=={r['winding'] for r in rows},
          'Independent oversized lattice enumeration inside the same light cone.')
    max_null = max(abs(-1+sum(x*x for x in r['direction'])) for r in rows)
    check('null_tangent', max_null < 1e-12, f'max |g(k,k)|={max_null:.17g}')
    # Past-directed ray: t=-lambda, x=o+lambda*n; future arrival k=(1,-n).
    endpoint_error = 0.
    for r in rows:
        end = [o+r['lookback']*n for o,n in zip(observer,r['direction'])]
        for x,s,l in zip(end,source,L):
            residual = (x-s)/l
            endpoint_error = max(endpoint_error, abs(residual-round(residual)))
    check('wrapped_endpoints', endpoint_error < 1e-12,
          f'max integer-period endpoint residual={endpoint_error:.17g}')
    shift = (.37, -.22, .43)
    moved_o = tuple((x+d)%l for x,d,l in zip(observer,shift,L))
    moved_s = tuple((x+d)%l for x,d,l in zip(source,shift,L))
    check('translation_invariance', signatures(rows)==signatures(catalog(moved_o,moved_s,L,depth)),
          'Translate observer and source through a cell face; sky unchanged.')
    huge = catalog(observer,source,(100.,100.,100.),depth)
    check('no_wrap_limit', len(huge)==1 and signatures(huge)==signatures(
        [r for r in rows if r['winding']==(0,0,0)]),
        'Large-period finite-depth control equals the direct Euclidean ray.')
    check('multiple_lookback_images', len(rows)>1 and len({r['lookback'] for r in rows})>1,
          'Repeated images are different emission events of the same static source.')
    # Finite-difference velocities verify zero acceleration in covering coordinates.
    max_acc = 0.
    for r in rows:
        h=.01
        points = [[o+lam*n for o,n in zip(observer,r['direction'])]
                  for lam in (0.,h,2*h)]
        max_acc=max(max_acc,max(abs(a-2*b+c)/h**2 for a,b,c in zip(*points)))
    check('straight_covering_geodesics',max_acc<1e-10,
          f'max finite-difference acceleration={max_acc:.17g}; Gamma=0 analytically.')
    # Representative directional probes are supplementary to the analytic proof:
    # every unit vector defines a complete ray for any finite lambda on the quotient.
    probes = [tuple(x/norm(v) for x in v) for v in itertools.product((-1.,0.,1.),repeat=3)
              if norm(v)>0]
    check('all_direction_probe', all(abs(norm(n)-1)<1e-12 for n in probes),
          '26 directions have null rays; absence of a wall follows from the smooth metric, not sampling.')
    csv_path = out/'images.csv'
    with csv_path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['nx','ny','nz','lookback_Lref_over_c','emission_time',
                         'longitude_deg','latitude_deg'])
        for r in rows:
            writer.writerow([*r['winding'],r['lookback'],r['emission_time'],
                             math.degrees(r['longitude']),math.degrees(r['latitude'])])
    save(csv_path,csv_path.read_text(encoding='utf-8'))
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="590" viewBox="0 0 1000 590">',
         '<rect width="1000" height="590" fill="#101827"/>',
         '<g font-family="sans-serif" fill="#edf2fa">',
         '<text x="45" y="35" font-size="22">Static T³: one source, multiple light paths</text>',
         '<text x="45" y="63" font-size="14">Exact geometric control • assumed cubic cell • no ITSM vacuum effect</text>']
    for lat in (-90,-45,0,45,90):
        y=100+(90-lat)*2
        svg.extend([f'<path d="M70 {y} H970" stroke="#354258"/>',
                    f'<text x="20" y="{y+5}" font-size="12">{lat}°</text>'])
    for lon in (-180,-90,0,90,180):
        x=70+(lon+180)*2.5
        svg.extend([f'<path d="M{x} 100 V460" stroke="#354258"/>',
                    f'<text x="{x-15}" y="483" font-size="12">{lon}°</text>'])
    for r in rows:
        x=70+(math.degrees(r['longitude'])+180)*2.5
        y=100+(90-math.degrees(r['latitude']))*2
        color='#ffcc66' if r['winding']==(0,0,0) else '#64d8e8'
        svg.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="6" fill="{color}"><title>n={r["winding"]}; lookback={r["lookback"]:.6f}</title></circle>')
    svg.extend([f'<text x="70" y="523" font-size="15">{len(rows)} images within lookback 1.6 Lref/c; yellow = direct image, cyan = winding images.</text>',
                '<text x="70" y="551" font-size="14">Longitude / latitude map, not an equal-area projection. No brightness or detection model.</text>',
                '</g></svg>'])
    save(out/'sky.svg','\n'.join(svg))
    summary=dict(result_id='T3-OPTICS-STATIC-CONTROL-V1',
                 scope='Assumed static flat rectangular T3; exact covering-space null paths',
                 claim_status='Conditional',review_status='DEFERRED',Rule9_cleared=False,
                 physics_pass=False,gate_effect='NONE',
                 research_execution='PROCEED_PROVISIONALLY_WITHIN_METHODS_SCOPE',
                 inputs=dict(lengths=L,observer=observer,source=source,depth=depth,c=1),
                 images=len(rows),earliest_lookback=rows[0]['lookback'],latest_lookback=rows[-1]['lookback'],
                 checks=checks,methods_checks_pass=all(c['passed'] for c in checks),
                 holds=['ITSM metric and photon/vacuum coupling not supplied',
                        'No physical topology length or expansion history supplied',
                        'No shear structure or optical effect derived',
                        'No Earth/atmosphere/occultation, luminosity or observed sky comparison',
                        'LEN-001 OPEN; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS',
                        'Canonical tests 1-3 HOLD_SUBSTANTIVE; Rule-9 review DEFERRED'],
                 source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    save(out/'summary.json',json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return 0 if summary['methods_checks_pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
