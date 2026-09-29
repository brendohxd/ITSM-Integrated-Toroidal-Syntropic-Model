# R4C1-S4C: frame/dust leading-coupling disposition

Date: 2026-09-26. Master Test 1; conditional R4C1-v1/B1.
Validation: 117/117 exact, provenance and rejection checks, twice with
byte-identical JSON artifacts in `itsm_env`. Review `DEFERRED`;
`Rule9_cleared=false`; `physics_pass=false`; `gate_effect=NONE`.
Owning [frozen contract](RES001_R4C1_FRAME_DUST_PRINCIPAL_CONTRACT_2026-09-26.md).

## Decision

The high-frequency frame/dust pair singled out by S4B is **not a closed
two-variable leading subsystem** of the full constrained scalar evolution.
At the regular B1 initial event, a unit frame-kinetic graph coordinate
generates three order-`p` outputs:

| Full S4B graph row | Quantity | Exact coefficient of `p` |
|---:|---|---:|
| 10 | `sqrt(b) delta Delta_psi` | `sqrt(330)/55` |
| 12 | `sqrt(M_U^2 c_L) p w` | `sqrt(10)/5` |
| 15 | added dust-gradient row `p v_d` | `sqrt(6)` |

Rows 10 and 12 lie outside the putative frame/dust pair (rows 11 and 15).
The exact dust-gradient input has no order-`p` output; neither column has a
term faster than `p`. The S4B witness limit
`r_1(p)/p -> sqrt(6)/2` is recovered exactly from the two columns together.
The isolated 2-by-2 cross-term-symmetrizer branch was therefore **not run**:
symmetrizing that truncated pair would omit physical leading couplings.

This is a negative result only for the proposed *two-variable leading
closure* at this registered B1 event. It does not establish that the full
system lacks a symmetrizer, a finite-time bound, or a controlled domain.
It also does not prove ill-posedness or physical high-frequency instability
beyond a cutoff.

## Exact construction and checks

The [S4B full graph](RES001_R4C1_MIXED_REGULARITY_REPORT_2026-09-26.md)
has 16 rows on twelve canonical scalar initial-data components. Select the
original-chart rows `(0,2,3,5,6,8,9,10,11,12,13,15)` as a coordinate map
`T_q`. The final row is precisely `p` times S4A's old selected dust row.
At the B1 initial coefficients, keeping its positive Friedmann `H` symbolic,

\[
 \det T_q=-\frac{\sqrt{66}\,p^5}{15840}
              (79200H^2+200p^2+1419)\ne0,
 \qquad p>0,\ H>0.
\]

This proves a regular finite-mode chart there; `T_q` is **not** substituted
for the S4B graph norm. Construct original-chart data `y_f,y_d` with
`T_q y_f=e_8`, `T_q y_d=e_{11}`. The full 16-row source graph vectors are
exactly `g_f=e_{11}` and `g_d=e_{15}+e_{14}/p`. The density-velocity
reconstruction denominator is
`(79200H^2+200p^2+1419)/240>0`. The script checks both density constraints,
the complete source graph data and canonical reconstruction using `R,Rdot`.

For each source direction, the script evaluates all 16 entries of
`(F_1dot+F_1 A)Z`, with `A=[[0,I],[-W,-G]]` and corrected
`W=Vc+Mcdot`. It cancels the exact rational functions of `p` and records
their leading degrees and coefficients, not a fitted large-mode slope.
It checks `pdot=-Hp`, the inherited determinant, S4B witness norm and
limit, source hashes and sidecars. Deliberately dropping `Rdot` from the
dust reconstruction is detected. The exact `F_1dot` and `Mcdot` identities
remain binding.

## Reproduction and next bounded step

Run:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_frame_dust_principal.py

The [summary receipt](../../../Analysis/MasterTests/outputs/test_01_r4c1_frame_dust_principal_summary.json)
has SHA-256 `ddccc444ac7e9191a1d19d6e61aaf009932e6394b700dcfe29af4d0bb361107b`.
Its [exact detail artifact](../../../Analysis/MasterTests/outputs/test_01_r4c1_frame_dust_principal_detail.json)
has SHA-256 `b4cd27382b516c7fec994c926829db60cc3c1bc295abd4074324c7a7c6ec24bc`.
The executable SHA-256 is
`8732ca4b991a60ce99eb32cf5de85a147435ae075f07dbf8495f661c22af6f82`.
Earlier S4A/S4B and S2 receipts were not rewritten.

The next separately frozen calculation should recursively close the
leading-mode span beginning with rows 11 and 15 and now including rows 10
and 12, checking whether further full-system rows enter. Only after a
closed leading subspace is identified should one test a positive
symmetrizer, with the complete graph norm and time-dependent/subprincipal
terms retained for any full estimate. An ordinary Euclidean norm on this
minor chart is not automatically equivalent to the S4B graph norm.

R9-MT1-S4C inherits S4B/S4A/S3/S2/S1/B1/VARIATION; its review is deferred.
The full constrained IVP, singular/homogeneous branches, other spin sectors,
causality, cutoff, GR recovery and physical matching remain open. Master
Test 1 and MAT-001 remain held; UVIR-003 is in progress;
`K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, Stage 4A closed. No canonical or
publication promotion follows.
