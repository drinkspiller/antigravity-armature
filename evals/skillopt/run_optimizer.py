#!/usr/bin/env python3
"""
Conductor SkillOpt Evaluation & Optimization Runner.

A zero-external-dependency benchmarking and optimization runner for the
Conductor skill suite. Evaluates skills against structured task suites and
optionally optimizes instructions using Gemini model reflection.

Usage:
  # Run benchmark on all tasks across all skills:
  python3 evals/skillopt/run_optimizer.py --eval_only

  # Run benchmark for a specific skill:
  python3 evals/skillopt/run_optimizer.py --target=skills/conductor-new-track/SKILL.md --eval_only

  # Run full optimization loop on a skill:
  python3 evals/skillopt/run_optimizer.py --target=skills/conductor-new-track/SKILL.md --optimize
"""

import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

TARGET_MODEL = "gemini-3.5-flash"
OPTIMIZER_MODEL = "gemini-3.1-pro-preview"
API_KEY = os.environ.get("GEMINI_API_KEY")

EVALS_DIR = os.path.dirname(os.path.abspath(__file__))
CONDUCTOR_ROOT = os.path.abspath(os.path.join(EVALS_DIR, "..", ".."))
TRAIN_PATH = os.path.join(EVALS_DIR, "tasks", "train.jsonl")
VAL_PATH = os.path.join(EVALS_DIR, "tasks", "val.jsonl")
RESULTS_PATH = os.path.join(EVALS_DIR, "eval_results.json")


