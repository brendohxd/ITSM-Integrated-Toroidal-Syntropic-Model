# MAT-001 TOP-X4 constraint/projection bookkeeping diagnostic contract

**Date:** 2026-09-18  
**Status:** FROZEN_NON_PROMOTING_METHOD_DIAGNOSTIC  
**Parent:** X4-S2F3 remains unchanged  
**Route:** X4-S4 remains a separately designed new parent  
**Gate effect:** NONE

## 1. Purpose

This contract records one bounded diagnostic motivated by the constrained
system bookkeeping in *Spinning Toroidal Brane Cosmology; A Classical and
Quantum Survey* (arXiv:1901.03292v2):

    https://arxiv.org/html/1901.03292v2

That paper is not an ITSM action derivation. The transferable method point is
that constrained variables must be reduced through their declared constraint
algebra while the induced brackets and projections are retained. This
diagnostic therefore tests only the algebraic source/kinetic reduction that
the current MAT-001/TOP-X4 bridge already requires. It does not claim a full
Hamiltonian Dirac analysis or a physical result.

## 2. Declared synthetic system

The executable uses an exact rational toy quadratic form with three
dynamical variables `q` and two auxiliary variables `a`:

    L2 = 1/2 q^T H_qq q + q^T H_qa a + 1/2 a^T H_aa a
         + c_q^T q + c_a^T a

The auxiliary stationarity equation is retained explicitly:

    H_aa a + H_aq q + c_a = 0.

Only when `H_aa` is invertible may the executable form the Schur-reduced
objects

    H_phys = H_qq - H_qa H_aa^-1 H_aq
    c_phys = c_q - H_qa H_aa^-1 c_a.

The selected mode is checked with its signed source numerator and positive
kinetic norm. Reversing the mode orientation must reverse the signed
numerator; a magnitude-only replacement is rejected.

## 3. Registered checks

The executable must check:

1. all authority inputs and byte sidecars are present and valid;
2. the prior X4-S4 route handoff remains non-promoting;
3. toy matrix dimensions and symmetry are valid;
4. the auxiliary stationarity equation is satisfied by the solved auxiliary
   response;
5. Schur reduction agrees with exact completion of the square;
6. full and reduced quadratic forms agree on the constrained response;
7. the reduced pair is covariant under declared invertible basis changes;
8. the selected mode has positive reduced kinetic norm;
9. orientation reversal changes the signed source numerator;
10. the auxiliary source contribution is retained in `c_phys`;
11. a singular auxiliary block is rejected without a pseudoinverse; and
12. the non-promoting firewall remains closed.

The mutation suite must reject promotion of the physical Hessian, freezing of
X4-S4, modification of X4-S2F3, acceptance of a singular-domain
pseudoinverse, erasure of the orientation sign, and dropping of the
auxiliary source contribution.

## 4. Scientific boundary

This is an algebraic bookkeeping receipt over declared synthetic matrices.
It does not construct the X4-S4 bulk or localized action, choose a warp
profile, derive junction conditions or a compact-space sum rule, compute a
finite-charge background, or evaluate any live TOP-X4 Hessian. It supplies no
`K_Q`, `V`, `G_eff`, `Q^mu`, stress tensor, determinant, counterterm
normalization, or observational prediction.

Binding status remains:

    parent_action_changed=false
    X4-S4_action_frozen=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

## 5. Next single gate

The next substantive gate remains
`TOPX4_H1_X4-S4_NEW_PARENT_ACTION_CONTRACT`. Full action selection,
variation, localized/global consistency and physical-Hessian work require a
separately frozen new-parent contract and the previously reserved Ultra
level of scrutiny.
