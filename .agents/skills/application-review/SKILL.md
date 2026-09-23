---
name: application-review
description: Orchestrate independent recruiter, hiring-manager, and configurable domain-specialist reviews after compilation and before artifact release.
---
# Application Review

The drafting pass cannot approve itself. Review observations are not career evidence.

## Reviewer configuration
Universal lenses:
- `reviewer-recruiter`
- `reviewer-hiring-manager`

Configurable third lens:
- `reviewer-domain-specialist`, whose perspective is derived from the exact JD and optional `domain_modules/` configuration.

For v0.1 pilot use all three for serious applications so redundancy and unique value can be measured. This is a pilot default, not a permanent universal requirement.

## Isolation
Each reviewer receives the same verified bundle: exact JD/snapshot, relevant canonical evidence/current state, material verified company context, and the packet/draft. Do not show generator rationale, desired conclusions, or other reviewers' findings before each pass is complete.

## Procedure
1. Verify the common input bundle and target version.
2. Run recruiter, hiring-manager, and domain-specialist passes independently.
3. Require concrete findings tied to packet/artifact locations and relevant evidence IDs where applicable.
4. Consolidate duplicates without erasing lens attribution.
5. Preserve disagreement explicitly; do not average it away.
6. Disposition each meaningful finding as `FIXED`, `ACCEPTED_RISK`, `NOT_APPLICABLE`, `REJECTED_FINDING`, or `UNRESOLVED`.
7. Send factual/semantic defects, evidence reselection, positioning changes, or substantial claim rewrites back to `application-compiler`.
8. Do not penalize an application merely because strong evidence, bullets, projects, profile structure, or skills also appear in other applications. Cross-application repetition is acceptable when it is still the strongest supported choice for the exact JD. Flag only stale/non-targeted reuse, ignored stronger evidence, or unsupported keyword carryover.
9. Return one release recommendation: `READY_FOR_ARTIFACT`, `REVISE`, or `HOLD`.

## Completion gate
`READY_FOR_ARTIFACT` means semantic review is complete. It is not artifact release or submission approval.
