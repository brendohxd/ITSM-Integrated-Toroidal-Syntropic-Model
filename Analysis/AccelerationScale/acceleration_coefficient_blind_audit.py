#!/usr/bin/env python3
"""Blind provenance audit for the ITSM acceleration coefficient."""
from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent/"outputs"
EXCLUDE=(".git/",".codex-remote-attachments/","CAMB_ITSM_Solver/","Analysis/AccelerationScale/outputs/")
PAT=re.compile(r"(?:a[_ ]?0|a_\{0\}).{0,100}(?:2\s*\\?pi|2π|H[_ ]?0|H_\{0\})|(?:2\s*\\?pi|2π).{0,100}(?:a[_ ]?0|H[_ ]?0)",re.I)
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def main():
 OUT.mkdir(parents=True,exist_ok=True); rows=[]
 for p in sorted(ROOT.rglob("*")):
  rel=p.relative_to(ROOT).as_posix()
  if not p.is_file() or p.suffix.lower() not in {".md",".tex",".txt"} or any(rel.startswith(x) for x in EXCLUDE): continue
  try: lines=p.read_text(encoding="utf-8",errors="replace").splitlines()
  except OSError: continue
  for n,line in enumerate(lines,1):
   if PAT.search(line):
    compact=" ".join(line.strip().split())[:320]
    form="undetermined"
    low=compact.lower().replace(" ","")
    if re.search(r"2(?:\\pi|π).*c.*h",low): form="multiplier_candidate"
    if re.search(r"(?:/|frac\{c.*h.*\}\{2(?:\\pi|π))",low): form="divisor_candidate"
    rows.append({"path":rel,"line":n,"form_hint":form,"text":compact})
 csvp=OUT/"acceleration_coefficient_provenance_hits.csv"
 with csvp.open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["path","line","form_hint","text"]); w.writeheader(); w.writerows(rows)
 summary={"audit":"BLIND_ACCELERATION_COEFFICIENT","parameterization":"a0_internal = C_chi c H0","verdict":"C_CHI_NOT_DERIVED","status":"PHENOMENOLOGICAL_RELATION_ONLY","provenance_hit_count":len(rows),"logic":["circulation quantization fixes a cycle integral/velocity scale, not a unique local acceleration","c^2/L becomes cH times a coefficient only after a physical length and radius-versus-circumference convention are selected","choosing L_cycle=2*pi*c/H returns 1/(2*pi) algebraically but that scale-identification is an extra postulate","the declared action does not yet provide normalized modulus/winding-to-matter force matching","observed MOND, SPARC, bTFR, weak-lensing and desired H0 values were not used to choose C_chi"],"candidate_status":{"2*pi":"historical_written_form_observationally_mismatched_not_derived","1/(2*pi)":"numerically_motivated_provisional_not_derived","sqrt(1-q)/(2*pi)":"external_curvature_closure_not_ITSM_derived","C_derived":"open"},"output_sha256":{csvp.name:h(csvp)},"boundary":"The scan reconstructs provenance; document occurrences are not evidence of derivation."}
 jp=OUT/"acceleration_coefficient_blind_audit_summary.json"; jp.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 report="""# Blind ITSM acceleration-coefficient audit

**Frozen parameterization:** `a0_internal = C_chi c H0`  
**Verdict:** `C_CHI_NOT_DERIVED`  
**Status:** `PHENOMENOLOGICAL_RELATION_ONLY`

## Blind derivation result

Circulation quantization, `integral v.dl = n kappa`, fixes a global cycle
integral and may fix a velocity scale once a cycle and normalization are
specified. It does not uniquely produce a local radial acceleration. A scale
`c^2/L` becomes proportional to `cH` only after identifying a physical length
with a Hubble-related length. Choosing the cycle circumference
`L_cycle = 2*pi*c/H` yields `cH/(2*pi)` algebraically, but the identification
of that cycle with the dynamical local-force threshold is the load-bearing
postulate. Choosing radius rather than circumference moves the factor.

The current action does not derive a stabilized normalized modulus/winding
mode, its coupling to the physical matter source, or the mapping from the
global cycle to the local weak-field threshold. Therefore topology and
dimensional analysis do not select `2*pi`, `1/(2*pi)`, or any other unique
coefficient.

## Provenance disposition

The archive contains both multiplier and divisor families, including written
multiplier equations paired with divisor-compatible numerical values. The
divisor's numerical agreement cannot repair the missing action-level map.
The `sqrt(1-q)/(2*pi)` alternative is a separate curvature closure and cannot
be imported into ITSM without derivation.

No observed MOND/SPARC/bTFR/weak-lensing value or desired H0 was used to
select the coefficient. Until T1/T2/T4 and MAT normalization close, retain
`C_chi` as unknown and keep observational dressing `C_obs` separate.
"""
 rp=OUT/"ACCELERATION_COEFFICIENT_BLIND_AUDIT.md"; rp.write_text(report,encoding="utf-8")
 (OUT/"acceleration_coefficient_blind_audit.sha256").write_text(f"{h(csvp)}  {csvp.name}\n{h(jp)}  {jp.name}\n{h(rp)}  {rp.name}\n",encoding="ascii")
 print(json.dumps({"verdict":summary["verdict"],"hits":len(rows)}))
if __name__=="__main__": main()
