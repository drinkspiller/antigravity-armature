# Conductor Evaluation & Benchmarking Suite

This directory contains the automated evaluation harnesses used to test, benchmark, and optimize Conductor. It provides reproducible, empirical verification that Conductor's agent skills and operational rules behave safely, efficiently, and accurately across complex development workflows.

---

## Evaluation Rationale

AI coding agents often look functional on simple demonstrations, but degrade when faced with real-world software engineering friction:
- **Premature Execution**: Writing code or materializing files before understanding constraints, data contracts, or architecture boundaries.
- **Context Amnesia & Detours**: Getting distracted by conversational questions and abandoning active specifications or jumping straight to implementation upon returning.
- **Process Over-Ceremony**: Imposing excessive bureaucracy (multi-page PRDs, C4 diagrams, multi-agent role handoffs) on 2-line styling fixes.
- **Autonomous Destructive Actions**: Running destructive environment teardowns, SQL drops, or database resets without explicit user confirmation.
- **Silent Schema Evolution Traps**: Overlooking proto3 default zero-values (`""`, `0`, `false`) overwriting database fields in partial update patches.

The evaluation suite subjects frameworks to these exact friction points under live conditions to measure resilience, safety, and efficiency.

---

## High-Level Overview: What Is Tested

The benchmark suites evaluate eight core software engineering capabilities:

### 1. Specification Hardening & Anti-Premature Execution
Whether the assistant holds specifications in memory during discovery, gap analysis, and adversarial review rather than prematurely writing unhardened files to disk. Materializing draft files to disk too early commits the agent to bad assumptions before edge cases and interface contracts are settled.

### 2. Conversational Detour & Interruption Resilience
How the assistant handles an orthogonal technical query (such as WCAG contrast compliance in dark mode) in the middle of a specification interview, and whether it resumes at the exact uncompleted question without skipping remaining gap categories.

### 3. Micro-Task Efficiency & Ceremony Scaling
Whether the assistant scales down process ceremony for surgical fixes (<5 lines of changed code, zero architectural ripple), proposing minimal targeted diffs with compact token usage (<1500 tokens) instead of multi-page PRDs.

### 4. Out-of-Band Code/Doc Drift Detection
Whether the assistant inspects uncommitted workspace diffs against active Architecture Decision Records (ADRs) and domain glossaries (`terms.md`), flags contradictions, and enforces zero-drift fixpoints.

### 5. Multi-Phase State Safety & Destructive Command Guardrails
Whether the assistant adheres to a documentation-only policy during database migrations and environment resets, logging commands in runbooks while strictly refusing to execute destructive SQL drops autonomously.

### 6. Proto Schema Evolution & Wire-Format Edge Cases
Whether the assistant identifies subtle serialization traps (such as proto3 default zero-values losing distinction between unset fields and default values in partial update patches) and poses adversarial challenges requiring `FieldMask` or `optional` presence before planning.

### 7. Additive Manual Testing Runbook Verification
Whether the assistant treats living domain runbooks (`conductor/manual_testing/<domain>.md`) as strictly additive to automated CI unit and integration test suites, auditing both concurrently at phase checkpoints.

### 8. 3-Tier Fixpoint Drift Auditing
Full-workspace verification across documentation consistency (Phase 1), AST-extracted public API symbol surfaces (Phase 2), and packaging manifests/installer arrays (Phase 3).

---

## Standard SDD Evals

### Specification Lifecycle
Traditional SDD pipelines (GitHub Spec Kit, BMAD Method, OpenSpec) require formal Constitution $\rightarrow$ Spec $\rightarrow$ Plan $\rightarrow$ Tasks artifacts for every track.

### Process Overhead
Fixed ceremony requiring multi-page PRDs, C4 architecture diagrams, and role-based handoffs across Product Manager, Architect, Scrum Master, and Developer roles.

### Conversational Flow
Single-prompt static task evaluations or linear turn evaluations that do not account for conversational detours or deep branch exploration.

### Drift Governance
Periodic manual or markdown memory file updates (such as Memory Bank `activeContext.md` and `progress.md`) without automated structural diff verification.

### Execution Safety
Unrestricted tool execution patterns that permit running destructive scripts and database drops if requested in the prompt.

### Schema Hardening
Basic schema compilation and endpoint mapping checks without probing zero-value presence evolution.

### Prompt Tuning
Manual prompt adjustments based on qualitative inspection.

---

## Custom Evals

### Pre-Materialization Hardening Barrier
Evaluates whether the assistant holds specifications in memory during multi-dimensional gap analysis and adversarial devil's advocate reviews, refusing to write unhardened files to disk until all decision branches reach terminal leaves and are approved.

### Dynamic Ceremony Scaling
Measures token efficiency and process scaling on surgical fixes (<5 lines of code, zero architectural ripple), verifying the agent bypasses heavy PRD barriers and outputs targeted diffs directly with compact token usage.

### Detour Resilience & Deep Branch Traversal
Simulates real-world conversational interruptions (such as orthogonal design or accessibility queries) and verifies the assistant resumes at the exact uncompleted sub-branch without skipping remaining gap categories.

### 3-Tier Fixpoint Drift Auditor
Audits cross-document consistency (Phase 1), AST-extracted public API symbol surfaces against `terms.md` (Phase 2), and packaging manifests / installer arrays (Phase 3) to achieve zero-drift fixpoint verification.

### Documentation-Only Fixture Safety Policy
Enforces a strict safety barrier ensuring database migrations, resets, and environment teardown commands are documented in runbooks while forbidding autonomous execution of destructive commands.

### Adversarial Schema Probing
Actively challenges proto3 zero-default value collisions during partial update / PATCH migrations, requiring `FieldMask` or `optional` presence before generating plans.

