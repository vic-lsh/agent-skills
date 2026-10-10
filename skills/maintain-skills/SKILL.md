---
name: maintain-skills
description: Add, edit, split or clean up an agent skill, or record a lesson about how to do a kind of task. Decides where a lesson belongs (a script, project docs, per-project state, the skill, or a reference file), keeps skills short and free of private details, and checks them with a lint. Use when creating or changing any skill, when a skill has grown long, or when the user says to remember a lesson that should apply beyond one project.
---

# Maintain skills

An agent reads a skill's whole `SKILL.md` every time the skill runs, so every line costs context and attention on every use. Keep in it only what is needed every time; put the rest where it is read only when needed.

If `~/.agent-state/maintain-skills/setup.md` exists, read it first: it says where this user's skill repositories are and which are public.

## Where a lesson goes

Take the first place that fits. A lesson lives in exactly one place; other places link to it.

1. **A script** in `scripts/`, if a program can check or do it. The skill says when to run it.
2. **The project's own docs** (its agent instructions file or contributor docs), if every contributor to that project should follow it. Propose it through the project's normal change process.
3. **Per-project state**, `~/.agent-state/<skill>/<project>.md`, if it is true only of one project or of this user's setup: paths, machines, commands, accounts, approvals.
4. **`SKILL.md`**, if the agent needs it every time the skill runs.
5. **A reference file** in `references/`, if it is needed only at one step. `SKILL.md` names the step and links the file there, for example "Before writing a brief, read `references/briefs.md`" as a markdown link.

Before adding a rule, search the skill for one that covers it, and sharpen that rule instead of adding a line. A lesson about a kind of task saved in one project's agent memory is invisible in every other project: move it to the skill and leave only the project-specific part behind.

## Layout

Follow the Agent Skills convention (agentskills.io):

```
<skill-name>/
  SKILL.md       required; the only file always read when the skill runs
  references/    docs the agent reads at a named step (*.md)
  scripts/       code the agent runs rather than reads
  assets/        files used in the output: templates, images, fonts
```

Nothing else sits next to `SKILL.md` except a license file. Link every reference file directly from `SKILL.md`, at the step that needs it: an unlinked file is never read, and one reached only through another reference tends to be read partially. Reference files may also link each other by relative path.

## Writing

- **Frontmatter:** `name` equals the folder name and names the task (`maintain-skills`, `open-pr`). `description` says what the skill covers and when to use it; it is the only part always loaded, so it decides when the skill triggers.
- **Rules, not stories.** Write each rule as one line saying what to do. The incident behind it goes in a reference file only if the reasoning is needed to apply the rule well.
- **Procedures as numbered steps.**
- **Link, don't restate:** project docs, other skills, reference files.
- **No private details in a general skill:** absolute paths, host or cluster names, project names, people. Read them from the per-project state file instead.

## Size

The lint limits `SKILL.md` to 100 lines and 1,200 words, and each reference file to 2,000 words. When over, in this order:

1. Delete rules that no longer change what the agent does, or that a script now enforces.
2. Merge rules that say the same thing.
3. Move material needed at only one step into a reference file.

## Refactoring a skill

1. List every rule in the current version with the place it should go, by "Where a lesson goes".
2. Rewrite. Every old rule ends up in exactly one place or on a deleted list with a one-line reason.
3. Run the lint.
4. Show the user the size before and after, and the deleted list, before publishing.

## Check

Run `python3 scripts/lint_skills.py <skills folder>` from this skill's folder after any change. It checks size, frontmatter, the layout above and that every link resolves. For a public repository add `--public --denylist ~/.agent-state/maintain-skills/denylist.txt`; it also refuses absolute paths and the private names listed there. When a new private name appears (a project, host or person), add it to the denylist.

New skills start in a private repository. Move one to a public repository only after the public lint passes and the user has reviewed it.
