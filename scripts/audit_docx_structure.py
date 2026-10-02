#!/usr/bin/env python3
"""Register a template fingerprint or compare an artifact to a template."""
from __future__ import annotations

import argparse
from pathlib import Path

from docx_structure import validate_artifact, validate_template, validate_registration, write_fingerprint


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("template", type=Path)
    p.add_argument("artifact", nargs="?", type=Path)
    p.add_argument("--fingerprint-out", type=Path)
    p.add_argument("--fingerprint", type=Path, help="Previously registered fingerprint to enforce exact source hash")
    args = p.parse_args()
    findings = validate_template(args.template)
    if args.fingerprint_out:
        write_fingerprint(args.template, args.fingerprint_out)
    if args.fingerprint:
        findings.extend(validate_registration(args.template, args.fingerprint))
    if args.artifact:
        findings.extend(validate_artifact(args.template, args.artifact))
    for finding in findings:
        print("FAIL:", finding)
    if findings:
        return 1
    print("PASS: template structure" if not args.artifact else "PASS: artifact structure matches template contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
