# UVIR-003 - Stage B scalar ADM principal-symbol reduction

Calculation status: **PASS**

Reduction status: **SUBHORIZON PRINCIPAL BLOCK REDUCED**

Causality status: **MULTICONE GLOBAL CAUSALITY OPEN**

Full UVIR-003: **IN PROGRESS**

MAT-001: **BLOCKED**

## Executive result

The verified flat-FRW branch removes the previous off-shell background
blocker. The next bounded calculation is the scalar ADM principal symbol:
freeze the evolving background coefficients over a wavelength, impose
aether-unitary scalar gauge, eliminate the lapse and scalar shift, and retain
the highest-derivative terms for physical wavenumber \(q=k/a\gg H\).

This calculation:

- derives the hypersurface-orthogonal ADM form of the declared aether action;
- solves the principal lapse and scalar-shift constraints;
- derives the reduced aether-curvature kinetic and gradient coefficients;
- independently recovers the published Einstein-aether spin-0 speed;
- derives the leading finite-\(q\) condensate kinetic correction;
- identifies the additional scale above which the principal reduction is
  controlled; and
- retains the already-factorized zero-gradient force mode.

For the representative dimensionless branch, the reduced aether-curvature
mode has positive kinetic and gradient coefficients,

\[
\mathcal K_{\mathcal R}=39.94375,
\qquad
\mathcal G_{\mathcal R}=52.3333333,
\]

and

\[
s_0^2=1.310175768,
\qquad
s_0=1.144629096.
\]

The value \(s_0>1\) is a multicone causality flag, not an exponential
instability. The representative coefficients were chosen only for background
existence and are not a physical parameter point.

This result does **not** determine the full time-dependent or strict low-\(q\)
system. UVIR-003 remains open.

## 1. Gauge and approximation

Use the aether-orthogonal scalar gauge in which the hypersurface-orthogonal
scalar part of the unit vector is the ADM normal:

\[
U^\mu=n^\mu.
\]

Write

\[
N=1+\delta N,
\qquad
N_i=\partial_i\beta,
\qquad
h_{ij}=a^2e^{2\mathcal R}\delta_{ij},
\]

and perturb the condensate as

\[
\rho(t,\mathbf x)=\rho(t)+\delta\rho(t,\mathbf x),
\qquad
\Theta(t,\mathbf x)=\Theta(t)+\vartheta(t,\mathbf x).
\]

The force background remains constant,
\(\psi=\bar\psi+\pi\), with \(\partial_\mu\bar\psi=0\).

The calculation freezes \(H,\rho,\dot\rho,\mu=\dot\Theta\) over one
wavelength and retains:

- the quadratic two-time-derivative terms;
- the \(q^2\) spatial principal terms;
- the force \(q^4\) regulator; and
- the leading lapse-induced \(1/q^2\) condensate kinetic correction.

Terms of order \(H/q\), \(\dot\mu/q\), masses, and the complete \(q^0\)
constraint response are not promoted into this result.

## 2. Aether ADM dictionary

For \(U^\mu=n^\mu\),

\[
\nabla_\mu U_\nu=K_{\mu\nu}-U_\mu a_\nu.
\]

Therefore

\[
(\nabla_\mu U_\nu)(\nabla^\mu U^\nu)
=K_{ij}K^{ij}-a_i a^i,
\]

\[
(\nabla_\mu U^\mu)^2=K^2,
\qquad
(\nabla_\mu U_\nu)(\nabla^\nu U^\mu)=K_{ij}K^{ij}.
\]

Combining the Einstein-Hilbert and Stage-A aether actions gives

\[
\mathcal L_{\rm grav+U}^{\rm ADM}
=\frac{N\sqrt h}{2}\left[
M_P^2\,{}^{(3)}R
+(M_P^2-M_U^2c_{13})K_{ij}K^{ij}
-(M_P^2+M_U^2c_2)K^2
+M_U^2c_{14}a_i a^i
\right],
\]

where

\[
c_{13}=c_1+c_3,\qquad
c_{14}=c_1+c_4,\qquad
c_{123}=c_1+c_2+c_3.
\]

