# R4C1-S4C: frame/dust leading-coupling and leakage audit

Date: 2026-09-26. Frozen before the S4C executable or new calculation.
Branch: recovery/v12-core-architecture. Owner: Master Test 1 / conditional
R4C1-v1/B1. Review `DEFERRED`; `Rule9_cleared=false`; `physics_pass=false`;
`gate_effect=NONE`.

## Question and decision boundary

S4B rejected an instantaneous wave-number-independent estimate in its fixed
one-extra-dust-derivative graph norm. Determine whether the leading physical
frame-kinetic/dust-gradient coupling is a *closed* two-variable subsystem
of the full constrained twelve-dimensional scalar evolution at the B1 initial
event. Only if it is closed at leading order, test a constant positive
cross-term symmetrizer of that leading 2-by-2 subsystem. This is a necessary
diagnostic, not a full-IVP or all-sector proof.

Do not alter R4C1-v1, B1 parameters, S1 constraints, the corrected S2
generator, S4A/S4B graph rows, domain or prior receipts. Preserve the old
negative results. At fixed comoving `k=2*pi*n`, let `p=k/a`; use the formal
`p -> +infinity` limit along permitted nonzero torus modes at the B1 `t=0`
event. This limit is mathematical and does not claim physical EFT validity.

## Frozen construction

Pin and verify S4B report, executable, summary and matrix artifact; inherit
their S4A/S3/S2/S1/B1/VARIATION pins and sidecars. In the original
`y=(q,qdot)` chart, use S4A's exact `Fq` and append S4B's row `p*Fq[14,:]`.
Let `Tq` select original full-graph rows

    (0,2,3,5,6,8,9,10,11,12,13,15).

The last selected row replaces S4A's row 14 by `p` times that row. Check
exactly that `det(Tq)` equals `p` times the inherited nonzero S4A original
minor. `Tq` is a coordinate chart, **not** a uniformly equivalent norm to
the complete 16-row S4B graph.

Define two physical original-chart vectors by `Tq*y_f=e_8` (unit frame
kinetic graph coordinate) and `Tq*y_d=e_11` (unit extra dust-gradient graph
coordinate), using exact S4A density-row reconstruction. Check their full
16-row graph data, the density constraint and regularity of the reconstruction
coefficient on `p>0,H>0`. Construct corresponding canonical `Z_f,Z_d` with
the pinned time-dependent `R,Rdot` map. Keep `H` symbolic while fixing the
other B1 initial coefficients exactly; verify those coefficients against the
pinned numerical B1 initial state.

With the unmodified `A=[[0,I],[-W,-G]]` and `W=Vc+Mcdot`, calculate all
16 components of `(F1dot+F1*A)*Z_f` and `(...)*Z_d`. For each component,
cancel the rational expression in positive `p` and report its exact leading
degree and coefficient (numerator degree minus denominator degree), including
zeros and any growth faster than `p`. Validate that the two columns together
reproduce S4B's exact `r_1(p)/p -> sqrt(6)/2` witness for `Z_f+Z_d`.

The source graph vectors tend to rows 11 and 15 as `p -> infinity`. A
two-variable leading `O(p)` subsystem is **closed** only if every component
outside those rows has degree less than 1, with no higher-than-1 degree
anywhere. If this fails, record the explicit leakage rows/coefficients and
stop short of an isolated symmetrizer claim. Do not infer full-system
ill-posedness from leakage.

If and only if closure passes, form the exact 2-by-2 leading block from
rows 11 and 15 and the two data columns. Solve the constant real symmetric
`P B+B^T P=0` equations for `P>0` in the fixed S4B graph units. Report the
positive-definiteness conditions or a proof of failure. Even a successful
leading symmetrizer does not control subprincipal terms, time dependence,
constraint reconstruction or the full twelve-dimensional system.

## Rejection controls and output

Reject mismatched source hashes/sidecars, wrong graph shape, swapped frame/
dust columns, omitted `Rdot`, omitted `F1dot` (including `pdot=-H p`), or
incorrect `W=Vc+Mcdot`. An exact consistency check must recover both the
S4B source graph support and witness limit. Failed or unevaluated symbolic
checks produce `UNVALIDATED`; do not weaken equalities or alter the chart.

Record exact columns, degrees/coefficient table, leakage/closure decision,
any conditional 2-by-2 symmetrizer and source hashes in JSON. If a symbolic
step exceeds a bounded attempt, preserve the partial evidence and report it
as `INCOMPLETE`, not as closure or failure. No new observational comparison,
parameter tuning, canonical promotion or publication claim is authorized.
Rule-9 review remains deferred and inherited; full constrained IVP,
homogeneous/singular branches, causality, cutoff, healthy GR recovery and
physical matching remain substantive holds.
