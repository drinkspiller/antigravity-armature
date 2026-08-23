# Changelog

All notable changes to Antigravity Conductor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.16.0] - 2026-08-23

### Added
- **CDD & SDD Live Evaluation Benchmark Suite (`evals/cdd_sdd_benchmark/`)**:
  - Standalone, zero-external-dependency live evaluation harness (`run_cdd_sdd_eval.py`) with 8-scenario, 32-criterion test suite comparing 7 industry frameworks (`jetski-conductor-dev`, `canonical_conductor`, `conductor_oss`, `bmad_method`, `memory_bank`, `github_spec_kit`, `openspec`).
  - Automated LLM Meta-Judge synthesis via `gemini-3.1-pro-preview` generating composite scores (0–100), rank, winner declaration, and markdown report artifacts.
  - Dynamic ceremony scaling rule for micro-hotfixes (<5 lines, zero ripple) bypassing heavy PRD barriers.
  - Adversarial proto schema evolution challenge rule during Step 7 / Step 9 Gap Analysis for proto3 default zero-value collisions in partial updates.
  - Additive manual testing runbook verification rule auditing living runbooks concurrently with automated unit/integration test suites.
- **SkillOpt Optimization Benchmark Suite (`evals/skillopt/`)**:
  - Extended training tasks `TRAIN_17`–`TRAIN_19` and validation tasks `VAL_14`–`VAL_15` covering micro-hotfix ceremony scaling, proto3 field presence evolution, and additive runbook auditing.

## [0.15.0] - 2026-08-23

### Added
- **Conductor Fixpoint Auditor (`/conductor-drift`)**: Dedicated command skill (`skills/conductor-drift/SKILL.md`) natively auditing divergence across project documentation, ADRs, domain manual testing runbooks, API surfaces (`.api_surface_cache.json`), and packaging manifests.
- **3-Tier Audit Architecture**:
  - *Phase 1 (Docs & Specs)*: Audits cross-document consistency, ADR schemas/sequences, domain runbook scenarios, and specification completeness.
  - *Phase 2 (Code & Interfaces)*: Compares public exports against `.api_surface_cache.json` and audits per-directory `## Conductor Context` boundary integrity.
  - *Phase 3 (Meta & Packaging)*: Audits `install.sh`, `install.bat`, `plugin.json`, `marketplace.json`, and `README.md` for installer array completeness and version stamp fixpoints.
- **Automated Lifecycle Drift Hooks**:
  - *Incremental Checkpoints*: Fast incremental diff scans at phase checkpoints in `/conductor-implement` Step 3.
  - *Track Completion Gate*: Mandatory Fixpoint verification in `/conductor-implement` Step 4 before archiving.
  - *Review Gate*: Added `Fixpoint Audit: [Pass/Fail]` to `/conductor-review` checklist and `review.md`.
  - *Ambient Health Banner*: 1-line passive Fixpoint health summary in `/conductor-status` and `/conductor-chat`.
- **29-Scenario SkillOpt Benchmark Suite**: Expanded `evals/skillopt/` with 29 multi-skill evaluation tasks (16 training, 13 validation) and enhanced candidate retry resilience in `run_optimizer.py`.

## [0.14.0] - 2026-08-23

