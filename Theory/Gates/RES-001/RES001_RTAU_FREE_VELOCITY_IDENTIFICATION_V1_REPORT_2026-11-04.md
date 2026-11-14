# Actual free-velocity coefficient identification

4 November 2026. Component of the acknowledged-High actual-rate bundle,
after the [paired gauge map](RES001_RTAU_PAIRED_GAUGE_RATE_V2_REPORT_2026-11-04.md).
R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE;
original R4C1 and G1-G6 unchanged and incomplete.

## What is established

The pointwise leading free-velocity coefficients obtained from the full
canonical inverse and actual spatial-gauge projector agree with the
shift-gradient Schur reduction of the same action. The momentum and
configuration-gradient coefficient maps are both identified. This connects
the canonical/gauge construction to the coefficient source used by the
registered ordinary principal operator; it is not a new fitted kinetic
matrix or an assumed similarity transformation.

The strong-state insertion, coordinate/time transport and complete bounded
velocity remainder still require assembly. No conclusion about the full
generator, physical evolution or interactions follows from this coefficient
identity alone.

## General coefficient proof

Use the thirteen nonauxiliary field slots. E embeds free slots
(0,1,3,6,7,8,9,10,11,12); W selects gauge slots (2,4,5). Let B be the
actual spatial field generator at the conformal initial slice. Then

    G=W*B=diag(a^2,a^2,2*a^2),
    Pi=I-B*G^-1*W, Pi*B=0, Pi*E=E.

Here B's three frame entries are -Vz. Thus the leading canonical momentum
constraint B^T*p=0 has the unique lift

    p=Pi^T*E*P_free.

Its eliminated rows are precisely the leading frame-momentum lift proved
in the previous owner; the field-dependent-generator and source terms
remain in that owner's H1 remainder. Gauge-fixed metric gradients have
zero leading rows in these three slots, while their smooth physical modulus
partners remain in the full reconstruction.

Let A=L_vv and D=L_vd be the full action's pointwise kinetic and mixed
coefficients. The shift-gradient dependence through v-Lie_S q gives

    L_vSz=-A*B, L_SzSz=B^T*A*B=K,
    L_Szd=-B^T*D.

These identities follow by differentiating that action dependence at fixed
q; they are not inferred from interval overlap. The inherited certified
temporal and shift inverses justify the algebra throughout the initial
root domain. Put

    M=E^T*(A-A*B*K^-1*B^T*A)*E,
    C=E^T*(D-A*B*K^-1*B^T*D)*E.

Use the invertible basis U=[E,B]. The upper rows of U^-1 are E^T*Pi.
The upper-left block of (U^T*A*U)^-1 is both the inverse of the Schur
complement M and E^T*Pi*A^-1*Pi^T*E. Therefore

    E^T*Pi*A^-1*Pi^T*E=M^-1.

For the mixed coefficient, set H=D-A*B*K^-1*B^T*D. It obeys B^T*H=0,
so H*E=Pi^T*E*(E^T*H*E). Since Pi*A^-1*A*B=0,

    E^T*Pi*A^-1*D*E=M^-1*C.

This proves both canonical/gauge free-velocity coefficient identities for
the full ten-slot free block. It does not require a positive full canonical
Hamiltonian or a new background ansatz. The original nine ordinary slots
are the first nine free slots; force slot 12 remains the tenth. The action's
exact temporal ordinary/force and force/shift-gradient zero blocks are
retained, not introduced as a new physical restriction.

Subtracting common material advection in the original coordinate replaces
C by C+S^z*M. Thus M^-1*(C+S^z*M)=M^-1*C+S^z*I, reproducing the declared
material mixed-coefficient convention. Actual coordinate drift and finite-
rank/global terms remain part of the pending full rate comparison; they
are not discarded by this pointwise algebra.

## Evidence and next calculation

[Executable](../../../Analysis/MasterTests/test_rtau_free_velocity_identification_v1.py),
[frozen criteria](RES001_RTAU_FREE_VELOCITY_IDENTIFICATION_V1_SPEC_2026-11-04.md),
[receipt](../../../Analysis/MasterTests/outputs/rtau_free_velocity_identification_v1_20261104/receipt.json).
14/14 bounded controls and byte-identical replay COMPLETE. Independent exact
rational controls use noncommuting, genuinely coupled blocks and check both
coefficient identities, the canonical covector constraint and basis proof.
Those fixtures are algebra controls, not physical background selections.

The cached unspecialized Hessian supplies whole-root enclosures of the
actual ten-slot kinetic, mixed and material-mixed blocks. The inherited
certified shift inverse is used, without a midpoint substitution or new
Hessian. Covariance residual intervals contain zero; these are consistency
checks of the action identities, not standalone proofs that a residual is
identically zero. Scientific source bytes, sidecars and timestamps are
preserved. Controls remain same-author; Rule-9 review is DEFERRED.

NEXT: combine these identified coefficients with the strong configuration-
gradient and momentum remainder bounds, the exact paired gauge map and
actual coordinate drift. Bound the resulting ordinary velocity remainder
in the physical strong variables. The force row still needs its proper
mixed-order treatment; an H1 velocity estimate is insufficient for two
uncompensated derivatives in the auxiliary rate. Full momentum/force rows,
moving Green/range maps, T_dot/H_dot and a genuine background tube remain
OPEN. This coefficient identification is not full remainder acceptance.
Goal ACTIVE; High remains acknowledged for the unfinished actual-rate bundle.
No new matching input, action adoption, paper/site promotion, vault mutation,
model dispatch, Git delivery or publication occurred.
