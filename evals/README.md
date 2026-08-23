# Conductor Evaluation & Benchmarking Suite

This directory contains the automated evaluation harnesses used to test, benchmark, and optimize Conductor. It provides reproducible, empirical verification that Conductor's agent skills and operational rules behave safely, efficiently, and accurately across complex development workflows.

---

## Why We Run Evaluations

AI coding agents often look functional on simple demonstrations, but degrade when faced with real-world software engineering friction:
- Prematurely writing code before understanding constraints or interface contracts.
- Getting distracted by conversational detours and abandoning active specifications.
- Imposing excessive bureaucracy (multi-page PRDs and C4 diagrams) on 2-line styling fixes.
- Autonomously executing destructive environment teardowns or database resets without user consent.
- Silently ignoring schema evolution traps (such as proto3 default zero-values overwriting database state in partial update patches).

The evaluation suite tests how different agent frameworks respond to these exact failure modes under live conditions.

---

## The Two Evaluation Systems

The suite is divided into two focused tracks:

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

This track benchmarks **Context-Driven Development (CDD)** against **Spec-Driven Development (SDD)** and alternative industry frameworks:

1. **`conductor_oss`**: Open-source Conductor implementation (`drinkspiller/antigravity-conductor`) with Deep Branch Resolution, 3-tier Fixpoint drift auditing, dynamic ceremony scaling, and additive manual runbook checks.
2. **`canonical_conductor`**: Upstream canonical Gemini CLI extension (`gemini-cli-extensions/conductor`).
3. **`bmad_method`**: Multi-agent enterprise agile framework (simulating PM, Architect, Scrum Master, and QA).
4. **`memory_bank`**: Stateful markdown memory system (Cline / Roo Code pattern).
5. **`github_spec_kit`**: Standardized Constitution -> Spec -> Plan -> Tasks pipeline.
6. **`openspec`**: Lightweight living specification framework with slash-command change proposals.

#### What Scenarios Are Tested?
The benchmark rolls out 8 standardized scenarios testing 32 empirical criteria:
- **Protocol & Schema Hardening**: Migrating REST endpoints to gRPC with backward-compatibility checks and adversarial schema probing.
- **Detour Resilience**: Answering an orthogonal design query mid-interview without dropping track context or prematurely generating code.
- **Micro-Hotfix Ceremony Scaling**: Delivering single-line UI fixes with compact token usage (<1500 tokens) rather than multi-page PRDs.
- **Out-of-Band Drift Detection**: Flagging contradictions between uncommitted code diffs and architectural decision records (ADRs).
- **Destructive State Safety**: Enforcing documentation-only command logging during database migrations instead of running destructive teardowns autonomously.
- **Proto Schema Evolution**: Posing adversarial challenges on proto3 zero-default values in partial update patches before writing code.
- **Additive Verification**: Auditing living manual testing runbooks concurrently with CI test passes rather than treating them as substitutes.

---

### Track 2: SkillOpt Prompt Optimizer (`skillopt/`)

This track optimizes Conductor's own prompt instructions and operational rules.
- **Training Suite (`tasks/train.jsonl`)**: 19 tasks focusing on edge-case probing, ceremony reduction, and safety guardrails.
- **Validation Suite (`tasks/val.jsonl`)**: 15 held-out tasks verifying that improvements generalize without causing regressions across other skills.
- **Optimizer Loop (`run_optimizer.py`)**: Runs baseline evaluations, generates candidate rule modifications using Gemini, validates candidates against regression suites, and selects winning rules that increase the overall pass rate.

---

## How the System Works Under the Hood

### Zero External Dependencies
The evaluation runners are pure Python 3 scripts utilizing standard library modules (`urllib.request`, `json`, `argparse`, `os`). They connect directly to Gemini API endpoints without requiring heavyweight third-party SDKs.

### Multi-Turn Agent Simulation
Rather than testing single prompts in isolation, the harness simulates multi-turn conversations between a software engineer and the AI assistant:
1. The assistant is initialized with the framework's system instructions and virtual project context files (e.g., `product.md`, `tech-stack.md`, `terms.md`, `adr/*.md`).
2. The harness feeds the scenario's initial user request.
3. If the scenario involves interruptions or clarifications, the harness exchanges subsequent turns dynamically based on assistant responses.

### Two-Tier LLM Meta-Judging
1. **Criterion-Level Judge (`gemini-3.1-pro-preview`)**: Evaluates the assistant's generated response against each criterion defined in the scenario, returning a boolean pass/fail status and an evidence-based explanation.
2. **Executive Meta-Judge**: Synthesizes the full rollout matrix into composite scores across 5 core pillars (Spec Gating, Detour Resilience, Surgical Efficiency, Drift Governance, and Fixture Safety), ranks the frameworks, and produces a justified winner report.

### Automated Network Failover
Target requests default to `gemini-3.7-flash` and automatically fail over to `gemini-3.5-flash` if transient rate limits (HTTP 503/429) occur, ensuring complete benchmark runs.

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
