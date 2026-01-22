# Git workflow notes

## Small PRs/MRs
- Prefer small, reviewable changes.
- Keep a clear commit history when it helps learning, but avoid over-optimizing for perfect history in MVPs.
- Each MR should have a clear purpose and be reviewable in 15-30 minutes.
- If a feature is large, split it into multiple smaller MRs that can be merged independently.

## Branching
- Feature branch from main.
- Open MR early, iterate.
- Branch naming: `feature/description`, `fix/issue-name`, `refactor/module-name`.
- Never commit directly to main/master in production repos.
- Use protected branches for main/master to enforce code review.

## Commit messages
- Use imperative mood: "Add feature X" not "Added feature X".
- First line should be concise (50-72 chars).
- Optional body explaining why, not what (the diff shows what).
- Reference issues: "Fix #123" or "Closes #456".

## Merge vs Rebase
- Merge: preserves full history, creates merge commits. Good for shared branches.
- Rebase: linear history, rewrites commits. Use for local branches before merging.
- Never rebase public/shared branches that others are using.

## Code review process
- At least one approval required before merge.
- Address all review comments before requesting re-review.
- Use "Request changes" for blocking issues, "Approve" or "Comment" for non-blocking feedback.
- Squash commits option: useful for cleaning up WIP commits before merge.
