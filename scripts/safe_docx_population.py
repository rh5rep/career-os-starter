#!/usr/bin/env python3
"""Strict in-place replacement for DOCX template text nodes.

Unknown structural controls are never cleared. A caller needing a different
paragraph structure must rebuild that paragraph deliberately from a reviewed
model and validate it against the registered template fingerprint.
"""
from __future__ import annotations

import re
from copy import deepcopy
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def structural_sequence(paragraph: ET.Element) -> tuple[str, ...]:
    return tuple(e.tag for e in paragraph.iter() if e.tag in {
        W + "tab", W + "drawing", W + "pict", W + "fldChar", W + "instrText",
        W + "hyperlink", W + "bookmarkStart", W + "bookmarkEnd",
    })


def replace_placeholder_run(paragraph: ET.Element, old: str, new: str) -> None:
    """Replace text only when the complete placeholder lives in one w:t node."""
    if not old or any(c in new for c in "\t\n\r"):
        raise ValueError("Replacement must be single-line text without tabs")
    matches = [t for t in paragraph.iter(W + "t") if t.text and old in t.text]
    if len(matches) != 1:
        raise ValueError(f"Expected one intact placeholder {old!r}; found {len(matches)}")
    before = structural_sequence(paragraph)
    matches[0].text = matches[0].text.replace(old, new)
    if structural_sequence(paragraph) != before:
        raise AssertionError("Structural sequence changed during text replacement")


def replace_text_preserve_structure(paragraph: ET.Element, replacements: dict[str, str]) -> None:
    for old, new in replacements.items():
        replace_placeholder_run(paragraph, old, new)


def rebuild_structural_paragraph(approved_model: ET.Element, replacements: dict[str, str]) -> ET.Element:
    """Clone a reviewed whole-paragraph model, then populate its text slots.

    The caller replaces the old paragraph node with this returned node. This
    cannot accidentally retain stale controls from the paragraph being replaced.
    A final template-derived structural comparison is still required.
    """
    rebuilt = deepcopy(approved_model)
    replace_text_preserve_structure(rebuilt, replacements)
    assert_no_stale_placeholder_structure(rebuilt)
    return rebuilt


def assert_no_stale_placeholder_structure(paragraph: ET.Element, pattern: str = r"\[\[[^]]+\]\]") -> None:
    text = "".join(t.text or "" for t in paragraph.iter(W + "t"))
    metadata = " ".join(str(v) for e in paragraph.iter() for v in e.attrib.values())
    if re.search(pattern, text) or re.search(pattern, metadata) or "PROJECT_ICON_SLOT" in metadata:
        raise ValueError("Placeholder remains after population")
