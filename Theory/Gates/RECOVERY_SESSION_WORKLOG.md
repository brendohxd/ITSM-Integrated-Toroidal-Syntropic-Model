# Recovery branch session worklog

Append-only log of tactical decisions during autonomous work sessions on the
v12 core recovery program: routes tried, routes abandoned or overwritten, and
why. Purpose: nothing gets silently dropped or replaced without a record the
user can review later. Every entry stays even if a later entry supersedes it —
do not delete or rewrite past entries; add a new one that references the old.

Format per entry: date, gate, what changed, why, what (if anything) was
abandoned or superseded.

---

## 2026-07-24 — UVIR-003 causality addendum opened

Gate: UVIR-003 (Stage A)

Started a causality check on the Stage-A regulated force dispersion relation
in response to the user's request to build on the recovery branch using the
historical archive as a source of routes, specifically following up on the
archive's flagged `c_s^2~1.11` superluminality concern. Produced:
`Theory/Gates/UVIR-003/UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md`,
`Analysis/UVIR/UVIR-003/uvir003_causality_check.py`, one new row in
`Theory/Core/ITSM_Claim_Migration_Ledger.csv`.

Finding: dispersion is superluminal both at long wavelength (`k->0`, if
background gradient `q` exceeds `K_Q/(3A(1+cos^2 theta))`) and at short
wavelength (`k->infinity`, unbounded, for every positive `K_Q,A,gamma`).
Nothing abandoned — this is new work, not a revision.

## 2026-07-24 — Correction: long-wavelength check is not closeable "once K_Q is fixed"

Gate: UVIR-003 (Stage A causality addendum)

**What changed:** the addendum's original Section 1 and its recommendation
said the long-wavelength superluminality question "does not require the
Stage B strong-coupling calculation to resolve" and was "closeable now, in
principle, once K_Q is fixed relative to A" — implying fixing K_Q was a free
normalization choice. Checked this against `Theory/Core/ITSM_Core_Architecture.md`
Section 3.4/4/5 directly rather than trusting the earlier framing.

**Why it changed:** Core Architecture normalizes the force scalar via
`Y = h^{mu nu} nabla_mu psi nabla_nu psi / a0^2` and gives
`L_IR = -(2 C_IR/3) M_P^2 a0^2 Y^(3/2)`, which fixes `A = C_IR/(12 pi G a0)`
in Stage A's unnormalized convention (verified this reduces to the Stage-A
`A` exactly, using `M_P^2=1/(8 pi G)`). `C_IR` at least has a tentative
candidate value (the `2/3` geometric-projection matching hypothesis, itself
only Conditional per the ledger). But `K_Q` — the coefficient of the `Q^2`
term, `Q=U^mu nabla_mu psi` — appears **nowhere else** in the architecture:
not in the static weak-field Lagrangian (Section 5, which drops time
derivatives entirely), not in any matching relation, not even as a
tentative guess. A field redefinition `psi -> psi/sqrt(K_Q)` can always
absorb `K_Q`'s literal numerical value into redefinitions of `A`, `gamma`,
and the background `q` — so "fixing K_Q" in isolation is not a meaningful,
free choice; what actually needs deriving is the physical, redefinition-
invariant combination `3Aq(1+cos^2 theta)/K_Q` in psi's true physical
normalization, and that requires an independent matching condition for
`K_Q` that presently does not exist anywhere in the theory (most likely
this has to come from the same UV-completion / matter-coupling work that
MAT-001 is supposed to do for `C_IR`, `C_m` — MAT-001 is itself blocked on
UVIR-003).

**What this supersedes:** the claim in
`UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md` that the long-wavelength check
"does not wait on a strong-coupling calculation" and is closeable "once K_Q
is fixed relative to A" is corrected below (Section 1 rewritten in place,
with this worklog entry as the record of the original, weaker claim and why
it was wrong). The two-regime structure of the finding (long-wavelength vs
short-wavelength) is NOT abandoned — it still stands and is still correct;
only the claim about how easily the long-wavelength half closes is revised.
Ledger row for this claim also updated to match.

## 2026-07-24 — Aether-sector mode speeds via literature substitution (Stage B, frame only)

Gate: UVIR-003 (Stage B, frame/aether sector only — force sector not touched)

Fetched the Eling-Jacobson-Mattingly Einstein-aether review (arXiv:gr-qc/0410001,
already cited in `UVIR-003_STAGE_A_REPORT.md` Section 1.3) to get literature-
verified coupled metric+aether mode speeds (spin-0/1/2), rather than trust
memory of the formulas — the Stage-A report itself warns sign/normalization
conventions differ across papers. Confirmed via an explicit sympy check
(`Analysis/UVIR/UVIR-003/uvir003_frame_sector_speeds.py`) that Stage-A's
`c1,c2,c3,c4` map identically (no relabeling) to EJM's, because the frame
action's declared extra minus sign on the `c4` term exactly cancels the sign
flip induced by the signature difference (mostly-minus vs mostly-plus).

