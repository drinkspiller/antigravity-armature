# Armature SkillOpt Evaluation Harness

This directory contains the automated evaluation and optimization suite for
Armature skills and protocols.

## Overview

The test harness uses Microsoft SkillOpt's text-space optimization framework
adapted for Gemini models to verify that Armature skills adhere to strict
execution guardrails, interaction barriers, and handoff contracts.

-   **Target Model (`gemini-3.5-flash` / `gemini-3.7-flash`)**: Executes task
    rollouts to expose instructional blind spots.
-   **Optimizer & Judge Model (`gemini-3.1-pro-preview`)**: Evaluates rollout
    adherence against granular assertion criteria.

## Test Suites

-   `tasks/train.jsonl`: Training scenarios covering detour resumption,
    premature draft convergence, compound prompt shielding, doc-heavy planning,
    tiered manual testing classification, and autonomous runbook
    synchronization.
-   `tasks/val.jsonl`: Held-out validation scenarios testing gRPC migrations, UI
    token refactors, standard track creation, documentation-only phase
    checkpoints, and additive manual testing review audits.

## Usage

### Prerequisites

Set your `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

### Run Benchmark (Evaluation Only)

```bash
# Run benchmark across all tasks
python3 evals/skillopt/run_optimizer.py --eval_only

# Run benchmark for a specific target skill
python3 evals/skillopt/run_optimizer.py --target=skills/arm-new-track/SKILL.md --eval_only
python3 evals/skillopt/run_optimizer.py --target=skills/arm-implement/SKILL.md --eval_only
python3 evals/skillopt/run_optimizer.py --target=skills/arm-review/SKILL.md --eval_only
```

### Run Optimization Loop

```bash
# Optimize a skill across 2 reflection epochs
python3 evals/skillopt/run_optimizer.py --target=skills/arm-new-track/SKILL.md --optimize --epochs=2
```