Two symbolic checks are important:

\[
(M_P^2-M_U^2c_{13})
+3(-M_P^2-M_U^2c_2)
=-2M_{\rm cos}^2,
\]

\[
(M_P^2-M_U^2c_{13})
+(-M_P^2-M_U^2c_2)
=-M_U^2c_{123}.
\]

The first reproduces the FRW kinetic normalization. The second supplies the
quadratic scalar-shift term that is absent in pure GR.

## 3. Principal constraints

For a Fourier mode with physical wavenumber \(q=k/a\), define

\[
\mathcal P
=\dot\rho\,\delta\rho+\rho^2\mu\,\vartheta,
\]

\[
\mathcal E_v
=\dot\rho\,\delta\dot\rho+\rho^2\mu\,\dot\vartheta.
\]

The principal lapse and scalar-shift solutions are

\[
\boxed{
\delta N
=-\frac{2M_P^2}{M_U^2c_{14}}\mathcal R
+\frac{\mathcal E_v}{M_U^2c_{14}q^2}
}
\]

and

\[
\boxed{
\beta
=-\frac{2M_{\rm cos}^2\dot{\mathcal R}+\mathcal P}
{M_U^2c_{123}q^2}.
}
\]

These are constraint solutions, not new propagating variables. The
\(1/q^2\) terms also show why this principal reduction cannot be extrapolated
to \(q=0\).

## 4. Reduced aether-curvature block

Use the normalized coefficients already fixed by the frame-sector audit,

\[
\alpha_i=\frac{M_U^2}{M_P^2}c_i,
\]

and define

\[
F=1+\frac{\alpha_{13}+3\alpha_2}{2}
=\frac{M_{\rm cos}^2}{M_P^2}.
\]

After eliminating \(\delta N\) and \(\beta\), the principal curvature block is

\[
\mathcal L_{\mathcal R}^{(2)}
=\mathcal K_{\mathcal R}\dot{\mathcal R}^2
-\mathcal G_{\mathcal R}q^2\mathcal R^2,
\]

with

\[
\boxed{
\mathcal K_{\mathcal R}
=\frac{2M_P^2F(1-\alpha_{13})}{\alpha_{123}}
}
\]

and

\[
\boxed{
\mathcal G_{\mathcal R}
=\frac{M_P^2(2-\alpha_{14})}{\alpha_{14}}.
}
\]

Consequently,

\[
\boxed{
s_0^2
=\frac{\alpha_{123}(2-\alpha_{14})}
{\alpha_{14}(1-\alpha_{13})
(2+\alpha_{13}+3\alpha_2)}.
}
\]

The script verifies this identity symbolically against the spin-0 result in
the Einstein-aether literature:

- T. Jacobson and D. Mattingly,
  *Einstein-Aether Waves*,
  <https://arxiv.org/abs/gr-qc/0402005>;
- T. Jacobson,
  *Einstein-aether gravity: a status report*,
  <https://arxiv.org/abs/0801.1547>.

The independent ADM derivation therefore cross-checks the earlier
literature-substitution result rather than merely repeating it.

A sufficient positive principal domain is

\[
F>0,\qquad
\alpha_{123}>0,\qquad
1-\alpha_{13}>0,\qquad
0<\alpha_{14}<2.
\]

## 5. Condensate principal block and validity scale

The finite-\(q\) condensate velocity Hessian for
\((\delta\rho,\vartheta)\) is

\[
\mathbf K_\Phi(q)=
\begin{pmatrix}
1-\dfrac{\dot\rho^2}{M_U^2c_{14}q^2}
&
-\dfrac{\dot\rho\,\rho^2\mu}{M_U^2c_{14}q^2}
\\[8pt]
-\dfrac{\dot\rho\,\rho^2\mu}{M_U^2c_{14}q^2}
&
\rho^2-\dfrac{\rho^4\mu^2}{M_U^2c_{14}q^2}
\end{pmatrix}.
\]

Its determinant factorizes:

