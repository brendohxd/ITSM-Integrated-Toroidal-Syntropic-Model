# Prepared R-tau norm calculation: auxiliary component

2 November 2026. High explicitly acknowledged. The larger physical-norm and
evolving-domain objective remains INCOMPLETE; this is a component calculation.
R-tau is unadopted; physics_pass=false, gate_effect=NONE; review DEFERRED.

## New results

1. Derived and implemented the fixed-coordinate auxiliary rate through two
   spatial derivatives for the full symmetric spatial metric. The exact local
   implementation requires explicit h/h_t jets through order 3 and psi/psi_t
   through order 4. It uses the inverse-metric derivative identity, full product
   terms and actual derivative output (not Taylor coefficients). Missing input
   jets and nonpositive spatial metrics are rejected rather than zero-filled.
2. Derived an auxiliary component bound in H-2 for an L2 scalar velocity, under
   explicit coefficient hypotheses. The bound retains metric time dependence.
   It distinguishes a strong point evaluator's input requirements from what
   a weak evolution estimate might need. No physical norm is selected merely
   by assigning this mathematical Sobolev weight.
3. In the flat all-frequency control, Z_t has L2 norm k^2 for a unit velocity
   Fourier mode, but H-2 norm k^2/(1+k^2)<=1. Thus demanding a bounded L2-to-L2
   rate map solely from the auxiliary relation would be unjustified. This is
   not a prepared coupled stability theorem or a license to remove modes.

See `RES001_RTAU_AUXILIARY_TIME_JETS_V1_CONTRACT_2026-11-02.md` and
`RES001_RTAU_AUXILIARY_WEAK_RATE_V1_2026-11-02.md` for precise formulas,
coefficient assumptions, Fourier convention and limitations.

## Verification and retained failure

Implementation: `Analysis/MasterTests/r4c1_auxiliary_time_jets_v1.py`.
Independent symbolic driver V2:
`Analysis/MasterTests/test_r4c1_auxiliary_time_jets_v2.py`.
Receipt: `Analysis/MasterTests/outputs/rtau_auxiliary_time_jets_v2_20261102/receipt.json`.
All **13 exact controls** pass; read-only recomputation is byte-identical.
Controls compare with direct symbolic Laplace-Beltrami differentiation on a
nonconstant positive full metric, check the complete spatial Lie transport,
flat output and rejected incomplete/nonphysical inputs. These are local exact
controls on rational fixture jets, not interval bounds on the actual root.

V1 driver failed in the Lie fixture because SymPy did not multiply an expression
by a Python Boolean indicator. Its source and failure record are preserved.
V2 uses integer indicators; implementation, equations, fixtures and acceptance
criterion are unchanged. No failed receipt was rewritten.

The exact flat weak-rate identity/probes are recorded by
`Analysis/MasterTests/test_rtau_auxiliary_weak_rate_v1.py`, with a fresh receipt
in `Analysis/MasterTests/outputs/rtau_auxiliary_weak_rate_v1_20261102/` and an
exact read-only replay. The all-k argument is algebraic; finite probes alone
would not prove the continuum conclusion. These same-author controls are not
independent peer review.

All **219 inherited input hashes** match after execution. Original scientific
files and sidecars, failed versions and unrelated dirty work remain unchanged.

## What remains for the real goal

The new helper has not been substituted into the frozen kernel or claimed to
supply its missing global compatible inverse. It returns additional derivatives
only when the caller actually supplies the required smooth jets. The certified
C2 initial shift root is not thereby assigned unproved higher/time regularity.

Next derive the physical observable/weak symplectic norm for the entire coupled
system and quantify its actual prepared coefficient bounds. Retain weighted
range/charges/means, metric moduli and momentum partners, gauge/chart drift,
zero-speed/quartic/subleading mixing and the physical clock flow. The local
auxiliary inequality alone neither controls rough metric velocities nor proves
constraint/domain preservation, a background tube, [0,.05] evolution, interaction
window, GR/local compatibility or matching. No old homogeneous theorem is imported.

No new K_Q, V or numerical acceleration prediction is supplied. No manuscript
or website change follows from this component. No parent adoption, vault
mutation, model dispatch, publication, commit or push occurred.

Native-goal distinction: its tool last reported BLOCKED before the new High
acknowledgement. Work here proceeded under the explicit user instruction; the
available status tool cannot set it active. No native resume or completion is
claimed by this document. The app must resume it for automatic continuation.
