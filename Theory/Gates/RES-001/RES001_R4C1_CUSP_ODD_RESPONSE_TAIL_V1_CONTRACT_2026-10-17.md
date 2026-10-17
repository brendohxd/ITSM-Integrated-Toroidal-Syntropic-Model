# R4C1 lower cusp response: complete odd-mode tail, V1

17 October 2026. Master Test1 / RES-001 / unchanged-action Stage2.
Conditional; review DEFERRED; physics_pass=false; gate_effect=NONE.
This independently addresses a missing ingredient of the physical-window task
while the complete weighted-generator replay remains running. It does not
depend on completion of that replay or change the physical GO conditions.

## Owning scope

Use the exact lower e|e| equation in the accepted CUSP3 evolution report,
generic planar frame mass/speed, frozen three family maps and original initial
prescription. Reuse all completed finite-mode integrations, not new fits.
For every odd integer n (both signs), k=40, r_n(0)=r_n_dot(0)=0:

    r_n_ddot+3H*r_n_dot+
        [cV2*(n*k/a)^2+mV2(t)]*r_n
      = -3*A*abs(psi_dot)^3*w*abs(w)*c_n.

c_n is the complex Fourier coefficient of cos(theta)*abs(cos(theta)).
Retain its exact infinite support, signs, and amplitude normalization.
The leading w satisfies the corresponding unsourced n=1 wave equation with
w(0)=1,w_dot(0)=0. All time variables/fields use the existing action units.

## Frozen acceptance

1. Bind the lower equation, generic mass and speed to the unchanged action
   export/source. Apply each family's parameters before bounds, at exact
   eta=1/4,1/64,1/1024. Re-establish the required homogeneous energy/charge
   balances and on-shell bootstrap on [0,1/20]; do not use sampled maxima.
2. Reuse the known coefficient formula; add an explicit all-n tail/response
   bound, not just another finite quadrature of the already known spectrum.
   Derive positive modified-wave energy and its differential inequality for
   every odd n. Keep H, a, mV2, and momentum drift; no frozen-background or
   analytic-cubic replacement. Constants and domain must be explicit.
3. Give explicit homogeneous Fourier Sobolev tail bounds for displacement and
   velocity, including the eta^(7/2) scale and N-dependent convergence domain.
   State what happens at endpoint exponents and preserve n=1,3. No sharp
   regularity assertion for a solved response follows from an upper bound.
4. Bind w(0),w_dot(0) and zero lower data to all18 immutable archived runs.
   Test the resulting inequality against every stored lower-mode sample.
   These are independent controls, not the continuous proof. Include an exact
   nonzero omitted n=5 witness and reject cosine-amplitude/complex-coefficient
   confusion and omitted mass/momentum drift.
5. Fresh exclusive receipts, versioned executable, all transitive pins and
   source/available-sidecar hash-size-mtime checks; exact read-only replay.
   Preserve failures, original sources and three inherited missing sidecars.
   Do not weaken acceptance after observing a result.

This is a theorem for the lower transverse response component of the declared
perturbation expansion. It is NOT a bound for the complete order-|e|^3
metric/frame/dust/regulator response, a constraint solution for all amplitudes,
an all-order nonlinear remainder, or a physical cutoff/GR/matching clearance.
The mean and even coupled outputs retain their separate constraints and source
terms; no branch is deleted from the programme because this lemma is scoped.

Inherit CUSP3-EVOLUTION-V1, G3N4 force coverage, generic action/evolving
reduction and all transitive deferred review debt. Stage1 complete only its
registered linear B1 scope; Stage2 incomplete/no physical family GO; Stage3
not entered; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No commit, push, publication, submission, vault mutation, provider dispatch,
or model/runtime configuration change.
