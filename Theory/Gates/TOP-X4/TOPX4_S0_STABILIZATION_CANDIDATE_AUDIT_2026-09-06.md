# TOP-X4 S0 stabilization-candidate audit

**Date:** 2026-09-06  
**Status:** `SELECT_X4-S2F3_FOR_MAX_RETRY_ONLY`  
**Physics pass:** false  
**Gate effect:** none  
**Canonical effect:** none

## 1. Question and boundary

This High prescreen asks whether one separately declared sector can make a
smooth fourth circle worth retesting after the frozen `X4-I1C` parent returned
`X4-D2 HOLD_UNSTABILIZED`. It does not calculate a determinant, establish a
finite-density stationary background, predict a radius or alter canonical
ITSM's `T3` identity.

No observed acceleration, expansion, galaxy, compactification-size or
normalization target entered the calculation.

## 2. Primary-source controls

| Source | Result used | Scope limit applied here |
|---|---|---|
| Ponton & Poppitz, JHEP 06 (2001) 019, [arXiv:hep-ph/0105021](https://arxiv.org/abs/hep-ph/0105021) | A periodic real scalar has negative smooth-circle Casimir energy; a periodic 5D fermion contributes `-4` times that scalar result. Massive repulsive and massless attractive sectors plus a positive renormalized bulk vacuum term can produce a zero-vacuum-energy minimum. | Their worked phenomenology is primarily orbifold-based, but their unorbifolded `S1` sums and the massive-field mechanism are explicitly given. The bulk counterterm is not predicted by the low-energy EFT. |
| Witten, Nucl. Phys. B 195 (1982) 481, [DOI:10.1016/0550-3213(82)90007-4](https://doi.org/10.1016/0550-3213(82)90007-4) | The elementary-fermion spin structure is relevant to the semiclassical bubble-of-nothing instability of a KK circle. | This is a nonperturbative consistency issue, not proof that the perturbative radion minimum is stable. |
| Blanco-Pillado & Shlaer, Phys. Rev. D 82 (2010) 086015, [arXiv:1002.4408](https://arxiv.org/abs/1002.4408) | A complex scalar winding an `S1` can stabilize an `AdS4 x S1` compactification, yet the compactification can still nucleate a bubble of nothing. | Classical radial stability does not establish nonperturbative stability or a viable cosmology. |
| Goldberger & Wise, Phys. Rev. Lett. 83 (1999) 4922, [arXiv:hep-ph/9907447](https://arxiv.org/abs/hep-ph/9907447) | Their modulus potential uses a bulk scalar and localized interactions on two branes. | This is an `S1/Z2`/brane route, not a repair of the frozen smooth circle. |

## 3. Candidate decisions

| Candidate | Exact result | Decision |
|---|---|---|
| `X4-S1` altered condensate/winding | A Mexican-hat complex scalar with integer winding and a tuned negative vacuum term has a genuine positive amplitude/radion Hessian in an allowed domain, but the direct-product solution is `AdS4 x S1` and has zero temporal charge. | Preserve as a conditional mathematical control; do not select as the finite-charge retry. |
| `X4-S2` sign-competing one-loop content | Three periodic massive 5D Dirac spectators are the minimum strict count that can overcome the five attractive graviton degrees plus the three massive real bosonic degrees of `X4-I1C` at small radius. | Select `X4-S2F3` for one Max retry only. |
| `X4-S3` classical flux/p-form | A gauge two-form field strength has no nonzero purely internal component on one one-dimensional circle; a flat Wilson line has zero classical stress; an axion/phase one-form winding is already `X4-S1`. | No distinct minimal smooth-`S1` repair was identified. |
| `X4-S4` orbifold/brane | Fixed points change the geometry and require localized actions, counterterms and junction conditions. | Defer as a different parent, not a retry of `X4-I1C`. |

## 4. `X4-S1` conditional result

For a static complex scalar with

\[
 U(\rho)=U_{\rm vac}-\frac{m^2\rho^2}{2}
 +\frac{\lambda\rho^4}{8},\qquad
 K_w=\frac{\rho^2w^2}{2r^2},
\]

the four-dimensional Einstein-frame potential is

\[
 V_E(\rho,r)=\frac{U(\rho)}r+
 \frac{\rho^2w^2}{2r^3}.
\]

Simultaneous scalar, radion and five-dimensional Einstein stationarity gives

\[
 -m^2+\frac{\lambda\rho^2}{2}+\frac{w^2}{r^2}=0,
 \qquad U=-3K_w,
 \qquad \kappa_4=-\frac{2K_w}{3M_5^3}<0.
\]

The amplitude/radion Hessian is positive when

\[
 m^2r^2>\frac53w^2.
\]

The deterministic witness `m=lambda=w=1`, `r=2` has
`rho^2=1.5`, `U_vac=-0.09375`, `kappa_4=-0.125` in the declared
dimensionless units and Hessian determinant `0.328125`. Thus the old statement
"positive winding cannot repair the positive-potential parent" remains true
for that parent, while the broader statement "winding can never stabilize the
circle" would be false. The repair changes the vacuum sector and yields AdS,
so it is not selected.

## 5. `X4-S2F3` existence prescreen

At zero density, the frozen parent has five massless gravitational degrees and
three massive real bosonic degrees (`Phi` contributes two and `chi` one). In
units of the periodic real-scalar determinant,

\[
 \gamma=-5\zeta(5),\qquad \beta=4N_F-3.
\]

Strict small-radius repulsion requires

\[
 \beta\zeta(5)>5\zeta(5),
\]

so `N_F=1` fails, `N_F=2` is only marginal and `N_F=3` is the minimum
strict count, with `beta=9`.

On the equal-mass benchmark, define

\[
 F(x)={\rm Li}_5(e^{-x})+x{\rm Li}_4(e^{-x})
 +\frac{x^2}{3}{\rm Li}_3(e^{-x}),
\]

\[
 V(x)={\cal C}x^{-6}f(x),\qquad
 f(x)=\alpha x^5+9F(x)-5\zeta(5),\qquad {\cal C}>0.
\]

The zero-vacuum-energy stationarity conditions `f=f'=0` give the
dimensionless witness

\[
 x_*=2.5306790213096324,
 \quad \alpha_*=0.010588871709224016,
 \quad f''(x_*)=4.168021638768341>0.
\]

The residuals are `|f|=6.23e-61` and `f'=0` at 60-digit working precision.
With `x=m_F ell`, `ell=2*pi R`, the declared point
`m_F/Lambda_5=0.04` gives

\[
 \frac{\Delta_{\rm KK}}{\Lambda_5}
 =\frac{2\pi(m_F/\Lambda_5)}{x_*}
 =0.099313\ldots <0.1.
\]

This demonstrates a nonempty controlled parameter domain. It does not select
`m_F`, `Lambda_5` or the absolute radius. The renormalized bulk vacuum
coefficient `alpha` is fixed by a normalization condition and is not a
low-energy prediction.

## 6. Execution record

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\TOP\TOP-X4\topx4_s0_stabilization_prescreen.py
```

- calculation checks: `8/8`;
- status: `SELECT_TOPX4_S2F3_FOR_MAX_RETRY_ONLY`;
- physics pass: false;
- output SHA-256:
  `0758752d9ad1b354cc9cf91dbdf1bff31dac83c67a685644bb9938b82578c29a`.

An 8/8 result means the prespecified algebra and selection checks executed. It
does not validate the fermion determinant on the finite-density background.

## 7. Decision

Freeze `X4-S2F3` as exactly one retry parent. The original `X4-I1C` result
remains `X4-D2 HOLD_UNSTABILIZED`; `X4-S2F3` is only `MAX_READY_FROZEN`, not a
radion or physics pass. Max must independently derive the determinant, solve
the finite-charge semiclassical equations and test the full Hessian and cutoff
domain. A4 and Ultra remain closed.

