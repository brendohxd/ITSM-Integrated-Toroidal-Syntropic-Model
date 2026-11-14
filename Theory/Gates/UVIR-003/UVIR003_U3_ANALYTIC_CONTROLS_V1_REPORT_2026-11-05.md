# U3 completed analytic controls: B1 and B2

5 November 2026. The original bounded U3 A0-A2 screen is COMPLETE within its
force-control scope. Neither branch is adopted as the live IR theory. The
larger U3 programme, including a microscopic origin and the full coupled
viability/amplitude calculation, remains OPEN.

Owner specification: [frozen contract](UVIR003_U3_ANALYTIC_CONTROLS_V1_SPEC_2026-11-05.md).
Executable: `Analysis/UVIR/UVIR-003/U3_ANALYTIC_CONTROLS/u3_analytic_controls_v1.py`.
Receipt: `Analysis/UVIR/UVIR-003/U3_ANALYTIC_CONTROLS/outputs/u3_analytic_controls_v1_20261105/receipt.json`.
The July force-completion owner already verified the two Taylor series. This
work reuses them and completes the dimensions, constitutive equations, force
Hamiltonian/DOF, direct ADM changes and normalized homogeneous contact kernel.

## A0: identity and scope

These are alternative completions of the existing spatial force operator.
They are not PKM1, a condensate derivation, AQUAL, a repair to R4C1, or a new
microscopic parent. Track A remains selected. The independent M4 pole/domain
limitation does not enter these algebraic force-control results and is not
resolved by them.

Use the existing hypersurface-orthogonal unit-frame host and rest-space
Laplacian. The homogeneous control has constant psi_bar, with Q_bar=0 and
D psi_bar=0. The fixed-frame flat force block is

    L = K Q_raw^2/2 - B F_i(Y) - r_reg (Delta_U psi)^2/2
        - C_m delta_rho psi,
    Q_raw = U.d psi,  Y=|D psi|^2/a_ref^2,
    r_reg = gamma/M_*^2.

K, B and r_reg are positive symbolic inputs. They have not been matched.
The matter term specifies the static source convention, not a derived
covariant matter action or physical MAT residue.

## A1: units, analytic domain and IR changes

In natural units with dimensionless psi, [derivative]=[a_ref]=1,
[K]=2, [B]=4, [r_reg]=0, [C_m]=0 and [delta_rho]=4. Both Y and sigma are
dimensionless. Here a_ref denotes the existing architecture's a0 normalization;
it is not newly chosen, calculated or fitted. In the raw-gradient chart
I=|D psi|^2 one has exactly

    B F_i(I/a_ref^2;sigma) = A_raw F_i,raw(I;Sigma_raw),
    A_raw=B/a_ref^3,  Sigma_raw=sigma*a_ref.

Thus the dimensionless crossover of the older owner is compatible with the
dimensionful raw-gradient invariant of the ADM owner. They must not be mixed
in one formula. `sigma=CONTROL_SCALE_NOT_DERIVED`; its physical normalization
also depends on the unresolved matter coupling.

The declared functions are

    F_1=(Y+sigma^2)^(3/2)-sigma^3,
    F_2=F_1-(3/2)sigma Y.

For sigma>0 they are real analytic on Y>-sigma^2. Their Taylor series about
zero converge for |Y|<sigma^2; the physical spatial invariant satisfies Y>=0.

    F_1=(3/2)sigma Y+(3/8)Y^2/sigma-(1/16)Y^3/sigma^3+R_4,
    F_2=                 (3/8)Y^2/sigma-(1/16)Y^3/sigma^3+R_4.

Taylor's theorem gives, for Y>0,

    3Y^4/[128(sigma^2+Y)^(5/2)] <= R_4 <= 3Y^4/(128sigma^5).

