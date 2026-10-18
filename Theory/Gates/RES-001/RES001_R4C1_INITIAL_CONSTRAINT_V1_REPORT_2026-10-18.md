# R4C1 initial constraints: exact system supplied, full data still open

18 October 2026. Unchanged-action Stage 2. Local validation 222/222 PASS;
complete fresh read-only replay exact, exit zero. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

**Initial-data acceptance is PARTIAL / OPEN.** This calculation supplies the
exact restricted nonlinear constraint system and a coercive shift problem.
It does not yet supply the fully certified finite-amplitude data required by
the [contract](RES001_R4C1_INITIAL_CONSTRAINT_V1_CONTRACT_2026-10-18.md).
No archived preparation, state or result is changed or newly adopted.

## What advanced

The transverse momentum constraint has an explicit nonlinear first integral.
The longitudinal constraint is a variable-coefficient linear boundary-value
problem for the shift once the other initial fields are specified. Its
coercivity has an explicit positive bound at every registered family/eta
point for the stated diagnostic amplitudes. Its quadratic limit agrees with
the old longitudinal shift in all 18 archived initial events.

The local lapse constraint is also exported, including its frame-momentum
flux. The remaining mean expansion and density problem is now specified;
it has not been certified by these checks. A well-defined shift operator is
not a physical energy, Cauchy or EFT-window verdict.

## 1. Initial slice and original action

Use the registered exact reference initial recipe at a=N=C=1, with flat
spatial metric, homogeneous scalar positions, u=r=sqrt(eta),
v_cond=psi=T=0, u_dot=0, r_dot=sqrt(eta)/4, p=psi_dot=eta/5,
rho0=1/5, and the original positive background H0. The prospective uniform
metric expansion H remains to be fixed; it is not set equal to H0 at finite
amplitude by assumption. The exact future-unit frame and shifts are

    V=(0,w(z),0),  w=e cos(kz),  k=40,
    V_dot=(0,-H0 w,0),  S=(0,Sy(z),R(z)),  R=Sz.

Let t=Sy' and q=R'. At this slice

    Kxx=Kyy=H, Kzz=H-q, Kyz=Kzy=-t/2,
    Xy=-H0 w-R w',   Z_hat=Z_dot-R Z'.

The calculation keeps arbitrary proper Xz until AFTER differentiating the
complete density, then evaluates Xz=0. Its momentum is not zero merely
because that velocity is zero. It generates part of the local lapse flux.
All four frame invariants, acceleration/regulator, force/cusp, alignment,
Cartesian and potential terms are retained. Dust/unit reductions inherit
their independent variations; no pre-variation T=t deletion is made.

The exported density is untruncated in w and gamma=sqrt(1+w^2). The intrinsic
curvature is zero on this chosen initial slice, not removed from the parent
action. This slice is neither arbitrary three-dimensional initial data nor
an automatically adopted nonlinear continuation of the old perturbative jet.

## 2. Exact transverse constraint

Writing L_t=partial L/partial t, the original shift variation gives
Cy=partial_z L_t. Choose the zero first integral that agrees with the
registered reflection sector. The solution is

    Sy' = -MU2 [c1+c3+2c3 w^2] w'/(gamma D_T),
    D_T = MP2-MU2[c1+c3+2c3 w^2-2c4(1+w^2)w^2].

Its coefficient is even in w, so its primitive can be taken odd in w.
This fixes the zero-mean periodic representative and makes Sy vanish at
the leading profile nodes. Other integration constants/sectors are not
declared solved or excluded. At leading order,

    Sy = -MU2(c1+c3)/(MP2-MU2(c1+c3)) * e cos(kz) + O(e^3).

The longitudinal shift is NOT set to zero in deriving this relation.
The x-momentum equation vanishes by the declared slice/reflection symmetry,
not by a claim about the arbitrary-3D theory.

## 3. Exact longitudinal constraint

