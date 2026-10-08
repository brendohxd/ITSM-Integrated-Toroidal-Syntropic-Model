# R4C1-G3F: finite-k evolution of the formal slow plane

Date: 2026-09-30. Master Test 1 / conditional R4C1-v1 / G3 family.
Frozen before finite-k calculations. Review DEFERRED; gate effect NONE.

Owning result: [G3A signed slow-action report](RES001_R4C1_G3_SLOW_ACTION_REPORT_2026-09-30.md).
It establishes a negative formal kinetic coefficient but leaves finite-k
control and a physical validity window open. Test finite-k approximation
against the full coupled G3S equations, not another frozen slow equation.
No action, coefficient, background initial data or existing receipt changes.

## Frozen calculation and decision rules

1. Use G3S's canonical equations xddot+G xdot+W x=0. Derive the full
   phase-space generator A=[[0,I],[-W,-G]] and canonical two-form
   J=[[G,I],[-I,0]]. Verify exactly Jdot+A^T J+J A=0, using the full registered
   background flow at fixed comoving k. A time-dependent two-form is not a
   conserved cosmological energy.
2. Use the exported G3E embeddings through their retained force order and
   leading propagating order. Set uncomputed next propagating amplitudes to
   zero, explicitly declaring this truncation. Let x=E_q(t,k)(X,Xdot), with
   B=[[0,1],[-m_E,0]], E_v=E_q_dot+E_q B and E=(E_q,E_v). Obtain the lower
   residual -W E_q-G E_v-E_v_dot-E_v B and initial pullback E^T J E.
   Exact coefficient differentiation uses the full background flow.
3. Use eta=(1,1/4,1/16), a subset of the sealed G3 family, and k=(20,40,80)
   in its existing dimensionless chart. Do not identify these values with
   measured physical wavelengths. Integrate from t=0 to 1, sampling 101
   equally spaced times. Initialize the full 12-dimensional system's two
   columns with E(0,k), corresponding to (X,Xdot)=(1,0) and (0,1).
4. Independently integrate the background by DOP853 and Radau at
   rtol=1e-11, atol=1e-13; require normalized discrepancy <=1e-10. Use the
   DOP853 dense background for both perturbation solvers, isolating their
   comparison. Integrate the slow 2x2 reference at those same tolerances.
   Integrate the full coupled columns by DOP853 and Radau at rtol=1e-9,
   atol=1e-11, with the exact linear Jacobian for Radau. Require solver
   success, full-column method discrepancy <=1e-7, and two-form transport
   drift <=1e-7 relative to the initial symplectic coefficient.
5. Report the entire registered grid, the minimum k/a reached, initial
   symplectic coefficient relative to K_s=1-12/eta, full-column approximation
   error, slow-coordinate/velocity error and embedding residual. The
   approximation error is max_t ||Y-E F_s||_F/(1+||E F_s||_F).
   Require its maximum over the two methods to decrease under both k
   doublings at each eta. The preregistered diagnostic accuracy target is
   <=5% at k=80 for each eta; this is a finite-time approximation target,
   not an observational or publication criterion. Record failures without
   adjusting the grid, interval, tolerances, target or embedding.
6. Check that the initial finite-k symplectic coefficient remains negative
   and approaches K_s under k doubling. Check its preservation along actual
   full-system evolution, not solely on the truncated embedding. Preserve
   sign disagreements and accuracy failures. No claim about arbitrary
   fast-wave initial data, uniform eta->0 control, stationary quantum norms
   or the full PDE is authorized by these finite numerical tests.

Pin direct and inherited inputs; write only a new numbered output directory,
refuse overwrites and support nonmutating replay. Publish no local logs or
private context. The physical EFT cutoff/window remains NOT_DERIVED even
if every finite numerical diagnostic passes. Do not convert a negative
formal sign into a demonstrated physical quantum ghost or all-action no-go.

Inherit R9-MT1-VARIATION/B1/G1/S1/S2/S3/G2/G3/G3S/G3Z/G3E/G3A and their
scope/review debt. Canonical Tests 1-3 HOLD_SUBSTANTIVE; physics_pass=false,
review DEFERRED, Rule9_cleared=false, gate_effect=NONE. MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED;
TOP-X4 unchanged. No PDF work, provider dispatch, commit, push or publication.
