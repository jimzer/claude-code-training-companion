# 10 - MCP (Model Context Protocol)

**Goal:** connect Claude Code to an external tool server over MCP, so the model can call tools you bring instead of just the built-ins.

**Concept:** MCP is an open protocol for exposing tools, resources, and prompts to an AI client. Claude Code is the client; an MCP server is a separate process (local stdio command or remote HTTP endpoint) that advertises capabilities. A server exposes tools (Claude calls them), resources (you @-mention them), and prompts (they show up as `/servername:promptname (MCP)` slash commands). This station runs the official filesystem server fully offline, no account needed.

## What's in here

- `.mcp.json` : project-scope config defining one stdio server named `filesystem`, pointed at `./docs`.
- `docs/notes.md` : sample project notes so the server has something real to read.
- `CLAUDE.md` : short orientation for the demo.

## Two ways to configure a server

Both produce the same result. Pick whichever fits the situation.

**A. The CLI.** Run this once and Claude Code writes the config for you:

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ./docs
```

For an HTTP server you pass a transport and URL instead:

```bash
claude mcp add --transport http <name> <url>
```

Control where it gets written with `--scope local|project|user` (default is `local`). With `--scope project` the server lands in a committed `.mcp.json` at the folder root, shared with the team.

**B. The committed `.mcp.json` file.** That is exactly what this station ships, already at project scope:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    }
  }
}
```

`claude mcp add filesystem ... --scope project` writes this same JSON. The file is the team source of truth; the CLI is just a convenience that edits it.

## Try it

```bash
cd 10-mcp
claude
```

1. Open Claude Code here. The first time, it asks you to trust the project's MCP servers. Approve it.
2. Run `/mcp` to list the `filesystem` server, see its status, and view the tools it exposes (read, list, search files). `claude mcp list` and `claude mcp get filesystem` show the same from the CLI.
3. Ask Claude: "Use the filesystem MCP tools to read the project notes and tell me who is on-call." Watch it call the server's tools.
4. Open `.mcp.json`. It is just JSON. Running `claude mcp add ... --scope project` would have written the same file.
5. Run `/context`. Note the line `MCP tools - /mcp (loaded on-demand)`, confirming the tools do not eat context until they are used.

## What to notice

- **Three scopes.** `local` (just you, this folder, the default), `project` (committed `.mcp.json`, shared with the team), and `user` (you, across all your projects). This station uses project scope so the server travels with the repo.
- **`.mcp.json` is the team file.** Commit it and everyone who opens the folder gets the same server. The CLI's `--scope project` writes to it.
- **On-demand loading saves context.** MCP tool definitions load lazily, only when needed, so adding servers does not bloat every prompt. `/context` shows them as `loaded on-demand`.
- **Trust caveat.** A server is third-party code that runs with your permissions and can read whatever you grant it. Only add servers you trust, and that is why Claude Code prompts before running a project's MCP servers.

### Reference only: an HTTP server

HTTP servers work the same way but usually need an account and OAuth, so this one is reference-only (not part of the offline demo):

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

After adding it, run `/mcp` and pick the server to complete the OAuth sign-in.
