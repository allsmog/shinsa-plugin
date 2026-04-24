---
name: nist-scan
description: Run an orchestrated NIST SP 800-53 Rev 5 compliance assessment with parallel domain assessors, cold review rounds, and durable artifacts
argument-hint: "[path] [--controls AC-3,IA-5] [--family AC,AU] [--severity critical,high] [--format json|md] [--output file] [--resume]"
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

# NIST Scan

Run a full NIST SP 800-53 Rev 5 assessment as a durable orchestration pipeline.

This command is the orchestrator. Domain reasoning belongs in the NIST assessor agents. Review belongs in fresh reviewer agents. Persist every phase to disk.

Reference the shared contract in `references/orchestration-contract.md`.

## Flags

| Flag | Effect |
|------|--------|
| `--controls` | Assess specific controls only |
| `--family` | Assess specific families only |
| `--severity` | Only report findings at or above severity |
| `--format` | Output format: `json` or `md` |
| `--output` | Save the final markdown report to a specific file path |
| `--resume` | Resume the latest incomplete NIST orchestration run |

## Shipped NIST Coverage

The full scan covers 53 shipped controls across these domains:

- `nist-access-control-assessor`: AC + IA
- `nist-audit-assessor`: AU
- `nist-sc-assessor`: SC
- `nist-si-assessor`: SI + MP
- `nist-cm-assessor`: CM + RA
- `nist-sa-assessor`: SA

Use reference skill material for interpretation, but emit standalone scores only for shipped controls.

## Phase 0: Initialize or Resume the Run

1. Determine the target path. Default to the current directory.
2. Discover candidate state files:

   ```bash
   find shinsa-output -path "*/shinsa-state.json" -type f 2>/dev/null
   ```

3. If `--resume` is set:
   - Load each candidate state JSON.
   - Keep only states where `standard = "nist-800-53"` and `run.phase != "completed"`.
   - Choose the candidate with the highest parseable `last_updated`; if `last_updated` is missing or invalid, fall back to file modification time.
   - Continue from that run's recorded `run.phase` and `run.round`.
   - If no incomplete NIST run exists, report that `--resume` has no target and stop without creating a new run.
4. Otherwise create a new `assessment_id` and initialize:

   ```text
   shinsa-output/runs/<assessment_id>/
   ```

5. Write the initial run state and mirror it to `shinsa-output/shinsa-state.json`.

## Phase 1: Scope the Repository

Collect language, framework, infrastructure, and size information:

```bash
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml pom.xml composer.json Gemfile 2>/dev/null || true
ls Dockerfile docker-compose.yml .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile terraform/*.tf k8s/*.yaml 2>/dev/null || true
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
```

Write `scope.md`, then update state with:

- `run.phase = "scope"`
- `run.round = 1`

## Phase 2: Write the Assessment Plan

Create:

- `assessment-plan.md`
- `applicability.json`
- `applicability.md`

The applicability phase must decide which shipped controls are in scope based on repo evidence:

- Always-code-assessable families: AC, IA, AU, SC, SI, MP
- Conditional families: CM, RA, SA when IaC, CI/CD, or testing infrastructure is detected

The assessment plan must include:

1. target and standard
2. requested filters
3. active controls after filtering and applicability pruning
4. domain-to-agent dispatch plan
5. reviewer angles
6. reconciliation rules

Update state:

- `run.phase = "plan"`
- `artifacts.plan_path = "shinsa-output/runs/<assessment_id>/assessment-plan.md"`

## Phase 3: Dispatch Domain Assessors in Parallel

Run the needed NIST assessors in parallel:

- `nist-access-control-assessor`
- `nist-audit-assessor`
- `nist-sc-assessor`
- `nist-si-assessor`
- `nist-cm-assessor`
- `nist-sa-assessor`

For each active domain:

1. Provide only the codebase, `scope.md`, `assessment-plan.md`, and the relevant active controls.
2. Require one JSON domain result and one markdown summary.
3. Persist to:
   - `domains/<agent-name>.json`
   - `domains/<agent-name>.md`
4. Merge each completed domain into the run state immediately.

Do not assess controls inline in the command itself.

Update state:

- `run.phase = "assessment"`
- `agents_completed = [...]`
- `artifacts.domain_results = [...]`

## Phase 4: Cold Review Round

Run these fresh reviewers against the persisted artifacts only:

- `evidence-completeness-reviewer`
- `control-interpretation-reviewer`
- `coverage-reviewer`

Persist outputs under:

```text
reviews/round-<n>/evidence-completeness.*
reviews/round-<n>/control-interpretation.*
reviews/round-<n>/coverage-review.*
```

Merge them into `review.rounds`, then update:

- `run.phase = "review"`
- `artifacts.review_paths += current round files`

## Phase 5: Reconciliation Loop

If any reviewer returns `changes_requested`:

1. group requested changes by affected domain
2. re-run only the impacted NIST assessors
3. overwrite the impacted domain artifacts
4. increment `run.round`
5. re-run all three reviewers

Maximum rounds: 3.

If unresolved after round 3:

- set `review.status = "unresolved"`
- preserve unresolved reviewer requests in state
- annotate final markdown with `[REVIEWER NOTE: unresolved]`

Otherwise set `review.status = "approved"`.

During reconciliation set:

- `run.phase = "reconciliation"`

## Phase 6: Final Synthesis

Assemble the final state and report from persisted artifacts only.

Write:

- `shinsa-output/runs/<assessment_id>/synthesis/compliance-report.md`
- `shinsa-output/runs/<assessment_id>/synthesis/evidence-index.json`
- `shinsa-output/runs/<assessment_id>/synthesis/control-matrix.json`
- `shinsa-output/runs/<assessment_id>/compliance-report.md`
- `shinsa-output/compliance-report.md`

The canonical `synthesis/compliance-report.md` is an enterprise evidence pack and must include:

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

Mirror final state to:

- `shinsa-output/runs/<assessment_id>/shinsa-state.json`
- `shinsa-output/shinsa-state.json`

If `--output` is set, also write the markdown report there.

The final state must use schema version `1.4.0` and include `run`, `review`, `artifacts`, evidence quality, manual-evidence markers, confidence/evidence-quality rationales, GRC action, and reviewer disposition.
