#!/usr/bin/env python3
"""Deterministic validator for Career Search OS Friend Pilot.

Checks structure, parseability, and core workflow invariants. It does not judge
candidate fit or rewrite facts to make validation pass.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATES = {"ACTIVE", "WAITING", "DONE", "DROPPED"}
EVIDENCE_STATUSES = {"VERIFIED", "SUPPORTED", "HOLD", "UNKNOWN"}

REQUIRED = [
    "README.md", "START_HERE.md", "QUICK_START.md", "SETUP_GITHUB.md", "TEMPLATE_SETUP.md", "FRIEND_HANDOFF.md", "AGENTS.md",
    "user_actions/START.md", "user_actions/FIND_OPPORTUNITIES.md",
    "user_actions/BUILD_APPLICATIONS.md", "user_actions/RECORD_UPDATE.md",
    "canonical/CURRENT_STATE.yaml", "canonical/CAREER_EVIDENCE.yaml",
    "canonical/CAREER_PREFERENCES.md", "canonical/ROLE_HYPOTHESES.md",
    "canonical/SKILLS_EVIDENCE.md", "canonical/MASTER_CAREER_CV.md",
    "canonical/TEMPLATE_REGISTRY.yaml",
    "generated/WORKFLOW_MANIFEST.yaml",
    "schemas/current_state.schema.json", "schemas/career_evidence.schema.json",
    "schemas/opportunity.schema.json", "schemas/application_packet.schema.json",
    "schemas/review_run.schema.json", "schemas/process_event.schema.json",
    "schemas/learning_proposal.schema.json", "schemas/workflow_issue.schema.json",
    ".agents/skills/career-os-coordinator/SKILL.md",
    ".agents/skills/opportunity-strategy/SKILL.md",
    ".agents/skills/application-compiler/SKILL.md",
    ".agents/skills/application-review/SKILL.md",
    ".agents/skills/artifact-build/SKILL.md",
    ".agents/skills/process-closeout/SKILL.md",
    ".agents/skills/reviewer-recruiter/SKILL.md",
    ".agents/skills/reviewer-hiring-manager/SKILL.md",
    ".agents/skills/reviewer-domain-specialist/SKILL.md",
    "docs/PILOT_FEEDBACK_LOG.md", "docs/ONBOARDING_QUESTIONNAIRE.md", "docs/FRIEND_QUICKSTART_PDF_SOURCE.md",
    "docs/internal/PILOT_UX_VALIDATION.md",
    "workflow_issues/README.md", "learning_proposals/README.md",
    "scripts/test_portable_invariants.py", "scripts/test_friend_pilot_ux.py",
]

JSON_SCHEMAS = [
    "schemas/current_state.schema.json", "schemas/career_evidence.schema.json",
    "schemas/opportunity.schema.json", "schemas/application_packet.schema.json",
    "schemas/review_run.schema.json", "schemas/process_event.schema.json",
    "schemas/learning_proposal.schema.json", "schemas/workflow_issue.schema.json",
]


def load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for validation") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"MISSING: {rel}")
        elif p.is_file() and p.stat().st_size == 0:
            errors.append(f"EMPTY: {rel}")

    for rel in JSON_SCHEMAS:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"JSON PARSE FAILED {rel}: {exc}")

    yaml_files = [
        "canonical/CURRENT_STATE.yaml", "canonical/CAREER_EVIDENCE.yaml",
        "canonical/TEMPLATE_REGISTRY.yaml", "pipeline/OPPORTUNITIES.yaml",
        "pipeline/APPLICATIONS.yaml", "pipeline/NETWORKING.yaml",
        "pipeline/OUTCOMES.yaml", "generated/WORKFLOW_MANIFEST.yaml",
    ]
    for rel in yaml_files:
        try:
            value = load_yaml(ROOT / rel)
            if value is None:
                errors.append(f"YAML EMPTY: {rel}")
        except Exception as exc:
            errors.append(f"YAML PARSE FAILED {rel}: {exc}")

    try:
        evidence = load_yaml(ROOT / "canonical/CAREER_EVIDENCE.yaml")
        records = evidence.get("records", []) if isinstance(evidence, dict) else []
        seen = set()
        for i, record in enumerate(records, 1):
            if not isinstance(record, dict):
                errors.append(f"EVIDENCE record {i} is not an object")
                continue
            evid = record.get("id")
            status = record.get("status")
            if not evid:
                errors.append(f"EVIDENCE record {i} missing id")
            elif evid in seen:
                errors.append(f"EVIDENCE duplicate id: {evid}")
            else:
                seen.add(evid)
            if status not in EVIDENCE_STATUSES:
                errors.append(f"EVIDENCE {evid or i} invalid/missing status: {status!r}")
            if "personal_contribution" not in record or "source_proof" not in record or "not_justified" not in record:
                errors.append(f"EVIDENCE {evid or i} missing contribution/source/boundary fields")
    except Exception as exc:
        errors.append(f"EVIDENCE VALIDATION FAILED: {exc}")

    try:
        registry = load_yaml(ROOT / "canonical/TEMPLATE_REGISTRY.yaml")
        if not isinstance(registry, dict) or "assets" not in registry or "candidate_approved" not in registry:
            errors.append("TEMPLATE REGISTRY missing assets/candidate_approved")
    except Exception as exc:
        errors.append(f"TEMPLATE REGISTRY VALIDATION FAILED: {exc}")

    try:
        opp = load_yaml(ROOT / "pipeline/OPPORTUNITIES.yaml")
        records = opp.get("opportunities", []) if isinstance(opp, dict) else []
        for i, row in enumerate(records, 1):
            state = row.get("workflow_state")
            if state not in ALLOWED_STATES:
                errors.append(f"OPPORTUNITY {i} invalid workflow_state: {state!r}")
            if state == "WAITING" and (not row.get("waiting_for") or not row.get("review_date_or_trigger")):
                errors.append(f"OPPORTUNITY {i}: WAITING requires waiting_for and review_date_or_trigger")
    except Exception as exc:
        errors.append(f"OPPORTUNITY VALIDATION FAILED: {exc}")

    events = ROOT / "pipeline/PROCESS_EVENTS.jsonl"
    if events.exists():
        for n, line in enumerate(events.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except Exception as exc:
                errors.append(f"PROCESS_EVENTS line {n} JSON parse failed: {exc}")
                continue
            if event.get("workflow_state_after") not in ALLOWED_STATES | {None}:
                errors.append(f"PROCESS_EVENTS line {n} bad workflow state")
            if event.get("event_type") == "SUBMITTED":
                if event.get("human_confirmed") is not True or event.get("confirmation") is not True:
                    errors.append(f"PROCESS_EVENTS line {n}: SUBMITTED must be human-confirmed")
                if not event.get("materials"):
                    errors.append(f"PROCESS_EVENTS line {n}: SUBMITTED requires exact materials")
            if event.get("workflow_state_after") == "WAITING":
                if not event.get("waiting_for") or not (event.get("review_date") or event.get("review_trigger")):
                    errors.append(f"PROCESS_EVENTS line {n}: WAITING requires dependency + date/trigger")

    actions = list((ROOT / "user_actions").glob("*.md"))
    if len(actions) != 4:
        errors.append(f"UX SURFACE: expected 4 user action files, found {len(actions)}")

    if errors:
        print("CAREER SEARCH OS FRIEND PILOT VALIDATION: FAIL")
        for err in errors:
            print(f"- {err}")
        return 1
    print("CAREER SEARCH OS FRIEND PILOT VALIDATION: PASS")
    print(f"Root: {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
