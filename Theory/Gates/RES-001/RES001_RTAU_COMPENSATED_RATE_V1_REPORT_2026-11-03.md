# Initial complete compensated-density rate bound

3 November 2026. Conditional initial planar calculation. R-tau remains an
unadopted comparator; original R4C1 unchanged. Review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 incomplete. Goal ACTIVE.

## Result and precise domain

The complete linearized time row of the action-derived compensated scalar
density Sigma has a finite H^-1 bound on the registered exact compatible
initial graph. This improves the derivative count of the preceding physical
rho time row, which was bounded in H^-2. The force/frame interaction and
surviving metric/regulator stress are included. No future conformal-metric,
frame-alignment, finite-band or parity restriction is introduced.

This is a forward bound between different spaces at the initial time. It is
not a closed energy inequality, a growth constant, a background lifetime or
a proof of well-posed physical evolution. In particular Sigma in L2 is an
EXPLICIT observable input; its norm is not inferred from Dminus. The old
trace inverse is not assumed to be an inverse in Sigma coordinates.

Owners: [calculation contract](RES001_RTAU_COMPENSATED_RATE_V1_SPEC_2026-11-03.md),
[exact compensated identity](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md),
[canonical rows](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md),
[initial gauge](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V2_REPORT_2026-11-03.md),
and [weak graph](RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md).

## Complete row retained

Use p=(psi_t-S^z*psi_z)/N, s=psi_z, mu=sqrt(h), kappa=h^{zz},
Z=-Delta_h psi, D_t=partial_t-S^z*D_z and

    Sigma=rho+(p*f_p-f)+b*Z^2/2,
    T=kappa*trK-2*Kupzz.

The full force f includes the independent plenum frame and nonzero
norm-cubed interaction. K_Q,A,b,beta are declared diagnostic coefficients;
no microscopic matching value is supplied by this calculation. The exact
owner gives

    D_t Sigma=N*(beta*p-trK)*Sigma-N*trK*f
       -(p/mu)*D_z(N*mu*f_s)-f_s*((N*p)_z+S^z_z*s)
       -sum_metric_frame f_q*D_t q+(p/mu)*E_other
       +b*N*(T*s*(Z_z-beta*s*Z)-trK*Z^2/2)
       +Ward_defect/(N*mu).

All seven non-defect contributions are bounded separately in the receipt.
The Ward term vanishes on the exact constraint root and compatible tangent;
the finite numerical centre is not assumed to have zero defect. This result
does not estimate off-constraint evolution by deleting its defect.

Normal-force first/second derivatives are evaluated on the whole certified
initial root ball with its positive Y branch. The independent normal and raw
canonical representations give consistent force-momentum enclosures. This
is an enclosure consistency check, not a claim that interval overlap alone
proves the Legendre identity; that identity belongs to the exact owner.

E_other is formed from the same action after subtracting the full force and
clock-spatial regulator. Auxiliary columns are excluded by exact sector
independence, not by treating small interval-subtraction remnants as zero.
Metric/frame work retains all six metric and three frame variations.

## Weak products, gauge and explicit constants

The flux derivative uses a*D(g)=D(a*g)-a_z*g. Its multiplier bound needs
only a and a_z. In particular the surviving Z_z stress is estimated weakly
from delta Z in L2, retaining its coefficient derivative. No unprovided
third derivative of the certified shift root is used.

The Eulerian adapted row includes the original shift, coordinate drift and
the corrective gauge shift. The term delta S^z*Sigma_background,z is
estimated as D(delta S^z*Sigma_background)-delta S^z_z*Sigma_background;
only the bounded background Sigma is needed. Scalar and canonical-density
coordinate factors are kept distinct. All harmonic and momentum-mean data,
the weighted longitudinal range condition and the original clock/charge
ensemble remain in force.

With normalized periodic Sobolev norms and the input order

    (Dminus, Qfree_H1_original, Pfree_L2_original,
     force_configuration_H2_original,
     harmonic_coordinate_velocity_adapted, Sigma_L2_original),

the complete initial adapted time row obeys the conservative outward bound

    ||delta Sigma_t,adapted||H^-1
       <=373256*Dminus +9732*Qfree +3842*Pfree
          +0.000301*force_H2 +55.726*harmonic +2.533*Sigma_L2.

These rounded-up constants enclose the receipt's binary interval endpoints.
The whole-root background |Sigma| upper bound is below 0.325969.
Dminus is the existing assembled density/momentum-source and retained-mean
data norm. It remains independent of the new stronger Sigma_L2 input.
The large constants are conservative forward operator bounds; interpreting
them as physical instability rates or usable time scales would be invalid.

## Verification and preservation

[Producer](../../../Analysis/MasterTests/test_rtau_compensated_rate_v1.py):
17/17 controls passed, no failed or unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_compensated_rate_v1_20261103/receipt.json)
and read-only recomputation matched byte for byte. The replay command was

    python -B Analysis/MasterTests/test_rtau_compensated_rate_v1.py --verify Analysis/MasterTests/outputs/rtau_compensated_rate_v1_20261103/receipt.json

The receipt contains binary intervals for every component and total, source
hashes, input order, conditional parameters and explicit non-closure flags.
Controls include whole-root finite coefficients, retained interaction and
stress contributions, exact weak-product algebra and an independent
nonconstant periodic transport pairing. They are same-author checks;
independent scientific review remains deferred. All 219 original source
pins and the snapshotted source/sidecar bytes and timestamps were preserved.
Earlier failed attempts remain intact; this version has no new failed run.

## Next deciding question and implications

Derive the actual compensated-density static operator and its compatible
trace/momentum inverse from the action. Changing rho to Sigma at fixed
unconstrained field data is invertible, but does not prove invertibility of
the constrained chart. Include lapse/volume variation, force-momentum
Legendre dependence, torus means and the original fixed-I ensemble. Do not
replace the original total charge with a fixed Sigma mean.

Only after that test can a candidate physical mixed norm be assessed with
the full symplectic map, zero-speed sector, quartic mode, moving inverse
and actual coupled background tube. A coercive physical energy, nonlinear
domain preservation, interactions/validity window and identifying matching
remain open. No numerical C_chi or a0 follows.

This comparator result establishes no concrete defect in the existing
P1/P2/Thermodynamics/original-R4C1 manuscripts. No public claim or paper
change is warranted. No action adoption, vault mutation/sync, external
review dispatch, publication, commit, push or deployment is included.
