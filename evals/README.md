# Conductor evaluation suite

Automated evaluation harnesses to test, benchmark, and tune Conductor. These tests check that Conductor's skills and rules handle real software engineering friction safely, efficiently, and accurately.

---

## Why run evaluations

AI coding assistants demo well on greenfield toy projects. They fall apart on real codebases:
- Writing code before checking existing types or interface contracts.
- Losing track of active specs the moment a developer asks a side question.
- Writing a ten-page PRD for a one-line CSS fix.
- Dropping database tables or clearing test fixtures without confirmation.
- Letting proto3 default zero-values silently wipe out database fields during partial updates.

This test suite checks how different agent frameworks hold up against these specific traps.

---

## What gets tested

The benchmark evaluates eight core engineering capabilities:

### Specification hardening
Holding specifications in memory during discovery and review instead of writing half-baked files to disk. Writing draft files too early locks the agent into bad assumptions before interface contracts are clear.

### Detour handling
Answering an unexpected technical question (like dark mode WCAG contrast) mid-interview and returning to the exact question left off, without skipping the rest of the checklist.

### Ceremony scaling
Scaling down process overhead for surgical fixes (<5 lines of changed code). The agent should emit a targeted diff with minimal token spend rather than demanding a multi-page specification.

### Out-of-band drift detection
Checking uncommitted diffs against architecture decision records (ADRs) and the domain glossary (`terms.md`), catching contradictions before the agent builds on top of them.

### Destructive command safety
Logging database migrations and environment teardowns in runbooks while strictly refusing to execute destructive SQL drops on its own.

### Proto schema evolution
Catching serialization traps, such as proto3 default zero-values losing the distinction between unset fields and default values in partial updates, and demanding field masks or `optional` presence before planning.

### Additive verification
Treating living domain runbooks (`conductor/manual_testing/<domain>.md`) as additive to automated CI tests, checking both at phase checkpoints.

### Fixpoint auditing
Checking documentation, exported AST symbols, ADRs, and installation manifests together to verify everything agrees before committing.

---

## Standard SDD evals

### Specification lifecycle
Standard spec-driven frameworks (GitHub Spec Kit, BMAD, OpenSpec) require formal Constitution -> Spec -> Plan -> Tasks documents for every track.

### Process overhead
Fixed ceremony requiring PRDs, C4 architecture diagrams, and role handoffs across Product Manager, Architect, Scrum Master, and Developer.

### Conversational flow
Single-prompt tasks or linear turn evaluations that ignore side questions and interruptions.

### Drift governance
Periodic markdown updates (like Memory Bank `activeContext.md`) without structural diff checks.

### Execution safety
Permissive tool runners that execute whatever script is in the prompt, including destructive drops.

### Schema checks
Basic compilation checks that miss zero-value evolution traps.

### Prompt tuning
Manual prompt adjustments based on qualitative inspection.

---

## Custom evals

### In-memory spec barrier
Holds specs in memory during gap analysis and review, refusing to write files until all decision branches are resolved and approved.

### Dynamic ceremony scaling
Bypasses heavy planning on small fixes (<5 lines), cutting token usage and getting straight to the diff.

### Detour resilience
Replays conversational interruptions to verify the agent returns to the exact uncompleted question.

### Three-tier drift audit
Audits document consistency, exported AST symbols, and installation manifests to catch drift.

### Documentation-only safety barrier
Forces database migrations and teardowns into runbooks and blocks autonomous destructive commands.

### Adversarial schema challenges
Probes proto3 default zero-value collisions during partial update migrations.

### Additive runbook checks
Audits living runbooks alongside automated test suites.

### SkillOpt prompt optimizer
Automates prompt mutation loops across training and validation tasks to measure and raise pass rates.

---

## Directory layout

```
evals/
├── README.md                 # Unified evaluation guide
├── cdd_sdd_benchmark/        # Track 1: Comparative framework benchmark & LLM meta-judge
│   ├── run_cdd_sdd_eval.py   # Multi-turn runner, HTML visualizer, and scoring harness
│   ├── tasks/scenarios.jsonl # 8 engineering scenarios (32 test criteria)
│   ├── configs/frameworks.json # Prompts & virtual contexts for evaluated frameworks
│   ├── eval_results.json     # Current consolidated rollout traces and scores
│   ├── cdd_sdd_live_benchmark_results.md   # Latest Markdown scorecard & report
│   ├── cdd_sdd_live_benchmark_results.html # Standalone interactive HTML visual report
│   └── history/              # Timestamped historical snapshot archives (JSON & HTML)
└── skillopt/                 # Track 2: Prompt optimization & validation loop
    ├── README.md             # Optimizer usage and validation gates
    ├── run_optimizer.py      # Automated prompt mutation engine
    └── tasks/
        ├── train.jsonl       # 19 prompt engineering training tasks
        └── val.jsonl         # 15 held-out validation tasks
```

