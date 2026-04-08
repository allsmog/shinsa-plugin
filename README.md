# Shinsa (審査) — Compliance Assessment Plugin for Claude Code

AI-first compliance assessment that scans your codebase against ISO 27001:2022 Annex A and NIST SP 800-53 Rev 5 controls with evidence-backed findings tied to specific files and line numbers.

Unlike checkbox-based GRC tools, Shinsa actually reads your code and tells you *exactly* where your authentication middleware uses `==` instead of constant-time comparison — and which control it violates.

## What You Get

- **13 shipped ISO 27001 controls** and **53 shipped NIST SP 800-53 controls**
- **10 specialized agents** across ISO and NIST domains
- **Evidence-anchored findings** with file paths, line numbers, and code snippets
- **Maturity scoring** (CMM 1-5) per control
- **Cross-standard mapping** to SOC 2, NIST 800-53, and PCI DSS v4.0
- **Structured output** (JSON + Markdown reports)
- **Resume support** — long assessments pick up where they left off

## Installation

```bash
claude mcp add-plugin shinsa-plugin --path /path/to/shinsa-plugin
```

Or clone and add manually:

```bash
git clone https://github.com/allsmog/shinsa-plugin.git
```

Then add to your Claude Code settings:

```json
{
  "plugins": ["/path/to/shinsa-plugin"]
}
```

## Quick Start

```
# Full ISO 27001 compliance assessment
/shinsa:compliance-scan

# Full NIST SP 800-53 compliance assessment
/shinsa:nist-scan

# Check a specific ISO control
/shinsa:quick-check A.8.5          # Secure authentication
/shinsa:quick-check A.8.24         # Cryptography
/shinsa:quick-check A.8.15         # Logging
/shinsa:quick-check A.8            # All supported ISO scan controls

# Check a specific NIST control
/shinsa:nist-quick-check AC-3      # Access enforcement
/shinsa:nist-quick-check AU        # All NIST audit controls
```

## Commands

| Command | Description |
|---------|-------------|
| `/shinsa:compliance-scan` | Full ISO 27001 Annex A assessment with the 13 shipped ISO controls |
| `/shinsa:quick-check <control>` | Fast check of the supported ISO scan controls |
| `/shinsa:nist-scan` | Full NIST SP 800-53 Rev 5 assessment with 53 shipped controls |
| `/shinsa:nist-quick-check <control>` | Fast check of a specific NIST control or family |

### compliance-scan flags

| Flag | Effect |
|------|--------|
| `--controls A.8.5,A.8.24` | Assess specific controls only |
| `--family A.8` | Assess entire control family |
| `--severity high` | Only report findings at or above severity |
| `--format json\|md` | Output format (default: both) |
| `--resume` | Resume from previous incomplete assessment |

## Agents

### ISO 27001 Agents

| Agent | Domain | Controls |
|-------|--------|----------|
| **auth-assessor** | Authentication, authorization, access control | A.8.2, A.8.3, A.8.5 |
| **crypto-assessor** | Cryptography, TLS, key management | A.8.21, A.8.24 |
| **data-protection-assessor** | Data masking, leakage prevention, transfers | A.5.14, A.8.10, A.8.11, A.8.12 |
| **logging-assessor** | Logging, monitoring, clock sync, audit | A.8.15, A.8.16, A.8.17, A.8.34 |

### NIST SP 800-53 Agents

| Agent | Domain | Control Families |
|-------|--------|-----------------|
| **nist-access-control-assessor** | Access control & authentication | AC (10), IA (6) |
| **nist-audit-assessor** | Audit & accountability | AU (10) |
| **nist-sc-assessor** | System & communications protection | SC (8) |
| **nist-si-assessor** | System integrity & media protection | SI (7), MP (1) |
| **nist-cm-assessor** | Configuration management & risk assessment | CM (6), RA (1) |
| **nist-sa-assessor** | System acquisition & development | SA (4) |

Each agent searches your code for specific patterns, reads the relevant files, and produces structured assessments with:

- **Status**: implemented, partially_implemented, not_implemented, not_applicable
- **Maturity**: 1-5 (CMM: Initial → Optimizing)
- **Confidence**: 0-1
- **Evidence**: File path, line number, code snippet, assessment rationale
- **Findings**: Issues with severity (critical/high/medium/low/info) and recommendations

## Skills

| Skill | Description |
|-------|-------------|
| **ISO 27001 Annex A** | Complete control definitions for all 93 controls with assessment criteria |
| **NIST SP 800-53** | Control definitions and assessment criteria for all 53 shipped NIST controls |
| **Evidence Generation** | Audit-ready evidence narrative methodology |
| **Control Mapping** | Cross-standard mapping (ISO 27001 ↔ SOC 2 ↔ NIST 800-53 ↔ PCI DSS v4.0) |

