#!/usr/bin/env python3
"""Template-derived DOCX structure fingerprint and release comparison.

This compares layout controls, not text equality. A template with variable
paragraph counts can still validate its generated document. Registration must
be repeated whenever the approved template changes.
"""
from __future__ import annotations

import hashlib
import json
import posixpath
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
P = "{http://schemas.openxmlformats.org/package/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
PLACEHOLDER = re.compile(r"\[\[[^]]+\]\]|PROJECT_ICON_SLOT|\[TARGET\]|\[AUTH\]", re.I)
VERSION = "1.0"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _xml(z: zipfile.ZipFile, name: str):
    return ET.fromstring(z.read(name))


def _semantic_xml(e: ET.Element):
    """Represent XML meaning without serializer whitespace/prefix differences."""
    return [
        e.tag,
        sorted(e.attrib.items()),
        (e.text or "").strip(),
        [_semantic_xml(child) for child in e],
    ]


def _part_names(z: zipfile.ZipFile) -> list[str]:
    return sorted(n for n in z.namelist() if re.fullmatch(r"word/(?:document|header\d+|footer\d+)\.xml", n))


def _rels(z: zipfile.ZipFile, part: str) -> dict[str, tuple[str, str]]:
    relpart = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    if relpart not in z.namelist():
        return {}
    result = {}
    for rel in _xml(z, relpart):
        target = rel.get("Target", "")
        if rel.get("TargetMode") != "External":
            target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(part), target))
        result[rel.get("Id")] = (rel.get("Type", ""), target)
    return result


def _tokens(p: ET.Element) -> tuple[list[str], str, list[str], str]:
    tokens, pieces, embeds, left = [], [], [], []
    seen_text = False
    passed_label_tab = False
    for e in p.iter():
        if e.tag == W + "t" and e.text:
            pieces.append(e.text)
            if not passed_label_tab:
                left.append(e.text)
            seen_text = True
            if not tokens or tokens[-1] != "TEXT":
                tokens.append("TEXT")
        elif e.tag == W + "tab":
            if seen_text:
                passed_label_tab = True
            tokens.append("TAB")
        elif e.tag in (W + "drawing", W + "pict"):
            tokens.append("DRAWING")
        elif e.tag in (W + "fldChar", W + "instrText", W + "fldSimple"):
            tokens.append("FIELD")
        elif e.tag == W + "hyperlink":
            tokens.append("HYPERLINK")
        elif e.tag in (W + "bookmarkStart", W + "bookmarkEnd"):
            tokens.append("BOOKMARK")
        if e.tag == A + "blip" and e.get(R + "embed"):
            embeds.append(e.get(R + "embed"))
    return tokens, "".join(pieces), embeds, "".join(left).split("[[", 1)[0].strip()


def _paragraph(p: ET.Element, z: zipfile.ZipFile, rels: dict) -> dict:
    pp = p.find(W + "pPr")
    sty = pp.find(W + "pStyle") if pp is not None else None
    tabs = pp.find(W + "tabs") if pp is not None else None
    align = pp.find(W + "jc") if pp is not None else None
    tokens, text, embeds, anchor = _tokens(p)
    image_hashes = []
    for rid in embeds:
        typ, target = rels.get(rid, ("", ""))
        image_hashes.append(sha(z.read(target)) if "image" in typ and target in z.namelist() else "BROKEN:" + rid)
    links = []
    for h in p.iter(W + "hyperlink"):
        rid = h.get(R + "id")
        if rid:
            links.append(rels.get(rid, ("BROKEN", rid)))
    return {
        "style": sty.get(W + "val") if sty is not None else "Normal",
        "pattern": tokens,
        "text": text,
        "anchor": anchor,
        "known_placeholders": sorted(set(PLACEHOLDER.findall(text))),
        "tab_stops": ET.tostring(tabs, encoding="unicode") if tabs is not None else "",
        "alignment": align.get(W + "val") if align is not None else None,
        "images": image_hashes,
        "fields": [e.text or "" for e in p.iter(W + "instrText")],
        "links": links,
    }


