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

## Imports and skills (`@` and `!`)

`imports-and-skills/` shows two ways to compose context:

- `CLAUDE.md` imports a shared file with `@conventions.md` (inlined at load time).
- `.claude/skills/changes/SKILL.md` is a skill that inlines a shell command's output
  with `` !`git status --short` ``, run before the prompt is sent. Invoke it with `/changes`.

Two things to know:

- `@` imports work in CLAUDE.md, but `!` command execution does NOT, it only works in
  skills and commands.
- Skills are the forward-facing standard (the portable Agent Skills format). Custom
  commands have been merged into skills and still work, but prefer a skill for new work.
  `disable-model-invocation: true` keeps it user-only, like a command.

## Try it

Read the three `CLAUDE.md` files side by side first. Then:

```bash
cd 01-claude-md-examples/enterprise
claude
```

1. Ask: "What conventions should you follow in this project?" and watch Claude answer from the `CLAUDE.md` plus the auto-loaded rules.
2. Open `.claude/rules/security.md` and note the `paths:` frontmatter.

## Tip: docs in /tmp

For heavy frameworks, tell Claude in `CLAUDE.md` to read the docs locally instead of browsing the web. Have it `git clone --depth 1 <repo> /tmp/<lib>` once, then read the cloned docs/source. This is faster, matches the exact version you use, works offline, and the whole team gets the same behavior from one instruction.

Good candidates: FastAPI, SQLAlchemy, TanStack Router/Query. See the `## Documentation` block in `enterprise/CLAUDE.md` for the wording.

## What to notice

- Rules in `.claude/rules/` load automatically. You do not import them.
- A rule with `paths:` is conditional: it only applies when Claude works on matching files. A rule without `paths:` always applies.
- Importing a rule with `@.claude/rules/foo.md` would inline it unconditionally and defeat the `paths:` scoping. That is why this example does not import them.
