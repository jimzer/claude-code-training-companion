# 09 - Advanced (scaffold)

> **Status: scaffold.** This station is intentionally not built out yet. In the
> course it is a slide segment ("here's what's possible next"), and live we just
> run the one headless teaser below. The folder exists so the topics have a home
> and we can grow it into a full hands-on station later.

## Topics (slides for now)

- **Headless mode:** `claude -p` runs Claude Code as a non-interactive, pipeable CLI. Scriptable, CI-able, composable with other tools. The teaser below is runnable today.
- **Dynamic workflows:** code-orchestrated multi-agent runs (fan-out, pipelines, loops) instead of one chat thread.
- **Remote control:** driving Claude from elsewhere (web, phone, triggers) against a connected repo.
- **Subagents at scale:** parallel specialized agents, building on station `04`.

## Headless teaser (runnable)

`headless.sh` is the one-liner we run live. It shows Claude Code working as a plain Unix filter: pipe in, get text out, exit.

```bash
git diff --staged | claude -p "Write a one-line conventional-commit message for this diff. Output only the message."
```

Try it: stage a change, then run `bash headless.sh`. That `claude -p "..."` is the seed of everything else on this list. Once Claude is a CLI, you can put it in scripts, hooks, and pipelines.

## TODO (when we build this out)

- [ ] A real dynamic-workflow example.
- [ ] A headless batch script (e.g. triage N files in a loop).
- [ ] Remote/web walkthrough tied to station `05`.
