# Claude Code Cheatsheet

## Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Shift+Tab` | Cycle permission mode: default → acceptEdits → plan |
| `Escape` | Interrupt current generation |
| `Ctrl+C` | Clear input (press twice to exit) |
| `#` | Add a memory to CLAUDE.md |
| `/help` | Show help |
| `/clear` | Clear conversation |
| `/compact` | Summarize conversation to save context |

## Permission Modes

| Mode | Description |
|------|-------------|
| **default** | Asks before edits and commands (default) |
| **acceptEdits** | Auto-accepts file edits, still asks for commands |
| **plan** | Read-only: proposes a plan, makes no changes |

## CLI Flags

```bash
claude                     # Interactive mode
claude "question"          # Start with a prompt
claude -p "question"       # Print mode (non-interactive)
cat file | claude "prompt" # Pipe input
claude --continue          # Resume the most recent conversation
claude --resume            # Pick a past session to resume
claude --model opus        # Choose model
```

## CLAUDE.md Essentials

```markdown
# Project Name

## Stack
- Language, framework, database

## Commands
- `make test` -- how to run tests
- `make lint` -- how to lint

## Conventions
- Key rules Claude should follow
```

**Hierarchy:** `~/.claude/CLAUDE.md` → repo `/CLAUDE.md` → subdirectory `/src/CLAUDE.md`

## Custom Skills (`.claude/skills/`)

```markdown
---
description: What triggers this skill (drives auto-invocation)
paths: "**/*.py"              # Optional: limit auto-trigger to matching files
user-invocable: true          # Optional (default true): show in the / menu
---

# Skill instructions here
```

> The command name comes from the folder: `.claude/skills/code-review/` → `/code-review`.

## Custom Agents (`.claude/agents/`)

```markdown
---
name: agent-name              # Slug: lowercase + hyphens (required)
description: What this agent does and when to use it
model: sonnet                 # Optional: sonnet | opus | haiku | inherit
permissionMode: plan          # Optional: default | acceptEdits | plan | bypassPermissions
isolation: worktree           # Optional: run in an isolated git worktree
tools:                        # Optional: omit to inherit all tools
  - Read
  - Glob
  - Grep
---

# Agent instructions here
```

## Hooks (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [...],     // Before tool execution
    "PostToolUse": [...],    // After tool execution
    "Stop": [...]            // When session ends
  }
}
```

## Key Patterns

### Explore First
> "What is this project? Give me an overview."

### Plan Before Building
> Press Shift+Tab twice → "Add pagination to the list endpoint"

### Pipe for Quick Tasks
```bash
git diff | claude "Review this diff"
cat error.log | claude "What caused this error?"
```

### Fix Bugs Autonomously
> "There's a timezone bug in the task service. Find and fix it."

### Generate Tests
> "Write tests for the user service. Cover happy path and edge cases."
