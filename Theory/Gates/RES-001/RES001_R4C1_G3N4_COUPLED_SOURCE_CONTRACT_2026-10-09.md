# R4C1-G3N4: unit-constrained coupled second-order source ledger

Date: 9 October 2026. Version 1. Test-1 continuation after G3N3.
Conditional; review DEFERRED; PROCEED_PROVISIONALLY within this calculation.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Objective and exact boundary

Assemble the sources driving the second-order metric/frame/condensate/
reservoir/force/dust/regulator response to the actual first-order transverse
G3V direction. Derive them by varying the frozen action before imposing the
first-order shift solution. Supply the source ledger and consistency controls
needed to solve the coupled response. This is not that response solution,
full nonlinear evolution, a physical Hessian or a canonical Test-1 pass.

Frozen action SHA-256 81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
G3N3 report SHA-256 7111692a94582e3a1d44f0ca5fa3a5a2a1a4550db009beecc851e841119fd32b;
G3N3 final summary SHA-256 ee6683f0b99a087f009e29c653e719fb86647242182c58beea7f44b5e9998871.
G3V report SHA-256 952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27;
G3V formulas SHA-256 1dc1d63b3b54a59f7236051125c028006b3c74ff24c5a16f99d2879fd6a90358.
Carry all inherited pins, original failed assertions and three absent sidecars.

## Bivariate variation, not a new action

Use independent formal parameters e (first-order vector amplitude) and d
(linear response variation). Coefficient e^2 d in the analytic action gives
the quadratic source functional; later d has perturbative size e^2. Keep
all response values and required derivatives independent:

```text
N=1+d alpha; h_ij=a^2(delta_ij+d M_ij)
N^i=(e B delta_iy+d S_i)/a
v^i=(e W delta_iy+d V_i)/a
gamma=sqrt(1+h_ij v^i v^j)
n^t=gamma/N; n^i=v^i-N^i gamma/N
U=(1+d nu)n; lambda_U=lambda_0+d Lambda_U
u=u_0+d du; v=v_0+d dv; r=r_0+d dr
psi=psi_0+d Pi; tau=tau_0+d T
epsilon_m=epsilon_0+d E_m; z_aux=d Z.
```

The inherited geometry depends on (t,z). Retain six symmetric M_ij, three
S_i, three V_i, alpha, du,dv,dr,Pi,T,E_m,Z,nu,Lambda_U: 22 response fields.
The independent norm variation nu is retained in L_U and its multiplier;
the normalized n in force/alignment/regulator is the frozen off-shell
extension. Do not normalize the L_U invariants themselves or omit its
normal equation. Unit variation fixes nu; the normal equation determines
the multiplier response in the later coupled solve.

The cosmic-time background has N=1,tau_0_dot=C=exp(beta psi_0), not tau=t.
Use the four original frame invariants, EH+GHY ADM bulk, Cartesian scalar
kinetics and frozen potentials/portal, alignment, temporal force kinetic,
dust action and first-derivative auxiliary regulator. Spatial Ricci depends
on h_ij, not e on this inherited first-order chart: prove its e^2 d coefficient
is zero rather than treating it as absent from the theory. Fixed/periodic
boundaries retain the original GHY and regulator surface convention.

## Required sources and controls

1. Verify the ADM inverse and normalized-frame identities through e^2 d.
   Derive the coefficient e^2 d separately for each analytic action sector.
   Each response-field source is the Euler derivative of that functional,
   divided by background a^3. Retain time coefficient derivatives, the 3H
   volume term, spatial derivatives and normal-frame/multiplier equations.
2. Export both source-functional coefficients and all 22 Euler sources,
   before and after B=-eta W/(8-eta). The existing first-order shift relation
   is applied only after variation. Derive/compare the zero-response e^2
   action with the complete G3V vector quadratic action and its regular
   shift constraint. No metric-frozen or regulator-dropped substitution.
3. Recover the G3N3 direct regulator source b[psi_dot W W_dot+
   (psi_ddot+2H psi_dot)W^2] as the Z Euler source. Independently compare the
   temporal-kinetic and alignment scalar-response sources with direct field
   variation, retaining the current-dependent u/v source.
4. Check on-shell quadratic-source temporal and longitudinal spatial
   diffeomorphism identities in the declared G3 family. Derive their gauge
   weights in the ADM/boost chart. Retain background equations and the
   linear vector equation; a source-only identity is not expected off shell.
   Failed identities remain explicit and prevent claiming a complete ledger.
5. Preserve homogeneous sources without Laplacian inverses or nonzero-mode
   Schur formulae. No finite-mode invariant response or solved initial data
   is presumed from the source construction.

Treat -A Y^(3/2) separately, without an ordinary cubic Taylor expansion.
Derive its leading transverse Euler source at both signs of e. Other
second-order force sources must be tested, not assumed. For the parent's
W=cos(chi)+(1/3)cos(3chi), derive all parity restrictions and the exact
general odd Fourier coefficient of W|W|; compare odd m=1,3,...,31 with
independent 50-digit quadratures to normalized error <=1e-12. Retain the
infinite harmonic tail; do not stop at the first/third harmonic. A rigorous
tail bound may be exported if derived; it is not an EFT cutoff.

Independent analytic mixed-variation controls use two generic off-shell
response jets, exact unexpanded ADM/frame geometry and 50-digit mpmath.
For e,d=(1e-3,1e-3),(5e-4,5e-4),(2.5e-4,2.5e-4), compare the even-e/odd-d
mixed difference with the symbolic e^2 d coefficient. Final normalized
error <=1e-5, decreasing across steps or all <=1e-12 at a numerical floor.
The nonanalytic sector is evaluated separately at its original absolute
value; it is not removed from the source ledger by the analytic control.

## Output, integrity and unresolved physics

New versioned executable and formula/source/control receipts with matching
sidecars; every failed/unknown assertion retained; no existing outputs
overwritten; exact read-only replay. A repair needs a new version preserving
the original attempt, not relaxed tolerances or a changed action.

All-sector sources in the inherited plane-wave chart are not all-sector
solutions on general T3 data. Compatible response and initial data, complete
constraint reduction, Cauchy/DAE domain, physical cutoff, stability and healthy
continuous GR recovery remain substantive inputs. No source coefficient is
a canonical numerical K_Q or computed matching V. Review alone is deferred;
missing physics cannot be deferred into an observational or publication pass.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action change, manuscript/PDF edit, vault mutation, provider dispatch,
commit, push, canonical promotion or publication.