## Output

### State file (`shinsa-output/shinsa-state.json`)

Machine-readable assessment state with control statuses, maturity scores, finding counts, and agent completion tracking.

### Report (`shinsa-output/compliance-report.md`)

Human-readable compliance report with:
- Executive summary
- Compliance overview (controls by status, average maturity)
- Critical and high findings with evidence
- All control assessments in table format
- Prioritized recommendations

## Controls Assessed

### ISO 27001 Full-Scan Controls

| Control | Name | Agent |
|---------|------|-------|
| A.8.2 | Privileged access rights | auth-assessor |
| A.8.3 | Information access restriction | auth-assessor |
| A.8.5 | Secure authentication | auth-assessor |
| A.8.10 | Information deletion | data-protection-assessor |
| A.8.11 | Data masking | data-protection-assessor |
| A.8.12 | Data leakage prevention | data-protection-assessor |
| A.8.15 | Logging | logging-assessor |
| A.8.16 | Monitoring activities | logging-assessor |
| A.8.17 | Clock synchronization | logging-assessor |
| A.8.21 | Security of network services | crypto-assessor |
| A.8.24 | Use of cryptography | crypto-assessor |
| A.8.34 | Protection during audit testing | logging-assessor |
| A.5.14 | Information transfer | data-protection-assessor |

### NIST SP 800-53 Full-Scan Coverage

Shinsa currently ships 53 NIST SP 800-53 Rev 5 controls across these domains:

- Access Control + Identification and Authentication: AC, IA
- Audit and Accountability: AU
- System and Communications Protection: SC
- System and Information Integrity + Media Protection: SI, MP
- Configuration Management + Risk Assessment: CM, RA
- System Acquisition: SA

### Cross-Standard Mapping

Each finding maps to equivalent controls in other frameworks:

| ISO 27001 | SOC 2 | NIST 800-53 | PCI DSS v4.0 |
|-----------|-------|-------------|--------------|
| A.8.5 | CC6.1-AUTH | IA-2, IA-5 | 8.3, 8.6 |
| A.8.24 | CC6.1, CC6.7 | SC-13 | 3.5, 3.6 |
| A.8.15 | CC7.1, CC7.2 | AU-2, AU-3 | 10.2 |
| A.8.12 | CC7.2-DP | SC-7 | 6.2 |

## Severity Levels

| Severity | Meaning | Example |
|----------|---------|---------|
| **Critical** | Immediately exploitable, breaks compliance | Plaintext passwords, hardcoded secrets |
| **High** | Significant gap in control implementation | Weak hashing (MD5), missing auth on endpoints |
| **Medium** | Partial implementation, additional measures needed | Missing MFA, incomplete CORS config |
| **Low** | Minor improvement opportunity | Suboptimal token lifetimes, verbose errors |
| **Info** | Best practice suggestion | Library upgrade recommendations |

## Current Coverage

Shinsa currently ships native, source-based assessments for:

- ISO 27001 Annex A
- NIST SP 800-53 Rev 5

The plugin also includes cross-standard mapping reference material for ISO 27001, SOC 2, NIST 800-53, and PCI DSS v4.0 so findings can be translated across frameworks when needed.

## E2E Verified

Tested against an intentionally insecure Node.js fixture app with hardcoded credentials, broken auth, plaintext logging, and MD5 crypto:

```
$ /shinsa:compliance-scan

shinsa-state.json    121 lines
compliance-report.md 309 lines

Controls assessed:  11
Implemented:         0 (0%)
Partially impl:      1 (9%)
Not implemented:    10 (91%)
Average maturity:    0.5 / 5

Findings: 26 total
  Critical: 7  (plaintext passwords, forgeable tokens, hardcoded secrets, MD5, secret leakage, stack traces)
  High:     9  (no rate limiting, no TLS, passwords in logs, PII unmasked, no RBAC)
  Medium:   6  (loose equality, no lockout, no session expiry, no input validation)
  Low:      4  (no structured logging, no monitoring, no log rotation)
```

Every finding includes `file:line` evidence (e.g., `src/auth.js:4`, `src/config.js:9`).

## Limitations

- This plugin assesses **code-level** compliance only. Organizational controls (A.5), people controls (A.6), and physical controls (A.7) require manual evidence.
- The assessment is **advisory** — it does not replace a formal ISO 27001 audit by an accredited certification body.
- Confidence scores reflect assessment thoroughness, not certainty. Low confidence findings should be manually reviewed.

## License

MIT
