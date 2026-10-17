# Three-family fixed-charge kinetic extension - unverified working note

15 October 2026. NOT an accepted research report or frozen execution contract.
No new scientific executable ran. No computational or physical PASS is claimed.
This note preserves the hand-derived candidate from the private handoff.
The repository write was initially blocked; see the update below.

## Approved scope and already completed work

Continue unchanged R4C1 with one bounded Stage-2 coupled/physical-domain task.
Stop at its result or precise obstruction and ask the operator to switch back
to Sol and confirm. No provider dispatch, publication, commit or push.

The B1 mean-mode energy report dated 11 October already distinguishes a negative
homogeneous momentum direction with varying dust charge from a positive block
in a separate fixed-U(1)-and-fixed-dust-charge ensemble. This is not new work,
and fixing a global charge is not a gauge repair of the original result.

The useful next extension is to bind that comparison to the generic 22-field
action for all three current diagnostic families. Do not substitute coefficients
into old B1-specialized matrices. The fixed-charge retarded V3 timing warning
remains unchanged; homogeneous quadratic positivity cannot remove it.

## Hand-derived candidate, not yet verified against the generic action

Use coordinate volume v=a^3, x=ln(v), complex radius R, reservoir r,
pd=psi_dot, fixed internal charge Q, M=M_cos2, Tm=M_T2.
The force scalar psi is not the internal U(1) angle.

```text
U = V_potential + rho + Q^2/(2*v^2*R^2),
6*M*H^2 = Rdot^2 + rdot^2 + K*pd^2 + 2*U.

G = diag(-2*M/3, 1, 1, Tm/4 [five shears], f2 [three frame modes]),
b = (2*M*H, -Rdot, -rdot, 0,...,0)^T.

K_variable_dust = [[G, b/C], [(b/C)^T, -2*U/C^2]],
K_fixed_both = G + b*b^T/(2*U).
```

The proposed fixed-both (x,R,r) leading principal minors are

```text
D1 = M*(Rdot^2+rdot^2+K*pd^2)/(3*U),
D2 = M*(rdot^2+K*pd^2)/(3*U),
D3 = M*K*pd^2/(3*U).
```

These are positive for M,U,K>0 and pd!=0, with separately positive Tm,f2.
The block congruence to diag(K_fixed_both,-2*U/C^2) retains one negative
direction in the larger ensemble. This conditional matrix argument is not
yet a completed generic constraint/charge reduction.

Independent Hamiltonian comparison to verify:

```text
B = diag(3/(4*M*v),-1/(2*v),-1/(2*v),
         -2/(Tm*v) [five],-1/(2*f2*v) [three]),
p = (-2*M*v*H,v*Rdot,v*rdot,0,...,0)^T,
F = p^T*B*p-Q^2/(2*v*R^2)-v*V_potential-C*P_tau,
H_psi = -pd_background*sqrt(2*K*v*F).

On rho=C*P_tau/v, F=K*v*pd^2/2 and the positive clock branch:
Hpp = -2*B+4*(B*p)*(B*p)^T/(K*v*pd^2)
    = inverse(K_fixed_both)/v.
```

This is a candidate quadratic momentum comparison at an aligned isotropic
background, not a nonlinear Hamiltonian for arbitrary boosted fields. Retain
the angular Routh term -N*Q^2/[2*v*R^2*(1-zeta*R^2*boost_squared)] and its boost
curvature. No full potential, characteristic, physical-window or GR claim.

Existing family maps give:

| Family | M_cos2 | M_T2 | f2 | K |
| --- | --- | --- | --- | --- |
| G3 | 1-eta/12 | 1-eta/8 | eta/6 | 3*eta |
| B1-frame | 1+eta/10 | 1 | eta/6 | 3*eta |
| Hierarchical | 1+eta/10+eta^2/16 | 1-eta^2/8 | eta/6 | 3*eta |

These coefficients are positive on 0<eta<=1/4. The inherited nonnegative
potential and rho>0 give U>0; nonzero clock and regular auxiliary constraints
remain necessary. eta=0 is singular. The diagnostic K is not canonical K_Q.

## Execution obstruction and preservation

ITSM Python 3.13.9 starts, but importing SymPy terminates without a Python
traceback (direct process exit 4294967295; wrapper exit 1). A separate context
optimizer status command succeeded. Conda startup reports Windows
`{Illegal System DLL Relocation}`. These are observed errors, not a diagnosis
of their cause and not evidence of malicious activity.

Bundled Python 3.12.14 starts but lacks SymPy. A process-local attempt to reuse
already-installed pure-Python math packages with compiled backends disabled
also terminates without a traceback. No package installation, copying, removal,
global environment/configuration change, firewall change or vault mutation.

The first attempted new contract/working-note write under Theory/Gates/RES-001
failed. Neither file existed at that point. C: had approximately 106 GB free when
checked. The existing dirty review register, sidecar and COMPACT_T3_CONTROL
directory were untouched. No original research file or sidecar was edited.

## Resume requirements

1. Establish a working math-library import without unapproved system changes.
2. Freeze the real contract and versioned executable before a fresh run.
3. Derive from the generic 22-field kernel, retaining density/lapse, normal,
   regulator and zero-mode constraints, evolving polar basis and boundary
   generator. Check cyclic-angle and dust-origin reductions, not just K.
4. Prove exact sign and independent Legendre identities; run all 378 archived
   background-node controls from both methods with predeclared conditioning-
   aware tolerances. Never silently project archived backgrounds on shell.
5. Preserve sources/sidecars and perform immutable replay. Only then issue an
   acceptance report and append the deferred-review register.

Pending review dependency: THREE-FAMILY-FIXED-CHARGE-KINETIC-V1, inheriting
MEAN-MODE-ENERGY, THREE-FAMILY-CHARGE-DOMAIN, FIXED-CHARGE-RETARDED,
PLANAR-WWR, GR-FAMILY-SURVEY and transitive debt. All reviews deferred, not cleared.

physics_pass=false; gate_effect=NONE; Rule9_cleared=false;
Tests1-3=HOLD_SUBSTANTIVE; MAT-001=BLOCKED; UVIR-003=IN_PROGRESS;
K_Q=NOT_DERIVED; V=NOT_COMPUTED; Stage4A=CLOSED; TOP-X4=UNCHANGED.
No physical Stage-2 GO; Stage 3 not entered. This working note is unverified and
must not be used as an accepted result. Switch back to Sol and await confirmation.

## Update after the operator allowed protected-folder access

The operator supplied Windows Security's Controlled folder access record naming
codex.exe and this exact Theory/Gates/RES-001 folder, then reported allowing it.
A subsequent new contract write succeeded. This identifies the earlier folder
write restriction; it does not diagnose the separate Python import failure.
The same unbuffered import check still printed Python 3.13.9 and exited 1
without reaching the SymPy/mpmath success marker. No scientific checks ran.

The companion scope contract is now saved as
`RES001_R4C1_THREE_FAMILY_FIXED_CHARGE_KINETIC_V1_CONTRACT_2026-10-15.md`.
This new working note and both new sidecars preserve the incomplete calculation.
The original private handoff is retained. Existing research results, hashes and
the living review register remain unchanged. No permissions or security settings
were changed by the assistant. Stop here and request the agreed return to Sol.

