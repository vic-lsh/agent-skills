# Writing a brief

Every brief is self-contained; the agent has none of your context. Include:

- **Goal and why:** one or two sentences tying the item to the overarching goal.
- **Setup:** worktree path; a new branch from an explicit base commit, plus branches to merge first; a build cache copied for this agent, never shared with a running one; a log directory inside its worktree.
- **Read-first list:** project instructions, the plan item, prior handoffs and findings, audit findings aimed at this item, and the profile's design guide for any item that adds a feature or changes a spec or interface.
- **Design items:** for a brief that designs or changes an interface, spec or stored format, add the brief items in [design-efforts.md](design-efforts.md).
- **Scope in priority order,** plus an out-of-scope list naming who owns each excluded piece. Excluded dependencies stay named, not assumed away.
- **File ownership** when agents run in parallel: files it owns, files others own, and what it may touch there (usually only mechanical updates, listed in the handoff).
- **Guardrails:** the profile's rules on what must not grow or weaken; no stub, mock or shortcut that makes a check pass without the real behavior; if it would have to weaken a result, stop and report.
- **Bug fixes:** ask for the class, not the instance: name the shared cause, the generator or property that covers the input space, and the sweep for the same flaw; require the new tests to fail at the buggy commit. Listing bugs one by one gets one test per bug.
- **Reachability:** every new input or dependency needs something that provides it: a caller, a config, a test that exercises it end to end.
- **Check cadence:** fast targeted checks while editing and per commit, scoped to consumer modules; the full check once at chunk end; the full CI set only at batch merges. Every check scoped to the project's own packages. Long checks run in the foreground with the maximum tool timeout; backgrounded checks never wake the agent. Size parallelism to current host load; cap parallel jobs and clean up worktrees, build state, processes and containers the agent created.
- **Commits:** small, each passing, pushed immediately; no stash; the attribution trailer on every commit including merges.
- **Scope and time box:** one plan step or fix cluster per agent, about 1 to 1.5 hours of planned work, with the hand-off point named; token budget about 200k for new or exploratory work and 350k to 400k for a continuation chunk on a branch whose state lives in a spec and a handoff document; the time box (45 to 90 minutes, first passing commit within ~30) is only a backstop. Say: "use the full box while scope remains and you are progressing", "a larger next step is not a reason to hand off: commit what passes and continue", and "stop and hand off at the box". For multi-hour items, require a committed sub-step plan (steps of at most ~30 minutes, each verifying) within 15 minutes, then execution step by step.
- **Integration first:** from the second chunk of a track on, require the end-to-end skeleton before more supporting pieces, with every gap named at an interface (an error path, a constructor parameter, a caller's responsibility).
- **Handoff contents:** a handoff document written with the `handoff` skill (path named in the brief), plus the delta on whatever the profile tracks and wall clock from `date`. A continuation brief points to that document as its first read.
- **Waiting on a measurement:** an agent that submits a benchmark or hardware request never waits for it. It continues with the scope that does not depend on the result; when nothing is left, it hands off with the request id and a pre-decided branch in Next ("if the judge passes and tok/s holds, merge; if the judge fails, start from X; if within noise, Y"). The orchestrator fills the slot with independent work and dispatches the continuation when the result lands.
- **Naming rules** from the profile.
- **Facts in the brief:** grep the definition before asserting a fact; check an assumption against the concrete case before calling it narrow.
