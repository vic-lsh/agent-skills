# agent-skills

Skills for Claude Code and Codex. Each folder under `skills/` is one skill (`SKILL.md` plus any files it references).

## Install

Symlink each skill into the folder your agent loads skills from:

```bash
git clone https://github.com/vic-lsh/agent-skills.git ~/.agent-skills
for s in ~/.agent-skills/skills/*/; do
  ln -sfn "${s%/}" ~/.claude/skills/"$(basename "$s")"   # Claude Code
  ln -sfn "${s%/}" ~/.codex/skills/"$(basename "$s")"    # Codex
done
```

## Per-project state

Skills that build up knowledge about a project keep it in `~/.agent-state/<skill>/<project>.md`, outside both the skill and the project repo. If `~/.agent-state` is a git checkout, the skill commits each change there (it never pushes).

## Skills

- [`maintain-skills`](skills/maintain-skills/SKILL.md): how to add, edit, split or clean up a skill, or record a lesson. Decides whether a lesson belongs in a script, project docs, state, the skill or a reference file, keeps skills short and free of private details, and runs a lint. Use whenever you create or change a skill.
- [`orchestrate-agents`](skills/orchestrate-agents/SKILL.md): run a long multi-agent engineering effort as an orchestrator that steers subagents and does not implement. Covers the work loop, dispatching, handling handoffs and recovering after a restart. Use when asked to orchestrate or coordinate subagents or to report on their progress periodically.
- [`progress-update`](skills/progress-update/SKILL.md): give a high-level status of an orchestrated multi-agent effort since the last update, including decisions made without the user so they can correct them. Use when the user asks for a progress update, recap or "where are we".
- [`validation-ladder`](skills/validation-ladder/SKILL.md): choose how to validate a change by climbing from cheap checks to expensive ones, using the project's own ladder or building one from an example. Covers minimum levels by risk, pushing escaped bugs down, keeping each level fast, and approval for expensive runs. Use when planning validation, gating a live run, or when a feedback loop is too slow.
- [`wtf`](skills/wtf/SKILL.md): ask for the last explanation again in simpler technical terms. Invoke as `/wtf`.

## Maintenance

When you add, rename or remove a skill, update the Skills list in the same commit.
