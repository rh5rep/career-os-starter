#!/usr/bin/env python3
"""Release record cannot pass with contact-sheet-only QA or no canary."""
import tempfile
import unittest
from pathlib import Path

from test_docx_structure import DOCUMENT, generated, package
from verify_artifact_release import sha, verify


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        package(self.base / "template.docx", DOCUMENT)
        package(self.base / "artifact.docx", generated())
        (self.base / "artifact.pdf").write_bytes(b"test-pdf")
        (self.base / "page-1.png").write_bytes(b"test-render")
        th, dh, ph = (sha(self.base / name) for name in ("template.docx", "artifact.docx", "artifact.pdf"))
        self.record = {
            "files": {k: {"path": f, "sha256": h} for k, f, h in (("template", "template.docx", th), ("docx", "artifact.docx", dh), ("pdf", "artifact.pdf", ph))},
            "semantic_qa": {"result": "PASS", "artifact_sha256": dh},
            "structural_qa": {"result": "PASS", "artifact_sha256": dh, "template_sha256": th, "validator_version": "1.0"},
            "ats_qa": {"result": "PASS", "artifact_sha256": dh, "extraction_sha256": "test-extraction"},
            "visual_qa": {"result": "PASS", "pdf_sha256": ph, "inspection_mode": "INDIVIDUAL_FULL_PAGE", "template_reference_sha256": th, "pdf_page_count": 1, "rendered_pages": [{"path": "page-1.png", "sha256": sha(self.base / "page-1.png"), "inspected_individually": True}], "reviewer": "independent reviewer", "timestamp": "2026-10-01T12:00:00-04:00"},
            "batch": {"canary": {"result": "PASS", "artifact_sha256": dh, "approved_at": "2026-10-01T11:00:00-04:00"}, "fanout_started_at": "2026-10-01T12:00:00-04:00"},
        }

    def test_complete_evidence_passes(self):
        self.assertEqual(verify(self.record, self.base), [])

    def test_contact_sheet_cannot_pass(self):
        self.record["visual_qa"]["inspection_mode"] = "CONTACT_SHEET"
        self.assertTrue(any("contact sheet" in x for x in verify(self.record, self.base)))

    def test_missing_canary_blocks_batch(self):
        self.record["batch"]["canary"] = {}
        self.assertTrue(any("canary" in x for x in verify(self.record, self.base)))

    def test_late_canary_blocks_batch(self):
        self.record["batch"]["canary"]["approved_at"] = "2026-10-01T13:00:00-04:00"
        self.assertTrue(any("precede" in x for x in verify(self.record, self.base)))

    def test_changed_pdf_invalidates_visual_qa(self):
        (self.base / "artifact.pdf").write_bytes(b"different")
        self.assertTrue(any("PDF" in x or "pdf" in x for x in verify(self.record, self.base)))

    def test_missing_rendered_page_blocks_release(self):
        self.record["visual_qa"]["pdf_page_count"] = 2
        self.assertTrue(any("rendered-page" in x for x in verify(self.record, self.base)))

    def test_changed_docx_is_rechecked(self):
        package(self.base / "artifact.docx", generated().replace('w:pos="9000"', 'w:pos="7000"', 1))
        self.record["files"]["docx"]["sha256"] = sha(self.base / "artifact.docx")
        self.assertTrue(any("structural QA" in x for x in verify(self.record, self.base)))


if __name__ == "__main__":
    unittest.main()
