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
- [`design-for-verification`](skills/design-for-verification/SKILL.md): shape a codebase so its correctness can be checked cheaply and at scale (deterministic core, injected nondeterminism, fault seams, recorded boundaries), then verify it from small to large: types and assertions, unit and property tests, fuzzing, deterministic simulation, model checking, end-to-end, replay and live runs. Use when designing a component, planning verification, or gating an expensive run.
- [`codify`](skills/codify/SKILL.md): turn any mechanical part of the work (review checks, recurring rules, repeated manual steps, slow loops) into code tools instead of agent reasoning: lints, enforced dependency structure, static analyzers, ratchets, caches and sharding, self-classifying diagnostics, generators. Use when a step or review finding recurs, a check is slow, or a defect was found late that a program could have caught.
- [`wtf`](skills/wtf/SKILL.md): ask for the last explanation again in simpler technical terms. Invoke as `/wtf`.

## Maintenance

When you add, rename or remove a skill, update the Skills list in the same commit.
