# R4C1-G3I: nonlinear unit-frame scattering and the shrinking probe scale

Date: 2026-10-08. Owner: Master Test 1 / conditional R4C1-v1 / G3.
219/219 local checks pass; zero failed/unknown. All three artifacts replay
byte-identically. Review DEFERRED, Rule9_cleared=false, physics_pass=false,
gate_effect=NONE. Canonical Tests 1-3 HOLD_SUBSTANTIVE.

## Result

The G3 scaling keeps A/K_Q^(3/2) finite, but that does not make the nonlinear
unit-frame sector weakly interacting at fixed canonical momentum as eta->0.
In the declared fixed-metric vacuum probe, directly contracted cubic/quartic
vertices and their complete frame exchange diagrams give, at 90 degrees,

```text
M_probe = (388/25) p^2/(eta M_P^2),
f^2 = M_U^2(c1+c4) = eta M_P^2/6,
p_probe(90 deg) = 5 sqrt(eta) M_P/sqrt(388).
```

Here p_probe is defined ONLY by |M_probe|=1. It is an order-one tree-amplitude
diagnostic, not a derived partial-wave unitarity bound or full physical EFT
cutoff. It shrinks as sqrt(eta), whereas this nonzero on-shell amplitude grows
as 1/eta at fixed p/M_P. This establishes a nonuniform perturbative endpoint
in this probe, beyond an isolated negative/positive kinetic or vertex sign.

The complete finite-density metric/frame/force/dust interaction problem is
not solved. This result does not prove the full G3 background's physical
cutoff, invalidate G3DF's numerical accuracy, reject the entire candidate,
exclude every GR approach, or turn a tree calculation into a loop-controlled
quantum theory. Full coupled physical validity remains open.

## Action and exact unit constraint

The [contract](RES001_R4C1_G3_FRAME_SCATTERING_CONTRACT_2026-10-08.md)
was frozen after analytic planning and before executable contractions,
vertex checks and numerical evaluation. The 90-degree formula above was a
falsifiable planning comparator; it was not substituted as the calculated
amplitude.

Use the unchanged R4C1 frame action with all four c_i contractions, flat
metric (-+++), future unit U=(sqrt(1+v.v),v), other fields in their vacuum/
zero-exchange controls, and frozen metric perturbations. This is a probe
restriction, not the full dynamical Einstein metric or the on-shell
finite-density G3 background. No old B1 evaluated scalar matrices are used.

Let v_t=partial_t v, D_ij=partial_i v_j, d=div(v),
a_v=(v.grad)v, c14=c1+c4 and c123=c1+c2+c3. Direct contraction after solving
the unit multiplier constraint gives the second through fourth orders:

```text
L2 = M_U^2/2 [
  c14 |v_t|^2 - c1 D_ij D_ij - c2 d^2 - c3 D_ij D_ji ],

L3 = -M_U^2 [
  c2 d (v.v_t) + c3 sum_i v_ti (v.partial_i v) - c4 v_t.a_v ],

L4 = M_U^2/2 [
  -(c123+c4)(v.v_t)^2
  + c1 sum_i (v.partial_i v)^2
  + c4 (|v|^2 |v_t|^2 + |a_v|^2) ].
```

The exact unit constraint and each of its four differentiated constraints
vanish. Arbitrary first-derivative jets are retained in the invariant
calculation, not just one monochromatic field. Holding U^0=1 would omit
essential interactions and fails the registered rejection control.

With V=f v and f^2=M_U^2 c14, derive the quadratic Fourier kernel:

```text
K_ij = (omega^2-c_T^2 |k|^2) delta_ij
       + (c_T^2-c_L^2) k_i k_j,
c_T^2=c1/c14=4/5, c_L^2=c123/c14=1/6,

P = (I-k k^T/|k|^2)/(omega^2-c_T^2 |k|^2)
    + (k k^T/|k|^2)/(omega^2-c_L^2 |k|^2).
```

These are probe speeds. G3's finite-eta metric-shift-reduced transverse
speed and full scalar characteristic are different calculations; they are
not replaced by these values. The propagator is independently extracted
from L2 by two distinct Fourier amplitudes and its inverse identity checked.

## Contact and exchange, with all internal frame polarizations

Take external transverse polarization y and elastic COM momenta in the x-z
plane. All external legs have omega^2=c_T^2 p^2. Convention:
exp(-i omega t+i k.x), interaction vertex i G.

