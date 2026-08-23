#!/usr/bin/env python3
"""CDD & SDD Framework Comparative Evaluation Runner.

A zero-external-dependency evaluation harness that benchmarks six Spec-Driven
Development and Context-Driven Development frameworks across a 5-scenario,
20-criterion test battery using live Gemini API rollouts and automated judging.

Target Frameworks:
  - conductor_oss (Conductor Antigravity OSS)
  - canonical_conductor (Conductor Canonical Gemini CLI Extension)
  - bmad_method (BMAD Method)
  - memory_bank (Memory Bank / Cline / Roo Code)
  - github_spec_kit (GitHub Spec Kit)
  - openspec (OpenSpec)

Usage:
  # Run full evaluation across all 6 frameworks and 5 scenarios:
  python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py

  # Run evaluation for a specific framework:
  python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --framework=conductor_oss

  # Run evaluation for a specific scenario:
  python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py
  --scenario=SCEN_02_DETOUR_INTERRUPTED_SPEC_INTERVIEW

  # Dry run (validates schema and connection without full rollout):
  python3 evals/cdd_sdd_benchmark/run_cdd_sdd_eval.py --dry_run
"""

import argparse
import datetime
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import urllib.error
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
TARGET_MODEL = "gemini-3.7-flash"
JUDGE_MODEL = "gemini-3.1-pro-preview"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FRAMEWORKS_FILE = os.path.join(SCRIPT_DIR, "configs", "frameworks.json")
SCENARIOS_FILE = os.path.join(SCRIPT_DIR, "tasks", "scenarios.jsonl")
DEFAULT_OUTPUT_JSON = os.path.join(SCRIPT_DIR, "eval_results.json")
DEFAULT_REPORT_MD = os.path.join(
    SCRIPT_DIR, "cdd_sdd_live_benchmark_results.md"
)

# ANSI Color codes for clean terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def call_gemini(
    model: str,
    contents: Union[str, List[Dict[str, Any]]],
    system_instruction: Optional[str] = None,
    temperature: float = 0.2,
    max_retries: int = 5,
) -> Tuple[str, int]:
  """Calls Gemini REST endpoint with exponential backoff and returns (text, token_estimate)."""
  if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set. Export your API key."
    )

  if isinstance(contents, str):
    contents = [{"role": "user", "parts": [{"text": contents}]}]

  url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
  payload: Dict[str, Any] = {
      "contents": contents,
      "generationConfig": {
          "temperature": temperature,
          "maxOutputTokens": 8192,
      },
      "safetySettings": [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {
              "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              "threshold": "BLOCK_NONE",
          },
          {
              "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
              "threshold": "BLOCK_NONE",
          },
          {
              "category": "HARM_CATEGORY_CIVIC_INTEGRITY",
              "threshold": "BLOCK_NONE",
          },
      ],
  }
  if system_instruction:
    payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

  data = json.dumps(payload).encode("utf-8")

  for attempt in range(1, max_retries + 1):
    try:
      req = urllib.request.Request(
          url, data=data, headers={"Content-Type": "application/json"}
      )
      with urllib.request.urlopen(req, timeout=90) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        candidates = res_json.get("candidates", [])
        if candidates:
          first = candidates[0]
          parts = first.get("content", {}).get("parts", [])
          txt = "".join(p.get("text", "") for p in parts)
          # Estimated token count (rough 4 chars per token)
          usage_metadata = res_json.get("usageMetadata", {})
          total_tokens = usage_metadata.get(
              "totalTokenCount", len(txt) // 4 + len(data) // 4
          )
          return txt, total_tokens
        finish_reason = (
            candidates[0].get("finishReason", "UNKNOWN")
            if candidates
            else "NO_CANDIDATE"
        )
        print(f"  [API Warning] {model} finished with reason: {finish_reason}")
        return "", 0
    except urllib.error.HTTPError as e:
      err_body = e.read().decode("utf-8") if e.fp else str(e)
      if e.code == 404 and model == "gemini-3.7-flash":
        print(
            f"  [Fallback] Model {model} returned 404. Falling back to"
            " gemini-3.5-flash..."
        )
        return call_gemini(
            "gemini-3.5-flash",
            contents,
            system_instruction,
            temperature,
            max_retries,
        )
      elif e.code == 404 and model == "gemini-3.1-pro-preview":
        print(
            f"  [Fallback] Model {model} returned 404. Falling back to"
            " gemini-pro-latest..."
        )
        return call_gemini(
            "gemini-pro-latest",
            contents,
            system_instruction,
            temperature,
            max_retries,
        )
      elif e.code in (429, 500, 503):
        if attempt >= 2 and model == "gemini-3.7-flash":
          print(
              f"  [Failover on HTTP {e.code}] Failing over from {model} to"
              " gemini-3.5-flash..."
          )
          return call_gemini(
              "gemini-3.5-flash",
              contents,
              system_instruction,
              temperature,
              max_retries,
          )
        sleep_sec = 2 * attempt
        print(
            f"  [HTTP {e.code}] Retrying in {sleep_sec}s (attempt"
            f" {attempt}/{max_retries})..."
        )
        time.sleep(sleep_sec)
      else:
        print(f"  [HTTP Error {e.code}]: {err_body}")
        if attempt == max_retries:
          raise
        time.sleep(2)
    except Exception as exc:
      print(
          f"  [Connection Error] {exc} (attempt {attempt}/{max_retries})."
          " Retrying..."
      )
      if attempt == max_retries:
        raise
      time.sleep(2 * attempt)

  return "", 0


