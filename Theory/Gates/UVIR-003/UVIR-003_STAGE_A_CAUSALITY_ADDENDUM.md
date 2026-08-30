# UVIR-003 — Stage-A causality addendum: force-sector characteristic speed

Addendum status: **new Open item identified; does not revise Stage-A PASS**

Scope: characteristic-speed check on the regulated force dispersion relation
already derived in `UVIR-003_STAGE_A_REPORT.md` Section 6. This does not
redo Stage A. It adds a check that Stage A did not perform and that its own
"Not established" list did not name explicitly.

## Executive result

The Stage-A regulated force dispersion relation,

\[
\omega^2
=\frac{1}{K_Q}\left[
3Aq(1+\cos^2\theta)k^2
+\frac{\gamma}{M_*^2}k^4
\right],
\]

has phase velocity $v_{\rm ph}^2=\omega^2/k^2$ that **grows without bound as
$k\to\infty$** for every direction `theta` and every `q>0`, given the
already-established necessary signs `K_Q,A,gamma>0`. Group velocity diverges
alongside it. This is a stronger and more specific statement than the generic
"Not established: … strong-coupling scale" bullet in Section 7 of the Stage-A
report; it identifies exactly which quantity that missing calculation must
resolve before this action can be called causally acceptable, and it further
shows the concern is not confined to the UV.

Two distinct regimes must be separated:

1. **Long-wavelength (`k -> 0`) superluminality**, set entirely by the ratio
   of the background force gradient `q` to `K_Q/A`, independent of the
   regulator (`gamma`, `M_*`). It does not wait on the strong-coupling
   calculation — but it is **not** presently closeable either, because
   `K_Q` has no matching condition anywhere in the declared architecture
   (see revision note below and `Theory/Gates/RECOVERY_SESSION_WORKLOG.md`,
   2026-07-24 entry).
2. **Short-wavelength (`k -> infinity`) superluminality**, forced by the
   `k^4` regulator term itself for every parameter choice. Whether this is
   physically meaningful depends on whether the crossover scale lies inside
   or outside the theory's regime of validity — this **does** wait on Stage
   B item 9 (strong-coupling scale).

Neither point is automatically fatal. UVIR-003 is a preferred-frame
(Einstein-aether-type) construction by explicit Stage-A design choice
(Section 2), and superluminal propagation relative to the metric null cone is
not, by itself, a causality violation in such theories — see
[Blas, Pujolas and Sibiryakov](https://arxiv.org/abs/1007.3503) and
[Jacobson and Mattingly](https://arxiv.org/abs/gr-qc/0007031), both already
cited in the Stage-A report (Sections 1.3–1.4). What such theories require
instead is a globally consistent causal ordering with respect to the
preferred frame's own foliation (no closed causal curves relative to `U^mu`
time), which is a separate, currently unperformed check on general
(accelerating, vortical) `U^mu` backgrounds — already flagged in Section 7 as
"a covariant regulator valid on accelerating or vortical frame backgrounds."
This addendum ties that existing bullet, the strong-coupling-scale bullet,
and the historical archive's `c_s^2~1.11` concern (found in a pre-recovery,
now-superseded Lagrangian; see `Theory/History/FullArchive/` transcript
"Bulletproofing") into one explicit, named calculation.

## 1. Long-wavelength characteristic speed

Take the `k -> 0` limit of the phase velocity directly:

\[
v_{\rm ph}^2(k\to 0)=\frac{3Aq(1+\cos^2\theta)}{K_Q}.
\]

This is finite and independent of the regulator. It exceeds 1 exactly when

\[
q>q_\times(\theta)=\frac{K_Q}{3A(1+\cos^2\theta)}.
\]

Stage A established `K_Q>0` and `A>0` but no relation fixing their ratio, so
`q_×` is currently unconstrained. `A` at least carries a tentative physical
value: matching Stage A's unnormalized `Y` against the `a0`-normalized force
operator declared in `Theory/Core/ITSM_Core_Architecture.md` Section 3.4/4
(`Y_{\rm arch}=h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi/a_0^2`,
`\mathcal L_{\rm IR}=-(2C_{\rm IR}/3)M_P^2a_0^2Y_{\rm arch}^{3/2}`, with
`M_P^2=1/(8\pi G)`) gives exactly `A=C_{\rm IR}/(12\pi G a_0)`, the same
relation already used elsewhere in the architecture, with `C_IR` at least
having a tentative candidate value (the `2/3` geometric-projection matching
hypothesis — itself only Conditional per the ledger).

`K_Q` has no such handle. It does not appear in the static weak-field
Lagrangian (Core Architecture Section 5, which drops all time derivatives),
in any matching relation, or as even a tentative guess anywhere in the
architecture. A field redefinition `psi -> psi/sqrt(K_Q)` can always absorb
`K_Q`'s literal value into redefinitions of `A`, `gamma`, and the background
`q`, so "fixing `K_Q` relative to `A`" is not a free normalization choice —
the redefinition-invariant combination `3Aq(1+\cos^2\theta)/K_Q` is what
must be pinned down in `psi`'s true physical normalization, and no matching
condition for `K_Q` exists yet anywhere in the theory. This most likely has
to come from the same UV-completion / matter-coupling work MAT-001 does for
`C_IR` and `C_m` — and MAT-001 is itself blocked pending UVIR-003. This
corrects an earlier, weaker version of this section that called the
long-wavelength check "closeable now, in principle"; see
`Theory/Gates/RECOVERY_SESSION_WORKLOG.md` (2026-07-24) for the record of
that correction.

