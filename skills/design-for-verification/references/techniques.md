# Verification techniques

Each entry: what it is, what the code must provide, and the usual pitfall.

## Static checks and types
Encode invariants in types: distinct types for distinct IDs and units, enums instead of strings, constructors that validate. Lint for forbidden dependencies across module boundaries. Pitfall: escape hatches (`any`, casts, raw maps) quietly undo it.

## Assertions and invariants
Write the invariant once as a function; call it in debug builds, in tests after every step, and in simulation after every event. Pitfall: assertions that log and continue hide the first failure.

## Unit tests and regression fixtures
Write the test before the fix and watch it fail. Reduce every real failure to the smallest input that still fails, and keep it as a fixture. Test contracts, not private details. Pitfall: tests that pass with the fix reverted.

## Property-based and model-based testing
State properties that hold for all inputs: round trips, idempotence, commutativity, "never loses data". For stateful code, run random operation sequences against a simple reference model and compare after each step. Needs: pure or resettable state and a way to build arbitrary valid inputs. Pitfall: generators that only produce easy inputs; check coverage. Cap run time.

## Fuzzing and differential testing
Coverage-guided fuzzing for anything that parses untrusted or complex input. Differential testing runs two implementations (old and new, fast and simple) on the same inputs and diffs the outputs. Needs: an entry point that takes bytes and has no side effects. Keep the corpus and add crashers as fixtures. Pitfall: unbounded runs; cap them.

## Deterministic simulation testing (DST)
Run the whole system in one process under a seeded scheduler with a simulated clock, network and disk. Inject faults: drops, reorders, delays, crashes, restarts, disk errors. Check invariants after every event. Any failure replays exactly from its seed. Swarm testing (randomly turning fault types on and off per seed) finds more bugs than all faults at once. Needs: every source of nondeterminism injected, and no real threads, sockets or wall-clock calls in the core. This is the main reason to design for determinism. Pitfall: one hidden real-time call or unordered map iteration breaks reproducibility; detect it by running each seed twice and comparing traces.

## Model checking and formal specs
Specify the protocol (leader election, commit, lease, retry) in TLA+, P or Alloy and check it exhaustively on small configurations. Most design bugs show up with 2-3 nodes. Keep the spec next to the code and update it with protocol changes. Pitfall: a spec that drifts from the implementation; link them with shared invariants checked in DST.

## Hermetic integration and honest fakes
Wire real components together with in-process fakes for external services. Run one contract test suite against both the fake and the real service, so the fake stays honest. Pitfall: each test writing its own ad-hoc fake.

## Scripted end-to-end and chaos
Run on a real but disposable environment with scripted inputs and no expensive dependencies (for example, no model calls). Inject real faults: kill processes, cut networks, fill disks. Reuse a warm environment between runs. Pitfall: rebuilding the environment every run until nobody runs it.

## Replay and shadow traffic
Record real inputs and responses at the boundaries, then rerun new logic on them offline and diff decisions. Shadow traffic sends live inputs to the new version without acting on its outputs. Needs: boundary recording designed in from the start. Pitfall: recordings that omit a field the decision depends on.

## Live runs
Smallest live smoke first, then the full run or a canary. Measure what only live conditions show. Every live failure that a smaller level could have shown is a gap to close there.

## Mutation testing
Change the code in small ways (flip a condition, drop a call) and check that some test fails. Surviving mutants mark untested behavior. Use it on critical modules, not everywhere.