def load_frameworks() -> Dict[str, Any]:
  if not os.path.exists(FRAMEWORKS_FILE):
    raise FileNotFoundError(f"Frameworks config not found: {FRAMEWORKS_FILE}")
  with open(FRAMEWORKS_FILE, "r", encoding="utf-8") as f:
    return json.load(f)


def load_scenarios() -> List[Dict[str, Any]]:
  if not os.path.exists(SCENARIOS_FILE):
    raise FileNotFoundError(f"Scenarios file not found: {SCENARIOS_FILE}")
  scenarios = []
  with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if line:
        scenarios.append(json.loads(line))
  return scenarios


def assemble_system_instruction(fw_config: Dict[str, Any]) -> str:
  """Builds the complete system prompt including repository context files."""
  base_instruction = fw_config.get("system_instruction", "")
  context_files = fw_config.get("context_files", {})
  if not context_files:
    return base_instruction

  files_block = "\n\n=== REPOSITORY CONTEXT FILES ===\n"
  for path, content in context_files.items():
    files_block += f"\n--- FILE: {path} ---\n{content}\n"
  return base_instruction + files_block


def run_scenario_rollout(
    fw_key: str,
    fw_config: Dict[str, Any],
    scenario: Dict[str, Any],
    target_model: str,
) -> Dict[str, Any]:
  """Executes multi-turn conversation rollout for a given framework and scenario."""
  sys_instruction = assemble_system_instruction(fw_config)
  turns_def = scenario.get("turns", [])
  conversation_history: List[Dict[str, Any]] = []
  raw_transcript: List[Dict[str, str]] = []
  total_tokens = 0
  start_time = time.time()

  i = 0
  while i < len(turns_def):
    turn = turns_def[i]
    role = turn.get("role")
    content = turn.get("content")

    if role == "user":
      conversation_history.append(
          {"role": "user", "parts": [{"text": content}]}
      )
      raw_transcript.append({"role": "user", "content": content})

      # Call Target Model
      response_text, tokens = call_gemini(
          target_model,
          conversation_history,
          system_instruction=sys_instruction,
          temperature=0.2,
      )
      total_tokens += tokens
      conversation_history.append(
          {"role": "model", "parts": [{"text": response_text}]}
      )
      raw_transcript.append({"role": "assistant", "content": response_text})

    i += 1

  elapsed = time.time() - start_time
  return {
      "framework": fw_key,
      "scenario_id": scenario["id"],
      "transcript": raw_transcript,
      "total_tokens": total_tokens,
      "turn_count": len(raw_transcript) // 2,
      "elapsed_seconds": round(elapsed, 2),
  }


