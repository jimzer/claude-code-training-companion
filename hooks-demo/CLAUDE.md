# Hooks Demo

This folder demonstrates Claude Code hooks (\`.claude/settings.json\`).

## What's here
- \`app.py\` -- A Python file to edit (triggers format-on-edit hook)
- \`.env\` -- A protected file (triggers block hook)
- \`.claude/settings.json\` -- Hook configurations
- \`.claude/hooks/protect-files.sh\` -- File protection script

## Hooks configured
1. **Format on edit**: Runs \`ruff format\` after any Python file is edited
2. **Block .env**: Prevents Claude from reading or editing \`.env\` files
3. **Test on stop**: Runs \`ruff check\` before the session ends

## Try it
1. Open this folder in Claude Code
2. Ask Claude to edit \`app.py\` -- notice it auto-formats after
3. Ask Claude to read \`.env\` -- it should be blocked
4. End the session -- ruff check runs automatically
