# Frozen contract: constrained fixed-charge patch momentum form

19 October 2026. Unchanged R4C1 action; approved bounded Stage-2 research.
Review DEFERRED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.

## Question and domain

Does an indefinite momentum form survive the actual lapse/spatial constraints
and the two fixed global charges on regular, nonzero-tilt patches of the
registered initial profiles? This is NOT a physical-mode/ghost/cutoff test.
Do not substitute a raw unreduced signature for this calculation.

Use all nine existing joint-root family/eta certificates, their unchanged
0<|e|<=1/500 range, k=40, positive p=eta/5 and future dust branch. Work only
on patches pi/6<theta<pi/3, theta=k*z modulo reflections. Thus w and Z_z do
not vanish on the support of compactly supported variations. Perturbations
vanish near every node. No new state is adopted or evolved. The complement
inverse may be bounded using its nodal limit; the force/regulator inverse
must NEVER be applied at a node. eta=0 is excluded.

## Derivation, before any numerical sign decision

1. Start from the existing original-action ADM density and true constraints,
   including the lapse flux. Eliminate independent unit/dust auxiliaries only
   after their variations. Use psi=tau as a local force-clock gauge AFTER
   canonical variation, not T=t simultaneously. With psi_i=0, s=psi_hat>0,
   the clock bracket is s and N=1/s. State the sign H_psi=-p_psi explicitly.
2. Retain the full twelve-velocity complement R and ell(s)=ell0+s*h.
   With volume=1 on the registered initial slice,
   Erest=(P-ell)^T R^-1(P-ell)/2+p_psi*s-f(s), p_Z=-b*w^2*s.
   f contains the original potential, curvature, spatial jets and cusp.
   On the positive-s patch its cubic coefficient is -A*|w|^3.
3. Set G_i=(h_xz,h_yz,h_zz-1) on the planar perturbation sector. Check the
   nonzero-mode gauge matrix (partial_z,partial_z,2partial_z); the translation
   kernel/zero mode is not inverted. Check the canonical one-form pullback.
   This is not an arbitrary-three-dimensional Dirac-algebra proof.
4. Hold configurations, p_V, phase momentum and p_T fixed, with v=0,u=Rc.
   For smooth F supported in a regular patch take delta p_Z=F'/Z_z and
   delta pi_zz=F/2. Check delta C_z=-F'+delta p_Z*Z_z=0 and the transverse
   rows. A separate delta p_u=chi, with chi of compact support and zero mean
   if desired, also preserves C_i and Q_U1=u*p_v-v*p_u. Q_dust=int p_T is
   fixed exactly, not just at first order. Solve p_psi from H_perp=0 at
   fixed positive p_T and unchanged lapse flux. Small amplitudes preserve
   s>0. No compensating mean dust-charge change is permitted.
5. Derive the Hessian of H_psi on this constraint-surface chart, not that of
   the unreduced action. At the background, with s=p and the local lapse
   equation imposed, the NEGATIVE of the s-s entry must be independently
   checked against B=[K_Q*(1+w^2)-h^T R^-1 h]/p-6*A*|w|^3
   -2*b*w^2*Z_hat/p^2. Indeed H_perp=p_psi*s+E0+p_T+flux gives
   H_psi=-p_psi=+(E0+p_T+flux)/s; this overall sign is not optional.
   Here Z_hat=Ud*w^2-Rshift*Z_z, with Rshift the original longitudinal shift;
   Ud is the jointly adjusted coefficient, NOT U_dot. Retain this drift.
6. If B>0 and R is regular, derive an explicit coercive patch criterion for
   the NEGATIVE of the F momentum form, including the induced pi_zz and its
   mixed term. With
   inverse infinity-norm bound N_R, Y>=|(R^-1(P-ell0))_zz|, U in [Ul,Uu],
   a=e^2, and B>=Bmin>0, a sufficient criterion is

       ||F'||^2/||F||^2 > a^4 * [
         9*N_R*b^2*Uu^2*k^2/(8*p*Bmin)
         +27*b^2*Y^2*Uu^4*k^2/(p^4*Ul^2*Bmin^2)].

   It follows from Young's inequality with c in [a/4,3a/4] and
   |Z_z| in [sqrt(3)*Ul*k*a/2,Uu*k*a]. Check the actual sufficient bound
   against Poincare's 36*k^2 on the declared patch, or report the necessary
   smaller support. Do not call this geometric test an EFT cutoff.
   Check the independent radial-momentum direction H_pu,pu=+1/p and its
   cross term, including fixed-charge reduction. Overall time reversal
   reverses all signs and cannot turn an indefinite form definite.

## Verification and failure policy

Freeze this contract, a versioned executable and their SHA-256 sidecars
before execution. Fresh output only; no edits to executed sources or failed
attempts. Use the standalone optimizer. Windows spawn process pool, at most
16 workers and at most nine independent case jobs, parent-only receipt writes.

Use exact symbolic identities and outward interval bounds over the declared
amplitude/angle and root boxes. Bound R^-1 by a proved Neumann criterion,
not sampled nonsingularity. Independently construct all R entries, affine
terms and the Legendre energy/Hessian from the original four-coordinate
density with nonzero shift and spatial gradients. Compare at both tilt signs
for every family/eta at 110 digits; freeze normalized tolerance 1e-45.
Those approximate first-jet controls do not replace the interval proof or
claim that a whole control configuration is the registered solution.

Reject omitted clock constraint, pi_zz compensation, lapse source/flux,
regulator drift, full complement, or fixed-charge conditions. A nonzero
off-shell lapse witness must show that the on-shell Hessian identity is not
an off-shell substitution. Keep failures/unknowns visible. Perform a fresh
read-only exact replay and preserve source/sidecar bytes, sizes and mtimes.

## Interpretation and stop boundaries

If both signs are established, the result is an indefinite constrained
fixed-charge INSTANTANEOUS MOMENTUM FORM on these regular planar patches.
Do not call it a complete physical Hessian, propagating ghost, dispersion
relation, below-cutoff instability, action no-go, family GO, or proof of a
nonempty physical window. Background evolution, coordinate-momentum mixing,
rank-changing nodes, C2/weak Cauchy existence, arbitrary3D constraint closure,
and the energy/frequency/interaction domain remain substantive questions.
An indefinite instantaneous form alone does not settle those questions.

The prior homogeneous fixed-both positive result and its different domain
remain intact, as do the old rejected velocity and new joint-root results.
No action/parent/model/provider/runtime change, vault mutation, manuscript,
PDF, site, publication, commit or push. Stage 2 incomplete; Stage 3 not entered;
matching inputs absent. Pending Rule-9 review alone does not block this work.
