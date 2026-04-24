# Shinsa - Compliance Assessment Plugin

Prompt-orchestrated compliance assessment for Claude Code. Shinsa scans codebases against ISO 27001 Annex A and NIST SP 800-53 Rev 5 with evidence-backed findings, cold review rounds, and durable run artifacts.

## Project Structure

```text
shinsa-plugin/
├── .claude-plugin/plugin.json
├── CLAUDE.md
├── commands/
│   ├── compliance-scan.md
│   ├── quick-check.md
│   ├── nist-scan.md
│   ├── nist-quick-check.md
│   ├── control-plan.md
│   └── control-implement.md
├── agents/
│   ├── auth-assessor.md
│   ├── crypto-assessor.md
│   ├── data-protection-assessor.md
│   ├── logging-assessor.md
│   ├── nist-access-control-assessor.md
│   ├── nist-audit-assessor.md
│   ├── nist-sc-assessor.md
│   ├── nist-si-assessor.md
│   ├── nist-cm-assessor.md
│   ├── nist-sa-assessor.md
│   ├── evidence-completeness-reviewer.md
│   ├── control-interpretation-reviewer.md
│   └── coverage-reviewer.md
├── skills/
├── hooks/
│   └── session-start.md
├── references/
│   ├── assessment.schema.json
│   └── orchestration-contract.md
├── evals/
│   ├── evals.json
│   ├── trigger_evals.json
│   └── benchmark.sample.json
└── scripts/
    ├── quick_validate.py
    └── validate_evals.py
```

## Key Commands

- `/shinsa:compliance-scan` — full ISO orchestration
- `/shinsa:quick-check` — focused ISO check with cold review
- `/shinsa:nist-scan` — full NIST orchestration
- `/shinsa:nist-quick-check` — focused NIST check with cold review
- `/shinsa:control-plan` — maintainer plan workflow
- `/shinsa:control-implement` — maintainer implementation workflow

## Assessment Methodology

1. Scope the repository
2. Write `assessment-plan.md` and applicability artifacts
3. Dispatch domain assessors
4. Run cold review rounds
5. Reconcile requested changes
6. Synthesize final state and report from persisted artifacts

## Agents

### Assessors

- `auth-assessor`
- `crypto-assessor`
- `data-protection-assessor`
- `logging-assessor`
- `nist-access-control-assessor`
- `nist-audit-assessor`
- `nist-sc-assessor`
- `nist-si-assessor`
- `nist-cm-assessor`
- `nist-sa-assessor`

### Cold Reviewers

- `evidence-completeness-reviewer`
- `control-interpretation-reviewer`
- `coverage-reviewer`

## Assessment Output

- `shinsa-output/runs/<assessment_id>/...` — canonical artifact set for a run
- `shinsa-output/shinsa-state.json` — latest compatibility state
- `shinsa-output/compliance-report.md` — latest compatibility report

The state schema is version `1.4.0` and includes `run`, `review`, `artifacts`, evidence quality, manual-evidence markers, confidence/evidence-quality rationales, GRC action, and reviewer disposition.

## Maintainer Validation

Run:

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_evals.py evals/benchmark.sample.json
```

These validate command/agent/doc inventory, schema contract fields, trigger coverage, evidence anchoring, and reviewer pass rate.
