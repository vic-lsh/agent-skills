---
name: validation-ladder
description: Choose how to validate a change by climbing a ladder of checks from cheap to expensive, using the project's own concrete ladder or building one when it has none. Use when planning validation for a change, deciding whether a change is ready for an expensive or live run, writing a brief that must state its validation, noticing a feedback loop is too slow, or analyzing a bug that escaped to a costly stage.
---

# Validation ladder

Each check costs more than the one below it and sees risks the cheaper ones cannot. Clear the cheap checks first, and climb only as far as the change's risk requires.

## Find the project's ladder

1. Look for the project's own ladder: a testing guide, contributor docs or a project skill that lists its checks with commands and costs. Use it; do not restate it.
2. If there is none, build one from [references/example-ladder.md](references/example-ladder.md): keep only the levels the project actually has, give each a real command and a measured cost, and propose adding it to the project's docs through its normal change process.

## Rules

1. **Climb only from green.** Run a level only after every cheaper level that applies passes. A cheap failure found late wastes the expensive run.
2. **Risk sets the minimum level.** Before an expensive run, a change must clear the level that can actually show its risk:
   - concurrency, restarts or failure handling: deterministic simulation or seeded fault injection;
   - credentials or secrets: property tests with canaries in every excluded field, plus an independent read-only review;
   - classification, trust or scoring logic: regression fixtures plus replay of real past data;
   - platform wiring (images, permissions, mounts, config): a scripted end-to-end run on a real, disposable environment;
   - prompts or model behavior: only replay and live runs show anything, so keep each such change small and isolated.
3. **Push escaped bugs down.** When a level finds a bug, add a regression at the lowest level that reproduces it, then fix the scenario that let the cheaper level miss it.
4. **Record where each bug was caught.** If expensive levels keep finding cheap-level bugs, make the lower levels more representative rather than running the expensive ones more often.
5. **Keep each level at its cost.** Know each level's expected wall-clock time. When a level runs well past it, stop and fix the loop: remove the slow step, reuse a warm environment, and add a guard so the slow path cannot return.

## Expensive runs need approval

Runs that spend real money, quota or shared resources need the user's approval. If the project's own ladder or experiment docs define an approval policy and where to save it, follow those instead of the steps below.

1. The first time in a project, ask which expensive runs are pre-approved, before one is near. Recommend: the smallest live smoke on the cheapest approved model is pre-approved; each full experiment is approved separately.
2. Save the answer in `~/.agent-state/validation-ladder/<project>.md` and reuse it. Update it as soon as the user changes it.
3. A run outside the saved preference waits for explicit approval. Keep running the cheaper levels meanwhile.

## In a brief

State the change's risk classes, the levels required before handoff, and which level gates the next expensive run. A handoff that skips a required level is not done.
