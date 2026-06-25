# Allowed skills & extensions registry

The single source of truth for what may be installed into Claude Code at [Company].
Nothing outside this list runs on company machines or repos. To add an entry, open
a PR; a reviewer reads the actual source before approving.

> Skills, subagents, MCP servers, and slash commands are **executable**. Treat this
> list like an approved-dependency list, because that is what it is.

## Approved skills

| Skill | Source (repo / commit) | What it does | Reviewed by | Date |
|-------|------------------------|--------------|-------------|------|
| `safety-net` | `internal/claude-skills@<sha>` | runs format+lint+types+tests gate | [name] | [date] |
| `test-writer` | `internal/claude-skills@<sha>` | generates pytest suites | [name] | [date] |
| _[add]_ | | | | |

## Approved MCP servers

| Server | Source | Scope / permissions | Reviewed by | Date |
|--------|--------|---------------------|-------------|------|
| _[add]_ | | | | |

## Rejected / blocked

Keep rejections visible so nobody re-proposes them blindly.

| Item | Source | Why rejected | Date |
|------|--------|--------------|------|
| _[example]_ | random gist | unreviewable, ran `curl \| sh` | [date] |

## Review checklist (before approving anything)

- [ ] Read the full source: no obfuscation, no `curl ... | sh`, no surprise network calls.
- [ ] Confirm the permissions/tools it requests are the minimum it needs.
- [ ] Confirm it sends nothing sensitive off-box.
- [ ] Pin to a specific commit/version, not a moving branch.
- [ ] Record who reviewed it and when (rows above).
