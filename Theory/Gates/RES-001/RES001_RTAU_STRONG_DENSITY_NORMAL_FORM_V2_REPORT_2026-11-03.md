# Second fast-gradient correction with density strength retained

3 November 2026. Conditional initial planar component; review DEFERRED.
R-tau unadopted; original R4C1 unchanged; physics_pass=false;
gate_effect=NONE; G1-G6 incomplete; goal ACTIVE.

## Result and scope

The two-step action/kinematics-derived linear normal form removes the
identified delta Z_z and delta p_z terms from the compensated density row.
It retains L2 density strength with canonical momentum L2 and force
configuration H2. The combined triangular transformation and its inverse
have initial operator bounds below 1.000115587 in the specified product
norm. Its coefficient value, spatial derivative and actual canonical time
derivative are enclosed across the certified initial root ball.

This extends [V1](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_REPORT_2026-11-03.md)
without replacing its source, exact means, drift or primitive commutators.
The full [normal-form/energy contract](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V1_CONTRACT_2026-11-03.md)
remains INCOMPLETE: ordinary coupled derivatives, the other zero-speed
partner, symplectic cross terms, moving constraints/Green maps and an
actual background time tube still need their energy analysis. No complete
fast/slow block diagonalization or physical clearance is claimed.

Execution owner: [V2 criteria](RES001_RTAU_STRONG_DENSITY_NORMAL_FORM_V2_EXECUTION_SPEC_2026-11-03.md).
The [weak-density screen](RES001_RTAU_WEAK_DENSITY_ENERGY_SCREEN_V1_REPORT_2026-11-03.md)
continues to prohibit promoting a density-only H^-1 weakening into the full
energy claim. The present corrections retain the stronger density order.

## Identify the remaining force gradient from the full force

Let p=(psi_t-S*psi_z)/N, s=psi_z, M=N*mu, chi=delta psi and
u1=delta Sigma-c*P(delta pi_psi), where P and c are exactly V1's periodic
primitive and action-current coefficient. The force f retains its independent
plenum frame and nonzero norm-cubed interaction.

V1's remaining local force-gradient terms include

    -(p/mu)*D_z(M*f_s)-f_s*D_z(N*p).

Their coefficient on delta p_z is

    A_p=-N*(p*f_ps+f_s).

The exact raw temporal Hessian has no ordinary/clock-velocity cross block.
After removing the force and regulator, the other action sectors have no
clock-velocity dependence. Thus an ordinary canonical velocity variation
does not hide another clock-momentum gradient in this coefficient test.
Other field derivatives and all existing couplings remain in the remainder.

Define the coefficient from this force, not from fitted mode weights:

    alpha=A_p/N=-(p*f_ps+f_s).

The exact linear clock kinematics are

    chi_t-S*chi_z=N*delta p+Gchi,
    Gchi=-beta*N*p*chi+s*delta S.

Their spatial derivative retains the coordinate-vector term S_z*chi_z:

    (chi_z)_t-S*(chi_z)_z
       =N*delta p_z+N_z*delta p+S_z*chi_z+D_z Gchi.

## Complete second transformed row

Write V1's complete row as

    (u1)_t-S*(u1)_z=C*u1+A_p*delta p_z+Q0.

Q0 is the ENTIRE remaining row after isolating that derivative. It retains
every primitive mean/current term, c_t,c_z, frame/metric/matter/lapse work,
auxiliary terms, gauge corrections and ordinary derivatives from V1.
No part is declared zero to simplify the transformation.

Set

    w=u1-alpha*chi_z
     =delta Sigma-c*P(delta pi_psi)-alpha*D_z(delta psi).

Then the exact row becomes

    w_t-S*w_z=C*w
       +(C*alpha-alpha_t+S*alpha_z-alpha*S_z)*chi_z
       +Q0-alpha*N_z*delta p-alpha*D_z Gchi.

The explicit delta p_z coefficient cancels because A_p=alpha*N.
Coefficient time drift and the vector-weight term -alpha*S_z are retained.
The scalar-gradient/coordinate-transport commutator is exactly

    D_z(S*chi_z)-S*D_z(chi_z)=S_z*chi_z.

An independent periodic calculation checks the entire second row with
nonconstant coefficients. V1's separate density-primitive commutator and
all mean terms still apply. Neither Fourier parity nor a zero mode is
deleted; the force field, its momentum and their means remain in the state.

## Actual coefficient time derivative and inversion

Use pi_psi=mu*f_p from the same action. Its actual canonical Euler time
derivative gives

    p_t=[pi_psi,t-mu_t*f_p
          -mu*(sum_q f_pq*q_t+f_ps*s_t)]/(mu*f_pp),
    s_t=D_z(psi_t).

The q partials hold p,s fixed and include all metric/frame variables. The
force branch Y>0 is retained throughout the certified root ball, and
f_pp>2.999999997 there. No division through a zero interval occurs. No
physical S_t=0 prescription is made: this canonical relation determines
the normal velocity derivative directly, including volume and frame drift.

Directional Taylor AD applies the actual q_t,p_t,s_t to the normal-force
first/second partials to enclose alpha_t. Only the first time coefficient
is used; unused zero higher Taylor slots are not physical assertions.
Independent closed force partial formulas at three prepared locations
check this derivative, including its norm-cubed contribution.

Whole-root outward initial bounds are

    ||alpha||infinity <0.000027941399,
    ||alpha_z||infinity <0.000096560723,
    ||alpha_t||infinity <0.000259815160,
    ||p_t||infinity <0.557761128.

The combined inverse is exact:

    delta Sigma=w+c*P(delta pi_psi)+alpha*chi_z.

On the product of density L2, scalar canonical momentum L2 and force H2,
||P||L2->L2<=1 and ||D_z chi||L2<=||chi||H2. Therefore both the complete
map and its inverse are bounded by

    1+||c||infinity+||alpha||infinity <1.000115587.

Other state data are unchanged. This retains the compensated density's
L2 order and the original physical-density reconstruction; it does not
substitute the earlier weaker density chart or infer an energy sign from
near-identity conditioning. All bounds are INITIAL, not time-uniform.

## Evidence and remaining work

[Executable V2](../../../Analysis/MasterTests/test_rtau_strong_density_normal_form_v2.py):
22/22 checks passed, no failed/unknown controls. Fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_strong_density_normal_form_v2_20261103/receipt.json)
SHA256 4cb333e544b5bdfe24c48f14753c3dd5fbbb926e07e10cc8ca878bedd3383d77.
Read-only recomputation matched the receipt byte for byte, with all 22
controls again passing. All 219 original source hashes
and snapshotted source/sidecar bytes and timestamps are preserved, including
V1. No failed run occurred in this version. Controls are same-author;
independent scientific review remains deferred.

Next test the actual remaining other-action Euler term through its raw-lapse
pullback, before treating its apparent derivatives as independent forcing.
The action source indicates that outside force/regulator sectors psi enters
through the lapse/lapse gradient; the dust multiplier vanishes in this
nonmatter clock-substituted density. An exact sector-wise lapse identity
may reorganize the remainder, but it is not assumed here. Then derive the
complete ordinary/zero-speed/quartic coupled energy with the correct moving
maps. These cancellations do not complete that work.

Actual time-domain preservation, nonlinear admission, physical interactions/
window, GR/local compatibility and identifying matching remain open. No
C_chi or a0 follows and no concrete existing-paper revision is established.
No action adoption, vault mutation/sync, dispatch, publication or Git delivery.
