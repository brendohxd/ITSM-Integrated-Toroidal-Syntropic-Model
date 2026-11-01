# Two-repair quadratic comparison: F-tau gradient failure, R-tau norm question

31 October 2026, Australia/Perth.
Result ID: R9-MT1-TWO-REPAIR-CHARACTERISTICS-V3.
Claim Conditional; review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE. Neither candidate is an adopted parent.

## Outcome and scope

The new full quadratic/current calculation distinguishes the two candidates
that passed the earlier temporal-kinetic test. On the common OLD homogeneous
B1 control, at the registered initial event:

| Candidate | New result | Disposition |
|---|---|---|
| F-tau: whole frame defined by the existing dust clock before variation | One ordinary high-frequency scalar branch has squared speed -1/33 | Fails gradient health as an uncut continuum on this control; dependent all-frequency healthy evolution is held |
| R-tau: only the regulator uses the dust-clock projector | Ordinary squared speeds are nonnegative; a repeated zero-speed scalar root is defective in the stated equal-order balanced variables | Supported comparator for a bounded physical-norm/constraint analysis; strong hyperbolicity and a physical window are NOT established |

The positive kinetic matrices from the first bundle remain correct in their
original scopes. They never implied healthy spatial propagation. These are
candidate-specific results, not revisions to the unchanged R4C1 action or an
all-ITSM no-go theorem. The later vortical eta=1/4 B1-frame preparation is NOT
the background tested here.

The [V1 contract](RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V1_CONTRACT_2026-10-31.md),
[execution specification](RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V1_EXECUTION_SPEC_2026-10-31.md)
and [candidate definitions](RES001_R4C1_TWO_REPAIR_CANDIDATES_V1_2026-10-31.md)
own the calculation. This bundle completes the declared quadratic export and
initial principal-symbol disposition. Physical constrained-norm clearance,
global reduction, nonlinear evolution and the interacting domain remain open.

## Construction retained in the calculation

The full second variation is recomputed from EACH candidate's own density.
Generic coefficients depend on (a,H,u,v,r,u_dot,v_dot,r_dot,psi_dot,psi,rho)
along the admitted common homogeneous solution. No old specialized B/Q or
propagator is reused as the candidate dynamics. The original full-frame Euler
row is used only as the declared chain-rule control for F-tau's clock current.

For each nonzero Fourier mode use exp(i*k*z), metric perturbation
h=a^2*(I+gamma), physical frame amplitudes v=a*delta U_spatial where present,
and the specified clock gauge. The multiplier gives N=tau_dot/C. Before
substitution, the independent lapse equation includes its spatial Euler flux
E_N=L_N-i*k*L_Nz and reconstructs the density; it is not discarded.

The new algebraic block for (delta Z,Sx,Sy,Sz) is, for BOTH candidates on
this aligned background,

    D = diag(5*a^3/11, a*k^2/2, a*k^2/2, -a*k^2/15).

Its negative shift entry is an algebraic pivot, not a propagating ghost.
The actual algebraic solve and stationary action pullback are verified.
The auxiliary equation gives delta Z=(k/a)^2*delta psi. No Z time velocity
is present. All three shift equations, density and lapse are reconstructed.

The regular reduction requires a>0, k!=0, nonzero declared coefficients and
the positive timelike-clock/dust branch, chi=C>0 and rho>0. Density zero,
clock-gradient nullity, caustics and degenerating constraint pivots are not
admitted by extrapolation. No uniform lifetime near these boundaries follows.

In L2=(qdot^dag M qdot+qdot^dag B q+q^dag B^dag qdot+q^dag Q q)/2,
the exported generator retains

    M*qddot + (M_dot+B-B^dag)*qdot + (B_dot-Q)*q = 0.

Here M=a^3*M0 and M_dot=3*H*M, but B_dot is evaluated using the actual
background flow. The time-dependent symplectic form with blocks
(B-B^dag,M;-M,0) satisfies its exact transport identity. Dropping drift or
continually projecting evolution onto selected modes is not part of this
construction. These identities do not themselves prove nonlinear stability.

## Changed clock current and matter balance checked in the coupled system

