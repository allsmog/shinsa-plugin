# Shinsa - Compliance Assessment Plugin

An AI-first compliance assessment plugin that scans codebases against ISO 27001 Annex A and NIST SP 800-53 Rev 5 controls with evidence-backed findings tied to specific files and line numbers.

## Project Structure

```
shinsa-plugin/
├── .claude-plugin/plugin.json  # Plugin manifest
├── AGENTS.md                   # This file
├── commands/                   # Slash commands
│   ├── compliance-scan.md      # /shinsa:compliance-scan — full ISO 27001 assessment
│   ├── quick-check.md          # /shinsa:quick-check — fast ISO control check
│   ├── nist-scan.md            # /shinsa:nist-scan — full NIST 800-53 assessment
│   └── nist-quick-check.md     # /shinsa:nist-quick-check — fast NIST control check
├── agents/                     # Specialized assessment agents
│   ├── auth-assessor.md        # ISO: Authentication & access control
│   ├── crypto-assessor.md      # ISO: Cryptography & key management
│   ├── data-protection-assessor.md  # ISO: Data protection & privacy
│   ├── logging-assessor.md     # ISO: Logging & monitoring
│   ├── nist-access-control-assessor.md  # NIST: AC + IA families
│   ├── nist-audit-assessor.md  # NIST: AU family
│   ├── nist-sc-assessor.md     # NIST: SC family
│   ├── nist-si-assessor.md     # NIST: SI + MP families
│   ├── nist-cm-assessor.md     # NIST: CM + RA families
│   └── nist-sa-assessor.md     # NIST: SA family
├── skills/                     # Compliance knowledge modules
│   ├── iso-27001-annex-a/      # ISO 27001 control knowledge
│   ├── nist-800-53/            # NIST 800-53 control knowledge
│   ├── evidence-generation/    # Audit evidence methodology
│   └── control-mapping/        # Cross-standard control mapping
├── hooks/                      # Event-driven automation
│   └── session-start.md        # Session initialization
└── references/                 # Shared schemas and resources
    └── assessment.schema.json  # Assessment output contract
```

## Key Commands

- `/shinsa:compliance-scan` — Full ISO 27001 compliance assessment (4 domains, 13 shipped controls)
- `/shinsa:quick-check` — Fast check of the supported ISO full-scan controls
- `/shinsa:nist-scan` — Full NIST SP 800-53 Rev 5 compliance assessment (6 domains, 53 shipped controls)
- `/shinsa:nist-quick-check` — Fast check of a specific NIST control or family

## Assessment Methodology

Follows ISO 27001:2022 Annex A or NIST SP 800-53 Rev 5 structure with Capability Maturity Model scoring:

1. **Scope** — Identify languages, frameworks, and architecture
2. **Assess** — Evaluate controls inline across assessment domains
3. **Evidence** — Anchor every finding to specific files and line numbers
4. **Report** — Structured output with maturity scores, gaps, and recommendations

## Agents

Each agent specializes in a compliance domain and assesses controls using Read, Glob, and Grep:

### ISO 27001 Agents

| Agent | Domain | Controls |
|-------|--------|----------|
| auth-assessor | Authentication & access control | A.8.2, A.8.3, A.8.5 |
| crypto-assessor | Cryptography | A.8.24, A.8.21 |
| data-protection-assessor | Data protection & privacy | A.8.10, A.8.11, A.8.12, A.5.14 |
| logging-assessor | Logging & monitoring | A.8.15, A.8.16, A.8.17, A.8.34 |

### NIST SP 800-53 Agents

| Agent | Domain | Control Families |
|-------|--------|-----------------|
| nist-access-control-assessor | Access control & authentication | AC (10), IA (6) |
| nist-audit-assessor | Audit & accountability | AU (10) |
| nist-sc-assessor | System & communications protection | SC (8) |
| nist-si-assessor | System integrity & media protection | SI (7), MP (1) |
| nist-cm-assessor | Configuration mgmt & risk assessment | CM (6), RA (1) |
| nist-sa-assessor | System acquisition & development | SA (4) |

## Assessment Output

All agents produce structured assessments with:
- **Control status**: implemented, partially_implemented, not_implemented, not_applicable
- **Maturity score**: 1-5 (CMM: Initial → Optimizing)
- **Confidence**: 0-1 (assessment certainty)
- **Evidence**: File path, line numbers, code snippets, assessment rationale
- **Severity**: critical, high, medium, low, info

## State Files

- `shinsa-output/shinsa-state.json` — Machine-readable assessment state
- `shinsa-output/compliance-report.md` — Human-readable compliance report
