# Exercise 1: Explore the Codebase

**Time:** 10 minutes

## Goal
Use Claude Code to understand the demo-app without reading a single file yourself.

## Steps

1. **Open the demo-app folder** in Claude Code:
   ```
   cd demo-app
   claude
   ```

2. **Ask Claude to explore the project:**
   - "What is this project? Give me an overview."
   - "What endpoints are available?"
   - "How is the database set up?"

3. **Dig deeper:**
   - "Are there any bugs or issues you can spot?"
   - "What test coverage exists? What's missing?"
   - "Explain the service layer architecture."

4. **Try piping:**
   ```bash
   cat app/services/task_service.py | claude "Review this code for bugs"
   ```

## What to notice
- Claude reads files autonomously
- It understands project structure from CLAUDE.md
- It can spot the timezone bug in task_service.py
- It identifies missing test coverage

## Bonus
- Ask Claude to compare task_service.py vs user_service.py. What's different about their timestamp handling?
