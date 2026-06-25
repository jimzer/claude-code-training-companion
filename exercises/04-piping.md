# Exercise 4: Piping & CLI Integration

**Time:** 10 minutes

## Goal
Use Claude Code's piping capabilities and CLI flags for quick, targeted tasks.

## Exercises

### 1. Code Review via Pipe
```bash
cat demo-app/app/services/task_service.py | claude "Find all bugs in this code"
```

### 2. Generate Documentation
```bash
cat demo-app/app/main.py | claude "Generate API documentation in markdown"
```

### 3. Quick Fixes with -p (Print mode)
```bash
# Non-interactive: get answer and exit
claude -p "In demo-app/, what files don't have type hints?"
```

### 4. Git Integration
```bash
cd demo-app
git diff | claude "Review this diff for issues"
git log --oneline -10 | claude "Summarize recent changes"
```

### 5. Error Investigation
```bash
make test 2>&1 | claude "Analyze these test results and suggest fixes"
```

### 6. Multi-file Analysis
```bash
find demo-app/app/services -name "*.py" -exec cat {} + | claude "Compare these services for consistency"
```

## What to notice
- Piping is great for quick, one-off tasks
- `-p` flag runs non-interactively (great for scripts/CI)
- You can pipe any command output to Claude for analysis
- Combine with standard Unix tools for powerful workflows

## Bonus: Create a Shell Alias
```bash
# Add to your .zshrc or .bashrc
alias review='git diff | claude "Review this diff"'
alias explain='claude -p "Explain this error:" < /dev/stdin'
```
