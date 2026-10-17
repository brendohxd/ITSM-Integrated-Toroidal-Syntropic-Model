# R4C1: three-family homogeneous fixed-charge kinetic comparison

16 October 2026. Master Test 1 / RES-001 / approved unchanged-action Stage 2.
Claim: Conditional. Local validation: 1470/1470; exact read-only replay passed.
Execution: PROCEED_PROVISIONALLY_WITHIN_HOMOGENEOUS_ENSEMBLE_SCOPE.
Review: DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and meaning

The completed 11 October B1 result extends to all three registered diagnostic
families on the stated regular background domain. Fixing both the internal
U(1) charge and global dust charge, with their global origins reduced, gives
a positive homogeneous quadratic momentum/kinetic block. With U(1) charge
fixed but dust charge allowed to vary, the larger homogeneous sector retains
one negative direction. These are different ensembles.

The generic unspecialized 22-field action supplies the new comparison; no
new-family coefficients were inserted into a B1-specialized matrix. The
evolving polar basis, nonlinear boundary generator and local constraint rows
were retained. An independent homogeneous Legendre calculation and finite
square-root-Hamiltonian controls agree with the kinetic reduction.

This settles the bounded homogeneous ensemble/sign question. It does not
admit the archived forced wave to a complete nonlinear fixed-charge phase
space, prove its full energy positive, or provide a physical frequency window.
The previous fixed-charge retarded V3 timing warning remains authoritative.

## Scope and assumptions

- Exactly homogeneous k=0 comparator about an aligned isotropic background.
  The separately archived k=40 wave responses are unchanged.
- Three diagnostic families, 0<eta<=1/4, with the full previously registered
  coefficient/scalar/background scalings. These maps are diagnostic choices.
- a,C,R,rho,M_cos2,M_T2,f2,K>0; positive force-clock branch psi_dot>0;
  regular density/normal/regulator constraints. The polar chart requires R>0.
- The force scalar psi is distinct from the complex internal phase.
- Coordinate-cell volume v=a^3. Integrated global charges multiply by (2*pi)^3.
  All numerical matrix values use the registered reference units and basis.
- Angular Routh coefficient v*R^2*(1-zeta*R^2*boost_squared)/N must be nonzero.
  This calculation expands at boost=0; it proves no arbitrary finite-boost domain.

eta=0 is excluded: frame and force-scalar kinetic coefficients vanish and
the clock/constraint reductions can become singular. Positive matrices at
eta>0 do not establish uniform control or healthy GR recovery at the endpoint.

## Generic calculation from the action

The compiler extracts the value, mixed and velocity blocks of all 22 generic
fields before any family substitution. It verifies the lapse primary, density
equation alpha=T_dot/C-beta*Pi, unit equation nu=0, homogeneous shift rows,
and regulator equation b*Z=0. The unreduced normal velocity block is

```text
[[-2*M/3, -MU2*c2],
 [-MU2*c2, -MU2*(c1+c2+c3+c4)]],

M = M_cos2 = MP2+MU2*(c1+3*c2+c3)/2.
```

Its determinant and hnu=-2*M/(3*v*det_normal) are retained. The density-chain
factor is hEm=v*C^8/rho. Their regularity, together with the declared domains,
is checked before the force-psi clock and cyclic reductions.

Cartesian background differentiation precedes the instantaneous polar section.
The nonlinear polar boundary generator is included in both value and mixed
blocks. Cyclic-angle and cyclic-dust-origin identities hold on the declared
background constraint. The polar canonical one-form is checked directly.
The angular Routh term remains

```text
-N*Q^2/[2*v*R^2*(1-zeta*R^2*boost_squared)],
```

including its quadratic boost contribution -N*zeta*Q^2*boost_squared/(2*v).

Define M=M_cos2, Tm=M_T2 and K as the diagnostic force-scalar coefficient;
these are not a new numerical identification of canonical K_Q. Write

```text
U = V_potential + rho + Q^2/(2*v^2*R^2),
G = diag(-2*M/3,1,1,Tm/4 [five shears],f2 [three frame modes]),
bvec = (2*M*H,-Rdot,-rdot,0,...,0)^T.
```

