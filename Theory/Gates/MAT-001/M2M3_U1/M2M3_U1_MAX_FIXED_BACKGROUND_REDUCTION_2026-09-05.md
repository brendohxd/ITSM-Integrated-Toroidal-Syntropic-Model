# M2/M3-U1 Max fixed-background reduction

**Date:** 2026-09-05  
**Branch:** `recovery/v12-core-architecture`  
**Reasoning tier:** Max  
**Status:** `BOUNDED_REDUCTION_COMPLETE_WITH_HOLDS`  
**Physics disposition:** `NONEMPTY_HEALTHY_SCALAR_CONTROL_NO_STANDALONE_MOND`  
**Gate effect:** none

Canonical status remains:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V=C_m/sqrt(K_Q) NOT_COMPUTED`.

## 1. Result first

The bounded condensate portal does make real progress, but not the progress
needed to close MAT-001.

1. The displayed RCP-C0 action has a nonempty healthy finite-density scalar
   domain. It produces a nonzero, field-chart-invariant fixed-background
   source coupling.
2. Its exact static kernel is Yukawa, becoming inverse-square inside the
   healing length. It does **not** produce the required MOND-like `1/r`
   acceleration law.
3. Nonlinear condensate expulsion screens dense sources for the stable portal
   sign. The opposite strong-source sign has a soft gradient instability.
4. The ITSM-compatible conformal action RCP-I1-C gives the linear dust-source
   coefficient `g_sigma=alpha_1 rho_0`, but `alpha_1`, the full function `A`,
   nonzero-density matter susceptibility and the metric constraints remain
   free or uncomputed.
5. A homogeneous finite-density condensate has nonzero enthalpy, so the flat
   background used here is not an on-shell solution of the displayed
   gravitating action. The result is a scalar fixed-background control, not a
   physical ITSM pole residue.
6. A useful new route falls out of the parent-to-EFT classification: a
   `|Phi|^6` parent potential gives a leading algebraic phase EFT proportional
   to `(X-m^2)^(3/2)`, whereas the present quartic gives `(X-m^2)^2`. This
   identifies a clean operator-shape candidate, not a normalization or gate
   pass.

No observational acceleration, `H_0`, SPARC coefficient, torus cycle count or
target healing length entered any step.

## 2. Conventions and field chart

Use signature `(-,+,+,+)`, natural units and

\[
\Phi=\frac{\rho}{\sqrt 2}e^{i\Theta},\qquad
s=|\Phi|^2=\frac{\rho^2}{2}.
\]

The published comparator chart is

\[
\Phi=(v+h)e^{i(\mu t+\pi)},
\]

so the exact map is

\[
\rho_0=\sqrt2v,\qquad \sigma=\sqrt2h,\qquad
q=\rho_0\pi=\sqrt2v\pi.
\]

The canonical fixed-background scalar fluctuations are `sigma` and `q`.
Their mass dimensions are one. The phase `pi` is dimensionless.

## 3. RCP-C0 background

In the core chart the frozen comparator is

\[
\mathcal L_{\rm C0}=
-\frac12(\partial\rho)^2
-\frac12\rho^2(\partial\Theta)^2
-\frac12m^2\rho^2
-\frac{\lambda_4}{8}\rho^4
-\frac{\rho^2}{2\Lambda^2}J.
\]

For `J=0`, `rho=rho_0` and `Theta=mu t`, the radial and phase equations give

\[
\mu^2=m^2+\frac{\lambda_4}{2}\rho_0^2
      =m^2+\lambda_4v^2,
\qquad
n=j^0=\mu\rho_0^2=2\mu v^2.
\]

Thus this is a finite-charge state fixed by an external charge/chemical
potential condition, not the Lorentz-invariant zero-density vacuum.

Its pressure and energy density are

\[
p=\frac{\lambda_4v^4}{2},\qquad
\varepsilon=2\mu^2v^2-\frac{\lambda_4v^4}{2},
\qquad
\varepsilon+p=2\mu^2v^2>0.
\]

The final identity is the on-shell-background obstruction used in section 11.

## 4. Complete fixed-metric quadratic kernel

Expanding `rho=rho_0+sigma`, `Theta=mu t+pi` and retaining all quadratic
amplitude-phase terms gives, up to the background and a phase total derivative,

\[
\begin{split}
\mathcal L_2={}&\frac12\dot\sigma^2-\frac12(\nabla\sigma)^2
-\frac12M_\sigma^2\sigma^2
+\frac12\dot q^2-\frac12(\nabla q)^2
+2\mu\sigma\dot q
-g_{\rm C0}\sigma J,\\
M_\sigma^2={}&\lambda_4\rho_0^2=2\lambda_4v^2,\\
g_{\rm C0}={}&\frac{\rho_0}{\Lambda^2}
=\frac{\sqrt2v}{\Lambda^2}.
\end{split}
\]

The source-independent term `-s_0J/Lambda^2` is retained in the full action
but does not change the linear scalar response between separated prescribed
sources.

With Fourier convention `exp(-i omega t+i k.x)`, the Euler-Lagrange kernel is

\[
\begin{pmatrix}
k^2+M_\sigma^2-\omega^2 & 2i\mu\omega\\
-2i\mu\omega & k^2-\omega^2
\end{pmatrix}
\begin{pmatrix}\sigma\\q\end{pmatrix}
=
\begin{pmatrix}-g_{\rm C0}J\\0\end{pmatrix}.
\]

Its determinant is

\[
\mathcal D=(k^2+M_\sigma^2-\omega^2)(k^2-\omega^2)
-4\mu^2\omega^2.
\]

Writing `M_H^2=M_sigma^2+4mu^2`, the exact branches are

\[
\omega_\pm^2=k^2+\frac{M_H^2}{2}
\pm\frac12\sqrt{M_H^4+16\mu^2k^2}.
\]

At zero momentum,

\[
\omega_-^2(0)=0,\qquad \omega_+^2(0)=M_H^2.
\]

The exact low-momentum expansion is

\[
\omega_-^2=c_s^2k^2+
\frac{16\mu^4}{M_H^6}k^4+O(k^6),
\qquad
c_s^2=\frac{M_\sigma^2}{M_\sigma^2+4\mu^2}.
\]

Only in the nonrelativistic regime does the `k^4` coefficient reduce to
`1/(4m^2)`.

### 4.1 Stability

The canonical momenta are

\[
p_\sigma=\dot\sigma,\qquad p_q=\dot q+2\mu\sigma,
\]

and the free Hamiltonian is a sum of squares,

\[
\mathcal H_2=\frac12p_\sigma^2
+\frac12(p_q-2\mu\sigma)^2
+\frac12(\nabla\sigma)^2+\frac12(\nabla q)^2
+\frac12M_\sigma^2\sigma^2.
\]

Therefore `lambda_4>=0` gives no scalar ghost and no negative-gradient branch
on this fixed background. `lambda_4>0` gives a nonzero sound speed. If
`lambda_4<0`, the root product
`k^2(k^2+M_sigma^2)` is negative for
`0<k^2<-M_sigma^2`; one branch has `omega^2<0` and the background is
unstable.

## 5. Fixed-background source-pole overlap

Eliminating `q` exactly, without calling the result a metric-reduced physical
mode, gives the radial source response

\[
\sigma(\omega,k)
=-g_{\rm C0}\frac{k^2-\omega^2}{\mathcal D(\omega,k)}J(\omega,k).
\]

After anchoring the lower eigenvector by a positive radial component, its
signed fixed-background source coupling has sign `sign(g_C0)` and
orientation-independent square

\[
g_-^2(k)=g_{\rm C0}^2
\frac{(k^2-\omega_-^2)^2}
{(k^2-\omega_-^2)^2+4\mu^2k^2}.
\]

At small momentum,

\[
g_-^2(k)=
\frac{4g_{\rm C0}^2\mu^2}{(M_\sigma^2+4\mu^2)^2}k^2+O(k^4).
\]

In the nonrelativistic limit, `g_-(k)` is proportional to
`g_C0 k/(2m)`. This is the derivative form factor that lets a gapless mixed
mode reproduce the static inverse-square response when `lambda_4` tends to
zero. It is not a constant fifth-force residue and it is not `V`.

Under `sigma'=r sigma`, the scalar kinetic coefficient becomes `1/r^2` and
the source coefficient becomes `g_C0/r`; their canonical ratio is unchanged.
The result is therefore a field-chart invariant scalar control.

