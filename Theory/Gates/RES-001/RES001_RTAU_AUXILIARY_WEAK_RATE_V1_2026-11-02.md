# Auxiliary rate: strong jets versus a weak estimate

High derivation, 2 November 2026. Conditional component estimate only; R-tau
unadopted, physical_norm=NOT_DERIVED, physical_clearance=false.

On the fixed 2pi-periodic planar coordinate write

    Z=-a psi_zz-b psi_z,
    Z_t=-a v_zz-b v_z-a_t psi_zz-b_t psi_z, v=psi_t,
    a=h^{zz}, b=a tr(h^{-1}h_z)/2-(h^{-1}h_z h^{-1})^{zz}.

Use periodic L2 with fixed dz measure, Bessel H2 with Fourier squared weight
(1+k^2)^2, and its dual H-2. These are mathematical control norms. Their
equivalence to physical weighted observables requires metric/volume bounds.

Assume a in W^{2,infinity}, b in W^{1,infinity}, a_t,b_t bounded, psi in H2,
v in L2. Define products distributionally. For periodic phi in H2,

    <a v_zz,phi>=<v,(a phi)_zz>,
    <b v_z,phi>=-<v,(b phi)_z>.

Expanding these products and applying Cauchy-Schwarz yields, with
a_j=||partial_z^j a||infinity and b_j analogously,

    ||Z_t||H-2 <= (a_0+2 a_1+a_2+b_0+b_1)||v||L2
                  + ||a_t||infinity ||psi_zz||L2
                  + ||b_t||infinity ||psi_z||L2.

Each factor is explicit, but numerical bounds on the actual uncertain prepared
or evolving background are NOT supplied. This estimate is for prescribed metric
coefficients; it does not eliminate the zero-speed/quartic coupling or assume
time persistence. In the full linearized system, variations of a_t,b_t multiply
background psi derivatives. The coupled metric velocity/momentum norms must
control those variations; arbitrary rough metric velocities cannot simply be
declared bounded coefficients.

Likewise ||Z||L2 <= a_0||psi_zz||L2+b_0||psi_z||L2. The strong point evaluator
needs psi_t derivatives through four to return two spatial derivatives of Z_t;
that implementation domain does not prove the physical phase space requires
psi_t in H4. Its weak domain can be strictly larger.

## All-frequency control and rejection

For the flat frozen control a=1,b=0, take an L2-normalized periodic Fourier
velocity mode v_k, integer k>=1, with psi=0 at that instant. Exactly,

    ||Z_t||L2=k^2,
    ||Z_t||H-2=k^2/(1+k^2)<=1,
    ||v_k||L2=1.

The strong norm is unbounded over k; the weak norm is uniformly bounded.
Therefore the auxiliary relation does not imply a bounded L2 velocity to L2
auxiliary-rate map. Imposing that strong requirement without physical
justification could exclude admissible data. This reference control does NOT
prove that the prepared coupled problem's correct physical norm has this
weight. That norm must still come from observables and the weak symplectic map.
No mode, forced tail, constraint or physical clock flow is removed.

Freeze exact controls at k=1,2,8,32,128,512 and the symbolic identity
1-k^2/(1+k^2)=1/(1+k^2)>0 before running their executable. The preceding
all-k argument, not those six probes, establishes the reference distinction.
The actual global compatible generator, quantitative coefficient bounds,
charges/means, moving gauge/range and finite-time estimate remain incomplete.