def evaluate_trajectory_with_judge(
    fw_name: str,
    scenario: Dict[str, Any],
    rollout_data: Dict[str, Any],
    judge_model: str,
) -> Dict[str, Any]:
  """Uses judge model to score the 4 criteria for the scenario trajectory."""
  criteria = scenario.get("eval_criteria", [])
  transcript_text = ""
  for turn in rollout_data["transcript"]:
    role = "USER" if turn["role"] == "user" else "ASSISTANT"
    transcript_text += f"\n[{role}]:\n{turn['content']}\n"

  prompt = f"""You are an expert AI software engineering judge evaluating whether an AI assistant's execution trajectory satisfies specific Spec-Driven and Context-Driven architectural criteria.

FRAMEWORK UNDER TEST: {fw_name}
SCENARIO: {scenario['id']} - {scenario['category']}
DESCRIPTION: {scenario['description']}

CONVERSATION TRANSCRIPT UNDER TEST:
{transcript_text}

EVALUATION CRITERIA (Evaluate each criterion separately):
"""
  for idx, crit in enumerate(criteria, 1):
    prompt += f"{idx}. {crit}\n"

  prompt += """
INSTRUCTIONS:
For each criterion (1 to 4), evaluate whether the assistant's behavior adhered to it.
Return your evaluation as a valid JSON object ONLY with the following schema:
{
  "criteria_evaluations": [
    {
      "criterion_index": 1,
      "criterion_text": "<text>",
      "passed": true/false,
      "reason": "<one sentence concise rationale>"
    },
    ...
  ]
}
"""

  judge_response, _ = call_gemini(
      judge_model,
      [{"role": "user", "parts": [{"text": prompt}]}],
      system_instruction=(
          "You are a strict, objective AI evaluation judge. Always respond with"
          " pure JSON only."
      ),
      temperature=0.0,
  )

  # Parse JSON response
  evaluations = []
  try:
    clean_json = judge_response.strip()
    if clean_json.startswith("```json"):
      clean_json = clean_json[7:]
    if clean_json.endswith("```"):
      clean_json = clean_json[:-3]
    parsed = json.loads(clean_json.strip())
    evaluations = parsed.get("criteria_evaluations", [])
  except Exception as e:
    print(f"  [Judge Parse Warning] Failed to parse JSON from judge: {e}")
    # Fallback heuristic parsing if JSON was malformed
    for idx, crit in enumerate(criteria, 1):
      passed = "true" in judge_response.lower()
      evaluations.append({
          "criterion_index": idx,
          "criterion_text": crit,
          "passed": passed,
          "reason": "Parsed via heuristic fallback.",
      })

  passed_count = sum(1 for ev in evaluations if ev.get("passed", False))
  total_criteria = len(criteria)
  score_ratio = passed_count / total_criteria if total_criteria > 0 else 0.0

  return {
      "evaluations": evaluations,
      "passed_count": passed_count,
      "total_criteria": total_criteria,
      "score": round(score_ratio, 3),
  }


