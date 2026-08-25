---
name: arm-status
description: Get a high-level overview of project progress across all tracks. Use when asked for project status, track progress, what's done, or run /arm-status.
persona: Armature Observer
---

# /arm-status — View Project Progress

**Purpose:** Get a high-level overview of project progress.

## Protocol

1.  **Context Resolution & Setup Check:**
    -   Resolve `{PROJECT_ROOT}` and `{PROJECT_CONTEXT_DIR}` (armature or conductor) per `armature_protocol.md` §7.
    -   Verify that the following core files exist:
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md`
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/product.md`
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tech-stack.md`
        -   `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/workflow.md`

    If any of these files are missing, halt execution and inform the user that
    the Armature context is incomplete.

2.  **Read and Parse Tracks:**

    -   Read `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks.md`.
    -   Parse the tracks. You must support BOTH the standard format (`- [ ] **Track:`) AND the legacy format (`## [ ] Track:`).
    -   Note the status of each track based on its checkbox:
        -   `[x]` = ✅ Complete
        -   `[~]` = 🔄 In Progress
        -   `[ ]` = ⬜ Pending

3.  **Analyze Task-Level Progress:**

    -   For each track, read its
        `{PROJECT_ROOT}/{PROJECT_CONTEXT_DIR}/tracks/<track_id>/plan.md` to get task-level
        progress.
    -   Extract current phase and task (marked `[~]`), next pending task
        (marked `[ ]`), and explicitly noted blockers.

4.  **Generate the Enhanced Status Summary:** Write the status summary as a
    Antigravity artifact (`arm_status.md`, `ArtifactType: walkthrough` using
    `write_to_file`) and present via `notify_user` with
    `PathsToReview`.

    Include the following structured information in the artifact:

    **Overview:**

    -   **Current Date/Time:** <current timestamp>
    -   **Project Status:** High-level assessment ("On Track", "Behind
        Schedule", "Blocked") based on tasks and blockers
    -   **Fixpoint Health:** Current drift health status (e.g., "✅ Fixpoint Reached (0 drift)" or "⚠️ Drift Detected (N issue(s) — run `/arm-drift`)")
    -   **Current Phase and Task:** The specific phase/task marked `[~]` in the
        active track
    -   **Next Action Needed:** The next `[ ]` pending task
    -   **Blockers:** Items explicitly marked as blockers
    -   **Phases:** Total phases
    -   **Tasks:** Total tasks
    -   **Progress:** tasks_completed / tasks_total (percentage%)

    **Track Registry Summary:** Display in table format:

    ```markdown
    ## Project Status

    ### Track Registry
    
    |---|-------|--------|
    
    
    
    ```

    **Phase/Task Breakdown:** For each in-progress track, display the plan
    structure:

    ```markdown
    ### Active Track: <track_name>
    - Phase 1: ✅ Complete
    - Phase 2: 🔄 In Progress
      - [x] Task 1
      - [x] Task 2
      - [~] Task 3 (current)
      - [ ] Task 4
      - [ ] Task 5
    - Phase 3: ⬜ Pending
    ```

    **Summary Statistics:** Total tracks: N, Completed: N, In progress: N, Pending: N.

5.  **Next Steps:** Use `ask_question` to present structured choices:
    1.  Implement the current task (/arm-implement)
    2.  Start a new track (/arm-new-track)
    3.  Review completed work (/arm-review)
    4.  Audit drift (/arm-drift)
