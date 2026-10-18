# R4C1 initial constraint surface: certified construction, evolution still open

18 October 2026. Unchanged-action Stage 2. Original local checks 217/217 PASS;
nine interval certificates. A separately instrumented fresh full read-only replay is exact (exit zero).
The earlier CLI replay failure described below remains preserved.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding and precise scope

For every registered family at eta=1/4,1/64,1/1024, the KNOWN canonical
initial constraints and both global charges admit the implicit construction
below, with strictly positive future dust, throughout |e|<=1/500. This is an
initial-only, planar/reference-slice result, not a theorem for arbitrary data.

The mean expansion has a unique root in the predeclared bracket
[49 H_bg/50,51 H_bg/50]. Pointwise lapse-derived density is bounded below
by 0.1683 in the reference units, versus the background value 0.2. Its
construction retains the local lapse flux, exact shift inverse, both charges,
regulator data and finite-regularity exclusions.

Full initial-data admission remains OPEN: higher/rank-changing Dirac
consistency, persistence and the temporal Cauchy problem are not proved.
No family receives physical GO; a physical Hessian/domain/window and healthy
GR remain unestablished. No candidate is automatically adopted or evolved.

The [contract](RES001_R4C1_INITIAL_ADMISSION_V1_CONTRACT_2026-10-18.md) defines
this distinction. This follows the [exact initial system](RES001_R4C1_INITIAL_CONSTRAINT_V1_REPORT_2026-10-18.md);
its completed 222-check audit is inherited, not rerun or counted as new closure.

## 1. Candidate is defined by equations, not a fit

Use the same flat initial slice a=N=C=1, homogeneous scalar positions,
u=r=Rc=sqrt(eta), v_cond=psi=T=0, u_dot=0, r_dot=sqrt(eta)/4,
p=psi_dot=eta/5, and rho0=1/5. H_bg is the controlled background expansion
from the original action/initial recipe, not an observed Hubble parameter.

The frame is w=e cos(theta), theta=kz, k=40, with coordinate
V=(0,w,0), V_dot=(0,-H_bg w,0). For each amplitude:

1. The previous transverse first integral fixes the zero-mean Sy primitive.
2. For a proposed uniform H, define R=Sz as the UNIQUE solution of the
   previous coercive longitudinal operator in its odd pi-periodic sector.
3. The phase velocity is D=d/(1-zeta Rc^2 e^2/2), retaining Q=Rc*d.
4. The unique mean root fixes H through F(H,e)=<E_rest>+rho0=0.
5. Define epsilon(z)=-E_rest-partial_z(gamma pVz) pointwise.
   The proved lower bound selects the positive future-dust branch.

The global dust charge is then <epsilon>=rho0 by the mean equation and
periodicity. Only the integrated flux vanishes; it is retained locally in
the density and every positivity enclosure. The local angular factor
1-zeta Rc^2 e^2 also remains strictly positive.

This is a certified IMPLICIT construction: the exact inverse and unique root
define the fields, while the polynomial approximation below has a controlled
remainder. No observational target, new action, extra fitted coefficient or
unconstrained parameter substitution fixes the root.

## 2. Regulator data come from the action

Keep the exact reference quadratic regulator coefficients as a declared
higher-order continuation choice,

    Z(z)=Zc e^2 cos^2(theta),  Z_dot(z)=Zdc e^2 cos^2(theta).

The original background and first-wave equations give

    p_dot_bg=-3 H_bg p-beta rho0/K_Q,
    rho_dot_bg=(-3 H_bg+beta p)rho0,
    w_ddot_bg=-(cV^2 k^2+m_frame^2),
    Zc=H_bg p+beta rho0/K_Q,
    Zdc=H_dot_bg p+H_bg p_dot_bg+beta rho_dot_bg/K_Q-w_ddot_bg p.

Here cV^2 and m_frame^2 are the original unspecialized action-derived
expressions, with all family maps retained. In particular wave acceleration
and background drift are not dropped from Zdc. These formulas are derived
before comparing with the archived coefficients; they are not fit to them.

This regulator continuation is not unique. Its compatibility with additional
higher consistency/evolution requirements has NOT been proved. The receipt
does not reinterpret the archived quadratic experiment as an exact evolved
finite-amplitude solution.

## 3. Shift approximation and explicit remainder

Set alpha=e^2, x=cos^2(theta), B=cos(theta)sin(theta), and use

    R_N=B sum_{n=1}^3 alpha^n p_n(x).

For R=B p(x), exact differentiation gives

    R_theta=(2x-1)p-2x(1-x)p_x = Q[p],
    R_thetatheta/B=4x(1-x)p_xx+6(1-2x)p_x-4p = J[p].

Polynomial inversion of the constant leading operator fixes p1,p2,p3.
The full variable-coefficient residual is retained exactly as

    L R_N-f = B N(alpha,x)/(1+alpha*x).

