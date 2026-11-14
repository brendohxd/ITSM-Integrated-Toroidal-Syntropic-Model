# Initial mixed energy with global partners and coordinate controls

The [assembly contract](RES001_RTAU_INITIAL_ENERGY_ASSEMBLY_V1_CONTRACT_2026-11-14.md)
now has a conditional initial forced energy inequality in the registered
planar periodic problem. It includes the twenty state directions and
fifteen retained global partners. The three harmonic coordinate velocities
remain explicit inputs of the existing spatial gauge.

In the benchmark convention, conservative rounded certificates are

    E'(0) <=4.488985e20 E(0)+1.658735e12 |H3(0)|^2.

The numerical upper endpoints are approximately
448898491229516560015.563602 and 1658734869183.116144.
These large initial bounds are not measured growth rates, useful accuracy
certificates, stability over [0,0.05] or a background evolution theorem.
Here forcing denotes the registered coordinate-control input.

## State, globals and supported domain

Use the actual state Y=(w,Q8,P9,zeta,xi), the existing cross normal form
Z=T Y and its diagonal controlling energy Hdiag. Retain

    g15=(mean(phi)_8, metric_moduli_3, mean(chi)_1, eta_3),
    E=mean(Z^dagger Hdiag Z)+|g15|^2.

All means use the original normalized 2*pi coordinate. The metric moduli
use their owning moving-chart definition and rates. Eta denotes the
original eliminated canonical momentum means, not adapted means promoted
to new charges. The total-I/U1 and weighted-range restrictions remain
conditions on admissible tuples. The variable count introduces no new
physical degrees of freedom.

The inequality applies to the inherited smooth compatible exact initial
Euler/constraint/auxiliary jets within the certified root enclosure.
Its bound covers all registered integer modes, not a sampled mode list.
The finite numerical centre is not declared an exact background. No
preservation of this domain at later times is asserted.

## Full derivative identity

Write G for the registered material principal operator and Gdiag for its
diagonal principal form. The completed actual row comparison and periodic
normal-form identity give

    Z_t=S D Z+Gdiag Z+K Z+T R_init(T^-1 Z,g,H3),
    K=Rpre T^-1+[T,S D]T^-1+T_t T^-1.

Every mean/primitive term in Rpre and the advection commutator is retained.
On the supported smooth periodic domain, the exact energy identity is

    E'=mean(Z^dagger Hdiag_t Z)
       -mean(Z^dagger (S Hdiag)_z Z)
       +Q_spatial[Z]+2 Re mean(Z^dagger Hdiag K Z)
       +2 Re mean(Z^dagger Hdiag T R_init)
       +2 Re(g^dagger g_t).

Q_spatial is the completed ordinary/fast principal spatial-adjoint form.
Its certified bound is inherited from the periodic-principal owner. The
physical advection term includes both S_z Hdiag and S Hdiag_z. Hdiag_t
is counted once; the pulled-back Horiginal_t is not added to this
transformed-state identity. The physical-rho observable is reconstructed
by its existing bounded static map; it is not substituted for w's row or
given a new bounded-rate assertion.

The differentiated trace/Green, weighted range, charge and gauge owners
support these initial compatible maps and rates. They are initial-jet
prerequisites, not a proof of an evolving compatible generator domain.

## Actual global rates

The eight original configuration means and force mean obey their actual
canonical field-rate equations. Their combined mean projection is a
contraction: its rows have Gram matrix diag(1/2,1,...,1). Thus

    |mean(phi)_t|^2+|mean(chi)_t|^2 <=||delta q_t,13||L2^2.

The gauge-closed canonical L2 rate is composed with the corrected momentum/
configuration lift and corrective shift. The existing physical-modulus
and three canonical-mean rate bounds are retained with their moving basis
and dual gauge terms. If q_j,m_j,e_xj,e_yj,e_zj are their nine input
coefficients, the full partner rate has coefficients

    L_j=sqrt(q_j^2+m_j^2+e_xj^2+e_yj^2+e_zj^2),
    |g_t|<=L U, L<291760.830603.

