# R4C1-T2P3: the coupled B1 linear branch has no square-root asymptote

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
The [T2P3 contract](RES001_R4C1_COUPLED_LINEAR_LIMIT_CONTRACT_2026-09-29.md)
(SHA-256 `84b391bb6da5a6ceabb6feefa03b48f754550fc7f436bfd62033ecdb24267bdb`)
was frozen before the executable run. The action, B1 background, S1/S2
matrices, four modes and numerical acceptance thresholds were not changed.
No observed acceleration, Hubble or galaxy data enter this calculation.

**Decision:** The complete *linear* scalar metric/frame/dust system about
the registered interacting B1 background has a finite, source-linear
response for each fixed nonzero Fourier mode on `[0,4]`. A fixed positive
square-root correction cannot be its arbitrarily small-amplitude
asymptote. This excludes a proposed derivation *from this linear branch*,
not a nonlinear/intermediate ITSM regime or another background. The new
34/34 local checks verify the gauge dictionary, a nonzero Jordan-dust
source, source pins and stored transfer interfaces. They do not prove
the continuum theorem by counting checks and do not evolve a new
nonlinear inhomogeneous solution. `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`,
`canonical_Test2_pass=false`.

## 1. Matter-metric potential dictionary with the shift retained

The [S1 scalar reduction](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md)
uses signature `-+++`, spatially flat scalar gauge and
`q=(du,dv,dr,dpsi,dtau,w)`, with lapse `alpha cos(kx)` and longitudinal
shift `S sin(kx)`. Here `k=2*pi*n`, `n!=0`; the homogeneous B1 frame and
conformal dust metric are `U=partial_t` and `g_tilde=C^2 g`,
`C=exp(beta*psi_bar)`. The first-order matter-metric components are

\[
\delta\tilde g_{00}=-2C^2(\alpha+\beta\,\delta\psi)\cos(kx),\quad
\delta\tilde g_{0x}=C^2a^2S\sin(kx),\quad
\delta\tilde g_{xx}=2C^2a^2\beta\,\delta\psi\cos(kx).
\]

Apply the infinitesimal time-coordinate shift
`xi^0=T cos(kx)`, `T=a^2 S/k`, and subtract the Lie derivative of the
*background matter metric*. Its `00`, `0x` and `xx` components are

\[
-2C^2(\dot T+\beta\dot{\bar\psi}T)\cos(kx),\quad
C^2kT\sin(kx),\quad
2C^2a^2(H+\beta\dot{\bar\psi})T\cos(kx).
\]

The transformed shift is zero. Defining the Newtonian-gauge matter
potentials by `g_tilde_00=-C^2(1+2 Phi_m cos(kx))` and
`g_tilde_xx=C^2a^2(1-2 Psi_m cos(kx))` gives

\[
\boxed{\Phi_m=\alpha+\beta\delta\psi-\dot T
                 -\beta\dot{\bar\psi}T},\qquad
\boxed{\Psi_m=(H+\beta\dot{\bar\psi})T-\beta\delta\psi}.
\]

S1's *retained dust constraint* is
`alpha=dot(dtau)/C-beta*dpsi`, so equivalently
`Phi_m=dot(dtau)/C-dot(T)-beta*psi_bar_dot*T`. Reading only the lapse or
only `beta grad(dpsi)` as the physical coupled force would omit the
shift/time-slicing terms. In the nonrelativistic matter-frame Newtonian
limit a potential-gradient contribution is proportional to
`k*|Phi_m|/(Ca)`; this report does **not** establish that the background,
time dependence and EFT domain admit a static-galaxy limit. The
independent sign controls reject reversing `T`, omitting `dot(T)`, and
omitting the background conformal derivative.

## 2. A nonzero compensated matter source exists on the regular chart

Write the Jordan-frame dust rest density as `epsilon_bar=rho_m/C^4`.
From the B1 flow, `dot(epsilon_bar)=-3(H+beta*psi_bar_dot)epsilon_bar`.
The scalar density in Newtonian gauge is therefore
`depsilon_N=depsilon-dot(epsilon_bar)*T`. This is the first-order source
for an **auxiliary**, fixed-positive-`G_ref` periodic Poisson comparison;
it is not an action-derived interacting-B1 Poisson law.

For an explicit consistent linear initial-data direction at `t=0`, set
`dtau=1` and all other retained `q` and `qdot` amplitudes to zero, then
solve the S1 auxiliaries. Let
`c_L=c1+c2+c3` and
`M_c^2=M_P^2+M_U^2(c1+3c2+c3)/2`. Exact differentiation of the exported
auxiliary expressions gives

\[
\frac{\partial\delta\epsilon}{\partial\delta\tau}
=-\frac{2HM_c^2\rho_m}{C^5M_U^2c_L},\qquad
\frac{\partial S}{\partial\delta\tau}
=\frac{\rho_m}{CM_U^2c_L k}.
\]

