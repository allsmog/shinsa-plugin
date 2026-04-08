---
name: NIST SP 800-53 Rev 5 Controls
description: >-
  This skill should be used when the user mentions "NIST 800-53", "NIST SP 800-53",
  "NIST controls", "federal compliance", "FedRAMP controls", "FISMA",
  "NIST security controls", "800-53 assessment", or needs to understand specific
  NIST SP 800-53 Rev 5 control requirements for code-level compliance assessment.
version: 1.0.0
---

# NIST SP 800-53 Rev 5 — Control Reference

## Purpose

Comprehensive reference for code-assessable NIST SP 800-53 Rev 5 controls. This skill provides control definitions, assessment criteria, and implementation guidance for the 53 controls that can be assessed from source code, configuration, and infrastructure-as-code.

## When to Use

- During NIST compliance scanning (`/shinsa:nist-scan`)
- When assessing specific NIST controls (`/shinsa:nist-quick-check`)
- When answering questions about NIST 800-53 requirements
- When mapping findings between NIST and other compliance frameworks

## Control Families

NIST SP 800-53 Rev 5 organizes controls into 20 families:

| Family | Name | Total Controls | Code-Assessable |
|--------|------|---------------|-----------------|
| AC | Access Control | 25 | ~10 (auto/hybrid) |
| AU | Audit and Accountability | 16 | ~10 (auto/hybrid) |
| AT | Awareness and Training | 6 | 0 (manual only) |
| CA | Assessment, Authorization, Monitoring | 9 | ~2 (hybrid) |
| CM | Configuration Management | 14 | ~6 (auto/hybrid) |
| CP | Contingency Planning | 13 | ~2 (hybrid) |
| IA | Identification and Authentication | 12 | ~6 (auto/hybrid) |
| IR | Incident Response | 10 | ~2 (hybrid) |
| MA | Maintenance | 7 | 0 (manual only) |
| MP | Media Protection | 8 | ~1 (auto) |
| PE | Physical and Environmental | 23 | 0 (manual only) |
| PL | Planning | 11 | 0 (manual only) |
| PM | Program Management | 32 | 0 (manual only) |
| PS | Personnel Security | 9 | 0 (manual only) |
| PT | PII Processing and Transparency | 8 | ~1 (hybrid) |
| RA | Risk Assessment | 10 | ~1 (hybrid) |
| SA | System and Services Acquisition | 23 | ~4 (auto/hybrid) |
| SC | System and Communications Protection | 51 | ~8 (auto/hybrid) |
| SI | System and Information Integrity | 23 | ~7 (auto/hybrid) |
| SR | Supply Chain Risk Management | 12 | 0 (manual only) |

## Assessment Domains

For code-level assessment, the 53 assessable controls are grouped into 6 domains:

### Domain 1: Access Control + Identification/Authentication (AC + IA)
16 controls — See `references/ac-ia-controls.md`

### Domain 2: Audit and Accountability (AU)
10 controls — See `references/au-controls.md`

### Domain 3: System and Communications Protection (SC)
8 controls — See `references/sc-controls.md`

### Domain 4: System and Information Integrity + Media Protection (SI + MP)
8 controls — See `references/si-mp-controls.md`

### Domain 5: Configuration Management + Risk Assessment (CM + RA)
7 controls — See `references/cm-ra-sa-controls.md`

### Domain 6: System Acquisition (SA)
4 controls — See `references/cm-ra-sa-controls.md`

## Assessment Modes

Each control is categorized by how it can be assessed:

- **auto**: Fully assessable from source code, configuration, IaC, CI/CD, dependencies, tests
- **hybrid**: Partially from code, but also requires manual evidence (policies, procedures, system configs)
- **manual**: Requires non-code evidence only (training records, physical security, personnel records)

For this plugin, we focus on `auto` and `hybrid` controls.

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
- **not_applicable**: Control does not apply to this system
- **not_assessed**: Control was not evaluated (out of scope for this assessment)

## NIST Baselines

NIST 800-53 defines three impact baselines. This plugin assesses all code-assessable controls regardless of baseline, but findings note which baseline they apply to:

- **Low**: Minimum controls for low-impact systems
- **Moderate**: Controls for moderate-impact systems (most common, FedRAMP Moderate)
- **High**: Full controls for high-impact systems

Most code-assessable controls are required at Moderate and High baselines.