After the stationary transverse reduction, define s0=c1+c2+c3 and

    P = MU2*s0*(1+w^2),
    T(w) = c4+[c1-(c2+c3)w^2]/(1+w^2),
    W = -MU2[(c2+T)(w')^2+c2*w*w''].

The complete original Sz Euler equation becomes

    -(P R')' + W R = f,

where

    A0(w) = c1+2c2+c4+(c2-c3+c4)w^2,
    AH(w) = 3c1+5c2+c3+2c4+(2c1+4c2+2c4)w^2,
    f = MU2*w*w'/(1+w^2) * [H0*A0(w)-H*AH(w)]
        + b*p*(Z*w*w'+Z'*w^2).

This is not a specialization of a previously frozen B1 matrix. It is
differentiated from the original restricted density. The coefficient of
R R' in that density is -MU2*c2*w*w'; retaining its derivative is necessary
to obtain W. The source is affine in H,H0 and retains Z and Z'. It is
independent of phase velocity, radial velocity, potential, K_Q, A and Z_dot
on THIS homogeneous-force initial slice. Those quantities still enter the
lapse/charge equations; they are not discarded from the action or dynamics.

For even pi-periodic prescribed regulator data, f is odd and pi-periodic
in theta=kz. Work in that registered odd shift sector. Then R has zero
mean and R=0 at theta=pi/2 modulo pi. The general zero mode and other
parity sectors remain outside this result.

## 4. Explicit coercivity and boundary conditions

Freeze Emax=1/500, |e|<=Emax, and define

    Tmax = |c4|+|c1|+|c2+c3| Emax^2,
    kappa = s0-Emax^2(2|c2|+Tmax)/4.

For w=e cos(kz), |w'|<=k Emax and |w''|<=k^2 Emax, so

    P >= MU2*s0,
    |W| <= MU2*k^2 Emax^2(2|c2|+Tmax).

The odd pi-periodic sector has no constant Fourier component and its
smallest spatial frequency is 2k. Therefore

    ||R||_2 <= ||R'||_2/(2k),
    integral[P(R')^2+W R^2] >= MU2*kappa ||R'||_2^2.

Every registered family at eta=1/4,1/64,1/1024 has MU2>0 and kappa>0,
verified with exact rational arithmetic. A bounded source then has a unique
weak solution in this parity sector by the coercive bilinear form, with

    ||R'||_2 <= ||f||_2/(2k MU2*kappa).

The coefficients are smooth for finite w. Smooth prescribed source data
therefore give the corresponding smooth solution of this one-dimensional
uniformly elliptic equation. This is a CONSTRAINT result conditional on those
prescribed data, not nonlinear temporal well-posedness or an admitted full state.

The transverse denominator has the all-angle lower bound

    D_T >= MP2-MU2|c1+c3|
       -2MU2 Emax^2[|c3|+|c4|(1+Emax^2)] > 0

at all nine registered family/eta points. The exact lower bounds are exported
in controls.json. No uniform inverse at eta=0, full-family physical GO or
physical momentum/frequency cutoff is inferred from these inequalities.

## 5. Lapse and global charges: retained, not yet solved

Compute forward momenta from the complete proper-velocity density. On the
restricted velocity span the exact Legendre energy is

    E_rest = H L_H + q L_q + t L_t + Xy L_Xy + Xz L_Xz
             + p L_p + Z_hat L_Zhat + D L_D + r_dot L_rdot - L.

This is the full momentum contraction on the chosen slice: the omitted
velocity components have zero value, not assumed zero momentum. In particular
pVz=L_Xz must still be evaluated before restricting Xz. The initial lapse
constraint is

    E_rest + partial_z(gamma pVz) + epsilon = 0.

Both the energy and the nonzero local flux are exported. The flux cannot be
removed before pointwise density and positivity are established. Periodicity
removes it only from the integrated equation

    <epsilon> = -<E_rest>,  <E_rest>+rho0=0.

At C=a=1 the dust charge per coordinate volume is <epsilon>. The second
global charge requires the original phase relation

    Q=<Rc*D*(1-zeta Rc^2 w^2)>,
    D=d/(1-zeta Rc^2 e^2/2).

The local angular factor also needs 1-zeta Rc^2 e^2>0. This repeats the
existing charge relation as part of the new combined system, not as a new
charge-only completion claim. The original cusp remains in E_rest with
contribution -2A|p w|^3; its sign is checked. It cannot be Taylor-expanded
through a nonexistent ordinary third derivative at Y=0.

The mean H root with both global charges, its relation to the archived
volume counter, the full lapse-derived positive density and compatible
regulator completion remain UNRESOLVED. These are substantive equations and
bounds, not pending-review or label blockers. The full initial-data acceptance
in the contract is therefore NOT met.

## 6. Original-density and archival controls

162 off-shell comparisons evaluate the complete original four-coordinate
metric/vector density against the newly restricted expression at 80 digits.
They retain nonzero Sy,Sz, their gradients, frame gradient, regulator and
regulator gradient. All three families and eta values, both amplitude signs,
|e|=1/500,1/1000,1/2000 and the three frozen angles remain.
Largest normalized discrepancy: 3.689769280130683e-81, tolerance 1e-50.
These are controls on this initial slice, not arbitrary-3D closure tests.

Before consulting the archived shift, the exact action gives

    R2(theta) =
      H0(2c1+3c2+c3+c4) sin(2theta)/(8k(c1+c2+c3)).

It solves the order-e^2 longitudinal equation and vanishes at the leading
nodes. All 18 archived initial events (both Radau and DOP853) agree with this
expression at the frozen three angles. Largest normalized discrepancy is
2.193755699376649e-18, below the inherited 1e-10 tolerance.
No family is selected and no coefficient is inserted from the archive.
This bridge does not yet certify the other lower-order data or higher orders.

## Disposition, preservation and next work

All 222 checks pass; zero failed/unknown CHECK rows do not remove the explicit
missing initial-data acceptance items. Complete read-only replay freshly
recomputes four JSON payloads and preserves all eight payload/sidecar bytes,
sizes and mtimes. Eighteen source pins and 36 source/sidecar metadata records
are unchanged. Original run and replay both exit zero. Same-author independent
implementations are not independent peer review.

Next solve the mean expansion/dust-charge equation using the certified shift
problem, prove pointwise density positivity, complete regulator/node-compatible
data, and verify all local constraints with controlled errors. No new
initialization is adopted or evolved by this report. Even successful initial
admission would leave persistence, arbitrary-3D/rank-changing reduction,
physical Hessian/Cauchy/energy domain, nonlinear remainder, a physical validity
window, healthy GR and genuine matching inputs to establish.

R9-MT1-INITIAL-CONSTRAINT-V1 is DEFERRED, not cleared; inherit node/canonical/
constraint, original preparation, G3N5, generic-family and transitive review debt.
Provisional reuse is limited to this exact system and conditional shift result.
Stage1 original linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.

No vault mutation, manuscript/PDF/site edit, commit/push, publication,
submission, action/parent selection, provider dispatch or runtime/model change.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| Contract | 1f2585c61811c41e0524b88209ee2f0761bf2aa27d388d138a66e4725dca90bc |
| Executable | 6ba9c73d71d2ef9dd3fc59f34d5fe781d528d5636a29a85bed748290bda989ff |
| summary.json | 586fe456022419f65965750ecc3137cf74b6eafb84f3a4dec670f2f611f51b3f |
| formulas.json | beaf647957a18ddd14881333de29cebc9a567ffcc62a9b4d775153984a0add73 |
| controls.json | d555bce09a97537c67441e3541ba193793457917fbcef2d6791a17ce1138d0ac |
| independent.json | 6632ba424bc896aec5ddfaea8f183a726802b0f4dca4eba481e3e007473ff95a |

Executable: Analysis/MasterTests/test_01_r4c1_initial_constraint_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01.

    python -B Analysis/MasterTests/test_01_r4c1_initial_constraint_v1.py --replay Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01

New computations require new nonexistent output directories. Preserve frozen
sources, hashes, failures and sidecars. Only the mutable execution/review indexes
receive guarded append-only continuations and refreshed index digests.
