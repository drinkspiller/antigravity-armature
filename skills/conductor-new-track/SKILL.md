---
name: conductor-new-track
description: Start a new feature or bug fix track with a specification and phased plan. Use when asked to create a new track, start a feature, plan a bug fix, or run /conductor-new-track.
persona: Conductor Planner
---

# /conductor-new-track — Create a New Track

**Purpose:** Start a new feature or bug fix track with a specification and
phased plan through a rigorous, multi-turn inquiry depth traversal interview.

## Mandatory Execution Guardrails

-   **Strict Interactive Discipline:** You MUST NEVER generate track artifacts
    (`spec.md`, `plan.md`) or write code in a single autonomous turn. Every
    track requires step-by-step user alignment.
-   **Synchronous Turn-Ending Barrier:** You MUST invoke `ask_question` and end
    your turn at Step 5 (Inquiry Depth Probes), Step 6 (Spec Approval), and Step 7
    (Plan Approval). Do not proceed to subsequent steps until the user responds.
-   **Compound Directive Shielding:** If the user invokes `/conductor-new-track`
    alongside other instructions (e.g., `/diagnose`, `Fix`, or implementation
    tasks), you MUST explicitly refuse to write code or generate `plan.md` prematurely. Complete all interactive track creation milestones sequentially before starting downstream execution.
-   **Premature Draft Command Shielding:** If the user issues commands like "Draft the spec", "Looks good, write the spec", or "Proceed to drafting" before all open inquiry matrix dimensions (error recovery, edge cases, accessibility, security, failure modes, adversarial challenges) have been explored, you MUST NOT materialize `spec.md` immediately. Explicitly state which inquiry dimensions remain open and pose the next targeted probe via `ask_question`.
-   **Anti-Early-Exit Invariant:** You MUST NEVER terminate the interview after only 1–3 happy-path questions. When the primary architectural flow is settled, you MUST continue formulating follow-up probes across failure recovery, boundary edge cases, accessibility/ARIA state, and adversarial stress tests before converging.
-   **No Autonomous Skipping:** The presence of extensive context (e.g., chat
    logs, design docs, bug descriptions, or codebase reconnaissance) informs
    your questions and recommendations, but NEVER excuses skipping the
    interactive interview.
-   **Pre-Materialization Hardening Barrier:** You MUST hold specification state
    in memory during Step 5. Canonical `spec.md` is only materialized on disk in
    Step 6 after all 6 inquiry dimensions reach resolved decisions and the user confirms the Convergence Summary.
-   **Interruption & Detour Recovery:** If the user asks side questions, clarifies
    requirements, or explores asset tangents mid-traversal, answer the inquiry
    and resume traversing the open inquiry matrix dimensions. NEVER leap to Plan
    Generation or VCS Commit.

## Protocol

1.  **Setup Check:** Verify that the following files exist:

    -   `{PROJECT_ROOT}/conductor/product.md`
    -   `{PROJECT_ROOT}/conductor/tech-stack.md`
    -   `{PROJECT_ROOT}/conductor/workflow.md`
    If ANY of these files are missing, halt immediately with the message:
    "Please run `/conductor-setup` first to initialize Conductor for this project."

2.  **Get Description & Infer Type:**

    -   If a description was provided in the initial prompt, use it.
    -   If no description was provided, ask via `ask_question`: "What feature or
        bug would you like to work on? Describe it in 1-2 sentences."
    -   Analyze the description to infer the track type (Feature vs. Bug/Chore).
        Do NOT ask the user to classify the type.

3.  **Duplicate Track Check & Initialization:**

    -   Before generating a track ID, check the
        `{PROJECT_ROOT}/conductor/tracks/` directory to ensure no existing track
        has a conflicting name.
    -   Generate a unique, short, descriptive `track_id` based on the
        description (e.g., `dark-mode-toggle`).
    -   Create the directory: `{PROJECT_ROOT}/conductor/tracks/<track_id>/`

4.  **Codebase Reconnaissance:**

    -   Read `{PROJECT_ROOT}/conductor/tech-stack.md` and
        `{PROJECT_ROOT}/conductor/product.md` for architectural context.
    -   Read `{PROJECT_ROOT}/conductor/terms.md` (if it exists) to ground term
        usage and prevent symbol/concept drift.
    -   Scan the `{PROJECT_ROOT}/conductor/adr/` directory listing (filenames
        only) to build awareness of existing architectural decisions.
    -   Read ALL existing track specs by scanning
        `{PROJECT_ROOT}/conductor/tracks/` for `*/spec.md` files.
    -   If the user's description references specific code areas, scan those
        files/directories to understand existing patterns, interfaces, and
        constraints.
    -   Use findings to inform the spec questions in the next step — questions
        must reference specific codebase context.

