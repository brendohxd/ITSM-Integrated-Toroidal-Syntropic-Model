# R4C1 global nodal lift: initial coordinate flow agrees, full DAE still open

20 October 2026; calculation/contract work began19 October.
Conditional unchanged-action Stage2. Local1072/1072; full fresh eight-worker
read-only replay exact. Review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE.

## Result and scope

The undivided scalar-rate block is now integrated with the full global
planar spatial constraints, both fixed charges and all three mean metric
canonical pairs. It runs on the CURRENT joint initial construction with
exact profile nodes, not the earlier nodeless method controls.

For all9 existing family/eta cases, the resulting Hamiltonian reproduces
the specified INITIAL coordinate flow, including the scalar-rate/regulator
row and necessary node equations, within the frozen numerical tolerances.
All remaining metric, frame, radial, fluctuating phase/dust and mean-metric
directions are retained. This supports consistency of the initial lift.

It is NOT full initial admission or a time-evolved solution. Momentum
evolution, the complete node-constraint/tangency hierarchy, an admissible
physical function space, the descriptor Hessian/drift and spectrum, physical
window and healthy GR remain unverified. The negative patch form and
unweighted inverse obstruction are not removed or reclassified as healthy.

## Construction from the existing action and data

Reuse the archived joint H,U,Ud point controls, original Hbg input and all
three frozen diagnostic parameter maps at eta=1/4,1/64,1/1024. Here e=1/500,
k=40 only; no new continuous-amplitude or arbitrary-eta certificate follows.
These coefficients/reference recipes are not microscopic matching inputs.

The candidate slice is

~~~text
h=I, u=r=Rc, v=psi=T=0,
V=(0,w,0), w=e*cos(theta), theta=k*z,
Z=U*w^2, s=p=eta/5, coordinate Z_dot_t=Ud*w^2.
~~~

Ud is not Udot. The original8/12-mode Galerkin inverse supplies Rshift and
Rshiftprime; the original transverse first integral supplies Syprime.
No shifted-state root is solved or target coefficient fitted here.

Retain the original proper initial velocities

~~~text
Kxx=Kyy=H, Kzz=H-Rshiftprime, Kyz=-Syprime/2,
Xy=-Hbg*w-Rshift*wprime,
uhat=0, vhat=Dphase, rhat=Rc/4,
Zhat=Ud*w^2-Rshift*Zprime.
~~~

The full coupled complement forwards the momenta:

~~~text
P_y=Rmat*y+ell(s)
p_psi=-partial_s(E0)|P_y-g*Zhat
p_Z=-g*s, g=b*sqrt(h)*V^2
p_T=-(E0+p_psi*s+div F)    on this C=1, T_i=0 initial slice.
~~~

Thus the dust density is LOCAL and action-derived, not replaced by its
mean. Check the registered per-cell charges Qdust=1/5 and Qtheta=eta without
renormalizing either. Forward mean metric momenta are retained. The global
constraint reconstruction's change to the remaining momenta is measured;
no replacement state is adopted/evolved or historical lift overwritten.

The global adapter sets p_Z=-g*s BEFORE solving spatial/global rows and
allows g=0. It still requires s>0, positive metric/dust, regular complement
and a valid global translation chart. It never calls the old divided
regular inverse at a node.

## What initial flow was actually compared

Use odd grids n=17,25,33 shifted by theta0=pi/2 and3pi/2:54 grid/node cases.
Each grid includes one analytic zero at index0, explicitly set to0 rather
than a floating cos(pi/2). The two orientations test both nodes separately;
this is not a discretization simultaneously resolving every nodal trace
condition for the final continuum mode problem.

Complex-step momentum variations preserve the two charges and the global
translation cotangent chart. Mean-metric variations have their proper
off-diagonal factor2. In psi time the compared rates are:

| Direction | Required initial rate |
| --- | --- |
| hxx,hyy and mean hzz | 2H/p |
| hxy and mean hxz,hyz | 0 |
| Vx,Vz | 0 |
| Vy | -Hbg*w/p |
| Radial amplitude R | 0 |
| Reservoir r | Rc/(4p) |
| Fluctuating phase and dust origins | 0 |
| Regulator through the scalar-rate row | H_s+g*Ud*w^2/p=0 |

The zero fluctuating phase rate is AFTER quotienting the global origin at
fixed charge. The original rotating matter velocity vhat=Dphase is retained;
the matter phase was not frozen before variation. The original nodal Z row,
canonical p_psi compatibility, original spatial generators and mean/charge
constraints are checked separately.

Two complex steps1e-18 and1e-22 are used on the middle grid. Momentum-rate
comparisons use frozen normalized1e-8. The cancellation-sensitive scalar
row and nodal p_psi checks use frozen1e-4 relative to K_Q and K_Q*p, not a
scale dominated by gravitational background energy. Raw residuals remain
in the receipts; these computational requirements are not physical
accuracy/window or lower-order effect certificates.

## Numerical evaluation improvement, not a changed equation

Exact constant fields are differentiated as D*(f-f[0]), equivalent to D*f
since D*1=0. Their physical means remain in the state, potential, charges,
Hamiltonian and constraints. This prevents exactly flat h from acquiring
roundoff Ricci; the unstabilized curvature noise reached2.567e-10 in these
reference grids. Fourier, primitive and adjoint controls remain explicit.
No nonzero global source mean is silently projected away.

