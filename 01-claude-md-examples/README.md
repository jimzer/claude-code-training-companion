# 01 - CLAUDE.md examples

**Goal:** see how project context scales from a 5-line file to a full enterprise setup, and how path-scoped rules work.

**Concept:** `CLAUDE.md` is how you give Claude persistent context (stack, commands, conventions). It loads automatically at session start, so Claude follows your rules without being told each time. Files higher in the tree and in `~/.claude/` compose with the project one.

## What's in here

Three versions of the same idea, increasing in depth:

- `minimal/CLAUDE.md` : the bare minimum, a few lines. A good starting point for any repo.
- `standard/CLAUDE.md` : a solid team setup (stack, commands, architecture, conventions, code style).
- `enterprise/CLAUDE.md` : a large project, plus `.claude/rules/`:
  - `rules/code-style.md` : loads everywhere (no `paths:` field).
  - `rules/security.md` : path-scoped via `paths:` so it only loads when Claude touches `services/` or `libs/` code.

## Try it

Read the three `CLAUDE.md` files side by side first. Then:

```bash
cd 01-claude-md-examples/enterprise
claude
```

1. Ask: "What conventions should you follow in this project?" and watch Claude answer from the `CLAUDE.md` plus the auto-loaded rules.
2. Open `.claude/rules/security.md` and note the `paths:` frontmatter.

## What to notice

- Rules in `.claude/rules/` load automatically. You do not import them.
- A rule with `paths:` is conditional: it only applies when Claude works on matching files. A rule without `paths:` always applies.
- Importing a rule with `@.claude/rules/foo.md` would inline it unconditionally and defeat the `paths:` scoping. That is why this example does not import them.
