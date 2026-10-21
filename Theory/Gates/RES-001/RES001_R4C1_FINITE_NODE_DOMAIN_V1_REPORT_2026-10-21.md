# Finite node conditions do not by themselves repair the unweighted inverse

21 October 2026. Conditional unchanged-R4C1 Stage2 domain result.
Local113/113; complete fresh read-only replay exact;710 raw-integer preservation
records unchanged. These are verification controls, not113 physical discoveries.

## Meaning and limitation first

The earlier scalar-rate bump was not certified to satisfy the auxiliary-node
conditions. The new argument closes a specific loophole: imposing any FINITE
collection of scalar homogeneous linear conditions still leaves a sequence
with arbitrarily small two-form response, IF the stated localized bulk freedom
remains available. Both node traces and nonlocal linear conditions may be
included; their number need not be small.

This does NOT identify ITSM's complete physical tangent space or prove that it
contains these probes. An infinite/pointwise relation, an appropriate graph or
weighted norm, or an independently justified finite bandwidth can exclude the
assumed freedom. A finite number of PDE equations imposed at every spatial point
is not a finite number of scalar constraints. The unknown full auxiliary
hierarchy is not assumed to be finite. No mixed-order/weighted no-go, physical
instability, all-action rejection, healthy-GR result or physical cutoff follows.

The practical requirement is now sharper: finite node checks alone cannot be
the justification for a uniformly bounded ordinary-L2 first-order inverse.
The physical domain and its norm must be derived and checked explicitly.

## Source form and domain

Use the full undivided reduced form already derived in NODAL-DESCRIPTOR-V2 and
the global planar reduction:

\[
 \Omega=d\Theta_{\rm other}-g\,ds\wedge dZ-s\,dg\wedge dZ,
 \qquad g=b\sqrt{\det h}\,V^ih_{ij}V^j.
\]

All metric/frame crosses are retained. At the registered analytic slice
\(h=I\), \(s=p>0\), \(V=(0,w,0)\), a simple alignment zero has local coordinate
\(x=z-z_*\) and \(w=\pm e\sin(kx)\), where \(e,k>0\). Hence
\(g=b e^2\sin^2(kx)\). The argument uses the ordinary coordinate-L2 integral
over the periodic planar direction. A common average/constant transverse-volume
normalization changes both sides consistently, not the inverse-response ratio.
It does not select a new torus topology or count only two nodes on a larger
periodic extension.

For a direction changing only the INDEPENDENT reduced scalar-rate coordinate,
\(v_f=(\delta s=f,\text{other independent variations}=0)\), contraction gives

\[
 \Omega v_f=(\text{only the }Z\text{ row}:\;g f).
\]

The crosses were not deleted: \(dg(v_f)=dZ(v_f)=0\). Dependent momenta in the
spatial/global constraint restoration are not frozen as independent variables.
Their effects belong in any full condition applied below. The symbolic control
keeps the generic metric/frame dependence of g, checks closure with all crosses,
and rejects the form with those crosses removed. Canonical spectator sectors
remain present and can be added as a direct sum; this is not a propagating-mode
count or an assertion that every direction is physically admitted.

## Conditional finite-constraint theorem

Let \(L_1,\ldots,L_r\) be any fixed finite collection of REAL homogeneous linear
functionals defined on the following smooth reduced probe space. Complex
conditions can be split into real and imaginary conditions. They may contain
both node traces, any finite number of jet/tangency conditions and nonlocal
linear functionals from the full constraint pullback. No L2-continuity is needed
for the finite-dimensional argument, but the functionals must actually be
defined on these probes. That assumption requires separate checking for the
eventual physical domain.

For

\[
 0<\epsilon<\frac{\pi}{8k},\qquad N=r+1,\qquad
 c_j=\epsilon\left(1+\frac{j+1/2}{N}\right),\qquad
 h_\epsilon=\frac{\epsilon}{4N},\quad j=0,\ldots,r,
\]

