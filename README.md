# Antigravity Conductor Skills

## Background

[Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) is a
Gemini CLI extension that enables Context-Driven Development. It manages the
full lifecycle of software development tracks: context setup, specification,
planning, implementation, and review.

This installer packages **Antigravity Skills** (with rules and setup assets) that
bring Conductor's capabilities to Antigravity.

## Motivation

Standard IDE-based AI agents are powerful, but store their plans, context, and
knowledge on the developer's machine. The intelligence accumulated during
development **doesn't travel with the code and is invisible to teammates**.

Conductor takes a different approach: **context is a managed artifact that lives
alongside your code.** Specs, plans, and progress live alongside the project
source in a `conductor/` directory as self-updating, curated knowledge
artifacts. Context travels with the codebase and can be shared by the whole
team.

Agents and engineers both draw from a common knowledge base, so the AI
understands the codebase, and so do the developers. Centralized technical
constraints (style guides, workflow rules, tech-stack choices) guide every agent
interaction's adherence to the team's practices and preferences. And all present
and future work benefits from the evolving project context — it gets smarter
over time, not stale.

By installing Conductor as an Antigravity Skill, you get both: Antigravity's visual,
powerful agentic coding tools and session-level knowledge, *plus* shared project
context that the whole team can use.

## Evaluation results & benchmark

Conductor is benchmarked against alternative Spec-Driven Development (SDD) and Context-Driven Development (CDD) frameworks across 30 real-world engineering scenarios (120 test criteria across 5 core pillars) using blinded LLM-as-Judge evaluation and deterministic token/safety bounds.

| Framework | Paradigm | Criteria Passed | Pass Rate (95% CI) | Avg Tokens / Task | Scenarios |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Conductor (Antigravity OSS) (this)** | Context-Driven Development (CDD) | **90 / 120** | **75.0%** (±7.7% (67.3%–82.7%)) | 2236 tokens | 30 |
| **BMAD Method** | Multi-Agent Agile SDD | **81 / 120** | **67.5%** (±8.4% (59.1%–75.9%)) | 2591 tokens | 30 |
| **GitHub Spec Kit** | Spec-Driven Development (SDD) | **75 / 120** | **62.5%** (±8.7% (53.8%–71.2%)) | 2797 tokens | 30 |
| **Conductor (Canonical Gemini CLI Extension)** | Context-Driven Development (CDD) | **69 / 120** | **57.5%** (±8.8% (48.7%–66.3%)) | 2387 tokens | 30 |
| **OpenSpec** | Lightweight SDD | **57 / 120** | **47.5%** (±8.9% (38.6%–56.4%)) | 1490 tokens | 30 |
| **Memory Bank (Cline / Roo Code)** | Stateful Agent Memory | **47 / 120** | **39.2%** (±8.7% (30.4%–47.9%)) | 2312 tokens | 30 |

Full reports and test documentation:
- [Evaluation suite guide](evals/README.md)
- [Live benchmark Markdown report](evals/cdd_sdd_benchmark/cdd_sdd_live_benchmark_results.md)

## What Gets Installed

### Plugin Manifest & Skills

File                   | Location                                              | Purpose
---------------------- | ----------------------------------------------------- | -------
`plugin.json`          | `~/.gemini/antigravity/`                              | Plugin package manifest (name, version, metadata)
`marketplace.json`     | `~/.gemini/antigravity/.claude-plugin/`               | Claude Code plugin manifest
`conductor-setup/`     | `~/.gemini/antigravity/skills/conductor-setup/`       | `/conductor-setup` — Initialize project context (persona: Conductor Architect)
`workflow_template.md` | `~/.gemini/antigravity/skills/conductor-setup/assets/`| Bundled project workflow template copied during `/conductor-setup`
`adr_template.md`      | `~/.gemini/antigravity/skills/conductor-setup/assets/`| Bundled project ADR template copied during `/conductor-setup`
`manual_testing_template.md` | `~/.gemini/antigravity/skills/conductor-setup/assets/`| Bundled domain manual testing runbook template copied during `/conductor-setup`
`.conductor_version`   | `~/.gemini/antigravity/skills/conductor-setup/`       | Version stamp for update detection
`conductor-new-track/` | `~/.gemini/antigravity/skills/conductor-new-track/`   | `/conductor-new-track` — Start a new feature or bug fix (persona: Conductor Planner)
`conductor-implement/` | `~/.gemini/antigravity/skills/conductor-implement/`   | `/conductor-implement` — Execute plan tasks sequentially (persona: Conductor Implementer)
`conductor-status/`    | `~/.gemini/antigravity/skills/conductor-status/`      | `/conductor-status` — View project progress (persona: Conductor Observer)
`conductor-review/`    | `~/.gemini/antigravity/skills/conductor-review/`      | `/conductor-review` — Review work against spec (persona: Principal Software Engineer)
`conductor-revert/`    | `~/.gemini/antigravity/skills/conductor-revert/`      | `/conductor-revert` — Undo work via VCS-aware revert (persona: Conductor Surgeon)
`conductor-chat/`      | `~/.gemini/antigravity/skills/conductor-chat/`        | `/conductor-chat` — Ceremony-free context mode (persona: Conductor Guide)
`conductor-drift/`     | `~/.gemini/antigravity/skills/conductor-drift/`       | `/conductor-drift` — Audit and reconcile drift across docs, code, and packaging (persona: Conductor Fixpoint Auditor)

