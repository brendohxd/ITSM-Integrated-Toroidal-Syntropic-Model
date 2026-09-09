# G-A4 / A-B3 Role-C adjudication

**Date:** 2026-09-05  
**Branch:** `recovery/v12-core-architecture`  
**Role:** Codex Role C — claim hygiene, provenance and gate reconciliation  
**Status:** `ADJUDICATED_WITH_HOLDS_AND_FOLLOWUP_REQUIRED`  
**Gate effect:** none  
**Commit/push/publication:** not performed

## 1. Decision

Neither external package is accepted verbatim and neither changes a gate.

- Grok `G-A4` establishes a bounded scalar result: a pure repulsive sextic
  complex parent has a healthy finite-charge fixed-background branch whose
  leading algebraic phase EFT is proportional to
  `(X_R-m^2)^(3/2)`. This is a timelike phase-EFT operator-shape result, not a
  derivation of the spatial `Y^(3/2)` force sector, screening, `K_Q`, `V` or
  `a_0`.
- Antigravity `A-B3` reproduces the frozen 30-check script and several useful
  independent controls, but the canonical checker contains literal,
  single-point and incomplete-proxy tests. Some requested mutations test the
  assertion machinery rather than the scientific expression. Its strongest
  completion label is therefore rejected.
- The next packages are refinement and verifier-repair tasks. They are not
  permission to begin the coupled amplitude-phase-metric calculation.

