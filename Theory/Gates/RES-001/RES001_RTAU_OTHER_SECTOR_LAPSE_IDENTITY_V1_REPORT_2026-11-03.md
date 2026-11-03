# Local other-sector Euler identity and strong-density reorganization

3 November 2026. Exact classical local identity in the declared nonmatter
clock sector; R-tau remains unadopted, original R4C1 unchanged.
Review DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.
Goal ACTIVE; full coupled physical energy and time tube remain open.

## Result

The other-sector clock Euler term obeys the exact off-shell local identity

    E_other=-beta*N*E_N,other=-beta*I_other=-beta*M*Sigma,
    delta E_other=-beta*(M*delta Sigma+Sigma*delta M), M=N*sqrt(h).

The lapse-gradient improvement and its full variation are necessary. No
scalar Euler equation, Friedmann relation, vanishing local source, global
average or numerical-centre constraint is assumed in this proof. The
nonzero other-action contribution is replaced by the same compensated
density, not set to zero.

This reorganizes the apparent other-sector metric/matter derivatives in
the density and scalar momentum rows. It is not a physical energy theorem,
a renormalized semiclassical action, identifying matching or completion
of the cosmological programme.

Owners: [contract](RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_CONTRACT_2026-11-03.md),
[execution criteria](RES001_RTAU_OTHER_SECTOR_LAPSE_IDENTITY_V1_EXECUTION_SPEC_2026-11-03.md),
[exact compensated definition](RES001_RTAU_COMPENSATED_DENSITY_V1_REPORT_2026-11-03.md),
and [two-step fast normal form](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V2_REPORT_2026-11-03.md).

## Scope: audit the sector before the clock substitution

Remove the FULL independent-frame force and clock-spatial regulator from
the nonmatter action, retaining ADM gravity, the plenum frame, alignment,
canonical matter kinetics and all matter/reservoir potentials. The normalized
local body's remaining proper-velocity dependence has no direct psi,
psi_z or psi_t argument: those dependencies belonged to the removed force/
regulator. Its geometry uses metric/frame slots; the remaining matter
fields and their gradients remain present.

Before clock substitution, other psi dependence comes through N and N_z.
The actual nonmatter lift sets the dust multiplier to zero; it is not a
rule for deleting a nonzero matter term in another action. The source audit
retains all other physical sectors, and the actual raw-lapse partials at
the registered controls independently check this decomposition. Numerical
near-zero interval differences are diagnostics, not exact-zero replacements
inside a bound.

## Exact local lapse homogeneity and improvement

The action's ordinary proper velocities are RV/N, where RV=v-Lie_S q;
frame acceleration terms also contain N_z/N. Treat geometry, frame and
spatial matter data as external arguments in the following identity. The
other action has the form

    L_other=N*F(q,d,RV/N,N_z/N)+N*G(q,d)-N_z*Flux(q,d),

with the volume absorbed into F and the weak curvature terms displayed.
Simultaneously rescaling N,N_z,RV gives the exact Euler homogeneity identity

    L_other=N*L_other,N+N_z*L_other,Nz
                           +sum_other pi_i*RV_i.

No quadratic restriction on the ordinary proper-velocity dependence is
needed. Generic exact differentiation verifies this identity. The actual
weak curvature retains BOTH its lapse and lapse-gradient pieces.

Let B0=N*L_other,Nz. The improved local density is

    I_other=L_other-sum_other pi_i*RV_i-D_z B0
           =N*(L_other,N-D_z L_other,Nz)=N*E_N,other.

The divergence is local and cannot be omitted just because its periodic
integral vanishes. The explicit canonical B0 contains the full frame and
curvature flux from the earlier owner and is independently matched to
the raw lapse derivative in the actual controls.

## Clock pullback and full first variation

On the declared N=exp(-beta*psi) branch,

    L_other,psi=-beta*N*L_other,N-beta*N_z*L_other,Nz,
    L_other,psi_z=-beta*N*L_other,Nz.

Therefore

    E_other=L_other,psi-D_z L_other,psi_z
           =-beta*N*(L_other,N-D_z L_other,Nz)
           =-beta*I_other.

