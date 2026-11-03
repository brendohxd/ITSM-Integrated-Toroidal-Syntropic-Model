# Retained ordinary/quartic principal assembly V1

4 November 2026. Continue the acknowledged-High coupled-energy bundle after
the actual ordinary Ward-energy V4 result. This is an INITIAL PRINCIPAL
ASSEMBLY, not acceptance of the full variable-coefficient energy contract.
Preserve the action, all original pins, old failures and sidecars. Reuse
the exported Hessian and its spatial derivative; do not rerun a Hessian.

Use the 18 ordinary directions and physical force pair (Z,xi=delta pi_psi).
Retain the metric part Z=kappa*k^2*chi-i*kappa*k*s*u, with
u=(delta hxx+delta hyy)/(2a^2), rather than setting Z=kappa*k^2*chi.
The leading strong graph has u=i*c*P_Vz/(a^2*k), c=gamma/a (MP2=1).
Density w includes both completed fast-gradient corrections; no density
gradient remains in its principal row by the existing full source bound.

Let m=L_vpsi,vpsi, aphi=1/m, kappa=a^-2, d=b*N*mu*kappa and
vphi=(L_vpsi,psiz+S*m)/m. Prove the force pair's leading and first spatial
coefficient rows directly from the canonical current and secondary equation:

    A2_fast=[[0,kappa*aphi],[-d,0]],
    A1_fast=i*[[-vphi,-(2*kappa*aphi_z+kappa*lambda_z*aphi)],
               [d_z-beta*d*s,-vphi]].

Here A(k)=k^2*A2+k*A1; gradients in A1_fast must NOT be omitted. With
Hfast=diag(d/kappa,aphi), prove pointwise Hfast*A2 is skew and the formal
first-derivative energy cancellation

    2*(Hfast*A2)_z+Hfast*B1-B1^T*Hfast=0,
    B1=A1_fast/i,

using d_z=d*(lambda_z-beta*s), not constant coefficients. Keep all
remaining order-zero/time/gauge terms explicitly outside this component.

Derive both ordinary<-force and force<-ordinary order-k blocks. The first
has momentum rows i*A_q*Z, with A_q=L_qslow,Zz and the exact initial metric
identity A_hxx=A_hyy=-d*s/(2a^2); other ordinary entries vanish. Retain all
canonical ordinary momentum rows. The second has the leading Z row

    -kappa*aphi*Tq*X -i*kappa*s*delta(Sz_z)
    -i*kappa*s*t*v/a^2 +i*vphi*(kappa*s*c/a^2)*P_Vz,

and zero xi row at order k. Here Tq=L_vpsi,qslow, v=M^-1(P-i*Brel*X),
t*v=(v_hxx+v_hyy)/2, and delta(Sz_z) is obtained from the FULL principal
shift-gradient Schur response, including all ordinary velocities and
gradients. In material velocities its gradient block is
Dshift_rel=Dshift+S*Cshift; retain this advection conversion as well.
Derive these terms from the local clock Legendre equation,
secondary metric variation and canonical force current. Do not guess a
coupling from the old homogeneous control. Check exact consistency of all
claimed zero columns against the full exported Hessian and current owners.

Assemble all 20 directions, k^2*D+k*B with D=diag(0,A2_fast). Denote the
two order-k cross blocks by Bof,Bfo. Construct the same-strength asymptotic
change T=I+S1/k, retaining BOTH pairs, with

    S1_of=-Bof*A2_fast^-1, S1_fo=A2_fast^-1*Bfo.

Prove B+[S1,D]=Bdiag and the exact FROZEN remainder

    T*(k^2*D+k*B)*T^-1
       =k^2*D+k*Bdiag+(S1*B-Bdiag*S1)*T^-1.

Give whole-root bounds for S1, a sufficient signed-|k| invertibility
threshold, and the frozen remainder. This mathematical high-frequency
threshold is NOT a physical cutoff or an observational/interaction window.
No low mode or generated tail is discarded; those remain for the full
operator calculation. Pointwise symbol equivalence does not prove global
Fourier decoupling when coefficients vary.

Use the actual ordinary-energy equivalence constants and positive force
weights to bound the full transformed principal norm. A principal-symbol
calculation does not bound the variable-coefficient composition remainder:
retain S1_z, coefficient gradients, T_dot, the moving constraint/Green/range
map and all global harmonic/charge partners for the next owning task.
Provide explicit independent symbolic block/metric/energy controls, outward
coefficient bounds, a fresh receipt and immutable replay. If the rows cannot
be justified or a bound is inconclusive, preserve that precise obstruction.

Review DEFERRED; physics_pass=false; gate_effect=NONE; R-tau unadopted;
G1-G6 incomplete. No new action, matching input, vault mutation/sync,
provider dispatch, publication, commit, push or deployment.