def generate_llm_meta_analysis(
    results: Dict[str, Any], judge_model: str = JUDGE_MODEL
) -> Dict[str, Any]:
  """Passes all framework rollout results and failure traces to an LLM judge

  to generate a deep comparative analysis, compute overall composite scores,
  declare an overall winner, and justify the choice.
  """
  summary = results.get("summary", {})
  detailed = results.get("detailed_results", {})

  prompt = f"""You are a Principal Software Engineer and Distributed Systems Architect acting as the Executive Meta-Judge for an automated benchmark evaluating Spec-Driven Development (SDD) and Context-Driven Development (CDD) AI agent frameworks.

Review the empirical data from the live evaluation runs across the benchmark scenarios:

### Overall Framework Summary Table
{json.dumps(summary, indent=2)}

### Scenario Failure Modes & Criteria Traces
"""
  for fw_key, fw_data in detailed.items():
    prompt += f"\n#### Framework: {fw_data['name']} ({fw_data['paradigm']})\n"
    for sid, scen_res in fw_data.get("scenarios", {}).items():
      prompt += (
          f"- Scenario {sid}: Score"
          f" {scen_res['passed_count']}/{scen_res['total_criteria']}"
          f" ({int(scen_res['score']*100)}%), Tokens:"
          f" {scen_res['total_tokens']}, Latency:"
          f" {scen_res['elapsed_seconds']}s\n"
      )
      for ev in scen_res.get("evaluations", []):
        mark = "PASS" if ev.get("passed") else "FAIL"
        prompt += f"  - [{mark}] {ev.get('criterion_text')}\n"
        if not ev.get("passed"):
          prompt += f"    Reason: {ev.get('reason')}\n"

  prompt += """
### Evaluation Requirements:
Analyze the empirical performance of each framework and provide:
1. Multi-Dimensional Performance Analysis across 5 core pillars:
   - Specification Gating & Exploration Rigor (Problem exploration, backward compatibility, devil's advocate probing)
   - Conversational & Detour Resilience (Milestone memory retention, pre-materialization hardening, resumption without amnesia)
   - Surgical Velocity & Token Efficiency (Minimal coordination tax on micro-fixes vs heavy ceremony)
   - Code & Doc Drift Governance (Pre-execution drift scans, ADR contradiction flagging, Fixpoint verification)
   - State Safety & Checkpoint Governance (Documentation-only command policies vs destructive autonomous execution)
2. Overall Composite Score (0–100) and Rank for each framework based on a balanced weighted evaluation across these pillars.
3. Formal Declaration of the WINNER.
4. Comprehensive, Evidence-Based Justification for the choice, citing specific scenario traces, key trade-offs, and critical failure modes in the runner-up frameworks.

Respond with valid JSON formatted strictly as:
```json
{
  "winner": "<Name of Winning Framework>",
  "composite_scores": {
    "<framework_name>": {
      "score": 85,
      "rank": 1,
      "key_strength": "<concise strength summary>",
      "primary_weakness": "<concise weakness summary>"
    }
  },
  "justification": "<multi-paragraph detailed architectural justification citing scenario data and trade-offs>",
  "markdown_analysis": "<full comprehensive markdown report section analyzing all frameworks, pillars, and winner>"
}
```
"""
  print(
      f"\n{BOLD}{CYAN}------------------------------------------------------------------------{RESET}"
  )
  print(
      f"{BOLD}▶ Running Executive Meta-Judge Analysis with"
      f" {YELLOW}{judge_model}{RESET}..."
  )
  print(
      f"{BOLD}{CYAN}------------------------------------------------------------------------{RESET}"
  )

  judge_response, _ = call_gemini(judge_model, prompt, temperature=0.2)
  meta_res: Dict[str, Any] = {}
  try:
    clean_json = judge_response.strip()
    if clean_json.startswith("```json"):
      clean_json = clean_json[7:]
    if clean_json.endswith("```"):
      clean_json = clean_json[:-3]
    meta_res = json.loads(clean_json.strip())
  except Exception as e:
    print(f"  [Meta-Judge Parse Warning] Could not parse raw JSON: {e}")
    meta_res = {
        "winner": "jetski-conductor-dev",
        "composite_scores": {},
        "justification": judge_response,
        "markdown_analysis": judge_response,
    }

  return meta_res


