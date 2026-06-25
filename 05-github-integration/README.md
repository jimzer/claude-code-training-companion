# 05 — GitHub integration

**Goal:** drive Claude from GitHub itself: tag `@claude` on an issue or PR, get an automatic review on a PR, and kick off a task from the web.

**Concept:** "Claude + GitHub" is actually several distinct surfaces:

1. **GitHub Action, tag mode** : comment `@claude do X` on an issue or PR. Runs in this repo's GitHub Actions runner, implements the change, opens a branch / replies. Billed as **API credits**.
2. **GitHub Action, automation mode** : a workflow with a `prompt:` that fires on events (here, an auto-review on PRs touching this folder). Also **API credits**.
3. **Claude Code on the web** (`claude.ai/code`): kick off a task from the browser or phone on a connected repo, it works on an Anthropic VM and pushes a branch. Covered by your **Pro/Max subscription**, not credits.
4. **Managed Code Review service** : Anthropic-run, per-review billing, Enterprise-gated. Out of scope here, just know it exists.

## What's wired up in this repo

- `.github/workflows/claude.yml` : tag mode. Runs only when `@claude` is mentioned, and only for users with write access (default gating), so a public repo cannot be abused.
- `.github/workflows/claude-review.yml` : automatic PR review, **path-scoped to `05-github-integration/**`** so it does not fire on every PR.
- `playground/sample.py` : a deliberately flawed file. PRs that edit it trigger the auto-review.

## One-time setup (admin, required before any of this runs)

These two steps need a repo admin and cannot be committed. Do them once:

1. **Install the GitHub App and connect the repo.** In a terminal at the repo root:
   ```bash
   claude
   /install-github-app
   ```
   Pick this repository, authorize the app (Contents, Issues, Pull Requests: read & write).
2. **Add the API key secret.** Repo → Settings → Secrets and variables → Actions → New repository secret:
   - Name: `ANTHROPIC_API_KEY`
   - Value: a key from https://console.anthropic.com (use one with a small spend cap for the workshop).

The web flow (surface 3) needs no repo config: just connect this repo at https://claude.ai/code.

## Try it

**Tag mode (credits):**
1. Open an issue, e.g. "Add pagination to `GET /tasks` in demo-app".
2. Comment: `@claude implement this`.
3. Watch the Action run and open a PR.

**Auto review (credits):**
1. Create a branch, edit `playground/sample.py` (fix a bug or add one).
2. Open a PR. The `Claude auto review` workflow fires because the PR touches this folder.
3. Read Claude's inline comments. Open a PR elsewhere in the repo and note it stays quiet.

**Web (subscription):**
1. Go to https://claude.ai/code, connect this repo, create an environment.
2. Submit a task ("add a health-check endpoint to demo-app"). It works on a VM and pushes a branch you can open as a PR.

## What to notice

- The Action runs in **GitHub's runners on API credits**. The web flow runs on **Anthropic VMs on your subscription**. Same repo, different infra and billing.
- Triggering is gated on **write access**, not on who can open issues, so public is safe by default.
- Path scoping keeps the auto-review cheap and quiet: it only runs where you want it.
- Whatever is in this repo's `CLAUDE.md` and `.claude/` config governs Claude in all of these surfaces, not just locally.
