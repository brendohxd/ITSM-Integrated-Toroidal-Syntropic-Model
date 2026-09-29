# R4C1-S4D: recursive leading-span diagnostic

Date: 2026-09-26. Branch: `recovery/v12-core-architecture`. Owner: Master
Test 1 / conditional R4C1-v1/B1. This contract is frozen before its S4D
executable or calculation. Review `DEFERRED`; `Rule9_cleared=false`;
`physics_pass=false`; `gate_effect=NONE`.

## Question and fixed inputs

S4C proved that the proposed frame/dust pair is not closed at order `p` in
the complete 16-row S4B graph: its frame input leaks into rows 10 and 12.
Starting from the S4C chart coordinates `(8,11)`, recursively include the
selected-chart coordinates whose order-`p` evolution is forced by the current
span. Determine whether this bounded leading-span construction closes, or
identify the first obstruction. Do not infer a symmetrizer or IVP estimate
from closure alone.

Pin the S4C report, executable, summary and detail artifacts (SHA-256 in the
S4C report), including their sidecars. Verify the transitive S4B/S4A/S3/S2/
S1/B1/variation pins through the S4C verifier. Do not rerun any prior `main()`
that would overwrite its receipt. Keep the R4C1 action, B1 initial data, S2
generator, S4B graph and S4C chart unchanged.

At the B1 initial event use the exact S4C substitutions, symbolic `H>0`,
`p=k/a>0`, and the formal limit along nonzero torus modes. Reconstruct the
same twelve-dimensional original chart with selected graph rows
`(0,2,3,5,6,8,9,10,11,12,13,15)`. This minor is a finite-mode coordinate
chart, not a uniformly equivalent replacement for the full graph norm.
Preserve `pdot=-H p`, the time-dependent `R,Rdot` reconstruction, and the
corrected `W=Vc+Mcdot` in every evolution column.

## Calculation and decision rule

For each needed selected-chart unit coordinate `e_i`, solve `Tq*y_i=e_i`
exactly, map `y_i` to canonical `Z_i`, and evaluate all sixteen entries of
`g_i=F_1 Z_i` and `ell_i=(F_1dot+F_1 A)Z_i`. Record the exact rational
large-`p` degree and coefficient, including zeros. Independently recover
S4C's frame/dust graph supports and order-`p` leakage before extending them.

Starting with indices `{8,11}`, add selected-chart indices receiving a
nonzero order-`p` or faster contribution from any current member. Iterate
only over newly added indices until no new index occurs or an obstruction is
found. Check all sixteen output rows at every stage; an unselected output
cannot be silently discarded. Compare the leading full-graph output with
the source-graph embedding of its selected-chart coordinates. If the
order-`p` residual outside that embedding is nonzero, record
`FULL_GRAPH_LEAKAGE`, not closure. Record the full-graph growth of every
source direction. If a newly required `e_i` has a full-graph norm that grows
with `p`, or a degree faster than `p` appears, stop this unweighted-chart
closure test as `CHART_REWEIGHT_REQUIRED` and report exact witnesses. Do not
call the span closed or claim instability. If the recursion terminates
without those obstructions, record the exact finite-mode leading block and
its full-graph embedding; positivity or a symmetrizer is a separate contract.

Reject changed pins/sidecars, wrong chart or source graph shape, missing
`Rdot`, missing `F_1dot`/`pdot`, omitted `Mcdot`, an incomplete row scan, or
failure to reproduce the S4C two-column result. A bounded symbolic timeout
is `INCOMPLETE`, not closure. Preserve failed attempts and previous receipts.

The output is a new S4D-only JSON receipt and report with exact source
hashes, local checks, domain and first obstruction or closed span. Inherit
`R9-MT1-S4C` and its registered dependencies. Full constrained IVP,
homogeneous/singular branches, all-sector stability, causality, EFT cutoff,
GR recovery and physical matching remain open. Master Test 1, MAT-001,
UVIR-003 and downstream canonical/publication statuses are unchanged.
