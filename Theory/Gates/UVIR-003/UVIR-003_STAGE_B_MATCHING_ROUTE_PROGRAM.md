# UVIR-003 Stage B — Matching-route program (R2 interface + R3 sketch)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (program executed; matching still **Open**)

Subgate:
`PASS_MATCHING_ROUTE_PROGRAM_OPEN`

Claim status: **Conditional structure + Open routes** (not Derived \(K_Q\))

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Numeric \(K_Q\): **NOT_DERIVED**

Master Plan criteria: M3 still PARTIAL (maps ready); M6 still OPEN; M7 OPEN

## Purpose

Advance the Master Plan critical path **after** inventory + Conditional causality
domain: for each named matching route, write **closed-form maps** of the primary
invariants \(Aq/K_Q\) and \(A/K_Q^{3/2}\), state DOF counting, and run Conditional
scans — without packaging a Derived \(K_Q\).

## Structural theorem (R2)

**Static \(\Cobs\) alone cannot fix \(Aq/K_Q\).**

Architecture weak-field reduction gives

\[
A=\frac{C_{\mathrm{IR}}}{12\pi G a_0},\qquad
\Cobs=\frac{C_m^{3/2}}{\sqrt{C_{\mathrm{IR}}}}.
\]

The long-wavelength causality ratio needs absolute \(K_Q\) (or a combination that
contains it). The redefinition-invariant **vertex residual**

\[
V := \frac{C_m}{\sqrt{K_Q}}
\]

closes the gap: once \(\Cobs\), \(C_{\mathrm{IR}}\), and \(V\) are known,

\[
I_{a_0} \equiv \frac{A a_0}{K_Q}
= \frac{C_{\mathrm{IR}}^{1/3}\, V^{2}}{12\pi G\, \Cobs^{4/3}}.
\]

Here \(Aq/K_Q\) is the field-redefinition invariant. The displayed
\(I_{a_0}\) is its named \(q=a_0\) field-chart diagnostic; if \(a_0\) is held
external under \(\psi\mapsto s\psi\), then \(I_{a_0}\mapsto I_{a_0}/s\).
The route algebra below remains valid on that declared chart.

**MAT-001 must compute \(V\) (and preferably \(\Cobs\)) from one \(S_{\mathrm{int}}\).**
Until then R2 remains Open; the *interface algebra* is ready.

## Route summary

| Route | Status | What it maps | Free after form |
|-------|--------|--------------|-----------------|
| **R1** | Conditional | chart-fixed \(I_{a_0}=(2/3)C_{\mathrm{IR}}/k_Q\) | \(k_Q\), \(C_{\mathrm{IR}}\) |
| **R2** | Open (interface ready) | chart-fixed \(I_{a_0}\) via \((\Cobs,C_{\mathrm{IR}},V,G)\) | \(V\) (MAT), \(\Cobs\), \(C_{\mathrm{IR}}\) |
| **R3** | Open (Conditional sketch) | chart-fixed \(I_{a_0}=(2/3)C_{\mathrm{IR}}/(Z_\psi r_\rho)\) | \(Z_\psi\), \(r_\rho\), \(C_{\mathrm{IR}}\) |
| **R5** | Conditional phenom | \(\Cobs\) only | does **not** fix \(K_Q\) alone |

**R3 ↔ R1:** under the residual ansatz \(K_Q=Z_\psi\rho_\Phi/a_0^2\) with
\(r_\rho=\rho_\Phi/(M_P^2 a_0^2)\), the product \(Z_\psi r_\rho\) plays the role of
R1’s \(k_Q\). Naive R1 is the special case \(Z_\psi r_\rho=1\).

## Headline numerics (Conditional)

| Point | \(I_{a_0}\) | \(R_c(\parallel,q=a_0)\) | \(q_\times/a_0\) (∥) |
|-------|-------------|---------------------------|---------------------|
| R1 naive \((k_Q,C_{\mathrm{IR}})=(1,2/3)\) | \(4/9\) | \(8/3\approx 2.67\) | \(0.375\) |
| R3 scan (default grids) | varies | **25%** of samples causal at \(q=a_0\) ∥ | — |

Larger \(V\) (R2) **shrinks** the causal window (larger \(I_{a_0}\)).

## Explicit non-claims

| Claim | Status |
|-------|--------|
| Numeric \(K_Q\) Derived | **NOT_DERIVED** |
| \(V\) from \(S_{\mathrm{int}}\) | **NOT_COMPUTED** (MAT blocked) |
| \(Z_\psi,r_\rho\) from \(S_\Phi\) | **NOT_DERIVED** (sketch only) |
| UVIR-003 M3/M6 closed as Derived | **NO** |
| MAT-001 unlock | **BLOCKED** |

## Reproduce

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_matching_route_program.py
# expect: PASS_MATCHING_ROUTE_PROGRAM_OPEN
```

Outputs:

- `outputs/uvir003_matching_route_program_summary.json`
- `outputs/uvir003_matching_route_R2_scan.csv`
- `outputs/uvir003_matching_route_R3_scan.csv`

## Next required calculation

1. **Stage 2a complete:** `INCOMPLETE_R3_UV_RESIDUE`; no action-level value or bound found.
2. **Stage 2b next:** write the explicit Conditional matching floor and MAT-only handoff scope.
3. **R2:** compute \(V=C_m/\sqrt{K_Q}\) only when the scoped handoff permits calculation.
4. Re-evaluate causality + \(\Lambda_\parallel\) under the Stage 2b floor (Stage 2c).
5. **Never** promote R1/R3 naive values to Derived.
