# Armature (OSS): Structural Permanence for AI Coding Agents

> [!NOTE]
> **Conductor is now Armature (OSS) (v0.19.0)**  
> Conductor has been officially rebranded to **Armature (OSS)**. Existing repositories with a `conductor/` directory continue operating seamlessly via Transparent Dual-Discovery with zero file migrations required.

## Background

**Armature (OSS)** is a Context-Driven Development (CDD) framework for Antigravity CLI, Claude Code, and Windsurf. It manages the full lifecycle of software development tracks: context setup, multi-turn inquiry depth specification, phased planning, test-driven implementation, living manual testing runbooks, and continuous multi-tier drift auditing.

This project was originally forked from the upstream Conductor CLI extension (`github.com/gemini-cli-extensions/conductor`). While upstream Conductor focused on basic task lists and prompt orchestration, this codebase diverged by integrating Context-Driven Development (CDD) workflows: living Architecture Decision Records (ADRs), domain glossaries (`terms.md`), continuous decision-tree traversal, living manual verification runbooks, and automated drift detection.

## Structural Permanence & Joint Discipline

In stop-motion animation, puppets look soft and pliable on the outside, but their movement is held together by an internal steel armature with adjustable tension joints. Without the armature, studio heat turns clay into a puddle.

Autonomous agents without structural boundaries do the exact same thing. When an agent gets an execution loop, it moves fast. Without an internal structural skeleton, models deform architecture, accumulate synonyms, and drift off spec.

**Conductor is now Armature (OSS).**

We replaced prompt wishes with an internal steel skeleton—giving agents full creative fluidity on the outside while anchoring them to deterministic structural boundaries underneath.

Armature (OSS) preserves **transparent dual-discovery**:
- **Primary (`armature/`)**: Greenfield projects initialized via `/arm-setup` create `armature/`.
- **Legacy Fallback (`conductor/`)**: Projects with existing `conductor/` directories continue operating seamlessly with zero file migrations required.

Context travels with the codebase and can be shared across the whole team.

### Why Code Alone Isn't the Single Source of Truth

Code shows what syntax exists today, but never why it was built that way or what constraints must not be broken. Without architectural context, an AI agent treats legacy workarounds and technical debt as intentional design—and faithfully replicates them. Armature (OSS) keeps architectural intent, domain terminology, and verification rules version-controlled right alongside the code.

## Keeping Docs, Terms, and Decisions in Sync

When agents write code, project context rots in three predictable ways. Armature (OSS) stops all three:

### 1. Stopping Vocabulary Drift (Terms)
When an agent calls an object `board` in one file, `canvas` in another, and `workspace` in a third, the codebase fills with synonyms that break search and ruin future prompts. Armature (OSS) creates a project glossary (`terms.md`) that locks in canonical terms and explicitly bans synonyms.

### 2. Stopping Decision Drift (Decisions)
Code only records what survived; it never records the failed architectures that were tried and discarded. Without recorded decisions, an agent will see an un-cached query or a complex serialization loop and "helpfully" re-introduce a race condition the team spent weeks debugging. Armature (OSS) records architectural trade-offs as version-controlled markdown files in `adr/`, each with an automated verification checklist injected into implementation tasks.

### 3. Stopping Documentation Drift (Docs & Specs)
Static specs and runbooks become fiction the moment implementation hits a real edge case. Armature (OSS) links specifications directly to living domain runbooks (`manual_testing/<domain>.md`). When a track finishes, verified test scenarios and behavior changes are synchronized automatically into the project documentation.

### 4. Automated Drift Auditing (`/arm-drift`)
`/arm-drift` is your codebase tripwire. It compares the real exported interfaces in your code against your docs, architectural decisions, and terms. If the code evolves in a way that turns your documentation into lies, Armature (OSS) catches the divergence before you commit.

### The Operational Loop

```
/arm-setup     →  Initialize glossary (terms.md), adr/ dir,
                  manual_testing/ dir, per-directory context (brownfield)
/arm-new-track →  Continuous decision-tree traversal & Grill Engine; synthesize spec & manual_testing.md
                  Enforce glossary terms in spec; gate decisions → ADRs
                  Translate ADR Confirmation blocks → plan.md tasks
                  Capture ADRs from Devil's Advocate challenges
/arm-implement →  Execute plan including ADR verification & manual test updates
                  Auto-extract API surfaces at phase boundaries
                  Auto-synchronize steady-state runbooks → manual_testing/<domain>.md
                  Capture ADRs from implementation guards
/arm-review    →  Audit code against ADRs, automated tests, and manual runbook
/arm-drift     →  Audit documentation consistency, API surfaces, and packaging
                  Reconcile mechanical drift automatically and guide semantic fixes
/arm-chat      →  Rapid context ingestion without ceremony or approval gates
/arm-revert    →  VCS-aware surgical task, phase, or track rollback
```

