# Manual Testing Guide: {Domain / Feature Name}

## 1. Environment & Prerequisites

## 2. Fixture Provisioning & Reset Tooling

## 3. Persona & Scenario Runbooks

### Persona: {Persona Name (e.g., Unauthenticated Guest, Admin, Invited Member)}

#### Preconditions & State Setup

```bash
{Exact command to establish or reset state for this persona}
```

#### Test {Domain}.{ID}: {Scenario Title}

-   **Action**: {Exact URL to visit, CLI command to run, or UI action to take}
-   **Expected Outcome**:
    {Expected route, visual state, HTTP response, or database mutation}
-   **Barrier Checks**:
    {Negative verification proving unauthorized forward hops or invalid actions are blocked}

## 4. Resilience, Error Handling & Telemetry
