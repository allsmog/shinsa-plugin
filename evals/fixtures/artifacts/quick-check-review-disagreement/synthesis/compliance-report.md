# Quick Check Report Fixture

## Assessment Metadata

- Timestamp: `[fixture timestamp]`
- Plugin Version: `fixture-1.4.0`
- Target Path: `evals/fixtures/sample-app`
- Target Commit: `[fixture commit]`
- Assessment Mode: `quick-check`
- Standards: `ISO 27001 Annex A`
- Scope Exclusions: non-authentication controls
- Methodology: persisted quick-check fixture artifacts with source anchor validation
- Raw Artifact References: `domains/auth-assessor.json`, `reviews/round-1/control-interpretation.json`, `synthesis/control-matrix.json`, `synthesis/evidence-index.json`

## Executive Summary

Fixture evidence pack for quick-check validation.

## Control Matrix

| Control | Status | Confidence | Confidence Rationale | Evidence Quality | Evidence Quality Rationale | Manual Evidence Checklist | Reviewer Disposition | Remediation Priority | Ticket-Ready Action | GRC Action |
|---------|--------|------------|----------------------|------------------|----------------------------|---------------------------|----------------------|----------------------|---------------------|------------|
| A.8.5 Secure authentication | implemented | 0.9 | Fixture password helper is treated as a narrow code-level quick check with direct source evidence. | strong | Direct source evidence supports the scoped password-hashing claim and no manual evidence is required. | none | approved | none | No action for fixture. | accept |

## Findings

Fixture finding at `src/auth/password.ts:1`.

## Evidence Index

- `src/auth/password.ts:1`

## Reviewer Notes

Approved fixture review.

## Unresolved Risks

None.

## Limitations

Fixture only. The quick check does not assess full identity governance.

## What To Do Next

Use realistic benchmark examples for product review.

## Human Sign-Off

Reviewer: ____________________
