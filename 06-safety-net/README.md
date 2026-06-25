# 06 - The safety net

**Goal:** make verification automatic, so that going faster with AI does not mean shipping more bugs.

## The thesis (this is the important part)

AI makes you write more code, faster. That is the whole point. But it shifts the bottleneck:

```
more AI  ->  more code & features  ->  less human review per line
         ->  more bugs & security holes slip through
```

The answer is NOT "review harder" (you can't out-review an AI). The answer is to **systematize verification** so that quality is checked by machines, every time, with no human discipline required. That layered set of automatic checks is your *safety net*:

| Layer | Catches | In this station |
|-------|---------|-----------------|
| Formatter (`ruff format`) | style drift | `make check` |
| Linter (`ruff check`) | dead code, bad patterns | `make check` |
| Type checker (`mypy`) | type errors, bad signatures | `make check` |
| Unit / integration / e2e tests | broken behavior | `make check` |
| Hooks | runs the net automatically | `.claude/hooks/safety-net.sh` |
| AI review on PRs | logic & security a linter can't see | station `05` |

The net works the same whether a human or Claude wrote the code. That is the point: **you stop trusting the author and start trusting the gate.**

## What's wired up in this repo

- `make check` runs the full gate: `ruff format --check` + `ruff check` + `mypy` + `pytest`. One command, all layers.
- `.claude/hooks/safety-net.sh` is a **Stop hook**: Claude cannot end its turn until `make check` is green. If anything fails, the failure is fed back to Claude and it keeps working. Try it below; it is the most convincing demo in the course.
- `ci.example.yml` shows the same gate running in GitHub Actions, so the net also guards every PR (rename to `.github/workflows/ci.yml` in a real repo).
- `app.py` + `tests/` are a clean, fully-passing baseline so you can watch the net react when you (or Claude) change something.

## Try it

1. Run `uv sync`, then `make check`. Everything passes (green baseline).
2. In Claude Code, ask: *"add a `total_with_tax` function to `app.py`"* but deliberately give it a vague spec. When Claude tries to finish, the Stop hook runs `make check`. If the new code has a type error, a lint issue, or no test, **Claude is blocked from stopping** and fixes it itself.
3. Break something on purpose (delete a type hint, add an unused import) and watch `make check` go red.

## What to notice

- The net is **author-agnostic**. It does not care that an AI wrote the code; it checks the result.
- Each layer catches a different class of problem. Tests don't catch type errors, types don't catch logic bugs, and none of them catch a leaked secret (that's the hook in station `03`). You want all of them.
- The Stop hook turns "please remember to run the tests" into a guarantee. Discipline you have to remember is discipline you don't have.

## Secrets belong in the net too

A leaked key is a quality failure like any other. Two complementary controls live elsewhere and pair with this station:

- **Block reads** of `.env` / `credentials` with a PreToolUse hook (see station `03`).
- **Inject** the keys your skills/scripts need via `.claude/settings.local.json` (normally git-ignored, force-tracked here with fake values so you can see the shape), never hard-coded. The `env` block is injected into the tool environment.
