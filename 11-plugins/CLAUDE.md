# Plugins Demo

This folder demonstrates packaging Claude Code components into one installable plugin, served from a local marketplace.

## What's here
- `.claude-plugin/marketplace.json`: the `formation-marketplace`, listing `my-first-plugin` from a local path
- `my-first-plugin/.claude-plugin/plugin.json`: the plugin manifest
- `my-first-plugin/commands/hello.md`: a `/hello` slash command
- `my-first-plugin/skills/greeter/SKILL.md`: a `greeter` skill
- `my-first-plugin/hooks/hooks.json`: a `PostToolUse` demo hook
- `my-first-plugin/.mcp.json`: a `filesystem` MCP server

## Try it
1. Open this folder in Claude Code
2. Run `/plugin marketplace add ./11-plugins`
3. Run `/plugin install my-first-plugin@formation-marketplace`
4. Use `/hello`, the `greeter` skill, and the edit hook
5. Run `/plugin` to disable then re-enable it, and check `enabledPlugins` in `.claude/settings.json`
