# R4C1-S4H: moving-background principal and temporal-persistence contract

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
This freezes the next single gate after S4G. Review is deferred, not cleared.
`physics_pass=false` and `gate_effect=NONE` unless a later parent gate
separately establishes its complete requirements.

## Frozen sources and domain

Use the unchanged R4C1 action, B1 homogeneous zero-winding background,
S2 canonical generator, S4B complete sixteen-row graph, S4F twelve-row
chart, and S4G initial-event metric. Verify their saved SHA-256 sidecars and
transitive source pins before calculating. Do not run any earlier
receipt-writing `main()` or replace a prior attempt. The trajectory is the
registered B1 `t in [0,4]`, not a fitted cosmology. Work with nonzero torus
mode `k=2*pi*|n|`, `p=k/a`; for the inherited graph comparison require
`p>=1`. The physical EFT cutoff is **not derived**, so the formal
`p->infinity` result cannot establish physical admissibility of arbitrarily
high modes. Keep the auxiliary constraint, `H=0`, `rho_m=0`, `a=0`, and
other singular branches outside the regular chart visible.

## Ordered calculations and rejection rules

1. Verify the existing exact original and canonical graph minors. For the
   S4F chart, replacing old row 14 by row 15 multiplies the old selected
   minor by `p`. State its nonzero domain explicitly. Do not infer global
   B1 existence or exact interval positivity from 801 numerical samples.
2. Form the **moving** selected graph `T(t,k)` and its derivative, from the
   pinned S4B matrices and fixed-comoving-`k` flow. Reconstruct
   `B=(Fdot+F A)[ROWS,:] T^{-1}` and
   `C=D B D^{-1}+Ddot D^{-1}`, with the S4F `ROWS`,
   `D=diag(p,1,p,1,p,1,1,1,1,1,1,1)`, and `pdot=-Hp`. Check the full
   sixteen-row graph identity and replay S4F/S4G at the initial event.
   Dropping `Fdot`, `Rdot`, `Mcdot`, or `pdot` is a rejection control.
   As an explicitly non-decisive reconstruction diagnostic, use the pinned
   801-point B1 CSV at `t={0,0.5,1,2,3,4}` and axial torus modes
   `n={1,8,64,256}` (`k=2*pi*n`). Compare the `t=0` moving reconstruction
   with saved S4F `C` at relative entrywise tolerance `1e-7` and report
   actual maxima. Sample agreement does not establish exact limits or
   interval validity.
3. Extract all 144 leading `C_2` and `C_1` coefficients by exact limits
   where possible. State any denominator-zero loci. On the regular B1
   trajectory determine whether the order-`p^2` block remains skew and
   the projected order-`p` slow block remains semisimple with imaginary
   spectrum. A concrete admissible counterexample rejects persistence of
   this S4G construction, **not** every possible norm or the physical
   theory. An unresolved symbolic or numerical-only scan is `INCOMPLETE`,
   never a uniform proof.
4. Only if that principal screen succeeds, construct a smooth
   time-dependent positive metric `M(t,p)`, including the necessary
   subprincipal correction, and prove explicit lower/upper graph
   equivalence and a uniform upper energy-rate constant over a declared
   closed time interval and allowed `p` domain. Track `Mdot` through the
   full background flow. This is the requirement for a finite-time
   energy estimate; one-event or finitely sampled positivity cannot pass.
   The estimate still would not certify wider phase cones, constraint
   propagation, all sectors, a physical cutoff, or healthy GR recovery.

Preserve a failed calculation as a new non-overwriting attempt and report
the exact failure, timeout or unknown. Record source hashes, failed and
unknown checks, and direct/inherited Rule-9 debt. A result limited to
steps 1-3 must be labelled `PRINCIPAL_SCREEN_ONLY` or `INCOMPLETE`, with
`full_constrained_IVP=NOT_PROVED`, `physical_EFT_cutoff=NOT_DERIVED`,
`Rule9_cleared=false`, `physics_pass=false`, and `gate_effect=NONE`.
No MAT-001, UVIR-003, Stage 4A, Test 2/3, Derived or publication status
changes follow from this gate.
