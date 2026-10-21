# R4C1 nodes: undivided descriptor, moving-node tangent and norm obstruction

19 October 2026. Conditional unchanged-action Stage2 research.
Local704/704; complete fresh eight-worker read-only replay exact.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## What changed, and what did not

The original action admits an undivided force-clock variational formulation
at V=0. The scalar rate s is retained as an independent variable instead
of reconstructing it by division by V^2. The full coupled partial Legendre
block is now executable at exact profile nodes and neighboring points.
Metric/frame cross terms in the resulting two-form are essential.

Two new domain results matter for the next spectrum calculation:

- A moving node generally has a NONZERO variation of the momentum's normal
  derivative at its OLD coordinate location. Setting that derivative to zero
  would incorrectly remove node motion.
- The resulting two-form has no uniform bounded inverse on the unrestricted
  ordinary unweighted L2 field space. This rejects blindly applying its
  inverse as a uniformly controlled global first-order formulation. It does
  not exclude a constraint-completed mixed-order/weighted DAE formulation.

The physical coupled spectrum and validity window are NOT computed. This
does not remove the earlier negative patch momentum direction, prove node
persistence or overturn the joint H/U/Ud root. No replacement state, action
change, smoothing or extra C3 regularity gate is introduced.

## Undivided action, including all coupled response

Use the force-clock spatial gauge psi_i=0 and s=psi_hat>0 after the original
independent unit/dust variations. Write v=sqrt(det h), c=V^i h_ij V^j,
g=b*v*c. Keep the original twelve-velocity complement R and affine ell(s):

~~~text
E0(s)=v*[(P_y-ell(s))^T R^-1(P_y-ell(s))/2-f(s)]
Hpsi(s)=<(E0(s)+Edust+div F)/s>.
~~~

R remains the full metric/frame/Cartesian block. f retains the original
potential, Ricci, cusp, alignment and regulator. Dust and lapse flux are
the same as in the preceding planar report. Only R, not the singular
force/regulator block, is inverted where its regularity is established.

Before eliminating the scalar/regulator variables the canonical action
contains, in addition to the other canonical pairs,

~~~text
p_psi*psi_dot+p_Z*Z_dot
 -N*[E0(s)+p_psi*s+(p_Z+g*s)*Z_hat+Edust+div F].
~~~

Variation precedes the gauge pullback. With psi=tau, the p_psi row gives
N=1/s, and the Z_hat row gives p_Z=-g*s. The multiplier pair can be
eliminated because the constraint derivative with respect to p_Z is1,
INCLUDING when g=0. No inverse of g is required. The resulting action is

~~~text
Spsi=integral[Theta_other(Xdot)-g*s*Z_dot-Hpsi(s)] d_tau.
~~~

Use the existing full spatial/global constraint solution with p_Z=-g*s;
all three mean metric pairs, local phase/dust modes and both fixed global
charges remain. This derivation is not a new propagating-mode count.

The complete two-form is

~~~text
Omega=dTheta_other-g*ds wedge dZ-s*dg wedge dZ
delta g=b*v*[c*tr(h^-1 delta h)/2+V^T delta h V
             +2 delta V^T h V].
~~~

Deleting the metric/frame cross term s*dg wedge dZ fails the exact closure
test away from alignment. Keeping only the scalar/regulator2x2 block is
therefore not the coupled descriptor.

Its scalar-rate and regulator rows are

~~~text
-g*Z_dot-H_s=0
d_tau(g*s)-H_Z=0.
~~~

Other canonical momenta retain the additional term -s*g_q*Z_dot. Here H_s
and H_Z denote the COMPLETE functional derivatives, not frozen-gravity
partial-sector derivatives. Linearization about a valid background requires

~~~text
Omega_ij*delta Xdot^j
 +[(partial_k Omega_ij)*Xdot_background^j
   -Hessian(Hpsi)_ik]*delta X^k=0.
~~~

The background-drift term is not zeroed. This displays the required operator
structure, not an evaluated functional Hessian or computed frequency pencil.
The inherited regular-planar restore routine still rejects nodes; this
checkpoint supplies the undivided partial block and variational/descriptor
binding, NOT a completed global nodal evolution or spectral solver.

