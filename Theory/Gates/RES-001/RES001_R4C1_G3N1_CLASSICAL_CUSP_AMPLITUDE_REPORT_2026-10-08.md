# R4C1-G3N1: classical cusp-amplitude report

Date: 8 October 2026. Owning gate: frozen G3N1 Test-1 prerequisite.
Claim Conditional; research PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Outcome

530/530 registered local checks pass; zero failed assertions.
The separate executable replays all three result artifacts byte-for-byte.
No registered equation, sampling rule or tolerance was changed after testing.

The leading nonanalytic interaction admits a regular Hamiltonian and
unique global evolution in the declared frozen-coefficient amplitude probe.
It does not need an ordinary third Taylor derivative for that classical ODE.
However, its spatial force has a nonzero third harmonic: the retained
one-mode Galerkin projection is not an invariant nonlinear field subspace.
Neither result establishes full R4C1 classical evolution, stability,
a physical EFT window, scattering, quantum consistency or Test-1 acceptance.

## Exact normalization and signed equation

G3V's C_X is the spatial-average coefficient for a local comoving field
X_amplitude cos(kz), not for a canonically normalized real mode amplitude.
With the spatial-average action density and

\[
X(t,z)=\sqrt2\,q(t)\cos(kz),\qquad D=2\sqrt2\,C_X,
\]

the retained probe is

\[
L=\tfrac12\dot q^2-\tfrac12\omega^2q^2-D|q|^3,\qquad
\ddot q+\omega^2 q+3Dq|q|=0.
\]

Here omega^2 is the positive parent canonical_frequency_squared at a
frozen chart event. The original metric-shift contribution and background
quadratic mass are retained through that parent coefficient.
The factor sqrt(2) follows from the cosine-square average 1/2;
the absolute-cubic average is 4/(3 pi). No parent coefficient is retuned.

q has mass dimension 1, dot(q) dimension 2, D dimension 1 and omega^2
dimension 2. L and H are spatial-average densities of dimension 4;
each amplitude-equation term has dimension 3. An integrated,
volume-normalized quantum mode would need an additional volume factor.
No quantum Fourier normalization or vertex is supplied by this probe.

For this L only, p=dot(q) and

\[
H=\tfrac12p^2+\tfrac12\omega^2q^2+D|q|^3.
\]

The velocity Hessian is 1. This does not audit the complete regulator/
auxiliary velocity Hessian or its reduced Legendre map.
The action remains C2 but not C3 at zero amplitude. Its force is C1 and
locally Lipschitz, but not C2 when D>0. Absolute values are not smoothed.

## Classical existence and the limit of that result

Set y=q/q_star, tau=omega t and gamma=3Dq_star/omega^2, with q_star>0.
Then y''=-y-gamma*y*abs(y). On |y|<=R its first-order phase vector field
has max-norm Jacobian bounded by 1+2 gamma R, so local uniqueness applies.
The conserved dimensionless energy is

