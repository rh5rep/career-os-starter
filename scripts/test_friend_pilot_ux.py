#!/usr/bin/env python3
"""Small deterministic checks for the friend-facing UX surface."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []

    # The friend-facing surface should remain small.
    actions = sorted((ROOT / "user_actions").glob("*.md"))
    if len(actions) != 4:
        errors.append(f"UX: expected exactly 4 friend-facing action files, found {len(actions)}")

    required_top = ["START_HERE.md", "QUICK_START.md", "SETUP_GITHUB.md", "TEMPLATE_SETUP.md"]
    for rel in required_top:
        if not (ROOT / rel).exists():
            errors.append(f"UX: missing {rel}")

    coordinator = ROOT / ".agents/skills/career-os-coordinator/SKILL.md"
    if not coordinator.exists():
        errors.append("UX: front-door coordinator Skill missing")
    else:
        c = coordinator.read_text(encoding="utf-8")
        for route in ["SETUP", "DISCOVERY", "TRIAGE", "APPLICATION", "NETWORKING", "INTERVIEW", "CLOSEOUT", "SYSTEM_MAINTENANCE"]:
            if route not in c:
                errors.append(f"UX: coordinator missing route {route}")
        if "do not ask them to select skills" not in c.lower():
            errors.append("UX: coordinator does not explicitly hide internal workflow selection")

    start = read("user_actions/START.md")
    for concept in ["resume/CV", "LinkedIn", "certifications/licenses", "work authorization", "compensation", "role hypotheses", "networking", "availability", "plain-English profile summary"]:
        if concept.lower() not in start.lower():
            errors.append(f"ONBOARDING: missing {concept}")
    if "do not ask me to edit YAML" not in start:
        errors.append("ONBOARDING: candidate could be pushed into manual YAML")

    github = read("SETUP_GITHUB.md")
    if "no terminal required" not in github.lower():
        errors.append("GITHUB: simple path is not clearly terminal-free")
    if "Private" not in github:
        errors.append("GITHUB: private repo requirement missing")

    start_here = read("START_HERE.md")
    for example in ["Find jobs for me in Boston and NYC", "Build applications for the top three", "I submitted Company A and Company B today", "I have an interview with Company X next Tuesday"]:
        if example not in start_here:
            errors.append(f"UX: missing natural-language example {example!r}")

    if errors:
        print("FRIEND PILOT UX TESTS: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("FRIEND PILOT UX TESTS: PASS")
    print("Friend-facing surface: 4 action files; one onboarding prompt; natural-language routing; browser-first private GitHub setup; internal concepts hidden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
