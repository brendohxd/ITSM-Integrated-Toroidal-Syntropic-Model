# The first additional alignment condition is not dynamically closed

30 October 2026. Result ID: R9-MT1-ALIGNED-PRESERVATION-V1.
Owner: domain-first goal M2-M3. Conditional; review DEFERRED.
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding

The seven-row linear candidate consisting of vanishing dust-normal frame displacement, vanishing frame velocity, and the first longitudinal alignment compatibility equation is NOT invariant under the actual time-dependent old-B1 coupled dynamics.

This is stronger than repeating the previous unrestricted-alignment test. There are explicit seeds satisfying all seven candidate conditions and the reconstructed linear action constraints, with zero initial frame acceleration, whose next time derivative leaves the candidate.

It rejects this finite restriction prescription. It does not prove that every more constrained aligned sector fails, establish nonlinear admission of a seed, classify every slicing/family, or reject unchanged R4C1/ITSM as a whole.

## Actual moving-domain test

Use the old admitted homogeneous B1 solution, a>0, real nonzero comoving k along z, its original coefficients and the full twenty-state reduced linear system x_dot=G(t,k)x. This is not the eta=1/4 vortical preparation.

Let the first six rows of R select (f_x,f_y,f_z,f_x_dot,f_y_dot,f_z_dot). The seventh row is the longitudinal frame acceleration row with terms proportional to those six selectors subtracted. This row convention recovers exactly the previous C_align equation and defines the same candidate kernel.

The necessary preservation test is

    R*x=0  =>  (R_dot+R*G)*x=0.

R_dot is derived from the actual homogeneous background flow, including the scale factor, Hubble drift, all scalar accelerations and physical amplitude normalization. It is not set to zero. No powers of a frozen generator replace this derivative.

At the registered initial event, the sigma_dot pivot in the seventh row is nonzero for every real k != 0. R has rank seven and its explicitly constructed kernel has dimension thirteen. The first six rows of (R_dot+R*G) annihilate that kernel; the seventh does not. Ten of the thirteen explicit kernel basis columns furnish counterexamples. The exported moving-row defect and kernel allow direct reproduction without a mode deletion.

## Simple exact witness

At the initial event take only

    delta u = epsilon*cos(k*z),

with all other reduced field displacements and all reduced velocities zero. Here epsilon is an infinitesimal amplitude, not the dust multiplier. u is the Cartesian condensate amplitude direction at background (u,v)=(1,0).

This seed satisfies the seven-row candidate. In particular the previous C_align row contains u_dot*delta u and u_dot=0 at this initial event, so it does not reject this seed. The initial frame displacement, velocity and acceleration all vanish.

The original linear reconstruction gives

    delta Z=Sx=Sy=Sz=delta N=0,
    delta rho=delta epsilon_dust=-(2341/1680)*epsilon*cos(k*z).

The actual moving-row derivative is

    d/dt (R*x)_7 = (11674951/9009000)*i*k*epsilon

in the complex Fourier convention. Since the selector equations and initial frame acceleration vanish, it is the longitudinal frame third time derivative at this event:

    f_z''' = -(11674951/9009000)*k*epsilon*sin(k*z).

This is a nonzero exact coefficient for every real k != 0, in the registered control units. It is a derivative in the LINEAR coupled solution, not a finite-time nonlinear error estimate, measured growth rate, physical cutoff or SI prediction. With [delta u]=1 and [k]=1, the displayed numerical coefficient represents a dimension-one control-unit coefficient, giving [f_z''']=3. No independent physical scale has been fixed.

Both seed and response have zero spatial mean at linear order. Small linear perturbations of the strictly positive background dust can retain positive reconstructed linear density. Finite-amplitude nonlinear initial-data completion and charge/harmonic preservation are not supplied by this calculation.

## Verification and preservation

- [Frozen contract](RES001_R4C1_ALIGNED_PRESERVATION_V1_CONTRACT_2026-10-30.md).
- [Versioned executable](../../../Analysis/MasterTests/test_01_r4c1_aligned_preservation_v1.py).
- [Scientific receipt](../../../Analysis/MasterTests/outputs/r4c1_aligned_preservation_v1_attempt_01/summary.json): 60/60, no failed/unknown checks.
- Receipt SHA256: 0a81d8e66531d55af1e0b024a3c345419a974cc33b56e894d626f4a2fe58a9ea.
- Full recomputing read-only replay is byte-identical, exit zero.
- Twenty-seven pinned sources and their sidecars retain bytes and modification times through calculation/replay.
- The earlier input-only receipt is separately labelled NOT_RUN/NOT_EVALUATED; it is not the scientific result.
- The parent generator and alignment compatibility row are recovered exactly. Each counterexample satisfies R*x=0 and zero initial frame acceleration before its moving-row defect is evaluated.
- Original shifts/Z, lapse/density and epsilon conversion remain available; no new projection is applied to evolution.
- Independent numerical differentiation along the actual background tangent at k=1,7,40 agrees with the moving-row assembly. With steps 1e-14 and 1e-22, maximum normalized errors are below 1.655e-27 and 1.655e-43 respectively. These controls are not rigorous evolved-error bounds.
- The exact drift partition is checked. Omitting R_dot changes the test; replacing the problem by a frozen-generator hierarchy would be incorrect.
- Fourier reality is checked for R and its moving defect. The real sine response above follows from the declared parent cosine/sine convention.
- The fifteen older excluded local files were independently rechecked against the existing private preservation inventory; all retained their hashes.
- Same-author symbolic/control/replay checks are not external peer review.

The operator had confirmed High and had not reported a setting change. A pending request to return to Medium did not revoke that confirmation. The earlier unnecessary extra execution stop was corrected without changing the model, reasoning setting or runtime. The frozen scientific contract and inputs were not rewritten.

## Direction and limits

Do not automatically add another row and continue an indefinite initial-derivative hierarchy. The bounded contract now reaches its prescribed domain/action assessment point. A nontrivial narrower sector would need an actual invariant constraint structure or a justified physical prescription, while retaining the intended matter/force response.

See the [domain/action decision packet](../../Core/ITSM_DOMAIN_ACTION_DECISION_V1_2026-10-30.md) for concrete continuations and missing inputs. No alternative is adopted here. The vortical preparation's separate principal, Frobenius, cusp-tail and weak-interface results remain unchanged; this calculation neither admits nor excludes every weak solution.

G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physical-domain admission, physical window and identifying matching remain open. MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED. Review DEFERRED; no new action, physical branch exclusion, cutoff, vault mutation, publication, commit/push or provider dispatch.

