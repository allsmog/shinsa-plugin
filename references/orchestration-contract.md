# Shinsa Orchestration Contract

This document defines the durable artifact contract for prompt-orchestrated Shinsa runs.

## Run Layout

Every assessment run writes to:

```text
shinsa-output/
  runs/<assessment_id>/
    assessment-plan.md
    scope.md
    applicability.json
    applicability.md
    shinsa-state.json
    domains/
      <agent-name>.json
      <agent-name>.md
    reviews/
      round-<n>/
        evidence-completeness.json
        evidence-completeness.md
        control-interpretation.json
        control-interpretation.md
        coverage-review.json
        coverage-review.md
    synthesis/
      compliance-report.md
      evidence-index.json
      control-matrix.json
```

Top-level compatibility outputs must continue to mirror the latest run:

```text
shinsa-output/shinsa-state.json
shinsa-output/compliance-report.md
```

`synthesis/compliance-report.md` is the canonical enterprise evidence pack. It must be suitable for Security/GRC review without access to prior chat context.

## Assessment Plan

`assessment-plan.md` is the contract between orchestration phases. It should contain:

1. Target path and standard
2. Scope summary
3. Requested filters (`--controls`, `--family`, `--severity`, `--resume`)
4. Applicable domains and controls
5. Dispatch plan mapping domains to assessor agents
6. Reviewer angles and escalation rules

## Domain Result Contract

Each assessor returns one JSON object and one markdown summary. The JSON object should match this shape:

```json
{
  "agent": "auth-assessor",
  "standard": "iso27001",
  "domain": "authentication-access-control",
  "status": "completed",
  "controls": [
    {
      "control_id": "A.8.5",
      "control_family": "A.8",
      "title": "Secure authentication",
      "status": "partially_implemented",
      "maturity": 3,
      "confidence": 0.86,
      "agent": "auth-assessor",
      "evidence_summary": "bcrypt and secure cookies are present, but login rate limiting is missing.",
      "evidence_quality": "partial",
      "manual_evidence_needed": true,
      "manual_evidence_items": [
        "Access review records for privileged users",
        "Production authentication policy covering lockout and MFA"
      ],
      "reviewer_disposition": "not_reviewed",
      "confidence_rationale": "Code evidence confirms bcrypt and secure cookie flags, but the repository does not include production lockout, MFA, or access review evidence.",
      "evidence_quality_rationale": "Evidence is partial because implementation files support only part of the secure authentication control and manual process evidence remains outstanding.",
      "grc_action": "create_remediation_ticket",
      "findings": [
        {
          "title": "Missing rate limiting on login",
          "severity": "high",
          "description": "Authentication endpoints do not throttle repeated failed attempts.",
          "evidence": [
            {
              "file_path": "src/routes/auth.ts",
              "start_line": 67,
              "end_line": 75,
              "snippet": "router.post('/login', loginHandler)",
              "assessment": "No rate limiting middleware is applied."
            }
          ],
          "gap": "Brute-force protection is absent.",
          "recommendation": "Add per-IP and per-account throttling."
        }
      ],
      "gaps": ["Missing login throttling"],
      "recommendations": ["Add rate limiting to authentication endpoints"]
    }
  ],
  "summary": {
    "controls_assessed": 3,
    "findings_total": 2
  }
}
```

## Evidence Pack Contract

The final markdown report is an audit evidence pack, not just a findings list. It must contain these top-level sections:

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

Each assessed control row must include:

- control ID and title
- implementation status
- confidence
- confidence rationale
- evidence quality
- evidence quality rationale
- manual evidence needed (`yes` or `no`)
- manual evidence item checklist
- reviewer disposition
- primary evidence path(s)
- recommended GRC action

## Enterprise Control Fields

Every assessor domain result, synthesized `controls[]` row, and `synthesis/control-matrix.json` row must include these fields for each control:

- `evidence_quality`: `strong`, `partial`, `inferred`, or `missing`
- `manual_evidence_needed`: boolean
- `manual_evidence_items`: array of specific missing policy, approval, operational, or production records; use `[]` only when no manual evidence is needed
- `reviewer_disposition`: `not_reviewed` in assessor outputs, later replaced by `approved`, `changes_requested`, or `unresolved` during synthesis
- `confidence_rationale`: concise explanation of why the confidence score is appropriate
- `evidence_quality_rationale`: concise explanation of why the evidence quality label is appropriate
- `grc_action`: one of `accept`, `reject`, `request_evidence`, or `create_remediation_ticket`

Do not mark a control `implemented` when `manual_evidence_needed` is `true`. Use `partially_implemented`, `not_implemented`, or `not_assessed` until the missing manual/process evidence is supplied. Code evidence can support implementation of technical measures, but it cannot prove full compliance for hybrid or manual controls by itself.

### Evidence Quality

Allowed evidence quality values:

- `strong`: concrete source/config evidence directly supports the control outcome, and no manual evidence is required for the claimed status
- `partial`: evidence supports part of the control, but gaps or non-code evidence remain
- `inferred`: outcome depends on absence-of-evidence or framework convention
- `missing`: no reliable evidence was found

### Manual Evidence Markers

Hybrid controls must be explicit about manual evidence needed for full compliance. Manual evidence includes policies, approvals, access reviews, training records, supplier agreements, incident records, and production configuration that is not present in the assessed repository.

### Reviewer Disposition

Allowed reviewer dispositions:

- `approved`
- `changes_requested`
- `unresolved`
- `not_reviewed`

If any reviewer remains non-approved, the evidence pack must show the unresolved item in both `Reviewer Notes` and `Unresolved Risks`.

## Reviewer Result Contract

Each reviewer returns one JSON object and one markdown summary. The JSON object should match this shape:

```json
{
  "angle": "evidence_completeness",
  "round": 1,
  "status": "changes_requested",
  "affected_controls": ["A.8.5"],
  "requested_changes": [
    "Confirm whether session rotation is implemented on login."
  ],
  "notes": "Evidence is sufficient for hashing and cookies, but session rotation was not checked. The A.8.5 evidence_quality should remain partial and manual_evidence_items should include production lockout/MFA policy evidence.",
  "artifact_path": "shinsa-output/runs/run-123/reviews/round-1/evidence-completeness.json"
}
```

Allowed reviewer statuses:

- `approved`
- `changes_requested`
- `unresolved`

Allowed reviewer angles:

- `evidence_completeness`
- `control_interpretation`
- `coverage_false_negative_risk`

## Reconciliation Rules

- Full scans run all three reviewers after each assessment round.
- Quick checks use one condensed cold review, but still persist the result using the reviewer contract above.
- Reconciliation may re-run only the affected domain assessors.
- Maximum review rounds: 3.
- If any reviewer remains non-approved after round 3, finalize with `[REVIEWER NOTE: unresolved]` in the markdown report and include the unresolved requests in `review.rounds`.

## Maintainer Workflow Contract

Maintainer commands create durable artifacts under `.plans/<slug>/` and `.plans/<slug>.md`.

Required files:

- `.plans/<slug>.md`
- `.plans/<slug>/research.md`
- `.plans/<slug>/implementation-notes.md`
- `.plans/<slug>/benchmark.json`

Maintainer benchmark artifacts are validated with `python3 scripts/validate_evals.py .plans/<slug>/benchmark.json`.