U is the original sum of nine strong/global input norms, including the
harmonic velocity norm. This uses actual field/modulus/momentum equations;
no physical mean rate is set to zero.

## Coercivity and scalar aggregation

From the actual state map and T inverse,

    U<=bz ||Z||+bg |g|+|H3|,
    bz=5||T^-1||, bg=sqrt(6+Cmod^2),
    Cmod=exp(4/13000)sqrt(1+4/13000^2).

Let a0 be the minimum of the inherited ordinary energy lower bound and
the two fast weights, and H0 bound Hdiag. The augmented energy satisfies

    E>=a0 ||Z||^2+|g|^2,
    E>=1.07346e-7 (||Z||^2+|g|^2).

For U0 equal to the first eight input norms, excluding the independent
coordinate velocity, the registered reconstruction also gives

    U0^2<=1.469641e9 E,
    E<=1.175392e7 U0^2.

These are explicit controlling-norm equivalences on the inherited chart.
The previously checked force H2, full canonical and physical-density maps
remain their prerequisites. This is not a flat-L2 inverse of the
unreduced physical symplectic operator or a positive-Hamiltonian verdict.

For reproducibility, put B=H0 ||T|| C_U, where C_U bounds the actual
twenty-row remainder per U, and let K0 bound the three bounded terms in K.
The exact derivative and Cauchy inequalities give the scalar terms

    base=||Hdiag_t||+A_spatial+||S_z||H0+||S|| ||Hdiag_z||
         +2 H0 K0+2 B bz,
    cross_zg=B bg+L bz, cross_zH=B,
    self_g=2 L bg, cross_gH=L.

Young's inequalities yield coefficients

    Kz=base+cross_zg+cross_zH,
    Kg=self_g+cross_zg+cross_gH,
    KH=cross_zH+cross_gH,
    CE=max(Kz/a0,Kg).

The receipt retains every contribution and the outward interval endpoints.
The fast Hdiag_z bound uses the certified mass derivative and the analytic
initial lapse/volume profiles, without differentiating a root-error radius.
Large conditioning and triangle bounds make CE especially conservative.

## Coordinate forcing and stronger claims

The owning spatial-gauge solution is

    xi_i=H_i+P[u_i(c_i-b_i)].

Its spatial derivative does not determine H_i. Adding H_i(t) leaves the
gauge gradient equations unchanged. Therefore those equations do not
supply an H_t law or a prescribed future history. This estimate retains
|H3|^2 as forcing and requires no invented zero-rate assumption.

The supported initial forced assembly is complete in this scope. Closed
autonomous physical evolution, a justified future gauge/control history,
compatible-domain persistence and an actual background/coefficient time
tube remain open. Initial constants cannot be integrated as if they held
uniformly over [0,0.05]. Next resolve those continuation prerequisites,
including whether the initial Ward/energy chart extends to the metric
directions permitted by the actual background evolution.

## Evidence

The [executable](../../../Analysis/MasterTests/test_rtau_initial_energy_assembly_v1.py)
verified 439 pinned sources and nineteen controls; its
[receipt](../../../Analysis/MasterTests/outputs/rtau_initial_energy_assembly_v1_20261114/receipt.json)
replayed byte for byte. Exact Laurent integration checks the complete
energy identity with variable ordinary/fast coefficients, nonzero means,
finite-rank and primitive terms, global rates and harmonic forcing.
Omission controls detect every such sector.

The [separate audit](../../../Analysis/MasterTests/audit_rtau_initial_energy_assembly_v1.py)
passed seventeen controls and replayed exactly. It checks canonical/global
rate aggregation, inherited coercivity, Young's identity and the final
constants with exact rational arithmetic, plus a higher-precision control
of the global chart weight. These are same-assistant computational checks,
not an independent peer-review panel or Rule-9 clearance. Original
scientific sources, hashes, sidecars and failures remain preserved.

R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
No action adoption, physical interaction window, matching value,
numerical acceleration prediction or canonical promotion follows.
