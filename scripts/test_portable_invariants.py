#!/usr/bin/env python3
"""Regression checks for the generic Career Search OS friend pilot."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    # 1) Friend-safe examples and friend-facing docs should not contain direct personal identifiers.
    friend_paths = [
        ROOT / "README.md", ROOT / "START_HERE.md", ROOT / "QUICK_START.md",
        ROOT / "SETUP_GITHUB.md", ROOT / "TEMPLATE_SETUP.md", ROOT / "FRIEND_HANDOFF.md",
        ROOT / "docs/FRIEND_QUICKSTART_PDF_SOURCE.md",
    ]
    friend_paths += [p for p in (ROOT / "user_actions").glob("*.md")]
    friend_paths += [p for p in (ROOT / "examples").rglob("*") if p.is_file()]
    forbidden_patterns = ["SOURCE_CANDIDATE_PRIVATE_DATA", "SOURCE_CANDIDATE_CONTACT", "SOURCE_REPO_PRIVATE_IDENTIFIER"]
    for p in friend_paths:
        data = p.read_text(encoding="utf-8", errors="ignore").lower()
        for token in forbidden_patterns:
            if token.lower() in data:
                failures.append(f"SANITIZATION: {p.relative_to(ROOT)} contains a source-candidate identifier pattern")

    # 2) Evidence status is required and HOLD/UNKNOWN are explicit in compiler.
    evidence_schema = json.loads(text("schemas/career_evidence.schema.json"))
    req = set(evidence_schema["$defs"]["evidence"]["required"])
    if "status" not in req:
        failures.append("EVIDENCE: status is not required")
    compiler = text(".agents/skills/application-compiler/SKILL.md")
    if "HOLD" not in compiler or "UNKNOWN" not in compiler or "cannot become applicant-facing" not in compiler:
        failures.append("EVIDENCE: compiler lacks HOLD/UNKNOWN external-claim boundary")

    # 3) Authorization must never be silently inferred.
    auth_prompt = text("prompts/onboarding/WORK_AUTHORIZATION_SETUP.md") + text("prompts/applications/APPLICATION_FORM_PREFLIGHT.md") + text("AGENTS.md")
    if "never infer" not in auth_prompt.lower():
        failures.append("AUTHORIZATION: no explicit no-inference rule")
    if "NEEDS_HUMAN_ANSWER" not in auth_prompt:
        failures.append("AUTHORIZATION: missing NEEDS_HUMAN_ANSWER gate")

    # 4) Generated artifacts must not imply submission.
    closeout = text(".agents/skills/process-closeout/SKILL.md") + text("docs/CLOSEOUT_PROCESS_MODEL.md")
    if "do not prove submission" not in closeout.lower() or "explicit human confirmation" not in closeout.lower():
        failures.append("SUBMISSION: explicit confirmation invariant missing")

    # 5) Internal discovery references stay bounded.
    discovery = list((ROOT / "prompts/discovery").glob("*.md"))
    if len(discovery) < 4:
        failures.append("DISCOVERY: bounded internal discovery references missing")
    for p in discovery:
        d = p.read_text(encoding="utf-8").lower()
        if not any(k in d for k in ["maximum", "at most", "bound", "stop"]):
            failures.append(f"DISCOVERY: no clear bound/stop wording in {p.name}")

    # 6) Reviewer isolation and configurable domain specialist.
    review = text(".agents/skills/application-review/SKILL.md")
    specialist = text(".agents/skills/reviewer-domain-specialist/SKILL.md")
    if "independently" not in review.lower() or "do not show" not in review.lower():
        failures.append("REVIEW: reviewer isolation wording missing")
    if "must not assume engineering" not in specialist.lower():
        failures.append("REVIEW: domain specialist is not explicitly domain-agnostic")
    review_schema = json.loads(text("schemas/review_run.schema.json"))
    if "DOMAIN_SPECIALIST" not in review_schema["properties"]["reviewer_lens"]["enum"]:
        failures.append("REVIEW: configurable DOMAIN_SPECIALIST missing from schema")

    # 7) Portable core does not require technical/engineering evidence.
    core = text("AGENTS.md") + text("QUICK_START.md") + text("docs/ONBOARDING_QUESTIONNAIRE.md")
    for phrase in ["must have github", "requires coding", "technical projects are required", "engineering evidence is required"]:
        if phrase in core.lower():
            failures.append(f"DOMAIN: portable core contains engineering-only requirement {phrase!r}")

    # 8) Learning cannot auto-rewrite rules.
    learning_schema = json.loads(text("schemas/learning_proposal.schema.json"))
    prop = learning_schema["properties"].get("automatic_rule_rewrite_allowed", {})
    if prop.get("const") is not False:
        failures.append("LEARNING: automatic_rule_rewrite_allowed must be false")

    # 9) Four-state model remains exact.
    opportunity_schema = json.loads(text("schemas/opportunity.schema.json"))
    states = set(opportunity_schema["properties"]["workflow_state"]["enum"])
    if states != {"ACTIVE", "WAITING", "DONE", "DROPPED"}:
        failures.append(f"STATE: unexpected workflow-state set {states}")

    # 10) Human override preserves a distinct decision state.
    if "HUMAN_OVERRIDE" not in opportunity_schema["properties"]["human_decision"]["enum"]:
        failures.append("HUMAN AGENCY: opportunity schema lacks HUMAN_OVERRIDE")
    packet_schema = json.loads(text("schemas/application_packet.schema.json"))
    if "HUMAN_OVERRIDE" not in packet_schema["properties"]["human_decision"]["enum"]:
        failures.append("HUMAN AGENCY: application packet lacks HUMAN_OVERRIDE")
    strategy = text(".agents/skills/opportunity-strategy/SKILL.md")
    if "preserve" not in strategy.lower() or "HUMAN_OVERRIDE" not in strategy:
        failures.append("HUMAN AGENCY: strategy does not preserve prior SKIP on override")

    # 11) Cross-application repetition is not treated as an automatic defect.
    if "artificial differentiation" not in text("AGENTS.md").lower() or "cross-application repetition is acceptable" not in review.lower():
        failures.append("CROSS-APPLICATION: overlap allowance missing")

    # 12) Template registry exists and artifact-build consumes it.
    if not (ROOT / "canonical/TEMPLATE_REGISTRY.yaml").exists():
        failures.append("TEMPLATES: template registry missing")
    if "TEMPLATE_REGISTRY.yaml" not in text(".agents/skills/artifact-build/SKILL.md"):
        failures.append("TEMPLATES: artifact-build does not consult template registry")

    if failures:
        print("PORTABLE INVARIANT TESTS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PORTABLE INVARIANT TESTS: PASS")
    print("Checked sanitization, evidence boundaries, authorization, submission, discovery bounds, reviewer isolation/configuration, domain neutrality, learning control, state model, human override, cross-application overlap, and template registration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