### Added
- **Manual Testing Guide Protocol**: Living, domain-organized manual testing runbooks stored at `conductor/manual_testing/<domain>.md` with environment prerequisites, CLI fixture setup, persona matrices, and error resilience.
- **Tiered Testing Strategy Classification**: Structured testing classification in `/conductor-new-track` Step 7 Gap Analysis, requiring full runbooks for stateful/route tracks and lightweight smoke checks for utility chores.
- **Specification `## Manual Verification Plan` Section**: Enforced dedicated manual testing section in all generated track specifications.
- **Developer Test Tooling Injection**: Automated injection of fixture seeding and CLI reset tasks into `plan.md` alongside feature code.
- **Autonomous Runbook Synchronization**: Fully automated synchronization of steady-state manual testing scenarios into `conductor/manual_testing/<domain>.md` upon track completion (`/conductor-implement` Step 4), generating walkthrough artifacts and clickable chat links.
- **Continuous Runbook Maintenance**: `/conductor-chat` automatically updates domain manual testing guides and outputs walkthrough artifacts with chat links when new functionality or behavioral changes are introduced.
- **Additive Manual Testing Review Audit**: Injected `Manual Testing Runbook: [Pass/Fail]` into `/conductor-review` checklist and `review.md`.
- **SkillOpt Evaluation Suite**: Integrated evaluation test harness under `evals/skillopt/` (`run_optimizer.py`, `tasks/train.jsonl`, `tasks/val.jsonl`, and documentation).
- **Setup Asset `manual_testing_template.md`**: Bundled canonical manual testing template in `skills/conductor-setup/assets/`.

### Fixed
- **Pre-Materialization Hardening Barrier & Detour Recovery**: Enforced in-memory draft retention until all gap analyses and devil's advocate challenges complete, with explicit resumption barriers after user detours in `/conductor-new-track`.
- **Neutral Retrospective ADR Prompting**: Step 5 in `/conductor-implement` uses neutral retrospective wording rather than referencing "archiving" before track disposition is chosen.

## [0.13.1] - 2026-08-17

### Fixed

