# Strong-density ordinary principal graph: reference energy and prepared enclosure

4 November 2026. Conditional component of the
[actual prepared coupled-energy contract](RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md).
R-tau remains an unadopted comparator; unchanged R4C1, all earlier failures
and original G1-G6 requirements are preserved. Review DEFERRED;
physics_pass=false; gate_effect=NONE.

## Result and precise limits

The strong-density ordinary chart retains 18 directions: corrected density,
eight independent gradient-scaled configurations and nine canonical momenta.
At the pinned rational action-coefficient reference its two zero-speed
directions are semisimple. An explicit polynomial-projector principal energy
is positive and cancels the reference generator exactly, with momentum-
independent bounds

    (1/5)*|Y|^2 <= E_reference(Y)
        <= (475671803/1981980)*|Y|^2 < 240*|Y|^2.

This is an EXACT OFF-SHELL COEFFICIENT CONTROL, not a new background solution,
an actual prepared-background energy theorem or positivity of the entire
canonical Hamiltonian. It does not override the earlier adverse result for
the density-only H^-1 weakening.

The whole prepared root is carried into a rigorously enclosed CANDIDATE
ordinary operator using the immutable action Hessian and certified shift
inverse. The reference-normalized temporal inverse contraction is below
0.094789435. No Hessian was rerun and no midpoint inverse was substituted.

Its trace-kinematic defect enclosure contains zero in every component, but
the enclosure's row norm bound is only below 0.725836. This is uncertainty
in a necessary consistency test: it is neither a measured nonzero defect
nor proof of the required exact identity. The actual graph identity and
uniform prepared symmetrizer remain OPEN. A finite interval enclosure of a
generator does not by itself control its momentum-growing symmetric part.

## Construction

Use slow slots (hxx,hxy,hyy,Vx,Vy,Vz,u,v,r). From the original full mixed
Hessian, eliminate only the principal shift-gradient block K:

    M=L_vv-L_vSz*K^-1*L_Szv,
    B=L_vd-L_vSz*K^-1*L_Szd,
    G=L_dd-L_dSz*K^-1*L_Szd.

Canonical momenta are retained. Remove common background advection S by

    Brel=B+S*M,
    Grel=G+S*(B+B^T)+S^2*M.

At the conformal initial metric h=a^2 I, the leading compensated density
constraint suggests the trace lift

    X=k*delta qordinary=E*Q+i*(gamma/a)*vtrace*P_Vz,

where vtrace=(1,0,1,0,0,0,0,0,0). E inserts half the transverse diagonal
difference, hxy, the three frame variables and three ordinary scalar fields;
R*E=I8. All nine P components remain independent at the local principal
level. The candidate material-frame rows are

    v=M^-1*(P-i*Brel*X),
    Pdot/k=-i*Brel^T*v+Grel*X,
    Qdot/k=R*v,
    wdot/k=0.

The last row uses the completed initial strong-density source estimate,
not a frozen T_dot=0 assumption. Its full bounded source is retained in
that owner. The further necessary trace-kinematic identity is

    (v_hxx+v_hyy)/2=i*(gamma/a)*(Pdot/k)_Vz.

It is exact at the rational reference. Its extension to actual prepared
coefficients needs an exact action/constraint identity, not a decision to
set the enclosed residual to zero. The whole candidate matrix and complex
defect intervals are exported for that follow-up.

## Exact reference energy, without sampled eigenvector fitting

For the reference 18-by-18 generator A, exact rational algebra gives

    det(c I-A)=c^2*(c^2+1)^4*(c^2+1/3)
                    *(c^2+4/5)^2*(c^2+14/13),
    A*(A^2+I/3)*(A^2+4I/5)*(A^2+I)*(A^2+14I/13)=0.

Both ker A and ker A^2 have dimension two. One direction is density;
the other is retained, not quotiented out. In the receipt's state order,
the latter can be represented by k*delta Vz=-2i, P_hxx=P_hyy=1 and all
other entries zero. This is a principal algebraic direction, not a proposed
finite-amplitude perturbation or an automatically admitted global tangent.

Let lambda range over {0,1/3,4/5,1,14/13} and define

    P_lambda=product_{mu != lambda}(A^2+mu I)/(mu-lambda).

The executable verifies exact idempotency, sum P_lambda=I, A*P_0=0 and
(A^2+lambda I)*P_lambda=0 for lambda>0. With fixed unit canonical-coordinate
norms, use

    E(Y)=sum_lambda |P_lambda Y|^2
          +sum_{lambda>0} |A*P_lambda Y|^2/lambda.

No numerical eigenvectors or fitted weights enter. The projector resolution
and Cauchy inequality prove the 1/5 lower bound; the exact trace of the
positive energy form gives the stated upper bound. Direct rational matrix
multiplication independently verifies A^*H+H*A=0. The reference scope is
essential: no prepared-background cancellation follows by perturbing this
identity without deriving its corresponding variable energy.

## Whole-root inverse and retained missing sectors

Whiten the raw temporal block and shift cross block BEFORE Schur
subtraction, using the existing exact reference congruence W. If

    E_M=W^T*M*W-I,

the outward infinity-norm bound is below 0.094789435. Sum 24 terms of the
alternating Neumann series, enclose the remainder by
delta^25/(1-delta), and transform back. The product enclosure contains I.
All action-Hessian uncertainty and original root uncertainty remain included.
Profile evaluation supplies a,gamma,S without evaluating a new action Hessian.

The quartic pair is retained separately: 18 ordinary plus 2 force directions
gives the existing nonzero-mode count 20. Counting is not its energy proof.
The force observable still contains

    delta Z=kappa*k^2*chi-i*kappa*k*s*u

at the leading initial trace orders; deleting its metric-gradient term is
rejected. Slow/fast mixing, the full symplectic cross blocks, global
mean/modulus/harmonic partners, charges and periodic range remain mandatory.
None is eliminated by this ordinary-only component.

## Verification, preservation and next calculation

[Frozen executable criteria](RES001_RTAU_ORDINARY_STRONG_GRAPH_V1_SPEC_2026-11-04.md),
executable `Analysis/MasterTests/test_rtau_ordinary_strong_graph_v1.py`,
receipt `Analysis/MasterTests/outputs/rtau_ordinary_strong_graph_v1_20261104/receipt.json`.
32/32 bounded controls passed and immutable replay was byte-identical.
Receipt SHA256:

    cd1963d8f69c62f32101195dcbc7c3e2a51e8da3e9a8b0ba81760dab503ba910

All 219 original pins, inherited sources, sidecar bytes and timestamps were
preserved. This check count does not clear physics or independent review.

NEXT: derive the actual prepared leading graph/ordinary operator identities
from the complete action and constraint/current equations. Verify that the
leading amplitudes used by that argument admit the registered global range
and charge completion. Then construct or reject its actual uniform energy,
compose the quartic pair and retain T_dot, G_dot, coefficient/gauge/range
drift and the full remainder. Only after that may an actual background tube
and finite-time result be claimed. The reference energy is useful input,
not acceptance of the owning coupled-energy contract.

The domain-first goal remains ACTIVE. Full coupled energy, actual time tube,
interactions/window and genuinely identifying matching remain incomplete.
No action adoption, vault mutation/sync, provider dispatch, publication,
commit, push or deployment occurred in this calculation.
