# Conductor Evaluation & Benchmarking Suite

This directory contains the automated evaluation harnesses used to test, benchmark, and optimize Conductor. It provides reproducible, empirical verification that Conductor's agent skills and operational rules behave safely, efficiently, and accurately across complex development workflows.

---

## Why We Run Evaluations

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
- **What is tested**: Whether the assistant holds specifications in memory during discovery, gap analysis, and adversarial review rather than prematurely writing unhardened files to disk.
- **Why it matters**: Materializing draft files to disk too early commits the agent to bad assumptions before edge cases and interface contracts are settled.

### 2. Conversational Detour & Interruption Resilience
- **What is tested**: How the assistant handles an orthogonal technical query (e.g. WCAG contrast compliance in dark mode) in the middle of a specification interview, and whether it resumes at the exact uncompleted question without skipping remaining gap categories.
- **Why it matters**: Real developer conversations are rarely linear; agents must handle interruptions without losing track context or corrupting interview state.

### 3. Micro-Task Efficiency & Ceremony Scaling
- **What is tested**: Whether the assistant scales down process ceremony for surgical fixes (<5 lines of changed code, zero architectural ripple), proposing minimal targeted diffs with compact token usage (<1500 tokens) instead of multi-page PRDs.
- **Why it matters**: Process frameworks that treat every single-line CSS fix like a major distributed systems migration impose massive token costs and slow down developers.

### 4. Out-of-Band Code/Doc Drift Detection
- **What is tested**: Whether the assistant inspects uncommitted workspace diffs against active Architecture Decision Records (ADRs) and domain glossaries (`terms.md`), flags contradictions, and enforces zero-drift fixpoints.
- **Why it matters**: Code and documentation diverge quickly; agents must actively govern alignment between behavioral contracts and actual code.

### 5. Multi-Phase State Safety & Destructive Command Guardrails
- **What is tested**: Whether the assistant adheres to a documentation-only policy during database migrations and environment resets, logging the commands in runbooks while strictly refusing to execute destructive SQL drops autonomously.
- **Why it matters**: Autonomous destructive actions can wipe out local databases, emulator state, or testing fixtures without developer oversight.

### 6. Proto Schema Evolution & Wire-Format Edge Cases
- **What is tested**: Whether the assistant identifies subtle serialization traps (e.g., proto3 default zero-values losing distinction between unset fields and default values in partial update patches) and poses adversarial challenges requiring `FieldMask` or `optional` presence before planning.
- **Why it matters**: Wire-format bugs frequently lead to silent data corruption in production backend services.

### 7. Additive Manual Testing Runbook Verification
- **What is tested**: Whether the assistant treats living domain runbooks (`conductor/manual_testing/<domain>.md`) as strictly additive to automated CI unit and integration test suites, auditing both concurrently at phase checkpoints.
- **Why it matters**: Automated tests verify unit logic, while manual runbooks verify user-facing workflows, setup scripts, and environment fixtures.

### 8. 3-Tier Fixpoint Drift Auditing
- **What is tested**: Full-workspace verification across documentation consistency (Phase 1), AST-extracted public API symbol surfaces (Phase 2), and packaging manifests/installer arrays (Phase 3).
- **Why it matters**: Guarantees that code, symbols, documentation, and installation scripts reach a verified, coherent state before code submission.

---

## Open-Source SDD Evals vs. Custom Conductor Evaluators

The evaluation suite balances industry-standard benchmarks with custom Conductor evaluators:

| Capability Area | Open-Source / Industry SDD Baselines | Custom Conductor Evaluators |
| :--- | :--- | :--- |
| **Specification Lifecycle** | Traditional SDD pipelines (GitHub Spec Kit, BMAD Method, OpenSpec) requiring formal Constitution $\rightarrow$ Spec $\rightarrow$ Plan $\rightarrow$ Tasks artifacts. | **Pre-Materialization Hardening Barrier**: In-memory draft holding with strict multi-dimension gap analysis before writing to disk. |
| **Process Overhead** | Fixed ceremony: Multi-page PRDs, C4 architecture diagrams, and role-based handoffs (PM $\rightarrow$ Architect $\rightarrow$ Scrum Master $\rightarrow$ Dev). | **Dynamic Ceremony Scaling**: Automatic bypass of PRDs on micro-hotfixes (<5 lines), optimizing token efficiency. |
| **Conversational Flow** | Single-prompt static task evaluation or basic prompt response. | **Detour Resilience & Deep Branch Traversal**: Replaying interruptions and evaluating resumption at exact uncompleted sub-branches. |
| **Documentation & Drift** | Periodic markdown memory file updates (Memory Bank `activeContext.md`, `progress.md`). | **3-Tier Fixpoint Auditor**: Dynamic AST API surface extraction, ADR scope cross-referencing, and packaging manifest checks. |
| **Execution Safety** | Often executes whatever script the user requests, including destructive drops. | **Documentation-Only Fixture Safety Policy**: Hard rule requiring interactive user confirmation before mutative operations. |
| **Schema Hardening** | Basic proto compilation and endpoint mapping checks. | **Adversarial Schema Probing**: Active Devil's Advocate challenges on proto3 zero-value overwrites and wire breaks. |
| **Prompt Tuning** | Manual prompt editing and qualitative review. | **SkillOpt Optimizer (`evals/skillopt/`)**: Automated iterative mutation loop against 19 training and 15 validation tasks. |

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
