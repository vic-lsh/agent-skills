---
name: handoff
description: Write or read a compact handoff document so a fresh agent can continue a chunk of work without re-reading what the previous agent already learned. Use when an agent stops at a chunk boundary, budget or time box, or when starting work that a previous agent handed off.
---

# Handoff

The next agent starts with no context. The handoff document is the only thing it reads before acting, plus the files on its read list. Aim for under 2,000 tokens.

## Writing (outgoing agent)

1. Write to the path the brief names; if none, `handoffs/<branch-with-slashes-as-dashes>.md` under the records location the brief names, else `$TMPDIR`. Overwrite the previous handoff for the same branch; durable history belongs in the project's findings or commits.
2. Verify the head before writing: `git log -1 origin/<branch>` must show your last commit.
3. Use these sections, in order, one line per item:
   - **Head:** branch, verified commit, worktree, build cache or volume, base branch and the commit last merged from it.
   - **Done:** each completed step with its commit hash.
   - **Next:** the remaining steps in order. The first step is a concrete action (a file and a symbol, a command), not a topic.
   - **Decided:** decisions made this chunk and the one-line reason, so the next agent does not reopen them. Link the spec or design note that holds settled decisions.
   - **Open:** questions only the orchestrator or user can answer, each with your recommended answer.
   - **Traps:** commands that need special flags, pre-existing failures to ignore (with proof they reproduce on the base), approaches tried and abandoned with why.
   - **Checks at head:** each check with pass, fail (one-line cause) or not run. Quote tools' own summary lines; never count by eye.
   - **Read list:** only what the next agent must read, as file plus symbol or section; never "read the crate".
   - **Skills:** skills the next agent should invoke.
   - **Cost:** tokens used; minutes in checks, in base-branch merges, and in editing.
4. Reference, never restate: specs, design notes, findings, commits and diffs are linked by path, hash or URL.
5. Leave out secrets, credentials, private hosts and personal data.
6. Reread it as the next agent: could you make the first edit within 10 minutes? If not, fix the Next and Read list sections.

## Reading (incoming agent)

1. Read the handoff first, then only its read list and the files you will edit.
2. Treat Decided as settled. Reopen a decision only with new evidence, and say so in your own handoff.
3. Rerun the checks marked fail or not run before relying on them; trust the passes at the verified head.
