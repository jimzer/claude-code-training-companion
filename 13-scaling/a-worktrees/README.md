# 13a - Worktrees

**Goal:** run two Claude sessions on the same repo at the same time without them fighting over files.

**Concept:** a git worktree is a second working directory backed by the same repo, checked out to its own branch. Each worktree has its own files on disk, so two sessions can edit, run, and commit in parallel and never collide. Merge the branches when each is done. This is the rung above subagents (station 04): use it when parallel work needs to touch the same files.

## What's in here

- `sample.py` : a tiny module with two functions, something concrete to change in each worktree.

## Four ways to get a worktree

1. **Manual git, then open Claude in it.** Most explicit; works anywhere.
   ```bash
   git worktree add ../feat-a feat-a   # new dir ../feat-a on branch feat-a
   cd ../feat-a && claude
   ```
2. **The integrated shortcut.** Claude creates and enters the worktree for you.
   ```bash
   claude --worktree feat-a
   ```
3. **In-session.** Ask a running Claude to "work in a worktree" and it sets one up and moves there, so the change is isolated from your main checkout.
4. **Subagents with isolation.** A subagent whose definition sets `isolation: worktree` runs on an isolated copy of the repo, so parallel subagents do not collide. See `04-agents-demo/.claude/agents/refactor-advisor.md`.

## Try it

```bash
cd 13-scaling/a-worktrees

# Worktree 1: rename the greeting
git worktree add ../wt-greet wt-greet
cd ../wt-greet/13-scaling/a-worktrees
claude
```

1. In session 1 ask: "In `sample.py`, make `greet` return `Hi, {name}.` instead." Let it save.
2. Open a second terminal and create a second worktree for an independent change:
   ```bash
   git worktree add ../wt-add wt-add
   cd ../wt-add/13-scaling/a-worktrees
   claude
   ```
3. In session 2 ask: "In `sample.py`, add a `multiply(a, b)` function." Let it save.
4. Both sessions edited the same file on different branches with zero conflict. Merge them back:
   ```bash
   cd <your main checkout>
   git merge wt-greet
   git merge wt-add
   ```
5. Clean up the worktrees when done:
   ```bash
   git worktree remove ../wt-greet
   git worktree remove ../wt-add
   ```

## What to notice

- Each worktree is a real directory with its own branch. The sessions never see each other's uncommitted files, so there is nothing to conflict over while they work.
- Conflicts, if any, surface only at **merge** time, exactly where git is built to handle them, not mid-edit.
- `claude --worktree <branch>` collapses "create worktree + cd + open Claude" into one step. Use manual `git worktree add` when you want full control over the path and branch.
- Worktrees and subagent `isolation: worktree` are the same mechanism: an isolated checkout. One is driven by you, the other by an agent definition.
