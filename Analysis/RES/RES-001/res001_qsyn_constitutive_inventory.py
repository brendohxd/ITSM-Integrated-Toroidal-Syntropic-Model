#!/usr/bin/env python3
"""RES-001: Q_syn / reservoir constitutive inventory (scaffold).

LABEL: Open identity scaffold — conservation + constitutive options
GATE:  RES-001 (reservoir throughput; not a UVIR/MAT substitute)
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY

Architecture commitments (checked as text structure, not dynamics):
  div T_m = Q_mp
  div T_P = -Q_mp + Q_syn
  div T_R = -Q_syn
  sum => total covariant conservation

Does NOT: fix a creation rate law, NEC-violating fluid, H0 law, 13/12,
or identify Q_syn with S_N without declaration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    repo = base.parents[2]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--architecture",
        type=Path,
        default=repo / "Theory" / "Core" / "ITSM_Core_Architecture.md",
    )
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    return p.parse_args()


def conservation_partition() -> dict[str, Any]:
    return {
        "sectors": ["matter", "plenum", "reservoir"],
        "exchange_currents": {
            "Q_mp": "matter–plenum local exchange",
            "Q_syn": "reservoir–plenum throughput (syntropy/entropy channel)",
        },
        "identities": [
            "nabla_mu T_m^{mu nu} = Q_mp^nu",
            "nabla_mu T_P^{mu nu} = -Q_mp^nu + Q_syn^nu",
            "nabla_mu T_R^{mu nu} = -Q_syn^nu",
            "sum_sectors nabla_mu T^{mu nu} = 0",
        ],
        "separation_rule": "Q_mp is not identical to Q_syn",
        "optional_wake": (
            "If WAK Route II is chosen later, I_W appears with its own T_W; "
            "still must sum to zero with Q_mp and Q_syn"
        ),
    }


def constitutive_candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "R0_NO_THROUGHPUT_CONTROL",
            "status": "CONTROL",
            "description": "Q_syn = 0; closed plenum+matter subsystem for tests",
        },
        {
            "id": "R1_DECLARED_CONSTITUTIVE_VECTOR",
            "status": "OPEN",
            "description": (
                "Q_syn^nu = constitutive functional of declared fields "
                "(U, rho, gradients) with energy accounting"
            ),
            "forbidden": "free tunable creation rate without action/constitutive law",
        },
        {
            "id": "R2_ACTION_COUPLED_RESERVOIR",
            "status": "OPEN",
            "description": "S_R + interaction S_int[plenum, reservoir] derives Q_syn",
            "forbidden": "NEC-violating fluid as silent exact Minkowski support",
        },
        {
            "id": "R3_TOPOLOGY_LOCKED_THROUGHPUT",
            "status": "OPEN_CONDITIONAL",
            "description": (
                "Master Plan preference: lock throughput to T^3 moduli/topology "
                "rather than free generic creation — still Conditional until derived"
            ),
            "forbidden": "infer 2/3 or 13/12 from cycle counting alone",
        },
    ]


def main() -> None:
    args = parse_args()
    checks: list[dict[str, Any]] = []

    arch_text = ""
    if args.architecture.exists():
        arch_text = args.architecture.read_text(encoding="utf-8")
    checks.append(
        {
            "name": "architecture_file_present",
            "ok": len(arch_text) > 0,
        }
    )
    checks.append(
        {
            "name": "architecture_mentions_Q_syn_or_reservoir",
            "ok": ("Q_syn" in arch_text) or ("reservoir" in arch_text.lower()),
        }
    )
    checks.append(
        {
            "name": "architecture_separates_Q_mp_and_Q_syn",
            "ok": ("Q_mp" in arch_text and "Q_syn" in arch_text)
            or ("matter–plenum" in arch_text or "matter-plenum" in arch_text),
        }
    )

    part = conservation_partition()
    checks.append(
        {
            "name": "conservation_sum_identity_declared",
            "ok": any("= 0" in s for s in part["identities"]),
        }
    )
    checks.append(
        {
            "name": "Q_mp_not_identical_to_Q_syn",
            "ok": "not identical" in part["separation_rule"],
        }
    )

    cands = constitutive_candidates()
    checks.append(
        {
            "name": "candidates_include_control_and_open_routes",
            "ok": any(c["id"].startswith("R0") for c in cands)
            and any(c["status"] == "OPEN" for c in cands),
        }
    )
    checks.append(
        {
            "name": "no_candidate_marked_Derived",
            "ok": all("DERIVED" not in c["status"] for c in cands),
        }
    )

    firewall = {
        "physics_pass": False,
        "Derived_creation_rate": False,
        "Q_syn_is_S_N_automatic": False,
        "H0_from_Q_syn": False,
        "13_12_from_reservoir": False,
        "NEC_violating_Minkowski_support": False,
        "RES_research_gate_PASS": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(c["ok"] for c in checks)
    subgate = (
        "PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN"
        if all_ok
        else "FAIL_RES001_QSYN_INVENTORY"
    )

    summary: dict[str, Any] = {
        "gate": "RES-001",
        "stage": "QSYN_CONSTITUTIVE_INVENTORY",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "conservation_partition": part,
        "constitutive_candidates": cands,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Inventories reservoir throughput Q_syn as an Open identity object "
            "with total conservation bookkeeping and exclusive constitutive "
            "candidate routes. No creation-rate law or cosmology is Derived."
        ),
        "next_required": [
            "Choose R1 or R2 and write a minimal constitutive/action draft",
            "Keep R3 topology-locked throughput Conditional until derived",
            "Interface later with WAK Route I/II without double-counting currents",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "res001_qsyn_constitutive_inventory_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "res001_qsyn_constitutive_inventory_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("RES-001 Q_syn constitutive inventory")
    print("  physics_pass: False | research_gate: OPEN_SCAFFOLD_ONLY")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
