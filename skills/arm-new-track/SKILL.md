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
    your turn at Step 5 (Leaf Probes & Convergence Gate), Step 6 (Spec
    Approval), and Step 7 (Plan Approval). Do not proceed to subsequent steps
    until the user responds.
-   **Mandatory Decision Tree Ledger:** In EVERY turn of Step 5, you MUST output
    a visible `### Decision Tree Ledger` block showing root branches and their
    spawned child leaves with explicit `[ ]` (OPEN) and `[x]` (Resolved)
    markers.
-   **Anti-Dictation Invariant (Zero Un-Queried Decisions):** You MUST NEVER
    assert or output declarative technical specifications, UI layouts, button
    behaviors, countdown cancel rules, or lifecycle state transitions in
    markdown for topics that have not been confirmed by the user. Every
    technical detail is an unresolved leaf ambiguity that MUST be posed via
    `ask_question`.
-   **Child Leaf Spawning Invariant (Hierarchical Sub-Tree Probing):** Selecting
    an option at the root of a branch does NOT close the branch. Every
    architectural choice MUST immediately spawn child leaf ambiguities (failure
    modes, token/resource bounds, state transitions, concurrency races) that
    must be probed one-by-one. A root branch CANNOT transition to `[x]` while
    child leaves remain `[ ]`.
-   **Compound Directive Shielding:** If the user invokes `/arm-new-track`
    alongside other instructions (e.g., `/diagnose`, `Fix`, or implementation
    tasks), you MUST explicitly refuse to write code or generate `plan.md`
    prematurely. Complete all interactive track creation milestones sequentially
    before starting downstream execution.
-   **Premature Draft Command Shielding:** If the user issues commands like
    "Draft the spec", "Looks good, write the spec", or "Proceed to drafting"
    while decision branches or child leaves remain `[ ]` (OPEN), you MUST NOT
    materialize `spec.md` immediately. List the remaining open leaves in the
    ledger and pose the next targeted probe via `ask_question`.
-   **Anti-Early-Exit & Natural Convergence:** The interview concludes ONLY when
    every branch and child leaf in the Decision Tree Ledger is marked `[x]`
    (Resolved) with zero open items. There are zero arbitrary question quotas;
    exhaustiveness is governed strictly by leaf resolution.
-   **Pre-Materialization Hardening Barrier:** You MUST hold specification state
    in memory during Step 5. Canonical `spec.md` is only materialized on disk in
    Step 6 after all branches and child leaves in the ledger are confirmed by
    the user.
-   **Interruption & Detour Recovery:** If the user asks side questions,
    clarifies requirements, or explores asset tangents mid-traversal, answer the
    inquiry, update the ledger, and resume traversing open leaves. NEVER leap to
    Plan Generation or VCS Commit.

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

5.  **Recursive Decision-Tree Grill Engine (Hierarchical Leaf Traversal):**

    Conduct an exhaustive, one-question-at-a-time interview with the user. The
    interview operates as an active recursive decision tree where choosing an
    option at the root of a branch NEVER closes the branch—it actively spawns
    child leaf ambiguities that must be probed down into concrete operational
    child leaves until zero ambiguity remains in that area:

    -   **Mandatory Decision Tree Ledger Block**:

        -   In EVERY turn of Step 5, you MUST output a visible `### Decision
            Tree Ledger` block at the top of your markdown response.
        -   Format:

            ```markdown
            ### Decision Tree Ledger
            - [x] Branch 1: <Root Topic> (<Confirmed approach>)
              - [x] Leaf 1.1: <Failure / Error Mode> (<Confirmed decision>)
              - [x] Leaf 1.2: <Concurrency / State Boundary> (<Confirmed decision>)
            - [ ] Branch 2: <Root Topic> (<Confirmed approach>)
              - [ ] Leaf 2.1: <Token / Resource Bound> (OPEN — probing now)
              - [ ] Leaf 2.2: <Contradiction / Conflict Policy> (OPEN)
            - [ ] Branch 3: <Root Topic> (OPEN)
            ```
        -   Track state accurately: `[ ]` indicates an unresolved root or child
            leaf; `[x]` indicates a confirmed decision.

    -   **Child Leaf Spawning Invariant & Pruning Heuristics (Hierarchical Sub-Tree Probing):**

        -   When the user selects an architectural direction for a root branch,
            do NOT advance to the next root branch.
        -   The chosen option MUST actively spawn all high-value Tier 1 child
            leaf probes covering the operational realities of that choice until
            all architectural ambiguities in the branch are resolved:
            -   **Tier 1 (Mandatory Operational Probes — Interrogate
                Interactively):**
                -   *Failure Modes & Error Recovery*: Network drops, rater/RPC
                    failures, timeout thresholds, degraded fallback states,
                    retry backoff strategies, abort/cancellation cascades.
                -   *Resource & Payload Bounds*: Token ceilings, candidate
                    truncation, payload transport limits, rate limits, cache
                    invalidation.
                -   *UI Controls & State Transitions*: Visual status feedback
                    (WIP spinners, disabled states), button layout, countdown
                    cancel triggers, 1-click master copy actions.
                -   *State Invariants & Concurrency*: Multi-tab broadcast races,
                    tie-breaker handling, parallel dispatch synchronization,
                    leader election crashes.
                -   *Schema & Proto Evolution*: FieldMasks, optional presence vs
                    default zero-values, circular query plans, gateway fallback
                    nulls.
            -   **Tier 2 (Deferred Implementation Details — Prune from
                Interview):**
                -   Pure cosmetic styling (exact pixel padding, hex colors, font
                    weights).
                -   Micro-copy or minor text wording variations.
                -   Internal non-exported helper function naming. *Rule:* Do NOT
                    spawn interactive interview questions for Tier 2 items.
                    Defer them as sensible defaults in the implementation plan
                    to prevent interview fatigue and turn exhaustion.
        -   A root branch CANNOT be marked `[x]` while any of its Tier 1 child
            leaves remain `[ ]` (OPEN).

    -   **Anti-Dictation Invariant (Zero Un-Queried Decisions):**

        -   You are STRICTLY FORBIDDEN from asserting or outputting declarative
            implementation designs, button placements, countdown rules, or
            lifecycle state transitions in markdown for topics that have not
            been confirmed via `ask_question`.
        -   If an implementation detail exists (e.g., how the countdown cancels,
            what buttons appear on the winner card, what text the prompt
            injects), it is an **unresolved leaf ambiguity**. It MUST be posed
            to the user via `ask_question`, never asserted as an unconfirmed
            fait accompli.

    -   **Active Adversarial Probing (Devil's Advocate):**

        -   Actively challenge fragile assumptions, concurrency hazards, and
            cascading failures as child leaf probes across the active decision
            branches until the solution is hardened against edge conditions.
        -   Ground challenges in concrete operational risks (e.g., SVG filter
            repaint overhead, distributed lock TTL drift, split-brain token
            races, proto3 default zero-value collisions).

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

    -   **Natural Convergence & Modal Confirmation Gate**:

        -   There are zero arbitrary question quotas; exhaustiveness is governed
            strictly by the Decision Tree Ledger.
        -   The interview concludes if and only if EVERY branch and child leaf
            in the Decision Tree Ledger is marked `[x]` (Resolved) with zero
            open items.
        -   ONLY THEN, present a structured **Convergence Summary** in markdown
            synthesizing all settled decisions.
        -   Call `ask_question`: "All decision branches and child leaves are
            resolved. Ready to materialize the specification and manual testing
            runbook?"
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
