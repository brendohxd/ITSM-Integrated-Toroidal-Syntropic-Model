# R4C1 finite tilt: canonical constraints supplied, physical reduction open

17 October 2026. Master Test 1 / unchanged-action Stage 2.
Conditional calculation: 204/204 canonical checks and 397/397 independent
backend-bridge checks; both complete fresh read-only replays exact, exit0.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## What this resolves

The finite-tilt canonical lapse and shift functionals are now derived from
the original action, including the lapse-gradient contribution from the
frame momentum. The complete metric/frame/Cartesian Legendre complement,
force/regulator mixing, spatial curvature, potential and matter sectors
are retained. The fast implementation agrees with the original density;
its planar constraint brackets also agree with the expected deformation
relations in the registered controls.

This removes the missing-FORMULA part of the previous checkpoint's lapse/
shift dependency. It does NOT prove the full constraint reduction or algebra
on arbitrary three-dimensional data, construct an admitted prepared state,
classify a physical ghost, establish a Cauchy/energy domain, or clear Stage 2.

## Full ADM decomposition, before clock gauge

Use unit ADM normal ell, positive spatial metric h, lapse N>0 and shift S.
Write n=gamma ell+V with contravariant spatial V and
gamma=sqrt(1+h_ij V^i V^j). After the earlier INDEPENDENT unit variation,
the future unit branch can be reduced to nu=0; its normal equation determines
LambdaU. No normal equation is replaced by a pre-variation constraint.

The canonical one-form remains canonical on this reduction: p_nu dnu=0,
p_Lambda dLambda=0. The later dust reduction has p_epsilon depsilon=0.
The remaining metric/frame momenta already include their coupled contributions.

Define, in all three spatial directions,

    K_ij=(h_dot_ij-L_S h_ij)/(2N),
    phi_hat=(phi_dot-S^i partial_i phi)/N,
    X^i=(V_dot^i-L_S V^i)/N+gamma D^i ln N.

Direct expansion of the original four-dimensional metric/vector connection
gives B_A^B=(nabla_A n)^B in the normal/spatial basis:

    B_0^0=V_i(X^i+K^i_j V^j)/gamma,
    B_0^j=X^j+K^j_k V^k,
    B_i^0=D_i gamma+K_ij V^j,
    B_i^j=D_i V^j+gamma K_i^j.

All 16 identities are checked exactly with arbitrary lapse/shift/metric/
vector first jets at a point. The orthonormal point basis does not set the
frame tilt, spatial jets or lapse/shift derivatives to zero. The expressions
are tensorial; independent general positive h, nonzero shift/lapse and
all-direction first-jet controls check the coordinate implementation.

Thus the FULL density has form N sqrt(h) L0(K,X,phi_hat;configuration,
spatial jets,R3). It retains all four frame invariants, the temporal force,
-A Y^(3/2), alignment, Cartesian kinetics, full potential/portal, dust and
ALL regulator terms, including -b Z acc(n).grad psi. Spatial Ricci is not
deleted merely because it has no temporal Hessian.

## Explicit coupled Legendre inverse

On the regular future unit branch order the complement as

    y=(Kxx,Kxy,Kxz,Kyy,Kyz,Kzz, Xx,Xy,Xz, u_hat,v_hat,r_hat).

At fixed psi_hat and configuration the original density is exactly

    L0_without_dust = y^T R y/2 + ell(psi_hat)^T y + f(psi_hat)
                     + Z_hat g_Z(psi_hat),
    g_Z=-b[V^2 psi_hat+gamma V^i D_i psi].

R and ell are the complete action coefficients, not a frozen-metric or
specialized B1 kernel. The executable constructs their full tensor blocks;
independent quadratic polarization of the original density checks them.
f retains spatial curvature, all spatial interactions, potential and cusp.

Let volume=sqrt(det h), P_psi=p_psi/volume, P_Z=p_Z/volume and

    P_y=(2 p_hxx,2 p_hxy,2 p_hxz,2 p_hyy,2 p_hyz,2 p_hzz,
         p_Vx,p_Vy,p_Vz,p_u,p_v,p_r)/volume.

Here six-component p_hxy=2*pi^(xy); this convention avoids losing the
off-diagonal factor. The actual inverse is

    psi_hat= -[P_Z/b+gamma V^i D_i psi]/V^2,
    y=R^-1(P_y-ell),
    Z_hat= -[P_psi-(partial_psi_hat ell)^T y-partial_psi_hat f]/(b V^2),
    E_rest=volume[(P_y-ell)^T R^-1(P_y-ell)/2+P_psi psi_hat-f].

