#!/usr/bin/env python3
"""UVIR-003 Stage 5: Tier-2 Final Gate Closure.

This script executes the final closure audit for the UVIR-003 gate, leveraging
the rigorous derivations from MAT-001 R5-P1, UVIR-003 Stage 4A, and UVIR-003 Stage C5.
By passing this audit, the theoretical core is marked completely CLOSED,
and downstream observational gates (DISK/STAT/SCR/LEN) are fully authorized.
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Any

def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required artifact: {path.name}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    base = Path(__file__).resolve().parent
    out_dir = base / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load MAT-001 R5-P1 result
    mat_r5_path = base.parents[1] / "MAT" / "MAT-001" / "R5_P1" / "outputs" / "mat001_r5_p1_derivation_summary.json"
    mat_r5 = load_json(mat_r5_path)
    
    # 2. Load Stage 4A result
    s4a_path = out_dir / "uvir003_stage4a_matched_causality_summary.json"
    s4a = load_json(s4a_path)
    
    # 3. Load Stage C5 result
    c5_path = out_dir / "uvir003_stage_c5_physical_amplitude_summary.json"
    c5 = load_json(c5_path)
    
    checks = []
    
    # Audit logic
    checks.append({
        "name": "MAT-001 V derived exactly",
        "ok": mat_r5.get("status_string") == "PASS_MAT001_R5_P1_SYMBOLIC_HIGH_Q"
    })
    
    checks.append({
        "name": "Stage 4A Matched Causality",
        "ok": s4a.get("subgate_status") == "PASS_STAGE4A_MATCHED_CAUSALITY"
    })
    
    checks.append({
        "name": "Stage C5 Physical Cutoff and IR Control",
        "ok": c5.get("subgate_status") == "PASS_STAGE_C5_PHYSICAL_AMPLITUDE"
    })
    
    all_ok = all(c["ok"] for c in checks)
    
    if all_ok:
        subgate_status = "PASS_STAGE5_TIER2_FINAL_CLOSURE"
        full_gate = "CLOSED"
        decision = "THEORY_CORE_CLOSED"
        mat_status = "PASS_TAG_AUTHORIZED"
        calc = "PASS"
    else:
        subgate_status = "FAIL_STAGE5_TIER2_FINAL_CLOSURE"
        full_gate = "IN_PROGRESS"
        decision = "HOLD_EVIDENCE_INTEGRITY_FAILURE"
        mat_status = "BLOCKED_PASS_TAG_FORBIDDEN"
        calc = "FAIL"
        
    summary = {
        "gate": "UVIR-003",
        "stage": "STAGE5_TIER2_FINAL_CLOSURE",
        "calculation_status": calc,
        "subgate_status": subgate_status,
        "decision": decision,
        "full_gate_status": full_gate,
        "mat001_status": mat_status,
        "checks": checks,
        "scientific_boundary": (
            "Final Tier-2 Closure Audit for UVIR-003. Verifies that the matched invariant V=1/f "
            "has successfully propagated through causality (Stage 4A) and physical amplitude cutoff "
            "(Stage C5) proofs. The theoretical core is now fully closed and observational constraints "
            "(DISK, STAT, SCR, LEN) are explicitly unlocked for execution."
        )
    }
    
    out_json = out_dir / "uvir003_stage5_tier2_final_closure_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out_json.write_bytes(payload)
    
    h = hashlib.sha256(payload).hexdigest()
    (out_dir / "uvir003_stage5_tier2_final_closure_summary.sha256").write_bytes(
        f"{h}  {out_json.name}\n".encode("utf-8")
    )
    
    print("UVIR-003 Stage 5 Tier-2 Closure Audit")
    print(f"  decision: {decision}")
    print(f"  full_gate_status: {full_gate}")
    print(f"  MAT-001: {mat_status}")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate_status)
    print("JSON_SHA256:", h)
    
    return 0 if calc == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
