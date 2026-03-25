# Shinsa (審査) — ISO 27001 Compliance Plugin for Claude Code

AI-first compliance assessment that scans your codebase against ISO 27001:2022 Annex A controls with evidence-backed findings tied to specific files and line numbers.

Unlike checkbox-based GRC tools, Shinsa actually reads your code and tells you *exactly* where your authentication middleware uses `==` instead of constant-time comparison — and which ISO 27001 control it violates.

## What You Get

- **12+ ISO 27001 Annex A controls** assessed from source code
- **4 specialized agents** (auth, crypto, data protection, logging)
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

# Check a specific control
/shinsa:quick-check A.8.5          # Secure authentication
/shinsa:quick-check A.8.24         # Cryptography
/shinsa:quick-check A.8.15         # Logging
/shinsa:quick-check A.8             # All technological controls
```

## Commands

| Command | Description |
|---------|-------------|
| `/shinsa:compliance-scan` | Full ISO 27001 Annex A assessment with all 4 agents |
| `/shinsa:quick-check <control>` | Fast check of a specific control or family |

### compliance-scan flags

| Flag | Effect |
|------|--------|
| `--controls A.8.5,A.8.24` | Assess specific controls only |
| `--family A.8` | Assess entire control family |
| `--severity high` | Only report findings at or above severity |
| `--format json\|md` | Output format (default: both) |
| `--resume` | Resume from previous incomplete assessment |

## Agents

| Agent | Domain | Controls |
|-------|--------|----------|
| **auth-assessor** | Authentication, authorization, access control | A.8.2, A.8.3, A.8.5 |
| **crypto-assessor** | Cryptography, TLS, key management | A.8.21, A.8.24 |
| **data-protection-assessor** | Data masking, leakage prevention, transfers | A.5.14, A.8.10, A.8.11, A.8.12 |
| **logging-assessor** | Logging, monitoring, clock sync, audit | A.8.15, A.8.16, A.8.17, A.8.34 |

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
| **Evidence Generation** | Audit-ready evidence narrative methodology |
| **Control Mapping** | Cross-standard mapping (ISO 27001 ↔ SOC 2 ↔ NIST 800-53 ↔ PCI DSS v4.0) |

## Output

### State file (`.claude/shinsa-state.json`)

Machine-readable assessment state with control statuses, maturity scores, finding counts, and agent completion tracking.

### Report (`.claude/compliance-report.md`)

Human-readable compliance report with:
- Executive summary
- Compliance overview (controls by status, average maturity)
- Critical and high findings with evidence
- All control assessments in table format
- Prioritized recommendations

## Controls Assessed

### Fully Code-Assessable (auto)

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

## Pro Mode

Shinsa community edition covers ISO 27001 Annex A (free, open source).

**Pro mode** (coming soon) adds:
- All 5 frameworks (ISO 27001, ISO 42001, SOC 2, NIST 800-53, PCI DSS v4.0)
- Cross-standard deduplication (53 mappings)
- All 14 assessment agents
- PDF/HTML audit-ready reports
- Multi-repo scanning
- SOA management
- Web dashboard

To configure Pro mode, create `.claude/shinsa.local.md`:

```yaml
---
shinsa_api_key: your-api-key-here
---
```

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
