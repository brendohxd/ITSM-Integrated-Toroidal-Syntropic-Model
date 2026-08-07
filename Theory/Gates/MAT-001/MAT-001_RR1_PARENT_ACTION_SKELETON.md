# MAT-001 RR1 parent-action skeleton

**Status:** `PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED`  
**RR1:** `DECLARED_SKELETON_COEFFICIENTS_UNMATCHED`  
**V:** **NOT_COMPUTED** · **Stage 4A:** **CLOSED** · **MAT:** **BLOCKED**

## Declared terms (same action)

| Term | Form |
|---|---|
| Parent kinetic | \((Z_\phi/2)(U\cdot\nabla\phi)^2\) |
| Matter vertex | \(-g_\phi\rho_b\phi\) |
| IR map | \(\psi=f_\phi\phi\), Track-A \(\psi=\psi_{\rm bar}+\pi\) |
| Induced | \(C_m=g_\phi/f_\phi\), \(K_Q=Z_\phi/f_\phi^2\), \(V=g_\phi/\sqrt{Z_\phi}\) |

Track-A IR force Lagrangian \(K_Q Q^2/2 - A Y^{3/2}-\cdots\) remains the host
EFT; matching requires \(K_Q^{\rm IR}=Z_\phi/f_\phi^2\) in the same chart.

## Unmatched

\(Z_\phi\), \(g_\phi\), \(f_\phi\) numeric/map values — **NOT_DERIVED**.

## Reproduction

```text
python -B Analysis/MAT/MAT-001/PARENT_ACTION_MATCHING/mat001_rr1_parent_action_skeleton_declaration.py
# STATUS: PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED
# SHA-256: 439D2EFAEAF98343F61250E36F7608F78772F0DCD77D839E274D0717C12F5BEC
```

## Next

**RR2:** derive or bound \(Z_\phi,g_\phi\), or compute residue \(V\).  
Do not treat this skeleton as Derived matching.
