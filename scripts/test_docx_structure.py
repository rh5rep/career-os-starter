#!/usr/bin/env python3
"""Portable structural regression cases, including the submitted batch failure."""
from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx_structure import validate_artifact, validate_registration, validate_template, write_fingerprint
from safe_docx_population import replace_placeholder_run, structural_sequence

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
ET.register_namespace("w", W[1:-1])
ET.register_namespace("r", R[1:-1])
ET.register_namespace("a", A[1:-1])

DOCUMENT = '''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><w:body>
<w:p><w:pPr><w:pStyle w:val="Entry"/><w:tabs><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr><w:r><w:drawing><a:blip r:embed="rId1"/></w:drawing></w:r><w:r><w:t>ACME [[Role]]</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>[[Dates]]</w:t></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="Project"/><w:tabs><w:tab w:val="right" w:pos="9000"/></w:tabs></w:pPr><w:r><w:drawing><a:blip r:embed="rId2"/></w:drawing></w:r><w:r><w:t>[[Project]]</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>[[Year]]</w:t></w:r></w:p>
<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="720" w:bottom="720"/><w:cols w:num="1"/></w:sectPr></w:body></w:document>'''
FOOTER = '''<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:r><w:t>Page </w:t></w:r><w:r><w:instrText>PAGE</w:instrText></w:r></w:p></w:ftr>'''
RELS = '''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo.png"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/project.png"/></Relationships>'''


def package(path: Path, document: str, footer: str = FOOTER, rels: str = RELS, extras: dict[str, bytes] | None = None):
    parts = {
        "word/document.xml": document.encode(),
        "word/footer1.xml": footer.encode(),
        "word/styles.xml": b"<styles/>",
        "word/_rels/document.xml.rels": rels.encode(),
        "word/media/logo.png": b"logo-one",
        "word/media/project.png": b"project-one",
    }
    parts.update(extras or {})
    with zipfile.ZipFile(path, "w") as z:
        for name, data in parts.items():
            z.writestr(name, data)


