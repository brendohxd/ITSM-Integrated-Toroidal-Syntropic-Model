# R4C1-G3N2: constrained transverse multimode entry

Date: 9 October 2026. Version 1. Test-1 continuation after G3K-C2.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Question and scope

Test the preferred-foliation and regulator-rank prerequisites for extending
G3N1's nonanalytic transverse-vector amplitude probe to coupled multimode
fields. Use the actual G3V transverse direction, not a substituted longitudinal
phonon-only model. Retain its first-order metric-shift/dust constraints.

Determine whether those allowed waves admit a local U-orthogonal clock and
whether the regulator can be assumed algebraic with uniform velocity rank
near the aligned state. These are prerequisites, not a new full nonlinear
trajectory, physical ghost theorem or all-action/classical-evolution no-go.
Export missing scalar/tensor/frame/constraint response rather than dropping it.

## Frozen inputs and chart

G3V owning report:
Theory/Gates/RES-001/RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md,
SHA-256 952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27.
G3N1 report SHA-256 c72e32b6f81f35f51d336de945debb8936b94623fdba44e15fc64e0e622202b4;
G3N1 summary SHA-256 1c355b1f40afdc3a770d27adaaa1cd0c2b6b0fefb1d5b00d2cadc08778754167.
G3V attempt_01 summary, formulas and samples SHA-256 respectively:
07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae;
1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358;
93288f37a919d22f59a397ab8ffb732f8386d23ee561469be2bebea489af3d03.
G3K-C2 report SHA-256 5145e5e0cb67871ca918d9919b6433233f65e22c9126eb048ece7e0ad5a9e82d;
C2 summary SHA-256 31f28b8d0bb12b2ff297f3a2f76d4de0f9ddef49ae5c2d06fce65fbf9d59e39d.
Verify their complete inherited source pins and available sidecars; preserve
the three declared missing sidecars and all original failed assertions.

G3V chart: ds^2=(-N^2+B_y^2)dt^2+2a B_y dt dy+a^2(dx^2+dy^2+dz^2),
U=(gamma/N,0,(w_y-B_y gamma/N)/a,0), gamma=sqrt(1+w_y^2).
The archived homogeneous background uses N=1 and tau_dot=C, not tau=t.
Do not mix that cosmic-time chart with C2's dust-clock N=C^-1 chart.
All 216 archived G3V chart records are used without reintegration/refitting.

## Retained transverse constraints and foliation test

Use the owning first-order nonzero-mode shift solution B_y=sigma w_y,
sigma=-eta/(8-eta), with zero homogeneous shift integration mode. The first-
order lapse/dust/regulator and other linear sectors retain their G3V scope.
No nonlinear all-sector constraint solution is presumed from this solution.

Derive U_flat and U_flat wedge dU_flat with w_y(t,z), B_y(t,z) arbitrary,
then insert only the linear shift solution. Derive its leading amplitude
coefficient and compare with direct covariant metric/one-form evaluation.
If this three-form is nonzero, a local U-orthogonal real clock cannot exist:
U_flat=-mu dT would imply U_flat wedge dU_flat=0. Later O(epsilon^2)
backreaction cannot cancel an established nonzero O(epsilon) coefficient.
This rejects an intrinsic-preferred-leaf assumption, not the retained
covariant definition of Delta on vortical frames or every possible time.

Use w_y=epsilon[cos(chi)+rho cos(3chi)], chi=kz.
Profile controls rho=(0,-1/3,1/3,1), epsilon=(1e-2,1e-3,1e-4).
The main 216-chart witness uses rho=1/3, epsilon=1e-3 and
chi=(pi/5,pi/3,pi/2,2pi/3,4pi/5). Retain zeros, not only nonzero points.
Derive a uniform small-amplitude bracket bound and the nonzero derivative
L2 norm; a grid alone is not a foliation proof. No physical torus size or
EFT amplitude is selected by these reference-coordinate profiles.
Direct one-form complex-step derivative comparison: normalized error <=1e-10.

## Regulator response and raw multimode velocity block

Retain the parent's direct second-order auxiliary response
Delta2=psi_dot W W_dot+(psi_ddot+2H psi_dot)W^2, z2=-Delta2.
For W=cos(chi)+(1/3)cos(3chi) and
W_dot=(1/4)cos(chi)-(1/8)cos(3chi), export every harmonic 0,2,4,6.
This is the direct response only: induced scalar/metric/psi contributions
at the same order remain an explicit missing input, not a completed J2.
Check Fourier reconstruction at all 216 charts with normalized error <=1e-10.

Use orthonormal spatial-average psi/z basis e=(1,sqrt(2)cos(2chi),
sqrt(2)cos(4chi),sqrt(2)cos(6chi)). Derive the unsmoothed raw time-kinetic
mixing -b a^3 w_y^2 z_dot psi_dot/N. No ordinary cubic Taylor vertex is
assumed and no |W|^3 is replaced by signed W^3.
Derive Gram G_mn=<W^2 e_m e_n> exactly by Fourier coefficients, including
all four modes. Prove positive definiteness for nonzero finite W, and check
all leading minors for the four rho controls. Compare independent SciPy and
50-digit mpmath integrals to the exact Gram: normalized error <=1e-10.

The psi/z raw velocity block is [Apsi,C;C^T,0], C=-b a^3 epsilon^2 G/N.
Retain the direct force-sector Apsi, including K(1+w_y^2) and the absolute-
cubic second derivative at the archived homogeneous psi_dot. This raw block
is not the full post-constraint interacting Hessian or a physical ghost test.
Prove its determinant/inverse identities and the epsilon=0 rank separately;
never invert epsilon=0. An epsilon-dependent numerical scaling cannot be
claimed as a regular endpoint field transformation.

Use the 12 DOP853 eta/t=(0,4), k=20 archived charts, all four rho profiles
and three epsilon values. Compare the 50-digit raw inverse against the block
formula with normalized error <=1e-10. Verify epsilon^4 times its z/z inverse
block approaches its explicit nonzero leading limit, discrepancy <=10 epsilon^2.
Supplement with unexpanded-action central-difference Hessian controls at
eta=1,t=0,k=20,rho=1/3,epsilon=1e-3, relative velocity steps
(1e-4,5e-5,2.5e-5); normalized discrepancies <=1e-10 at 50 digits.

## Disposition and boundaries

If the transverse Frobenius coefficient survives its actual linear constraint,
reject the naive extension that treats all these waves as an intrinsic-leaf
system. If the raw regulator rank changes and its inverse is nonuniform,
reject uniform algebraic-z / regular-Legendre claims inferred from G3N1.
Do not infer a failure of every classical formulation or every possible
constraint reduction from either result. Full nonlinear scalar/tensor/frame/
dust constraints, physical Cauchy/DAE domain, finite-band/cutoff and the
nonanalytic quantum/scattering prescription remain required inputs.

Store exact algebra, all failures/unknowns, hashes, scopes, numerical controls
and exact read-only replay in new versioned files. Preserve original sources.
Review debt DEFERRED; Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. No action change, manuscript/PDF edit, vault mutation,
provider dispatch, commit, push, promotion or publication.
