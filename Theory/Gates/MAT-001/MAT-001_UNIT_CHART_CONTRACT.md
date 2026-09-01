# MAT-001 — natural/SI unit-chart contract

**Date:** 2026-08-05
**Branch:** `recovery/v12-core-architecture`
**Subgate:** `PASS_MAT001_UNIT_CHART_CONTRACT_OPEN`
**Contract status:** `FORMALIZED_COEFFICIENT_CHARTS_MATCHING_OPEN`
**V status:** **NOT_COMPUTED**
**MAT-001:** **BLOCKED**
**UVIR-003:** **IN_PROGRESS**
**Stage 4A:** **closed**
**physics_pass:** **false**

## Decision

The existing force-sector formulae are dimensionally closed in their declared
natural-unit, covariant-derivative chart. A universal extra factor of (c^{-2})
must **not** be inserted into (Aq/K_Q) or (Aa_0/K_Q).

The apparent ambiguity comes from using the same symbol (K_Q) for two
different possible SI coefficients. If (x^0=ct), define (K_Q^{(x^0)}) by

\[
\mathcal L_{m kin}^{m SI}
=\frac{K_Q^{(x^0)}}{2}
 \left(U^\mu\partial_\mu\psi_{\rm SI}\right)^2.
\]

If instead the kinetic term is written with coordinate time (t), define

\[
\mathcal L_{m kin}^{m SI}
=\frac{K_Q^{(t)}}{2}
 \left(\frac{d\psi_{\rm SI}}{dt}\right)^2,
\qquad
K_Q^{(t)}=\frac{K_Q^{(x^0)}}{c^2}.
\]

The two dimensionless causality forms are therefore

\[
R_c^{(x^0)}(\theta)
=\frac{3Aq(1+\cos^2\theta)}{K_Q^{(x^0)}},
\]

and

\[
R_c^{(t)}(\theta)
=\frac{3Aq(1+\cos^2\theta)}{K_Q^{(t)}c^2}.
\]

These are the same statement in different coefficient charts. Adding (c^2)
to the first or omitting it from the second mixes conventions.

## Live action provenance

The Core Architecture declares (c=\hbar=1) except when restored for
dimensions. UVIR-003 Stage A uses the unnormalised covariant invariants

\[
\mathcal Q=U^\mu\nabla_\mu\psi,
\qquad
\mathcal Y=h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi,
\]

and the provisional force action

\[
\mathcal L_\psi
=\frac{K_Q}{2}\mathcal Q^2
-A\mathcal Y^{3/2}
-\frac{\gamma}{2M_*^2}(\Delta_U\psi)^2.
\]

Thus (K_Q) is **declared but unmatched**, not absent. No live parent action
relates it to the candidate matter coefficient (C_m).

## Dimension tables

### Natural units

All entries are mass/energy powers with (c=\hbar=1).

| Quantity | Mass dimension |
|---|---:|
| (psi), (C_m) | 0 |
| (a_0), (q=\lVert\nabla\psi\rVert), (mathcal Q), (A) | 1 |
| (mathcal Y), (K_Q), (gamma) | 2 |
| (ho_b), (mathcal L) | 4 |
| (V=C_m/\sqrt{K_Q}) | -1 |

Therefore (Aq/K_Q), (Aa_0/K_Q), and (gamma/K_Q) are dimensionless as
written.

### SI coefficient charts

Here (psi_{\rm SI}) has gravitational-potential units
([\psi]=L^2T^{-2}), (q) and (a_0) have acceleration units, and (C_m) is
dimensionless.

| Quantity | (M,L,T) dimensions |
|---|---|
| (A= C_{\rm IR}/(12\pi G a_0)) | (M L^{-4}T^4) |
| (K_Q^{(x^0)}) | (M L^{-3}T^2=G^{-1}) |
| (K_Q^{(t)}=K_Q^{(x^0)}/c^2) | (M L^{-5}T^4) |
| (V^{(x^0)}=C_m/\sqrt{K_Q^{(x^0)}}) | (M^{-1/2}L^{3/2}T^{-1}=\sqrt G) |
| (V^{(t)}=C_m/\sqrt{K_Q^{(t)}}) | (M^{-1/2}L^{5/2}T^{-2}=c\sqrt G) |

The statement “(V) has dimensions (c\sqrt G)” is therefore true only in
the coordinate-time coefficient chart. It is not a chart-independent SI
statement.

## Matter metric bridge

The candidate conformal metric

\[
\widetilde g_{\mu\nu}
=e^{2C_m\psi_{\rm SI}/c^2}g_{\mu\nu}
\]

has a dimensionless exponent. For nonrelativistic matter with baryonic **mass
density** (ho_b), its candidate weak-field term is

\[
\mathcal L_{\rm int}^{\rm NR}=-C_m\rho_b\psi_{\rm SI}.
\]

If an energy-density convention is used instead, the corresponding (c^{-2})
belongs to the density conversion. The density convention must therefore be
named together with the kinetic chart.

## Response terminology

For the quadratic template

\[
\mathcal L_2=\frac12\psi K_QP\psi-C_m\rho_b\psi,
\qquad \chi=\sqrt{K_Q}\psi,
\]

the distinct objects are:

| Object | Coefficient |
|---|---|
| Canonical matter-source vertex | (V) |
| Mixed field-source response, (chi/\rho_b) | (V/P) |
| Source-source exchange kernel | (-V^2P^{-1}/2) in the stated convention |
| Canonical field propagator | (P^{-1}) |

This template does not replace constraint reduction or projection onto the
live physical eigenmode.

## Reproduce

```powershell
python Analysis\MAT\MAT-001\UNIT_CHART\mat001_unit_chart_contract.py
# expect: PASS_MAT001_UNIT_CHART_CONTRACT_OPEN
# V_status: NOT_COMPUTED; MAT: BLOCKED; Stage4A: CLOSED
```

## Acceptance requirements for a computed V

1. Derive the kinetic and matter coefficients from one declared action.
2. Name the field chart and prove constant-rescaling covariance.
3. Name (x^0=ct) or coordinate time (t) before restoring SI units.
4. State whether (ho_b) is mass density or energy density.
5. Reduce constraints and project the source onto the physical canonical mode.
6. Distinguish canonical vertex, mixed response, and exchange residues.
7. Provide deterministic evidence and exact upstream status contracts.
8. Reopen Stage 4A only after the matched invariant exists.

## Explicit non-claims

- No numerical (K_Q), (C_m), or (V)
- No selected SI observable chart
- No microscopic completion
- No MAT-001 or UVIR-003 PASS
- No Stage 4A unlock
- No downstream Derived observable or manuscript-release claim
