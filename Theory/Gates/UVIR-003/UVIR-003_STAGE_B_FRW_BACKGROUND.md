# UVIR-003 - Stage B evolving flat-FRW background

Calculation status: **PASS**

Background status: **REPRESENTATIVE ON-SHELL BRANCH VERIFIED**

Scalar ADM reduction: **READY TO BEGIN ON THE EVOLVING FRW BACKGROUND**

Full UVIR-003: **IN PROGRESS**

MAT-001: **BLOCKED**

## Executive result

The background-completion screen selected a self-consistent evolving
flat-FRW route rather than an artificially supported exact-Minkowski
finite-density state. This calculation derives the corresponding homogeneous
equations from the declared Stage-A sectors and verifies one representative
dimensionless solution.

Use

\[
ds^2=-N(t)^2dt^2+a(t)^2\delta_{ij}dx^idx^j,
\qquad
U^\mu=\left(\frac1N,0,0,0\right),
\]

\[
\Phi=\frac{\rho(t)}{\sqrt2}e^{i\Theta(t)},
\qquad
\bar\psi=\text{constant}.
\]

The condensate current is parallel to the aether, so the alignment term
vanishes on the background. The constant force field also contributes no
background stress in the declared truncation. No reservoir exchange or
condensate-charge source is introduced in the representative branch.

The comoving aether does not add a new homogeneous degree of freedom.
Isotropy and the unit constraint fix its direction and norm; its spatial
equation is identically satisfied, while the multiplier is determined
algebraically. Its kinetic operators renormalize the cosmological Planck mass:

\[
M_{\rm cos}^2
=M_P^2+\frac{M_U^2}{2}(c_1+3c_2+c_3).
\]

The reduced condensate--gravity system has a conserved charge and supports
regular expanding solutions. The supplied representative branch satisfies
the Friedmann constraint, charge conservation and energy continuity to the
reported numerical tolerances.

This result removes the background blocker. It does not perform the scalar
perturbation reduction or close UVIR-003.

## 1. Homogeneous reduction of the aether

For the comoving unit vector, define

\[
H_N=\frac{\dot a}{aN}.
\]

The four Stage-A aether contractions reduce to

\[
(\nabla_\mu U_\nu)(\nabla^\mu U^\nu)=3H_N^2,
\]

\[
(\nabla_\mu U^\mu)^2=9H_N^2,
\]

\[
(\nabla_\mu U_\nu)(\nabla^\nu U^\mu)=3H_N^2,
\qquad
a_\mu a^\mu=0.
\]

Therefore

\[
\mathcal L_U^{\rm FRW}
=-\frac{3M_U^2}{2}(c_1+3c_2+c_3)H_N^2.
\]

After including the Einstein--Hilbert term and discarding its standard
boundary term, the gravitational minisuperspace coefficient is

\[
\boxed{
M_{\rm cos}^2
=M_P^2+\frac{M_U^2}{2}c_\theta,
\qquad
c_\theta=c_1+3c_2+c_3.
}
\]

Using the corrected frame normalization
$\alpha_i=(M_U^2/M_P^2)c_i$, this is

\[
M_{\rm cos}^2
=M_P^2\left[1+\frac{\alpha_{13}+3\alpha_2}{2}\right].
\]

This agrees with the cosmological rescaling structure discussed in the
Einstein--aether review:

- C. Eling, T. Jacobson and D. Mattingly,
  *Einstein--Aether Theory*,
  <https://arxiv.org/abs/gr-qc/0410001>.

## 2. Minisuperspace action

Let

\[
V(\rho)
=\frac12m^2\rho^2
+\frac{\lambda_4}{8}\rho^4
+\frac{\lambda_6}{24\Lambda^2}\rho^6.
\]

The homogeneous action per unit comoving volume is

\[
S_{\rm bg}
=\int dt\left[
-\frac{3M_{\rm cos}^2a\dot a^2}{N}
+\frac{a^3}{2N}
\left(\dot\rho^2+\rho^2\dot\Theta^2\right)
-Na^3V(\rho)
\right].
\]

The background alignment invariant is zero because
$J_\Phi^\mu\parallel U^\mu$:

\[
h_{\mu\nu}J_\Phi^\mu J_\Phi^\nu=0.
\]

Every derivative of the constant $\bar\psi$ also vanishes, so the force
sector contributes zero at background order.

## 3. Background equations

After variation, set $N=1$ and define
$\mu=\dot\Theta$. Lapse variation gives

\[
\boxed{
3M_{\rm cos}^2H^2
=\frac12\dot\rho^2+\frac12\rho^2\mu^2+V(\rho).
}
\]

The scale-factor equation, or the time derivative of the Friedmann equation
combined with matter conservation, gives

\[
\boxed{
-2M_{\rm cos}^2\dot H
=\dot\rho^2+\rho^2\mu^2.
}
\]

The amplitude equation is

\[
\boxed{
\ddot\rho+3H\dot\rho-\rho\mu^2+V_{,\rho}=0.
}
\]

