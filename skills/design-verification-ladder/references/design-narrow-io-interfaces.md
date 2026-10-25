# Narrow I/O interfaces and honest fakes

**What.** Every external system sits behind a small interface that exposes only the operations the code uses. One fake per interface is shared by every test, and a contract test suite keeps it honest against the real system.

**Enables.**
- Hermetic integration tests.
- Deterministic simulation: the fake runs on the simulated clock and network.
- Fault seams (see design-fault-seams.md).

**How.**
- Define the interface by what the caller needs (`ObjectStore{get, put_if_absent, list(prefix)}`), not by the vendor SDK's surface.
- Write the fake to match the real semantics that matter: errors, ordering, consistency and limits. A fake that is more forgiving than reality hides bugs.
- Run one contract suite against both the fake and the real system, in CI or on a schedule. When the real one changes behavior, the contract test fails first.

**Anti-patterns.**
- Passing the vendor client through the codebase.
- Mocks per test that assert call sequences, not outcomes.
- A fake that never fails, never reorders and never times out.

**Review check.** Is there exactly one fake per boundary, and does a contract test run it against the real implementation?