choose translated smooth unit bumps \(f_j\), each supported within
\((c_j-h_\epsilon,c_j+h_\epsilon)\). Their supports are disjoint and lie strictly
inside \((\epsilon,2\epsilon)\). Thus every bump and every point jet vanish at
both neighboring nodes and all other nodes of the periodic extension.

Form the REAL matrix \(M_{\alpha j}=L_\alpha(v_{f_j})\). It has r rows and r+1
columns, hence rank at most r and a nonzero kernel vector. Normalize a real
kernel vector a so that \(\sum_j a_j^2=1\). Then

\[
 f_\epsilon=\sum_j a_j f_j,\qquad
 \|f_\epsilon\|_2=1,\qquad L_\alpha(v_{f_\epsilon})=0.
\]

The coefficients may depend on epsilon and the actual functionals. The bounds
below are independent of that choice. This is not an implemented physical
constraint projector: the unknown full ITSM hierarchy was not substituted by
the synthetic numerical examples.

On the whole support, \(k\epsilon<kx<2k\epsilon<\pi/4\). Concavity of sine on
\([0,\pi/2]\) gives \(\sin y\ge2y/\pi\), while \(|\sin y|\le|y|\). Therefore

\[
 \frac{4}{\pi^2}|b|e^2k^2\epsilon^2
 \le \|\Omega v_{f_\epsilon}\|_2
 \le 4|b|e^2k^2\epsilon^2.
\]

For fixed nonzero b this is an explicit two-sided order-epsilon-squared result
for the FULL displayed two-form image, not a slope fitted to samples. If b=0
the direction is null. A uniform estimate
\(\|v\|_2\le C\|\Omega v\|_2\) on this finitely constrained probe-containing
space is impossible as epsilon tends to zero.

If the two-form is pulled back further to the finite-constraint space, the
restricted covector norm with the inherited L2 norm is no larger than the full
covector norm. The upper-bound obstruction therefore persists. The displayed
LOWER bound is not asserted for that restricted covector norm: restriction may
make the image even smaller or null.

## Positive clock, controlled remainder and coordinate normalization

An explicit smooth template is

\[
 \psi(u)=\frac{e^{-1/(1-u^2)}}{\sqrt J}\quad(|u|<1),\qquad
 J=\int_{-1}^{1}e^{-2/(1-u^2)}du,
\]

with psi zero outside. The interval \([-1/2,1/2]\) gives
\(J\ge e^{-8/3}\); the maximum integrand gives \(J\le2e^{-2}\). Consequently
\(\|\psi\|_\infty\le e^{1/3}\). Disjoint supports and \(|a_j|\le1\) imply
\(\|f_\epsilon\|_\infty\le e^{1/3}/\sqrt{h_\epsilon}\). Choosing

\[
 \alpha_\epsilon=\frac{p\sqrt{h_\epsilon}e^{-1/3}}2
\]

keeps \(p+\alpha_\epsilon f_\epsilon\ge p/2\). The linear inverse-response
ratio is unchanged. This establishes kinematic scalar-rate positivity only,
not nonlinear constraint admission or existence of an evolved solution.
These are stationary-node probe directions; moving-node perturbations are not
banned or replaced. Smooth probes do not impose a C3 requirement on the action.

The exact sine-squared coefficient is retained. From
\(|\sin y-y|\le|y|^3/6\) and \(|\sin y|\le|y|\),
\(|\sin^2 y-y^2|\le y^4/3\). Thus

\[
 \|(g-b e^2k^2x^2)f_\epsilon\|_2
 \le \frac{16}{3}|b|e^2k^4\epsilon^4.
\]

This is a controlled local approximation of the response, not a changed action,
new dust convergence claim or physical cutoff. These are reference-chart norms
with heterogeneous field dimensions, NOT SI energy normalization. The explicit
powers use \(k\epsilon\) dimensionless and do not supply a uniform eta-to-zero
GR theorem.

