# R4C1-S4E: phase-pair graph-equivalent reweight screen

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
This contract is fixed before the S4E executable and calculation. Review is
`DEFERRED`; `Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.

## Question and frozen inputs

S4D found that selected-chart phase-gradient coordinate `e_7` drives the
phase-kinetic graph row 9, selected-chart coordinate `e_6`, at exact order
`p^2` with coefficient `sqrt(165)/33`. Test whether **any positive diagonal
reweighting of this selected chart that is uniformly equivalent to the full
S4B 16-row graph norm** can make this off-diagonal term `O(p)`. This is only a
necessary screening test for a graph-equivalent principal estimate. A
non-diagonal symmetrizer or a different, explicitly non-equivalent space is
outside its no-go claim.

Pin the S4D report `9479d990e612658d08c68c8a7e2521c1f4a11461a49946e5be6ff73d240f4a2e`,
contract `3cd2ad808053862ca1d947bae4ae0d69b46e8fdae415706b3f332cf3867aede1`,
executable `e11b15b7b8cd8d7a1c513fec5fd611b7a83269b409097dfba9a394a0577f32c1`,
attempt-02 summary `319ce57136468f51eb4040c4362d12efa0da08106dc68ed3e5a0c1d354b60097`,
and exact detail `719d011083ae8c7f5a80b00c210d58e138aa49b07dbbbf3b1cc666c954f2e9f0`.
Verify sidecars and the inherited S4C/S4B/S4A/S3/S2/S1/B1/variation pins
through the S4D verifier. Do not call any prior receipt-writing `main()`.
The R4C1 action, B1 state, S2 generator, S4B graph, S4C chart and S4D result
are unchanged.

Use the exact S4C B1 initial substitutions with symbolic fixed `H>0` and
`p=k/a>0` along nonzero torus modes. The selected full-graph rows are
`(0,2,3,5,6,8,9,10,11,12,13,15)`. Treat this as a finite-mode coordinate
chart, not a uniformly equivalent norm by assumption. Retain `pdot=-Hp`,
time-dependent `R,Rdot`, `F_1dot` and corrected `W=Vc+Mcdot`.

## Exact calculation and decision

1. Reconstruct the exact chart inverse and canonical initial-data columns for
   `e_6`, `e_7` and S4D's unprocessed `e_9`. For each, calculate all 16 entries
   of the full graph source `g_i=F_1 Z_i` and full evolution
   `ell_i=(F_1dot+F_1 A)Z_i`; record exact rational large-`p` degree and
   leading coefficient, including zeros. Check `T_q y_i=e_i`, full-graph
   reconstruction, and S4D's saved `e_7` column exactly.
2. Let `Q=F_1 Z(c)` and let `B_{ji}` be the evolution in selected chart rows.
   Independently verify `g_7` has exactly unit row 10, `g_6` has selected row
   9 equal to one, and `B_{6,7}/p^2 -> sqrt(165)/33`. The last limit must be
   checked both by rational polynomial leading terms and a direct SymPy limit.
3. For arbitrary positive diagonal `D(p)=diag(d_i(p))`, suppose constants
   `0<m<=M<infinity`, independent of `p`, satisfy
   `m ||Q c|| <= ||D c|| <= M ||Q c||` for every chart vector and all
   sufficiently large registered modes. Unit `e_7` gives `d_7<=M`; unit
   `e_6` and `||Q e_6||>=1` give `d_6>=m`. Therefore the off-diagonal
   transformed generator obeys
   `|B^D_{6,7}|=(d_6/d_7)|B_{6,7}| >= (m/M)|B_{6,7}|`, so it is not `O(p)`.
   `Ddot D^-1` is diagonal and cannot cancel this entry. Record
   `DIAGONAL_GRAPH_EQUIVALENT_ORDER_P_REJECTED` only if every premise is
   exactly verified; otherwise record `INCOMPLETE`, not a no-go.
4. Classify all full-graph outputs from `e_6` and `e_9`, including every
   order-`p` or faster selected and unselected row. Record the further
   coordinates required for a complete principal-span calculation. Do not
   truncate the pair into a putative closed physical subsystem or infer an
   IVP result from this three-column screen.

Reject changed pins or sidecars, a wrong row map, omitted time derivatives,
wrong `Mcdot`, an incomplete 16-row scan, inconsistent `e_7` replay or an
incorrect large-`p` coefficient. A deliberate bad digest must fail the pin
comparison in memory without altering files. A bounded timeout is
`INCOMPLETE`. Preserve all prior receipts and use a fresh S4E attempt
directory that refuses overwrite.

The output is an S4E-only exact JSON receipt and report with source hashes,
domain, local checks and the narrow conclusion. The possible no-go applies
only to diagonal graph-equivalent chart reweightings at the registered B1
event. Non-diagonal symmetrizers, non-equivalent Sobolev spaces, finite-time
transfer, homogeneous/singular sectors, physical EFT cutoff, GR recovery and
canonical Test-1 acceptance remain open. Test 2, Test 3, MAT-001, UVIR-003,
Stage 4A and publication statuses do not change.
