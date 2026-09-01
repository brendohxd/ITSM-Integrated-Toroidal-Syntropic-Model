# WAK-001 Stage 2 - constrained action variation

**Date:** 2026-08-03
**Calculation status:** `PASS_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES`
**Stage-2 status:** In progress
**Gate status:** Open
**Physics pass:** `false`
**Physical wake law:** Not yet derived

## Question

Does the Route-II conservative trial family give mutually consistent field,
metric and preferred-frame variations on the declared local background?

## Declared calculation family

Use signature `(-,+,+,+)`, a contravariant frame variable $U^\mu$, and

\[
U^\mu U_\mu=-1,
\qquad
h^{\mu\nu}=g^{\mu\nu}+U^\mu U^\nu.
\]

The source remains zero. The constrained local density is

\[
\mathcal L_{W,c}=
\frac{Z_W}{2}(U^\mu\nabla_\mu W)^2
-\frac{Z_Wc_W^2}{2}h^{\mu\nu}\nabla_\mu W\nabla_\nu W
-\frac{M_W^2}{2}W^2
+\lambda_U(U^\mu U_\mu+1).
\]

This is one calculation family. It is not yet the ITSM wake action.

## Variations

The $W$ variation gives

\[
\nabla_\mu\!\left[
Z_W(D_UW)U^\mu-Z_Wc_W^2h^{\mu\nu}\nabla_\nu W
\right]+M_W^2W=0.
\]

Holding contravariant $U^\mu$ independent during metric variation, the
wake-plus-unit-constraint contribution to the frame equation is

\[
\mathcal R_\mu^{(W)}=
Z_W(1-c_W^2)(D_UW)\nabla_\mu W+2\lambda_UU_\mu.
\]

The Hilbert tensor of the wake-plus-unit-constraint calculation is

\[
T_{\mu\nu}^{(W+c)}=
Z_Wc_W^2\nabla_\mu W\nabla_\nu W
+g_{\mu\nu}\mathcal L_W
+2\lambda_UU_\mu U_\nu
\]

on the unit constraint. Whether the final multiplier term is assigned to a
separate $T_W^{\mu\nu}$ or to the parent preferred-frame sector is a
bookkeeping convention that must be fixed by the coupled action. Only the
complete stress tensor is unambiguous.

## Rest-frame identity

For $U^\mu=(1,0,0,0)$, the temporal frame equation gives

\[
\lambda_U=\frac{Z_W}{2}(1-c_W^2)\dot W^2.
\]

Substitution into $T_{00}^{(W+c)}$ returns the canonical density

\[
\mathcal H_W=
\frac{Z_W}{2}\dot W^2
+\frac{Z_Wc_W^2}{2}|\nabla W|^2
+\frac{M_W^2}{2}W^2.
\]

If the constraint/frame response is omitted, the metric energy differs from
the canonical result by

\[
-Z_W(1-c_W^2)\dot W^2,
\]

which is nonzero away from the luminal special case. This negative control is
why the preferred-frame variation cannot be dropped.

## Executable audit

Run:

```powershell
python Analysis\WAK\WAK-001\wak001_route2_action_variation.py
```

The audit checks the unit frame and projector, covariant-to-rest reduction,
canonical momentum and Hamiltonian, dispersion and static susceptibility,
the multiplier solution, metric/canonical energy agreement, the missing-term
negative control, and the shared-frame response. Fourteen checks pass. Two
independent outputs match at SHA-256
`16890ED3F02A6532838F98130859DCEE5FB0740DED89A82A6944C5356230D5EE`.

Expected footer:

```text
STATUS: PASS_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES
STAGE-2: IN_PROGRESS
HOLD: HOLD_COUPLED_FRAME_COMPLETION_AND_MODE_INVENTORY
Physical wake law: NOT_YET_DERIVED
```

## Result and hold

The local constrained variation identities pass. This advances W2.1 but does
not complete it globally: a generic spatial $W$ gradient sources the shared
$U^\mu$ equation. The parent $S_U+S_W$ system must therefore establish
constraint ownership and determine whether $W$ is independent of existing
`Phi`, `U` and `psi` modes.

Record:

`HOLD_COUPLED_FRAME_COMPLETION_AND_MODE_INVENTORY`.

No interaction source, exchange current, dissipation, static AQUAL correction,
metric observable or wake phenomenology is derived.

## Next calculation

Perform W2.5 as a coupled quadratic mode-inventory audit against the declared
`Phi`, `U` and `psi` sectors. Keep `J_W=0`. Do not open W2.6 interaction or
exchange bookkeeping until the new mode is shown not to duplicate an existing
degree of freedom.
