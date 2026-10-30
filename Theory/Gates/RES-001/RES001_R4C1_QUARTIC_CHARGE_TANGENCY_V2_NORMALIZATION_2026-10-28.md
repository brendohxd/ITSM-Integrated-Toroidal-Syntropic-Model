# Physical density versus density weight: V2 normalization correction

28 October 2026. Conditional; review DEFERRED; no gate promotion.

The V1 contract and executable confused the time derivative of a weight-one
Hamiltonian density with the derivative of the physical scalar dust density.
V1's FAILED 216/236 receipt, executable, contract and sidecars are retained.
All twenty failures were the dust comparison, twice at each registered point.
The unvalidated working-algebra note has the same error. This addendum
explicitly corrects that equation; it does not alter the action or current law.

The original full density is L=sqrt(h)*L_scalar. Its momenta and Legendre
energy E are weight-one densities. The normalized-frame lapse flux
J=gamma*h_inverse[z,i]*Pi_Vi is likewise a vector density. Lapse variation
therefore imposes the density equation

    E+partial_z(J)+sqrt(h)*rho=0,
    rho=(-E-partial_z(J))/sqrt(h).

At the registered initial h=I, the scalar and weight-one values coincide,
but their time derivatives do not. Differentiate the quotient BEFORE
substituting h=I and hdot=2H*I:

    sqrt(h)_dot/sqrt(h)=trace(h_inverse*hdot)/2=3H,
    rho_dot=-E_dot-partial_z(J_dot)-3H*rho.

This correction follows from the determinant and the lapse equation, not
from assigning the required dust-current answer. E_dot is still computed
from the independent full generator; J_dot still retains inverse-metric drift.
On this initial spatially constant metric rho_z is unchanged.

Recompute all ten points and both steps in a new V2 executable and fresh
directory. Keep the V1 precision, steps, tolerance, Fourier construction,
all fields, real/Taylor controls and substantive holds. Pin V1's receipt
and source chain. Add exact determinant/quotient identities and a direct
real differentiation of the physical-density quotient at the two interior
controls. Add a rejection control for omission of the -3H*rho volume drift.
Do not patch V1 results or claim a physical failure from V1's normalization
error. No criterion is weakened. Reproduce the corrected scientific bytes
with a different worker count.

This remains a sampled initial tangency diagnostic, not continuum constraint
propagation, nodal persistence, an IVP, physical-window clearance or matching.
G1-G6 INCOMPLETE; physics_pass=false; gate_effect=NONE. All original source
files, sidecars and failed attempts remain unchanged. No vault mutation,
commit/push, publication or external dispatch.
