# Recipe prompts

Copy-paste starting points. Adapt the data source to your own.

## 1. Interactive HTML dashboard

```
Read tasks.json (or: the output of `curl localhost:8000/tasks`). Build a single
self-contained dashboard.html with inline CSS and JS, no external dependencies,
no build step. Include: total counts, a bar chart of tasks by status, and a table
of the 10 most recent. It must open correctly by double-clicking the file.
```

## 2. Rich report / one-pager

```
Turn the notes in meeting-notes.md into a styled one-page HTML report:
a title, an executive summary, decisions as a checklist, and action items in a
table with owners. Clean, printable, self-contained. Save as report.html.
```

## 3. Test generation (grows the safety net)

```
Read app/services/user_service.py. It has no tests. Write a complete pytest
suite in tests/test_user_service.py covering the happy path, edge cases, and
error handling. Then run the tests and fix anything that fails.
```

## 4. Slide deck

```
From outline.md, generate a slide deck. One TSX component per slide using the
shared components, then render to PDF. (See the presentation/ repo for the
exact system this course's own slides use.)
```

## Tips

- Ask for **self-contained** output (inline everything) when you want zero-friction sharing.
- Have Claude **open or run** the artifact and iterate, rather than guessing. For example: "open it and fix the layout."
- Pair recipe 3 with station `06`: generated tests only count once they pass the gate.
