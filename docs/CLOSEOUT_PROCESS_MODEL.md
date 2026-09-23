# Closeout and Process Model

## Two separate questions

**Workflow state** answers: what should the Career OS do now?  
**Process stage** answers: where is the candidate in the employer's process?

Do not collapse them into one field.

## Workflow states

- `ACTIVE` — work is happening now and there is a concrete next action.
- `WAITING` — an external dependency exists; record what/who is awaited plus a review date or trigger.
- `DONE` — a meaningful terminal outcome is known or the process is otherwise complete.
- `DROPPED` — intentionally closed without a known employer terminal outcome because it is stale, superseded, no longer worth pursuing, or cannot be reconstructed safely.

## Process stages

Use specific stages supported by facts, for example discovered, deciding, preparing application, submitted, recruiter contact, screen, assessment, interview, final/onsite, reference check, offer, closed, unknown. Scheduled and completed events are distinct.

## Submission is an event, not a guess

Generated documents do not prove submission. A form opened in a browser does not prove submission. Intent does not prove submission. Create a `SUBMITTED` event only after explicit human confirmation.

After submission, record exact known materials, source/platform/channel, date, confirmation, networking/outreach state, workflow state, process stage, next action, and date/trigger. Unknown fields remain UNKNOWN.

## Append-only history

Prefer append-only process events to rewriting history. Correct an erroneous record transparently rather than silently making the historical sequence cleaner.
