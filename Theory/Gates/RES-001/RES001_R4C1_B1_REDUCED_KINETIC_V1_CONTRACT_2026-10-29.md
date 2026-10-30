# B1 reduced kinetic and instantaneous symplectic control — V1

Frozen before calculation, 29 October 2026. Conditional, review DEFERRED;
physics_pass=false; gate_effect=NONE. This is an independent G2/G4 control,
not replacement or admission of the registered vortical G1 preparation.

## Inputs and scope

Reuse the original R4C1 action and the old homogeneous B1 initial data in
`test_01_r4c1_interacting_background.py`, with the existence theorem in
`RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md`. Do not substitute
the later eta=1/4 B1-frame parameter map. In particular old B1 has g_r=3/7,
not its eta-scaled value. Use the full original ADM weak-action density,
including spatial curvature, potentials, dust and regulator.

At t=0, a=C=1, H=+sqrt(3469/4620), (u,v,r)=(1,0,1),
(u_dot,v_dot,r_dot,psi_dot)=(0,1,1/4,1/5), rho_m=1/5,
V=0, Z=0. Spatial homogeneity and the background equations are inherited,
not inferred from a fresh numerical trajectory.

For a nonzero planar torus mode k, fix delta tau=0 and the three spatial
metric components delta h_xz=delta h_yz=delta h_zz=0. Vary the dust
multiplier first: its positive branch fixes N=tau_dot/C, hence at this
event N=exp(-beta delta psi) and N_z=-beta N delta psi_z. The lapse
equation determines delta epsilon; do not discard its flux or impose an
additional vacuum Hamiltonian constraint. Explain this elimination and
its local positive-dust restriction explicitly.

Use physical spatial metric/frame amplitudes, with delta h=a^2 gamma,
delta V=a^-1 v; retain their 2H gamma and -H v velocity terms. Retain all
three shifts until their nonzero-mode equations are solved. Keep Z until
its own algebraic equation is derived. The norm-cubed force has zero
quadratic variation at zero projected gradient; certify this C2 fact and
retain the physical A coefficient in independent finite-perturbation checks.

## Required calculation and verification

1. Derive the complete local quadratic density at this event, including
   field/velocity/spatial-derivative mixing. Use Hermitian Fourier assembly
   or an equivalent real two-quadrature calculation, not same-sign spatial
   derivatives in both test and trial factors.
2. Solve the shift and auxiliary equations from that density; state their
   determinants and all singular exclusions, including k=0. Construct the
   reduced kinetic block, q-dot/q block and quadratic Hamiltonian map.
3. Determine exact kinetic inertia and an explicit congruence/normalization
   if regular. Retain the antisymmetric q-dot/q contribution in the actual
   instantaneous symplectic form. Do not equate a positive kinetic block
   with gradient stability, full mode stability or a physical cutoff.
4. Check against the original physical density with independent directional
   second differences or automatic differentiation, including curvature and
   physical cubic remainder. Check Hermitian/real-quadrature signs, the
   eliminated equations and the canonical momentum/two-form map.
5. Fresh non-overwriting receipts and immutable replay. Preserve input
   files, old reports and sidecars. Do not interpret check counts as closure.

## Acceptance and holds

A reproducible full instantaneous reduction on the already justified
homogeneous B1 control, or a specific demonstrated obstruction. No claim
of perturbation evolution, interval-wide stability, nonlinear control,
matching, GR recovery, or admission of the nodal warning probes follows.
G1-G6 remain incomplete unless their own scientific requirements are met.
Rule-9 review stays deferred. No new action, new adopted initial state,
weak-product prescription, publication, commit, push or vault mutation.