def inspect(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise ValueError(f"Corrupt ZIP member: {bad}")
        parts = {}
        broken_rels = []
        referenced_media = set()
        for part in _part_names(z):
            rels = _rels(z, part)
            root = _xml(z, part)
            paragraphs = [_paragraph(p, z, rels) for p in root.iter(W + "p")]
            parts[part] = {
                "paragraphs": paragraphs,
                "tables": len(list(root.iter(W + "tbl"))),
                "text_boxes": len(list(root.iter(W + "txbxContent"))),
                "section_geometry": [
                    {
                        name: {k.split("}")[-1]: v for k, v in el.attrib.items()}
                        for name in ("pgSz", "pgMar", "cols")
                        if (el := s.find(W + name)) is not None
                    }
                    for s in root.iter(W + "sectPr")
                ],
            }
            for rid, (typ, target) in rels.items():
                if "image" in typ:
                    referenced_media.add(target)
                    if target not in z.namelist():
                        broken_rels.append(f"{part}:{rid}->{target}")
        # Orphan accounting must include relationships from every Word part,
        # not just body/header/footer; a footnote image is still referenced.
        for relpart in z.namelist():
            if not relpart.startswith("word/") or not relpart.endswith(".rels") or "/_rels/" not in relpart:
                continue
            folder, name = relpart.rsplit("/_rels/", 1)
            source = folder + "/" + name.removesuffix(".rels")
            for rid, (typ, target) in _rels(z, source).items():
                if "image" in typ:
                    referenced_media.add(target)
                    if target not in z.namelist():
                        finding = f"{source}:{rid}->{target}"
                        if finding not in broken_rels:
                            broken_rels.append(finding)
        media = {n for n in z.namelist() if n.startswith("word/media/") and not n.endswith("/")}
        styles = {}
        style_semantics = None
        if "word/styles.xml" in z.namelist():
            style_root = _xml(z, "word/styles.xml")
            style_semantics = sha(json.dumps(_semantic_xml(style_root), separators=(",", ":")).encode())
            for s in style_root.iter(W + "style"):
                sid = s.get(W + "styleId")
                if not sid:
                    continue
                parent = s.find(W + "basedOn")
                font = s.find("./" + W + "rPr/" + W + "rFonts")
                size = s.find("./" + W + "rPr/" + W + "sz")
                indent = s.find("./" + W + "pPr/" + W + "ind")
                styles[sid] = {
                    "based_on": parent.get(W + "val") if parent is not None else None,
                    "fonts": {k.split("}")[-1]: v for k, v in font.attrib.items()} if font is not None else {},
                    "size_half_points": size.get(W + "val") if size is not None else None,
                    "indent": {k.split("}")[-1]: v for k, v in indent.attrib.items()} if indent is not None else {},
                }
        return {
            "version": VERSION,
            "source_sha256": sha(path.read_bytes()),
            "styles_sha256": sha(z.read("word/styles.xml")) if "word/styles.xml" in z.namelist() else None,
            "style_semantics_sha256": style_semantics,
            "style_hierarchy": styles,
            "parts": parts,
            "broken_image_relationships": broken_rels,
            "orphan_media_hashes": sorted(sha(z.read(n)) for n in media - referenced_media),
        }


def fingerprint(path: Path) -> dict:
    data = inspect(path)
    # Literal text before a tab is a fixed anchor unless registration marks it
    # as a placeholder. This also protects tabbed templates with no drawings.
    for part in data["parts"].values():
        for p in part["paragraphs"]:
            p["fixed_anchor"] = p["anchor"] if ("TAB" in p["pattern"] or p["images"]) and p["anchor"] and not PLACEHOLDER.search(p["anchor"]) else None
            p.pop("text")
            p.pop("anchor")
    return data


def validate_template(path: Path) -> list[str]:
    data = inspect(path)
    return ["broken image relationship: " + x for x in data["broken_image_relationships"]]


def validate_artifact(template: Path, artifact: Path, *, placeholder_patterns: list[str] | None = None) -> list[str]:
    base, final = fingerprint(template), inspect(artifact)
    findings = ["broken image relationship: " + x for x in final["broken_image_relationships"]]
    if final["style_semantics_sha256"] != base["style_semantics_sha256"]:
        findings.append("style semantics changed from approved template")
    extra_orphans = Counter(final["orphan_media_hashes"]) - Counter(base["orphan_media_hashes"])
    if extra_orphans:
        findings.append("new orphan media in artifact")
    for part_name, part in base["parts"].items():
        actual = final["parts"].get(part_name)
        if actual is None:
            findings.append(f"missing document/header/footer part {part_name}")
            continue
        for key in ("tables", "text_boxes", "section_geometry"):
            if actual[key] != part[key]:
                findings.append(f"{part_name}: {key} changed from approved template")
        expected_by_style = defaultdict(list)
        for p in part["paragraphs"]:
            expected_by_style[p["style"]].append(p)
        actual_by_style = defaultdict(list)
        for p in actual["paragraphs"]:
            actual_by_style[p["style"]].append(p)
        for style, actual_paras in actual_by_style.items():
            if style not in expected_by_style:
                findings.append(f"{part_name}: unexpected paragraph style {style}")
                continue
            expected = expected_by_style[style]
            # Non-structural variable paragraphs can grow and change text freely.
            guarded = [p for p in expected if any(t != "TEXT" for t in p["pattern"])]
            for idx, p in enumerate(actual_paras):
                if any(link[0] == "BROKEN" for link in p["links"]):
                    findings.append(f"{part_name}: style {style} instance {idx + 1} broken hyperlink relationship")
                if not guarded and all(t == "TEXT" for t in p["pattern"]):
                    continue
                candidates = guarded or expected
                key = lambda x: (x["pattern"], x["tab_stops"], x["alignment"], x["fields"])
                matches = [x for x in candidates if key(x) == key(p)]
                if not matches:
                    findings.append(f"{part_name}: style {style} instance {idx + 1} structural sequence/tab stops/alignment differs: {p['pattern']}")
                    continue
                if "TAB" in p["pattern"]:
                    # A right metadata field cannot be empty after its structural tab.
                    if p["pattern"][-1] == "TAB" or not p["text"].strip():
                        findings.append(f"{part_name}: style {style} instance {idx + 1} missing right metadata")
                fixed = [x for x in matches if x.get("fixed_anchor") and p["text"].startswith(x["fixed_anchor"])]
                if any(x.get("fixed_anchor") for x in matches) and not fixed:
                    findings.append(f"{part_name}: style {style} instance {idx + 1} fixed label moved or replaced")
                if fixed and p["images"] not in [x["images"] for x in fixed]:
                    findings.append(f"{part_name}: style {style} instance {idx + 1} wrong image for fixed anchor")
                if any(x["images"] for x in matches) and not p["images"]:
                    findings.append(f"{part_name}: style {style} instance {idx + 1} missing drawing")
        if part_name != "word/document.xml":
            # Header/footer paragraph counts are usually fixed by the template.
            for style, expected in expected_by_style.items():
                if len(actual_by_style[style]) != len(expected):
                    findings.append(f"{part_name}: style {style} paragraph count changed")
    for part_name in final["parts"]:
        if part_name not in base["parts"]:
            findings.append(f"unexpected document/header/footer part {part_name}")
    patterns = [PLACEHOLDER] + [re.compile(x, re.I) for x in (placeholder_patterns or [])]
    for part_name, part in final["parts"].items():
        for idx, p in enumerate(part["paragraphs"]):
            if any(pattern.search(p["text"]) for pattern in patterns):
                findings.append(f"{part_name}: paragraph {idx + 1} retains placeholder text")
    with zipfile.ZipFile(artifact) as z:
        for name in z.namelist():
            if name.startswith("word/") and name.endswith(".xml") and b"PROJECT_ICON_SLOT" in z.read(name):
                findings.append(f"{name}: stale PROJECT_ICON_SLOT metadata")
    return sorted(set(findings))


def write_fingerprint(template: Path, output: Path) -> None:
    output.write_text(json.dumps(fingerprint(template), indent=2) + "\n")


def validate_registration(template: Path, registered_fingerprint: Path) -> list[str]:
    registered = json.loads(registered_fingerprint.read_text())
    current = fingerprint(template)
    findings = []
    if registered.get("version") != VERSION:
        findings.append("registered fingerprint validator version changed; re-register template")
    if registered.get("source_sha256") != current["source_sha256"]:
        findings.append("approved template source hash differs from registered fingerprint")
    return findings