The Z_hat term cancels by its OWN momentum equation, not by deleting the
regulator or setting its momentum to zero. No inversion is valid at V^2=0,
b=0, det R=0 or a singular unit/dust branch. No interval-wide regularity or
uniform alignment/eta=0 limit is inferred from the arithmetic controls.

The positive future dust branch is eliminated after its own variation,
giving E_dust=p_T sqrt(C(psi)^2+h^(ij)D_i T D_j T), with p_T>0. This C(psi)
is the original matter conformal factor, not an acceleration coefficient.
No T=t gauge is used; comoving normalization remains N=T_dot/C.

## Actual lapse and shift constraints

Since each proper velocity scales as 1/N and X absorbs D_i N/N,
the actual density's chain rule gives

    partial L_density/partial N = -(E_rest+E_dust),
    partial L_density/partial(partial_i N)=gamma p_V^i.

First use the unreduced dust energy in this chain rule; substituting its
separately derived density constraint gives E_dust above. That stationary
elimination preserves the lapse equation; it is not a clock-gauge deletion.

Therefore the complete lapse Euler derivative is -H_perp, where

    H_perp=E_rest+E_dust+partial_i(gamma p_V^i),
    p_V^i=h^(ij)p_Vj.

The flux is a vector DENSITY. Its divergence integrates to zero on T3, but
it cannot be deleted from the local constraint or the lapse-smeared generator:
integral N partial_i(gamma p_V^i)=-integral (partial_i N)gamma p_V^i.

The proven ADM dependence similarly gives
delta_S L_density=-pi^(ij)L_deltaS h_ij-p_Vi L_deltaS V^i
                  -sum_scalar p_s deltaS^i D_i phi_s.
The exact undifferentiated and gradient coefficients are checked before
periodic integration by parts, yielding Euler_shift_i=-C_i, with

    C_i=-2partial_j(h_ik pi^(jk))+pi^(jk)partial_i h_jk
         +p_Vj partial_i V^j+partial_j(p_Vi V^j)
         +sum_s p_s partial_i phi_s.

The scalar sum is u,v,r,psi,Z,T after the stated unit/dust reduction.
This is not obtained by inserting a generic Lie generator in place of the
action: its applicability follows from the full connection/density derivation.
The unspecialized formulas retain the mean and harmonic obligations. Neither
pointwise constraints nor their global charge/mean conditions have been
solved on the registered finite-amplitude prepared data by this calculation.

## Independent checks and actual scope

The 204 checks include exact all-direction connection identities, shift-
variation coefficients, general-coordinate density tests, complete coupled
inverse/energy tests, positive dust elimination and all three families.
The 80-digit density controls use eta=1/4,1/64,1/1024. Largest normalized
coordinate-density discrepancy is 2.635549485807631e-82; tensor discrepancy
1.3177747429038154e-82; full complement velocity-inverse error
6.588873714519077e-83, against the frozen1e-50 controls.

The numerical bracket tests use all15 remaining canonical pairs, full
metric/vector components, actual R3[h], full potentials/C(psi) and both
transverse/longitudinal fields. The fields depend periodically on z; all
three momentum components remain. There are 12 action cases (three families,
eta=1/4,1/64, grids17/25) and two independent GR+scalar/dust controls.

| Bracket | Largest GR residual | Largest action residual |
|---|---:|---:|
| D-D | 6.335806445462167e-19 | 7.555533889508359e-19 |
| D-H | 5.2808269096569355e-18 | 1.6183729127595883e-17 |
| H-H | 1.1258355359089478e-15 | 2.7569092841961407e-15 |

These normalized residuals are below the frozen1e-7 tolerance. Maximum
complex-step-size discrepancy is 9.707512571566213e-15 against1e-9.
Both grids and every case are retained; no monotonic convergence law or
arbitrary3D closure theorem is asserted from these finite tests.

The separate397/397 bridge compares the fast backend to 80-digit original-
density polarization and momenta at18 general first-jet controls. It checks
all144 complement entries,12 affine entries,12 solved velocities, psi_hat,
total energy including eliminated dust, lapse flux and ALL15 momentum
derivatives. Maximum binary64 discrepancy is 2.1926904736346842e-14 against
the separately frozen1e-10 tolerance. Thus the numerical bracket calculation
is tied to THIS action, rather than merely to some covariant Hamiltonian.
These same-author independent implementations are not independent peer review.

## Preserved failure and immutable replay

