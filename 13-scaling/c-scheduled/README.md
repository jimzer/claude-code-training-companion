# 13c - Scheduled tasks

**Goal:** run a prompt on a cadence instead of typing it again every few minutes, and understand the difference between a session-bound loop and an always-on routine.

**Concept:** there are three levels, by how persistent you need the cadence to be:

- **`/loop`** runs a prompt on a recurring cadence **tied to the current terminal session**. Close the terminal and the loop stops.
  - `/loop 5m "<prompt>"` runs every 5 minutes (`30s`, `5m`, `1h`, ...).
  - `/loop "<prompt>"` omits the interval and lets the model self-pace (it decides when to run again).
- **`/schedule`** creates **cloud Routines** that run on a cron schedule even when your machine is off. This is the always-on option. (Reference only here; it runs in the cloud, not in this folder.)
- **Desktop scheduled tasks** run locally on a schedule via the Claude desktop app, between the two.

Natural language works too: "remind me at 3pm to push" or "every 10 minutes, check the deploy" is understood and turned into the right mechanism.

## Try it (the runnable part: `/loop`)

```bash
cd 13-scaling/c-scheduled
claude
```

1. Start a safe, read-only loop that just summarizes repo status on a cadence:
   ```
   /loop 5m "Run `git status --short` and give me a one-line summary of what changed. Do not edit anything."
   ```
2. Let it fire a couple of times. Each run is a fresh turn on the same schedule.
3. Stop it: interrupt the loop (Esc / the stop control) or close the terminal session. The cadence is session-bound, so ending the session ends the loop.

## Reference only: always-on with `/schedule`

For a cadence that survives your terminal closing, use a cloud Routine:

```
/schedule
```

Then describe the job and cron cadence (for example, "every weekday at 9am, summarize new issues"). Routines run in the cloud on their schedule with no terminal open. Manage them with the same command. We do not run one here because it lives in the cloud, not in this folder.

## What to notice

- `/loop` is **ephemeral and local**: great for polling something while you watch ("keep checking the build"), gone when the session ends.
- `/schedule` is **durable and remote**: great for unattended recurring jobs.
- Omitting the interval (`/loop "<prompt>"`) hands pacing to the model, useful when "how often" depends on what it finds rather than a fixed clock.
- Keep looped prompts read-only or tightly scoped. A loop that edits files repeatedly, unattended, is a fast way to make a mess.
