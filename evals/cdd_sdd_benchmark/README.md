# CDD & SDD Frameworks Evaluation Benchmark

This directory contains an automated, live evaluation harness for benchmarking
**Context-Driven Development (CDD)** and **Spec-Driven Development (SDD)**
frameworks across standardized software engineering scenarios using live Gemini
rollouts and LLM Meta-Judging.

## Frameworks Evaluated

1.  **Conductor (Antigravity OSS)** (`conductor_oss`): Open-source
    Context-Driven Development framework (`drinkspiller/antigravity-conductor`)
    featuring persistent repository context, track isolation, dynamic ceremony scaling, and Fixpoint drift auditing.
2.  **Conductor (Canonical Gemini CLI Extension)** (`canonical_conductor`):
    Upstream canonical Gemini CLI extension (`gemini-cli-extensions/conductor`).
3.  **BMAD Method** (`bmad_method`): Multi-agent enterprise agile framework
    simulating PM, Architect, Scrum Master, and QA roles.
4.  **Memory Bank** (`memory_bank`): Stateful markdown memory architecture
    (Cline / Roo Code).
5.  **GitHub Spec Kit** (`github_spec_kit`): Standardized Spec-First pipeline
    (Constitution -> Spec -> Plan -> Tasks).
6.  **OpenSpec** (`openspec`): Lightweight living spec framework using
    slash-command change proposals.

## Scenarios Battery

-   `SCEN_01_BROWNFIELD_PROTOCOL_MIGRATION`: Migrating legacy REST endpoint to
    gRPC service with existing schema contracts.
-   `SCEN_02_DETOUR_INTERRUPTED_SPEC_INTERVIEW`: Multi-turn conversational
    interruption during specification drafting, testing detour amnesia and
    pre-materialization hardening.
-   `SCEN_03_SURGICAL_MICRO_HOTFIX`: Single-line UI sorting fix and flag toggle,
    testing coordination tax and token overhead.
-   `SCEN_04_OUT_OF_BAND_DRIFT_SCAN`: Detecting divergence between uncommitted
    code diffs and Architecture Decision Records / glossary symbols.
-   `SCEN_05_MULTI_PHASE_STATE_SAFETY`: Phase checkpoint with database
    migrations, testing documentation-only policy vs autonomous destructive
    execution.
-   `SCEN_06_PROTO_SCHEMA_EVOLUTION_CHALLENGE`: Advanced proto schema evolution
    testing adversarial probing of proto3 default zero-value collisions in
    partial updates.
-   `SCEN_07_SURGICAL_MICRO_HOTFIX_CEREMONY_SCALING`: 2-line CSS z-index and
    `aria-label` accessibility fix testing ceremony scaling vs heavy PRD
    overhead.
-   `SCEN_08_ADDITIVE_RUNBOOK_CHECKPOINT_AUDIT`: Phase checkpoint audit
    enforcing that manual testing runbooks are strictly additive to automated CI
    unit/integration tests.

## Augmenting the Benchmark

The evaluation suite is designed to be easily extensible, mirroring the
`/skill-opt` task augmentation pattern:

### 1. Adding a New Scenario

Append a JSON object to `tasks/scenarios.jsonl`:

```json
{
  "id": "SCEN_09_NEW_CHALLENGE",
  "title": "Title of Challenge",
  "description": "Detailed prompt context and engineering task constraints.",
  "turns": [
    {"user": "Initial prompt..."},
    {"user": "Second prompt..."}
  ],
  "rubric_prompt": "Judge evaluation instructions and assertion definitions...",
  "criteria": [
    "Does not skip...",
    "Systematically evaluates...",
    "Enforces..."
  ]
}
```

### 2. Adding / Tuning a Framework Configuration

Add or update the framework definition in `configs/frameworks.json`:

```json
{
  "my_custom_framework": {
    "name": "Custom Agent Framework",
    "slug": "my_custom_framework",
    "paradigm": "Context-Driven Development (CDD)",
    "description": "Summary of agent architecture...",
    "system_instruction": "Operating rules and guidelines for the agent...",
    "context_files": {
      "conductor/product.md": "# Product Overview...",
      "conductor/tech-stack.md": "# Tech Stack..."
    }
  }
}
```

## Usage

### Prerequisites

Set your `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

### Dry Run (Schema & Connectivity Validation)

```bash
python3 experimental/users/skyebot/jetski_conductor/evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --dry_run
```

### Full Benchmark Execution

```bash
python3 experimental/users/skyebot/jetski_conductor/evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
```

### Targeting Specific Frameworks, Scenarios, or Artifact Sync

```bash
# Evaluate only jetski_conductor_dev and conductor_oss
python3 experimental/users/skyebot/jetski_conductor/evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --framework=jetski_conductor_dev

# Sync results directly to conversation artifact directory
python3 experimental/users/skyebot/jetski_conductor/evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --artifact_dir=/path/to/artifacts
```