**Bug caught before trusting the result:** the first version of the
consistency check (verifying EJM's exact formulas reduce to Stage-A's
decoupled `c1/c14`, `c123/c14` ratios in the weak-metric-coupling limit)
scaled only `c1,c3 -> eps*c1,eps*c3` while leaving `c2,c4` at O(1). This
failed the assertion (correctly — the script raised rather than silently
passing). EJM's text specifies the reduction holds "for c_i small compared
to unity" — i.e. all four `c_i` scaled together. Fixed by scaling
`c1,c2,c3,c4 -> eps*(...)` uniformly; the corrected limit passes and matches
Stage A's decoupled speeds exactly. Nothing about the underlying physics
claim was wrong — the bug was in how the limit was taken to check it. Logged
here per the instruction to record tactic changes, even ones this small,
so a later reviewer doesn't have to guess whether the first failing run
indicated a real problem with the substitution itself.

## 2026-07-24 — Force-sector longitudinal IR NDA estimate

Gate: UVIR-003 (Stage B item 9, partial)

Estimated one NDA derivative scale for the force sector's nonanalytic cubic
operator, following the method precedent already set by
`UVIR-001_GATE_REPORT.md` Section 7 (canonical-normalize, read the scale off
the cubic vertex). Initially considered doing this fully — all three spatial
directions plus the k^4-dominated regime above `k_cross` — but the
anisotropic Hessian (diag(6Aq,3Aq,3Aq)) makes a fully rigorous coordinate
rescaling delicate (the volume element and field normalization mix under an
anisotropic spatial rescaling in a way that isn't a quick generalization of
UVIR-001's single-scalar-invariant case), and the k^4-dominated regime has
different (Lifshitz, z=2) scaling entirely.

**Decision:** scoped down to the longitudinal direction only (largest
quadratic coefficient, most conservative choice) and the k^2-dominated
regime below `k_cross`, explicitly excluding the transverse directions and
the Lifshitz regime rather than force an estimate that would silently paper
over those complications. Result:
`Lambda_NDA,long^(IR) ~ K_Q^(3/4)/sqrt(A)`
(`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_STRONG_COUPLING.md`). This is a
time-normalized longitudinal derivative scale, not a completed physical EFT
cutoff. It is blocked numerically on the same missing `K_Q` matching condition
as the causality addendum's long-wavelength check; transverse normalization,
Lifshitz power counting, and the physical cutoff remain open.

## 2026-07-24 — Conditional K_Q estimate (speculative, escalates priority)

Gate: UVIR-003 (causality addendum, extension)

While looking for any existing handle on `K_Q` (which the causality addendum
found has no matching condition anywhere), found that
`UVIR-002_ROUTE_SELECTION.md` declares the temporal invariant as
`Q=U^mu nabla_mu psi/a0` (a0-normalized, same pattern as Core Architecture's
`Y` normalization). Constructed a candidate matching hypothesis by direct
analogy to how `A=C_IR/(12 pi G a0)` was fixed (same `M_P^2*a0^2`
dimensional-necessity prefactor), giving `K_Q ~ k_Q * M_P^2`. This is
explicitly NOT a derivation — no document states or implies this prefactor
choice for the temporal sector — but is a defensible dimensional analogy
given `M_P` and `a0` are the only scales the architecture declares.

Substituting `k_Q~1` (unjustified NDA guess) and `C_IR~2/3` (already only
Conditional per the ledger) gives `q_cross ~ 0.375-0.75 * a0` — i.e. the
long-wavelength causality threshold would sit *below* `a0`, inside rather
than outside the theory's core physical regime. Verified symbolically and
numerically (`uvir003_conditional_kq_estimate.py`).

**Explicitly not claiming this is a finding about the theory** — three
unconfirmed premises are stacked. Logging this prominently because it
changes the practical priority of the open `K_Q` item: it is not safely
deferrable bookkeeping, since the naive expected values land at or past the
causality edge rather than comfortably away from it. If a future pass
derives `K_Q` properly and finds `q_cross >> a0`, this speculative estimate
should be marked superseded here, not deleted — record why the naive
estimate was wrong once the real answer exists.

## 2026-07-26 - Zero-gradient force block and K_Q identifiability

Gate: UVIR-003 (Stage B, force sector on the declared constant background)

**What changed:** expanded the force action in a generic first-order metric and
frame perturbation with `psi_bar=constant`. Added
`Analysis/UVIR/UVIR-003/uvir003_zero_gradient_force_block.py`, its JSON output,
and `UVIR-003_STAGE_B_ZERO_GRADIENT_FORCE_BLOCK.md`.

**Finding:** every derivative of `psi` begins at first order. The temporal
`Q^2` term and projected regulator therefore contain no lapse, shift, frame or
condensate variable at quadratic order, while `Y^(3/2)` begins at cubic order.
The force block factorizes and contains one nonnegative `z=2` scalar for
positive `K_Q` and `gamma`. This is a partial force-block pass, not the missing
metric-aether-condensate reduction.

**K_Q result:** a constant field rescaling changes `K_Q`, `A`, `gamma` and
`C_m` while preserving the physical coefficient ratios. A standalone `K_Q`
is therefore not identifiable from the bottom-up EFT. The earlier
`K_Q~M_P^2` estimate remains speculative and is not promoted.

**Dependency correction:** UVIR-003 should derive a stable and causal domain
in field-redefinition invariant ratios. MAT-001 or a parent microscopic
completion must fix the physical field normalization and select a point in
that domain. This avoids requiring MAT-001's matching result as an input to
the structural part of UVIR-003 while MAT-001 remains downstream.

**Still open:** the reduced metric-aether-condensate scalar/vector/tensor
Hamiltonians, nonzero-gradient force mixing, covariant regulator, physical
cutoff and technical naturalness. Nothing was abandoned except the attempt to
derive a standalone numerical `K_Q` from an EFT in which it is not identifiable.

## 2026-07-26 - Scalar ADM readiness audit

Gate: UVIR-003 (Stage B prerequisite for the metric-aether-condensate block)

**Attempted next step:** begin the scalar ADM reduction around the Stage-A
background `g=eta`, `Phi=rho0 exp(i mu t)/sqrt(2)`, constant `U` and constant
`psi_bar`.

**Readiness finding:** the finite-density condensate has
`rho_Phi+p_Phi=mu^2*rho0^2>0`. A constant vacuum-energy subtraction shifts
energy density and pressure oppositely and cannot cancel this enthalpy.
Therefore the declared Minkowski background is not an exact solution of the
declared coupled Einstein equations.

**Constraint consequence:** any reservoir or driver that supports exact
Minkowski must carry `rho_R+p_R=-mu^2*rho0^2`, so it is not a cosmological
constant. Its scalar perturbations generally enter the lapse and shift
constraints. Eliminating those constraints without declaring the support
sector would produce an off-shell, completion-dependent kinetic matrix.

**Frame correction:** EJM factor the aether operators with `M_P^2/2`, while
Stage A uses `M_U^2/2`. The exact published speeds therefore use
`alpha_i=(M_U^2/M_P^2)c_i`. The prior sign map survives, and the Stage-A
ratios remain the `M_U^2/M_P^2 -> 0` limit, but bare coefficient identity
requires `M_U=M_P`.

**Decision:** record a passed readiness audit and block the scalar ADM
reduction pending an on-shell reservoir/driver, controlled rigid-support, or
cosmological completion. The zero-gradient force-block partial pass survives.

## 2026-07-26 - Background-completion screen

Gate: UVIR-003 (Stage B route selection after the ADM readiness blocker)

**Candidates tested:** constant vacuum energy, a homogeneous minimally coupled
`P(X)` support scalar, the ghost-condensate point, prescribed rigid support, a
new higher-derivative NEC-violating sector and a self-consistent evolving
flat-FRW background.

**Finding:** exact Minkowski support needs
`rho_R+p_R=-mu^2*rho0^2<0`. Vacuum energy and the ghost-condensate point have
zero enthalpy. For `L_R=P(X_R)`, the support condition requires `P_X<0`, while
the two-derivative spatial-gradient health condition is `P_X>0`. The minimal
local scalar route therefore cannot be healthy on the required homogeneous
support state. Stable NEC violation would require added operator structure and
a separate theory gate.

**Rigid boundary:** a prescribed counterstress may label a controlled local
decoupling calculation, but it has no action-derived scalar constraint
response and cannot close the full ADM reduction.

**Route decision:** select a self-consistent evolving flat-FRW background
using the declared sectors. For isolated condensate charge,
`dot(n)+3Hn=0`; exact constant density in expansion would require a separately
declared charge-transfer source `S_N=3Hn`, which is not automatically the
stress-energy exchange vector `Q_syn^nu`.

**Status:** the route is selected, but no background solution is yet claimed.
The next task is to derive and verify an on-shell homogeneous branch, then
perform the metric-aether-condensate scalar constraint reduction on it.
UVIR-003 remains in progress and MAT-001 remains blocked.

## 2026-07-26 - Evolving flat-FRW background

Gate: UVIR-003 (Stage B background construction)

**Homogeneous ansatz:** flat FRW with lapse `N(t)`, comoving unit aether
`U^mu=(1/N,0,0,0)`, evolving complex condensate
`Phi=rho(t) exp(i Theta(t))/sqrt(2)`, constant force background and no
reservoir exchange.

**Aether result:** the four Stage-A contractions reduce to
`O1=3H_N^2`, `O2=9H_N^2`, `O3=3H_N^2`, `a_mu a^mu=0`. The combined
minisuperspace coefficient is therefore
`M_cos^2=M_P^2+(M_U^2/2)(c1+3c2+c3)`, consistent with the corrected
`alpha_i=(M_U^2/M_P^2)c_i` normalization.

**Condensate result:** lapse, amplitude and phase variation give the
Friedmann equation, radial equation and exact conservation of
`a^3 rho^2 mu`. The alignment term vanishes because the homogeneous current is
parallel to the aether; every constant-force derivative also vanishes.

**Existence check:** integrated a representative dimensionless branch with
DOP853 from `t=0` to `t=8`. It stays regular and expanding. The maximum
relative Friedmann residual is `2.124e-10`, charge drift is `2.220e-16`, and
the relative continuity residual is `1.898e-15`. The scale factor grows by
`4.5716`; these numbers are diagnostics of the chosen dimensionless example,
not cosmological predictions.

**Decision:** the absence-of-background blocker is removed. The remaining
scalar ADM reduction is ready to begin on the evolving branch. UVIR-003
remains in progress because no scalar perturbation kinetic/gradient matrix,
physical cutoff or low-k cosmological stability result has been derived.
MAT-001 remains blocked.

## 2026-07-26 - Scalar ADM principal-symbol reduction

Gate: UVIR-003 (Stage B scalar perturbations)

**Controlled scope:** aether-unitary scalar gauge on the verified evolving
FRW branch, with background coefficients frozen over a wavelength and
`q_phys=k/a >> H`. Retained the principal time derivatives, `q_phys^2`
terms, the force `q_phys^4` regulator and the leading lapse-induced
`1/q_phys^2` condensate kinetic correction.

**Constraint result:** the lapse and scalar shift are algebraic in the
principal truncation. Their elimination gives
`K_R=2 M_P^2 F(1-alpha13)/alpha123` and
`G_R=M_P^2(2-alpha14)/alpha14`. Their ratio exactly reproduces the published
Einstein-aether spin-0 speed, providing an independent ADM cross-check of the
earlier literature substitution.

**Condensate result:** the reduced two-field velocity Hessian has determinant
`rho^2[1-(rho_dot^2+rho^2 mu^2)/(M_U^2 c14 q_phys^2)]`. Define
`q_ADM^2=(rho_dot^2+rho^2 mu^2)/(M_U^2 c14)`. The principal signs are
interpretable only for `q_phys >> q_ADM` as well as `q_phys >> H`.

**Representative check:** `K_R=39.94375`, `G_R=52.33333`,
`s0^2=1.310175768`. The principal block is positive. The 801-point trajectory
has `max(a q_ADM)=5.95264` and `max(aH)=0.632766`. The scalar cone is wider
than the metric cone, so global multicone causality remains open; the
dimensionless point is not a physical parameter selection.

**Decision:** record a passed scalar ADM principal-symbol subgate. Do not call
UVIR-003 closed. Next retain the full time dependence and all finite-`q`
terms, solve the constraints along the trajectory and track the reduced
eigenvalues toward `q_phys=0`. MAT-001 remains blocked.

## 2026-07-26 - Time-dependent finite-q scalar ADM reduction

Gate: UVIR-003 (Stage B scalar perturbations)

**Quadratic system:** expanded the full declared two-derivative
metric-aether-condensate scalar action on the verified FRW trajectory in
aether-unitary gauge. Used `Sigma=q_phys^2 beta` for the nonzero-wavenumber
momentum constraint, retained all background, `q_phys^0`, `q_phys^2` and
scalar-shift `q_phys^4` terms, and kept the constant-background force scalar as
its separately factorized `z=2` block.

**Constraint result:** the lapse and momentum constraints are algebraic and
nonsingular over the representative scan. Their exact elimination gives
`L_red=L_0-J^T C^(-1)J/2`. The high-`q` limit reproduces the earlier principal
curvature, amplitude and phase Hessians.

**Finite-q scan:** evaluated 801 background times and 61 logarithmic
wavenumbers from `q_phys/H=10^-3` to `10^3`, for 48,861 matrices. Every
nonzero-`q` kinetic matrix has inertia `3 positive, 0 negative`; the smallest
constraint singular value is `0.0501148`.

**Low-q result:** the exact on-shell kinetic determinant is proportional to
`q_phys^2`. The fitted smallest-eigenvalue power is `2.00066271`, and the
strict `q=0` reduced kinetic rank is two of three. This is not classified as a
ghost because `Sigma` is not an independent exactly homogeneous perturbation.
It is a hold pending the cubic action and canonical normalization of the
collapsing eigenmode.

**Decision:** record `PASS_FINITE_Q_CONSTRAINT_ELIMINATION` together with
`HOLD_KINETIC_RANK_LOSS_AT_Q_TO_ZERO`. UVIR-003 remains in progress. The next
calculation is the cubic low-`q` interaction-scale audit; MAT-001 remains
blocked.

## 2026-07-26 - Low-q scalar gauge-orbit audit

Gate: UVIR-003 (Stage B scalar perturbations)

**Exact endpoint:** the on-shell `q=0` kinetic matrix annihilates
`(H,rho_dot,mu)`, which is the tangent to the homogeneous background under a
time translation. The invariant combinations
`Q_rho=delta_rho-(rho_dot/H)R` and
`Q_theta=vartheta-(mu/H)R` remove this direction.

**Representative check:** the normalized two-field `q=0` physical block has
inertia `2 positive, 0 negative` at all 801 trajectory points, minimum
eigenvalue `0.9372858341` and maximum condition number `1.066910396`. At
`q_phys/H=10^-3`, the smallest finite-`q` eigenvector has minimum alignment
cosine `0.9999999999999994` with the time-shift orbit.

**Decision:** replace the low-`q` kinetic-rank hold with
`PASS_LOW_Q_GAUGE_ORBIT_AUDIT`. Reject a strong-coupling scale inferred by
canonically normalizing the vanishing gauge direction. UVIR-003 remains in
progress and MAT-001 remains blocked.

## 2026-07-26 - Bounded aether Stueckelberg cubic audit

Gate: UVIR-003 (Stage B cubic readiness)

**Controlled scope:** restored `T=t+pi` and expanded the normalized
hypersurface-orthogonal aether through cubic order for a one-dimensional
longitudinal profile with the metric held flat.

**Result:** with the overall `M_U^2` factor suppressed,
`L2=[c14 pi_tx^2-c123 pi_xx^2]/2`, while
`L3=-c14 pi_t pi_tx^2+c123 pi_t pi_xx^2-c14 pi_tt pi_tx pi_x
+(2c123-c14) pi_tx pi_x pi_xx`. The nonzero Fourier mode is normalized by
`chi_k=M_U sqrt(c14)|k|pi_k` and has speed squared `c123/c14`.

**Decision:** record `PASS_BOUNDED_VERTEX_BASIS`, not a physical cutoff. The
one-dimensional decoupling truncation omits non-collinear triads, second-order
lapse and shift response, the evolving background and coupled physical-mode
projection. The physical interaction scale is `NOT_YET_DERIVED`; UVIR-003
remains in progress and MAT-001 remains blocked.

## 2026-07-26 - Three-dimensional khronon cubic and constraint-order audit

Gate: UVIR-003 (Stage B nonlinear scalar readiness)

**3D vertex:** expanded the normalized hypersurface-orthogonal aether through
cubic order in three spatial dimensions. The resulting basis contains the
five compact tensor structures built from `p_i=partial_i pi`,
`v_i=partial_i dot(pi)` and `H_ij=partial_i partial_j pi`; its collinear
reduction exactly reproduces the previous one-dimensional result.

**Constraint order:** for an algebraic constraint block
`L2=z^T J+z^T C z/2`, stationarity of the first-order solution
`z1=-C^(-1)J` cancels every cubic contribution from the second-order
constraint correction `z2`. The reduced cubic action therefore needs the full
cubic ADM vertex evaluated on `z1`, not an explicit `z2` solution.

**Kinematics and scale:** a non-collinear on-shell three-point amplitude is
forbidden for the linear scalar dispersion because equality in the triangle
inequality forces collinearity. An operator-basis NDA diagnostic gives
`q_NDA=0.125778823734` at the unselected representative dimensionless point,
but this is not invariant under field redefinitions and is not a physical
cutoff.

**Decision:** record `PASS_3D_CUBIC_AND_CONSTRAINT_IDENTITY`. The next physical
scale calculation is the constrained scalar `2-to-2` amplitude including
cubic exchange, the quartic contact vertex and physical eigenmode projection.
UVIR-003 remains in progress and MAT-001 remains blocked.
## 2026-07-26 - Three-dimensional khronon quartic and 2-to-2 readiness audit

Gate: UVIR-003 (Stage B nonlinear interaction readiness)

**Quartic basis:** derived the complete three-dimensional flat-decoupling
quartic khronon action. The expanded result has 96 monomials, exactly
reproduces the previous quadratic and cubic actions and matches an independent
one-dimensional quartic construction.

**Elastic COM identities:** the on-shell contact coefficient is
`4[c123^2/c14-(2c123-c14)cos^2(theta)]`. The elastic static-transfer cubic
vertex is proportional to the unit-vector identity, so `t/u` exchange vanishes
exactly. The `s` channel carries zero spatial momentum and its khronon inverse
kernel vanishes: it is the homogeneous preferred-time gauge orbit and cannot
be inverted or dropped in the flat decoupling description.

**Constraint order:** quartic reduction genuinely requires the second-order
constraint source via `Lred4=L4[x,z1]-S2^T C^(-1)S2/2`, where
`S2=partial_z L3[x,z1]`; third-order constraint solutions cancel at this order.

**Decision:** record `PASS_QUARTIC_BASIS_WITH_2_TO_2_GAUGE_HOLD`. Do not assign
a physical cutoff. The next target is the full evolving-FRW constrained cubic
and quartic scalar system, physical eigenmode projection and gauge-regular
`2-to-2` unitarity amplitude. UVIR-003 remains in progress and MAT-001 remains
blocked.

## 2026-07-26 - Nonlinear ADM action-provenance audit

Gate: UVIR-003 (Stage B nonlinear scalar readiness)

**Parent action:** reconstructed the exact aether-unitary ADM action for the
`gravity+aether+condensate+alignment` block. Its coefficient identities
reproduce the verified cosmological Planck mass, FRW minisuperspace action,
finite-`q` lapse/shift constraint matrix, linear source `J1` and alignment
phase-gradient stiffness.

**Action boundary:** the declared force regulator does not yet define a full
nonlinear evolving-frame action. `Delta_U` lacks its generally covariant
completion, and about the selected zero-gradient background
`Y^(3/2)=|epsilon|^3 Y2^(3/2)`, not an ordinary analytic cubic Taylor vertex.
The force mode factorizes at quadratic order but cannot silently be omitted
from the complete nonlinear scalar amplitude.

**Decision:** record `PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE` together with
`HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED`. Do not derive or quote a
full cosmological `J2`, quartic Schur complement or physical cutoff until the
force completion and perturbative prescription are declared. UVIR-003 remains
in progress and MAT-001 remains blocked.

## 2026-07-26 - Force-completion option audit

Gate: UVIR-003 (Stage B force-sector action completion)

**Regulator comparison:** verified the rest-space identity
`D_mu D^mu psi=h^{mu nu}nabla_mu nabla_nu psi+theta Q`, its homogeneous-FRW
cancellation and its constant-frame Stage-A limit. The rest-space Laplacian is
recommended for explicit derivation but is not yet adopted. The projected
Hessian alone changes the homogeneous FRW action; the spacetime divergence
adds an acceleration/lapse-gradient coupling.

**Non-analytic branch:** verified the nonzero-gradient expansion through
quartic order and the zero-gradient series of two smooth completions. The
exact branch supports a local expansion only on a nonzero spatial gradient,
whose quartic transverse coefficient diverges as the background gradient
vanishes. An unsubtracted smoothing generates a canonical `Y` term; a
linear-subtracted smoothing begins at `Y^2`. Both change the exact deep-IR
law.

**Decision:** record `HOLD_ARCHITECTURE_DECISION_REQUIRED`. Track A preserves
exact `Y^(3/2)` but moves the force calculation to a local nonzero-gradient
background. Track B preserves a homogeneous analytic amplitude but introduces
a smoothing scale and requires the weak-field law to be re-tested. Do not
derive the full force-inclusive `J2` until a track is selected. UVIR-003
remains in progress and MAT-001 remains blocked.

## 2026-07-26 - Track A force ADM expansion

Gate: UVIR-003 (Stage B force-sector nonlinear completion)

**Architecture selection:** selected Track A. Adopted
`Delta_U psi=D_mu D^mu psi`, retained exact `Y^(3/2)` and assigned its ordinary
perturbative force analysis to a declared local nonzero-gradient background.
No smoothing scale or canonical linear-`Y` term was introduced.

**ADM expansion:** on the homogeneous zero-gradient FRW branch, verified the
exact rest-space regulator, temporal `Q^2` term and exact IR functional through
direct quartic order. The completed regulator exactly preserves the prior
quadratic `z=2` force block.

**Constraint source:** derived
`J2_deltaN,force=-a^3 K_Q pi_dot^2/2-gamma(partial^2 pi)^2/(2M_*^2 a)` and,
after spatial integration by parts,
`J2_beta,force=a K_Q partial_i(pi_dot partial_i pi)`. The regulator supplies no
shift source and exact `Y^(3/2)` supplies no `J2` term at zero gradient.

**Decision:** record `PASS_FORCE_SECTOR_J2_COMPONENT`. The complete
`g+U+Phi+alignment+psi` source is not yet assembled, and the non-analytic local
force amplitude, quartic Schur complement, physical eigenmode projection and
cutoff remain open. UVIR-003 remains in progress and MAT-001 remains blocked.

## 2026-07-29 - Complete finite-q J2 and quartic Schur block

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Source assembly:** expanded the fixed nonlinear
`gravity+aether+condensate+alignment` ADM parent action to the quadratic
lapse/scalar-shift source and combined it with the Track-A force component.
The linear terms regress exactly to the previous finite-`q` `J1` in the
`(delta_N,Sigma=q_phys^2 beta)` convention.

**Complete result:** derived the full `J2_N` and `J2_Sigma` for
`q_phys>0`. The latter is a finite-wavenumber inverse-Laplacian convolution,
as required by the normalized scalar shift. The exact zero-gradient
`Y^(3/2)` source remains zero under the declared Track-A rule.

**Quartic constraint block:** inverted the exact `2x2` constraint matrix and
verified both by matrix multiplication and direct completion of the square
that second-order constraint elimination contributes
`-J2^T C^(-1)J2/2`.

**Historical decision (superseded by the dressing audit below):** recorded `PASS_COMPLETE_FINITE_Q_J2_AND_SCHUR`. The direct
multi-sector quartic contact action, physical scalar eigenmode projection,
gauge-regular cosmological `2-to-2` amplitude, unitarity criterion and
nonzero-gradient exact-`Y` reduction remain open. UVIR-003 remains in progress
and MAT-001 remains blocked.

## 2026-07-29 - Direct physical-field contact block

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Expansion:** set the lapse and scalar shift to their background values and
expanded the fixed nonlinear
`gravity+aether+condensate+alignment+Track-A force` parent action through
quartic order in `x=(R,delta_rho,vartheta,pi)`. This fixes the complete
constraint-free direct blocks `L3[x,0]` and `L4[x,0]`.

**Regression:** the gravity, condensate/alignment and Track-A force formulas
all pass independent symbolic coefficient checks. The force terms regress
exactly to the constraint-free part of the prior ADM expansion. Exact
`Y^(3/2)` remains a classical `|epsilon|^3` functional rather than an analytic
homogeneous cubic Taylor vertex.

**Decision:** record `PASS_X_ONLY_DIRECT_CONTACT_BLOCK`. This is not
`L3[x,z1]`, `L4[x,z1]`, a physical eigenmode projection or an interaction
cutoff. The next calculation must retain all constraint-dependent cubic and
quartic terms, substitute `z1=-C^(-1)J1`, and combine the result with the
verified `-J2^T C^(-1)J2/2` block. UVIR-003 remains in progress and MAT-001
remains blocked.

## 2026-07-29 - Constraint-dressing completeness correction

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Audit:** expanded the exact homogeneous gravity-plus-condensate lapse
action through quartic order while retaining the first-order lapse. The cubic
action contains `delta_N^2 B1-delta_N^3 B0`, so it is not affine in the
constraint.

**Exact correction:** on the Friedmann background,

```text
S2_N - J2_N,origin =
  2 B1 delta_N1 + 3 V delta_N1^2.
```

The correct general source and quartic reduction are

```text
S2 = partial_z L3[x,z1],
L4_red = L4[x,z1] - S2^T C^(-1) S2/2.
```

**Decision:** record `PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT`.
Reclassify the preceding `J2` and Schur result as a verified origin-linear
component, not the complete second-order source or quartic constraint block.
Complete finite-`q` scalar-shift dressing remains open. UVIR-003 remains in
progress and MAT-001 remains blocked.

## 2026-07-29 - Finite-q scalar-shift dressing sub-block

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Expansion:** derived the exact gravity/aether extrinsic-curvature action
through quartic order for a finite-`q` scalar shift with one homogeneous soft
curvature leg. The quadratic constraint sub-matrix regresses exactly to the
verified finite-`q` lapse/shear block.

**Dressing:** substituted `z1=-C^(-1)J1` and verified explicit nonzero
corrections to both `S2_N` and `S2_Sigma`. The declared channel now has
symbolic `L3[x,z1]` and `L4[x,z1]` sub-blocks.

**Decision:** record `PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK`. This does
not establish the generic non-collinear three-momentum shift kernel,
arbitrary `D_iR D_i beta` contractions, condensate/force shift-advection,
physical projection, amplitude or cutoff. The `q=0` gauge-orbit result is
unchanged. UVIR-003 remains in progress and MAT-001 remains blocked.

## 2026-07-29 - Generic gravity/aether shift kernel

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Tensor expansion:** retained the arbitrary three-dimensional conformal-ADM
structures `D_iD_j beta`, `D_iR D_j beta`, `D_iR D_i beta` and
`(D delta_N)^2` through cubic order.

**Constraint dressing:** separated the direct, origin-linear and nonlinear
constraint-degree pieces of `L3`, then derived the lapse and beta Euler
operators at `z1`. The generic calculation regresses exactly to the preceding
soft-curvature `L2`, `L3`, `S2_N` and `S2_Sigma` results.

**Decision:** record `PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL`.
Condensate and Track-A force shift-advection, combined complete finite-`q`
`S2`, physical projection, amplitude and cutoff remain open. The `q=0`
gauge-orbit result is unchanged. UVIR-003 remains in progress and MAT-001
remains blocked.

## 2026-07-29 - Complete finite-q S2 functional

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Condensate dressing:** expanded the exact temporal ADM block and derived
the nonlinear lapse and scalar-shift advection operators at
`z1=-C^(-1)J1`.

**Force audit:** verified that the Track-A cubic force block is affine in the
constraints. It contributes no nonlinear correction beyond its existing
`J2_origin` component on the homogeneous zero-gradient branch.

**Assembly:** combined the origin-linear source, generic gravity/aether
dressing and condensate dressing into the complete finite-`q`
`S2=partial_z L3[x,z1]`. The corrected constraint functional is
`-S2^T C^(-1)S2/2`.

**Decision:** record `PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL`. Complete generic
`L4[x,z1]`, physical scalar projection, the exchange-plus-contact amplitude,
physical cutoff and the local nonzero-gradient exact-`Y` reduction remain
open. The `q=0` gauge-orbit result is unchanged. UVIR-003 remains in progress
and MAT-001 remains blocked.

## 2026-07-29 - Complete generic L4 contact functional

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Expansion:** retained every generic gravity/aether, condensate/alignment
and homogeneous zero-gradient Track-A quartic term at
`z1=-C^(-1)J1`.

**Regression:** recovered the independently verified direct `L4[x,0]` and
soft-curvature gravity/aether `L4[x,z1]` blocks exactly.

**Decision:** record `PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT`. The complete
reduced quartic functional is assembled before physical projection. The
physical scalar basis, amplitude and cutoff remain open.

## 2026-07-29 - Regular finite-q physical scalar basis

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Basis:** defined `Xi=(q_phys/H)R`,
`Q_rho=delta_rho-(rho_dot/H)R`, and
`Q_chi=rho[vartheta-(mu/H)R]`.

**Verification:** the transformed kinetic determinant and `q_phys -> 0`
matrix are finite and nonzero on shell. The representative scan has positive
inertia across 39,249 matrices over `10^-3 <= q_phys/H <= 10^3`.

**Projection:** fixed the time-dependent, leg-wise cubic and quartic
projection maps. The exactly homogeneous `Xi` leg remains excluded as gauge.

**Decision:** record `PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS`. Explicit
projected vertices, amplitude and cutoff remain open.

## 2026-07-29 - Complete factorized cubic momentum kernel

Gate: UVIR-003 (Stage B constrained nonlinear scalar action)

**Cubic assembly:** consolidated and regressed the complete generic
multi-sector `L3[x,z1]` functional against the direct, generic
gravity/aether, condensate temporal, Track-A and soft-curvature audits.

**Fourier polarization:** polarized the analytic cubic functional over three
non-collinear legs, inserted exact finite-`q` per-leg lapse/shear resolvers,
and applied the time-dependent `(Xi,Q_rho,Q_chi,Pi)` map.

**Boundary:** the exact `|grad(pi)|^3` term has no ordinary Taylor kernel at
the homogeneous zero-gradient background. The exactly homogeneous internal
`Xi` channel is outside the finite-`q` map and cannot be obtained by naive
substitution.

**Decision:** record
`PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL`. The reduced quartic
momentum kernel, gauge-regular homogeneous internal-channel prescription,
exchange-plus-contact amplitude and cutoff remain open. UVIR-003 remains in
progress and MAT-001 remains blocked.
