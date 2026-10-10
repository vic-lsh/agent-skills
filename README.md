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
