# Exercise 5: Spec-first Prompting

**Time:** 20 minutes

## Goal
For a larger feature, get Claude to interview you, write a `SPEC.md`, then implement from that spec in a fresh session.

## The Task
Add **pagination** to the `demo-app` list endpoints (or pick an auth feature instead).

## Steps

1. **Start in the demo app:**
   ```bash
   cd demo-app
   claude
   ```

2. **Ask Claude to interview you, not to code yet:**
   > "I want to add pagination to the list endpoints. Don't write any code. Interview me with clarifying questions first, one batch at a time."

3. **Answer the questions** (offset vs cursor, default page size, response shape, backward compatibility).

4. **Have it write the spec:**
   > "Write everything we agreed on to `SPEC.md`: scope, API changes, schema changes, tests, and edge cases."

5. **Start a fresh session** so the context is clean:
   ```bash
   claude
   ```

6. **Implement from the spec:**
   > "Read `SPEC.md` and implement it. Follow it exactly."

7. **Verify:**
   ```bash
   make test
   ```

## What you learn
- An interview surfaces decisions you would otherwise leave Claude to guess
- A written `SPEC.md` is a durable handoff: review it, edit it, reuse it
- A fresh session implements from the spec without the noise of the discussion
- Separating "decide" from "build" produces sharper results on larger features
