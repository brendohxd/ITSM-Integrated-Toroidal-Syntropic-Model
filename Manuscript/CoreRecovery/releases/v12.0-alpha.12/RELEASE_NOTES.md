# ITSM Core v12.0-alpha.12

Date: 06 August 2026  
Label: Hold retained; MAT Conditional interface and matching incompleteness

## Scientific checkpoint

This release freezes the **dual-status** post-alpha.11 recovery boundary. It
does **not** close UVIR-003, unlock MAT-001, compute $V$, or reopen Stage 4A.

- Stage 5 remains `HOLD_TIER1_CLOSURE` / `PASS_STAGE5_DECISION_HOLD_TIER1`.
  UVIR-003 remains `IN_PROGRESS`; M2, M3, M6 and M7 still block tier-1 closure.
- MAT-001 remains `BLOCKED`. A Conditional Track-A force-host kit exports
  form-level $S_{\rm int}$ and matter covectors $d=(-C_m)$, $h=(0,0)$ with
  symbolic host $K_Q$ only. Free-sector ADM is **not** identified with Track-A.
- Dual-status Conditional matching probes are open for diagnostics only; they
  are not Derived $V$ or $K_Q$.
- Parent-action matching for absolute $Z_\phi$ and $g_\phi$ is audited
  **incomplete** (research requirements RR1--RR5 open).
- TOP/VOR remain open scaffolds (`physics_pass: false`). WAK/RES retain
  `NOT_SELECTED` route decisions.

## Manuscript integration

- Working draft date marker advanced to after alpha.11.
- New dual-status subsection in scope/status; open-gates MAT/UVIR wording updated.
- Abstract and conclusion state the hold and incompleteness without claim promotion.

## Explicit non-claims

No tier-1 UVIR closure, numeric Derived $K_Q$, numeric $V$, MAT PASS, Stage 4A
reopen, selected wake/reservoir identity, or derived SPARC/$H_0$/lensing
packaging is created by this release.

## Immutable path

```text
Manuscript/CoreRecovery/releases/v12.0-alpha.12/
```
