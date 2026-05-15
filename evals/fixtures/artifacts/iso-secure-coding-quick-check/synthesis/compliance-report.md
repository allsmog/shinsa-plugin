# Secure Coding Quick Check Fixture

## Assessment Metadata

- Timestamp: `[fixture timestamp]`
- Plugin Version: `fixture-1.4.0`
- Target Path: `evals/fixtures/sample-app`
- Target Commit: `[fixture commit]`
- Assessment Mode: `quick-check`
- Standards: `ISO 27001 Annex A`
- Scope Exclusions: secure coding policy, code review records, and SAST exports
- Methodology: persisted A.8.28 quick-check fixture artifacts with source anchor validation
- Raw Artifact References: `domains/data-protection-assessor.json`, `reviews/round-1/control-interpretation.json`, `synthesis/control-matrix.json`, `synthesis/evidence-index.json`

## Executive Summary

Fixture evidence pack for ISO 27001 A.8.28 secure coding quick-check validation.

## Control Matrix

| Control | Status | Confidence | Confidence Rationale | Evidence Quality | Evidence Quality Rationale | Manual Evidence Checklist | Reviewer Disposition | Remediation Priority | Ticket-Ready Action | GRC Action |
|---------|--------|------------|----------------------|------------------|----------------------------|---------------------------|----------------------|----------------------|---------------------|------------|
| A.8.28 Secure coding | partially_implemented | 0.86 | The fixture source directly shows unsafe query construction, but organizational secure coding standards and review evidence are outside the repository. | partial | Code evidence directly supports the injection finding and manual secure SDLC evidence remains outstanding. | Secure coding standard; secure code review evidence; SAST or dependency vulnerability scan results | approved | critical | Replace SQL string concatenation with parameterized queries and attach secure coding review evidence. | create_remediation_ticket |

## Findings

1. [CRITICAL] Search route builds SQL with request input (`src/routes/search.ts:1`)
   - Gap: Secure coding controls do not prevent injection in the search route.
   - Recommendation: Replace string concatenation with a parameterized query and validate the email input before querying.

## Evidence Index

- `src/routes/search.ts:1` - request input is concatenated into a SQL string.

## Reviewer Notes

Approved fixture review. A.8.28 is the correct ISO control for the injection-oriented secure coding finding.

## Unresolved Risks

None.

## Limitations

Fixture only. Full compliance still needs secure coding standards, review records, and vulnerability scan evidence.

## What To Do Next

Use the fixture to validate A.8.28 quick-check artifact generation and evidence anchoring.

## Human Sign-Off

Reviewer: ____________________
