# TOP-X4 / KK-001 A1 action-selection ledger

**Date:** 2026-09-06  
**Status:** `FROZEN_CONTROL_PARENT`; background verified control-only  
**Gate effect:** none  
**Canonical effect:** none; canonical ITSM spatial topology remains `T3`

## 1. Purpose and scope

This ledger freezes one complete, bounded five-dimensional control theory for
the A1 background test. It does not declare the control to be the physical
ITSM parent. Its real scalar is a bulk matter proxy chosen so that the matter
stress tensor and future inter-sector transfer can be derived from an
off-shell action rather than inserted phenomenologically.

The test is blind to `a0`, `H0`, SPARC, a target `2*pi` coefficient, a desired
compactification radius and a desired `Q^mu`.

## 2. Alternatives considered

| Candidate | Matter realization | Disposition | Reason |
|---|---|---|---|
| `X4-C0` | No dynamical gravity or matter | Retain as kinematic comparator | Cannot pass A1 because a finite-density Minkowski background is generally off shell once gravity is restored |
| `X4-I1C` | Bulk real scalar proxy | **Selected and frozen for the control** | Complete local action, unambiguous stress tensors, no brane junction conditions, and an explicit nested zero-portal limit |
| `X4-B1` | Brane-localized matter | Deferred | Adds a brane action, localization mechanism and junction conditions before the bulk control is understood |
| `X4-G1` | Gauged condensate plus bulk matter | Deferred | Adds a gauge field, Gauss constraint and Higgs sector not required for the first global-charge control |

Results may not be moved between these candidates without a new ledger.

## 3. Frozen conventions

- Signature: `(-,+,+,+,+)`.
- Coordinates: `x^A=(t,x^1,x^2,x^3,y)` with every spatial coordinate
  dimensionless and periodic; `y ~ y+2*pi`.
- Metric background:

  \[
  ds_5^2=-N(t)^2dt^2+a(t)^2\sum_{i=1}^3(dx^i)^2+b(t)^2dy^2.
  \]

  Thus the fourth-circle radius is `b(t)` and circumference is `2*pi*b(t)`.
- Condensate symmetry: global `U(1)`.
- Matter-proxy symmetry: `chi -> -chi`.
- Finite-density ensemble: fixed nonzero global charge. No chemical potential
  is inserted into the covariant action; the phase velocity is dynamical.
- Initial A1 background sector: zero winding, `w=0`. Integer `w` is retained
  in the equations as a later registered control.
- All fields are bulk fields. No four-dimensional portal or brane term is
  permitted in this parent.

## 4. Frozen off-shell action

Let `s=Phi* Phi`. The control action is

\[
\begin{aligned}
S_{I1C}=\int d^5x\sqrt{-G}\bigg[&
 \frac{M_5^3}{2}\,{}^{(5)}R
 -G^{AB}\partial_A\Phi^*\partial_B\Phi-U_5(s)\\
&-\frac12G^{AB}\partial_A\chi\partial_B\chi-W_5(\chi)
-\frac{g_5}{2}s\chi^2\bigg],
\end{aligned}
\]

with

\[
 U_5(s)=U_0+m_\Phi^2s+\frac{\lambda_{\Phi5}}{2}s^2,
 \qquad
 W_5(\chi)=\frac{m_\chi^2}{2}\chi^2+
 \frac{\lambda_{\chi5}}{4!}\chi^4.
\]

The fields have dimensions

\[
 [\Phi]=[\chi]=\frac32,\quad [M_5]=1,\quad
 [U_0]=5,\quad[m_\Phi^2]=[m_\chi^2]=2,
 \quad[\lambda_{\Phi5}]=[\lambda_{\chi5}]=[g_5]=-1.
\]

For the bounded numerical control, positive scalar masses and nonnegative
quartics are used. This is a stability prior for the control, not an empirical
fit or a claim that the same potential yields the required ITSM infrared law.

## 5. Homogeneous reduction to be verified

Use

\[
 \Phi(t,y)=\frac{\rho(t)}{\sqrt2}
 e^{i\theta(t)+iwy},\qquad \chi=\chi(t),\qquad w\in\mathbb Z.
\]

After varying the covariant action and only then fixing `N=1`, define

\[
 H_a=\frac{\dot a}{a},\quad H_b=\frac{\dot b}{b},\quad
 \mu=\dot\theta,\quad \Theta=3H_a+H_b.
\]

The registered field equations are

\[
 \ddot\rho+\Theta\dot\rho-\rho\mu^2
 +\frac{w^2}{b^2}\rho+m_\Phi^2\rho
 +\frac{\lambda_{\Phi5}}{2}\rho^3
 +\frac{g_5}{2}\rho\chi^2=0,
\]

\[
 \frac{d}{dt}\left(a^3b\rho^2\mu\right)=0,
\]

\[
 \ddot\chi+\Theta\dot\chi+m_\chi^2\chi
 +\frac{\lambda_{\chi5}}{6}\chi^3
 +\frac{g_5}{2}\rho^2\chi=0.
\]

Writing `K_t=(dot(rho)^2+rho^2 mu^2+dot(chi)^2)/2`,
`K_w=rho^2 w^2/(2b^2)` and
`V=U_5+W_5+g_5 rho^2 chi^2/4`, the energy density and principal pressures are

\[
 \varepsilon=K_t+K_w+V,\qquad
 p_a=K_t-K_w-V,\qquad p_y=K_t+K_w-V.
\]

The registered Einstein equations are

\[
 3H_a(H_a+H_b)=\frac{\varepsilon}{M_5^3},
\]

\[
 -2\dot H_a-\dot H_b-3H_a^2-2H_aH_b-H_b^2
 =\frac{p_a}{M_5^3},
\]

\[
 -3\dot H_a-6H_a^2=\frac{p_y}{M_5^3}.
\]

The last two equations reduce to the standard isotropic five-dimensional
FLRW pressure equation when `H_a=H_b` and `p_a=p_y`.

## 6. A1 numerical control and pass rule

The deterministic control must integrate the equations from registered
dimensionless initial data satisfying the Hamiltonian constraint. It passes
only if:

1. the solver completes the registered interval without a non-finite field or
   `rho=0` singularity;
2. the Hamiltonian-constraint residual remains below `1e-8` in normalized
   absolute units;
3. the global charge `a^3 b rho^2 mu` is conserved to relative error below
   `1e-9`;
4. the analytic continuity residual is below `1e-10`;
5. the zero-portal declaration is a literal nested `g5=0` limit;
6. the source contains none of the forbidden observational target tokens.

Passing means only that this frozen control action possesses the tested
on-shell finite-charge background. It does not establish perturbative health,
radion stabilization, a physical matter model, nonzero exchange, `K_Q`, `V`,
screening, lensing or any observational prediction.

## 7. Predeclared A2/A3 kill criteria

Freeze or reject this route if later reduction finds a physical ghost, an
uninterpreted tachyon, a singular zero-charge/zero-mode limit, no hierarchy
between the KK gap and EFT cutoff, a failed decompactification limit, or no
stable/metastable radion domain. A running `b(t)` is allowed in A1 but is not
radion stabilization.
