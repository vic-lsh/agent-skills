# Scalable time

**What.** Make every timeout, interval, backoff and settle window configurable. Derive them from one time-scale factor where possible, so tests and smoke runs finish in seconds instead of minutes.

**Enables.**
- Fast end-to-end and integration runs.
- Simulation, where time is virtual anyway.
- Cheap smoke tests on real environments.

**How.**
- Read every duration from config. None are hard-coded.
- Apply one scale factor, so tests change one number.
- Write waits as conditions with a deadline ("wait until healthy, at most T"), never as fixed sleeps.
- Note which checks a short scale weakens (for example, a shorter verification window), and keep full scale for measured runs.

**Anti-patterns.**
- `sleep(300)` in a test path.
- Durations duplicated as constants across modules.
- Waits that cannot end early once the condition holds.

**Review check.** Can a full end-to-end scenario run at a tenth of real time by changing one setting?
