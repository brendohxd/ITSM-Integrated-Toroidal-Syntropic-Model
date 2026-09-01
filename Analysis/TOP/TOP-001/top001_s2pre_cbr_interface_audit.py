#!/usr/bin/env python3
"""TOP-001 S2-pre: CBR-001 interface map (fixed rectangular T^3, template only).

LABEL: mathematical-template-only / Conditional interface
GATE:  TOP-001 Stage S2-pre (CBR interface, not modulus action)
CLAIM: none Derived; physics_pass always false
STATUS: OPEN_SCAFFOLD_ONLY

Natural next task after S1 triaxial geometry (IDENTITY checkpoint):
  a carefully scoped CBR-001 interface without target packaging.

What this package does
----------------------
1. Declares the TOP→CBR handoff object: (L1,L2,L3) or fixed-V log-shape alphas.
2. Builds the periodic free-scalar mode lattice k_n = 2π n_i / L_i.
3. Checks biaxial reduction, triaxial covariance, volume scale invariance of
   dimensionless shape diagnostics.
4. Records that free Casimir stress evaluation is owned by CBR-001 tools;
   TOP owns only geometry / BC declaration.

Does NOT:
  - recompute renormalized Casimir energy/stress (CBR-001 owns that)
  - introduce S_mod or dynamical moduli potential
  - prefer twisted E2/E3
  - insert 13/12, H0, a0, C_obs, or driven anisotropy
  - claim TOP research-gate PASS
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

TWO_PI = 2.0 * math.pi


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--V", type=float, default=1.0)
    p.add_argument("--n-max", type=int, default=5)
    return p.parse_args()


def lengths_from_log_shape(V: float, ax: float, ay: float) -> tuple[float, float, float]:
    az = -(ax + ay)
    L = V ** (1.0 / 3.0)
    return L * math.exp(ax), L * math.exp(ay), L * math.exp(az)


def mode_lattice_moments(
    lengths: tuple[float, float, float], n_max: int
) -> dict[str, float]:
    L1, L2, L3 = lengths
    sum_k2 = 0.0
    sum_k2_x = 0.0
    sum_k2_y = 0.0
    sum_k2_z = 0.0
    count = 0
    for n1 in range(-n_max, n_max + 1):
        for n2 in range(-n_max, n_max + 1):
            for n3 in range(-n_max, n_max + 1):
                if n1 == 0 and n2 == 0 and n3 == 0:
                    continue
                kx = TWO_PI * n1 / L1
                ky = TWO_PI * n2 / L2
                kz = TWO_PI * n3 / L3
                k2 = kx * kx + ky * ky + kz * kz
                sum_k2 += k2
                sum_k2_x += kx * kx
                sum_k2_y += ky * ky
                sum_k2_z += kz * kz
                count += 1
    inv = 1.0 / float(count)
    return {
        "n_modes": float(count),
        "mean_k2": sum_k2 * inv,
        "frac_kx2": (sum_k2_x / sum_k2) if sum_k2 > 0 else float("nan"),
        "frac_ky2": (sum_k2_y / sum_k2) if sum_k2 > 0 else float("nan"),
        "frac_kz2": (sum_k2_z / sum_k2) if sum_k2 > 0 else float("nan"),
        "anisotropy_A": float(
            max(sum_k2_x, sum_k2_y, sum_k2_z) / min(sum_k2_x, sum_k2_y, sum_k2_z) - 1.0
            if min(sum_k2_x, sum_k2_y, sum_k2_z) > 0
            else float("nan")
        ),
    }


def main() -> None:
    args = parse_args()
    if not math.isfinite(args.V) or args.V <= 0:
        raise SystemExit("V must be positive finite")
    if args.n_max < 1:
        raise SystemExit("n_max >= 1 required")

    checks: list[dict[str, Any]] = []

    # Cubic control
    Lc = lengths_from_log_shape(args.V, 0.0, 0.0)
    vol_ok = abs(Lc[0] * Lc[1] * Lc[2] - args.V) < 1e-12 * args.V
    checks.append({"name": "cubic_volume", "ok": vol_ok, "L": Lc})
    mc = mode_lattice_moments(Lc, args.n_max)
    cubic_iso = abs(mc["frac_kx2"] - 1.0 / 3.0) < 1e-9
    checks.append(
        {
            "name": "cubic_mode_fractions_isotropic",
            "ok": cubic_iso and mc["anisotropy_A"] < 1e-9,
            "moments": mc,
        }
    )

    # Biaxial reduction (alpha_x = -alpha_y, alpha_z = 0)  => Lx,Ly vary, Lz fixed
    a = 0.15
    Lb = lengths_from_log_shape(args.V, a, -a)
    checks.append(
        {
            "name": "biaxial_volume",
            "ok": abs(Lb[0] * Lb[1] * Lb[2] - args.V) < 1e-12 * args.V,
            "L": Lb,
        }
    )
    mb = mode_lattice_moments(Lb, args.n_max)
    checks.append(
        {
            "name": "biaxial_anisotropy_positive",
            "ok": mb["anisotropy_A"] > 1e-6,
            "A": mb["anisotropy_A"],
        }
    )

    # Full triaxial
    Lt = lengths_from_log_shape(args.V, 0.2, -0.05)
    checks.append(
        {
            "name": "triaxial_volume",
            "ok": abs(Lt[0] * Lt[1] * Lt[2] - args.V) < 1e-12 * args.V,
            "L": Lt,
        }
    )
    mt = mode_lattice_moments(Lt, args.n_max)
    checks.append(
        {
            "name": "triaxial_anisotropy_positive",
            "ok": mt["anisotropy_A"] > mb["anisotropy_A"] * 0.1,
            "A": mt["anisotropy_A"],
        }
    )

    # Permutation covariance of A
    perms = [
        (Lt[0], Lt[1], Lt[2]),
        (Lt[1], Lt[2], Lt[0]),
        (Lt[2], Lt[0], Lt[1]),
    ]
    A_vals = [mode_lattice_moments(p, args.n_max)["anisotropy_A"] for p in perms]
    checks.append(
        {
            "name": "anisotropy_permutation_invariant",
            "ok": max(A_vals) - min(A_vals) < 1e-12,
            "A_vals": A_vals,
        }
    )

    # Scale invariance of A and fractions under V -> 8V, same alphas
    L8 = lengths_from_log_shape(8.0 * args.V, 0.2, -0.05)
    m8 = mode_lattice_moments(L8, args.n_max)
    checks.append(
        {
            "name": "shape_diagnostics_volume_scale_invariant",
            "ok": abs(m8["anisotropy_A"] - mt["anisotropy_A"]) < 1e-12
            and abs(m8["frac_kx2"] - mt["frac_kx2"]) < 1e-12,
        }
    )

    # Interface contract
    interface = {
        "TOP_owns": [
            "rectangular_T3_side_lengths_L_i",
            "optional_fixed_volume_log_shape_alphas",
            "BC_class_declaration_default_periodic",
        ],
        "CBR001_owns": [
            "renormalized_free_scalar_Casimir_stress",
            "biaxial_or_triaxial_stress_scan",
            "free_field_backreaction_negative_13_12_result",
        ],
        "handoff_object": {
            "primary": "(L1, L2, L3)",
            "equivalent_fixed_V": "(V, alpha_x, alpha_y) with sum alpha_i = 0",
            "mode_lattice_template": "k_i = 2*pi*n_i/L_i, n in Z^3 \\ {0}",
        },
        "forbidden_smuggling": [
            "insert_13_12_into_modulus_potential",
            "claim_persistent_free_field_attractor",
            "derive_a0_or_Cobs_from_shape_alone",
            "prefer_twisted_BC_without_energy_comparison",
        ],
        "status": "INTERFACE_DECLARED_TEMPLATE_ONLY",
    }
    checks.append(
        {
            "name": "interface_declared_without_casimir_recompute",
            "ok": interface["status"] == "INTERFACE_DECLARED_TEMPLATE_ONLY",
        }
    )

    firewall = {
        "physics_pass": False,
        "Derived_topology": False,
        "Derived_Casimir_from_this_package": False,
        "persistent_13_12": False,
        "H0_72_97": False,
        "a0_from_topology": False,
        "Cobs_from_topology": False,
        "modulus_action_S_mod": False,
        "twisted_preference": False,
        "TOP_research_gate_PASS": False,
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
        "PASS_TOP001_S2PRE_CBR_INTERFACE_TEMPLATE"
        if all_ok
        else "FAIL_TOP001_S2PRE_CBR_INTERFACE"
    )

    summary: dict[str, Any] = {
        "gate": "TOP-001",
        "stage": "S2PRE_CBR_INTERFACE",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "claim_status": "Conditional_interface_template",
        "parameters": {"V": args.V, "n_max": args.n_max},
        "samples": {
            "cubic": {"L": Lc, "moments": mc},
            "biaxial": {"L": Lb, "moments": mb},
            "triaxial": {"L": Lt, "moments": mt},
        },
        "cbr001_interface": interface,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Declares TOP→CBR-001 geometry handoff and free-scalar mode lattice "
            "diagnostics on fixed rectangular T^3. Does not evaluate Casimir "
            "stress, does not write S_mod, does not restore 13/12 packaging."
        ),
        "next_required": [
            "Optional: call CBR-001 lattice tools with declared (L1,L2,L3) samples",
            "S2: modulus action only after firewall review of any potential",
            "Twisted BC only after energy/stability comparison (not Derived yet)",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "top001_s2pre_cbr_interface_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "top001_s2pre_cbr_interface_summary.sha256").write_bytes(
        f"{h}  {out.name}\n".encode("utf-8")
    )

    print("TOP-001 S2-pre CBR interface")
    print("  physics_pass: False | research_gate: OPEN_SCAFFOLD_ONLY")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
