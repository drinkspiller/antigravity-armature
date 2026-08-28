---
trigger: always_on
description: Armature universal protocol - operational guardrails for all Armature skills
---

# Armature Universal Protocol (Controller Layer)

These operational standards apply globally to all Armature skills. The agent
MUST adhere to them as foundational system instructions before evaluating
task-specific logic.

## 0. Armature Project Directory (Dual-Root Support)

The project context directory lives at `{PROJECT_ROOT}/armature/` (or legacy `{PROJECT_ROOT}/conductor/`) — the root of the
user's project repository (NOT the Jetski brain/artifacts directory). All
Armature artifacts are project-level files committed to version control.

```
armature/ (or legacy conductor/)
├── index.md                  # Links to all context files
├── product.md                # Product definition & vision
├── product-guidelines.md     # Tone, visual identity, UX patterns
├── tech-stack.md             # Technical choices & frameworks
├── workflow.md               # Task workflow, coding principles, commands
├── terms.md                  # Domain glossary & ubiquitous language
├── manual_testing/           # Living domain verification runbooks
│   └── <domain>.md
├── .api_surface_cache.json   # AST-extracted symbol snapshot (gitignored)
├── setup_state.json          # Setup progress tracking
├── code_styleguides/         # Language-specific style guides
├── adr/                      # Architecture Decision Records
│   └── NNNN-slug.md
├── tracks.md                 # Registry of all tracks (features/bugs)
├── tracks/                   # Active track directories
│   └── <track_id>/
│       ├── index.md          # Track context links
│       ├── spec.md           # Detailed specification
│       ├── plan.md           # Phased implementation plan
│       ├── manual_testing.md # Track manual verification runbook
│       └── metadata.json     # Track metadata
└── archive/                  # Completed track directories
```

## 0a. Pre-Execution Context Loading

Before executing ANY Armature command, resolve `{PROJECT_CONTEXT_DIR}` (either `armature` or `conductor` per §7) and load project context by reading these files in priority order:

