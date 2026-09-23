# Start Here

## What this does

Career Search OS keeps one private source of truth about your career, preferences, job-search activity, application materials, and process updates. You interact with it mostly in plain English.

The normal loop is:

**SET UP ONCE → SEARCH → CHOOSE / APPLY → TRACK / PREP → LEARN**

You do **not** need to understand the internal schemas, evidence IDs, Skills, reviewer passes, application packets, or workflow files. The system handles those in the background.

## First-time setup

1. Open the [Career Search OS starter](https://github.com/rh5rep/career-os-starter). Follow `SETUP_GITHUB.md`.
2. Choose **Use this template → Create a new repository**, place it in your own GitHub account, and set it to **Private**.
3. Connect your ChatGPT/Codex workspace to that new private repository using the GitHub connection available to you.
4. Open `user_actions/START.md` and send its single onboarding prompt.
5. Upload whatever you already have: resume/CV, LinkedIn export or profile notes, cover-letter example, portfolio/work samples, certifications/licenses, transcripts, or other career records.
6. Answer the onboarding questions in manageable rounds.
7. Review the final plain-English profile summary. Correct anything wrong or uncertain.
8. Approve the profile. The system then maintains the structured files for you.

You should not need to manually edit YAML.

## Daily use

Once setup is approved, just ask naturally. Examples:

- “Find jobs for me in Boston and NYC.”
- “Focus on remote customer success and implementation roles this week.”
- “Which of these five are actually worth applying to?”
- “Apply anyway to the third one even though you said skip.”
- “Build applications for the top three.”
- “Help me decide whether to message anyone at Company X.”
- “I have an interview with Company X next Tuesday. Prep me.”
- “I submitted Company A and Company B today.”
- “Company C rejected me.”

The coordinator routes the request to the appropriate internal workflow automatically. You should not have to choose a Skill or prompt.

## What still requires you

The system can research, organize, draft, review, update records, and prepare files. You still make or confirm the consequential choices:

- correct facts and uncertain claims;
- decide whether to pursue or skip when it matters;
- answer legal/work-authorization questions when not already verified;
- make compensation commitments;
- approve the final resume/CV/letter;
- submit applications yourself;
- send networking messages yourself;
- make interview, negotiation, and offer decisions.

## Templates

During onboarding, the system asks what resume/CV/letter format you want to preserve. If you already have a good resume design, keep it. See `TEMPLATE_SETUP.md` only if you want the details.

If you do not register a template, setup, discovery, and triage can still continue. Before producing a final application artifact, the system must pause and ask you to approve a format; it must not silently declare a design approved.

## Need help?

If the system asks you to edit a schema, choose a reviewer, assign an evidence ID, or manually maintain workflow state during normal use, that is UX friction. Tell it to handle that internally and record the issue for the pilot.
