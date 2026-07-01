# 13e - Agent view (research preview)

> **Research preview.** Background sessions and the agent view are version-gated and may change or be unavailable in your build. This is a guided walk, not a runnable artifact. If the commands below are not present, your version does not have it yet.

**Goal:** kick off work that runs without you watching it, then supervise many such runs from one screen.

**Concept:** a **background session** is an agent that runs detached from your current chat, so you can keep working (or walk away) while it makes progress. The **agent view** is a single screen that shows every background session grouped by state, so you do not have to remember what you launched.

- `/bg "<task>"` launches a background agent from inside a session.
- `claude --bg "<task>"` launches one from the shell, without entering an interactive session first.
- `claude agents` opens the agent view: all background sessions grouped by state (to-do / in-progress / done).
- In the view: **Space** peeks at a session (a quick look without leaving the list), **Enter** attaches to it (jump in and take over).

## Try it (guided)

```bash
cd 13-scaling/e-agent-view
claude --bg "List the Python files in this folder and summarize what each does."
```

1. Launch one background task with the command above (or `/bg "..."` from inside a session).
2. Open the agent view:
   ```bash
   claude agents
   ```
3. Find your task under its state column (it moves to-do -> in-progress -> done as it runs).
4. Press **Space** to peek at its progress without leaving the list.
5. Press **Enter** to attach and take over if you want to steer it.

## What to notice

- Launching is **fire-and-forget**: `/bg` and `--bg` return immediately; the work continues without your attention.
- The **state grouping** (to-do / in-progress / done) is the supervision tool. With many background runs, this one screen replaces "which terminals did I leave things in?".
- **Peek vs attach** is the key distinction: Space is a glance, Enter is taking the wheel. Peek often, attach only when you need to intervene.
- This pairs with the rest of the station: background sessions are how scaled work runs unattended; the agent view is how you keep it all in view.
