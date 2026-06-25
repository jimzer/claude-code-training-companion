---
description: Performs a structured code review of the current file or changes
user-invocable: true
---

# Code Review Skill

When invoked with `/code-review`, perform a structured review:

## Review Checklist
1. **Correctness**: Are there logic errors or edge cases?
2. **Error handling**: Are errors handled gracefully?
3. **Security**: Any injection risks, hardcoded secrets, or unsafe patterns?
4. **Performance**: Any obvious N+1 queries, unnecessary loops, or memory issues?
5. **Style**: Does it follow Python/project conventions?

## Output Format
For each issue found:
- 🔴 **Critical**: Must fix before merge
- 🟡 **Warning**: Should fix, not blocking
- 🟢 **Suggestion**: Nice to have

End with a summary: "X critical, Y warnings, Z suggestions"
