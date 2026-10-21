# Two-node graph domain for the full planar two-form; generator admission open

21 October2026. Unchanged R4C1 Stage2; version1. Local320/320 and complete
fresh exact read-only replay. This is a mathematical instantaneous inverse-
domain result, NOT a positive physical energy or a well-posedness theorem.

## Result and meaning

The complete retained planar two-form has a densely defined CLOSED inverse
on an explicit maximal L2 forcing domain, although it has NO bounded inverse
on all unweighted L2. A positive inverse-graph norm is available. This gives
a precise mixed-order route for studying both nodes together without dropping
metric/frame crosses or requiring a uniformly bounded ordinary inverse.

For H2 auxiliary residuals, simultaneous value AND first-derivative conditions
at BOTH quadratic nodes are necessary and sufficient for square-integrable
auxiliary rates. Crucially, these conditions apply to the CROSS-CORRECTED
regulator residual, not to raw r_Z. The raw residual can have a simple zero
and still correspond to a perfectly regular constructed two-form rate.

This does not prove that the actual coupled descriptor enters or preserves
this domain. It does not remove the negative clock-Hamiltonian restriction,
admit a physical state/mode, establish healthy GR or supply a physical cutoff.
The finite-grid auxiliary Schur audit and the earlier negative results remain
unchanged. No new action or background is selected.

## Complete operator, including quotient and mean adjoints

Use normalized coordinate averages on the registered periodic planar section.
Let Hc be the canonical-position Hilbert space, including the three mean
metric coordinates and the already declared phase/dust/translation quotients.
Use its true product inner product, not a pointwise replacement of mean pairs.
The full space is H=Hc_Q x Hc_P x L2_s x L2_Z in fixed reference-chart units.

At h=I,V=(0,w,0),s=p>0,w=e*cos(kz), define

    g=b*w^2; B=p*Dg : Hc_Q -> L2.

The derivative retains canonical metric/frame fields and the mean L=hzz:

    B*a=p*b*[w^2*(a_hxx/2+3*a_hyy/2+a_L/2)+2*w*a_Vy].

B^* includes the translation projection of its Vy field component and the
mean integral of its L component. These are not discarded as small corrections.
For v=(vQ,vP,vs,vZ), the full two-form action is

    Omega*v=(-vP-B^*vZ, vQ, -g*vZ, g*vs+B*vQ).

All signs follow the owning dTheta convention with Theta=<P*dQ-g*s*dZ>+PM*dM.
For r=(rQ,rP,rs,rZ), set a=rP, rztilde=rZ-B*a. The regular a.e. inverse is

    vQ=rP; vZ=-rs/g; vs=rztilde/g;
    vP=-rQ+B^*(rs/g).

The actual dynamic forcing is ALWAYS

    r=K*u=Hessian(Hpsi)*u-dOmega[u]*Xdot_background.

The exact variation identity retains the full background drift. The source
does not replace K by a static or scalar-only Hessian or assert that arbitrary
constructed r is a physically admitted K*u.

## Maximal domain, closedness and positive graph norm

For fixed eta>0 the coefficients g and B are bounded. The two g zeros per
period have measure zero, so g>0 a.e. The maximal inverse domain is EXACTLY

    Yg={r in H : rs/g in L2 and (rZ-B*rP)/g in L2}.

Necessity follows from the two auxiliary rows; sufficiency follows from the
displayed full inverse and boundedness of B^*. This is the range of Omega,
not the whole forcing Hilbert space. No value of a generic quotient is assigned
at a node: elements of L2 are equivalence classes up to measure-zero changes.

Omega is bounded and skew-adjoint with the retained adjoint/projections. Its
kernel is zero: the canonical momentum rows first give vQ=0; the auxiliary
rows then give vZ=vs=0 a.e.; the canonical position rows give vP=0. Hence
range(Omega) is dense because its orthogonal complement is kernel(Omega^*)=0.
Its inverse is closed: if r_n->r and Omega^-1*r_n->v in H, boundedness gives
Omega*v=r, hence r is in Yg and its inverse is v. No surjectivity onto H or
bounded inverse on H is asserted.

Define

    N(r)^2=||r||^2+||rs/g||^2+||rztilde/g||^2,
    G(r)^2=||r||^2+||Omega^-1*r||^2.

The inverse formula and Young's inequality give

    N<=G<=sqrt(max(3,1+2*||B||^2))*N.

For the frozen recipes0<eta<=1,p=eta/5,b=5eta/11,e=1/500,

    ||B||^2 <= (p*b)^2*(11*e^4/4+4*e^2)
             =4000011*eta^4/30250000000000 <1,
    N<=G<=sqrt(3)*N.

