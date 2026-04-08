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

## NIST 800-53 to ISO 27001 Reverse Mappings

### Access Control (AC) → ISO 27001

| NIST 800-53 | ISO 27001 | Relationship |
|-------------|-----------|-------------|
| AC-2 (Account mgmt) | A.5.16 (Identity mgmt) | partial |
| AC-3 (Access enforcement) | A.8.3 (Access restriction) | equivalent |
| AC-5 (Separation of duties) | A.5.3 (Segregation of duties) | equivalent |
| AC-6 (Least privilege) | A.8.2 (Privileged access) | equivalent |
| AC-7 (Failed logon) | A.8.5 (Secure auth) | partial |
| AC-11 (Session lock) | A.8.5 (Secure auth) | partial |
| AC-12 (Session termination) | A.8.5 (Secure auth) | partial |

### Identification and Authentication (IA) → ISO 27001

| NIST 800-53 | ISO 27001 | Relationship |
|-------------|-----------|-------------|
| IA-2 (Auth mechanisms) | A.8.5 (Secure auth) | equivalent |
| IA-4 (Identifier mgmt) | A.5.16 (Identity mgmt) | partial |
| IA-5 (Authenticator mgmt) | A.8.5 (Secure auth), A.5.17 (Auth info) | equivalent |
| IA-6 (Auth feedback) | A.8.5 (Secure auth) | partial |

### Audit and Accountability (AU) → ISO 27001

| NIST 800-53 | ISO 27001 | Relationship |
|-------------|-----------|-------------|
| AU-2 (Event logging) | A.8.15 (Logging) | equivalent |
| AU-3 (Audit record content) | A.8.15 (Logging) | equivalent |
| AU-6 (Review/analysis) | A.8.16 (Monitoring) | partial |
| AU-8 (Timestamps) | A.8.17 (Clock sync) | equivalent |
| AU-9 (Audit protection) | A.8.15 (Logging) | partial |

### System and Communications Protection (SC) → ISO 27001

| NIST 800-53 | ISO 27001 | Relationship |
|-------------|-----------|-------------|
| SC-4 (Shared resources) | A.8.11 (Data masking) | equivalent |
| SC-7 (Boundary protection) | A.8.12 (Leakage prevention) | partial |
| SC-8 (Transmission security) | A.8.21 (Network services), A.5.14 (Transfer) | equivalent |
| SC-12 (Key mgmt) | A.8.24 (Cryptography) | partial |
| SC-13 (Crypto protection) | A.8.24 (Cryptography) | equivalent |
| SC-23 (Session authenticity) | A.8.5 (Secure auth) | partial |
| SC-28 (Data at rest) | A.8.24 (Cryptography) | partial |

### System and Information Integrity (SI) → ISO 27001

| NIST 800-53 | ISO 27001 | Relationship |
|-------------|-----------|-------------|
| SI-2 (Flaw remediation) | A.8.8 (Vulnerability mgmt) | equivalent |
| SI-4 (System monitoring) | A.8.16 (Monitoring) | equivalent |
| SI-10 (Input validation) | A.8.12 (Leakage prevention), A.8.28 (Secure coding) | equivalent |
| SI-11 (Error handling) | A.8.12 (Leakage prevention) | partial |
| SI-12 (Info retention) | A.8.10 (Deletion) | equivalent |
| MP-6 (Media sanitization) | A.8.10 (Deletion) | equivalent |

### NIST Controls Without ISO 27001 Equivalent

The following NIST 800-53 controls have no direct ISO 27001 Annex A equivalent:

| NIST 800-53 | Notes |
|-------------|-------|
| AC-8 (System use notification) | No ISO equivalent — login banners/terms |
| AC-14 (Actions without auth) | No ISO equivalent — unauthenticated access inventory |
| AU-4 (Storage capacity) | No ISO equivalent — log storage sizing |
| AU-5 (Failure response) | No ISO equivalent — logging failure handling |
| AU-7 (Reduction/reporting) | No ISO equivalent — log query capability |
| AU-11 (Record retention) | Partial overlap with A.8.15 but distinct focus |
| AU-12 (Record generation) | Partial overlap with A.8.15 but distinct focus |
| CM-2 (Baseline config) | A.8.9 (Config mgmt) is partial overlap |
| CM-3 (Change control) | A.8.32 (Change mgmt) is manual-only in ISO |
| CM-5 (Change access) | No direct ISO equivalent |
| CM-7 (Least functionality) | No direct ISO equivalent |
| CM-8 (Component inventory) | A.5.9 (Asset inventory) is manual-only in ISO |
| RA-5 (Vuln scanning) | A.8.8 (Vulnerability mgmt) is partial overlap |
| SA-3 (SDLC) | A.8.25 (Secure SDLC) is partial overlap |
| SA-4 (Acquisition process) | No direct ISO equivalent for code-level |
| SA-15 (Dev standards) | No direct ISO equivalent for code-level |
