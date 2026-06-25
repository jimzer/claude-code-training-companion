# 04 - Subagents

**Goal:** delegate work to specialized subagents, including running several in parallel and isolating one in its own git worktree.

**Concept:** a subagent is defined in `.claude/agents/<name>.md` with its own description, tool allowlist, permission mode, and optional model. Each runs with its own isolated context, so you can fan out work and keep concerns separate.

## What's in here

- `sample_app.py` : a small app with intentional issues for the agents to find.
- `tests/` : a test suite for the test-runner to execute.
- `.claude/agents/`:
  - `security-reviewer.md` : read-only security review (`permissionMode: plan`).
  - `test-runner.md` : runs the test suite and reports (`Bash` access).
  - `refactor-advisor.md` : suggests refactors, runs in an isolated worktree.

## Try it

```bash
cd 04-agents-demo
claude
```

1. Ask: "Run the security-reviewer, test-runner, and refactor-advisor agents in parallel on this folder."
2. Watch each report back independently.
3. Open the three agent files and compare their `tools`, `permissionMode`, and `isolation`.

## What to notice

- Each agent has its own tools and permission mode. The security reviewer cannot edit because it is read-only (plan mode).
- `isolation: worktree` runs an agent on an isolated copy of the repo, so parallel agents do not collide.
- Subagents start with their own context. Anything they need (file paths, error messages) must be in the delegation prompt.
