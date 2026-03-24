# Shinsa - Compliance Assessment Plugin

An AI-first compliance assessment plugin that scans codebases against ISO 27001 Annex A controls with evidence-backed findings tied to specific files and line numbers.

## Project Structure

```
shinsa-plugin/
├── .claude-plugin/plugin.json  # Plugin manifest
├── CLAUDE.md                   # This file
├── commands/                   # Slash commands
│   ├── compliance-scan.md      # /shinsa:compliance-scan — full guided assessment
│   └── quick-check.md          # /shinsa:quick-check — fast single-control check
├── agents/                     # Specialized assessment agents
│   ├── auth-assessor.md        # Authentication & access control
│   ├── crypto-assessor.md      # Cryptography & key management
│   ├── data-protection-assessor.md  # Data protection & privacy
│   └── logging-assessor.md     # Logging & monitoring
├── skills/                     # Compliance knowledge modules
│   ├── iso-27001-annex-a/      # ISO 27001 control knowledge
│   ├── evidence-generation/    # Audit evidence methodology
│   └── control-mapping/        # Cross-standard control mapping
├── hooks/                      # Event-driven automation
│   └── session-start.md        # Session initialization
└── references/                 # Shared schemas and resources
    └── assessment.schema.json  # Assessment output contract
```

## Key Commands

- `/shinsa:compliance-scan` — Full ISO 27001 compliance assessment with all 4 agents
- `/shinsa:quick-check` — Fast check of a specific control or control family

## Assessment Methodology

Follows ISO 27001:2022 Annex A structure with Capability Maturity Model scoring:

1. **Scope** — Identify languages, frameworks, and architecture
2. **Assess** — Run specialized agents against relevant controls
3. **Evidence** — Anchor every finding to specific files and line numbers
4. **Report** — Structured output with maturity scores, gaps, and recommendations

## Agents

Each agent specializes in a compliance domain and assesses controls using Read, Glob, and Grep:

| Agent | Domain | ISO 27001 Controls |
|-------|--------|-------------------|
| auth-assessor | Authentication & access control | A.8.2, A.8.3, A.8.5 |
| crypto-assessor | Cryptography | A.8.24, A.8.21 |
| data-protection-assessor | Data protection & privacy | A.8.10, A.8.11, A.8.12, A.5.14 |
| logging-assessor | Logging & monitoring | A.8.15, A.8.16, A.8.17, A.8.34 |

## Assessment Output

All agents produce structured assessments with:
- **Control status**: implemented, partially_implemented, not_implemented, not_applicable
- **Maturity score**: 1-5 (CMM: Initial → Optimizing)
- **Confidence**: 0-1 (assessment certainty)
- **Evidence**: File path, line numbers, code snippets, assessment rationale
- **Severity**: critical, high, medium, low, info

## State Files

- `.claude/shinsa-state.json` — Machine-readable assessment state
- `.claude/compliance-report.md` — Human-readable compliance report
