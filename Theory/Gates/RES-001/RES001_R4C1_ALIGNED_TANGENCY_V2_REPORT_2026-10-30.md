# Dust alignment is not an invariant unrestricted perturbation domain

30 October 2026. Result ID: R9-MT1-ALIGNED-TANGENCY-V2.
Owner: domain-first goal M1-M3, necessary domain diagnostic.
Claim: Conditional. Review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE.

## Finding

The full old-B1 coupled linear equations do not preserve initially exact dust-normal alignment for arbitrary constraint-reconstructed nonzero-mode perturbations. An especially simple witness has only a spatially varying initial force-field velocity. Its initial frame displacement and velocity vanish, but its longitudinal frame acceleration is nonzero.

This rejects the unrestricted aligned LINEAR perturbation class containing that seed. It also obstructs a smooth invariant nonlinear aligned domain IF its admitted tangent includes the seed. Nonlinear initial-data completion for the seed is not established here; this is not a theorem excluding every narrower aligned sector, every slicing, or the full action.

The old aligned homogeneous solution and its certified full linear propagator remain unchanged. Its propagator already retained frame perturbations: the new result does not contradict that certificate. It shows why freezing those perturbations to maintain exact alignment would change the coupled problem.

## Scope and identification

Use the admitted old homogeneous B1 background and original coefficients, not the later eta=1/4 vortical B1-frame preparation. Work at a>0 with real nonzero comoving k along z, positive background dust, the existing dust-clock gauge and all original nonzero-mode reductions.

The ADM decomposition is n=gamma*n_ADM+V with gamma=sqrt(1+h(V,V)). In the clock gauge the future dust velocity is n_ADM. At alignment delta gamma=0 and the physical frame amplitude is f=a*delta V. Consequently f=0 is the first-order dust-normal alignment condition, regardless of the reconstructed coordinate shift.

The existing M,B,Q and their actual background derivatives give

    M*qdd + (M_dot+B-B^dagger)*qdot + (B_dot-Q)*q = 0.

All metric/frame/canonical scalar/force fields are retained before testing the alignment restriction. Auxiliary Z and all three shifts are solved, not suppressed; lapse and density use the original clock and lapse equations including flux.

## Explicit necessary compatibility equation

Let sigma=delta psi, Gamma=gamma_xx+gamma_yy, p=psi_dot, and let u,v,r denote the homogeneous Cartesian condensate and reservoir fields. With f=f_dot=0, transverse frame accelerations vanish automatically. The longitudinal equation is

    f_z_ddot = -(i*k/a) * C_align,

where, in the registered old-B1 control units,

    C_align =
        3*Gamma_dot
        + 6*(u_dot*delta u + v_dot*delta v + r_dot*delta r)
        + (6/13)*(u*v_dot-v*u_dot)*(u*delta v-v*delta u)
        + (22/5)*H*sigma - (2/5)*sigma_dot
        + (30/11)*p*(k^2/a^2)*sigma.

Exact initial alignment therefore requires C_align=0 as a further necessary condition if it is to persist. The initial compatibility row has rank one on the fourteen-dimensional space left after imposing the six frame-position/velocity conditions. This is a tangent condition, not a proof that its kernel is dynamically preserved.

Dimensions are inherited from the action: [f]=[sigma]=[Gamma]=0, [k/a]=[H]=[p]=1, [u]=[v]=[r]=1. The numerical coefficients 6, 6/13 and 30/11 represent respectively 1/mu, zeta/mu and b/mu in the old control units, with mu=M_U^2*(c1+c4)=1/6 in those units. Their pre-unit-choice dimensions are -2, -4 and -2. Thus C_align has dimension one and f_z_ddot dimension two. No physical mass scale, SI normalization or acceleration coefficient is identified.

At the registered initial event a=1, H=sqrt(3469/4620), (u,v,r)=(1,0,1), (u_dot,v_dot,r_dot)=(0,1,1/4), p=1/5, this reduces to

    C_align =
        3*Gamma_dot + (84/13)*delta v + (3/2)*delta r
        + [(22/5)*H+(6/11)*k^2]*sigma - (2/5)*sigma_dot.

## Simple constraint-reconstructed witness