This follows from F_i''''=9/[16(Y+sigma^2)^(5/2)], positive and decreasing.
Keeping only terms through Y^2 instead has a negative remainder of magnitude
at most Y^3/(16sigma^3). These are mathematical expansion bounds, not a
physical EFT cutoff.

At fixed positive Y both functions tend to Y^(3/2) as sigma->0. But the
quartic-gradient coefficient diverges as 1/sigma. The zero-smoothing limit
does not restore the exact original operator AND retain finite homogeneous
Taylor vertices. No such exchange of limits is used here.

Variation on the constant flat frame gives the actual static equation

    div[(2B/a_ref^2) F_i'(Y) grad psi] - r_reg Delta^2 psi
      = C_m delta_rho.

Define the constitutive multiplier mu_i=(2/3)F_i'. Then

    mu_A=sqrt(Y),
    mu_1=sqrt(Y+sigma^2),
    mu_2=sqrt(Y+sigma^2)-sigma
        =Y/[sqrt(Y+sigma^2)+sigma].

For Y<<sigma^2, B1 has mu_1->sigma, hence a linear Poisson-type force flux.
B2 has mu_2~Y/(2sigma), hence a cubic-gradient force flux. The original flux
is quadratic in the gradient magnitude. Consequently neither completion
preserves the original square-root constitutive asymptote. Where a separate
high-symmetry local reduction and regulator-neglect approximation are justified,
the corresponding algebraic source powers would be one, one-third and
one-half respectively. These are conditional constitutive comparisons,
not universal pointwise acceleration laws or disk solutions.

The regulator cannot be discarded simply because the gradient is small.
For the periodic profile psi=epsilon cos(kx), B2's leading nonlinear flux
has fundamental Fourier coefficient

    -9B epsilon^3 k^4/(8sigma a_ref^4),

whereas the regulator contributes `-r_reg epsilon k^4`. Their magnitude ratio
is `9B epsilon^2/(8sigma a_ref^4 r_reg)`, which tends to zero as epsilon->0
at fixed positive coefficients and nonzero k. Thus the linear regulated
response dominates this small-amplitude limit. A blanket cube-root prediction
for the full B2 boundary-value problem would be incorrect.

On T^3 with periodic fields the static equation also requires
`C_m integral(delta_rho)=0`. The mean source must be compensated or assigned
to a separately evolving background equation. The regulator, curl/harmonic
sectors and boundary conditions are not eliminated by the constitutive
comparison. No constant gradient is assumed to be a globally periodic field.

The spatial energy Hessian has eigenvalues

    lambda_perp=3B mu_i/a_ref^2,
    lambda_parallel=3B(mu_i+2Y mu_i')/a_ref^2.

B1 is strictly positive even at the origin. B2 is positive at Y>0, but both
second-order stiffness eigenvalues vanish at Y=0. The retained fourth-spatial-
derivative term supplies the homogeneous nonzero-mode dispersion there.

## A2: unchanged local force-mode count and changed vertices

No fields or higher time derivatives are introduced. At constant psi_bar
the force quadratic block still factorizes from the other host variables:
each derivative of pi starts at first order, so factors of metric/frame
perturbations enter this force action only at higher order. Its flat quadratic
Hamiltonian is

    p_pi=K pi_dot,
    H_2=p_pi^2/(2K)+c_i |grad pi|^2/2+r_reg (Delta pi)^2/2,
    c_1=3B sigma/a_ref^2,  c_2=0.

There is one force canonical pair for K>0, with nonnegative quadratic energy.
For nonzero spatial momentum,

    omega_1^2=(3B sigma/(K a_ref^2))k^2+(r_reg/K)k^4,
    omega_2^2=(r_reg/K)k^4.

The k=0 shift mode is a separate collective coordinate with zero frequency;
it is not a particle state with a nonzero-frequency oscillator normalization.
The result certifies neither the other host block's health nor the full
nonlinear coupled constraint rank. The formal large-k dispersion does not
define a physical validity window or a causal UV completion.

The direct ADM changes are explicit. Set N=1+n, h_ij=a^2 exp(2R)delta_ij and
G_pi=partial_i pi partial_i pi. Write

    c=3B sigma/(2a_ref^2),  lambda=3B/(8sigma a_ref^4).

The new spatial terms for B1 are

    L_2=-c a G_pi,
    L_3=-c a(n+R)G_pi,
    L_4=-c a(nR+R^2/2)G_pi-lambda G_pi^2/a.

B2 instead has zero new L_2 and L_3, and

    L_4=-lambda G_pi^2/a.

In particular B1 changes the quadratic lapse source by
`Delta J2_N=-c a G_pi`; B2's new spatial operator changes no J2 component.
The existing kinetic and regulator cubic/constraint sources still remain in
both branches. B1 therefore cannot inherit the old force exchange calculation
unchanged. B2's finite contact does not remove any other exchange or constraint
contribution from the full four-point problem.

## Actual homogeneous force contact kernel

Time-normalize chi=sqrt(K)pi. The new flat quartic force interaction for both
controls is

    L_4=-g_4 (partial_i chi partial_i chi)^2,
    g_4=3B/(8sigma a_ref^4 K^2),  [g_4]=-4.

With all four spatial momenta incoming and Fourier derivative +i k_i,

    i M_contact = -i 8g_4 [
        (k1.k2)(k3.k4)+(k1.k3)(k2.k4)+(k1.k4)(k2.k3)].

For an elastic centre-of-mass configuration with incoming p,-p and outgoing
p',-p', |p'|=|p|=k, its amputated contact kernel is

    M_contact=-3B k^4(1+2cos^2(theta))/(sigma a_ref^4 K^2).

It is finite for sigma,K>0, nonzero for generic nonzero momenta, and ordinary
polynomial polarization exists at the homogeneous force background. This
answers the original B2 homogeneous-vertex question affirmatively WITHIN THE
RESTRICTED FORCE CONTROL, using the existing positive regulator for its
nonzero-mode external dispersion. Without that regulator B2 has no quadratic
spatial propagation about the origin; the quartic operator alone does not
supply its own perturbative external modes.

This is an amputated force contact, not the full constrained amplitude.
External state factors must use the branch's actual omega_k, not a silently
relativistic omega=k. On a finite torus the mode expansion instead gives
discrete transition coefficients, with momentum Kronecker conservation and
volume/state normalization; it does not by itself define an asymptotic
cosmological S-matrix. No optical theorem, unitarity bound or physical cutoff
is established by this calculation.

## Field-rescaling check and unresolved identifying inputs

For psi'=s psi, s>0, at fixed a_ref the same control is represented by

    K'=K/s^2, r_reg'=r_reg/s^2, B'=B/s^3,
    sigma'=s sigma, C_m'=C_m/s, Y'=s^2 Y.

Exactly `F_i(s^2 Y;s sigma)=s^3 F_i(Y;sigma)`. Thus the dispersion coefficients,
g_4, C_m/sqrt(K), and the signed matter-gradient crossover C_m sigma a_ref are
invariant. Keeping sigma fixed while rescaling psi would change the control,
not merely rename it. No numerical K_Q, matter residue, crossover acceleration
or acceleration coefficient has been identified.

## Verification, completion and handoff

The fresh executable passes 33/33 controls and byte-identical replay. It
checks exact gradient Hessians, ADM terms, force Hamiltonians, source mean,
rescaling and limit identities. The four-leg coefficient is also reproduced
by independent subset polarization on three elastic integer-momentum
configurations. High-precision direct function evaluations at nine points
verify the analytic Taylor-remainder enclosure. These are bounded computational
controls, not independent peer review or physical clearance.

- Original U3 B1/B2 A0-A2 analytic-control deliverable: COMPLETE_SCOPED.
- Full U3 UV-origin, radiative protection, coupled physical amplitudes and
  validity window: OPEN. Neither sigma nor the subtraction has a derived
  microscopic origin here. No architecture adoption is made.
- MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; live V NOT_COMPUTED.
  The existing M4 physical-domain/residue task remains INCOMPLETE independently.
- The next original U7/U6 conditional tasks must follow their actual triggers;
  do not invent a rank obstruction or start a replacement parent to populate
  a checklist. Other unfinished routes retain their separate acceptance tests.

The condition check uses the current
[U5 rank owner](../MAT-001/MAT001_U5_PKM1_COVARIANT_COMPLETION_V1_REPORT_2026-11-05.md)
and [M4 pole/domain owner](../MAT-001/MAT001_M4_P0B_POLE_DOMAIN_V1_REPORT_2026-11-05.md).
U5 found no ADM/covariant rank discrepancy in its regular domain, so U7 is
NOT_TRIGGERED on that evidence. M4's lack of a demonstrated slow-pole hierarchy
is not a demonstrated failure of the metric host; U6 is likewise
NOT_TRIGGERED_BY_CURRENT_RESULTS. Neither status is completion of the optional
calculation or a permanent exclusion of that route. Those reports are used
for this handoff condition only, not as prerequisites for U3's force algebra.

Direct provisional dependencies are the pinned existing force/architecture
owners; all unresolved reviews of those used inputs are inherited. No M4
physical-pole clearance is assumed. `review_status=DEFERRED`,
`Rule9_cleared=false`, execution `PROCEED_PROVISIONALLY` for this completed
control, `physics_pass=false`, `gate_effect=NONE`. There is no substantive
blocker to reusing the stated algebra; missing matching, UV origin and full
coupled physics block the stronger uses listed above. Original source bytes,
hashes and sidecars are preserved. No publication, provider dispatch, vault
mutation, Git delivery, deployment or runtime reconfiguration occurred.
