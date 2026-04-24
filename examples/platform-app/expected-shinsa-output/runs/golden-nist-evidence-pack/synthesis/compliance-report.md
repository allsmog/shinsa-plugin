# Golden Platform App NIST Evidence Pack

## Assessment Metadata

- Timestamp: `[golden timestamp]`
- Plugin Version: `shinsa-plugin 1.4.0`
- Target Path: `examples/platform-app`
- Target Commit: `[golden target commit]`
- Assessment Mode: `full-scan`
- Standards: `NIST SP 800-53 Rev 5`
- Scope Exclusions: production Kubernetes runtime policy, asset inventory, vulnerability scanner export, risk acceptance records
- Methodology: Shinsa NIST assessors reviewed persisted repository artifacts, cold reviewers challenged evidence completeness and coverage, and synthesis propagated unresolved reviewer notes to the report.
- Raw Artifact References: `assessment-plan.md`, `scope.md`, `applicability.md`, `domains/nist-cm-assessor.json`, `domains/nist-si-assessor.json`, `reviews/round-2/evidence-completeness.json`, `reviews/round-2/control-interpretation.json`, `reviews/round-2/coverage-review.json`, `synthesis/control-matrix.json`, `synthesis/evidence-index.json`

## Executive Summary

Shinsa assessed the golden platform app for NIST CM, RA, and SI evidence. CI includes vulnerability scanning and the application includes input validation, but CM-6 remains unresolved because repository evidence does not prove the production container runs as a non-root user. The evidence pack separates repository-backed findings from manual production evidence needed for audit use.

## Control Matrix

| Control | Status | Confidence | Confidence Rationale | Evidence Quality | Evidence Quality Rationale | Manual Evidence Checklist | Reviewer Disposition | Remediation Priority | Ticket-Ready Action | GRC Action |
|---------|--------|------------|----------------------|------------------|----------------------------|---------------------------|----------------------|----------------------|---------------------|------------|
| CM-6 Configuration Settings | partially_implemented | 0.74 | Repository evidence supports the Docker hardening finding, but production runtime configuration was not available. | partial | Source evidence shows a configuration gap and manual runtime evidence is required to close the reviewer concern. | Production container runtime configuration; approved baseline configuration; container hardening exception or remediation ticket | unresolved | medium | Add an explicit non-root USER directive or attach production runtime evidence proving non-root execution. | request_evidence |
| RA-5 Vulnerability Monitoring and Scanning | partially_implemented | 0.72 | CI configuration shows automated dependency scanning, but scan results and remediation tracking are outside the repository. | partial | The workflow proves a scan command exists but not that vulnerabilities are reviewed and remediated. | Latest dependency vulnerability scan export; vulnerability remediation ticket queue; risk acceptance records for unresolved findings | approved | medium | Attach the latest scan results and remediation tracking evidence. | request_evidence |
| SI-10 Information Input Validation | implemented | 0.82 | The assessed code path contains direct validation logic and no manual evidence is needed for this code-level outcome. | strong | The source anchor directly supports the validation claim for the scoped route. | none | approved | none | Keep validation tests current as routes change. | accept |

## Findings

1. Medium: Dockerfile does not declare a non-root runtime user at `Dockerfile:1`.
   - Control: CM-6 Configuration Settings
   - Evidence basis: the Dockerfile starts from the Node image and does not include a `USER` directive.
   - Recommendation: add a non-root user to the image or provide production runtime evidence showing equivalent enforcement.

## Evidence Index

- `Dockerfile:1`: Node image is declared, but no `USER` directive appears in the container file.
- `.github/workflows/ci.yml:15`: CI runs `npm audit --audit-level=high`.
- `src/server.js:5`: input validation rejects non-string and overlong values.

## Reviewer Notes

Round 1 requested clarification for the container runtime user. Round 2 evidence-completeness review left CM-6 unresolved pending human review of production runtime configuration. The affected control row above carries `reviewer_disposition: unresolved`.

## Unresolved Risks

CM-6 unresolved reviewer note: Round 2 evidence-completeness review could not confirm production non-root runtime. This risk blocks accepting CM-6 as implemented until a non-root `USER` directive, runtime policy, or approved exception is supplied.

## Limitations

This evidence pack does not include production Kubernetes policy, vulnerability scanner output, exception approvals, asset inventory records, or production runtime inspection results.

## What To Do Next

- Request production runtime evidence for CM-6 or create a remediation ticket to add a non-root `USER` directive.
- Attach the latest vulnerability scan export and remediation queue for RA-5.
- Accept SI-10 for the scoped code-level validation evidence, then re-test when routes change.

## Human Sign-Off

Reviewer: ____________________
Date: ____________________
Disposition: accept / reject / request more evidence
Sign-off note: Shinsa supports assessment preparation; final audit acceptance requires human review of repository and manual evidence.