The earlier exact force Legendre/regulator compensation supplies
I_other=M*Sigma. This proves the stated identity OFF SHELL, without using
the clock Euler equation as an assumption. The full first variation gives

    delta E_other=-beta*delta I_other
                  =-beta*(M*delta Sigma+Sigma*delta M).

Metric volume and clock-lapse variations in delta M remain essential.
The source's beta is constant; this formula is not asserted for arbitrary
other clock couplings or actions with additional explicit psi terms.

## Reorganize both complete equations without losing a flux

In the density row, combine the original reaction and other-sector term:

    N*(beta*p-trK)*Sigma+(p/mu)*E_other=-N*trK*Sigma.

Thus the exact material row becomes

    D_t Sigma=-N*trK*Sigma-N*trK*f
       -(p/mu)*D_z(M*f_s)-f_s*((N*p)_z+S_z*psi_z)-W_f
       +b*N*(T*psi_z*(Z_z-beta*psi_z*Z)-trK*Z^2/2)
       +Ward_defect/M.

All metric/frame dynamics remain in Sigma, trK, W_f and the other retained
coefficients. This does not decouple gravity or declare exchange zero.
The Ward term retains its exact constrained-background/tangent scope.

The scalar momentum row is equivalently

    pi_psi,t=D_z(S*pi_psi-M*f_s+d*Z_z-2*beta*d*Z*psi_z)
                  +beta*M*(e_force-Sigma)-beta*L_reg,
    d=b*M*kappa, e_force=p*f_p-f.

The old flux had -L_other,psi_z and the old local source had
L_other,psi. They are replaced TOGETHER by E_other, not individually
discarded. Their exact local identity is why the reorganized equation
contains no independent other-sector Euler derivative term.

The two normal-form corrections remain

    w=delta Sigma-c*P(delta pi_psi)-alpha*D_z(delta psi),
    c=T*psi_z/(mu*kappa), alpha=-(p*f_ps+f_s), P=Dinv*P0.

Their full generic formulas apply with C=-N*trK and the complete new
current/local remainders. The local regulator still supplies
r=beta*d*psi_z on delta Z_z, so its primitive mean/commutator terms are
unchanged. All momentum means, original fixed-I/U1/range conditions,
harmonic data and gauge terms remain. Reaction and remainder definitions
must be changed consistently; split-only old constants are not silently
reused as new strong-source bounds.

## Evidence and limits

[Executable](../../../Analysis/MasterTests/test_rtau_other_sector_lapse_identity_v1.py):
55/55 controls passed, no failed or unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_other_sector_lapse_identity_v1_20261103/receipt.json)
SHA256 152d0af346f902b0325ea0c4ef8be6c1c69cf84b1e350fadf7799cafb95c7594.
Read-only recomputation matched the receipt byte for byte, with all 55
controls again passing.

The proof combines the actual sector structure with generic exact
homogeneity and local Euler/IBP identities. Three prepared-point controls
independently compare raw and clock action expressions, both improvement
coefficients and full local identities. At every point, an all-field/
canonical-momentum/nonzero-shift variation and a separate clock-sector
variation test the full linearization through the certified temporal and
derivative inverses. Tests reject omitted improvement, lapse-gradient
chain terms and physical measure variation. Samples alone would not prove
the operator identity. Controls are same-author; independent review remains
deferred. All 219 original source pins and snapshotted source/sidecar bytes
and timestamps are preserved; no failed attempt occurred in this version.

NEXT: bound the ENTIRE reorganized, two-step density source in L2 on the
declared strong-density/canonical/force domain, keeping every nonlocal mean,
coefficient drift and gauge correction. Only then combine it with the full
ordinary/zero-speed/quartic physical energy. A pointwise identity alone
does not supply that quantitative mixed-domain bound, background time tube,
nonlinear preservation, physical interaction window or matching inputs.
No C_chi or a0 follows. No concrete existing-paper defect or public claim
change is established. No action adoption, vault mutation/sync, dispatch,
publication, commit/push or deployment.
