# Example ladder

A starting point for a project that has no ladder. Keep only the levels the project has, replace each cost with a measured one, and add the project's real command for each.

| # | Level | Typical cost | Catches | Misses |
|---|---|---|---|---|
| 0 | Format, lint, types, import and boundary checks | seconds | Typos, missing imports, forbidden dependencies | Behavior |
| 1 | Unit and contract tests, written to fail first | seconds | Logic errors at an interface | Cases nobody wrote |
| 2 | Regression fixtures reduced from real incidents | seconds | Recurrence of known bugs | New bugs |
| 3 | Property and fuzz tests, time-capped | minutes | Edge cases in parsers, projections, classifiers | Timing and state |
| 4 | Deterministic simulation: seeded schedules, fault injection, virtual clock, replay by seed | minutes | Interleavings, restarts, partial failures | Real inputs, model behavior |
| 5 | Hermetic integration with in-process fakes | about a minute | Wiring between components | Real platform semantics |
| 6 | Scripted end-to-end on a real, disposable environment, no model calls | minutes | Real platform, images, permissions, mounts | Scenarios it does not exercise |
| 7 | Offline replay of archived real runs | minutes | How new logic would have handled real past data | The new agent's own behavior |
| 8 | Independent adversarial review, read-only | 30-60 min | Design and security holes no test targets | What the reviewer does not think of |
| 9 | Smallest live smoke | tens of minutes plus model cost | Prompt and agent behavior, quotas, live plumbing | Effects that build up over many runs |
| 10 | Full live experiment | hours plus model cost | Cumulative effects, cost comparisons | — |

Shapes by kind of project:

- **Library:** levels 0-3, plus benchmarks if performance matters.
- **Web service:** 0-3, 5, a browser or API end-to-end suite as 6, and a staging deploy as 9.
- **Distributed or infrastructure system:** most levels; 4 and 6 matter most.
- **ML training:** 0-1, then overfit one small batch, then a short run at a small fraction of scale, before a full run.
- **LLM agent system:** 0-2, 5-7, then 9 before 10; prompt changes are only visible at 7, 9 and 10.
