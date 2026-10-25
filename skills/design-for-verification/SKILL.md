---
name: design-for-verification
description: Shape a codebase so its correctness can be checked cheaply and at scale (deterministic core, injected nondeterminism, narrow I/O seams, explicit state, recorded boundaries), and verify it by climbing from small, fast techniques (types, assertions, unit and property tests, fuzzing) to large ones (deterministic simulation, model checking, end-to-end, replay, live runs). Use when designing a component or interface, planning how a change will be verified, deciding whether a change is ready for an expensive run, writing a brief that must state its verification, or analyzing a bug that escaped to a costly stage.
---

# Design for verification

Correctness comes from design, not from testing afterwards. Code built to be checked can be verified in seconds by machines; code that is not can only be watched in production. Design for verification from the first line.

**Do not take the shortcut.** Skipping injectable seams or a deterministic core feels faster today, but every later bug then costs a slow, flaky, expensive run to find, and retrofitting the seams costs more than building them. The investment pays for itself many times over a project's life.

## Design for verification

Before writing a component, decide how each level below will check it, and build the seams those levels need. Read the technique's reference when applying or reviewing it:

1. **Deterministic core, thin shell.** Put decisions in pure functions of their inputs; keep I/O in a thin outer layer. See [design-deterministic-core.md](references/design-deterministic-core.md).
2. **Inject every source of nondeterminism:** clock, timers, randomness, IDs, scheduling, network, disk, environment. One seed must reproduce a whole run. See [design-injected-nondeterminism.md](references/design-injected-nondeterminism.md).
3. **Narrow I/O interfaces** so a fake or simulator slots in. Keep one fake per boundary, shared by all tests, and check it against the real thing with contract tests. See [design-narrow-io-interfaces.md](references/design-narrow-io-interfaces.md).
4. **Explicit state.** Model lifecycles as state machines with serializable state, and write invariants as functions a test can call at any step. See [design-explicit-state.md](references/design-explicit-state.md).
5. **Fault seams at every external call,** so tests can inject errors, delays, partial writes and crashes. See [design-fault-seams.md](references/design-fault-seams.md).
6. **Idempotent, restartable operations.** A crash at any point is a test case, not an outage. See [design-idempotent-restartable.md](references/design-idempotent-restartable.md).
7. **Record at boundaries.** Capture inputs and responses so any real run can be replayed offline. See [design-boundary-recording.md](references/design-boundary-recording.md).
8. **Observable decisions.** Every decision, including a skip or no-op, returns or records its reason. See [design-observable-decisions.md](references/design-observable-decisions.md).
9. **Scalable time.** Timeouts and intervals are configurable, so tests run in seconds. See [design-scalable-time.md](references/design-scalable-time.md).

A design review checks these. A component without them is not done, even if it works.

## The ladder

Climb from small to large; each level sees what the cheaper ones cannot. Details, tools and pitfalls for each are in [references/techniques.md](references/techniques.md).

| Scale | Techniques | Shows |
|---|---|---|
| Static | Types that make illegal states unrepresentable, lint, boundary checks | Whole bug classes, before running |
| In code | Assertions, invariants, contracts | Violations at the moment they happen |
| Unit | Example tests written to fail first; regression fixtures from real bugs | Logic at an interface; known bugs stay fixed |
| Generated inputs | Property-based and stateful model-based tests; coverage-guided fuzzing; differential testing against a reference | Edge cases nobody thought to write |
| Whole system, simulated | Deterministic simulation testing (DST): one process, seeded scheduler, simulated clock, network and disk, fault injection, replay by seed | Interleavings, crashes, partial failures, reproducibly |
| Design | Model checking or a formal spec of the protocol (TLA+, P, Alloy) | Design flaws no implementation test reaches |
| Integration | Hermetic integration with honest fakes; scripted end-to-end on a real, disposable environment; chaos injection | Real platform behavior and wiring |
| Real data | Replay of recorded real runs; shadow traffic | How new logic handles real inputs |
| Live | Smallest live smoke, then full runs or canaries | Behavior only real conditions show |

Check the tests themselves with mutation testing when their strength matters.

## Rules

1. **Climb only from green.** A cheap failure found late wastes the expensive run.
2. **Risk sets the minimum level:**
   - concurrency, restarts, failure handling: DST or seeded fault injection;
   - protocols and distributed agreement: model checking plus DST;
   - parsers, decoders, serializers: fuzzing and round-trip properties;
   - credentials or secrets: property tests with canaries in every excluded field, plus an independent review;
   - classification or scoring: regression fixtures plus replay of real data;
   - platform wiring: scripted end-to-end;
   - prompts or model behavior: replay and live runs only, so keep each change small.
3. **Push escaped bugs down.** Add a regression at the lowest level that reproduces the bug, then fix the gap that let it pass there. If a program could catch the whole bug class, or the check is reusable verification infrastructure (a fuzz harness, a simulator), build it with skill `codify`.
4. **Record where bugs are caught.** If large levels keep catching small-level bugs, invest in the small levels.
5. **Keep each level fast.** Know each level's expected time; when one runs well past it, fix the loop and guard against the slow path returning.
6. **Use the project's ladder.** If the project documents concrete commands per level, use them; if not, propose one built from this table.

## In a brief

State the change's risk classes, the seams the design provides, the levels required before handoff, and which level gates the next expensive run. A handoff that skips a required level is not done.
