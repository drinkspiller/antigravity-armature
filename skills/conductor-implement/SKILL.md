---
name: conductor-implement
description: Execute the plan for the current active track, working through tasks sequentially with TDD lifecycle and phase checkpointing. Use when asked to implement, execute the plan, work on the next task, or run /conductor-implement.
persona: Conductor Implementer
---

# /conductor-implement — Execute the Plan

**Purpose:** Execute the plan for the current active track, working through
tasks sequentially, synchronizing documentation, and managing track cleanup.

## Protocol

### Step 1: Setup Check

1.  Verify the existence of the core context files (`product.md`, `tech-stack.md`, `workflow.md`).
2.  If core context files exist in the workspace or are provided in the prompt context, proceed immediately. If files are missing and cannot be located, halt and inform the user.

### Step 2: Track Selection & Milestone Routing

1.  **Direct Milestone Routing**: If the user prompt specifically instructs you to execute a particular milestone or phase (e.g., "Execute Phase N checkpoint", "Finalize and synchronize documentation", "Proceed to Step 5", "Proceed to track closeout", or "What should we do now?"), jump directly to that targeted step without pausing for exploratory file listing or selection confirmation.
2.  Otherwise, read `{PROJECT_ROOT}/conductor/tracks.md`.
3.  If a track name was provided:
    -   Find the exact match in `tracks.md`.
    -   Use `ask_question` to confirm the selection: "Proceed with track '{Track Name}'?" [Yes] / [No]
4.  If no track name was provided:
    -   Find the first non-completed track (marked `[ ]` or `[~]`).
    -   Use `ask_question` to confirm the selection: "Proceed with track '{Track Name}'?" [Yes] / [No]
5.  If no incomplete tracks exist, announce that all tracks are complete and halt.

### Step 3: Track Implementation & Phase Checkpoints

1.  Before starting tasks, update the selected track's status to `[~]` in
    `{PROJECT_ROOT}/conductor/tracks.md`.
2.  Load the track context (`spec.md`, `plan.md`, `workflow.md`).
3.  Execute tasks sequentially as defined in `plan.md`. For each uncompleted task (`[ ]`):
    -   **Per-Directory Context**: Before modifying files in a directory for the first time in this track, check case-insensitively for `GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`. If present with `## Conductor Context`, load it. If multiple or none exist and architectural justification exists, prompt via `ask_question` for the preferred filename. If simple, proceed without prompting.
    -   **Lifecycle Execution**: Follow TDD Red/Green/Refactor.
    -   **ADR Capture**: If an invariant or behavioral contract is introduced, capture via ADR.
    -   **Mark Complete**: Update the task to `[x]` in `plan.md` and record commit SHA.
4.  **Phase Checkpointing**: When the last task in a phase is completed (or when explicitly asked to execute a Phase checkpoint):
    -   Run the automated test suite.
    -   **API Surface Extraction**: Extract public symbols for changed files and update `.api_surface_cache.json`.
    -   **Per-Directory Rule Reconciliation**: Reconcile local directory rules in `GEMINI.md` / `AGENTS.md`.
    -   **Manual Verification Protocol Generation**:
        -   Update `{PROJECT_ROOT}/conductor/tracks/<track_id>/manual_testing.md` with exact reproduction steps, CLI reset commands, URLs, and test personas for the phase deliverables.
        -   **Documentation-Only Invariant**: Document the exact commands with precision, but do NOT execute mutative database resets or environment teardowns autonomously.
    -   **Incremental Drift Audit**: Perform an incremental drift check on modified files against touched ADRs and runbooks (`/conductor-drift --scope=phase`).
    -   **Walkthrough Artifact**: Write `{ARTIFACT_DIR}/conductor_implement_phase_N_verification.md` using `write_to_file` with `IsArtifact: true` (`ArtifactType: walkthrough`).
    -   **Turn-Ending Barrier**: Notify the user with `PathsToReview` and pause via `ask_question`: "Phase N implementation complete. Please review the manual verification guide and confirm to proceed." (`["(Recommended) Proceed to next phase", "I need to test first", "Revise verification steps"]`). End your turn and wait for confirmation.

### Step 4: Document Synchronization

**Mandatory Single-Turn Continuous Execution:** When asked to finalize/synchronize documentation (or when transitioning from completing all tasks), you MUST execute all steps of Step 4 AND Step 5.1 & Step 5.2 in a single turn. Perform all file operations, edits, commits, and retrospective review tasks autonomously without printing intermediate conversational updates or waiting for the user. Do NOT end your turn or pause until you invoke the mandatory `ask_question` next-steps modal in Step 5.2.

When all tasks in the track are complete (or when asked to finalize and synchronize documentation):