Extract the four-identical-polarization contact coefficient from four
distinct wave amplitudes in L4. Extract the WWV_i cubic coefficient from
two y-polarized external waves and each internal frame polarization in L3:

```text
G_i = [(c2+c3)(omega1+omega2)(k1_i+k2_i)
       + c4(omega1 k2_i+omega2 k1_i)]/(c14 f),
M_exchange = -G_left^T P G_right.
```

For x=cos(theta), strictly -1<x<1, the direct result is

```text
M_contact = 8 p^2/(3 f^2),
M_s = 0,
M_t = -p^2 (1+x)/[25 f^2 (1-x)],
M_u = -p^2 (1-x)/[25 f^2 (1+x)],

M_total = (p^2/f^2) [
  8/3 - (1/25)((1+x)/(1-x)+(1-x)/(1+x)) ].
```

The internal y vertex vanishes in these planar kinematics. The t/u vertices
are transverse to their exchanged momentum; the full transverse and
longitudinal propagator was nevertheless retained. The zero-spatial-momentum
s channel is evaluated with its nonzero-frequency propagator, not an inverse
through a vanishing spatial projector. Energy/momentum conservation, every
external mass shell and theta->pi-theta symmetry hold exactly.

At 90 degrees the contact is 16 p^2/(eta M_P^2), while each of t/u contributes
-0.24 p^2/(eta M_P^2). Their sum is 15.52 p^2/(eta M_P^2). Omitting exchanges,
reversing their sign or omitting the acceleration interaction is detected.

The t/u exchange poles at forward/backward angles are infrared poles, not
UV cutoff measurements. No finite partial-wave integral, infrared treatment,
phase-space normalization or unitarity bound was derived from them.

## Cancellation control

With c2=c3=c4=0 and c1>0, the identical-polarization on-shell amplitude is
exactly zero although the off-shell quartic derivative term is nonzero.
Its time and spatial pieces cancel on shell. This verifies that a derivative
coefficient alone would give a false diagnosis for this channel. It does not
claim that every polarization channel of that control is noninteracting.

The actual G3 nonzero sum remains after its own exchange diagrams. The
vanishing canonical rank at eta=0 is never inverted. A finite
A/K_Q^(3/2)=2 sqrt(3)/63 in reference units does not cancel this frame
amplitude, since the force term is absent from the declared frame probe.

## Frozen numerical grid and background screen

The full grid comprises six archived eta values, angles 60/90/120 degrees,
and p/M_P=(0.01,0.1,1,20,40,80): 108 amplitude events. Every contact,
s/t/u exchange, total and |M|<=1 classification is exported.
Maximum normalized symbolic/numerical discrepancy is 1.16858e-16.
All fixed-momentum eta refinements multiply the amplitude by four; each
registered momentum doubling multiplies it by four. Twenty-one events meet
the declared probe threshold and 87 exceed it. Strong events are diagnostic
results, not failed algebra checks.

| eta | f/M_P | p_probe(90 deg)/M_P |
|---:|---:|---:|
| 1 | 0.408248 | 0.253837 |
| 1/4 | 0.204124 | 0.126918 |
| 1/16 | 0.102062 | 0.0634591 |
| 1/64 | 0.0510310 | 0.0317296 |
| 1/256 | 0.0255155 | 0.0158648 |
| 1/1024 | 0.0127578 | 0.00793239 |

The archived G3DF backgrounds use M_P=1 reference units, eta=1,1/4,1/16,
k=20,40,80, [0,1],101 samples, both original background methods. Their
p=k/a and H are compared with the VACUUM probe scale, not a claimed
background amplitude calculation:

| eta | Range of p_probe/H, both methods | Range p/p_probe for k=20 |
|---:|---:|---:|
| 1 | 0.267413-0.431386 | 36.7345-78.7909 |
| 1/4 | 0.257200-0.376681 | 104.257-157.582 |
| 1/16 | 0.191624-0.270446 | 238.220-315.163 |

Ratios for k=40 and 80 are twice and four times the last column.
No registered sample satisfies p>=10H AND p<=p_probe. Even the corresponding
continuous momentum interval inferred from those sampled H values is empty
under that diagnostic screen, since p_probe<H. The threshold 10 is declared,
not an independently controlled adiabatic remainder bound.

