# GitHub Setup

This project is designed so a beginner can use GitHub mainly as a private, versioned folder. Command-line Git is optional.

## Preferred path — no terminal required

1. Create a GitHub account if you do not already have one.
2. Open the [Career Search OS starter](https://github.com/rh5rep/career-os-starter).
3. Choose **Use this template → Create a new repository**.
4. Select your own GitHub account as the owner.
5. Name the repository something like `my-career-search-os`.
6. Set visibility to **Private** and create the repository.
7. In ChatGPT/Codex, connect GitHub using the available GitHub connection/integration and grant access to this new private repository.
8. Open `user_actions/START.md` in your connected workspace and send its single onboarding prompt.

Do not put personal career data back into the public starter. Your private copy is the workspace that will hold your profile, applications, and process history.

## Fallback when template mode is unavailable

Download the starter repository as a ZIP, unzip it, create a new **private** repository in your GitHub account, and use **Add file → Upload files** to upload the extracted contents. The files should live directly at repository root—not inside an extra `career-os-starter/` folder. Commit the upload through the GitHub web interface, connect that private repository to ChatGPT/Codex, and start with `user_actions/START.md`.

For normal use, the system should maintain structured files and routine updates. You should not need to make branches, resolve merge conflicts, or edit YAML by hand.

## Privacy

Keep the repository private because it may contain contact details, work history, application records, compensation constraints, and other personal career information. Grant access only to tools and people you intentionally use for the search.

## What GitHub is doing for you

GitHub gives you a recoverable history. If the system changes a profile, opportunity, or application record, earlier versions remain recoverable instead of being silently overwritten forever.

## Optional advanced workflow

If you already know Git, you can clone the repo locally, use feature branches for larger system changes, commit frequently, and merge reviewed changes into your main branch. This is optional. The friend pilot does not require command-line Git for daily job-search work.
