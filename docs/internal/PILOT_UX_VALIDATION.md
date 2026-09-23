# Friend Pilot UX Validation — Synthetic Operations Candidate

**Purpose:** test whether the candidate can use the system without understanding its internal architecture. This walkthrough uses the existing fictional operations persona and synthetic opportunities only; it is not a live job search.

## Persona

Taylor Morgan, fictional Operations Coordinator. Existing synthetic evidence includes maintaining a scheduling workbook used by 15 staff and coordinating routine vendor arrivals. The evidence explicitly does not support claims such as workforce-strategy ownership or vendor-contract negotiation.

## Simulated walkthrough

### 1. Repository setup
**Friend action:** open the public starter, choose **Use this template**, create a new private repository in their own account, and connect the AI workspace to that private copy. Download/upload remains a fallback only.

**Internal concepts exposed:** private repository, files. No terminal, branch, schema, or Git object knowledge required.

### 2. Onboarding
**Friend manually selects:** one prompt — `user_actions/START.md`.

**Friend provides:** current resume, LinkedIn profile notes, and an existing clean one-page resume template. No CV or letter template.

**Coordinator behavior:** asks in small rounds; creates internal evidence records and identifiers; marks uncertain work-authorization detail `UNKNOWN`; registers the resume template; does not ask Taylor to edit YAML.

### 3. Profile approval
**System shows:** a plain-English summary containing current identity/contact, employment history, education, strongest accomplishments, skills, work authorization status, hard/strong/soft preferences, role hypotheses, availability, and template choice. It separately lists unresolved authorization information.

**Friend action:** correct one date and approve the profile.

**System behavior:** updates canonical files, leaves the unresolved authorization item visible, validates the repo.

### 4. Bounded search request
**Friend says:** “Find operations jobs for me in Boston and NYC.”

**Coordinator behavior:** interprets this as `DISCOVERY`, runs a bounded search workflow internally, deduplicates, and returns a manageable board rather than producing resumes immediately.

### 5. Triage
**Friend says:** “Which of these are actually worth applying to?”

**Coordinator behavior:** routes top roles through opportunity strategy and presents supported fit, gaps, form/legal issues, and a small recommended pursue/stretch/watch/skip surface. It does not show evidence IDs or reviewer internals unless asked.

**Override check:** one synthetic role is labeled `SKIP` because its requirements are a poor fit. Taylor says, “I still want to apply to that one.” The system retains `SKIP` as the prior triage recommendation and records `HUMAN_OVERRIDE`; it does not rewrite history.

### 6. Application build
**Friend says:** “Build the application for the first role.”

**Coordinator behavior:** routes through exact-JD verification/preflight, compiler, independent review, and artifact build. It uses the registered one-page resume template. Evidence that also appeared in another application is not rejected merely for repetition; it is kept when still strongest for this JD.

**Friend action:** review and approve the finished artifact. Submission remains manual.

### 7. Submission closeout
**Friend says:** “I submitted it today through the company site using the resume you made.”

**Coordinator behavior:** asks only for any missing confirmation/material detail, then records a human-confirmed submission, exact material, process stage, operational state, and next review trigger.

## UX measurements

- **Specialized prompts manually selected by the user after setup:** 0.
- **Prompt-library choices required:** 1 total, the initial onboarding prompt.
- **Command-line Git knowledge required:** none.
- **Internal concepts the beginner needed to understand:** effectively none beyond “private repo,” “profile,” “job,” “application,” and “status.”
- **Schemas exposed:** 0.
- **Evidence IDs exposed:** 0.
- **Reviewer-selection decisions exposed:** 0.
- **Application-packet mechanics exposed:** 0.

## Where a beginner may still hesitate

1. Connecting the AI workspace to a private GitHub repository varies by product/account setup.
2. Deciding whether an old resume format is genuinely good enough to preserve can require judgment.
3. Work-authorization questions may require outside verification and must remain unresolved until the candidate confirms them.
4. Uploading very large or scattered career archives can create onboarding noise; the coordinator should process sources in batches.

## Friction removed in this pass

- Added one front-door coordinator.
- Reduced visible prompt choices to four, with one true onboarding prompt.
- Made interview/networking natural-language routes.
- Added candidate-approved template registration.
- Made the template-first private-copy path browser-only, with download/upload as a fallback.
- Made human override explicit without falsifying triage history.
- Prevented cross-application overlap from becoming an artificial differentiation requirement.
- Moved normal users away from the long handbook/internal prompt library.

## Result

The simulated beginner can complete repo setup → onboarding → profile approval → discovery → triage → application build → submission closeout without manually selecting internal workflows or editing structured data. The main remaining friction is external connection/setup variability rather than Career OS concepts.
