---
name: process-closeout
description: Record human-confirmed submissions and later employer-process changes using append-only events, compact workflow state, and separate process stage.
---
# Process Closeout

Use this Skill after an actual submission or any confirmed employer-process change.

## Invariants
- Prepared files, opened forms, drafts, and intent do not prove submission.
- Record `SUBMITTED` only after explicit human confirmation.
- Unknown remains `UNKNOWN`; never reconstruct missing history as fact.
- Workflow state is exactly `ACTIVE`, `WAITING`, `DONE`, or `DROPPED`.
- Process stage is separate.
- `WAITING` requires what/who is awaited plus a review date or trigger.
- A scheduled event is not a completed event. A closed role is not automatically a candidate rejection.

## On submission
Record exact known employer/role/opportunity ID, material filenames/versions, source/platform/channel, date, confirmation, networking decision, actual outreach state, process stage, workflow state, next action, owner, and date/trigger. Do not record legal or compensation answers unless the candidate confirms what was submitted.

## Later changes
Append the most specific supported event: recruiter contact, screen scheduled/completed, assessment received/completed, interview scheduled/completed, reference check, rejection, withdrawal, role closed, offer received/accepted/declined, or other explicit state change. Preserve the source/confirmation and never rewrite prior events merely to make history cleaner.

## Learning boundary
Events may inform later analysis, but one outcome cannot prove why it happened. Material workflow changes go through a learning proposal and human approval.
