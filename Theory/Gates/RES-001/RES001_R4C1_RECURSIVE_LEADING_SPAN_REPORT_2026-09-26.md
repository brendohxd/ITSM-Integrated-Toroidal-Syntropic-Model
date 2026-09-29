# R4C1-S4D: recursive leading-span disposition

Date: 2026-09-26. Master Test 1; conditional R4C1-v1/B1. The
[precalculation contract](RES001_R4C1_RECURSIVE_LEADING_SPAN_CONTRACT_2026-09-26.md)
holds the action, background, S2 generator, S4B graph and S4C chart fixed.
Review `DEFERRED`; `Rule9_cleared=false`; `physics_pass=false`;
`gate_effect=NONE`. This is a formal high-frequency diagnostic, not a
physical EFT-limit calculation.

## Decision

The unweighted S4C selected-chart recursion **does not close as an
order-`p` leading system**. S4C's frame/dust inputs require selected-chart
coordinates 7 and 9 (full-graph rows 10 and 12). The first newly processed
coordinate, `e_7`, is a unit `sqrt(b) delta Delta_psi` graph datum: its
complete source graph has only row 10 equal to 1, with no growing source
norm. Yet its exact full-graph evolution has

\[
 \lim_{p\to+\infty}p^{-2}
 [(F_{1\,dot}+F_1 A)Z_7]_{9}=\frac{\sqrt{165}}{33}>0,
 \qquad p=k/a>0,\ H>0.
\]

Row 9 is `sqrt(K_Q) delta psi_dot` in the registered S4B reference-unit
graph. The rational expression and its denominator are in the
[exact detail artifact](../../../Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/detail.json);
the denominator is `p^2(65340000 H^2+165000 p^2+1170675)>0` on this domain.
Its highest powers give the coefficient above, and a separate direct SymPy
limit agrees. At `H=1`, the illustrative ratios of this row to `p^2` are
`0.3892494457040933` at `p=100` and `0.3892494720779883` at `p=1000`;
these are arithmetic spot checks, not a physical background or fit.

The preregistered stop rule gives `CHART_REWEIGHT_REQUIRED`: a possible
alternative weighting or full-system formulation needs its own declared
domain and estimate. Coordinate 9 was queued but **not processed** after
the order-`p^2` obstruction; the full-graph residual, leading block and
symmetrizer branches were not run. This result rejects only the proposed
unweighted-chart order-`p` recursive closure. It does not prove a general
ill-posedness, unbounded finite-time transfer, physical instability beyond
an EFT cutoff, or impossibility of a different norm/symmetrizer.

## Reproduction and integrity

The first S4D attempt passed 124/124 checks and is preserved. A second
attempt added explicit pending-index recording and a post-discovery
independent limit confirmation; the equations, sources, chart, domain and
decision rule were unchanged. The second attempt passes **125/125 local
symbolic, source-pin and reconstruction checks**. It exactly reproduces
the pinned S4C frame/dust source and evolution columns before processing
`e_7`. The finite-mode chart inverse, `Rdot`, `F_1dot`, `pdot=-Hp`, and
`W=Vc+Mcdot` identities are checked. A separate read-only audit matched
all 42 receipt input hashes and the detail artifact hash, with no mismatch.
An in-memory deliberate bad contract pin was rejected as the sole failed
check; it did not alter any source or receipt.

Run the S4D executable in a fresh, non-colliding attempt directory; its
`--attempt` argument intentionally refuses to overwrite an earlier attempt:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_recursive_leading_span.py --attempt 3

Frozen evidence for this disposition:

- [S4D executable](../../../Analysis/MasterTests/test_01_r4c1_recursive_leading_span.py): SHA-256 `e11b15b7b8cd8d7a1c513fec5fd611b7a83269b409097dfba9a394a0577f32c1`.
- [Attempt-02 summary](../../../Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/summary.json): SHA-256 `319ce57136468f51eb4040c4362d12efa0da08106dc68ed3e5a0c1d354b60097`.
- [Attempt-02 exact detail](../../../Analysis/MasterTests/outputs/r4c1_s4d_attempt_02/detail.json): SHA-256 `719d011083ae8c7f5a80b00c210d58e138aa49b07dbbbf3b1cc666c954f2e9f0`.
- [S4D contract](RES001_R4C1_RECURSIVE_LEADING_SPAN_CONTRACT_2026-09-26.md): SHA-256 `3cd2ad808053862ca1d947bae4ae0d69b46e8fdae415706b3f332cf3867aede1`.

`R9-MT1-S4D` inherits S4C/S4B/S4A/S3/S2/S1/B1/VARIATION review debt.
Its local negative result may guide the next separately contracted
principal/weighted-space diagnostic, but its independent review remains
deferred. Full constrained IVP, homogeneous/singular sectors, causality,
EFT cutoff, healthy GR recovery, physical coefficient matching and
canonical action acceptance remain substantive holds. Master Test 1 and
MAT-001 remain held; UVIR-003 remains in progress; `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, Stage 4A closed. No downstream Derived promotion or
publication readiness follows.