\[
e=\tfrac12(y'^2+y^2)+\frac{\gamma}{3}|y|^3.
\]

For initial (+/-1,0) and gamma>=0, the monotonically increasing potential
in |y| bounds |y|<=1 and |y'|<=sqrt(1+2 gamma/3). The bounded phase orbit
and locally Lipschitz vector field continue the frozen probe for all tau.
This is an ODE argument, not a full nonlinear Cauchy/PDE theorem.

If coefficients evolve, the exact probe balance instead contains

\[
\frac{dH}{dt}
 =\tfrac12\dot{\omega^2}q^2+\dot D\,|q|^3.
\]

The reported integrations freeze coefficients and do not silently infer
conservation or global existence on a changing cosmological background.

## Higher-harmonic obstruction to one-mode closure

For an unsmoothed cosine profile, the retained nonlinear spatial force
is proportional to cos(z)*abs(cos(z)). Exact quadrant integration gives

\[
\langle\cos^3(z)\,\mathrm{sign}(\cos z)\rangle
 =\langle|\cos z|^3\rangle=\frac4{3\pi},
\]
\[
\langle\cos(3z)\cos(z)|\cos(z)|\rangle=\frac4{15\pi}.
\]

Its third-harmonic force projection is therefore 1/5 of its fundamental
force projection. This is a ratio within the nonlinear force, NOT a
prediction that a physical third-harmonic field amplitude is 20% of the
fundamental, or that the full dynamics has been solved.

The one-mode Galerkin projection remains a useful declared probe, but the
retained nonlinear field equation does not preserve that one-mode subspace.
Other harmonics, the full constraint response and higher-order interactions
cannot be omitted when extending this result to the complete action.

## Registered numerical verification

All 216 pinned G3V chart events have finite positive sampled kinetic,
gradient, frozen canonical frequency-squared and cusp inputs.
This is not a continuous-domain or all-sector stability result.

Twelve DOP853 archived charts (six eta values, t=0 or 4, k=20) were used
with initial |W|=0.01 and q_star=a^(3/2)*sqrt(kinetic_weight)*|W|/sqrt(2).
This is a chosen probe amplitude, not a certified physical EFT bound.
No cosmological background was reintegrated or refitted.

Synthetic gamma=(0,1/8,1) controls are separately labeled and are not
retuned ITSM backgrounds. Signed states were integrated using DOP853
and Radau with the frozen tolerances: 60 fine runs and four coarse controls.
Both methods are local numerical checks, not independent peer review.

| Check | Maximum measured error | Registered bound |
| --- | --- | --- |
| Relative frozen-energy drift | 3.2831091691430353e-10 | 2e-8 |
| Quarter-period versus energy quadrature | 1.2359746939682063e-13 | 2e-8 |
| Paired-method normalized state difference | 2.195034154439668e-10 | 2e-8 |
| Signed parity difference | 0 | 2e-8 |
| Synthetic gamma=1 coarse/fine state difference | 5.0457787059698944e-8 | 2e-6 |

The independent 50-digit mpmath quarter-period quadrature uses the
endpoint-substituted energy integral, not a fitted integration period.
It does not upgrade the precision of the archived coefficients.

The twelve archived probe gamma values span 4.030372215075516e-20 to
1.0254387325218494e-6; eleven are below 2e-8. No nonlinear detection is
claimed when an effect lies below the numerical tolerance. Even a resolved
effect in this probe is not a prediction of complete R4C1 dynamics:
the regulator quartic, higher-mode backreaction and full constraints are
not computed by G3N1 and need not be negligible at the chosen amplitude.

## Related newer tilted-background work

The live register also contains the separate
[tilted-background G3T report](RES001_R4C1_G3_TILTED_BACKGROUND_REPORT_2026-10-08.md),
SHA-256 f3ad690310aa762aff87f37fba961f5be9280b4c1844a9d608c2b90b5e037105.
Its opening disposition and remaining-work section were checked for overlap.
G3T is not a computational input to this frozen G3N1 result, is not
overwritten, and its 268/268 checks are not added to G3N1's count.

G3T reports local reduced tilted Y>0 backgrounds, while preferred Cauchy
admissibility, the coupled finite-k physical spectrum and the physical
cutoff remain unresolved. G3N1 does not settle its clock/Hessian issue.
The frontier is a constraint-aware, admissible physical-domain calculation,
not a promotion of this single-amplitude probe.

## Artifacts and reproduction

- [Frozen contract](RES001_R4C1_G3N1_CLASSICAL_CUSP_AMPLITUDE_CONTRACT_2026-10-08.md):
  SHA-256 83a6aafc934d00982b28ce745ef4626fdd6a4a017e5c2dcd328e14ea0985a102.
- [Versioned source](../../../Analysis/MasterTests/test_01_r4c1_g3n1_classical_cusp_amplitude_v1.py):
  SHA-256 dde5c735beb7851e9a0c37c593e81bf0b2ffc8c04cb2fb3ff77b55d0fe943402.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n1_attempt_01/summary.json):
  SHA-256 1c355b1f40afdc3a770d27adaaa1cd0c2b6b0fefb1d5b00d2cadc08778754167.
- [Formulas](../../../Analysis/MasterTests/outputs/r4c1_g3n1_attempt_01/formulas.json):
  SHA-256 1f1c1dab57079d1a2478d3d8f3e1bd2a12a011fa7be7be4e8947c5779ec66e24.
- [Cases](../../../Analysis/MasterTests/outputs/r4c1_g3n1_attempt_01/cases.json):
  SHA-256 1a23e209177e19c9093099890d37710fab768bca63f8a42a07ef0de388f47704.

~~~powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3n1_classical_cusp_amplitude_v1.py --replay
~~~

Initial-run private log:
.local/itsm-context/output-c25057b03874465e8c6a0306c11ee607.txt,
SHA-256 dca1aefbfd6a6171e09c1786f7d04d755a04e57b0bed16c858f0b0d9de5793e2.
Successful replay log:
.local/itsm-context/output-3c71ab783f9d418bad83d4dd5c1447df.txt,
SHA-256 31a9b7de244978bc2859082ce401ec32887506ec1fe2f2c0c5152ecec1ef0249.
Logs remain ignored/private. Original G3V and all failed parent receipts,
sources and sidecars remain unchanged.

## Review and publication boundaries

Register R9-MT1-G3N1 inherits G3V-CROSSCHECK/G3V/V1-integrity and all
their direct/transitive substantive and deferred-review dependencies.
Pending review alone does not prevent this local bounded work.

Canonical Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
Ordinary full cubic Taylor scattering and the physical cutoff remain held.

P1/P2 release decisions are recorded separately; G3N1 is not silently
imported into those candidates. No old manuscript/PDF or scientific
artifact is rewritten; no vault mutation, provider dispatch, model change,
commit, push, upload, canonical promotion or publication.

