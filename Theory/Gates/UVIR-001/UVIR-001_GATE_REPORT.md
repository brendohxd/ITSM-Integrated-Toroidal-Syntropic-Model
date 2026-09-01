# UVIR-001 — Condensate-to-phonon matching gate

Status: **closed negative for the declared minimal candidate**
Calculation validation: **PASS**
Microscopic candidate verdict: **FAIL**
Broader UV/IR architecture: **OPEN**
MAT-001: **BLOCKED pending an alternative UV/IR route**

## Executive result

The minimally kinetic single complex scalar declared in the v12 core
architecture has a stable finite-density branch and, in the pure-sextic
limit, integrating out its amplitude at tree level gives

\[
P(Z)=\frac{2\Lambda}{3\sqrt{\lambda _6}}
      (Z-m^2)^{3/2},
\qquad
Z=-\nabla_\mu\Theta\nabla^\mu\Theta.
\]

That result does **not** generate the required ITSM spatial operator

\[
\mathcal L_{\rm IR}\propto
-\left(h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi\right)^{3/2}.
\]

On a timelike finite-density background, $Z_0=\mu^2$, a static phase
gradient $q=|\nabla\vartheta|$ gives

\[
P(\mu^2-q^2)-P(\mu^2)
=-P_Z(\mu^2)q^2+\mathcal O(q^4),
\qquad
P_Z=\frac{\rho_0^2}{2}>0.
\]

Thus the leading static response is quadratic. It is not cubic. This conclusion
is independent of the detailed analytic potential for any stable, nonzero
condensate with the canonical phase kinetic term.

The result rejects one microscopic candidate, not all possible complex
condensates or the bottom-up $Y^{3/2}$ weak-field EFT.

## 1. Scope and sources

