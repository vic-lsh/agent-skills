---
name: codify
description: Turn any mechanical part of the work (a review check, a recurring rule, a repeated manual step, a slow loop) into code that does or checks the work (lints, enforced dependency structure, static analyzers, ratchets, caches and sharding, self-classifying diagnostics, generators, fixture builders, or anything else) instead of leaving it to agent reasoning. Use when a step or a review finding recurs, a check is slow, a defect was found late that a program could have caught, or a written rule keeps being broken.
---

# Codify

Code is written once and runs on every change; reasoning costs tokens on every run and drifts. If a program can do or check something, write the program. Leave to agents only what code cannot decide, such as design judgment. How the product's own code is structured for correctness checking is skill `design-for-verification`; this skill builds the tools.

## Step 0

Read the repo's tooling map: the index of existing tools, how to plug a new one in, and the repo's tool conventions. The project's agent instructions name its location. If the repo has none, create one beside the tools and name it in the instructions file.

## When to codify

Common signs (not a complete list):

- The same manual step was done twice: resolving a generated file in a merge, isolating a cost regression, assembling evidence for a review.
- A reviewer reported the same kind of finding twice.
- A written rule in a brief, skill or instructions file keeps being broken. A written rule is the weakest tool.
- A defect reached review or CI that a program could have caught earlier.
- A check takes more than about 5 minutes.

No cost-benefit argument is needed. Tools are used for a long time once built; prefer the tool.

## Steps

1. **State what a program would need to know** to do or check the work, and where that information already exists (types, the build graph, the compiler's or checker's output, structured logs).
2. **Choose the tool.** Any code that takes the work off the agent qualifies. Kinds that have paid off before, as examples only: static checks and lints, enforced dependency layers, ratchets that only go down, test selection, caching and sharding, diagnostics that classify their own findings, generators and regenerators, fixture builders that own boilerplate, merge helpers. If the right tool is none of these, build it anyway.
3. **Search the tooling map** for a tool that already does part of this; extend it rather than adding a second tool for the same job.
4. **Build it to these rules:**
   - Structural, not textual: use types, visibility, build features and the toolchain's own output. Never pattern-match source text to enforce a rule.
   - Deterministic: no dependence on run order, process ids, temporary paths or timestamps. Cache keys contain only what the result depends on.
   - Fast: aim under 5 minutes; cache on the true dependency closure; shard by measured cost.
   - Actionable output: what failed, why, and the fix or the next command. A diagnostic labels its own findings (for example noise versus a real regression) instead of leaving the analysis to the reader.
   - Fails closed: if it cannot measure or decide, it says so and stops; it never skips silently.
5. **Prove it** with the lower levels of skill `design-for-verification`: a negative control that makes it fire for the intended reason (follow the repo's negative-control procedure if it has one), a regression test of the tool's own logic, and a clean run on the main branch.
6. **Roll out:** report-only first; blocking once main is clean and its control passes, recording the decision. A ratchet baseline only goes down; a new exception is a signal to restructure, not a fix.
7. **Close the loop:** add the tool to the tooling map; delete every written rule (brief, skill, instructions) the tool now enforces; record what it saves in the effort's ledger if one exists.

## Do not

- Satisfy a check by widening its own rule or adding an allowance for new code.
- Let two agents build the same tool in parallel: give each tool one owner.
- Write transient issues into the tooling map or a skill. A known gap becomes a tooling item or an issue; only the lasting lesson goes in prose.
