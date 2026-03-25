---
name: compliance-scan
description: Run a full ISO 27001 Annex A compliance assessment against the codebase with all 4 assessment agents
argument-hint: "[path] [--controls A.8.5,A.8.24] [--family A.8] [--severity critical,high] [--format json|md] [--output file] [--resume]"
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
  - Agent
  - TodoWrite
  - AskUserQuestion
---

# Compliance Scan

Run a full ISO 27001 Annex A compliance assessment with evidence-backed findings.

**Persistence rule**: Write artifacts to disk incrementally. Use the Write tool to save `shinsa-output/shinsa-state.json` after each agent completes (not only at the end). Write `shinsa-output/compliance-report.md` as the final step. This ensures partial runs still produce usable output.

## Flags

| Flag | Effect |
|------|--------|
| `--controls` | Assess specific controls only (comma-separated IDs, e.g., `A.8.5,A.8.24`) |
| `--family` | Assess an entire control family (`A.5`, `A.6`, `A.7`, or `A.8`) |
| `--severity` | Only report findings at or above severity (e.g., `--severity high`) |
| `--format` | Output format: `json` or `md` (default: both) |
| `--output` | Save report to a specific file path |
| `--resume` | Resume from a previous incomplete assessment |

## Step 1: Check for prior state

Check if a previous assessment exists:

```bash
ls shinsa-output/shinsa-state.json 2>/dev/null || true
```

If `--resume` is passed and state exists, load it and skip completed agents. Otherwise start fresh.

## Step 2: Scope the codebase

Identify the repository structure, languages, and frameworks:

1. **Language detection** — Check file extensions and package manifests:
   ```bash
   ls package.json pyproject.toml requirements.txt go.mod Cargo.toml pom.xml composer.json Gemfile 2>/dev/null || true
   ```

2. **Framework detection** — Identify web frameworks, ORMs, auth libraries:
   - Read the primary package manifest
   - Note frameworks that affect control assessment (e.g., Express implies Node.js auth patterns)

3. **Architecture detection** — Check for infrastructure-as-code, CI/CD, Docker:
   ```bash
   ls Dockerfile docker-compose.yml .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile terraform/*.tf k8s/*.yaml 2>/dev/null || true
   ```

4. **Size check** — Count source files:
   ```bash
   find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
   ```

Record the scope in a brief summary for agent context.

## Step 3: Determine applicable controls

Based on scope, determine which ISO 27001 Annex A controls are assessable from code:

**Always applicable** (technological controls assessable from source):
- A.8.2 (Privileged access rights)
- A.8.3 (Information access restriction)
- A.8.5 (Secure authentication)
- A.8.10 (Information deletion)
- A.8.11 (Data masking)
- A.8.12 (Data leakage prevention)
- A.8.15 (Logging)
- A.8.16 (Monitoring activities)
- A.8.21 (Security of network services)
- A.8.24 (Use of cryptography)
- A.8.28 (Secure coding)
- A.5.14 (Information transfer)

**Conditionally applicable** (based on detected infrastructure):
- A.8.9 (Configuration management) — if IaC detected
- A.8.25 (Secure development life cycle) — if CI/CD detected
- A.8.31 (Separation of environments) — if Docker/K8s detected

If `--controls` or `--family` is specified, filter to those only.

## Step 4: Assess controls and persist incrementally

**CRITICAL: Do NOT dispatch subagents for assessment. Perform the assessment INLINE to avoid subagent startup overhead. Assess each control domain in order, and IMMEDIATELY write the updated state file to `shinsa-output/shinsa-state.json` after each domain before proceeding to the next.**

**For each domain, do the assessment yourself (do not use the Agent tool):**

### Domain 1: Authentication & Access Control (A.8.2, A.8.3, A.8.5)
Search for auth implementations using Grep/Glob, read the relevant files, assess against the control requirements. Look for:
- Password hashing algorithms, session management, JWT handling
- Authorization middleware, RBAC, route protection
- Rate limiting, account lockout

**After assessing, IMMEDIATELY use Write tool to save `shinsa-output/shinsa-state.json` with auth results.**

### Domain 2: Cryptography (A.8.24, A.8.21)
Search for crypto usage, TLS config, key management. Look for:
- Algorithm choices, hardcoded keys, encryption modes
- TLS/SSL configuration, certificate validation

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with crypto results added.**