## Aligned rows and the moving-node tangent

At V=0, g=dg=0, but spatial frame derivatives need not vanish. The s row
reduces to the aligned energy compatibility

~~~text
H_s=-(Eother+Edust+div F+v*K_Q*s^2/2)/s^2=0,
P_psi=K_Q*s.
~~~

Eother is the partial energy with the aligned -v*K_Q*s^2/2 separated out.
The original regulator row is chi=Z+s*div V=0 in the force-clock gauge.
These are necessary auxiliary equations; they do NOT prescribe Z_dot=0.
Higher compatibility and actual lower-regularity persistence remain open.
This binds the new action to the earlier undivided regulator-node report
rather than repeating its187-check audit.

For initial h=I, s=p and V=(0,w(z),0), let w vanish simply with slope w'.
Differentiating p_Z=-b*v*c*s gives

~~~text
delta p_Z(node)=0
delta p_Zprime(node)=-2*b*p*wprime*delta V_y(node).
~~~

For a perturbation that moves the alignment surface,
delta z_node=-delta V_y/wprime and p_Zsecond=-2*b*p*wprime^2, hence

~~~text
delta p_Zprime+delta z_node*p_Zsecond=0.
~~~

The numerator's double-zero condition follows the ACTUAL surface, not a
fixed old coordinate location. Transverse delta V may instead lift the
alignment zero; the calculation explicitly retains that possibility. It
does not assume every perturbed solution has the same alignment worldsheet.
These are kinematic tangent identities, not proof that the nonlinear
equations admit all such variations as physical modes.

## Explicit unweighted inverse bound, with its precise limitation

On the registered simple-node profile w=+/-e*sin(k*x), h=I, choose the
L2-normalized C2 scalar-rate bump supported on |x|<=epsilon:

~~~text
delta s = sqrt(3003/(2048*epsilon))*(1-x^2/epsilon^2)^3.
~~~

It vanishes outside that support. The normalization integral is2048/3003;
the normalized fourth moment is1/85. Hold the other reduced coordinates
and momenta fixed. Its image under the full two-form is only g*delta s
in the Z row. Since |sin(k*x)|<=k*|x|,

~~~text
||Omega*delta s||_2 <= b*e^2*k^2*epsilon^2/sqrt(85) ->0,
||delta s||_2=1.
~~~

Thus a positive uniform lower bound, and hence a uniform bounded inverse
of Omega on this unrestricted unweighted space, is impossible. Any smooth
unit bump with that support also obeys the weaker b*e^2*k^2*epsilon^2 bound.
Shrinking smooth supports may avoid the node itself while approaching it.
Small perturbation amplitudes can preserve s>0; this does not remove the
linear operator's lack of a uniform lower bound.

IMPORTANT: these norm probes are NOT certified to satisfy the complete
auxiliary-node/tangency hierarchy. In particular the centered polynomial
bump need not satisfy the linearized H_s row when other momenta are fixed.
The result does not prove failure of every constraint-completed physical
tangent space, weighted norm, mixed-order reduction or finite-band EFT.
Nor is the epsilon bound a physical cutoff, growth rate or observed scale.
Defining and validating that admissible physical space is still required.
Pointwise grid rank is not converted into a global mode count.

## Verification, preserved failure and reproducibility

All9 registered parameter cases use exact nodes and signed nearby angles
0,+/-1e-2,+/-1e-6 in both slope orientations:90 local controls. Nontrivial
coupled velocities and local curvature/lapse-flux controls are retained.
They are ORIGINAL-DENSITY METHOD CONTROLS, not newly adopted/evolved global
backgrounds or a stronger certified density floor for the registered state.

The new numerical partial block is copied from the pinned canonical full
block with explicit s replacing the divided inverse, no p_psi*s in E0,
and exact Y=c*s^2 in this gauge. Complex scalar-rate probes preserve their
dtype. No epsilon inverse or deleted cusp is used. Original100-digit
momenta, full Legendre energy and all144 nodal complement entries from
independent quadratic polarization check the block. The pointwise cusp is
used only through its valid C2 structure, not an ordinary cubic tensor.

