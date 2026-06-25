# Governance: adopting AI coding responsibly

A template **company adoption playbook**. This is the document a team lead keeps and adapts after the training. It is policy, not code: how to roll out AI coding without creating data-privacy, security, or quality problems.

Adapt the bracketed `[...]` parts to your organization.

---

## 1. Data privacy: what may leave the building

The first question every company must answer: **what are people allowed to send to an AI model?**

### Default rule
> [Company] code, internal docs, and non-personal config **may** be sent to [approved provider]. **Never** paste customer PII, secrets, credentials, or [regulated data category] into any AI tool.

### Know your training-data setting
This is the part most people get wrong:

| Plan | Is your data used to train the model by default? |
|------|--------------------------------------------------|
| Personal (Free / Pro / Max) | **Yes, by default.** You can **opt out** in settings. |
| Team / Enterprise | **No, opted out by default.** |

Action items:
- For any company work on personal plans, **turn off training/data-sharing** in account settings, and verify it.
- Prefer **Team/Enterprise** plans for company use: opt-out is the default and you get central admin control.
- Document which plan tier is approved for which kind of work.

## 2. A repository of allowed skills

Skills (and subagents, MCP servers, slash commands) are **executable instructions**. A skill copied from a random gist can run commands, read files, and exfiltrate data.

> **Rule:** only skills from `[company-skills-repo]` may be installed. Anything from the internet is **reviewed and added to that repo first**, never loaded ad hoc.

- Maintain a vetted internal registry. See `allowed-skills.md` for the template.
- Review new skills like you review dependencies: read what they actually do before approving.
- The same caution applies to MCP servers and any `.claude/` config pulled from outside.

## 3. Least privilege for tools, especially databases

An agent that can run SQL can also `DROP TABLE` by mistake. Don't rely on the model being careful; **remove the capability**.

> **Rule:** when Claude can execute SQL, it connects as a **read-only / least-privilege DB user**, never as an admin or the app's write user.

- Create a dedicated `claude_readonly` DB role with `SELECT` only (grant writes only to specific tables when genuinely needed).
- Same principle for filesystem, cloud, and API credentials: scope tokens to the minimum, prefer read-only.
- Use Claude Code's permission model and hooks (see station `03`) to block dangerous tools by default.

## 4. Secrets handling

> **Rule:** secrets are **never** hard-coded, pasted into chat, or committed. They are injected via local config and kept out of git.

- Put local-only keys in **`.claude/settings.local.json`** under `env`. This file is normally git-ignored and the values are injected into the tool environment. See `06-safety-net/.claude/settings.local.json` for a (fake-value) example.
- Block AI access to `.env` / `credentials` / `secrets` files with a **PreToolUse hook** (see station `03`).
- Add a **secret-scanner** to the CI gate (station `06`) so a leaked key fails the build.

## 5. Keep the safety net mandatory

AI raises code volume, which lowers review-per-line. The net (station `06`) is what keeps quality flat as volume rises.

> **Rule:** all AI-assisted code passes the same automated gate as human code: format, lint, types, tests, and AI review on PRs (station `05`). No exceptions for "the AI wrote it."

## 6. Human accountability

> **Rule:** a named human **owns** every merge. AI assists; it does not approve its own work. The author is responsible for what they ship, regardless of who typed it.

---

## Rollout checklist

- [ ] Pick approved plan tier(s); verify training opt-out is set.
- [ ] Stand up the allowed-skills registry (`allowed-skills.md`).
- [ ] Create least-privilege DB roles for AI use.
- [ ] Standardize secrets via `settings.local.json` and the `.env` block hook.
- [ ] Make the safety-net gate mandatory in CI.
- [ ] Write down the data-privacy rule and circulate it.
- [ ] Name accountability for merges.
