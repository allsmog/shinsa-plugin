---
name: compliance-scan
description: Run an orchestrated ISO 27001 Annex A compliance assessment with parallel domain assessors, cold review rounds, and durable artifacts
argument-hint: "[path] [--controls A.8.5,A.8.24] [--family A.8] [--severity critical,high] [--format json|md] [--output file] [--resume]"
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

# Compliance Scan

Run a full ISO 27001:2022 Annex A assessment as a durable orchestration pipeline.

This command is the orchestrator. Domain reasoning belongs in the assessor agents. Review belongs in fresh reviewer agents. Persist every phase to disk.

Reference the shared contract in `references/orchestration-contract.md`.

## Flags

| Flag | Effect |
|------|--------|
| `--controls` | Assess specific shipped controls only (comma-separated IDs, e.g. `A.8.5,A.8.24`) |
| `--family` | Assess shipped controls within a family (`A.5` or `A.8`) |
| `--severity` | Only report findings at or above severity |
| `--format` | Output format: `json` or `md` (default: both) |
| `--output` | Save the final markdown report to a specific file path |
| `--resume` | Resume the latest incomplete ISO orchestration run |

## Shipped ISO Coverage

The full scan produces standalone scored results for:

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

Additional ISO guidance in the reference skill may inform analysis, but do not emit standalone scores for unshipped controls.

## Phase 0: Initialize or Resume the Run

1. Determine the target path. Default to the current directory.
2. Discover candidate state files:

   ```bash
   find shinsa-output -path "*/shinsa-state.json" -type f 2>/dev/null
   ```

3. If `--resume` is set:
   - Load each candidate state JSON.
   - Keep only states where `standard = "iso27001"` and `run.phase != "completed"`.
   - Choose the candidate with the highest parseable `last_updated`; if `last_updated` is missing or invalid, fall back to file modification time.
   - Continue from that run's recorded `run.phase` and `run.round`.
   - If no incomplete ISO run exists, report that `--resume` has no target and stop without creating a new run.
4. Otherwise create a new `assessment_id` and run root:

   ```text
   shinsa-output/runs/<assessment_id>/
   ```

5. Initialize `shinsa-output/runs/<assessment_id>/shinsa-state.json` immediately and mirror it to `shinsa-output/shinsa-state.json`.

## Phase 1: Scope the Repository

Detect languages, frameworks, infrastructure, and source size:

```bash
ls package.json pyproject.toml requirements.txt go.mod Cargo.toml pom.xml composer.json Gemfile 2>/dev/null || true
ls Dockerfile docker-compose.yml .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile terraform/*.tf k8s/*.yaml 2>/dev/null || true
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
```

Write `scope.md` with:

- target path
- detected languages
- detected frameworks
- detected infrastructure
- source file count
- any obvious scoping caveats

Update state:

- `run.phase = "scope"`
- `run.round = 1`
- `scope = ...`

## Phase 2: Write the Assessment Plan

Create:

- `assessment-plan.md`
- `applicability.json`
- `applicability.md`

The assessment plan must include:

1. target and standard
2. requested filters
3. active ISO controls after filtering
4. domain-to-agent dispatch plan
5. reviewer angles
6. reconciliation rules

Use this domain mapping:

- `auth-assessor`: A.8.2, A.8.3, A.8.5
- `crypto-assessor`: A.8.21, A.8.24
- `data-protection-assessor`: A.8.10, A.8.11, A.8.12, A.5.14
- `logging-assessor`: A.8.15, A.8.16, A.8.17, A.8.34

Update state:

- `run.phase = "plan"`
- `artifacts.plan_path = "shinsa-output/runs/<assessment_id>/assessment-plan.md"`

## Phase 3: Dispatch Domain Assessors in Parallel

Run the 4 domain assessors in parallel where the filtered scope still requires them.

For each assessor:

1. Provide only the target path, `scope.md`, `assessment-plan.md`, and the relevant active controls.
2. Instruct the assessor to return:
   - one JSON object matching the domain result contract
   - one markdown summary
3. Write the results to:
   - `domains/<agent-name>.json`
   - `domains/<agent-name>.md`
4. After each domain completes, merge its controls and findings into `shinsa-state.json`, then mirror the state to `shinsa-output/shinsa-state.json`.

Do not ask the orchestrator itself to perform inline control assessment. The agents own domain reasoning.

Update state:

- `run.phase = "assessment"`
- `agents_completed = [...]`
- `artifacts.domain_results = [...]`

## Phase 4: Cold Review Round

Run three fresh reviewers against the persisted artifacts only:

- `evidence-completeness-reviewer`
- `control-interpretation-reviewer`
- `coverage-reviewer`

Rules:

1. Give reviewers the codebase plus persisted artifacts, not assessor reasoning.
2. Reviewers must inspect `assessment-plan.md`, `scope.md`, `applicability.*`, and all current domain result artifacts.
3. Persist outputs under:

   ```text
   reviews/round-<n>/evidence-completeness.json
   reviews/round-<n>/evidence-completeness.md
   reviews/round-<n>/control-interpretation.json
   reviews/round-<n>/control-interpretation.md
   reviews/round-<n>/coverage-review.json
   reviews/round-<n>/coverage-review.md
   ```

4. Merge reviewer results into `review.rounds`.

Update state:

- `run.phase = "review"`
- `review.rounds += current round`
- `artifacts.review_paths += current round files`

## Phase 5: Reconciliation Loop

If every reviewer returns `approved`, continue to synthesis.

If any reviewer returns `changes_requested`:

1. Collect requested changes by affected domain.
2. Re-run only the impacted domain assessors.
3. Write new domain artifacts in place.
4. Increment `run.round`.
5. Re-run all three reviewers on the updated artifact set.

Maximum rounds: 3.

If any reviewer is still non-approved after round 3:

- set `review.status = "unresolved"`
- carry forward the unresolved requests
- tag the final markdown report with `[REVIEWER NOTE: unresolved]`

Otherwise set `review.status = "approved"`.

During reconciliation set:

- `run.phase = "reconciliation"`

## Phase 6: Final Synthesis

Synthesize the final report from persisted artifacts only. Do not re-scan the codebase in this phase.

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

The final state must include:

- `run`
- `review`
- `artifacts`
- merged `scope`
- merged `summary`
- merged `controls`

Mirror the final run state to:

- `shinsa-output/runs/<assessment_id>/shinsa-state.json`
- `shinsa-output/shinsa-state.json`

If `--output` is set, also write the markdown report there.

## Final Output Expectations

The completed state must use schema version `1.4.0` and include review provenance, evidence quality, manual-evidence markers, confidence/evidence-quality rationales, GRC action, and reviewer disposition. The compatibility report remains human-readable, but the canonical source of truth is the artifact set under `shinsa-output/runs/<assessment_id>/`.
