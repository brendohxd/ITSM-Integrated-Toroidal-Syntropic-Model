# TOP-001 analysis — mathematical template only

**Status:** optional helper for `Theory/Gates/TOP-001/`
**Label:** **mathematical-template-only**
**Not a physics pass of TOP-001**

## Purpose

Provide a **tiny, deterministic** check of fixed-volume rectangular-torus
**shape diagnostics**, free-scalar **mode-lattice anisotropy**, and exact
modular-basis identities, with refinement and negative controls. Supports
Stage S0.4 / S1 of the gate spec only.

## Contents

| File | Role |
|------|------|
| `top001_shape_template_audit.py` | **Reviewed biaxial** fixed-volume template (do not overwrite) |
| `top001_s1_triaxial_fixed_volume_audit.py` | **Stage S1** full-triaxial fixed-volume log-shape audit (separate) |
| `top001_s1m_modular_basis_equivalence_audit.py` | **Stage S1.7 / S1M** exact \(SL(3,\mathbb Z)\) basis-equivalence and deformation-separation audit |
| `top001_s1m_physical_cutoff_spectrum_audit.py` | **Stage S1.8 / S1M robustness** complete physical-eigenvalue cutoff spectrum and raw-label-box negative control |
| `outputs/` (created on run) | Deterministic JSON summaries + sha256 sidecars |

## Run

Biaxial scaffold (reviewed):

```powershell
python Analysis\TOP\TOP-001\top001_shape_template_audit.py
# expect: PASS_TOP001_MATH_TEMPLATE_ONLY
# physics_pass: false
```

Stage S1 full triaxial (independent chart; hardened continuation):

```powershell
python Analysis\TOP\TOP-001\top001_s1_triaxial_fixed_volume_audit.py
# expect: PASS_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE
# physics_pass: false
# 9 checks: volume, cubic, non-cubic, smooth cubic approach, permutation
# covariance, refinement <=1%, V-scale invariance, malformed, firewall
```

Stage S1.7 / S1M modular-basis identity:

```powershell
python Analysis\TOP\TOP-001\top001_s1m_modular_basis_equivalence_audit.py
# expect: PASS_TOP001_S1M_MODULAR_BASIS_EQUIVALENCE_TEMPLATE
# physics_pass: false
# exact basis/reindexing identities; not a preferred physical shear
```

Stage S1.8 / S1M physical-cutoff spectrum:

```powershell
python Analysis\TOP\TOP-001\top001_s1m_physical_cutoff_spectrum_audit.py
# expect: PASS_TOP001_S1M_PHYSICAL_CUTOFF_SPECTRUM_INVARIANCE
# 358 modes / 179 eigenvalues in every tested modular chart
# physics_pass: false
```

## Explicit non-claims

- Not free Casimir stress (use CBR-001 for that)
- Not \(13/12\) attractor, \(H_0\), \(a_0\), or \(\Cobs\)
- Not dynamical modulus action
- Not twisted \(E_2/E_3\) preference
- Not physical significance for the labels \(1,4,7\)
- Not cosmology, lensing, SPARC, or NANOGrav

## Negative / refinement controls

1. Cubic limit \(L_1=L_2=L_3\) → mode anisotropy diagnostic \(\approx 0\)
2. Volume held fixed under shape scan
3. Tested non-cubic biaxial shapes → nonzero diagnostic in this chart
4. Grid refinement of truncated mode sums → diagnostic stable within 1%
5. Invalid volume and mode-cutoff domains are rejected
6. Forbidden-packaging flags remain false in JSON

## Claim class

**Open / template-only.** Upgrade requires TOP-001 staged research (S1+ beyond toy).
