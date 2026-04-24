# Shinsa (審査) — Prompt-Orchestrated Compliance Assessment for Claude Code

AI-first compliance assessment that scans codebases against ISO 27001:2022 Annex A and NIST SP 800-53 Rev 5 with evidence-backed findings tied to specific files and line numbers.

Shinsa is still markdown prompts, reference skills, and small validation scripts. The product focus is now enterprise evidence packs: assessors write artifacts, cold reviewers challenge them, and final reports are structured for Security/GRC review.

## What You Get

- 13 shipped ISO 27001 and 53 shipped NIST SP 800-53 controls
- 10 domain assessor agents plus 3 cold reviewer agents
- Durable run artifacts under `shinsa-output/runs/<assessment_id>/`
- Enterprise evidence packs with executive summary, control matrix, evidence index, reviewer notes, limitations, and human sign-off
- Review provenance in `shinsa-state.json` schema `1.4.0`
- Maintainer planning and implementation commands for extending Shinsa itself
- Eval harness scripts for trigger checks, evidence anchoring, evidence-pack section checks, inventory drift, and reviewer pass rate

## Installation

```bash
claude mcp add-plugin shinsa-plugin --path /path/to/shinsa-plugin
```

Or clone and add manually:

```bash
git clone https://github.com/allsmog/shinsa-plugin.git
```

Then add it to Claude Code settings:

```json
{
  "plugins": ["/path/to/shinsa-plugin"]
}
```

## Quick Start

```text
/shinsa:compliance-scan
/shinsa:nist-scan
/shinsa:quick-check A.8.5
/shinsa:nist-quick-check AC-3
```

Maintainer-only workflows:

```text
/shinsa:control-plan add-a8-28-coverage
/shinsa:control-implement add-a8-28-coverage
```

## Golden Evidence Pack Demo

Use the sample apps to see the intended product experience before scanning your own repository:

```text
/shinsa:compliance-scan examples/api-service --controls A.8.5,A.8.15
/shinsa:nist-scan examples/platform-app --family CM,RA,SI
```

Expected evidence packs are checked in under:

- `examples/api-service/expected-shinsa-output/runs/golden-iso-evidence-pack/synthesis/compliance-report.md`
- `examples/platform-app/expected-shinsa-output/runs/golden-nist-evidence-pack/synthesis/compliance-report.md`

Each evidence pack includes:

- executive summary for GRC readers
- control matrix with status, confidence rationale, evidence quality rationale, manual-evidence checklist, reviewer disposition, and GRC action
- findings tied to file and line evidence
- evidence index
- reviewer notes and unresolved risks
- limitations and human sign-off

## Commands

| Command | Description |
|---------|-------------|
| `/shinsa:compliance-scan` | Full ISO 27001 orchestration with parallel assessors, 3 cold reviewers, reconciliation, and final synthesis |
| `/shinsa:quick-check <control>` | Focused ISO check with one domain assessor and one condensed cold review |
| `/shinsa:nist-scan` | Full NIST orchestration with parallel assessors, 3 cold reviewers, reconciliation, and final synthesis |
| `/shinsa:nist-quick-check <control>` | Focused NIST check with one domain assessor and one condensed cold review |
| `/shinsa:control-plan <slug>` | Maintainer-only plan workflow for new coverage, prompt changes, or evaluator changes |
| `/shinsa:control-implement <slug>` | Maintainer-only implementation workflow that reads a plan, applies changes, and validates eval artifacts |

## Orchestration Model

Full scans now run as a 6-phase pipeline:

1. Scope the target repository
2. Write `assessment-plan.md` and applicability artifacts
3. Dispatch domain assessors in parallel
4. Run 3 cold reviewers:
   - `evidence-completeness-reviewer`
   - `control-interpretation-reviewer`
   - `coverage-reviewer`
5. Reconcile reviewer-requested changes for up to 3 rounds
6. Synthesize the final state and report from persisted artifacts only

Quick checks use the same artifact contract, but with one assessor and one condensed cold review.

## Agents

### ISO 27001 Assessors

