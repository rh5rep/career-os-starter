#!/usr/bin/env python3
"""Verify that release evidence binds every gate to the exact files shipped.

The independent visual reviewer supplies the inspection record. This program
checks completeness and hashes; it cannot substitute for looking at the pages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

from docx_structure import validate_artifact


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(record: dict, base: Path) -> list[str]:
    findings = []
    files = record.get("files", {})
    actual = {}
    for name in ("template", "docx", "pdf"):
        entry = files.get(name) or {}
        path = base / entry.get("path", "")
        if not entry.get("path") or not path.is_file():
            findings.append(f"missing {name} file")
        elif sha(path) != entry.get("sha256"):
            findings.append(f"{name} hash mismatch")
        else:
            actual[name] = entry["sha256"]
    if "template" in actual and "docx" in actual:
        for finding in validate_artifact(base / files["template"]["path"], base / files["docx"]["path"]):
            findings.append("structural QA: " + finding)
    for gate in ("semantic_qa", "structural_qa", "ats_qa", "visual_qa"):
        data = record.get(gate) or {}
        if data.get("result") != "PASS":
            findings.append(f"{gate} is not PASS")
        if data.get("artifact_sha256") != actual.get("docx") and gate != "visual_qa":
            findings.append(f"{gate} does not bind to DOCX hash")
        if gate == "structural_qa":
            if data.get("template_sha256") != actual.get("template") or not data.get("validator_version"):
                findings.append("structural QA lacks template hash or validator version")
        if gate == "ats_qa" and not data.get("extraction_sha256"):
            findings.append("ATS QA lacks extraction hash")
    visual = record.get("visual_qa") or {}
    if visual.get("pdf_sha256") != actual.get("pdf"):
        findings.append("visual QA does not bind to PDF hash")
    if visual.get("inspection_mode") != "INDIVIDUAL_FULL_PAGE":
        findings.append("contact sheet or unrecorded inspection cannot satisfy visual QA")
    pages = visual.get("rendered_pages") or []
    if not pages:
        findings.append("no rendered pages recorded")
    if visual.get("pdf_page_count") != len(pages):
        findings.append("rendered-page list does not match recorded PDF page count")
    for i, page in enumerate(pages, 1):
        path = base / page.get("path", "")
        if not page.get("path") or not path.is_file() or sha(path) != page.get("sha256"):
            findings.append(f"page {i} render missing or hash mismatch")
        if not page.get("inspected_individually"):
            findings.append(f"page {i} lacks individual inspection")
    if not visual.get("reviewer") or not visual.get("timestamp") or not visual.get("template_reference_sha256"):
        findings.append("visual QA lacks reviewer, timestamp, or reference hash")
    if record.get("batch"):
        batch = record["batch"]
        canary = batch.get("canary") or {}
        if canary.get("result") != "PASS" or not canary.get("approved_at") or not canary.get("artifact_sha256"):
            findings.append("batch lacks approved canary before fan-out")
        try:
            approved = datetime.fromisoformat(canary["approved_at"])
            started = datetime.fromisoformat(batch["fanout_started_at"])
            if approved >= started:
                findings.append("canary approval did not precede batch fan-out")
        except (KeyError, TypeError, ValueError):
            findings.append("batch lacks valid canary/fan-out timestamps")
    return findings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("record", type=Path)
    args = p.parse_args()
    findings = verify(json.loads(args.record.read_text()), args.record.parent)
    for finding in findings:
        print("FAIL:", finding)
    if findings:
        return 1
    print("PASS: hash-bound release evidence complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
