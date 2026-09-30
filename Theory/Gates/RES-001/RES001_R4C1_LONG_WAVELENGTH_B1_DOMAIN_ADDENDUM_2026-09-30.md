# R4C1-T2P4a: the formal long-wave branch misses the B1 subhorizon proxy

Date: 2026-09-30. Owner: Master Test 2 / conditional R4C1-v1.
Status: `ANALYTIC_CONDITIONAL_DOMAIN_RESTRICTION`; `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`.

This is an append-only qualification of the [T2P4 order-of-limits note](RES001_R4C1_LONG_WAVELENGTH_ORDER_OF_LIMITS_NOTE_2026-09-30.md),
SHA-256 `95f8d2f83d06c085d86b5220dbdc2c5b7f0652d9f25e21858ae73c740f1726af`.
That note's exact elliptic limit is unchanged. The B1 initial numbers and
finite-mode boundary come from the [T2P3 report](RES001_R4C1_COUPLED_LINEAR_LIMIT_REPORT_2026-09-29.md),
SHA-256 `0a947adceec27ba2b2ce3b3290928991de7d94727a7b9de9e6050b38e949b114`;
the original conditional equation is pinned by the [T2P1 report](RES001_R4C1_PERIODIC_FORCE_REPORT_2026-09-29.md),
SHA-256 `5f178a121aae03fb5b4d47cf383586f0496a7d18262fc5b6069dc8be0fc658ad`.
No parent source or sidecar is edited.

At the registered B1 initial state, `a=C=1`, `rho_bar=1/5`,
`H_E=sqrt(3469/4620)=0.866525129968...`, `beta=2/5`,
`psi_dot=1/5`, `A=2/7`, and `b=5/11`, in the same dimensionless reference
units. For the T2P4a source `delta_rho=epsilon*cos(kx)`, positivity of
`rho_bar+delta_rho` everywhere requires `0<epsilon<rho_bar`. The exact
rescaled elliptic parameter obeys

\[
 \delta^2=\frac{b^2 k^5}{3A\beta\epsilon}
  >\frac{b^2 k^5}{3A\beta\rho_{\rm bar}}.
\]

Consequently the declared **crossover diagnostic** `delta<=1` requires

\[
 k<k_*:=\left(\frac{3A\beta\rho_{\rm bar}}{b^2}\right)^{1/5}
   =0.802043109007\ldots < H_E.
\]

At `k=H_E`, even the limiting maximum contrast `epsilon=rho_bar` would
give `delta=1.21327325946...`; strict positive-density contrast gives a
larger value. Thus no member of **this fixed-B1, positive-total-density,
single-cosine family** has both `delta<=1` and `k>=a H_E` at `a=1`.
If one uses the matter metric `g_tilde=C^2 g`, its instantaneous Hubble
wavenumber at this initial state is still larger:
`a_m H_m=a*(H_E+beta*psi_dot)=0.946525129968...`.
The usual quasistatic requirement would be `k >> a_m H_m`, not merely
`k>=a H_E`, so the non-overlap under this permissive proxy is decisive for
the *strict* T2P4 long-wave asymptotic. Along `epsilon=k^4`, the ratio
`k/(a H_E)` tends to zero as `k -> 0`: that analytic square-root-shaped
limit is driven outside a subhorizon interpretation.

`delta<=1` is a transparent crossover diagnostic, **not** a proven
accuracy threshold for a physical radial-acceleration law. This inequality
does not rule out a finite mixed regime at `delta>1`, another background,
another source geometry, a different torus scale/time, or the full
coupled action. In particular, a full metric/frame/dust/Euler solution,
its physical EFT cutoff and a controlled quasistatic error remain absent.
The factor `C_contrast` is still not `C_chi`, no `a0` is derived, and
canonical Tests 1-3 and every parent/publication hold remain unchanged.