### Track 1: Framework benchmark (`cdd_sdd_benchmark/`) — Conductor vs. Competitors

Puts Conductor against 5 rival paradigms (BMAD, Memory Bank, Spec Kit, OpenSpec, and Canonical Conductor) across 8 real-world engineering scenarios. An independent LLM Meta-Judge grades each framework on detour recovery, ceremony scaling, and safety, outputting comparative scorecards and Markdown leaderboards. `conductor_oss` (this) ranked #1 with an 87.5% pass rate.

1.  `conductor_oss` (this): Open-source Conductor implementation
    (`drinkspiller/antigravity-conductor`).
2.  `canonical_conductor`: Upstream canonical Gemini CLI extension
    (`gemini-cli-extensions/conductor`).
3.  `bmad_method`: Multi-agent agile framework.
4.  `memory_bank`: Persistent stateful memory architecture.
5.  `github_spec_kit`: Standardized spec-first pipeline.
6.  `openspec`: Lightweight living specification framework.

### Track 2: SkillOpt optimizer (`skillopt/`) — Conductor vs. Itself

An automated mutation loop that tunes Conductor's own operational instructions. It runs 19 training tasks and 15 held-out validation tasks to find prompt edge cases, eliminate token bloat, and verify fixes before releasing new versions.

-   `tasks/train.jsonl` (19 tasks): Edge-case discovery, ceremony scaling, proto
    evolution, and state safety.
-   `tasks/val.jsonl` (15 tasks): Held-out regression verification ensuring
    changes generalize without regressions.
-   `run_optimizer.py`: Runs baseline rollouts, evaluates failures, proposes
    candidate rule diffs, and validates improvements against the full suite.

---

## How the runner works

### Zero external dependencies
The evaluation runners are standalone Python 3 scripts using standard library modules (`urllib.request`, `json`, `argparse`, `os`). They interact directly with Gemini REST endpoints (`generateContent`).

### Multi-turn simulation
The harness simulates full conversational interactions:
1. Primes the assistant with system instructions and virtual project files (`product.md`, `tech-stack.md`, `terms.md`, `adr/*.md`).
2. Delivers engineer prompts step-by-step.
3. Dynamically handles follow-up turns, clarifications, and conversational interruptions.

### Two-tier LLM meta-judging
1. **Criterion Judge (`gemini-3.1-pro-preview`)**: Evaluates the assistant's generated response against each criterion in the scenario, returning boolean pass/fail status and evidence-based rationale.
2. **Executive Meta-Judge**: Computes composite scores across five core pillars (Spec Gating, Detour Resilience, Surgical Efficiency, Drift Governance, and Fixture Safety), ranks the frameworks, and produces a justified winner report.

### Incremental state merging
When running a single framework (`--framework=<key>`) or a single scenario (`--scenario=<id>`), the runner loads existing `eval_results.json`, merges new evaluation results in-place, and re-triggers the Executive Meta-Judge over the entire combined matrix. This allows testing a single rule mutation or new framework in seconds without paying the latency or token cost of rerunning the full matrix.

### Dated snapshots & history
The runner dates each execution in the payload (`timestamp`) and archives snapshots into `evals/cdd_sdd_benchmark/history/`:
- `eval_results_YYYYMMDD_HHMMSS.json`
- `cdd_sdd_benchmark_YYYYMMDD_HHMMSS.html`

The HTML visual report reads this history directory to render interactive multi-run comparison timelines, showing score trends over time and across model releases.

### Automated network failover
Target rollouts use `gemini-3.7-flash` with automatic failover to `gemini-3.5-flash` on transient rate limits (HTTP 503/429), ensuring uninterrupted benchmark runs.

---

## Commands

### Running the benchmark

Run full evaluation across all frameworks and scenarios:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
```

Benchmark a single framework (merges into existing scorecard):
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

Generate standalone HTML visual report:
```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
```

### Running the SkillOpt optimizer

Run optimization across training and validation tasks:
```bash
python3 evals/skillopt/run_optimizer.py
```

---

## Adding scenarios and frameworks

### Adding a scenario
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

### Adding a framework
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
The runner detects the new framework and includes it in subsequent benchmark runs, scorecard tables, and HTML reports.
