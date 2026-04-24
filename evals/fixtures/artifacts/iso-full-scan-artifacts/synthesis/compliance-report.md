# Compliance Report Fixture

## Assessment Metadata

- Timestamp: `[fixture timestamp]`
- Plugin Version: `fixture-1.4.0`
- Target Path: `evals/fixtures/sample-app`
- Target Commit: `[fixture commit]`
- Assessment Mode: `full-scan`
- Standards: `ISO 27001 Annex A`
- Scope Exclusions: production identity provider configuration
- Methodology: persisted fixture artifacts with source anchor validation
- Raw Artifact References: `domains/auth-assessor.json`, `reviews/round-1/evidence-completeness.json`, `synthesis/control-matrix.json`, `synthesis/evidence-index.json`

## Executive Summary

Fixture evidence pack for ISO validation.

## Control Matrix

| Control | Status | Confidence | Confidence Rationale | Evidence Quality | Evidence Quality Rationale | Manual Evidence Checklist | Reviewer Disposition | Remediation Priority | Ticket-Ready Action | GRC Action |
|---------|--------|------------|----------------------|------------------|----------------------------|---------------------------|----------------------|----------------------|---------------------|------------|
| A.8.5 Secure authentication | partially_implemented | 0.8 | Fixture source anchor supports the authentication gap, but production identity evidence is absent. | partial | Code evidence is present and manual authentication evidence remains outstanding. | Production MFA policy; login lockout configuration | approved | high | Add login throttling and attach MFA/lockout evidence. | create_remediation_ticket |

## Findings

Fixture finding at `src/routes/auth.ts:1`.

## Evidence Index

- `src/routes/auth.ts:1`

## Reviewer Notes

Approved fixture review.

## Unresolved Risks

None.

## Limitations

Fixture only. Production identity provider evidence is out of scope.

## What To Do Next

Use realistic benchmark examples for product review.

## Human Sign-Off

Reviewer: ____________________