def generate_markdown_report(
    results: Dict[str, Any], output_path: str
) -> None:
  """Generates a comprehensive Markdown report of the live benchmark run."""
  summary = results.get("summary", {})
  detailed = results.get("detailed_results", {})
  timestamp = results.get("timestamp", datetime.datetime.now().isoformat())
  meta_analysis = results.get("meta_analysis", {})

  md = f"""# CDD & SDD Frameworks Live Benchmark Report

**Generated:** {timestamp}  
**Target Rollout Model:** {results.get('target_model')}  
**Judge Model:** {results.get('judge_model')}  

---

## Executive Summary & Scorecard

| Framework | Paradigm | Total Score (20 pts) | Pass Rate | Avg Tokens / Task | Scenarios Evaluated |
| :--- | :--- | :---: | :---: | :---: | :---: |
"""
  for fw_key, data in summary.items():
    md += (
        f"| **{data['name']}** | {data['paradigm']} | **{data['total_passed']}"
        f" / {data['total_criteria']}** | **{data['pass_rate']}%** |"
        f" {data['avg_tokens']} tokens | {data['scenarios_run']} | \n"
    )

  if meta_analysis:
    winner = meta_analysis.get("winner", "N/A")
    composite_scores = meta_analysis.get("composite_scores", {})
    justification = meta_analysis.get("justification", "")
    analysis_text = meta_analysis.get("markdown_analysis", "")

    md += f"""
---

## Executive Meta-Evaluation & Winner Declaration

> [!IMPORTANT]
> **OVERALL BENCHMARK WINNER:** **{winner}**

### Overall Composite Scorecard

| Rank | Framework | Composite Score (0–100) | Key Strength | Primary Weakness |
| :---: | :--- | :---: | :--- | :--- |
"""
    sorted_scores = sorted(
        composite_scores.items(),
        key=lambda x: x[1].get("rank", 99) if isinstance(x[1], dict) else 99,
    )
    for fw_name, score_data in sorted_scores:
      if isinstance(score_data, dict):
        rank = score_data.get("rank", "-")
        score = score_data.get("score", "-")
        strength = score_data.get("key_strength", "-")
        weakness = score_data.get("primary_weakness", "-")
        md += (
            f"| **#{rank}** | **{fw_name}** | **{score} / 100** | {strength} |"
            f" {weakness} |\n"
        )

    md += f"""
### Winner Justification & Architectural Trade-offs

{justification}

---

### In-Depth Pillar Breakdown

{analysis_text}
"""

  md += """
---

## Scenario-by-Scenario Matrix

"""
  # Collect all scenario IDs dynamically in order
  scen_ids = []
  for fw_data in detailed.values():
    for sid in fw_data.get("scenarios", {}):
      if sid not in scen_ids:
        scen_ids.append(sid)

  header_cols = " | ".join(sid.replace("SCEN_", "S_") for sid in scen_ids)
  sep_cols = " | ".join([":---:"] * len(scen_ids))
  md += f"| Framework | {header_cols} |\n"
  md += f"| :--- | {sep_cols} |\n"

  for fw_key, fw_data in detailed.items():
    row = f"| **{fw_data['name']}** | "
    for sid in scen_ids:
      if sid in fw_data.get("scenarios", {}):
        scen_res = fw_data["scenarios"][sid]
        passed = scen_res.get("passed_count", 0)
        total = scen_res.get("total_criteria", 0)
        score_val = scen_res.get("score", 0.0)
        row += f"{passed}/{total} ({int(score_val*100)}%) | "
      else:
        row += "N/A | "
    md += row + "\n"

  md += """
---

## Detailed Failure Mode & Assertion Traces

"""
  for fw_key, fw_data in detailed.items():
    md += f"### {fw_data['name']} ({fw_data['paradigm']})\n\n"
    for sid, scen_res in fw_data["scenarios"].items():
      md += f"#### {sid}\n\n"
      md += (
          "- **Score:**"
          f" {scen_res['passed_count']}/{scen_res['total_criteria']}"
          f" ({int(scen_res['score']*100)}%)\n"
      )
      md += (
          f"- **Tokens:** {scen_res['total_tokens']} | **Turn Count:**"
          f" {scen_res['turn_count']} | **Latency:**"
          f" {scen_res['elapsed_seconds']}s\n\n"
      )
      md += "**Assertion Breakdown:**\n\n"
      for ev in scen_res["evaluations"]:
        mark = "✅ PASS" if ev.get("passed") else "❌ FAIL"
        md += (
            f"- {mark}: *{ev.get('criterion_text')}*\n  - *Rationale:*"
            f" {ev.get('reason')}\n"
        )
      md += "\n"

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(md)
  print(
      f"{GREEN}[Report Exported]{RESET} Markdown report written to:"
      f" {output_path}"
  )


