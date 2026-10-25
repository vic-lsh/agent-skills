# Explicit state and checkable invariants

**What.** Model lifecycles as explicit state machines with named states, allowed transitions and serializable state. Write invariants as functions that take the state and return the violations.

**Enables.**
- Model-based testing: compare against a simple reference machine.
- Simulation that checks invariants after every event.
- Model checking: the spec mirrors the machine.
- Crash tests that save and restore state at any point.

**How.**
- Make the state one value, not fields spread across objects.
- Have the transition function reject illegal transitions loudly, as an error rather than a no-op.
- Write `check_invariants(state) -> [violation]`. Call it in tests after every step, in simulation after every event, and in debug builds.
- Make the state serializable, so tests can snapshot it, restart from it and diff two runs.

**Anti-patterns.**
- State implied by a mix of flags (`started && !done && retries > 0`).
- Transitions scattered across callbacks.
- Invariants that live only in comments.

**Review check.** Can you list every state and transition from the code alone, and is there a callable invariant check?
