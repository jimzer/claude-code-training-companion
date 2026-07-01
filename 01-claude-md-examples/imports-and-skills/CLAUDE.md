# Imports and skills demo

This project keeps its shared conventions in a separate file and imports it
instead of copy-pasting:

@conventions.md

Notes:
- `@path` import works in CLAUDE.md and memory files. It inlines the file at load
  time, resolved relative to THIS file. `~/` paths work; nesting up to 4 levels.
- Imports inside a code span like `@conventions.md` are ignored.
- `@path` import does NOT work in SKILL.md. Skills reference supporting files with
  normal markdown links, and inline command output with `` !`command` ``.
- `!` command execution does NOT work in CLAUDE.md either. To inline a command's
  output, use a skill (see `.claude/skills/changes/SKILL.md`), invoked with `/changes`.
- Skills are the forward-facing standard (the portable Agent Skills format).
  Custom commands have been merged into skills and still work, but new work should
  prefer a skill. `disable-model-invocation: true` makes it user-only, like a command.
