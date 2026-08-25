---
name: arm-new-track
description: Start a new feature or bug fix track with a specification and phased plan. Use when asked to create a new track, start a feature, plan a bug fix, or run /arm-new-track.
persona: Armature Planner
---

# /arm-new-track — Create a New Track

**Purpose:** Start a new feature or bug fix track with a specification and
phased plan through a rigorous, multi-turn decision-tree traversal interview
resolving all open branches and ambiguities.

## Mandatory Execution Guardrails

-   **Strict Interactive Discipline:** You MUST NEVER generate track artifacts
    (`spec.md`, `plan.md`) or write code in a single autonomous turn. Every
    track requires step-by-step user alignment.
-   **Synchronous Turn-Ending Barrier:** You MUST invoke `ask_question` and end
    your turn at Step 5 (Branch Resolution Probes), Step 6 (Spec Approval), and
    Step 7 (Plan Approval). Do not proceed to subsequent steps until the user
    responds.
-   **Compound Directive Shielding:** If the user invokes `/arm-new-track`
    alongside other instructions (e.g., `/diagnose`, `Fix`, or implementation
    tasks), you MUST explicitly refuse to write code or generate `plan.md`
    prematurely. Complete all interactive track creation milestones sequentially
    before starting downstream execution.
-   **Premature Draft Command Shielding:** If the user issues commands like
    "Draft the spec", "Looks good, write the spec", or "Proceed to drafting"
    while decision branches, operational failure modes, or architectural
    ambiguities remain unresolved, you MUST NOT materialize `spec.md`
    immediately. Explicitly state which decision branches and operational
    dimensions remain open and pose the next targeted probe via `ask_question`.
-   **Anti-Early-Exit & Branch Completeness Invariant:** You MUST NEVER
    terminate the interview prematurely after only happy-path questions. Walk
    down every branch of the design tree, resolving dependencies and operational
    edge cases one-by-one until no ambiguities remain.
-   **No Autonomous Skipping:** The presence of extensive context (e.g., chat
    logs, design docs, bug descriptions, or codebase reconnaissance) informs
    your questions and recommendations, but NEVER excuses skipping the
    interactive interview.
-   **Pre-Materialization Hardening Barrier:** You MUST hold specification state
    in memory during Step 5. Canonical `spec.md` is only materialized on disk in
    Step 6 after all decision branches, failure modes, and adversarial
    challenges reach resolved decisions and the user confirms the Convergence
    Summary.
-   **Interruption & Detour Recovery:** If the user asks side questions,
    clarifies requirements, or explores asset tangents mid-traversal, answer the
    inquiry and resume traversing the open branches. NEVER leap to Plan
    Generation or VCS Commit.

## Protocol

