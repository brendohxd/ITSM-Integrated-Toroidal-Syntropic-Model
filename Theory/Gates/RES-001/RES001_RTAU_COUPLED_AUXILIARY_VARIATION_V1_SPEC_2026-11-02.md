# Coupled auxiliary variation: frozen formulas and verification scope

Substep of the coupled observable-norm bundle; High remains acknowledged.
No parent adoption or full physical norm is inferred. Fixed original coordinate.

Let mu=sqrt(det h), H=h^-1, a=Hzz, c=mu*a, q=1/mu, p=mu_t/mu^2.
Metric perturbations are k=delta h and l=delta h_t; scalar perturbations
chi=delta psi, eta=delta psi_t; background v=psi_t.
Use full symmetric matrices, with Frobenius contraction over both indices:

    E=H/2, d=E:k,
    D=mu*(-H[:,z] H[z,:]+a*H/2), delta c=D:k,
    d_t=E:l+E_t:k,
    F=c*chi_z+(D:k)*psi_z,
    G=c_t*chi_z+(D:l+D_t:k)*psi_z+(D:k)*v_z.

Then, exactly,

    delta Z=-d*Z-q*F_z,
    delta Z_t=-d_t*Z-d*Z_t+p*F_z-q*G_z-q*(c*eta_z)_z.

These follow from differentiating Z=-mu^-1*(c psi_z)_z, with time and variation
commuting in the fixed coordinate. They retain six metric and velocity entries,
including constant/harmonic metric variations; no coordinate quotient is taken.

For fixed smooth background coefficients, distributional integration by parts
gives ||u f_z||H-1 <= (||u||inf+||u_z||inf)||f||L2. Thus the strong point
formula may contain l_z, while its H-2 bound requires only l in L2.
Let E0,Et0,D0,Dt0 bound Frobenius norms. Let S1,S2 bound |psi_z|,|psi_zz|,
V1,V2 bound |v_z|,|v_zz|, Z0,Zt0 bound |Z|,|Z_t|. Put
Q1=||q||inf+||q_z||inf, P1=||p||inf+||p_z||inf. Then

    ||delta Z_t||H-2 <= K_v||eta||L2+C_chi||chi_z||L2
                          +C_k||k||L2(Frobenius)+C_l||l||L2(Frobenius),
    C_chi=P1*c0+Q1*ct0,
    C_k=Et0*Z0+E0*Zt0+P1*D0*S1+Q1*(Dt0*S1+D0*V1),
    C_l=E0*Z0+Q1*D0*S1.

For the actual ORIGINAL initial conformal background, r=1/13000,
M bounds |lambda_t| and B=2*epsilon/31 bounds |lambda_t,z| as previously
certified. With epsilon=1/1000, use
S1=epsilon*(1/29+2/31), S2=epsilon*(1/29+4/31),
V1=3*epsilon/47, V2=9*epsilon/47,
Z0=exp(2r)*(S2+r*S1),
Zt0=2*M*Z0+exp(2r)*(V2+r*V1+B*S1),
E0=sqrt(3)*exp(2r)/2, Et0=2*M*E0,
D0=sqrt(3)*exp(r)/2, Dt0=M*D0,
c0=exp(r), ct0=M*exp(r), Q1=exp(3r)*(1+3r),
P1=3*exp(3r)*(M+B+3*M*r).
Here D=exp(-lambda)*diag(1/2,1/2,-1/2), not exp(+lambda) times that matrix.
The constant part 1/5 of v is retained in the action; its spatial derivatives
vanish in this auxiliary map, not by deleting physical clock evolution.

Freeze exact controls before execution: compare mixed time/metric/scalar
variation against direct full-metric Laplace-Beltrami differentiation on a
nonconstant rational fixture with all six metric perturbations nonzero. Check
spatial Lie transport with its tensor-index terms, constant metric variation,
and a nonzero independent velocity perturbation. Reject dropping volume
variation or l. Use exact equality. Export actual initial constants using
60-digit outward interval arithmetic, source pins, fresh receipt and replay.

No claim is made here that l in L2 follows from constrained momenta, or that
the coordinate Sobolev topology is the full physical norm. That pullback,
the order-minus-two density block, moving inverse/range, zero-speed/quartic
mixing and background time persistence remain in the same unfinished bundle.
