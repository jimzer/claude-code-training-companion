# 08 - Power-user recipes

**Goal:** break the habit of treating Claude Code as a chat box that only emits text. It can produce *artifacts* (runnable files, rich HTML, charts, decks, test suites) directly into your repo. Output is not limited to the terminal.

This is the "wow" station. Keep it short and let the artifacts speak.

## The mindset shift

Most people ask Claude a question and read the answer. Power users ask Claude to **build the thing**:

- Instead of asking "how's our test coverage?", ask it to **generate the missing tests**.
- Instead of asking "summarize these logs", ask it to **build an HTML dashboard** you can open in a browser.
- Instead of asking "what should the report say?", ask it to **write the report as a styled document**.

The deliverable is a file in your repo, not a paragraph you then have to act on.

## Recipes

See `prompts.md` for the exact prompts. Each produces a real file.

1. **Interactive HTML dashboard.** Point Claude at some data (a CSV, log file, or API output) and ask for a single self-contained `.html` with charts. `examples/dashboard.html` was generated this way; open it in a browser.
2. **Rich report / one-pager.** Turn raw notes or query results into a styled, shareable HTML or Markdown document instead of a wall of text.
3. **Test generation.** Point at an untested module and ask for a full pytest suite (this is also how you grow the safety net from station `06`).
4. **Slide deck.** Generate a presentation from an outline. This very training's slides are built exactly this way, as TSX rendered to PDF.

## Try it

1. Open `examples/dashboard.html` in a browser to see the target.
2. In Claude Code, run the dashboard prompt from `prompts.md` against your own data (or the demo-app's task list).
3. Ask for one change ("add a pie chart of tasks by status") and watch it edit the file in place.

## What to notice

- **Self-contained beats fancy.** A single HTML file with inline CSS/JS has no build step and opens anywhere, which is ideal for a quick dashboard or report you hand to a non-technical colleague.
- The artifact lives in your repo, so it's versioned, reviewable, and regenerable.
- Anything with a text format (HTML, SVG, Markdown, CSV, TSX, Mermaid) is fair game. "Generate a file" is a first-class use of the tool.
