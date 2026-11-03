# Initial canonical/gauge pullback of the coupled auxiliary estimate

High bundle continues. Initial linear rate-map estimate only; not a physical
Hamiltonian norm, transported generator or statement about a future background.

Use all thirteen nonauxiliary canonical q,p slots. Let Q0=||delta q||L2,
Q1=||partial_z delta q||L2, P0=||delta p||L2, with Euclidean slot norms.
On the frozen original-coordinate zero-corrective-shift Legendre map,

    V0=||delta v0||L2 <= M_inv*(P0+A*Q0+B*Q1).

Here M_inv is the certified original temporal inverse; A,B are Frobenius upper
bounds of actual whole-circle/root-ball Hessian blocks L_vq and L_vd for rows
v0..v12 and columns q0..q12/d0..d12. The omitted auxiliary columns must be
EXACTLY absent under the receipt's sparse-zero convention; test this explicitly.
They are not dropped as a small numerical term. Indefinite shifts are not
treated as a positive physical kinetic matrix.

This is the initial coordinate rate convention of the existing gauge-velocity
owner. Its paired pullback supplies T*(delta v0-Lie_w delta q). With certified
W=sup|w|, P=sup|w_z|, the latter Lie term has L2 bound W*Q1+2P*Q0 in these
slots. Set F=max(1,J_upper,J_lower^-2), using an upward enclosure, and let Cxi
be the larger inherited L2-to-H1 gauge-velocity bound. Conversion of xi back
to the original corrective shift has H1 bound Cback=max(1,(1+r)/J_lower).
Then, with retained harmonic velocity norm Hc in adapted coordinates,

    Sbound = Cback*Cxi*F*(V0+W*Q1+2P*Q0)+Cback*Hc.

The bound is for the actual initial linear gauge-rate construction. It does
not identify that fixed-time composition with the complete nonlinear moving
constraint chart or assume its time persistence. Physical metric-modulus
rates remain the constants of the periodic solve. They are not set to zero.

For h=exp(2lambda)I, the full Frobenius metric Lie response has bound
Ch=2 exp(2r)*(1+sqrt(3)r) times ||delta S||H1. Thus

    ||delta h_t||L2,F <= sqrt(2)*V0+Ch*Sbound,
    ||delta psi_t||L2 <= V0+S1*Sbound,
    ||delta h||L2,F <= sqrt(2)*Q0,
    ||delta psi_z||L2 <= Q1.

The sqrt(2) factors account for double off-diagonal entries in a full matrix;
no metric component or harmonic is removed. Insert these in the coupled
auxiliary inequality. If Ceta,Cchi,Ck,Cl are its constants, define
R=Ceta*S1+Cl*Ch, U=Ceta+sqrt(2)*Cl+R*Cback*Cxi*F. Obtain

    ||delta Z_t||H-2 <= Cp*P0+Cq*Q0+Cd*Q1+Charm*Hc,
    Cp=U*M_inv,
    Cq=U*M_inv*A+2P*R*Cback*Cxi*F+sqrt(2)*Ck,
    Cd=U*M_inv*B+W*R*Cback*Cxi*F+Cchi,
    Charm=R*Cback.

All norms here are explicit coordinate control norms, not a selected physical
norm. Apply the map on the already compatible canonical data, retaining the
nonlocal eliminated momenta. Relating their sizes to density/free data through
the order-minus-two weak symplectic graph remains another part of the bundle.
No claim of constraint preservation or a closed evolution estimate follows.

Freeze controls: verify sparse auxiliary columns exactly absent; compare row
sum/column sum and Frobenius block norm bounds (all are valid upper bounds),
retain nonzero harmonic response, and independently test the metric Lie
Frobenius factor and scalar/matrix slot conversion on exact rational probes.
Use outward interval constants, pin receipts, immutable replay and verify
all inherited sources unchanged. No prior action, data or threshold changes.
