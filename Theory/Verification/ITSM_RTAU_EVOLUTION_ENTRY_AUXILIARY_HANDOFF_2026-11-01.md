# Prepared evolution entry/auxiliary handoff - 1 November 2026

Goal ACTIVE; High explicitly confirmed. Owner: ../Gates/RES-001/RES001_R4C1_RTAU_EVOLUTION_ENTRY_AUXILIARY_V2_REPORT_2026-11-01.md.
Canonical entry15/15, second spatial jet15/15, auxiliary21/21: ALL exact
replays COMPLETE. Sessions40643/35009 terminal exit0; auxiliary replay
terminal exit0. Older V1/V2 progress/live_handoff notes are historical.
No process remains running from these components; do not duplicate replays.

Flow module r4c1_prepared_canonical_flow_v2.py reconstructs13 nonauxiliary
rates through second spatial order and14 momentum Euler rows. Shift is
still caller-supplied. Auxiliary module r4c1_auxiliary_geometry_rate_v1.py
returns Z/deltaZ through second spatial order and Zdot/deltaZdot VALUES.
Explicit metric third and force fourth inputs are mandatory; time-spatial
jets beyond the supplied inputs are not returned. No independent aux mode.

NEXT: actual gauge-velocity closure, then explicit clock-current density
row and constraint/charge transport. Reuse source specs and existing
private next_geometry_notes.md. In adapted zeta coordinates gauge FP is
(d_zeta(hxx*d_zeta xi_x), d_zeta(hyy*d_zeta xi_y),
2*Abar^2*d_zeta^2 xi_z). Its existing inverse gap handles mean-free sources;
retain harmonic coordinate freedom and physical metric/momentum moduli.
The already-derived w map must transform field/shift/momentum-density
rates together. Canonical dual Lie derivative is (w*p)_z-T(w_z)^T*p,
where Lie_w q=w*q_z+T(w_z)*q. Do not drop its density Jacobian.

Current density evolution uses the explicit action clock flux, not bare
continuity. Fixed clock charge does not authorize quotienting physical
time. Full prepared generator, physical norm and finite-time domain remain
incomplete. Review DEFERRED; physics_pass=false; R-tau unadopted;
G1-G6 incomplete. No action adoption, vault mutation, publication or commit/push.