Thus N is a complete positive inverse-graph norm. It is NOT derived from a
positive Hamiltonian, is NOT an invariant physical energy normalization, and
does not reverse the scalar-rate negative-curvature result. Its 1/g weights
are unbounded in ordinary forcing L2. This is fully consistent with the
previous localized unweighted-inverse obstruction.

Smooth retained canonical rates together with smooth auxiliary rates are
dense in H; canonical quotient projection preserves smooth density and all
mean pairs remain. Their images under the bounded analytic-coefficient Omega
give a smooth double-trace core dense in Yg in its graph norm. This is a core
for the TWO-FORM inverse, not a core or closure proof for Omega^-1*K.

## Both-node H2 trace criterion and whole-circle estimate

Let r denote EITHER rs or rztilde, and assume r is periodic H2. Its value and
first derivative have traces in one dimension. Since g has a quadratic zero,
a nonzero r(node) makes r/g behave as1/x^2; a nonzero r'(node), after r(node)=0,
makes it behave as1/x. Neither lies in L2. These establish necessity.

For sufficiency, partition the full circle into four half-arcs from a nearest
node to the midpoint between adjacent nodes. Each half-arc has length a=pi/(2k).
With x its distance from the node,0<x<a and

    |sin(kx)|>=2*k*x/pi,
    |g|>=4*abs(b)*e^2*k^2*x^2/pi^2.

For f in H2(0,a) with f(0)=f'(0)=0, integration by parts gives

    integral |f'|^2/x^2 <=2*||f'/x||*||f''||,
    integral |f|^2/x^4 <=(2/3)*||f/x^2||*||f'/x||,
    ||f/x^2|| <=(4/3)*||f''||.

The finite-interval boundary terms are -|f'(a)|^2/a and -|f(a)|^2/(3a^3),
both NONPOSITIVE; no artificial endpoint condition at a is imposed. At the
node, f'(x)=integral_0^x f'' and f(x)=integral_0^x(x-t)f''(t) imply that the
boundary terms tend to zero, using the vanishing local L2 norm of f''. Smooth
approximation/these integral representations extend the estimate to H2.
For complex fields apply the same argument with real parts and absolute values.
Summing the squared bounds over all four half-arcs yields

    ||r/g||_L2 <= pi^2/(3*abs(b)*e^2*k^2)*||r''||_L2.

Therefore, within H2, division into L2 is equivalent to value AND first-derivative
vanishing at BOTH nodes. For real residuals this gives eight real scalar trace
conditions; complex residuals split into real and imaginary parts. The maximal
Yg does not require H2; these are an explicit regular
subdomain characterization, not new C3 smoothness requirements for the action.

