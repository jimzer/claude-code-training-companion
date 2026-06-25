# Skills Demo

This folder demonstrates Claude Code custom skills.

## What's here
- `sample_api.py` -- A small FastAPI app to practice on
- `.claude/skills/` -- Three example skills:
  - `api-conventions/` -- Auto-triggers when editing API files
  - `code-review/` -- User-invocable via `/code-review`
  - `test-writer/` -- User-invocable via `/test-writer`, includes examples

## Try it
1. Open this folder in Claude Code
2. Edit `sample_api.py` -- the api-conventions skill should auto-trigger
3. Run `/code-review` to review the sample API
4. Run `/test-writer` to generate tests
