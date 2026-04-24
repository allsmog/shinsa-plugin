---
name: quick-check
description: Orchestrated ISO quick check of a specific control or family with durable artifacts and a cold review pass
argument-hint: "<control-id|family> [path] [--verbose]"
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
  - Agent
  - TodoWrite
  - AskUserQuestion
---

# Quick Check

Run a focused ISO quick check using one domain assessor plus one condensed cold review.

Reference the shared contract in `references/orchestration-contract.md`.

## Scope Rules

Supported ISO quick-check controls:

- A.8.2
- A.8.3
- A.8.5
- A.8.10
- A.8.11
- A.8.12
- A.8.15
- A.8.16
- A.8.17
- A.8.21
- A.8.24
- A.8.34
- A.5.14

If the user requests another ISO control, explain that the reference skill contains broader guidance but the shipped quick-check command scores only the controls above.

## Workflow

### Phase 1: Resolve the Target

1. Parse the requested control or family.
2. Map it to the responsible domain assessor:
   - `auth-assessor`
   - `crypto-assessor`
   - `data-protection-assessor`
   - `logging-assessor`
3. Create a run directory under `shinsa-output/runs/<assessment_id>/`.

### Phase 2: Scope and Plan

Write:

- `scope.md`
- `assessment-plan.md`
- `applicability.json`
- `applicability.md`

The plan must record:

- requested control(s)
- target path
- responsible assessor
- cold review rule for disagreement handling

Initialize `shinsa-state.json` with:

- `run.mode = "quick-check"`
- `run.phase = "plan"`
- `run.round = 1`

### Phase 3: Assess

Dispatch the responsible ISO domain assessor with the scoped controls only.

Persist the result to:

- `domains/<agent-name>.json`
- `domains/<agent-name>.md`

Merge the returned controls and findings into the run state.

### Phase 4: Condensed Cold Review

Run one fresh reviewer cold. Use `control-interpretation-reviewer` unless the orchestrator has a stronger reason to choose another reviewer.

The quick-check reviewer must examine:

- evidence sufficiency
- control interpretation
- obvious false-negative risk within the narrow scope

Persist the result under `reviews/round-1/`.

### Phase 5: Reconcile or Finalize

If the reviewer returns `changes_requested`:

1. re-run the same assessor with the requested changes
2. overwrite the domain artifact
3. re-run the reviewer once more

If disagreement remains after the second pass:

- finalize with `review.status = "unresolved"`
- tag the markdown output with `[REVIEWER NOTE: unresolved]`

Otherwise set `review.status = "approved"`.

### Phase 6: Write Canonical and Compatibility Outputs

Write the canonical quick-check report to:

- `shinsa-output/runs/<assessment_id>/synthesis/compliance-report.md`
- `shinsa-output/runs/<assessment_id>/synthesis/evidence-index.json`
- `shinsa-output/runs/<assessment_id>/synthesis/control-matrix.json`

The canonical report is an enterprise evidence pack and must include:

1. `Assessment Metadata`
2. `Executive Summary`
3. `Control Matrix`
4. `Findings`
5. `Evidence Index`
6. `Reviewer Notes`
7. `Unresolved Risks`
8. `Limitations`
9. `What To Do Next`
10. `Human Sign-Off`

Assessment metadata must include timestamp, plugin version, target path, target commit placeholder or commit hash, assessment mode, standards, scope exclusions, methodology, and raw artifact references.

Every assessed control must show status, confidence, `confidence_rationale`, evidence quality (`strong`, `partial`, `inferred`, or `missing`), `evidence_quality_rationale`, whether manual evidence is needed, `manual_evidence_items`, reviewer disposition, evidence paths, remediation priority, and `grc_action`.

Then mirror the latest run outputs to:

- `shinsa-output/runs/<assessment_id>/shinsa-state.json`
- `shinsa-output/runs/<assessment_id>/compliance-report.md`
- `shinsa-output/shinsa-state.json`
- `shinsa-output/compliance-report.md`

If `--verbose` is set, keep passing checks in the markdown report. Otherwise lead with findings and summary.
