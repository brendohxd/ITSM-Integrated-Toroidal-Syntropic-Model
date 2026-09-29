# R4C1-PD1: physical-domain and GR-limit preflight contract

Date: 2026-09-29. Owner: conditional R4C1-v1 / Master Test 1.
This freezes a **necessary-condition audit**, not a new action, parameter fit,
EFT cutoff, GR construction, or parent-gate pass. The owning Test-1 contract,
R4C1 action, G1 limit audit, S2 propagation audit, and S4H-U envelope retain
their original scopes and statuses.

## Frozen inputs

Pin the live contents before evaluating any assertion:

- R4C1 action: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
- G1 report: `b3f3483ae99c868ee60a09b8bd44dd5375dadbc137d04f239405c159a5a8c404`.
- S2 report: `653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9`.
- S4H-U report: `3517579269b26bed5e9c03315dba67d7241442ec690f332b3808576861001314`.
- B1 executable: `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
- Test-1 contract: `a1fa48eca3db80b510b111d0bc22b5d92904eaa78f4d6e0dbab6840cbc3b7448`.

Do not execute a prior receipt-producing `main()` to obtain constants. Read the
frozen B1 parameter literal and independently compute the assertions below.
Preserve all earlier receipts.

## Questions and declared domain

1. On G1's isolated, nonzero-mode frame/metric control at fixed B1 couplings,
   derive the necessary equality surface for static and cosmological Newton
   constants from the already derived expressions. Evaluate the B1 distance
   from that surface and the exact ratio. This is **not** a full PPN calculation,
   interacting B1 inhomogeneous solution, or all-path GR no-go.
2. For any declared positive monomial family
   `K_Q = K0 eta^q`, `A = A0 eta^a` with `q>0`, test the exponent of the
   canonical spatial `|grad psi_c|^3` coefficient `A/K_Q^(3/2)`.
   State the necessary non-divergence condition and evaluate only G1's
   registered `q=a=1` family. Do not certify another family by changing the
   frozen B1 path or ignoring frame/constraint sectors.
3. Read the R4C1 dimensions and action: `Lambda` appears in the condensate
   sextic potential; `b` is the dimensionless quartic-force regulator
   coefficient. Compute the mass dimensions and B1 values of the formal
   coefficient scales `sqrt(K_Q/b)` and `sqrt(K_Q^(3/2)/A)`.
   They are **not** a matched physical EFT cutoff, scattering bound, or proof
   that the branch is weakly coupled. In particular, no quadratic spatial
   `Y` operator may be invented to label the first scale a measured crossover.
4. Compare S4H-U's sufficient formal-domain thresholds `p0=8*10^13`,
   `k>=4.8*10^15` for the full `[0,4]` interval, and axial
   `|n|>=8*10^14` with the absence of an action-derived physical upper
   momentum. If a future uniform physical cutoff `p_max` is derived, a mode
   admitted for the full interval must obey both `p(t)>=p0` and
   `p(t)<=p_max`; using the conservative sufficient `k` threshold requires
   `p_max>=k` at `a(0)=1`. Without `p_max`, classify overlap as unknown,
   neither passed nor disproved. The coarse S4H-U threshold is not a
   necessary physical threshold.

## Rejection controls and decision rule

Reject: replacing normalized `alpha_i` by bare `c_i`; treating `Q=0` as pure
GR; interpreting the condensate-potential `Lambda=2` or either coefficient
scale as the EFT cutoff; claiming no physical mode solely from the coarse
formal bound; claiming a healthy alternative GR path from its exponent alone;
or converting a local algebra check into Test-1 physics closure.

The executable should return nonzero on an exact-algebra or source-pin failure
and save a separate receipt with every check and unchanged gate statuses.
Even if its local checks pass, the Test-1 parent remains on hold unless the
physical cutoff/domain, full constrained IVP, and healthy continuous GR limit
are independently established. Rule-9 review is deferred, not cleared.
