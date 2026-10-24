# Fault seams at every external call

**What.** Every call that crosses a boundary (network, disk, subprocess, another service) goes through a point where a test can inject failure: an error, a timeout, a delay, a partial result, a duplicate or a crash.

**Enables.**
- Fault injection in unit tests and deterministic simulation.
- Chaos tests end to end.
- Proof that every error path runs at least once.

**How.**
- Route calls through the narrow interfaces (design-narrow-io-interfaces.md), and give the fake a fault plan: `fail the 3rd put`, `delay all gets 2s`, `crash after write before ack`.
- Inject crashes at named points (`crashpoint("after-commit")`). These are no-ops in production; the simulator can stop there.
- Return errors as values the caller must handle. Do not let them escape as panics.
- In simulation, pick faults randomly per seed. Swarm testing (turning fault kinds on and off per seed) finds more bugs.

**Anti-patterns.**
- Error handling that was never executed.
- Retries tested only with "always succeeds".
- Catch-all handlers that log and continue.

**Review check.** For each external call: which test makes it fail, and what does the system do then?
