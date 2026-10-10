---
name: progress-update
description: Give the user a high-level progress update on a multi-agent effort they asked you to orchestrate, covering everything since their last requested update, plus the decisions you made on your own so they can correct them. Use when the user asks for a progress update, status, recap, or "where are we" during an orchestrated effort, or invokes this skill by name.
---

# Progress update

The user asks for this when they come back. Write it for someone who read nothing in between: scheduled check-in reports may have scrolled past unread, so never assume they were seen.

## Steps

1. Find the effort's records the way `orchestrate-agents` does (its project profile names the records location; fall back to the plan file in the session scratchpad). Read the goals and workstreams the user named, the ledger, the decision log, and `updates.md` beside them.
2. Find the last update marker in `updates.md`. Recap everything after it; with no marker, recap since the effort started.
3. Refresh facts before writing: what merged, what is open, what each agent is doing, roadmap sub-issue counts if the effort has a roadmap. Never report a claim you have not checked.
4. Write the update (format below).
5. Append a marker to `updates.md`: the time, and the ids of the decisions this update presented. Save it as `~/.agent-state/README.md` says if the records live in agent state.
6. If the user corrects a decision, apply the correction, log it as a new decision that supersedes the old one, and tell the affected agents. If the user says nothing about a decision, it stands: do not revise it or ask again.

## Format

Plain language, outcomes not artifacts. No PR or issue numbers, branch names, commit hashes, file paths, or agent ids unless the user asks for them.

1. **One line on the whole effort:** percent done toward the end goal and time left, using the ledger's estimate bias to correct the estimate.
2. **One short section per goal or workstream the user named:**
   - percent done;
   - what is now true that was not at the last update, in user terms ("the app reconnects after the laptop sleeps");
   - what is next and its time left;
   - anything blocked.
3. **Decisions I made since your last update:** one entry per decision:
   - what was decided;
   - why, in a sentence;
   - the main alternative;
   - what reversing it would cost.

   End with: "Tell me if you want any of these changed; otherwise they stand."
4. **Needs you:** only questions that block work under the effort's decision policy, each with a recommended answer. Omit the section when empty.

Keep it under about 300 words unless the user asks for detail.
