# UVIR-002 — Alternative UV/IR route selection

Status: **closed as a provisional architecture selection**
Calculation validation: **PASS**
Microscopic closure: **OPEN**
Selected route: **two-sector preferred-frame force EFT**
MAT-001: **BLOCKED pending UVIR-003**

## Executive result

UVIR-001 showed that a stable canonical finite-density complex scalar cannot
directly generate the required spatial `Y^(3/2)` operator: its nonzero
`P_Z` produces a quadratic static-gradient term first. UVIR-002 compared three
ways around that no-go.

1. A nonrelativistic gradient-dominated single field produces the desired
   cubic spatial action exactly, but its zero-temperature target branch has a
   negative quadratic time kinetic coefficient. It is rejected as a standalone
   microscopic route.
2. Splitting the density carrier and force mediator removes the requirement
   that one field satisfy incompatible equilibrium and force roles. This is a
   useful architectural move, but it does not derive the cubic force operator,
   its coefficient, or a regular zero-gradient limit.
3. A preferred frame permits independent temporal and spatial invariants. It
   can therefore combine positive time kinetics with a spatial cubic response
   without contradicting UVIR-001. The cubic truncation is locally stable about
   a nonzero spatial gradient, but its quadratic spatial operator degenerates
   at zero gradient and the Wilson coefficient remains unmatched.

The gate therefore provisionally selects a hybrid of routes 2 and 3:

```text
complex condensate Phi
    -> finite density, circulation, vortices, topology and background stress

separate preferred-frame force sector (psi, U^mu)
    -> independent temporal Q and spatial Y invariants
    -> conditional low-acceleration Y^(3/2) response
```

This is a route selection, not a microscopic derivation. UVIR-003 must build
and test the full selected action before MAT-001 may match the matter vertex.

## 1. Selection criteria

Each route was tested against seven requirements:

1. existence of the spatial cubic operator;
2. positive quadratic time kinetic term;
3. stability of the target branch;
4. controlled behavior as the background spatial gradient tends to zero;
5. derivation of the cubic Wilson coefficient;
6. a path to universal matter dynamics and lensing;
7. retention of the recovered ITSM condensate, circulation and topology core.

No candidate passes all seven. The result is consequently a conditional
selection of the least incomplete route, not a declaration of UV closure.

## 2. Route A — nonrelativistic gradient-dominated single field

Use the Galilean superfluid invariant

\[
X=\dot\theta-m\Phi_N-
\frac{|\nabla\theta|^2}{2m}
\]

and the branch

\[
P(X)=\kappa X\sqrt{|X|}.
\]

For a static gradient-dominated configuration, write

\[
X=-u=-\frac{q^2}{2m}<0,
\qquad q=|\nabla\theta|.
\]

Then

\[
P=-\kappa u^{3/2}
=-\frac{\kappa}{(2m)^{3/2}}q^3.
\]

Thus this branch produces the required spatial power exactly. However,

\[
P_X=\frac32\kappa\sqrt{u}>0,
\qquad
P_{XX}=-\frac{3\kappa}{4\sqrt{u}}<0.
\]

For `theta = theta_bar + pi`, the quadratic action contains

\[
\mathcal L^{(2)}
\supset
\frac12P_{XX}\dot\pi^2
-\frac{P_X}{2m}|\nabla\pi|^2.
\]

The negative `P_XX` is a ghost on precisely the branch that supplies the
MOND-like cubic response. Finite-temperature operators or additional fields
can change this conclusion, but then the route is no longer the minimal
single-field candidate being tested.

**Verdict: Rejected as a standalone zero-temperature route.**