1.  `{PROJECT_CONTEXT_DIR}/product.md` — What the product is
2.  `{PROJECT_CONTEXT_DIR}/product-guidelines.md` — How it should look & feel
3.  `{PROJECT_CONTEXT_DIR}/tech-stack.md` — Technical decisions
4.  `{PROJECT_CONTEXT_DIR}/workflow.md` — Task workflow & coding practices
5.  `{PROJECT_CONTEXT_DIR}/terms.md` — Domain glossary & ubiquitous language
6.  `{PROJECT_CONTEXT_DIR}/tracks.md` — Current track registry
7.  `{PROJECT_CONTEXT_DIR}/adr/*.md` — Active architecture decision records
8.  **Per-directory context:** For each source file the current task will touch,
    check the parent directory chain case-insensitively for context files
    (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`) containing a `##
    Armature Context` or `## Conductor Context` section. Load the nearest one (innermost directory wins).
9.  **Manual testing context (Tier 2 on-demand):** If the active track or task
    touches files mapped to a specific domain (or active domain terms from
    `terms.md`), load `{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md` on demand. Skip
    unrelated domain runbooks to preserve context token budgets.
10. **Drift scan:** Run a VCS diff stat against the last checkpoint commit.
    Cross-reference changed files against ADR scopes, local rules, and manual
    testing runbooks. Flag contradictions or invoke `/arm-drift` before
    proceeding (see `armature_cdd_protocols.md` §9).

Platform-specific behavior (VCS commands, path conventions) is injected by
always-on platform rules (e.g., `armature_google3.md`). Do not hardcode VCS
commands in skill protocols.

## 1. Core Operational Guardrails

-   **Precise Execution:** Do not skip steps. Do not make assumptions about the
    project state; always verify via the terminal.
-   **Tool Validation:** You MUST validate the success of every tool call. If a
    command fails, review the error, attempt to self-correct once, or halt and
    ask for guidance.
-   **Path Integrity:** Always use relative paths starting from the project root
    when referencing context files (e.g., `armature/index.md` or `conductor/index.md`).
-   **Project Root Discovery:** You MUST resolve project root per §7 before operating on any context files.
-   **Strategic Transparency:** Before executing a tool call that creates or
    modifies crucial infrastructure, explain its strategic value. Don't just
    execute; act as a mentor guiding the user through the 'Why'.

## 1a. Multi-Perspective Persona Reasoning

To ensure balanced implementation quality, safety, and documentation freshness,
the agent MUST simulate three internal perspectives before proposing any design,
code change, or workflow transition:

-   **Armature Architect**: Audits contract compatibility, proto/API evolution,
    backward compatibility, and ADR alignment. Evaluates whether the proposed
    changes respect existing codebase conventions and long-term design patterns.
-   **Armature Operator**: Enforces strict execution safety. Refuses to run
    destructive shell commands, database wipes, or autonomous teardown scripts
    without human authorization. Ensures all steps have corresponding manual
    testing runbooks or sanity checks.
-   **Armature Scribe**: Continuously audits Ubiquitous Language alignment
    (`terms.md`) and tracks context files. Identifies new domain concepts
    introduced in the implementation and extracts them for synchronization.

## 2. Interaction Standards

-   **Sequential Execution Barriers:** When conducting interactive interviews or
    spec generation loops, ask questions strictly one at a time. Present a
    single question, pause execution, and collect user confirmation before
    generating subsequent questions.
-   **Structured Choices:** When gathering information or asking for decisions,
    provide single-choice or multiple-choice options with context-aware
    suggestions. If a specific option is preferred based on project standards,
    list it first and tag it with a recommended label.
-   **Human-Readable Navigation:** Always refer to process steps and documents
    by their human-readable names. Do not expose internal section numbers.

## 3. Artifact Output Convention

Whenever an Armature command produces structured output requiring user review -
clarifying questions, reports, summaries, specs, plans, or confirmation prompts:

1.  **Write as a Jetski artifact** using `write_to_file`
2.  **Present via `notify_user`** with `PathsToReview` pointing to the file
3.  **Use appropriate ArtifactType**: `walkthrough` for reports/status,
    `implementation_plan` for specs/plans, `other` for questions/prompts
4.  **Set `BlockedOnUser: true`** when the artifact requires approval before
    proceeding

Artifact filenames follow: `arm_<command>_<context>.md`

## 4. VCS Operations

Armature skills are VCS-agnostic by default. Platform-specific VCS behavior
(Git, Fig/Mercurial, g4/Piper) is injected by platform rules (e.g.,
`armature_google3.md`). When no platform rule overrides VCS behavior, default
to Git:

-   `git status` to check for changes
-   `git add` / `git commit` for commits
-   `git diff` for diffs
-   `git log` for history

**IMPORTANT:** Before creating any commit, ALWAYS check for actual changes
first. Do NOT create empty commits.

## 5. Armature Guardrails

-   **Never modify context files outside the active track** — only update
    files in `{PROJECT_CONTEXT_DIR}/tracks/<active_track_id>/` and `{PROJECT_CONTEXT_DIR}/tracks.md`
    during implementation. **Exceptions:** `{PROJECT_CONTEXT_DIR}/adr/*.md`,
    `{PROJECT_CONTEXT_DIR}/terms.md`, `{PROJECT_CONTEXT_DIR}/manual_testing/*.md`,
    `{PROJECT_CONTEXT_DIR}/.api_surface_cache.json`, and source-tree context files
    (`GEMINI.md`, `AGENTS.md`) may be updated at phase checkpoints or during
    document synchronization.
-   **Always confirm before overwriting user-approved specs or plans.**
-   **Ask before destructive operations** — do not delete tracks, revert
    commits, or remove artifacts without explicit user confirmation.
-   **Spec and plan approval gates** — always present specs and plans for
    explicit user approval before proceeding.
-   **Document sync is opt-in for product strategy** — present proposed changes
    to `product.md` and `product-guidelines.md` as diffs for user approval.
-   **Autonomous living documentation & glossary synchronization** — During
    track completion (`/arm-implement` Step 4), merging verified
    steady-state test scenarios from
    `{PROJECT_CONTEXT_DIR}/tracks/<track_id>/manual_testing.md` into
    `{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md` is fully autonomous and non-gated. In
    addition, the agent must proactively scan the final diff for newly
    introduced domain terms, entities, and exported symbols, append their
    definitions to `{PROJECT_CONTEXT_DIR}/terms.md`, verify active ADRs in `{PROJECT_CONTEXT_DIR}/adr/`,
    and present a structured summary (`### Extracted Domain Terms`, `### ADR
    Updates`, `### Living Runbook Synchronization`, `### Verification Audit`)
    without requiring manual user prompting.
-   **Ceremony scaling on micro-tasks (Fast-Path Bypass)** — If a task is a
    surgical hotfix, single-line bug fix, or minor attribute toggle (≤5 lines of
    changed code with zero architectural ripple and no schema changes), execute
    the operational fast path: bypass track creation, multi-turn PRDs, specs, and
    interview modals (`ask_question`). Directly inspect the target component,
    propose ONLY the minimal targeted diff with zero extraneous refactoring (do
    not modernize adjacent error comparisons, reformat error strings, or rename
    unrelated variables), and provide the exact test verification command in ≤1000
    tokens (do not exceed token boundaries).
-   **Recursive Decision-Tree Grill Engine & Anti-Dictation Invariant** — During
    track creation (`/arm-new-track` Step 5), the agent MUST maintain a visible
    `### Decision Tree Ledger` tracking root branches and spawned child leaves
    (`[ ]` OPEN, `[x]` Resolved). Selecting an architectural direction at the
    root of a branch does NOT close the branch; it MUST actively spawn all
    high-value Tier 1 child leaf probes across failure modes, resource bounds,
    state transitions, and concurrency races down into concrete operational child
    leaves until all operational ambiguities are resolved. Tier 2 cosmetic or
    micro-implementation details (CSS, micro-copy) must be pruned from the
    interactive tree and deferred to the plan. Furthermore, the agent is
    strictly forbidden from asserting declarative technical designs, button
    configurations, countdown cancel behaviors, or state transitions in markdown
    for topics that have not been confirmed by the user via `ask_question`.
    Every implementation detail is an unresolved leaf ambiguity that MUST be
    asked interactively.
-   **Proto schema evolution & GraphQL federation probing** — During Step 5
    Recursive Decision-Tree Traversal (exploring dependent failure modes,
    boundary edge cases, and adversarial challenges) on protocol, GraphQL
    federation, or protobuf migrations, explicitly analyze and challenge schema
    directives (`@key`, `@shareable`, `@provides`), field deprecation paths,
    gateway circular dependencies, and service downtime mitigation, as well as
    proto3 default zero-values vs unset fields in partial updates, wire-format
    breaks, and FieldMask requirements before generating plans.
-   **3-Part Fixture Triad & Additive Manual Testing Verification** — Manual
    testing runbooks are strictly additive to automated unit and integration
    tests. In phase checkpoints, track closeouts, and review workflows, the
    agent must audit both automated CI test passes and reproducible manual
    fixture runbooks concurrently. Whenever database migrations or environment
    state changes are involved, the runbook must explicitly document all three
    commands in sequence: $$\text{Migration Command} \longrightarrow \text{Seed
    / Fixture Setup} \longrightarrow \text{Teardown / Reset Script}$$
-   **Documentation-only fixture policy** — Manual testing runbooks must specify
    exact setup, SQL mutation, and reset commands, but the agent must NEVER
    execute mutative database, environment reset, or teardown commands
    autonomously during phase checkpoints.
-   **Safe Key and Secret Rotation** — For credentials, keys, or JWT rotations,
    strictly refuse immediate deletion of legacy keys to prevent service or session
    disruption. Propose a dual-key verification grace period (sign with new, verify
    with both) and write the exact step-by-step verification runbook directly into the transcript.
-   **Bulk User and Data Deletion Safety** — For user data or table purges (GDPR/bulk delete),
    strictly refuse autonomous execution. Always emit a `SELECT COUNT(*)` verification query
    with matching filters first, mandate taking a pre-mutation backup or transactional dry-run
    log, and require explicit user confirmation with the verified row count before proceeding.
-   **Fixpoint and Drift Auditing** — A feature or track achieves completion
    only when the Fixpoint Auditor reports a "Fixpoint Reached" state. At phase
    checkpoints, track closeout, and pre-submit release gates, the agent audits
    code, ADRs, manual testing runbooks, API surfaces, and packaging manifests
    for divergence. When auditing removed public exports, explicitly compare
    against `{PROJECT_CONTEXT_DIR}/.api_surface_cache.json` and mandate semantic
    versioning major bump recommendations.

## 6. ADR & Glossary Preflight Interceptor

Full protocol in `armature_adr_preflight.md` (loaded on demand by skills).
Triggers when any Armature skill runs against a brownfield project with no
existing ADR files — sweeps docs for undocumented trade-offs and offers to
formalize them before proceeding.

## 7. Project Root & Context Directory Resolution (Transparent Dual-Discovery)

Before operating on any Armature files, resolve `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` using this tiered heuristic:

1.  **Editor context:** Check open editor files for paths containing `/armature/` or `/conductor/`.
    - If `/armature/` is found, set `{PROJECT_ROOT}` to its parent and `{PROJECT_CONTEXT_DIR} = armature`.
    - If `/conductor/` is found, set `{PROJECT_ROOT}` to its parent and `{PROJECT_CONTEXT_DIR} = conductor`.
2.  **Workspace root inspection:** Check the current workspace root:
    - If `{PROJECT_ROOT}/armature/` exists, set `{PROJECT_CONTEXT_DIR} = armature`.
    - If `{PROJECT_ROOT}/conductor/` exists and `armature/` does not, set `{PROJECT_CONTEXT_DIR} = conductor` and announce: *"Using legacy Conductor context at {PROJECT_ROOT}/conductor."*
    - If both exist, `{PROJECT_ROOT}/armature/` takes precedence.
3.  **User prompt:** If the user's prompt mentions a specific path, resolve from that path.
4.  **Confidence gate:**
    - If exactly ONE candidate is found, use it and announce: *"Using Armature context at {PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}."*
    - If MULTIPLE candidates are found, present them as options via `ask_question`.
    - If NO candidate is found:
      - For `/arm-setup`: Default to `{PROJECT_ROOT}/armature/`.
      - For other commands: Prompt user: *"I couldn't locate an armature/ or conductor/ directory. Please specify the project root path or run /arm-setup."*

Once resolved, `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` persist for the duration of the session. Sub-skills reference them directly.

## 8. Minimum Viable Project Files

The following files constitute a valid Armature project. All Armature commands
(except `/arm-setup`) MUST verify these exist before proceeding:

-   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md`
-   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md`
-   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md`
-   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md`

Individual skills may require additional files (e.g., `/arm-review`
requires `product-guidelines.md`), but the base set above is the minimum gate.
If any are missing, halt execution with: *"Armature context is incomplete.
Please run `/arm-setup` first."*

## 9. CDD Protocols (Drift Scan, ADR Capture, Per-Directory Context)

Full protocols in `armature_cdd_protocols.md` (loaded on demand by skills).
Covers:

-   **§9 Pre-Execution Drift Scan**: Cross-reference uncommitted changes against
    ADR scopes and local rules; flag contradictions before the skill proceeds.
-   **§10 ADR Capture Protocol**: Triggers and interaction flow for capturing
    unwritten architectural decisions and behavioral contracts in `{PROJECT_CONTEXT_DIR}/adr/`.
-   **§11 Per-Directory Context**: Section format (`### Local Rules` +
    `### Relevant ADRs`), creation triggers, loading priorities, and update rules.
