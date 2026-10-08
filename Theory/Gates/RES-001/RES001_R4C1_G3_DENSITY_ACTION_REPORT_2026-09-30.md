# R4C1-G3D: physical density action and canonical sign interpretation

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / formal G3 slow branch.
Review DEFERRED; gate effect NONE; physics_pass=false.

## Decision and affected use

The density-action audit passes **172/172 local checks** and both artifacts
replay byte-identically. The physical leading dust-density coordinate has

\[
 K_D=\frac{a^5\rho_m}{k^2}>0
\]

on the registered domain. Its time-dependent canonical transformation and
first-order action boundary identity are verified, not assumed. The negative
G3A frame-coordinate coefficient is unchanged. It is **not by itself a
wrong-sign dust-kinetic rejection**.

This resolves the formal branch's density-kinetic interpretation; it does
not supply a positive-definite Hamiltonian or all-sector energy theorem.
The density mass is negative, and its growing-density mechanism agrees with
the formal GR dust control. Physical EFT validity, arbitrary fast-wave data,
full constraints/quantum interpretation and a healthy continuous **full**
GR limit remain substantive requirements.

The new result refines the interpretation of
[G3A](RES001_R4C1_G3_SLOW_ACTION_REPORT_2026-09-30.md) and
[G3F](RES001_R4C1_G3_FINITE_K_REPORT_2026-09-30.md) without rewriting either.
Their negative frame-based action coefficient and ordered-basis symplectic
sign remain correct. A time-dependent phase transformation mixes coordinate
and momentum; its Hamiltonian includes explicit boundary/time terms.
Opposite second-order kinetic signs in those different coordinates are not
a choice to reverse the overall action sign.

## Registered assumptions and map

Follow the unchanged [G3D contract](RES001_R4C1_G3_DENSITY_ACTION_CONTRACT_2026-09-30.md).
It was frozen before executable validation and new numerical sampling, but
after analytic planning from the existing frozen maps. No claim of an
observational preregistration or a blind pre-algebra discovery is made.

Work at fixed k,eta, with X=sqrt(eta)*chi/k and v=chidot. The inherited action is

\[
 L_\chi=\frac{\kappa}{2}(v^2-m_E\chi^2),\qquad
 \kappa=-\frac{12-\eta}{k^2}.
\]

The physical leading density contrast is D=f chi+g v, with

\[
 g=\frac{12-\eta}{\sqrt6\,a^{5/2}\rho_m},\qquad
 f=g s,\qquad s=\beta\dot\psi-\frac{H}{2},\qquad
 \beta=\frac{2\eta^2}{5}.
\]

The full G3S background flow, including
rhodot=(-3H+beta*psidot)rho, yields gdot=-f exactly. Differentiating with the
slow generator gives

\[
 \dot D=h\chi,\qquad h=\frac{\sqrt6}{a^{5/2}},\qquad
 T=\frac{\partial(D,\dot D)}{\partial(\chi,v)}
   =\begin{pmatrix}f&g\\h&0\end{pmatrix},
 \qquad \Delta_D=\det T=-\frac{12-\eta}{a^5\rho_m}<0.
\]

This is the density/derivative phase map, not G3E's different
density/comoving-velocity map. Confusing their determinants would give an
incorrect sign interpretation. The inherited two-form transforms as

\[
 \kappa\,d\chi\wedge dv
   =K_D\,dD\wedge d\dot D,\qquad K_D=\kappa/\Delta_D.
\]

The determinant and kinetic coefficient have the displayed signs throughout
0<eta<=1, a,rho_m,k>0, subject to the inherited H,C and auxiliary-rank
conditions. There is no extra density phase-map zero inside this domain.
At rho_m=0 or a=0, the density map is undefined; k=0 invalidates the
normalization. The inherited H=0 gauge boundary and eta=0 auxiliary rank
change remain excluded even though some density coefficient formulas have
a smooth formal extension. The extrapolated eta=12 zero lies outside the
registered domain and also destroys Mc2. No singular boundary is inverted.

## Generator and properly normalized action

The transformed generator (Tdot+T B) T^-1, with
B=[[0,1],[-m_E,0]], gives

\[
 \ddot D+\Gamma_D\dot D+M_D D=0,\qquad
 \Gamma_D=2H+\beta\dot\psi,\qquad
 M_D=-\frac{\rho_m}{2M_c^2},\qquad M_c^2=1-\eta/12.
\]

The quantity Mc2 is the background effective Planck coefficient, not G3S's
mixing matrix. The symplectically fixed K_D satisfies
K_D_dot/K_D=Gamma_D. Thus the action is

\[
 L_D=\frac{K_D}{2}(\dot D^2-M_D D^2),\qquad
 P_D=K_D\dot D,\qquad
 H_D=\frac{P_D^2}{2K_D}+\frac{K_D M_D D^2}{2}.
\]

No arbitrary integrating factor is used to choose the kinetic sign.

To prove equivalence off shell in the **slow first-order phase action**,
treat chi and its momentum P_chi=kappa*v as independent variables. Set
D=f*chi+g*v and P_D=K_D*h*chi=-kappa*chi/g, and use the generating boundary

