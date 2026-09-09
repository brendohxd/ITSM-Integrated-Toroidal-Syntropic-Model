# TOP-X4 / KK-001 A2/A3 reduction and radion result

**Date:** 2026-09-06  
**Status:** `HOLD_TOPX4_A2A3_UNSTABILIZED_CONTROL`  
**A2 disposition:** `PARTIAL_FIXED_BACKGROUND_CONTROL_ONLY`  
**A3 disposition:** `HOLD_UNSTABILIZED_RADION`  
**Advance to A4:** false  
**Physics pass:** false  
**Gate effect:** none

## 1. Question tested

Does the exact frozen `X4-I1C` five-dimensional parent reduce to a healthy
four-dimensional KK/radion theory with a non-empty EFT domain and a stable or
metastable fourth-circle radius?

The answer for the frozen control is **no**. Several fixed-background
kinematic and scalar-sector results survive, but no stationary radion
background exists in the registered classical sector. Therefore a full
physical metric--radion--condensate pole calculation would be an expansion
about an off-shell background and is not permitted.

## 2. Independently verified Einstein-frame reduction

Let `R_ref` be a fixed reference radius, `r=R/R_ref` and
`ell_ref=2*pi*R_ref`. The Einstein-frame ansatz is

\[
 ds_5^2=r^{-1}g_{\mu\nu}dx^\mu dx^\nu
 +R_{\rm ref}^2r^2(dy+\mathcal A_\mu dx^\mu)^2.
\]

Direct construction of the five-dimensional Ricci scalar, followed by removal
of its explicit total derivative, gave

\[
 \sqrt{-G}\,{}^{(5)}R\ \doteq\
 \frac32R_{\rm ref}(\partial_t\ln r)^2
\]

on the flat time-dependent radion control. Consequently,

\[
 M_{\rm Pl}^2=\ell_{\rm ref}M_5^3,
 \qquad
 \sigma=\sqrt{\frac32}\,M_{\rm Pl}\ln r
\]

gives a positive canonical radion kinetic term. The independent symbolic audit
passed 6/6 exact checks; every simplified residual was zero.

For

\[
 \Phi(x,y)=\ell_{\rm ref}^{-1/2}
 \sum_{n\in\mathbb Z}\phi_n(x)e^{iny},
\]

the independently recovered four-dimensional Einstein-frame mass is

\[
 m_{\Phi,n}^2(r)=\frac{m_\Phi^2}{r}
 +\frac{n^2}{R_{\rm ref}^2r^3},
 \qquad
 \Delta_{\rm KK}=\frac{1}{R_{\rm ref}r^{3/2}}.
\]

The local vertices retain exact integer KK momentum conservation. For example,
`Phi* Phi Phi* Phi` contains only combinations satisfying

\[
 -n_1+n_2-n_3+n_4=0.
\]

The zero-density gravity spectrum has the standard bounded interpretation: a
four-dimensional massless graviton, graviphoton and radion at `n=0`, and the
massive KK graviton tower at nonzero `n`. This statement does not transfer to
the finite-density time-dependent background without the full constraint
reduction.

## 3. Fixed-background finite-density scalar comparator

For a static matter-only comparator with

\[
 \mu^2=m_\Phi^2+\frac{\lambda_{\Phi5}}2\rho_0^2,
 \qquad M_\rho^2=\lambda_{\Phi5}\rho_0^2,
\]

the amplitude--phase tower obeys

\[
 (\omega^2-p_n^2-M_\rho^2)(\omega^2-p_n^2)
 -4\mu^2\omega^2=0,
 \qquad
 p_n^2=k^2+\frac{n^2}{R^2}.
\]

The registered scan found no negative `omega^2`, retained the exact zero-mode
Goldstone root and gave

\[
 c_s^2=\frac{M_\rho^2}{M_\rho^2+4\mu^2}=\frac17
\]

for the dimensionless control. The `chi` proxy tower also remained positive,
with registered zero-mode mass squared `1.05`.

These are fixed-background scalar results only. They do not include the lapse,
shift, radion or metric constraints and therefore are not physical-pole
evidence.

## 4. Exact classical radion obstruction

For a static fourth radius, `H_b=dot(H_b)=0`, the three independent
five-dimensional Einstein equations imply

\[
 3p_a-\varepsilon-2p_y=0.
\]

For the frozen condensate and matter-proxy stress tensor this reduces exactly
to

\[
 -2(V+3K_w)=0,
 \qquad
 K_w=\frac{\rho^2w^2}{2b^2}.
\]

