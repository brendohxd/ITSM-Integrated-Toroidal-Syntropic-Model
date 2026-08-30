# MAT-001 RG1 hostile R5-P1 and M1-M5 comparison

**Parent status:** `BLOCKED`  
**Invariant vertex:** `V NOT_COMPUTED`; `K_Q NOT_DERIVED`

## A0-A2 matrix

| Route | A0 | A1 | A2 | RG1 disposition | Decisive reason |
|---|---|---|---|---|---|
| R5-P1/M1-current | FAIL | FAIL | FAIL | `REJECT_CURRENT_INSTANTIATION` | real compensator toy replaces the required finite-density complex condensate; f and ell remain free; no constrained signed physical residue; Cassini inequality fails its own numbers |
| M1-redesign | OPEN | OPEN | OPEN | `DO_NOT_ADVANCE_RG1` | requires a new complete parent action and cannot inherit evidence from rejected R5-P1 |
| M2 | OPEN | OPEN | OPEN | `ADVANCE_CHEAP_REDUCTION` | closest microscopic test of whether the declared condensate radial/heavy sector generates a static matter vertex; falsifiable by absent source or independent soft coefficient |
| M3 | OPEN | OPEN | OPEN | `HOLD` | no single parent portal currently prevents appended coupling or double counting |
| M4 | PASS_METHOD | BLOCKED_BY_PARENT | OPEN | `ADVANCE_INVARIANT_RESIDUE_CONTROL` | directly asks for the chart-invariant source-pole residue and can kill normalization artifacts without assigning bare K_Q |
| M5 | OPEN | OPEN | OPEN | `HOLD_PENDING_T1_T2` | normalized moduli/winding modes and matter coupling are absent; inserting L=c/H, 2*pi, 2/3, or a cycle count is forbidden |

## Hostile R5-P1 finding

The current R5-P1 chain does not satisfy its own specification. Its source is
a toy static `alpha rho_b` term rather than a derived vertex of the declared
finite-density parent; the compensator is a real scalar, `f` and `ell` remain
free, the full constraint/ghost reduction and signed physical pole residue are
missing, and the reported `alpha ~= 0.016` exceeds its own Cassini requirement
`alpha < 0.0022`. Contact energy-independence is not a unitarity proof, and a
conformal scalar does not independently supply lensing. The current
instantiation is rejected/quarantined; this is not a no-go for every M1 design.

## RG1 bounded selection

Advance **M4** only as an invariant-residue/null control and **M2** only as a
cheap explicit radial/heavy-mode integrate-out. Neither is a physics pass.
M4 must expose chart/source-normalization dependence; M2 must include the
static matter interaction and derive `g_phys/sqrt(Z_phys)`. Stop either route
at its first A0-A2 kill criterion.
