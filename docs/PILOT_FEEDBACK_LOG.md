# Pilot Feedback Log

The portable system is being built while the source Career Search V2.5 pilot is still being validated. New lessons must not silently become universal rules.

## Allowed status

`PENDING` · `APPROVED` · `REJECTED` · `NEEDS_MORE_EVIDENCE`

## Entry template

### PF-YYYY-MM-DD-### — Short title
- **Observation:**
- **Source / context:**
- **Reproducible?** YES / NO / UNKNOWN
- **Scope:** CANDIDATE_SPECIFIC / DOMAIN_SPECIFIC / PORTABLE_SYSTEM
- **Proposed portable-system impact:**
- **Alternative explanations:**
- **Does not mean:**
- **Status:** PENDING
- **Human decision / date:**
- **Follow-up validation:**

## Current seed items

### PF-2026-09-23-001 — Three-reviewer default
- **Observation:** the source V2.5 pilot currently runs recruiter, hiring-manager, and technical-principal lenses for serious applications.
- **Reproducible?** UNKNOWN across domains.
- **Scope:** PORTABLE_SYSTEM
- **Proposed impact:** use recruiter + hiring manager + configurable domain specialist during v0.1 pilot and measure redundancy/value.
- **Status:** NEEDS_MORE_EVIDENCE

### PF-2026-09-23-002 — One-page composition optimization
- **Observation:** the source pilot identified a truthful but over-compressed one-page composition and added a semantic return loop when rendering exposed unused capacity.
- **Reproducible?** UNKNOWN across templates/domains.
- **Scope:** PORTABLE_SYSTEM
- **Proposed impact:** keep the general “use finite space deliberately” principle; do not encode exact density thresholds or fixed alternative-count rules as universal.
- **Status:** NEEDS_MORE_EVIDENCE

### PF-2026-09-23-003 — Cross-application overlap is allowed
- **Observation:** repeated evidence, bullets, projects, profile structure, or skills may legitimately remain the strongest supported content across multiple exact JDs.
- **Source / context:** friend-pilot UX simplification correction.
- **Reproducible?** YES as a workflow principle; target-specific quality still requires review.
- **Scope:** PORTABLE_SYSTEM
- **Proposed portable-system impact:** do not flag repetition by itself. Flag only lazy/non-targeted composition, stale company text, ignored stronger evidence, or unsupported keyword reuse.
- **Alternative explanations:** some repeated language may still indicate under-tailoring, so exact-JD review remains necessary.
- **Does not mean:** every application should be identical or that stale content is acceptable.
- **Status:** APPROVED
- **Human decision / date:** approved in pilot simplification pass, 2026-09-23.
- **Follow-up validation:** observe whether cross-batch review finds meaningful target-specific defects rather than artificial-differentiation pressure.

### PF-2026-09-23-004 — Human override of SKIP
- **Observation:** a candidate may deliberately choose to apply even when the system recommends `SKIP`.
- **Source / context:** friend-pilot UX simplification correction.
- **Reproducible?** YES as a human-agency boundary.
- **Scope:** PORTABLE_SYSTEM
- **Proposed portable-system impact:** permit application build after explicit human override while preserving the original `SKIP` recommendation and recording `HUMAN_OVERRIDE` as the candidate decision.
- **Alternative explanations:** an override may reflect non-fit reasons such as curiosity, relationship value, or asymmetric upside.
- **Does not mean:** the prior triage should be rewritten as `PURSUE`, or that hard legal/verification blockers should be ignored.
- **Status:** APPROVED
- **Human decision / date:** approved in pilot simplification pass, 2026-09-23.
- **Follow-up validation:** track overrides separately from system-recommended pursuit so later learning does not erase the decision provenance.
