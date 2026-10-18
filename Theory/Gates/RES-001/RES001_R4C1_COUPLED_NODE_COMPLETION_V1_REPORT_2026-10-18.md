# R4C1 coupled mean/node equations: restricted completion certified

18 October 2026. Unchanged-action Stage 2. Local checks 104/104 PASS;
complete fresh read-only replay exact, exit zero. All nine registered cases
have a unique root of the stated restricted system. Full initial admission,
higher consistency and evolution remain OPEN. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding and boundary

The previous [node-acceleration report](RES001_R4C1_NODE_ACCELERATION_V2_REPORT_2026-10-18.md)
rejected the selected constant regulator coefficient U0, not every continuation
of the action. The present calculation solves for the mean expansion H AND a
regulator coefficient U together, with the longitudinal shift and local density
depending on both. It does not insert old H,R,rho into an isolated correction.

For every registered family at eta=1/4,1/64,1/1024 and the full continuous range
`|e|<=1/500`, the known constraints and the necessary scalar node condition have
the implicit construction below. Both global charges are retained, the exact
shift inverse has newly controlled errors, and local future dust is positive.
The result is initial-only on the specified planar reference slice. It is not
arbitrary-3D constraint closure, physical family GO or a nonlinear IVP theorem.

The action, diagnostic family coefficients and background recipe are unchanged.
In particular the inserted family value `K_Q=3*eta` is not a microscopic matching
derivation. Neither required identifying matching input is supplied.

## 1. Same initial sector, different higher-order regulator continuation

Retain all initial fields, frame velocity and charge prescriptions from the
[known initial-surface construction](RES001_R4C1_INITIAL_ADMISSION_V1_REPORT_2026-10-18.md),
with `w=e*cos(kz)`, `k=40`, `V_dot_y=-Hbg*w`, and rho0=1/5. Set

    alpha=e^2,  U0=Hbg*p+beta*rho0/K_Q,
    Z=U*w^2,  Z_dot=Ud0*w^2.

Ud0 remains the old action-derived quadratic velocity coefficient as an
EXPLICITLY UNPROVED higher-order velocity continuation. Its further compatibility
is not inferred from the present root. No new state is adopted or evolved.

The transverse shift uses the same exact first integral. R=Sz is the unique
solution of the same coercive longitudinal operator in the odd pi-periodic
sector. Its source retains the full H dependence and, for the present Z,

    b*p*(Z*w*w'+Z'*w^2)=3*b*p*U*w^3*w'.

The operator is independent of H and U; the source is affine in both.
The phase velocity remains `D_phase=d/(1-zeta*Rc^2*alpha/2)`, retaining its
global charge. Local density is still `rho=-E-partial_z(gamma*pVz)`, with the
complete forward-momentum energy and LOCAL lapse flux. Only the average flux
vanishes on the periodic slice.

## 2. Coupled equations and fixed brackets

Write J for that local flux, `K=K_Q`, and s^2=k^2*alpha at a profile node.
The mean equation and the exact necessary scalar node defect are

    F=<E>+rho0=0,
    G=(K+2b*k^2*alpha)U-K*Hbg*p-K*p*R'_node-beta*rho_node=0.