V1 passed1018/1018 and its full exact replay. Its largest initial-rate
residual7.674e-9 lay close to1e-8. Read-only isolation identified Vz, whose
rate should be0. On the same worst case, evaluating the known periodic
identity

~~~text
Hpsi=<(E+div F)/s>=<E/s-F*partial_z(1/s)>
~~~

reduced that raw transverse rate from7.674e-9 to2.714e-17 with identical
inputs and step. V2 uses the right-hand scalar-functional evaluation and
keeps Hdirect for an additional equivalence check at EVERY grid/node/case.
Pointwise p_psi=-(E+div F)/s is UNCHANGED. The flux is not omitted: its
scalar-rate derivative is essential, including at the initial constant s.

Only restore_undivided, grid_case equivalence bookkeeping and source pins
change; every other function/class AST is identical. No target, parameter,
initial jet, gauge, charge, clock, tolerance or physical formula changed.
The V1 and V2 formulas.json bytes are IDENTICAL. V1 is preserved as a
successful, narrow-margin implementation, not rewritten as a failure.

## Observed controls and immutable replay

| Control across all cases | V2 result |
| --- | --- |
| Largest normalized coordinate/mean-rate discrepancy | <2.197e-12 |
| Scalar-rate row relative to K_Q | <1.182e-6 |
| Scalar-rate row, raw reference value | <3.461e-9 |
| Original spatial-constraint residual | <3.111e-14 |
| Nodal Z-row residual | <2.467e-23 |
| Independent100-digit node momentum/density comparison | <1.095e-16 |
| Direct/by-parts Hamiltonian comparison | <1.338e-17 |
| Mean dust-charge discrepancy | <5.552e-17 |
| Sampled local dust density | >0.1997359 |

The sampled density is NOT a stronger continuous-density certificate or
an observational density measurement. The archived joint point roots,
8/12 inverse and new finite grids remain approximate controls; inherited
interval results retain only their original scopes.

All1072 local checks pass. Most repeat checks across grids/nodes/cases;
they are not1072 physical discoveries. Original100-digit node-density
checks and the independent original8/12 shift control are retained.
No ordinary cubic cusp tensor, epsilon inverse or unweighted Omega inverse
is used.

Both V1 and V2 have COMPLETE fresh eight-worker read-only replays.
For V2 all85 source pins/170 source-and-sidecar metadata records and6
scientific output files remain unchanged, including sizes/mtimes.
A separate220-record guard additionally preserves previous successes,
failed attempts and both current versions. Original sources/hashes are
untouched; only mutable research/review indexes receive guarded appends.

| Artifact | SHA-256 |
| --- | --- |
| V1 contract | bc94c33a7b2e1bb6793c43afe32272732cc845b9e058cb2f11c608d4d038297b |
| V1 executable | 052000518f5c745a028aba3def170c1ae0b6b276c8a124aab3c5cbec70a9c6ee |
| V2 flux addendum | 9730305c00a173905f3c2f2d4b6742338cd8b2a1dc31ed9a8451ff5936486de5 |
| V2 executable | 8ff1ccdd3c47c151276c21f968e355d032ec75698a300918546d19ffe0892cce |
| Attempt02 summary.json | 28ec677f75404d9e48431d1c1c7dc8ffcce99f70e18dfc9b66f0be7cd6f3778d |
| formulas.json, V1 and V2 | 08058e16cf87399b7f59e130f364dee99484ee41f6e122b6828e5407fd7ac19e |
| independent.json | 66acfd3d7a29c30ec145d64f4843aed21d5267fad64b427b46bd7d6420503607 |

Executable: Analysis/MasterTests/test_01_r4c1_global_nodal_lift_v2.py.
Receipts: Analysis/MasterTests/outputs/r4c1_global_nodal_lift_attempt_02/.
Use existing itsm_env Python, --workers 16 and NEW --output, or --replay
pointing to attempt02. Runtime/diagnostic journals are private/ignored.

## Next required work

Compute the complete initial momentum evolution with the metric/frame
two-form crosses; test time preservation of the auxiliary node conditions.
Then form the full coupled descriptor Hessian AND background-drift operator
on an explicitly admissible mixed-order/weighted domain, with both nodal
traces and global means/charges treated consistently. Only then assess its
spectrum/convergence and the physical interaction/frequency window.

A finite-grid initial-coordinate match does not establish full background
evolution, all node compatibility, arbitrary3D closure, nonlinear error
control, healthy GR or family GO. The unrestricted unweighted inverse
obstruction remains. Do not skip nodes, project away negative directions,
adopt a potential/vacuum-probe scale as a physical cutoff or change the
parent/action without a separate operator decision. Both identifying
matching inputs for Stage3 remain absent.

R9-MT1-GLOBAL-NODAL-LIFT-V2: DEFERRED; inherit NODAL-DESCRIPTOR-V2,
PLANAR-REDUCED-HAMILTONIAN-V1, joint/node/regularity/canonical and transitive
review debt. Memory pointer chk_aea5be32b4d6bc8f86bc1494 located the existing
joint report; live source files and frozen action govern this result.

Stage1 registered linear prepared-dust scope only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
No state adoption/evolution, vault-management write, manuscript/PDF/site,
publication, commit/push, action/provider/model/global-runtime change.
