# Career Search OS — Friend Quickstart

## 1. What Career Search OS does

Career Search OS is a private, versioned workspace for a human-led job search. It helps you build a reliable career profile, discover and evaluate roles, prepare tailored application materials, track hiring activity, and learn from outcomes. You use normal language; the structured files and checks stay mostly behind the scenes.

The loop is simple:

**SET UP ONCE → SEARCH → CHOOSE / APPLY → TRACK / PREP → LEARN**

## 2. What to have before starting

Use whatever is available; none of these must be perfect:

- current or older resume/CV;
- LinkedIn export or profile notes;
- cover-letter examples;
- portfolio or work samples;
- certifications or licenses;
- transcript or other useful records;
- document templates you want to preserve.

It is fine to say “I don’t know,” “I need to verify,” or “I think so, but I’m not sure.” Uncertainty should remain visible rather than being turned into fact.

## 3. Create your private GitHub copy

1. Open the [Career Search OS starter](https://github.com/rh5rep/career-os-starter).
2. Choose **Use this template → Create a new repository**.
3. Select your GitHub account, give the copy a name, and set it to **Private**.
4. Connect that private repository to ChatGPT/Codex using the GitHub connection available to you.
5. Keep all personal career information in this private copy—not in the public starter.

If template mode is unavailable, use the browser-only download/upload fallback in `SETUP_GITHUB.md`. The starter files must sit directly at repository root.

## 4. How onboarding works

Open `user_actions/START.md` and send its one prompt. The system first asks for existing materials and preferred templates, then interviews you in manageable rounds about:

- contact details, education, and work history;
- responsibilities, accomplishments, metrics, and your actual contribution;
- skills, certifications, licenses, authorization, and sponsorship;
- location, relocation, work arrangement, commute, and availability;
- compensation constraints, industries, exclusions, and work environment;
- role ideas, networking preferences, and interview readiness.

Uploaded records are sources to reconcile, not unquestioned truth. Claims remain VERIFIED, SUPPORTED, HOLD, or UNKNOWN according to the evidence.

Before setup is finalized, the system shows a plain-English profile review and clearly lists unresolved items. You must correct or explicitly approve it. No silent finalization is allowed.

You may finish onboarding without a document template. Search and triage can continue, but the system must ask you to register or approve a format before it creates a final application artifact.

## 5. Normal daily use

Ask naturally:

> Find jobs for me in Boston and NYC.

> Which of these are worth applying to?

> Build applications for the top three.

> I want to apply to number four anyway.

> I have an interview with Company X next week.

> I submitted these two today.

If you choose to pursue a role the system marked SKIP, it should continue while preserving the original SKIP and recording your decision as HUMAN_OVERRIDE.

## 6. What the system handles automatically

The system can handle evidence identifiers, routine file creation, bounded research, validation, reviewer routing, workflow updates, and artifact quality checks. Reusing the same strongest evidence across multiple applications is acceptable when it genuinely fits each job; artificial variation is not a goal.

## 7. What you still control

You confirm facts and preferences. You decide consequential pursue/skip choices, legal and work-authorization answers, compensation commitments, interview decisions, and offer decisions. You approve final application materials.

**You submit applications and send networking messages yourself.** The system records submission only after you explicitly confirm it happened.

## 8. Simple checklist

- Create a private copy and connect it.
- Send the prompt in `user_actions/START.md`.
- Share available source materials.
- Answer onboarding questions in rounds.
- Correct and approve the plain-English profile review.
- Search for a bounded set of roles.
- Review pursue/stretch/skip recommendations.
- Approve application targets and final materials.
- Submit externally yourself.
- Tell the system what happened so it can close out and track next actions.

## 9. When something looks wrong

- **A fact is wrong or too certain:** stop and correct it; ask the system to mark it HOLD or UNKNOWN until verified.
- **The system asks you to edit YAML, pick a reviewer, or choose an internal Skill:** tell it to handle that internally and record the friction.
- **A template is missing:** continue profile/search work, but register or explicitly approve a format before final artifact creation.
- **A job recommendation seems wrong:** ask for the exact JD evidence, gaps, and reasoning; the final pursue/skip choice is yours.
- **A workflow update is missing:** state the real event, date, channel, materials, and next action. Submission requires your explicit confirmation.
- **Repository access fails:** confirm that the connected GitHub integration can access your private copy and that you did not connect the public starter by mistake.