The induced clock current from the first report is retained. Define the
scaled bare-dust density perturbation

    j = delta rho - beta*rho*delta psi + rho*tr(gamma)/2,
    W = j_dot + (3*H-beta*psi_dot)*j - i*k*rho*Sz/a.

For R-tau the new equations give exactly

    W = b*psi_dot*k^2/a^2 * delta Z
      = b*psi_dot*(k/a)^4*delta psi.

For F-tau they give W=(i*k/a^4)*E_vz,density, with the OLD complete frame
Euler density evaluated on the new F configuration, not imposed as zero.
Both identities are checked coefficient by coefficient modulo the background
Friedmann constraint. Omitting lapse-gradient Euler flux fails the explicit
rejection control. The full condensate U(1) current, including the R-tau
frame contribution, satisfies its own exact Ward identity.

Thus old bare-dust continuity is NOT a valid replacement equation for either
candidate. On clock-normal slices the induced current has zero normal flux;
its spatial flux changes local transport without adding an independent
normal charge density. This specifies the scope of the earlier phrase
"combined clock charge". The original matter force and changed energy-balance
identities are those in the first comparison report; no irreversible entropy
production is inferred from this reversible classical calculation.

## Initial mixed-order characteristics

Use exp(i*k*z-i*omega*t), a=1 at the registered initial event, and metric
light speed one in the control units. Extract the ordinary omega~k and fast
omega~k^2 asymptotics of the FULL coupled scalar determinant. The fast field
is not deleted. The displayed principal pencil retains k^2 and k^4 terms and
velocity-gradient mixing; it omits background-scale lower-order terms only
for this asymptotic analysis. It is not the complete finite-k dispersion law.

Let y=omega^2/k^2 and z=omega^2/k^4. The monic leading scalar polynomials are

    F-tau ordinary: (y-1)^2*(13*y-14)*(33*y+1)/429,
    R-tau ordinary: y*(y-1)^2*(3*y-1)*(13*y-14)/39,
    F-tau fast: z^4*(33*z-5)/33,
    R-tau fast: z^5*(33*z-5)/33.

The zeros in the fast scaling include the slower ordinary branches; they
are not additional propagating zero-frequency particles.

| Initial branch | F-tau | R-tau |
|---|---|---|
| Tensor squared speeds, two polarizations | 1,1 | 1,1 |
| Independent vector squared speeds | No independent frame vectors | 4/5,4/5 |
| Ordinary scalar squared speeds | -1/33,1,1,14/13 | 0,1/3,1,1,14/13 |
| Nonzero quartic branch | omega^2~(5/33)*k^4 | omega^2~(5/33)*k^4 |

These are control-unit coefficients, not a conversion to a physical torus
length, cutoff or observed frequency. Isotropy justifies local helicities;
it does not imply arbitrary global rotations of the compact torus.

F-tau's negative squared speed implies an asymptotic exponentially growing
ordinary branch, rate |k|/sqrt(33) at the frozen event. The positive quartic
branch does not cure this separate branch. This rejects an all-frequency
healthy continuum claim on this control. It does NOT exclude every separately
justified low-energy EFT domain; no physical cutoff has been derived here,
and selecting one solely to hide the failure is not authorized.

R-tau's real nonnegative squared roots do not establish strong hyperbolicity.
Its ordinary limiting trace/frame block, in variables
(k*Gamma,k*v_z,Gamma_dot,v_z_dot), Gamma=(gamma_xx+gamma_yy)/2, has

    A = [[0,0,1,0], [0,0,0,1],
         [1/33,0,0,-2*i/33], [0,0,-6*i,0]].

The zero eigenvalue has algebraic multiplicity two and geometric multiplicity
one; dim ker(A^2)=2. Explicitly e=(0,1,0,0), g=(2*i,0,0,1) obey Ae=0 and
Ag=e. Hence the frozen limiting block has g+k*t*e evolution in this balanced
norm. This is an obstruction to a k-uniform estimate in THAT norm, not yet a
proof that every physically constrained or appropriately mixed-regularity
dust formulation fails. The reconstructed density involves derivatives, the
full operator contains background-scale mixing, and the quartic mode must
remain in an actual estimate. Removing the zero mode is not an acceptable
repair. This physical-norm/constraint interpretation is the next deciding task.

