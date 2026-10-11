# Failure patterns

Read at each handoff and when planning a phase. Each line is a mistake that happened in a past effort, followed by the response. Patterns already enforced by a rule in `SKILL.md`, [briefs.md](briefs.md), [integration.md](integration.md) or [reviews.md](reviews.md) are not repeated here.

## Handoff checks

Check at every handoff, at minimum: the design checks the brief required are present, with no unresolved "no" row and no old form kept beside its general form; the change is systematic (more than ~3 sites or several layers for one feature is a structure finding that gets a design item); nothing passes because of a stub, mock or shortcut; every new input has something that provides it; nothing the profile tracks grew or weakened unplanned; "done" with a dependency only named is partial; a fix to a cost or size metric gets the structural-cause question under Metrics and targets below.

## Design and structure

- **A feature added by patching every layer that assumed the old single case** (one new case at many dispatch sites, duplicated logic under a new key, the same assumption restated in several layers), so every track hit a fresh design stop and nothing ran end to end. → Count sites and layers per feature at each handoff; past about three, stop patching and dispatch a short design item naming the missing abstraction, its interface and the migration. Brief agents to report such triggers instead of patching.
- **Going from one instance to N surfaced the same gap one handoff at a time.** → Sweep every assumption restricted to the one-instance case up front and plan them as one item.
- **A design passed review at the wrong abstraction level** because no one asked whether another level was cheaper, and its alternatives section was written after the choice. → Alternatives are scored before choosing; reviews check they span different levels.
- **The orchestrator made design decisions and wrote briefs without the project's design guide,** so a refactor's sweep covered dispatch code but missed specs and contracts. → Read the profile's design guide before any design decision or design brief; each decision states how its cost grows per new feature; the instance-fact table searches specs and contracts, not only code that names the feature.
- **A generalization kept the old form beside the new one** because removing it was hard. → Not accepted: fix the cause, or record why in a finding with a removal item.
- **Facts true only of today's hardware or backend sat in neutral layers** and surfaced only when the user asked. → Hardware behavior enters the core only as backend parameters or per-backend obligations with their own evidence; a check refuses backend names in neutral code. Backends may declare guarantees in a neutral vocabulary kept apart from operation contracts, so an unused one is inert.
- **A cross-cutting interface change looked local but broke consumers several layers up.** → Before deciding, have an agent list every consumer of what is changing (about 15 minutes).

## Checks and tests

- **A check passed because of a stub or shortcut, not the real behavior.** → Briefs forbid it; reviews and handoffs look for it.
- **A test expected to fail passed for the wrong reason** (a timeout, a build error). → The test runner requires the intended failure kind.
- **A parallelism cap set while the host was busy stayed in briefs after it went idle,** making a full check several times slower. → Size parallelism in each brief to current load; when one agent runs alone, tell it to raise parallelism.

- **The top of a PR stack conflicted after its parents were squash-merged by the queue,** so it was ejected even though the stack was enqueued as one unit. → After any parent of a stack lands, sync the remaining PRs with main before (re-)enqueueing them, and check the queue each tick.

## Steering

- **The plan kept its original shape after results changed what was needed,** and the user had to ask for simplification. → When asked how to finish, propose the smallest path first.
- **A steering message to an agent that had already handed off resumed it,** and it kept committing while its worktree was being cleaned up. → Route follow-ups to a new item; clean up a worktree only after the final completion notification.

## Metrics and targets

- Chasing a number oscillates on noise: set a fixed target below the limit, measure the maximum over several seeds, and park after two chunks.
- When a cost or size metric keeps crossing its limit and each handoff fixes it locally, ask whether the cause is structural (does the cost grow with each added feature?); a cause seen twice becomes a design item.
- Treat any check over 10 minutes (ideally 5) as a defect to localize, group, cache or shard; raising a timeout is only a stopgap.