## 6. Static Green function and force classification

For a static source and nonzero `k`, the phase equation forces `q=0`. The
radial equation is

\[
(-\Delta+M_\sigma^2)\sigma=-g_{\rm C0}J.
\]

For `J=M delta^3(x)`,

\[
\sigma(r)=-g_{\rm C0}\frac{M}{4\pi r}e^{-r/\ell},
\qquad
\ell=\frac1{M_\sigma}
=\frac1{\sqrt{2\lambda_4v^2}}.
\]

The second equality is exact for RCP-C0. The frequently quoted
`ell approximately 1/(2mc_s)` additionally assumes the nonrelativistic
relations `mu approximately m` and `lambda_4 v^2 << m^2`.

If `J=M_i delta^3(x-x_i)` is also the classical probe normalization, direct
integration of the displayed canonical action gives

\[
U_{12}(r)=-\frac{g_{\rm C0}^2M_1M_2}{4\pi r}e^{-M_\sigma r},
\]

and

\[
|F_{12}|=\frac{g_{\rm C0}^2M_1M_2}{4\pi r^2}
(1+M_\sigma r)e^{-M_\sigma r}.
\]

Thus the mechanism is:

- inverse-square for `r<<ell`;
- Yukawa suppressed for `r>>ell`;
- exactly long-range only in the `lambda_4->0` limit.

