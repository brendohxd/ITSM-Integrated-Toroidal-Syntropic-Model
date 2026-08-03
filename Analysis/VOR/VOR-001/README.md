# VOR-001 analysis — mathematical template only

**Status:** optional helper for `Theory/Gates/VOR-001/`
**Label:** **mathematical-template-only**
**Not a physics pass of VOR-001**

## Purpose

Provide a **tiny, reproducible** check that topological winding integers on a
periodic cell can be separated from continuous local phase data, with
**negative controls**. This supports Stage S0.4 of the gate spec only.

## Contents

| File | Role |
|------|------|
| `vor001_winding_template_audit.py` | Template audit (no physical constants from ITSM packaging) |
| `outputs/` (created on run) | JSON summary of template checks |

## Run

```powershell
python Analysis\VOR\VOR-001\vor001_winding_template_audit.py
# expect: PASS_VOR001_MATH_TEMPLATE_ONLY
```

## Explicit non-claims

- Not a derivation of \(a_0\), \(\Cobs\), \(H_0\), or PTA frequencies
- Not a superfluid action validation
- Not UVIR / MAT / TOP closure
- Not restoration of lunar SWNT or historical numbers
- Wilson coefficients are **absent by design** (template uses dimensionless toy energy)

## Negative controls (must pass as controls)

1. Trivial winding \(\mathbf{n}=\mathbf{0}\) → holonomy integrals vanish
2. Forced smooth density floor \(\rho\ge\rho_{\min}\) on a defect-like profile →
   core indicator turns off
3. Non-integer fake “winding” → rejected by integer check
4. Under-resolved winding with phase advance at the Nyquist boundary → rejected
   before holonomy estimation

## Claim class

**Open / template-only.** Upgrade requires VOR-001 staged research (S1+).