Use the derived combination B=G-beta*F, not a different physical equation.
Let `E=Ebase(H,D_phase)+alpha*Edelta`, with the exact cusp retained. Then

    B=K*(U-U0)+alpha*Dnode,
    Dnode=2b*U*k^2-K*p*(R'_node/alpha)
          -beta*(<Edelta>-Edelta_node-J_node/alpha).

The symbolic identity is checked from the full mean/local-density relation.
The constant base cancels only in this combination; the local flux, regulator
velocity, phase charge and inverse sensitivities are not deleted. Here Dnode
is a defect function, not the phase velocity D_phase.

The pre-execution brackets, unchanged after evaluation, are

    H in [49Hbg/50,51Hbg/50], U in [49U0/50,51U0/50].

Hbg is the controlled action/background value, not an observed Hubble parameter.
These are diagnostic initial-data brackets, not microscopic predictions.
At e=0, U labels the continued limiting system; the physical field Z vanishes
and does not identify U on the aligned stratum.

## 3. Controlled exact inverse and its H/U sensitivities

Reuse the frozen symbolic three-term approximation

    R_N=cos(theta)*sin(theta)*sum_{n=1}^3 alpha^n*p_n(cos^2(theta)).

Its full variable-coefficient residual, not an asymptotic proxy, is

    L R_N-f = cos(theta)*sin(theta)*N(alpha,x)/(1+alpha*x).

The exact residual starts at alpha^4. Recompute every coefficient enclosure
over the NEW H/U rectangle. No U0-only error bound is reused unchanged.
The exact same coercive operator controls derivatives with respect to H and U,
because the operator is independent of these parameters. Differentiating the
source and residual therefore supplies controlled exact inverse sensitivities.

For 0<alpha<=amax, each residual monomial obeys

    |residual|/alpha <= (1/2)*sum |c_nj|*amax^(n-1).

Use the fixed positive coercivity C0, Pmin, |W| upper bound and half-cell length
L<2/k to obtain, for the residual and EACH H/U differentiated residual,

    |delta R|/alpha <= L*r_scaled/(2*k*C0),
    |delta R'|/alpha <= L*(Wmax*Rerror_scaled+r_scaled)/Pmin.

Every scaled remainder is enclosed before taking a zero-amplitude limit.
There is no fixed absolute error divided by alpha near zero. Constants and
all three error pairs are exported per case in certificates.json.
The transverse denominator and positive angular/phase factors retain the same
registered-domain restrictions. No eta=0 inverse or GR endpoint is inferred.

## 4. Existence, uniqueness, density and correction bounds

For every case and the whole continuous amplitude interval, outward evaluation
proves the following over the fixed H/U rectangle:

    F(Hlo,U)>0, F(Hhi,U)<0 for all U,
    B(H,Ulo)<0, B(H,Uhi)>0 for all H,
    F_H<0,
    B_U-B_H*F_U/F_H>0,
    rho(z)>0 for all angles.

The H/U derivatives include the EXACT inverse sensitivities with their new
controlled remainders. The first two F signs and F_H give a unique continuous
H(U) curve. Along it, dB/dU equals the strictly positive expression above.
The B-face signs then give existence and uniqueness of the restricted joint
root. This is not merely a two-dimensional numerical root finder.

All nine cases succeed at the first frozen partition, 16 angular interval
boxes. The precision is mp.dps=110 for point/endpoint inspection and
mpmath.iv.dps=80 for outward enclosures. No bracket, amplitude, family,
tolerance or partition-sequence change is used.

At the coupled root `(U-U0)/alpha=-Dnode/K`. The following displayed enclosures
are rounded outward from saved binary endpoints; density floors are rounded
down. They hold throughout the registered amplitude range, not just at the
sampled numerical root:

| Family | eta | Enclosure of (U-U0)/e^2 | Density lower floor |
|---|---:|---:|---:|
| Archived G3 | 1/4 | [-16.145, -15.458] | 0.17154 |
| Archived G3 | 1/64 | [-0.63843, -0.61277] | 0.19081 |
| Archived G3 | 1/1024 | [-0.037966, -0.036448] | 0.1920008 |
| B1-frame | 1/4 | [-17.492, -16.825] | 0.17135 |
| B1-frame | 1/64 | [-0.64496, -0.61954] | 0.19080 |
| B1-frame | 1/1024 | [-0.038029, -0.036523] | 0.1920008 |
| Hierarchical | 1/4 | [-17.064, -16.401] | 0.17140 |
| Hierarchical | 1/64 | [-0.64483, -0.61942] | 0.19080 |
| Hierarchical | 1/1024 | [-0.038029, -0.036523] | 0.1920008 |

Thus U<U0 for each nonzero amplitude in this construction. Globally across the
cases a conservative bound is `|U-U0|<17.492*e^2`. Consequently

    |Z-Z_old|<17.492*e^4*cos^2(theta).

This is a controlled quartic change of the regulator INITIAL FIELD, not a
nonlinear evolution remainder or a claim that all other initial fields have
that order. It leaves the previous rejection of exactly U0 intact. The zero
limit describes the continued equations, not identification of a new constant.
All quantities here are diagnostic reference-unit values.

In the frozen dimensionless-psi chart, [K]=2, [U]=2, [H]=[p]=[k]=1,
[e]=[b]=[beta]=0, [rho]=4 and [R']=1. F, G, B and Dnode have mass dimension
four; the regulator correction coefficient and Z have dimension two. Every
expanded equation term is checked with these dimensions.

The proof is conditional on the pinned exact equations, sector choices and
correctness of the interval implementation; it is not formal verification of
that library or independent peer review.

## 5. Separate numerical controls

At |e|=1/500, all nine high-precision APPROXIMATE coupled roots converge in
five Newton evaluations using the analytic coupled Jacobian. Their largest
recorded residual is below 7.825e-76 against the frozen 1e-60 criterion.
Their approximately 0.194%-0.223% decreases of U are point diagnostics, not
the continuous-domain proof or a physical observable.

The point calculation uses 64 periodic quadrature nodes only for the analytic
energy; the mean of the nonanalytic cusp is included exactly as
`<|cos(theta)|^3>=4/(3*pi)`. It is not silently approximated by analytic
quadrature. Polynomial inverse truncation errors are not certified away by
these tiny numerical root residuals; the interval proof supplies the exact
restricted existence and remainder control.

Independently assembled original-action odd-sector Galerkin systems at eight
and twelve harmonics retain variable P,W and the H/U-dependent source.
Their normalized field/gradient discrepancies at the frozen angles are below
8.630e-54, passing the frozen 1e-30 criterion. Comparison with the polynomial
approximation is also exported. These mesh/quadrature controls do not certify
the Galerkin error or replace the residual/coercivity proof. They are
same-author independent implementations, not an independent review panel.

## Preservation, next use and unchanged gates

All 104 local checks pass, with zero failed/unknown rows. Complete fresh
read-only replay recomputes all four JSON payloads and preserves all eight
payload/sidecar bytes, sizes and mtimes. The 29 source pins and 58 source/sidecar
metadata records are preserved. Original run and replay both exit zero, with
separate byte-equality and metadata guards.

All old sources, failed attempts, certificates, archives and sidecars remain
unchanged. In particular NODE-ACCELERATION-V2 still rejects the old U0
continuation, while INITIAL-ADMISSION-V1 still certifies its stated known
constraint surface. The new conditional completion is a distinct construction,
not a relabelling or replacement of either result.

Next test the retained regulator velocity and higher node time-consistency,
then persistence and the full rank-changing constrained acceleration system.
The current pair does not prove simultaneous satisfaction of every temporal
field equation. No corrected data are adopted/evolved by this report.
Physical constrained Hessian, Cauchy/energy domain, nonlinear remainder,
nonempty physical momentum/frequency window and healthy GR remain unproved.
Earlier negative-energy, defective-mode and failed-proof findings are retained.

R9-MT1-COUPLED-NODE-COMPLETION-V1 remains DEFERRED, not cleared, inheriting
node-acceleration, initial-admission, initial-constraint, node/canonical/
preparation/generic-family and transitive review debt. Provisional reuse is
limited to this implicit construction and its stated bounds.

Stage1 original bounded linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE. Both identifying
matter-residue and nonlinear-force matching inputs remain absent.

No vault mutation, manuscript/PDF/site edit, commit/push, publication/submission,
new parent/action, provider dispatch or model/runtime change is included.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| Contract | b63c9f3106d5b86c080a63c30b6fdb8ff188bdc08069c286b97d95b52966381a |
| Executable | 6fe275eed4aef446978809f12225af8aac16a546bddada8709d5a0ace9911a88 |
| summary.json | e66ac815aada3fa577db841cc99d55f095115dc203956426a9606fc9ba41ac8e |
| formulas.json | 3a8149e4667b79084d2c4c681ade164bde3ffd8f7a351a7128557a035a228095 |
| certificates.json | e02cef26c9776f1c4df2b827995ddf2e887038fad886be5f3034bc5133a17cce |
| independent.json | 3fd32bd7cf07408c0e0a0c62e2ea0348e2f10079d91f59620425feac78eb6eca |

Executable: Analysis/MasterTests/test_01_r4c1_coupled_node_completion_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01.

    python -B Analysis/MasterTests/test_01_r4c1_coupled_node_completion_v1.py --replay Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01

New calculations require fresh nonexistent output directories. Only mutable
execution/review indexes receive guarded appends and refreshed index digests.
