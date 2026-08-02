#!/usr/bin/env python3
"""Delete ITSM recovery *gate-segment* Zenodo deposits (declutter).

Policy: archive **papers** on Zenodo, not every gate substep progression.
This script removes the CBR-001 / UVIR-003 / claim-hygiene *segment* records
created during recovery packaging — drafts via DELETE, published records via
discard if API allows (owner delete).

  $env:ZENODO_TOKEN = '...'   # never commit
  python Scripts/zenodo/scrap_gate_deposits.py
  python Scripts/zenodo/scrap_gate_deposits.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

API = "https://zenodo.org/api"

# Known segment deposits from 2026-08-02 recovery packaging
# (drafts + published v1 + new-version drafts)
DEPOSIT_IDS = [
    21745260,  # CBR-001 published v1
    21745270,  # UVIR-003 published v1
    21745276,  # claim hygiene draft
    21753798,  # CBR-001 new-version draft
    21753799,  # UVIR-003 new-version draft
]


def require_token() -> str:
    token = os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")
    if not token:
        print(
            "[!] ZENODO_TOKEN not set. Set it then re-run, or delete manually in UI:\n"
            "    https://zenodo.org/me/uploads\n"
            "    Targets: " + ", ".join(str(i) for i in DEPOSIT_IDS),
            file=sys.stderr,
        )
        sys.exit(2)
    return token


def get_dep(token: str, dep_id: int) -> dict | None:
    r = requests.get(
        f"{API}/deposit/depositions/{dep_id}",
        params={"access_token": token},
        timeout=60,
    )
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        raise RuntimeError(f"GET {dep_id}: {r.status_code} {r.text[:300]}")
    return r.json()


def delete_dep(token: str, dep_id: int) -> str:
    r = requests.delete(
        f"{API}/deposit/depositions/{dep_id}",
        params={"access_token": token},
        timeout=60,
    )
    if r.status_code in (204, 200, 202):
        return "deleted"
    if r.status_code == 404:
        return "already_gone"
    return f"failed:{r.status_code}:{r.text[:200]}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        default=None,
        help="Override default deposit ID list",
    )
    parser.add_argument(
        "--results-json",
        type=Path,
        default=Path("releases/zenodo/2026-08-02/ZENODO_SCRAP_RESULTS.json"),
    )
    args = parser.parse_args()
    ids = args.ids or DEPOSIT_IDS

    if args.dry_run:
        token = os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")
        if not token:
            print("[dry-run] no token — would attempt delete for:", ids)
            return
        for dep_id in ids:
            d = get_dep(token, dep_id)
            if d is None:
                print(f"[dry-run] {dep_id}: not found")
            else:
                print(
                    f"[dry-run] {dep_id}: state={d.get('state')} "
                    f"submitted={d.get('submitted')} title={(d.get('title') or '')[:50]}"
                )
        return

    token = require_token()
    results = []
    for dep_id in ids:
        d = get_dep(token, dep_id)
        if d is None:
            print(f"[*] {dep_id}: already gone")
            results.append({"id": dep_id, "status": "already_gone"})
            continue
        title = (d.get("title") or d.get("metadata", {}).get("title") or "")[:60]
        print(f"[*] Deleting {dep_id} ({d.get('state')}) {title}...")
        status = delete_dep(token, dep_id)
        print(f"    -> {status}")
        results.append(
            {
                "id": dep_id,
                "status": status,
                "was_state": d.get("state"),
                "was_submitted": d.get("submitted"),
                "title": title,
            }
        )

    args.results_json.parent.mkdir(parents=True, exist_ok=True)
    args.results_json.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"\n[+] Wrote {args.results_json}")
    print(
        "Policy: future Zenodo uploads should be **paper packages** "
        "(P1/P2/…), not every UVIR/CBR gate micro-slice."
    )


if __name__ == "__main__":
    main()
