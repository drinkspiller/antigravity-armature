---
name: conductor-new-track
description: Start a new feature or bug fix track with a specification and phased plan. Use when asked to create a new track, start a feature, plan a bug fix, or run /conductor-new-track.
persona: Conductor
---

# Conductor New Track

## Overview

Initialize a new development track with an interactive specification and
planning workflow. Creates a track directory under `conductor/tracks/<track_id>/`
with `spec.md`, `plan.md`, `manual_testing.md`, `metadata.json`, and `index.md`, and registers it in
`conductor/tracks.md`.

## Protocol

### 1. Setup Verification

Before starting track creation:

1.  Verify the minimum viable project files exist:
    -   `{PROJECT_ROOT}/conductor/product.md`
    -   `{PROJECT_ROOT}/conductor/tech-stack.md`
    -   `{PROJECT_ROOT}/conductor/workflow.md`
    -   `{PROJECT_ROOT}/conductor/tracks.md`
2.  If any are missing, halt execution and instruct the user to run
    `/conductor_setup` first.
3.  Check for existing tracks in `{PROJECT_ROOT}/conductor/tracks/` to understand
    active work.

### 2. Infer Track Type and Scope

Determine whether this track is a:

-   **Feature**: New capabilities or enhancements
-   **Bug Fix**: Correcting unintended behavior
-   **Chore**: Maintenance, refactoring, dependencies, tech debt

### 3. Generate Track Identifier

-   Create a concise, URL-safe slug (e.g., `user-auth`, `fix-cart-summary`,
    `dark-mode`).
-   Verify `{PROJECT_ROOT}/conductor/tracks/<track_id>` does not already exist.

### 4. Codebase Reconnaissance

-   Before asking spec questions, inspect relevant source files and
    directories to understand existing patterns, interfaces, and
    constraints.
-   Use findings to inform the spec questions in the next step — questions
    must reference specific codebase context.

### 5. Interactive Spec & Design Elicitation (Grill Protocol)

Conduct a rigorous, one-question-at-a-time interview with the user to build a deep shared understanding before drafting the spec and plan.

-   **Domain Loading**: Silently load context by reading `{PROJECT_ROOT}/conductor/product.md` (for glossary/product context), `{PROJECT_ROOT}/conductor/tech-stack.md` (for technical constraints), and scanning existing `*/spec.md` files.
-   **Questioning Strategy**: Interview the user one question at a time across all spec sections (Problem Statement, Functional Requirements, Non-Functional Requirements, Scope Boundaries, Acceptance Criteria).
    -   Use `ask_question` with your recommended answer listed first (`(Recommended)`) alongside 2–4 other plausible options.
    -   Codebase reconnaissance informs your questions and recommendations,
        but NEVER replaces user dialogue.
    -   Follow branches where complexity, ambiguity, or trade-offs emerge.
    -   **MANDATORY:** End your turn after each `ask_question` call to wait
        for the user's answer.
-   **Domain Enforcement**: Actively challenge glossary conflicts against `product.md`, sharpen fuzzy language using explicit subjects and active voice, and cross-reference stated behavior against the codebase.
-   **Inline Design Decision & ADR Elicitation**: As architectural trade-offs emerge during questioning:
    -   Evaluate the 3-part gate: (1) Hard to reverse, (2) Surprising without context, (3) Real trade-off.
    -   If all three criteria are met, immediately prompt using `ask_question`: "This decision looks worth recording. Create an ADR?" (`["Yes", "No", "Skip all ADR prompts for this track"]`).
    -   If approved, scan `{PROJECT_ROOT}/conductor/adr/` for the next sequence number (`NNNN`) and write `{PROJECT_ROOT}/conductor/adr/NNNN-slug.md` using `adr_template.md`.
-   **Inline Glossary Elicitation (`terms.md`)**: If a question or decision introduces/refines a domain term not in `terms.md`, offer to add it inline via `ask_question` (`["Yes, with definition", "Yes, I'll write the definition", "No"]`).
-   **Inline ADR Elicitation**: If a decision implies a load-bearing behavioral contract or architectural rule (ordering requirement, initialization guard, call-sequence dependency), offer to capture it following the ADR Capture Protocol in `conductor_cdd_protocols.md` §10.
-   **Termination**: End the grill session when the user signals done ("done", "let's move on") or when natural convergence is reached and you propose ending via `ask_question`: "I think we've covered the key areas. Ready to draft the spec?" (`["Yes, draft the spec", "Not yet — I want to discuss [topic]"]`).
-   All resolved decisions must be recorded in the track spec under `## Design Decisions`.

### 6. Preliminary Specification Synthesis (In-Memory ONLY)

