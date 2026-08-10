#!/usr/bin/env python3
"""Fail-closed validation for the public ITSM Pages artifact."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

REQUIRED = {
    "index.html": (
        "Freeze α.12",
        "UVIR-003 IN PROGRESS",
        "Tier-1 NOT MET",
        "MAT-001 BLOCKED",
        "V NOT COMPUTED",
        "K_Q NOT DERIVED",
    ),
    "research.html": (
        "α.12 frozen",
        "Tier-1 is NOT_MET",
        "V</code> is NOT_COMPUTED",
        "K_Q</code> is NOT_DERIVED",
        "Stage 4A is CLOSED",
        "eight required artifacts remain TODO",
        "STAT awaits predictions",
    ),
}

FORBIDDEN = (
    re.compile(r"(?:alpha|α)[.-]?13", re.IGNORECASE),
    re.compile(r"UVIR-003\s*(?:is|:|-)?\s*(?:complete|closed|cleared|pass(?:ed)?)\b", re.IGNORECASE),
    re.compile(r"MAT-001\s*(?:is|:|-)?\s*(?:complete|closed|cleared|pass(?:ed)?)\b", re.IGNORECASE),
    re.compile(r"STAT-001\s*(?:is|:|-)?\s*(?:complete|closed|cleared|pass(?:ed)?)\b", re.IGNORECASE),
    re.compile(r"(?:chi|χ)\s*(?:\^?2|²)\s*=\s*7\.38", re.IGNORECASE),
    re.compile(r"recovery/v12-core-architecture", re.IGNORECASE),
)


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.resources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        attr = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if attr and values.get(attr):
            self.resources.append(values[attr] or "")


def local_target(page: Path, reference: str) -> Path | None:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:")):
        return None
    if not parsed.path:
        return None
    return (page.parent / parsed.path).resolve()


def main() -> int:
    errors: list[str] = []
    html_files = sorted(DOCS.glob("*.html"))
    if not html_files:
        errors.append("docs contains no HTML files")

    cname = (DOCS / "CNAME").read_text(encoding="utf-8").strip()
    if cname != "itsm-cosmology.com":
        errors.append(f"unexpected CNAME: {cname!r}")

    for name, tokens in REQUIRED.items():
        text = (DOCS / name).read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{name}: missing required boundary {token!r}")

    for page in html_files:
        text = page.read_text(encoding="utf-8")
        for pattern in FORBIDDEN:
            match = pattern.search(text)
            if match:
                excerpt = " ".join(match.group(0).split())
                errors.append(f"{page.name}: forbidden public claim/link: {excerpt!r}")

        parser = ResourceParser()
        parser.feed(text)
        for reference in parser.resources:
            target = local_target(page, reference)
            if target is not None and (DOCS not in target.parents and target != DOCS):
                errors.append(f"{page.name}: local reference escapes docs: {reference!r}")
            elif target is not None and not target.exists():
                errors.append(f"{page.name}: missing local resource: {reference!r}")

    if errors:
        print("PAGES_PUBLIC_CLAIM_FIREWALL: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PAGES_PUBLIC_CLAIM_FIREWALL: PASS ({len(html_files)} HTML pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