| Control across all cases | Result |
| --- | --- |
| Original-density partial Legendre discrepancy | <1.247e-16 |
| Undivided clock-row binary64 discrepancy | <1.424e-16 |
| Nodal complement polarization discrepancy | <3.358e-18 |
| High-precision momentum/descriptor identities | <=1e-45 |
| Binary64 comparison requirement | <=1e-8 |
| Largest b*e^2*k^2/sqrt(85), reference chart | <7.889e-5 |

Independent100-digit bump quadratures at epsilon*k=1e-2,1e-3 satisfy the
explicit bound for every family/eta. The proof of nonuniform inversion is
the inequality above, not extrapolation of those two samples.

V1/attempt01 remains FAILED65/74: all9 cases stopped at a missing tensor_h
binding. V2 adds only tensor_h=canonical.tensor_h and HM=canonical.HM plus
source/failure/addendum pins. ALL function ASTs are identical. The failed
and successful formulas.json files are BYTE-IDENTICAL. V1 source, sidecar
and all6 receipts are preserved; no failure or scientific hash was rewritten.

V2 completed704/704. A complete fresh eight-worker replay reproduces all
three scientific payloads and three sidecars, including sizes/mtimes.
All77 source pins/154 metadata records remain unchanged. A separate
198-record guard also covers earlier successes, preserved failures and
new receipts. These repeated method checks are not704 physics discoveries.

| Artifact | SHA-256 |
| --- | --- |
| V1 contract | 1cd091d3f41e51e5face8bead912c765124cc54a8eb75f37968c18ae6bdb7e2b |
| V1 executable, preserved failure | 86b1c665d2130fd48fb75fbb6b5aa4fe5ee7518dbd2a1a5b3e7c34646573343f |
| V2 binding addendum | 8ad10bc9ef42496713d66d82b625922249327c0563cee1f2ab4dbf3cc92b6b83 |
| V2 executable | b19f4ce9a665d711b3be021cfa149fe3b4753851e1c11d99bc705156537f8bf5 |
| Attempt02 summary.json | 96b64865c5e94490ab6bfaedd5def0668d0c30c071b84935b2835c61f609a4c2 |
| formulas.json, V1 and V2 | 280ee1834ef44e3428990563baa98951a2c43a147b5464dc2b04c8b66fafcfd2 |
| independent.json | 559d3d05ebe68f755f38a85225f15b7676036f23348655e0211743d70b286fef |

Executable: Analysis/MasterTests/test_01_r4c1_nodal_descriptor_v2.py.
Receipts: Analysis/MasterTests/outputs/r4c1_nodal_descriptor_attempt_02/.
Use existing itsm_env Python, --workers 16 and a NEW --output, or --replay
pointing to attempt02. Runtime/failure journals remain private and ignored.

## Next work and unchanged parent holds

Integrate this undivided block into the full global constrained functional,
define its mixed-order/weighted admissible tangent space and auxiliary-node
conditions, then compute the complete coupled descriptor Hessian/drift and
spectrum there. Do not invert Omega on the rejected unrestricted L2 domain,
skip nodes, impose fixed-node jets or project out negative directions to
manufacture a physical window. Full nonlinear admission/persistence,
arbitrary3D closure, interaction/error bounds, healthy GR and physical
cutoff/frequency evidence remain substantive. No identifying matter-residue
or nonlinear-force matching input has appeared.

R9-MT1-NODAL-DESCRIPTOR-V2: DEFERRED, not cleared; inherit PLANAR-REDUCED-
HAMILTONIAN-V1, REGULATOR-NODE-V1, joint/node/regularity/canonical and
transitive review debt. Memory chunk chk_4227d4c03f610c91d2cb3fc7 located the
earlier node report; the live source and action govern this result.

Stage1 registered linear prepared-dust scope only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
No state adoption/evolution, vault-management write, manuscript/PDF/site,
publication, commit/push, action/provider/model/global-runtime change.
