# MAT-001 ST1: induced gravitational scale and the matter source

13 October 2026. Candidate/result ID `MAT001-ST1-v1`.
Status: **separate Conditional scalar-tensor matching control**.
Authority: operator instruction to proceed after the RM1 source/pole screen.
Freeze this contract before the executable. No R4C1 replacement, canonical
parent adoption or advancement of the rejected R5-P1 instantiation is included.

## Question

Can a separate scalar's nonminimal curvature coupling tie its matter source
and kinetic normalization to a gravitational scale, while retaining a physical
soft scalar and enough information to identify its normalized coupling?
Compare fixed Jordan masses, masses scaling with the scalar, and the local
Weyl-degenerate kinetic relation. Do not assume those are the same theory.

## Fully declared control action and fields

Use signature `(-+++)`, `c=hbar=1`, spacetime `I x T3`, periodic spatial
variations and Dirichlet endpoint metric/scalar data or compactly supported
interior variations. Independent Jordan variables are `g_J`, a separate real
scalar `sigma>0`, and complex condensate `Phi`. Constants `M_P,xi,sigma0>0`
satisfy the reference-chart relation `xi sigma0^2=M_P^2`; it defines the
background normalization, not a determination of a measured Newton constant.
The dimensionless scalar kinetic coefficient `zeta` is initially real.

```text
F(sigma)=xi sigma^2
g_E=(F/M_P^2) g_J                      (derived metric, not an extra field)
S_control = integral sqrt(-g_J) [F R_J/2 - zeta (grad_J sigma)^2/2]
            + S_Phi[Phi,g_E] + S_probe[sigma,g_J] + S_boundary
S_Phi = integral sqrt(-g_E) [-grad_E Phi* . grad_E Phi - V_Phi(s)]
s=2 Phi*Phi
V_Phi(s)=m_c^2 s/2 +lambda4 s^2/8 +lambda6 s^3/(24 Lambda^2)
S_probe=-sum_a integral m_a0 (sigma/sigma0)^p ds_J
S_boundary=integral_boundary sqrt(|gamma_J|) epsilon_boundary F K_J.
```

Here `epsilon_boundary=normal^2`; preserve the conformal surface term and
boundary transformation together. For this screen the separate sigma
potential is exactly zero, not an unspecified function. The allowed global
scale-invariant quartic alternative would transform into a constant Einstein
potential, and is only an algebraic control, not a stabilization calculation.

The matter mass exponent p is universal within each probe model and chosen
explicitly. Two distinct models are registered: `p=0` (fixed Jordan masses),
`p=1` (Jordan masses proportional to sigma). Neither choice is deduced from
ITSM or from the condensate action. Other p values are symbolic controls only.
At p=1, `m_a0/sigma0` is a dimensionless mass coupling.

The finite-density condensate is retained, not replaced by sigma. Its action
is deliberately minimal to the derived Einstein metric; this is a stated
choice which makes it independent of sigma after the variable change. Take
`Phi=rho exp(i Theta)/sqrt2`, `Theta=mu t_E`, a nonzero rho branch, and an
independently specified positive U(1) charge/state. Use the UVIR-001 branch
domain `lambda6>0`, `lambda4>=0`, `Lambda>0`, `mu^2>m_c^2`. Its known negative
spatial cubic-law result is retained. Finite-density curved background,
metric/frame/reservoir interactions and their force matching are not solved.
No independent U field, reservoir action, or Y^(3/2) operator is supplied by
this control; it cannot pass the full ITSM identity/gate checklist.

Use `tau=ln(sigma/sigma0)` as the separate force-field chart, anchored toward
increasing sigma. Derive the Einstein scalar kinetic coefficient before
canonical normalization. Admit only its strictly positive finite interior
for a propagating scalar. Treat zero or negative kinetic coefficient separately.
The nonzero-source response is a covariant linear scalar response on a
constant-sigma Einstein/condensate background; its flat vacuum Fourier limit
is a local methods control, not a flat solution with nonzero condensate stress.
No global static torus zero-mode inverse is permitted; sources for static
torus response must be compensated.