At the registered B1 initial values `a=C=1`, `rho_m=1/5`,
`psi_bar_dot=1/5`, `beta=2/5`, `M_c^2=11/10`,
`M_U^2 c_L=1/15`, `H_0=sqrt(3469/4620)>0` and `k=2*pi`, this yields

\[
\delta\epsilon_N
=-\frac{33}{5}H_0
 +\frac{9}{20\pi^2}\left(H_0+\frac{2}{25}\right)
=-5.6759094868558137\ldots\ne0.
\]

It is a compensated nonzero torus mode; scaling it sufficiently small
preserves positive total dust density. At fixed positive `G_ref`, the
auxiliary Poisson equation
`-k^2 Phi_bar=4*pi*G_ref*(Ca)^2*depsilon_N` has a
nonzero baryonic acceleration amplitude proportional to the initial
amplitude. No `G_ref` or galactic acceleration is fitted or used to
select a coefficient.

## 3. Exact finite-mode linear obstruction and its boundary

On aligned B1, `Y` begins at second perturbative order. The force term
`-A Y^(3/2)` is cubic in the perturbation norm and has **zero second
variation** there; it is not replaced by an analytic cubic Taylor
polynomial. The pinned S1 `K,M,V` and S2 canonical `G,W` exports contain
no `A`. The S1 auxiliary block is invertible for this nonzero `k` with
`b>0`, `M_U^2c_L>0`, `C>0`. Its kinetic form is positive on the chart.
The [B1G argument](RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md)
establishes `H,C,a,rho_m>0` and smooth homogeneous coefficients on
`[0,4]`. Thus, for **each fixed finite** nonzero mode, the S2 equation

\[
\ddot x+G(t,k)\dot x+W(t,k)x=0
\]

is an ordinary linear system with continuous coefficients and a unique
finite transfer matrix. Multiplying a consistent initial perturbation
by `lambda` multiplies every reconstructed first-order `q`, auxiliary,
matter-frame potential and dust density by exactly `lambda`. This is
not an infinite-mode well-posedness or EFT statement.

For the nonzero source above, let `g_bar,ref(lambda)=lambda*g_bar,ref(1)`
be its positive auxiliary baryonic acceleration amplitude, and let
`g_m(lambda)=lambda*g_m(1)` denote a finite first-order matter-potential
gradient amplitude at a fixed time/mode. Then

\[
\frac{g_m(\lambda)-g_{\rm bar,ref}(\lambda)}
     {\sqrt{g_{\rm bar,ref}(\lambda)}}
=\sqrt{\lambda}\,
  \frac{g_m(1)-g_{\rm bar,ref}(1)}
       {\sqrt{g_{\rm bar,ref}(1)}}\longrightarrow0.
\]

A fixed positive `C_proj*sqrt(a0)` square-root term would require a
nonzero limit. Therefore the proposed weak-field expression cannot be
obtained by treating this coupled **linear** B1 response as its
arbitrarily weak-source limit. The argument is about first-order mode
amplitudes, **not** a pointwise radial-acceleration relation. A singular
nonlinear branch, finite intermediate source window, different
background or different action could behave differently. The current
candidate's full nonlinear metric/frame/dust/Euler solution and
quasistatic remainder have not been calculated, so Test 2 remains open.

## 4. Numerical/source controls and review boundary

The [write-once attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_t2p3_attempt_01/summary.json)
(SHA-256 `28a76334ca9af87658ccf4c8a3b8a18174b706a7bc327d08eaa3f5a84f2e1596`)
passes 34/34 local controls and replays byte-identically *in memory*.
The [executable](../../../Analysis/MasterTests/test_02_r4c1_coupled_linear_limit.py)
has SHA-256 `f747089197223f785872762336c2a834f677038d433b2449440758d6444fae25`.
It checks twelve direct source pins plus fifteen unique inherited S1/S2
sources and any present sidecars before calculating. The four archived
S2 mode transfers have finite `12x12` endpoints; DOP853/Radau endpoint
disagreements are at most `2.114e-7`, below the frozen `1e-5` threshold.
Multiplying a stored transfer by scaled initial vectors is a matrix
interface check, not a new independent integration or nonlinear test.

The pre-execution exploratory parser initially treated `beta`/`Lambda`
as SymPy built-ins and stopped before producing a scientific receipt.
Explicitly declaring those identifiers as symbols corrected the parser;
no frozen scientific input or threshold changed. The first executable
attempt passed without a failed receipt. The earlier S1/S2 failed and
corrected attempts retain their own history; this work does not erase it.

Later independent review must check the time-shift and conformal signs,
the Jordan-density/source derivation, inherited S1/S2 variational and
transfer calculations, and the strict distinction between linear
asymptotics and a physical nonlinear galaxy solution. Rule-9 review is
deferred, not cleared. The `2/3` projection, unique `C_chi`, `a0(z)`,
physical cutoff, complete constrained IVP, MAT-001, UVIR-003, Stage 4A,
Master Tests 1–3 and publication holds remain unchanged.
