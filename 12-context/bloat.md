# Bloat prompts

Paste these one at a time into a fresh session. Each one pulls a pile of file
contents into the conversation, growing the Messages slice. Run `/context`
before you start and again after a few of these to watch it climb.

1. Read every file under `../demo-app/app` and summarize each one in detail.
2. Now read `../demo-app/app/routers` and `../demo-app/app/services` and explain how requests flow through them line by line.
3. Read `../demo-app/tests` and explain the test coverage, walking through each test case.
4. Read `../demo-app/CLAUDE.md` and `../demo-app/pyproject.toml` and explain the stack and conventions.
5. Read `../demo-app/app/models` and `../demo-app/app/schemas` and dump every field with its type and purpose.
6. Quote the full contents of `../demo-app/app/main.py` and `../demo-app/app/db.py` back to me and annotate every line.

By now Messages should dominate `/context`. That is the lever you control.
