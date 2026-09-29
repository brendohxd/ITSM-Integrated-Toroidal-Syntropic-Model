# R4C1-S4F: complete chart and graph-normalized leading symbol

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
Frozen before S4F implementation or calculation. Review DEFERRED;
Rule9_cleared=false, physics_pass=false, gate_effect=NONE. This is a
formal B1 initial-event principal calculation, not an EFT-valid
all-sector stability or full-IVP claim.

## Fixed sources and domain

Pin the S4E contract, report, executable and attempt-01 summary/detail,
including SHA-256 sidecars; verify their transitive S4D/S4C/S4B/S4A/S3/S2/
S1/B1/variation dependencies through the S4E verifier. Do not execute any
earlier receipt-writing main function. Keep the R4C1 action, B1 initial
data, S2 generator, S4B 16-row graph and S4C 12-row chart unchanged.

At the exact S4C B1 initial event keep H>0 symbolic and use
p=k/a>0 along nonzero torus modes, with pdot=-Hp. The asymptotic
normalization domain is p>=1 (satisfied at a=1 by nonzero torus
k=2*pi*|n|). H=0, p=0 and other singular branches are excluded.
The formal p->infinity limit is not an assertion that modes beyond an
unknown physical cutoff belong to the EFT.

Use the selected full-graph rows
(0,2,3,5,6,8,9,10,11,12,13,15) in this exact order. Retain
R,Rdot,F_1dot and W=Vc+Mcdot in every evolution column.

## Calculation and preregistered decisions

1. Invert the exact finite-mode chart once. Reconstruct all twelve
   canonical unit-coordinate columns. For each, compute every one of
   the 16 full graph source entries Q_i=F_1 Z_i and 16 evolution
   entries L_i=(F_1dot+F_1 A)Z_i. Verify selected(Q)=I, exact original
   graph reconstruction, and all previous S4E e_6/e_7/e_9 source and
   evolution columns without modifying those receipts. Classify every
   rational entry by exact large-p degree/coefficient, including zero.
2. Verify, rather than assume, the proposed full graph metric in this
   chart:

       Q^T Q = diag(1+p^2, 1, 1+p^2, 1, 1+p^2, 1,
                    1, 1, 1, 1, 1, 1+p^-2).

   Reject this candidate if any full-graph row or cross term disagrees.
   With D=diag(p,1,p,1,p,1,1,1,1,1,1,1), prove for p>=1 that
   ||D c||^2 <= ||Q c||^2 <= 2||D c||^2. This is equivalence to the
   S4B reference-unit graph, not a physical Hamiltonian.
3. Form the exact selected-chart generator B from the selected rows
   of L. Form the D-normalized generator
   C=D B D^-1 + Ddot D^-1, with Ddot D^-1 equal to -H at indices
   0,2,4 and zero elsewhere. Classify all 144 entries of C and
   every full-graph output in L. Independently check direct limits
   for each nonzero entry of degree >=2. Preserve exact witnesses.
4. If any C entry grows faster than p^2, record
   HIGHER_ORDER_FULL_SYMBOL_COUPLING with its exact location and
   coefficient. Otherwise assemble the complete 12-by-12 C_2 from
   lim p^-2 C, and check C_2+C_2^T exactly. If zero, record
   FULL_P2_SYMBOL_SKEW_IN_GRAPH_EQUIVALENT_NORM; if nonzero, record
   FULL_P2_SYMBOL_NOT_SKEW_IN_CANDIDATE_NORM with exact symmetric
   witnesses. Neither result alone proves or rejects a different
   non-diagonal positive symmetrizer, a subprincipal energy estimate,
   time-dependent well-posedness or physical stability.
5. Record all order-p or faster couplings and the leading degree of
   the symmetric part of C. A bounded symbolic timeout or unresolved
   exact algebra is INCOMPLETE, not a pass or no-go.

Reject changed pins/sidecars, wrong chart, omitted Rdot/F_1dot/pdot,
missing Mcdot, non-unit selected source coordinates, incomplete
12-column/16-row scans, an incorrect graph metric, an incorrect
Ddot term, or failure to replay S4E. In-memory deliberate bad pin and
wrong-D-weight controls must fail without altering sources. A fresh
S4F attempt directory must refuse overwrite; keep prior receipts intact.

Output a S4F-only JSON receipt, exact matrix/detail artifact and owning
report with hashes, assumptions, results and inherited review debt.
Master Test 1 remains held until its full action/GR/stability requirements
are met; Tests 2 and 3 are not promoted. MAT-001, UVIR-003, K_Q, V,
Stage 4A, canonical claims and publication status are unchanged.