It is neither an AQUAL equation nor a `1/r` acceleration law.

### 6.1 Published factor-two hold

The displayed canonical action gives the short-distance coefficient

\[
\frac{g_{\rm C0}^2}{4\pi}
=\frac{v^2}{2\pi\Lambda^4}.
\]

The 2019 paper and 2026 review print `v^2/(4pi Lambda^4)`. This is an exact
factor-two discrepancy if their stated `J=M delta^3(x)` is also used as the
probe normalization. It may reflect an unstated source-to-particle
normalization, but that cannot be inferred from the scalar action alone.

**Disposition:** `SOURCE_TO_PROBE_NORMALIZATION_UNRESOLVED`. Neither value is
allowed to become an ITSM coefficient until one off-shell matter action fixes
the source normalization.

## 7. Leading-derivative phase EFT versus GP reduction

Define

\[
X_R=-\partial_\mu\Theta\partial^\mu\Theta.
\]

Neglecting radial derivatives, the C0 Lagrangian is algebraic in `s`:

\[
\mathcal L=s\left(X_R-m^2-\frac{J}{\Lambda^2}\right)
-\frac{\lambda_4}{2}s^2.
\]

On its positive-density branch,

\[
s_*(X_R,J)=\frac{X_R-m^2-J/\Lambda^2}{\lambda_4},
\]

and substitution gives

\[
P(X_R,J)=
\frac{(X_R-m^2-J/\Lambda^2)^2}{2\lambda_4}.
\]

At `J=0`, `P_X=s_0=v^2`, `P_XX=1/lambda_4`, and the quadratic phase
action has

\[
\mathcal L_{\pi}^{(2)}=
(P_X+2\mu^2P_{XX})\dot\pi^2-P_X(\nabla\pi)^2.
\]

It reproduces

\[
c_s^2=\frac{P_X}{P_X+2\mu^2P_{XX}}
=\frac{\lambda_4v^2}{\lambda_4v^2+2\mu^2}.
\]

This reduction is not valid wherever the radial gradient creates the
nonlocal force. In the nonrelativistic regime it requires momenta below the
collective scale, parametrically `k<<m c_s`. Its expansion of the portal is a
local derivative coupling plus contact terms; it cannot be used to claim the
full Yukawa/Coulomb profile.

For the separate nonrelativistic chart

\[
\Phi=\frac{e^{-imt}}{\sqrt{2m}}\psi
\]

(with the opposite charge sector obtained by complex conjugation), the
Gross-Pitaevskii action is

\[
\mathcal L_{\rm GP}=\frac{i}{2}
(\psi^*\dot\psi-\dot\psi^*\psi)
-\frac{|\nabla\psi|^2}{2m}
-\frac{\lambda_4}{8m^2}|\psi|^4
-\frac{J}{2m\Lambda^2}|\psi|^2.
\]

