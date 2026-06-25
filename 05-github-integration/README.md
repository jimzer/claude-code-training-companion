# 05 - GitHub integration

**Goal:** drive Claude from GitHub itself: tag `@claude` on an issue or PR, get an automatic review on a PR, and kick off a task from the web.

**Concept:** "Claude + GitHub" is actually several distinct surfaces:

1. **GitHub Action, tag mode**: comment `@claude do X` on an issue or PR. Runs in this repo's GitHub Actions runner, implements the change, opens a branch or replies.
2. **GitHub Action, automation mode**: a workflow with a `prompt:` that fires on events (here, an auto-review on PRs touching this folder).
3. **Claude Code on the web** (`claude.ai/code`): kick off a task from the browser or phone on a connected repo. It works on an Anthropic VM and pushes a branch. Covered by your Pro/Max subscription.
4. **Managed Code Review service**: Anthropic-run, per-review billing, Enterprise-gated. Out of scope here, just know it exists.

### How the Action is billed
The GitHub Action can authenticate two ways, and that choice decides who pays:

- `claude_code_oauth_token` (from `/install-github-app` when you authorize with a subscription): the Action bills against your **Pro/Max subscription**. This is how this repo is set up, so the Action needs **no API credits**.
- `anthropic_api_key` (a key from console.anthropic.com): the Action bills **API credits** instead. Use this if you prefer per-token billing or don't want to attach a subscription.

## What's wired up in this repo

- `.github/workflows/claude.yml`: tag mode. The action only responds to users with **write access** by default, so a public repo cannot be abused.
- `.github/workflows/claude-code-review.yml`: automatic PR review, **path-scoped to `05-github-integration/**`** so it does not fire on every PR.
- `playground/sample.py`: a deliberately flawed file. PRs that edit it trigger the auto-review.

Both workflows authenticate with the `CLAUDE_CODE_OAUTH_TOKEN` secret (subscription).

## One-time setup (admin, required before any of this runs)

Run `/install-github-app` **from inside this repo's folder** (not a parent directory, or it can't detect the repo):

```bash
cd claude-code-training-companion
claude
/install-github-app
```

Pick this repository and authorize the app. When you authorize with a subscription, the flow stores a `CLAUDE_CODE_OAUTH_TOKEN` secret on the repo automatically. That is all the auth the Action needs.

Notes from real setup:
- The "GitHub CLI not authenticated" warning is often spurious (the spawned `gh` can't reach the macOS Keychain). Press Enter to continue; if it truly blocks, run `GH_TOKEN=$(gh auth token) claude`.
- The installer writes its own default workflow files. This repo keeps a curated set instead (gated tag mode + path-scoped review), so do not let it overwrite them, or restore them afterward.

The web flow (surface 3) needs no repo config: just connect this repo at https://claude.ai/code.

## Try it

**Tag mode:**
1. Open an issue, e.g. "Add pagination to `GET /tasks` in demo-app".
2. Comment: `@claude implement this`.
3. Watch the Action run and open a PR.

**Auto review:**
1. Create a branch, edit `playground/sample.py` (fix a bug or add one).
2. Open a PR. The `Claude Code Review` workflow fires because the PR touches this folder.
3. Read Claude's inline comments. Open a PR elsewhere in the repo and note it stays quiet.

**Web:**
1. Go to https://claude.ai/code, connect this repo, create an environment.
2. Submit a task ("add a health-check endpoint to demo-app"). It works on a VM and pushes a branch you can open as a PR.

## What to notice

- The Action runs in **GitHub's runners**; the web flow runs on **Anthropic VMs**. Same repo, different infrastructure. With the OAuth-token setup both bill your subscription.
- Triggering is gated on **write access**, not on who can open issues, so public is safe by default.
- Path scoping keeps the auto-review cheap and quiet: it only runs where you want it.
- Whatever is in this repo's `CLAUDE.md` and `.claude/` config governs Claude in all of these surfaces, not just locally.
