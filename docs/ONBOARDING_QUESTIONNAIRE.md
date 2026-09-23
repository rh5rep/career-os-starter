# Beginner Onboarding Questionnaire

This is an internal human-readable companion to the single friend-facing onboarding prompt in `user_actions/START.md`. The system should ask these in **small batches**, not as one giant form. The candidate should not manually maintain YAML or evidence IDs.

## Stage 0 — Existing sources and artifact assets
Ask what already exists: resume/CV, LinkedIn export or profile information, cover-letter example, portfolio/work samples, certifications/licenses, transcripts, and other career records. Treat these as sources to reconcile, not automatic truth. Also ask which existing resume/CV/letter templates should be preserved and whether any logos/media are genuinely part of that document system. Register approved assets in `canonical/TEMPLATE_REGISTRY.yaml`.

## Stage 1 — Identity and current state
- What name should applications use?
- What email/phone/portfolio/LinkedIn should be used, if any?
- What is your current city or region?
- Are you open to relocation? Where?
- When could you start a new role?
- What is your current employment status?
- For each country you may target, what do you know about your right to work and sponsorship needs?
- Which of those answers are fully verified versus uncertain?

## Stage 2 — Education
For each institution: institution, degree/program, field, dates, completion status, distinctions/awards, and relevant coursework only when useful. Flag uncertain dates or wording.

## Stage 3 — Work history
For each role: employer, title, dates, responsibilities, projects, problem/objective, **your** contribution, tools/methods, outcomes, metrics, collaborators/stakeholders, artifacts/proof, and uncertainty.

Useful follow-ups:
- What did you personally decide, build, write, analyze, coordinate, sell, test, present, or improve?
- What belonged to the team rather than you?
- Who used the output?
- What changed because of the work?
- Is there a metric? How was it measured and whose result was it?
- What would be an overstatement of this work?

## Stage 4 — Other evidence
Freelance/client work, volunteering, clubs, leadership, side projects, publications, certifications/licenses, awards, presentations, portfolio work, entrepreneurial work, customer/client work, community work, teaching/mentoring, or other useful evidence.

## Stage 5 — Preferences
Locations, remote/hybrid/onsite, commute, travel, industries, exclusions, role types, company size/stage, compensation, work-life, mission, management style, team environment, and lifestyle constraints. Classify each as HARD / STRONG / SOFT / EXPERIMENTAL.

## Stage 6 — Role hypotheses
- What roles do you already think you want?
- What adjacent functions might use the same evidence?
- Which paths are experiments rather than commitments?
- What roles should be deprioritized or excluded?
- What evidence supports each hypothesis and what gaps exist?

## Stage 7 — Search constraints and readiness
Urgency, weekly application capacity, networking comfort, interview readiness, portfolio/work-sample readiness, legal constraints, and any deadlines.

## Uncertainty is allowed
At any stage, valid answers include: **“I don't know,” “I need to verify,”** and **“I think so but am not sure.”** Those answers become HOLD or UNKNOWN rather than polished guesses.


## Stage 8 — Human-readable approval
Before treating setup as complete, present a plain-English summary of identity/current state, education, work history, strongest evidence, skills/certifications, preferences/constraints, role hypotheses, work authorization status, networking/interview readiness, and registered templates. List all material HOLD/UNKNOWN items separately. Only after the candidate approves or corrects this summary should the system finalize canonical files and mark onboarding complete.
