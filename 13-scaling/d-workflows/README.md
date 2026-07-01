# 13d - Dynamic workflows

**Goal:** let Claude orchestrate parallel, multi-step work in the background and hand you back only the results, so your conversation context stays clean.

**Concept:** instead of running every step in the chat, Claude writes a **script** that the runtime executes in the background. That script can loop, fan out to parallel agents, branch on conditionals, and run adversarial verification (one agent checks another's output). Intermediate results land in **variables**, not in your context window, so a workflow that touches hundreds of sources still costs you only the final summary.

Two entry points:

- **`/deep-research`** is a built-in dynamic workflow: it fans out parallel agents to search, fetch, and cross-check sources, then synthesizes a cited report. This is the easy runnable example.
- **`ultracode`** is a keyword that opts into **authoring** your own multi-agent workflow. You describe the orchestration (the fan-out, the loops, the verification) and Claude builds it; you can then **save it as a command** to reuse. This is advanced; expect to iterate.

## Try it (the runnable part: `/deep-research`)

```bash
cd 13-scaling/d-workflows
claude
```

1. Run the built-in workflow on a real question:
   ```
   /deep-research What changed in Python packaging tooling between 2023 and 2025?
   ```
2. Watch it fan out: multiple agents search and fetch in parallel, results accumulate in the background, and you get back a synthesized, cited answer rather than a wall of intermediate search dumps.
3. Notice how little of the raw retrieval shows up in your chat. The heavy lifting happened in the background; only the conclusion landed in your context.

## Authoring your own (advanced, reference)

To build a custom workflow, opt in with the keyword in your prompt:

```
ultracode: build a workflow that, for each file in src/, runs a reviewer agent
and a separate verifier agent, then collects only the files that fail review.
```

Claude writes the orchestration script, runs it in the background, and returns the collected result. If it is useful, save it as a reusable command. Be honest with yourself: custom workflows are a power-user feature and usually need a few iterations to get the fan-out and verification right.

## What to notice

- The win is **context hygiene**: intermediate results live in variables in the background run, not in your conversation, so big fan-outs do not blow your context window.
- **Adversarial verification** (a second agent checking the first) is what makes fan-out trustworthy, not just fast. It is the same "trust the gate, not the author" idea from station 06, applied inside a workflow.
- `/deep-research` is the gentle on-ramp; `ultracode` is the build-your-own. Start with the former to feel the pattern before authoring your own.
