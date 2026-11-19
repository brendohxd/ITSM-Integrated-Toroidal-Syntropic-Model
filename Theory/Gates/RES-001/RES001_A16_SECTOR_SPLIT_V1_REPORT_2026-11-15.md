# A16.1 portal allocation and the next physical-memory question

15 November 2026. Existing R4C1 bookkeeping control, Conditional in its
declared action scope. No new action or thermodynamic state is selected.

## Exact allocation result

For W=g_r(u^2+v^2)r^2/4, move a constant fraction eta of -W from the plenum
to the reservoir Lagrangian. With signature (-,+,+,+),

    delta L_P=+eta W,       delta L_R=-eta W,
    delta T_P^{mu nu}=+eta W g^{mu nu},
    delta T_R^{mu nu}=-eta W g^{mu nu},
    delta Q_syn^nu=eta nabla^nu W.

The current sign uses the existing div T_R=-Q_syn convention. Total action,
Euler equations and total stress are unchanged; the matter Lagrangian,
conformal matter metric and matter–plenum current are not reassigned.
This is an allocation identity, not a new solution or observable calculation.

In an orthonormal homogeneous frame,

    delta rho_R=+eta W, delta p_R=-eta W,
    delta rho_P=-eta W, delta p_P=+eta W,
    delta Q_syn^0=-eta Wdot.

The paired continuity equations retain their signs and expansion terms.
The portal is U(1)-invariant, so this bookkeeping change supplies no charge
creation. Its isotropic metric-proportional stress contributes no spatial
trace-free stress for a fixed observer. This invariance is specific to this
non-derivative scalar-potential reassignment, not every possible stress split.

Holding illustrative sector temperatures fixed would change a naive heat-only
entropy sum by eta Wdot(1/T_R-1/T_P). Rational examples reverse this contribution
when eta reverses. This is a rejection of that incomplete diagnostic, not
physical entropy production, actual ITSM temperatures or a second-law violation.
An operational subsystem/entropy map must transform consistently.

## Verification

[Contract](RES001_A16_SECTOR_SPLIT_V1_CONTRACT_2026-11-15.md) and
[source pins](RES001_A16_SECTOR_SPLIT_V1_INPUTS_2026-11-15.json) were frozen
before running the [versioned executable](../../../Analysis/MasterTests/test_a16_sector_split_v1.py).
[Receipt](../../../Analysis/MasterTests/outputs/a16_sector_split_v1_20261115/receipt.json):
17 exact symbolic/component/rational controls passed; a separate fresh output
directory produced byte-identical receipt bytes. These are same-assistant
controls, not external scientific review or a full curved-background variation.
Metric compatibility supplies div(g W)=grad W; the executable exercises the
local orthonormal and homogeneous component identities.

## A16.2: recovered evidence avoids an unnecessary new experiment

The [11 October finite-mode owner](RES001_R4C1_G3N5_DUST_FINITE_K_REPORT_2026-10-11.md),
sections Domain and Initial Data, defines retained observables (D,Vx), not
all matter/force variables. Its two original complementary columns have zero
initial retained signal by construction and subsequently excite dust. They
are not claimed pure fast eigenmodes. By linearity they can be compared with
the zero perturbation in that same registered linear system.

The [12 October certificate](RES001_R4C1_G3N5_DUST_CERTIFIED_NUMERICAL_REPORT_2026-10-12.md)
covers all four original columns over [0,0.05] at ell=4,8,16,32,64. It retains
nonmonotonic complementary response. This assessment read the owners and
initial-column construction; it does not claim a fresh certificate replay.
It reuses the original result and its domain/review dependencies.

Consequently a proposed diagnostic using exactly these retained observables
and original probes is already answered in scope: (D,Vx) alone is not an
autonomous state for this full linear control. This does not establish failure
for every enlarged retained state, a physical thermal bath, irreversible memory,
or a unique reservoir contribution. Choosing additional retained rates or fields
defines a different test and requires a fresh equality-of-initial-state check.

The [exact split owner](RES001_R4C1_G3N5_DUST_REMAINDER_REPORT_2026-10-11.md)
already provides Wdot=(M+Delta)W+R r and rdot=S W+J r with moving maps retained.
Here W is that owner's two-component observable, not the scalar portal above.
It is the appropriate starting point for separating hidden-initial-state forcing
from history feedback. No physical kernel or Markov approximation is computed
in this checkpoint.

## Next bounded calculation

Use the existing exact split to identify which complement channels feed the
observable, distinguish internal force/frame/condensate/reservoir contributions,
and retain canonical constraints and coordinate invariance. Establish whether
the intended enlarged retained state admits distinct covered initial states.
Then construct the corresponding deterministic history operator and hidden-state
forcing with error control. Statistical noise/entropy statements additionally
need a declared ensemble and physical subsystem map. Do not execute the gated
microscopic reservoir programme or adopt a bath merely to obtain a kernel.

For tests of organizing stress, total metric response and the fixed-observer
trace-free channel avoid the particular potential-allocation ambiguity above;
their dynamics and physical interpretation remain to be derived. No mechanism
for structure selection, matched acceleration or positive entropy is supplied.

Review DEFERRED; physics_pass=false; gate_effect=NONE. MAT matching, original
G1–G6, R-tau domain continuation and physical validity-window holds unchanged.