## Evaluation Results & Benchmark

Armature (OSS) is benchmarked against alternative Spec-Driven Development (SDD) and Context-Driven Development (CDD) frameworks across a 30-scenario stratified engineering battery (120 criteria across 5 pillars) using live model rollouts and LLM Meta-Judging.

| Rank | Framework | Composite Score | Pass Rate (95% CI) | Avg Tokens / Task | Key Takeaway |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **#1** | **Armature (OSS)** *(this)* | **85 / 100** | **85.0%** (102/120, ±6.4%) | 3038 tokens | 100% drift governance, continuous decision-tree traversal, and transparent dual-discovery. |
| **#2** | **BMAD Method** | **66 / 100** | **65.8%** (79/120, ±8.5%) | 2634 tokens | Multi-agent role separation; high coordination overhead on micro-fixes. |
| **#3** | **GitHub Spec Kit** | **63 / 100** | **63.3%** (76/120, ±8.6%) | 2835 tokens | Spec-first rigor with Constitution gating; heavy planning ceremony for minor edits. |
| **#4** | **Conductor (Canonical Upstream CLI)** | **49 / 100** | **49.2%** (59/120, ±8.9%) | 2346 tokens | Fast on linear task lists; lacks multi-turn branch resolution and OCC analysis. |
| **#5** | **OpenSpec** | **40 / 100** | **40.0%** (48/120, ±8.8%) | 1597 tokens | Lightweight change proposals; lacks destructive command safeguards. |
| **#6** | **Memory Bank (Cline / Roo Code)** | **39 / 100** | **39.2%** (47/120, ±8.7%) | 2703 tokens | Stateful markdown memory; vulnerable to out-of-band filesystem drift. |

## What Gets Installed

Armature (OSS) installs as a unified plugin under `~/.gemini/config/plugins/antigravity-armature/`:

### Plugin Manifest & Skills

| File | Location in `~/.gemini/config/plugins/antigravity-armature/` | Agent Persona | Purpose |
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

| File | Type | Location in `~/.gemini/config/plugins/antigravity-armature/` | Purpose |
| :--- | :--- | :--- | :--- |
| `armature_protocol.md` | Core Model | `rules/` | Always-on: directory structure, transparent dual-discovery (§7), guardrails, interaction standards |
| `armature_antigravity.md` | View / Controller Adapter | `rules/` | Always-on: Antigravity CLI and multi-agent interaction adapter (`ask_question`, artifact rendering) |
| `armature_adr_preflight.md` | Dynamic Interceptor | `rules/` | On-demand: ADR preflight interceptor for brownfield projects |
| `armature_cdd_protocols.md` | CDD Engine | `rules/` | On-demand: Drift scan, ADR capture, per-directory context rules |

### Supported Agent Environments

- **Antigravity / Antigravity CLI**: Installs to `~/.gemini/config/plugins/antigravity-armature/` (auto-discovered via plugin registry).
- **Claude Code**: Discoverable via `.claude-plugin/marketplace.json` or `.agents/skills/`.
- **Windsurf**: Discoverable via `.windsurf/` or `.agents/rules/`.

## Installation

```bash
# From the repository root
bash install.sh

# Preview what will happen (no files written)
bash install.sh --dry_run

# Overwrite without creating backups
bash install.sh --force

# Update to latest version
bash install.sh --update
```

### Windows Installation

```cmd
install.bat
```

## Uninstall

```bash
bash install.sh --uninstall
```

## Flags

| Flag | Description |
| :--- | :--- |
| `--dry_run` | Preview changes without writing or deleting files |
| `--force` | Overwrite existing files without creating `.bak` backups |
| `--uninstall` | Remove all installed Armature plugin and legacy files |
| `--update` | Update to the latest version (implies `--force`) |
| `--target=<path>` | Custom install target directory (defaults to `~/.gemini/config/plugins/antigravity-armature`) |
| `--release_notes` | Show release notes for the current version from `CHANGELOG.md` |
| `--help` | Show usage information |

## Usage

Once installed, the `/arm-*` commands are available globally in chat:

```
/arm-setup          # Initialize a project's armature/ context (or adopt legacy conductor/)
/arm-new-track      # Create a new feature or bug fix track via continuous decision trees
/arm-implement      # Execute the current track's plan with incremental drift checks
/arm-status         # View progress across all tracks
/arm-review         # Review completed work against spec and living runbooks
/arm-revert         # Undo work from a track, phase, or task
/arm-drift          # Run 3-tier continuous drift audit
/arm-chat           # Ingest project knowledge, then proceed with task directly
```

## Version

Current: **v0.19.0** — See [CHANGELOG.md](CHANGELOG.md) for release notes.
