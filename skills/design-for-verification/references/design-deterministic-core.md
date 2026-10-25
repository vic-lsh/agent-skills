# Deterministic core, thin shell

**What.** Put every decision in pure functions: same inputs, same outputs, no I/O. A thin outer shell does the I/O. It gathers inputs, calls the core, and carries out the returned effects.

**Enables.**
- Unit, property and model-based tests on the core, with no fakes.
- Deterministic simulation, where the shell is swapped for a simulator.
- Replay, which feeds recorded inputs to the core.

**How.**
- Have the core return effects as data (`[Send(to, msg), Write(key, val), Sleep(5s)]`) instead of performing them. The shell executes them.
- Pass in everything the core reads: current time, config, observed state.
- Keep the shell boring: no branching beyond "execute these effects and report the results back".

```
decide(state, event, now) -> (new_state, effects)   # pure
loop: event = shell.next(); (state, fx) = decide(state, event, clock.now()); shell.run(fx)
```

**Anti-patterns.**
- A core function that "just logs" or "just reads one config value" from a global.
- Decisions buried in the shell's error handling.
- Effects done halfway inside the core.

**Review check.** Can every decision function be called in a test with plain values, with no setup of real or fake I/O?
