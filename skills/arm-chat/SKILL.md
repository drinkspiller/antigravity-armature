---
name: arm-chat
description: Load all Armature or Conductor project context (product, tech-stack, guidelines, workflow, active tracks) and proceed immediately to the user's task. Use when asked to "use armature context", "load armature", "armature chat", or when the user wants to work with context without creating tracks or running the full ceremony.
persona: Armature Guide
---

# /arm-chat — Context-Primed Freeform Agent

**Purpose:** Rapidly ingest all Armature/Conductor project knowledge into context and
then proceed directly to the user's task — no follow-up questions, no new
tracks, no approval gates. This is the lightweight complement to the full
Armature workflow.

## When to Use

-   The user wants to leverage existing project knowledge to inform a
    coding task, research question, or design decision.
-   The user wants to "just go" with project context without the ceremony of
    creating tracks, specs, or plans.
-   The user invokes `/arm-chat` or asks to "load armature context."

## Protocol

### Step 1: Locate the Context Directory

> [!NOTE] Project root resolution is handled by `armature_protocol.md` §7.
> If protocol §7 has already resolved `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}`, skip directly to Step 2.

1.  **Resolve Context Directory**: Follow `armature_protocol.md` §7 to resolve `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` (armature or conductor).
2.  **Validate** that at least `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md` exists. If not, suggest running `/arm-setup`.

### Step 2: Tiered Context Loading

Load the project context in two tiers. Read files silently — do NOT produce
artifacts, summaries, or status reports for the loading process itself.

#### Tier 1: Core Context (always loaded)

Read the following files in order:
1.  `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md` — Product definition & vision
2.  `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product-guidelines.md` — Tone, visual identity, UX
3.  `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md` — Technical choices & frameworks
4.  `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md` — Task workflow & coding practices
5.  `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md` — Track registry

#### Tier 2: Active Track Context (loaded selectively)

1.  Parse `tracks.md` for all tracks. Identify tracks marked as in-progress (`[~]`) or pending (`[ ]`).
2.  For each active or pending track, read `spec.md` and `plan.md`.
3.  Skip archived tracks unless requested.

#### Tier 2b: Code Style Guides (loaded if present)

If `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/code_styleguides/` exists, read all files in it.

#### Tier 2c: Manual Testing Runbooks (loaded on demand)

If the user's task touches files mapped to a specific domain (or active domain terms from `terms.md`), load `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md` on demand.

### Step 3: Act on the User's Task

After context is loaded, determine next action:

-   **If prompt contains a task/question:** Proceed immediately to fulfilling it using standard agent tools.
-   **Continuous Manual Testing Maintenance**: Whenever implementation introduces new functionality or route changes:
    -   Update `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md` (or track `manual_testing.md`).
    -   Use structured scenario headers (`### Test <Domain>.<ID>: <Scenario Title>`).
    -   **Documentation-Only Invariant**: Do NOT execute mutative database or reset commands autonomously.
    -   Write updated guide as artifact (`arm_manual_testing_<domain>.md`).
    -   In response, provide clickable markdown link to the file.
-   **If no accompanying prompt:** Announce context is loaded and ask what the user would like to work on.

## Guardrails

-   **Permitted File Updates**: You are explicitly permitted to update `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md`.
-   **Read-Only Files**: Do NOT modify `product.md`, `tech-stack.md`, `product-guidelines.md`, `tracks.md`, or track `spec.md`/`plan.md` unless requested.
-   **No Ceremony**: Do NOT create artifacts for the loading process.
