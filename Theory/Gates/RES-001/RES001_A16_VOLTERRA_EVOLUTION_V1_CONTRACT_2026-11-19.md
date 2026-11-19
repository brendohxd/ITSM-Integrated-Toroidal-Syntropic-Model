# A16.2 independent retained Volterra evolution: contract V1

19 November 2026. High confirmed. Unchanged conditional original R4C1/B1.

Independently advance R in the exact retained history law on [0,1/20],
ell=4,8,16,32,64, for the registered radial-rate seed. Retain h0, both kernel
feedback factors, background/map/momentum drift and original constraints.

The advancing algorithm consumes only the validated kernel factors L,Rh,Lp,
the instantaneous A and pressure row P_R, their errors, R(0)=0 and
h0=(0,0,1/ell,0). Supply no full-system R/P trajectory or original hidden
generator to that function. Filter and seal these coefficient inputs before
advancement. Keep the original references for post-solve comparison only.

Solve the causal product-integration recurrence

    J(t)=integral_0^t Rh(s)R(s) ds,
    R_dot=A R+L(h0+J), P=P_R R+Lp(h0+J).

Eight retained variables and four history accumulators are computationally
advanced. The accumulators store the integral; they are not a declaration
of eight memory-free degrees of freedom or discarded initial information.
Use fresh degree-24 polynomial trajectories, continuous tile joins, and
retained coefficient-rounding/tail defects in both equations. No projection
onto the full reference, desired graph, or target data is allowed.

Prove a continuous error certificate. If r_R and r_J bound numerical and
physical-factor defects, lift the numerical curve analytically as
(R_hat,U_h(t,0)(h0+J_hat)). Its mixed-state residual is (r_R,U_h r_J).
The exact moving mixed-to-balanced map and existing full-vector Q-norm
propagator then bound the evolution error without integrating an unproved
initial constant or projecting dynamics. Check the moving-map conjugacy on
the registered shell, its regularity and initial agreement explicitly.
This analytic error lift must not be used to supply advancing trajectories.

Acceptance: uniform retained-state and pressure absolute errors <1e-8 over
the interval; continuous post-solve comparison with the certified full
trajectory <1e-8. Preserve the ell=64 sign change. No independent new seed,
physical domain, thermal reservoir, memoryless approximation or nonlinear
stability is inferred. Computational checks do not clear physical gates.

Controls: causal coefficient/inhomogeneous recurrence; exact zero solution
when hidden initial forcing is removed from zero retained initial data;
retention of J and h0; independent numerical integration of the filtered
Volterra realization; independent rational defect/error-budget audit;
source/input hashes and sealed pre-comparison curve hashes; fresh exact
replays. Preserve failures and original sidecars; update A16.2 and the
deferred-review register. Freeze source and pins before calculation.
physics_pass=false; gate_effect=NONE; Rule-9 DEFERRED. No new action/provider,
publication, paper/PDF/site edit, bulk vault mutation, commit, push or deploy.
