# UVIR-003 - Stage B scalar ADM readiness audit

Calculation status: **PASS**

Scalar ADM reduction: **BLOCKED PENDING AN ON-SHELL BACKGROUND COMPLETION**

Full UVIR-003: **IN PROGRESS**

MAT-001: **BLOCKED**

## Executive result

The next planned calculation was the complete scalar ADM reduction of the
metric, aether and finite-density condensate around

\[
g_{\mu\nu}=\eta_{\mu\nu},\qquad
\Phi=\frac{\rho_0}{\sqrt2}e^{i\mu t},\qquad
U^\mu=(1,0,0,0),\qquad
\bar\psi=\text{constant}.
\]

That reduction is not yet mathematically well posed. The condensate carries
nonzero background enthalpy,

\[
\rho_\Phi+p_\Phi=\mu^2\rho_0^2>0.
\]

Consequently, Minkowski space is not an exact solution of the declared
Einstein equations. An arbitrary cosmological-constant or vacuum-energy
subtraction cannot repair this because it shifts energy density and pressure
oppositely and leaves their sum unchanged.

The repository architecture contains a reservoir/driver sector that could
support a stationary finite-density state, but Stage A explicitly omitted its
local stress and has not declared its quadratic scalar response. Any support
sector that cancels the condensate background must carry

\[
\rho_R+p_R=-\mu^2\rho_0^2,
\]

so it is not equivalent to a cosmological constant. Its lapse and shift
variations cannot be silently discarded in a full constraint calculation.

The correct scientific outcome is therefore a readiness blocker, not an
off-shell kinetic matrix.

## 1. Declared condensate stress

For

\[
\Phi=\frac{\rho}{\sqrt2}e^{i\Theta}
\]

the minimal condensate action is

\[
\mathcal L_\Phi
=-\frac12(\nabla\rho)^2
-\frac12\rho^2(\nabla\Theta)^2
-V(\rho).
\]

On the homogeneous background \(\rho=\rho_0\), \(\Theta=\mu t\), define
\(s=\rho_0^2\). Then

\[
p_\Phi=\frac12s\mu^2-V(\rho_0),
\qquad
\rho_\Phi=\frac12s\mu^2+V(\rho_0),
\]

and hence

\[
\boxed{\rho_\Phi+p_\Phi=s\mu^2.}
\]

This agrees with the perfect-fluid form of a relativistic superfluid:
the on-shell phase Lagrangian is its pressure, while
\(\rho=\mu n-p\) with \(n=\mu s\).

For the declared mass-quartic-sextic potential,

\[
V(s)=\frac12m^2s+\frac{\lambda_4}{8}s^2
+\frac{\lambda_6}{24\Lambda^2}s^3,
\]

the nonzero stationary branch obeys

\[
\mu^2=m^2+\frac{\lambda_4}{2}s
+\frac{\lambda_6}{4\Lambda^2}s^2.
\]

Its on-shell pressure is

\[
p_\Phi=\frac{\lambda_4}{8}s^2
+\frac{\lambda_6}{12\Lambda^2}s^3.
\]

The stable positive-coupling branch therefore has both nonzero enthalpy and
positive pressure.

## 2. Why a constant subtraction is insufficient

Add an arbitrary constant vacuum energy \(\Lambda_{\rm vac}\). It changes

\[
\rho_{\rm total}=\rho_\Phi+\Lambda_{\rm vac},
\qquad
p_{\rm total}=p_\Phi-\Lambda_{\rm vac},
\]

but

\[
\rho_{\rm total}+p_{\rm total}
=\rho_\Phi+p_\Phi=s\mu^2.
\]

Flat space requires both background Einstein equations to vanish. Their sum
would require \(s\mu^2=0\), contradicting the declared nonzero finite-density
branch. A constant counterterm can cancel either the energy density or the
pressure, not both.

This is not a small bookkeeping tadpole. Eliminating lapse and shift about an
off-shell background can generate gauge-dependent or spurious terms, and it
cannot support the required \(k\rightarrow0\) Hamiltonian audit.

## 3. Required support sector

An exact Minkowski completion would need a support sector satisfying

\[
\rho_R=-\rho_\Phi,\qquad p_R=-p_\Phi.
\]

Therefore

