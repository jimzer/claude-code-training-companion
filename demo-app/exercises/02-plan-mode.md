# Exercise 2: Plan Mode

**Time:** 15 minutes

## Goal
Use Plan Mode (Shift+Tab x2) to design a feature before implementing it.

## The Task
Add **pagination** to the task list endpoint (`GET /tasks`).

## Steps

1. **Enter Plan Mode** by pressing `Shift+Tab` twice

2. **Give the instruction:**
   > "Add pagination to the GET /tasks endpoint. Support `page` and `per_page` query parameters with sensible defaults."

3. **Review the plan** Claude proposes:
   - Does it touch the right files?
   - Does it update schemas?
   - Does it include tests?

4. **Approve and let it implement**

5. **Verify:**
   ```bash
   make test
   ```
   ```bash
   curl "http://localhost:8000/tasks?page=1&per_page=5"
   ```

## What to notice
- Plan mode shows you the full approach before any code is written
- You can iterate on the plan before accepting
- The implementation follows the approved plan
- Claude updates tests to cover the new functionality

## Bonus
- Try rejecting the plan and asking for a different approach (e.g., cursor-based pagination instead of offset-based)
- Use plan mode to design adding authentication to the API
