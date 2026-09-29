# R4C1-S4F: complete B1 graph-normalized leading symbol

Date: 2026-09-29. Master Test 1; conditional R4C1-v1/B1. The
[frozen S4F contract](RES001_R4C1_FULL_SYMBOL_CONTRACT_2026-09-29.md)
precedes the executable and calculation. Review is `DEFERRED`;
`Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.
This is an exact formal calculation at one B1 initial event, not a
physical high-frequency/EFT assertion, a full constrained-IVP estimate,
or canonical action approval.

## Scoped result

All twelve selected-chart source and evolution columns, including all
sixteen output rows, were reconstructed from the pinned S2/S4B/S4C matrices.
The chart rows, in zero-based indexing, are
`(0,2,3,5,6,8,9,10,11,12,13,15)`. The exact source map satisfies
`selected(Q)=I_12`; every source column agrees with the original graph
map, and the three earlier S4E columns replay exactly. The full graph
Gram matrix in this chart is

\[
 Q^TQ=\operatorname{diag}(1+p^2,1,1+p^2,1,1+p^2,1,
                  1,1,1,1,1,1+p^{-2}),\qquad p=k/a\geq1.
\]

For `D=diag(p,1,p,1,p,1,1,1,1,1,1,1)`, exact diagonal comparison gives
`||Dc||^2 <= ||Qc||^2 <= 2||Dc||^2` for every chart vector on that domain.
This is equivalence to the frozen sixteen-row reference graph, **not**
an action-derived physical Hamiltonian.

The normalized chart generator is `C=D B D^-1 + Ddot D^-1`, with
`Ddot D^-1=-H` at indices `0,2,4` and zero elsewhere, using
`pdot=-Hp`. All 144 entries of `C` and all twelve 16-row graph outputs
were classified exactly. No normalized generator entry has degree above
two. The **only** degree-two entries are

\[
 \lim_{p\to\infty}p^{-2}C_{6,7}=\frac{\sqrt{165}}{33},\qquad
 \lim_{p\to\infty}p^{-2}C_{7,6}=-\frac{\sqrt{165}}{33}.
\]

Thus the complete `C_2` is the skew block
`(sqrt(165)/33)(e_6 e_7^T-e_7 e_6^T)` and `C_2+C_2^T=0` exactly. This
extends S4E's *restricted-pair* observation to the complete B1 principal
matrix in a uniformly full-graph-equivalent **candidate** norm. It does
not establish a symmetrizer for the whole generator or an energy bound.

The symmetric part of `C` still has degree **one**. An exact witness is

\[
 \lim_{p\to\infty}p^{-1}
    \frac{C_{2,3}+C_{3,2}}{2}=-\frac1{26}.
\]

Other order-`p` symmetric couplings and the 17 order-`p`-or-faster
generator entries are retained in the exact detail. Therefore the
leading skew cancellation does **not** dispose of the subprincipal
growth, time dependence or fixed-time transfer question. In particular,
do not relabel S4D's order-`p^2` term as either a proven instability or
a completed stability proof.

## Reproducibility and controls

The [attempt-01 summary](../../../Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/summary.json)
has SHA-256 `c1b47d62d1e6da23269867420be774d114b77d3a33e40e95284e327dfce08604`;
the [exact detail](../../../Analysis/MasterTests/outputs/r4c1_s4f_attempt_01/detail.json)
has SHA-256 `6336924b22b91f5c3c91d835c498c81e8e3880227215ab117c8ccac19dcd8273`.
The [executable](../../../Analysis/MasterTests/test_01_r4c1_full_symbol.py)
has SHA-256 `d2a34c1855ef0260e6609ff906fd22ea1a11ec051e820e2bb48af29c25d08546`;
the frozen contract has SHA-256
`5cd9ed377cb640b50ded531e41ef44a81588fa560a835c8e7df6f6d4bb79168d`.
All four SHA-256 sidecars match. The receipt records 52 source hashes,
`208/208` passing local checks, no failed/unknown checks, and
`FULL_P2_SYMBOL_SKEW_IN_GRAPH_EQUIVALENT_NORM`. Its checks cover the
transitive pinned inputs, bad-pin/wrong-weight controls, chart inversion,
full graph reconstruction, S4E replay, `Mcdot`, `Rdot`, `F_1dot`,
`pdot`, graph-norm identities and direct limits for both degree-two
entries. A separate read-only SymPy evaluation of the saved exact `C`
entries recovered both degree-two coefficients, zero phase-pair
degree-two symmetric coefficient, and the `-1/26` order-`p` witness.
Neither local test counts nor hash checks constitute independent review.
Earlier receipts were not rewritten.

For a fresh attempt only, change the attempt number; never overwrite
attempt 01:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_full_symbol.py --attempt 2

## Next gate and unchanged holds

The next single gate should contract the **order-`p` symmetric defect**
in the complete graph-equivalent chart: decide, with exact positivity and
uniform-equivalence tests, whether a permitted non-diagonal correction
can remove it, or whether a different finite-time transfer mechanism is
needed. Inspect the complete `C` and its evolving coefficients, not the
phase pair in isolation. A failure of one candidate correction is not a
general no-go. Full constrained IVP, wider phase cone, quartic
dispersion, homogeneous/singular branches, physical cutoff, GR recovery
and matching remain open.

R9-MT1-S4F inherits S4E/S4D/S4C/S4B/S4A/S3/S2/S1/B1/VARIATION
review debt. Master Test 1 is still held by its action-input and
physical-viability requirements; Tests 2 and 3 are incomplete. MAT-001
remains `BLOCKED`, UVIR-003 `IN_PROGRESS`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, Stage 4A closed. No Derived or publication promotion
follows.