\[
\rho_R+p_R=-s\mu^2\ne0.
\]

This support cannot be represented by a cosmological constant. Before the ADM
reduction, the theory must provide one of the following:

1. a covariant reservoir/driver action and its background solution, including
   its scalar perturbations;
2. a declared external or rigid support approximation, together with the
   regime in which omitting its perturbations is controlled;
3. a self-consistent cosmological background, followed by a subhorizon
   reduction with an explicit hierarchy \(k/a\gg H\).

Option 3 cannot answer the strict low-\(k\) question by itself because the
subhorizon approximation fails as \(k\rightarrow0\).

## 4. Aether normalization correction

The Einstein-aether review used for the existing frame-sector substitution
places the Ricci scalar and aether operators under the same prefactor,

\[
\frac{M_P^2}{2}\left[R-\alpha_i\mathcal O_i\right].
\]

The Stage-A ITSM action instead declares

\[
\frac{M_P^2}{2}R-\frac{M_U^2}{2}c_i\mathcal O_i.
\]

The coefficient dictionary therefore has two parts:

\[
\boxed{\alpha_i=r_Uc_i,\qquad r_U=\frac{M_U^2}{M_P^2}.}
\]

The previous sign and signature map remains correct, but a bare identity map
\(\alpha_i=c_i\) is valid only after imposing \(M_U=M_P\).

The published coupled speeds must be read as

\[
s_2^2=\frac{1}{1-\alpha_{13}},
\]

\[
s_1^2=
\frac{\alpha_1-\tfrac12\alpha_1^2+\tfrac12\alpha_3^2}
{\alpha_{14}(1-\alpha_{13})},
\]

\[
s_0^2=
\frac{\alpha_{123}(2-\alpha_{14})}
{\alpha_{14}(1-\alpha_{13})(2+\alpha_{13}+3\alpha_2)}.
\]

In the weak-gravity-coupling limit \(r_U\rightarrow0\), the vector and scalar
speeds still reduce to the Stage-A frozen-metric ratios
\(c_1/c_{14}\) and \(c_{123}/c_{14}\). Thus that consistency check survives,
while the exact finite-coupling formulas require the corrected normalization.

## 5. Consequence for the force result

The zero-gradient force scalar still factorizes at quadratic order because
every derivative of \(\psi\) begins at first perturbative order. Its healthy
\(z=2\) result for positive \(K_Q\) and \(\gamma\) is unaffected.

The blocker applies to the remaining metric-aether-condensate block. It does
not reverse the force-block partial pass and does not close UVIR-003.

## 6. Gate decision and next move

### Derived

- the declared finite-density condensate has
  \(\rho_\Phi+p_\Phi=s\mu^2>0\);
- no constant vacuum-energy subtraction makes the declared Minkowski
  background on shell;
- a supporting reservoir/driver must have non-vacuum stress and its scalar
  constraint response must be declared;
- the exact Einstein-aether formulas use
  \(\alpha_i=(M_U^2/M_P^2)c_i\).

### Not derived

- the reduced scalar kinetic or gradient matrix;
- the lapse, shift and multiplier solutions;
- the coupled low-\(k\) Hamiltonian;
- the support-sector perturbation spectrum.

### Next required theory decision

The subsequent background-completion screen rejects vacuum energy, a healthy
two-derivative `P(X)` support scalar and the ghost-condensate point as exact
Minkowski support. It selects a self-consistent evolving flat-FRW background
as the least-assumptive route. That route still requires an explicit on-shell
solution before the scalar ADM constraints are eliminated. See
`UVIR-003_STAGE_B_BACKGROUND_COMPLETION.md`.

The subsequent FRW-background calculation has now supplied and verified a
representative on-shell evolving branch. The readiness blocker is therefore
removed; see `UVIR-003_STAGE_B_FRW_BACKGROUND.md`. The scalar reduction itself
remains unperformed.

## 7. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_adm_readiness.py
```

Expected footer:

```text
UVIR-003 scalar ADM readiness identities: VERIFIED
Declared Minkowski finite-density background: OFF_SHELL
Aether normalization: alpha_i=(M_U^2/M_P^2)*c_i
Scalar ADM reduction: BLOCKED_PENDING_ON_SHELL_BACKGROUND_COMPLETION
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_READINESS_AUDIT
```
