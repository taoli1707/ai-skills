# ai-skills

Skills for AI coding agents (Claude Code and compatible tools).

Each skill lives in `skills/<name>/` and contains a `SKILL.md` that the agent
loads, plus any references, scripts and assets the skill needs.

## Skills

| Skill | Purpose |
|---|---|
| [explainer-html](skills/explainer-html/) | How to write HTML pages that are easy to understand for a reader whose first language is not English: concrete examples, full detail, explicit step-by-step logic, data with sources. |

## Installing a skill in Claude Code

Copy or symlink a skill folder into `~/.claude/skills/`:

```sh
ln -s "$(pwd)/skills/explainer-html" ~/.claude/skills/explainer-html
```
