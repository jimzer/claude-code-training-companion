# Claude Code Formation

Companion repository for the Claude Code training.

## Structure

```
├── demo-app/                 # FastAPI demo application (the substrate we explore)
│   ├── app/                  # Application code
│   ├── tests/                # Test suite
│   └── CLAUDE.md             # Project context for Claude
│
│   # Concept stations, in the order we go through them:
├── 01-claude-md-examples/    # Give Claude context (minimal / standard / enterprise)
├── 02-skills-demo/           # Reusable instructions (.claude/skills/)
├── 03-hooks-demo/            # Deterministic automation (.claude/ hooks + scripts)
├── 04-agents-demo/           # Specialized subagents (.claude/agents/)
├── 05-github-integration/    # @claude on PRs, auto-review, web (.github/workflows/)
│
├── exercises/                # Hands-on exercises (consolidation)
│   ├── 01-explore.md         # Codebase exploration
│   ├── 02-plan-mode.md       # Plan mode practice
│   ├── 03-freestyle.md       # Open challenges
│   └── 04-piping.md          # CLI & piping tricks
│
└── cheatsheet.md             # Quick reference card
```

## Getting Started

### Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- [uv](https://docs.astral.sh/uv/) installed (Python package manager)
- Python 3.11+

### Quick Start
```bash
# Clone the repo
git clone <repo-url>
cd claude-formation

# Set up the demo app
cd demo-app
uv sync
make test  # Verify everything works
make run   # Start the API server

# Open Claude Code
claude
```

## Demo App

The centerpiece is a **Task Manager API** built with FastAPI. It has:
- Full CRUD for tasks and users
- SQLite database with SQLAlchemy async
- Intentional bugs and gaps for demo purposes
- Partial test coverage

### Intentional Demo Opportunities
1. **Timezone bug** -- `task_service.py` uses naive `datetime.now()` instead of UTC
2. **No pagination** -- List endpoints return all records
3. **Missing tests** -- User service has no tests
4. **Lint issues** -- Some inconsistent formatting

## Session Outline

1. **Introduction** -- What is Claude Code, how it works
2. **Live Demo** -- Exploring code, finding bugs, plan mode
3. **Hands-On Workshop** -- Exercises 1-4
4. **Customization** -- CLAUDE.md, Skills, Agents, Hooks
5. **Advanced Patterns** -- Subagents, worktrees, scaling
6. **Best Practices & Wrap-Up**

## Resources
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- See `cheatsheet.md` for quick reference
