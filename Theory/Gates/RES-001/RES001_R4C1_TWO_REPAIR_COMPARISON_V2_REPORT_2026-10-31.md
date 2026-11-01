# First two-route repair comparison: both survive the bounded kinetic test

31 October 2026, Australia/Perth.
Result ID: R9-MT1-TWO-REPAIR-COMPARISON-V2.
Operator authorized comparison of both routes; neither is adopted as a canonical parent.
Claim Conditional; review DEFERRED; Rule9_cleared=false.
physics_pass=false; gate_effect=NONE.

## Outcome and physical meaning

Both explicitly defined candidates survive this first shared action-to-kinetic
test. This is a positive bounded result, not merely a label correction:

| Candidate | Actual change | Established here | Principal remaining requirement |
|---|---|---|---|
| F-tau | U is replaced by the normalized dust-clock gradient before variation, throughout the action | Seven remaining nonzero-mode kinetic amplitudes have a positive exact initial block on the common homogeneous control | Full coupled gradients/characteristics and physical evolution; independent frame twisting is no longer a configuration |
| R-tau | Independent U is retained; only the regulator uses the dust-clock spatial projector | Ten kinetic amplitudes remain positive on the registered small-tilt initial curve; Z is algebraic, with no time-velocity pairing | Full coupled characteristics/interactions and the changed clock/matter balance |

Both preserve the condensate/reservoir and T3 ingredients as declared fields
and topology. Neither identifies a microscopic matter residue or numerical
acceleration normalization. F-tau removes independent frame twisting by its
new variational definition; R-tau retains that freedom but assigns regulator
spatiality to the matter clock. That assignment is a new physical assumption.

The R-tau result specifically removes the auxiliary temporal pairing that
caused the tested old-action tilted kinetic obstruction. It does not prove
that every instability or principal-symbol problem has disappeared.

## Exact candidate definitions and source authority

The [candidate specification](RES001_R4C1_TWO_REPAIR_CANDIDATES_V1_2026-10-31.md)
and [shared frozen contract](RES001_R4C1_TWO_REPAIR_COMPARISON_V1_CONTRACT_2026-10-31.md)
own the equations and acceptance. S0 is the unchanged 25 September action.

Off shell define chi=sqrt(-grad(tau)^2)>0, t=-grad(tau)/chi and
p_t^{mu nu}=g^{mu nu}+t^mu*t^nu.

- F-tau is S0 with U=t substituted BEFORE variation; the identically zero
  unit multiplier term is removed. No new scalar field is added.
- R-tau is S0+integral sqrt(-g)*(L_reg[t]-L_reg[n]). Independent U and its
  unit multiplier, force and alignment sectors retain their original form.

The original action, failed domains and scientific hashes are not overwritten.
The implementation is explicitly a dust-clock ADM backend for these
covariantly defined candidates, not a solver for arbitrary gauges or a
complete metric/clock Hamiltonian analysis.

