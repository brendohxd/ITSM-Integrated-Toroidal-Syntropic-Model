# R4C1 finite-amplitude initial constraints: frozen V1 calculation

18 October 2026. Unchanged-action Stage 2, following REGULATOR-NODE-V1.
This contract precedes execution. The full objective is a constraint-admissible
finite-amplitude completion with the registered charges and lower-order data,
not merely another sample of the regular Legendre rank.

## Scope and construction to examine

Use the existing exact reference-unit initial recipe: a=N=C=1, flat spatial
metric, homogeneous scalar positions, u=r=sqrt(eta), v_cond=psi=T=0,
u_dot=0, r_dot=sqrt(eta)/4, psi_dot=eta/5, rho=1/5,
and the controlled positive H0 from the original background constraint.
Keep all three frozen family maps and eta=1/4,1/64,1/1024.
The leading frame is V=(0,e cos(kz),0), k=40, V_dot=(0,-H0 V_y,0).

Examine the existing initial-slice freedom, not a new parent action:
uniform metric expansion H, transverse and longitudinal shifts Sy(z),Sz(z),
the exact global-charge phase counter, and lapse-derived density. Higher
corrections are candidate data only; do not adopt or evolve them automatically.
They must reproduce the original first/quadratic preparation, with floating
archive residues kept distinct from the exact reference recipe.

Do not set Sz=0. Do not infer a full lapse equation from an energy expression
with the local divergence of gamma*pV omitted. Do not invert through V=0.
Use forward momenta from the full density and the separately varied future
unit and positive dust branches. Preserve the regulator field, velocity and
nodal compatibility requirements; their exact completion is part of acceptance.

## Required work

1. Recompute the full restricted density from the unspecialized ADM action,
   retaining arbitrary proper Xz before differentiating, all frame invariants,
   acceleration/regulator terms, phase alignment, cusp, potential and matter.
   Derive Cy,Cz and the local lapse functional, not a specialized B1 transplant.
   Distinguish a restricted shift variation from a full physical Hessian.
2. Derive the transverse first integral and the exact longitudinal variable-
   coefficient operator. Analyze periodic/parity boundary conditions, kernels
   and coercivity using explicit constants; treat the zero mode separately.
3. Retain both global charges. Reduce the mean lapse/dust-charge equation
   without discarding its local flux. A scalar mean root alone is not the
   complete initial constraint solve.
4. Construct and certify candidate data where possible: every local constraint,
   both global charges, node regularity, positive dust and a nonempty declared
   amplitude domain. Match registered lower-order phase, volume, shift and
   regulator data. State remaining free-data choices and nonuniqueness.
5. If only the exact equations/operator or numerical candidates are obtained,
   record PARTIAL and leave full initial-data acceptance OPEN. A collocation
   residual, implicit-function slogan or formal series alone is insufficient.

## Controls frozen before running

Symbolic identities are exact. Independent full original-density evaluations
use 80 digits and normalized 1e-50 tolerance. Binary64 archive comparisons use
normalized 1e-10. Diagnostic amplitudes are +/-1/500,+/-1/1000,+/-1/2000;
no physical cutoff is inferred. Keep all three families, all eta values and
both archived methods; do not tune the action, target or tolerance afterward.

Check off-shell periodic profiles as well as any solved candidate. Independently
test coordinate density versus the restricted tensor formula. Reject missing
longitudinal shift, lapse flux, spatial frame jets, acceleration, complete
momentum differentiation, local positivity or global mean/charge constraints.
An analytic parity/coercivity result is not a dynamical hyperbolicity result.

## Artifacts, preservation and acceptance

Executable: Analysis/MasterTests/test_01_r4c1_initial_constraint_v1.py.
Fresh directory: Analysis/MasterTests/outputs/r4c1_initial_constraint_attempt_01.
Export exact formulas, independent controls, archive comparisons and a summary
explicitly separating local validation from full initial-data acceptance.
Freeze exact source/sidecar hashes and metadata; reproduce receipts by complete
read-only replay. Keep all old failures and existing files unchanged.

Full acceptance requires the certified initial data described above; otherwise
the report must name the precise unsolved equations/bounds and retain an OPEN
disposition. Even full initial acceptance would not prove nonlinear evolution,
arbitrary-3D reduction, a physical Hessian/domain/window or healthy GR.

Stage1 remains complete only in its original linear prepared-dust scope;
Stage2 INCOMPLETE; Stage3 NOT_ENTERED and both identifying matching inputs absent.
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
R9-MT1-INITIAL-CONSTRAINT-V1 inherits node/canonical/constraint, original
preparation, G3N5, generic-family and all transitive review debt.

No new action/parent, manuscript/PDF/site edit, vault mutation, commit/push,
publication, submission, provider dispatch or model/runtime change is included.