The registered control has `w=0`, `U0=0`, positive masses and nonnegative
quartics, so `V=0.625>0` at the registered initial state. The stationarity
condition is impossible there. Allowing positive winding within the same
positive-potential sector makes `V+3K_w` larger rather than repairing it.

The same obstruction is visible in four-dimensional Einstein frame. At fixed
zero-mode fields the declared positive classical contributions have the form

\[
 V_{\rm cl}(r)=\frac{A}{r}+\frac{B}{r^3},
 \qquad A>0,\ B\geq0,
\]

and hence

\[
 \frac{dV_{\rm cl}}{dr}
 =-\frac{Ar^2+3B}{r^4}<0.
\]

There is no stationary radius. Consistently, the on-shell A1 integration
evolved `b` from `1` to `1.4107405201388812` and ended with
`H_b=0.2784455851413206`; it did not stabilize.

## 5. Quantum/Casimir boundary

For one stable real periodic bosonic mode on a smooth circle, the subtracted
one-loop term has the sign and Einstein-frame shape

\[
 V_C(r)=-C r^{-6}F(x),\qquad C>0,\quad
 x=m\ell_{\rm ref}r,
\]

\[
 F(x)=\operatorname{Li}_5(e^{-x})
 +x\operatorname{Li}_4(e^{-x})
 +\frac{x^2}{3}\operatorname{Li}_3(e^{-x}),
\]

with

\[
 F'(x)=-\frac{x}{3}\operatorname{Li}_3(e^{-x})
 -\frac{x^2}{3}\operatorname{Li}_2(e^{-x})<0.
\]

The audit verified this sign over the registered dimensionless samples. All
fields frozen in `X4-I1C` are periodic bosons, so their stable one-loop vacuum
determinants do not provide the opposite-sign competition by themselves. In
the massless truncation,

\[
 V(r)=\frac{A}{r}+\frac{B}{r^3}-\frac{C}{r^6}
\]

can have an extremum, but at that extremum

\[
 V''(r)=-\frac{5Ar^2+9B}{r^5}<0;
\]

it is a maximum, not a stabilized radion.

This agrees with the general compactification warning in Ponton and Poppitz,
JHEP 06 (2001) 019, that Casimir stabilization depends on field content,
boundary conditions and renormalized counterterms, and that massless content
alone gives a runaway rather than a predictive radius:
<https://arxiv.org/abs/hep-ph/0105021>.

The audit does **not** claim to have evaluated the full finite-density one-loop
determinant on the evolving A1 spacetime. That calculation requires a declared
quantum state, subtraction prescription, counterterms and adiabatic domain;
none was frozen in A1. Importing a convenient term afterward would violate the
fixed-action test.

## 6. EFT hierarchy

A valid four-dimensional truncation would require a non-empty regime such as

\[
 \{H,\mu,m_{\rm light}\}\ll\Delta_{\rm KK}
 \ll\Lambda_5.
\]

The kinematic limits behave correctly: the KK gap rises for a small circle and
tends to zero during decompactification. But `X4-I1C` neither selects a radius
nor specifies a quantitative five-dimensional cutoff. Therefore it does not
establish the required hierarchy; choosing `R` to create one would be an input,
not a derivation.

## 7. Exact execution record

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a2_radion_symbolic_audit.py
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_a2a3_reduction_radion_control.py
```

- independent radion/reduction symbolic audit: 6/6;
- fixed-action reduction/radion audit: 15/15 calculation checks;
- symbolic JSON SHA-256:
  `52c44d8c0d3568c49ab39cf2fc44e6477ff065a44d23f6f06bd88794e8c301aa`;
- A2/A3 JSON SHA-256:
  `d5a82f23204b5e02d046a8da43ce549dec53acebe9e0770c6f4c7cdabefddc5a`;
- independent reruns: byte-identical.

The 15/15 count means that the registered calculations executed and recovered
the stated obstruction. It is not a 15/15 physics pass.

## 8. Decision

`X4-I1C` is retained as a useful negative/control parent and frozen at
`X4-D2 HOLD_UNSTABILIZED`. A4 exchange calculations and the Ultra coupled
constraint plan remain closed because there is no stable background on which
to define their physical poles.

No canonical ITSM equation or manuscript should be revised to adopt `T4` from
this result. A retry requires a separately frozen stabilization sector with
its operator or additional field, boundary condition, quantum state,
counterterms and cutoff declared before calculation. Candidate coefficients
must not be selected from an observed acceleration or any desired ITSM output.
