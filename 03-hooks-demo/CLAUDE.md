# Hooks Demo

This folder demonstrates Claude Code hooks (`.claude/settings.json`).

## What's here
- `app.py`: a Python file to edit (triggers the format-on-edit hook)
- `.env`: a protected file (triggers the block hook)
- `.claude/settings.json`: hook configurations
- `.claude/hooks/protect-files.sh`: file protection script

## Hooks configured
1. **Format on edit**: runs `ruff format` after any Python file is edited
2. **Block .env**: prevents Claude from reading or editing `.env` files
3. **Test on stop**: runs `ruff check` before the session ends

## Try it
1. Open this folder in Claude Code.
2. Ask Claude to edit `app.py`, and notice it auto-formats afterward.
3. Ask Claude to read `.env`; it should be blocked.
4. End the session, and `ruff check` runs automatically.