5.  **Continuous Inquiry Depth Traversal (The 6-Dimension Matrix):**

    Conduct a rigorous, one-question-at-a-time interview with the user. The interview systematically explores the 6 fundamental dimensions of production software engineering before converging on a specification:

    -   **The 6-Dimension Inquiry Matrix**:
        1.  *Primary Architectural & UX Flow*: Core trigger mechanisms, component hierarchy, route transitions, data contracts, and happy-path presentation.
        2.  *Failure Modes & Error Recovery*: Network outages, backend 500s/RPC failures, timeout thresholds, degraded fallback UI states, retry backoff strategies, and abort/cancellation cascades.
        3.  *Boundary Interactions & Escape Hatches*: ESC dismissal, backdrop navigation interrupts, double-submit debounce/guards, route teardown cleanup, and rapid navigation race conditions.
        4.  *State Invariants, Concurrency & Security*: Multi-tab synchronization, session expiration handling (401/403 vs 500), cache invalidation, input sanitization, PII redaction, and ACL enforcement.
        5.  *Accessibility, Contrast & Environmental Constraints*: ARIA live regions/announcements for async operations, focus trapping and restoration, screen reader visibility (`aria-hidden`), dark/light theme contrast, and bundle/performance overhead.
        6.  *Adversarial Stress Testing (Devil's Advocate)*: Present at least 2 explicit adversarial challenges ("What happens if [X]?", "Have you considered [Y]?", "This assumes [Z] — is that valid?"), probing schema evolution breaks, dependency weight, race conditions, or unhandled cascading states.

    -   **Progressive Depth Traversal**:
        -   When the user chooses an architectural path for the primary flow (Dimension 1), do NOT stop questioning.
        -   Immediately formulate targeted follow-up probes addressing the remaining open dimensions (Dimensions 2 through 6).
        -   Every question must be concrete, referencing codebase paths, component names, and real runtime constraints discovered during reconnaissance.

    -   **Detour Recovery & State Resumption**:
        -   If the user takes a detour, clarifies tangent requirements, or explores assets, answer accurately.
        -   Preserve the active matrix state, synthesize decisions reached during the detour, and cleanly resume probing the remaining open dimensions without skipping.

    -   **Testing Strategy Classification**:
        Classify the track's manual testing depth as part of the interview:
        -   *Interactive / Stateful / Route / API Tracks*: Require a full `manual_testing.md` runbook with environment setup, CLI reset tooling, persona matrices, and sequential route test cases.
        -   *Pure Refactor / Utility / Chore Tracks*: Require a lightweight `manual_testing.md` with concise smoke and sanity checks alongside automated unit tests.

    -   **Questioning Mechanics**:
        -   Ask questions **strictly one at a time** using `ask_question`.
        -   List your recommended option first (`(Recommended)`) with 2–4 calibrated peer choices.
        -   **MANDATORY:** End your turn after each `ask_question` call to wait for the user's answer.

    -   **Inline Design Decisions & ADRs**:
        -   Evaluate the 3-part gate as trade-offs emerge: (1) Hard to reverse, (2) Surprising without context, (3) Real trade-off.
        -   If met, immediately offer to capture an ADR (`conductor/adr/NNNN-slug.md`) using `ask_question`.

    -   **Inline Glossary Elicitation (`terms.md`)**:
        -   If a decision introduces or refines domain terminology, offer to record it in `terms.md`.

    -   **Cross-Track & ADR Conflict Check**:
        -   Check active decisions against `conductor/tracks.md` and matching `conductor/adr/` records to flag cross-track dependencies or policy violations inline.

    -   **Convergence Summary & Modal Confirmation Gate**:
        -   When all 6 dimensions have been explored, present a structured **Convergence Summary** in markdown summarizing the settled decisions across all dimensions.
        -   Then, call `ask_question`: "All 6 inquiry dimensions and adversarial challenges are resolved. Ready to materialize the specification and manual testing runbook?" (`["(Recommended) Yes, materialize spec and runbook", "Not yet — let's revisit [dimension]"]`).
        -   **MANDATORY:** End your turn and wait for explicit confirmation.

6.  **Spec & Manual Testing Materialization & Final Confirmation:**

    -   ONLY NOW, write the canonical specification to `{PROJECT_ROOT}/conductor/tracks/<track_id>/spec.md` using `write_to_file` with `IsArtifact: true` (`ArtifactType: other`).
    -   The spec MUST contain: `## Overview`, `## Functional Requirements`, `## Non-Functional Requirements`, `## Design Decisions`, `## Manual Verification Plan`, `## Acceptance Criteria`, and `## Out of Scope`.
    -   Write `{PROJECT_ROOT}/conductor/tracks/<track_id>/manual_testing.md` based on `manual_testing_template.md` tailored to the classified testing depth.
    -   Present `spec.md` and `manual_testing.md` via `notify_user` with `PathsToReview`.
    -   **Present options** using `ask_question`: "Approve" (Proceed to planning), "Revise" (Suggest manual edits).
    -   **MANDATORY:** End your turn and wait for explicit user approval before proceeding to plan generation.

7.  **Interactive Plan Generation:**

    -   Verify the spec is approved.
    -   Read the confirmed spec and `{PROJECT_ROOT}/conductor/workflow.md`.
    -   Generate a hierarchical plan with Phases, Tasks, and Sub-tasks.
    -   Include status markers `[ ]` for EVERY task and sub-task.
    -   **Developer Test Tooling Tasks**: If the track introduces new routes, state guards, or flags, ensure Phase 1 includes explicit tasks for developer reset tooling, CLI scripts, or fixture seeding needed by `manual_testing.md`.
    -   **Verification Bridge**: For each verification checkbox `[ ]` defined in an ADR's Confirmation section, inject a corresponding explicit verification task into the relevant Phase of `plan.md`.
    -   **Phase Checkpointing**: If `workflow.md` defines phase checkpointing, inject Phase Completion meta-tasks at the end of each Phase.
    -   Write to `{PROJECT_ROOT}/conductor/tracks/<track_id>/plan.md` using `write_to_file` with `IsArtifact: true` (`ArtifactType: implementation_plan`).
    -   Present via `notify_user` with `PathsToReview` and `ask_question`: "Approve" (Proceed to track creation), "Revise" (Suggest changes).
    -   **MANDATORY:** End your turn and wait for explicit user approval before finalizing artifacts or starting implementation.

8.  **Generate Remaining Track Artifacts:**

    -   Create `{PROJECT_ROOT}/conductor/tracks/<track_id>/metadata.json` containing: `track_id`, inferred `type`, `status` (`planned`), timestamps, and `description`.
    -   Write `{PROJECT_ROOT}/conductor/tracks/<track_id>/index.md` containing summary and relative links to `spec.md`, `plan.md`, `manual_testing.md`, and `metadata.json`.
    -   Append the new track to `{PROJECT_ROOT}/conductor/tracks.md`: `- [ ] **Track: <Track Title>** _Link: [./tracks/<track_id>/](./tracks/<track_id>/)_`

9.  **Commit Changes:**

    -   Commit the new track directory and updated `tracks.md` using VCS commands.
    -   Commit message: `chore(conductor): Add new track '<description>'`

10. **Confirm Completion:**

    -   Display: "✅ Track `<track_id>` created! Run `/conductor-implement` to start working through the plan."

## Guardrails

-   **Compound Directive Shielding**: If the user prompt includes compound instructions (e.g., "create a track and implement it immediately in foo.ts"), do NOT start implementation or write code. Strictly limit scope to track planning and state that implementation must wait until the plan is approved.
-   **Turn-Ending Barriers**: Enforce strict synchronous pauses at Step 5 (Inquiry Depth Probes & Convergence Gate), Step 6 (Spec Approval), and Step 7 (Plan Approval) via `ask_question`. Never batch questions or skip ahead.
-   **Pre-Materialization Barrier**: Hold `spec.md` in memory during Step 5. Never write `spec.md` to disk until all 6 inquiry dimensions are explored and the convergence summary is confirmed.
-   **Continuous Inquiry Depth**: Never conclude an interview turn without systematically probing failure modes, boundary interactions, accessibility, state invariants, and adversarial stress challenges.
