# Armature CDD: Structural Permanence for AI Coding Agents

> [!NOTE]
> **Conductor is now Armature (v0.19.0)**  
> Conductor has been officially rebranded to **Armature** — representing the internal precision steel skeleton that provides joint discipline and structural permanence to fluid, autonomous AI agents. Existing repositories with a `conductor/` directory continue operating seamlessly via Transparent Dual-Discovery with zero file migrations required.

## Background

**Armature** (formerly Antigravity Conductor) is an advanced Context-Driven Development (CDD) framework for Antigravity, Gemini CLI, Claude Code, and Windsurf. It manages the full lifecycle of software development tracks: context setup, multi-turn inquiry depth specification, phased planning, test-driven implementation, living manual testing runbooks, and continuous multi-tier drift auditing.

This project was originally forked from the canonical Gemini CLI Conductor (`github.com/gemini-cli-extensions/conductor`). While upstream Conductor focused on basic task planning and linear prompt orchestration, this codebase diverged substantially to pioneer Context-Driven Development (CDD). Over successive releases, it introduced living Architecture Decision Records (ADRs), ubiquitous domain glossaries (`terms.md`), interactive multi-dimension inquiry matrices, living manual verification runbooks, and automated multi-tier drift detection.

The rebrand from Conductor to **Armature** reflects this fundamental architectural divergence: shifting from an orchestral conductor waving a baton over a fluid model to an internal, precision-machined steel skeleton that gives autonomous agents structural permanence and joint discipline.

## Motivation: Structural Permanence & Joint Discipline

Code adapts to physical reality. It changes when a compiler fails, an endpoint times out, or a database constraint complains. Code lives in the present.

The things that actually rot, decay, and drift over time are the **documentation, the specifications, and the architectural decisions**.

```
Day 1:   Spec is written. Decision is recorded. Both are true.
Day 3:   Code hits production reality. A workaround is added. The code adapts.
Day 7:   The spec is now historical fiction. The decision is dead law.
Week 3:  An AI agent arrives. It reads the fictional docs, believes them, and breaks the real code.
```

When an autonomous coding agent enters an existing codebase, it doesn't fail because it lacks capability. It fails because it reads stale documentation, believes outdated specs, and implements features against an architecture that ceased to exist three weeks ago.

Without an internal structural skeleton, generative models and their documentation inevitably sag, deform, and drift apart.

**Antigravity Conductor is now Armature.**

In stop-motion animation, puppets look soft and pliable on the outside, but their movement is held together by an internal steel armature with adjustable tension joints. Without the armature, studio heat turns the clay into an unrecoverable puddle.

We replaced prompt wishes with an internal steel skeleton—giving agents full creative fluidity on the outside while anchoring documentation, specifications, and architectural decisions to deterministic codebase reality.

Armature preserves **transparent dual-discovery**:
- **Primary (`armature/`)**: Greenfield projects initialized via `/arm-setup` create `armature/`.
- **Legacy Fallback (`conductor/`)**: Projects with existing `conductor/` directories continue operating seamlessly with zero file migrations required.

Context travels with the codebase and can be shared across the whole team.

## Keeping Docs, Terms, and Decisions in Sync

When agents write code, project context rots in three predictable ways. Armature stops all three:

### 1. Stopping Vocabulary Drift (Terms)
When an agent calls an object `board` in one file, `canvas` in another, and `workspace` in a third, the codebase fills with synonyms that break search and ruin future prompts. Armature creates a project glossary (`terms.md`) that locks in canonical terms and explicitly bans synonyms.

### 2. Stopping Decision Drift (Decisions)
Architectural trade-offs usually vanish into chat transcripts or forgotten design docs. Armature saves decisions as version-controlled markdown records in `adr/`. Every decision record includes an automated verification checklist that gets injected straight into implementation tasks—forcing the agent to prove it respected the architecture before marking work done.

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