This gate tests the tree-level, lowest-derivative action already declared in
the recovery manuscript. The general $P(Z)$ structure of a relativistic
superfluid and the identification of the constant-gradient action with its
zero-temperature equation of state follow the standard construction of
[Son](https://arxiv.org/abs/hep-ph/0204199). The explicit integration of radial
modes in relativistic complex-scalar theories is also treated by
[Joyce, Nicolis, Podo and Santoni](https://arxiv.org/abs/2204.03678).

The nonrelativistic $X\sqrt{|X|}$ phonon route used in superfluid-dark-matter
models is a related but different branch; see
[Berezhiani and Khoury](https://arxiv.org/abs/1507.01019). Published analysis
has identified equilibrium, MOND-limit and stability tensions when one field
carries both the background density and long-range force, motivating a
two-field alternative; see
[Mistele](https://arxiv.org/abs/2009.03003).

These references guide the EFT interpretation. All algebraic claims below are
independently reproduced by the accompanying symbolic calculation.

## 2. Candidate microscopic theory

Use signature $(-+++)$ and

\[
\Phi=\frac{\rho}{\sqrt2}e^{i\Theta}.
\]

The declared action becomes

\[
\mathcal L
=-\frac12(\nabla\rho)^2
 -\frac12\rho^2(\nabla\Theta)^2
 -V(\rho),
\]

with

\[
V(\rho)
=\frac12m^2\rho^2
 +\frac{\lambda_4}{8}\rho^4
 +\frac{\lambda_6}{24\Lambda^2}\rho^6.
\]

Define the Lorentz scalar

\[
Z=-\nabla_\mu\Theta\nabla^\mu\Theta.
\]

When gradients of the amplitude can be neglected,

\[
\mathcal L_{\rm TF}
=\frac12\rho^2Z-V(\rho).
\]

## 3. Finite-density background

For

\[
\Theta=\mu t,
\qquad
s\equiv\rho_0^2,
\]

the nonzero stationary branch satisfies

\[
\mu^2
=m^2+\frac{\lambda_4}{2}s
 +\frac{\lambda_6}{4\Lambda^2}s^2.
\]

For the sufficient stability domain

\[
\lambda_6>0,
\qquad
\lambda_4\ge0,
\qquad
\mu^2>m^2,
\]

the positive solution is

\[
s
=\frac{\Lambda^2}{\lambda_6}
 \left[-\lambda_4+
 \sqrt{\lambda_4^2+
 \frac{4\lambda_6}{\Lambda^2}(\mu^2-m^2)}\right].
\]

The branch is unique in this sufficient domain. More complicated branches with
negative quartic coupling are not required to decide the gate.

## 4. Amplitude curvature and physical modes

The curvature of the fixed-$Z$ amplitude potential is

\[
M_\rho^2
=V''(\rho_0)-\mu^2
=\lambda_4s+\frac{\lambda_6}{\Lambda^2}s^2.
\]

This is the scale controlling the static radial susceptibility and the local
derivative expansion. It must not be confused with the physical gapped pole,
because the amplitude mixes with the phase at finite chemical potential.

Writing

\[
\rho=\rho_0+\sigma,
\qquad
\Theta=\mu t+\pi,
\]

the quadratic action is

\[
\mathcal L_2
=\frac12\left(\dot\sigma^2-|\nabla\sigma|^2-M_\rho^2\sigma^2\right)
 +\frac{s}{2}\left(\dot\pi^2-|\nabla\pi|^2\right)
 +2\mu\sqrt{s}\,\sigma\dot\pi.
\]

The exact mode equation is

\[
(\omega^2-k^2-M_\rho^2)(\omega^2-k^2)
-4\mu^2\omega^2=0.
\]

At zero momentum it contains a Goldstone mode and a gapped mode with

\[
M_{\rm gap}^2=M_\rho^2+4\mu^2.
\]

The two scales have different jobs:

- $M_{\rm gap}$ is the physical homogeneous pole gap;
- $M_\rho$ controls whether the amplitude follows a static inhomogeneous
  phase configuration algebraically.

The Thomas–Fermi integration requires momenta, frequencies and variations of
the background invariant to be small compared with the relevant radial scale.
It fails as $M_\rho\to0$.

## 5. Integrated phase action

Solving the radial equation at fixed $Z$ gives

\[
Z=m^2+\frac{\lambda_4}{2}s(Z)
 +\frac{\lambda_6}{4\Lambda^2}s^2(Z).
\]

Substitution yields

\[
P(Z)
=\frac{\lambda_4}{8}s^2(Z)
 +\frac{\lambda_6}{12\Lambda^2}s^3(Z).
\]

The envelope identities are

\[
P_Z=\frac{s}{2},
\qquad
P_{ZZ}=\frac{s}{M_\rho^2}.
\]

They are the central identities for the gate. In particular, every nonzero
finite-density branch has $P_Z>0$.

### Pure-sextic limit

For $\lambda_4=0$,

\[
s(Z)=\frac{2\Lambda}{\sqrt{\lambda_6}}\sqrt{Z-m^2},
\]

and

\[
\boxed{
P(Z)=\frac{2\Lambda}{3\sqrt{\lambda_6}}(Z-m^2)^{3/2}
}.
\]

Thus the sextic interaction genuinely generates a three-halves power of the
**timelike relativistic invariant**. This is a successful intermediate result.
It is not yet the spatial ITSM operator.

## 6. Stability, sound speed and compressibility

On the sufficient stable branch,

\[
P_Z>0,
\qquad
P_Z+2ZP_{ZZ}>0.
\]

The Goldstone sound speed is

\[
c_s^2
=\frac{P_Z}{P_Z+2ZP_{ZZ}}
=\frac{M_\rho^2}{M_\rho^2+4\mu^2},
\]

so $0<c_s^2<1$. In the pure-sextic case,

\[
M_\rho^2=4(\mu^2-m^2),
\qquad
c_s^2=\frac{\mu^2-m^2}{2\mu^2-m^2}.
\]

The charge density and fixed-volume susceptibility are

\[
n_Q=\frac{\partial P}{\partial\mu}=\mu s,
\]

\[
\frac{\partial n_Q}{\partial\mu}
=s+\frac{4\mu^2s}{M_\rho^2}>0.
\]

Therefore the candidate has a stable timelike phonon branch in the stated
domain. Stability is not the part that fails.

## 7. High-density interaction scale

In the high-density pure-sextic limit $m^2\ll Z=\mu^2$, define

\[
A=\frac{2\Lambda}{3\sqrt{\lambda_6}},
\qquad
P(Z)=AZ^{3/2}.
\]

Expanding $Z=(\mu+\dot\pi)^2-|\nabla\pi|^2$ gives

\[
\mathcal L_2
=3A\mu\dot\pi^2
 -\frac{3}{2}A\mu|\nabla\pi|^2,
\]

and

\[
\mathcal L_3
=A\dot\pi^3
 -\frac{3}{2}A\dot\pi|\nabla\pi|^2.
\]

With canonical normalization $F^2=6A\mu$, the cubic interaction becomes
strong parametrically at

\[
\Lambda_{\rm sc}^{(3)}
\sim\left(\frac{F^3}{A}\right)^{1/2}
=2\sqrt3\,
 \frac{\Lambda^{1/4}\mu^{3/4}}{\lambda_6^{1/8}},
\]

up to order-one factors associated with the sound-cone normalization. A
conservative EFT cutoff must also lie below the radial and microscopic scales.
This estimate is valid only in the high-density branch; it is not a global
cutoff formula near condensation threshold.

## 8. The decisive static test

Let

\[
\Delta_0=\mu^2-m^2>0,
\qquad
q=|\nabla\pi|,
\qquad
\dot\pi=0.
\]

The pure-sextic pressure gives

\[
\Delta\mathcal L_{\rm static}
=A\left[(\Delta_0-q^2)^{3/2}-\Delta_0^{3/2}\right].
\]

For $q^2\ll\Delta_0$,

\[
\boxed{
\Delta\mathcal L_{\rm static}
=-\frac32A\sqrt{\Delta_0}\,q^2
 +\frac{3A}{8\sqrt{\Delta_0}}q^4
 +\mathcal O(q^6)
}.
\]

There is no leading $q^3$ operator.

This is not special to the sextic potential. For every minimally kinetic
single complex scalar of the form tested here, the envelope theorem gives

\[
P_Z(Z_0)=\frac{\rho_0^2}{2}.
\]

Consequently,

\[
P(Z_0-q^2)-P(Z_0)
=-\frac{\rho_0^2}{2}q^2+\mathcal O(q^4).
\]

A nonzero stable condensate therefore necessarily produces a quadratic
leading spatial-gradient term.

At $q^2\to\Delta_0$, the pure-sextic condensate approaches $s\to0$ and

\[
M_\rho^2=4(\Delta_0-q^2)\to0.
\]

The amplitude can no longer be integrated out. For $q^2>\Delta_0$, the
positive real pure-sextic condensate branch does not exist. Extending the
formula with an absolute value would be a new postulate, not a result of the
declared microscopic action.

## 9. Coefficient matching

The microscopic calculation produces the timelike coefficient

\[
A=\frac{2\Lambda}{3\sqrt{\lambda_6}}.
\]

It does not produce the required spatial cubic coefficient, so no physical
map to $C_{\rm IR}$ exists for this candidate.

If one formally imposed a separate spacelike branch and normalized
$\psi=f\Theta$, coefficient comparison would give

\[
\frac{A}{f^3}
\stackrel{\rm formal}{=}
\frac{C_{\rm IR}}{12\pi G a_0}.
\]

This relation is not a match because the necessary branch is absent and the
normalization $f$ is not fixed. It is retained only to make the missing
information explicit.

## 10. Compatibility with the matter coupling

The observable weak-field coefficient is

\[
C_{\rm obs}=\frac{C_m^{3/2}}{\sqrt{C_{\rm IR}}}.
\]

Because this candidate does not yield $C_{\rm IR}$, compatibility with
$C_m$ cannot be tested. MAT-001 must not start by assigning the formal
timelike coefficient $A$ to $C_{\rm IR}$.

## 11. Required-deliverable matrix

| UVIR-001 requirement | Result |
|---|---|
| Finite-density background | **PASS** in a sufficient stable parameter domain |
| Amplitude-mode mass | **PASS**; static curvature and physical pole gap distinguished |
| Conditions for integrating it out | **PASS**; fail near the branch endpoint |
| Effective phase action | **PASS**; exact tree-level $P(Z)$ obtained |
| Sign and stability | **PASS** on the timelike branch |
| Sound speed | **PASS**; positive and subluminal in the tested domain |
| Strong-coupling scale | **PARTIAL**; high-density cubic estimate obtained |
| Map to $C_{\rm IR}$ | **FAIL**; the required spatial operator is absent |
| Compatibility with $C_m$ | **BLOCKED** |

## 12. Gate classification

### Derived

- A stable finite-density branch exists for sufficient positive couplings.
- The pure sextic potential produces $P(Z)\propto(Z-m^2)^{3/2}$.
- The amplitude/phase spectrum, sound speed and susceptibility are controlled
  in the stated timelike domain.
- The leading static perturbation around that domain is quadratic.

### Rejected

> The declared minimally kinetic single complex scalar with analytic mass,
> quartic and sextic potential directly generates the spatial ITSM
> $Y^{3/2}$ weak-field operator.

### Still open

- A noncanonical microscopic kinetic theory.
- A controlled nonrelativistic gradient-dominated branch.
- A two-field construction separating background density from force phonon.
- An explicitly preferred-frame spatial EFT with a technically natural UV
  completion.

## 13. Consequence for the recovery programme

The bottom-up $Y^{3/2}$ weak-field EFT remains a valid conditional inverse
construction. Its proposed derivation from the canonical sextic condensate is
now rejected.

MAT-001 remains blocked. The next dependency must be a new UV/IR choice, not a
matter-vertex calculation performed on the failed one-field match.

Recommended successor gate:

> **UVIR-002 — compare a controlled nonrelativistic gradient branch, a
> two-field force/background split, and a noncanonical preferred-frame
> condensate; select one route using stability, naturalness and matching
> criteria before resuming MAT-001.**

## Reproducibility

Run:

```powershell
python Analysis/UVIR/UVIR-001/uvir001_symbolic.py
```

The script prints separate calculation and hypothesis statuses:

```text
Validation status: PASS
UVIR-001 candidate verdict: FAIL
```

Machine-readable outputs are stored in
`Analysis/UVIR/UVIR-001/outputs/`.
