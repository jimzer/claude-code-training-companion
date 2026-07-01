# 11 - Plugins

**Goal:** package everything you wired up by hand in stations 01-10 (a command, a skill, a hook, an MCP server) into one installable plugin, and serve it from a local marketplace with no GitHub.

**Concept:** a plugin is a folder that bundles component types at its root (`commands/`, `agents/`, `skills/<name>/SKILL.md`, `hooks/hooks.json`, `.mcp.json`) plus a manifest at `.claude-plugin/plugin.json`. A marketplace is a manifest (`.claude-plugin/marketplace.json`) that lists plugins and where to find them. The source can be a local path, so the whole flow runs offline. Plugins are GA.

## What's in here

- `.claude-plugin/marketplace.json` : the marketplace `formation-marketplace`. Lists `my-first-plugin` with `"source": "./my-first-plugin"` (a local relative path, no GitHub needed).
- `my-first-plugin/.claude-plugin/plugin.json` : the plugin manifest (`name`, `description`, `version`, `author`).
- `my-first-plugin/commands/hello.md` : a `/hello` slash command. The markdown body is the prompt.
- `my-first-plugin/skills/greeter/SKILL.md` : a small `greeter` skill with `description` frontmatter.
- `my-first-plugin/hooks/hooks.json` : one `PostToolUse` hook that echoes a line after an Edit or Write. Same shape as settings hooks.
- `my-first-plugin/.mcp.json` : a minimal `filesystem` MCP server entry.

Notice the split: the manifests live under `.claude-plugin/`, the components live at the plugin root.

## Try it

```bash
cd 11-plugins
claude
```

1. Add the local marketplace: `/plugin marketplace add ./11-plugins`.
2. Install the plugin: `/plugin install my-first-plugin@formation-marketplace`.
3. Run the bundled command: `/hello`.
4. Trigger the bundled skill and hook: ask "greet Alice for me" (the `greeter` skill), then ask Claude to edit or create a file and watch the hook echo `[my-first-plugin] file changed`.
5. Open the manager with `/plugin`, disable `my-first-plugin`, then re-enable it.
6. Look at `enabledPlugins` in `.claude/settings.json` to see the toggle persisted, e.g. `{"enabledPlugins":{"my-first-plugin@formation-marketplace":true}}`.

## What to notice

- One plugin bundles everything you configured by hand in stations 01-10 (skills, commands, hooks, MCP) and ships it all in a single `/plugin install`.
- The manifest lives in `.claude-plugin/`; the components live at the plugin root. Keep that split straight and the layout is obvious.
- A local-path marketplace needs no GitHub. Point `source` at a folder and the same install flow works fully offline. Swap the source for an `owner/repo` shorthand or a git URL to share it.
