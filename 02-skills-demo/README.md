# 02 - Skills

**Goal:** build and use custom skills, both the kind Claude triggers on its own and the kind you call like a slash command.

**Concept:** a skill is a reusable instruction set in `.claude/skills/<name>/SKILL.md`. The folder name becomes the command (`/<name>`). The `description` lets Claude invoke it automatically when relevant, and `paths:` can scope auto-triggering to certain files.

## What's in here

- `sample_api.py` : a small FastAPI app to practice on.
- `.claude/skills/`:
  - `api-conventions/` : auto-triggers when editing API files (`paths:` scoped).
  - `code-review/` : user-invocable as `/code-review`.
  - `test-writer/` : user-invocable as `/test-writer`, with an `examples/` file that shapes its output.

## Try it

```bash
cd 02-skills-demo
claude
```

1. Run `/code-review` and let it review `sample_api.py`.
2. Run `/test-writer` to generate pytest tests for it.
3. Ask Claude to add an endpoint to `sample_api.py` and watch the `api-conventions` skill kick in on its own.

## What to notice

- The command name comes from the folder name, not a frontmatter field.
- `description` is what makes Claude auto-invoke a skill, so write it well.
- `paths:` limits auto-triggering (here, to API files).
- An `examples/` file gives the skill a concrete pattern to follow.
