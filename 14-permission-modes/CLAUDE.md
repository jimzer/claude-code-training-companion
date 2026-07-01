# Permission Modes

This folder is a hands-on station for Claude Code's six permission modes.

## What's here
- `sample.py`: a harmless file to edit repeatedly under different modes
- `.claude/settings.json`: pins the starting mode to `default` (Normal)

## The modes
- `default` (Normal): asks on first use of each tool. In the Shift+Tab cycle.
- `acceptEdits` (Auto-accept edits): auto-applies edits and common fs commands; still asks for Bash and network. In the cycle.
- `plan` (Plan): read-only, proposes a plan, changes nothing. In the cycle.
- `auto` (Auto): auto-approves with background safety checks (research preview). In the cycle.
- `bypassPermissions` (Bypass): no prompts; sandbox only; set via `--dangerously-skip-permissions`. Not in the cycle.
- `dontAsk`: auto-denies anything not pre-approved in `/permissions`. Config-only.

Shift+Tab cycles Normal -> Auto-accept -> Plan -> Auto. Set a mode with `--permission-mode <mode>` or `permissions.defaultMode` in settings.json.
