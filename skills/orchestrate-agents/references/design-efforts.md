# Design efforts

Read when the effort designs or migrates software: it changes interfaces, specs, stored data or contracts, or the profile marks it as a design effort. Read it when planning a phase, before writing a design brief, at each handoff and review, and when bugs arrive together.

## Bugs that arrive together

When several findings arrive at once (a dogfood round, several red checks, a review), do not route them one per fixer.

1. Group them by mechanism, not by symptom or file. Different-looking bugs often share one cause: one fact held in several copies that drift, state carried across a boundary it should not cross, an effect with no owner, or a request that can be built without what it needs.
2. For each group, ask what change makes the class impossible: one source the others are derived from, a type that cannot represent the bad state, a constructor that requires its inputs, removing the unowned effect.
3. Dispatch that change as one item, with a regression test per symptom. If it is too large for now, land the smallest unblocking fix and schedule the mechanism change as an owned item.
4. Log the cause, the class and the rejected per-bug alternative as a decision.

If the code being patched is about to be replaced, keep the fix to the mechanism and minimal.

## Handoff checks

- The design checks the brief required are present, with no unresolved "no" row and no old form kept beside its general form.
- The change is systematic: more than ~3 sites or several layers for one feature is a structure finding that gets a design item.

## Brief items

- **Design checks for a new instance** (a model, store, optimization, backend or device), written in the first commit's finding as the profile's design guide defines them:
  - a mechanism-reuse table: which existing mechanism does the same job; reuse, generalize, or new with a reason;
  - an instance-fact table: facts in code, specs and contracts true only of today's instances, including today's backend or hardware, each with its general form;
  - a per-pair count: code naming two features at once; target zero, plus one test with every existing feature on.
- **Alternatives considered** for any item that designs or changes an interface or spec: at least three designs that differ in abstraction level or mechanism, scored on one rubric (guarantees identical or disqualified; where facts are established and how cost grows per new feature or instance; trusted surface; expressiveness; migration cost), and why the choice wins. A mechanism already in the design docs is one candidate, not a reason. Prototyping is the agent's call.
- **Future-feature walk:** every plan update and design brief walks the project's catalog of features and optimizations it wants to support (the profile names it): per entry, does the change support it, stay neutral, or add a site a later feature must remove. No expedient form when the general one is buildable now; an interim form only when the general form needs an unbuilt prerequisite, shipped with an owned, scheduled removal item.
- **Design docs with the decision:** a design decision merges with its design-doc update, written as the current design with unbuilt parts in a status table, never deferred to the end of a migration. Search existing design notes for an approved one before briefing a design question.
- **Definition visibility** for items that add or change specs: decide which definitions callers may see the body of (interfaces open, small, stable; representations hidden behind a few exported facts; anything that grows with each feature hidden by default), with a consumer count per definition. A per-function fix for a size or cost budget whose cause is a shared definition's visibility is a structure finding.
- **Ratchets at design time:** a design note or spec lists the items it will add and runs the profile's generality and trust checkers against that plan; the implementing agent runs them again at its first commit, not only at chunk end.

## Failure patterns

- **A feature added by patching every layer that assumed the old single case** (one new case at many dispatch sites, duplicated logic under a new key, the same assumption restated in several layers), so every track hit a fresh design stop and nothing ran end to end. → Count sites and layers per feature at each handoff; past about three, stop patching and dispatch a short design item naming the missing abstraction, its interface and the migration. Brief agents to report such triggers instead of patching.
- **Going from one instance to N surfaced the same gap one handoff at a time.** → Sweep every assumption restricted to the one-instance case up front and plan them as one item.
- **A design passed review at the wrong abstraction level** because no one asked whether another level was cheaper, and its alternatives section was written after the choice. → Alternatives are scored before choosing; reviews check they span different levels.
- **The orchestrator made design decisions and wrote briefs without the project's design guide,** so a refactor's sweep covered dispatch code but missed specs and contracts. → Read the profile's design guide before any design decision or design brief; each decision states how its cost grows per new feature; the instance-fact table searches specs and contracts, not only code that names the feature.
- **A generalization kept the old form beside the new one** because removing it was hard. → Not accepted: fix the cause, or record why in a finding with a removal item.
- **Facts true only of today's hardware or backend sat in neutral layers** and surfaced only when the user asked. → Hardware behavior enters the core only as backend parameters or per-backend obligations with their own evidence; a check refuses backend names in neutral code. Backends may declare guarantees in a neutral vocabulary kept apart from operation contracts, so an unused one is inert.
- **A cross-cutting interface change looked local but broke consumers several layers up.** → Before deciding, have an agent list every consumer of what is changing (about 15 minutes).
- An interface law (a contract a plugin must meet) designed against stand-ins fails review repeatedly: once against a stand-in consumer, then with the real consumer but no producer. A law item's acceptance names both sides: the real consumer statement proved from the law, and one real instance proving the law's premises at the real inputs, built in the same item.
- Agents hand off at the first interface question (a missing framework fact, an unchosen shape) even with most of the box left, so each small decision costs one handoff and one dispatch. When the orchestrator owns design decisions, briefs say: decide it per the design guide, write it in the design text in place, mark it for review in the finding, and continue; reviews of marked decisions batch at the merge.
- A plugin interface grew one member per review round against its single real kind, so every later kind would implement stubs for the first kind's concerns. Before the second real kind is built, run a paper-instantiation review: write each planned kind's implementation of every member, and mark each member used, trivial or not fitting. The result drives one consolidation item. Paper instantiation checks shape only; the first real second kind confirms provability and proof cost.

## Reviews

Beyond findings, each review proposes changes that make a whole class of error impossible or trivial to test: types that cannot represent the bad state, one shared mechanism instead of per-module copies, constructors that require evidence, generic harnesses every new component gets for free (crash at every boundary, reload every step, shared contract suites for Fakes and production). Each proposal names the error class, the findings it would have prevented, and its cost.

### Design alignment

Periodically, and before a phase adds a new kind of instance, compare each design's promises (interfaces, per-instance cost claims, stated generality) with the implementation. Give each mismatch one verdict: implementation drift (fix the code), a design gap the implementation exposed (revise the design, with review), both wrong (a design item), or a deliberate deferral (owner and removal plan). Reviews of a sub-design check it against its parent design's cost promises and walk one operation of every instance kind, deferred ones included, through the new interface. A periodic design-level review re-asks, for designs in flight, whether another abstraction level would be cheaper.
