# CDD Protocols (Drift Scan, ADR Capture, Per-Directory Context)

> Loaded on demand by Conductor skills. Not an always-on rule.

## 9. Pre-Execution Drift Scan

After completing context loading (items 1–7), and before executing the invoked
skill's primary protocol, perform a lightweight drift check:

1.  **Diff stat:** Run a VCS diff stat (`git diff --stat` / `hg diff --stat`)
    against the last Conductor checkpoint commit (or HEAD if no checkpoint
    exists). This yields the list of files with uncommitted or recent changes.
2.  **Scope matching:** For each changed file, scan the loaded ADRs in
    `conductor/adr/*.md` and directory context files for scope annotations that
    reference the changed file or its parent directory.
3.  **Targeted read:** For each scope match, read the changed file and the
    matching ADR decision statement or confirmation rule. Check for surface-level
    contradictions (e.g., ADR says "use WebSocket for mutations" but the file
    adds a direct REST call).
4.  **Resolution:** If drift is detected:
    -   Present a `> [!WARNING]` callout naming the ADR/rule, the file, and
        the contradiction.
    -   Use `ask_question` with a randomized prompt:
        *   "Drift detected against {source}. How to handle?"
        *   "The code diverges from {source}. What's the call?"
        *   *Options*: `["Fix the code now", "Update the ADR",
            "Acknowledge as tech debt and proceed", "Show me the details"]`
    -   Handle the selection:
        -   **Fix the code now**: Apply a targeted fix before proceeding with
            the originally invoked command.
        -   **Update the ADR**: Draft an update or amendment to the relevant ADR
            and enter a Draft Review Loop.
        -   **Acknowledge as tech debt**: Log the divergence in the active
            track's `spec.md` under a `## Tech Debt` section (create if absent)
            and proceed.
        -   **Show me the details**: Display the full ADR text and the
            relevant diff, then re-present the resolution options.
5.  **No drift:** If no scope matches are found or no contradictions are
    detected, proceed silently — no output overhead.

## 10. ADR Capture Protocol

Architectural decisions and non-negotiable behavioral contracts (ordering
constraints, null-check requirements, state guards, initialization rules)
must be recorded in `{PROJECT_ROOT}/conductor/adr/NNNN-slug.md`.

### Capture Triggers

ADR capture can fire at five points in the Conductor lifecycle:

1.  **During spec generation** (`/conductor_newTrack` Step 10 — Devil's
    Advocate): when a challenge reveals an architectural trade-off or ordering
    assumption.
2.  **During design decisions** (`/conductor_newTrack` Step 6): when an interview
    decision establishes a project-wide pattern or technology choice.
3.  **During implementation** (`/conductor_implement` Step 3): when the agent
    writes a guard, assertion, or safety constraint that extends beyond the
    active track.
4.  **During review** (`/conductor_review` § 2.4): when a correctness finding
    implies an architectural rule or race condition fix.
5.  **User-initiated**: when the user explicitly states a non-negotiable rule.

### Capture Interaction

At each trigger point, the agent follows this protocol:

1.  Identify the architectural decision or behavioral contract (ordering
    constraint, state guard, initialization requirement).
2.  Present via `ask_question` with a randomized prompt:
    *   "This establishes an architectural rule: '{description}'. Record an ADR?"
    *   "A load-bearing constraint worth preserving: '{description}'. Capture it as an ADR?"
    *   *Options*: `["Yes — draft an ADR", "Yes, but rephrase it", "No — track-specific only"]`
3.  If accepted:
    -   Find the next sequential number (e.g., `0003-slug.md`).
    -   Draft the ADR following standard MADR format (`Status`, `Context`,
        `Decision`, `Consequences`, `Confirmation`).
    -   Save to `{PROJECT_ROOT}/conductor/adr/NNNN-slug.md`.

## 11. Per-Directory Context Protocol

For complex project modules, per-directory context reduces the context loading
tax by scoping what the agent reads to what's relevant for the current task.

### Section Format

Conductor manages a `## Conductor Context` section inside existing agent context
files (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`). The section is
delimited by boundary comments:

```markdown
<!-- Conductor Context: START (manual edits go above this line) -->
## Conductor Context

### Purpose
{1-2 sentences describing the directory's role}

### Local Rules
{Directory-scoped rules, handler conventions, and failure handling policies}

### Relevant ADRs
- [ADR-NNNN: Title](file:///conductor/adr/NNNN-slug.md)

### Key Types
{Primary exported types, classes, and functions}

### Term Overrides
{Terms used differently in this directory vs project-level terms.md}
<!-- Conductor Context: END (manual edits go below this line) -->
```

### Multi-File Discovery & Creation

Before modifying files in a directory for the first time in a track, check
case-insensitively for existing agent context files: `GEMINI.md`, `CLAUDE.md`,
`AGENTS.md`, or `AGENT.md`.

-   **Discovery**: If any of these files exist and contain a `## Conductor
    Context` section, use that file and do NOT prompt to create a new one.
-   **Appending**: If exactly one of those files exists but lacks a `##
    Conductor Context` section, append the section to that existing file rather
    than creating a second context file.
-   **Creation & Architectural Justification**: Do NOT automatically prompt to
    create a context file based on arbitrary file counts. Only prompt if there
    is a concrete architectural justification (multiple interacting services,
    complex stateful controllers, subtle local rules, or domain gotchas).
    If multiple files exist without a context section or if creating a new file
    from scratch, prompt the user via `ask_question` to select their preferred
    filename (`GEMINI.md`, `AGENTS.md`, `AGENT.md`, `CLAUDE.md`).
-   **Simple Directories**: If the directory is simple (straightforward UI
    components, simple utilities, or basic CRUD wrappers), skip prompting
    entirely.

### Loading

See context loading item 8 in `conductor_protocol.md` §0a. The agent reads the
nearest context file (`GEMINI.md`, `CLAUDE.md`, `AGENTS.md`, or `AGENT.md`)
containing a `## Conductor Context` section in the parent directory chain of
each file the current task touches. Innermost directory wins.

### Updates

At phase checkpoints, if the agent added new exports or discovered new local
rules in a directory, propose appending them to the directory's context file
`## Conductor Context` section. Only modify content between the START and END
boundary comments.
