# Profile template

A profile answers, briefly. Ask the user for what you cannot derive from the project's instructions file and agent memory; link those rather than copying them. Keep only what is specific to this user's setup: a rule every contributor should follow belongs in the project's docs.

- **Checks:** the fast, full and CI check commands; which run per commit, per chunk, per batch; time limits and how to split slow suites.
- **Guardrails:** what must not grow (unchecked code, dependencies, API surface) and what counts as a weakened result; what must never change without the user.
- **Design effort:** whether the effort designs or migrates software, so [design-efforts.md](design-efforts.md) applies.
- **Design guide:** the document or skill agents read before adding a feature or changing an interface.
- **Additional handoff and review checks** specific to the project's kind of work.
- **Branches:** integration branch, merge style, what needs the user's go.
- **Gates:** expensive or hardware gates, when they run, how resources are held.
- **Records:** paths of the decision log, ledger, audits; memory entries to link.
- **Names:** reserved terms and naming rules.
- **Stop points and constraints** the user has set for this project.
- **Project-specific failure patterns,** if any.