U is an energy density, distinct from the unresolved canonical matching V.
On the background constraint 6*M*H^2=Rdot^2+rdot^2+K*psi_dot^2+2*U,

```text
K_variable_dust = [[G,bvec/C],[(bvec/C)^T,-2*U/C^2]],
K_fixed_both = G+bvec*bvec^T/(2*U).
```

An exact Schur congruence relates the first matrix to
diag(K_fixed_both,-2*U/C^2). The fixed-both (x=ln(v),R,r) leading minors are

```text
D1 = M*(Rdot^2+rdot^2+K*psi_dot^2)/(3*U),
D2 = M*(rdot^2+K*psi_dot^2)/(3*U),
D3 = M*K*psi_dot^2/(3*U).
```

These are strictly positive on the stated domain; the eight remaining
diagonal kinetic directions are positive separately. The variable-dust
sector therefore has inertia (11 positive,1 negative), while fixed-both has
11 positive directions. The additional charge/origin quotient changes the
number of canonical pairs from 12 to 11. It does not change the old ensemble.

The family coefficients and normal determinants are proved regular on
0<eta<=1/4 by exact polynomial sign checks, including the upper endpoint.

| Family | M_cos2 | M_T2 | f2 | Diagnostic K |
| --- | --- | --- | --- | --- |
| G3 | 1-eta/12 | 1-eta/8 | eta/6 | 3*eta |
| B1-frame | 1+eta/10 | 1 | eta/6 | 3*eta |
| Hierarchical | 1+eta/10+eta^2/16 | 1-eta^2/8 | eta/6 | 3*eta |

## Independent Hamiltonian and numerical controls

The lapse-unfixed homogeneous Legendre calculation includes all eleven
remaining metric/radial/reservoir/shear/frame velocities, the force scalar
and the positive-density dust branch. Direct differentiation of the full
positive-clock square-root Hamiltonian gives

```text
B = diag(3/(4*M*v),-1/(2*v),-1/(2*v),
         -2/(Tm*v) [five],-1/(2*f2*v) [three]),
p_background = (-2*M*v*H,v*Rdot,v*rdot,0,...,0)^T,
Hpp = -2*B+4*(B*p_background)*(B*p_background)^T/(K*v*psi_dot^2)
    = inverse(K_fixed_both)/v.
```

The mixed volume/dust-momentum Hessian remains negative in determinant when
dust charge varies. Pure Einstein-dust also has homogeneous dust-clock
volume-momentum curvature -3/(2*M_P_squared*v). The mean sign alone therefore
does not identify a local propagating ghost.

All 378 archived nodes were used unchanged: 18 runs, two methods, three
families, three eta values, 21 saved times each. Calculation used 80 decimal
digits; it did not replace the stored H or solve a new background. The raw
matrix uses W=3*M*H^2-(Rdot^2+rdot^2+K*psi_dot^2)/2. With D=W-U, the exact
raw/shell difference is -D*bvec*bvec^T/(2*U*W). This accounts for archived
constraint residuals rather than silently projecting them away.

| Control | Observed maximum or minimum |
| --- | --- |
| Smallest fixed-both kinetic eigenvalue, registered basis | 1.7504833566e-10 |
| Most negative variable-dust kinetic eigenvalue | -2.1081090244 |
| Normalized archived Friedmann residual | 7.1988769835e-16 |
| Friedmann residual relative to K*psi_dot^2 | 4.4247612766e-6 |
| Raw/shell matrix difference | 2.0707409185e-15 |
| Constraint-correction identity residual | 2.0350651957e-81 |
| Two-method normalized kinetic comparison | 7.1077044220e-16 |
| Independent finite full-Hessian comparison | 3.8779817175e-15 |

The last comparison used nine separately constructed exact-initial-recipe
controls, all 11 momenta and mixed derivatives, and both frozen step sizes.
Those controls are explicitly distinct from the untouched archived nodes.
All finite probes stayed on the positive-radicand branch. Ordinary eigenvalue
sizes depend on the reference basis/units; the sign inertia is invariant under
regular real congruence. No cutoff or physical sound speed follows from them.

