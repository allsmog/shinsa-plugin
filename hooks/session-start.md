---
name: session-init
description: Initialize a Shinsa session by detecting the latest orchestrated run state
event: SessionStart
---

# Compliance Assessment Session Initialization

On session start, detect the latest orchestrated run and summarize its phase, round, and review status.

## State Detection

Check for existing assessment state:

```bash
ls shinsa-output/shinsa-state.json shinsa-output/runs/*/shinsa-state.json 2>/dev/null || true
```

## If a State File Exists

Read the latest `shinsa-output/shinsa-state.json` and summarize:

- target
- standard
- `run.id`
- `run.mode`
- `run.phase`
- `run.round`
- `review.status`
- controls assessed
- findings totals
- last updated timestamp

Also mention that canonical artifacts live under:

```text
shinsa-output/runs/<assessment_id>/
```

Quick actions:

- `/shinsa:compliance-scan --resume`
- `/shinsa:nist-scan --resume`
- `/shinsa:quick-check <control>`
- `/shinsa:nist-quick-check <control>`

If the state is unresolved, explicitly call out that the latest report contains reviewer notes.

## If No State File Exists

Count source files:

```bash
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
```

Display a short welcome that includes:

- the four assessment commands
- the two maintainer commands
- the fact that full scans persist artifacts to `shinsa-output/runs/<assessment_id>/`
