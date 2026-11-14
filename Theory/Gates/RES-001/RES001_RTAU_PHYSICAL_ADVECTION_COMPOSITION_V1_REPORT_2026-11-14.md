# Initial physical-time advection through the periodic normal form

Under the [frozen contract](RES001_RTAU_PHYSICAL_ADVECTION_COMPOSITION_V1_CONTRACT_2026-11-14.md),
physical advection now has an exact composition identity and an all-mode
initial L2 bound through the registered left-primitive change. This closes
the advection component only. The normal-form time derivative, energy
time derivative and evolving compatible-domain/background tube remain open.

## Exact original-coordinate identity

Write D=partial_z, M f=mean(f), P=D^-1(I-M) and

    T=I+i P C(z).

C is the existing cross normal-form matrix, denoted S in the earlier
periodic-principal owner. In this report v is the original background
longitudinal shift, not the force propagation drift. Thus physical
advection is v D. Both the mean and primitive are the original normalized
coordinate operations on the 2*pi circle, not proper-volume means.

For smooth periodic vector f,

    [T,vD]f = i [v M(Cf)-M(vCf)-P((v C_z+v_z C)f)].

Indeed, integration by parts gives

    P(Cv Df)=Cv f-M(Cv f)-P((Cv)_z f),
    v D P(Cf)=v Cf-v M(Cf).

The local products cancel because v is scalar. Neither remaining mean
term may be dropped. In particular

    M([T,vD]f)=i[M(v) M(Cf)-M(vCf)],

which need not vanish. For constant f the commutator is generally nonzero;
the original zero mode is included, not removed by division by frequency.
The density row of C is zero, so that row of this commutator remains zero.

The identity is first established on smooth inputs. Its right-hand side
extends boundedly to L2. This does not assert that v D itself is bounded
on L2 or enlarge its physical evolution domain.

## Whole-initial-root numerical bound

Let v0,v1 bound the shift and its spatial derivative and C0,C1 bound the
matrix coefficient and its spatial derivative in operator norm. Since
||P||=||M||=1 in the registered normalized L2 convention,

    ||[T,vD]|| <= 2 v0 C0+v0 C1+v1 C0.

Use the existing certified shift bounds from the physical-density
remainder coefficient environment and the registered mixed/periodic
principal certificates:

| Coefficient | Upper bound, rounded upward |
| --- | ---: |
| v0 | 0.002048606 |
| v1 | 0.003413280 |
| C0 | 0.601919086 |
| C1 | 0.058384797 |
| ||T^-1|| | 2.512052107 |

The executable uses the preserved binary interval endpoints, rather than
these displayed rounded values. It obtains

    ||[T,vD]|| <0.004641,
    ||[T,vD] T^-1|| <0.011657.

The corresponding upper endpoints are approximately
0.004640314286464 and 0.011656711276358. The separate exact-rational audit
certifies the displayed strict decimal inequalities. The coefficient
enclosures retain the prepared root uncertainty and original shift jets.
No derivative of a certification error radius was taken.

On the transported registered domain,

    T(vD)T^-1=vD+[T,vD]T^-1.

The original periodic inverse exists without a frequency cutoff under
its earlier norm and mixed-regularity domain proof. This equation adds
the bounded physical-advection commutator to the principal comparison;
it does not prove that the physical constraint domain persists in time.

## Position in the full calculation

With Z=T(t)Y the physical-time generator also contains

    T_t T^-1 Z.

This term has not been set to zero or included in the number 0.011657.
The time-dependent energy additionally needs its own H_t and compatible
global-partner estimates. Initial coefficient bounds supply no actual
background time tube and cannot be integrated as time-uniform constants.
The earlier initial twenty-row bound 226066 U remains unchanged.

Next derive C_t from the actual generic action-derived matrix dependence,
retaining the inverse/Schur derivatives and force Legendre terms. Establish
which initial background rates suffice; do not assume future conformality,
fixed normal clock velocity or stationary matching coefficients by analogy.
Any missing required rate remains an explicit substantive hold.

## Verification and preservation

The [executable](../../../Analysis/MasterTests/test_rtau_physical_advection_composition_v1.py)
verified 427 pinned inputs and sixteen controls. Independent sparse exact
Fourier convolution with nonconstant matrix/shift coefficients and
nonzero-mean inputs verifies the complete identity and detects omission
of either mean or either gradient term. A constant-input control retains
the zero mode and a separate mean identity checks its finite-rank response.
No grid sampling or Fourier tail truncation is used for the proof or bound.

The [receipt](../../../Analysis/MasterTests/outputs/rtau_physical_advection_composition_v1_20261114/receipt.json)
replayed byte for byte. The
[separate audit executable](../../../Analysis/MasterTests/audit_rtau_physical_advection_composition_v1.py)
checks aggregation, inverse composition and decimal certificates using
exact rational arithmetic. These are same-assistant computational checks,
not an independent reviewer panel or Rule-9 clearance. Original sources,
sidecars and failed prior versions remain preserved.

R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
No action, physical cutoff, matching value or publication status changes.
