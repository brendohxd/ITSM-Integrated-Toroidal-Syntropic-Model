# UVIR-003 — Conditional `K_Q` estimate (speculative, not a derivation)

Status: **speculative order-of-magnitude estimate, explicitly not a
derivation — flags a priority, does not resolve anything**

This extends `UVIR-003_STAGE_A_CAUSALITY_ADDENDUM.md`, which identified that
`K_Q` (the force sector's temporal kinetic coefficient) has no matching
condition anywhere in the declared architecture, blocking a numeric
evaluation of the long-wavelength causality threshold `q_×`. This note tests
one candidate matching hypothesis by dimensional analogy. It is not a
derivation, and every premise below is unconfirmed — flagged as such
throughout, and again here: **do not treat the numeric result in Section 2
as a finding about the theory; treat it as a reason to prioritize deriving
`K_Q` properly.**

## 1. The candidate hypothesis

`UVIR-002_ROUTE_SELECTION.md` (Section on preferred-frame invariants)
declares the temporal invariant with an explicit `a0` normalization,
parallel to how `Theory/Core/ITSM_Core_Architecture.md` Section 3.4
normalizes `Y`:

\[
Q=\frac{U^\mu\nabla_\mu\psi}{a_0}\qquad\text{(UVIR-002)},\qquad
Y=\frac{h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi}{a_0^2}\qquad\text{(Core Architecture)}.
\]

Core Architecture fixes the force operator's overall prefactor by dimensional
necessity: `Y` is dimensionless, so multiplying `Y^{3/2}` by anything of
Lagrangian dimension 4 requires a mass⁴ combination, and the only two scales
the architecture declares are `M_P` and `a0` — giving
`L_IR=-(2C_IR/3)M_P^2a_0^2Y^{3/2}`, which is exactly how `A=C_IR/(12\pi Ga_0)`
was confirmed in the causality addendum.

**The candidate hypothesis is that the same logic applies to the temporal
sector**: a term quadratic in the dimensionless `Q` (with no subtracted
background, `Q_0=0`, matching Stage A's own treatment where `Q=\dot\pi`
directly) built from the same two available scales would need the same
`M_P^2a_0^2` prefactor:

\[
\mathcal L_Q\overset{?}{=}\frac{k_Q}{2}M_P^2a_0^2\,Q_{\rm norm}^2=\frac{k_Q}{2}M_P^2\,Q_{\rm unnorm}^2,
\]

giving `K_Q = k_Q M_P^2 = k_Q/(8\pi G)` for a dimensionless Wilson
coefficient `k_Q`, parallel in role to `C_IR`.

**This relation is introduced only in this conditional-estimate note.** It is
a plausible dimensional analogy, not a matching calculation: neither the
declared action nor the prior architecture derives the temporal sector's
natural scale as `M_P^2a_0^2` rather than something else (for example a scale
tied to the condensate or matter-coupling sector).

## 2. What it would imply, if true

Substituting `K_Q=k_QM_P^2` into `q_×(\theta)=K_Q/(3A(1+\cos^2\theta))`
alongside the confirmed `A=C_{\rm IR}/(12\pi Ga_0)`:

\[
q_\times(\theta)=\frac{k_Q\,a_0}{2\,C_{\rm IR}\,(1+\cos^2\theta)}.
\]

Taking `k_Q\sim1` (naive NDA expectation, unconfirmed) and `C_{\rm IR}\sim2/3`
(the ledger's own tentative geometric-projection candidate, itself only
Conditional):

| direction | `q_×` (formula) | `q_×` (numeric, `k_Q=1,C_IR=2/3`) |
|---|---|---|
| along background gradient (`θ=0`) | `k_Q a0/(4 C_IR)` | `0.375 a0` |
| perpendicular (`θ=90°`) | `k_Q a0/(2 C_IR)` | `0.75 a0` |

Verified symbolically and numerically in
`uvir003_conditional_kq_estimate.py`.

**If both premises hold**, the long-wavelength causality threshold sits
*below* `a0` in every direction — meaning the force operator would already
be superluminal at long wavelength for background gradients at or above
roughly a third to three-quarters of `a0`. Since the operator is explicitly
designed to be the dominant physics precisely where `q` is of order `a0` and
above (the MOND-to-Newtonian transition and beyond — the theory's entire
reason for existing), this would place the superluminal regime inside, not
outside, the theory's intended domain of applicability.

## 3. What this does and does not mean

**Does not mean:** the theory is confirmed broken, or that this is a
finding about UVIR-003 itself. Every input is unconfirmed:

- the `M_P^2a_0^2`-prefactor hypothesis for the temporal sector is an
  analogy, not a derivation;
- `k_Q\sim1` is an unjustified NDA-style guess with no calculation behind
  it;
- `C_{\rm IR}\sim2/3` is already flagged Conditional in the ledger, not
  confirmed.

Three unconfirmed premises stacked together produce a number that could
easily be off by an order of magnitude or more in either direction once any
one of them is actually derived.

**Does mean:** the "K_Q has no matching condition" gap identified in the
causality addendum is not a routine bookkeeping omission that can be
deferred indefinitely. Filling it with the most naively expected values
lands at or past the causality threshold in the theory's own core physical
regime, not safely away from it. That raises the priority of deriving `K_Q`
rigorously — whether from the eventual UV completion MAT-001 needs anyway,
or from an independent matching argument — above where it would sit if this
back-of-envelope estimate had instead come out comfortably subluminal (e.g.
`q_×\gg a_0`).

## 4. Recommended action

Do not cite the `0.375`–`0.75` numbers as a property of ITSM. Cite this note
only as the reason `K_Q`'s derivation should be treated as urgent, alongside
`C_IR`'s, in whatever work eventually addresses MAT-001's blocked matching
program. Ledger row updated accordingly
(`Theory/Core/ITSM_Claim_Migration_Ledger.csv`).

## 5. Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_conditional_kq_estimate.py
```
