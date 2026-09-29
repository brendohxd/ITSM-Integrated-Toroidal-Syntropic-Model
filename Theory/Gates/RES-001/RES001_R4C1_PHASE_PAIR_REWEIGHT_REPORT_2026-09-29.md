# R4C1-S4E: phase-pair and diagonal-reweight disposition

Date: 2026-09-29. Master Test 1; conditional R4C1-v1/B1. The
[frozen S4E contract](RES001_R4C1_PHASE_PAIR_REWEIGHT_CONTRACT_2026-09-29.md)
pins S4D and its transitive sources. Review is DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
This is an exact formal high-frequency calculation at one B1 initial event,
not a physical EFT-limit calculation or a full constrained-IVP estimate.

## Narrow decision

The proposed **uniformly full-graph-equivalent diagonal chart reweighting**
cannot turn the S4D phase coupling into an entrywise order-p generator.
The local receipt status is DIAGONAL_GRAPH_EQUIVALENT_ORDER_P_REJECTED.
It does **not** reject a non-diagonal symmetrizer, an explicitly different
Sobolev domain, or a finite-time solution estimate.

There is also a constructive reason not to call S4D's p-squared term an
instability. In the exact S4C selected chart, let B be the generator
defined by selected rows of the complete 16-row evolution. Only the
listed columns of B are calculated here. For coordinates e_6
(full graph row 9, phase kinetic) and e_7 (row 10, phase gradient),

\[
 \lim_{p\to\infty}p^{-2}B_{\{6,7\},\{6,7\}}
 =\frac{\sqrt{165}}{33}
   \begin{pmatrix}0&1\\-1&0\end{pmatrix},
 \qquad H>0,\quad p=k/a>0 .
\]

The exact graph sources are Qe_6=f_9 and Qe_7=f_10, where f_r
is the unit vector in full-graph row r. Thus this *restricted principal
pair* is skew in its source graph coordinates: its order-p-squared
contribution to the pair's Euclidean energy derivative cancels. A
separate read-only SymPy limit of the saved exact rational expressions
gave B_7,6/p^2 -> -sqrt(165)/33, B_6,7/p^2 -> sqrt(165)/33, and
(B_7,6+B_6,7)/p^2 -> 0. The full 12-column principal matrix was not
computed, so this cancellation is **not** a full-system symmetrizer or
stability theorem.

## Why the diagonal order-p route fails

Suppose a positive diagonal chart weighting D(p)=diag(d_i(p)) satisfies
uniform full-graph equivalence

\[
 m\|Qc\|\leq\|Dc\|\leq M\|Qc\|,\qquad 0<m\leq M<\infty,
\]

for every chart vector and all sufficiently large registered modes. Since
the exact stored columns give ||Qe_6||=||Qe_7||=1, both d_6 and d_7
lie between m and M. The off-diagonal transformed entry is
B^D_6,7=(d_6/d_7)B_6,7; the time-dependent term Ddot D^-1 is
diagonal. Hence |B^D_6,7| >= (m/M)|B_6,7|, and the verified
positive sqrt(165)/33 times p-squared leading term cannot be O(p).
This necessary-condition argument uses arbitrary positive diagonal
weights, not just power-law weights. An order-p-squared skew block can
still admit an energy estimate, so an entrywise order-p criterion must
not be confused with well-posedness.

## Remaining columns and validation

S4D had stopped before selected coordinate e_9. S4E computes complete
16-row source and evolution columns for e_6, e_7 and e_9, keeping
Rdot, F_1dot, pdot=-Hp and W=Vc+Mcdot. In addition to the phase pair:

- Qe_9=f_12 exactly. Its only order-p or faster output is full-graph
  row 11 at order p, coefficient -sqrt(10)/6.
- e_6 drives row 11 at order p with coefficient
  3 sqrt(2)/(110H); e_7 drives row 11 at order p with coefficient
  -sqrt(330)/55.
- The already pinned S4D frame/dust columns e_8,e_11 have no
  faster-than-p output. The seven remaining chart columns have not
  been screened here.

The [attempt-01 summary](../../../Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/summary.json)
has SHA-256 597535a08264a038a225b68ef8f13b62d3e47ba3d83a882d1b8e6a8e615b5c4b;
the [exact detail](../../../Analysis/MasterTests/outputs/r4c1_s4e_attempt_01/detail.json)
has SHA-256 c82d6076df21f9b89b8b2e6fe0d739f1381cc3a8efd974be32431f6376f9b472.
Its 147/147 local source-pin, reconstruction, full-row and exact-limit
checks pass; no failed or unknown checks were reported. The receipt
records 47 source hashes, and its output sidecars match. The
[S4E executable](../../../Analysis/MasterTests/test_01_r4c1_phase_pair_reweight.py)
is SHA-256 cf5d2c96c4f61529b89cdeac84b7243f22c176760a9682d1fcc0089e1dc1bc01.
It imports parent functions without running any prior receipt-producing
entrypoint. These local checks are not independent scientific review or
proof of parent physics closure.

Run only in a fresh, non-colliding attempt directory:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_phase_pair_reweight.py --attempt 2

## Next gate and unchanged holds

The next separately contracted test should assemble **all twelve**
selected-chart columns and the full 16-row graph embedding at the same
B1 event, classify every order-p-squared coupling, and decide whether a
positive non-diagonal full-symbol symmetrizer or controlled dispersive
energy estimate exists. Preserve the actual skew phase pair; do not
preemptively force it to order p. Then address time dependence,
subprincipal terms, finite-time transfer, the physical cutoff and the
homogeneous/singular sectors before a full-IVP claim.

R9-MT1-S4E inherits S4D/S4C/S4B/S4A/S3/S2/S1/B1/VARIATION review
debt. Master Test 1 remains held; Tests 2 and 3 remain incomplete.
MAT-001 remains BLOCKED, UVIR-003 IN_PROGRESS, K_Q=NOT_DERIVED,
V=NOT_COMPUTED, Stage 4A closed. No canonical Derived promotion or
publication-readiness claim follows.
