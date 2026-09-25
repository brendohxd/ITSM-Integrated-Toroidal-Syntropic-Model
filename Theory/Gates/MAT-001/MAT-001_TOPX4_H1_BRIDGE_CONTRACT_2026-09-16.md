# MAT-001 TOP-X4 to H1 bridge contract

**Date:** 2026-09-16  
**Status:** `FROZEN_NON_PROMOTING_BRIDGE_READINESS`  
**Route disposition:** `TOPX4_PRIMARY_RESEARCH_CANDIDATE_HELD`  
**Candidate parent:** `X4-S2F3`  
**Fallback:** a separately versioned M1/R5-P1 parent redesign  
**Gate effect:** none

**Binding global boundary:** MAT-001 remains `BLOCKED`; UVIR-003 remains
`IN_PROGRESS`; `K_Q` remains `NOT_DERIVED`; `V` remains `NOT_COMPUTED`;
Stage 4A remains `CLOSED`; `physics_pass=false`.

## 1. Purpose

This contract asks whether a future surviving TOP-X4 parent can supply the
same-action, canonically normalized matter residue required by MAT-001 H1.
It freezes the bridge calculation before any new matter sector is selected.

The target is not a convenient numerical value of `K_Q`. The target is the
signed invariant coupling of a declared baryonic source to an oriented,
positive-norm physical scalar mode. A successful calculation could satisfy
MAT-001 through that equivalent action-level invariant even if a standalone
number called `K_Q` is never quoted.

This contract does not modify `X4-S2F3`, adopt a five-dimensional parent as
canonical ITSM, or authorize A4, A5/Ultra, Stage 4A or publication work. Any
physical matter addition requires a separately frozen child action.

## 2. Existing parent boundary

The frozen TOP-X4 control contains five-dimensional gravity, the complex
finite-density condensate `Phi`, a real bulk scalar `chi`, and three neutral
periodic Dirac spectators. In the A1 ledger, `chi` is explicitly a bulk
**matter proxy** used to make an off-shell stress tensor and portal control
well-defined. It is not declared Standard Model matter, a baryonic source, or
an equivalence-principle matter sector.

The S2F3 freeze adds no matter portal, brane term, gauge charge or scalar
coupling to the spectator fermions. Therefore none of `chi`, the Dirac
spectators, the radion or the condensate phase may be relabelled as baryonic
matter by notation.

The present bounded evidence supplies:

- a positive fixed-background canonical radion chart,
  `sigma=sqrt(3/2) M_Pl ln(R/R_ref)`;
- a fixed-metric rank-three scalar operator;
- a theorem-backed scalar-matrix state at its declared mathematical scope;
- a scoped homogeneous curved Dirac operator; and
- the MAT same-action identity `V=g_phi/sqrt(Z_phi)`.

It does not supply a stabilized radion, complete renormalized effective
action, state-dependent stress, constrained physical Hessian, physical matter
action, baryonic source covector, oriented source-carrying eigenmode or
Track-A field-chart map.

## 3. Required constrained source projection

Before auxiliary constraints are removed, write the scalar-sector quadratic
form schematically as

\[
 \Gamma^{(2)}=
 \frac12
 \begin{pmatrix}q\\a\end{pmatrix}^{T}
 \begin{pmatrix}H_{qq}&H_{qa}\\H_{aq}&H_{aa}\end{pmatrix}
 \begin{pmatrix}q\\a\end{pmatrix}
 +J_b\left(c_q^Tq+c_a^Ta\right).
\]

Here `q` contains the retained dynamical scalar variables and `a` contains
lapse, shift and any other auxiliary scalar variables. The candidate `q`
space may include the radion, condensate amplitude and phase, `chi`, and
metric scalar combinations; the physical mode is not selected in advance.

Where `H_aa` is invertible in a declared domain,

\[
 H_{\rm phys}=H_{qq}-H_{qa}H_{aa}^{-1}H_{aq},
 \qquad
 c_{\rm phys}=c_q-H_{qa}H_{aa}^{-1}c_a.
\]

If the auxiliary block is singular, the gauge and constraint reduction must
be performed on the appropriate reduced domain; inserting a formal inverse is
forbidden.

For an oriented physical mode `u_H1`, define

\[
 Z_{H1}=u_{H1}^{T}K_{\rm phys}u_{H1}>0,
 \qquad
 g_{H1}=\frac{c_{\rm phys}^{T}u_{H1}}{\sqrt{Z_{H1}}}.
\]

