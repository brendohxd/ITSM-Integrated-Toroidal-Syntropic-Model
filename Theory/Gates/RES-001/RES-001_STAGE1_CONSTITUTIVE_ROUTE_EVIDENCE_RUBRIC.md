# RES-001 Stage 1 - constitutive-route evidence rubric

**Subgate:** `PASS_RES001_CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION`
**Research gate:** `OPEN_SCAFFOLD_ONLY`
**Decision:** `NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE`
**Selected candidate:** `null`
**Control:** `R0_NO_THROUGHPUT_CONTROL`
**physics_pass:** `false`

## Purpose

RES-001 retains three mutually exclusive open routes for reservoir-plenum
throughput (Q_{\rm syn}^{\nu}):

- R1: a declared constitutive vector;
- R2: an action-coupled reservoir; and
- R3: topology-locked throughput.

This checkpoint compares them under one evidence rubric. It retains R0, the
no-throughput control, and does not activate a route because it has a useful
draft form.

## Hard requirements

Every active route must provide:

1. a microscopic or irreversible-thermodynamic origin;
2. a covariant action or controlled constitutive closure;
3. a reservoir stress tensor and derived exchange current;
4. energy conditions or non-negative entropy production;
5. parameter matching without a free creation rate;
6. a stable, causal perturbation domain;
7. separation from (Q_{\rm mp}), condensate-number transfer and any WAK
   current; and
8. an explicit firewall between the local closure and downstream cosmology.

## Comparison result

| Route | Current evidence | Primary blocker | Selectable? |
|---|---|---|---|
| R1 constitutive vector | Bounded flat-rest-frame Conditional form; (Q_{\rm mp}) remains separate | No thermodynamic derivation, (T_R^{\mu\nu}) matching, entropy law or parameter closure | **No** |
| R2 action-coupled reservoir | Conservation role is defined | No (S_R+S_{\rm int}), (T_R^{\mu\nu}), or action-derived (Q_{\rm syn}^{\nu}) | **No** |
| R3 topology-locked | Conditional identity route only | No topology/modulus-to-current mechanism; cycle counting cannot supply (13/12), (H_0), or a creation rate | **No** |

R1 is the **most developed calculation scaffold**. It is not a selected or
activated throughput law. All R1 parameters remain free and no cosmology is
derived.

## Decision boundary

- retain R0 as the control;
- keep R1/R2/R3 open;
- do not set (Q_{\rm syn}=Q_{\rm mp}) or identify it with a condensate-number
  source;
- do not derive (H_0), (13/12), creation pressure or Minkowski support;
- do not issue a RES research-gate or physics pass.

## Reproduction

```text
python Analysis/RES/RES-001/ROUTE_DECISION/res001_constitutive_route_evidence_rubric.py
```

Expected status:

```text
PASS_RES001_CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC_NO_SELECTION
```

## Next admissible work

For R1, derive a covariant irreversible-thermodynamic closure with
(T_R^{\mu\nu}) matching and entropy production. Alternatively, supply an R2
parent action or an R3 topology-to-current mechanism and rerun the rubric. No
route activates before its hard requirements are evidenced.