For one real torus wave, initially choose sigma_dot=epsilon*cos(k*z), all reduced field displacements zero and all other reduced velocities zero. Here epsilon labels an infinitesimal perturbation amplitude, not the dust multiplier.

The reconstructed linear initial quantities are

    delta Z = Sx = Sy = Sz = delta N = 0,
    delta rho = delta epsilon_dust = -(3/5)*epsilon*cos(k*z).

The exact complex-mode frame acceleration is (0,0,2*i*k/5) per unit sigma_dot. In the stated real cosine/sine convention this is

    f_z_ddot = -(2/5)*k*epsilon*sin(k*z).

Thus the frame is initially aligned and stationary relative to the clock normal but immediately has a nonzero relative acceleration. The reduced linear constraints have been reconstructed; the state is not produced by deleting metric or matter equations. Strictly positive background density means sufficiently small finite-mode LINEAR perturbations do not force negative reconstructed linear density; this statement is not finite-amplitude nonlinear admission.

Both the seed and this response have zero spatial mean at linear order. Fixing a homogeneous frame harmonic alone therefore does not impose pointwise alignment. No claim is made about nonlinear fixed-harmonic constraint completion or preservation.

The fourteen probes also find initial departures for force displacement, condensate phase displacement, reservoir displacement and metric-trace velocity. Amplitude-only and tensor probes can satisfy this first tangent test. Passing it supplies no finite-time invariant sector or nonlinear stability certificate.

## Verification and preserved failure

- Frozen [V1 contract](RES001_R4C1_ALIGNED_TANGENCY_V1_CONTRACT_2026-10-30.md).
- [V1 executable](../../../Analysis/MasterTests/test_01_r4c1_aligned_tangency_v1.py) and failed receipt are preserved: 68/71. Three independent-control comparisons retained symbolic H on one side while evaluating the other at the registered initial H.
- [V2 execution addendum](RES001_R4C1_ALIGNED_TANGENCY_V2_EXECUTION_ADDENDUM_2026-10-30.md) records the repair. No equations, probes, parameters or acceptance thresholds changed.
- [V2 executable](../../../Analysis/MasterTests/test_01_r4c1_aligned_tangency_v2.py).
- [V2 receipt](../../../Analysis/MasterTests/outputs/r4c1_aligned_tangency_v2_attempt_01/summary.json): 71/71, zero failed/unknown checks.
- V2 receipt SHA256: 836f9e718212d689a86cad0eec22657bdce293b5fb422e693c7abcb43545dc9c.
- Full recomputing read-only replay is byte-identical, exit zero.
- Twenty-three source pins and their sidecars are checked inside V2. An additional baseline verification retained all thirty-four initially snapshotted files and native modification times before documentation append.
- The complete initial generator is recovered exactly; independent reconstruction from the original local second variation recovers M,B,Q and all eliminated constraint rows at the same initial event.
- Numerical differentiation of the general M/B coefficient functions along the actual background tangent, assembled through the full Euler equations, agrees at k=1,7,40. Steps 1e-14 and 1e-22 give normalized errors at most 2.991e-29 and 2.991e-45 respectively. These are numerical controls, not rigorous evolved-error estimates.
- Exact real cosine/sine and complex Fourier calculations agree. Wrong Fourier sign, discarded force response and omitted actual drift are rejected.
- Same-author algebra/replay and a differently assembled numerical control are not independent scientific peer review.

## Next supported work and unchanged boundaries

M1's contract and preservation work is complete in scope. This supplies a necessary M2/M3 rejection for the unrestricted aligned perturbation class. It does not complete the search for a justified nontrivial physical domain.

A narrower candidate must preserve its additional compatibility equations under the actual time-dependent constrained dynamics. A mere kernel of the initial row or powers of a frozen generator are insufficient. The next bounded question can test preservation of this explicitly derived restriction, while retaining coupled force/matter modes; stop before launching an indefinite derivative hierarchy if new physical input is required.

The vortical G1 principal, Frobenius, forced-tail, weak-interface and concentration obstructions remain separately scoped and unchanged. No alternative family, parent, quantum-ghost interpretation, cutoff or physical branch exclusion is adopted.

G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED. Physical-domain admission, interacting window and identifying matching remain open. No manuscript/PDF/site, vault mutation, commit/push, model/provider dispatch or publication.

