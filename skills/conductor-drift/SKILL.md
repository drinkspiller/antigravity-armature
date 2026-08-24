---
name: conductor-drift
description: Audit and resolve documentation drift, spec divergence, and packaging inconsistencies across Conductor projects. Use when asked to audit drift, check fixpoint, run /conductor-drift, or verify spec-to-code alignment.
persona: Conductor Fixpoint Auditor
---

# /conductor-drift — Fixpoint Auditor

**Purpose:** Audit project documentation, active specifications, Architecture
Decision Records (ADRs), domain manual testing runbooks, API surfaces, and
installer packaging for divergence. Coordinates automated and guided
reconciliation until the project reaches a verified **Fixpoint Reached** state.

## Protocol

### Step 1: Scope & Mode Resolution

1.  **Parse Arguments**:
    -   `--scope=docs`: Phase 1 only (audit project files, ADRs, and glossary).
    -   `--scope=phase`: Incremental Phase Checkpoint mode (audit files changed in active phase against ADRs and runbooks without blocking WIP code).
    -   `--scope=code`: Phase 2 only (audit `.api_surface_cache.json`, public exports, and per-directory `## Conductor Context` boundaries).
    -   `--scope=meta`: Phase 3 only (audit `install.sh`, `install.bat`, `plugin.json`, `marketplace.json`, and `README.md` packaging arrays and version agreement).
    -   `--fix`: Automatically apply mechanical auto-fixes (installer arrays, version alignment, table freshness, and `.api_surface_cache.json` refresh).
    -   `--check`: Non-interactive CI / pre-submit validation mode (verifies fixpoint state and outputs pass/fail status).
2.  **Resolve Project Root**: Follow Conductor Protocol Rule 7 to locate `{PROJECT_ROOT}`.

### Step 2: Native Scan Execution

Execute the audit across the three tiers (or the requested scope) using native file inspection tools:

1.  **Incremental Phase Checkpoint Mode (`--scope=phase`)**:
    -   Determine which files and directories were modified or added in the active track's current phase (using the active track's `plan.md` and/or VCS diff).
    -   For each changed file:
        -   Identify matching ADRs in `conductor/adr/` and directory context files (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`). Verify that any new architectural decisions or constraints introduced by the changes are recorded as ADRs.
        -   Identify matching manual testing runbook scenarios in the active track's `manual_testing.md` or domain guides in `conductor/manual_testing/`.
        -   If a new route handler, state guard, or major logic flow was added, verify it has corresponding manual verification test cases. If missing, report a `[WARNING]`.
        -   Audit modified source tree context files for standard boundary tags.
    -   Report all findings as advisory warnings (`[WARNING]`) without blocking work-in-progress code execution.
2.  **Phase 1: Project Documentation Fixpoint**:
    -   Verify minimum viable project files exist (`product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`).
    -   Audit ADR sequence numbers, filename format (`NNNN-slug.md`), and MADR section schemas (`## Context`, `## Decision`, `## Confirmation`).
    -   Audit domain manual testing runbooks (`conductor/manual_testing/<domain>.md`) for standard `### Test <Domain>.<ID>` headers.
    -   Audit active track specifications (`conductor/tracks/<track_id>/spec.md`) for required `## Manual Verification Plan` sections.
3.  **Phase 2: Codebase & Implementation Fixpoint**:
    -   Compare public exported symbols against `.api_surface_cache.json` and `conductor/terms.md`. Flag untracked API symbols.
    -   Inspect source tree context files (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, `AGENT.md`) for standard `START`/`END` boundary tags and valid ADR references.
4.  **Phase 3: Meta, Packaging & Release Manifest Fixpoint (Developer Mode)**:
    -   Verify all sub-skills in `skills/` are registered in `install.sh` (`SUB_SKILL_NAMES`), `install.bat`, and `README.md`.
    -   Verify rule files in `rules/` are in `RULE_FILE_NAMES` / `ALL_TARGET_FILES`.
    -   Verify setup asset templates in `skills/conductor-setup/assets/` are in installer target arrays.
    -   Verify 100% version agreement across `install.sh` (`VERSION=`), `install.bat` (`set "VERSION="`), `plugin.json` (`"version"`), `.claude-plugin/marketplace.json`, and `CHANGELOG.md`.

**Render the Fixpoint Audit Report**:
Always print the complete audit results directly in your response:
-   If no discrepancies exist: Print `✅ [Fixpoint Reached] Zero drift detected across all tiers.` (or in the active phase scope).
-   If discrepancies exist: Group findings by phase/scope with severity tags (`[ERROR]`, `[WARNING]`, `[INFO]`) and indicate `[Auto-Fixable]` status.

### Step 3: Interactive Reconciliation & Remediation

1.  **Zero Drift Detected**:
    -   Display: `✅ [Fixpoint Reached] Zero drift detected across all tiers.`
    -   Conclude execution.

2.  **Mechanical Drift Detected**:
    -   Display the detected mechanical issues (e.g., installer array omissions, version stamp mismatches, or `README.md` table gaps).
    -   If `--fix` flag was provided, apply fixes directly using file editing tools and print the applied changes.
    -   Otherwise, prompt the user via `ask_question`: "Mechanical drift detected in packaging/manifests. Apply automatic fixes?" with options `["(Recommended) Apply mechanical fixes", "Review discrepancies first", "Skip for now"]`.
    -   Apply approved fixes surgically.

3.  **Semantic / Architectural Drift Detected**:
    -   **Report First**: Output all semantic issues as formatted Markdown sections in your response FIRST, detailing the conflicting files, ADR citations, and spec quotes.
    -   For each semantic divergence, call `ask_question` with tailored choices:
        *   *ADR vs Code divergence*: `["Update code to match ADR", "Update ADR to reflect new decision", "Acknowledge as tech debt"]`
        *   *Missing manual testing runbook*: `["Generate domain runbook scenarios now", "Add task to active plan", "Skip"]`
        *   *Unrecorded glossary term*: `["Add definition to terms.md", "Ignore symbol"]`
    -   Incorporate user decisions into the respective files.

### Step 4: Verification & Checkpoint Commit

1.  Re-verify the modified files to confirm all issues are resolved and Fixpoint is reached.
2.  If fixes were made to project or packaging files, offer to commit them using VCS commands with message:
    `chore(conductor): Reconcile documentation drift and packaging manifests`

## Guardrails

-   **Deterministic In-Memory Scans**: The agent must inspect files directly using native tools without consuming excessive context.
-   **Documentation-Only Invariant**: Do NOT execute mutative database resets or environment teardowns during manual testing scenario reconciliation.
-   **No Destructive Fallbacks**: Never delete unlinked ADRs or active track directories without explicit double-confirmation.
