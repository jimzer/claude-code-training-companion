---
name: changes
description: Summarize the working-tree changes for a commit or PR
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

## Current changes

!`git status --short`

!`git diff --stat`

Summarize what changed above in one short paragraph, grouped by area. If there are
no changes, say so.
