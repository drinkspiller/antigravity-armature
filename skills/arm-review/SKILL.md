---
name: arm-review
description: Review completed work against specifications, guidelines, and quality gates. Use when asked to review a track, check work quality, run acceptance criteria, or run /arm-review.
persona: Armature Reviewer
---

# /arm-review — Review Completed Work

**Purpose:** Review completed work against specifications and guidelines to
ensure code quality, correctness, and adherence to project standards.

## Protocol

### 1. Initialization

1.  **Context Resolution & Setup Check:**
    -   Resolve `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` (armature or conductor) per `armature_protocol.md` §7.
    -   Verify that core files exist: `tracks.md`, `product.md`, `tech-stack.md`, `workflow.md`, `product-guidelines.md`.
    -   If any are missing, halt execution and inform the user that Armature is not fully initialized.

### 2. Execution Phase

#### 2.1 Scope Identification

1.  Check for user-provided arguments describing what to review.
2.  **Auto-detect:** Read `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md` and look for an in-progress track (`[~]`).
3.  Confirm selection via `ask_question`: "Review track '<track_name>'?" (Options: "Yes", "No, specify scope").
4.  If no track is found, prompt for review scope.

#### 2.2 Context Retrieval

1.  Load `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product-guidelines.md` and `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md`.
2.  Load ALL files in `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/code_styleguides/`. Treat these as "Law".
3.  Check for installed skills and enable specialized feedback if relevant.
4.  Load the track's `plan.md` and `spec.md`. Extract commit SHAs/revisions from `plan.md`.
5.  Determine the revision range for the review based on the plan and current workspace state.

#### 2.3 Smart Chunking & Review Process

1.  **Volume check:** Run VCS diff stat.
2.  Determine diff size:
    -   **Small/Medium (<300 lines):** Perform a single-pass review by reading the full diff output.
    -   **Large (>300 lines):** Confirm with user via `ask_question`: "Iterative Review Mode may take longer. Proceed?"
        -   If yes: Review each source file individually using `view_file` (skip lock files and assets). Store per-file findings and aggregate them.
        -   If no: Attempt a high-level summary review or ask user to narrow scope.

#### 2.4 Analysis Checklist

Evaluate the changed code against the following criteria:

-   **Intent verification:** Does the implementation fulfill requirements in `plan.md` and `spec.md`?
-   **ADR compliance:** For each ADR in `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/adr/` active in the modified modules, verify adherence to the recorded decision and its confirmation checklist.
-   **Style compliance:** Are `product-guidelines.md` and `code_styleguides/*.md` rules followed?
-   **Correctness & safety:** Check for bugs, race conditions, null risks, hardcoded secrets, or PII.
-   **Automated testing:** Check for new automated tests covering changes. Run test suite.
-   **Manual testing runbook:** Explicitly audit changed routes, navigation guards, persona transitions, and error handlers against `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_name>/manual_testing.md`.
-   **Skill-specific checks:** Apply specialized guidelines from relevant installed skills.

### 3. Review & Resolution

#### 3.1 Report & Decision

Generate review report as a Antigravity artifact (save to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_name>/review.md` using `write_to_file`).

Use the following strict output format for the report:

```markdown
# Code Review Report: Track <track_name>

## Executive Summary
{1-2 paragraphs summarizing the review outcome, key strengths, and overall readiness}

## Verification Checks
- **Automated Testing:** [Pass / Fail / Warnings]
- **Manual Testing Runbook:** [Pass / Fail / Warnings]
- **ADR Compliance:** [Pass / Fail / Warnings]
- **Style & Standards:** [Pass / Fail / Warnings]
- **Fixpoint Audit:** [Pass / Fail]

## Detailed Findings
{Numbered findings categorized by severity: [BLOCKING], [WARNING], [NOTE]}

## Recommendation
{Clear recommendation: Approve / Approve with Minor Edits / Revise Required}
```

#### 3.2 Resolution & Next Steps

Use `ask_question` to present structured next steps:
1. "Approve and proceed to track completion (/arm-implement Step 5)"
2. "Address findings and re-review"
3. "Acknowledge findings as tech debt"
