# UVIR-003 - Stage B background-completion screen

Calculation status: **PASS**

Route decision: **SELF-CONSISTENT EVOLVING FLAT-FRW BACKGROUND SELECTED**

Background solution: **NOT YET DERIVED**

Scalar ADM reduction: **BLOCKED PENDING THE SOLVED ON-SHELL BACKGROUND**

Full UVIR-003: **IN PROGRESS**

MAT-001: **BLOCKED**

## Executive result

The ADM readiness audit established that the finite-density condensate cannot
inhabit exact Minkowski space under the declared Einstein equations unless an
additional sector cancels both its energy density and pressure. This screen
tests the minimal ways of supplying that support.

The exact support requirement is

\[
\rho_R+p_R=-\mu^2\rho_0^2<0.
\]

A cosmological constant fails because its enthalpy is zero. A minimally
coupled, shift-symmetric scalar with Lagrangian \(P_R(X_R)\) can have the
required negative enthalpy only when \(P_{R,X}<0\). The same derivative is the
coefficient of its two-derivative spatial-gradient term, so the required
background is not a healthy short-wavelength support state. The
ghost-condensate point \(P_{R,X}=0\) has zero enthalpy and is also
insufficient. A rigid prescribed stress can support a local decoupling
calculation, but it has no action-derived lapse or shift response and cannot
close the full ADM gate.

Stable null-energy-condition violation is possible in more elaborate
higher-derivative theories, but that would introduce a new microscopic sector
with its own constraint, cutoff and stability gates. It is not a minimal
completion of the declared ITSM action. The relevant literature likewise
treats healthy NEC violation as a substantive EFT construction, not as an
arbitrary background counterterm:

- A. Vikman, *Can dark energy evolve to the Phantom?*,
  <https://arxiv.org/abs/astro-ph/0407107>.
- N. Arkani-Hamed et al., *Ghost Condensation and a Consistent Infrared
  Modification of Gravity*, <https://arxiv.org/abs/hep-th/0312099>.
- P. Creminelli et al., *Starting the Universe: Stable Violation of the Null
  Energy Condition and Non-standard Cosmologies*,
  <https://arxiv.org/abs/hep-th/0606090>.

The least-assumptive next route is therefore a self-consistent, evolving
flat-FRW background using the sectors already declared. This route is
selected, but the background has not yet been solved.

## 1. Exact Minkowski support requirement

For the homogeneous condensate,

\[
\rho_\Phi+p_\Phi=s\mu^2,\qquad s=\rho_0^2>0.
\]

Exact Minkowski space requires the total background stress to vanish:

\[
\rho_R=-\rho_\Phi,\qquad p_R=-p_\Phi.
\]

Therefore

\[
\boxed{\rho_R+p_R=-s\mu^2.}
\]

This is a negative-enthalpy, or NEC-violating, support requirement. It is
stronger than cancellation of the condensate energy density alone.

## 2. Candidate screen

### 2.1 Constant vacuum energy - rejected

For a constant term,

\[
\rho_{\rm vac}=\Lambda_{\rm vac},\qquad
p_{\rm vac}=-\Lambda_{\rm vac},\qquad
\rho_{\rm vac}+p_{\rm vac}=0.
\]

It cannot cancel \(s\mu^2\).

### 2.2 Minimal local \(P_R(X_R)\) scalar - rejected as healthy support

Use signature \((-+++)\) and

\[
X_R=-\frac12\nabla_\mu\chi\nabla^\mu\chi>0
\]

on a homogeneous timelike background. For
\(\mathcal L_R=P_R(X_R)\),

\[
p_R=P_R,\qquad
\rho_R=2X_RP_{R,X}-P_R,\qquad
\rho_R+p_R=2X_RP_{R,X}.
\]

Matching the required exact-Minkowski counterstress gives

\[
P_{R,X}=-\frac{s\mu^2}{2X_R}<0.
\]

Writing \(\chi=\bar\chi(t)+\pi\), the principal two-derivative quadratic
action is

\[
\mathcal L_R^{(2)}
=\frac12\left(P_{R,X}+2X_RP_{R,XX}\right)\dot\pi^2
-\frac12P_{R,X}(\nabla\pi)^2.
\]

Short-wavelength health requires

\[
P_{R,X}+2X_RP_{R,XX}>0,\qquad P_{R,X}>0.
\]

The support requirement and spatial-gradient condition have opposite signs.
If the time-kinetic coefficient is positive, the support state has a gradient
instability; changing the time coefficient's sign instead introduces a
ghost. Thus a healthy two-derivative \(P(X)\) scalar cannot provide the exact
Minkowski support required here.

### 2.3 Ghost-condensate point - insufficient

At \(P_{R,X}=0\),

\[
\rho_R+p_R=0.
\]

Higher-spatial-derivative operators can supply a \(k^4\) fluctuation term, but
the point itself does not supply the missing nonzero background enthalpy.
Moving to a stable NEC-violating construction requires additional operators
and a new theory audit.

