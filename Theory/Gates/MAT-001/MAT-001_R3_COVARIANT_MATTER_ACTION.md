# MAT-001 R3 covariant matter action and ADM-source derivation

**Date:** 2026-08-07

**Scoped status:** `PASS_MAT001_R3_COVARIANT_MATTER_ACTION_SCOPED`

**Global status unchanged:** MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`;
$V$ `NOT_COMPUTED`; $K_Q$ `NOT_DERIVED`; Stage 4A `CLOSED`

**Authority:** This note implements R3 of
`MAT-001_TIER1_REMEDIATION_ADDENDUM_2026-08-07.md`. It is subordinate to the
Master Plan, Core Architecture and Core Recovery Plan.

## 1. Decision

Select the conformal matter metric already admitted by the unit-chart contract:

\[
 \widetilde g_{\mu\nu}=A(\psi)^2g_{\mu\nu},\qquad
 A(\psi)=\exp[C_m(\psi-\psi_*)]
\]

in natural units. In the SI chart,

\[
 A(\psi_{\rm SI})=
 \exp\!\left[\frac{C_m(\psi_{\rm SI}-\psi_{*,\rm SI})}{c^2}\right].
\]

The normalization point satisfies $A(\psi_*)=1$. The matter and interaction
sectors in the architecture inventory are defined without double counting by

\[
 S_m^{(0)}=S_m[\Psi_m,g],\qquad
 S_{\rm int}=S_m[\Psi_m,A^2g]-S_m[\Psi_m,g],
\]

so that $S_m^{(0)}+S_{\rm int}=S_m[\Psi_m,A^2g]$.

This selects a covariant MAT matter-force action. It does not select a UV
completion, determine $C_m$, identify $C_m=C_{\rm IR}$, or complete the
lensing sector.

## 2. Why this candidate was selected

| Candidate | Disposition | Reason |
|---|---|---|
| Reduced $-C_m\rho_b\psi$ alone | Rejected as parent action | Correct NR term but no covariant matter variables or metric variation |
| Universal conformal metric $A^2g$ | Selected for scoped R3 | Covariant, same action generates force and exchange, and reproduces the declared NR vertex |
| Disformal/aether-dependent matter metric | Deferred | Adds new Wilson functions and preferred-frame matter couplings before the minimal route is tested |
| Derivative current coupling $J^\mu\nabla_\mu\psi$ | Rejected as primary route | Does not generically reproduce the required static mass-density force and changes charge/exchange assumptions |
| External prescribed $\rho_b(x)$ | Rejected as fundamental matter model | Cannot by itself satisfy the matter equations and diffeomorphism Ward identity |

The form $S_m[\Psi_m,A(\psi)^2g]$ is standard in tensor-scalar gravity; see
Damour and Esposito-Farese,
[Class. Quantum Grav. 9 (1992) 2093](https://doi.org/10.1088/0264-9381/9/9/015).
For a covariant perfect-fluid/dust action and its canonical formulation, see
Brown,
[Class. Quantum Grav. 10 (1993) 1579](https://doi.org/10.1088/0264-9381/10/8/017).

The superfluid-DM literature is useful as a warning about provenance, not as a
derivation for ITSM. The baryon-phonon density term is treated as an empirical
or soft symmetry-breaking interaction and its relativistic completion is
separate: [Phys. Rev. D 92, 103510](https://doi.org/10.1103/PhysRevD.92.103510)
and [JCAP 09 (2018) 021](https://doi.org/10.1088/1475-7516/2018/09/021).

## 3. Matter variables

The fundamental representative used for the ADM variation is a collection of
massive baryonic worldlines,

\[
 S_m=-\sum_A m_A\int A(\psi)\,ds_g.
\]

This is equivalent to minimal worldline coupling to $\widetilde g_{\mu\nu}$.
Its coarse-grained, conserved-number, pressureless limit defines the dust used
for $\rho_b$. Therefore $\rho_b$ is not an arbitrary external scalar in the
covariant theory; it is the rest-mass density obtained from dynamical matter.

Pressure, internal energy and radiation can be restored through a full fluid or
field action. They are not needed to establish the dust weak-field vertex, but
the trace dependence below means relativistic species do not couple like dust.

## 4. ADM convention and exact variation

Use signature $(-+++ )$ and

\[
 ds^2=-N^2dt^2+h_{ij}(dx^i+N^idt)(dx^j+N^jdt).
\]

For one particle define

\[
 w^i=\dot x^i+N^i,\qquad
 D=\sqrt{N^2-h_{ij}w^iw^j},\qquad
 L_A=-m_AA(\psi)D.
\]

The variation is restricted to the future-directed timelike ADM domain
$N>0$ and $D^2=N^2-h_{ij}w^iw^j>0$. Outside this domain the
worldline square root is not real and the formulas below are not claimed.

Holding the worldline coordinates fixed during metric variation gives

\[
 \frac{\partial L_A}{\partial N}=-\frac{m_AA N}{D},
\]

\[
 \frac{\partial L_A}{\partial N^i}
 =\frac{m_AA h_{ij}w^j}{D},
\qquad
 \frac{\partial L_A}{\partial h_{ij}}
 =\frac{m_AA w^iw^j}{2D}.
\]

For the continuum projections $E=T_{\mu\nu}n^\mu n^\nu$,
$j_i=-h_{i\mu}n_\nu T^{\mu\nu}$, and
$S^{ij}=h^i{}_{\mu}h^j{}_{\nu}T^{\mu\nu}$, the same convention gives

\[
 \frac{\delta S_m}{\delta N}=-\sqrt h\,E,
 \qquad
 \frac{\delta S_m}{\delta N^i}=+\sqrt h\,j_i,
 \qquad
 \frac{\delta S_m}{\delta h_{ij}}=\frac{N\sqrt h}{2}S^{ij}.
\]

These are the lapse, shift and spatial-metric matter sources. They are not zero
for generic matter. For $S_{\rm int}$, replace $A$ by $A-1$ in the lapse,
shift and spatial-stress expressions.

## 5. Controlled recovery of the Track-A linear covectors

Take the named local background

\[
 N=1,\quad N^i=0,\quad \dot x^i=0,\quad \psi=\psi_*,\quad A(\psi_*)=1,
\]

and write $\psi=\psi_*+\pi$. At first order in the extra-force source sector,

\[
 \left.\frac{\partial L_{\rm int}}{\partial\pi}\right|_*= -m_AC_m,
 \qquad
 \left.\frac{\partial L_{\rm int}}{\partial N}\right|_*=0,
 \qquad
 \left.\frac{\partial L_{\rm int}}{\partial N^i}\right|_*=0.
\]

Thus the earlier J2 linear covectors are recovered only in this controlled
sector:

\[
 d=(-C_m),\qquad h=(0,0).
\]

This does not imply covariant constraint independence. The mixed lapse vertex is

\[
 \left.\frac{\partial^2L_{\rm int}}
 {\partial\pi\,\partial N}\right|_*=-m_AC_m,
\]

and moving matter gives, in a one-direction representative,

\[
 \left.\frac{\partial^2L_{\rm int}}
 {\partial\pi\,\partial N^\parallel}\right|_{N=1,N^i=0,\psi_*}
 =\frac{m_AC_mv}{\sqrt{1-v^2}}.
\]

For a scalar shift $N_i\propto\partial_i\beta$, the latter carries the
corresponding spatial momentum. It vanishes in the comoving limit, not as an
identity of the parent action.

## 6. Weak-field limit

With $N=1+\Phi_N$, small velocity and small $\pi$,

\[
 L_A=-m_A+\frac12m_Av^2-m_A\Phi_N-m_AC_m\pi+\cdots .
\]

After coarse graining, this recovers

\[
 \mathcal L_{\rm int}^{\rm NR}=-C_m\rho_b\pi.
\]

The coefficient sign therefore follows from the selected positive exponential
and the repository's ADM convention; it is not an absolute-value convention.

## 7. Conservation and Bianchi consistency

Define the Einstein-chart stress tensor by variation with respect to
$g_{\mu\nu}$, and

\[
 \alpha(\psi)=\frac{d\ln A}{d\psi}=C_m.
\]

Diffeomorphism invariance gives the matter Ward identity

\[
 \nabla_\mu T_m^{\mu}{}_{\nu}
 =\alpha T_m\nabla_\nu\psi.
\]

For pressureless dust $T_m=-\rho_m$, hence

\[
 Q_{{\rm mp}\,\nu}=-C_m\rho_m\nabla_\nu\psi,
 \qquad
 \nabla_\mu T_\psi^{\mu}{}_{\nu}=-Q_{{\rm mp}\,\nu}
\]

when the force-field equation holds. Therefore the matter-plus-force block is
covariantly conserved. This is $Q_{\rm mp}$, not the distinct reservoir
exchange $Q_{\rm syn}$.

The result is a scoped Ward-identity check. Full propagation of the joined
gravity+aether+condensate+force+dust constraints remains a separate UVIR task.

## 8. Reproduction and independent check

Run

```text
python -m py_compile Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/mat001_r3_covariant_matter_action.py
python Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/mat001_r3_covariant_matter_action.py --self-test-mutations
python Analysis/MAT/MAT-001/COVARIANT_MATTER_ACTION/mat001_r3_covariant_matter_action.py
```

The mutation suite rejects a sign-flipped $d$, deletion of the mixed lapse
vertex, and promotion of the controlled $h=0$ statement to a global claim.
Wolfram Language independently returned exact derivative residuals $(0,0)$,
controlled derivatives $(-C_mm,0,0,-C_mm,0)$, and the moving mixed-shift
coefficient $C_mmv/\sqrt{1-v^2}$.

Output digest:
`99F712392F0DD42820D760FDAA7D1CDAEA1E301D04D610D5C4B49C663377F676`.

## 9. Disposition

R3 is `PASS_SCOPED` for action provenance, exact matter ADM variation,
weak-field recovery and the matter-force Ward identity. It does not close RR2,
RR3, MAT-001, UVIR-003, LEN-001 or Stage 4A. The next remediation item is R4:
propagate the signed coupling through canonical normalization and the projected
source-residue contract, retaining the R3 mixed constraint vertices at the
appropriate perturbative order.
