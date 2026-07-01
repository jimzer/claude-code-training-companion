# 12 - Context Management

**Goal:** feel the context window as your #1 constraint and learn the three levers that keep it lean: `/clear`, `/compact`, and `/context`, plus delegating heavy reads to a subagent.

**Concept:** every token in the window costs money and attention. `/context` shows where the tokens go (System prompt, System tools, MCP tools, Memory files, Skills, Messages, Free space). Messages, your actual conversation, is almost always the biggest slice and the one you control. `/clear` resets it between unrelated tasks, `/compact` summarizes it so you can keep going, and a subagent quarantines expensive exploration so only a short summary lands in the parent window.

## What's in here

- `bloat.md` : an ordered list of prompts to paste that deliberately balloon the Messages slice by reading the sibling `../demo-app`.
- `.claude/agents/explorer.md` : a read-only subagent that explores broadly and returns only a tight summary, to demonstrate context-saving delegation.

This station works best run from the repo root checkout so the sibling `../demo-app` (a FastAPI app) is reachable.

## Try it

```bash
cd 12-context
claude
```

1. Run `/context` on a fresh session and note the baseline. Messages is tiny, Free space is large.
2. Open `bloat.md` and paste its prompts one by one to fill the window with file contents.
3. Run `/context` again and watch Messages dominate while Free space shrinks.
4. Run `/compact`, then `/context` again. The conversation is summarized and Messages drops.
5. Run `/clear`, then `/context`. You are back to the baseline from step 1.
6. Redo the heavy exploration the lean way: ask "use the explorer subagent to map ../demo-app" and then run `/context`. The parent window stays lean because only the summary returns.

## What to notice

- Messages is usually the biggest slice and the one you directly control.
- `/clear` between unrelated tasks keeps each task starting from a clean window.
- `/compact` when you want to keep going on the same task: it trades detail for room.
- Subagents quarantine expensive reads. The subagent reads a lot, the parent gets a summary.
- A bloated window degrades quality: the model spreads attention thin and starts to drift.