Mass dimensions: `[sigma]=[sigma0]=[M_P]=[m_a0]=[rho]=[Lambda]=[m_c]=1`,
`[F]=2`, `[tau]=[p]=[xi]=[zeta]=[lambda4]=[lambda6]=0`,
`[rho_b]=[T]=4`. A canonical scalar has dimension one; a normalized
fractional matter-mass coupling must have dimension minus one.

## Required derivation and decision checks

1. Conformally transform the bulk F R term and scalar kinetic term. Retain
   the metric-scalar mixing contribution and account for the boundary term.
   Derive the Einstein-frame mass from both the original worldline action
   and the resulting effective matter metric.
2. Normalize the separate scalar, derive its signed fractional mass coupling
   and source sign, and derive the scalar source response in the local flat
   quadratic limit. Keep the vertex distinct from its squared exchange pole.
3. Independently eliminate the linearized Jordan curvature using the metric
   trace and scalar equation. Compare with the Einstein scalar source equation
   in the reference chart. This is a linearized cross-check, not a full ADM or
   finite-density coupled constraint computation.
4. Test the `p=0` and `p=1` mass assignments independently. For the Weyl
   kinetic relation, inspect the unnormalized action/equation rather than
   dividing by zero or extrapolating a canonical source formula.
5. Display the residual dimensionless coefficient ratio. Construct at least
   three admissible coefficient sets with identical reference gravitational
   coefficient and condensate/background inputs but differing matter residue.
   Verify that the field-chart redundancy does not remove that physical ratio.
6. Check dimensions, a conditional bound if the Jordan kinetic coefficient
   is restricted to be nonnegative, and the distinction between the Einstein
   gravitational coefficient and a measured Newton response. Use rational
   parameter diagnostics and negative controls against lost metric mixing,
   wrong source sign, omitted mass scaling, wrong Weyl sign, singular canonical
   normalization, and premature numerical ITSM promotion.

Success at the source test means only that a parameterized static source
exists within the declared control. Numerical identification requires a
relation or independent data selecting all remaining physical ratios. If
symmetry removes the source or the physical scalar, record that outcome and
do not call it a nonzero matching result. This contract does not claim that
all scale-based completions fail.

## Authority, references and holds

Use the exact route-decision/RM1 source boundaries and signed R4 contract.
The rejected R5-P1 and RG1 numerical claims supply no matching input.
Source versions used:

- Route decision SHA
  `00e784bc797600fd4e8c31192026f5c2c7977b66d39f4b5faeddce71ef46b4ac`.
- RM1 report SHA
  `eb1d0d47e137a115451c6908d259bdb1fae61153c8ce217f68c285232c7512ef`.
- Core architecture SHA
  `332489b09476a4403e8bbebe81b3ff329a114005daa1cf39e8b4738f95b9ac8a`.
- R4 signed-source contract SHA
  `63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386`.
- RG1 route comparison SHA
  `c2c97125b7c144cfd4649243bcc3e08f7e3e6d7c1e1de8ecdab00a380695ed5b`.

Primary methodological checks: [Jarv, Kuusk, Saal and Vilson, PRD 91,
024041 (2015)](https://arxiv.org/abs/1411.1947), scalar-tensor frame invariants;
[Sotiriou and Faraoni, RMP 82, 451 (2010)](https://arxiv.org/abs/0805.1726),
degenerate Brans-Dicke scalar discussion. Only the relevant transformation
and degeneracy sections are used; no external paper supplies ITSM matching.

Review DEFERRED, not cleared. Inherit route/RM1 and R4/R5 authority dependencies
for the actual inputs used. `PROCEED_PROVISIONALLY` for this diagnostic only.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `V=NOT_COMPUTED`,
`K_Q=NOT_DERIVED`, `Stage4A=CLOSED`, Tests 1-3 `HOLD_SUBSTANTIVE`.
