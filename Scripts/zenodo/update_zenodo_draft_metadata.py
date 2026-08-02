#!/usr/bin/env python3
"""Update Zenodo deposit metadata (inclusive descriptions, ORCID, website).

- Unsubmitted drafts: PUT metadata in place.
- Already published records: create a *new version* draft, then PUT metadata
  (does not publish the new version).

  $env:ZENODO_TOKEN = '...'   # never commit; rotate if exposed
  python Scripts/zenodo/update_zenodo_draft_metadata.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zenodo_deposit_metadata import DEPOSITS  # noqa: E402

API = "https://zenodo.org/api"


def require_token() -> str:
    token = os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")
    if not token:
        print(
            "[!] ZENODO_TOKEN not set.\n"
            "    $env:ZENODO_TOKEN = 'your_token'\n"
            "    Token needs deposit:write (+ deposit:actions for newversion).",
            file=sys.stderr,
        )
        sys.exit(2)
    return token


def get_deposition(token: str, dep_id: int) -> dict:
    r = requests.get(
        f"{API}/deposit/depositions/{dep_id}",
        params={"access_token": token},
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"GET {dep_id} failed: {r.status_code} {r.text}")
    return r.json()


def put_metadata(token: str, dep_id: int, metadata: dict) -> dict:
    current = get_deposition(token, dep_id)
    if current.get("submitted") or current.get("state") == "done":
        raise RuntimeError(
            f"Deposition {dep_id} is published; use newversion first."
        )
    new_meta = dict(current.get("metadata") or {})
    # Replace with our authoritative inclusive metadata fields
    for key, value in metadata.items():
        new_meta[key] = value
    r = requests.put(
        f"{API}/deposit/depositions/{dep_id}",
        params={"access_token": token},
        data=json.dumps({"metadata": new_meta}),
        headers={"Content-Type": "application/json"},
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"PUT {dep_id} failed: {r.status_code} {r.text}")
    return r.json()


def open_new_version(token: str, dep_id: int) -> dict:
    """Create a new version draft from a published deposition; return draft."""
    r = requests.post(
        f"{API}/deposit/depositions/{dep_id}/actions/newversion",
        params={"access_token": token},
        timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(
            f"newversion {dep_id} failed: {r.status_code} {r.text}"
        )
    body = r.json()
    # Prefer latest_draft link
    draft_url = (body.get("links") or {}).get("latest_draft")
    if not draft_url:
        # Sometimes API returns the concept with links
        raise RuntimeError(f"newversion response missing latest_draft: {body}")
    r2 = requests.get(draft_url, params={"access_token": token}, timeout=60)
    if r2.status_code != 200:
        raise RuntimeError(
            f"GET latest_draft failed: {r2.status_code} {r2.text}"
        )
    return r2.json()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--which",
        nargs="+",
        choices=list(DEPOSITS.keys()) + ["all"],
        default=["all"],
    )
    parser.add_argument(
        "--results-json",
        type=Path,
        default=Path("releases/zenodo/2026-08-02/ZENODO_METADATA_UPDATE.json"),
    )
    args = parser.parse_args()
    keys = list(DEPOSITS.keys()) if "all" in args.which else args.which
    token = require_token()

    results = []
    for key in keys:
        spec = DEPOSITS[key]
        dep_id = int(spec["deposition_id"])
        current = get_deposition(token, dep_id)
        published = bool(current.get("submitted") or current.get("state") == "done")
        target_id = dep_id
        action = "update_draft"

        if published:
            print(f"[*] {key} id={dep_id} is published — opening new version draft...")
            draft = open_new_version(token, dep_id)
            target_id = int(draft["id"])
            action = "new_version_draft"
            print(f"    new draft id={target_id}")
        else:
            print(f"[*] {key} id={dep_id} is unsubmitted — updating metadata...")

        updated = put_metadata(token, target_id, spec["metadata"])
        meta = updated.get("metadata") or {}
        creators = meta.get("creators") or []
        orcid = creators[0].get("orcid") if creators else None
        print(f"    title: {meta.get('title', '')[:72]}...")
        print(f"    orcid: {orcid}")
        print(f"    related_identifiers: {len(meta.get('related_identifiers') or [])}")
        print(f"    html: https://zenodo.org/uploads/{target_id}")
        print(f"    published: False (draft only)")

        results.append(
            {
                "key": key,
                "source_deposition_id": dep_id,
                "updated_deposition_id": target_id,
                "action": action,
                "title": meta.get("title"),
                "orcid": orcid,
                "version": meta.get("version"),
                "related_identifiers": meta.get("related_identifiers"),
                "html": f"https://zenodo.org/uploads/{target_id}",
                "published": False,
            }
        )
        # Keep module deposition_id as the live draft for later updates
        spec["deposition_id"] = target_id

    args.results_json.parent.mkdir(parents=True, exist_ok=True)
    args.results_json.write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    # Write pointer file for latest draft IDs
    pointers = {
        row["key"]: {
            "deposition_id": row["updated_deposition_id"],
            "html": row["html"],
            "action": row["action"],
        }
        for row in results
    }
    ptr_path = args.results_json.parent / "ZENODO_LATEST_DRAFTS.json"
    ptr_path.write_text(json.dumps(pointers, indent=2) + "\n", encoding="utf-8")
    print(f"\n[+] Wrote {args.results_json}")
    print(f"[+] Wrote {ptr_path}")


if __name__ == "__main__":
    main()
