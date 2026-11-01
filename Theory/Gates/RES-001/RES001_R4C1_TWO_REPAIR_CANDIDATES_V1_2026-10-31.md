# R4C1 two-route repair comparison: candidate definitions V1

31 October 2026, Australia/Perth. Operator authorized looking at both routes.
These are separate mathematical comparison candidates, not adopted canonical
actions. The frozen R4C1 action and every prior result retain their identity.

## Common baseline and domain

Let S0 be exactly RES001_R4C1_ACTION_FREEZE_2026-09-25.md, including its
first-order auxiliary regulator and boundary convention. Retain signature
(-+++), I x T3, the original potentials, Einstein term, condensate, reservoir,
conformal dust and numerical old-B1 CONTROL coefficients. No observed target
or new physical scale selects a coefficient.

For the existing dust proper-time scalar tau define off shell

    chi = sqrt(-g^{mu nu} partial_mu tau partial_nu tau) > 0,
    t^mu = -nabla^mu tau/chi,
    p_t^{mu nu} = g^{mu nu}+t^mu*t^nu,
    a_t^mu = t^nu nabla_nu t^mu,
    theta_t = nabla_mu t^mu,
    Delta_t psi = p_t^{mu nu} nabla_mu nabla_nu psi
                  + theta_t*t^mu partial_mu psi.

t is future-directed on the chosen branch. Its definition precedes variation
and does not use the dust multiplier equation. [tau]=-1, [chi]=[t]=0.
The unit constraint implies chi=C(psi) only after variation.

Use smooth compactly supported interior variations and periodic spatial
fields. For a temporal boundary comparison, fix tau and its first derivative
as well as the other required endpoint fields. A complete global boundary
value/Cauchy theorem is not asserted by these local candidate definitions.

Write

    L_reg[v] = b*Z^2/2
       - b*(g^{mu nu}+v^mu*v^nu)*partial_mu Z*partial_nu psi
       - b*Z*(v^nu nabla_nu v^mu)*partial_mu psi

for a specified unit future vector v. Bulk auxiliary elimination gives
Z=-Delta_v psi and -b*(Delta_v psi)^2/2 with the declared boundary treatment.

## F-tau: restrict the entire preferred frame before variation

Define S_F by substituting U=t(tau,g) everywhere in S0 before variation and
removing the identically zero multiplier term lambda_U*(U^2+1)/2.
Consequently n=t in force, alignment and regulator sectors as well as in L_U.

Independent U and lambda_U are absent. No additional clock scalar is
introduced. The new tau equation includes the response of all substituted
sectors. Matter and metric variations must include that dependence. This is
a different variational theory, not deletion of the old frame equations
after solving them.

In the dust-clock ADM gauge the frame is the slice normal. Its action term is

    L_U,F = -M_U^2/2 * [
       (c1+c3)*K_ij*K^ij + c2*K^2 - (c1+c4)*a_i*a^i ],
    a_i = partial_i ln N.

This excludes independent twisting of U. It does not itself remove the
separate condensate phase winding/vortex sector; their compatibility and
global domains still require investigation.

## R-tau: change only the regulator's preferred spatial operator

Define

    S_R = S0 + integral sqrt(-g) * (L_reg[t]-L_reg[n]).

Keep independent U, its original unit multiplier, all four frame invariants,
the normalized n in K_Q*(n.partial psi)^2/2-A*Y_n^(3/2), and L_align[n].
No new adjustable coupling or field is added.

The regulator is now spatial with respect to the matter clock, rather than
the independent frame. In the clock ADM gauge it is exactly

    N*sqrt(h)*[ b*Z^2/2 - b*h^{ij}*D_i Z*D_j psi
                         - b*Z*a_i*D^i psi ].

There is no Z time derivative in this expression. Its Euler equation is
Z=-D_i D^i psi, not a discarded degree of freedom imposed by hand. The choice
of the matter clock as regulator foliation is a new physical assumption,
not a microscopic result. U may still tilt or twist independently.

Both routes modify tau dependence. In general neither inherits the original
bare-dust clock current or the original matter-exchange vector unchanged.

## Literature controls, not validation

Jacobson, arXiv:1001.4823v3, provides the before-variation hypersurface-normal
construction and its ADM frame decomposition. Its conventions must be
translated to the baseline signature; its vacuum results do not prove
health of either candidate with the present matter/force couplings.

Langlois and Noui, arXiv:1510.06930v2, supply a constraint-degeneracy precedent.
No DHOST classification or health theorem is claimed for R-tau merely
because its clock-gauge Z velocity is absent.

## Non-adoption boundary

Compare candidate-specific equations and constraints; never substitute a
changed coefficient into a specialized old matrix and call it a new action
derivation. Preserve old-B1 versus vortical B1-frame distinctions.

No microscopic matching, C_chi/a0, physical cutoff, all-sector stability,
GR/PPN recovery or observational success is assumed. Keep both candidates
Conditional and all original scientific gate holds until their own actual
requirements are demonstrated.