The phase equation is exact charge conservation:

\[
\boxed{
\frac{d}{dt}\left(a^3\rho^2\mu\right)=0.
}
\]

Writing the conserved comoving charge as $\mathcal N$,

\[
\mu(t)=\frac{\mathcal N}{a(t)^3\rho(t)^2}.
\]

The energy density and pressure are

\[
\rho_\Phi
=\frac12\dot\rho^2+\frac12\rho^2\mu^2+V,
\qquad
p_\Phi
=\frac12\dot\rho^2+\frac12\rho^2\mu^2-V,
\]

and satisfy

\[
\dot\rho_\Phi+3H(\rho_\Phi+p_\Phi)=0.
\]

These equations make explicit why constant $\rho$ and constant $\mu$
cannot generally persist during expansion without a charge-transfer source.

## 4. Representative branch

The accompanying script integrates a dimensionless existence example. The
chosen coefficients are not fitted and are not a proposed physical parameter
point:

\[
M_P=1,\quad M_U=0.5,\quad
(c_1,c_2,c_3,c_4)=(0.10,0.05,0.05,0.05),
\]

\[
m^2=1,\quad \lambda_4=0.50,\quad
\lambda_6=0.20,\quad \Lambda=2.
\]

They obey the existing necessary frame conditions

\[
c_{14}>0,\qquad c_1>0,\qquad c_{123}>0,
\]

and give

\[
M_{\rm cos}^2=1.0375.
\]

Initial data are

\[
a(0)=1,\qquad \rho(0)=1,\qquad \dot\rho(0)=0.
\]

The initial chemical potential is placed on the instantaneous radial branch,

\[
\mu(0)^2=\frac{V_{,\rho}(\rho_0)}{\rho_0},
\]

and $H(0)>0$ is fixed by the Friedmann constraint. Expansion then dilutes
the conserved charge and drives a genuinely time-dependent solution.

The exact numerical endpoint and residuals are recorded in
`Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_summary.json`; the full
sampled branch is in
`Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_trajectory.csv`.

For the default integration from $t=0$ to $t=8$:

| Quantity | Initial | Final |
|---|---:|---:|
| $a$ | 1 | 4.571577 |
| $\rho$ | 1 | 0.134236 |
| $\mu$ | 1.123610 | 0.652648 |
| $H$ | 0.619841 | 0.076405 |

The monitored maximum relative residuals are

| Check | Maximum |
|---|---:|
| Friedmann constraint | $2.124\times10^{-10}$ |
| comoving-charge drift | $2.220\times10^{-16}$ |
| condensate continuity | $1.898\times10^{-15}$ |

## 5. Gate decision

### Derived and verified

- the comoving aether renormalizes the homogeneous gravitational coefficient
  to $M_{\rm cos}^2$;
- the alignment and constant-force terms vanish on this background;
- the Friedmann, Raychaudhuri, amplitude and phase equations follow from the
  reduced action;
- an isolated condensate has exactly conserved $a^3\rho^2\mu$;
- a regular representative expanding branch exists and preserves the
  Friedmann constraint and continuity equation within the reported numerical
  tolerances.

### Not derived

- a phenomenologically selected parameter point;
- a reservoir-driven background or charge-transfer law;
- a cosmological attractor;
- the reduced scalar kinetic and gradient matrices;
- low-$k$ cosmological perturbation stability;
- CMB, growth or distance predictions.

### Consequence

The scalar ADM calculation is no longer blocked by the absence of an on-shell
background. It is now **ready to begin on the evolving FRW branch**. The
calculation must retain the background time dependence; a subhorizon
approximation is valid only for $k/a\gg H$, and cannot answer the strict
$k\rightarrow0$ question.

## 6. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_frw_background.py
```

Expected footer:

```text
UVIR-003 flat-FRW minisuperspace identities: VERIFIED
Comoving aether cosmological normalization: VERIFIED
Representative evolving background: ON_SHELL
Max relative Friedmann residual: <reported value>
Max relative charge drift: <reported value>
Max relative continuity residual: <reported value>
Scalar ADM reduction: READY_TO_BEGIN_ON_EVOLVING_FRW_BACKGROUND
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_EVOLVING_FRW_BACKGROUND
```

## Subsequent scalar ADM status

The next bounded subgate has now been completed. In aether-unitary scalar
gauge, the frozen-coefficient subhorizon principal reduction eliminates the
lapse and scalar shift, independently recovers the exact Einstein-aether
spin-0 speed and derives the condensate `q_ADM` validity scale. See
`UVIR-003_STAGE_B_SCALAR_ADM_PRINCIPAL.md`.

The subsequent complete quadratic finite-`q` reduction has also eliminated
the constraints along the evolving branch. Its representative nonzero-`q`
kinetic inertia is positive, but the exact determinant scales as `q^2` and
loses one rank at the homogeneous endpoint. See
`UVIR-003_STAGE_B_SCALAR_ADM_FINITE_Q.md`. The cubic low-`q` canonical
normalization remains open.
