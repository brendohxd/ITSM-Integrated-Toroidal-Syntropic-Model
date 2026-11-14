# Compensated-density coordinate defect: dependent-use hold

4 November 2026. This supersedes dependent-use statements in the 4 November
strong-reconstruction bundle, not the preserved original artifacts.

## Finding

The compensated-density owner defines Sigma = rho + e_force + b Z^2/2,
where e_force = p f_p - f and pi_psi = mu f_p. Strong constraint lift V2
instead used delta I_total = M delta Sigma + rho delta M. This is wrong:

    delta I_total = M delta Sigma + rho delta M
                    - M (delta e_force + b Z delta Z).

At fixed metric, field and auxiliary variables the omitted term is
-N p delta pi_psi, which is generically nonzero. A mean-free test variation
also shows why retaining a global charge does not eliminate the local defect.
This is a mathematical coordinate error, not review debt or a label mismatch.

The exact Legendre differential is

    delta e_force = (p/mu) delta pi_psi - p f_p delta mu/mu
                    - sum(f_q delta q) - f_s delta s.

The new executable `test_rtau_sigma_coordinate_defect_v1.py` records 13/13
exact diagnosis/reference/preservation checks. Its receipt is in
`Analysis/MasterTests/outputs/rtau_sigma_coordinate_defect_v1_20261104/receipt.json`.
Replay is required separately. These checks diagnose an error, not physics.

## Affected and unaffected scope

HOLD_SUBSTANTIVE for reuse in the declared Sigma norm of numerical constants
from strong constraint lift V2, its audit's physical interpretation, strong
force coordinate V2, momentum rate lift V1, ordinary velocity remainder V1
and ordinary momentum remainder V2. Their old checks and hashes remain
historical evidence; they do not repair the omitted variation.

The generic canonical inverse, Schur complement/free-velocity identification,
paired gauge identities and momentum constraint identities do not logically
require this rho/Sigma substitution. Their independent algebra can be reused
within its own scope. Their composition with the incorrect strong norm cannot.
The original total-current graph and the compensated-density/other-sector
identities distinguish the two densities and are the repair inputs.

No full generator, evolving-domain energy estimate, physical stability,
finite-time tube or physical clearance was established by the affected work.
This defect supplies neither an instability proof nor an all-action no-go.

## Authorized repair

Follow RES001_RTAU_SIGMA_RECONSTRUCTION_REPAIR_V1_CONTRACT_2026-11-04.md.
Reconstruct I_other = M Sigma directly, preserving the force/regulator
compensation, lapse improvement, constraints and independent charge tangents.
Use new versions and fresh receipts. Revalidate descendants sequentially.
The corrected rest reference alone does not certify the actual inverse.

R-tau UNADOPTED; Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE;
G1-G6 INCOMPLETE. Goal remains ACTIVE and High acknowledged for this repair.
