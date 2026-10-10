# Integration, batches and expensive runs

## Dividing work

- **Two agents share a module only with a written ownership split,** and only for real critical-path time saved. The later one merges the earlier one's branch as it advances. Move ownership explicitly when routing a fix into someone else's file, and tell both agents.
- **Coupled changes go on one integration branch.** Before dispatching parallel PRs, list each one's write set. Overlap on a module means one integration branch with stacked, separately reviewable commits, the change that alters a shared assumption first. Disjoint PRs stay independent and land as soon as they are green; one big PR for everything is not the answer.
- **Split a shared file by responsibility rather than serialize on it.** A short mechanical split item (one concern per file) usually costs less than the wait. Design notes name each new item's file; briefs put new concerns in new files.
- **Shared registries:** per-item files and derived tables instead of one hand-edited list.

## Batches and merges

- Critical-path items base on their input branches directly, not on the integration branch.
- Batch finished branches. Start a batch merge when a slot is free and the critical path is blocked anyway, not after everything finishes.
- Pipeline: a merge agent runs host CI on a batch branch; a gate agent runs expensive or hardware gates; you merge into the integration branch from a temporary worktree and never touch another agent's checkout.
- When the integration head fails a check, fix it once there as one small item and tell running agents to merge that fix, instead of each fixing it on its own base.
- Trial merges: when merge-only failures (each side passes, the merged tree fails) occur more than about once per 6 to 8 batches, run an hourly trial merge of all in-flight branches with targeted checks. Below that rate it costs more than it saves. Track the rate in the ledger.

## Live and hardware runs

- Keep a live run going whenever resources and a slot allow; live runs find the bugs host tests miss. Build each from the main branch plus the reviewed fix branches it needs, with hashes recorded. Never wait for those fixes to clear a merge queue. Skip a run only when a known bug would crash it within minutes and no fix branch exists.
- For every bug a live run finds, ask which host test should have caught it and add that class of test.
- When a device or hardware path merges, run a hardware smoke test of it at once. Host tests run every pass the device path runs, or name the ones they skip. Build diagnostics (refusal causes, data dumps, stage-wise comparison with a reference) before the first hardware run.
- When hardware failures repeat, hold one hardware lease for one interactive debug agent instead of one gate run per fix.
- Check free disk space before parallel runs, and prune finished items' build state at acceptance.
