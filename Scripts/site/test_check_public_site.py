"""Offline regression controls for public paper freshness, not physics review."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from check_public_site import Page, REPO_PREFIX, RESEARCH_BRANCH, current_paper_failures


class CurrentPaperChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="itsm-site-paper-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.directory = Path("papers") / "Example"
        (self.root / self.directory).mkdir(parents=True)
        self.tracked = set()
        self.definitions = {"example": "Example"}
        self.install_version("0.2.0-rc7")

    def install_version(self, version):
        self.version = version
        version_path = self.directory / "VERSION"
        (self.root / version_path).write_text(version + "\n", encoding="utf-8")
        self.tracked.add(version_path.as_posix())
        self.pdf = self.directory / ("Example_v" + version + ".pdf")
        data = b"PDF checksum test fixture, not a manuscript"
        (self.root / self.pdf).write_bytes(data)
        self.sidecar = self.pdf.with_suffix(".pdf.sha256")
        (self.root / self.sidecar).write_text(hashlib.sha256(data).hexdigest() + "\n",
                                             encoding="utf-8")
        self.tracked.update((self.pdf.as_posix(), self.sidecar.as_posix()))

    def card(self, version=None, pdf=None, visible=None):
        version = self.version if version is None else version
        pdf = self.pdf if pdf is None else pdf
        visible = "v" + version if visible is None else visible
        parser = Page()
        parser.feed('<article data-paper="example" data-version="' + version + '">'
                    '<p>' + visible + '</p><a href="' + REPO_PREFIX + 'blob/' +
                    RESEARCH_BRANCH + '/' + pdf.as_posix() + '">PDF</a></article>')
        parser.close()
        self.assertEqual(parser.errors, [])
        return parser.paper_cards[0]

    def errors(self, cards=None):
        return current_paper_failures([self.card()] if cards is None else cards,
                                      self.root, self.tracked, self.definitions)

    def test_current_version_and_checksum_pass(self):
        self.assertEqual(self.errors(), [])

    def test_retained_older_pdf_does_not_make_stale_card_current(self):
        old = self.card()
        self.install_version("0.2.0-rc8")
        self.assertTrue(any("Stale card version" in error for error in self.errors([old])))

    def test_stale_link_fails_even_when_label_is_current(self):
        stale = self.directory / "Example_v0.2.0-rc3.pdf"
        self.assertTrue(any("Missing current PDF link" in error
                            for error in self.errors([self.card(pdf=stale)])))

    def test_stale_visible_label_fails_even_when_metadata_is_current(self):
        self.assertTrue(any("Missing visible current version" in error
                            for error in self.errors([self.card(visible="v0.2.0-rc3")])))

    def test_missing_card_fails(self):
        self.assertTrue(self.errors([]))

    def test_duplicate_card_fails(self):
        self.assertTrue(self.errors([self.card(), self.card()]))

    def test_unknown_card_fails(self):
        unknown = self.card()
        unknown["paper"] = "unregistered"
        self.assertTrue(any("Unknown current-paper card" in error
                            for error in self.errors([self.card(), unknown])))

    def test_untracked_pdf_cannot_be_advertised(self):
        self.tracked.remove(self.pdf.as_posix())
        self.assertTrue(any("tracked current-version PDF" in error for error in self.errors()))

    def test_missing_pdf_fails(self):
        (self.root / self.pdf).unlink()
        self.assertTrue(self.errors())

    def test_untracked_version_fails(self):
        self.tracked.remove((self.directory / "VERSION").as_posix())
        self.assertTrue(self.errors())

    def test_missing_version_fails(self):
        (self.root / self.directory / "VERSION").unlink()
        self.assertTrue(self.errors())

    def test_malformed_version_fails(self):
        (self.root / self.directory / "VERSION").write_text("latest", encoding="utf-8")
        self.assertTrue(any("Invalid VERSION" in error for error in self.errors()))

    def test_checksum_mismatch_fails(self):
        (self.root / self.pdf).write_bytes(b"changed fixture")
        self.assertTrue(any("checksum mismatch" in error for error in self.errors()))

    def test_missing_checksum_fails(self):
        (self.root / self.sidecar).unlink()
        self.assertTrue(self.errors())

    def test_untracked_checksum_fails(self):
        self.tracked.remove(self.sidecar.as_posix())
        self.assertTrue(self.errors())

    def test_malformed_checksum_fails(self):
        (self.root / self.sidecar).write_text("not-a-checksum", encoding="utf-8")
        self.assertTrue(any("Invalid current PDF checksum" in error for error in self.errors()))

    def test_quarantined_version_is_not_auto_promoted(self):
        self.install_version("0.2.0-quarantined-draft")
        self.assertTrue(any("Quarantined version" in error for error in self.errors()))

    def test_conditional_draft_suffix_is_supported(self):
        self.install_version("0.7.1-conditional-draft")
        self.assertEqual(self.errors(), [])

    def test_unrelated_historical_link_does_not_satisfy_current_card(self):
        parser = Page()
        expected = REPO_PREFIX + "blob/" + RESEARCH_BRANCH + "/" + self.pdf.as_posix()
        parser.feed('<a href="' + expected + '">History</a>'
                    '<article data-paper="example" data-version="' + self.version + '">'
                    '<p>v' + self.version + '</p></article>')
        self.assertTrue(self.errors(parser.paper_cards))


if __name__ == "__main__":
    unittest.main()
