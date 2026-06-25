# 07 - Status line & staying aware of cost

**Goal:** always know, at a glance, which model you're on, how hard it's thinking, how full the context is, and how much of your plan you've burned. Awareness is the cheapest cost control there is.

## What's here

- `statusline.sh` + `statusline-parse.py`: a fast (<50 ms), dependency-free status line. It reads the JSON payload Claude Code pipes in on stdin, with no external CLI calls.
- `.claude/settings.json`: wires the script in via the `statusLine` key.

It renders two lines:

```
➜ demo
🤖 Sonnet 4.6 · 🧪 high · 🧠 42% (43k) · ⏱ 5h 18% (in 2h30m) · 📅 week 63% (in 2d7h)
```

| Field | Meaning |
|-------|---------|
| 🤖 model | which model is active (`⚡` if fast mode) |
| 🧪 effort | current thinking effort (low / medium / high / xhigh) |
| 🧠 ctx% | how full the context window is (color-coded, compact before it's red) |
| ⏱ 5h | rolling 5-hour usage limit and when it resets |
| 📅 week | weekly usage limit and when it resets |

Percentages go green, then yellow, then red, so the cost signal is pre-attentive: you feel it before you read it.

## Install it (for real, not just the demo)

Copy the two files to `~/.claude/`, make `statusline.sh` executable, and add to `~/.claude/settings.json`:

```json
{
  "statusLine": { "type": "command", "command": "sh ~/.claude/statusline.sh" }
}
```

Use an absolute path globally. The `.claude/settings.json` in this folder uses a repo-relative path so it works when you open the station directly.

## The concepts behind the numbers

### Match the model to the task
Different models cost very differently. The cheapest correct model wins.

| Model | Use it for | Rough cost |
|-------|-----------|-----------|
| **Haiku** | cheap, high-volume, mechanical edits; quick lookups | $ |
| **Sonnet** | the daily driver for most coding, refactors, reviews | $$ |
| **Opus** | hard reasoning, gnarly debugging, architecture, big refactors | $$$$ |

Heuristic: **default to Sonnet, drop to Haiku for bulk/trivial work, reach for Opus when a problem is genuinely hard.** Switch with `/model`.

### Match the thinking effort to the difficulty
"Thinking" is the model reasoning before it answers. More thinking finds better answers but costs more tokens and latency. You control the budget (low / medium / high / xhigh). Routine edits don't need deep thinking; a subtle concurrency bug does. The status line's 🧪 field always shows the current setting so you never over- or under-spend silently.

### Understand your subscription limits
On Pro/Max, usage is governed by **two rolling windows**: a **5-hour** session limit and a **weekly** limit. The status line surfaces both (⏱ and 📅) with reset countdowns, so you can pace heavy work instead of hitting a wall mid-task. API usage is billed per-token instead, which is the credits model used by the GitHub Action in station `05`.

## Try it

1. Copy the two files into `~/.claude/`, wire up `settings.json`, restart Claude Code.
2. Run `/model` to switch models and watch 🤖 change.
3. Work for a while and watch 🧠 climb; run `/compact` and watch it drop.
4. Note how ⏱ and 📅 let you see a limit coming before it stops you.
