# Armature CDD: Structural Permanence for AI Coding Agents

> [!NOTE]
> **Conductor is now Armature (v0.19.0)**  
> Conductor has been officially rebranded to **Armature**. Existing repositories with a `conductor/` directory continue operating seamlessly via Transparent Dual-Discovery with zero file migrations required.

## Background

**Armature** is a Context-Driven Development (CDD) framework for Antigravity, Gemini CLI, Claude Code, and Windsurf. It manages the full lifecycle of software development tracks: context setup, multi-turn inquiry depth specification, phased planning, test-driven implementation, living manual testing runbooks, and continuous multi-tier drift auditing.

This project was originally forked from Gemini CLI Conductor (`github.com/gemini-cli-extensions/conductor`). While upstream Conductor focused on basic task lists and prompt orchestration, this codebase diverged by integrating Context-Driven Development (CDD) workflows: living Architecture Decision Records (ADRs), domain glossaries (`terms.md`), interactive multi-dimension inquiry matrices, living manual verification runbooks, and automated drift detection.

## Structural Permanence & Joint Discipline

In stop-motion animation, puppets look soft and pliable on the outside, but their movement is held together by an internal steel armature with adjustable tension joints. Without the armature, studio heat turns clay into a puddle.

Autonomous agents without structural boundaries do the exact same thing. When an agent gets an execution loop, it moves fast. Without an internal structural skeleton, models deform architecture, accumulate synonyms, and drift off spec.

**Antigravity Conductor is now Armature.**

We replaced prompt wishes with an internal steel skeleton—giving agents full creative fluidity on the outside while anchoring them to deterministic structural boundaries underneath.

Armature preserves **transparent dual-discovery**:
- **Primary (`armature/`)**: Greenfield projects initialized via `/arm-setup` create `armature/`.
- **Legacy Fallback (`conductor/`)**: Projects with existing `conductor/` directories continue operating seamlessly with zero file migrations required.

Context travels with the codebase and can be shared across the whole team.

### Why Code Alone Isn't the Single Source of Truth

Code shows what syntax exists today, but never why it was built that way or what constraints must not be broken. Without architectural context, an AI agent treats legacy workarounds and technical debt as intentional design—and faithfully replicates them. Armature keeps architectural intent, domain terminology, and verification rules version-controlled right alongside the code.

## Keeping Docs, Terms, and Decisions in Sync

When agents write code, project context rots in three predictable ways. Armature stops all three:

### 1. Stopping Vocabulary Drift (Terms)
When an agent calls an object `board` in one file, `canvas` in another, and `workspace` in a third, the codebase fills with synonyms that break search and ruin future prompts. Armature creates a project glossary (`terms.md`) that locks in canonical terms and explicitly bans synonyms.

### 2. Stopping Decision Drift (Decisions)
Code only records what survived; it never records the failed architectures that were tried and discarded. Without recorded decisions, an agent will see an un-cached query or a complex serialization loop and "helpfully" re-introduce a race condition the team spent weeks debugging. Armature records architectural trade-offs as version-controlled markdown files in `adr/`, each with an automated verification checklist injected into implementation tasks.

### 3. Stopping Documentation Drift (Docs & Specs)
Static specs and runbooks become fiction the moment implementation hits a real edge case. Armature links specifications directly to living domain runbooks (`manual_testing/<domain>.md`). When a track finishes, verified test scenarios and behavior changes are synchronized automatically into the project documentation.

### 4. Automated Drift Auditing (`/arm-drift`)
`/arm-drift` is your codebase tripwire. It compares the real exported interfaces in your code against your docs, architectural decisions, and terms. If the code evolves in a way that turns your documentation into lies, Armature catches the divergence before you commit.

### The Operational Loop

```
/arm-setup     →  Initialize glossary (terms.md), adr/ dir,
                  manual_testing/ dir, per-directory context (brownfield)
/arm-new-track →  6-Dimension inquiry matrix; synthesize spec & manual_testing.md
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

Armature is benchmarked against alternative Spec-Driven Development (SDD) and Context-Driven Development (CDD) frameworks across a 30-scenario stratified engineering battery (120 criteria across 5 pillars) using live Gemini rollouts and LLM Meta-Judging.










## What Gets Installed

Armature installs as a unified plugin under `~/.gemini/config/plugins/antigravity-armature/`:

### Plugin Manifest & Skills


















### Rules (MVC Architecture)









## Installation

```bash
# From the google3 root of any workspace
bash experimental/users/skyebot/antigravity_armature/install.sh

# Preview what will happen (no files written)
bash experimental/users/skyebot/antigravity_armature/install.sh --dry_run

# Overwrite without creating backups
bash experimental/users/skyebot/antigravity_armature/install.sh --force

# Update to latest version
bash experimental/users/skyebot/antigravity_armature/install.sh --update
```

## Uninstall

```bash
bash experimental/users/skyebot/antigravity_armature/install.sh --uninstall
```

## Flags











## Usage

Once installed, the `/arm-*` commands are available globally in chat:

```
/arm-setup          # Initialize a project's armature/ context (or adopt legacy conductor/)
/arm-new-track      # Create a new feature or bug fix track
/arm-implement      # Execute the current track's plan
/arm-status         # View progress across all tracks
/arm-review         # Review completed work against spec
/arm-revert         # Undo work from a track, phase, or task
/arm-drift          # Run 3-tier continuous drift audit
/arm-chat           # Ingest project knowledge, then proceed with task directly
```

## Version

Current: **v0.19.0** — See [CHANGELOG.md](CHANGELOG.md) for release notes.
