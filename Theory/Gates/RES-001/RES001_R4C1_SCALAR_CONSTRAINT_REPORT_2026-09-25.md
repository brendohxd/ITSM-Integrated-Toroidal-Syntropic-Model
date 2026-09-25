# R4C1-S1: interacting scalar constraint reduction

Date: 2026-09-25. Conditional R4C1-v1 candidate; Master Test 1.
Review: DEFERRED. Research use: PROCEED_PROVISIONALLY within the scope below.
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Implementation validation: 71/71 checks pass; no failed or unknown check.

## Result and scope

The nonzero-mode scalar quadratic action of the frozen R4C1 candidate has
been reduced with its lapse, longitudinal shift, dust multiplier and regulator
constraints retained. It has six scalar kinetic directions. At the unchanged
B1 coefficients, its kinetic form is positive definite in the regular
expanding, spatially flat gauge. This follows from an exact sum of squares,
not merely from numerical eigenvalues. The registered numerical samples
independently show no negative or unresolved kinetic eigenvalue.

This is a **classical scalar-sector no-ghost result**, not full stability or
Test-1 closure. Gradient/characteristic analysis, evolving perturbations,
homogeneous constraints, all-sector robustness, EFT validity and a healthy
continuous GR limit remain open. It supplies no microscopic coefficient
matching and does not change Test 3's identifiability result.

Owning [contract](RES001_R4C1_SCALAR_CONSTRAINT_CONTRACT_2026-09-25.md);
[frozen action](RES001_R4C1_ACTION_FREEZE_2026-09-25.md);
[B1 background](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md).

## 1. Physical chart and retained variables

On the homogeneous B1 solution use signature -+++ and

\[
 ds^2=-N^2dt^2+a^2(dx+Sdt)^2+a^2dy^2+a^2dz^2,\qquad N=1+\alpha,
\]
\[
 U^0=\frac{\sqrt{1+w^2}}{N},\qquad
 U^x=\frac{w}{a}-S\frac{\sqrt{1+w^2}}{N}.
\]

This parametrization solves the unit-frame constraint on its regular future
timelike branch. It retains the longitudinal frame degree of freedom and
the metric dependence of the normalization; it does not freeze the frame.
The frame multiplier's normal equation determines that multiplier rather
than providing an extra propagating scalar.

Spatially flat scalar gauge removes the spatial metric scalar variables using
the two scalar diffeomorphisms. It is valid here for H!=0 and k!=0. Lapse and
shift are NOT gauge-set to zero. On the on-shell background, the omitted
spatial scalar metric equations are related to the retained equations by
diffeomorphism identities. An H=0 background needs another chart; this
calculation does not establish its physical scalar reduction.

Let q=(delta u,delta v,delta r,delta psi,delta tau,w), and retain auxiliaries
y=(alpha,S,delta epsilon,z). Use sqrt(2) cos(kx) for scalar quantities and
sqrt(2) sin(kx) for w,S. The coordinate periods are one reference length:
k=2*pi*n, n=(1,2,4,8), not k=n. The homogeneous isotropic background gives an
isotropic local Fourier symbol; the tested integer vectors are (n,0,0).
Cartesian u,v remain regular when either condensate component vanishes.

The action is expanded before solving the dust multiplier constraint. In
particular, the dust action is not set to zero by prematurely imposing its
normalization. Fixed temporal endpoint variations, periodic spatial
boundaries and the frozen GHY term are retained.

## 2. Action-level checks and constraint block

Define

\[
 c_{13}=c_1+c_3,\quad c_{14}=c_1+c_4,\quad c_L=c_1+c_2+c_3,
 \quad c_\theta=c_1+3c_2+c_3,
\]
\[
 M_c^2=M_P^2+\tfrac12M_U^2c_\theta,\quad
 M_t^2=M_P^2-M_U^2c_{13},\quad C=e^{\beta\bar\psi},
\]
and S_kin=udot^2+vdot^2+rdot^2+K_Q psidot^2.
The script builds all four frame invariants from the perturbed metric
connection. Their quadratic density has no lapse or shift time derivatives.
The EH+GHY contribution divided by a^3 is

