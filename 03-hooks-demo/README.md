# 03 - Hooks

**Goal:** use hooks to enforce deterministic actions on lifecycle events, things that should always happen, not things the model decides to do.

**Concept:** hooks are shell commands wired to events in `.claude/settings.json`. They fire automatically: before a tool runs (`PreToolUse`), after it runs (`PostToolUse`), when the session ends (`Stop`), and more. A `PreToolUse` hook that exits with code 2 blocks the tool call.

## What's in here

- `.claude/settings.json` : three hooks configured.
  - `PostToolUse` on edits: runs `ruff format` so code is always formatted.
  - `PreToolUse` on reads/edits: runs `protect-files.sh`, which blocks access to sensitive files.
  - `Stop`: runs `ruff check` before the session ends.
- `.claude/hooks/protect-files.sh` : the block script (exits 2 on a protected path).
- `app.py`, `ugly.py` : Python files to edit (watch them auto-format).
- `.env` : a protected file with fake secrets (the block target).

## Try it

```bash
cd 03-hooks-demo
claude
```

1. Ask Claude to clean up `ugly.py`. Notice it gets auto-formatted right after the edit.
2. Ask Claude to read `.env`. The PreToolUse hook blocks it.
3. End the session. `ruff check` runs automatically.

## What to notice

- Hooks are deterministic. They run regardless of what the model "decides".
- Exit code 2 from a `PreToolUse` hook blocks the action. That is the guardrail mechanism.
- `matcher` controls which tools a hook applies to.
- The `.env` values are fake. The point is the block, not the secrets.