Its coefficients through alpha^3 vanish exactly; the nonzero residual is
NOT called zero because a series was truncated. For 0<=x<=1 and
0<=alpha<=Emax^2, |B|<=1/2 and the denominator is at least one.
The absolute coefficient sum of N supplies a uniform outward residual bound
r_inf. The exact polynomial pieces and residual are exported in proof.json.

Let C0=MU2*kappa be the positive coercivity bound from the previous report,
Pmin a lower bound on P, and Wmax an upper bound on |W|. On the half-cell
of length L=pi/(2k)<2/k, the error satisfies

    ||delta R'||_2 <= sqrt(L) r_inf/(2k C0),
    |delta R| <= L r_inf/(2k C0).

For J_err=P delta R', its weighted mean is zero because the error vanishes
at both endpoints. Thus J_err has a zero, and integration of its equation gives

    |delta R'| <= L (Wmax |delta R|_max+r_inf)/Pmin.

The source is affine in H and the operator independent of H. The same proof
bounds the H derivative using the differentiated exact residual. Therefore
the root-derivative calculation includes inverse sensitivity, not a frozen R.

Across all nine cases, the conservative uniform bounds include

    |R-R_N| < 7.57e-21,
    |R'-R_N'| < 6.06e-19.

These bound the exact inverse, not a continuously projected evolution.
They are reference initial-data estimates, not physical EFT cutoffs.

## 4. Outward interval root and positivity certificates

All proof enclosures use the existing mpmath.iv implementation at 80 decimal
digits. Endpoint inspection uses 110 digits; exact binary endpoints are
retained so decimal display rounding is not the basis of a strict inequality.
The rational printer is checked against exact integer fractions. No ordinary
high-precision point calculation is substituted for an interval enclosure.

Reflection and amplitude-sign symmetries of the energy/flux are checked
symbolically before reducing averages to a quadrant. Interval boxes cover
that entire quadrant, the full H bracket, all 0<=e^2<=(1/500)^2 and both
physical amplitude signs. Shift approximation errors are included in R,R'
and their H derivatives before energy/flux evaluation.

Each case satisfies, uniformly over the amplitude range,

    F(49 H_bg/50,e)>0,
    F(51 H_bg/50,e)<0,
    dF/dH=<E_H+E_R R_H+E_q R'_H><0,
    epsilon(z)>0.

Continuity gives a root and the strict total derivative gives uniqueness.
The first registered partition, 16 angular interval boxes, succeeds in all
nine cases; no bracket widening, action change or post-result tolerance
adjustment is used. The frozen refinement sequence is therefore unused.

Conservative floors for the certified density over ALL H in the bracket,
not merely at the root, are:

| Family | eta | Density lower floor |
|---|---:|---:|
| Archived G3 | 1/4 | 0.16830084 |
| Archived G3 | 1/64 | 0.19075292 |
| Archived G3 | 1/1024 | 0.19199721 |
| B1-frame | 1/4 | 0.17029676 |
| B1-frame | 1/64 | 0.19078288 |
| B1-frame | 1/1024 | 0.19199879 |
| Hierarchical | 1/4 | 0.17035720 |
| Hierarchical | 1/64 | 0.19078308 |
| Hierarchical | 1/1024 | 0.19199879 |

Every floor is rounded downward from its stored interval endpoint. Across
the cases, the lower-end mean margin exceeds 0.00799, the upper-end mean
value is below -0.00815, and the total mean derivative is below -1.5256.
These are diagnostic reference-unit bounds, not cosmological measurements.

The certificates are conditional on the pinned equations, declared parity/
free-data choices and correctness of the interval-arithmetic implementation.
They are not a formal verification of that library or independent peer review.

## 5. Nodes and continuity with the archived preparation

Odd pi-periodicity gives R=0 at every leading profile node. The initial
force field and p are homogeneous, N=1 and div V=0. The inherited unreduced
node constraint and its first transport reduce there to Z=0 and Z_dot=0;
both selected regulator profiles have the required cos^2 factor.

With COMPLETE forward momenta, the regular-side inverse numerators obey

    F_psi=-w^2 p,  F_Z=-b w^2 Z_hat.

Their values and first normal derivatives vanish at a simple node. No division
through w=0, omitted cusp momentum or invented ordinary third cusp derivative
is used. At e=0 the original homogeneous aligned control applies; no regular
inverse through the globally aligned stratum is asserted.

These are only the known initial and first-transport compatibility conditions.
Higher/hidden constraints and acceleration-level consistency through the
rank-changing surface remain OPEN.

At zero amplitude, F_H=-6 M H_bg is nonzero. The coercive inverse depends
smoothly on alpha,H in this fixed sector; its periodic derivative has zero
mean. Together with the C2 cusp this justifies the quadratic mean coefficient
and the separate |e|^3 term, without an ordinary third derivative at e=0.
The exact quadratic mean coefficient and phase counter agree with all 18
archived initial preparations. The necessary cubic cusp mean counter is
retained from the original calculation, with H3=x_dot3/3.
The regulator field AND velocity coefficients also match all 18 runs.