-   **Enforce Mandatory Interactive Gating in `conductor-new-track`**: Added
    unyielding synchronous turn-ending stop barriers at Steps 5 (Grill
    interview), 8 (Gap analysis), 10 (Devil's advocate), 11 (Spec approval), and
    12 (Plan approval).
-   **Eliminated Autonomous Skip Loophole**: Removed the permissive clause
    allowing agents to bypass user dialogue when codebase context is available.
-   **Compound Prompt Shielding**: Added explicit guardrails preventing agents
    from prematurely executing downstream commands (e.g., `/diagnose` or `Fix`)
    before completing all interactive track creation milestones.

## [0.13.0] - 2026-08-14

### Changed

-   **Subsumed Invariants into ADRs and Local Rules**: Eliminated `conductor/invariants.md` to prevent fragmentation across architectural decisions and invariant rules.
-   **MADR Schema Alignment**: Behavioral contracts, ordering constraints, and safety guards are now recorded directly as Architecture Decision Records in `conductor/adr/*.md` using standard MADR structure (`## Decision` and `## Confirmation` verification tasks).
-   **Per-Directory Context Scoping**: Local conventions and failure handling rules are recorded in `## Conductor Context` (`### Local Rules` and `### Relevant ADRs`) within directory-level agent context files (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`).
-   **Protocol & Skill Harmonization**: Rebranded §10 in `conductor_cdd_protocols.md` to **ADR Capture Protocol**, and updated `/conductor-setup`, `/conductor-new-track`, `/conductor-implement`, and `/conductor-review` to verify ADRs and local rules directly.

## [0.12.0] - 2026-08-14

### Changed

-   **Terminology Scrubbing**: Scrubbed lingering internal references and standardized artifact phrasing across all skill files and rules.
-   **Installer Fixes**: Fixed Windows uninstaller (`install.bat`) rule cleanup loop and updated version references to `v0.12.0`.
-   **Documentation**: Updated `README.md` to align the "What Gets Installed" table with current kebab-case skill paths and rules.

## [0.11.1] - 2026-07-20

### Added

-   **Agent Plugin Manifests**: Root `plugin.json` (v0.11.1) and `.claude-plugin/marketplace.json` for agent plugin auto-discovery across `agy` (Antigravity CLI) and Claude Code.

### Changed

-   **Co-located Setup Assets**: Relocated setup templates into `skills/conductor-setup/assets/` to make skill subdirectories completely self-contained.
-   **Enhanced Modal Rules**: Updated `rules/conductor_antigravity.md` with enhanced `ask_question` modal rendering guardrails and report-first interaction standards.
-   **Installer & Docs**: Updated `install.sh`, `install.bat`, and `README.md` to support `assets/` and dual plugin manifests.

## [0.11.0] - 2026-07-20

### Breaking

-   **Consolidated Grill into `conductor-new-track`**: Deleted
    `conductor_newTrack_grill` and `conductor_newTrack_discovery`. Grilling is
    now the default one-question-at-a-time interview protocol inside
    `conductor-new-track` Step 5.
-   **Kebab-Case Skill Renaming**: Renamed all sub-skill directories to
    kebab-case hyphens (`conductor-setup`, `conductor-new-track`,
    `conductor-implement`, `conductor-status`, `conductor-review`,
    `conductor-revert`, `conductor-chat`). Added automatic installer cleanup
    (`migrate_to_v0_11_0`) to remove deprecated underscore folders.

### Changed

-   **Per-Directory Context Protocol**: Updated `conductor-implement` Step 3.3,
    `conductor_cdd_protocols.md` §11, `conductor-setup` Artifact 10, and
    `conductor_protocol.md` §0a item 9 to:
    -   Discover agent context files case-insensitively (`GEMINI.md`,
        `CLAUDE.md`, `AGENTS.md`, `AGENT.md`). Append to existing files without
        creating duplicates; prompt user for preferred filename when multiple or
        zero files exist.
    -   Use reason-driven creation based on architectural justification
        (interacting services, stateful controllers, local invariants, domain
        gotchas) rather than arbitrary file-count thresholds.
-   **Report First, Ask Second**: Updated `conductor_antigravity.md` and
    `conductor-implement` Step 5.1 (Retrospective ADR Review) to mandate
    printing full context, trade-off summaries, and spec quotes in the main chat
    response before calling `ask_question`.

## [0.3.0] - 2026-06-22

### Breaking

-   **Removed hub skill** (`conductor/SKILL.md`): The directory structure and
    context loading priorities now live in `conductor_protocol.md` §0/§0a.
    Individual command skills (`conductor_setup`, `conductor_newTrack`, etc.)
    are discoverable via their YAML frontmatter descriptions. No routing table
    or hub orientation doc is needed.

### Added

-   **API Surface Auto-Extraction**: Phase checkpoints in `/conductor_implement`
    now run full-file AST extraction (via `ast-grep`) on changed files, compare
    against a cached snapshot (`.api_surface_cache.json`), and propose novel
    symbols for addition to `terms.md`. Catches new methods on existing classes,
    interface properties, and enum members — not just top-level exports.

-   **Invariants as First-Class Artifact**: New `conductor/invariants.md` file
    for behavioral contracts (ordering constraints, null-check requirements,
    data-flow rules). Capture triggers fire during spec generation (Devil's
    Advocate), design decisions, implementation, review, and user-initiated
    statements.

-   **Pre-Execution Drift Scan**: Every Conductor command now performs a
    lightweight drift check during context loading. Changed files are
    cross-referenced against ADR scopes and invariant scopes; contradictions are
    flagged with resolution options before the command proceeds.

-   **Per-Directory GEMINI.md Context**: Conductor manages a `## Conductor
    Context` section inside existing `GEMINI.md` files for large directories.
    Sections include Purpose, Invariants, Key Types, and Term Overrides,
    delimited by boundary comments to prevent merge conflicts. Created during
    `/conductor_setup` (brownfield) and `/conductor_implement` (on first
    directory access).

-   **Grill mode** for `/conductor_newTrack` — conductor-aware relentless
    interview mode, triggered by "grill", "grill-me", or "grill me" in the
    prompt. Merges grill-me's recursive questioning with conductor domain
    awareness (glossary enforcement, code cross-referencing, spec-section
    targeting). New sub-skill: `conductor_newTrack_grill` (persona: Conductor
    Interrogator).

-   **Discovery mode** extracted to its own sub-skill — the
    `[experimental-discovery]` categorized questioning is now
    `conductor_newTrack_discovery` (persona: Conductor Explorer), keeping the
    newTrack protocol clean.

-   **ADR & Glossary Preflight Interceptor**: When any Conductor command
    executes against an existing brownfield project that lacks
    `conductor/adr/*.md` files, execution pauses to perform an automated
    document sweep, filter trade-offs through the 3-part gate, and backfill
    historical ADRs before resuming the primary command.

-   **Domain Modeling & ADR Integration**:
    -   **Project Glossary (`terms.md`)**: Semi-mandatory, skippable glossary
        step in `/conductor_setup`. Auto-populates from codebase scans in
        Brownfield projects; interviews the developer in Greenfield.
    -   **Inline ADR Gating**: 3-part gate (hard to reverse × surprising × real
        trade-off) evaluated per-decision in `/conductor_newTrack`.
    -   **Immediate ADR Writing**: Confirmed decisions written immediately to
        `conductor/adr/NNNN-slug.md` using the bundled `adr_template.md`.
    -   **Verification Bridge**: `plan.md` generation scans ADR `Confirmation`
        sections and injects their criteria as explicit verification tasks.
    -   **ADR Compliance Reviews**: `/conductor_review` checks code changes
        against active ADRs, warning on drift and offering to fix, update the
        ADR, or record tech debt.

-   **MVC rules architecture**: Extracted universal guardrails and Antigravity
    UX adapter into always-on rule files (`conductor_protocol.md`,
    `conductor_antigravity.md`). Extended protocols extracted to inert reference
    files (`conductor_adr_preflight.md`, `conductor_cdd_protocols.md`) loaded
    on demand by skills.

-   **Agent personas**: Each sub-skill defines a named persona (Conductor
    Architect, Conductor Planner, Conductor Implementer, Principal Software
    Engineer, Conductor Observer, Conductor Surgeon, Conductor Guide, Conductor
    Interrogator, Conductor Explorer).

-   **`--release_notes` flag** in installer: Shows changes for the installed
    version from CHANGELOG.md.

### Changed

-   **Token footprint reduction (~68%)**: Always-on protocol rule is compact.
    Extended protocols extracted to inert reference files loaded on demand by
    skills. Hub skill eliminated entirely.
-   **Glossary file renamed**: `TERMS.md` → `terms.md` for consistency with
    all other lowercase conductor artifact filenames.
-   **Templates relocated**: `workflow_template.md` and `adr_template.md` moved
    from `conductor/templates/` to `conductor_setup/templates/` — the only
    skill that uses them.
-   **Version stamp relocated**: `.conductor_version` now lives under
    `conductor_setup/` instead of the removed `conductor/` directory.
-   **Installer**: Installs rules and reference files alongside skills. Removed
    hub skill installation. Hub skill migration auto-removes old `conductor/`
    directory during upgrade. Added `ast-grep` optional dependency check.
-   **`conductor_newTrack` Step 6** refactored to a mode dispatch point —
    detects grill/discovery/default mode from the user's prompt and delegates
    to the appropriate sub-skill.

## [0.2.2] - 2026-04-10

### Added

-   `/conductor_chat` — Lightweight ceremony-free context mode
-   Enhanced `/conductor_newTrack` discovery pipeline (gap analysis, cross-track
    awareness, devil's advocate)
-   Individual `ask_question` calls for gap analysis and devil's advocate items
-   `ask_question` best practices with positive/negative examples

### Changed

-   Hub skill expanded with detailed artifact output conventions
-   Sub-skills updated with per-item structured questioning

## [0.2.1] - 2026-03-01

### Added

-   Skills-based architecture (migrated from workflows)
-   Hub-and-spoke model with central conductor skill
-   Version stamping (`.conductor_version`)
-   Legacy workflow migration in installer
-   Dry-run mode, backup-by-default, idempotent installs

## [0.1.0] - 2026-02-01

### Added

-   Initial conductor implementation as Antigravity workflows
-   Core commands: setup, newTrack, implement, status, review, revert