For a fixed bounded invertible coordinate map T, the two-form becomes
\(T^*\Omega T\). Normalize \(u=T^{-1}v/\|T^{-1}v\|\); then
\(\|T^*\Omega T u\|\le\|T\|^2\|\Omega v\|\). A fixed nonsingular bounded
normalization cannot remove the vanishing response. Singular/weighted or
epsilon-dependent normalizations are outside this assertion and require their
own physical justification.

## Verification and exact replay

The executable checks the full symbolic contraction and retained crosses,
exact normalization/support/C2 endpoint controls, arbitrary rational finite
constraint kernels, and a separate translated-bump moment construction. For
the latter, coefficients \((-1)^j\binom rj\) annihilate moments of degree below r
for any common translated smooth template; their squared norm is
\(\binom{2r}{r}\). Exact-polynomial C2 controls are identified as controls, not
mislabelled C-infinity physical perturbations. No floating rank threshold,
pseudoinverse or physical negative-mode deletion is used.

Synthetic conditions r=0,1,2,4,8 and k*epsilon=0.1,0.01,0.001,0.0001 have
independent80-digit quadrature controls. Measured normalized response ratios
range2.2452785959--2.4340526162 within the analytic [4/pi^2,4] bracket; the largest
normalized fourth-order remainder is below2.2958384758, versus the analytic16/3
bound. Quadrature is not an interval certificate and is not the proof.

All113 local checks pass. Complete fresh read-only replay returns exit0 and
READ_ONLY_REPLAY_EXACT, reproducing all three scientific JSONs and sidecars.
All16 source pins/34 source-and-library metadata records are unchanged. The
separate710-record raw-integer guard confirms exact hashes, sizes, timestamps
and file set, including the704 pre-audit records, the verified QR checkpoint,
earlier failures and every new receipt. Historical JavaScript timestamp
limitations remain documented separately; no original evidence was rewritten.

| Artifact | SHA256 |
| --- | --- |
| Contract |fbcc101c6fc653a636072bb63af789d4cad2cb3c1cf3cf1e1d2aa9a35a6d3266 |
| Executable |e1c15ae0a29cd0ad8587c75138b569e0f0f85edc07dbc20327c42ff8414a06a9 |
| summary.json |5937cb432ae3c7bb5f079a45ba44f604ed894fd068de84b4cee2a57cbb6b488c |
| independent.json |eb372f940a0e6b8347a87b96e249d69875339a8be6f8dc8ced5695f186bf765f |
| formulas.json |db7f4f6a75de2aead87786fde1d175ddfb9688c319049d12f789074af912dee4 |

Executable: Analysis/MasterTests/test_01_r4c1_finite_node_domain_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_finite_node_domain_v1_attempt_01/.
Private optimizer/runtime snapshots remain ignored. These are same-author
computational controls and replay, not independent scientific review.

## Required next route and unchanged programme status

Explicitly define the complete auxiliary/physical perturbation domain and its
norm: a justified weighted/graph or mixed-order formulation, a genuine bulk
elimination, or a derived physical finite-band restriction may alter the above
assumptions. Their positivity, closure, persistence and interaction/error bounds
must be demonstrated, not asserted. Completing QR alone cannot supply them;
the saved full372-mode numerical continuation also remains unfinished.

No actual complete physical constraint hierarchy was instantiated here. Physical
mode/energy/clock normalization, simultaneous continuum compatibility, nonlinear
interactions/cutoff, healthy GR and both identifying matching inputs remain open.
The earlier six numerically consistent cases, twelve unresolved cases and every
negative-action/nonoscillatory direction are unchanged. Stage1 complete only in
its registered bounded linear prepared-dust scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged. Rule9 DEFERRED; Rule9_cleared=false; inherit the cited nodal,
global-reduction, tangency, descriptor and transitive review dependencies.
physics_pass=false; gate_effect=NONE. No new action/parent, state adoption/
evolution, vault-management write, manuscript/site edit, publication,
commit/push, paid provider dispatch or model/package/global-runtime change.