### Rules (MVC Architecture)

| File                         | Location                        | Purpose           |
| ---------------------------- | ------------------------------- | ----------------- |
| `conductor_protocol.md`      | `~/.gemini/antigravity/rules/`  | Always-on: directory structure, context loading, guardrails, interaction standards |
| `conductor_antigravity.md`   | `~/.gemini/antigravity/rules/`  | Always-on: Antigravity platform UI adapter (`ask_question`, artifact rendering) |
| `conductor_adr_preflight.md` | `~/.gemini/antigravity/rules/`  | On-demand: ADR preflight interceptor for brownfield projects |
| `conductor_cdd_protocols.md` | `~/.gemini/antigravity/rules/`  | On-demand: Drift scan, ADR capture, per-directory context |

## Installation

You can run the installer script on Mac/Linux or Windows.

### Mac, Linux, and WSL

```bash
# Standard installation
bash install.sh

# Preview what will happen (no files written)
bash install.sh --dry_run

# Overwrite without creating backups
bash install.sh --force
```

### Windows (CMD or PowerShell)

```bat
:: Standard installation
install.bat

:: Preview what will happen (no files written)
install.bat --dry_run

:: Overwrite without creating backups
install.bat --force
```

## Uninstall

**Mac, Linux, and WSL:**
```bash
bash install.sh --uninstall
```

**Windows:**
```bat
install.bat --uninstall
```

## Flags

Flag          | Description
------------- | --------------------------------------------------------
`--dry_run`   | Preview changes without writing or deleting files
`--force`     | Overwrite existing files without creating `.bak` backups
`--update`    | Update to the latest version (implies `--force`)
`--uninstall` | Remove all installed Conductor files
`--help`      | Show usage information

## Checking for Updates

The `--update` flag checks if your installed version is current and, if not,
performs the update automatically (implying `--force`):

```bash
bash install.sh --update
```

If already up to date, it exits immediately. A version check also runs
automatically at the end of every regular install.

## Usage After Installation

In Antigravity, typing `/` opens an autocomplete dropdown listing available workflows. The conductor commands are available globally once installed:

```
/conductor-setup          # Initialize a project's conductor/ context
/conductor-new-track       # Create a new feature or bug fix track
/conductor-implement      # Execute the current track's plan
/conductor-status         # View progress across all tracks
/conductor-review         # Review completed work against spec
/conductor-revert         # Undo work from a track, phase, or task
/conductor-chat           # Ingest conductor knowledge, then go — no tracks or gates.
                          # Ideal for asking how things work, exploring the codebase
                          # with full context, or diving into lightweight implementations
                          # that don't warrant a dedicated track.
```

### Via Natural Language

The Conductor skill is also attached as a global skill, so you can invoke it
with **natural language** instead of workflow commands. For example:

> *"Start a new track for adding dark mode support to the settings page"*

> *"Show me the current status of all my tracks"*

> *"Implement the next task in the active track"*

> *"Review the work I've done on the current track against the spec"*

Antigravity will automatically read the Conductor skill and execute the
appropriate command based on your prompt.

## Evaluation & Live Benchmark Results

Antigravity Conductor is continuously evaluated against industry agent development frameworks using the live CDD & SDD benchmark suite (`evals/cdd_sdd_benchmark/`):

| Framework | Paradigm | Criteria Passed | Pass Rate (95% CI) | Avg Tokens / Task | Scenarios |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **BMAD Method** | Multi-Agent Agile SDD | **33 / 40** | **82.5%** (±11.8% (70.7%–94.3%)) | 2007 tokens | 10 |
| **Conductor (Antigravity OSS) (this)** | Context-Driven Development (CDD) | **32 / 40** | **80.0%** (±12.4% (67.6%–92.4%)) | 1802 tokens | 10 |
| **GitHub Spec Kit** | Spec-Driven Development (SDD) | **31 / 40** | **77.5%** (±12.9% (64.6%–90.4%)) | 2376 tokens | 10 |
| **Conductor (Canonical Gemini CLI Extension)** | Context-Driven Development (CDD) | **24 / 40** | **60.0%** (±15.2% (44.8%–75.2%)) | 2265 tokens | 10 |
| **OpenSpec** | Lightweight SDD | **16 / 40** | **40.0%** (±15.2% (24.8%–55.2%)) | 1132 tokens | 10 |
| **Memory Bank (Cline / Roo Code)** | Stateful Agent Memory | **12 / 40** | **30.0%** (±14.2% (15.8%–44.2%)) | 1304 tokens | 10 |

*Evaluated across 10 complex engineering scenarios using blinded LLM-as-Judge scoring with `gemini-3-flash-preview`. Full details in [`evals/cdd_sdd_benchmark/cdd_sdd_live_benchmark_results.md`](evals/cdd_sdd_benchmark/cdd_sdd_live_benchmark_results.md).*

## Version

Current: **v0.17.0**