The integration-by-parts method is classical Hardy/Rellich reasoning; see
[Evans and Lewis (2007), section2](https://files.ele-math.com/articles/jmi-01-40.pdf).
The specific one-dimensional finite-interval/circle estimate above is derived
here, not imported from that paper's higher-dimensional theorems.

For e=1/500,k=40,b=5eta/11 the bound constant is

    1375*pi^2/(12*eta) < 166375/(147*eta).

The rational ceiling uses the exact positive-integral identity
integral_0^1 x^4*(1-x)^4/(1+x^2) dx=22/7-pi>0. This is a reference-chart
mixed-order estimate, NOT a physical frequency/momentum cutoff. At eta=0 both
g and B vanish and the two auxiliary L2 sectors lie in the kernel; the inverse
does not extend. No uniform healthy-GR conclusion follows.

## Why subtracting the cross term is necessary

Take a constructed canonical frame rate a_Vy=1, all other canonical rates zero,
and vs=vZ=0. It respects the translation tangent section since <sin(theta)>=0.
Then rs=0,rP=a and raw rZ=2*p*b*w. At theta=pi/2 and3pi/2:

    raw rZ=0; raw rZ'=respectively -2*p*b*e*k and+2*p*b*e*k.

The raw residual has a SIMPLE zero, while rztilde=rZ-B*a is identically zero.
Imposing raw rZ'=0 would incorrectly reject this full-two-form method direction.
This is not a newly admitted physical mode; it demonstrates the algebraic
necessity of the cross term. Linearized evolution must use its full K forcing.

Moving/lifted alignment sets change g and its domain. The current result is
instantaneous on the registered base. It does not impose frozen old-node
momentum conditions, prove persistence of either alignment surface, or show
that the physical domain is invariant under time evolution.

## Weak rates, verification and preservation

The residual r=abs(cos(theta))^(7/4) is H2 with the required traces. Its quotient
is proportional to abs(cos(theta))^(-1/4), UNBOUNDED but in L2. Its norm does
not imply a finite classical rate value at a node. Constants or simple-zero
residuals give non-L2 quotients. The weak example prevents silently replacing
the stated L2 domain by a stronger classical-pointwise domain.

Eight smooth Fourier-polynomial controls use r=cos(theta)^2*P(theta). Exact
Laurent/Parseval integrals are compared with independent100-digit quadrature;
dimensionless norm ratios range0.506895--0.734061, below pi^2/3. For the weak
example, beta/gamma integrals agree with quadrature after a square-coordinate
change removes its integrable endpoint singularity. Recorded normalized values:
rate-square1.66925368335 and residual-second-derivative-square2.13003725219.
Quadrature is an independent METHOD CONTROL, not the proof or an interval bound.

All9 family/eta cases,17/25/33 grids and both node offsets give54 original
complete-two-form comparisons. Smooth directions retain every canonical sector,
mean metric rates and both auxiliary rates. Quotients are evaluated only away
from exact nodes; stored node entries are null/NOT_ASSIGNED. Finite nodal
matrices retain null rows: these tests do not assert an injective discrete
inverse or convert one grid node into both simultaneous continuum traces.

| Control | Recorded maximum/range |
| --- | --- |
| Canonical inverse, means and projections |3.827e-102 normalized |
| Regular auxiliary inverse |2.600e-99 normalized |
| B/B^* inner-product discrepancy |2.462e-106 raw |
| Error if the cross were omitted |0.92134--452.227 in reference units |

All320 checks pass, with zero failed/unknown rows. Full fresh8-versus16-worker
read-only replay returns exit0 and READ_ONLY_REPLAY_EXACT, reproducing all three
JSONs and sidecars byte-for-byte. Every54 replay key and its checks were
inspected programmatically. Sources cover124 pins/337 native metadata records;
the separate746-record/39-directory raw-integer preservation guard is exact.
All older successes/failures, hashes and timestamps remain unchanged; historical
timestamp transport limitations are preserved. One unsealed preflight assertion
compared equivalent polynomials in different forms; it was normalized to a
zero-difference check before freezing. Its failed log remains, with no change
to equations, scientific thresholds or a prior frozen artifact.

| Artifact | SHA256 |
| --- | --- |
| Contract |dd0645e4d411e8ced0a208326e72aaca68cd78086f6abecfab9c8768d428d628 |
| Executable |193780d9ef812d919ae40a21a39410648aaee6e54b0b51d0cd818efc9d1e53fc |
| summary.json |d01dcf6489222e65cb94a9e530bec930f8fada5d10d346797dbc8c1955c5272a |
| independent.json |6ddcee256b8a67f8da70a6d827e6d4013097eb859d5bb29a1553cfa016d391bc |
| formulas.json |76a3ec7cb1f8a2851f506320bf948f8e29ec03e929b492934c9c9829ac75b61a |
| Full replay log |37abb2f8e76012518f2d0a3d8dc6fac45ebe45917c8c0e691a3bc2583e71237e |
| Raw post-replay guard log |0e108f3393d5ec1253889b70be602545d3cdb0fafc2c49d74fb83b4a1120e0f5 |

Executable: Analysis/MasterTests/test_01_r4c1_two_node_graph_domain_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_two_node_graph_domain_v1_attempt_01/.
The parent alone writes fresh receipts; replay writes none. Private runtime
logs stay ignored. No speedup or billed-token saving is inferred.

## Next actual physical requirement

For the actual full K, determine the state domain

    D(A)={u in D(K): K*u in Yg}, A=Omega^-1*K,

including the full background drift, nonlocal spatial/global constraints and
mean/charge sectors. Prove whatever mapping, closedness/resolvent, density and
time-domain-invariance estimates are required for evolution. A composition of
closed operators need not be closed; the two-form result does not supply this.
The negative Hamiltonian restriction and physical auxiliary admission remain
binding evidence, not results removed by choosing a graph norm.

Stage1 bounded linear prepared-dust scope only; Stage2 INCOMPLETE; Stage3
NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged.
Full auxiliary hierarchy/persistence, physical modes/characteristics, positive
physical control, interactions/cutoff, healthy GR, arbitrary-direction completion
and both identifying matching inputs remain substantive. The full372 QR
continuation is preserved and unfinished. Rule9 DEFERRED; Rule9_cleared=false;
inherit scalar-energy, Legendre/finite-node/nodal/global-reduction/tangency/
descriptor and transitive review debt. Local verification is not independent
scientific review. physics_pass=false; gate_effect=NONE; root goal ACTIVE.
No state adoption/evolution, new action/parent, vault mutation, manuscript/site/
publication, commit/push, paid dispatch or model/package/global-runtime change.
