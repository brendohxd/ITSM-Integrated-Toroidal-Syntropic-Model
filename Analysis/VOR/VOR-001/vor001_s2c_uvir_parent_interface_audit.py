#!/usr/bin/env python3
"""Fail-closed VOR-001 S2c comparison with the live UVIR parent record.

This is an interface inventory, never a parent-action or physics-gate pass.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

PASS = "PASS_VOR001_UVIR_PARENT_INTERFACE_INVENTORY_OPEN"
FAIL = "FAIL_VOR001_UVIR_PARENT_INTERFACE_INVENTORY"
HOLD = "HOLD_VOR_TO_UVIR_PARENT_IDENTIFICATION_UNDECLARED"


def arguments() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vor", type=Path, default=here / "outputs" / "vor001_s2b_parent_action_template_summary.json")
    parser.add_argument("--uvir", type=Path, default=root / "Analysis" / "UVIR" / "UVIR-003" / "outputs" / "uvir003_nonlinear_adm_action_provenance_summary.json")
    parser.add_argument("--output-dir", type=Path, default=here / "outputs")
    return parser.parse_args()


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path.name)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} is not a JSON object")
    return value


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def at(data: dict[str, Any], *keys: str) -> Any:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            raise ValueError("missing " + ".".join(keys))
        value = value[key]
    return value


def validate_vor(v: dict[str, Any]) -> None:
    need(v.get("gate") == "VOR-001", "wrong VOR gate")
    need(v.get("stage") == "S2B_PARENT_ACTION_TEMPLATE", "wrong VOR stage")
    need(v.get("subgate_status") == "PASS_VOR001_S2B_PARENT_ACTION_TEMPLATE_DECLARED", "wrong VOR subgate")
    need(v.get("research_gate_status") == "OPEN_SCAFFOLD_ONLY", "VOR gate promoted")
    need(v.get("physics_pass") is False, "VOR physics_pass promoted")
    need(v.get("hold") == "HOLD_PARENT_ACTION_NOT_UVIR_VALIDATED", "VOR hold missing")
    need(at(v, "action_convention", "Phi") == "rho/sqrt(2) * exp(i*Theta)", "VOR normalization changed")
    need("no aether" in at(v, "action_convention", "D_mu").lower(), "VOR no-aether boundary missing")
    firewall = at(v, "claim_firewall")
    for key in ("physics_pass", "UVIR_parent_validated", "identified_as_ITSM_UVIR_condensate", "aether_frame_coupling", "force_law_claim", "VOR_research_gate_PASS"):
        need(firewall.get(key) is False, f"VOR firewall promoted: {key}")


def validate_uvir(u: dict[str, Any]) -> None:
    need(u.get("gate") == "UVIR-003", "wrong UVIR gate")
    need(u.get("stage") == "B_NONLINEAR_ADM_ACTION_PROVENANCE", "wrong UVIR stage")
    need(u.get("subgate_status") == "PASS_G_U_PHI_ALIGNMENT_ACTION_PROVENANCE", "wrong UVIR subgate")
    need(u.get("full_gate_status") == "IN_PROGRESS", "UVIR gate promoted")
    need(u.get("mat001_status") == "BLOCKED", "MAT-001 unblocked")
    need(u.get("full_J2_status") == "HOLD_FORCE_SECTOR_NONLINEAR_COMPLETION_REQUIRED", "force hold missing")
    parent = at(u, "symbolic_audit", "adm_parent_action")
    need("varrho" in parent.get("condensate", ""), "UVIR condensate block missing")
    need("zeta_align" in parent.get("alignment", ""), "UVIR alignment missing")
    need("U^mu=n^mu" in parent.get("gauge", ""), "UVIR frame declaration missing")
    obstruction = at(u, "symbolic_audit", "force_sector_obstructions")
    need(obstruction.get("Delta_U_covariant_completion") == "NOT_DECLARED_FOR_THE_EVOLVING_NONLINEAR_FRAME", "Delta_U hold erased")
    need(obstruction.get("analytic_cubic_vertex") == "NOT_DEFINED_BY_AN_ORDINARY_TAYLOR_EXPANSION", "nonanalytic-vertex hold erased")


def reject(name: str, mutation: Callable[[dict[str, Any], dict[str, Any]], None], vor: dict[str, Any], uvir: dict[str, Any]) -> dict[str, Any]:
    v, u = copy.deepcopy(vor), copy.deepcopy(uvir)
    mutation(v, u)
    try:
        validate_vor(v)
        validate_uvir(u)
    except (ValueError, TypeError, KeyError) as error:
        return {"case": name, "ok": True, "error": type(error).__name__}
    return {"case": name, "ok": False, "error": "mutation_not_rejected"}


def controls(v: dict[str, Any], u: dict[str, Any]) -> list[dict[str, Any]]:
    cases: list[tuple[str, Callable[[dict[str, Any], dict[str, Any]], None]]] = [
        ("vor_physics_promoted", lambda a, b: a.__setitem__("physics_pass", True)),
        ("vor_parent_identified", lambda a, b: a["claim_firewall"].__setitem__("identified_as_ITSM_UVIR_condensate", True)),
        ("vor_aether_smuggled", lambda a, b: a["action_convention"].__setitem__("D_mu", "aether covariant")),
        ("uvir_gate_promoted", lambda a, b: b.__setitem__("full_gate_status", "PASS")),
        ("mat_unblocked", lambda a, b: b.__setitem__("mat001_status", "READY")),
        ("force_hold_erased", lambda a, b: b.__setitem__("full_J2_status", "PASS")),
        ("alignment_removed", lambda a, b: b["symbolic_audit"]["adm_parent_action"].__setitem__("alignment", "")),
        ("delta_u_declared", lambda a, b: b["symbolic_audit"]["force_sector_obstructions"].__setitem__("Delta_U_covariant_completion", "COMPLETE")),
        ("cubic_vertex_claimed", lambda a, b: b["symbolic_audit"]["force_sector_obstructions"].__setitem__("analytic_cubic_vertex", "DERIVED")),
    ]
    return [reject(name, mutation, v, u) for name, mutation in cases]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError("input outside repository") from error


def main() -> None:
    args = arguments()
    root = Path(__file__).resolve().parents[3]
    try:
        vor, uvir = load(args.vor), load(args.uvir)
        validate_vor(vor)
        validate_uvir(uvir)
        sidecar = args.vor.with_suffix(".sha256")
        need(sidecar.is_file(), "VOR sidecar missing")
        vor_hash = digest(args.vor)
        need(sidecar.read_text(encoding="utf-8").split()[0].upper() == vor_hash, "VOR sidecar mismatch")
        negative = controls(vor, uvir)
        need(all(row["ok"] for row in negative), "negative control failed")
        firewall = {
            "same_parent_action": False,
            "uvir_completed_by_vor": False,
            "vor_validated_by_uvir": False,
            "mat001_unblocked": False,
            "V_computed": False,
            "stage4a_reopened": False,
            "resonance_number_derived": False,
            "a0_or_Cobs_derived": False,
            "physics_pass": False,
        }
        summary = {
            "gate": "VOR-001",
            "stage": "S2C_UVIR_PARENT_INTERFACE_INVENTORY",
            "calculation_status": "PASS",
            "subgate_status": PASS,
            "research_gate_status": "OPEN_SCAFFOLD_ONLY",
            "physics_pass": False,
            "hold": HOLD,
            "inputs": {
                "vor_s2b": {"path": relative(args.vor, root), "sha256": vor_hash, "sidecar_verified": True},
                "uvir_parent": {"path": relative(args.uvir, root), "sha256": digest(args.uvir), "sidecar_verified": False, "note": "hash pinned here; no upstream sidecar"},
            },
            "shared_conventions": {"complex_polar_field": True, "amplitude_phase_split": True, "action_identity_established": False},
            "unresolved_bridges": {
                "common_background_and_chart": "NOT_DECLARED",
                "potential_parameter_map": "NOT_DECLARED",
                "finite_density_ensemble_map": "NOT_DECLARED",
                "aether_alignment_in_vor": "ABSENT_BY_TEMPLATE_SCOPE",
                "compact_winding_on_live_uvir_background": "NOT_COMPUTED",
                "phi_to_psi_interaction": "NOT_DERIVED",
                "matter_vertex": "NOT_DERIVED",
            },
            "negative_controls": negative,
            "claim_firewall": firewall,
            "scientific_boundary": "The records share a compatible polar complex-field convention only; their parent actions, backgrounds, frame/alignment content, compact winding realization and force/matter interfaces are not identified.",
            "next_required": ["declare one common parent action and finite-density ensemble", "derive compact winding on that background", "derive any Phi-psi or matter interaction", "repeat stability and energy accounting before promotion"],
        }
        need(all(value is False for value in firewall.values()), "firewall must remain false")
        args.output_dir.mkdir(parents=True, exist_ok=True)
        output = args.output_dir / "vor001_s2c_uvir_parent_interface_summary.json"
        payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
        output.write_bytes(payload)
        output_hash = hashlib.sha256(payload).hexdigest().upper()
        output.with_suffix(".sha256").write_text(f"{output_hash}  {output.name}\n", encoding="utf-8", newline="\n")
        print("physics_pass: False")
        print("action_identity_established: False")
        print("negative_controls:", len(negative))
        print("STATUS:", PASS)
        print("JSON_SHA256:", output_hash)
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        print("STATUS:", FAIL)
        print("ERROR:", f"{type(error).__name__}: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
