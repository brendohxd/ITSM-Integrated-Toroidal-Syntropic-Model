# Test 3: dimensional repair of the historical circulation chain

Date: 2026-09-30. Branch: `recovery/v12-core-architecture`.
Status: `ANALYTIC_DIMENSIONAL_CANDIDATE_ONLY`; `physics_pass=false`,
`canonical_Test3_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`. This is an append-only follow-up, not a revision of
the original manuscripts, their hashes, or any sealed gate report. No observed
`a0`, Hubble posterior, galaxy datum, or desired coefficient enters the check.

## Source and question

The [original-PDF comparison](ITSM_TEST_03_ORIGINAL_PDF_CIRCULATION_CROSSCHECK_2026-09-30.md)
(SHA-256 `d74d80895325137c41fb06d3896039864c460001d24c647d211dbbb235473199`)
pins v7.2 and v11.1.1 and verifies that both display the invalid step
`kappa/(2*pi*ell)=cH0/(2*pi)` after defining `kappa=c^2/H0` and `ell=c/H0`.
The printed ratio is `c/(2*pi)`, a speed. The question here is narrower:
can those **definitions alone** be recombined into an acceleration, and does
that repair determine the physical dimensionless coefficient?

The [R4C1-C1 coefficient report](RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md)
(SHA-256 `c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a`)
supplies an independent action-level check of the latter question for the
current **conditional** R4C1 candidate. It does not make the historical
definitions a term of that action.

## Exact dimensional result

Take `[kappa]=L^2 T^-1`, `[ell]=L`, and seek a monomial
`kappa^p ell^q` with acceleration dimension `L T^-2`. Its exponents must obey

```text
2p + q = 1,   -p = -2  =>  p = 2, q = -3.
```

Thus the unique monomial using **only these two dimensional quantities** is

```text
kappa^2/ell^3 = (c^2/H0)^2/(c/H0)^3 = c H0.
```

This is a dimensionally valid *candidate scale*, unlike the printed
`kappa/ell=c`. It is **not** an algebraic correction that either PDF made or
derived. Moreover `kappa=c ell` by their definitions, so
`kappa^2/ell^3=c^2/ell=cH0`: introducing `kappa` supplies no independent
physical information beyond `c` and the assumed Hubble length. A general
acceleration built this way is `f kappa^2/ell^3=f cH0`, with dimensionless
`f` unconstrained by dimensional analysis. The special assignment
`f=1/(2*pi)` would restore the desired numerical form but **would insert**
the missing coefficient rather than derive it.

Flat `T^3` permits winding integers and periodic lengths. A `2*pi` can
therefore appear in a coordinate or phase convention, but neither the
historical definitions nor the torus topology alone provide the map from
winding/circulation to the matter-frame acceleration or fix its coupling.
That missing dynamics is consequential: R4C1-C1 holds the background,
linearized data and `T^3` periods fixed while changing the physical
`-A Y^(3/2)` coefficient. Its conditional static normalization is
`a_dyn=beta^3/(12*pi*G_static*A)`. Varying positive `A` changes this
normalization without changing the historical dimensional construction.
The `12*pi` in that *conditional* spherical flux calculation is likewise
not a derivation of historical `f` or of the separate projection factor.

## Decision boundary

**Rejected:** repairing the v7.2/v11.1.1 displayed chain by a dimensionally
valid monomial is sufficient to derive `C_chi=1/(2*pi)` or any other unique
`C_chi`. **Retained as Conditional:** `cH0` is a possible dimensional scale
if the Hubble length is independently justified, but it is not yet an ITSM
force prediction. A viable route must derive, without target acceleration,
the action-level circulation/current-to-force map, the physical matter
coupling and `G_static`, a controlled common weak-field/EFT domain, the
projection factor, and the cosmological/local-frame `H(z)` relation. Only
then could an independent blinded coefficient and held-out data test follow.

The result is exact algebra, not analyst blinding, a physical solution, or
independent review. Master Tests 1-3, MAT-001, UVIR-003, Stage 4A and
publication holds are unchanged; `K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, and
Rule-9 review remains deferred rather than cleared. No legacy file or
sidecar was edited, and no commit, push or publication is authorized here.
