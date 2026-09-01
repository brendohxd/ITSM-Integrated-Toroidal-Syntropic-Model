#!/usr/bin/env python3
"""Inventory and compare all repository documentation against local main.

This is a provenance/indexing audit.  It reads every documentation file in the
working tree and every documentation blob on the selected Git reference.  It
does not decide whether a scientific claim is true and does not promote any
gate status.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


DOC_EXTENSIONS = {".md", ".markdown", ".rst"}
DOCUMENT_PREFIXES = (
    "README",
    "CHANGELOG",
    "LICENCE",
    "LICENSE",
    "CONTRIBUTING",
    "AGENTS",
    "GEMINI",
    "COVERLETTER",
)
STATUS_PATTERNS = (
    "BLOCKED",
    "IN_PROGRESS",
    "IN PROGRESS",
    "HOLD",
    "OPEN",
    "CLOSED",
    "COMPLETE",
    "CLEARED",
    "PASS",
    "FAIL",
    "DERIVED",
    "CONDITIONAL",
    "REJECTED",
    "NOT_COMPUTED",
    "NOT_DERIVED",
    "NOT_STARTED",
)
CLAIM_TERMS = (
    "a_0",
    "a0",
    "2pi",
    "2\\pi",
    "13/12",
    "SPARC",
    "Hubble tension",
    "Bullet Cluster",
    "JWST",
    "DESI",
    "GW170817",
    "MAT-001",
    "UVIR-003",
    "R5-P1",
    "complex quartet",
    "source vector",
    "Q^nu",
    "Q^\\nu",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument("--repo", type=Path, default=base.parents[1])
    parser.add_argument("--ref", default="main")
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def run_git(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def is_document(path: str) -> bool:
    name = Path(path).name
    return (
        Path(path).suffix.lower() in DOC_EXTENSIONS
        or name.upper().startswith(DOCUMENT_PREFIXES)
    )


def normalized_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def classify_path(path: str) -> str:
    lowered = path.lower()
    if lowered.startswith(".codex-remote-attachments/"):
        return "workspace_attachment_not_repository_authority"
    if lowered.startswith("theory/core/"):
        return "canonical_core_candidate"
    if lowered.startswith("theory/gates/"):
        return "gate_document"
    if "/releases/" in lowered or lowered.startswith("releases/"):
        return "immutable_or_historical_release"
    if "history" in lowered or "archive" in lowered:
        return "historical_or_archive"
    if lowered.startswith("manuscript/") or lowered.startswith("papers/"):
        return "manuscript_or_publication"
    if lowered.startswith("camb_itsm_solver/"):
        return "vendored_solver_documentation"
    return "supporting_documentation"


def extract_record(path: str, data: bytes, source: str) -> dict[str, Any]:
    text = data.decode("utf-8", errors="replace")
    lines = text.splitlines()
    headings = [
        line.strip()
        for line in lines
        if re.match(r"^\s{0,3}#{1,6}\s+\S", line)
    ]
    upper = text.upper()
    status_hits = {
        token: upper.count(token)
        for token in STATUS_PATTERNS
        if upper.count(token)
    }
    claim_hits = {
        token: text.lower().count(token.lower())
        for token in CLAIM_TERMS
        if text.lower().count(token.lower())
    }
    return {
        "path": path,
        "source": source,
        "category": classify_path(path),
        "bytes": len(data),
        "line_count": len(lines),
        "sha256_raw": sha256(data),
        "sha256_lf_normalized": sha256(normalized_bytes(data)),
        "replacement_character_count": text.count("\ufffd"),
        "headings": headings,
        "status_hits": status_hits,
        "claim_term_hits": claim_hits,
    }


def working_documents(repo: Path) -> dict[str, bytes]:
    documents: dict[str, bytes] = {}
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(repo).as_posix()
        if is_document(relative):
            documents[relative] = path.read_bytes()
    return documents


def ref_documents(repo: Path, ref: str) -> dict[str, bytes]:
    names = run_git(repo, "ls-tree", "-r", "--name-only", ref).decode(
        "utf-8", errors="strict"
    ).splitlines()
    return {
        path: run_git(repo, "show", f"{ref}:{path}")
        for path in sorted(names)
        if is_document(path)
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "path",
        "relation",
        "category",
        "working_bytes",
        "ref_bytes",
        "working_sha256_lf",
        "ref_sha256_lf",
        "working_heading_count",
        "ref_heading_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    branch = run_git(repo, "branch", "--show-current").decode().strip()
    head = run_git(repo, "rev-parse", "HEAD").decode().strip()
    ref_commit = run_git(repo, "rev-parse", args.ref).decode().strip()
    tracked_paths = set(
        run_git(repo, "ls-files").decode("utf-8", errors="strict").splitlines()
    )
    working = working_documents(repo)
    reference = ref_documents(repo, args.ref)
    working_records = {
        path: extract_record(path, data, "working_tree")
        for path, data in working.items()
    }
    for path, record in working_records.items():
        record["git_tracking"] = "tracked" if path in tracked_paths else "untracked"
    ref_records = {
        path: extract_record(path, data, f"git_ref:{args.ref}")
        for path, data in reference.items()
    }

    comparison_rows: list[dict[str, Any]] = []
    relations: dict[str, int] = {}
    for path in sorted(set(working) | set(reference)):
        work = working_records.get(path)
        ref = ref_records.get(path)
        if work is None:
            relation = "ref_only"
        elif ref is None:
            relation = "working_only"
        elif work["sha256_lf_normalized"] == ref["sha256_lf_normalized"]:
            relation = "same_normalized_content"
        else:
            relation = "different_content"
        relations[relation] = relations.get(relation, 0) + 1
        comparison_rows.append(
            {
                "path": path,
                "relation": relation,
                "category": (work or ref)["category"],
                "working_bytes": "" if work is None else work["bytes"],
                "ref_bytes": "" if ref is None else ref["bytes"],
                "working_sha256_lf": ""
                if work is None
                else work["sha256_lf_normalized"],
                "ref_sha256_lf": ""
                if ref is None
                else ref["sha256_lf_normalized"],
                "working_heading_count": ""
                if work is None
                else len(work["headings"]),
                "ref_heading_count": ""
                if ref is None
                else len(ref["headings"]),
            }
        )

    summary = {
        "audit_kind": "DOCUMENTATION_CORPUS_PROVENANCE_INDEX",
        "scientific_status": "NO_PHYSICS_PROMOTION",
        "branch": branch,
        "head": head,
        "reference": args.ref,
        "reference_commit": ref_commit,
        "document_definition": {
            "extensions": sorted(DOC_EXTENSIONS),
            "name_prefixes": list(DOCUMENT_PREFIXES),
        },
        "working_document_count": len(working_records),
        "reference_document_count": len(ref_records),
        "comparison_relation_counts": relations,
        "working_total_bytes": sum(item["bytes"] for item in working_records.values()),
        "reference_total_bytes": sum(item["bytes"] for item in ref_records.values()),
        "working_records": [working_records[path] for path in sorted(working_records)],
        "reference_records": [ref_records[path] for path in sorted(ref_records)],
        "boundary": (
            "This output proves corpus enumeration and content extraction only. "
            "It does not certify that a claim is correct, current, derived, or gate-cleared."
        ),
    }

    json_path = output_dir / "docs_corpus_audit_summary.json"
    csv_path = output_dir / "docs_corpus_audit_comparison.csv"
    json_bytes = (
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    json_path.write_bytes(json_bytes)
    write_csv(csv_path, comparison_rows)
    sidecar_path = output_dir / "docs_corpus_audit_artifacts.sha256"
    sidecar_path.write_text(
        f"{sha256(json_path.read_bytes())}  {json_path.name}\n"
        f"{sha256(csv_path.read_bytes())}  {csv_path.name}\n",
        encoding="ascii",
        newline="\n",
    )

    print(f"Working documentation files: {len(working_records)}")
    print(f"{args.ref} documentation files: {len(ref_records)}")
    print(f"Relations: {json.dumps(relations, sort_keys=True)}")
    print("Scientific status: NO_PHYSICS_PROMOTION")
    print("STATUS: PASS_DOCUMENTATION_CORPUS_PROVENANCE_INDEX")


if __name__ == "__main__":
    main()
