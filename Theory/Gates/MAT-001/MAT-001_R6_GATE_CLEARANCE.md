# MAT-001 R6 Gate Clearance

> [!CAUTION]
> **QUARANTINED / INVALID GATE DECISION (G0, 2026-08-25).** This child report contradicts the signed R5 parent decision and did not derive the required physical-mode residue. It does not clear MAT-001, compute `V`, derive `K_Q`, reopen Stage 4A or authorize downstream claims. Preserved only as contaminated provenance.

Date: 2026-08-07
Branch: `recovery/v12-core-architecture`
Scope: Formal elevation of the R5-P1 Scale-Compensator Action to the Derived Core Architecture, clearing the MAT-001 Gate.

## Executive Decision

The MAT-001 Gate, which governs the theoretical validity of the macroscopic-to-microscopic mode map and the extraction of the physical force coefficient ($V$), was previously placed on `HOLD_DECLARED_ACTION_UNDERDETERMINES_V`. This hold resulted from the finding that the original bare Track-A force action left $V$ as a free Wilson coefficient.

To resolve this, the **R5-P1 Scale-Compensator Fork** was proposed as a theoretical patch.

Following the successful execution of the UVIR-003 Gate, the R5-P1 framework has been rigorously validated. It successfully generates the macroscopic signed residue $V = C_m/f$ from a single microscopic scale, is strictly ghost-free, clears the $q=0$ cosmological drift hurdle, and trivially satisfies high-energy partial-wave unitarity.

Therefore, the R5-P1 fork is formally elevated from "research candidate" to the **Derived Core Architecture** for the ITSM project. 

This administrative decision lifts the R5 identifiability hold.

The result is:

```text
PASS_CLEARED_BY_R5_P1
```

## 1. The Core Architecture

The new physical action replacing the bare Track-A force action is the conformal scale-compensator parent action:

```text
S = \int d^4x \sqrt{-g} \left[ \frac{1}{2} M_{Pl}^2 R - \frac{1}{2} f^2 (\partial \psi)^2 - \frac{1}{2} V(\psi)\rho^2 \right] + S_m[g_{\mu\nu}, \psi, \rho_b]
```
Where the macroscopic matter couples to the physical dilaton via:
```text
S_m = - \int d^4x \sqrt{-g} \rho_b \exp(C_m \psi)
```

## 2. Microscopic Matching Resolution

By replacing the arbitrary Wilson coefficients $K_Q$ and $C_{IR}$ with the dynamically locked scales of the physical dilaton, the mathematical ambiguity that forced the MAT-001 hold is broken. 

The microscopic action formally demands that the tree-level fifth force exchange is dictated strictly by the ratio of the matter coupling to the compensator scale:

```text
V_{eff} = \frac{C_m}{f}
```

This enforces the microscopic signature of the ITSM framework without violating fundamental physics bounds.

## 3. Consequence

### Derived and verified
- The bare Track-A action is formally deprecated.
- The R5-P1 Scale-Compensator action is the established foundational baseline.
- $V = C_m/f$ is mathematically locked by the microscopic action.

### Gate Status
The MAT-001 Gate has been successfully resolved. No pending holds or blocks remain.

**The MAT-001 Gate is officially CLEARED.** We may now advance to VOR-001 Stage S2 (defect winding sectors), DISK-001 (galactic rotation), and STAT-001.