With `n=|psi_0|^2=2mv^2`, its contact coefficient is
`g_NR=lambda_4/(4m^2)` and

\[
\omega^2=c_{s,{\rm NR}}^2k^2+\frac{k^4}{4m^2},
\qquad
c_{s,{\rm NR}}^2=\frac{\lambda_4v^2}{2m^2}.
\]

The crossover `2mc_s=M_sigma` is the inverse force range. The three
descriptions therefore have distinct scopes:

| Description | Retained content | Validity / loss |
|---|---|---|
| Relativistic two-field kernel | Both poles and exact mixing | Fixed-background scalar EFT domain |
| `P(X_R)` | Leading derivative, algebraic radial response | Loses radial-gradient nonlocality; low `k` only |
| GP/Bogoliubov | NR phonon plus `k^4/(4m^2)` | `k<<m`; does not restore metric constraints |

## 8. Exact nonlinear uniform-sphere control

This subsection applies only to RCP-C0 with `lambda_4=0`, static
`J=+rho_source` inside a sphere of radius `R`, and vacuum source outside.
Writing `varphi=v+h`,

\[
\Delta\varphi=\frac{J}{\Lambda^2}\varphi,
\qquad
x=\frac{R\sqrt{\rho_{\rm source}}}{\Lambda}.
\]

Regularity at the origin and `C^1` matching at `R` give

\[
h_{\rm in}(r)=v\left[
-1+\operatorname{sech}x\,
\frac{\sinh(xr/R)}{xr/R}
\right],
\]

\[
h_{\rm out}(r)=-\frac{v}{\Lambda^2}
\frac{M_{\rm eff}}{4\pi r},
\]

with

\[
M_{\rm eff}=4\pi\Lambda^2R
\left(1-\frac{\tanh x}{x}\right),
\]

or equivalently

\[
\frac{M_{\rm eff}}{M}
=\frac{3(x-\tanh x)}{x^3},
\qquad
M=\frac{4\pi}{3}\rho_{\rm source}R^3.
\]

The limits are

\[
x\ll1:\ M_{\rm eff}\to M,
\qquad
x\gg1:\ M_{\rm eff}\to4\pi\Lambda^2R.
\]

The weak-distortion condition is

\[
x^2=\frac{\rho_{\rm source}R^2}{\Lambda^2}\ll1.
\]

The expression `rho R/Lambda^2<1` in Grok G-A1 is missing one power of `R`
and fails dimensional analysis.

For `J=+rho_source`, the source raises the condensate's local quadratic cost
and expels it from the core. For `J=-rho_source`, the quoted local strong-source
phonon dispersion is

\[
\omega^2=-\frac{\rho_{\rm source}}{4\Lambda^2m^2}k^2
+\frac{k^4}{4m^2},
\]

which is unstable for `k<sqrt(rho_source)/Lambda` once modes of that wavelength
fit within the source. This is a scoped sign no-go, not a proof against every
function `A(s)` in RCP-I1-C.

The screened charge depends on size and density. Even if microscopic test
coupling is universal, macroscopic scalar charge is compactness-dependent.
Equivalence-principle and strong-field sensitivities therefore require their
own calculation.

## 9. RCP-I1-T sign hold

For the literal trace control

\[
\mathcal L_{\rm int}=F_T(s)T_m^{(0)},
\]

the scalar variation contains `F_T'(s) T_m^(0) delta s`. This action must
remain symbolic because the frozen ledger contains an internal sign mismatch:

\[
J=-T,\qquad -\frac{sJ}{\Lambda^2}
=+\frac{sT}{\Lambda^2}.
\]

Therefore direct comparison to C0 requires `F_T=+s/Lambda^2`, whereas the
ledger later states `F_T=-s/Lambda^2`. The latter corresponds to `J=+T`, not
the previously declared `J=-T`.

No action is silently changed here. RCP-I1-T is held as a literal operator
with `F_T` and its sign explicit until a signed erratum is approved. Its metric
variation also contains the functional response of `T_m^(0)` and is not
automatically a universal matter coupling.

