#!/usr/bin/env python3
"""Fail-closed preflight for the ITSM-to-BBN background interface.

This executable audits the currently registered UVIR-003 FRW export against
the minimum data contract needed to supply an external BBN network.  It does
not infer a temperature from a dimensionless scale factor, identify a
condensate density with radiation, or invent a transfer current or effective
gravity.  A missing contract is therefore an expected, explicit refusal to
run an ITSM BBN prediction rather than a silent standard-cosmology fallback.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from bbn001_action_derived_input_contract import (
    CONTRACT_PATH,
    contract_alias_map,
    load_contract,
    validate_contract,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
BACKGROUND_REL = Path("Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_summary.json")
TRAJECTORY_REL = Path("Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_trajectory.csv")
OUTPUT_PATH = Path(__file__).parent / "outputs" / "bbn001_upstream_interface_preflight_summary.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_or_missing(path: Path) -> dict[str, Any]:
    relative = path.relative_to(REPO_ROOT).as_posix()
    return {
        "path": relative,
        "exists": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else "MISSING",
    }


def _flatten_names(value: Any) -> set[str]:
    """Collect JSON object keys without treating their values as inputs."""

    names: set[str] = set()
    if isinstance(value, dict):
        names.update(str(key) for key in value)
        for child in value.values():
            names.update(_flatten_names(child))
    elif isinstance(value, list):
        for child in value:
            names.update(_flatten_names(child))
    return names


def _match_aliases(names: set[str], aliases: tuple[str, ...]) -> list[str]:
    folded = {name.casefold(): name for name in names}
    matches: list[str] = []
    for alias in aliases:
        if alias in names:
            matches.append(alias)
            continue
        # A one-letter T/t distinction is semantic here: the export's `t` is
        # time and must never satisfy the network's photon-temperature `T`.
        if alias in {"T", "t"}:
            continue
        if alias.casefold() in folded:
            matches.append(folded[alias.casefold()])
    return matches


def _check_contract(names: set[str], contract: dict[str, tuple[str, ...]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field, aliases in contract.items():
        matches = _match_aliases(names, aliases)
        result[field] = {
            "available": bool(matches),
            "matched_names": matches,
            "accepted_aliases": list(aliases),
        }
    return result


def _missing_input_receipt(
    network: dict[str, Any], itsm: dict[str, Any], status: str
) -> dict[str, Any]:
    blocking_fields: list[dict[str, Any]] = []
    for domain, fields in (("network_history", network), ("itsm_closing_inputs", itsm)):
        for field, item in fields.items():
            if not item["available"]:
                blocking_fields.append(
                    {
                        "domain": domain,
                        "field": field,
                        "accepted_aliases": item["accepted_aliases"],
                        "matched_names": item["matched_names"],
                        "reason": (
                            "No accepted alias appears in the registered export. "
                            "The value, dimensions and action-level provenance are not inferred."
                        ),
                    }
                )
    return {
        "record_type": "BBN001_ACTION_DERIVED_MISSING_INPUT_RECEIPT",
        "status": status,
        "presence_check_only": True,
        "value_validation": "NOT_PERFORMED",
        "provenance_validation": "NOT_PERFORMED",
        "no_value_inference": True,
        "blocking_fields": blocking_fields,
        "blocking_field_count": len(blocking_fields),
    }


def _load_trajectory_header(path: Path) -> list[str]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def run_preflight() -> dict[str, Any]:
    contract = load_contract()
    contract_validation = validate_contract(contract)
    if not contract_validation["ok"]:
        return {
            "record_type": "BBN001_UPSTREAM_INTERFACE_PREFLIGHT",
            "gate": "BBN-001",
            "status": "ERROR_BBN001_ACTION_DERIVED_INPUT_CONTRACT",
            "physics_pass": False,
            "gate_effect": "NONE",
            "publication_status": "NOT_A_PHYSICS_CLAIM",
            "contract": {
                "path": relative_or_missing(CONTRACT_PATH),
                "sha256": sha256_file(CONTRACT_PATH) if CONTRACT_PATH.is_file() else "MISSING",
            },
            "contract_validation": contract_validation,
            "decision": {
                "minimum_external_network_history_available": False,
                "physical_network_history_ready": False,
                "action_derived_itsm_bbn_ready": False,
                "missing_network_fields": [],
                "missing_itsm_fields": [],
                "refusal_reason": "The frozen BBN-001 input contract failed validation; no upstream field is accepted.",
            },
            "missing_input_receipt": _missing_input_receipt({}, {}, "ERROR_BBN001_ACTION_DERIVED_INPUT_CONTRACT"),
            "required_next_inputs": contract.get("required_next_inputs", []),
            "nonclaims": contract.get("publication_boundary", {}).get("nonclaims", []),
        }

    background_path = REPO_ROOT / BACKGROUND_REL
    trajectory_path = REPO_ROOT / TRAJECTORY_REL
    source_files = {
        "background_summary": relative_or_missing(background_path),
        "background_trajectory": relative_or_missing(trajectory_path),
    }

    background: dict[str, Any] = {}
    load_error = None
    if background_path.is_file():
        try:
            loaded = json.loads(background_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                background = loaded
            else:
                load_error = "background summary root is not a JSON object"
        except (OSError, json.JSONDecodeError) as exc:
            load_error = f"could not load background summary: {exc}"
    else:
        load_error = "background summary is missing"

    json_names = _flatten_names(background)
    trajectory_header = _load_trajectory_header(trajectory_path)
    observed_names = json_names | set(trajectory_header)
    network = _check_contract(observed_names, contract_alias_map(contract, "network_history"))
    itsm = _check_contract(observed_names, contract_alias_map(contract, "itsm_closing_inputs"))

    # The registered trajectory has H and t, but its authority explicitly
    # describes the branch as dimensionless.  Presence of a field is not
    # treated as physical closure without a unit declaration.
    dimensionless_branch = (
        background.get("representative_branch", {}).get("parameter_scope")
        == "Dimensionless existence example only; not a cosmological fit."
    )
    network_fields_ready = all(item["available"] for item in network.values())
    itsm_fields_ready = all(item["available"] for item in itsm.values())
    unit_map_ready = itsm["physical_unit_map"]["available"]
    physical_network_ready = network_fields_ready and unit_map_ready and not dimensionless_branch
    action_derived_ready = physical_network_ready and itsm_fields_ready

    missing_network = [field for field, item in network.items() if not item["available"]]
    missing_itsm = [field for field, item in itsm.items() if not item["available"]]
    status = "READY_FOR_ACTION_DERIVED_BBN_ADAPTER" if action_derived_ready else "BLOCKED_UPSTREAM_BACKGROUND"

    return {
        "record_type": "BBN001_UPSTREAM_INTERFACE_PREFLIGHT",
        "gate": "BBN-001",
        "status": status,
        "physics_pass": contract["publication_boundary"]["physics_pass"],
        "gate_effect": contract["publication_boundary"]["gate_effect"],
        "publication_status": contract["publication_boundary"]["publication_status"],
        "contract": {
            "path": relative_or_missing(CONTRACT_PATH),
            "sha256": sha256_file(CONTRACT_PATH),
            "version": contract["version"],
            "status": contract["status"],
        },
        "contract_sha256": sha256_file(CONTRACT_PATH),
        "contract_validation": {
            "ok": contract_validation["ok"],
            "checks_passed": contract_validation["checks_passed"],
            "checks_total": contract_validation["checks_total"],
        },
        "source_files": source_files,
        "source_load": {"ok": load_error is None, "error": load_error},
        "observed_export": {
            "json_key_count": len(json_names),
            "trajectory_columns": trajectory_header,
            "trajectory_column_count": len(trajectory_header),
            "dimensionless_branch_declared": dimensionless_branch,
        },
        "network_contract": network,
        "itsm_closing_contract": itsm,
        "contract_field_requirements": {
            "network_history": contract["network_history"],
            "itsm_closing_inputs": contract["itsm_closing_inputs"],
        },
        "decision": {
            "minimum_external_network_history_available": network_fields_ready,
            "physical_network_history_ready": physical_network_ready,
            "action_derived_itsm_bbn_ready": action_derived_ready,
            "missing_network_fields": missing_network,
            "missing_itsm_fields": missing_itsm,
            "refusal_reason": (
                "The registered UVIR-003 export is a dimensionless representative branch and "
                "does not provide a physical photon-temperature history or the action-derived "
                "plenum/transfer/gravity contract. No values are inferred."
                if not action_derived_ready
                else "All declared upstream fields are present; an action-derived adapter may be evaluated separately."
            ),
        },
        "missing_input_receipt": _missing_input_receipt(network, itsm, status),
        "required_next_inputs": contract["required_next_inputs"],
        "nonclaims": contract["publication_boundary"]["nonclaims"],
    }


def main() -> int:
    try:
        result = run_preflight()
    except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
        result = {
            "record_type": "BBN001_UPSTREAM_INTERFACE_PREFLIGHT",
            "gate": "BBN-001",
            "status": "ERROR_BBN001_ACTION_DERIVED_INPUT_CONTRACT",
            "physics_pass": False,
            "gate_effect": "NONE",
            "publication_status": "NOT_A_PHYSICS_CLAIM",
            "contract": {
                "path": relative_or_missing(CONTRACT_PATH),
                "sha256": sha256_file(CONTRACT_PATH) if CONTRACT_PATH.is_file() else "MISSING",
            },
            "contract_load_error": str(exc),
            "decision": {
                "minimum_external_network_history_available": False,
                "physical_network_history_ready": False,
                "action_derived_itsm_bbn_ready": False,
                "missing_network_fields": [],
                "missing_itsm_fields": [],
                "refusal_reason": "The frozen BBN-001 input contract could not be loaded; no upstream field is accepted.",
            },
            "missing_input_receipt": _missing_input_receipt({}, {}, "ERROR_BBN001_ACTION_DERIVED_INPUT_CONTRACT"),
            "required_next_inputs": [],
            "nonclaims": ["No upstream value is inferred or accepted."],
        }
    result["script_sha256"] = sha256_file(Path(__file__))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    OUTPUT_PATH.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256").write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii", newline="\n"
    )
    print("BBN-001 upstream interface preflight complete")
    print(f"Status: {result['status']}")
    print(f"Minimum external network history: {result['decision']['minimum_external_network_history_available']}")
    print(f"Action-derived ITSM BBN ready: {result['decision']['action_derived_itsm_bbn_ready']}")
    print(f"SHA-256: {digest}")
    print(f"Output: {OUTPUT_PATH}")
    if result["status"].startswith("ERROR_"):
        return 1
    return 0 if result["decision"]["action_derived_itsm_bbn_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