-   **Synthesize Draft in Memory**: Generate a comprehensive draft of the
    specification containing: `## Overview`, `## Functional Requirements`,
    `## Non-Functional Requirements`, `## Design Decisions`, `## Manual
    Verification Plan`, `## Acceptance Criteria`, `## Out of Scope`.
-   **MANDATORY HARDENING BARRIER**: Do NOT write `spec.md` to disk at this step.
    The specification MUST remain an in-memory draft until Step 10. You must
    NOT call `write_to_file` on `conductor/tracks/<track_id>/spec.md` or any
    canonical track artifact here.
-   **Interruption & Detour Recovery**: If the user asks a question, raises a
    technical concern, or takes a conversational detour (e.g., asset handling,
    styling, DB schema), answer the inquiry directly and then explicitly
    **RESUME** at Step 7 (Gap Analysis). Never skip directly to planning or
    code writing after an interruption.
-   Announce: *"I have synthesized a preliminary draft in memory. Proceeding to
    Gap Analysis."*

### 7. Structured Gap Analysis (7 Mandatory Categories)

-   Run a structured gap check against ALL 7 mandatory categories: 1. Error handling, 2. Edge cases, 3. Backwards compatibility, 4. Security (PII, auth, input validation), 5. Performance (scale, bundle size), 6. Accessibility, and 7. Testing strategy.
-   **Interruption Resilience**: If resuming after a user question, architectural detour, or asset tangent, do NOT jump directly to spec finalization. Explicitly assess and present findings across all 7 categories.
-   **Testing Strategy Classification**: Under Testing strategy, classify
    the track's manual testing depth:
    -   *Interactive / Stateful / Route / API Tracks*: Require a full
        `manual_testing.md` runbook with environment setup, CLI reset
        tooling, persona matrices, and sequential route test cases.
    -   *Pure Refactor / Utility / Chore Tracks*: Require a lightweight
        `manual_testing.md` with concise smoke and sanity checks alongside
        automated unit tests.
-   For each gap found, generate a concrete suggestion.
-   Present ALL findings as a numbered list in your regular markdown
    response first (where formatting renders properly).
-   Then, for **each individual gap**, call `ask_question` with a short
    question and options **tailored to that specific finding**. Do NOT
    combine all gaps into a single question. Each question should offer
    meaningful choices relevant to the nature of that gap.
-   **MANDATORY:** End your turn at each `ask_question` call.
-   After all individual gap questions have been answered, incorporate the
    user's per-gap decisions into your in-memory spec draft.
-   **Opportunities Selection:** If discovery mode identified opportunities:
    -   Present the brainstormed opportunities to the user using the
        `ask_question` tool with `is_multi_select: true`.
    -   For each selected opportunity, integrate it into Functional or Non-Functional Requirements.

### 8. Cross-Track Awareness & ADR Scan

-   Read `{PROJECT_ROOT}/conductor/tracks.md` and review the existing
    `*/spec.md` files.
-   **ADR Cross-Reference**: Scan `{PROJECT_ROOT}/conductor/adr/` (if it
    exists).
    -   To conserve tokens, perform a **title-scan** (reading filenames
        only) by default.
    -   Identify ADRs whose slugs contain domain terms that match the active
        terms identified in the current track's scope (based on
        `{PROJECT_ROOT}/conductor/terms.md`).
    -   For matching ADRs, load their full text to check for architectural
        constraints or precedents.
-   Identify: overlapping scope with existing tracks, sequencing
    dependencies, shared component opportunities, or contradictions with
    historical ADRs.
-   If conflicts/dependencies are found, present findings and **present
    options** using the `ask_question` tool: "Adjust scope", "Acknowledge
    dependency", "No action needed". Update the in-memory spec if requested.
-   If no issues found, announce "No cross-track conflicts detected" and
    proceed.

### 9. Devil's Advocate Stress Testing

-   Generate 2-3 challenges to the spec's assumptions based on codebase
    context.
-   You MUST format these challenges explicitly as: "What happens if [X]?", "Have you considered [Y]?", or "This assumes [Z] — is that still valid?"
-   Present ALL challenges as a numbered list in your regular markdown
    response first (with full context, code references, and reasoning).
-   Then, for **each individual challenge**, call `ask_question` with the
    challenge as the question and options **tailored to that specific
    concern**. Do NOT combine all challenges into a single question.
-   **MANDATORY:** End your turn at each `ask_question` call.
-   After all individual challenge questions have been answered, apply the
    user's per-challenge decisions to the in-memory spec draft.
-   **ADR Capture Sweep**: For each challenge the user chose to address, evaluate
    whether the fix establishes an architectural decision that extends beyond
    this track. If so, follow the ADR Capture Protocol defined in
    `conductor_cdd_protocols.md` §10.