### Domain 3: Data Protection (A.8.10, A.8.11, A.8.12, A.5.14)
Search for data handling, masking, leakage prevention. Look for:
- PII in logs, error message sanitization, input validation
- Data deletion, masking in API responses, security headers

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with data protection results added.**

### Domain 4: Logging & Monitoring (A.8.15, A.8.16, A.8.17, A.8.34)
Search for logging config, monitoring, audit trails. Look for:
- Structured logging, security event coverage, sensitive data exclusion
- Health checks, metrics, timestamp handling

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with logging results added.**

## Step 5: Final state update

After all 4 domains are assessed, read `shinsa-output/shinsa-state.json` from disk, compute final summary, and write the completed state. The state file should already contain all control assessments from incremental writes — just update `completed_at` and the final summary totals.

**How to write**: Use `mkdir -p shinsa-output && cat > shinsa-output/shinsa-state.json << 'JSONEOF'` via Bash.

## Step 6: Generate report (from state file only)

**IMPORTANT: Generate the report by reading `shinsa-output/shinsa-state.json` from disk. Do NOT re-read or re-analyze the codebase.** The state file already contains all control assessments, findings, maturity scores, and evidence. Just format it as markdown.

Write human-readable report to `shinsa-output/compliance-report.md` using `cat > shinsa-output/compliance-report.md << 'REPORTEOF'` via Bash.

## State file schema

`shinsa-output/shinsa-state.json`:

```json
{
  "target": "<project-path>",
  "standard": "iso27001",
  "started_at": "<ISO-8601>",
  "last_updated": "<ISO-8601>",
  "completed_at": "<ISO-8601 or null>",
  "scope": {
    "languages": ["typescript"],
    "frameworks": ["express"],
    "infrastructure": ["docker", "github-actions"],
    "source_file_count": 150
  },
  "agents_completed": ["auth-assessor", "crypto-assessor", "data-protection-assessor", "logging-assessor"],
  "summary": {
    "controls_assessed": 12,
    "implemented": 8,
    "partially_implemented": 2,
    "not_implemented": 1,
    "not_applicable": 1,
    "compliance_percentage": 75,
    "average_maturity": 3.2,
    "findings": {
      "total": 5,
      "critical": 1,
      "high": 2,
      "medium": 1,
      "low": 1,
      "info": 0
    }
  },
  "controls": [
    {
      "controlId": "A.8.5",
      "status": "partially_implemented",
      "maturity": 3,
      "confidence": 0.85,
      "agent": "auth-assessor",
      "finding_count": 2
    }
  ]
}
```

## Step 7: Generate report

Write human-readable report to `shinsa-output/compliance-report.md`:

```markdown
# ISO 27001 Annex A Compliance Assessment

**Target**: <project-path>
**Date**: <ISO-8601>
**Standard**: ISO/IEC 27001:2022 Annex A

## Executive Summary

<2-3 sentences summarizing compliance posture>

## Compliance Overview

| Metric | Value |
|--------|-------|
| Controls Assessed | X |
| Implemented | X (Y%) |
| Partially Implemented | X (Y%) |
| Not Implemented | X (Y%) |
| Average Maturity | X.X / 5 |

## Critical & High Findings

### [FINDING-001] <title>
- **Control**: A.X.X — <control name>
- **Severity**: critical/high
- **Status**: not_implemented / partially_implemented
- **Evidence**:
  - `<file>:<line>` — <code snippet>
  - <assessment rationale>
- **Gap**: <what's missing>
- **Recommendation**: <how to fix>

## All Control Assessments

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| A.8.2 | Privileged access rights | implemented | 4/5 | 0 |
| A.8.5 | Secure authentication | partial | 3/5 | 2 |
| ... | ... | ... | ... | ... |

## Recommendations (Prioritized)

1. <Most critical recommendation>
2. <Next priority>
3. ...
```

## Step 8: Emit requested format

### `--format json`
Output the full assessment as structured JSON (all control assessments with findings and evidence).

### `--format md` (default)
Display the compliance report summary in the conversation. Reference `shinsa-output/compliance-report.md` for the full report.

## Notes

- Every finding MUST include file path, line numbers, and code snippet as evidence
- Confidence below 0.5 should be flagged as "low confidence — manual review recommended"
- Controls that cannot be assessed from code alone (A.5 organizational, A.6 people, A.7 physical) are marked `not_applicable` with a note explaining they require manual evidence
- The assessment is advisory — it does not replace a formal ISO 27001 audit
