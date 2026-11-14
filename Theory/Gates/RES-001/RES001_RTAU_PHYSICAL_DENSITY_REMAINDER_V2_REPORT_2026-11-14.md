# Initial physical-density remainder: numerical composition

Under the [frozen contract](RES001_RTAU_PHYSICAL_DENSITY_REMAINDER_V1_CONTRACT_2026-11-14.md),
the initial physical-density projection now has a numerical bound for
its lower-order remainder. This is conditional on the registered exact
compatible initial jets, certified root enclosure and unchanged R-tau
comparator. It is not a bound for the whole physical-density rate.

## Retained equation and norm

Use the complete equation and notation of the
[physical-density rate owner](RES001_RTAU_PHYSICAL_DENSITY_RATE_V1_REPORT_2026-11-09.md):

    rho_t = S D rho + j kappa a_phi D^2 xi - a_rho d D^2 zeta
            +(a_rho v+j g-h a_phi)D xi
            +(c d-a_rho r+j v)D zeta-j Jrow D Y18+R_rho.

All derivative terms, including ordinary-to-force coupling and physical
advection, remain explicit. In particular, the nonzero order-two
coefficient -a_rho d and its earlier derivative-order result survive.

Let U be the sum of the original nine input norms: corrected-density L2;
free ordinary configuration H1 including metric moduli; free momentum L2
including xi; auxiliary force L2; absolute force mean; absolute values of
the three eliminated momentum means; and the adapted harmonic coordinate
velocity norm. Then, in the original normalized periodic Sobolev convention,

    ||R_rho||_L2 <= 138337 U.

The interval aggregation's maximum upper endpoint is approximately
138336.126277872. The integer 138337 is the conservative certificate;
decimal displays are not substituted for the binary interval endpoints.
The receipt retains a distinct coefficient for each original input.

## Composition

The exact remainder is

    R_rho = R_w + D_coeff + c(C_S+F0)
            -a_rho R_xi -j R_zeta -h C_chi+B M delta q,
    M=partial_t-S D.

Original-coordinate primitive means, paired clock gauge, harmonic velocity
and coefficient drift are included. With C_name denoting coefficient sup
bounds, the two commutator estimates used are

    ||C_S+F0||2 <= (2 C_S+C_Sz+2 C_v+C_vz)||xi||2
                   +(3 C_dz+C_dzz+2 C_r+C_rz)||zeta||2+||R_xi||2,

    ||C_chi||2 <= C_a_phi_z ||xi||2
                 +(C_v+C_Sz+C_vz)||chi||H2
                 +(C_K_chi+C_K_chi_z)||delta q||H1
                 +(C_psi_z+C_psi_zz)||epsilon^z||H1.

Here C_S is the shift magnitude, distinct from the commutator C_S in the
preceding exact remainder formula. The executable uses named fields to
avoid that notational ambiguity. The ordinary material velocity is bounded
by the gauge-closed canonical L2 rate plus ||S||inf ||delta q||H1.

The time part of D_coeff uses the corrected
[observable drift V3](RES001_RTAU_OBSERVABLE_DRIFT_SIGN_REPAIR_V1_REPORT_2026-11-14.md),
with bound 89 U8. Its spatial part uses

    ||S||inf [ (||c_z||inf+||(a_rho)_z||inf)||delta p||2
              +||h_z||inf||chi||H2+||B_z||inf||delta q||H1
              +||j_z||inf||zeta||2 ].

Spatial B and K_chi derivatives are computed from the generic force,
volume and metric/frame differentials before specialization. In particular

    B_i=f_qi+p f_p (log mu)_qi,
    (K_chi)_i=-N/f_pp [f_p(log mu)_qi+f_pqi]
              -beta N p delta_i,clock.

The exact force invariant
Y=(gamma^2-1)p^2+2 gamma w p s+(kappa+w^2)s^2
justifies the generic geometric chain rule. The bare clock B coefficient
is zero; its gradients, momentum and regulator effects are retained in
the other terms. Whole-circle spatial jets include the previously
certified third shift derivative and the prepared root uncertainty.

## Twenty-direction comparison and limitations

Apply the exact initial state map of
[the Y20 owner](RES001_RTAU_DENSITY_STATE_MAP_V1_REPORT_2026-11-14.md):

    U <= 5||Y20||2+sqrt(2)|mean(phi)|+Cmod|metric_moduli|
         +|mean(chi)|+sqrt(3)|eta|+|harmonic_velocity|,
    Cmod=exp(4/13000)sqrt(1+4/13000^2).

Thus the remainder's Y20 coefficient is below 691681. After the registered
periodic normal form, its state coefficient is below 1737538. Original
finite-dimensional partners keep their separate weights in the receipt.
The large constants are conservative estimates, not numerical growth
measurements, useful-accuracy certificates, stability results or a cutoff.

This finishes the numerical total left open in the physical-density rate
owner. It does not identify the other nineteen actual generator rows,
construct the time derivative of their normal form, establish preservation
of the joint domain or provide an evolving background/energy tube.
The differentiated trace-source estimate remains conditional on compatible
initial jets and uses the independently bounded direct trace rate; it is
not an existence bootstrap. A09.1's wider operator comparison stays open.

## Verification and preservation

The [V2 executable](../../../Analysis/MasterTests/test_rtau_physical_density_remainder_v2.py)
verified 417 pinned inputs and fourteen controls, including the inherited
independent Fourier-convolution projection and omission tests. Its
[receipt](../../../Analysis/MasterTests/outputs/rtau_physical_density_remainder_v2_20261114/receipt.json)
replayed byte for byte. A separate
[audit executable](../../../Analysis/MasterTests/audit_rtau_physical_density_remainder_v1.py)
checks exact rational aggregation of every interval endpoint, the force
geometry identity, the Legendre clock row, the scale-sign defect and
retained holds. Its six controls passed and its separate receipt replayed.
These are complementary checks by the same assistant, not independent
peer review or Rule-9 clearance.

V1 stopped on interval-scalar/spatial-jet multiplication before producing
a receipt. Its source, sidecar and failure record remain untouched. V2
corrects operand ordering and keeps the equations and inputs. The earlier
auxiliary sign correction is separately documented and all V2 historical
observable-drift evidence remains preserved.

R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
Canonical matching, K_Q, V, weak-field normalization and publication
readiness receive no promotion from this initial operator component.