def generated() -> str:
    root = ET.fromstring(DOCUMENT)
    paras = list(root.iter(W + "p"))
    replace_placeholder_run(paras[0], "[[Role]]", "Engineer")
    replace_placeholder_run(paras[0], "[[Dates]]", "2024-2026")
    replace_placeholder_run(paras[1], "[[Project]]", "Prototype")
    replace_placeholder_run(paras[1], "[[Year]]", "2025")
    return ET.tostring(root, encoding="unicode")


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / "template.docx"
        self.out = Path(self.tmp.name) / "artifact.docx"
        package(self.base, DOCUMENT)

    def check_failure(self, document: str, *, footer: str = FOOTER, rels: str = RELS, extras=None, contains: str):
        package(self.out, document, footer, rels, extras)
        findings = validate_artifact(self.base, self.out)
        self.assertTrue(any(contains in x for x in findings), findings)

    def test_good_template(self):
        self.assertEqual(validate_template(self.base), [])

    def test_registration_binds_exact_source_hash(self):
        fp = Path(self.tmp.name) / "fingerprint.json"
        write_fingerprint(self.base, fp)
        self.assertEqual(validate_registration(self.base, fp), [])
        package(self.base, DOCUMENT.replace("ACME", "Other"))
        self.assertTrue(any("source hash" in x for x in validate_registration(self.base, fp)))

    def test_good_generated_artifact(self):
        package(self.out, generated())
        self.assertEqual(validate_artifact(self.base, self.out), [])

    def test_stale_tab_and_duplicate_right_tab(self):
        doc = generated().replace("</w:drawing></w:r><w:r><w:t>ACME", "</w:drawing></w:r><w:r><w:tab /></w:r><w:r><w:t>ACME", 1)
        self.check_failure(doc, contains="structural sequence")

    def test_project_stale_tab(self):
        doc = generated().replace("</w:drawing></w:r><w:r><w:t>Prototype", "</w:drawing></w:r><w:r><w:tab /></w:r><w:r><w:t>Prototype", 1)
        self.check_failure(doc, contains="structural sequence")

    def test_missing_right_metadata(self):
        doc = generated().replace("2024-2026", "")
        self.check_failure(doc, contains="structural sequence")

    def test_moved_label_after_tab(self):
        doc = generated().replace("ACME Engineer", "2024-2026").replace("<w:t>2024-2026</w:t></w:r></w:p>", "<w:t>ACME Engineer</w:t></w:r></w:p>", 1)
        self.check_failure(doc, contains="fixed label moved")

    def test_no_logo_template_still_guards_tab_sides(self):
        base = ET.fromstring(DOCUMENT)
        final = ET.fromstring(generated())
        for root in (base, final):
            p = next(root.iter(W + "p"))
            p.remove(next(r for r in p.findall(W + "r") if r.find(W + "drawing") is not None))
        texts = list(next(final.iter(W + "p")).iter(W + "t"))
        texts[0].text, texts[-1].text = texts[-1].text, texts[0].text
        package(self.base, ET.tostring(base, encoding="unicode"))
        package(self.out, ET.tostring(final, encoding="unicode"))
        self.assertTrue(any("fixed label moved" in x for x in validate_artifact(self.base, self.out)))

    def test_stale_placeholder(self):
        self.check_failure(DOCUMENT, contains="retains placeholder")

    def test_deleted_drawing(self):
        doc = generated().replace('<w:r><w:drawing><a:blip r:embed="rId1" /></w:drawing></w:r>', "", 1)
        self.check_failure(doc, contains="structural sequence")

    def test_wrong_logo_relationship(self):
        doc = generated().replace('r:embed="rId1"', 'r:embed="rId2"', 1)
        self.check_failure(doc, contains="wrong image")

    def test_orphan_project_media(self):
        self.check_failure(generated(), extras={"word/media/unreferenced.png": b"stale-project-placeholder"}, contains="orphan media")

    def test_style_change(self):
        self.check_failure(generated().replace('w:val="Entry"', 'w:val="Other"', 1), contains="unexpected paragraph style")

    def test_style_definition_change(self):
        package(self.out, generated(), extras={"word/styles.xml": b"<styles><style bold='true'/></styles>"})
        self.assertTrue(any("style semantics" in x for x in validate_artifact(self.base, self.out)))

    def test_tab_stop_change(self):
        self.check_failure(generated().replace('w:pos="9000"', 'w:pos="7000"', 1), contains="tab stops")

    def test_unexpected_table(self):
        self.check_failure(generated().replace("</w:body>", "<w:tbl/></w:body>"), contains="tables changed")

    def test_project_placeholder_metadata(self):
        self.check_failure(generated().replace("Prototype", "Prototype PROJECT_ICON_SLOT"), contains="PROJECT_ICON_SLOT")

    def test_footer_page_number_removed(self):
        self.check_failure(generated(), footer=FOOTER.replace("<w:instrText>PAGE</w:instrText>", ""), contains="footer1.xml")

    def test_page_geometry_change(self):
        self.check_failure(generated().replace('w:w="12240"', 'w:w="11900"'), contains="section_geometry")

    def test_parser_text_can_pass_while_structure_fails(self):
        doc = generated().replace("</w:drawing></w:r><w:r><w:t>ACME", "</w:drawing></w:r><w:r><w:tab /></w:r><w:r><w:t>ACME", 1)
        self.assertIn("ACME Engineer", "".join(t.text or "" for t in ET.fromstring(doc).iter(W + "t")))
        self.check_failure(doc, contains="structural sequence")

    def test_safe_replacement_rejects_tabs(self):
        p = next(ET.fromstring(DOCUMENT).iter(W + "p"))
        before = structural_sequence(p)
        with self.assertRaises(ValueError):
            replace_placeholder_run(p, "[[Role]]", "\tEngineer")
        self.assertEqual(structural_sequence(p), before)


if __name__ == "__main__":
    unittest.main()
