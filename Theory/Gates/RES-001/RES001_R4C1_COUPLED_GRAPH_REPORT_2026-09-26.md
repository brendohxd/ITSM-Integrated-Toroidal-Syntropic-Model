# R4C1-S4A: full scalar graph estimate disposition

Date: 2026-09-26. Master Test 1; conditional R4C1-v1/B1.
Validation: 99/99 checks, including provenance and rejection controls.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Owning [contract](RES001_R4C1_COUPLED_GRAPH_CONTRACT_2026-09-26.md).

## Decision

The registered S3 graph norm extends to a positive full-rank metric on all
twelve scalar initial-data components in the regular B1 chart. However, its
instantaneous logarithmic growth rate cannot have a wave-number-independent
upper bound: exact density/velocity data give a rate asymptotic to p/2.

Thus the direct differential energy estimate in this fixed norm fails.
This does NOT prove that the full solution operator has unbounded growth at
fixed time, or exclude a different uniformly equivalent symmetrizer. Full
coupled well-posedness remains open. The S3 frozen two-component result is
preserved; extending it to the entire coupled system requires additional work.

The action, background parameters, graph rows and tolerances were unchanged.
The diagnostic includes all scalar branches, time-dependent reconstruction,
constraints and the complete S2 generator, with W=Vc+Mcdot. There is no
fast-mode elimination or two-dimensional embedding in this calculation.

## Full metric and rank

With Z=(x,xdot), define q=[R,0]Z and qdot=[Rdot,R]Z. The fifteen graph
rows are exactly the S3 reference-unit quantities, now evaluated on all Z:

    delta f, p delta f, delta fdot (f=u,v,r);
    sqrt(K_Q) delta psidot; sqrt(b) delta Delta_psi;
    sqrt(M_U^2 c14) wdot; sqrt(M_U^2 cL) p w;
    D=delta rho_m/rho_m; v_d=p delta tau/C.

Write these rows as FZ and S=F^T F. For rows
(0,2,3,5,6,8,9,10,11,12,13,14), the exact determinant is

\[
 -\frac{\sqrt{66}\,k^4\left(a^2 B+k^2\right)}
 {13068 H^2 a^{24}\rho_m},\qquad
 B=396H^2+18\dot\psi^2+6(\dot u^2+\dot v^2+\dot r^2).
\]

It is nonzero for a>0, H>0, rho_m>0 and k>0 at the fixed B1 parameters;
C is finite and positive and the inherited S1 constraints remain regular.
Therefore S is positive definite for each such finite mode/event. This is
not a k-uniform condition-number bound. H=0, k=0 and rho_m=0 are not covered.
The factor 5H+4*psi_dot in S3's restricted limiting map is not a singular
factor of this full finite-k minor.

The stored matrix artifact exports F, Fdot, its original-variable version,
the selected minor, and the exact witness below. Fixed B1 reference units
remain in use: this diagnostic sum of squares is not a physical Hamiltonian.

## Exact differential obstruction

For A=[[0,I],[-W,-G]], define L=Fdot+FA and E=L^T F+F^T L. Then

\[
 \frac{d}{dt}\|FZ\|^2=Z^T E Z,\qquad
 \mu(t,k)=\tfrac12\lambda_{\max}(E,S).
\]

Consider legitimate full constrained initial data with D=1 and v_d=-1,
and every other graph row zero. In the original q,qdot chart set
delta tau=-C/p and choose delta taudot using the linear D row so that D=1;
all other independent entries vanish. The coefficient allowing this choice is

\[
 \frac{\partial D}{\partial\delta\dot\tau}
   =\frac{a^2 B+k^2}{6Ca^2\rho_m}>0.
\]

The graph norm squared is two; division of the data by sqrt(2) normalizes it.
Its exact instantaneous logarithmic norm rate is

\[
 r(p)=\frac{p-H}{2}-\frac{\dot\psi}{5}
 +\frac{\rho_m\left[9(33H^2-15\dot\psi^2-5\Sigma)
                      -\tfrac{21}{2}p^2\right]}{p(B+p^2)},
 \qquad \Sigma=\dot u^2+\dot v^2+\dot r^2.
\]

At each fixed regular background event, r(p)/p tends exactly to 1/2 and
mu(t,k)>=r(p). Thus no wave-number-independent bound on the instantaneous
norm derivative exists in this fixed metric. Multiplying every mode norm
by the same Sobolev factor (1+|k|^2)^s does not change this ratio.

This is a formal large-wave-number statement about the classical equations;
no physical EFT validity at unlimited p is asserted. A large instantaneous
derivative alone does not prove a fixed-time semigroup obstruction. In
particular, this is not a theorem of ill-posedness in every admissible space.

The witness is an explicitly post-scan analytic strengthening: the initial
94-check calculation exposed the trend, then five exact checks were added.
The original norm/domain/thresholds were retained; the initial successful
artifacts are preserved locally. No failed result or tolerance was hidden.

## Numerical evidence

The four existing S2 endpoint transfers on [0,4] were evaluated in the full
initial/final graph metrics. These are reweighted saved transfers, not new
integrations of the perturbations.

| Torus mode n, k=2*pi*n | Endpoint graph amplification (DOP853) | Normalized DOP853/Radau difference |
|---|---:|---:|
| 1 | 5.4235603176 | 1.76e-11 |
| 2 | 10.5780243744 | 3.32e-13 |
| 4 | 20.9523242437 | 6.72e-14 |
| 8 | 41.7316139173 | 3.36e-14 |

The roughly linear trend over four modes is evidence to investigate, not
an asymptotic fixed-time transfer theorem. All 54 local metric samples are
positive. At p=1608.4954 the sampled mu values range from about 803.91 to
804.18. Maximum raw metric conditioning is 6.3988051e16.

Sixty-decimal arithmetic controls norm evaluation. Cholesky/SVD and a
separate inverse-square-root generalized-eigenvalue calculation agree to
2.49e-56; background and inherited transfer precision remain unchanged.
The centered full energy derivative has relative discrepancy 5.84e-10.
Negative controls detect omitted Rdot, Fdot, Mcdot and two-component reuse.
These are implementation validations, not 99 independent physics criteria.

## Reproduction and continuation

    python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_coupled_graph.py

[Receipt](../../../Analysis/MasterTests/outputs/test_01_r4c1_coupled_graph_summary.json):
SHA-256 cacd1b1bf9970399c89383e5ac6f2bbfe4614fa5cb6ebf04806bb700a0ae16c0.
The receipt pins inputs, executable and matrix/sample artifacts. Upstream
receipts and historical attempts remain unchanged.

R9-MT1-S4A inherits S3/S2/S1/B1/VARIATION; all review remains deferred.
Provisional use: exact reconstruction, rank and the scoped negative result.
The next bounded step is to preregister an estimate with the additional dust
velocity regularity suggested by the continuity equation, and check all
couplings and time derivatives. Any altered space must be declared explicitly;
an equivalent symmetrizer needs a uniform-equivalence proof. Neither approach
is already validated by S4A. Preserve this fixed-metric rejection.

Full IVP, homogeneous/singular sectors, causality, cutoff, healthy GR recovery
and matching remain open. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED.