This result is consistent with the model history in
[Berezhiani and Khoury](https://arxiv.org/abs/1507.01019), where the phonon
MOND-like EFT is assumed, and with the stability/equilibrium analysis of
[Mistele](https://arxiv.org/abs/2009.03003).

## 3. Route B — split density and force fields

A two-field architecture assigns different physical jobs to different modes:

```text
Phi: finite-density background, energy density, circulation and defects
psi: long-range low-acceleration force response
```

This removes the requirement that a shift-breaking baryonic force solution
also be the equilibrium density-carrying superfluid solution. Published work
has identified that role conflict and proposed a two-field resolution.

The split alone is not a derivation. If the force action simply contains

\[
-A\left(h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi\right)^{3/2},
\]

then the required exponent and coefficient have been supplied as EFT input.
Moreover, a force scalar with an ordinary positive time kinetic term and only a
spatial cubic has no quadratic spatial restoring term about zero gradient.

**Verdict: Conditional architectural ingredient, insufficient alone.**

## 4. Route C — preferred-frame force sector

The finite-density medium already defines, or motivates, a unit timelike frame
`U^mu` and spatial projector

\[
h^{\mu\nu}=g^{\mu\nu}+U^\mu U^\nu.
\]

Define independent invariants

\[
Q=\frac{U^\mu\nabla_\mu\psi}{a_0},
\qquad
Y=\frac{h^{\mu\nu}\nabla_\mu\psi\nabla_\nu\psi}{a_0^2}.
\]

A schematic force-sector action is

\[
\mathcal L_{\rm force}
=M_Q^4 K(Q)
-\frac{2C_{\rm IR}}{3}M_P^2a_0^2Y^{3/2}
+\mathcal L_{\rm reg}
+\mathcal L_{\rm mix}.
\]

Near a temporal background `Q_0`, positive time kinetics can be supplied by

\[
K(Q)=\frac{k_Q}{2}(Q-Q_0)^2+\cdots,
\qquad k_Q>0.
\]

This is the essential improvement: UVIR-001 tied time and space derivatives
to one Lorentz scalar `Z`; the preferred-frame construction does not.

### 4.1 Local spatial stability check

Let the spatial energy density be

\[
E=A|\mathbf v+\nabla\varphi|^3,
\qquad A>0,
\qquad |\mathbf v|=q>0.
\]

Choose `v=(q,0,0)`. The Hessian with respect to the three components of
`grad(varphi)` is

\[
\frac{\partial^2 E}{\partial(\partial_i\varphi)
\partial(\partial_j\varphi)}
=\operatorname{diag}(6Aq,3Aq,3Aq).
\]

It is positive for `A,q>0`. With temporal coefficient `F^2>0`, the local
characteristic speeds of the decoupled truncation are

\[
c_L^2=\frac{6Aq}{F^2},
\qquad
c_T^2=\frac{3Aq}{F^2}.
\]

Both vanish as `q -> 0`. Therefore the simple cubic truncation has a degenerate
linearized spatial operator at zero gradient. It needs a controlled regulator,
additional operators, or mixing with metric/vector modes. A full theory must
also check all constraints and propagating degrees of freedom; positivity of
this local Hessian is not a complete stability proof.

Preferred-foliation and scalar-vector theories provide relevant precedents.
[Blanchet and Marsat](https://arxiv.org/abs/1107.5264) construct a heuristic
preferred-foliation MOND theory with a metric lensing path.
[Skordis and Zlosnik](https://arxiv.org/abs/2007.00082) use distinct temporal
and spatial structures in a relativistic scalar-vector theory and report a
quadratic action free of ghost instabilities. Their separate stability study
also identifies the remaining mode-dependent qualifications
([arXiv:2109.13287](https://arxiv.org/abs/2109.13287)). These results establish
precedent, not automatic stability of the ITSM truncation.

**Verdict: Conditional and the best force-sector route tested.**

## 5. Provisional selected architecture

The successor theory to test is

\[
S=S_{\rm EH}
+S_{\Phi}[\Phi,g]
+S_U[U,g]
+S_{\rm force}[\psi,U,g]
+S_{\rm int}[\psi,\Phi,\Psi_m]
+S_R.
\]

The division of labor is:

- `Phi` retains finite density, amplitude physics, winding, vortices and the
  compact-topology ontology;
- `U^mu` supplies the physical rest frame and spatial projector;
- `psi` mediates the conditional low-acceleration force;
- the force action uses independent `Q` and `Y` invariants;
- `S_int` must later generate the matter force and exchange current together;
- `S_R` remains the reservoir sector required for the open subsystem.

Whether `U^mu` is the normalized condensate current, an independent aether
field, or a khronon foliation is deliberately not fixed by UVIR-002. That is a
dynamical choice to be settled by UVIR-003, not a wording choice.

## 6. Why microscopic closure remains open

The selected route has not yet shown:

- a symmetry that protects the relative temporal and spatial operators;
- a regular `q -> 0` limit that retains the deep cubic regime;
- the complete constraint and degree-of-freedom count;
- a Hamiltonian bounded below for all coupled modes;
- subluminal or otherwise acceptable characteristics across regimes;
- derivation of `C_IR` from condensate parameters;
- a controlled high-gradient screened branch;
- the unique relation between `U^mu` and the condensate;
- the matter metric and lensing response.

In particular, the fact that `Y^(3/2)` is permitted by the preferred frame does
not explain why lower-order spatial operators are absent or sufficiently small.
That technical-naturalness question is load-bearing.

## 7. UVIR-003 pass conditions

UVIR-003 must:

1. declare one full covariant two-sector action;
2. fix whether `U^mu` is derived or independent;
3. count constraints and propagating degrees of freedom;
4. derive the quadratic action about cosmological, zero-gradient and galactic
   nonzero-gradient backgrounds;
5. demonstrate positive kinetic and gradient matrices in the claimed domain;
6. regularize the zero-gradient limit without destroying the cubic deep branch;
7. identify the cutoff and strong-coupling scale;
8. state the symmetry or matching mechanism controlling lower operators;
9. derive, rather than assign, the candidate map to `C_IR` if possible;
10. expose the matter/lensing and screening dependencies without claiming they
    are already closed.

MAT-001 remains blocked until at least items 1–8 pass. A failure to derive
`C_IR` would leave a phenomenological EFT and must be recorded explicitly.

## 8. Gate classification

| Item | Classification |
|---|---|
| Nonrelativistic `X<0` branch produces a static cubic | Derived |
| Same branch has `P_XX<0` | Derived; route rejected |
| Two-field role split resolves the one-field role conflict | Conditional |
| Preferred frame evades the single-invariant UVIR-001 no-go | Derived structurally |
| Cubic spatial Hessian is positive at nonzero gradient | Derived locally |
| Cubic truncation is controlled at zero gradient | Rejected |
| Two-sector preferred-frame route | Provisionally selected |
| Microscopic origin and coefficient of `Y^(3/2)` | Open |
| MAT-001 readiness | Blocked pending UVIR-003 |

## 9. Reproduction

From the repository root run:

```powershell
python Analysis/UVIR/UVIR-002/uvir002_route_comparison.py
```

Expected terminal footer:

```text
UVIR-002 calculation validation: PASS
Route A verdict: REJECTED
Route B verdict: CONDITIONAL
Route C verdict: CONDITIONAL
Selected route: TWO_SECTOR_PREFERRED_FRAME_FORCE_EFT (PROVISIONAL)
Microscopic closure: OPEN
MAT-001: BLOCKED_PENDING_UVIR_003
STATUS: PASS
```

The machine-readable summary and comparison table are stored under
`Analysis/UVIR/UVIR-002/outputs/`.
