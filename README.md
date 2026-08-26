# Armature: Structural Permanence for AI Coding Agents

> [!NOTE]
> **Conductor is now Armature (v0.19.0)**  
> Conductor has been officially rebranded to **Armature**. Existing repositories with a `conductor/` directory continue operating seamlessly via Transparent Dual-Discovery with zero file migrations required.

## Fluid on the Outside, Rigid Underneath

In stop-motion animation, puppets look soft and pliable on the outside, but their movement is held together by an internal steel armature with adjustable tension joints. Without the armature, studio heat turns clay into a puddle.

Autonomous agents without structural boundaries do the exact same thing. When an agent gets an execution loop, it moves fast. Without an internal structural skeleton, models deform architecture, accumulate synonyms, and drift off spec.

**Conductor is now Armature.**

Armature gives agents full creative fluidity on the outside while anchoring them to deterministic structural boundaries underneath.

### Why Code Alone Isn't the Single Source of Truth

Code shows what syntax exists today, but never why it was built that way or what constraints must not be broken. Without architectural context, an AI agent treats legacy workarounds and technical debt as intentional design—and faithfully replicates them.

Most agentic harnesses trap project memory, learned patterns, and scratchpad context in local SQLite caches or user-directory configs on an individual developer's machine. When a teammate pulls the branch or an agent runs in CI, that hard-won context evaporates.

Armature stores architectural decisions, domain terminology, and verification runbooks directly in the repository (`armature/`). Context travels with the codebase, versions alongside your git commits, and stays immediately shared across the entire team.

---

## Table of Contents