\[
 {\cal F}=\kappa\left(\chi v+\frac{s\chi^2}{2}\right).
\]

The phase-gradient identity and the explicit time-dependent Hamiltonian
identity both hold:

\[
 P_\chi\,d_z\chi-P_D\,d_zD=d_z{\cal F},\qquad
 H_D=H_\chi+P_D(\partial_t D)_z+(\partial_t{\cal F})_z.
\]

Consequently the full first-order actions differ by dF/dt for arbitrary
phase paths. The proof does **not** set chi_path_dot=v before checking that
identity. Algebraic elimination of P_D then gives the second-order L_D and
its Euler equation. An independent regular rational coefficient-jet check
also verifies the canonical/boundary identities. This is an off-shell
phase-path identity on the inherited background, not a new claim of a
fully renormalized spacetime action.

## Energy interpretation and GR control

The density Hamiltonian Hessian in (P_D,D) is
diag(1/K_D,K_D*M_D). Since K_D>0 and M_D<0, it is **indefinite with positive
kinetic weight**, not positive definite. Its mass/potential sign produces
density growth; it does not mean a negative density kinetic coefficient.

The energy balance is

\[
 \left.\frac{dH_D}{dt}\right|_{\rm EOM}
 =-\frac{\dot K_D}{2}\dot D^2
   +\frac{(K_D M_D)^{\displaystyle\cdot}}{2}D^2.
\]

The background and canonical transformation are time dependent. Do not
identify either reduced Hamiltonian with a conserved global gravitational
energy, or infer a stationary quantum norm from these coefficients.

In the separately declared **formal GR dust coefficient control**, eta->0,
no transfer, zero scalar/force velocities, rho_m=3H^2 and
Hdot=-3H^2/2 in the MP2=1 chart give

\[
 K_D^{\rm GR}=\frac{3a^5H^2}{k^2}>0,\qquad
 \ddot D+2H\dot D-\frac{3H^2}{2}D=0.
\]

Both D=a and D=a^(-3/2) solve this equation exactly. The kinetic logarithmic
derivative is 2H, also checked exactly. This recovers a positive dust kinetic
coefficient alongside the prior GR density growth/decay result. It does not
turn the original eta=0 rank-changing full-system endpoint into a regular
inverse or prove all-sector decoupling.

## Entire registered numerical sample and verification

Sample all six sealed G3 eta values, both archived background methods,
t=(0,.5,1,2,3,4), and k=(20,40,80): **216 coefficient events**. Every event has
K_D>0, Delta_D<0 and M_D<0. The result retains every event and all 172 checks:
28 exact/domain/control checks plus 144 grouped numerical checks.

- Minimum K_D: 3.125e-5.
- Largest density mass: -9.988117314e-4, still negative.
- Minimum sampled friction: 0.2029508255; this is not a general-domain
  friction-sign theorem for arbitrary psidot.
- Worst normalized coefficient discrepancy: 8.684e-17.
- Worst separately evaluated Hamiltonian-boundary discrepancy: 1.191e-18.

Numerical boundary checks use chi=.3,v=-.2 as algebraic evaluation points,
not a claim that those amplitudes constitute physical linear perturbation
histories. The rational check is a coefficient jet, not an additional
on-shell cosmological initial condition. Existing G3 trajectories are read
without invoking their old receipt-writing main(). No observed a0,H0 or
target dataset enters the calculation.

## Provenance and reproduction

| Artifact | SHA-256 |
| --- | --- |
| Frozen contract | `0ff843db7c1887fea71e307fd8801841427628d0426bf8f9bd83e4b78e9c5758` |
| Executable | `1a855ad2a5bbafbee0ad7164604a210f5a236529896cbbab5a62173d6e822fc8` |
| Attempt 01 summary | `c309ec0fbd3e3c3bff9ac05c86c4c0fe5f5e37edd5cc66a2a37cabb9bc6e5b72` |
| Formula export | `68aaddb629ba729aa197804d46f8228d509111195757288221d21bb7f7a692e8` |

Both summary.json and formulas.json recompute byte-identically. The
executable verifies direct/inherited pins, refuses existing output
directories and replays without writes. Local logs remain ignored.

~~~powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_density_action.py --replay
~~~

## Disposition and remaining requirements

PROCEED_PROVISIONALLY applies to the equivalent formal density action,
its nonzero phase-map determinant and positive kinetic coefficient on
the registered domain, and the formal GR dust control. The frame-based
negative kinetic coefficient alone must not be used as a dust-ghost verdict.

All-sector stability, a physical EFT cutoff/window, arbitrary fast-wave
data, controlled physical finite-k density reduction, uniform eta endpoint
and healthy continuous full GR remain unverified. This does not complete
canonical Test 1 or the independent weak-field/blind-coefficient requirements
of Tests 2 and 3. No positive-definite energy or quantum-norm certificate
is issued.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A/G3F and their
scope/review debt. Canonical Tests 1-3 HOLD_SUBSTANTIVE; claim CONDITIONAL,
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage 4A CLOSED; TOP-X4 unchanged. Prior scientific inputs and receipts
remain untouched. No PDF edit, provider dispatch, commit, push or publication.

