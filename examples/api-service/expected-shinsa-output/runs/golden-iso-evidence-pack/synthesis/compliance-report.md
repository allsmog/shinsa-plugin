# Golden API Service ISO Evidence Pack

## Assessment Metadata

- Timestamp: `[golden timestamp]`
- Plugin Version: `shinsa-plugin 1.4.0`
- Target Path: `examples/api-service`
- Target Commit: `[golden target commit]`
- Assessment Mode: `full-scan`
- Standards: `ISO 27001:2022 Annex A`
- Scope Exclusions: production identity provider configuration, access review evidence, SIEM retention exports
- Methodology: Shinsa domain assessors reviewed persisted source/config artifacts, cold reviewers checked evidence completeness, control interpretation, and coverage, then synthesis merged reviewer dispositions.
- Raw Artifact References: `assessment-plan.md`, `scope.md`, `applicability.md`, `domains/auth-assessor.json`, `domains/logging-assessor.json`, `reviews/round-1/evidence-completeness.json`, `reviews/round-1/control-interpretation.json`, `reviews/round-1/coverage-review.json`, `synthesis/control-matrix.json`, `synthesis/evidence-index.json`

## Executive Summary

Shinsa assessed the golden API service for ISO 27001 Annex A controls A.8.5 and A.8.15. The repository contains concrete positive evidence for password handling and structured logging, but the evidence pack records two implementation gaps: missing login throttling and missing privileged-action audit logging. Both controls remain partially implemented because production identity governance and log-retention evidence are manual artifacts outside the sample repository.

## Control Matrix

| Control | Status | Confidence | Confidence Rationale | Evidence Quality | Evidence Quality Rationale | Manual Evidence Checklist | Reviewer Disposition | Remediation Priority | Ticket-Ready Action | GRC Action |
|---------|--------|------------|----------------------|------------------|----------------------------|---------------------------|----------------------|----------------------|---------------------|------------|
| A.8.5 Secure authentication | partially_implemented | 0.86 | Source evidence directly supports password hashing and the missing rate-limit gap, but production identity governance evidence was not present. | partial | Concrete code anchors cover only technical authentication behavior and manual access governance records remain outstanding. | Production MFA policy; login lockout configuration export; privileged access review records | approved | high | Add per-IP and per-account login throttling, then attach MFA and lockout evidence. | create_remediation_ticket |
| A.8.15 Logging | partially_implemented | 0.78 | Application logging code and the missing privileged-action audit call were reviewed, but production retention and monitoring records were not available. | partial | Source anchors support selected logging behavior, while operational log governance requires manual artifacts. | Production log retention policy; SIEM ingestion evidence; privileged action review procedure | approved | medium | Add structured audit logging for privileged user deletion and attach retention/SIEM evidence. | create_remediation_ticket |

## Findings

1. High: login endpoint lacks rate limiting at `src/routes/auth.ts:7`.
   - Control: A.8.5 Secure authentication
   - Evidence basis: the login route calls the handler directly and no throttling middleware is present in the assessed route.
   - Recommendation: add per-IP and per-account throttling with lockout monitoring.
2. Medium: privileged user deletion is not audit-logged at `src/routes/admin.ts:5`.
   - Control: A.8.15 Logging
   - Evidence basis: the admin route performs the sensitive action without an audit logger call.
   - Recommendation: emit structured audit events for privileged CRUD operations.

## Evidence Index

- `src/auth/password.ts:4`: bcrypt password verification supports secure authentication.
- `src/routes/auth.ts:7`: login route has no throttling middleware.
- `src/logger.ts:1`: structured logger is available for application events.
- `src/routes/admin.ts:5`: admin delete action runs without audit log call.

## Reviewer Notes

All three round-1 reviewers approved the sample evidence pack. Evidence is adequate for the sample assessment, but reviewers noted that production log retention, MFA policy, lockout settings, and access review records remain manual evidence before audit submission.

## Unresolved Risks

None in this sample evidence pack.

## Limitations

This is repository-level evidence. It does not prove identity governance, production monitoring, access review completion, SIEM retention, or production authentication policy operation.

## What To Do Next

- Create a remediation ticket for A.8.5 login throttling and attach MFA/lockout evidence.
- Create a remediation ticket for A.8.15 privileged-action audit logging and attach SIEM retention evidence.
- After remediation, rerun the scan and ask a reviewer to confirm the updated anchors.

## Human Sign-Off

Reviewer: ____________________
Date: ____________________
Disposition: accept / reject / request more evidence
Sign-off note: Shinsa supports assessment preparation; final audit acceptance requires human review of repository and manual evidence.
