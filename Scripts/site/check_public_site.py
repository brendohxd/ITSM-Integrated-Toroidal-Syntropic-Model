"""Read-only website checks. A website pass is never a scientific clearance."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PAGES = ("index.html", "vision.html", "architecture.html", "research.html",
         "papers.html", "claims.html", "reproduce.html")
REPO_PREFIX = "https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model/"
NAV = ("vision.html", "architecture.html", "research.html", "papers.html", "claims.html")
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
CURRENT_PAPERS = {
    "p1": "P1-Scale-Matching-Reconstruction",
    "p2": "P2-Rectangular-T3-Casimir",
    "thermodynamics": "Syntropic-Thermodynamics",
    "r4c1": "R4C1-Covariant-Exchange-Model",
}
RESEARCH_BRANCH = "recovery/v12-core-architecture"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.stack, self.errors = set(), [], [], []
        self.h1 = self.main = self.description = self.viewport = 0
        self.title = self.lang = False
        self.nav, self.in_nav = [], False
        self.paper_cards, self.current_paper = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "article" and a.get("data-paper"):
            if self.current_paper is not None:
                self.errors.append("Nested current-paper card")
            self.current_paper = {"paper": a["data-paper"],
                                  "version": a.get("data-version", ""),
                                  "refs": [], "text": []}
            self.paper_cards.append(self.current_paper)
        if a.get("id"):
            if a["id"] in self.ids:
                self.errors.append("Duplicate id: " + a["id"])
            self.ids.add(a["id"])
        self.h1 += tag == "h1"
        self.main += tag == "main"
        self.title |= tag == "title"
        self.lang |= tag == "html" and a.get("lang") == "en"
        if tag == "meta":
            self.description += a.get("name") == "description" and bool(a.get("content"))
            self.viewport += a.get("name") == "viewport" and bool(a.get("content"))
        if tag == "nav" and a.get("aria-label") == "Main navigation":
            self.in_nav = True
        if self.in_nav and tag == "a" and "brand" not in a.get("class", "").split():
            self.nav.append(a.get("href"))
        if tag == "img" and "alt" not in a:
            self.errors.append("Image has no alt attribute")
        for key in ("href", "src", "data-lightbox"):
            if a.get(key):
                self.refs.append(a[key])
                if self.current_paper is not None and key == "href":
                    self.current_paper["refs"].append(a[key])

    def handle_data(self, data):
        if self.current_paper is not None:
            self.current_paper["text"].append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "article":
            self.current_paper = None
        if tag == "nav":
            self.in_nav = False
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append("Unbalanced closing tag: " + tag)
        else:
            self.stack.pop()


def current_paper_failures(cards, root, tracked, definitions=CURRENT_PAPERS):
    """Check current cards, not historical links or the scientific claims."""
    failures = []
    for card in cards:
        if card["paper"] not in definitions:
            failures.append("Unknown current-paper card: " + card["paper"])
    for key, directory in definitions.items():
        matching_cards = [card for card in cards if card["paper"] == key]
        if len(matching_cards) != 1:
            failures.append("Expected one current-paper card: " + key)
            continue
        card = matching_cards[0]
        relative_dir = Path("papers") / directory
        version_path = relative_dir / "VERSION"
        try:
            if version_path.as_posix() not in tracked:
                raise ValueError("VERSION is not tracked")
            version = (root / version_path).read_text(encoding="utf-8-sig").strip()
            if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?", version):
                raise ValueError("Invalid VERSION")
            if "quarantined" in version.lower():
                raise ValueError("Quarantined version cannot be a current review card")
        except (OSError, ValueError) as error:
            failures.append(key + ": " + str(error))
            continue
        if card["version"] != version:
            failures.append(key + ": Stale card version; expected " + version)
        if "v" + version not in "".join(card["text"]):
            failures.append(key + ": Missing visible current version " + version)
        candidates = [path for path in (root / relative_dir).glob("*.pdf")
                      if path.name.endswith("_v" + version + ".pdf")
                      and path.relative_to(root).as_posix() in tracked]
        if len(candidates) != 1:
            failures.append(key + ": Expected one tracked current-version PDF")
            continue
        pdf = candidates[0]
        relative_pdf = pdf.relative_to(root).as_posix()
        expected_ref = REPO_PREFIX + "blob/" + RESEARCH_BRANCH + "/" + relative_pdf
        if expected_ref not in card["refs"]:
            failures.append(key + ": Missing current PDF link " + relative_pdf)
        sidecar = pdf.with_suffix(".pdf.sha256")
        try:
            if sidecar.relative_to(root).as_posix() not in tracked:
                raise ValueError("Current PDF checksum is not tracked")
            fields = sidecar.read_text(encoding="utf-8-sig").split()
            if not fields or not re.fullmatch(r"[a-fA-F0-9]{64}", fields[0]):
                raise ValueError("Invalid current PDF checksum")
            if hashlib.sha256(pdf.read_bytes()).hexdigest() != fields[0].lower():
                raise ValueError("Current PDF checksum mismatch")
        except (OSError, ValueError) as error:
            failures.append(key + ": " + str(error))
    return failures


def check():
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0"))
    failures, pages, references = [], {}, 0
    pdfs = set()
    pinned_targets = set()
    for name in PAGES:
        body = (DOCS / name).read_text(encoding="utf-8")
        page = Page()
        page.feed(body)
        page.close()
        pages[name] = page
        errors = list(page.errors)
        if page.stack:
            errors.append("Unclosed tags: " + repr(page.stack))
        if not (page.h1 == page.main == page.description == page.viewport == 1):
            errors.append("Expected one h1, main, description and viewport")
        if not page.title or not page.lang or "main" not in page.ids:
            errors.append("Missing title, language or skip-link target")
        if tuple(page.nav) != NAV:
            errors.append("Inconsistent main navigation")
        if 'href="styles.css?v=20261014a"' not in body:
            errors.append("Stale stylesheet version")
        if "26 September 2026" in body or body.rstrip().endswith("\\n"):
            errors.append("Stale snapshot or literal escaped-newline artifact")
        if re.search(r"(?:AppData[/\\]|[A-Z]:[/\\]|memory\.db|\.local/|rollout-)", body):
            errors.append("Private/local path found in public HTML")
        failures.extend({"page": name, "error": error} for error in errors)
    for name, page in pages.items():
        for ref in page.refs:
            references += 1
            url = urlsplit(ref)
            if url.scheme == "javascript":
                failures.append({"page": name, "error": "Executable link URL"})
            if ref.startswith(REPO_PREFIX + "blob/recovery/v12-core-architecture/"):
                path = unquote(url.path.split("/blob/recovery/v12-core-architecture/", 1)[1])
                if path not in tracked or not (ROOT / path).is_file():
                    failures.append({"page": name, "error": "Unpublished repository link: " + path})
                if path.endswith(".pdf"):
                    pdfs.add(path)
            if ref.startswith(REPO_PREFIX):
                pinned = re.fullmatch(r"blob/([a-f0-9]{40})/(.+)",
                                      unquote(url.path.split("/ITSM-Integrated-Toroidal-Syntropic-Model/", 1)[1]))
                if pinned:
                    target_spec = pinned[1] + ":" + pinned[2]
                    if target_spec not in pinned_targets:
                        pinned_targets.add(target_spec)
                        result = subprocess.run(["git", "cat-file", "-e", target_spec],
                                                cwd=ROOT, capture_output=True, check=False)
                        if result.returncode:
                            failures.append({"page": name, "error": "Missing pinned repository target: " + target_spec})
            if url.scheme or url.netloc:
                continue
            target = (DOCS / unquote(url.path or name)).resolve()
            if not target.is_relative_to(DOCS.resolve()) or not target.is_file():
                failures.append({"page": name, "error": "Missing/unsafe local link: " + ref})
            if url.fragment and target.name in pages and unquote(url.fragment) not in pages[target.name].ids:
                failures.append({"page": name, "error": "Missing fragment: " + ref})
    for path in pdfs:
        if not re.search(r"_v\d+\.\d+(?:\.\d+)?", Path(path).name) and path != "Manuscript/CoreRecovery/ITSM_Core_working.pdf":
            failures.append({"page": "papers.html", "error": "Unversioned retained document: " + path})
    failures.extend({"page": "papers.html", "error": error} for error in
                    current_paper_failures(pages["papers.html"].paper_cards, ROOT, tracked))
    claims = (DOCS / "claims.html").read_text(encoding="utf-8")
    for boundary in ("K_Q=NOT_DERIVED", "V=NOT_COMPUTED", "MAT-001=BLOCKED",
                     "UVIR-003=IN_PROGRESS", "Stage4A=CLOSED", "physics_pass=false",
                     "gate_effect=NONE", "Rule9_cleared=false"):
        if boundary not in claims:
            failures.append({"page": "claims.html", "error": "Missing boundary: " + boundary})
    for name in ("manifest.json", "site.webmanifest"):
        json.loads((DOCS / name).read_text(encoding="utf-8"))
    sw = (DOCS / "sw.js").read_text(encoding="utf-8")
    for asset in re.findall(r"^\s*'(\./[^']*)',?$", sw, flags=re.M):
        target = DOCS / asset
        if not target.exists():
            failures.append({"page": "sw.js", "error": "Missing precache asset: " + asset})
    if "itsm-pwa-v12-20261021" not in sw:
        failures.append({"page": "sw.js", "error": "Stale service-worker cache"})
    print(json.dumps({"validation": "FAIL_WEBSITE_SOURCE" if failures else "PASS_WEBSITE_SOURCE_ONLY",
                      "pages_checked": len(pages), "references_checked": references,
                      "public_pdf_targets_checked": len(pdfs), "failures": failures,
                      "current_paper_versions_checked": len(CURRENT_PAPERS),
                      "pinned_repository_targets_checked": len(pinned_targets),
                      "scientific_validation": False, "gate_effect": "NONE"}, indent=2))
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(check())