[Jacobson, arXiv:1001.4823v3](https://arxiv.org/abs/1001.4823v3)
is the primary construction/variation precedent for the hypersurface-normal
frame. [Langlois and Noui, arXiv:1510.06930v2](https://arxiv.org/abs/1510.06930v2)
motivate testing the full constraint structure of higher-derivative proposals.
Neither reference proves health for the present matter-coupled candidates;
no DHOST classification is claimed here.

## Clock equation and matter exchange really change

At fixed metric the exact normalized-gradient variation is

    delta t^mu = -p_t^{mu nu}*partial_nu(delta tau)/chi.

Let E_{t,mu} be the complete Euler derivative of the sector X that depends
on t, after its own integrations by parts. X includes all substituted
frame/force/alignment/regulator terms for F-tau, but only L_reg[t] for R-tau.
The induced bulk clock Euler term is

    F_X^nu = p_t^{mu nu}*E_{t,mu}/chi,
    E_tau,X = nabla_nu F_X^nu.

The dust contribution and total clock equation are therefore

    E_tau,m = nabla_mu(epsilon*C^2*nabla^mu tau),
    E_tau,m + E_tau,X = 0.

This is conservation of a combined clock-shift current. The old bare-dust
current cannot simply be declared separately conserved.

The off-shell matter Ward identity, including the multiplier Euler term,
is checked explicitly. On its multiplier equation and the total clock
equation, the matter-sector balance is

    nabla_mu T_m^{mu nu}
      = beta*T_m*nabla^nu psi - E_tau,X*nabla^nu tau.

For rho=epsilon*C^4>0, T_m^{mu nu}=rho*t^mu*t^nu and chi=C, this implies

    t.partial rho + rho*nabla.t
      = beta*rho*(t.partial psi) + chi*E_tau,X,
    a_t^nu = -beta*p_t^{nu mu}*partial_mu psi.

The new term changes the matter energy balance; it is parallel to t and
does not add an orthogonal force in this specified dust sector. This is
classical reversible action bookkeeping, not derived irreversible entropy
production or a microscopic particle-production mechanism.

A concrete R-tau flat-operator check gives
E_{t,z}=b*(Z*partial_z psi_dot-psi_dot*partial_z Z).
For psi=psi_bg(t)+amp*cos(k*z), Z=k^2*amp*cos(k*z), the induced clock Euler
term is b*psi_bg_dot*k^4*amp*cos(k*z), which need not vanish. This example
demonstrates the extra operator/current; flat space is not asserted to be
an admitted finite-density background.

Dimensions: [tau]=-1, [chi]=[t]=0, [E_t]=[F_X]=4, [E_tau,X]=5.
The additional matter-balance term has dimension five, as does nabla T.
[K_Q]=[Z]=2, [b]=0; Z^2, grad Z.grad psi and Z*a.grad psi each have dimension four.

## New reduction, not projection of the old evolution

The calculation starts from original physical-density contractions with
only the declared candidate substitutions. The multiplier/lapse constraints
are retained before the dust-clock reduction. All three spatial gauges and
shift equations are included for nonzero planar modes. The lapse equation
reconstructs epsilon: its coefficient on the clock constraint is
-sqrt(h)*C^4, nonzero on the declared regular patch.

In the clock gauge both candidate regulators are

    N*sqrt(h)*[b*Z^2/2-b*h^{ij}*D_i Z*D_j psi-b*Z*a_i*D^i psi].

Variation, including the acceleration term a_i=partial_i ln N, yields
Z=-D_i D^i psi. Omitting that term gives the wrong lapse-weighted operator.
There is no Z time velocity. The positive algebraic pivot at the initial
event is b=5/11; Z is eliminated by this equation, not deleted.

For F-tau the frame ADM term is checked independently from the four
original invariants:

    L_U = -M_U^2/2*[(c1+c3)*K_ij*K^ij+c2*K^2-(c1+c4)*a_i*a^i].

No independent spatial frame displacement/velocity is varied in this
candidate. A supplied finite independent tilt is explicitly rejected by
its parameterization, rather than silently projected out of old solutions.

## Background and initial kinetic results

Use the OLD homogeneous B1 control and coefficients, not the later eta=1/4
vortical B1-frame preparation. All coefficients are control inputs, not
microscopic matches.

The old homogeneous aligned solution is a common on-shell control:
for F-tau it lies in the substituted configuration class and restricted
variations preserve its stationarity; for R-tau both old/new regulator
terms and their first variations vanish there because Z=Delta psi=0.
The original background theorem is reused, not rerun or reinterpreted.

F-tau's fresh reduced kinetic matrix for
(gamma_xx,gamma_xy,gamma_yy,delta u,delta v,delta r,delta psi) has eigenvalues

    33/4, 1/4, 1/2, 1, 1, 1, 3.

Its minimum is 1/4 and determinant 99/32 in the registered amplitude units.
The three-shift derivative block is diag(1/2,1/2,-1/15); its negative shift
pivot is algebraic, not a propagating kinetic sign.

For R-tau retain V_y=w with |w|<=1/500, V_x=V_z=0 and initial physical tilt
derivative zero. Recomputing its original scalar/dust charges and lapse
recovers the declared charge-preserving H curve; all homogeneous metric,
frame and scalar accelerations remain available thereafter. Z=0 is its
regular homogeneous auxiliary solution.

Its thirteen-coordinate homogeneous temporal Hessian has determinant

    f(w)*11*(w^2-13)*(w^2+5)^2*(2*w^2+3)
          /[539136000*(1+w^2)],
    f(w)=3*(1+w^2)-(12/35)*abs(w)^3 > 0.

The determinant is nonzero throughout this small interval, including
alignment. The autonomous homogeneous Routh energy equals minus the unfixed
lapse equation; its on-shell conservation preserves the initial lapse
constraint. Spatial momentum constraints vanish by homogeneity; both
charges are checked. This supports pointwise local homogeneous admission,
not a uniform lifespan or nonlinear inhomogeneous Cauchy theorem.

The newly derived nonzero-mode R-tau ten-field kinetic matrix equals the
positive ten-field subblock of the pinned old diagnostic after actual
candidate-specific recomputation. The old B9 LDL and f(w) interval proof
therefore applies to this identical matrix. The old auxiliary cross
-b*w^2*psi_dot*Z_dot is absent. Its shift determinant is

    -(1+w^2)*(w^4+5*w^2+15)/900,

nonzero on the declared interval. Fourier shift elimination additionally
requires k!=0; k=0 is not covered by that reduction. The positive subblock
in the OLD eleven-field matrix did not cure its negative auxiliary pair:
the new candidate changes the action so that this pair is no longer a
time-velocity block.

## Verification, failed attempt and replay

- [Primary V2 executable](../../../Analysis/MasterTests/test_01_r4c1_two_repair_comparison_v2.py)
  and [candidate backend V2](../../../Analysis/MasterTests/r4c1_two_repair_actions_v2.py).
- [Primary V2 receipt](../../../Analysis/MasterTests/outputs/r4c1_two_repair_comparison_v2_attempt_01/summary.json):
  70/70, no failures/unknowns; SHA256
  964c24a88923a3326902eb8f5b37fa23a0f3ab6ee8964c60406e52211ea52f91.
- [Additional identity audit](../../../Analysis/MasterTests/audit_01_r4c1_two_repair_comparison_v1.py)
  and [receipt](../../../Analysis/MasterTests/outputs/r4c1_two_repair_additional_identities_v1_attempt_01/summary.json):
  18/18; SHA256
  826c9ab941991aa6a0760939febbd6c678aaafbddc684ecc3139e518e4e34107.
- Both full recomputing read-only replays are byte-identical, exit zero.
- R-tau's full physical derivative Hessian is independently differentiated
  at w=+/-0.001,+/-0.002 and 120 digits, with the original norm-cubed force
  retained. Normalized errors are at most 5.358e-38 and 5.358e-50 for complex
  steps 1e-20 and 1e-26; both satisfy the frozen 1e-35 requirement.
- Real centered physical-action differences at F-tau alignment respect the
  C2 cusp. The largest normalized discrepancies are below 5.142e-13 and
  5.142e-19 at steps 1e-10 and 1e-16, within the frozen 1000*step bounds.
- V1 returned 54/70 with machine-float contamination from integer background
  arrays; its backend/source/failed receipt are preserved. The
  [V2 addendum](RES001_R4C1_TWO_REPAIR_COMPARISON_V2_EXECUTION_ADDENDUM_2026-10-31.md)
  records exact/multiprecision input rebuilding. No equation or threshold was changed.
- The primary and audit verify 34 and 36 source pins respectively, preserving
  source/sidecar bytes and modification times. The fifteen older local
  exclusions also retain their original hashes.
- Differently assembled local identities, independent differentiation and
  replay are not external scientific peer review.

## Next comparison and unchanged holds

Carry BOTH candidates to their newly derived full coupled gradient and
characteristic problem on the justified common background, including
changed clock/matter equations, actual drift, metric/scalar/frame mixing
where present, and separate zero-mode treatment. Do not reuse old B/Q
matrices, old matter continuity or old propagator as a new-action result.

R-tau deserves particular attention because it retains the independent
frame while removing the tested auxiliary pairing, but there is no
physical winner yet. The choice of regulator foliation needs justification.
F-tau remains a live comparator with a larger configuration restriction.

No complete interacting physical domain, cutoff, GR/PPN recovery, microscopic
matching, C_chi/a0 or observational fit follows. G1-G6 and the original
unchanged-action objective remain incomplete; MAT-001 BLOCKED; K_Q
NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
Review DEFERRED; physics_pass=false; gate_effect=NONE. No canonical parent
adoption, manuscript/site edit, vault mutation, publication, commit/push
or model/provider/runtime change.

