---
name: Evidence Generation
description: >-
  This skill should be used when generating audit evidence, producing compliance
  documentation, creating evidence narratives, writing assessment reports, or when
  the user asks about "audit evidence", "compliance evidence", "evidence package",
  "audit documentation", or "ISO 27001 evidence".
version: 1.0.0
---

# Audit Evidence Generation

## Purpose

Transform raw code assessment findings into formal, auditor-ready evidence narratives. This skill guides the production of evidence that meets ISO 27001 audit requirements.

## When to Use

- After completing a compliance scan
- When producing evidence packages for auditors
- When documenting control implementation for certification
- When generating compliance reports

## Evidence Requirements

ISO 27001 auditors expect evidence that demonstrates:

1. **What** was assessed (control requirement)
2. **How** it was assessed (methodology)
3. **What** was found (evidence of implementation or gaps)
4. **Where** the evidence is (specific file paths, line numbers)
5. **When** the assessment was performed (timestamp)

## Evidence Structure

### Per-Control Evidence

```markdown
## Control: A.8.5 — Secure Authentication

### Implementation Status: Partially Implemented
### Maturity Level: 3/5 (Defined)

### Evidence of Implementation

The application implements authentication using [framework/library] with the
following security measures observed:

**Password Storage** (A.8.5.a):
- Passwords are hashed using Argon2id with cost parameters [memory=65536, time=3, parallelism=4]
- Evidence: `src/auth/password.ts` lines 15-28
- Assessment: Meets OWASP recommendations for password storage

**Session Management** (A.8.5.b):
- Session tokens generated using cryptographically secure random bytes (32 bytes)
- Tokens stored with HttpOnly, Secure, and SameSite=Strict flags
- Evidence: `src/auth/session.ts` lines 10-35
- Assessment: Meets secure session management requirements

### Identified Gaps

1. **Rate Limiting**: No rate limiting observed on the login endpoint
   (`src/routes/auth.ts:45`). This creates risk of brute-force attacks.

2. **MFA**: No multi-factor authentication implementation found.

### Recommendations

1. Implement rate limiting on authentication endpoints (priority: high)
2. Add multi-factor authentication support (priority: medium)

### Assessment Metadata
- **Assessed by**: Shinsa Compliance Plugin v1.0.0
- **Date**: [ISO-8601 timestamp]
- **Confidence**: 0.85
- **Scope**: [repository path]
```

## Narrative Style Guide

### Tone
- Write in third person, past tense
- Be factual and objective — state what was observed, not opinions
- Use "was observed", "was found", "evidence indicates" language
- Avoid absolute certainty — use "appears to", "evidence suggests" for partial findings

### Structure
- Lead with the strongest evidence (positive or negative)
- Group evidence by sub-requirement
- Always include the specific file and line number
- Include brief code context (what the code does, not the raw snippet)

### Severity Language
- Critical: "Immediately exploitable", "Requires urgent remediation"
- High: "Significant gap", "Material weakness in control implementation"
- Medium: "Partial implementation", "Additional measures recommended"
- Low: "Minor improvement opportunity", "Enhancement recommended"
- Info: "Best practice consideration", "No compliance impact"

## Evidence Quality Checklist

Before finalizing evidence, verify:

- [ ] Every finding references a specific file and line number
- [ ] The control requirement is clearly stated
- [ ] Implementation status is justified with evidence
- [ ] Maturity score is explained with specific observations
- [ ] Gaps are clearly identified with remediation steps
- [ ] Assessment date and scope are recorded
- [ ] Confidence level reflects thoroughness of assessment
- [ ] No subjective language or unsupported claims
