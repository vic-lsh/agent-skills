# Observable decisions

**What.** Every decision, including skips, no-ops, fallbacks and deferrals, returns or records a reason that a test can assert and a person can read.

**Enables.**
- Tests that assert why something happened, not only what.
- Simulation invariants on decisions.
- Faster diagnosis of live failures.

**How.**
- Return structured results (`Skip{reason: "lease held by B"}`), not booleans.
- Log fallbacks loudly, and record them in the run's results, so a degraded path cannot pass silently.
- Count each decision kind; a test can assert the counts after a simulated run.

**Anti-patterns.**
- An early `return` with no reason.
- Errors swallowed into defaults.
- "Works but slower" fallbacks nobody can see.

**Review check.** For each branch that does nothing, what tells you it was taken, and why?
