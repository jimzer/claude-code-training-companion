# MCP Demo

This folder demonstrates connecting Claude Code to an MCP (Model Context Protocol) server.

## What's here
- `.mcp.json`: a project-scope config defining one stdio server named `filesystem`
- `docs/notes.md`: sample project notes for the server to read

## Try it
1. Open this folder in Claude Code
2. Run `/mcp` to list the `filesystem` server and its tools
3. Ask Claude to read the notes through the MCP server's tools
4. Run `/context` to confirm MCP tools load on demand
