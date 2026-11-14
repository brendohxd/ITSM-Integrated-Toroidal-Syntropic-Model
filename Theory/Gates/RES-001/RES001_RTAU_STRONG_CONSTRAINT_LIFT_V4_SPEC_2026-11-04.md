# Corrected compensated-current strong constraint lift V4

4 November 2026. Implements the Sigma reconstruction repair V1 contract.
V2 and its descendants' old numerical norm claims remain held.

Let L_o=L_total-M f-L_reg, with the action's full force and regulator removed.
The ordinary canonical momenta equal those of L_total, whereas pi_psi,o=0.
Use the other-sector lapse improvement F_o=N gamma h^(iz) pi_Vi-N flux/2.
Then I_o=L_o-sum(pi_o*(v-Lie_S q))-D_z F_o=M Sigma exactly.
Its first differential at fixed canonical ordinary momenta has coefficients
C0=L_o,q+index(pi_o,S_z)-D_z F_o,q, C1=L_o,d+S pi_o-F_o,q-D_z F_o,d,
C2=-F_o,d. The canonical momentum coefficients are -material velocity for
ordinary variables and zero for pi_psi. Retain the unchanged spatial momentum
constraints, all integration constants and independent total-I/U1 tangents.

The corrected normal form w=delta Sigma-c P delta pi_psi-alpha D_z delta psi
still applies; its original c and alpha estimates are reused. Source norms
are w in L2, ordinary free fields including moduli in H1, free canonical
momenta in L2, psi in H2, and all three eliminated momentum means.

Independent conformal trace check, with delta hxx=delta hyy=a^2 f:

    L_Sigma = L_current + correction0*f + correction1*D_z f,
    correction0 = -I_total - M*p*f_p - M*a^2*(f_hxx+f_hyy),
    correction1 = -b*M*Z*kappa*psi_z.

Here f_h derivatives hold the proper clock velocity and spatial gradient
fixed. This follows from the canonical Legendre differential and
delta Z=-kappa*psi_z*D_z f; the direct other-action calculation must agree.
The second-derivative trace coefficient and momentum improvement are unchanged.
The rest reference changes by -8/25, giving nonzero-mode mass 17/16 and
mean mass -4951/8400. Do not infer the actual inverse from these alone.

Bound the additional multiplication/first-derivative perturbation in
H1 -> H^-1 and combine with the existing total-current perturbation bound.
Use sixteen closed cells covering the circle, each with full registered root
uncertainty. Require a strict Neumann margin with reference Green norm
8400/4951. No Fourier cutoff, mean deletion or prepared-root refit is allowed.
Derive the one-derivative trace remainder with the corrected A0/A1 and existing
momentum gradient cancellation, retaining coefficient gradients and measure.

Acceptance is an INITIAL corrected reconstruction only, with explicit
constants, exact generic identities, independent compensation checks, source
preservation and immutable replay. Descendant bounds require new versions.
No full generator, evolving-domain norm, stability or physical window claim.
R-tau UNADOPTED; review DEFERRED; physics_pass=false; G1-G6 INCOMPLETE.

## V3 attempt and V4 implementation correction

V3's 16 failed exact-zero checks were interval subtraction X-X dependency,
not evidence of a nonzero clock momentum. V3 remains preserved. V4 proves
the clock-velocity absence by the pinned action dependency graph, uses its
exact zero, and retains a separate interval consistency control. It also
corrects V3's source assembly to keep the TOTAL pi_psi in the longitudinal
spatial momentum constraint. Removing force from I_other must not remove it
from the full momentum constraint. These are implementation corrections;
the action and Sigma norm remain unchanged. Descendants remain held.