## 2. Short-wavelength characteristic speed

At any fixed `q>0` and `theta`, both phase and group velocity diverge as
`k -> infinity`:

\[
v_{\rm ph}^2(k)=\frac{3Aq(1+\cos^2\theta)}{K_Q}+\frac{\gamma}{K_Q M_*^2}k^2
\;\xrightarrow[k\to\infty]{}\;\infty,
\]

\[
v_g(k)=\frac{d\omega}{dk}
\xrightarrow[k\to\infty]{}
2k\sqrt{\frac{\gamma}{K_QM_*^2}}\;\to\;\infty.
\]

This divergence is a direct, structural consequence of choosing a `k^4`
regulator to cure the degenerate `q=0` dispersion (the
[Motohashi–Mukohyama](https://arxiv.org/abs/1912.00378) mechanism the report
already cites in Section 1.5) — it is not a numerical accident of any
parameter choice, and no positive `K_Q,A,gamma` avoids it. The regulator
trades a non-propagating degenerate mode at `q=0` for unbounded superluminal
propagation at large `k`.

This is only physically meaningful within the EFT's regime of validity. The
crossover to `v_ph>1` occurs at

\[
k_{\rm light}^2(\theta)=\frac{M_*^2\left[K_Q-3Aq(1+\cos^2\theta)\right]}{\gamma}
\qquad(\text{when } K_Q>3Aq(1+\cos^2\theta)),
\]

i.e. below the earlier `q_×` threshold this is a genuine second, higher
crossover; above it, superluminality already starts at `k=0`. Stage A's own
roadmap (Section 8, item 9) calls for power counting and the physical EFT cutoff
`Lambda_EFT`. The restricted longitudinal IR NDA scale now available is an
input to that calculation, not a substitute for it. Only the completed
anisotropic and Lifshitz-regime analysis can decide whether `k_light` lies
below `Lambda_EFT` (a prediction within the weakly coupled theory that needs
resolution) or above it (outside the EFT's domain of validity, pending a UV
completion).

## 3. Classification

**Derived** (within the flat decoupling limit already declared in Stage A,
given `K_Q,A,gamma>0`):

- the force-sector dispersion relation has no finite upper bound on phase or
  group velocity as `k -> infinity`, for any parameter choice;
- long-wavelength (`k->0`) superluminality is controlled by `q` versus
  `K_Q/(3A(1+cos^2 theta))` alone, independent of the regulator.

**Open** (not decided by Stage A or by this addendum):

- a matching condition for `K_Q` itself: unlike `A` (tied to `C_IR` via the
  already-declared `a0`-normalized force operator), `K_Q` has no candidate
  value or derivation anywhere in the current architecture; one is needed
  before `q_×(theta)` can be evaluated at all;
- whether `K_Q` and `A`, once that condition exists, place the physically
  relevant background gradient `q~a0` above or below `q_×(theta)`;
- the physical EFT cutoff `Lambda_EFT` for the full anisotropic
  cubic-plus-`k^4` system (Stage A Section 7; Stage B roadmap item 9), and
  whether `k_light < Lambda_EFT` or `k_light > Lambda_EFT`; the available
  longitudinal IR NDA scale does not decide this comparison;
- whether the `U^mu` foliation is causal (no closed causal curves) on the
  accelerating/vortical backgrounds Stage A explicitly defers (Section 7:
  "a covariant regulator valid on accelerating or vortical frame
  backgrounds"), which is the condition that would make metric-superluminal
  propagation in this theory non-paradoxical in the sense of
  Blas–Pujolas–Sibiryakov and Jacobson–Mattingly.

**Not rejected**: this addendum does not find UVIR-003 Stage A's action
inconsistent or reverse its PASS. It sharpens one existing "Not established"
item into two concrete, checkable sub-questions and adds one new one, all
three of which must close before UVIR-003 (not just Stage A) can be marked
PASS, and before MAT-001 can unblock on causality grounds specifically.

## 4. Recommended addition to the Stage B roadmap

Insert an explicit item between roadmap items 6 and 7 in
`UVIR-003_STAGE_A_REPORT.md` Section 8:

> 6a. For the coupled nonzero-gradient dispersion, evaluate `v_ph` and `v_g`
> at `k->0` and compare against 1 across the physically relevant range of
> background gradient `q` (order `a0` and above); for the `k->infinity`
> branch, defer the pass/fail verdict until item 9 establishes the physical
> EFT cutoff, and compare `k_light` against `Lambda_EFT` directly.

## 5. Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_causality_check.py
```

Expected footer:

```text
UVIR-003 Stage-A causality addendum: long-wavelength speed CONDITIONAL (depends on K_Q/A vs q)
Short-wavelength speed: UNBOUNDED for all positive K_Q, A, gamma (structural)
Strong-coupling comparison: NOT PERFORMED (requires Stage B item 9)
STATUS: OPEN
```