The 14/13 branch exceeds the metric squared light speed. Neither causality
clearance nor an observational exclusion follows from this number alone.
Preferred-foliation characteristics, interactions, coupling to realistic
matter and applicable primary-source experimental constraints remain to be
assessed. Tensor speed one alone is not GR/PPN recovery.

## Homogeneous torus mode treated separately

k=0 is constructed before the nonzero-mode spatial gauge and shift inverse.
All six homogeneous metric amplitudes are retained. Constant homogeneous
shifts are gauge choices with identically homogeneous momentum constraints;
they are not inverted copies of D at k=0. Z has its nonzero algebraic pivot.

The homogeneous temporal matrices have raw inertia (9 positive,1 negative)
for F-tau and (12 positive,1 negative) for R-tau, and are invertible. These
include the homogeneous metric-volume direction. They are not a new quantum
ghost verdict from an unreduced conformal sign. Two independent clock/U(1)
charge rows obey the exact transported conservation equations, giving
charge-restricted linear phase-space dimensions 18 and 24 respectively.
This is not a completed global symplectic/Dirac quotient, a dust-caustic
theorem or proof of a global clock. No torus mean is silently removed.

## Verification, preservation and actual holds

- [V3 executable](../../../Analysis/MasterTests/test_01_r4c1_two_repair_characteristics_v3.py),
  [V2 full-quadratic helper](../../../Analysis/MasterTests/r4c1_two_repair_quadratic_v2.py),
  unchanged declared candidate backend V2.
- [Fresh receipt](../../../Analysis/MasterTests/outputs/r4c1_two_repair_characteristics_v3_attempt_01/summary.json):
  129/129, zero failed/unknown checks; SHA256
  acc0558461b0e7882edc6e59baae4d9b2d886fb33882bd0bc5928834a1a57515.
  Full recomputing read-only replay is byte-identical, exit zero.
- 39 input pins and their sidecars retain bytes and modification times.
  Physical-action real centered differences retain the full norm-cubed force:
  largest normalized errors below 1.451e-12 and 1.451e-18 at steps 1e-10 and
  1e-16, below the frozen 1000*step bounds. Its zero C2 contribution at this
  aligned event is not an absence at finite amplitude.
- Actual B_dot centered differences at k=1,7,40 have normalized errors below
  2.664e-28 and 2.664e-44 for steps 1e-14 and 1e-22. Independent real
  two-quadrature assembly, stationary action pullback, current identities and
  actual symplectic drift are checked.
- V1 exact-type mismatch and V2 filename-preflight failure are preserved with
  their source files, seals and private logs. Neither produced a scientific
  receipt. The [V3 addendum](RES001_R4C1_TWO_REPAIR_CHARACTERISTICS_V3_EXECUTION_ADDENDUM_2026-10-31.md)
  records these implementation fixes; no equation or tolerance was changed.
- Same-author controls and exact replay remain provisional, not independent
  peer review. Original R4C1 evidence, earlier failures and paper versions
  retain their separate authority.

Proceed with a bounded R-tau physical-norm/constraint analysis under the
operator's existing two-route comparison authority. F-tau's dependent
all-frequency healthy-continuum route is held by an actual gradient failure.
Neither is canonically selected. No physical interacting window, cutoff,
finite-time nonlinear domain, microscopic clock selection, realistic-matter
extension, healthy GR limit, numerical C_chi/a0 or identifying matching follows.

No concrete defect in the existing P1/P2, Thermodynamics or unchanged-action
R4C1 manuscripts is established by these NEW unadopted candidate results;
they were not silently folded into those papers. Original G1-G6 INCOMPLETE;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED; TOP-X4 unchanged. Rule-9 DEFERRED is not the substantive
blocker. No publication, vault mutation, model/provider dispatch, commit,
push or deployment. The native goal controller last remains BLOCKED; the
exposed API cannot resume it, though the selected comparison work is authorized.
