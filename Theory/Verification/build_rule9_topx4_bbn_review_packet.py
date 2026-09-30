#!/usr/bin/env python3
"""Assemble a local Rule-9 review packet for the current TOP-X4/BBN boundary.

The packet is evidence preparation only.  It records hashes, role-separated
review prompts and unresolved questions, but it never assigns reviewers,
creates consensus or promotes a gate.  The fixed artifact list is deliberate:
the packet should fail visibly if an authoritative receipt or sidecar is
missing rather than silently shrinking its review scope.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "Theory" / "Verification"
OUTPUT_MD_PATH = OUTPUT_DIR / "ITSM_RULE9_TOPX4_BBN_REVIEW_PACKET_2026-09-16.md"
OUTPUT_JSON_PATH = OUTPUT_DIR / "ITSM_RULE9_TOPX4_BBN_REVIEW_PACKET_2026-09-16.json"

AUTHORITY_FILES = [
    ("Core operating rules", "GEMINI.md"),
    ("Canonical identity briefing", "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md"),
    ("Master research plan", "Theory/Core/ITSM_Master_Research_Plan.md"),
    ("Recovery execution queue", "Theory/Core/ITSM_Recovery_Execution_Queue.md"),
    ("Active research dashboard", "active_research.md"),
    ("Recovery branch guide", "RECOVERY_BRANCH_README.md"),
    (
        "TOP-X4 Plan 11 parent freeze",
        "Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
    ),
    (
        "TOP-X4 Plan 11 calculation plan",
        "Theory/Core/Reasoning_Mode_Plans/11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md",
    ),
    (
        "TOP-X4 Dirac/parity/anomaly contract",
        "Theory/Gates/TOP-X4/TOPX4_S2F3_DIRAC_PARITY_ANOMALY_READINESS_CONTRACT_2026-09-16.md",
    ),
    (
        "TOP-X4 scoped curved Dirac-operator contract",
        "Theory/Gates/TOP-X4/TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT_2026-09-16.md",
    ),
    (
        "BBN-001 action-derived input contract",
        "Analysis/Cosmology/BBN-001/bbn001_action_derived_input_contract.json",
    ),
]

RECEIPT_FILES = [
    ("TOP-X4 static determinant JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_static_determinant_summary.json"),
    ("TOP-X4 static determinant receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_STATIC_CHECKPOINT_RECEIPT_2026-09-09.md"),
    ("TOP-X4 finite-charge operator JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_finite_charge_operator_summary.json"),
    ("TOP-X4 finite-charge operator receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_FINITE_CHARGE_OPERATOR_CHECKPOINT_2026-09-12.md"),
    ("TOP-X4 dynamic state JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dynamic_state_subtraction_summary.json"),
    ("TOP-X4 dynamic state receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT_2026-09-12.md"),
    ("TOP-X4 exact transport JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_exact_transport_retry_summary.json"),
    ("TOP-X4 exact transport receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_EXACT_TRANSPORT_RETRY_CHECKPOINT_2026-09-12.md"),
    ("TOP-X4 D5 readiness JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_hadamard_subtraction_readiness_summary.json"),
    ("TOP-X4 D5 readiness receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_HADAMARD_SUBTRACTION_READINESS_2026-09-12.md"),
    ("TOP-X4 covariant scalar JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_covariant_scalar_matrix_summary.json"),
    ("TOP-X4 covariant scalar receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_COVARIANT_SCALAR_MATRIX_CHECKPOINT_2026-09-12.md"),
    ("TOP-X4 scalar parametrix JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json"),
    ("TOP-X4 scalar parametrix receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CHECKPOINT_2026-09-12.md"),
    ("TOP-X4 global scalar state JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_global_state_construction_summary.json"),
    ("TOP-X4 global scalar state receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_GLOBAL_STATE_CONSTRUCTION_2026-09-16.md"),
    ("TOP-X4 physical Hessian JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_physical_hessian_readiness_summary.json"),
    ("TOP-X4 physical Hessian receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_PHYSICAL_HESSIAN_READINESS_2026-09-16.md"),
    ("TOP-X4 Dirac/parity/anomaly JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dirac_parity_anomaly_readiness_summary.json"),
    ("TOP-X4 Dirac/parity/anomaly receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_DIRAC_PARITY_ANOMALY_READINESS_2026-09-16.md"),
    ("TOP-X4 scoped curved Dirac-operator JSON", "Analysis/TOP/TOP-X4/outputs/topx4_s2f3_curved_dirac_operator_summary.json"),
    ("TOP-X4 scoped curved Dirac-operator receipt", "Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_CURVED_DIRAC_OPERATOR_2026-09-16.md"),
    ("BBN-001 upstream preflight JSON", "Analysis/Cosmology/BBN-001/outputs/bbn001_upstream_interface_preflight_summary.json"),
    ("BBN-001 contract validation JSON", "Analysis/Cosmology/BBN-001/outputs/bbn001_action_derived_input_contract_summary.json"),
]

HISTORICAL_FILES = [
    (
        "Historical Rule-9 synthesis (context only; not current TOP-X4 clearance)",
        "Theory/Verification/TRIANGULATED_CONSENSUS_SYNTHESIS_REPORT.md",
    )
]

REVIEW_ROLES = [
    {
        "role": "Role A",
        "title": "Mathematical and dimensional auditor",
        "reviewer_status": "NOT_ASSIGNED",
        "report_status": "NOT_RECEIVED",
        "prompt": (
            "Independently inspect the frozen actions, operator conventions, "
            "dimensions, state boundaries, BBN field semantics and the "
            "Dirac/parity/anomaly contract. Recompute or symbolically check "
            "any claimed bounded identity that is in scope. Identify missing "
            "operator, phase, spin-structure, anomaly or unit information. "
            "Do not infer a value and do not promote any gate."
        ),
    },
    {
        "role": "Role B",
        "title": "Numerical and pipeline auditor",
        "reviewer_status": "NOT_ASSIGNED",
        "report_status": "NOT_RECEIVED",
        "prompt": (
            "Independently replay the registered executables, verify JSON "
            "byte identity and SHA-256 sidecars, and exercise the declared "
            "negative/rejection controls. Check that the BBN preflight is "
            "presence-only and that the TOP-X4 readiness audit does not "
            "silently substitute static, finite-order or parity-even data. "
            "Report environment limits and any mismatch; do not repair or "
            "reinterpret a failing receipt inside the review."
        ),
    },
    {
        "role": "Role C",
        "title": "Claim-hygiene and gate-ledger auditor",
        "reviewer_status": "NOT_ASSIGNED",
        "report_status": "NOT_RECEIVED",
        "prompt": (
            "Compare the receipts against the canonical identity, active "
            "research dashboard, recovery queue and publication firewall. "
            "Check every Derived/Conditional/Open/Rejected boundary, the "
            "BBN CONTROL_ONLY and upstream hold, TOP-X4 physics_pass=false, "
            "and the absence of Rule-9 self-certification. Flag any status "
            "divergence or downstream claim. Do not clear Rule-9 without "
            "independent Role A and Role B reports and a final cross-check."
        ),
    },
]

UNRESOLVED_QUESTIONS = [
    "The Hamiltonian-form curved five-dimensional Dirac operator and homogeneous spin connection are now derived on the registered metric; can this be extended to the complete finite-charge background, state domain and normalization required by the determinant?",
    "What dimension-appropriate infinite-order Dirac Hadamard construction supplies the state and wavefront conditions required for stress renormalization?",
    "What regulator/reference phase and spin-structure data define the parity-odd determinant, including any spectral-flow or global contribution?",
    "Which local/global anomaly terms occur for the frozen field content, and what quantized counterterms cancel them without importing an external result?",
    "Can the BBN interface receive physical T_gamma, dT_gamma/dt, T_nu, H, baryon normalization, plenum density, Q_mp^mu, Q_syn^mu, S_N, G_eff and perturbation matching from one action-derived chart?",
    "Have all receipt hashes, sidecars and role-separated reports been independently compared against the current canonical documents?",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def artifact_record(label: str, relative_path: str, sidecar_required: bool) -> dict[str, Any]:
    path = REPO_ROOT / Path(relative_path)
    exists = path.is_file()
    actual = sha256_file(path) if exists else "MISSING"
    sidecar_path = Path(str(path) + ".sha256")
    expected = "NOT_REQUIRED" if not sidecar_required else "MISSING"
    if sidecar_required and sidecar_path.is_file():
        tokens = sidecar_path.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    sidecar_matches = not sidecar_required or (exists and actual == expected)
    return {
        "label": label,
        "path": relative(path),
        "exists": exists,
        "sha256": actual,
        "sidecar_required": sidecar_required,
        "sidecar_sha256": expected,
        "sidecar_matches": sidecar_matches,
    }


def build_manifest() -> dict[str, Any]:
    authority = [artifact_record(label, path, sidecar_required=False) for label, path in AUTHORITY_FILES]
    receipts = [artifact_record(label, path, sidecar_required=True) for label, path in RECEIPT_FILES]
    historical = [artifact_record(label, path, sidecar_required=False) for label, path in HISTORICAL_FILES]
    all_records = authority + receipts + historical
    return {
        "schema": "ITSM_RULE9_TOPX4_BBN_REVIEW_PACKET_v1",
        "record_type": "ITSM_RULE9_LOCAL_REVIEW_PACKET",
        "date": "2026-09-16",
        "branch": "recovery/v12-core-architecture",
        "scope": "Local evidence preparation for independent Rule-9 review of current TOP-X4 and BBN boundaries.",
        "packet_status": "READY_FOR_INDEPENDENT_REVIEW_ONLY" if all(item["exists"] and item["sidecar_matches"] for item in all_records) else "PACKET_INCOMPLETE",
        "rule9_status": "THREE_WAY_CLEARANCE_NOT_MET",
        "review_protocol": [
            "Frame: assign one reviewer to each role and provide this manifest and the listed artifacts.",
            "Compare: each role independently checks its prompt, hashes and bounded results, then records disagreements.",
            "Decide: only after all three reports are present may the roles be cross-checked against canonical sources; this packet itself cannot clear Rule-9.",
        ],
        "authority_artifacts": authority,
        "receipt_artifacts": receipts,
        "historical_context_artifacts": historical,
        "review_roles": REVIEW_ROLES,
        "unresolved_questions": UNRESOLVED_QUESTIONS,
        "current_boundary": {
            "MAT-001": "BLOCKED",
            "K_Q": "NOT_DERIVED",
            "V": "NOT_COMPUTED",
            "UVIR-003": "IN_PROGRESS",
            "BBN-001": "CONTROL_ONLY_AND_BLOCKED_UPSTREAM",
            "TOP-X4": "PHYSICS_PASS_FALSE",
            "physics_pass": False,
            "gate_effect": "NONE",
            "publication_status": "NOT_A_PHYSICS_CLAIM_FOR_THIS_PACKET",
            "external_review_dispatch": "NOT_PERFORMED",
        },
        "nonclaims": [
            "No reviewer is assigned or represented by this local packet.",
            "No three-way consensus or Rule-9 clearance is claimed.",
            "No missing action-derived input, Dirac state, parity phase, anomaly term, counterterm, stress or Hessian is inferred.",
            "No physics gate, publication, A4 or Ultra status changes follow.",
        ],
        "source_sha256": sha256_file(Path(__file__)),
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Local Rule-9 TOP-X4/BBN evidence and review packet",
        "",
        "**Date:** 2026-09-16  ",
        "**Branch:** `recovery/v12-core-architecture`  ",
        "**Packet status:** `" + manifest["packet_status"] + "`  ",
        "**Rule-9 status:** `THREE_WAY_CLEARANCE_NOT_MET`  ",
        "**External review dispatch:** `NOT_PERFORMED`",
        "",
        "## 1. Purpose and binding boundary",
        "",
        "This is a local evidence-preparation packet for independent review of",
        "the current TOP-X4 and BBN-001 recovery boundaries. It is not a review",
        "report, a consensus record or a publication package. The historical",
        "triangulated synthesis listed below is context only and does not clear",
        "the current TOP-X4/BBN receipts.",
        "",
        "The packet preserves `MAT-001=BLOCKED`, `K_Q=NOT_DERIVED`,",
        "`V=NOT_COMPUTED`, `UVIR-003=IN_PROGRESS`, BBN-001's control/upstream",
        "hold, `physics_pass=false` and `gate_effect=NONE`. No independent",
        "reviewer has been assigned by this artifact.",
        "",
        "## 2. Review protocol",
        "",
    ]
    for step in manifest["review_protocol"]:
        lines.append("- " + step)
    lines.extend(["", "## 3. Role-separated review prompts", ""])
    lines.extend([
        "| Role | Reviewer | Report | Prompt |",
        "|---|---|---|---|",
    ])
    for role in manifest["review_roles"]:
        prompt = role["prompt"].replace("|", "\\|")
        lines.append(f"| {role['role']} — {role['title']} | `{role['reviewer_status']}` | `{role['report_status']}` | {prompt} |")
    lines.extend(["", "No role is self-certified here. A missing report is a failed Rule-9 prerequisite, not an implied pass.", "", "## 4. Unresolved questions", ""])
    for question in manifest["unresolved_questions"]:
        lines.append("- " + question)
    lines.extend(["", "## 5. Current status firewall", "", "| Item | Binding status |", "|---|---|"])
    for key, value in manifest["current_boundary"].items():
        lines.append(f"| `{key}` | `{str(value).lower() if isinstance(value, bool) else value}` |")
    lines.extend(["", "No BBN input, `Q^mu`, `S_N`, `G_eff`, perturbation matching, Dirac completion, parity phase, anomaly cancellation, quantized counterterm, determinant, stress, physical Hessian, gate promotion or publication claim is inferred from this packet.", "", "## 6. Authoritative source documents", "", "| Label | Path | SHA-256 |", "|---|---|---|"])
    for item in manifest["authority_artifacts"]:
        lines.append(f"| {item['label']} | `{item['path']}` | `{item['sha256']}` |")
    lines.extend(["", "## 7. Authoritative receipt manifest", "", "All receipt entries below require a matching `.sha256` sidecar. `sidecar_matches` is recorded in the machine-readable manifest.", "", "| Label | Path | SHA-256 | Sidecar |", "|---|---|---|---|"])
    for item in manifest["receipt_artifacts"]:
        sidecar_status = "MATCH" if item["sidecar_matches"] else "MISMATCH_OR_MISSING"
        lines.append(f"| {item['label']} | `{item['path']}` | `{item['sha256']}` | `{sidecar_status}` |")
    lines.extend(["", "## 8. Historical context (not current clearance)", "", "The following document records an earlier audit context. It is not treated as independent review of the current TOP-X4 or BBN packet:", "", "| Label | Path | SHA-256 | Sidecar |", "|---|---|---|---|"])
    for item in manifest["historical_context_artifacts"]:
        sidecar_status = "MATCH" if item["sidecar_matches"] else "MISMATCH_OR_MISSING"
        lines.append(f"| {item['label']} | `{item['path']}` | `{item['sha256']}` | `{sidecar_status}` |")
    lines.extend(["", "## 9. Final decision", "", "```text", "THREE_WAY_CLEARANCE_NOT_MET", "physics_pass=false", "gate_effect=NONE", "external_review_dispatch=NOT_PERFORMED", "```", "", "This packet is complete only as a local handoff surface. It must not be cited as Role A, Role B or Role C review, and it must not be used to promote any scientific or publication gate.", ""])
    return "\n".join(lines)


def write_with_sidecar(path: Path, payload: bytes) -> str:
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{digest}  {path.name}\n", encoding="ascii", newline="\n"
    )
    return digest


def main() -> int:
    manifest = build_manifest()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_payload = (json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    json_digest = write_with_sidecar(OUTPUT_JSON_PATH, json_payload)
    markdown_payload = render_markdown(manifest).encode("utf-8")
    markdown_digest = write_with_sidecar(OUTPUT_MD_PATH, markdown_payload)
    print(f"packet_status={manifest['packet_status']}")
    print("rule9_status=THREE_WAY_CLEARANCE_NOT_MET")
    print(f"authority_artifacts={len(manifest['authority_artifacts'])}")
    print(f"receipt_artifacts={len(manifest['receipt_artifacts'])}")
    print(f"json_sha256={json_digest}")
    print(f"markdown_sha256={markdown_digest}")
    print(f"json_output={OUTPUT_JSON_PATH}")
    print(f"markdown_output={OUTPUT_MD_PATH}")
    return 0 if manifest["packet_status"] == "READY_FOR_INDEPENDENT_REVIEW_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
