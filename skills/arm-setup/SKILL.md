---
name: arm-setup
description: Initialize or update a project's Armature context. Use when asked to set up armature, initialize project context, create armature directory, or run /arm-setup.
persona: Armature Architect
---

# /arm-setup — Initialize Project Context

**Purpose:** Initialize or update the project's Armature context (run once per
project).

## Protocol

1.  **Project Audit (§1.2):**

    -   Check if `{PROJECT_ROOT}/armature/` or `{PROJECT_ROOT}/conductor/` exists.
    -   **Tier 1:** If `{PROJECT_ROOT}/armature/` exists:
        -   Set `{PROJECT_CONTEXT_DIR} = armature`.
        -   Read `{PROJECT_ROOT}/armature/setup_state.json` to determine which artifacts are configured.
        -   Map existing artifacts to their target sections, skip completed ones, and resume from the next incomplete artifact.
    -   **Tier 2 (Legacy):** If `{PROJECT_ROOT}/conductor/` exists and `armature/` does not:
        -   Set `{PROJECT_CONTEXT_DIR} = conductor`.
        -   Read `{PROJECT_ROOT}/conductor/setup_state.json` to determine which artifacts are already configured.
        -   Map existing artifacts to their target sections, skip completed ones, and resume from the next incomplete artifact.
    -   **Greenfield:** If none exists:
        -   Set `{PROJECT_CONTEXT_DIR} = armature`.
        -   Create the directory `{PROJECT_ROOT}/armature/` and `{PROJECT_ROOT}/armature/setup_state.json`.

2.  **Brownfield / Greenfield Detection (§2.0):**

    -   Detect project maturity by checking for existing dependency manifests
        (e.g., `package.json`, `pom.xml`, `requirements.txt`, `go.mod`,
        `Cargo.toml`) and ./Git `BUILD` files.
    -   Check for common source code directories (e.g., `src/`, `app/`, `lib/`,
        `bin/`).
    -   If indicators are found, this is a **Brownfield** project. Before
        scanning, use `ask_question` to gate access: "A brownfield project
        detected. May I perform a read-only scan?"
        -   Upon approval, perform a read-only scan to extract the tech stack
        -   Respect `.geminiignore` and `.gitignore` when scanning.
        -   Handle large files (>1MB) carefully: only read the head and tail 20
            lines.
    -   If no indicators are found, this is a **Greenfield** project.

3.  **Artifact Generation Protocol:** For each missing artifact, follow the
    steps below. Generate one artifact at a time.

    -   Present structured choices to the user using `ask_question` or write
        clarifying questions as a Antigravity artifact (`write_to_file`).
    -   **Draft Review Loop**: After drafting an artifact, present it for review
        using `ask_question` with options: "Approve" or "Suggest changes". Loop
        until approved.
    -   Present each generated context file using `notify_user` with
        `PathsToReview` pointing to the file.
    -   Update `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/setup_state.json` after each approval.

--------------------------------------------------------------------------------

### Artifact 1: `product.md`

Use `ask_question` to present structured options: "Interactive" or
"Autogenerate" for drafting `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md`.
- **Interactive**: Guide the user through questions about project name, target users, core value proposition, key features, and competitive landscape.
- **Autogenerate**: Draft the document based on a brief project goal provided by the user.

Draft the document, enter the Draft Review Loop ("Approve" or "Suggest changes"), and upon approval, write it to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md` and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 2: `product-guidelines.md`

Use `ask_question` to present structured options: "Interactive" or
"Autogenerate" for drafting `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product-guidelines.md`.
- **Interactive**: Guide user through tone, brand identity, UX patterns, and accessibility requirements.
- **Autogenerate**: Draft based on project goals or brownfield codebase insights.

Draft the document, enter the Draft Review Loop, write the file and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 3: `tech-stack.md`

For drafting `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md`:
- **For Greenfield**: Use `ask_question` to present "Interactive" or "Autogenerate". Ask languages, frameworks, databases, and CI/CD tools.
- **For Brownfield**: State inferred tech stack from scan and confirm with user via `ask_question`.

Draft document, enter Draft Review Loop, write the file and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 4: `code_styleguides/`

Based on the tech stack identified, recommend style guides for each language.
- Write to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/code_styleguides/` (e.g., `python.md`, `typescript.md`).
- Enter Draft Review Loop for each, write files and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 5: `workflow.md`

Use `ask_question` to present "Default" or "Customize" for drafting `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md`.
- **Default**: Use standard TDD conventions, default commit frequency, and generic coverage targets.
- **Customize**: Ask preferred coverage target, commit frequency, commit message format, specific build/test commands, and phase checkpointing.

Draft document, enter Draft Review Loop, write the file and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 6: Skills Selection (§2.6)

Check for existing skills catalog or directories containing agent skills.
- Recommend specific skills based on tech stack.
- Use `ask_question` to present structured options: "Install recommended", "Hand-pick skills", or "Skip".
- Update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 7: `tracks.md` and `index.md`

Generate:
- `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md` — An empty track registry with standard heading.
- `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/index.md` — A central index linking to all newly created context files.

Enter Draft Review Loop for both. Upon approval, write files and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 8: `terms.md`

Use `ask_question` to present structured options: "Interactive", "Autogenerate", or "Skip for now".
- **Interactive**: Guide through domain concepts and non-standard terms.
- **Autogenerate (Brownfield only)**: Extract domain nouns via AST scan.
- **Skip for now**: Proceed without creating a glossary.

Draft document, enter Draft Review Loop, write to `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/terms.md` and update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 8b: Living Manual Testing Runbooks (`manual_testing/`)

Initialize `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/manual_testing/`:
- Copy bundled `manual_testing_template.md` template into `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/manual_testing/`.
- For brownfield projects with identifiable functional domains (e.g., auth, billing, navigation), create initial domain runbooks (`{PROJECT_CONTEXT_DIR}/manual_testing/<domain>.md`) seeded with baseline smoke scenarios.
- Update `setup_state.json`.

--------------------------------------------------------------------------------

### Artifact 8c: Architecture Decision Records (`adr/`) & Preflight Sweep

Initialize `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/adr/`:
- Copy bundled `adr_template.md` template into `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/adr/`.
- **Brownfield ADR Preflight Sweep**: Sweep existing project documentation for unrecorded architectural trade-offs.
- If unformalized decisions are detected, offer via `ask_question` to formalize into initial ADR files (`{PROJECT_CONTEXT_DIR}/adr/0001-slug.md`, etc.).
- Update `setup_state.json`.

--------------------------------------------------------------------------------

### Finalization (§2.7)

1.  **Commit Setup Files**: Commit all generated context files using VCS
    commands with a clear message like `chore: initialize armature context`.
2.  **Summarize Actions**: Display a summary of all actions taken and list all
    created files.
3.  **Closing**: Present the final message: "✅ Armature setup complete! Run
    `/arm-new-track` to start your first feature or bug fix track."
