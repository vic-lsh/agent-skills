# Reviews and forecasts

## When to review

Trigger reviews by events, not by the clock:

- **Before implementation:** an adversarial read-only review of every design note or spec, with fixes integrated before the first implementation chunk. This is where most review value comes from.
- **Before a new feature family:** an architecture pass on the single-instance assumptions that family will hit, each priced now versus later.
- **Sweep:** every 3 to 4 merges into the integration branch, covering everything changed since the last sweep across all PRs. It reports only findings that would change a decision; the rest go in an appendix.
- **Vision review:** at every merge batch, compare the whole current design and code to the project's vision document, not to recent changes. Each gap gets one verdict: planned (item and phase), accepted limit (recorded load-bearing reason) or problem (no planned change), which becomes a design item at once. Reviews scoped to one diff or note miss structural gaps that no single change introduced.

Every review, of any kind, also looks for anti-patterns in how the verification is built: anything that makes proofs costlier to change, slower to check, duplicated, coupled across modules, or weaker than they appear. Known examples are a starting point, not the list: closed sets matched across modules where plugins add cases, one argument re-proved per instance, large invariants revealed whole. The profile points to the project's guide. A reviewer reports any new pattern it sees and proposes adding it to the guide. A pattern seen in two items is a design item, not a cleanup.

Route review findings into the next brief of the owning item, never into a running chunk.

## Sweep checklist

The sweep checks:

- the previous review's findings landed, structure findings above all;
- guards that trust caller-supplied fields instead of established facts; success reported without verifying the effect;
- crash and replay at every effect boundary: duplicate effects, false success, permanent failure where "unknown" is right; states that get stuck or are never retried;
- identity keys that are partial or mix namespaces;
- tests that cannot fail: stubs, state surgery, seeded state, private internals, no real restart; Fakes that diverge from production;
- duplicated mechanisms and layering violations;
- gaps across PRs: contracts or producers named in handoffs that no item owns;
- the profile's project-specific review items.

Design efforts add the class-removal proposals and design alignment in [design-efforts.md](design-efforts.md).

Route each finding to the item that owns the code. Structure findings go to a named consolidation item with its own time box, scheduled before work that would multiply the problem; never mark them low and leave them unowned.

## Forecasts

Never sum design-table estimates unscaled. Scale them by the measured actual-to-estimate ratio (recompute every ~15 finished steps), then add review rounds, batch merges and their fallout, and scope that moves out of a step. Calendar time is set by those and by serialized files, not step length. Schedule a measurement run when per-item notes are the only record of cost.