\[
 -3M_P^2H^2\alpha^2-2M_P^2H\alpha\,\partial_xS.
\]

Direct covariant expansion also gives

\[
 \delta\Delta_\psi=a^{-2}\partial_x^2\delta\psi
       +\frac{\dot{\bar\psi}}a\partial_xw,
\qquad
 \delta\Delta_{\psi,k}=-\frac{k^2}{a^2}\delta\psi
       +\frac{k\dot{\bar\psi}}a w.
\]

The regulator density is b z^2/2+b z delta Delta, after periodic integration
by parts. Thus z=-delta Delta and its contribution is -b(delta Delta)^2/2.
Omitting the frame term changes the operator and is rejected by the check.
The alignment density before Fourier averaging is

\[
 -\frac\zeta2\left[\frac{\bar v\partial_x\delta u-
 \bar u\partial_x\delta v}{a}
 +(\bar v\dot{\bar u}-\bar u\dot{\bar v})w\right]^2.
\]

Y begins at quadratic perturbative order as
(partial_x delta psi/a+psidot*w)^2. Therefore -A Y^(3/2) has zero second
variation at this aligned background. No ordinary quadratic gradient is
inserted, and no analytic cubic Taylor vertex is claimed.

For the averaged density divided by a^3, the auxiliary Hessian is

\[
 B=\begin{pmatrix}
 -6M_c^2H^2+S_{\rm kin}+\rho_m+M_U^2c_{14}k^2/a^2
       &-2M_c^2Hk&-C^4&0\\
 -2M_c^2Hk&-M_U^2c_Lk^2&0&0\\
 -C^4&0&0&0\\
 0&0&0&b
 \end{pmatrix},
\qquad \det B=C^8M_U^2b k^2c_L.
\]

Its signature is NOT the physical kinetic signature. It is invertible on
the registered domain. In addition to the gauge boundary H=0, k=0, b=0,
M_U^2=0 or c_L=0 require different constrained reductions. No inverse or
pseudoinverse through those surfaces is used. Finite C>0 is required.

The dust equation gives alpha=delta taudot/C-beta delta psi. Defining
X=udot*delta u+vdot*delta v+rdot*delta r+K_Q psidot*delta psi,
the shift solution is

\[
 S=\frac wa+\frac{X+\rho_m\delta\tau/C-2M_c^2H\alpha}{M_U^2c_Lk}.
\]

The remaining lapse equation fixes delta epsilon. Its complete formula and
all sixteen-by-sixteen pre-constraint entries are exported in the matrix
artifact. Each auxiliary Euler equation vanishes exactly after substitution;
the twelve retained field/velocity derivatives also satisfy the reduction
chain rule. Direct substitution agrees exactly with the Schur complement.

## 3. Reduced matrices and exact kinetic certificate

The machine-readable artifact supplies K,M,V in

\[
 \langle L^{(2)}\rangle/a^3
 =\tfrac12\dot q^TK\dot q+\dot q^TMq-\tfrac12q^TVq.
\]

Both K and V are symmetric. M need not be. Time evolution requires

\[
 K\ddot q+(\dot K+3HK+M-M^T)\dot q
       +(\dot M+3HM+V)q=0,
\]

not an eigenvalue test on V alone. The kinetic bilinear has the exact form

\[
\begin{aligned}
 \dot q^TK\dot q={}&
 \sum_{f=u,v,r}(\delta\dot f-\dot{\bar f}\delta\dot\tau/C)^2\\
 &+K_Q(\delta\dot\psi-\dot{\bar\psi}\delta\dot\tau/C)^2\\
 &+M_U^2c_{14}(\dot w-k\delta\dot\tau/(aC))^2
 +D(\delta\dot\tau/C)^2,\\
 D={}&\frac{4H^2M_c^2M_t^2}{M_U^2c_L},\qquad
 \det K=\frac{K_QM_U^2c_{14}D}{C^2}.
\end{aligned}
\]

For unchanged B1 parameters the square weights are 1,1,1,3,1/6 and
D=66H^2. The velocity transformation defining these squares is invertible
for finite positive C. Thus K is positive definite for H!=0 in this regular
chart. This analytic identity was added after the first registered numerical
run as an explicitly labelled strengthening; no action, parameter, sample,
threshold or outcome was adjusted to obtain positivity.

