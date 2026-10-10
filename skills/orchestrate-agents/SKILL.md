---
name: orchestrate-agents
description: Run a long multi-agent engineering effort as an orchestrator that steers and does not implement. Use when the user asks you to orchestrate, steer, or coordinate subagents on a large task, starts a /loop that reports on agent progress, or asks for periodic progress reports and dispatch reflection over a work plan.
---

# Orchestrate agents

You own scoping, sequencing, integration and reporting. Subagents own implementation. Do not edit code yourself; logging decisions, filling ledgers and merging already-gated branches are fine.

## Step 0: load the project profile

Read `~/.agent-state/orchestrate-agents/<repo-name>.md` (repo name = basename of the git top-level directory) and this machine's `~/.agent-state/hosts/<hostname -s>.md`, whose Locations table resolves each `{name}` the profile uses; create the host file if missing. It holds everything project-specific: checks, guardrails, branch and gate rules, record locations, names, stop points, approvals. "The profile" below means its values. Also read `~/.agent-state/orchestrate-agents/defaults.md` if it exists: the user's standing choices for every project. If no profile exists, write one from [profile-template.md](references/profile-template.md) before dispatching. Whenever you change a profile and `git -C ~/.agent-state rev-parse` succeeds, commit that file there with a one-line message. Do not push.

## Standing inputs

Each overrides the defaults below.
- **Fanout cap:** maximum concurrent agents. If neither user nor profile gave one, use 3 provisionally and say so in the first report. One light read-only audit may run as an extra. Subagents spawn no nested agents unless the brief allows, then at most 2.
- **Model policy:** strongest model for design, hard implementation and spec or interface changes; a cheaper one for scoped execution (merges, CI, tooling, docs, measurement). Never exceed the model ceiling the user or defaults set. Try a new model on a contained task with clear pass/fail first. Never swap the model of work in progress.
- **Autonomy:** never block on the user's decision. Pick the recommended option, start it and all option-independent work in the same turn, log it as provisional with what reversing it would cost, and present it for override. Ask only about what the user reserved.
- **Stop points:** at any "checkpoint with me when X is done", stop dispatching and report.

## The loop

- **Start it on invocation** if none runs: invoke the `loop` skill with no interval and a prompt that re-enters this skill (`/orchestrate-agents tick: <goal>. Assess each agent against expected progress, steer, reflect on efficiency, report.`). Cadence from user or profile, default 30 minutes. Reuse a `/loop` the user started.
- **Self-paced:** `ScheduleWakeup` with the prompt verbatim; re-arm every tick, after every task notification, and after a restart. Stop the loop at a stop point or when done, and say so.
- **Each tick:**
  1. Inspect cheaply: `git fetch`, each branch's recent log, `git status` in each worktree, log mtimes and processes. Never read a running agent's transcript. Stop orphaned processes and containers left by finished agents.
  2. Compare each agent with its expected first commit and handoff time. Behind without activity: one steering message, specific and short; still silent ~10 minutes later: stop it and restart on the same model. Behind because scope grew: re-scope or split.
  3. Handle finished work (below).
  4. Simplify: stop or defer gates, items, batches and checks that no longer change the outcome, plans built on a false assumption, and deferrable scope; merge batches that can be one. Log each cut with the wall time it saves.
  5. Find multipliers: a per-step cost that repeats across remaining items (CI minutes, merge churn, check time, review rounds). Any check over 10 minutes is a defect to fix, not a timeout to raise. If fixing it saves more wall time than it costs, dispatch it now, ahead of feature work.
  6. Fill free slots with unblocked, non-conflicting work on the critical path; leave a slot idle rather than dispatch into a conflict.
  7. Report.
- **Report,** plain and in real units:
  1. Progress toward the end-to-end goal: overall percent weighted by remaining effort, then a table of workstreams with percent (merged and written separately when they differ), what remains and wall time left. Lead with time left when items keep uncovering work.
  2. What landed since the last report, with numbers.
  3. Efficiency: where wall time went, the biggest waste, the top lever with its gain and cost, and what you changed because of it.
  4. Simplification: what was cut and what it saves, or the smallest remaining path.
  5. Agents last, briefly: each one's job relative to the goal; whether each slot is on the critical path, which are idle on purpose, and whether fanout and model choices are right. Change something or say why not.

## Dispatching

When planning a phase, read [failure-patterns.md](references/failure-patterns.md). Before dispatching parallel items, read [integration.md](references/integration.md). Before writing a brief, read [briefs.md](references/briefs.md). Split work by file ownership, not plan numbering; feed the critical path first and recompute it as items land. Start downstream items early when their write sets are disjoint. When parallel items overlap on a module, sequence them on one integration branch, foundation first. It also covers batching, merges and live or hardware runs.

## Handling a handoff

1. Verify the head on origin; never trust a claimed commit.
2. Read [failure-patterns.md](references/failure-patterns.md) and check the handoff against it and against the profile's additional checks. At minimum: the design checks the brief required are present, with no unresolved "no" row and no old form kept beside its general form; the change is systematic (more than ~3 sites or several layers for one feature is a structure finding that gets a design item); nothing passes because of a stub, mock or shortcut; every new input has something that provides it; nothing the profile tracks grew or weakened unplanned; "done" with a dependency only named is partial; a fix to a cost or size metric gets the structural-cause question in failure-patterns.md.
3. Route each remaining obligation to an owning item; message running agents it affects. Never message a finished agent.
4. Decide the next chunk: continue, split, re-plan or park. Park work that doesn't converge after two chunks and is off the critical path, recording its gains and lessons.
5. Log a decision entry and a ledger row.
6. Never relay a denied action to another agent; surface it to the user.

## Records and reviews

Keep a numbered decision log (decision, why, alternatives, follow-ups) and an effort ledger (one row per item: model, estimate, wall clock, check time, tokens, outcome). Run a read-only review every ~2 hours of agent work or every 3 to 4 landed PRs; read [reviews.md](references/reviews.md) for what it checks, design alignment, and forecasting. Private operational detail stays out of the project repo and out of briefs that commit.

## Recovering from a restart

Stopped agents cannot be resumed. Inspect each branch and worktree (pushed commits, uncommitted edits, stray files), start a continuation agent on the same model whose brief states exactly what is pushed and that in-flight external runs are gone, and re-arm the loop.
