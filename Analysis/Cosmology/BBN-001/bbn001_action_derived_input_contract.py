#!/usr/bin/env python3
"""Validate the frozen machine-readable BBN-001 upstream input contract.

The validator checks the contract's field vocabulary, semantic requirements
and fail-closed publication boundary.  It also compares the current upstream
preflight receipt after that receipt has been generated.  Passing this script
means that the bookkeeping contract is valid; it does not mean that the
action-derived inputs exist or that BBN-001 is a physics gate.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "Cosmology" / "BBN-001"
CONTRACT_PATH = BASE / "bbn001_action_derived_input_contract.json"
PREFLIGHT_PATH = BASE / "outputs" / "bbn001_upstream_interface_preflight_summary.json"
OUTPUT_PATH = BASE / "outputs" / "bbn001_action_derived_input_contract_summary.json"

EXPECTED_FIELDS = {
    "network_history": (
        "time",
        "photon_temperature",
        "photon_temperature_derivative",
        "neutrino_temperature",
        "hubble",
        "baryon_density",
    ),
    "itsm_closing_inputs": (
        "physical_unit_map",
        "baryon_normalization",
        "early_plenum_density",
        "matter_plenum_transfer",
        "reservoir_plenum_transfer",
        "condensate_charge_source",
        "effective_gravity",
        "perturbation_matching",
    ),
}

EXPECTED_MISSING_NETWORK = [
    "photon_temperature",
    "photon_temperature_derivative",
    "neutrino_temperature",
    "baryon_density",
]
EXPECTED_MISSING_ITSM = [
    "physical_unit_map",
    "baryon_normalization",
    "early_plenum_density",
    "matter_plenum_transfer",
    "reservoir_plenum_transfer",
    "condensate_charge_source",
    "effective_gravity",
    "perturbation_matching",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("BBN-001 contract root must be a JSON object")
    return loaded


def contract_alias_map(contract: dict[str, Any], section: str) -> dict[str, tuple[str, ...]]:
    entries = contract[section]
    return {
        str(entry["field"]): tuple(str(alias) for alias in entry["accepted_aliases"])
        for entry in entries
    }


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def validate_contract(contract: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "contract_identity_is_frozen",
        contract.get("record_type") == "BBN001_ACTION_DERIVED_INPUT_CONTRACT"
        and contract.get("schema") == "ITSM_BBN001_ACTION_DERIVED_INPUT_CONTRACT_v1"
        and contract.get("gate") == "BBN-001"
        and contract.get("version") == "2026-09-16.v1"
        and contract.get("status") == "FROZEN_ACTION_DERIVED_INPUT_CONTRACT",
        record_type=contract.get("record_type"),
        schema=contract.get("schema"),
        gate=contract.get("gate"),
        version=contract.get("version"),
        status=contract.get("status"),
    )

    sections_ok = True
    section_details: dict[str, Any] = {}
    for section, expected in EXPECTED_FIELDS.items():
        entries = contract.get(section)
        valid_entries = isinstance(entries, list) and all(isinstance(item, dict) for item in entries)
        actual = [item.get("field") for item in entries] if valid_entries else []
        section_ok = valid_entries and actual == list(expected)
        sections_ok = sections_ok and section_ok
        section_details[section] = {"expected": list(expected), "actual": actual}
    add_check(checks, "required_field_vocabulary_is_exact", sections_ok, sections=section_details)

    all_entries: list[tuple[str, dict[str, Any]]] = []
    for section in EXPECTED_FIELDS:
        entries = contract.get(section)
        if isinstance(entries, list):
            all_entries.extend((section, item) for item in entries if isinstance(item, dict))

    field_specs_ok = True
    field_spec_details: list[dict[str, Any]] = []
    exact_aliases: dict[str, str] = {}
    for section, item in all_entries:
        aliases = item.get("accepted_aliases")
        item_ok = (
            isinstance(item.get("field"), str)
            and item.get("required") is True
            and isinstance(aliases, list)
            and bool(aliases)
            and all(isinstance(alias, str) and bool(alias) for alias in aliases)
            and len(aliases) == len(set(aliases))
            and isinstance(item.get("required_dimensions"), str)
            and bool(item.get("required_dimensions"))
            and isinstance(item.get("semantic"), str)
            and bool(item.get("semantic"))
            and isinstance(item.get("provenance_requirement"), str)
            and bool(item.get("provenance_requirement"))
        )
        duplicate_aliases: list[str] = []
        if isinstance(aliases, list):
            for alias in aliases:
                if alias in exact_aliases and exact_aliases[alias] != item.get("field"):
                    duplicate_aliases.append(alias)
                else:
                    exact_aliases[alias] = str(item.get("field"))
        item_ok = item_ok and not duplicate_aliases
        field_specs_ok = field_specs_ok and item_ok
        field_spec_details.append(
            {
                "section": section,
                "field": item.get("field"),
                "ok": item_ok,
                "duplicate_aliases": duplicate_aliases,
            }
        )
    add_check(checks, "every_field_has_dimensions_semantics_provenance_and_unique_aliases", field_specs_ok, fields=field_spec_details)

    policy = contract.get("validation_policy")
    policy_expected = {
        "field_presence_is_not_value_validation": True,
        "physical_unit_map_required": True,
        "dimensionless_branch_is_rejected": True,
        "required_provenance": True,
        "no_value_inference": True,
        "missing_input_status": "BLOCKED_UPSTREAM_BACKGROUND",
        "missing_input_exit_code": 2,
    }
    policy_ok = isinstance(policy, dict) and all(policy.get(key) == value for key, value in policy_expected.items())
    add_check(checks, "validation_policy_is_fail_closed", policy_ok, expected=policy_expected, actual=policy)

    boundary = contract.get("publication_boundary")
    boundary_ok = (
        isinstance(boundary, dict)
        and boundary.get("physics_pass") is False
        and boundary.get("gate_effect") == "NONE"
        and boundary.get("publication_status") == "NOT_A_PHYSICS_CLAIM"
        and isinstance(boundary.get("allowed_use"), list)
        and isinstance(boundary.get("nonclaims"), list)
        and len(boundary.get("nonclaims")) >= 5
    )
    add_check(checks, "publication_firewall_is_locked", boundary_ok, boundary=boundary)

    expected = contract.get("expected_current_decision")
    expected_ok = (
        isinstance(expected, dict)
        and expected.get("status") == "BLOCKED_UPSTREAM_BACKGROUND"
        and expected.get("action_derived_itsm_bbn_ready") is False
        and expected.get("missing_network_fields") == EXPECTED_MISSING_NETWORK
        and expected.get("missing_itsm_fields") == EXPECTED_MISSING_ITSM
    )
    add_check(checks, "current_missing_boundary_is_explicit", expected_ok, expected=expected)

    required_next = contract.get("required_next_inputs")
    next_ok = isinstance(required_next, list) and len(required_next) >= 5 and all(isinstance(item, str) and item for item in required_next)
    add_check(checks, "next_input_list_is_nonempty_and_textual", next_ok, required_next_inputs=required_next)

    rejection_tests = contract.get("rejection_tests")
    rejection_ok = (
        isinstance(rejection_tests, list)
        and len(rejection_tests) >= 5
        and all(
            isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and isinstance(item.get("condition"), str)
            and item.get("result") == "REJECT"
            for item in rejection_tests
        )
        and len({item.get("id") for item in rejection_tests}) == len(rejection_tests)
    )
    add_check(checks, "deterministic_rejection_tests_are_registered", rejection_ok, rejection_tests=rejection_tests)

    return {
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
    }


def validate_current_preflight(contract_hash: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    sidecar = sidecar_check(PREFLIGHT_PATH)
    add_check(checks, "current_preflight_exists_and_sidecar_matches", sidecar["matches"], receipt=sidecar)
    loaded: dict[str, Any] = {}
    load_error = None
    if PREFLIGHT_PATH.is_file():
        try:
            candidate = json.loads(PREFLIGHT_PATH.read_text(encoding="utf-8"))
            if isinstance(candidate, dict):
                loaded = candidate
            else:
                load_error = "preflight root is not a JSON object"
        except (OSError, json.JSONDecodeError) as exc:
            load_error = str(exc)
    else:
        load_error = "preflight receipt is missing"

    contract_metadata = loaded.get("contract", {}) if loaded else {}
    contract_path_metadata = contract_metadata.get("path", {}) if isinstance(contract_metadata, dict) else {}
    recorded_contract_path = (
        contract_path_metadata.get("path")
        if isinstance(contract_path_metadata, dict)
        else contract_path_metadata
    )
    add_check(
        checks,
        "preflight_records_this_contract_hash",
        loaded.get("contract_sha256") == contract_hash
        and recorded_contract_path == relative(CONTRACT_PATH),
        contract_sha256=loaded.get("contract_sha256"),
        expected_contract_sha256=contract_hash,
        contract_path=recorded_contract_path,
    )
    decision = loaded.get("decision", {})
    add_check(
        checks,
        "preflight_preserves_the_current_blocked_decision",
        loaded.get("status") == "BLOCKED_UPSTREAM_BACKGROUND"
        and loaded.get("physics_pass") is False
        and loaded.get("gate_effect") == "NONE"
        and loaded.get("publication_status") == "NOT_A_PHYSICS_CLAIM"
        and decision.get("action_derived_itsm_bbn_ready") is False
        and decision.get("missing_network_fields") == EXPECTED_MISSING_NETWORK
        and decision.get("missing_itsm_fields") == EXPECTED_MISSING_ITSM,
        status=loaded.get("status"),
        missing_network_fields=decision.get("missing_network_fields"),
        missing_itsm_fields=decision.get("missing_itsm_fields"),
    )
    receipt = loaded.get("missing_input_receipt", {})
    blocking_fields = receipt.get("blocking_fields", []) if isinstance(receipt, dict) else []
    blocking_names = [item.get("field") for item in blocking_fields if isinstance(item, dict)]
    add_check(
        checks,
        "preflight_missing_input_receipt_is_precise",
        receipt.get("status") == "BLOCKED_UPSTREAM_BACKGROUND"
        and receipt.get("presence_check_only") is True
        and receipt.get("value_validation") == "NOT_PERFORMED"
        and receipt.get("provenance_validation") == "NOT_PERFORMED"
        and receipt.get("no_value_inference") is True
        and blocking_names == EXPECTED_MISSING_NETWORK + EXPECTED_MISSING_ITSM,
        receipt=receipt,
        load_error=load_error,
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
    }


def main() -> int:
    contract_error = None
    try:
        contract = load_contract()
        contract_validation = validate_contract(contract)
    except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
        contract = {}
        contract_error = str(exc)
        contract_validation = {
            "ok": False,
            "checks": [],
            "checks_passed": 0,
            "checks_total": 0,
        }

    contract_hash = sha256_file(CONTRACT_PATH) if CONTRACT_PATH.is_file() else "MISSING"
    preflight_validation = validate_current_preflight(contract_hash) if not contract_error else {
        "ok": False,
        "checks": [],
        "checks_passed": 0,
        "checks_total": 0,
    }
    checks = list(contract_validation["checks"]) + list(preflight_validation["checks"])
    all_ok = not contract_error and all(check["ok"] for check in checks)
    result: dict[str, Any] = {
        "schema": "ITSM_BBN001_ACTION_DERIVED_INPUT_CONTRACT_VALIDATION_v1",
        "record_type": "BBN001_ACTION_DERIVED_INPUT_CONTRACT_VALIDATION",
        "gate": "BBN-001",
        "status": "CONTRACT_VALIDATED_UPSTREAM_PHYSICS_BLOCKED" if all_ok else "ERROR_BBN001_ACTION_DERIVED_INPUT_CONTRACT",
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "contract": {
            "path": relative(CONTRACT_PATH),
            "sha256": contract_hash,
            "status": contract.get("status", "UNAVAILABLE"),
            "version": contract.get("version", "UNAVAILABLE"),
        },
        "contract_error": contract_error,
        "validation_checks_passed": sum(check["ok"] for check in checks),
        "validation_checks_total": len(checks),
        "checks": checks,
        "current_boundary": {
            "upstream_status": "BLOCKED_UPSTREAM_BACKGROUND",
            "physics_pass": False,
            "gate_effect": "NONE",
            "publication_status": "NOT_A_PHYSICS_CLAIM",
            "rule9_status": "THREE_WAY_CLEARANCE_NOT_MET",
        },
        "nonclaims": [
            "Contract validation does not supply any missing BBN or ITSM input.",
            "Field-name presence does not validate values, dimensions, provenance or numerical stability.",
            "No temperature, Q^mu, S_N, G_eff, perturbation map or likelihood is inferred.",
            "No BBN physics prediction, gate promotion, consensus clearance or publication follows.",
        ],
        "source_sha256": sha256_file(Path(__file__)),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    OUTPUT_PATH.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256").write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii", newline="\n"
    )
    print("BBN-001 action-derived input contract validation complete")
    print(f"Status: {result['status']}")
    print(f"Validation checks: {result['validation_checks_passed']}/{result['validation_checks_total']}")
    print(f"Contract SHA-256: {contract_hash}")
    print(f"Receipt validation: {preflight_validation['ok']}")
    print(f"SHA-256: {digest}")
    print(f"Output: {OUTPUT_PATH}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