1.  **Deterministic AST & Symbol Extraction for Ubiquitous Language (`terms.md`)**:
    -   Proactively scan the workspace git diff, new interface exports, proto definitions, and entity models for newly introduced domain terminology and symbols.
    -   Append newly identified definitions to `{PROJECT_ROOT}/conductor/terms.md` and present the updated glossary diff to the user.
2.  **Autonomous ADR Reconciliation**:
    -   Cross-reference newly introduced patterns or modifications against active ADRs in `{PROJECT_ROOT}/conductor/adr/`.
    -   If an architectural trade-off was formalized, capture or update the relevant ADR.
3.  **Structured Synchronization Output**:
    -   Present document synchronization progress in distinct, structured sections:
        *   `### Extracted Domain Terms`
        *   `### ADR Updates & Alignment`
        *   `### Living Runbook Synchronization`
        *   `### Verification Audit`
4.  **Tech Stack & Guidelines Sync**:
    -   If tech stack / workflow altered: update `tech-stack.md` / `workflow.md`.
    -   If product capabilities / UX guidelines changed: update `product.md` / `product-guidelines.md` (present diff for approval).
5.  **Living Manual Testing Runbook Synchronization (`manual_testing/<domain>.md`)**:
    -   **Autonomous Sync Policy**: Extract verified steady-state test scenarios from `{PROJECT_ROOT}/conductor/tracks/<track_id>/manual_testing.md`.
    -   Reconcile into `{PROJECT_ROOT}/conductor/manual_testing/<domain>.md` using structured headings (`### Test <Domain>.<ID>`) without an `ask_question` confirmation gate.
    -   **Artifact Generation & Chat Reference**: Write the finalized domain manual testing runbook as a walkthrough artifact (`{ARTIFACT_DIR}/conductor_manual_testing_<domain>.md`, `ArtifactType: walkthrough`).
    -   **Chat Notification**: In your response to the user, you MUST explicitly state that the manual testing guide artifact has been created and provide a clickable markdown link to the file (e.g., `[conductor_manual_testing_<domain>.md](file://...)`).
6.  **Fixpoint Verification Gate**: Run the full 3-tier Fixpoint Audit (`/conductor-drift --check`) to verify zero drift.
7.  Commit documentation changes: `docs(conductor): Synchronize docs for track '<description>'`.

### Step 5: Track Completion & Next Steps Orchestration

This step occurs **only** after all plan tasks are marked `[x]` and Document
Synchronization has been handled.

1.  **Retrospective ADR Review**:
    -   Review the completed track's `spec.md` under "## Design Decisions" for any decisions recorded in the spec that were not captured as standalone ADRs.
    -   If unwritten decisions exist:
        -   **Print Candidates First**: Output all candidate decisions with rationale and spec quotes in chat FIRST.
        -   Then invoke `ask_question` with `is_multi_select: true` using neutral retrospective phrasing ("Some decisions from this track weren't captured as ADRs. Looking back, should any of these be recorded?").
        -   Write selected ADRs using the template and commit them.
2.  **Next Steps Elicitation Gate (Mandatory Turn Barrier)**:
    -   You MUST invoke `ask_question` to ask the user what they want to do next. Do NOT end the turn with a static summary or draft PR description without presenting this decision modal.
    -   *Question:* "All tasks and documentation for track '<track_name>' are complete. What would you like to do next?"
    -   *Options:*
        *   `"(Recommended) Test the implementation with the manual testing guide ([<domain>.md](file://...))"`
        *   `"Push changes / Create PR"`
        *   `"Run full code review (/conductor-review)"`
        *   `"Archive completed track and finish"`
        *   `"Keep track active and finish"`
    -   **MANDATORY:** End your turn after calling `ask_question`.
3.  **Execution of Selected Next Step**:
    -   If **Test with Manual Testing Guide**: Present the specific verification scenarios from `{PROJECT_ROOT}/conductor/manual_testing/<domain>.md` with CLI setup/reset commands and walk the user through testing.
    -   If **Push changes / Create PR**: Verify formatting, check git status, commit, and push.
    -   If **Review**: Transition directly into `/conductor-review`.
    -   If **Archive**: Move track folder to `conductor/archive/`, remove from `tracks.md`, and commit.
    -   If **Keep Track Active**: Leave the track folder in place.

## Guardrails

-   **Sequential Task Execution**: Implement tasks one at a time. Do not batch multiple plan tasks into a single unreviewed turn.
-   **Documentation-Only Manual Testing Invariant**: Document exact setup, seed, and reset commands in manual testing runbooks, but NEVER execute mutative database, environment reset, or teardown commands autonomously.
-   **Mandatory Completion Next-Steps Barrier**: When all plan tasks are `[x]` and document synchronization is complete, you MUST NOT go silent after printing summaries or draft PR descriptions. You MUST invoke `ask_question` to offer the user clear next steps (Manual testing with the guide, Pushing changes / Creating PR, Running `/conductor-review`, or Archiving the track).
