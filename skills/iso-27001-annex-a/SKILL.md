---
name: ISO 27001 Annex A Controls
description: >-
  This skill should be used when the user mentions "ISO 27001", "Annex A controls",
  "information security controls", "ISMS controls", "compliance controls",
  "ISO 27001 assessment", or needs to understand specific ISO 27001:2022 control
  requirements for code-level compliance assessment.
version: 1.0.0
---

# ISO 27001:2022 Annex A — Control Reference

## Purpose

Comprehensive reference for all 93 ISO 27001:2022 Annex A controls, with focus on the technological controls (A.8) that are assessable from source code. This skill provides control definitions, assessment criteria, and implementation guidance for each control.

## When to Use

- During compliance scanning (`/shinsa:compliance-scan`)
- When assessing specific controls (`/shinsa:quick-check`)
- When answering questions about ISO 27001 requirements
- When mapping findings to compliance frameworks

## Orchestration Note

This skill is reference material, not the orchestrator. The command files own run planning, assessor dispatch, reviewer loops, and artifact persistence.

## Shipped Command Coverage

This skill is intentionally broader than the currently shipped ISO scan commands.

The shipped `/shinsa:compliance-scan` and `/shinsa:quick-check` commands currently produce standalone scored assessments for 13 core controls:
- A.8.2, A.8.3, A.8.5
- A.8.10, A.8.11, A.8.12, A.5.14
- A.8.15, A.8.16, A.8.17, A.8.34
- A.8.21, A.8.24

Additional controls in the reference files, including A.8.9, A.8.25, A.8.28, and A.8.31, remain useful as guidance and supporting context but are not currently emitted by the shipped commands as standalone scored results.

## Control Families

ISO 27001:2022 Annex A organizes 93 controls into 4 families:

| Family | Name | Controls | Code-Assessable |
|--------|------|----------|-----------------|
| A.5 | Organizational | 37 | ~5 (hybrid) |
| A.6 | People | 8 | 0 (manual only) |
| A.7 | Physical | 14 | 0 (manual only) |
| A.8 | Technological | 34 | ~20 (auto/hybrid) |

## Assessment Modes

Each control is categorized by how it can be assessed:

- **auto**: Fully assessable from source code, configuration, IaC, CI/CD, dependencies, tests
- **hybrid**: Partially from code, but also requires manual evidence (policies, procedures)
- **manual**: Requires non-code evidence only (training records, contracts, physical access logs)

For this plugin, we focus on `auto` and `hybrid` controls.

## Language-Specific References

Detailed control assessment criteria by control family:

- **Technological Controls (A.8)**: See `references/a8-technological-controls.md`
- **Organizational Controls (A.5)**: See `references/a5-organizational-controls.md`

## Assessment Methodology

### For Each Control

1. **Identify relevant code** — Use grep/glob patterns to find implementations
2. **Read and analyze** — Check if the implementation meets the control requirement
3. **Score maturity** (CMM 1-5):
   - **1 Initial**: No formal implementation, ad-hoc practices
   - **2 Managed**: Basic implementation exists but inconsistent
   - **3 Defined**: Consistent, documented approach
   - **4 Measured**: Implementation monitored with metrics
   - **5 Optimizing**: Continuously improved, automated verification
4. **Document evidence** — File path, line number, code snippet, assessment rationale
5. **Identify gaps** — What control requirements are not met
6. **Recommend remediation** — Specific, actionable steps to close gaps

### Status Determination

- **implemented**: Control requirements fully met with evidence
- **partially_implemented**: Some requirements met, gaps exist
- **not_implemented**: No evidence of control implementation
- **not_applicable**: Control does not apply (e.g., physical controls for SaaS)
- **not_assessed**: Control was not evaluated (out of scope for this assessment)
