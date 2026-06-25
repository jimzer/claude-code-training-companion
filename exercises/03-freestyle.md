# Exercise 3: Freestyle Challenge

**Time:** 20 minutes

## Goal
Pick a challenge and solve it using Claude Code. Use any features you've learned!

## Choose your challenge:

### Challenge A: Fix the Timezone Bug
The task service uses naive datetimes. Fix it to use UTC everywhere.
- Hint: Compare `task_service.py` with `user_service.py`
- Run tests after to make sure nothing breaks

### Challenge B: Add User Authentication
Design and implement basic API key authentication.
- Use plan mode to design the approach first
- Add middleware to protect endpoints
- Allow unauthenticated access to `GET /` and `/docs`

### Challenge C: Write Missing Tests
The test coverage is incomplete. Fix it!
- Add tests for user endpoints
- Add tests for task update, delete, and complete
- Aim for comprehensive edge case coverage

### Challenge D: Your Own Idea
Have something you want to build? Go for it!
- Use plan mode for anything non-trivial
- Leverage Claude's ability to explore, plan, and implement

## Tips
- Start with plan mode for anything beyond a simple fix
- Use `/code-review` in skills-demo to review your changes
- Don't forget to run tests: `make test`
- Ask Claude to explain its changes if something isn't clear
