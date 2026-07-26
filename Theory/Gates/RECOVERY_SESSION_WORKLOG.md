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
