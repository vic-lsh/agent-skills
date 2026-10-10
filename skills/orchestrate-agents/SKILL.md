---
name: orchestrate-agents
description: Run a long multi-agent engineering effort as an orchestrator that steers and does not implement. Use when the user asks you to orchestrate, steer, or coordinate subagents on a large task, starts a /loop that reports on agent progress, or asks for periodic progress reports and dispatch reflection over a work plan.
---

# Orchestrate agents

You own scoping, sequencing, integration and reporting. Subagents own implementation. Do not edit code yourself. Small orchestrator-owned actions are fine: logging decisions, filling in ledgers, and merges of already-gated branches.

## Step 0: load the project profile

Read `~/.agent-state/orchestrate-agents/<repo-name>.md` (repo name = basename of the git top-level directory). The profile supplies everything project-specific: check commands, guardrails (what must not grow or weaken), branch and gate rules, record locations, reserved terms, stop points and approval rules. Where this file says "the profile", use its values.

If no profile exists, ask the user for the items in "Profile contents" below, or derive them from `CLAUDE.md` and memory, and write the profile there before dispatching (create the directory if missing). Profiles live outside the project repo and outside this skill because they may name private paths; link to `CLAUDE.md` and memory rather than copying them. Keep only what is specific to this user's setup: a rule every contributor should follow belongs in the project's own docs, so propose it there instead.

Whenever you create or change a profile, and `git -C ~/.agent-state rev-parse` succeeds (the state directory is version-controlled), commit that file there with a one-line message saying what changed. Do not push.

## Standing inputs from the user

Each overrides the defaults below.
- **Fanout cap.** The maximum number of concurrent agents. If neither the user nor the profile gave one, ask (AskUserQuestion, recommended option first) before the first dispatch. A light read-only audit may run as one extra. Subagents may not spawn nested agents unless the brief allows it, and then at most 2.
- **Model policy.** Default: the strongest model for design, hard implementation, and anything that changes a spec or interface (never Fable unless the user requests or authorizes it; the strongest default is Opus); a cheaper model for scoped execution (merges, CI runs, tooling, docs, measurement). Try a new model version on a contained task with clear pass/fail before widening its use. Never swap the model of work already in progress; a restarted agent keeps its original model.
- **Autonomy.** If the user said to decide without them, decide, log each decision, and present them on return. Ask only about what they reserved.
- **Stop points.** Honor any "checkpoint with me when X is done": stop dispatching there and report.

## The loop