| Agent | Domain | Controls |
|-------|--------|----------|
| `auth-assessor` | Authentication and access control | A.8.2, A.8.3, A.8.5 |
| `crypto-assessor` | Cryptography and network services | A.8.21, A.8.24 |
| `data-protection-assessor` | Data protection and information transfer | A.8.10, A.8.11, A.8.12, A.5.14 |
| `logging-assessor` | Logging, monitoring, and audit testing | A.8.15, A.8.16, A.8.17, A.8.34 |

### NIST SP 800-53 Assessors

| Agent | Domain | Coverage |
|-------|--------|----------|
| `nist-access-control-assessor` | Access control and identification/authentication | AC, IA |
| `nist-audit-assessor` | Audit and accountability | AU |
| `nist-sc-assessor` | System and communications protection | SC |
| `nist-si-assessor` | System integrity and media protection | SI, MP |
| `nist-cm-assessor` | Configuration management and risk assessment | CM, RA |
| `nist-sa-assessor` | System acquisition and development | SA |

### Cold Reviewers

| Agent | Angle | Purpose |
|-------|-------|---------|
| `evidence-completeness-reviewer` | Evidence sufficiency | Ensures every finding and status is backed by concrete file-and-line evidence |
| `control-interpretation-reviewer` | Standards correctness | Checks that statuses and findings match ISO/NIST control intent |
| `coverage-reviewer` | False-negative risk | Looks for missed files, missed controls, and scoped coverage gaps |

## Artifact Layout

Every assessment run writes to:

```text
shinsa-output/
  runs/<assessment_id>/
    assessment-plan.md
    scope.md
    applicability.json
    applicability.md
    domains/
      <agent-name>.json
      <agent-name>.md
    reviews/
      round-<n>/
        evidence-completeness.json
        control-interpretation.json
        coverage-review.json
    synthesis/
      compliance-report.md
      control-matrix.json
      evidence-index.json
    shinsa-state.json
```

Compatibility outputs still mirror the latest run:

- `shinsa-output/shinsa-state.json`
- `shinsa-output/compliance-report.md`

## State Contract

`references/assessment.schema.json` now requires schema version `1.4.0` with:

- `run { id, standard, mode, phase, round, resumed_from? }`
- `review { status, rounds[] }`
- `artifacts { run_root, scope_path, plan_path, domain_results[], review_paths[], report_path }`
- each control outcome to include `evidence_quality`, `manual_evidence_needed`, `manual_evidence_items`, `confidence_rationale`, `evidence_quality_rationale`, `grc_action`, and `reviewer_disposition`

This makes runs resumable and auditable without depending on ephemeral chat history.

## Maintainer Workflow

Maintainer workflows persist durable artifacts under `.plans/`:

- `.plans/<slug>.md`
- `.plans/<slug>/research.md`
- `.plans/<slug>/implementation-notes.md`
- `.plans/<slug>/benchmark.json`

Use:

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_evals.py evals/benchmark.sample.json
```

The eval harness checks:

- trigger coverage
- schema contract drift
- evidence anchoring
- evidence-pack required sections
- doc/command/agent inventory consistency
- reviewer pass rate

## Reference Material

| Path | Purpose |
|------|---------|
| `skills/iso-27001-annex-a/` | ISO 27001 control reference |
| `skills/nist-800-53/` | NIST control reference |
| `skills/evidence-generation/` | Auditor-ready evidence narrative guidance |
| `skills/control-mapping/` | Cross-standard mapping guidance |
| `references/orchestration-contract.md` | Shared artifact and reviewer contract |
| `docs/supported-controls.md` | Automated, hybrid, and manual control coverage |
| `docs/limitations-and-false-positives.md` | Trust boundaries and review handling |
| `docs/troubleshooting.md` | Install, scan, resume, and reviewer troubleshooting |
| `docs/release-checklist.md` | Release readiness checklist |

## Limitations

- Shinsa still assesses code-level compliance only; organizational, people, and physical controls remain manual or hybrid.
- Reviewer loops improve rigor, not certainty. Findings remain advisory until validated in the target environment.
- Full scans are intentionally slower now because rigor and replayability were prioritized over minimal latency.

## License

MIT
