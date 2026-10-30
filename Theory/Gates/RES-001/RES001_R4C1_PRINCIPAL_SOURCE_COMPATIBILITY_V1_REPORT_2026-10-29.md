# Retained auxiliary branch: exact source compatibility, not yet nonlinear admission

29 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Finding and scientific consequence

The full constrained principal operator has a defective double
characteristic at each c=+/-i/w in the registered nonzero-tilt range. A source
can have ZERO direct left-kernel overlap and still generate a simple pole in
the retained auxiliary response through the other coupled fields. Thus a
direct projection test alone cannot establish a safe prepared domain.

The required cancellation is now explicit. This is an algebraic transfer map
and a necessary source-compatibility test. The ACTUAL nonlinear cusp source
has not been transported through that map. No prepared weak domain, controlled
interval, physical spectrum, cutoff or all-solution exclusion is established.

## 1. Full nine-field reduction at the retained branch

Reuse the [exported original-action constrained pencil](RES001_R4C1_CONSTRAINED_PRINCIPAL_V1_REPORT_2026-10-28.md)
without recomputing or specializing a different action. Order the retained
variables as y=(hxx,hxy,hyy,Vx,Vy,Vz,u,v,r), followed by psi,Z. Write

    P(c) = [ B(c)  d(c)    0   ]
           [ d(c)^T a(c)  -r(c)]
           [   0   -r(c)   0   ],
    r(c)=b*(1+w^2*c^2), b=5/44,
    c_s=s*i/w, s=+1 or -1.

Here B is the nine-field block of the constrained PRINCIPAL PENCIL, not the
earlier 12-field time-mass complement, and Zbar denotes its background Z.
Transpose is the complex bilinear transpose in this polynomial problem;
it is not a Hermitian inner product or a physical positive norm.

An algebraic congruence D with D_Vz=i/sqrt(1+w^2), other entries one, reduces
the complex-frequency block to rational subblocks. It does not redefine the
physical fields. The (hxx,hyy,Vy,Vz) four-block determinant is

    -205/[256*w^8*(w^4+5*w^2+60)].

The (hxy,Vx) two-block determinant is (1+w^2)^2/(48*w^4); the remaining
three diagonal entries are each -(1+w^2)/w^2. Reversing the congruence gives

    det B(c_s)=-205*(1+w^2)^6/[12288*w^18*(w^4+5*w^2+60)].

Thus this nine-field block is invertible for every real w!=0, independently
of finite real Zbar. No inverse or continuation through w=0 is asserted.

Keeping ALL its metric, frame, condensate and radion responses, define
x_s=B(c_s)^(-1)*d(c_s). Exact cancellation gives

    x_s=(0,0,0,0, -30*Zbar*w/11,
         -s*i*w*(1200*Zbar+11*w^2+11)/(440*sqrt(1+w^2)), 0,0,0)^T.

The zero metric entries are derived cancellations after the coupled solve;
they are not an omitted metric sector. The remaining scalar Schur entry is

    a_eff(c_s)=a-d^T*B^(-1)*d
             =3*(w^2*abs(w)-140*w^2-140)/(560*w^2),
    a_eff+3/(4*w^2)=3*(abs(w)-140)/560.

Consequently a_eff < -3/(4*w^2) < 0 for the registered
0<abs(w)<=1/500, with any finite real Zbar. The physical cubic Hessian remains
present through abs(w); A has not been removed. This sign is a value at a
complex principal frequency, not a physical ghost or mode-norm verdict.

## 2. Double characteristic and generalized chain

Because det(P)=-r^2*det(B), r has a simple zero at c_s, and both det(B)
and a_eff are nonzero there, the characteristic has exactly multiplicity two
and kernel span(e_Z). The time-mass matrix is nonsingular for nonzero w in
the registered range by the parent exact determinant identity. Hence the
22-dimensional frequency companion has a nonsemisimple length-two chain.

Explicitly, choose the configuration part q1 by

    q1_psi=r'(c_s)/a_eff, q1_y=-x_s*q1_psi, q1_Z=0.

The ENTIRE pencil satisfies P(c_s)*q1=-P'(c_s)*e_Z exactly. Thus
(e_Z,c_s*e_Z) and (q1,c_s*q1+e_Z) form the companion chain. For
P=M*c^2+C*c+G, its left eigenvector can be written

    ell=(e_Z^T*(C+c_s*M), e_Z^T*M).

For a companion forcing (0,M^(-1)*F), ell pairs to F_Z. Its zero pairing
with a source therefore tests only the leading left-eigenvector condition;
it does not check the generalized response.

## 3. Exact inhomogeneous response and cancellation condition