The 1470 checks include many repeated node/grid controls, not 1470 independent
physical discoveries. The exact generic identities and independent controls
support this scope; the count alone supplies no gate clearance.

## Failed attempts and immutable provenance

Attempt 01 was interrupted before a receipt while locating slow algebra.
Attempt 02 reran unchanged V1 with a private stack log and located automatic
2x2 determinant simplification as the bottleneck. Neither is called a pass.
Both interruption records and the V1 source remain preserved.

V2 / attempt 03 completed 79/80 checks and correctly skipped numerics after
one inverse-Hessian check failed. All four residuals were explicit multiples
of the Friedmann constraint. The independent reducer handled H^2 but left
odd powers unreduced. V3 applies exact polynomial remainder reduction and
tests odd/even powers and a nonzero off-shell witness. The failed source and
receipts are untouched. In particular formulas.json has the SAME SHA-256 in
failed V2 and accepted V3: no physical formula was changed to obtain the pass.

V3 / attempt 04 completed 1470/1470 and reproduced all receipt/sidecar bytes
in an exact read-only replay. It verified 323 source pins and preserved
643 source/sidecar hash-size-mtime records; three historical absent sidecars
are explicitly inherited, not presented as newly verified files.

| Evidence | SHA-256 |
| --- | --- |
| V3 executable | 9fb9c72f36db0f87e1e47db010237ab1b3d3d5260c98e2ecd3bacd265dbffbd5 |
| Attempt04 summary.json | 9429ab897513fe5bbeda30242fa2bc535687378567eee388229450f1c963e898 |
| formulas.json, V2 and V3 | b20bb8b9894332d4617af9453ca866fff3eead995f6899b7f26c751aa5f852b5 |
| Attempt04 numerics.json | a492eb968a2f26551d3ce81949b1776d213a9bc44b638293c00f2d4ffc33750a |
| Attempt04 verification.json | 656f37fd8d55713371e92be211c0baaa45d7df9c53774e76c2f7ad4551947ed7 |

Executable: `Analysis/MasterTests/test_01_r4c1_three_family_fixed_charge_kinetic_v3.py`.
Receipts: `Analysis/MasterTests/outputs/r4c1_three_family_fixed_charge_kinetic_attempt_04/`.
Reproduce with the existing itsm_env Python and `--replay` pointing there.
The scope contract and all three addenda are pinned in the summary manifest.

## Deferred review, limits and next permitted step

ID R9-MT1-THREE-FAMILY-FIXED-CHARGE-KINETIC-V3. Review DEFERRED, not cleared.
Inherit B1 MEAN-MODE-ENERGY, THREE-FAMILY-CHARGE-DOMAIN V5,
FIXED-CHARGE-RETARDED V3, PLANAR-WWR, GR-FAMILY-SURVEY and transitive debt.
Continuity packet ctx_d3efffe135fd983f5eb7422a located the existing contract
and working note (doc_b57336cc510edc1e849eab34,
doc_6cca64599fdf21fee748693c); live files and hashes govern this result.

Substantive blockers within the stated conditional homogeneous kinetic
comparison: NONE_WITHIN_STATED_SCOPE, because the generic action/constraint
binding, cyclic reductions, exact sign/Hamiltonian identities, prescribed
numerical controls and replay all pass on the explicitly restricted domain.
This permits provisional reuse of this comparison only.

The full potential and momentum-coordinate mixing, inhomogeneous scalar/
vector/tensor characteristics including quartic dispersion, complete nonlinear
fixed-charge admission of the forced state, physical interaction/window and
error control, tensor/local-gravity/healthy-GR tests remain substantive.
The prior retarded timing warning is unchanged. A bounded finite-k constrained
energy/characteristic calculation is the next relevant research route; this
report does not authorize a full-model stability claim or a Stage-3 fit.

Stage 1 remains complete only in its previously registered linear B1 dust
scope. Stage 2 remains incomplete; no family receives physical GO. Stage 3
is not entered: matter-residue and nonlinear-force identifying inputs remain
missing. Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false.

The former Python startup failure is no longer reproduced in this session;
its cause is unassigned. No security configuration, dependency installation,
provider/model, manuscript/PDF, publication, commit or push was changed.
