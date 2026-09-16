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


REPO_ROOT = Path(__file__).resolve().parents[3]
BACKGROUND_REL = Path("Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_summary.json")
TRAJECTORY_REL = Path("Analysis/UVIR/UVIR-003/outputs/uvir003_frw_background_trajectory.csv")
OUTPUT_PATH = Path(__file__).parent / "outputs" / "bbn001_upstream_interface_preflight_summary.json"

NETWORK_CONTRACT = {
    "time": ("t",),
    "photon_temperature": ("T_gamma", "T", "temperature"),
    "photon_temperature_derivative": ("dTdt", "dT_gamma_dt", "dTgamma_dt"),
    "neutrino_temperature": ("Tnu", "T_nu", "T_neutrino"),
    "hubble": ("H", "Hubble"),
    "baryon_density": ("nb_etaf", "n_b_eta_f", "baryon_density"),
}

ITSM_CONTRACT = {
    "physical_unit_map": ("unit_map", "units", "physical_units"),
    "baryon_normalization": ("eta", "ombh2", "Omega_b_h2", "baryon_to_photon_ratio"),
    "early_plenum_density": ("rho_plenum", "rho_P", "plenum_density", "plenum_fraction"),
    "matter_plenum_transfer": ("Q_mp", "Q_mp^0", "Q_mu", "transfer_current"),
    "reservoir_plenum_transfer": ("Q_syn", "Q_syn^0", "reservoir_current"),
    "condensate_charge_source": ("S_N", "charge_source", "number_source"),
    "effective_gravity": ("G_eff", "Geff", "effective_newton_constant"),
    "perturbation_matching": ("perturbation_matching", "boltzmann_matching", "metric_sources"),
}


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
    network = _check_contract(observed_names, NETWORK_CONTRACT)
    itsm = _check_contract(observed_names, ITSM_CONTRACT)

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
        "physics_pass": False,
        "gate_effect": "NONE",
        "publication_status": "NOT_A_PHYSICS_CLAIM",
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
        "required_next_inputs": [
            "action-derived early-time background with physical units",
            "photon temperature T_gamma(t) and dT_gamma/dt",
            "neutrino temperature and baryon-density history or a derived eta mapping",
            "distinct Q_mp^mu, Q_syn^mu and condensate-number source S_N",
            "G_eff(t) with its action-level derivation and perturbation matching contract",
            "independent review and likelihood specification before any publication claim",
        ],
        "nonclaims": [
            "No temperature is inferred from a, rho, mu or H.",
            "No condensate energy density is identified with radiation or plenum density.",
            "No Q^mu, S_N or G_eff is fitted or supplied by DeltaN.",
            "No AlterAlterBBN/PArthENoPE network run is promoted to an ITSM prediction.",
            "No gate, architecture, publication or Rule-9 status changes follow.",
        ],
    }


def main() -> int:
    result = run_preflight()
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
    return 0 if result["decision"]["action_derived_itsm_bbn_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