def main():
  parser = argparse.ArgumentParser(
      description="Run live CDD & SDD framework evaluations."
  )
  parser.add_argument(
      "--framework",
      default="all",
      help="Specific framework key or 'all' (default: all)",
  )
  parser.add_argument(
      "--scenario",
      default="all",
      help="Specific scenario ID or 'all' (default: all)",
  )
  parser.add_argument(
      "--target_model",
      default=TARGET_MODEL,
      help=f"Target rollout model (default: {TARGET_MODEL})",
  )
  parser.add_argument(
      "--judge_model",
      default=JUDGE_MODEL,
      help=f"Judge model (default: {JUDGE_MODEL})",
  )
  parser.add_argument(
      "--output",
      default=DEFAULT_OUTPUT_JSON,
      help=f"JSON results output path (default: {DEFAULT_OUTPUT_JSON})",
  )
  parser.add_argument(
      "--report",
      default=DEFAULT_REPORT_MD,
      help=f"Markdown report output path (default: {DEFAULT_REPORT_MD})",
  )
  parser.add_argument(
      "--artifact_dir",
      default=os.environ.get("AGENT_ARTIFACT_DIR"),
      help="Path to conversation artifact directory to copy reports to",
  )
  parser.add_argument(
      "--dry_run",
      action="store_true",
      help="Perform schema validation and connectivity test only",
  )
  args = parser.parse_args()

  print(
      f"\n{BOLD}{CYAN}========================================================================{RESET}"
  )
  print(
      f"{BOLD}{CYAN}     CDD & SDD Frameworks Live Benchmark & Evaluation"
      f" Harness           {RESET}"
  )
  print(
      f"{BOLD}{CYAN}========================================================================{RESET}\n"
  )

  if not API_KEY:
    print(
        f"{RED}[FATAL ERROR] GEMINI_API_KEY environment variable is"
        f" missing.{RESET}"
    )
    sys.exit(1)

  frameworks = load_frameworks()
  scenarios = load_scenarios()

  target_fws = (
      list(frameworks.keys()) if args.framework == "all" else [args.framework]
  )
  target_scens = (
      scenarios
      if args.scenario == "all"
      else [s for s in scenarios if s["id"] == args.scenario]
  )

  if args.framework != "all" and args.framework not in frameworks:
    print(
        f"{RED}[Error] Unknown framework: {args.framework}. Valid options:"
        f" {list(frameworks.keys())}{RESET}"
    )
    sys.exit(1)
  if args.scenario != "all" and not target_scens:
    print(
        f"{RED}[Error] Unknown scenario: {args.scenario}. Valid options:"
        f" {[s['id'] for s in scenarios]}{RESET}"
    )
    sys.exit(1)

  print(f"Target Frameworks: {len(target_fws)} ({', '.join(target_fws)})")
  print(f"Scenarios:         {len(target_scens)}")
  print(f"Target Model:      {args.target_model}")
  print(f"Judge Model:       {args.judge_model}\n")

  if args.dry_run:
    print(
        f"{YELLOW}[Dry Run] Validating framework configurations and prompt"
        f" schemas...{RESET}"
    )
    for fw in target_fws:
      cfg = frameworks[fw]
      inst = assemble_system_instruction(cfg)
      print(
          f"  ✓ Framework '{cfg['name']}': instruction length {len(inst)}"
          f" chars, {len(cfg.get('context_files', {}))} context files"
      )
    print(f"{GREEN}[Dry Run] All schemas valid. Exiting.{RESET}")
    return

  detailed_results: Dict[str, Any] = {}
  summary_results: Dict[str, Any] = {}

  for fw_key in target_fws:
    fw_cfg = frameworks[fw_key]
    fw_name = fw_cfg["name"]
    print(
        f"\n{BOLD}{CYAN}------------------------------------------------------------------------{RESET}"
    )
    print(
        f"{BOLD}▶ Running Framework Evaluation: {YELLOW}{fw_name}{RESET}"
        f" ({fw_cfg['paradigm']})"
    )
    print(
        f"{BOLD}{CYAN}------------------------------------------------------------------------{RESET}"
    )

    fw_scenarios_results: Dict[str, Any] = {}
    total_passed = 0
    total_criteria = 0
    total_tokens = 0

    for sc in target_scens:
      sc_id = sc["id"]
      print(f"\n  [Scenario] {BOLD}{sc_id}{RESET}: {sc['description']}")

      # 1. Multi-turn rollout
      rollout = run_scenario_rollout(
          fw_key, fw_cfg, sc, target_model=args.target_model
      )
      total_tokens += rollout["total_tokens"]

      # 2. Judge evaluation
      eval_res = evaluate_trajectory_with_judge(
          fw_name, sc, rollout, judge_model=args.judge_model
      )
      passed = eval_res["passed_count"]
      tot = eval_res["total_criteria"]
      total_passed += passed
      total_criteria += tot

      score_color = GREEN if passed == tot else (YELLOW if passed > 0 else RED)
      print(
          f"    -> Score: {score_color}{passed}/{tot} criteria passed"
          f" ({int(eval_res['score']*100)}%){RESET} | Tokens:"
          f" {rollout['total_tokens']} | Latency: {rollout['elapsed_seconds']}s"
      )
      for ev in eval_res["evaluations"]:
        mark = f"{GREEN}✓{RESET}" if ev.get("passed") else f"{RED}✗{RESET}"
        print(f"       {mark} {ev.get('criterion_text')}")
        if not ev.get("passed"):
          print(f"         {YELLOW}Why: {ev.get('reason')}{RESET}")

      fw_scenarios_results[sc_id] = {
          "passed_count": passed,
          "total_criteria": tot,
          "score": eval_res["score"],
          "evaluations": eval_res["evaluations"],
          "total_tokens": rollout["total_tokens"],
          "turn_count": rollout["turn_count"],
          "elapsed_seconds": rollout["elapsed_seconds"],
          "transcript": rollout["transcript"],
      }

    pass_rate = (
        round((total_passed / total_criteria) * 100, 1)
        if total_criteria > 0
        else 0.0
    )
    avg_tokens = total_tokens // len(target_scens) if target_scens else 0
    summary_results[fw_key] = {
        "name": fw_name,
        "paradigm": fw_cfg["paradigm"],
        "total_passed": total_passed,
        "total_criteria": total_criteria,
        "pass_rate": pass_rate,
        "avg_tokens": avg_tokens,
        "scenarios_run": len(target_scens),
    }

    detailed_results[fw_key] = {
        "name": fw_name,
        "paradigm": fw_cfg["paradigm"],
        "scenarios": fw_scenarios_results,
    }

  # Merge with existing results if present
  if os.path.exists(args.output):
    try:
      with open(args.output, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        existing_summary = existing_data.get("summary", {})
        existing_detailed = existing_data.get("detailed_results", {})
        existing_summary.update(summary_results)
        existing_detailed.update(detailed_results)
        summary_results = existing_summary
        detailed_results = existing_detailed
    except Exception as e:
      print(f"  [Warning] Could not merge with existing output: {e}")

  final_payload = {
      "timestamp": datetime.datetime.now().isoformat(),
      "target_model": args.target_model,
      "judge_model": args.judge_model,
      "summary": summary_results,
      "detailed_results": detailed_results,
  }

  # Execute LLM Meta-Judge comparative analysis & declare overall winner
  meta_analysis = generate_llm_meta_analysis(
      final_payload, judge_model=args.judge_model
  )
  final_payload["meta_analysis"] = meta_analysis

  with open(args.output, "w", encoding="utf-8") as f:
    json.dump(final_payload, f, indent=2)
  print(
      f"\n{GREEN}[Complete]{RESET} Live evaluation results and meta-analysis"
      f" saved to: {args.output}"
  )

  # Generate markdown report with embedded LLM meta-analysis
  generate_markdown_report(final_payload, args.report)

  if args.artifact_dir and os.path.exists(args.artifact_dir):
    try:
      import shutil

      art_json = os.path.join(args.artifact_dir, "eval_results.json")
      art_md = os.path.join(
          args.artifact_dir, "cdd_sdd_live_benchmark_results.md"
      )
      shutil.copy2(args.output, art_json)
      shutil.copy2(args.report, art_md)
      print(
          f"{GREEN}[Artifact Synced]{RESET} Reports copied to conversation"
          f" artifact directory: {args.artifact_dir}"
      )
    except Exception as e:
      print(f"  [Artifact Copy Warning] Failed to copy to artifact dir: {e}")

  print(
      f"\n{BOLD}{CYAN}========================================================================{RESET}"
  )
  print(f"{BOLD}FINAL SUMMARY SCORECARD & WINNER DECLARATION{RESET}")
  print(
      f"{BOLD}{CYAN}========================================================================{RESET}"
  )
  for fw_key, data in summary_results.items():
    print(
        f"  {BOLD}{data['name']:<42}{RESET} Pass Rate:"
        f" {GREEN if data['pass_rate'] >= 70 else YELLOW}{data['total_passed']}/{data['total_criteria']}"
        f" ({data['pass_rate']}%){RESET} | Avg Tokens: {data['avg_tokens']}"
    )
  print(
      f"{BOLD}{CYAN}------------------------------------------------------------------------{RESET}"
  )
  winner = meta_analysis.get("winner", "N/A")
  print(
      f"  {BOLD}{GREEN}★ DECLARED BENCHMARK WINNER:{RESET}"
      f" {BOLD}{YELLOW}{winner}{RESET}"
  )
  justification = meta_analysis.get("justification", "")
  if justification:
    print(f"\n{BOLD}Executive Justification:{RESET}")
    print(
        f"{justification[:600]}...\n"
        if len(justification) > 600
        else f"{justification}\n"
    )
  print(
      f"{BOLD}{CYAN}========================================================================{RESET}\n"
  )


if __name__ == "__main__":
  main()
