# R4C1-G3N5: full-field, three-spatial-direction response kernel

Date: 9 October 2026. Version 1. Master Test 1 continuation after G3N4.
Conditional research; review DEFERRED; physics_pass=false; gate_effect=NONE.

## Actual deliverable and scope

Derive the unreduced quadratic action and linear Euler operator for all 22
ADM/frame/Cartesian-scalar/dust/regulator response fields, retaining x,y,z
derivatives. Use the frozen R4C1 action on its aligned, homogeneous isotropic
cosmic-time background. This is the kernel needed for coupled second-order
response to the G3N4 sources, not a new background, solution, physical Hessian,
stability proof, nonlinear evolution or healthy GR limit.

The full goal is not narrowed to this checkpoint. General nonlinear T3 data,
constraint-compatible initial data and evolution remain required. Earlier
tilted-domain C1/C2 findings are not changed by this aligned-background kernel.

Owning G3N4 report SHA-256:
1c7eca17f22a8e3e3ec39bb09017d05908b133f130b1f24e85f523b18af47a4b.
Force supplement summary SHA-256:
ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287.
Frozen R4C1 action SHA-256:
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
Inherit all source pins, three absent sidecars and original failed attempts.

## Fields, chart and dimensions

Use one formal response amplitude d with

```text
N=1+d alpha; h_ij=a^2(delta_ij+d M_ij);
N^i=d S_i/a; v^i=d V_i/a;
gamma=sqrt(1+h_ij v^i v^j);
n^t=gamma/N; n^i=v^i-N^i gamma/N;
U=(1+d nu)n; lambda_U=lambda0+d LambdaU;
u=u0+d du; v=v0+d dv; r=r0+d dr;
psi=psi0+d Pi; tau=tau0+d T;
epsilon=epsilon0+d Em; z_aux=d Z;
tau0_dot=C=exp(beta psi0).
```

Retain alpha, three S_i, six independent symmetric M_ij, three V_i,
du,dv,dr,Pi,T,Em,Z,nu,LambdaU. Independent values plus t,x,y,z first
derivatives form 110 jets; retain second jets when exporting the Euler
operator. Background coefficients remain symbolic and may be off shell.
The normal variation belongs to L_U; force/alignment/regulator use normalized
n, as frozen. No multiplier or auxiliary equation is omitted. Cartesian
u,v remain valid at zero amplitude. Preserve the action's mass dimensions;
formal K_Q,A,b or illustrative jets are not microscopic matching results.

## Required derivation and comparisons

1. Check exact ADM inverse, normalized n and off-unit U identities through
   d^2. Include volume, all four frame invariants, EH+GHY ADM kinetic bulk,
   Cartesian kinetics and complete potential/portal/vacuum term, alignment,
   temporal-force term, dust, unit multiplier and first-derivative regulator.
2. Derive spatial Ricci through d^2 with all spatial metric derivatives.
   Show its conversion to the first-derivative quadratic bulk by an explicit
   divergence identity on periodic T3. It must not be dropped because its
   direct G3N4 vector-source coefficient happened to vanish.
3. Export sector densities, tadpoles, the full sparse symmetric 110-jet
   quadratic Hessian, and all 22 linear Euler operators. Check quadratic
   homogeneity/reconstruction and retain time derivatives of background
   coefficients and the 3H measure term in the operators.
4. Recover the exact multiplier equations for Em,LambdaU,Z. Check that lapse,
   shifts and multipliers have no own time-derivative density. This does not
   authorize ignoring their equations or claiming a physical DOF count.
5. Compare temporal force, projected alignment and regulator with independent
   all-direction formulas. Recover the G3V complete transverse vector action
   at M=nu=0 before solving the shift. Check the vacuum TT principal gravity
   block and scalar flat-spatial-metric EH limit with their signs/factors.
6. Preserve -A Y^(3/2) separately: show Y0=Y1=0 and
   Y2=sum_i(Pi_i/a+p V_i)^2. It has no quadratic kernel here, but its unsmoothed
   directional cubic density and second-order Euler forcing remain required.
   No ordinary cubic vertex, smoothing or finite harmonic closure is asserted.

## Independent control thresholds frozen before execution

Compare the non-Ricci analytic quadratic coefficient against centered second
differences of the exact unexpanded geometry/action on two generic off-shell
jets with all spatial directions retained. Use 50-digit mpmath and
d=1e-3,5e-4,2.5e-4. Final normalized error <=1e-5; errors decrease or all
<=1e-12 at the numerical floor. Spatial Ricci receives the separate exact
bulk/divergence control above. The nonanalytic force is not counted as an
analytic Taylor term; its projected-gradient coefficient is checked exactly.
No local jet is described as an integrated physical solution.

## Integrity and unresolved work

New versioned executable/receipts and sidecars only; refuse existing output
directories; exact replay is read-only. Preserve every failure/unknown and
inherited failed attempt. A repair requires a new version, not editing the
original receipt, equations or acceptance threshold.

No gauge fixing, Schur inverse, homogeneous-sector elimination, physical
rank/sign inference or characteristic-domain claim is supplied by this
unreduced kernel. Next work must retain compatible constraints, homogeneous
data, unsmoothed forcing and the harmonic tail in the response solve.
Review alone remains deferred; missing physics is substantive.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action replacement, manuscript/PDF/vault change, provider dispatch,
commit, push, canonical promotion or publication.
