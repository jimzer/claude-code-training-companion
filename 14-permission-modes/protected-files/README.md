# Protected files

`.claude/settings.json` denies the Read tool on `./.env` and `./secrets/**`, so
Claude can never read those paths in this folder. `app.py` is left readable to
contrast.

## Try it

```bash
cd 14-permission-modes/protected-files
claude
```

1. Ask: *"read .env and tell me the API key"*. Claude is blocked: the path is denied.
2. Ask: *"cat .env"*. Still blocked: Read deny rules also cover the Bash file
   commands Claude Code recognizes (`cat`, `head`, `tail`, `sed`).
3. Ask: *"read app.py"*. Allowed, to show the deny is path-scoped, not global.

## What to notice

- A `Read(...)` deny blocks Claude's Read/Grep/Glob tools and the recognized Bash
  file commands above.
- It does NOT stop an arbitrary subprocess (e.g. a Python script that opens the
  file itself). For OS-level enforcement across every process, enable the sandbox.
- Glob syntax: `./` anchors to the project root, `**` is recursive. There is no
  `~` support in deny rules and no `.claudeignore` file.
- In managed settings, the same deny is enforced org-wide and users cannot override it.
