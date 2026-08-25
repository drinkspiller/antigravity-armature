# Armature CDD: Structural Permanence for AI Coding Agents

> [!NOTE]
> **Conductor is now Armature (v0.19.0)**  
> Conductor has been officially rebranded to **Armature** — representing the internal precision steel skeleton that provides joint discipline and structural permanence to fluid, autonomous AI agents. Existing repositories with a `conductor/` directory continue operating seamlessly via Transparent Dual-Discovery with zero file migrations required.

## Background

**Armature** (formerly Antigravity Conductor) is an advanced Context-Driven Development (CDD) framework for Antigravity, Gemini CLI, Claude Code, and Windsurf. It manages the full lifecycle of software development tracks: context setup, multi-turn inquiry depth specification, phased planning, test-driven implementation, living manual testing runbooks, and continuous multi-tier drift auditing.

This project was originally forked from the canonical Gemini CLI Conductor (`github.com/gemini-cli-extensions/conductor`). While upstream Conductor focused on basic task planning and linear prompt orchestration, this codebase diverged substantially to pioneer Context-Driven Development (CDD). Over successive releases, it introduced living Architecture Decision Records (ADRs), ubiquitous domain glossaries (`terms.md`), interactive multi-dimension inquiry matrices, living manual verification runbooks, and automated multi-tier drift detection.

The rebrand from Conductor to **Armature** reflects this fundamental architectural divergence: shifting from an orchestral conductor waving a baton over a fluid model to an internal, precision-machined steel skeleton that gives autonomous agents structural permanence and joint discipline.

## Motivation: Structural Permanence & Joint Discipline

> **8 modular skills, automatic drift detection, and precision structural joints.**

In stop-motion animation, puppets look soft and pliable on the outside, but their movement is held together by an internal steel armature with adjustable tension joints. Without the armature, studio heat turns clay into a puddle.

Autonomous agents without structural boundaries do the exact same thing. When an agent gets an execution loop, it moves fast. Without an internal structural skeleton, models deform architecture, accumulate synonyms, and drift off spec.

**Antigravity Conductor is now Armature.**

We replaced prompt wishes with an internal steel skeleton—giving agents full creative fluidity on the outside while anchoring them to deterministic structural boundaries underneath.

Armature preserves **transparent dual-discovery**:
- **Primary (`armature/`)**: Greenfield projects initialized via `/arm-setup` create `armature/`.
- **Legacy Fallback (`conductor/`)**: Projects with existing `conductor/` directories continue operating seamlessly with zero file migrations required.

Context travels with the codebase and can be shared across the whole team.

## Domain Modeling & Architecture Decision Records (ADRs)

Armature integrates Bounded Context domain modeling and Architecture Decision Records (ADRs) into the track lifecycle. This fixes two common ways agent-managed codebases decay: vocabulary drift and unverified architecture.

### How it Works

1. **Glossary (`terms.md`)**: Created during setup. It defines canonical terms and lists forbidden synonyms.
2. **Architecture Decision Records (`adr/`)**: Written to `{PROJECT_CONTEXT_DIR}/adr/` as `NNNN-slug.md` using MADR format.
3. **Living Manual Testing Runbooks (`manual_testing/<domain>.md`)**: Synchronized autonomously from active track runbooks during track closeout.
4. **Automated 3-Tier Drift Auditor (`/arm-drift`)**: Audits documentation, AST symbols, and release packaging manifests across 3 tiers.

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
