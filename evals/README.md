# Conductor Evaluation Suite

Automated evaluation harnesses to objectively test, benchmark, and calibrate
Conductor and alternative development paradigms. The suite measures how agent
frameworks handle real-world software engineering friction, specification
discipline, conversational detours, architectural drift, and state safety.

--------------------------------------------------------------------------------

## Why Run Evaluations

AI coding assistants frequently succeed on trivial, greenfield toy tasks but
fail in production environments due to:

-   **Premature Code Generation**: Writing code before validating existing
    schemas, types, or backward compatibility contracts.
-   **Conversational Amnesia**: Losing active specification state and milestone
    progress when interrupted by developer questions or detours.
-   **Bureaucratic Coordination Tax**: Emitting multi-page PRDs, C4 architecture
    diagrams, and complex multi-agent ceremonies for single-line bug fixes.
-   **Out-of-Band Architectural Drift**: Ignoring divergence between uncommitted
    code diffs, Architecture Decision Records (ADRs), and ubiquitous domain
    glossaries (`terms.md`).
-   **Autonomous Destructive Actions**: Executing destructive database drops,
    table wipes, or environment teardowns without confirmation barriers.
-   **Wire-Format & Protocol Traps**: Failing to account for proto3 default
    zero-value semantics or serialization collisions during partial update
    migrations.

This evaluation suite measures how different agent frameworks hold up against
these specific failure modes.

--------------------------------------------------------------------------------

## Evaluation Methodology & Guardrails

The benchmark enforces strict scientific measurement standards to ensure
unbiased, reproducible, and objective results:

### 1. Authentic, Uncontaminated Baselines

All candidate frameworks (Conductor, GitHub Spec Kit, OpenSpec, BMAD Method,
Memory Bank, Canonical Conductor) are configured with authentic system
instructions reflecting upstream methodology. System prompts do not contain
scenario-specific test answers, keywords, or strawman constraints.

### 2. Blinded LLM-as-Judge Scoring

To eliminate brand and name association bias, the evaluation runner masks
framework identities (`CANDIDATE UNDER TEST (Blinded Candidate)`) before
submitting transcripts to the criterion judge (`gemini-3.1-pro-preview`).

### 3. Deterministic Verification & Safety Assertions

In addition to semantic LLM judging, the harness deterministically validates:

-   **Token Efficiency**: Hard token budget limits (<1500 tokens) for
    micro-hotfixes.
-   **Execution Safety**: Automatic rejection of unshielded destructive shell
    patterns (`DROP TABLE`, `rm -rf`).
-   **Tool Invocation Syntax**: Verification of structured interactive tool
    calls (`ask_question`, `write_to_file`).

### 4. Statistical Rigor & 95% Confidence Intervals

Pass rates are reported alongside standard errors and 95% normal confidence
intervals ($p \pm 1.96 \cdot SE$), providing clear bounds on measurement
variance.

--------------------------------------------------------------------------------

## The 5 Core Evaluation Pillars

The benchmark evaluates 10 distinct, non-redundant engineering scenarios across
5 core pillars:

1.  **Specification & Plan Gating (`SCEN_01`, `SCEN_06`, `SCEN_07`)**: Evaluates
    problem exploration, backward compatibility analysis, proto3 zero-value vs.
    unset null handling, and explicit human review gates before code generation.
2.  **Conversational Detour Resilience (`SCEN_02`)**: Assesses whether an agent
    answers an orthogonal design inquiry (e.g., WCAG dark mode contrast) and
    cleanly resumes the active specification milestone without amnesia or
    premature file materialization.
3.  **Surgical Velocity & Token Efficiency (`SCEN_03`, `SCEN_07`)**: Measures
    process efficiency and coordination tax on micro-tasks (<5 lines of code),
    ensuring targeted diff proposals under 1500 tokens without heavy ceremony.
4.  **Code & Doc Drift Governance (`SCEN_04`, `SCEN_10`)**: Assesses
    pre-execution drift scans, contradiction flagging between uncommitted code
    diffs and ADRs/glossaries, and post-implementation terminology
    synchronization.
5.  **State Safety & Execution Guardrails (`SCEN_05`, `SCEN_08`, `SCEN_09`)**:
    Enforces documentation-only command policies, ensuring database teardowns
    and migrations are recorded in runbooks while strictly refusing autonomous
    destructive drops.

--------------------------------------------------------------------------------

## Directory Layout

```
evals/
├── README.md                 # Unified evaluation guide & methodology
├── cdd_sdd_benchmark/        # Track 1: Comparative framework benchmark & LLM meta-judge
│   ├── run_cdd_sdd_eval.py   # Multi-turn runner, blinded judge, HTML visualizer, and scoring harness
│   ├── tasks/scenarios.jsonl # 10 distinct engineering scenarios (40 test criteria)
│   ├── configs/frameworks.json # Clean, authentic system instructions & virtual contexts
│   ├── eval_results.json     # Current consolidated rollout traces, metrics, and CI bounds
│   ├── cdd_sdd_live_benchmark_results.md   # Latest Markdown scorecard & report
│   └── history/              # Timestamped historical snapshot archives (JSON/HTML)
└── skillopt/                 # Track 2: Prompt optimization & validation loop
    ├── README.md             # Optimizer usage and validation gates
    ├── run_optimizer.py      # Automated prompt mutation engine with anti-overfitting rules
    └── tasks/
        ├── train.jsonl       # 16 prompt engineering training tasks
        └── val.jsonl         # 12 held-out validation tasks across distinct domains
```

--------------------------------------------------------------------------------

## Running the Benchmark & Optimizer

### Running Track 1: Framework Comparative Benchmark

Run the full evaluation battery across all 6 frameworks and 10 scenarios:

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
```

Benchmark a single framework (merges into existing scorecard):

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --framework=conductor_oss
```

Test a single scenario:

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --scenario=SCEN_01_BROWNFIELD_PROTOCOL_MIGRATION
```

Dry-run schema and connectivity check:

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --dry_run
```

Regenerate reports directly from existing benchmark output (sorted descending by
criteria passed):

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --report_only
```

Generate standalone visual HTML report:

```bash
python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --html_report=evals/cdd_sdd_benchmark/cdd_sdd_live_benchmark_results.html
```

### Running Track 2: SkillOpt Optimizer

Run evaluation on held-out validation tasks:

```bash
python3 evals/skillopt/run_optimizer.py --eval_only
```

Run full optimization loop on a specific skill:

```bash
python3 evals/skillopt/run_optimizer.py --target=skills/conductor-new-track/SKILL.md --optimize
```

--------------------------------------------------------------------------------

## Adding Scenarios & Frameworks

### Adding a Scenario

Append a JSON object to `evals/cdd_sdd_benchmark/tasks/scenarios.jsonl`:

```json
{
  "id": "SCEN_11_NEW_SCENARIO_NAME",
  "category": "Pillar or Architecture Category",
  "description": "Concise description of what is being tested.",
  "turns": [
    {"role": "user", "content": "Initial engineer prompt."}
  ],
  "eval_criteria": [
    "Specific assertion 1 the assistant must fulfill.",
    "Specific assertion 2 the assistant must fulfill."
  ]
}
```

### Adding a Framework

Add an entry to `evals/cdd_sdd_benchmark/configs/frameworks.json`:

```json
{
  "my_framework": {
    "name": "My Framework Name",
    "slug": "my_framework",
    "paradigm": "Framework Paradigm",
    "description": "High-level summary of framework principles.",
    "system_instruction": "Authentic upstream system prompt instructions...",
    "context_files": {
      "docs/overview.md": "# Project Overview\n..."
    }
  }
}
```
