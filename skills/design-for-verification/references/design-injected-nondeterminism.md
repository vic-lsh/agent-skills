# Inject every source of nondeterminism

**What.** The clock, timers, randomness, ID generation, scheduling and iteration order come from interfaces passed in, never from globals. So do network, disk and environment access. One seed reproduces a whole run.

**Enables.**
- Deterministic simulation: a failing seed replays exactly.
- Stable property tests.
- Time-travel tests: "advance 30 minutes" takes no real time.

**How.**
- Interfaces: `Clock{now, sleep, after}`, `Rand{seeded}`, `IDs{next}`, `Scheduler{spawn, yield}`. Production passes real implementations; tests pass seeded or simulated ones.
- Derive every random stream from one root seed, and log the seed on every run.
- Iterate maps in a sorted or insertion order wherever order can affect behavior.
- Do concurrency through the injected scheduler, or keep it out of the core entirely.

**Anti-patterns.**
- `time.Now()`, `random()`, `uuid4()` or `os.getenv()` deep in logic.
- Real goroutines or threads inside the core.
- Hash-map iteration order leaking into outputs.
- Sleeping for real in tests.

**Detect leaks.** Run each simulation seed twice and diff the full event traces. Any difference means some nondeterminism is not injected.

**Review check.** Grep the core for direct clock, random, ID, environment and thread calls. There should be none.
