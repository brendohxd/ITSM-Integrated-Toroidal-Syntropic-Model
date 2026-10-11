# G3N5 independent temporal-block control

Date: 9 October 2026. Version 1, frozen before execution.
Owner: the existing G3N5 response-kernel checkpoint, not a replacement route.
Conditional research; Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE.

## Scope and owning input

Derive the complete 22-by-22 pure time-velocity Hessian on the aligned isotropic
background independently of G3N5's truncated-jet implementation. This is a
control on a block of the unreduced three-direction operator, not a homogeneous
physical evolution, a solved constraint system, or a physical Hessian. Spatial
and mixed time/spatial blocks are not supplied by this control.

The frozen action is RES001_R4C1_ACTION_FREEZE_2026-09-25.md, SHA-256
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
G3N5 contract: 11cf25cef8cc0192f1f690dbf1f7fee2f9e0268eff508d7fb1a65709907f2c02.
Running G3N5 v1 source: 0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7.
Retain the G3N4 transitive pins, original failures, and three absent sidecars.

Use the same 22 fields and all three components of the boost and shift. At a
local point set response values and spatial first derivatives to zero, but keep
all 22 time derivatives independent. Rebuild g, its four-dimensional connection,
and independent U derivatives directly from the ADM time jet, before imposing
any multiplier equation. The background may be off shell. This operation
extracts the pure-velocity coefficient; it does not discard spatial terms from
the theory or select zero-mode initial data.

With N=1, h=a^2 I at the point, define a formal amplitude d:

```text
g_t00=-2d alpha_t; g_t0i=a d S_i,t;
g_tij=a^2(2H delta_ij+d M_ij,t);
U=(1,0,0,0);
partial_t U^0=d(nu_t-alpha_t);
partial_t U^i=d(V_i,t-S_i,t)/a.
```

No constrained normalization is imposed on nu_t. The tangent-unit condition
follows only when the multiplier equation and its time preservation are used.
Carry the full frame-normal/metric-trace kinetic mixing through the control.

## Required exact controls

1. Verify the connection's metric compatibility and the off-unit norm derivative.
2. Derive all four frame invariants from the direct connection and compare with
   their separate trace formulas. Include the ADM/GHY Einstein kinetic term,
   Cartesian kinetics, temporal force, and conformal dust kinetic term.
3. Extract and compare all 484 Hessian entries with the independently written
   quadratic form. Check all seven nondynamical velocity rows exactly, without
   interpreting the remaining raw rank as a physical degree-of-freedom count.
4. Verify the metric-trace/normal 2-by-2 determinant and exact generic and
   singular-boundary rank controls. No Schur inverse or physical-sign claim.
5. Reject omitting nu, omitting its trace mixing, dropping c4 from the boost
   kinetic term, reversing the Einstein sign, importing a projector trace into
   the metric coefficient, adding a lapse velocity, or using C^4 instead of C^2
   in the dust velocity coefficient.

## Independent numerical control frozen before execution

Rebuild the unexpanded four-dimensional point-density numerically, independently
of the symbolic block. Use 50-digit mpmath, two all-field velocity jets, and
d=1e-3,5e-4,2.5e-4. Because this point-density is exactly quadratic in d,
require every normalized centered-coefficient error <=1e-38.

The two rational coefficient sets are defined explicitly in the versioned
executable; MP2,MU2,K_Q,C,epsilon0 are positive. They are illustrative local
operator inputs, not action-derived microscopic values or physical solutions.

When the full G3N5 receipt exists, a separate comparison attempt must verify
its artifacts/sidecars and compare every time/time entry with this independent
matrix. Until then report FULL_KERNEL_COMPARISON_PENDING explicitly, even if
every independent temporal control passes. Do not equate that pass with the
G3N5 deliverable or constraint-compatible initial data.

## Preservation and inherited holds

New versioned executable/output only; refuse existing output paths. Replay
recomputes and compares bytes without writing. Any repair needs a new version;
no original executable, receipt, sidecar, action, threshold, or running process
is replaced. Private logs stay ignored.

Constraints/gauge reduction, compatible initial data, homogeneous sector,
unsmoothed forcing/harmonic tail, coupled response, general T3 nonlinear IVP,
physical stability, cutoff, continuous healthy GR, and C1/C2 findings remain
open/unchanged. The new block is not a substitute for any of these requirements.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No manuscript/PDF/vault change, provider dispatch, commit, push, promotion,
or publication is authorized by this control.
