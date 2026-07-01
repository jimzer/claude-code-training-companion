# 13b - Goals

**Goal:** keep an agent driving toward a verifiable end state across many turns, instead of nudging it step by step.

**Concept:** `/goal "<verifiable end state>"` sets a target. After each turn an independent evaluator checks whether the end state is met; if not, it relaunches the agent to keep working. You describe the END STATE, not the steps. The trick is to phrase the goal so a machine can decide pass/fail, for example "all tests in this folder pass" or "the server returns 200 on /health", not "make the code better".

## What's in here

- `widget.py` : two functions, one of which (`discount_price`) raises `NotImplementedError`.
- `test_widget.py` : two tests; the `discount_price` test fails until the function is written.

## Try it

```bash
cd 13-scaling/b-goals

# 1. See the failing test (one failure, one pass)
python -m pytest -q

# 2. Open Claude in this folder
claude
```

1. Confirm the red baseline: `pytest` shows `test_discount_price` failing.
2. In Claude set the goal as an end state, not a recipe:
   ```
   /goal "all tests in 13-scaling/b-goals pass"
   ```
3. Watch the loop: Claude implements `discount_price`, the evaluator runs the tests, and it keeps iterating until the suite is green, then stops on its own.

## What to notice

- You stated the *destination* ("tests pass"), not the *route* ("edit line 14"). The evaluator owns the check; the agent owns the work.
- The goal is **verifiable**: a test run gives an unambiguous pass/fail. Vague goals ("make it nicer") have nothing to converge to and the loop never ends.
- The evaluator is independent of the working agent, so "I think I'm done" does not end the loop; the actual check does. This is the same trust shift as the safety net in station 06: stop trusting the author, trust the gate.
- Goals compose with scaling: a goal can pin a long-running background or team task to a target so the parallel work converges instead of drifting.