- **Start it on invocation.** When this skill is invoked and no progress loop is running, start one before or right after the first dispatch: invoke the `loop` skill via the Skill tool with no interval (dynamic mode) and a prompt that re-enters this skill, for example `/orchestrate-agents tick: <goal in one line>. Every 30 minutes assess each agent against the progress expected, steer or restructure if behind, reflect on fanout use toward the goal, and report.` Use the cadence the user or profile gives (default 30 minutes, `delaySeconds` 1800). If the user already started a `/loop`, use theirs instead of starting a second one.
- **Self-paced.** `ScheduleWakeup` with the loop's prompt verbatim, at that cadence. Re-arm every tick and after handling every task notification. After a process restart the wakeup is gone; re-arm it. Stop the loop (`stop: true`) at a stop point or when all work is done, and say so in the final report.
- **Progress against expectation.** At dispatch, note each agent's expected first commit and handoff time (from its time box). Each tick, compare: an agent behind with no recent commits or log writes gets a short steering message; one that is behind because its scope grew gets re-scoped or split; one that is idle or stuck goes through the silent-agent rule in "Failure patterns".
- **Each tick:**
  1. Inspect cheaply: `git fetch`, recent log on each agent's branch, `git status` in its worktree. Never read a running agent's transcript; it floods context.
  2. Act on anything finished (see "Handling a handoff").
  3. Simplify. Before adding work, look for work to remove:
     - items, gates, batches or checks that no longer change the outcome (a gate another gate will cover, an audit a recent one covers, cleanup that is not on the path to the goal);
     - plans built on an assumption that turned out false (for example, work planned in one layer that another layer's result already made unnecessary);
     - separate batches or merges that can be combined into one;
     - running agents whose remaining scope can be deferred without blocking the goal.
     Stop or defer what qualifies, log each cut as a decision, and say in the report what was cut and what it saves in wall time.
  4. Fill free slots with unblocked work that won't conflict.
  5. Report.
- **Report,** concise and plain, with real units:
  - what each agent is doing, relative to the overarching goal;
  - what landed since the last report, with numbers;
  - per track: remaining wall time and what remains, named. Percent of obligations done overstates progress when items keep uncovering work; lead with time left.
  - dispatch reflection against the fanout cap: is each slot on the critical path, is parallelism right, is anything idle on purpose, are model choices right. Change something or say why not.
  - simplification: what was cut or merged this tick, or the smallest remaining path to the goal if nothing was cut.

## Scoping a brief

Every brief is self-contained; the agent has none of your context.
- **Goal and why:** one or two sentences tying the item to the overarching goal.
- **Setup:** worktree path and a new branch from an explicit base commit, plus branches to merge first; a build cache copied for this agent, never shared with a running agent; a log directory inside its worktree.
- **Read-first list:** project instructions, the plan item, prior handoffs and findings, audit findings aimed at this item, and the profile's design guide for any item that adds a feature or changes a spec or interface.
- **Design checks for a new instance** (a model, store, optimization or device), written in the first commit's finding, as the profile's design guide defines them: a mechanism-reuse table (which existing mechanism does the same job: reuse, generalize, or new with a reason), an instance-fact table (facts in code, specs and contracts true only of today's instances, including today's backend or hardware, with their general forms), and a per-pair count (code naming two features at once; target zero, plus one test with every existing feature on).
- **Alternatives considered** for any item that designs or changes an interface or spec: the note lists at least three designs that differ in abstraction level or mechanism, scored on one rubric (guarantees identical or disqualified; proof burden: where facts are proved, per-operation obligations, growth per new feature or instance, solver hotspots, trusted surface; expressiveness and openness; migration cost), and says why the choice wins. A mechanism already written in the project's design docs is one candidate, not a reason. Prototyping is the agent's call, not a requirement.
- **Design docs with the decision:** a design decision merges with its design-doc update, written as the current design (unbuilt parts in a status table); never deferred to the last step of a migration. Before briefing a design question, search existing design notes for one already approved.
- **Definition visibility** for any item that adds or changes specs: decide at design time which definitions callers may see the body of (interface: open, small, stable; representation: hidden behind a few exported facts; anything whose body grows with each feature hidden by default; automatic rules scoped to their users), with a consumer count per definition. Hiding a body changes cost and coupling, never a guarantee. A per-function fix for a solver or size budget whose cause is a shared definition's visibility is a structure finding.
- **Scope in priority order,** plus an out-of-scope list naming who owns each excluded piece. Excluded dependencies stay named, not assumed away.
- **File ownership** when agents run in parallel: the files it owns, the files others own, and what it may touch there (usually only mechanical updates, listed in the handoff).
- **Guardrails:** the profile's rules on what must not grow or weaken; no stub, mock or shortcut that makes a check pass without the real behavior; if it would have to weaken a result, stop and report.
- **Reachability:** every new input or dependency it relies on needs something that actually provides it (a caller, a config, a test that exercises it end to end).
- **Check cadence:** fast targeted checks while editing and per commit; the full check once at chunk end; the full CI set only at batch merges. Long checks run in the foreground with the maximum tool timeout; backgrounded checks stall agents.
- **Commits:** small, each passing, pushed immediately; no stash; the attribution trailer on every commit including merges.
- **Time box:** 45 to 90 minutes; first passing commit within about 30; "use the full box while scope remains and you are progressing" (otherwise agents hand off at about 40 minutes); "stop and hand off at the box".
- **Handoff contents:** what is done; remaining work with exact statements and sources; the delta on whatever the profile tracks; tests; cost numbers; what the next items need; wall clock from `date`.
- **Naming rules** from the profile.

## Parallelism and work division

- **Find the critical path.** Feed it first; recompute as items land. Tracks can swap which one is longer mid-run.
- **Split items by file ownership, not plan numbering.** When one item holds a module, start the halves of later items that live elsewhere.
- **Two agents may share a module only with a written ownership split.** The later one merges the earlier one's branch as it advances. Accept this only for real critical-path time saved. Move ownership explicitly when routing a fix into someone else's file, and tell both agents.
- **Start downstream items early when their write set is disjoint:** a "prep" pass on a later item surfaces its hidden work while the blocker is still running.
- **Leave a slot idle rather than dispatch into a conflict.** Say so in the report.
- **Prefer splitting a shared file by responsibility over serializing.** When two items need the same large file for different concerns, a short mechanical split item (one concern per file) usually costs less than the wait. Design notes name each new item's file, organized by concern, and briefs put new concerns in new files.
- **Integration trails.** Critical-path items base on their input branches directly, not on the integration branch. Batch finished branches; start a batch merge when a slot is free and the critical path is blocked anyway, rather than waiting for everything.
- **Batch pipeline:** a merge agent runs host CI on a batch branch; a gate agent runs expensive or hardware gates; you merge into the integration branch from a temporary worktree and never touch someone else's checkout.
- **Trial merge of in-flight branches:** when merge-only failures (each side passes, the merged tree fails) occur more than about once per 6 to 8 batches, run an hourly trial merge of all in-flight branches with targeted checks of the touched modules, so an interaction surfaces within the hour with a named owner; below that rate it costs more than it saves. Track the rate in the ledger.

## Handling a handoff

1. **Verify the head on origin.** Do not trust a claimed commit.
2. **Check the claims against the goal:**
   - Was the change systematic? If one feature touched more than about three dispatch sites or several layers, or restated a single-instance assumption, treat it as a structure finding: route a design item before more patches land.
   - Are the design checks present, with no unresolved "no" row, a per-pair count of zero or each site named, and no old form kept beside its general form?
   - Does anything pass only because of a stub, mock or shortcut?
   - Did anything the profile tracks grow or weaken, and was that planned?
   - Is every new input or dependency actually provided somewhere? Ask for the caller or end-to-end test. Work that depends on something nothing provides looks done but never runs, and can go unnoticed across many items.
   - If a report says "done" but a dependency is only named, the item is partial. Record it as partial.
   - Apply the profile's additional handoff checks.
3. **Route each remaining obligation to an owning item,** and message running agents whose code it affects. Messages to a running agent are for steering: specific and short.
4. **Decide the next chunk:** continue, split, re-plan (a blocker may need a design decision you make and log), or park. Park work that doesn't converge after two chunks and is off the critical path, keeping its gains and lessons.
5. **Log a decision entry and a ledger row.**
6. **Never relay a denied action to another agent.** If an agent reports a permission denial, surface it to the user.

## Records

- **Decision log:** numbered entries: what was decided, why, alternatives, follow-ups.
- **Effort ledger:** one row per work item: model, planned estimate, wall clock, check wall, tokens, outcome, key numbers. Schedule a measurement run when per-item notes are the only record of cost.
- **Calibrated forecasts:** never sum design-table estimates into a forecast unscaled. Scale them by the measured actual/estimate ratio (recompute every ~15 finished steps), then add review rounds, batch merges and their fallout, and scope that moves out of a step; calendar time is set by those and by serialized files, not step length.
- **Periodic audit:** a read-only review of structure and quality after each landed batch or every few hours. Route each finding to the item that owns the code.
- **Design alignment:** periodically, and before a phase adds a new kind of instance, compare each design's promises (interfaces, per-instance cost claims, stated generality) with the implementation. Give each mismatch one verdict: implementation drift (fix the code), a design gap the implementation exposed (revise the design, with review), both wrong (a design item), or a deliberate deferral (owner and removal plan). Reviews of a sub-design check it against its parent design's cost promises and walk one operation of every instance kind, deferred ones included, through the new interface.
- **Private operational detail** (credentials, cluster paths, job scripts) stays out of the project repo and out of briefs that commit.

## Recovering from a restart

- Stopped agents cannot be resumed. Inspect each branch and worktree: pushed commits, uncommitted edits, stray files.
- Start a fresh continuation agent on the same model. Its brief says exactly what is pushed, to verify-or-revert uncommitted edits, and that in-flight external runs are gone.
- Re-arm the loop.

## Failure patterns

| Pattern | Response |
|---|---|
| A feature was added by patching each layer that assumed the old single case (one new case at many dispatch sites, lemmas duplicated under a new key, the same assumption restated in several layers), so every track hit a fresh design stop and nothing ran end to end | At each handoff count the sites and layers one feature touched; past about three, stop patching and dispatch a short design item that names the missing abstraction, its interface and the migration; brief agents to report such triggers instead of patching |
| A design passed soundness and fit review at the wrong abstraction level (byte-level, value-free permissions where logical, value-carrying ones prove the same guarantees with local reasoning), because reviews never asked whether another level was cheaper to prove and the alternatives section was written after the choice | Every design note scores alternatives at different abstraction levels before choosing; reviews check the alternatives span the space; a periodic read-only design-level review re-asks the question for designs already in flight |
| The orchestrator wrote design decisions and briefs without invoking the project's design guide, so a refactor's sweep covered dispatch code but not specs or contracts, and a single-instance fact surfaced mid-feature in a trusted contract | Invoke the profile's design guide before any design decision or design brief; each decision states its marginal-cost contract; briefs route agents to the guide; the instance-fact table searches specs and contracts, not the feature's name |
| A generalization kept the old form beside the new one because removing it destabilized a proof | Not accepted: fix the proof (opaque spec, lemma split) or record why in a finding with a removal item |
| An agent handed off early because the next step was bigger than planned | Briefs say a larger step is not a reason to hand off: commit what passes and continue; restart the remainder rather than accepting the partial |
| A cross-cutting interface change looked local but broke consumers several layers up | Before deciding, have an agent list every consumer of the facts being changed (15 min); decide after |
| A claim in a brief was wrong (a fact assumed to follow from a check that did not state it) | Grep the definition before asserting a fact in a brief |
| Generalizing from one instance to N surfaced the same gap one handoff at a time | Sweep every assumption restricted to the one-instance case up front and plan them as one item |
| Parallel check jobs and accumulated worktrees and build state filled a shared disk | Briefs cap parallel jobs and require cleanup of what they create; check free space before parallel runs; prune finished items' build state at acceptance |
| An assumption was reported as "false only in narrow cases" when it is false in general | Check an assumption against the concrete case before describing it to the user |
| Audit structure findings were marked low and routed to no owner, so they stayed open across many audits while the problem grew | Route structure findings to a named consolidation item with its own time box; schedule it before work that would multiply the duplication; audits check whether the previous audit's structure findings landed |
| Backgrounded checks never wake the agent | Foreground rule in every brief; nudge an agent that reports waiting on one |
| Facts true only of today's hardware (lane masking, stream semantics, allocator behavior, vendor tuning variables, a backend-keyed sizing table) sat in neutral layers and one trusted clause, and surfaced only when the user asked | Instance-fact tables include a "true only on today's backend or hardware" row; hardware behavior enters the core only as backend parameters or per-backend obligations with their own evidence; a check refuses backend names in neutral code; backends may declare guarantees in a neutral vocabulary, kept apart from operation contracts so an unused one is inert |
| A running agent goes silent (no pushes, no log writes, no processes) and messages never arrive because it never reaches a tool round | Each tick check activity (log mtimes, processes), not just pushes; after one unanswered nudge and about 10 more minutes, stop it and restart on the same model with the state it left |
| Checks take 30 to 55% of agent time | The three-level check cadence |
| An interface change with consumers elsewhere led agents to re-verify whole crates mid-chunk; a finished agent's check kept running for over an hour on code outside the project | Briefs: consumer-module checks only between edits, whole crates at chunk end; every check scoped to the project's packages; agents stop what they started; each tick looks for orphaned processes and containers |
| A parallelism cap set when the host was busy stayed in briefs after it went idle, so a full check suite ran several times slower than needed | Size check parallelism to current host load in each brief; when a single agent runs, message it to raise parallelism |
| A check passed because of a stub or shortcut, not the real behavior | Audits look for it; briefs forbid it |
| Work depended on an input nothing provided | Reachability check at every handoff; an end-to-end test |
| A test expected to fail passed for the wrong reason (timeout, build error) | The test runner requires the intended failure kind |
| Performance or cost chasing oscillated from noise | Fixed target below the limit, measure max over seeds, park after two chunks |
| Merge conflicts on shared registries | Per-item files and derived tables |
| Agents hand off early with scope left, judging the next multi-hour statement "does not fit" (four times in a row on one track, despite a "use the full box" line) | Pre-cut multi-hour items: the brief requires a committed sub-step plan (steps of at most ~30 min, each verifying) within 15 minutes, then execution step by step |
| One agent was briefed with several plan steps under one time box and compacted repeatedly mid-task | Scope each agent to one plan step or fix cluster (about 1 to 1.5 h of planned work); the brief names the hand-off point, and the time box is only a backstop |
| A slow check (27 min CI step) was accepted for a whole session, and its timeout raised instead of fixed | Treat any check over 10 min (ideally 5) as a defect: localize, group, cache or shard it; a timeout raise is only a stopgap |
| An item planned as small keeps uncovering interface gaps | Report time left, not percent; start disjoint downstream prep early |
| The plan kept its original shape after results changed what was needed: separate gates for batches one gate could cover, items that became cleanup rather than correctness, a planned step another result made unnecessary; the user had to ask for simplification | A simplify step every tick; when asked how to finish, propose the smallest path first |
| A steering message sent to an agent that had already handed off resumed it; it kept committing while its worktree was being cleaned up | Never message a finished agent; route follow-ups to a new item. Clean up a worktree only after the final completion notification |
| Chunks keep building supporting pieces and deferring the integration they serve | By the second or third chunk, require the end-to-end skeleton first, with every gap made explicit and named at an interface (an error path, a constructor parameter, a caller's responsibility) |
| A new device path was built and tested on a host stand-in (CPU interpreter, `--device cpu`, type-check only) and first ran on hardware at the final gate; each device-only gap (missing producer, a pass the stand-in skips, a startup check never run on host, memory sizing, precision) then cost one fix plus one gate, serially | When a device path merges, run a hardware smoke test of it at once. Host tests must run every pass the device path runs, or name the ones they skip. Build diagnostics (refusal causes, data dumps, stage-wise reference comparison) before the first hardware run. When failures repeat, hold one hardware lease for one interactive debug agent instead of one gate per fix |
| A cost or size metric (proof solver budget, build time, function size) kept crossing its limit and each handoff fixed its function locally, so a structural cause recurring across items (one function enumerating every feature, one predicate every caller unfolds) surfaced only when the user asked | At each handoff that fixes a metric, ask whether the cause is structural: compare with earlier findings, and check whether the cost grows with each added feature. A cause seen twice becomes a design item |
| A check broke on the integration branch and several running agents each fixed it separately on their own bases, producing conflicting fixes | When the integration head fails a check, fix it once on the integration branch (one small item) and message running agents to merge that fix instead of fixing it themselves |

## Profile contents

A profile answers, briefly:
- **Checks:** the fast, full and CI check commands; which run per commit, per chunk, per batch; time limits and how to split slow suites.
- **Guardrails:** what must not grow (e.g. unchecked code, dependencies, API surface) and what counts as a weakened result; what must never change without the user.
- **Additional handoff checks** specific to the project's kind of work.
- **Branches:** integration branch, merge style, what needs the user's go.
- **Gates:** expensive or hardware gates, when they run, how resources are held.
- **Records:** paths of the decision log, ledger, audits; memory entries to link.
- **Names:** reserved terms and naming rules.
- **Stop points and constraints** the user has set for this project.
- **Project-specific failure patterns,** if any.
