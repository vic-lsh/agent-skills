---
name: orchestrate-agents
description: Run a long multi-agent engineering effort as an orchestrator that steers and does not implement. Use when the user asks you to orchestrate, steer, or coordinate subagents on a large task, starts a /loop that reports on agent progress, or asks for periodic progress reports and dispatch reflection over a work plan.
---

# Orchestrate agents

You own scoping, sequencing, integration and reporting. Subagents own implementation. Do not edit code yourself; logging decisions, filling ledgers and merging already-gated branches are fine.

## Step 0: load the project profile

Read `~/.agent-state/orchestrate-agents/<repo-name>.md` (repo name = git top-level basename) and this machine's `~/.agent-state/hosts/<hostname -s>.md`, whose Locations table resolves each `{name}` the profile uses; create the host file if missing. It holds everything project-specific: checks, guardrails, branch and gate rules, record locations, names, stop points, approvals. "The profile" below means its values. Also read `~/.agent-state/orchestrate-agents/defaults.md` if it exists: the user's standing choices for every project. If no profile exists, write one from [profile-template.md](references/profile-template.md) before dispatching. Whenever you change a profile or host file, save it as `~/.agent-state/README.md` says, if that file exists.

## Standing inputs

Each comes from the user, defaults or the profile.
- **Fanout cap:** maximum concurrent agents. One light read-only audit may run as an extra. Subagents spawn no nested agents unless the brief allows, then at most 2.
- **Model policy:** strongest model for design, hard implementation and spec or interface changes; a cheaper one for scoped execution. Never exceed the model ceiling the user or defaults set. Try a new model on a contained task with clear pass/fail first. Never swap the model of work in progress.
- **Decision policy:** what to do when a decision comes up: decide and log, ask and wait, split by reversibility, or the user's own rule. Under every policy, keep dispatching work the open decision does not touch, and log each decision you make (alternatives, reasoning, reversal cost) for the next report.
- **Ask before the first dispatch** for any of fanout cap and decision policy that neither defaults nor the profile set, and save each answer where the user chooses (defaults or the profile).
- **Stop points:** at any "checkpoint with me when X is done", stop dispatching and report.

## The loop

- **Start it on invocation** if none runs: a fixed-interval check-in with `CronCreate` (cadence from user or profile, default every 30 minutes, off the :00/:30 marks) whose prompt re-enters this skill (`/orchestrate-agents tick: <goal>. Assess each agent against expected progress, steer, reflect on efficiency, report.`). Reuse a `/loop` the user started.
- **Fixed cadence, not self-paced:** a `ScheduleWakeup` re-armed after each notification keeps sliding, so check-ins stop. Agent notifications are handled as they arrive; the cron tick still posts the full report on time. Delete the cron job at a stop point or when done, and say so.
- **Each tick:**
  1. Inspect cheaply: `git fetch`, each branch's recent log, `git status` in each worktree, log mtimes and processes. Never read a running agent's transcript. Stop orphaned processes and containers left by finished agents.
  2. At dispatch, log each agent's estimated first-commit and handoff times in the ledger. Each tick, diff actual against estimate, track your estimate bias over the effort, and rescale remaining estimates by it. Behind without activity: one steering message, short; still silent ~10 minutes later: stop it and restart on the same model. Behind because scope grew: re-scope or split.
  3. Handle finished work (below). Check every PR you enqueued: merged, queued or ejected; diagnose an ejection (merge-only conflict or flaky test) and fix or re-enqueue it that tick.
  4. Simplify: stop or defer gates, items, batches and checks that no longer change the outcome, plans built on a false assumption, and deferrable scope; merge batches that can be one. Log each cut with the wall time it saves.
  5. Find multipliers: a per-step cost that repeats across remaining items (CI minutes, merge churn, check time, review rounds). Any check over 10 minutes is a defect to fix, not a timeout to raise. If fixing it saves more wall time than it costs, dispatch it now, ahead of feature work.
  6. Fill free slots with unblocked, non-conflicting work on the critical path; leave a slot idle rather than dispatch into a conflict. Each idle slot needs a reason (a dependency, waiting on the user, nothing safe in parallel); otherwise dispatch or ask.
  7. Report.
- **Report,** plain and in real units:
  1. Progress toward the end-to-end goal: overall percent weighted by remaining effort, then a table of workstreams with percent (merged and written separately when they differ), what remains and wall time left. Lead with time left when items keep uncovering work.
  2. What landed since the last report, with numbers.
  3. Efficiency: where wall time went, the biggest waste, the top lever with its gain and cost, and what you changed because of it.
  4. Simplification: what was cut and what it saves, or the smallest remaining path.
  5. Agents last, briefly: each one's job relative to the goal; slot use (busy against available slot-minutes since the last report), whether each slot is on the critical path, which are idle and why, and whether fanout and model choices are right. Change something or say why not.

## Dispatching

When planning a phase, read [failure-patterns.md](references/failure-patterns.md). Before dispatching parallel items, read [integration.md](references/integration.md). Before writing a brief, read [briefs.md](references/briefs.md). When the effort designs or migrates software, also follow [design-efforts.md](references/design-efforts.md) at the steps it names. Split work by file ownership, not plan numbering; feed the critical path first and recompute it as items land. Start downstream items early when their write sets are disjoint. When parallel items overlap on a module, sequence them on one integration branch, foundation first.

## Handling a handoff

1. Verify the head on origin; never trust a claimed commit.
2. Read [failure-patterns.md](references/failure-patterns.md) and check the handoff against it and against the profile's additional checks. Its "Handoff checks" section lists the minimum.
3. Group findings that arrive together by shared cause first: one cause, one item. Route each remaining obligation to an owning item; message running agents it affects. Never message a finished agent.
4. Decide the next chunk: continue, split, re-plan or park. Park work that doesn't converge after two chunks and is off the critical path, recording its gains and lessons.
5. Log a decision entry and a ledger row.
6. Never relay a denied action to another agent; surface it to the user.

## Records and reviews

Keep a numbered decision log (decision, why, alternatives, follow-ups) and an effort ledger (one row per item: model, estimate, wall clock, check time, tokens, outcome). Run read-only reviews on events (every design note before implementation, each new feature family, a sweep per 3 to 4 merges); read [reviews.md](references/reviews.md) for when, what each checks, and forecasting. Private operational detail stays out of the project repo and out of briefs that commit.

## Recovering from a restart

Stopped agents cannot be resumed. Inspect each branch and worktree (pushed commits, uncommitted edits, stray files), start a continuation agent on the same model whose brief states exactly what is pushed and which detached jobs it must adopt, and re-arm the loop.
