# Reviews, design alignment and forecasts

## Periodic review

One read-only review agent every ~2 hours of agent work or every 3 to 4 landed PRs, covering everything changed since the last review across all PRs, not one review per PR. It checks:

- the previous review's findings landed, structure findings above all;
- guards that trust caller-supplied fields instead of established facts; success reported without verifying the effect;
- crash and replay at every effect boundary: duplicate effects, false success, permanent failure where "unknown" is right; states that get stuck or are never retried;
- identity keys that are partial or mix namespaces;
- tests that cannot fail: stubs, state surgery, seeded state, private internals, no real restart; Fakes that diverge from production;
- duplicated mechanisms and layering violations;
- gaps across PRs: contracts or producers named in handoffs that no item owns;
- the profile's project-specific review items.

Beyond findings, each review proposes changes that make a whole class of error impossible or trivial to test: types that cannot represent the bad state, one shared mechanism instead of per-module copies, constructors that require evidence, generic harnesses every new component gets for free (crash at every boundary, reload every step, shared contract suites for Fakes and production). Each proposal names the error class, the findings it would have prevented, and its cost.

Route each finding to the item that owns the code. Structure findings go to a named consolidation item with its own time box, scheduled before work that would multiply the problem; never mark them low and leave them unowned.

## Design alignment

Periodically, and before a phase adds a new kind of instance, compare each design's promises (interfaces, per-instance cost claims, stated generality) with the implementation. Give each mismatch one verdict: implementation drift (fix the code), a design gap the implementation exposed (revise the design, with review), both wrong (a design item), or a deliberate deferral (owner and removal plan). Reviews of a sub-design check it against its parent design's cost promises and walk one operation of every instance kind, deferred ones included, through the new interface. A periodic design-level review re-asks, for designs in flight, whether another abstraction level would be cheaper.

## Forecasts

Never sum design-table estimates unscaled. Scale them by the measured actual-to-estimate ratio (recompute every ~15 finished steps), then add review rounds, batch merges and their fallout, and scope that moves out of a step. Calendar time is set by those and by serialized files, not step length. Schedule a measurement run when per-item notes are the only record of cost.
