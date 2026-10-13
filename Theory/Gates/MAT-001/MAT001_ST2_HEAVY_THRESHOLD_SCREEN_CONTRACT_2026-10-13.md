# MAT-001 ST2: can a calculable heavy threshold select the source normalization?

13 October 2026. Result `MAT001-ST2-v1`; separate **Conditional** control.
Operator scope: proceed with the next identifying diagnostic after ST1.
Freeze before execution. No canonical parent replacement or R5-P1 revival.

## Declared action, state and approximation

Signature (-+++), c=hbar=1. Retain independent Jordan metric g_J, separate
sigma>0, complex condensate Phi and one new real heavy scalar H. H is not
the condensate amplitude, a measured baryon, or an identified ITSM degree of
freedom. In a chosen reference renormalization scheme/scale:

```text
S_J = integral sqrt(-g_J) [xi(mu) sigma^2 R_J/2
      -zeta(mu) (grad_J sigma)^2/2 -lambda(mu) sigma^4/4
      -(grad_J H)^2/2 -(g sigma^2+eta R_J) H^2/2]
      +S_Phi[Phi,g_bar]+S_probe[sigma,g_J]+S_counterterms+S_boundary
g_bar=(sigma/sigma0)^2 g_J
S_Phi = integral sqrt(-g_bar) [-grad Phi* . grad Phi-V_Phi(2 Phi*Phi)]
V_Phi(s)=m_c^2 s/2+lambda4 s^2/8+lambda6 s^3/(24 Lambda^2)
S_probe=-sum_a integral m_a0 (sigma/sigma0)^p ds_J.
```

The reference condensate embedding g_bar is fixed, not redefined to depend
on loop-generated F. It agrees with the ST1 reference metric at tree level
after choosing the reference gravitational scale. Its action and finite
U(1) charge remain retained, with lambda6>0, lambda4>=0, Lambda>0 and
mu_c^2>m_c^2. It generally is NOT a sigma-independent spectator in the final
loop-corrected Einstein chart. The full finite-density response is not solved.

Quantize H only around H=0. sigma, the metric, condensate and probes are
external unquantized backgrounds in this determinant calculation. g>0 is a
dimensionless heavy portal, eta a real curvature coupling; xi>0 and
B_tree=6+zeta/xi>0. The locally heavy mass squared is X=g sigma^2>0.
Use Euclidean vacuum continuation and minimal-subtraction finite constants
specified in the derivation. Compute bulk local coefficients on a smooth
boundaryless Euclidean compact control (or interior local patches). The
Lorentzian ITSM I x T3 boundary/state completion is not computed. Bulk F K
boundary data must be transformed with F when used; new quantum surface
counterterms and finite-volume/Casimir pieces are outside this bulk screen.

The two-derivative local expansion requires external momenta and curvature
small compared with X, slow sigma variation, and heavy correlation length
short relative to torus sizes. No physical cutoff, torus size or observed
hierarchy is supplied. Retain potential and curvature renormalization along
with kinetic terms. Do not discard induced sigma potential to keep a pole
massless. Required counterterm classes include sigma^4, sigma^2 R, and
curvature-squared invariants; zeta is an independently allowed kinetic input
even if this particular one-loop determinant has no bulk kinetic UV pole.

## Registered derivation and rejection tests

1. Use D=-nabla_E^2+X+eta R, E=-(X+eta R). Substitute into a4 to derive the
   bulk potential/curvature pole structures and distinguish total derivatives
   from kinetic UV divergences. Derive renormalized U and F with explicit
   Euclidean/Lorentzian gravity sign accounting.
2. Independently derive the finite kinetic threshold from the quadratic
   Tr log expansion and the momentum bubble, including real-field factors.
   Check its Feynman-parameter derivative and convergent radial momentum
   integral using rational symbolic controls and 80-decimal arithmetic.
3. Transform the resulting two-derivative F,Z theory to its Einstein chart.
   Derive the signed fractional probe-mass vertex, full metric-scalar kinetic
   coefficient and strict one-loop expansion. The exact algebra of a displayed
   truncated action is not an all-orders quantum prediction or an on-shell pole.
4. Check p=0 and p=1, eta=1/6 and nonconformal eta independently. Do not reuse
   the ST1 p=1 cancellation when a running F changes the mass/frame factor.
   Do not interpret a quantum correction near the excluded B_tree=0 Weyl
   boundary as a newly physical gauge mode without complete Ward/anomaly work.
5. Construct three positive-kinetic off-shell coefficient controls with the
   same heavy determinant and reference gravity/condensate inputs but different
   independent zeta. Distinguish physical parameter freedom from a change of
   renormalization scheme holding the full effective action fixed.
6. Derive heavy-only scale cancellation and integration-constant freedom:
   RG running is not selection of renormalized boundary values. Setting bare
   coefficients to zero is an extra UV matching condition, not a consequence
   of a finite threshold or compact geometry.
7. Inspect the Einstein potential for the conformal-heavy eta=1/6 subclass.
   Test constant-sigma vacuum stationarity rather than assuming a gapless
   scalar. This does not rule out a finite-density/reservoir balance or a
   different multi-field completion.
8. Check dimensions, source orientation, perturbative domain, omitted mixing,
   wrong curvature sign, real-field factors, absent counterterms and illicit
   gate promotion. Freeze receipts with source pins and retain failed runs.

All numerical cases are target-free arithmetic controls, not observationally
admissible ITSM backgrounds. No observed G, Cassini, a0 or galactic response
selects an input. No Y^(3/2), preferred-frame/reservoir completion, physical
GR/PPN response or canonical K_Q is supplied by this Lorentz-invariant block.

## Authority and review

Inherit ST1 contract/report, the route decision, MAT R4 signed residue and R5
microscopic identifiability decision, and Core Identity/architecture. Relevant
Rule-9 debt is DEFERRED, not cleared. Method sources: Vassilevich, Phys. Rept.
388 (2003) 279, https://arxiv.org/abs/hep-th/0306138, equations 2.2, 2.31-32,
3.6 and 4.27-28; Jarv et al., PRD91 024041, https://arxiv.org/abs/1411.1947,
frame-invariant scalar normalization. The loop calculation is this declared
candidate, not a claim that those papers determine an ITSM coupling.

PROCEED_PROVISIONALLY for this bulk threshold/identifiability diagnostic.
Canonical Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged;
physics_pass=false; gate_effect=NONE; Rule9_cleared=false.
No memory mutation, paid/provider dispatch, commit, push or publication.
