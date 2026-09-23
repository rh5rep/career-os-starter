---
name: opportunity-strategy
description: Evaluate a newly found opportunity through live-JD verification, bounded same-company comparison, form preflight, multidimensional triage, preliminary evidence mapping, and an explicit human decision before tailoring.
---
# Opportunity Strategy

Use this Skill from discovery through the human decision gate. Stop before application compilation.

## Inputs and authority
Follow `AGENTS.md`. Use the employer-hosted posting or employer-linked ATS as the authoritative JD when available. Use `canonical/CURRENT_STATE.yaml` for current facts and constraints, `canonical/CAREER_EVIDENCE.yaml` for career claims, `canonical/CAREER_PREFERENCES.md` for preferences, and `canonical/ROLE_HYPOTHESES.md` as hypotheses rather than identity.

## Procedure
1. **Verify the target.** Capture company, exact title, location, requisition when available, authoritative URL, retrieval date/time, and a snapshot/reference. Mark live status `VERIFIED`, `UNKNOWN`, or `CLOSED`; never rely on a stale mirror when a source posting is available.
2. **Save and deduplicate.** Reuse a stable opportunity ID. Check saved opportunities and process events for the same company/requisition/title/location. Missing history stays unknown.
3. **Bounded same-company role check.** Inspect materially plausible alternatives on the current employer board. Compare seniority, function, evidence fit, domain, location/work arrangement, hard constraints, and unsupported must-haves. Stop after the plausible set is exhausted; do not turn this into a general company-wide search.
4. **Application-form preflight.** Before expensive tailoring where practical, inspect requirements for letters, short answers, salary, authorization/sponsorship, relocation/travel, years of experience, legal attestations, assessments, portfolio/work samples, references/transcripts, file rules, deadlines, and duplicate/cooldown rules. Use `NEEDS_HUMAN_ANSWER` for consequential questions the system cannot answer from canonical state.
5. **Triage without a fake score.** Assess seniority, required experience, functional fit, evidence support, gaps, geography, authorization, compensation, industry, interest, effort, company conflict, and strategic value separately.
6. **Preliminary evidence map.** For major JD requirements, identify evidence IDs, gaps, and `HOLD`/`UNKNOWN` items. Preserve professional/coursework/personal/freelance scope.
7. **Company intelligence and human resonance where useful.** Capture only facts that materially affect the decision, application story, networking, or interview preparation. The human confirms what actually resonates; do not manufacture motivation.
8. **Return a decision surface.** Present target identity, role alternatives, preflight findings, fit/gaps, key evidence IDs, hard blockers, positioning options, and one of `PURSUE`, `PURSUE_AS_STRETCH`, `NETWORK_WATCH`, or `SKIP` as an analysis category. The candidate makes the consequential pursue/skip decision.
9. **Preserve human override.** If the system recommendation is `SKIP` but the candidate explicitly says to apply anyway, retain the original `SKIP` recommendation and record the candidate decision as `HUMAN_OVERRIDE`. Do not rewrite the earlier analysis as pursuit. Continue unless a legal, safety, live-role, or verification blocker actually prevents preparation.

## Completion gate
Do not invoke `application-compiler` until the candidate explicitly approves `PURSUE`, a stretch application, or a recorded `HUMAN_OVERRIDE`. Legal/authorization uncertainty may allow preparation but cannot be converted into an attestation.
