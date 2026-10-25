# Idempotent, restartable operations

**What.** Any operation can be retried safely, and a process can crash at any point and resume from durable state without loss or duplication.

**Enables.**
- Crash-point tests and simulation with restarts.
- Safe retries under fault injection.
- At-least-once delivery without double effects.

**How.**
- Give each operation a stable ID. The receiver records the IDs it has applied and ignores repeats.
- Write intent before acting and completion after. On restart, finish or roll back every intent that has no completion.
- Prefer conditional writes (compare-and-set, `put_if_absent`) over read-then-write.
- Make startup the same code path as recovery. There is no separate "clean start".

**Test.** For each crash point, crash there, restart, and check the invariants plus "every effect happened exactly once".

**Anti-patterns.**
- In-memory progress counters.
- Side effects before the durable record.
- Recovery code that only runs after real outages.

**Review check.** What happens if the process dies on each line that has an external effect?
