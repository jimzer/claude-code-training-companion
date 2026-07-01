# 13 - Scaling

**Goal:** run more work in parallel without drowning in coordination. Learn the ladder from one focused session to a supervised team of agents, plus the controls that keep many agents productive.

**Concept:** scaling is a ladder, not a switch. Each rung adds parallelism but also adds coordination cost. Climb only when the current rung saturates; more agents = more coordination.

```
single session            one Claude, one context, one task
   -> subagents           fan out isolated contexts (see station 04)
   -> worktrees           parallel branches, no file fights
   -> agent teams         peers sharing a task list, supervised by a lead
```

Around the ladder sit the controls that make scaled work converge instead of sprawl:

- **Goals** keep an agent driving toward a verifiable end state across many turns.
- **Dynamic workflows** let Claude write a script the runtime runs in the background (fan-out, loops, verification) so the context stays clean.
- **The agent view** is one screen to watch every background session.
- **Scheduled tasks** run work on a cadence, in the terminal or in the cloud.

## What's in here

- `a-worktrees/` (runnable): parallel git worktrees so two sessions never fight over files.
- `b-goals/` (runnable): `/goal` sets a verifiable target; an evaluator relaunches until it is met.
- `c-scheduled/` (partly runnable): `/loop` for session-bound cadence, `/schedule` for always-on cloud routines.
- `d-workflows/` (partly runnable): dynamic multi-agent workflows; `/deep-research` as the built-in example.
- `e-agent-view/` (guided, research preview): background sessions and the `claude agents` view.
- `f-agent-teams/` (guided, experimental): a lead session supervising peer sessions on a shared task list.

## How to read this station

Start at the bottom of the ladder and only climb when you feel the squeeze:

1. One session is slow because tasks are independent -> reach for **subagents** (station 04).
2. Parallel edits collide on the same files -> give each its own **worktree** (`a-worktrees`).
3. A long task drifts off target -> pin it with a **goal** (`b-goals`).
4. Work needs to fan out and self-verify in the background -> a **dynamic workflow** (`d-workflows`).
5. You are juggling many background runs -> watch them in the **agent view** (`e-agent-view`).
6. The work is genuinely a team effort -> stand up an **agent team** (`f-agent-teams`).

## What to notice

- Every rung up multiplies output but also multiplies the things that can go out of sync. The win is real only when the work is genuinely parallel.
- Isolation (worktrees, subagent contexts) is what makes parallelism safe. Without it, agents stomp on each other.
- Goals and verification are what make parallelism *converge*. Without them, more agents just means more drift.
