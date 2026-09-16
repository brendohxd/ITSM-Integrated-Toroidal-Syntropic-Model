#!/usr/bin/env python3
"""Fail-closed receipt audit for the corrected TOP-001 toy controls."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent
OUTPUTS = BASE / "outputs"
TARGETS = (
    "top001_3d_epstein_casimir_summary.json",
    "top001_driven_moduli_summary.json",
    "top001_coupled_moduli_summary.json",
)
ABSOLUTE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|/(?:Users|home)/)")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, str):
        yield value


def run_audit() -> dict:
    checks = []
    for filename in TARGETS:
        path = OUTPUTS / filename
        sidecar = path.with_name(path.name + ".sha256")
        if not path.is_file() or not sidecar.is_file():
            raise RuntimeError(f"missing TOP-001 receipt or sidecar: {filename}")
        data = json.loads(path.read_text(encoding="utf-8"))
        actual_hash = _sha256(path)
        recorded_hash = sidecar.read_text(encoding="utf-8").split()[0].strip()
        if actual_hash.lower() != recorded_hash.lower():
            raise RuntimeError(f"sidecar hash mismatch: {filename}")
        if data.get("physics_pass") is not False:
            raise RuntimeError(f"physics_pass is not false: {filename}")
        if data.get("gate_effect") != "NONE":
            raise RuntimeError(f"gate_effect is not NONE: {filename}")
        if data.get("publication_status") != "NOT_A_PHYSICS_CLAIM":
            raise RuntimeError(f"publication status is not fail-closed: {filename}")
        absolute_strings = [item for item in _strings(data) if ABSOLUTE_PATH.search(item)]
        if absolute_strings:
            raise RuntimeError(f"absolute path entered receipt: {filename}")
        checks.append(
            {
                "file": filename,
                "physics_pass": False,
                "gate_effect": "NONE",
                "publication_status": "NOT_A_PHYSICS_CLAIM",
                "sha256": actual_hash,
                "absolute_path_strings": 0,
            }
        )

    return {
        "record_type": "TOP001_CLAIM_FIREWALL_CONTROL",
        "gate": "TOP-001",
        "status": "PASS_TOP001_CLAIM_FIREWALL_CONTROL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "publication_status": "NOT_A_PHYSICS_CLAIM",
        "checks": checks,
        "interpretation": "Receipt metadata is fail-closed; this does not validate the underlying toy as a physical model.",
    }


def main() -> int:
    result = run_audit()
    output = OUTPUTS / "top001_claim_firewall_summary.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = _sha256(output)
    output.with_name(output.name + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    print("TOP-001 claim-firewall audit complete")
    print(f"Receipts checked: {len(result['checks'])}")
    print("physics_pass: False")
    print(f"SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
