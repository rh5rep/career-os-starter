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
Artifact build may format, wrap, place, paginate, adjust spacing, make layout-safe wording changes that preserve meaning, extract ATS/text, and inspect visual quality.

Artifact build may **not** silently change positioning, reinterpret the JD, select different substantive evidence, invent achievements, resolve `HOLD`/`UNKNOWN` claims, change legal answers, or materially broaden ownership/scope. If layout exposes a semantic problem, return to compiler → review → artifact build.

## QA
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