This establishes more than the four sampled wave numbers for the algebraic
kinetic form, but NOT uniform positivity in singular limits or EFT validity
at arbitrary k. As H approaches zero this chart degenerates; raw eigenvalues
can also approach zero in singular wavelength/parameter limits. A healthy
uniform decoupling or cutoff does not follow from this identity.

Natural-unit dimensions are those of the action freeze: scalar amplitudes
have mass dimension one, psi and w dimension zero, tau dimension minus one,
and every density above dimension four. D has dimension four. K's entries
carry different dimensions across fields; its numerical eigenvalue magnitudes
are reference-chart quantities. Inertia is invariant under nonsingular real
field rescaling. No canonical observational normalization is implied.

## 4. Registered numerical evidence

Use the pinned B1 trajectory at 801 times on [0,4], with n=(1,2,4,8).
A separate Radau integration of the same frozen background equations gives
the second trajectory. There are 3,204 time-mode pairs and 6,408 evaluated
kinetic matrices, not 6,408 independent physics requirements.

- Every sampled inertia is (positive,negative,unresolved)=(6,0,0).
- Minimum raw kinetic eigenvalue: 0.009292929115976269, in the stated chart.
- Maximum auxiliary condition number: 204303.30722233158.
- Independent trajectory difference: 1.411611475586304e-11, normalized as
  prescribed; maximum relative eigenvalue difference: 1.911724753795918e-11.
- Numeric Schur agreement: 9.602576958628832e-16; kinetic asymmetry: zero.
- Minimum sampled H=0.14221719136506666 and a=1 keep the chart regular.

The independently coded, unexpanded frame density gives second-difference
errors 1.7118112899394688e-9, 5.044437506596111e-10 and
4.489325994283533e-10 for epsilon=(1e-3,5e-4,2.5e-4). These decrease and meet
the frozen 1e-5 bound; no tolerance relaxation was needed. The final step is
near a floating-point cancellation plateau. This is an independent code
path for a deterministic off-shell jet, not an independent reviewer.

Negative algebraic controls detect the wrong regulator sign, omitted frame
contribution to Delta, missing second-order unit normalization and the use
of a metric-frozen velocity block as the constrained kinetic matrix.

## 5. Reproduction, provenance and next work

```
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_scalar_constraints.py
```

The executable writes its own named outputs and SHA-256 sidecars. It does
not overwrite the B1 inputs. The [summary](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_summary.json)
contains source pins, exact validation counts, every check, implementation
versions and output hashes. The [matrix export](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_matrices.json)
contains all unreduced/reduced formulas, and the [sample export](../../../Analysis/MasterTests/outputs/test_01_r4c1_scalar_constraints_samples.json)
retains both numerical trajectories' kinetic diagnostics.

Execution history: the first launch stopped at a syntax error before any
scientific calculation; this was corrected. The first completed run passed
67 checks. During the supplementary certificate calculation, a costly generic
symbolic determinant run was stopped before writing new receipts; it was
replaced by the exact two-by-two block determinant identity. The final run
passes 71 checks. Local optimizer logs preserve these attempts; no scientific
failure was hidden and no numerical acceptance condition was loosened.

Inherited unreviewed dependencies: R9-MT1-VARIATION and R9-MT1-B1. New result:
R9-MT1-S1. Pending review alone does not prevent using these matrices in
the next bounded scientific calculation. Later correction must propagate
to dependent calculations. The old ten-receipt reviewer snapshot remains
historical: it did not contain S1 and does not constitute S1 review.

Next: freeze a scalar gradient/characteristic and evolving-mode contract,
using K,M,V and the same action/background. Retain time derivatives of the
matrices and distinguish dust/Jeans growth from ghost or gradient instability.
The k=0 sector and singular constraint branches need separate treatment.
This is not the TOP-X4 fixed-global-charge physical-Hessian programme and
does not close its stress/state/gravity/parity/constraint requirements.

No reviewer dispatch, target-data fit, parameter retuning, commit, push or
publication occurred. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED. Tests 1-3 remain active, not completed.
