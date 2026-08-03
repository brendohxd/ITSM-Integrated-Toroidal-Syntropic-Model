# TOP-001 analysis — mathematical template only

**Status:** optional helper for `Theory/Gates/TOP-001/`
**Label:** **mathematical-template-only**
**Not a physics pass of TOP-001**

## Purpose

Provide a **tiny, deterministic** check of fixed-volume rectangular-torus
**shape diagnostics** and free-scalar **mode-lattice anisotropy**, with
refinement and negative controls. Supports Stage S0.4 / S1 of the gate spec only.

## Contents

| File | Role |
|------|------|
| `top001_shape_template_audit.py` | Template audit (no ITSM packaging constants) |
| `outputs/` (created on run) | Deterministic JSON summary |

## Run

```powershell
python Analysis\TOP\TOP-001\top001_shape_template_audit.py
# expect: PASS_TOP001_MATH_TEMPLATE_ONLY
# physics_pass: false
```

## Explicit non-claims

- Not free Casimir stress (use CBR-001 for that)
- Not \(13/12\) attractor, \(H_0\), \(a_0\), or \(\Cobs\)
- Not dynamical modulus action
- Not twisted \(E_2/E_3\) preference
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