**Conditional implication:** IF the coupled finite-density theory shares
this upper interaction scale, these reference backgrounds have no overlap
between an adiabatic momentum range and a weak probe-amplitude range.
The antecedent has not been established. Metric mixing, density-dependent
normalization, force/dust constraints and interaction cancellations may
alter the background eigenstate amplitudes. This screen is NOT a physical
exclusion or an all-action no-go.

G3DF's transfer accuracy and positive kinetic pullback remain valid within
their archived classical scope. They establish no low-energy quantum/EFT
admissibility. None of these chart momenta are measured galactic wavelengths.

## External methodology and retained physics inputs

[Withers, Einstein-aether as a quantum effective field theory
(arXiv:0905.2446v1)](https://arxiv.org/pdf/0905.2446) develops unit-constraint
and mixed gravity/aether power counting, and gives vacuum four-aether
scattering with leading energy-squared/aether-scale-squared behavior
(sections 3-5, especially equations 4.7-4.10 and 5.5). It is methodological
context only; the coefficients above were calculated from R4C1.
Its two-derivative vacuum analysis does not provide power counting for
R4C1's quartic force dispersion, nonanalytic Y^(3/2) vertex or pressureless
finite-density dust sector. Only selected relevant sections were inspected;
no paper replay or full coupled-cutoff proof is claimed.

To establish or reject a physical window, the next discriminating calculation
must reinstate dynamical metric constraints on an actual finite-density
background, derive the coupled cubic/quartic vertices and physical
eigenstate amplitudes, and test whether the probe's shrinking scale survives.
If it does, the frozen G3 trajectory cannot be admitted on the basis of the
earlier density tests; a separately frozen route/domain decision is required.
Unknown higher-derivative matching, loops, infrared treatment, arbitrary
fast-wave data, complete IVP/continuous estimates and healthy GR remain
substantive holds. The probe alone does not justify retuning old parameters.

## Reproducibility and disposition

- Contract:
  f54c7a7297350256ae199c3ba2b5f19266094c57739b95c6dad0ee253627d5f8.
- [Executable](../../../Analysis/MasterTests/test_01_r4c1_g3_frame_scattering.py):
  131dba4eccba8dcaffb6f5a1215d6089576907a04f45ec5cb534ea9cb0bea343.
- [Attempt 01 receipt](../../../Analysis/MasterTests/outputs/r4c1_g3i_attempt_01/summary.json):
  0d85d136e7c7a3c4cd4b49d984f70d3bfdbdd70aed82b3fc423181028aa1d9c7.
- [Exact vertices and amplitudes](../../../Analysis/MasterTests/outputs/r4c1_g3i_attempt_01/formulas.json):
  cacb666c1f4594d75637075572b4ea37d401f2b02ff7e25edf5a62b0acc49694.
- [Full numerical grid and conditional screen](../../../Analysis/MasterTests/outputs/r4c1_g3i_attempt_01/grid.json):
  3b9c00b82d33b7e821d6a2421d3b4da8245d68032df2d1b90fc1f0fe1c539efa.

All 58 unique direct/transitive source pins match, including the original
failed G3 receipt and retained refinement/descendant evidence. All new
artifact sidecars match. Replay recomputes all artifacts without writes,
with identical bytes. Existing outputs are refused. No old main() invoked.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_frame_scattering.py --replay
```

The initial executable failed during JSON serialization because SymPy's
Matrix.applyfunc(str) did not produce plain string matrix entries. It wrote
no scientific receipt. Its source is preserved as
test_01_r4c1_g3_frame_scattering_v1.py, SHA-256
70c9ce82c7f874219fdfed2161ae58cf3e4a309e29f4286b5b801f0e0c67a524.
The preserved ignored failure log has digest
6b82a53ecdd764a4709901207cbc21018c22d26c93950f374ed8cc7522bb1154.
Only matrix string export was corrected; frozen physics, grid and criteria
did not change. No numerical or scientific failure was erased.

Register R9-MT1-G3I. Inherit R9-MT1-VARIATION/B1/G1/S1/G2/G3/G3S/G3Z/
G3E/G3A/G3F/G3D/G3DF and applicable PD1 scope/review dependencies.
PROCEED_PROVISIONALLY for this probe; claim Conditional, review DEFERRED.
The calculations pass; the full physical cutoff and canonical dependent
uses remain HOLD_SUBSTANTIVE. No SPARC prediction or likelihood is supplied.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged. No memory mutation, PDF edit, provider
dispatch, commit, push, promotion or publication.
