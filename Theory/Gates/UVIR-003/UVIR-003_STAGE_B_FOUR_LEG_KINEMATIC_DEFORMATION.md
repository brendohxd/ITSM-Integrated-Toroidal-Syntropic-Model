# UVIR-003 Stage B — four-leg kinematic deformation audit

Date: 2026-08-01

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS**

Subgate:
`PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Physical `2-to-2` status:
**LOCAL DEFORMED KERNEL AUDITED; COSMOLOGICAL S-MATRIX NOT ESTABLISHED**

## Result

The local exchange-plus-reduced-contact four-leg kernel was extended off the
regular-tetrahedral slice using an isosceles disphenoid family of equal-magnitude
momenta with

```text
alpha = beta = -q^2/3 + delta,
gamma = -q^2/3 - 2 delta,
alpha + beta + gamma = -q^2.
```

Channel momenta

```text
q_s = sqrt(2q^2 + 2 alpha),  q_t = sqrt(2q^2 + 2 beta),  q_u = sqrt(2q^2 + 2 gamma)
```

are independent. At `delta = 0` the geometry recovers the tetrahedron
(`q_s = q_t = q_u = 2q/sqrt(3)`).

Across the default grid (external `q/H ∈ {50,75}`, `delta/q^2 ∈ {0,0.05,0.10,0.15,0.20}`,
three mode pairs → 30 cases):

| Diagnostic | Value |
|------------|-------|
| Combined kernels finite | yes |
| Combined kernels nonzero | yes |
| Max imag fraction | < 1e-8 |
| Min pole separation | ~0.059 |
| Max tetra-baseline match error (`delta=0` vs alpha.9 summary) | ~3.5e-14 |
| Domain-failure cases (exact channel ratio not admitted) | 6 / 30 |
| Near-homogeneous flags (`q_K/q < 0.15`) | 0 |

Record `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT`.

Domain admission failures at some deformed channel ratios are **reported**, not
swept under a hard fail of the kernel assembly: the kernel remains finite/real
while the controlled-exchange domain gate is not satisfied for every exact
internal ratio. This is part of the pole/homogeneous approach audit, not a
unitarity claim.

## Scientific boundary

Established:

- local kernel assembly off tetrahedron on the declared isosceles disphenoid family;
- recovery of the alpha.9 tetrahedral baseline at `delta=0`;
- pole-distance and domain-admission diagnostics under deformation.

Not established:

- asymptotic FRW in/out states / S-matrix;
- optical theorem / partial-wave unitarity;
- strong-coupling scale or physical cutoff;
- denser approach to the exact homogeneous channel (`gamma → -q^2`);
- nonzero-gradient `|grad(pi)|^3` sector;
- MAT-001.

## Reproduction

```powershell
conda activate itsm_env
cd Analysis\UVIR\UVIR-003
python uvir003_four_leg_kinematic_deformation.py
```

Outputs:

- `outputs/uvir003_four_leg_kinematic_deformation_summary.json`
- `outputs/uvir003_four_leg_kinematic_deformation.csv`

Expected footer:

```text
STATUS: PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT
```

## Dense-edge follow-up

Optional denser scan toward the homogeneous edge:

```powershell
python uvir003_four_leg_kinematic_deformation.py `
  --ratios 50 --deltas 0.0 0.10 0.20 0.25 0.28 0.30 0.31 `
  --mode-pairs "0,0;1,1" --output-tag dense_edge
```

Outputs: `uvir003_four_leg_kinematic_deformation_dense_edge_summary.json`.  
On 2026-08-01 this still returns `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT`
with more domain-admission failures as $q_u/q$ decreases and smaller min pole
separation — expected approach behavior, not unitarity.

## Next required calculation

1. ~~Optional denser `delta` scan~~ (done as `dense_edge` tag).  
2. ~~Local adiabatic packet observable normalization~~ (see
   `UVIR-003_STAGE_B_LOCAL_ADIABATIC_OBSERVABLE_NORM.md`).  
3. Promote packet proxy toward true in-in correlator on FRW trajectory.  
4. Derive nonzero-gradient exact-`|grad(pi)|^3` contribution.  
5. Only then formulate a declared perturbative-unitarity / EFT-validity criterion.