1.  **Context Resolution & Setup Check:**
    -   Resolve `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` (armature or conductor) per `armature_protocol.md` §7.
    -   Verify that the following files exist:
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md`
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md`
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md`
    -   If ANY of these files are missing, halt immediately with the message:
        "Please run `/arm-setup` first to initialize Armature for this project."

2.  **Get Description & Infer Type:**

    -   If a description was provided in the initial prompt, use it.
    -   If no description was provided, ask via `ask_question`: "What feature or
        bug would you like to work on? Describe it in 1-2 sentences."
    -   Analyze the description to infer the track type (Feature vs. Bug/Chore).
        Do NOT ask the user to classify the type.

3.  **Duplicate Track Check & Initialization:**

    -   Before generating a track ID, check the
        `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/` directory to ensure no existing track
        has a conflicting name.
    -   Generate a unique, short, descriptive `track_id` based on the
        description (e.g., `dark-mode-toggle`).
    -   Create the directory: `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/`

4.  **Codebase Reconnaissance:**

    -   Read `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md` and
        `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md` for architectural context.
    -   Read `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/terms.md` (if it exists) to ground term
        usage and prevent symbol/concept drift.
    -   Scan the `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/adr/` directory listing (filenames
        only) to build awareness of existing architectural decisions.
    -   Read ALL existing track specs by scanning
        `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/` for `*/spec.md` files.
    -   If the user's description references specific code areas, scan those
        files/directories to understand existing patterns, interfaces, and
        constraints.
    -   Use findings to inform the spec questions in the next step — questions
        must reference specific codebase context.

5.  **Continuous Decision-Tree Traversal & Ambiguity Resolution (Grill Engine):**

    Conduct a rigorous, one-question-at-a-time interview with the user about
    every aspect of their task until you have reached a shared understanding and
    resolved all open design branches, dependencies, and ambiguities:

    -   **Decision-Tree Traversal Philosophy**:
        -   Walk down each branch of the design tree, resolving dependencies
            between decisions one-by-one.
        -   Do NOT guess, assume, or settle for high-level approximations.
        -   If a question can be answered by exploring the codebase, explore the
            codebase instead.

    -   **Traverse All Unresolved Branches & Operational Layers**:
        -   *Architectural & UX Foundations*: Core trigger mechanisms, user
            journeys, competing UI/API patterns, component boundaries, data
            contracts, and explicit scope exclusions.
        -   *Process & Protocol Architecture*: Lockfile strategy, multi-instance
            concurrency, daemon vs sidecar boundaries, process signal handling
            (`SIGTERM` graceful drain vs `SIGKILL` orphan cleanup), and network
            polling vs event-driven triggers.
        -   *Proto/Schema Evolution & Backward Compatibility*: Zero-downtime field
            migrations, deprecation schedules, default zero-value handling,
            FieldMasks, and gateway schema federation directives (`@key`,
            `__resolveReference`).
        -   *Operational Hardening & Failure Recovery*: Dependent failure modes,
            network outages, timeout thresholds, degraded fallback UI states,
            retry backoff strategies, and abort/cancellation cascades.
        -   *Boundary Interactions & Concurrency*: Navigation interrupts (ESC,
            backdrop, route teardown in-flight), double-submit debounce/guards,
            duplicate delivery/idempotency, multi-tab sync, cache invalidation,
            leader election crash recovery, session expiration.
        -   *State Invariants, Security & Accessibility*: Webhook signatures,
            PII redaction, auth token handling (distinguishing 401 retry loops
            from 403 terminal rejections), log token scrubbing, database
            transaction atomicity, ARIA live regions for async state, focus
            trapping/restoration, screen reader visibility (`aria-hidden`).

    -   **Active Adversarial Probing (Devil's Advocate)**:
        -   Actively challenge fragile assumptions, breaking proto/schema
            evolutions, concurrency hazards, and cascading failures across the
            active decision branches until the solution is hardened against edge
            conditions.
        -   When specific technical choices are proposed (e.g., CSS filters,
            distributed locks, polling loops, WebSocket heartbeats), mount
            direct adversarial challenges grounded in the operational risks,
            concurrency hazards, and performance trade-offs of those choices.

    -   **Testing Strategy Classification**: Classify manual testing depth:
        -   *Interactive / Stateful / Route / API Tracks*: Full `manual_testing.md`
            runbook with environment setup, CLI reset tooling, persona matrices,
            and sequential route test cases.
        -   *Pure Refactor / Utility / Chore Tracks*: Lightweight
            `manual_testing.md` with concise smoke and sanity checks alongside
            automated unit tests. When requirements for a pure refactor or
            utility track are already clear, immediately formulate the Testing
            Strategy classification and proceed directly to the Convergence
            Summary without injecting redundant questioning loops.

    -   **Questioning Mechanics**:
        -   Ask questions **strictly one at a time** using `ask_question`.
        -   List recommended option first (`(Recommended)`) with 2–4 calibrated
            choices.
        -   **MANDATORY:** End your turn after each `ask_question` call to wait for
            the user's answer.

    -   **Inline Design Decisions & ADRs**:
        -   If the 3-part gate is met, offer to capture an ADR
            (`{PROJECT_CONTEXT_DIR}/adr/NNNN-slug.md`) using `ask_question`.
    -   **Inline Glossary Elicitation (`terms.md`)**:
        -   If a decision introduces domain terminology, offer to record it in
            `{PROJECT_CONTEXT_DIR}/terms.md`.

    -   **Convergence Summary & Modal Confirmation Gate**:
        -   When all branches of the design tree have been explored and all
            operational ambiguities, failure modes, and adversarial challenges
            are fully resolved, present a structured **Convergence Summary** in
            markdown synthesizing all settled decisions.
        -   Call `ask_question`: "All decision branches, failure modes, and adversarial challenges are resolved. Ready to materialize the specification and manual testing runbook?"
        -   **MANDATORY:** End your turn and wait for explicit confirmation.

6.  **Spec & Manual Testing Materialization & Final Confirmation:**

    -   ONLY NOW, write the canonical specification to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/spec.md` using `write_to_file`.
    -   Write `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/manual_testing.md` based on `manual_testing_template.md` tailored to the classified testing depth.
    -   Present `spec.md` and `manual_testing.md` via `notify_user` with `PathsToReview`.
    -   Present options using `ask_question`: "Approve" (Proceed to planning), "Revise" (Suggest manual edits).
    -   **MANDATORY:** End your turn and wait for explicit user approval before proceeding to plan generation.

7.  **Interactive Plan Generation:**

    -   Verify the spec is approved.
    -   Read confirmed spec and `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md`.
    -   Generate hierarchical plan with Phases, Tasks, and Sub-tasks with `[ ]` checkboxes.
    -   **Developer Test Tooling Tasks**: If new routes, state guards, or flags are added, ensure Phase 1 includes explicit tasks for developer reset tooling, CLI scripts, or fixture seeding needed by `manual_testing.md`.
    -   **Verification Bridge**: For each verification checkbox `[ ]` defined in an ADR's Confirmation section, inject a corresponding explicit verification task into `plan.md`.
    -   **Phase Checkpointing**: If `workflow.md` defines phase checkpointing, inject Phase Completion meta-tasks at the end of each Phase.
    -   Write to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/plan.md` using `write_to_file`.
    -   Present via `notify_user` with `PathsToReview` and `ask_question`: "Approve", "Revise".
    -   **MANDATORY:** End your turn and wait for explicit user approval.

8.  **Generate Remaining Track Artifacts:**

    -   Create `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/metadata.json` containing: `track_id`, inferred `type`, `status` (`planned`), timestamps, and `description`.
    -   Write `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/index.md` containing summary and relative links to `spec.md`, `plan.md`, `manual_testing.md`, and `metadata.json`.
    -   Append new track to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md`: `- [ ] **Track: <Track Title>** _Link: [./tracks/<track_id>/](./tracks/<track_id>/)_`

9.  **Commit Changes:**

    -   Commit the new track directory and updated `tracks.md` using VCS commands.
    -   Commit message: `chore(armature): Add new track '<description>'`

10. **Confirm Completion:**

    -   Display: "✅ Track `<track_id>` created! Run `/arm-implement` to start working through the plan."

## Guardrails

-   **Compound Directive Shielding**: Never start implementation or write code prematurely.
-   **Turn-Ending Barriers**: Enforce strict synchronous pauses at Step 5, Step 6, and Step 7 via `ask_question`.
-   **Pre-Materialization Barrier**: Hold `spec.md` in memory during Step 5.
-   **Continuous Decision-Tree Traversal & Ambiguity Resolution**: Never conclude an interview turn while decision branches, dependencies, failure modes, or architectural ambiguities remain unresolved.
