# Canonical conditioning V1: retain the full frozen quadratic form

20 October 2026. Continue the unchanged R4C1 Stage-2 numerical route from the
complete V3 n17 matrices and their exact replay. This calculation does not
advance Stage3, choose another action or admit a physical state/domain.

## Question and invariant transformation

Can cancellation be reduced by an invertible CONSTANT canonical momentum shear,
without dropping any coordinate, sign, mean, constraint correction or drift term?
Use every entry of the sealed 372-by-372 retained-planar matrices. They already
contain the evolving embedding correction; do not reconstruct another action.

Partition the original, not forcibly symmetrized, numerical form as

    S = [[K,C],[B,M]].

If M is invertible, solve F=M^(-1)*B at arbitrary precision and choose ONLY the
shear generator L=(F+F^T)/2. Symmetrizing L makes the transformation canonical;
it is NOT permission to symmetrize S or erase an antisymmetric mixed component.
For original variables u=T*v, use

    T=[[I,0],[-L,I]],  T^(-1)=[[I,0],[L,I]],
    T^T*Omega_can*T=Omega_can,
    S_new=T^T*S*T,
    S_new_qq=K-C*L-L^T*(B-M*L),
    S_new_qp=C-L^T*M,  S_new_pq=B-M*L,  S_new_pp=M.

Retain both mixed blocks and all raw symmetry errors. No assumption B=C^T or
M=M^T may replace actual entries. No pseudoinverse, eigenvalue clipping, added
regulator, discarded singular direction or threshold-based entry deletion.
Failure to solve M is failure of this representation route, not a theory no-go.

This is a frozen numerical change of coordinates only. Do not add or omit any
physical background drift. Using a time-evolving shear would require its own
time derivative and is outside this calculation.

## Precision and numerical tests

Treat the supplied eighty-digit decimal matrix as the declared numerical input;
working at100 digits does not recreate a higher-precision physical operator or
certify its truncation/discretization error. Perform the shear independently at
80 and100 digits and compare complete transformed forms and complete spectra.
Do all cancellation-prone block algebra BEFORE binary64 eigensolving.

Reuse the V3 NumPy/OpenBLAS full-spectrum evaluator, its constant symplectic
diagonal balancing, fixed independent canonical rescaling, left/right matching,
energy identity and unresolved-mode handling. Keep1e-8 backward/identity and
1e-6 complete-spectrum comparison criteria. Additional coordinate, solve and
precision identities use these same thresholds; no weakened acceptance rule.
Retain every raw failed numerical check and all modes. Passing these tests is
only local finite-matrix numerical evidence, never physical stability/ghost,
healthy-GR, matching, continuum or validity-window clearance.

Check the full mixed solve residual, L symmetry and inverse transformation.
Verify the block formula against independent direct T^T*S*T and Hamiltonian
similarity on exact small rational controls. Check a large mixed-square
cancellation example, negative-energy and real-growing examples, the zero-mode
case, a genuinely antisymmetric mixed remainder and singular-M rejection.
Evaluate original-coordinate eigenpair residuals after back-transformation;
retain the canonical norm under the full transformation. Backward residuals
and precision agreement are not certified eigenvalue forward-error enclosures.

## Coverage, execution and provenance

Target all eighteen registered n17 family/eta/node matrices. A declared subset
may be used first as bounded execution/conditioning preflight; never describe
it as complete family coverage. The unchanged n25/n33 and continuum requirements
remain outstanding even if the complete coarse-grid numerical tests pass.

Freeze contract/source and sidecars after AST preflight, before execution.
Use the already installed mpmath/NumPy/OpenBLAS and at most16 bounded spawn
workers, with one local BLAS thread per spectrum call. No package installation,
host environment/provider/model change or paid dispatch. Parent-only fresh case
receipts, immutable resume and full fresh read-only replay. Store the shear,
transformed quadratic form, complete spectra, input hashes and actual failures.
Keep runtime progress private/ignored; identify actual live handles when waiting.

Preserve all earlier sources, results, failures, hashes and sidecars. New results
need an owning report, external metadata guards and append-only continuity notes.
Rule9 DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED. Nonlinear interactions, physical space/
normalization, refinement/continuum admission, healthy GR and both identifying
matching inputs remain substantive. No state adoption/evolution, new parent,
vault mutation, manuscript/site changes, publication, commit or push.
