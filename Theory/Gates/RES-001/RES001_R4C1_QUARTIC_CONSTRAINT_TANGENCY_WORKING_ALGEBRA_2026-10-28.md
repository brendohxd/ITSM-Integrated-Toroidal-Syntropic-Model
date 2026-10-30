# Next constraint-tangency calculation: working algebra, NOT VALIDATED

28 October 2026. No result, acceptance or new blocker is claimed in this note.
The accepted total-jerk report remains the owning frontier. High is already
operator-confirmed for the ongoing G1 transport scope; avoid a redundant
model-confirmation loop. This note preserves the next implementation route.

## 1. Hamiltonian/dust-clock compatibility: do NOT assign the answer

Use the original physical fourteen-coordinate density, not its analytic split
alone. q indices: h0..5,V6..8,u9,v10,r11,psi12,Z13. Pi_i=gradient[14+i].
Let E=sum(Pi_i*normal_i)-L be the original proper Legendre energy and
J=gamma*h_inverse[z,i]*Pi_Vi. Initial h=I gives rho_H=-E-partial_z(J).

Compute rho_H_dot from the full coupled generator and compare it with the
separately varied dust-clock current. Do not define rho_dot by that current
and call it a compatibility test. On the homogeneous-clock initial slice,
pT=sqrt(h)*rho/C_matter, and the original current requires

    pT_dot=partial_z(R*pT),
    rho_dot_expected=R*rho_z+(-3H+Rprime+beta*p)*rho.

Check the original clock convention: varying the stated dust multiplier
gives C^2*(grad tau)^2+C^4=0, so at N=1 and tau_z=0 its future root is
tau_dot=C, not 1/C. Here psi=0 initially, C=1. The pT formula above is
consistent with this convention. Verify it against the source before launch.

At the initial metric/velocity, IMPORTANT inverse-metric drift gives

    J_dot=(gamma_dot-2H*gamma)*Pi_Vz
           +gamma*(L_qVz-partial_z(L_dVz)),
    gamma_dot=(H-Hbg)*w^2/gamma.

The -2H*gamma term is REQUIRED by time differentiation of h_inverse[z,i].
It must not be lost by differentiating only the initial shorthand J=gamma*Pi_Vz.
Then rho_H_dot=-E_dot-partial_z(J_dot). E_dot may be evaluated by the
original full gradient along (qdot,actual_acceleration,partial_z(qdot),0,0).
Use two independent complex steps and real/Taylor controls where appropriate.
Retain local flux/density, not a mean-density substitution.

For point controls, reconstruct the NEW quartic shift (source includes
5*b*p*W*w^5*wprime), preferably the independent12-mode Fourier solution,
not the stale quadratic shift. Preserve root/shift residual errors. A tiny
sampled mismatch is not a continuum constraint-transport certificate.

## 2. Independent phase-current tangency

On the initial phase chart, pTheta=u*Pi_v-v*Pi_u=Rc*Pi_v. Compute its time
derivative from the actual acceleration and Hessian-vector evolution:

    pTheta_dot=Rc*Pi_v_dot-D*Pi_u.

The separately varied U(1) current requires pTheta_dot=partial_z(R*pTheta)
on this homogeneous-phase-gradient initial slice. Verify both, retaining
metric volume and frame/phase alignment. Integrals of the periodic currents
and node-interface fluxes can then be assessed, without an evolved charge claim.

## 3. Actual alignment-set jets

Use B(0) and original forcing to calculate all three V accelerations at a node.
Do not infer full alignment from Vy alone. The parent force enclosure makes
the Vx source identically zero, the new symbolic calculation establishes the
Vy source node zero; derive/check the Vz source explicitly before concluding
the full vector's second-time jet. No numerical nodal assignment is allowed.

If Vy has a simple zero and a C2 continuation EXISTS, the implicit node has
z_dot=-Vy_dot/Vy_z and its second derivative follows from the same full
chain rule. Initial zero node velocity/acceleration would not prove alignment
persistence. A kinematic counterexample Vy=sigma*x+a*t^3,Vz=b*t^3 shows
why; it is a rejection control, not an action-derived solution.

## 4. Full constraints remain separate

The original off-shell Ward identity contains vector terms
E_Ua*nabla_nu U^a+nabla_mu(U^mu*E_U nu). Do not discard them or infer
Hamiltonian/momentum propagation from Bianchi balance alone. Derive the
appropriate normalized-frame ADM identity and its needed derivatives before
using it at this regularity. The known weak jerk delta must be retained in
any equation where it actually occurs, even though multiplication by g
kills that particular weighted singular term. A first-time tangency result
does not prove persistence, uniqueness or a nonlinear IVP.

Freeze a new contract/executable before numerical scientific launch. Keep
Conditional/DEFERRED, all substantive holds and originals. No state adoption,
new parent, vault mutation, publication, dispatch or commit/push.
