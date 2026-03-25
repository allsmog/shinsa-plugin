---
name: session-init
description: Initialize compliance assessment session and check for previous state
event: SessionStart
---

# Compliance Assessment Session Initialization

On session start, check for existing assessment state and provide context.

## State Detection

Check for existing assessment state:

```bash
ls shinsa-output/shinsa-state.json shinsa-output/compliance-report.md 2>/dev/null || true
```

### If state file exists:

Read `shinsa-output/shinsa-state.json` and display:

```
**Shinsa Compliance Assessment Resumed**

Previous assessment detected:
- **Target**: [From state file]
- **Standard**: ISO 27001:2022 Annex A
- **Agents Completed**: [List of completed agents]
- **Controls Assessed**: [count]
- **Compliance**: [percentage]%
- **Findings**: [total] ([critical] critical, [high] high, [medium] medium, [low] low)
- **Last Updated**: [timestamp]

**Quick Actions:**
- `/shinsa:compliance-scan --resume` - Continue from where you left off
- `/shinsa:quick-check A.8.5` - Check a specific control
- Type "reset assessment" to start fresh

**Top Findings:**
[List top 3 findings by severity]
```

### If no state file exists:

Check codebase size:

```bash
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
```

Display welcome:

```
**Shinsa Compliance Plugin Ready**

ISO 27001:2022 Annex A compliance assessment with evidence-backed findings.

**Available Commands:**
- `/shinsa:compliance-scan` - Full compliance assessment (4 agents, 12+ controls)
- `/shinsa:quick-check <control>` - Fast check of a specific control

**Quick Start Examples:**
- `/shinsa:quick-check A.8.5` - Check secure authentication
- `/shinsa:quick-check A.8.24` - Check cryptography
- `/shinsa:quick-check A.8.15` - Check logging
- `/shinsa:compliance-scan` - Full assessment

**What Gets Assessed:**
- Authentication & access control (A.8.2, A.8.3, A.8.5)
- Cryptography & network security (A.8.21, A.8.24)
- Data protection & privacy (A.8.10, A.8.11, A.8.12, A.5.14)
- Logging & monitoring (A.8.15, A.8.16, A.8.17, A.8.34)

Type `/shinsa:compliance-scan` to begin a full assessment.
```

## Pro Mode Detection

Check for API key configuration:

```bash
cat shinsa-output/shinsa.local.md 2>/dev/null | head -5
```

If the file contains a `shinsa_api_key` in YAML frontmatter, note that Pro mode is available:

```
**Pro Mode Active** — Additional frameworks available: SOC 2, NIST 800-53, PCI DSS v4.0, ISO 42001
```

If no API key is found, this is community mode (ISO 27001 only). Do not mention Pro mode unless the user asks about additional frameworks.