\[
\boxed{
\det\mathbf K_\Phi
=\rho^2\left[
1-\frac{\dot\rho^2+\rho^2\mu^2}
{M_U^2c_{14}q^2}
\right].
}
\]

Define

\[
\boxed{
q_{\rm ADM}^2
=\frac{\dot\rho^2+\rho^2\mu^2}{M_U^2c_{14}}.
}
\]

The principal condensate block is controlled only for

\[
q^2\gg q_{\rm ADM}^2
\]

in addition to \(q\gg H\). Near or below this scale, the omitted \(q^0\)
terms and full time dependence must be restored before signs are interpreted.

At asymptotically high \(q\), the amplitude speed is unity. The phase gradient
receives the alignment contribution

\[
c_\vartheta^2=1+\zeta_{\rm align}\rho^2.
\]

The declared \(\zeta_{\rm align}>0\) gives a positive phase gradient but opens
another preferred-frame cone. Its global causal interpretation remains a
separate gate.

## 6. Force block

The constant force background still factorizes at quadratic order. The
zero-gradient mode remains

\[
\omega_\pi^2
=\frac{\gamma}{K_QM_*^2}q^4,
\]

with positive principal energy for

\[
K_Q>0,\qquad \gamma>0.
\]

This block does not repair or invalidate the low-\(q\) metric-aether-condensate
system.

## 7. Representative branch

For the existing dimensionless background example,

\[
\alpha_{13}=0.0375,\qquad
\alpha_{14}=0.0375,\qquad
\alpha_{123}=0.05,\qquad
F=1.0375.
\]

The reduced coefficients and speed are

| Quantity | Value |
|---|---:|
| \(\mathcal K_{\mathcal R}\) | 39.94375 |
| \(\mathcal G_{\mathcal R}\) | 52.3333333 |
| \(s_0^2\) | 1.310175768 |
| \(s_0\) | 1.144629096 |

The 801-point trajectory scan gives

| Validity diagnostic | Maximum | Time |
|---|---:|---:|
| \(q_{\rm ADM}\) | 5.802298 | 0.00 |
| \(q_{\rm ADM}/H\) | 11.939072 | 2.52 |
| \(a q_{\rm ADM}\) | 5.952641 | 1.99 |
| \(aH\) | 0.632766 | 1.05 |

Thus a fixed comoving mode used in this audit must satisfy

\[
k\gg \max_t(aq_{\rm ADM},aH),
\]

not merely \(k/a>H\) at the initial time.

## 8. Gate decision

### Derived and verified

- the aether-unitary ADM operator dictionary;
- the principal lapse and scalar-shift solutions;
- the reduced aether-curvature kinetic and gradient coefficients;
- exact agreement with the published Einstein-aether spin-0 speed;
- the leading finite-\(q\) condensate kinetic matrix and its factorized
  determinant;
- the additional \(q_{\rm ADM}\) validity scale;
- positive principal coefficients at the representative dimensionless point.

### Still open

- all \(H/q\), \(\dot\mu/q\), mass, and \(q^0\) terms;
- finite-\(q\) eigenvalues outside the controlled principal domain;
- the strict \(q\rightarrow0\) Hamiltonian and gradient audit;
- a physical alignment coefficient and a phenomenologically selected aether
  domain;
- global multicone causality;
- the physical cutoff and full strong-coupling comparison;
- vector and tensor rechecks on the evolving background.

### Consequence

The scalar ADM programme advances from “ready to begin” to
**principal subhorizon reduction passed**. It does not close UVIR-003.
The next calculation is the full time-dependent finite-\(q\) scalar quadratic
action along the evolving branch.

## 9. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_principal.py
```

Expected footer:

```text
UVIR-003 scalar ADM principal identities: VERIFIED
Lapse and scalar shift: ELIMINATED
Einstein-aether spin-0 formula: INDEPENDENTLY_RECOVERED
Representative spin-0 speed squared: 1.31017576801
Maximum representative q_ADM/H: 11.9391
Scalar ADM reduction: PASS_SUBHORIZON_PRINCIPAL_REDUCTION
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_SCALAR_ADM_PRINCIPAL_SYMBOL
```