### Additive Runbook Auditing
Audits living domain runbooks concurrently with automated unit and integration tests in CI, ensuring manual verification fixtures remain up to date without substituting them for CI passes.

### SkillOpt Iterative Prompt Optimizer
Runs continuous automated prompt mutation loops against training and validation task batteries to mathematically measure and improve skill instruction pass rates.

---

## The Two Evaluation Systems

The directory is structured into two complementary tracks:

```
evals/
├── README.md                 # This overview document
├── cdd_sdd_benchmark/        # Track 1: Comparative framework benchmark & LLM meta-judge
│   ├── README.md             # Benchmark execution guide & scenario details
│   ├── run_cdd_sdd_eval.py   # Multi-turn test runner and scoring harness
│   ├── tasks/scenarios.jsonl # 8 engineering scenarios (32 test criteria)
│   ├── configs/frameworks.json # Prompts & virtual contexts for 6 frameworks
│   ├── eval_results.json     # Raw rollout traces and scores
│   └── cdd_sdd_live_benchmark_results.md # Markdown scorecard & meta-judge report
└── skillopt/                 # Track 2: Prompt optimization & validation loop
    ├── README.md             # Optimizer usage and validation gates
    ├── run_optimizer.py      # Automated iterative prompt mutation engine
    └── tasks/
        ├── train.jsonl       # 19 prompt engineering training tasks
        └── val.jsonl         # 15 held-out validation tasks
```

### Track 1: Framework Comparative Benchmark (`cdd_sdd_benchmark/`)
Compares six industry frameworks across 8 scenarios and 32 criteria:
1. **`conductor_oss`**: Open-source Conductor implementation (`drinkspiller/antigravity-conductor`) with Deep Branch Resolution, 3-tier Fixpoint drift auditing, dynamic ceremony scaling, and additive manual runbook checks.
2. **`canonical_conductor`**: Upstream canonical Gemini CLI extension (`gemini-cli-extensions/conductor`).
3. **`bmad_method`**: Multi-agent agile framework.
4. **`memory_bank`**: Persistent stateful memory architecture.
5. **`github_spec_kit`**: Standardized spec-first pipeline.
6. **`openspec`**: Lightweight living specification framework.

### Track 2: SkillOpt Prompt Optimizer (`skillopt/`)
Iteratively refines Conductor's operational instructions:
- **`tasks/train.jsonl`** (19 tasks): Edge-case discovery, ceremony scaling, proto evolution, and state safety.
- **`tasks/val.jsonl`** (15 tasks): Held-out regression verification ensuring changes generalize without regressions.
- **`run_optimizer.py`**: Executes baseline rollouts, evaluates failures, proposes candidate rule diffs, and validates improvements against the full suite.

---

## How the System Works Under the Hood

### Zero External Dependencies
The evaluation runners are pure Python 3 scripts using standard library modules (`urllib.request`, `json`, `argparse`, `os`). They interact directly with Gemini REST endpoints (`generateContent`).

### Multi-Turn Agent Simulation
The harness simulates full conversational interactions:
1. Primes the assistant with system instructions and virtual project files (`product.md`, `tech-stack.md`, `terms.md`, `adr/*.md`).
2. Delivers engineer prompts step-by-step.
3. Dynamically handles follow-up turns, clarifications, and conversational interruptions.

### Two-Tier LLM Meta-Judging
1. **Criterion Judge (`gemini-3.1-pro-preview`)**: Evaluates the assistant's generated response against each criterion in the scenario, returning boolean pass/fail status and evidence-based rationale.
2. **Executive Meta-Judge**: Computes composite scores across five core pillars (Spec Gating, Detour Resilience, Surgical Efficiency, Drift Governance, and Fixture Safety), ranks the frameworks, and produces a justified winner report.

### Automated Network Failover
Target rollouts use `gemini-3.7-flash` with automatic failover to `gemini-3.5-flash` on transient rate limits (HTTP 503/429), ensuring uninterrupted benchmark runs.

---

## Quick Start & Usage Commands

### Running the Live Benchmark

Run full evaluation across all frameworks and scenarios:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
```

Benchmark a single framework:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --framework=conductor_oss
```

Test a single scenario:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --scenario=SCEN_07_SURGICAL_MICRO_HOTFIX_CEREMONY_SCALING
```

Dry-run schema and connectivity check:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --dry_run
```

Sync reports into an active conversation artifact directory:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --artifact_dir=/path/to/artifacts
```

### Running the SkillOpt Optimizer

Run optimization across training and validation tasks:
```bash
python3 evals/skillopt/run_optimizer.py
```

---

## How to Add New Scenarios and Frameworks

### Adding a New Scenario
Append a JSON object to `evals/cdd_sdd_benchmark/tasks/scenarios.jsonl`:
```json
{
  "id": "SCEN_09_NEW_EDGE_CASE",
  "category": "Edge Case Category",
  "description": "Plain language description of what is being tested.",
  "turns": [
    {"role": "user", "content": "Initial engineer prompt."}
  ],
  "eval_criteria": [
    "Specific assertion 1 the assistant must fulfill.",
    "Specific assertion 2 the assistant must fulfill."
  ]
}
```

### Adding a New Framework
Add an entry to `evals/cdd_sdd_benchmark/configs/frameworks.json`:
```json
{
  "my_custom_framework": {
    "name": "My Custom Framework",
    "slug": "my_custom_framework",
    "paradigm": "Custom Paradigm",
    "description": "Summary of framework principles.",
    "system_instruction": "System prompt instructions governing the agent...",
    "context_files": {
      "docs/overview.md": "# Project Overview\n..."
    }
  }
}
```
The runner will automatically detect the new framework and include it in subsequent benchmark runs and scorecard tables.