- [Quickstart](#quickstart)
- [Structural Joints for Autonomous Agents](#structural-joints-for-autonomous-agents)
  - [The Grill Engine (`/arm-new-track`)](#the-grill-engine-arm-new-track)
  - [Architectural Decision Records (`adr/`)](#architectural-decision-records-adr)
  - [Domain Glossary (`terms.md`)](#domain-glossary-termsmd)
  - [Living Runbooks (`manual_testing/`)](#living-runbooks-manual_testing)
  - [Self-Updating Documentation (`/arm-drift`)](#self-updating-documentation-arm-drift)
  - [Quick-Fix Bypass (*Bypass*)](#quick-fix-bypass-bypass)
- [Armature Commands](#armature-commands)
- [Evaluation Results & Benchmark](#evaluation-results--benchmark)
- [What Gets Installed](#what-gets-installed)
- [Installation Details & Flags](#installation-details--flags)
- [Origins & Compatibility](#origins--compatibility)

---

## Quickstart

Install Armature globally across your development environments:

```bash
# Install fresh via curl
curl -fsSL https://raw.githubusercontent.com/drinkspiller/antigravity-armature/main/install.sh | bash

# Or update an existing installation
bash install.sh --update
```

## Structural Joints for Autonomous Agents

Autonomous coding agents move fast when given an execution loop, but velocity without constraints quickly degrades codebase integrity. Without architectural guardrails, models introduce conflicting abstractions, resurrect discarded patterns, and let documentation drift away from real interfaces. Armature establishes six structural joints that keep autonomous execution aligned with system design:

### The Grill Engine (`/arm-new-track`)
Most AI coding agents jump straight from a short prompt into file edits. When given underspecified requirements, models make silent assumptions about architecture, pick the first familiar pattern that emerges in their context window, and begin generating code without probing failure modes.

The Grill Engine enforces a structured decision-tree interview before any implementation plan is drafted. It systematically traverses edge cases, concurrency boundaries, error recovery, security scope, and verification strategy. By resolving design ambiguities and surfacing hidden trade-offs up front, Armature ensures the implementation plan is grounded in concrete technical constraints rather than unvetted assumptions.

### Architectural Decision Records (`adr/`)
Code only records the implementation that survived; it never records the alternatives that were considered and rejected. Without a record of past architectural decisions, an AI agent examining a codebase sees an un-cached database query, a missing abstraction, or a manual loop and assumes it is an oversight—often re-implementing the exact pattern the team intentionally discarded.

Armature captures architectural trade-offs, rationale, and negative constraints as version-controlled markdown records in `adr/`. Each record includes an active verification checklist that is automatically injected into implementation tasks. When an agent plans or executes work, it is evaluated against these historical constraints, preventing regression into known architectural dead ends.

### Domain Glossary (`terms.md`)
As codebases grow and multiple agent sessions touch different files, terminology naturally fragments. One agent may refer to a core entity as a `workspace`, another as a `board`, and a third as a `canvas`. This vocabulary drift breaks semantic search, degrades codebase grep accuracy, and forces human developers to write increasingly verbose disambiguation prompts.

Armature maintains a central domain glossary in `terms.md` that defines canonical ubiquitous language for the project and explicitly lists banned synonyms. The agent is bound to this vocabulary across specifications, code symbols, and documentation, ensuring consistent naming conventions across the entire lifecycle.

### Living Runbooks (`manual_testing/`)
Automated unit and integration tests are necessary, but they often fail to capture end-to-end user workflows, environmental prerequisites, and stateful side effects. At the same time, manual testing instructions in READMEs or runbooks typically rot within weeks of being written, as interfaces shift and commands fall out of date.

Armature pairs every development track with an active verification runbook. When an implementation task is completed, steady-state manual test scenarios, reproduction steps, and fixture setup commands are automatically synchronized into permanent domain runbooks under `manual_testing/<domain>.md`. Verification instructions stay aligned with the code as it evolves.

### Self-Updating Documentation (`/arm-drift`)
Documentation drift occurs incrementally. When an engineer or an agent renames an exported symbol, alters a CLI parameter, or updates a package dependency, the corresponding documentation often remains unchanged. Over time, specs and guides become inaccurate, misleading both human contributors and future AI sessions.

`/arm-drift` acts as an automated tripwire by extracting AST symbols and public API surfaces directly from the source code and comparing them against project documentation, ADRs, and packaging manifests. It detects mechanical and semantic discrepancies before changes are committed, automatically reconciling straightforward documentation drift and alerting developers to deeper divergences.

### Quick-Fix Bypass (*Bypass*)
Heavyweight specification workflows are counterproductive for trivial modifications. Enforcing multi-turn interviews, architectural records, and phased implementation plans for single-line bug fixes or styling adjustments adds unnecessary friction and slows down routine maintenance.

The Quick-Fix Bypass establishes a ceremony-free fast path for surgical changes of five lines or fewer that carry zero architectural ripple. The agent directly inspects the target component, applies the minimal required diff, and verifies the change against relevant tests without generating track artifacts or approval gates.

---

## Armature Commands

Once installed, the `/arm-*` commands are available globally in chat:

| Command | Purpose |
| :--- | :--- |
| `/arm-setup` | Initialize a project's `armature/` context (or adopt legacy `conductor/`) |
| `/arm-new-track` | Create a new feature or bug fix track via continuous decision trees |
| `/arm-implement` | Execute the current track's plan with incremental drift checks |
| `/arm-status` | View trajectory and contract health across all active tracks |
| `/arm-review` | Multi-dimensional review against living runbooks and ADRs |
| `/arm-drift` | Continuous 3-tier drift tripwire across docs, interfaces, and code |
| `/arm-chat` | Ceremony-free context ingestion with automatic glossary sync |
| `/arm-revert` | VCS-aware surgical task, phase, or track rollback |

---

## Evaluation Results & Benchmark

Armature is benchmarked against alternative Spec-Driven Development (SDD) and Context-Driven Development (CDD) frameworks across a 30-scenario stratified engineering battery (120 criteria across 5 pillars) using live model rollouts and LLM Meta-Judging.

| Rank | Framework | Composite Score | Pass Rate (95% CI) | Avg Tokens / Task | Key Takeaway |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **#1** | **Armature** *(this)* | **85 / 100** | **85.0%** (102/120, ±6.4%) | 3038 tokens | 100% drift governance, continuous decision-tree traversal, and transparent dual-discovery. |
| **#2** | **BMAD Method** | **66 / 100** | **65.8%** (79/120, ±8.5%) | 2634 tokens | Multi-agent role separation; high coordination overhead on micro-fixes. |
| **#3** | **GitHub Spec Kit** | **63 / 100** | **63.3%** (76/120, ±8.6%) | 2835 tokens | Spec-first rigor with Constitution gating; heavy planning ceremony for minor edits. |
| **#4** | **Conductor** | **49 / 100** | **49.2%** (59/120, ±8.9%) | 2346 tokens | Efficient linear track orchestration; lacks multi-turn branch resolution and OCC analysis. |
| **#5** | **OpenSpec** | **40 / 100** | **40.0%** (48/120, ±8.8%) | 1597 tokens | Lightweight change proposals; lacks destructive command safeguards. |
| **#6** | **Memory Bank (Cline / Roo Code)** | **39 / 100** | **39.2%** (47/120, ±8.7%) | 2703 tokens | Stateful markdown memory; vulnerable to out-of-band filesystem drift. |

---

## What Gets Installed

Armature installs as a modular plugin bundle containing skills, rule protocols, assets, and packaging manifests:

### Plugin Manifest & Skills

| File | Location in Plugin Bundle | Agent Persona | Purpose |
| :--- | :--- | :--- | :--- |
| `plugin.json` | `plugin.json` | — | Plugin package manifest (name, version, metadata) |
| `marketplace.json` | `.claude-plugin/marketplace.json` | — | Claude Code plugin manifest |
| `arm-setup/` | `skills/arm-setup/` | Armature Architect | `/arm-setup` — Initialize project context, glossary, ADR directory, and living runbooks |
| `workflow_template.md` | `skills/arm-setup/assets/` | — | Bundled project workflow template copied during `/arm-setup` |
| `adr_template.md` | `skills/arm-setup/assets/` | — | Bundled project ADR template copied during `/arm-setup` |
| `manual_testing_template.md` | `skills/arm-setup/assets/` | — | Bundled manual testing guide template copied during `/arm-setup` |
| `.armature_version` | `.armature_version` | — | Version stamp for update detection |
| `arm-new-track/` | `skills/arm-new-track/` | Armature Planner | `/arm-new-track` — Start a new feature or bug fix with continuous decision-tree elicitation |
| `arm-implement/` | `skills/arm-implement/` | Armature Implementer | `/arm-implement` — Execute plan tasks sequentially with phase checkpoint drift audits |
| `arm-status/` | `skills/arm-status/` | Armature Observer | `/arm-status` — View project trajectory with ambient contract health monitoring |
| `arm-review/` | `skills/arm-review/` | Armature Reviewer | `/arm-review` — Multi-dimensional review against living runbooks and ADRs |
| `arm-revert/` | `skills/arm-revert/` | Armature Surgeon | `/arm-revert` — Surgical rollbacks with destructive operation shielding |
| `arm-drift/` | `skills/arm-drift/` | Armature Drift Auditor | `/arm-drift` — Continuous 3-tier drift auditing across docs, interfaces, and packaging |
| `arm-chat/` | `skills/arm-chat/` | Armature Guide | `/arm-chat` — Ceremony-free context ingestion with automatic glossary sync |

### Rules (MVC Architecture)

| File | Type | Location in Plugin Bundle | Purpose |
| :--- | :--- | :--- | :--- |
| `armature_protocol.md` | Core Model | `rules/` | Always-on: directory structure, transparent dual-discovery (§7), guardrails, interaction standards |
| `armature_antigravity.md` | View / Controller Adapter | `rules/` | Always-on: Antigravity CLI and multi-agent interaction adapter (`ask_question`, artifact rendering) |
| `armature_adr_preflight.md` | Dynamic Interceptor | `rules/` | On-demand: ADR preflight interceptor for brownfield projects |
| `armature_cdd_protocols.md` | CDD Engine | `rules/` | On-demand: Drift scan, ADR capture, per-directory context rules |

### Supported Environments

- **Antigravity / Antigravity CLI**: Installs to `~/.gemini/config/plugins/antigravity-armature/` (auto-discovered via plugin registry).
- **Claude Code**: Discoverable via `.claude-plugin/marketplace.json` or `.agents/skills/`.
- **Windsurf**: Discoverable via `.windsurf/` or `.agents/rules/`.
- **Custom / Other Harnesses**: Use `--target=<path>` to install to any custom plugin or skills directory.

---

## Installation Details & Flags

```bash
# Preview what will happen (no files written)
bash install.sh --dry_run

# Overwrite without creating backups
bash install.sh --force

# Update to latest version
bash install.sh --update

# Windows installation
install.bat

# Uninstall
bash install.sh --uninstall
```

### Flags

| Flag | Description |
| :--- | :--- |
| `--dry_run` | Preview changes without writing or deleting files |
| `--force` | Overwrite existing files without creating `.bak` backups |
| `--uninstall` | Remove all installed Armature plugin and legacy files |
| `--update` | Update to the latest version (implies `--force`) |
| `--target=<path>` | Custom install target directory (defaults to Antigravity global plugin directory `~/.gemini/config/plugins/antigravity-armature`) |
| `--release_notes` | Show release notes for the current version from `CHANGELOG.md` |
| `--help` | Show usage information |

---

## Origins & Compatibility

### Lineage

Armature was inspired by and forked from the [Conductor](https://github.com/gemini-cli-extensions/conductor/) extension (`github.com/gemini-cli-extensions/conductor`), which pioneered structured track-based task orchestration for AI coding assistants. 

Armature builds directly upon Conductor's foundational lifecycle, extending it with living Architecture Decision Records (ADRs), ubiquitous language domain glossaries (`terms.md`), continuous decision-tree traversal, living manual verification runbooks, and automated multi-tier drift auditing.

### Backwards Compatibility w/ Conductor

Armature preserves **transparent dual-discovery**:
- **Primary (`armature/`)**: Greenfield projects initialized via `/arm-setup` create `armature/`.
- **Legacy Fallback (`conductor/`)**: Projects with existing `conductor/` directories continue operating seamlessly with zero file migrations required.

---

## Version

Current: **v0.19.0** — See [CHANGELOG.md](CHANGELOG.md) for release notes.
