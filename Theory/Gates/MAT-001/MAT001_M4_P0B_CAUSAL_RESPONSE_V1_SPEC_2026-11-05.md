# M4 P0-B causal metric response V1

5 November 2026. High explicitly retained for this derivation. Use the actual
source/kernel export and frozen P0-B background parameters, not a new parent.

Derive the canonical first-order response for z=(x,p), with
p=a^3(K dot x+D x+s_v). Retain volume/time factors and all derivative sources.
Eliminate constraints with the actual matter source, reconstruct alpha and
beta=-Sigma/q^2, and derive Bardeen potentials Phi=alpha+dot beta and
Psi=-R-H beta in the frozen E=0 spatial gauge. Include local source/contact
pieces and derivatives of source in the reconstructed metric response.

State retarded data, the Green-function jump, field-chart covariance and source
conservation. Do not infer stationary poles from an evolving matrix. The
calculation concerns nonzero scalar harmonics; the homogeneous and harmonic
vector sectors retain their separate exported constraints and charge conditions.

Run a reproducible, conditional numerical response control on t in [0,0.5],
comoving k=1 and 4 on a coordinate 2pi torus, M_P=1, m^2=1, lambda4=0.50,
lambda6=0.20, Lambda=2, a=rho=1, rho_dot=0 initially and the frozen finite
charge/expanding initial H. No parameter is chosen from observations.
Use external isotropic pressure p_m=10^-6 sin^4(pi*t/0.5), tau=3p_m.
Integrate its energy/momentum Ward equations from delta_e=j=0 alongside the
linear response; this signed probe is not a positive-density astrophysical model.

Compare canonical DOP853 at rtol=10^-8/10^-10 (atol=10^-11/10^-13), and a
separately assembled second-order Euler RK45 response at the tighter tolerances.
Use relative trajectory error <=10^-5 against scale max(10^-6,peak tight
trajectory). Check metric reconstruction similarly with analytic coefficient
derivatives; no noisy finite-difference substitute. Track all solver success,
background constraint residuals, source conservation, chart/source algebra and
nonstationarity. Numerical agreement is not a validated continuum error bound.
For this homogeneous background and isotropic probe, independently check the
traceless spatial metric equation Phi=Psi to the same scaled 10^-5 tolerance:
the condensate and J(a^2) have no linear spatial traceless stress at a=0.

Acceptance: actual causal source-to-metric response construction, reproducible
controls and an explicit pole/residue disposition. Full M4 closure requires
a justified physical pole/regime or a scoped obstruction, not merely this
control. Preserve all old sources/failures; fresh executable/receipts and replay.
No observational fit, new physical scale, native-goal change, provider dispatch,
vault mutation, publication or Git delivery. Rule-9 DEFERRED; physics_pass=false.
