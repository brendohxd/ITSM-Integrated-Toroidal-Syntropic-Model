# R4C1-S4G: conditional B1 order-p symmetrizer screen

Date: 2026-09-29. Master Test 1; conditional R4C1-v1/B1. The
[frozen S4G contract](RES001_R4C1_ORDER_P_SYMMETRIZER_CONTRACT_2026-09-29.md)
pins S4F and its transitive sources. `review_status=DEFERRED`,
`Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.

## Narrow result

At the registered B1 **initial event** and for each fixed `H>0`, there
is an explicit positive graph-equivalent metric for the saved normalized
scalar generator whose **instantaneous formal high-p energy-rate matrix
is bounded as p tends to infinity**. The local receipt status is
`B1_FORMAL_BOUNDED_ENERGY_RATE_CANDIDATE`. This removes the S4F
order-`p` symmetric defect in the stated candidate norm. It is **not** a
finite-time constrained-IVP estimate, a claim that the physical EFT
contains arbitrarily high torus modes, a complete stability result, or
canonical acceptance of the action.

The exact S4F generator is decomposed entrywise as

\[
 C(p,H)=p^2 C_2+p C_1+R(p,H),\qquad R=O(1),\qquad p=k/a\geq1.
\]

All 144 coefficients were obtained by direct limits of the saved rational
matrix. `C_2` is supported only on the phase pair `P={6,7}` and is the
skew block `(sqrt(165)/33)[[0,1],[-1,0]]`. The order-`p` slow block
`A=C_1[K,K]`, with `K={0,...,11}\P`, has characteristic polynomial

\[
 \chi_A(\lambda)=\frac{\lambda^2(\lambda^2+1)^2
 (3\lambda^2+1)(13\lambda^2+14)}{39},
\]

and exact minimal polynomial

\[
 m_A(\lambda)=\frac{\lambda(\lambda^2+1)
 (3\lambda^2+1)(13\lambda^2+14)}{39}.
\]

The zero eigenspace has dimension two, equal to its algebraic
multiplicity. The projected order-`p` block is therefore semisimple
with frequencies squared `1`, `1/3`, and `14/13`, plus its two
zero directions. This is a property of the frozen B1 symbol, not of
the time-dependent physical system.

Let `P_0,P_1,P_{1/3},P_{14/13}` be the exact polynomial projectors
of `A^2` onto eigenvalues `0,-1,-1/3,-14/13`. Their saved matrices
resolve the identity, are idempotent and mutually annihilating, and
`A P_0=0`. Define

\[
 G=P_0^T P_0+\sum_{\omega^2\in\{1,1/3,14/13\}}
 \left(P_{\omega^2}^T P_{\omega^2}
 +\frac{(A P_{\omega^2})^T(A P_{\omega^2})}{\omega^2}\right).
\]

The exact check gives `A^T G+G A=0`. This is a positive metric for
all stated `H>0`: each term is a nonnegative square, and
`sum P_j=I` implies by Cauchy-Schwarz that `G>=I/4`. Positivity is
thus algebraic, not inferred from a numerical eigenvalue. The
displayed denominators in `G` and the correction below are constants
times powers of `H`; no additional positive-`H` pole appeared.

Embed `G` on K and the Euclidean identity on P to obtain `M_0`.
Its order-`p^2` energy contribution vanishes. The K/K and P/P
blocks of `S_1=M_0 C_1+C_1^T M_0` vanish exactly. With
`J=C_2[P,P]`, set the K/P block of symmetric `M_1` to
`-S_1[K,P]J^{-1}` and its P/K block to the transpose, with zero
diagonal blocks. Direct full-matrix verification gives

\[
 M_0 C_2+C_2^T M_0=0,\qquad
 M_0 C_1+C_1^T M_0+M_1 C_2+C_2^T M_1=0.
\]

Omitting `M_1` leaves a nonzero order-`p` defect, as the in-memory
negative control confirms. For `M=M_0+M_1/p`, the exact inequality

\[
 p\geq\max\{1,\;8\|M_1(H)\|_F\}
 \quad\Longrightarrow\quad M\succeq I/8
\]

follows from `M_0>=I/4` and the Frobenius-norm perturbation bound.
At each fixed `H>0`, the upper norm of `M` is finite. Thus this
metric is uniformly equivalent, for sufficiently large p, to the
S4F `D` norm and hence to the frozen full graph; no global H-uniform
threshold or physically permitted wave-number range has been proved.

The B1 flow gives `Hdot=-553/880` and `pdot=-Hp`. Including both in
`Mdot`, all 144 entries of

\[
 \mathcal E=M C+C^T M+\dot M
\]

have exact large-p degree at most zero. A separate read-only parse
of the saved matrices found zero `p^2` and `p` cancellation residuals,
zero nonsymmetric entries of `\mathcal E`, and maximum rational
p-degree zero across its 144 entries. A numerical positive eigenvalue
check at `H=1` was used only as a diagnostic; the all-`H>0` lower
bound comes from the projector identity above.

## Provenance and failed-attempt boundary

The first S4G run computed the same exact detail but stopped while
serializing its summary: a SymPy integer in an audit value was not
native JSON. Its [attempt-01 detail](../../../Analysis/MasterTests/outputs/r4c1_s4g_attempt_01/detail.json)
(SHA-256 `a778e9d25e5cc4c9b9789aa55f2b2ed30242c3e213da89d6510eefc7c07b037c`)
is preserved as **incomplete**, not a validated receipt. The script's
JSON boundary was corrected without changing the equations, and a
fresh attempt 02 was used. Its
[summary](../../../Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/summary.json)
has SHA-256 `37530650e1f75ea22caef79b0ead1621b9866e595f89a055572a447f162d174f`;
its [exact detail](../../../Analysis/MasterTests/outputs/r4c1_s4g_attempt_02/detail.json)
has SHA-256 `a778e9d25e5cc4c9b9789aa55f2b2ed30242c3e213da89d6510eefc7c07b037c`.
The [executable](../../../Analysis/MasterTests/test_01_r4c1_order_p_symmetrizer.py)
is SHA-256 `1e5d7c517ef1249119ed9de0bc7a94b363dcf22b0e8482ff7fe6b57ea7ae54c3`;
the contract is SHA-256
`74ec49a2e51ff3f27fcfb960b0f6ce7d04ba33d5a82b2122677a67438bbdbb80`.
All listed sidecars match. The attempt-02 receipt has 194/194 local
checks, zero failed/unknown, and 57 pinned source hashes; a separate
read-only file-hash pass found zero mismatches. Neither checks nor
hashes amount to independent scientific review.

For any future replay, use only a fresh non-colliding attempt number:

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_order_p_symmetrizer.py --attempt 3

## Next gate and unchanged holds

The next single gate is **temporal persistence**: construct the analogous
symbol and smooth metric along the registered finite B1 trajectory,
verify uniform positivity and energy constants over an explicit time
interval and allowed p-domain, and keep the auxiliary-constraint and
singular-branch conditions visible. An initial-event bound alone cannot
be integrated into a finite-time transfer bound. A formal large-p
threshold above an unknown physical cutoff would also not establish
physical viability. Even success there would not close the wider phase
cone, quartic dispersion, all-sector causality, GR recovery or the
canonical Test-1 action input.

R9-MT1-S4G inherits S4F/S4E/S4D/S4C/S4B/S4A/S3/S2/S1/B1/VARIATION
review debt. Master Test 1 remains held; Tests 2 and 3 are incomplete.
MAT-001 remains `BLOCKED`, UVIR-003 `IN_PROGRESS`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, Stage 4A closed. No Derived or publication promotion
follows.
