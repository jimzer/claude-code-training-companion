# 14 - Permission Modes

**Goal:** feel the difference between Claude Code's permission modes by editing one file in each mode and watching when Claude asks versus when it acts on its own.

**Concept:** the permission mode decides how much Claude can do before it stops to ask you. The same edit request behaves differently depending on the mode you are in. You switch modes live with Shift+Tab, set one at startup with `--permission-mode`, or pin a starting mode in `settings.json`.

## The six modes

| Identifier | What it does | In the Shift+Tab cycle? | How to set |
|------------|--------------|-------------------------|------------|
| `default` (Normal) | Prompts for permission on the first use of each tool. | yes | `--permission-mode default` / `permissions.defaultMode` |
| `acceptEdits` (Auto-accept edits) | Auto-applies file edits and common filesystem commands; still prompts for other things (Bash, network). | yes | `--permission-mode acceptEdits` / `permissions.defaultMode` |
| `plan` (Plan) | Read-only. Explores and proposes a plan, changes nothing. | yes | `--permission-mode plan` / `permissions.defaultMode` |
| `auto` (Auto) | Auto-approves tool calls with background safety checks that verify the action matches your request (research preview). | yes | `--permission-mode auto` / `permissions.defaultMode` |
| `bypassPermissions` (Bypass) | No prompts at all. For sandboxed or throwaway environments only. | no | `--dangerously-skip-permissions` or `--permission-mode bypassPermissions` |
| `dontAsk` | Auto-denies anything not pre-approved in `/permissions`. | no | `--permission-mode dontAsk` / `permissions.defaultMode` |

The interactive Shift+Tab cycle rotates through: Normal -> Auto-accept -> Plan -> Auto. Bypass is opt-in (a launch flag), and `dontAsk` is config-only.

## What's in here

- `sample.py` : a small, harmless file (two functions with a tiny style issue) to edit repeatedly under each mode.
- `.claude/settings.json` : sets `permissions.defaultMode` to `default`, so this station opens in Normal.
- `protected-files/` : a separate demo of `permissions.deny` `Read(...)` rules that keep Claude from ever reading `.env` and `secrets/`. See its own README.

## Try it

```bash
cd 14-permission-modes
claude
```

1. You open in Normal (`default`). Ask: *"fix the style issue in `sample.py`"*. Watch Claude ASK before editing the file.
2. Press Shift+Tab once to reach Auto-accept (`acceptEdits`). Ask for another edit (e.g. *"add a docstring to `add`"*). It applies WITHOUT asking. Then ask it to run a Bash command (e.g. *"run `python sample.py`"*) and notice it still ASKS for that.
3. Press Shift+Tab again to reach Plan (`plan`). Ask it to change `sample.py`. It only PROPOSES a plan and edits nothing.
4. Press Shift+Tab again to reach Auto (`auto`). Ask for an edit. It is auto-approved, with a background safety check verifying the action matches your request.
5. Bypass is not in the cycle. You would launch it with `claude --dangerously-skip-permissions` (or `--permission-mode bypassPermissions`). It never prompts, so only use it in a disposable sandbox where nothing it touches matters. You do not need to run it here.

## What to notice

- Which modes touch files: Normal edits after you approve, Auto-accept and Auto edit on their own, and Plan never edits. Bypass edits anything; `dontAsk` only does what is already allowlisted.
- The live cycle is Shift+Tab, rotating Normal -> Auto-accept -> Plan -> Auto.
- `permissions.defaultMode` in `.claude/settings.json` sets the mode Claude starts in. This station starts in Normal.
- Bypass (`--dangerously-skip-permissions`) skips every prompt and is for disposable sandboxes only, never your real working repo.
- `dontAsk` auto-denies anything not pre-approved, so it locks Claude to whatever you have allowed in `/permissions`.