V1 completed203/204 and remains FAILED. Its sole failed row compared an
unexpanded post-substitution polynomial with literal0. Exact expansion and
factorization each give zero. The [normal-form addendum](RES001_R4C1_FINITE_TILT_CANONICAL_V2_NORMAL_FORM_ADDENDUM_2026-10-17.md)
freezes V2's assertion correction; no action, numerical function or tolerance
changes. Source-AST comparison confirms all numerical/action functions are
identical. No failed row is deleted or automatically made successful.

V2 freshly recomputes the full calculation and passes204/204. All16 non-
summary JSON payloads are byte-identical to V1's corresponding payloads;
V1's failed summary is not overwritten. The separate backend audit passes
397/397. Both fresh replays recompute everything and compare exact bytes and
mtime/size:34 original main files and2 original audit files remain unchanged.
Main14 source pins/28 metadata records and audit16 pins/32 metadata records
are retained; the larger counts include frozen failure/addendum provenance.

## Remaining physics and next work

The next dependency is an actual arbitrary3D constraint-algebra/reduction
proof and constraint-admissible finite-amplitude initial data, not another
raw-rank or planar-grid sweep. In particular the registered transverse wave
has alignment/profile-zero strata not covered by this regular inverse.
Do not divide by its vanishing V^2 or assume those strata are harmless.

Admissible Cauchy/characteristic and physical energy domains, the physical
reduced Hessian, controlled nonlinear remainder, nonempty physical window
and justified GR recovery remain necessary. No extra propagating-mode count,
physical ghost/healthy classification or family GO is established here.
Genuine identifying matter-residue and nonlinear-force matching inputs remain
absent. Stage3 is NOT_ENTERED; no numerical C_chi/a0 prediction is sealed.

R9-MT1-FINITE-TILT-CANONICAL-V2: DEFERRED, not cleared. Provisional reuse is
limited to these regular-branch canonical formulas and bounded controls.
Inherit FINITE-TILT-CONSTRAINT-V1, G3N5 off-shell/kernel, G3N2, generic-family
and all transitive review debt. Scientific missing inputs still block uses
beyond that scope; pending Rule-9 review alone does not block research.

Stage1 complete only in registered linear prepared-dust scope; Stage2
INCOMPLETE; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No vault, manuscript/PDF/site, commit/push, publication/submission, provider/
model/runtime or action change. Unrelated working paper edits are untouched.

## Frozen sources and receipts

| Artifact | SHA-256 |
|---|---|
| V1 contract | c2c0c054867f4b11cbfafa5a20b792a6c8592f57ebbb737c28f7dd55ce99cade |
| V1 executable | 1ce336217fd71267a7af5b5f08b8c89c1899321c7eb2641e3827b3ab43f2c115 |
| V1 failed summary | e13647178a72afa39c80488a6c50bf1c4569bc186b03134c79e343fea20de027 |
| V2 normal-form addendum | 167e540c28d0722620f28dfa84ab9a47dfc93dee95073b7df68de975210ea8dc |
| V2 executable | 4c2a64f45741161ccacdb75bd0816e5113a9d0b95ba2aa402584f2cb8533dada |
| V2 summary | ba203bf4c29ddf7834c5db2c2a7a98625343508ed3f24025a56b90438020d44b |
| V2 formulas | 42474290257ef61f1f8328b401a210622b07576ded035f80eb5fb66dde51fe99 |
| V2 independent controls | c9e1225df72a339babb4a46f737c5b501a556128983bdc3014bec93ac7be5151 |
| Backend addendum | 709837f95506893169451cdf3f0352b91af2c6662c27119798ff513cda004846 |
| Backend executable | 9bbccd7dfddef6ffc5e499c19d485a79a6f1d8326d2c02a5462b57b2e932c7cb |
| Backend verification | 97d4ca6c7dbe6a7af27e21529d40532944cffb8f5d92f9781a52708b3391557a |

Main: `Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_attempt_02/`.
Audit: `Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_backend_attempt_01/`.

    python -B Analysis/MasterTests/test_01_r4c1_finite_tilt_canonical_v2.py --replay Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_attempt_02
    python -B Analysis/MasterTests/audit_01_r4c1_finite_tilt_canonical_backend_v1.py --replay Analysis/MasterTests/outputs/r4c1_finite_tilt_canonical_backend_attempt_01

New calculations require NEW nonexistent output directories. This checkpoint
does not re-run or revise the completed dust, cubic-tail or243/243 velocity
audit. Only the mutable research/review indexes receive guarded append-only
entries and new index digests; original evidence and failures remain intact.