### 10. Spec & Manual Testing Materialization & Final Confirmation

-   ONLY NOW, write the canonical specification to `{PROJECT_ROOT}/conductor/tracks/<track_id>/spec.md` using `write_to_file` with `IsArtifact: true` (using `ArtifactType: other`).
-   The spec MUST contain these sections: `## Overview`, `## Functional
    Requirements`, `## Non-Functional Requirements`, `## Design Decisions`,
    `## Manual Verification Plan`, `## Acceptance Criteria`, `## Out of
    Scope`.
-   Write the initial
    `{PROJECT_ROOT}/conductor/tracks/<track_id>/manual_testing.md` based on
    `manual_testing_template.md` tailored to the classified testing depth.
-   Ensure it incorporates all accepted suggestions, gap analysis decisions, and devil's advocate refinements.
-   Use `notify_user` with `PathsToReview` pointing to the updated `spec.md`
    and `manual_testing.md` to request a final review.
-   **Present options** using the `ask_question` tool: "Approve" (Proceed to
    planning), "Revise" (Suggest manual edits). Do not proceed until
    approved.
-   **MANDATORY:** End your turn and wait for explicit user approval before
    proceeding to plan generation.

### 11. Interactive Plan Generation

-   Verify the Milestone Pre-Plan Checklist is complete.
-   Read the confirmed spec and `{PROJECT_ROOT}/conductor/workflow.md`.
-   Generate a hierarchical plan with Phases, Tasks, and Sub-tasks.
-   Include status markers `[ ]` for EVERY task and sub-task.
-   **Developer Test Tooling Tasks**: If the track introduces new routes,
    state guards, or flags, ensure Phase 1 includes explicit tasks for
    developer reset tooling, CLI scripts, or fixture seeding needed by
    `manual_testing.md`.
-   **Verification Bridge**: Scan any ADR files created or referenced during
    this track for `## Confirmation` sections. For each verification
    checkbox `[ ]` defined in an ADR's Confirmation section, inject a
    corresponding explicit verification task into the relevant Phase of
    `plan.md` (e.g., `[ ] Verify ADR-0001: <criteria>`).
-   **CRITICAL:** If `workflow.md` defines phase checkpointing, you must
    inject Phase Completion meta-tasks at the end of each Phase.
-   Write this to `{PROJECT_ROOT}/conductor/tracks/<track_id>/plan.md` using
    `write_to_file` with `IsArtifact: true` (using `ArtifactType:
    implementation_plan`).
-   Use `notify_user` with `PathsToReview` pointing to the written `plan.md`
    to request review.
-   **Present options** using the `ask_question` tool: "Approve" (Proceed to
    track creation), "Revise" (Suggest changes). Do not proceed until
    approved.
-   **MANDATORY:** End your turn and wait for explicit user approval before
    finalizing artifacts or starting implementation.

### 12. Generate Remaining Track Artifacts

-   Create `{PROJECT_ROOT}/conductor/tracks/<track_id>/metadata.json`
    containing: `track_id`, inferred `type`, `status` (set to `planned`),
    current `createdAt` and `updatedAt` timestamps, and the original
    `description`.
-   Write `{PROJECT_ROOT}/conductor/tracks/<track_id>/index.md` containing a
    summary and relative links to `spec.md`, `plan.md`, `manual_testing.md`,
    and `metadata.json`.
-   Append the new track to `{PROJECT_ROOT}/conductor/tracks.md`: `- [ ]
    **Track: <Track Title>** _Link:
    [./tracks/<track_id>/](./tracks/<track_id>/)_`

### 13. Commit Changes

-   Commit the new track directory and the updated `tracks.md` using VCS
    commands.
-   The commit message MUST be: `chore(conductor): Add new track
    '<description>'`

### 14. Confirm Completion

Display: "✅ Track `<track_id>` created! Run
`/conductor-implement` to start working through the plan."

## Guardrails

-   **Compound Directive Shielding**: If the user prompt includes compound instructions (e.g., "create a track and implement it immediately in foo.ts"), do NOT start implementation or write code. Strictly limit scope to track planning and state that implementation must wait until the plan is approved.
-   **Turn-Ending Barriers**: Enforce strict synchronous pauses at Steps 5, 7, 9, 10, and 11 via `ask_question`. Never batch questions or skip ahead.
-   **Pre-Materialization Barrier**: Hold `spec.md` in memory during Step 6. Never write `spec.md` to disk until all Gap Analysis and Devil's Advocate barriers are complete.
-   **Structured 7-Category Gap Analysis**: Always evaluate all 7 dimensions (Error handling, Edge cases, Backwards compatibility, Security, Performance, Accessibility, Testing strategy) even when resuming from conversational interruptions.