### 2.4 Rigid support - decoupling only

A prescribed counterstress may be useful for a local calculation over scales
where the support dynamics is demonstrably negligible. It is not a full
covariant completion: without an action it provides no reservoir perturbation,
Hamiltonian constraint contribution or momentum-constraint response.

It may therefore label a future decoupling check, but it cannot be used for
the strict scalar ADM reduction or the \(k\rightarrow0\) Hamiltonian audit.

### 2.5 Higher-derivative NEC-violating support - open new theory

The screen does not establish a universal no-go against all NEC-violating
theories. Ghost-condensate and Galileon-type constructions show that extra
operator structure can alter the stability conclusion. Adopting such a sector
would add physical degrees of freedom and a new cutoff, and would require:

1. a complete covariant action;
2. an exact background solution;
3. scalar constraint and mode counting;
4. ghost, gradient and tachyon checks;
5. a controlled EFT domain.

No such sector is presently part of the canonical ITSM action, so it is not
introduced by this screen.

## 3. Selected route: an evolving flat-FRW background

For a spatially flat FRW metric, the background equations are

\[
3M_P^2H^2=\rho_{\rm total},
\qquad
-2M_P^2\dot H=\rho_{\rm total}+p_{\rm total}.
\]

Unlike exact Minkowski space, these equations do not require an added sector
to cancel the condensate enthalpy. The condensate, frame and any explicitly
declared reservoir stress instead determine \(H(t)\) and \(\dot H(t)\).

The background cannot retain every Minkowski ansatz unchanged. If
\(n=\mu\rho^2\) is the condensate charge density and the condensate \(U(1)\)
charge is isolated, then

\[
\dot n+3Hn=0.
\]

Hence \(n\propto a^{-3}\), and the amplitude or chemical potential generally
evolves. Exact constant \(n\) in an expanding state would require a separately
declared charge-transfer source

\[
\dot n+3Hn=S_N,\qquad S_N=3Hn.
\]

\(S_N\) is not automatically the same object as the stress-energy exchange
vector \(Q_{\rm syn}^{\nu}\). A model must derive their relationship if the
reservoir transfers both energy-momentum and condensate charge.

## 4. Scope of the route decision

### Derived

- exact Minkowski support requires negative reservoir enthalpy;
- constant vacuum energy cannot supply it;
- a healthy two-derivative \(P(X)\) scalar cannot supply it on a homogeneous
  timelike background;
- the ghost-condensate point has insufficient enthalpy;
- prescribed rigid support cannot close the full ADM constraints;
- an evolving flat-FRW background avoids the artificial exact-Minkowski
  counterstress requirement.

### Selected but not derived

- the self-consistent evolving flat-FRW route is selected for the next
  UVIR-003 background calculation;
- no specific ITSM FRW solution, parameter point or attractor is claimed;
- no stable higher-derivative reservoir completion is claimed;
- the scalar ADM kinetic and gradient matrices remain uncomputed.

This screen rejects an *unspecified minimal reservoir as an exact Minkowski
counterstress*. It does not reject the reservoir ontology or prove that every
possible higher-derivative NEC-violating theory is pathological.

## 5. Next calculation

The next UVIR-003 task is now concrete:

1. derive the homogeneous equations for
   \(a(t),\rho(t),\Theta(t),U^\mu(t)\) and any retained reservoir variables;
2. conserve condensate charge, or declare and derive a distinct \(S_N\);
3. construct at least one verified on-shell evolving branch;
4. reduce the metric-aether-condensate scalar constraints on that branch;
5. use a subhorizon limit only when \(k/a\gg H\);
6. reserve the strict low-\(k\) cosmological audit for the complete
   perturbation system.

This is background construction, not the COS-001 observational fit. COS-001
and PERT-001 remain downstream for the fiducial parameter branch and full
cosmological transfer system.

### Subsequent outcome

`UVIR-003_STAGE_B_FRW_BACKGROUND.md` now derives the homogeneous equations and
verifies a representative on-shell evolving branch. The route-selection task
in this report is therefore complete and the background blocker is removed.
The scalar ADM reduction is ready to begin on that branch, but remains
unperformed.

## 6. Reproduction

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_background_completion.py
```

Expected footer:

```text
UVIR-003 background-completion identities: VERIFIED
Vacuum-energy exact Minkowski support: REJECTED
Healthy two-derivative P(X) exact Minkowski support: REJECTED
Rigid support: DECOUPLING_ONLY
Selected route: SELF_CONSISTENT_EVOLVING_FLAT_FRW_BACKGROUND
Background solution: NOT_YET_DERIVED
Scalar ADM reduction: BLOCKED_PENDING_SOLVED_ON_SHELL_FRW_BACKGROUND
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_BACKGROUND_ROUTE_SELECTION
```