def call_gemini(
    model: str,
    prompt: str,
    system_instruction: str = None,
    temperature: float = 0.2,
    max_retries: int = 5,
) -> str:
  if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Set GEMINI_API_KEY environment variable."
    )

  url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
  payload = {
      "contents": [{"parts": [{"text": prompt}]}],
      "generationConfig": {
          "temperature": temperature,
          "maxOutputTokens": 8192,
      },
      "safetySettings": [
          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
          {"category": "HARM_CATEGORY_CIVIC_INTEGRITY", "threshold": "BLOCK_NONE"},
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
          if "content" in first:
            parts = first["content"].get("parts", [])
            return "".join(p.get("text", "") for p in parts)
          else:
            finish_reason = first.get("finishReason", "UNKNOWN")
            print(f"  [API Warning] {model} finished with reason: {finish_reason}", file=sys.stderr, flush=True)
        return ""
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
      print(
          f"  [API Warning] {model} call failed (attempt {attempt}/{max_retries}): {e}",
          file=sys.stderr,
          flush=True,
      )
      if attempt == max_retries:
        raise
      time.sleep(2 * attempt)
  return ""


def load_tasks(filepath: str, target_skill: str = None):
  tasks = []
  if not os.path.exists(filepath):
    return tasks
  with open(filepath, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if not line:
        continue
      task = json.loads(line)
      if target_skill and target_skill != "all":
        skill_name = os.path.basename(os.path.dirname(target_skill)) if target_skill.endswith("SKILL.md") else target_skill
        if task.get("target_skill") and task.get("target_skill") != skill_name:
          continue
      tasks.append(task)
  return tasks


def resolve_skill_path(target_arg: str) -> str:
  if os.path.isabs(target_arg):
    return target_arg
  direct_path = os.path.join(CONDUCTOR_ROOT, target_arg)
  if os.path.exists(direct_path):
    return direct_path
  skill_dir = os.path.join(CONDUCTOR_ROOT, "skills", target_arg, "SKILL.md")
  if os.path.exists(skill_dir):
    return skill_dir
  return direct_path


def get_skill_text_for_task(task: dict, default_skill_text: str, default_skill_name: str) -> str:
  task_target = task.get("target_skill")
  if not task_target or task_target == default_skill_name:
    return default_skill_text
  skill_path = resolve_skill_path(f"skills/{task_target}/SKILL.md")
  if os.path.exists(skill_path):
    with open(skill_path, "r", encoding="utf-8") as f:
      return f.read()
  return default_skill_text


def evaluate_task(task: dict, default_skill_text: str, default_skill_name: str):
  skill_text = get_skill_text_for_task(task, default_skill_text, default_skill_name)
  target_skill_name = task.get("target_skill", default_skill_name)

  system_instruction = (
      f"You are an AI assistant executing instructions in the Conductor '{target_skill_name}' skill document strictly:\n\n"
      f"```markdown\n{skill_text}\n```\n\n"
      "Follow all guardrails, turn-ending barriers, step sequencing, and interaction protocols exactly."
  )

  rollout_prompt = (
      f"Execute the following user request and scenario:\n\n{task['prompt']}\n\n"
      "Detail every action, step number, tool invocation (e.g. ask_question, write_to_file, etc.), "
      "and the exact output/questions you present to the user."
  )

  try:
    rollout_output = call_gemini(
        TARGET_MODEL,
        rollout_prompt,
        system_instruction=system_instruction,
        temperature=0.1,
    )
  except Exception as e:
    print(f"  [Rollout Error] Task {task['id']} failed: {e}", flush=True)
    rollout_output = f"[ERROR: Execution failed with exception: {e}]"

  criteria = task.get("eval_criteria") or task.get("criteria", [])
  judge_prompt = f"""You are a strict evaluator assessing whether an agent's execution rollout satisfies each required criterion.

Task Scenario:
{task['prompt']}

Target Skill: {target_skill_name}

Agent Rollout Output:
\"\"\"
{rollout_output}
\"\"\"

Evaluation Criteria to assess:
{json.dumps(criteria, indent=2)}

For each criterion in the list above, output a JSON object with:
- "criterion": the exact text of the criterion
- "passed": boolean (true if satisfied, false if violated or skipped)
- "reason": 1-sentence explanation of evidence from the rollout output

Respond with ONLY a valid JSON array of objects:
[
  {{"criterion": "...", "passed": true/false, "reason": "..."}},
  ...
]
"""
  try:
    judge_raw = call_gemini(OPTIMIZER_MODEL, judge_prompt, temperature=0.0)
    match = re.search(r"\[.*\]", judge_raw, re.DOTALL)
    if match:
      eval_results = json.loads(match.group(0))
    else:
      eval_results = [
          {"criterion": c, "passed": False, "reason": "Failed to parse judge JSON"}
          for c in criteria
      ]
  except Exception as e:
    print(f"  [Judge Error] Task {task['id']} judge failed: {e}", flush=True)
    eval_results = [
        {"criterion": c, "passed": False, "reason": str(e)} for c in criteria
    ]

  passed_count = sum(1 for r in eval_results if r.get("passed", False))
  total_count = len(criteria)
  score = passed_count / total_count if total_count > 0 else 0.0

  return {
      "task_id": task["id"],
      "target_skill": target_skill_name,
      "category": task.get("category", ""),
      "score": score,
      "passed_count": passed_count,
      "total_count": total_count,
      "eval_results": eval_results,
      "rollout_sample": rollout_output[:1000],
  }


def run_benchmark(default_skill_text: str, default_skill_name: str, tasks: list, split_name: str):
  print(f"\n--- Running Benchmark on {split_name} ({len(tasks)} tasks) ---", flush=True)
  task_results = []
  total_passed = 0
  total_criteria = 0

  for task in tasks:
    res = evaluate_task(task, default_skill_text, default_skill_name)
    task_results.append(res)
    total_passed += res["passed_count"]
    total_criteria += res["total_count"]
    print(
        f"  Task {res['task_id']} [{res['target_skill']}] ({res['category']}): Score = {res['score']:.2f} ({res['passed_count']}/{res['total_count']})",
        flush=True,
    )
    for r in res["eval_results"]:
      status = "PASS" if r.get("passed") else "FAIL"
      print(f"    [{status}] {r.get('criterion')}: {r.get('reason')}", flush=True)

  aggregate_score = total_passed / total_criteria if total_criteria > 0 else 0.0
  print(
      f"-> {split_name} Aggregate Score: {aggregate_score:.4f} ({total_passed}/{total_criteria})",
      flush=True,
  )
  return aggregate_score, task_results


def validate_syntax_and_clip(seed_text: str, candidate_text: str) -> tuple[bool, str]:
  if not (candidate_text.startswith("---") and "\nname:" in candidate_text and "\ndescription:" in candidate_text):
    return False, "Malformed YAML frontmatter"

  seed_lines = seed_text.splitlines()
  cand_lines = candidate_text.splitlines()
  matcher = difflib.SequenceMatcher(None, seed_lines, cand_lines)
  ratio = matcher.ratio()
  diff_pct = (1.0 - ratio) * 100
  if diff_pct > 40.0:
    return False, f"Edit distance too large: {diff_pct:.1f}% modified (limit is 40%)"

  return True, f"Valid (diff: {diff_pct:.1f}%)"


def reflect_and_mutate(current_skill: str, failed_traces: list, val_score: float) -> str:
  print("\n--- Reflecting on Failure Traces & Synthesizing Surgical Patch ---", flush=True)
  step_sizing = (
      "Current performance is below 0.70. Perform structural additions, missing procedural steps, and strict prerequisite barriers."
      if val_score < 0.70
      else "Current performance is >= 0.70. Perform minimal surgical edits (targeted phrasing, single-line constraints, strict sequencing guards) while preserving working sections."
  )

  reflection_prompt = f"""You are an expert prompt engineer and Skill Optimizer optimizing a Conductor skill markdown file.

Failed Task Traces & Violated Criteria:
{json.dumps(failed_traces, indent=2)}

Optimization Guidelines:
{step_sizing}

Current SKILL.md Content:
\"\"\"markdown
{current_skill}
\"\"\"

Requirements for Candidate Mutation:
1. Maintain valid YAML frontmatter (name, description, persona).
2. Fix the violated criteria surgically without degrading working features.
3. Preserve all existing guardrails, step alignments, and interaction barriers.
4. Output the FULL updated SKILL.md in a single ```markdown ... ``` block without conversational preamble.
"""
  candidate_raw = call_gemini(OPTIMIZER_MODEL, reflection_prompt, temperature=0.2)
  match = re.search(r"```markdown\s*\n(.*?)\n```", candidate_raw, re.DOTALL)
  if match:
    return match.group(1).strip()
  match = re.search(r"```\s*\n(.*?)\n```", candidate_raw, re.DOTALL)
  if match:
    return match.group(1).strip()
  return candidate_raw.strip()


def main():
  parser = argparse.ArgumentParser(description="Conductor SkillOpt Benchmarking & Optimization")
  parser.add_argument(
      "--target",
      default="all",
      help="Target skill path relative to conductor root or skill name (e.g. skills/conductor-new-track/SKILL.md, or 'all')",
  )
  parser.add_argument(
      "--eval_only",
      action="store_true",
      help="Run evaluation benchmarks without mutation",
  )
  parser.add_argument(
      "--optimize",
      action="store_true",
      help="Run full SkillOpt optimization loop",
  )
  parser.add_argument(
      "--epochs",
      type=int,
      default=2,
      help="Number of optimization epochs (default: 2)",
  )
  args = parser.parse_args()

  target_skill_name = "all"
  skill_text = ""
  target_path = "all"

  if args.target != "all":
    target_path = resolve_skill_path(args.target)
    if not os.path.exists(target_path):
      sys.exit(f"Target skill path does not exist: {target_path}")
    target_skill_name = os.path.basename(os.path.dirname(target_path)) if target_path.endswith("SKILL.md") else args.target
    with open(target_path, "r", encoding="utf-8") as f:
      skill_text = f.read()

  print("=== Conductor SkillOpt Evaluation Runner ===", flush=True)
  print(f"Target: {target_path}")
  print(f"Target Model: {TARGET_MODEL} | Optimizer Model: {OPTIMIZER_MODEL}")

  train_tasks = load_tasks(TRAIN_PATH, args.target)
  val_tasks = load_tasks(VAL_PATH, args.target)
  print(f"Loaded {len(train_tasks)} train tasks and {len(val_tasks)} val tasks.")

  train_score, train_res = run_benchmark(skill_text, target_skill_name, train_tasks, "TRAIN")
  val_score, val_res = run_benchmark(skill_text, target_skill_name, val_tasks, "VAL")

  results = {
      "target": target_path,
      "baseline": {
          "train_score": train_score,
          "val_score": val_score,
      },
      "train_results": train_res,
      "val_results": val_res,
  }

  with open(RESULTS_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

  print(f"\nResults saved to: {RESULTS_PATH}")

  if args.optimize and args.target != "all" and val_score < 1.0:
    best_skill = skill_text
    best_val_score = val_score

    for epoch in range(1, args.epochs + 1):
      print(f"\n=== Optimization Epoch {epoch}/{args.epochs} ===")
      failed_traces = []
      for tr in train_res:
        failed_criteria = [r for r in tr["eval_results"] if not r.get("passed", False)]
        if failed_criteria:
          failed_traces.append({
              "task_id": tr["task_id"],
              "category": tr["category"],
              "failed_criteria": failed_criteria,
              "rollout_sample": tr["rollout_sample"],
          })

      if not failed_traces:
        print("All train criteria passed.")
        break

      candidate = reflect_and_mutate(best_skill, failed_traces, best_val_score)
      valid, msg = validate_syntax_and_clip(best_skill, candidate)
      print(f"Syntax & Clip Guard: {msg}")
      if not valid:
        continue

      cand_val_score, _ = run_benchmark(candidate, target_skill_name, val_tasks, f"VAL (Candidate Epoch {epoch})")
      if cand_val_score > best_val_score:
        print(f"Accepted candidate: {best_val_score:.4f} -> {cand_val_score:.4f}")
        best_skill = candidate
        best_val_score = cand_val_score

    best_out_path = os.path.join(EVALS_DIR, f"best_{target_skill_name}.md")
    with open(best_out_path, "w", encoding="utf-8") as f:
      f.write(best_skill)
    print(f"Optimized skill written to: {best_out_path}")


if __name__ == "__main__":
  main()