For F=(F9,Fpsi,FZ), wherever B and r are invertible, set
H=d^T*B^(-1)*F9 and a_eff=a-d^T*B^(-1)*d. The full solution is

    psi=-FZ/r,
    y=B^(-1)*F9+B^(-1)*d*FZ/r,
    Z=(H-Fpsi)/r-a_eff*FZ/r^2.

This is an exact block identity for the full pencil. If FZ is IDENTICALLY zero
near c_s, a regular response additionally requires

    Fpsi(c_s)=x_s^T*F9(c_s).

For analytic sources this removes the indicated simple pole at the isolated
branch while B remains invertible. It does not prove boundedness uniformly
in w, domain invariance or time evolution. If FZ merely vanishes AT c_s,
its frequency derivatives can still contribute through FZ/r^2; the displayed
homogeneous-auxiliary cancellation must not be used as a sufficient condition
in that different case. General nonzero FZ can produce the double pole.

A synthetic unit Vz source with Fpsi=FZ=0 has zero direct overlap but
nonzero simple-pole numerator at the registered signed probe points. The
unit FZ control instead produces the double pole. They verify the operator
map; neither is presented as a physical nonlinear cusp forcing.

## 4. What is still needed for the actual cusp and weak domain

The [finite-band finding](RES001_R4C1_FINITE_BAND_DOMAIN_V1_REPORT_2026-10-29.md)
establishes a nonsmooth actual initial Vy acceleration. Its coexistence with
a complex principal characteristic does NOT by itself prove excitation of
that characteristic in the full variable-coefficient evolution. In particular:

1. Export the actual nonlinear Euler source and its retained scalar and
   auxiliary components after the clock/lapse/density and spatial gauge
   reductions. Retain inhomogeneous shift-source Schur terms, moving bases,
   coefficient drift, means and interface distributions. Do not insert a
   complement acceleration vector as if it were that reduced source covector.
2. Its Fourier tail is generated at the alignment nodes. The present inverse
   is for w!=0 and changes rank at the nodes, so substituting a frozen tilt
   into a global tail calculation is not a justified projection. Establish
   a variable-coefficient mixed/weighted nodal domain and trace/constraint
   conditions before applying or extending this compatibility map there.
3. If the resulting admissible source satisfies a cancellation, prove that
   the ORIGINAL evolution preserves it with controlled estimates. Do not
   impose the condition by continual projection, remove the branch, or turn
   it into an unapproved new physical prescription.

These are substantive mathematical/physical requirements, not Rule-9 debt.
This calculation supplies no new microscopic matching information, no
independent scale, and no numerical a0/C_chi prediction. Earlier bounded dust
and initial-jet results remain unchanged. No action/state/parent change or
automatic TOP-X4 pivot follows.

## 5. Reproducibility and preservation

Contract: RES001_R4C1_PRINCIPAL_SOURCE_COMPATIBILITY_V1_CONTRACT_2026-10-29.md.
Executable: Analysis/MasterTests/test_01_r4c1_principal_source_compatibility_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_principal_source_compatibility_v1_attempt_01/summary.json.
Receipt SHA256: 7ff7adb23c832dc7bc801ad8dc4c4ec2ceb2ecdb66fd037b22aefa5de1a24f58.

70/70 checks, no failed/unknown rows, READ_ONLY_REPLAY_EXACT. Exact full-block,
Schur, chain and left-eigenvector identities are checked for both branches.
Independent full 11-field linear solves use both tilt signs and algebraic
Zbar probes 0,1e-5, with homogeneous/nonzero auxiliary sources. These Zbar
values are operator controls, not newly selected background solutions.
160 digits address the deliberately singular pole controls; normalized
full-solve criterion remains 1e-30 and pole-limit criterion 1e-25. The full
solves have discrepancies below1.61e-161; pole tests pass their frozen
criterion. Those limits are implementation controls, not a time-error bound.

180 inherited/current source pins and sidecars are verified before and after
calculation. Same-author independent methods/replay are not independent peer
review. Original evidence and failed attempts remain immutable; live indices
are appended only with backups of their original bytes and current digests.
No manuscripts, PDFs, website, provider sessions, vault records, commits,
pushes or publication are changed. The native goal remains usageLimited;
the authorized manual calculation does not reactivate it.

G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
PROCEED_PROVISIONALLY for this compatibility map; HOLD_SUBSTANTIVE for the
unproved actual-source/domain/time/window/matching claims. Inherit all
constrained-principal/action/backend/root/kinetic/force/cusp/jerk/node/current/
Ward review dependencies. Review DEFERRED, not cleared.
