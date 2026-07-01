# Built-in skills

Claude Code ships with a set of bundled skills you can call right away. These are distinct from the custom skills in this station (`api-conventions`, `code-review`, `test-writer`) which live in `../.claude/skills/`. The built-in ones come with the tool itself.

## What's bundled

- `/code-review` : reviews the current diff in a fresh subagent, so the review starts from a clean context.
- `/debug` : helps track down a failing test or runtime error.
- `/run` : launches the app so you can see it working.
- `/verify` : runs the app and confirms a change actually did what it should.
- `/security-review` : scans the code for security issues.
- `skill-creator` : interviews you about a workflow and generates a `SKILL.md` for it.

## What to notice

- They are prompt-based, not hardcoded. A built-in skill is just instructions, like any other skill.
- A local skill with the same name overrides the built-in one. Drop a `code-review/` into `.claude/skills/` and your version wins.
- You can turn them all off with `disableBundledSkills` in `settings.json`:

```json
{
  "disableBundledSkills": true
}
```

## Try it

Use the sibling `../demo-app` as the target:

```bash
cd ../demo-app
claude
```

1. Make a small change, then run `/code-review` to review the diff in a fresh subagent.
2. Run `/run` to launch the API server.
3. Run `/verify` to confirm your change works in the running app.
