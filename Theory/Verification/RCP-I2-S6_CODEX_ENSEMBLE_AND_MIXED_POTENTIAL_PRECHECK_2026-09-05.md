# RCP-I2-S6 Codex ensemble and mixed-potential precheck

**Date:** 2026-09-05  
**Branch:** `recovery/v12-core-architecture`  
**Role:** Codex independent canonical precheck  
**Status:** `PRELIMINARY_DERIVATION_PENDING_SEALED_EXTERNAL_COMPARISON`  
**Reasoning:** High  
**Gate effect:** none

## 1. Purpose and boundary

This is the Codex-side calculation to be compared later with sealed Grok
`G-A5` and Antigravity `A-B4`. It was performed before either new response was
received. It does not freeze a canonical action and does not begin metric
constraint reduction.

The calculation addresses two holds from the G-A4/A-B3 adjudication:

1. distinguish fixed chemical potential from fixed total charge;
2. determine how a symmetry-allowed quartic changes the pure-sextic `3/2`
   phase-EFT result.

Binding status remains `MAT-001 BLOCKED`, `UVIR-003 IN_PROGRESS`,
`K_Q NOT_DERIVED`, and `V NOT_COMPUTED`.

## 2. Declared scalar class

On a fixed background, use

\[
\mathcal L=-|\partial\Phi|^2-U(s),
\qquad
s=|\Phi|^2=\rho^2/2,
\]

with

\[
U(s)=m^2s+\frac{\lambda_4}{2}s^2+\frac{\kappa_3}{3}s^3.
\]

For `Phi=(rho/sqrt(2)) exp(i Theta)` the conserved homogeneous charge density
in the adopted normalization is

\[
n=j^0=2\mu s.
\]

This precheck restricts the explicit branch analysis to
`kappa_3>0`, `lambda_4>=0`, `s>0`. Negative-quartic metastable branches require
a separate global-potential analysis and are not classified here.

## 3. Ensemble distinction

### 3.1 Fixed chemical potential

For `Theta=mu t`, the homogeneous grand-potential density is

\[
\Omega_\mu(s)=U(s)-\mu^2s.
\]

Stationarity and local homogeneous stability require

\[
U_s(s_0)=\mu^2,
\qquad
U_{ss}(s_0)>0.
\]

For the mixed potential,

\[
\mu^2-m^2=\lambda_4s_0+\kappa_3s_0^2,
\qquad
U_{ss}=\lambda_4+2\kappa_3s_0.
\]

### 3.2 Fixed total charge

At fixed charge density `n` in a fixed volume, eliminate
`mu=n/(2s)`. The homogeneous energy density is

\[
\varepsilon_n(s)=\frac{n^2}{4s}+U(s).
\]

Its stationary equation is the same background equation,

\[
\frac{\partial\varepsilon_n}{\partial s}=0
\quad\Longleftrightarrow\quad
U_s=\frac{n^2}{4s^2}=\mu^2,
\]

but its fixed-charge homogeneous Hessian is

\[
\frac{\partial^2\varepsilon_n}{\partial s^2}
=\frac{2\mu^2}{s}+U_{ss}.
\]

For `lambda_4>=0`, `kappa_3>0`, `s>0`, both displayed ensemble Hessians are
positive. This does not make the ensembles identical: fixing total charge
removes or constrains the spatially homogeneous charge fluctuation. Nonzero
momentum local modes should agree in the thermodynamic limit only when the
charge susceptibility is positive:

\[
\frac{dn}{d\mu}=2s+\frac{4\mu^2}{U_{ss}}>0.
\]

The treatment of that global zero mode must be declared in any action freeze.

## 4. Exact stable mixed-potential branch

Let

\[
\Delta=X_R-m^2.
\]

Algebraic radial elimination gives

\[
\Delta=\lambda_4s+\kappa_3s^2.
\]

For the declared nonnegative-coupling branch,

\[
s_+(\Delta)=
\frac{-\lambda_4+\sqrt{\lambda_4^2+4\kappa_3\Delta}}
{2\kappa_3},
\qquad \Delta\ge0,
\]

and

\[
U_{ss}(s_+)=\sqrt{\lambda_4^2+4\kappa_3\Delta}>0.
\]

Using the stationary equation, the exact leading-derivative pressure is

\[
P(X_R)=\frac{\lambda_4}{2}s_+^2+
\frac{2\kappa_3}{3}s_+^3.
\]

The radial mass and phase sound speed are

\[
M_\sigma^2=2s_+U_{ss},
\qquad
c_s^2=\frac{s_+U_{ss}}{s_+U_{ss}+2\mu^2}.
\]

These quantities are positive on the declared branch, but this is still a
fixed-background scalar statement.

## 5. Quartic-to-sextic crossover

For small positive `Delta`,

\[
s_+=\frac{\Delta}{\lambda_4}
-\frac{\kappa_3\Delta^2}{\lambda_4^3}+O(\Delta^3),
\]

and

\[
P=\frac{\Delta^2}{2\lambda_4}
-\frac{\kappa_3\Delta^3}{3\lambda_4^3}+O(\Delta^4).
\]

Thus every nonzero positive quartic restores a quadratic phase-EFT behavior
close enough to the zero-density branch.

Sextic dominance requires parametrically

\[
4\kappa_3\Delta\gg\lambda_4^2,
\]

where

\[
P=\frac{2}{3\sqrt{\kappa_3}}\Delta^{3/2}
-\frac{\lambda_4}{2\kappa_3}\Delta+\cdots.
\]

Therefore:

- exact pure `3/2` behavior requires `lambda_4=0` in this truncation;
- a nonzero quartic permits only an asymptotic sextic-dominated interval;
- near `Delta=0`, the effective exponent is `2`, not `3/2`;
- whether the sextic-dominated interval is physically controlled also depends
  on radial-gradient corrections, higher operators and the Wilsonian cutoff.

## 6. Preliminary disposition

The algebra does not yet kill the S6 route, but it narrows the claim:

`S6_SHAPE_CONDITIONAL_ON_A_SEXTIC_DOMINANCE_WINDOW`.

The existence of a nonempty *physical* window is unresolved until all of the
following are simultaneously shown:

1. `4 kappa_3 Delta >> lambda_4^2`;
2. frequencies and momenta remain below `M_sigma`;
3. radial-gradient corrections remain perturbative;
4. field amplitudes and energies remain below a declared Wilsonian cutoff;
5. higher symmetry-allowed operators do not dominate;
6. a renormalization condition or symmetry explains the required quartic
   hierarchy without observational input.

No result here supplies a spatial `Y^(3/2)` force operator, screened charge,
matter coupling, metric pole residue, `K_Q`, `V`, `a_0`, topology or reservoir
current.

## 7. Required comparison when external reports return

Codex must compare, equation by equation:

- the fixed-`mu` and fixed-charge Hessians;
- the treatment of the homogeneous charge mode;
- all real branches of the mixed potential;
- the exact pressure and crossover expansion;
- the meaning of the generated quartic estimate;
- the claimed nonempty EFT hierarchy;
- any Antigravity semantic check that purports to validate these statements.

Disagreement, a free hierarchy or a missing cutoff remains a mandatory hold.