| New lower-order bridge | Largest normalized discrepancy |
|---|---:|
| Phase counter | 7.683073229291716e-20 |
| Volume counter | 2.705136721166174e-16 |
| Regulator field | 6.409855338667157e-18 |
| Regulator velocity | 3.315072089565093e-16 |

The inherited tolerance is 1e-10. Signed charge diagnostics retain
+/-1/500,+/-1/1000,+/-1/2000. All families/methods remain; no original floating
residue is overwritten or called exact. The previous longitudinal-shift bridge
is inherited from the pinned INITIAL-CONSTRAINT-V1 receipt, not rerun here.
Existing cubic timing warnings, negative-energy/defective-mode findings and
all earlier failed proof constructions are unchanged.

## Preserved replay failure and independent instrumentation

The first CLI replay stopped at the combined byte/metadata guard on proof.json.
Its recomputed proof was not saved, so the error does NOT establish which
condition failed. The [frozen hold note](RES001_R4C1_INITIAL_ADMISSION_V1_REPLAY_HOLD_2026-10-18.md)
preserves that failure without attributing it to serialization, physics or
external interference.

A second fresh, unchanged-V1 execution completed 217/217; all four JSON
payloads match the original byte-for-byte. The subsequent
[strict auditor](RES001_R4C1_INITIAL_ADMISSION_REPLAY_AUDIT_V1_CONTRACT_2026-10-18.md)
separates each file's recomputed-byte equality from its original-byte and
metadata preservation. Its full fresh run passes every strict comparison on
all eight files. The candidate is retained in a separate new directory.

The earlier CLI failure's cause remains NOT_ESTABLISHED_BY_THIS_AUDIT. It has
not been relabelled, its source/serializer/tolerances were not repaired, and
this report does not claim the CLI can never fail intermittently. The audited
replay proves the stated new run; its successful outcome is not a diagnosis
of the historical failure.

## 6. Verification and open physical requirements

Original run: 217/217 local checks, nine certified cases, exit zero.
Complete fresh replay through the separately frozen auditor passes exit zero:
all four recomputed JSON payloads and four sidecars match exactly, and all
eight original bytes/sizes/mtimes are unchanged. It calls the unchanged V1
calculate function without monkeypatches. The auditor's four source pins and
eight source/sidecar metadata records are separately preserved.

Nineteen source pins and 38 source/sidecar metadata records are unchanged.
A separate delivery check uses exact rational reconstructions of the stored
binary endpoints to recheck strict signs and density floors. It checks
integrity/signs only; it does not replace the complete computational replay.

The certified result is the known canonical initial-constraint surface on
this declared slice. Full initial-data admission and Stage 2 remain OPEN.
Next test higher/rank-changing Dirac and acceleration consistency and
persistence, then the physical reduced Hessian, temporal Cauchy/energy domain,
nonlinear evolution error, physical frequency/momentum window and healthy GR.
A numerical acceleration coefficient still needs genuinely identifying
matter-residue AND nonlinear-force matching inputs, which remain absent.

R9-MT1-INITIAL-ADMISSION-V1 is DEFERRED, not cleared. Inherit initial-constraint,
node, canonical, preparation, generic-family and transitive review debt.
Provisional reuse is limited to these stated construction/bounds.

Stage1 original linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.

No state adoption or evolution, vault mutation, manuscript/PDF/site edit,
commit/push, publication/submission, action/parent choice, provider dispatch
or model/runtime reconfiguration is included.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| Contract | 88b0ddb963912de6ddca377108361bcb9a584686826a6934bdc598adb6b0a7a2 |
| Executable | d994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a |
| summary.json | 993b5cfffcb4b7c4106656a6929dfcc0379858c53e6556f60bb5b56b24ec5f4c |
| proof.json | b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b |
| certificates.json | 7c3465014fd85d7a98b905eed721c907f2f7764ccefadf856680ecf068d7127a |
| archive_controls.json | 9267bb9360495eb103f44940e9b4d5120d862ac6ab585eca902ed170fef31673 |
| Preserved CLI hold | 47b347c15fa72f0da7bb860fdd89bf82dd2b7574c5872fb036ece9d7aa594628 |
| Audit contract | 83e1d2c3152825dca5ceb1e597c624b98807ff59b71b95f73db0ac95a9e738c1 |
| Auditor source | 1dd930c4b239a185d1402c0fa3be2eada8df46aa838b472074c9cc87e5a6baad |
| audit.json | 9351821690ca15a3fe58b59b0b932090a229ecbc84c30bc700b2b36c39df3491 |

Executable: Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01.

    python -B Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py --replay Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01

Audited replay evidence: Analysis/MasterTests/outputs/r4c1_initial_admission_replay_audit_attempt_01/audit.json.
The strict auditor accepts --output with a NEW nonexistent audit directory;
it recomputes the original calculation and never writes to the original.

New computations require new nonexistent output directories. Preserve all
original sources, receipts, failed attempts and hashes. Only mutable research/
review indexes receive guarded appends and refreshed index digests.

