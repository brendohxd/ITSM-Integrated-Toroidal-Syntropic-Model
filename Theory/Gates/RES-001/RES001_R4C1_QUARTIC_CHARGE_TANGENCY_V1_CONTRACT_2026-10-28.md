# Quartic initial dust/phase tangency: frozen diagnostic contract

28 October 2026, Australia/Perth. Conditional; Rule-9 DEFERRED;
physics_pass=false; gate_effect=NONE. G1-G6 remain INCOMPLETE.

## Scope and source

Continue the unchanged R4C1 action, B1 eta=1/4,e=1/500,k=40 quartic
construction. The total-jerk report of 28 October is the owning frontier.
Use the original fourteen-coordinate density and its full coupled Hessian.
Keep metric, frame, condensate, scalar, regulator and local dust feedback.
Do not replace density by its mean, impose a slow graph, invert at w=0,
adopt a new state or parent, or infer time evolution from point controls.

Use the existing restricted four-condition root representative H,U,Ud,W.
Independently reconstruct the new quartic shift by periodic Galerkin assembly:
12 sine modes, 64 quadrature nodes; compare with 8 modes. Include the
5*b*p*W*w^5*wprime source. This is a numerical representative, not a new
continuum/root-error certificate. Preserve earlier certified bounds and holds.

## Independently varied dust current

The frozen action contains L_m=-epsilon*(C^2*(grad tau)^2+C^4)/2,
C=exp(beta*psi). Vary before imposing its multiplier equation. On the
future homogeneous-clock slice tau_dot=C and pT=sqrt(h)*rho/C.
Clock variation requires pT_dot=partial_z(R*pT). Thus, at h=I,psi=0,

    rho_dot_required=R*rho_z+(-3H+Rprime+beta*p)*rho.

This is the comparison target, NEVER the definition of computed rho_dot.
Compute the local Hamiltonian density and its derivative separately:

    E=sum_i Pi_i*normal_i-L,  i=0..13,
    J=gamma*h_inverse[z,i]*Pi_Vi,
    rho_H=-E-partial_z(J),
    rho_H_dot=-E_dot-partial_z(J_dot).

The actual coupled generator defines E_dot. At this initial slice, with
fixed initial shift time derivative, the full inverse-metric drift gives

    J_dot=(gamma_dot-2H*gamma)*Pi_Vz
          +gamma*(L_qVz-partial_z(L_dVz)),
    gamma_dot=(H-Hbg)*w^2/gamma.

Keep the -2H*gamma term. Retain all fourteen velocities in E and normal_i.
Reject omission of that drift and of the beta*p*rho current term if their
effect exceeds the frozen tolerance; report an insensitive control honestly.
If the original-generator balance fails, preserve it as an unresolved
diagnostic; do not change the tolerance or define the answer by conservation.

## Phase current and independent controls

Derive the U(1) identity from the original canonical/alignment/potential
terms. On the initial chart u=Rc,v=0,udot=0,vdot=D and zero phase gradient,

    pTheta=Rc*Pi_v,
    pTheta_dot_actual=Rc*Pi_v_dot-D*Pi_u,
    pTheta_dot_required=partial_z(R*pTheta).

Pi_dot uses the complete acceleration and Hessian-vector generator, not
the required phase-current law. Check the phase spatial current directly
from density gradients. Derive/check dust-clock and U(1) identities exactly
where possible, separately from the numerical comparisons.

Register ten nonnodal controls: theta=pi/4,3pi/4 and both nodes
pi/2,3pi/2 offset by +/-0.1 and +/-0.01. No nodal matrix is inverted.
Use 110 decimal working digits; complex steps 1e-20 and 1e-26; normalized
tolerance 1e-18 for Hessian symmetry, Euler solve, dust and phase balances,
cross-step agreement and shift-ODE residual. Check 8/12 shift agreement
against 1e-25. Use original real/Taylor Euler controls at the two interior
points and real differentiation for energy drift as an independent check.
Record all exceptions and failures. Do not discard nonmonotonic results.

Maximum four independent worker processes. Sort controls deterministically.
Write a fresh receipt directory and replay with a different worker count,
requiring identical scientific bytes. Pin originals, inherited source chain,
contract and executable; verify them before and after the run. Preserve all
attempts, sources, hashes and sidecars. No publication, dispatch, commit,
push, deployment or memory mutation.

## Acceptance and limits

Acceptance here means the registered initial point controls agree with
independently varied current requirements, with the exact identity and
rejection controls stated separately. This is NOT a continuum tangency,
node/interface persistence, ADM propagation, uniqueness, physical-window or
background-admission certificate. Initial nodal jets and full normalized-frame
Ward/ADM transport remain separate required calculations. Never discard
the known weak jerk interface term where it occurs.

All existing substantive holds remain. Review-only debt permits provisional
research; canonical promotion and publication readiness still require review.