The binding boundary remains:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V=C_m/sqrt(K_Q) NOT_COMPUTED`;
- downstream screening, lensing, disk and cosmology claims remain unavailable.

## 2. Sealed intake and provenance

Raw external responses remain in private local model/session stores. Only
claim-level findings and hashes are recorded here.

| Item | SHA-256 | Disposition |
|---|---|---|
| Sealed Grok `G-A4` handoff | `86d25b4b842f57b30f60b753d686cc5c0f0ccbf2bb8d6b666c149aae04800233` | Manifest match |
| Exact Grok report body | `7b51aa29976bad92006e6fbf8ec51498f07799969833f8a226f56bd62deddfaf` | Reviewed |
| Exact Grok final assistant content | `dd1e924db201c8141c44e1fc10b9c3afc4ff0423d10441fe549fbe8e6891e73c4` | Reviewed |
| Sealed Antigravity `A-B3` handoff | `8b1902eb040678f866479357d13321aaad8d05cfa644a0e0fa1d6a7b9421bc96` | Manifest match |
| Antigravity temporary audit script | `295449b842064401e5377239039025abe6ac2e583394baffa7674c3b14eb9570` | Reviewed as temporary code |
| Antigravity raw audit JSON | `b451b8db96994efec2ec14ffd3d3b904d5b9bd3ef9611b88c2dcc8861462af39` | Reviewed with precision limitation |
| Exact Antigravity final assistant content | `e18c8ddde2636a66d346aed4bb8145bf5c7b1ae6cce730ee1e631c3ef97d22ce` | Reviewed |

Hash equality establishes artifact identity only. It is not scientific
validation or reviewer independence.

## 3. Claim-by-claim reconciliation

| Claim or equation | Grok Role A | Antigravity Role B | Codex check | Disposition |
|---|---|---|---|---|
| `mu^2=m^2+kappa_3 s_0^2` | Derived | Root controls consistent | Direct background variation agrees | Confirmed on the declared positive-density branch |
| `M_sigma^2=kappa_3 rho_0^4=4(mu^2-m^2)` | Derived | Numerical roots consistent | Direct quadratic expansion agrees | Confirmed fixed-background scalar identity |
| Exact mixed-mode dispersion | Derived | Five-point root comparison | Characteristic sum/product and limits agree | Confirmed for the two-field scalar kernel |
| Positive scalar Hamiltonian for `kappa_3>0` | Derived | Sampled stable points | Completion of squares agrees | Confirmed only on the fixed background |
| `P(X_R)=2(X_R-m^2)^(3/2)/(3 sqrt(kappa_3))` | Derived | Monomial identity reproduced | Direct algebraic elimination agrees | Confirmed leading-derivative real-branch result |
| The same result derives static `Y^(3/2)` or MOND | Explicitly rejected | Not established | Static reality domain excludes the required uncontrolled continuation | Contradicted |
| Pure sextic is a closed natural EFT | Not claimed; quartic warning | Not tested | `s^2` is symmetry-allowed and relevant relative to `s^3` | Open; requires explicit Wilsonian hierarchy audit |
| Conformal matter normalization is fixed | Rejected | Not tested | `alpha_1 rho_0` remains free | Contradicted |
| Minkowski is an on-shell finite-charge background | Rejected | Enthalpy check agrees | `epsilon+p=mu^2 rho_0^2` cannot be cancelled by one cosmological constant | Contradicted |
| Canonical 30/30 means Tier-1 closure | Not in scope | Strong label proposed | Several checks are literals or incomplete proxies | Contradicted |
| A-B3 low-`k` convergence is sealed in its JSON | Not in scope | Final prose reports exact follow-up | JSON contains float64 cancellation at the smallest `k`; exact follow-up is outside its cited JSON hash | Provenance discrepancy |

## 4. Accepted bounded S6 result

For

\[
S_{\rm S6}=\int d^4x\sqrt{-g}\left[
-|\partial\Phi|^2-m^2s-\frac{\kappa_3}{3}s^3
\right],\qquad s=|\Phi|^2=\frac{\rho^2}{2},
\]

the repulsive finite-charge branch satisfies

\[
\mu^2=m^2+\kappa_3s_0^2,
\qquad \kappa_3>0,
\qquad \mu^2>m^2.
\]

The quadratic scalar reduction gives

\[
M_\sigma^2=4(\mu^2-m^2),
\qquad
c_s^2=\frac{\mu^2-m^2}{2\mu^2-m^2}.
\]

After explicitly dropping radial gradients, the positive algebraic branch is

\[
s_*(X_R)=\sqrt{\frac{X_R-m^2}{\kappa_3}},
\]

and hence

\[
P(X_R)=\frac{2}{3\sqrt{\kappa_3}}(X_R-m^2)^{3/2}.
\]

This is classified as:

`S6_OPERATOR_SHAPE_SURVIVES_BOUNDED_SCALAR_AUDIT`.

It is not a canonical action freeze because the thermodynamic ensemble,
lower-order operator hierarchy, cutoff domain, gravitating background and
matter interface are not closed.

## 5. Mandatory corrections to G-A4

1. Select and propagate one ensemble. A fixed-chemical-potential calculation
   uses a grand-potential/Routhian description; a fixed-charge calculation
   requires the corresponding Legendre transform and constraint on the
   homogeneous mode. Saying either can be held fixed is insufficient for an
   action freeze.
2. The estimate `delta lambda_4 ~ kappa_3 Lambda_UV^2/(16 pi^2)` is schematic.
   A follow-up must identify the diagram, regulator, counterterm convention and
   any combinatorial coefficient, or label only the power counting.
3. The suspected `P_X`/`P_XX` notation error in the 2026 review must remain a
   comparator hold until checked against its source/PDF conventions.
4. The branch point `X_R=m^2` is simultaneously where `M_sigma` closes and the
   radial-gradient expansion fails. It cannot be advertised as controlled IR
   nonanalyticity without a quantified separation of scales.
5. External agreement is literature precedent, not ITSM evidence.

## 6. Mandatory corrections to A-B3

The result is classified as

`REPRODUCTION_WITH_BOUNDED_CHECK_OR_HARNESS_DISCREPANCIES`.

The following must be repaired before the checker can support a stronger
statement:

1. Parse the trace-sign convention from the frozen ledger instead of comparing
   two in-code literals.
2. Propagate mass dimensions through expressions instead of testing literal
   integer arithmetic.
3. Replace single numerical stability samples with symbolic sign/domain
   statements plus declared boundary samples.
4. Compare the analytic dispersion with a separately constructed first-order
   Hamiltonian evolution matrix, not roots of the same characteristic
   polynomial.
5. Use arbitrary precision for the declared low-`k` sequence in the first
   sealed run. The current JSON suffers catastrophic cancellation for the
   smallest values.
6. Mutate scientific expressions, not expected booleans.
7. Create an actual extra run-2 artifact and compare complete output trees in
   both directions.
8. Include every follow-up result and the final report in one manifest before
   calculating the reported output hash.
9. Use `predeclared in the sealed prompt` rather than `preregistered` for the
   fixed grid unless a genuinely prior public or immutable registration exists.

## 7. Canonical dependency and contamination audit begun by Role C

A bounded live-tree search found the following relevant classes.

| Location class | Finding | Action |
|---|---|---|
| `active_research.md` | Already states that a sextic/three-body parent is only a plausible route and that matching and normalization are not derived | Preserve |
| Current MAT/UVIR gate documents | Continue to state `K_Q NOT_DERIVED` and `V NOT_COMPUTED` | Preserve |
| `Theory/Gates/TOP-001/TOP-001_GATE_SPEC.md` | Rejects deriving `a_0=cH_0/(2*pi)` from topology alone | Preserve |
| Historical and alpha.13-era manuscripts | Contain strong `a_0`, topology, screening and phenomenology claims inconsistent with the current gate boundary | Do not use as authority; publication firewall remains active |
| Downstream papers and supplementary material | Some still use `a_0=cH_0/(2*pi)` as if fixed | Audit only if selected for publication; do not let S6 inherit those claims |

The exact dependency firewall for the new S6 route is:

```text
pure sextic parent
  -> bounded timelike phase-EFT 3/2 shape
  -/> spatial Y^(3/2) force operator
  -/> nonlinear screening law
  -/> K_Q or V
  -/> a_0 or its coefficient
  -/> PPN, lensing, SPARC or cosmology
```

## 8. Next sealed packages

- Grok `G-A5`: compare fixed-`mu` and fixed-charge ensembles, add the
  symmetry-allowed quartic, quantify the sextic-dominance and derivative
  domains, and decide whether an S6 or mixed-potential action class is ready
  for a later metric calculation.
- Antigravity `A-B4`: construct a temporary version-2 verifier with semantic
  checks, arbitrary-precision convergence, independent Hamiltonian roots,
  real file-tree mutations and a complete sealed evidence manifest.
- Codex Role C: independently maintain the dependency firewall, verify both
  returned packages against their sealed prompts, and decide whether the
  candidate advances to an action freeze, remains conditional, or is killed.

Neither package authorizes Ultra work or a gate edit.

