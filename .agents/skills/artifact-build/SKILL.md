---
name: artifact-build
description: Build and quality-check resume, CV, letter, portfolio, or other approved application artifacts from semantically reviewed content.
---
# Artifact Build

Own the boundary from `READY_FOR_ARTIFACT` to `READY_FOR_HUMAN_RELEASE`, `RETURN_FOR_SEMANTIC_REVISION`, or `HOLD`.

## Inputs
Use the exact target/JD reference, reviewed semantic packet, review disposition, chosen artifact profile, `canonical/TEMPLATE_REGISTRY.yaml`, current-state identity/contact data, and unresolved holds. Prefer a registered candidate-approved existing format when suitable; do not impose a universal design.

If no suitable template is registered and candidate-approved, stop at `HOLD` and ask the candidate to register or explicitly approve a format before producing a final application artifact. This does not block onboarding, discovery, triage, or semantic application work. Never silently create or label a design as approved.

## Allowed work

Treat the approved template as an OOXML structural contract. Replace text placeholders in place or deliberately reconstruct a whole paragraph from a reviewed structural model. Never erase visible text while leaving tabs, drawings, fields, or other controls and append new content after them. `scripts/safe_docx_population.py` gives strict in-place helpers. Register a structural fingerprint with `scripts/audit_docx_structure.py --fingerprint-out` whenever an approved DOCX is registered or changed.
Artifact build may format, wrap, place, paginate, adjust spacing, make layout-safe wording changes that preserve meaning, extract ATS/text, and inspect visual quality.

Artifact build may **not** silently change positioning, reinterpret the JD, select different substantive evidence, invent achievements, resolve `HOLD`/`UNKNOWN` claims, change legal answers, or materially broaden ownership/scope. If layout exposes a semantic problem, return to compiler → review → artifact build.

## QA
Run template-derived structural comparison (`scripts/audit_docx_structure.py <template> <artifact>`) before profile-specific checks. ATS/text extraction, structural, visual, and semantic QA are separate required gates. A parser pass, batch consistency, contact sheet, or pixel identity to a prior broken render cannot satisfy another gate.

For a new or materially changed template, generation path, renderer, or logo/media path, produce one canary and pass all four gates before fan-out. Render every final page and inspect it individually at readable/full-page scale against the approved template or canary. A contact sheet is only an overview. After any final patch, rerender and recheck. Keep hash-bound gate evidence using `scripts/verify_artifact_release.py`; the visual reviewer must inspect final pages rather than generator summaries.
Check:
- semantic fidelity and claim provenance;
- current identity/contact/location and authorization wording;
- no stale target/company text;
- correct artifact profile and expected page count;
- ATS/text extraction and reading order where relevant;
- selectable text when required;
- clipping, broken sections, bad wraps, hidden text, unreasonable density, and unexplained underuse;
- template/logo/image correctness when those assets are used;
- placeholders and accidental source-template remnants;
- visual hierarchy, spacing, alignment, typography, and every rendered page;
- paired visual-family consistency for resume/CV and letter when applicable.

## Human release
Only a passing artifact can be marked `READY_FOR_HUMAN_RELEASE`. The candidate approves what is actually sent. This Skill never submits applications or sends networking messages.
