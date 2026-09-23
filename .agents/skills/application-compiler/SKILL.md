---
name: application-compiler
description: Convert a human-approved opportunity into an evidence-traceable semantic application packet before rendering.
---
# Application Compiler

Start only after a recorded human `PURSUE`, approved stretch, or explicit `HUMAN_OVERRIDE`. When an override follows a system `SKIP`, preserve both the original triage recommendation and the later human choice. The output is semantic content and decisions, not a finished document.

## Authority chain
`CAREER_EVIDENCE.yaml` → `MASTER_CAREER_CV.md` → exact target requirements → evidence selection → target content. Use `CURRENT_STATE.yaml` for current identity/location/availability/authorization and `SKILLS_EVIDENCE.md` for skill wording. A prior tailored resume/CV is never factual authority.

## Procedure
1. Freeze the exact JD reference and human decision. Accept `HUMAN_OVERRIDE` only when it is explicit and the prior triage recommendation remains preserved. Reject mismatched or stale target inputs.
2. Decompose the JD into major requirements. Avoid false precision in importance labels.
3. Retrieve canonical evidence and preserve `VERIFIED`, `SUPPORTED`, `HOLD`, `UNKNOWN`, source/proof, ownership, metric, proficiency, and prohibited-overstatement boundaries.
4. Map evidence to each requirement as strong, partial, gap, or unresolved.
5. Choose primary positioning and optional secondary positioning. Escalate materially ambiguous positioning.
6. Select the artifact profile using country, industry, seniority, evidence volume, role family, and target conventions. Do not assume a one-page engineering resume.
7. Allocate finite attention/space competitively. Prefer the strongest target-relevant evidence; record high-value omissions and why they lost. When meaningful capacity remains, compare plausible additions instead of padding.
8. Draft candidate bullets/claims with provenance. Each material claim records evidence IDs and semantic purpose. New wording is allowed when evidence-grounded.
9. Run an ATS/semantic pass: use supported target terminology naturally; never graft unsupported keywords.
10. Set profile/summary direction only if the chosen artifact profile benefits from one. Avoid keyword dumps and generic objective language.
11. Record letter and networking decisions, but do not manufacture personal motivation. Important personalization must come from verified company context plus confirmed human resonance.
12. Produce a compact application packet using `schemas/application_packet.schema.json` or an equivalent structured in-chat record.

## Claim rule
`HOLD` and `UNKNOWN` evidence may appear inside the packet as unresolved items, but cannot become applicant-facing factual claims until resolved. Internal caution language should not leak into external prose when a positive, accurately scoped claim is available.

## Completion gate
The packet is ready for review only when target identity, requirements, evidence selection, positioning, gaps/holds, artifact profile, and candidate claims are traceable and stable enough for independent reviewers.
