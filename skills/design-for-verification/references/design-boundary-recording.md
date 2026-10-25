# Record at boundaries

**What.** Capture every input and every external response at the system's boundaries, in a stable format, so any real run can be replayed offline through new code.

**Enables.**
- Replay of real runs.
- Regression fixtures made from real failures.
- Differential testing of old versus new logic on real data.
- Debugging without touching production.

**How.**
- Record at the same narrow interfaces used for fakes. A replay is then just another fake that serves recorded responses.
- Record everything a decision reads, including time and randomness seeds. A missing field makes the replay diverge.
- Version the format, and keep a loader test for old recordings.
- Strip or replace secrets at record time with typed placeholders. Never store them.

**Anti-patterns.**
- Logs written for humans used as the only record.
- Recording outputs but not the inputs that caused them.
- Formats that change without a version.

**Review check.** Pick a recent real run: can you replay one decision from it offline and get the same result?
