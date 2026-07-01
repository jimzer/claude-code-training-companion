# 13f - Agent teams (experimental)

> **EXPERIMENTAL.** Agent teams are behind a feature flag and may change between versions. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Treat anything here as subject to change.

**Goal:** turn a multi-part task into a coordinated team of peer sessions that split the work and keep going on their own.

**Concept:** this is the top rung of the scaling ladder. A **lead** session supervises several **peer** sessions that share one **task list**. The peers pull items off the list, do the work, and update shared state. Because the task list is shared, the team keeps making progress even if the lead is interrupted: a teammate just picks up the next item. Unlike subagents (station 04), which report back to a single parent and then vanish, teammates are persistent peers coordinating through shared state.

## Try it (guided, experimental)

```bash
cd 13-scaling/f-agent-teams
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude
```

1. Start Claude with the flag set (one-off above, or `export` it for the shell session).
2. Ask the lead to stand up a small team for a genuinely splittable task, for example:
   ```
   Spin up a small team to document this repo: one teammate writes a one-paragraph
   summary of each top-level folder, another assembles them into an index. Share a
   task list and keep going until every folder is covered.
   ```
3. Watch the lead create the shared task list and hand items to teammates working in parallel.
4. Interrupt the lead mid-run. Notice the teammates keep working off the shared list rather than stalling.

## What to notice

- The **shared task list** is the coordination substrate. It is what lets peers divide work and what lets the team survive the lead being interrupted.
- Teammates are **peers**, not throwaway subagents: they persist and coordinate, rather than reporting once and ending.
- This rung pays off only when the work is **genuinely splittable**. If the parts depend on each other, the coordination overhead can cost more than it saves. Climb here only when the lower rungs (subagents, worktrees) have saturated.
- Being experimental, the exact commands, env var, and behavior may shift between versions. If it behaves differently than described, check your version's notes.
