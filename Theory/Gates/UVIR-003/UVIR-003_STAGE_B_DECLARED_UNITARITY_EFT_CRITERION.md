# UVIR-003 Stage B — Declared unitarity / EFT criterion (scoped)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (criterion declared and checked; theory not closed)

Subgate:
`PASS_DECLARED_UNITARITY_EFT_CRITERION`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

## Purpose

State an explicit, machine-checked **perturbative-unitarity / EFT-validity
criterion package** for the two sectors that alpha.10 has actually constructed:

1. **L** — Track-A local nonzero-gradient force (`PASS_NONZERO_GRADIENT_FORCE_LOCAL`)
2. **G** — high-$q$ mode-projected Green proxy (`PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN`)

This is a **declared criterion**, not a completed optical theorem and not a
physical cutoff with matched $K_Q$.

## Sector L (local force)

Canonical cubic coupling (longitudinal):

\[
g_3 = \frac{A_{\mathrm{IR}}}{K_Q^{3/2}},\qquad
\Lambda_\parallel = \frac{K_Q^{3/4}}{\sqrt{A_{\mathrm{IR}}}}.
\]

Tree parallel vertex (canonical $\chi=\sqrt{K_Q}\,\pi$):

\[
|V_\parallel(q)| = \frac{6 A_{\mathrm{IR}} q^3}{K_Q^{3/2}}.
\]

s-wave proxy (O(1) NDA, not a proof):

\[
u_L(q) := \frac{|V_\parallel(q)|}{16\pi}.
\]

**Declared weak-coupling window:**

\[
\frac{q}{\Lambda_\parallel}\le r_{\max}
\quad\text{and}\quad
u_L(q)\le u_{\max}
\]

with defaults $r_{\max}=0.3$, $u_{\max}=1$.

## Sector G (high-$q$ Green)

Inherited health checks from the multi-slice Green PASS:

- prior subgate PASS  
- multi-slice $|K|$ relative span $\le 0.25$  
- finite positive $G_{\mathrm{proxy}}$ diagnostic  
- causal Green with diagonal = local $K$  
- **IR transfer HOLD modes remain out of scope**

## Joint PASS meaning

Both sector diagnostics pass and the L-domain is non-empty.  
It does **not** mean UVIR-003 is closed.

## Explicit non-claims

| Claim | Status |
|-------|--------|
| Optical theorem / multi-channel unitarity | **NOT_COMPUTED** |
| Physical strong-coupling cutoff | **NOT_ESTABLISHED** ($K_Q$ matching open) |
| Homogeneous FRW S-matrix | **NOT_ESTABLISHED** |
| MAT-001 | **BLOCKED** |
| Full UVIR-003 gate | **IN_PROGRESS** |

## Reproduction

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_declared_unitarity_eft_criterion.py
# expect: PASS_DECLARED_UNITARITY_EFT_CRITERION
```

Outputs:

- `outputs/uvir003_declared_unitarity_eft_criterion_summary.json`
- `outputs/uvir003_declared_unitarity_eft_criterion_scan.csv`

## Alpha.10 subgate chain (post–alpha.9 working, not manuscript freeze)

1. `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT`  
2. `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION`  
3. `PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED`  
4. `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN`  
5. `PASS_NONZERO_GRADIENT_FORCE_LOCAL`  
6. `PASS_DECLARED_UNITARITY_EFT_CRITERION` ← this note  

## Next

- $K_Q$ / force normalization matching (shared blocker with causality NDA)  
- Optional: anisotropic force vertex → multi-slice Green source  
- Manuscript freeze **alpha.10** when ready to record the chain immutably  
