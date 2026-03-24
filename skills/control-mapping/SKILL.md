---
name: Control Mapping
description: >-
  This skill should be used when mapping ISO 27001 controls to other compliance
  frameworks (SOC 2, NIST 800-53, PCI DSS), when the user asks about "cross-standard
  mapping", "control mapping", "SOC 2 equivalent", "NIST mapping", "PCI DSS mapping",
  or when findings from one standard need to be translated to another framework.
version: 1.0.0
---

# Cross-Standard Control Mapping

## Purpose

Map ISO 27001 Annex A controls to equivalent or related controls in SOC 2 Type II, NIST SP 800-53, and PCI DSS v4.0. This enables organizations pursuing multiple certifications to reuse evidence and identify overlapping requirements.

## When to Use

- When a user needs to understand how ISO 27001 findings map to other standards
- When preparing for multiple compliance certifications
- When generating cross-standard compliance reports
- When the Pro tier (future) maps findings across frameworks

## Mapping Relationships

| Relationship | Meaning |
|-------------|---------|
| **equivalent** | Controls have nearly identical requirements — evidence from one satisfies the other |
| **partial** | Overlapping requirements but scope differs — additional evidence may be needed |
| **supporting** | One control enables or supports the other |

## Authentication & Access Control Mappings

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 | Relationship |
|-----------|-------|-------------|--------------|-------------|
| A.8.2 (Privileged access) | CC6.3 | AC-6 | 7.2 | equivalent |
| A.8.3 (Access restriction) | CC6.1 | AC-3 | 7.3 | equivalent |
| A.8.5 (Secure auth) | CC6.1-AUTH | IA-2, IA-5 | 8.3, 8.6 | equivalent |
| A.5.15 (Access control) | CC6.1 | AC-1, AC-2 | 7.1 | partial |
| A.5.16 (Identity mgmt) | CC6.1 | IA-1, IA-4 | 8.1 | partial |

## Cryptography Mappings

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 | Relationship |
|-----------|-------|-------------|--------------|-------------|
| A.8.24 (Cryptography) | CC6.1, CC6.7 | SC-13 | 3.5, 3.6 | equivalent |
| A.8.21 (Network services) | CC6.7 | SC-8 | 4.2 | partial |

## Data Protection Mappings

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 | Relationship |
|-----------|-------|-------------|--------------|-------------|
| A.8.10 (Deletion) | CC6.5 | MP-6, SI-12 | 3.7 | equivalent |
| A.8.11 (Data masking) | CC6.5 | SC-4 | 3.3, 3.4 | equivalent |
| A.8.12 (Leakage prevention) | CC7.2-DP | SC-7 | 6.2 | partial |
| A.5.14 (Information transfer) | CC6.7 | SC-8, SC-13 | 4.1, 4.2 | partial |
| A.5.34 (Privacy/PII) | P1.1 | SI-12 | 3.3 | partial |

## Logging & Monitoring Mappings

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 | Relationship |
|-----------|-------|-------------|--------------|-------------|
| A.8.15 (Logging) | CC7.1, CC7.2 | AU-2, AU-3 | 10.2 | equivalent |
| A.8.16 (Monitoring) | CC7.2, CC7.3 | AU-6 | 10.4 | partial |
| A.8.17 (Clock sync) | CC7.1 | AU-8 | 10.6 | equivalent |
| A.8.34 (Audit testing) | CC4.1 | CA-2, CA-7 | 11.3 | partial |

## Secure Development Mappings

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 | Relationship |
|-----------|-------|-------------|--------------|-------------|
| A.8.25 (Secure SDLC) | CC8.1 | SA-3, SA-15 | 6.2 | partial |
| A.8.28 (Secure coding) | CC8.1 | SA-11 | 6.2.4 | equivalent |
| A.8.31 (Env separation) | CC8.1 | CM-2 | 6.5.1 | partial |
| A.8.9 (Config mgmt) | CC8.1 | CM-2, CM-6 | 2.2 | partial |

## Using Mappings

### Single-Finding Multi-Standard Report

When a finding is identified against an ISO 27001 control, automatically reference the mapped controls:

```
**Finding**: Weak password hashing (SHA-256 for password storage)

**Affected Controls**:
- ISO 27001 A.8.5 — Secure Authentication
- SOC 2 CC6.1-AUTH — Logical and Physical Access Controls (equivalent)
- NIST 800-53 IA-5 — Authenticator Management (equivalent)
- PCI DSS v4.0 8.3 — Authentication Policies (equivalent)

This single finding creates a compliance gap across all 4 frameworks.
```

### Evidence Reuse

When evidence satisfies an ISO 27001 control with an `equivalent` mapping, that same evidence can be presented for the mapped standard's control with minimal adaptation.

### Gap Amplification

A gap in one control amplifies across mapped controls. If A.8.5 is `not_implemented`, the equivalent controls in SOC 2, NIST, and PCI DSS are also `not_implemented`. This makes cross-standard deduplication valuable — fix one gap, close multiple compliance items.

## Pro Tier Note

In the community edition, this mapping is informational. The Pro tier (via Shinsa API) provides:
- Automated cross-standard assessment (scan once, report across all 5 frameworks)
- 53 verified cross-standard mappings with relationship types
- Deduplication engine that consolidates findings across standards
- Multi-framework compliance reports
