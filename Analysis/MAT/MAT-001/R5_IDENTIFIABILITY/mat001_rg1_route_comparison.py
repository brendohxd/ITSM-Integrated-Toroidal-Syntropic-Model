#!/usr/bin/env python3
"""Emit the preregistered A0-A2 RG1 route-disposition matrix."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

BASE=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent/"outputs"/"rg1"

ROUTES=[
 {"id":"R5-P1/M1-current","identity":"PARTIAL","A0":"FAIL","A1":"FAIL","A2":"FAIL","disposition":"REJECT_CURRENT_INSTANTIATION","reason":"real compensator toy replaces the required finite-density complex condensate; f and ell remain free; no constrained signed physical residue; Cassini inequality fails its own numbers"},
 {"id":"M1-redesign","identity":"HIGH_IF_CONDENSATE_RETAINED","A0":"OPEN","A1":"OPEN","A2":"OPEN","disposition":"DO_NOT_ADVANCE_RG1","reason":"requires a new complete parent action and cannot inherit evidence from rejected R5-P1"},
 {"id":"M2","identity":"HIGH","A0":"OPEN","A1":"OPEN","A2":"OPEN","disposition":"ADVANCE_CHEAP_REDUCTION","reason":"closest microscopic test of whether the declared condensate radial/heavy sector generates a static matter vertex; falsifiable by absent source or independent soft coefficient"},
 {"id":"M3","identity":"MEDIUM","A0":"OPEN","A1":"OPEN","A2":"OPEN","disposition":"HOLD","reason":"no single parent portal currently prevents appended coupling or double counting"},
 {"id":"M4","identity":"HIGH","A0":"PASS_METHOD","A1":"BLOCKED_BY_PARENT","A2":"OPEN","disposition":"ADVANCE_INVARIANT_RESIDUE_CONTROL","reason":"directly asks for the chart-invariant source-pole residue and can kill normalization artifacts without assigning bare K_Q"},
 {"id":"M5","identity":"HIGHEST","A0":"OPEN","A1":"OPEN","A2":"OPEN","disposition":"HOLD_PENDING_T1_T2","reason":"normalized moduli/winding modes and matter coupling are absent; inserting L=c/H, 2*pi, 2/3, or a cycle count is forbidden"},
]

def h(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 evidence=[
  BASE/"Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md",
  BASE/"Theory/Gates/MAT-001/R5_P1_T2_COVARIANT_COMPENSATOR.md",
  BASE/"Theory/Gates/MAT-001/R5_P1_T7_OBSERVATIONAL_COMPLIANCE.md",
  BASE/"Theory/Core/ITSM_Tier1_Route_Test_Programme.md",
 ]
 summary={"audit":"MAT-001_RG1_R5_P1_M1_M5_A0_A2","calculation_status":"PASS_DETERMINISTIC_DISPOSITION_MATRIX","physics_status":"MAT-001_BLOCKED","V":"NOT_COMPUTED","K_Q":"NOT_DERIVED","selected_for_next_cheap_work":["M4","M2"],"routes":ROUTES,"rules":["no ordinal score is a physics result","current R5-P1 rejection does not reject every possible M1 action","advancement authorizes only the named cheap reduction/control, not MAT promotion"],"evidence_sha256":{str(p.relative_to(BASE)).replace('\\','/'):h(p) for p in evidence}}
 jp=OUT/"mat001_rg1_route_comparison_summary.json"; jp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 rows="\n".join(f"| {r['id']} | {r['A0']} | {r['A1']} | {r['A2']} | `{r['disposition']}` | {r['reason']} |" for r in ROUTES)
 report=f"""# MAT-001 RG1 hostile R5-P1 and M1-M5 comparison

**Parent status:** `BLOCKED`  
**Invariant vertex:** `V NOT_COMPUTED`; `K_Q NOT_DERIVED`

## A0-A2 matrix

| Route | A0 | A1 | A2 | RG1 disposition | Decisive reason |
|---|---|---|---|---|---|
{rows}

## Hostile R5-P1 finding

The current R5-P1 chain does not satisfy its own specification. Its source is
a toy static `alpha rho_b` term rather than a derived vertex of the declared
finite-density parent; the compensator is a real scalar, `f` and `ell` remain
free, the full constraint/ghost reduction and signed physical pole residue are
missing, and the reported `alpha ~= 0.016` exceeds its own Cassini requirement
`alpha < 0.0022`. Contact energy-independence is not a unitarity proof, and a
conformal scalar does not independently supply lensing. The current
instantiation is rejected/quarantined; this is not a no-go for every M1 design.

## RG1 bounded selection

Advance **M4** only as an invariant-residue/null control and **M2** only as a
cheap explicit radial/heavy-mode integrate-out. Neither is a physics pass.
M4 must expose chart/source-normalization dependence; M2 must include the
static matter interaction and derive `g_phys/sqrt(Z_phys)`. Stop either route
at its first A0-A2 kill criterion.
"""
 rp=OUT/"MAT-001_RG1_ROUTE_COMPARISON.md"; rp.write_text(report,encoding="utf-8")
 sp=OUT/"mat001_rg1_route_comparison.sha256"; sp.write_text(f"{h(jp)}  {jp.name}\n{h(rp)}  {rp.name}\n",encoding="ascii")
 print(json.dumps({"status":summary["physics_status"],"selected":summary["selected_for_next_cheap_work"]}))
if __name__=="__main__": main()
