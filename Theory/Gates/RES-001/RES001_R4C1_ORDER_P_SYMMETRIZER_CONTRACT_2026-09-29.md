# R4C1-S4G: order-p graph-equivalent symmetrizer screen

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
Frozen before S4G implementation and calculation. This is a single
formal initial-event high-frequency gate. `review_status=DEFERRED`,
`Rule9_cleared=false`, `physics_pass=false`, `gate_effect=NONE`.

## Frozen inputs and domain

Pin the S4F contract, executable, report and attempt-01 summary/detail
with SHA-256 sidecars, and verify S4F's transitive S4E/S4D/S4C/S4B/
S4A/S3/S2/S1/B1/variation source chain. Read the exact S4F `C` matrix;
do not execute an earlier receipt-writing main or alter any earlier
artifact. Use the same zero-based twelve-coordinate chart and full
sixteen-row graph, same conditional action, B1 initial event and
`D=diag(p,1,p,1,p,1,1,1,1,1,1,1)` with `p=k/a>=1`, `H>0`,
`pdot=-Hp`. The formal `p->infinity` calculation does not establish
the physical EFT cutoff or validity of arbitrarily short wavelengths.
The graph equivalence `||Dc||^2<=||Qc||^2<=2||Dc||^2` is inherited, not
a physical Hamiltonian.

## Preregistered calculation and decisions

1. Reconstruct every exact `C_2` and `C_1` entry independently from the
   saved rational `C` by direct limits: `C_2=lim C/p^2` and
   `C_1=lim (C-p^2 C_2)/p`. Verify all 144 residuals have degree at
   most zero after subtracting `p^2 C_2+p C_1`. Replay S4F's phase
   pair and order-p symmetric `-1/26` witness. Fail closed on changed
   pins, altered chart, or a degree mismatch.
2. Split into phase subspace `P={6,7}` and its ten-coordinate
   complement `K`. Verify `C_2` is supported only in `P`, is skew,
   and is invertible there. Compute the exact characteristic and minimal
   polynomials of `A=C_1[K,K]`, its zero-eigenspace rank and the
   semisimplicity/imaginary-spectrum conditions. If it has a real
   growing root or defective imaginary/zero branch, record the exact
   obstruction; do not infer a full-system no-go or physical instability.
3. If `A` is semisimple with spectrum contained in the imaginary axis,
   construct an exact real symmetric positive `G` with
   `A^T G+G A=0`. A permitted deterministic construction uses the
   spectral projectors of `A^2` and oscillator energies. Verify
   projector resolution/orthogonality, exact skew identity, and
   positivity from a sum-of-squares identity for all `H>0` where
   denominators are nonzero. A numerical eigenvalue alone is not a
   positivity certificate.
4. Set `M_0=diag(G,I_2)` in K/P order. Check the order-p symmetric
   defect of `M_0 C+C^T M_0`: its K/K block must vanish; inspect P/P
   and K/P exactly. Where algebraically permitted, construct a real
   symmetric off-diagonal `M_1` satisfying
   `M_1 C_2+C_2^T M_1=-(M_0 C_1+C_1^T M_0)`.
   Verify this full 12-by-12 identity exactly, not by selected entries.
   If P/P has an uncancellable trace or another exact obstruction,
   record it rather than forcing a solution.
5. Form `M(p,H)=M_0(H)+M_1(H)/p`. Prove `M` is positive and uniformly
   equivalent to the S4F graph for all sufficiently large p at each
   fixed `H>0` by an explicit spectral-norm/eigenvalue inequality;
   no unproved global H-uniform threshold is allowed. Using the B1
   flow's `Hdot` and `pdot=-Hp`, classify every entry of
   `M C+C^T M+Mdot` exactly. If the remainder is degree at most zero,
   record `B1_FORMAL_BOUNDED_ENERGY_RATE_CANDIDATE`; otherwise record
   the highest exact positive-degree witness. This is only a local
   high-p candidate. It is not a finite-time estimate, all-sector
   stability result, strong-hyperbolicity theorem or EFT approval.

Negative controls: an in-memory bad source hash must fail; omitting
the `M_1` correction must retain at least one order-p symmetric term;
the prior S4F graph-equivalence and phase-pair checks must replay.
An unresolved symbolic calculation or bounded timeout is `INCOMPLETE`,
not a pass or a no-go. Write a new S4G-only exact receipt, detail and
owning report with hashes in a fresh non-overwriting attempt directory.
No canonical gate, MAT/UVIR, Test 2/3 or publication status changes.