## 10. RCP-I1-C conformal variation

The universal action class is

\[
S=S_{\rm EH}+S_\Phi+S_m[\chi,\widetilde g],
\qquad
\widetilde g_{\mu\nu}=A^2(s/M_*^2)g_{\mu\nu},
\qquad A>0.
\]

Define the Jordan-frame tensor and trace by

\[
\widetilde T^{\mu\nu}
=\frac{2}{\sqrt{-\widetilde g}}
\frac{\delta S_m}{\delta\widetilde g_{\mu\nu}},
\qquad
\widetilde T=\widetilde g_{\mu\nu}\widetilde T^{\mu\nu},
\]

and

\[
\alpha(s)=\frac{d\ln A}{ds},
\qquad
T_E=A^4\widetilde T.
\]

At fixed Einstein metric and matter variables,

\[
\delta\widetilde g_{\mu\nu}
=2\alpha\widetilde g_{\mu\nu}\delta s,
\]

so the source is derived, not pasted in:

\[
\boxed{
\delta S_m=\int d^4x\sqrt{-g}\,\alpha(s)T_E\,\delta s
}.
\]

The scalar background equation for a constant trace is

\[
\mu^2=U_s(s_0)-\alpha(s_0)T_{E0}.
\]

For a zero-matter background and a first-order nonrelativistic dust probe,
`T_E=-J_E`, `delta s=rho_0 sigma+O(sigma^2)`, hence

\[
\mathcal L_{\rm source}^{(1)}
=-\alpha_1\rho_0\sigma J_E,
\qquad
g_{\rm I1C}=\alpha_1\rho_0.
\]

Here `[alpha_1]=-2` and `[g_I1C]=-1`, as required. At this order C0 is
recovered by `alpha_1=+1/Lambda^2`, consistent with the signed trace map in
section 9.

For a nonzero matter background the quadratic radial mass is not fixed by
`alpha_1` alone. Define

\[
\Xi_T=\left.\frac{d(\alpha T_E)}{ds}\right|_0
=\alpha_2T_{E0}
+\alpha_1\left.\frac{dT_E}{ds}\right|_0.
\]

Then

\[
M_{\sigma,{\rm matter}}^2
=\rho_0^2\left[U_{ss}(s_0)-\Xi_T\right].
\]

The response `dT_E/ds` is a matter susceptibility determined by the off-shell
matter system, including its equation of state and metric response. It is not
specified by quoting `alpha_1` and `alpha_2`. Singular coefficients and
stability therefore cannot be tested for a dense medium until `A(s)` and the
matter action are fixed.

Consequences:

- linear vacuum-probe response is calculable but proportional to free
  `alpha_1 rho_0`;
- the RCP-C0 nonlinear sphere cannot be imported into an arbitrary `A(s)`;
- classical four-dimensional Maxwell theory is conformally invariant and
  traceless, so there is no direct classical scalar-photon trace vertex;
- universal Jordan-metric coupling gives the usual test-body weak-equivalence
  structure, but screened/compact-body sensitivities and the strong
  equivalence principle remain open;
- PPN and lensing require the coupled metric solution.

**RCP-I1-C disposition:**
`HEALTHY_LINEAR_PROBE_DOMAIN_CALCULABLE_FREE_NORMALIZATION`.

## 11. Why this is not yet an on-shell ITSM background

RCP-I1-C includes Einstein gravity, but the Max calculation was authorized to
remain fixed-background if no declared on-shell support existed. For the
finite-density state,

\[
\varepsilon+p=\mu^2\rho_0^2>0.
\]

A cosmological constant changes `epsilon` and `p` by opposite amounts and
cannot cancel this enthalpy. Flat Minkowski space is therefore not a solution
of the displayed Einstein-plus-condensate action for `mu rho_0 !=0` unless an
additional supporting sector is specified.

The honest next background is a self-consistent FRW/inhomogeneous solution or
a separately declared compensating sector. Freezing the metric is valid for
the comparator calculation but cannot establish the physical scalar metric
mode, signed gravitational residue, PPN parameters or lensing potentials.

This triggers the predeclared Max stop condition. No lapse/shift/metric
constraint has been eliminated.