The R4 source convention fixes the Track-A bridge condition to

\[
 g_{H1}=-\frac{C_m}{\sqrt{K_Q}}=-V_{\rm signed}.
\]

An absolute value or source-source residue `g_H1^2` cannot replace this signed
matching condition. The orientation anchor must be transported through every
basis transformation.

In the four-dimensional natural-unit chart, a canonical scalar has mass
dimension one and baryonic mass/energy density has dimension four. Therefore
`-g_H1 rho_b phi_c` has dimension four only when `[g_H1]=-1`, matching the
MAT unit-chart dimension `[V]=-1`. The density convention and SI time chart
must be named before restoring powers of `c`.

## 4. Matter-architecture decision

Exactly one physical matter realization must be frozen before the source
projection is calculated.

| Option | Required construction | Principal open cost |
|---|---|---|
| Five-dimensional bulk matter | One universal bulk matter action and its reduction, including matter KK modes and the same metric/scalar coupling used in the residue | Light/excited matter spectrum, equivalence-principle and cutoff constraints |
| Four-dimensional brane-localized matter | A localization/brane action, induced physical metric, brane stress and all junction/counterterm conditions | New brane dynamics, junction conditions and localized renormalization |
| Inserted four-dimensional portal | Not admissible inside the frozen parent | It is a different theory and requires a separately frozen action; it cannot be mixed with bulk or brane matter |

No hybrid of bulk matter, brane matter and an inserted portal is admissible.
The current `chi` proxy does not make the bulk-matter option selected.

## 5. Closure requirements

The bridge remains held until all of the following are present in one
versioned evidence chain:

1. one physical matter localization and action are frozen;
2. the complete same-action kinetic and matter-source couplings are varied;
3. the selected TOP-X4 parent has a stabilized finite-charge on-shell
   background with a controlled EFT hierarchy;
4. the renormalized effective action includes scalar, Dirac, graviton, ghost,
   parity/anomaly and normalized counterterm sectors;
5. the auxiliary constraints and singular domains are treated canonically;
6. an oriented positive-norm source-carrying physical mode is identified;
7. the signed residue `g_H1` is computed without an observational target;
8. a field/unit-chart map proves equivalence to the Track-A source invariant;
9. regulator, state, subtraction, cutoff and parameter-domain robustness are
   demonstrated; and
10. independent Rule-9 review is completed before any gate promotion.

## 6. Serial route

1. Preserve the current Plan-11 parent-survival work and all existing holds.
2. Run a bounded bulk-versus-brane physical-matter architecture comparison;
   do not add either option to `X4-S2F3` during the comparison.
3. Only if the parent survives and one matter option is approved, freeze a new
   child action containing that matter sector.
4. Re-vary the complete action, solve the background and construct the
   constrained Hessian and source covector.
5. Calculate `g_H1`, transport its sign/orientation, and test the Track-A map.
6. Reopen Stage 4A only after the invariant and its domain are independently
   reviewed.

The M1/R5-P1 redesign remains a fallback research fork. It is not silently
merged with the TOP-X4 route.

## 7. Rejection tests

Reject a bridge result if it:

- calls `chi` or a neutral spectator the physical baryonic source without a
  new matter action;
- combines bulk and brane matter, or inserts a four-dimensional portal into
  the frozen parent;
- uses the fixed-metric scalar operator as the physical constrained Hessian;
- sets an absent metric/radion/source mixing block to zero;
- computes a residue on an off-shell or unstabilized background;
- replaces the signed vertex by its magnitude or square;
- selects a radius, coefficient or root using `a0`, `H0`, SPARC or another
  desired output;
- reports `K_Q`, `V`, MAT closure or Stage-4A reopening from artifact presence
  or a successful bookkeeping count; or
- treats model agreement as independent Rule-9 scientific validation.

## 8. Binding current decision

```text
HOLD_MAT001_TOPX4_H1_BRIDGE_INPUTS_NOT_CLOSED
matter_architecture=UNSELECTED
physical_mode=NOT_IDENTIFIED
signed_residue=NOT_COMPUTED
track_a_map=NOT_DERIVED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
MAT-001=BLOCKED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```

The next bridge-specific task is the bounded bulk-versus-brane physical-matter
architecture comparison. It may recommend a new child freeze, but it cannot
alter the current parent or promote a gate.