## 12. Parent-shape insight: a bounded sextic route

The algebraic parent-to-phase map can be classified without observational
input. Let

\[
U(s)=m^2s+\frac{\kappa_n}{n}s^n,
\qquad n>1.
\]

Neglecting radial derivatives gives

\[
X_R-m^2=\kappa_n s^{n-1}
\]

and therefore

\[
P(X_R)=\frac{n-1}{n}\,
\kappa_n^{-1/(n-1)}(X_R-m^2)^{n/(n-1)}.
\]

The exponent is `3/2` if and only if `n=3`:

\[
U(s)=m^2s+\frac{\kappa_3}{3}s^3
\quad\Longrightarrow\quad
P(X_R)=\frac{2}{3\sqrt{\kappa_3}}(X_R-m^2)^{3/2}.
\]

Since `s^3=|Phi|^6`, this gives an exact **operator-shape lead** for the
relativistic-parent-to-phonon programme. It also explains why the current
quartic parent (`n=2`) can only give a quadratic `P(X_R)` at this order.

Limits of this insight:

- `[kappa_3]=-2` in four spacetime dimensions, so this is an EFT operator and
  needs a cutoff/UV completion;
- radial-gradient corrections, the full two-field spectrum and stability must
  be rederived for that parent;
- `alpha_1` or the relevant matter coupling remains free;
- the conformal metric, constrained physical residue and actual static
  acceleration equation remain uncomputed;
- no topology or condensate parameter has fixed the coefficient.

The appropriate next registration, if pursued, is a separate
`RCP-I2-S6` action class. It must not be mixed into the completed RCP-C0
calculation post hoc.

## 13. Deterministic verification

Canonical verifier:

```text
Analysis/MAT/MAT-001/M2M3_U1/
  m2m3_u1_fixed_background_checks.py
  outputs/m2m3_u1_fixed_background_summary.json
  outputs/m2m3_u1_fixed_background_summary.sha256
```

Final execution used Python `3.13.9` and SymPy `1.14.0` from `itsm_env`.
Thirty symbolic/dimensional/limit checks passed. Two consecutive final runs
produced the same JSON SHA-256:

```text
391fcb099453ae493056c786b6f784b857d2b2f0a8f2626c8ed161cdc0f77c10
```

Source script SHA-256:

```text
50a6bd0242c227c9287ae178bc772d391ae282de3adf9dbe4f91e9d7e046dd0f
```

Development history is not represented as a false one-shot run. An initial
symbolic assertion exposed an incomplete background substitution in the
`P(X)` comparison and was corrected. A later serialization attempt failed on
a SymPy `BooleanTrue` value and was corrected by explicit boolean conversion.
The final two canonical executions then passed and were byte-identical.

`PASS_BOUNDED_SYMBOLIC_IDENTITIES` is a code/algebra status only. It is not a
physics-gate pass.

## 14. Gate decision and next reasoning mode

| Question | Decision |
|---|---|
| Did the portal supply a scalar source? | Yes, within the fixed-background control |
| Did it derive a MOND-like force? | No; Yukawa/inverse-square only |
| Did it fix the force normalization? | No; `Lambda` or `alpha_1` remains free and a factor-two probe normalization is unresolved |
| Did it derive `K_Q`? | No |
| Did it compute `V`? | No |
| Is the flat gravitating background on shell? | No; nonzero-enthalpy obstruction |
| Is there a healthy scalar domain? | Yes, for repulsive self-interaction and weak probe coupling |
| Is Ultra metric work performed here? | No |

The Max package is complete. It is safe to switch down to High for review,
packaging or a new action-class specification. Ultra is warranted only for a
separately authorized, frozen on-shell amplitude-phase-metric constraint
calculation. Given the standalone force-law no-go, the higher-leverage next
step is first to decide at High whether to register and freeze the sextic
`RCP-I2-S6` parent-shape control.

## 15. Primary comparison sources

- <https://arxiv.org/abs/1812.09332>;
- <https://arxiv.org/abs/2505.23900>;
- <https://doi.org/10.1103/PhysRevD.99.076003>.

These sources establish the external comparator only. They do not validate
ITSM ontology, topology, reservoir physics or gate status.
